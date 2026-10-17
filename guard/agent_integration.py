"""Agent integration and test execution runner (Task T7).

Provides `guard run`: an agent calls this command before declaring work complete.
- Calls `guard check` on proposed changes.
- If trust is low or changes are uncovered (fallback), forces a full test suite run.
- If trust is high, runs only the selected test subset.
- Blocks task completion if any test fails.
"""
from __future__ import annotations
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Any

from guard.thin_slice import guard_check

REPO_ROOT = Path("target_repos/flask").resolve()


def apply_patch(diff_file: Path, repo_path: Path | None = None) -> bool:
    """Applies patch to target repo."""
    target = repo_path or REPO_ROOT
    proc = subprocess.run(["git", "apply", str(diff_file)], cwd=str(target), capture_output=True, text=True)
    if proc.returncode != 0:
        patch_proc = subprocess.run(["patch", "-p1", "-i", str(diff_file)], cwd=str(target), capture_output=True)
        return patch_proc.returncode == 0
    return True


def reset_repo(repo_path: Path | None = None):
    """Restores target repo to clean state."""
    target = repo_path or REPO_ROOT
    subprocess.run(["git", "checkout", "--", "."], cwd=str(target), capture_output=True)
    subprocess.run(["git", "clean", "-fdx"], cwd=str(target), capture_output=True)


def count_collected_tests(test_targets: list[str], repo_path: Path | None = None) -> int:
    """Counts how many test items are collected for the targets."""
    target = repo_path or REPO_ROOT
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"] + test_targets
    proc = subprocess.run(cmd, cwd=str(target), capture_output=True, text=True)
    lines = proc.stdout.strip().splitlines()
    for line in reversed(lines):
        if "test" in line:
            parts = line.split()
            for p in parts:
                if p.isdigit():
                    return int(p)
    return len(test_targets)


def run_agent_guard(
    diff_file: str | Path | None = None,
    repo_path: str | Path | None = None,
    graph_name: str = "guard",
) -> tuple[dict[str, Any], int]:
    """Runs Guard check and executes tests according to trust level.
    
    Returns:
        (report_dict, exit_code)
    """
    repo = Path(repo_path).resolve() if repo_path else REPO_ROOT
    diff_path = Path(diff_file).resolve() if diff_file else None

    # 1. Run guard check
    check_res = guard_check(
        diff_file=diff_path,
        repo_path=repo,
        graph_name=graph_name,
    )

    forced_full = check_res.is_fallback or (check_res.status == "run-all")
    tests_to_run = ["tests"] if forced_full else check_res.selected_tests

    # 2. If a patch file was passed, apply it temporarily for test execution
    applied = False
    if diff_path and diff_path.exists():
        reset_repo()
        applied = apply_patch(diff_path)
        if not applied:
            return {
                "status": "error",
                "forced_full": True,
                "fallback_reason": "Failed to apply patch diff",
                "changed_functions": [],
                "tests_run": [],
                "tests_run_count": 0,
                "duration_s": 0.0,
                "tests_passed": False,
                "exit_code": 1,
                "output_summary": "Error: Failed to apply patch cleanly to target repo.",
            }, 1

    try:
        # Count collected tests
        test_count = count_collected_tests(tests_to_run)

        # 3. Execute pytest
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short"] + tests_to_run
        start = time.time()
        proc = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
        duration_s = time.time() - start

        passed = (proc.returncode == 0)
        report = {
            "status": check_res.status,
            "forced_full": forced_full,
            "fallback_reason": check_res.fallback_reason,
            "changed_functions": check_res.changed_functions,
            "tests_run": tests_to_run,
            "tests_run_count": test_count,
            "duration_s": round(duration_s, 3),
            "tests_passed": passed,
            "exit_code": proc.returncode,
            "output_summary": proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "",
        }
        return report, proc.returncode
    finally:
        if applied:
            reset_repo()
