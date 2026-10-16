#!/usr/bin/env bash
set -e

# scripts/verify_prep.sh
# Read-only verification preparation script for the independent verifier.

echo "================================================================================"
echo "1. GIT STATUS"
echo "================================================================================"
git status

echo ""
echo "================================================================================"
echo "2. GIT DIFF --STAT (against HEAD)"
echo "================================================================================"
git diff --stat HEAD

echo ""
echo "================================================================================"
echo "3. PROTECTED FILES CHECK"
echo "================================================================================"
python3 -c '
import subprocess
import os

protected_files = [
    "tests/test_static.py",
    "tests/verify_t1.py",
    "evals/split.json",
]

changed_protected = []

# Check diff vs HEAD for both staged and unstaged tracked files
res = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True)
modified = [l.strip() for l in res.stdout.splitlines() if l.strip()]

# Check untracked files
status_proc = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
untracked = [l[3:].strip() for l in status_proc.stdout.splitlines() if l.startswith("??")]

all_changed = set(modified + untracked)

for p in protected_files:
    if p in all_changed:
        changed_protected.append(p)

# Check CLAIM and DEFINITIONS section in PLAN.md
if "PLAN.md" in modified:
    try:
        def get_claim_defs(text):
            lines = text.splitlines()
            in_sec = False
            sec = []
            for line in lines:
                if "CLAIM (FROZEN" in line:
                    in_sec = True
                elif "METRICS AND PAIRED METRICS" in line:
                    in_sec = False
                if in_sec:
                    sec.append(line.rstrip())
            return sec

        head_text = subprocess.run(["git", "show", "HEAD:PLAN.md"], capture_output=True, text=True).stdout
        with open("PLAN.md", "r") as f:
            curr_text = f.read()

        if get_claim_defs(head_text) != get_claim_defs(curr_text):
            changed_protected.append("PLAN.md (CLAIM and DEFINITIONS section)")
    except Exception:
        pass

if changed_protected:
    print("PROTECTED files/sections changed:")
    for cp in changed_protected:
        print(f"  - {cp}")
else:
    print("PROTECTED files/sections changed: None (0 changed)")
'

echo ""
echo "================================================================================"
echo "4. PYTEST SUMMARY (with skipped / xfailed counts)"
echo "================================================================================"
# Locate pytest
if [ -x ".venv/bin/pytest" ]; then
    PYTEST_BIN=".venv/bin/pytest"
elif command -v pytest >/dev/null 2>&1; then
    PYTEST_BIN="pytest"
elif python3 -m pytest --version >/dev/null 2>&1; then
    PYTEST_BIN="python3 -m pytest"
else
    PYTEST_BIN="python -m pytest"
fi

# Run pytest strictly read-only: use isolated cache directory in /tmp
$PYTEST_BIN tests -o cache_dir=/tmp/.pytest_cache 2>&1 | python3 -c '
import sys, re

output = sys.stdin.read()
lines = [l for l in output.splitlines() if l.strip()]
summary_line = ""
for l in reversed(lines):
    if " in " in l and ("passed" in l or "failed" in l or "skipped" in l or "error" in l):
        summary_line = l
        break
if not summary_line and lines:
    summary_line = lines[-1]

def get_count(pat, text):
    m = re.search(r"(\d+)\s+" + pat, text)
    return int(m.group(1)) if m else 0

passed = get_count("passed", summary_line)
skipped = get_count("skipped", summary_line)
xfailed = get_count("xfailed", summary_line)
failed = get_count("failed", summary_line)
warnings = get_count("warning", summary_line)

print(f"Pytest summary line: {summary_line}")
print(f"Counts: skipped={skipped}, xfailed={xfailed}, passed={passed}, failed={failed}, warnings={warnings}")
'
