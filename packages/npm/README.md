# @apeiron-tech/stray

npm launcher for **stray** — call your team's APIs through one credential-injecting
proxy, with no keys on your machine.

```bash
npx @apeiron-tech/stray login
npx @apeiron-tech/stray tool ls
```

Or install globally:

```bash
npm install -g @apeiron-tech/stray
stray login
```

stray itself is a Python CLI; this package finds it on your machine and runs it,
installing it first (via `uv`, `pipx`, or `pip3`) if it's missing.

- Docs & interactive tutorial: https://treg.to/tutorial
- Source: https://github.com/apeiron-tech/stray
