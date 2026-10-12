#!/usr/bin/env bash
# fresh-test-reset.sh — wipe every trace of stray from this machine so the next
# onboarding run is a true first-time experience. No backups: this is a dev tool
# for testing signup/install flows, and everything it removes is re-creatable
# (`stray login`, `stray mcp install`, install.sh).
#
# Removes, when present:
#   ~/.stray/                      CLI login token, active org, local-proxy CA state
#   ~/.claude/skills/stray/        the agent skill install.sh drops into Claude Code
#   Claude Code MCP registration  `claude mcp remove stray` (user scope)
#   Codex MCP registration        `codex mcp remove stray`, if a codex CLI exists
#   the stray binary itself        uv tool / pipx / brew / pip, whichever answers
#
# Deliberately NOT touched: a repo checkout's .env (server-side platform keys,
# not user state) and ~/.local/bin on PATH generally.

set -uo pipefail

say()  { printf '  %-34s %s\n' "$1" "$2"; }

echo "stray fresh-test reset"

# ---- CLI state --------------------------------------------------------------
if [ -d "$HOME/.stray" ]; then
  rm -rf "$HOME/.stray" && say "~/.stray" "removed (login + proxy state)"
else
  say "~/.stray" "not present"
fi

# ---- agent skill ------------------------------------------------------------
if [ -d "$HOME/.claude/skills/stray" ]; then
  rm -rf "$HOME/.claude/skills/stray" && say "~/.claude/skills/stray" "removed"
else
  say "~/.claude/skills/stray" "not present"
fi

# ---- MCP registrations ------------------------------------------------------
if command -v claude >/dev/null 2>&1; then
  if claude mcp get stray >/dev/null 2>&1; then
    claude mcp remove stray >/dev/null 2>&1 && say "claude mcp (stray)" "removed"
  else
    say "claude mcp (stray)" "not registered"
  fi
else
  say "claude mcp (stray)" "claude CLI not found — skipped"
fi

if command -v codex >/dev/null 2>&1; then
  if codex mcp get stray >/dev/null 2>&1; then
    codex mcp remove stray >/dev/null 2>&1 && say "codex mcp (stray)" "removed"
  else
    say "codex mcp (stray)" "not registered"
  fi
fi

# ---- the binary -------------------------------------------------------------
# Try each installer that could own it; the package is named stray on
# PyPI but stray in Homebrew. Loop because more than one can be present at once.
removed_binary=""
if command -v uv >/dev/null 2>&1 && uv tool list 2>/dev/null | grep -q '^stray '; then
  uv tool uninstall stray >/dev/null 2>&1 && removed_binary="$removed_binary uv-tool"
fi
if command -v pipx >/dev/null 2>&1 && pipx list 2>/dev/null | grep -q 'stray'; then
  pipx uninstall stray >/dev/null 2>&1 && removed_binary="$removed_binary pipx"
fi
if command -v brew >/dev/null 2>&1 && brew list stray >/dev/null 2>&1; then
  brew uninstall stray >/dev/null 2>&1 && removed_binary="$removed_binary brew"
fi
if command -v stray >/dev/null 2>&1; then
  # Still resolvable → a plain `pip install` (or stray copy). Ask pip, then fall
  # back to deleting the executable pointed at, which is at worst a dangling shim.
  pip uninstall -y stray >/dev/null 2>&1 || pip3 uninstall -y stray >/dev/null 2>&1
  command -v stray >/dev/null 2>&1 && rm -f "$(command -v stray)"
  command -v stray >/dev/null 2>&1 || removed_binary="$removed_binary pip/stray"
fi
if [ -n "$removed_binary" ]; then
  say "stray binary" "removed (${removed_binary# })"
elif command -v stray >/dev/null 2>&1; then
  say "stray binary" "STILL PRESENT at $(command -v stray) — remove by hand"
else
  say "stray binary" "not installed"
fi

# ---- verdict ----------------------------------------------------------------
echo
leftover=0
[ -d "$HOME/.stray" ] && leftover=1
[ -d "$HOME/.claude/skills/stray" ] && leftover=1
command -v stray >/dev/null 2>&1 && leftover=1
if [ "$leftover" -eq 0 ]; then
  echo "clean — this machine now looks like a first-time user's."
else
  echo "⚠ some state survived (see above)."
  exit 1
fi
