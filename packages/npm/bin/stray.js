#!/usr/bin/env node
// @apeiron-tech/stray — npm launcher for the stray CLI (a Python tool).
// Finds an installed `stray`; if missing, installs it via the registry's
// installer (https://treg.to/install.sh), then execs it.
'use strict';

const { spawnSync } = require('node:child_process');
const { existsSync } = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const BASE = process.env.STRAY_BASE_URL || 'https://treg.to';
const args = process.argv.slice(2);

function findStray() {
  const probe = spawnSync(process.platform === 'win32' ? 'where' : 'which', ['stray'], {
    encoding: 'utf8',
  });
  if (probe.status === 0 && probe.stdout.trim()) return probe.stdout.trim().split('\n')[0];
  // common install location not always on npm's PATH
  const local = path.join(os.homedir(), '.local', 'bin', 'stray');
  if (existsSync(local)) return local;
  return null;
}

function run(bin) {
  const res = spawnSync(bin, args, { stdio: 'inherit' });
  process.exit(res.status === null ? 1 : res.status);
}

let bin = findStray();
if (bin) run(bin);

if (process.platform === 'win32') {
  console.error('stray is a Python CLI. Install it with:');
  console.error('  uv tool install git+https://github.com/apeiron-tech/stray.git');
  console.error('(get uv: https://docs.astral.sh/uv/getting-started/installation/)');
  process.exit(1);
}

console.error(`stray not found — installing from ${BASE} ...`);
const install = spawnSync('sh', ['-c', `curl -fsSL ${BASE}/install.sh | sh`], {
  stdio: 'inherit',
});
if (install.status !== 0) {
  console.error('\nAutomatic install failed. Install manually:');
  console.error(`  curl -fsSL ${BASE}/install.sh | sh`);
  process.exit(install.status === null ? 1 : install.status);
}

bin = findStray();
if (!bin) {
  console.error('\nInstalled, but `stray` is not on PATH. Add ~/.local/bin to your PATH and retry.');
  process.exit(1);
}
run(bin);
