"""Automated Acceptance Verification Script for Task T7: Agent Integration.

Acceptance criteria:
- An agent test run calls `guard run` (or hook);
- Low trust / uncovered change forces a full test suite run; agent cannot skip it.
- High trust change runs the selected test subset.
- Test failures block completion (non-zero exit code).
- Kill rule: Hook execution and decision must complete within 30s.
"""
import sys
import os
import json
import time
import subprocess
from pathlib import Path


def check_agent_runner_high_trust():
    print("[T7 Check 1/3] Verifying agent run on high-trust change selects subset...")
    covered_patch = Path("evals/fixtures/diff_passing_covered.patch").resolve()
    assert covered_patch.exists(), f"{covered_patch} not found!"

    # Run guard run with covered patch
    cmd = [
        sys.executable,
        "-m",
        "guard.cli",
        "run",
        "--diff",
        str(covered_patch),
        "--json",
    ]
    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    assert proc.returncode == 0, f"guard run failed on high trust patch:\n{proc.stderr}\n{proc.stdout}"
    data = json.loads(proc.stdout)
    print(f"  -> High-trust run ({elapsed:.2f}s): policy={data.get('status')}, forced_full={data.get('forced_full')}")
    print(f"     Ran {data.get('tests_run_count')} tests (Subset selection: {data.get('tests_run')})")

    assert data.get("forced_full") is False, "Expected forced_full=False on high trust change"
    assert data.get("status") == "select", "Expected status='select'"
    assert 0 < data.get("tests_run_count", 0) < 50, f"Expected small subset of tests, got {data.get('tests_run_count')}"
    print("  -> High-trust run successfully executed targeted subset.")


def check_agent_runner_low_trust_forces_full():
    print("[T7 Check 2/3] Verifying low-trust change forces full suite run (cannot skip)...")
    uncovered_patch = Path("evals/fixtures/diff_uncovered.patch").resolve()
    assert uncovered_patch.exists(), f"{uncovered_patch} not found!"

    # Run guard run with uncovered patch
    cmd = [
        sys.executable,
        "-m",
        "guard.cli",
        "run",
        "--diff",
        str(uncovered_patch),
        "--json",
    ]
    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    assert proc.returncode == 0, f"guard run failed on uncovered patch:\n{proc.stderr}\n{proc.stdout}"
    data = json.loads(proc.stdout)
    print(f"  -> Low-trust run ({elapsed:.2f}s): policy={data.get('status')}, forced_full={data.get('forced_full')}")
    print(f"     Reason: {data.get('fallback_reason')}")
    print(f"     Ran full suite ({data.get('tests_run_count')} tests)")

    assert data.get("forced_full") is True, "ACCEPTANCE VIOLATION: Low trust failed to force full run!"
    assert data.get("status") == "run-all", "Expected status='run-all'"
    assert data.get("tests_run_count", 0) >= 400, f"Expected full suite run (>= 400 tests), got {data.get('tests_run_count')}"
    print("  -> Low trust successfully forced full suite run; agent could not skip it.")


def check_agent_runner_blocks_on_failure():
    print("[T7 Check 3/3] Verifying test failure blocks agent with non-zero exit code...")
    failing_patch = Path("evals/fixtures/diff_covered.patch").resolve()
    assert failing_patch.exists(), f"{failing_patch} not found!"

    cmd = [
        sys.executable,
        "-m",
        "guard.cli",
        "run",
        "--diff",
        str(failing_patch),
        "--json",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    print(f"  -> Exit code on failure: {proc.returncode} (Expected non-zero)")
    assert proc.returncode != 0, f"Expected non-zero exit code on test failure, got {proc.returncode}"
    data = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    assert data.get("tests_passed") is False, "Expected tests_passed=False"
    assert data.get("exit_code") != 0, "Expected non-zero exit_code in report"
    print("  -> Failure correctly blocked agent run with non-zero exit code.")


def main():
    print("=" * 60)
    print("Starting Task T7 Automated Acceptance Check")
    print("=" * 60)

    start = time.time()
    check_agent_runner_high_trust()
    check_agent_runner_low_trust_forces_full()
    check_agent_runner_blocks_on_failure()
    elapsed = time.time() - start

    assert elapsed < 30, f"KILL RULE TRIGGERED: verification took {elapsed:.2f}s > 30s"

    print("\n" + "=" * 60)
    print("ALL T7 ACCEPTANCE CHECKS PASSED:")
    print("  - High trust change runs targeted test subset.")
    print("  - Low trust change forces full suite run (agent cannot skip).")
    print("  - Test failure blocks agent with non-zero exit code.")
    print(f"  - Completed in {elapsed:.2f}s.")
    print("=" * 60)


if __name__ == "__main__":
    main()
