# stray — onboarding

The bootstrap an agent (or human) follows to start calling shared tools and to share its own.
The CLI is a thin client over the API at `https://treg.to`; the API is the only brain.

## 1. Install the CLI

```bash
curl -fsSL https://treg.to/install.sh | sh   # installs `stray`, points it at the registry
```

(Working from a clone instead? `uv sync && uv run stray --help`.)

## 2. Sign in

Three doors, one identity (your email):

```bash
stray login                                  # GitHub OAuth (opens the browser)
stray login --email you@example.com          # email one-time code
stray login --token <TOKEN>                  # agents/CI: a per-org token from a team owner
```

Your token identifies you on every call (`X-Stray-Token`). New here? `stray onboard` walks you
through everything with a disposable demo team.

## 3a. Use a tool someone already shared (consumer)

```bash
stray tool ls                                 # what's available
stray call posthog query/events --query limit=5
stray run gh -- pr list                       # vendor CLIs work too
```

You hold **no upstream key** — the registry injects it server-side.

## 3b. Share your own (creator)

Point stray at a project — it finds the provider keys in the `.env`, the skill folders, and the
installed catalog CLIs, and registers what you pick:

```bash
stray scan          # read-only preview; nothing leaves the machine
stray upload        # register (encrypted server-side); idempotent, --replace to update
```

For one skill or a tricky tool (multi-credential, OAuth), see the manual flow in
[`USAGE.md`](../USAGE.md) — `stray skill init` / `skill add`, `stray tool add --bind`,
`stray oauth connect`.

## 4. Verify + observe

```bash
stray call <tool> <upstream-path>     # smoke-test
stray calls                           # audit: who called which tool, when, status
stray health                          # credential health across the org
```

## Notes

- Secrets are write-only; the API never returns a stored value.
- A tool can reference a secret another member uploaded (use-without-hold).
- Everything is org-scoped: `stray org ls` / `stray org use <slug>` picks the active team.
