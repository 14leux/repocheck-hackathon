#!/usr/bin/env python3
"""
RepoCheck hackathon -- tiny stdlib-only .env loader.

Why this exists: this harness's Bash/PowerShell tool spawns a fresh,
non-persistent shell for every command -- `export`/`$env:` set in one
tool call does not survive to the next (both tools' own docs say so
explicitly). Relying on real shell persistence would mean either a
persistent OS-level environment variable (`setx` + fully restarting
this session) or, worse, ever having a secret typed into a chat
message. Neither is necessary: each Python process can load its own
secret straight off disk at the moment it needs it, which sidesteps
shell persistence entirely -- the value lives in a git-ignored file,
never in a shell's environment and never in a chat transcript.

Deliberately not python-dotenv. This project is pure standard library
by design (see anthropic_provider.py's own docstring; DECISIONS.md),
and this loader's contract is small enough not to need a dependency
for it: one KEY=VALUE per line, `#` comments, blank lines ignored,
optional matching quotes stripped.

Real process environment variables always win -- os.environ.setdefault()
never overwrites a value already set some other way (a real `export`, a
CI secret, a value from `setx`), so this file is a fallback, not an
override.
"""

import os

DEFAULT_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

_loaded_paths = set()


def load_env_file(path=None):
    """
    Read `path` (default: .env next to this file) and set any KEY=VALUE
    pair into os.environ, without overwriting a variable that is already
    set. Does nothing if the file does not exist -- a missing .env is a
    normal, expected state (CI, or a real env var already set), never
    an error.

    Safe to call more than once per process, and from more than one
    module -- each provider calls this right before it reads its own
    secret, so no call site has to remember a separate "load the .env
    once at startup" step, and calling it twice is a cheap no-op.
    """
    target = path or DEFAULT_ENV_PATH
    if target in _loaded_paths:
        return
    _loaded_paths.add(target)

    if not os.path.isfile(target):
        return

    with open(target, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            if key and value:
                os.environ.setdefault(key, value)
