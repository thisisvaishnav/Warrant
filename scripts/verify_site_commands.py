#!/usr/bin/env python3
"""Audit site-advertised CLI commands against the installed Guard CLI.

Ensures that documentation and marketing copy cannot advertise a CLI command
or flag that does not exist in the current release.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SITE_FILES = [
    REPO_ROOT / "landing" / "src" / "App.tsx",
    REPO_ROOT / "landing" / "src" / "data" / "agents.json",
]

# Guard known top-level subcommands from parser
VALID_SUBCOMMANDS = {
    "init",
    "doctor",
    "run",
    "check",
    "hook",
    "feedback",
    "ingest-static",
    "ingest-coverage",
    "callers",
    "stats",
    "covering-tests",
}


def extract_guard_commands() -> set[str]:
    commands: set[str] = set()

    for file_path in SITE_FILES:
        if not file_path.exists():
            continue
        text = file_path.read_text(encoding="utf-8")

        # Match shell invocations like: guard init, guard doctor, guard hook uninstall, etc.
        # e.g. in code blocks, strings, pre/code tags
        matches = re.findall(r"\bguard\s+([a-z\-]+)(?:\s+([a-z\-]+))?", text)
        for sub, sub2 in matches:
            if sub in VALID_SUBCOMMANDS:
                if sub == "hook" and sub2 in {"install", "uninstall", "stop", "session-start", "status"}:
                    commands.add(f"hook {sub2}")
                else:
                    commands.add(sub)

    return commands


def main() -> int:
    print("Auditing CLI commands advertised on the website...")
    commands = extract_guard_commands()
    print(f"Extracted subcommands to verify: {sorted(commands)}")

    failures: list[str] = []

    for cmd in sorted(commands):
        sub_args = cmd.split()
        full_cmd = ["guard", *sub_args, "--help"]
        try:
            res = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode != 0:
                failures.append(f"'guard {cmd}' failed with return code {res.returncode}: {res.stderr.strip()}")
            else:
                print(f"  ✓ 'guard {cmd} --help' passed")
        except Exception as e:
            failures.append(f"'guard {cmd}' raised error: {e}")

    if failures:
        print("\n[!] CLI Audit FAILED! The website advertises commands that do not exist:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("\n[✓] All advertised CLI commands verified successfully against release binary.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
