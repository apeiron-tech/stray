"""The per-agent skills-path registry + target resolution (`stray agents`, skill fan-out).

Pure logic over the registry - no DB, no network. Covers: the two-dir default fan-out, all-agents
targeting, global-scope resolution, install detection, and that env overrides (CLAUDE_CONFIG_DIR,
CODEX_HOME, XDG_CONFIG_HOME) are honored at call time.
"""
from __future__ import annotations

from pathlib import Path

from stray import agents as ag


def test_default_fanout_is_agents_plus_claude():
    bases = ag.resolve_targets()
    assert bases == [Path(".agents/skills"), Path(".claude/skills")]


def test_all_agents_dedupes_shared_bucket():
    dirs = ag.resolve_targets(all_agents=True)
    # every .agents/skills agent collapses to a single entry
    assert dirs.count(Path(".agents/skills")) == 1
    assert Path(".claude/skills") in dirs
    assert Path(".windsurf/skills") in dirs
    # far fewer distinct dirs than agents
    assert len(dirs) < len(ag.AGENTS)


def test_single_agent_global_scope(monkeypatch, tmp_path):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "cx"))
    assert ag.resolve_targets(agent="codex", scope_global=True) == [tmp_path / "cx" / "skills"]


def test_global_scope_uses_detected_or_falls_back(monkeypatch, tmp_path):
    # point every marker into an empty home so nothing is "installed"
    monkeypatch.setattr(ag, "HOME", tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / ".claude"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / ".config"))
    monkeypatch.delenv("CODEX_HOME", raising=False)
    assert ag.detect_installed() == []
    bases = ag.resolve_targets(scope_global=True)
    # fallback: claude global + the standard ~/.agents/skills
    assert (tmp_path / ".claude" / "skills") in bases
    assert (tmp_path / ag.STANDARD_PROJECT_DIR) in bases


def test_detect_installed_reads_markers(monkeypatch, tmp_path):
    monkeypatch.setattr(ag, "HOME", tmp_path)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / ".claude"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / ".config"))
    monkeypatch.delenv("CODEX_HOME", raising=False)
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".claude").mkdir()
    detected = ag.detect_installed()
    assert "cursor" in detected and "claude-code" in detected
    assert "codex" not in detected  # ~/.codex absent


def test_claude_config_dir_override(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "cc"))
    assert ag.global_dir("claude-code") == tmp_path / "cc" / "skills"


def test_skill_bootstrap_installs_every_advertised_skill(monkeypatch, tmp_path, capsys):
    """`stray skill bootstrap` (what install.sh runs) drops the stray skill AND every other skill the
    registry's well-known index advertises, and never turns a hostile name into a path."""
    from types import SimpleNamespace

    from stray import cli

    pages = {
        "/skill.md": "---\nname: stray\n---\n",
        "/.well-known/skills/index.json": {"skills": [{"name": "stray"}, {"name": "lead-signals"}, {"name": "../evil"}]},
        "/.well-known/skills/lead-signals/SKILL.md": "---\nname: lead-signals\n---\n",
    }

    def fake_get(url, **_):
        body = pages.get(url.removeprefix("https://reg.example"), "")
        return SimpleNamespace(status_code=200 if body else 404, text=body if isinstance(body, str) else "",
                               json=lambda: body, raise_for_status=lambda: None)

    monkeypatch.setattr(cli.httpx, "get", fake_get)
    monkeypatch.setattr(ag, "resolve_targets", lambda **_: [tmp_path / "skills"])
    monkeypatch.delenv("STRAY_TOKEN", raising=False)
    cli.cmd_skill_bootstrap(SimpleNamespace(project=False, all_agents=False), {"base_url": "https://reg.example"})
    installed = sorted(p.parent.name for p in (tmp_path / "skills").glob("*/SKILL.md"))
    assert installed == ["lead-signals", "stray"]
    assert not (tmp_path / "evil").exists()


def test_skill_bootstrap_retires_the_folders_the_skill_used_to_install_as(monkeypatch, tmp_path):
    """The skill was `tools-registry`, then `treg`. A leftover copy would load beside `stray` as a
    duplicate, so a folder holding only our SKILL.md is removed; one with anything else in it is not."""
    from types import SimpleNamespace

    from stray import cli

    skills = tmp_path / "skills"
    for old in ("treg", "tools-registry"):
        (skills / old).mkdir(parents=True)
        (skills / old / "SKILL.md").write_text("old")
    (skills / "treg" / "notes.md").write_text("somebody's own file")   # not exactly ours: keep it
    pages = {"/skill.md": "---\nname: stray\n---\n", "/.well-known/skills/index.json": {"skills": []}}

    def fake_get(url, **_):
        body = pages.get(url.removeprefix("https://reg.example"), "")
        return SimpleNamespace(status_code=200 if body else 404, text=body if isinstance(body, str) else "",
                               json=lambda: body, raise_for_status=lambda: None)

    monkeypatch.setattr(cli.httpx, "get", fake_get)
    monkeypatch.setattr(ag, "resolve_targets", lambda **_: [skills])
    monkeypatch.delenv("STRAY_TOKEN", raising=False)
    cli.cmd_skill_bootstrap(SimpleNamespace(project=False, all_agents=False), {"base_url": "https://reg.example"})
    assert (skills / "stray" / "SKILL.md").is_file()
    assert not (skills / "tools-registry").exists()
    assert (skills / "treg" / "notes.md").exists()
