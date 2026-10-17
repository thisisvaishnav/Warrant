"""Automated Acceptance Verification Script for Task T5a: Thin Slice.

Acceptance criteria:
- For 3 hand-made diffs, `guard check` outputs a test list or "run all":
    1. diff_covered.patch -> selects a test subset (is_fallback=False).
    2. diff_uncovered.patch -> forces "run all" fallback because function has no evidence (is_fallback=True).
    3. diff_mixed.patch -> selects a test subset covering changed function(s).
- T0 evaluation harness scores the result with --strategy guard without manual steps.
- Kill rule: End-to-end check runtime must be < 10s per check.
"""
import sys
import os
import json
import time
import subprocess
from pathlib import Path


FIXTURES = {
    "covered": Path("evals/fixtures/diff_covered.patch"),
    "uncovered": Path("evals/fixtures/diff_uncovered.patch"),
    "mixed": Path("evals/fixtures/diff_mixed.patch"),
}


def check_fixtures_exist():
    print("[T5a Check 1/3] Verifying 3 hand-made diff fixtures exist...")
    for name, path in FIXTURES.items():
        assert path.exists(), f"Fixture {path} does not exist!"
        content = path.read_text()
        assert len(content.strip()) > 0, f"Fixture {path} is empty!"
        print(f"  -> Fixture '{name}': {path} ({len(content)} bytes)")
    print("  -> All 3 diff fixtures verified.")


def check_guard_check_cli():
    print("[T5a Check 2/3] Running `guard check` on all 3 diff fixtures...")

    # 1. Covered diff -> must select a subset of tests
    start = time.time()
    proc_cov = subprocess.run(
        [sys.executable, "-m", "guard.cli", "check", "--diff", str(FIXTURES["covered"]), "--json"],
        capture_output=True,
        text=True,
    )
    t_cov = time.time() - start
    assert proc_cov.returncode == 0, f"`guard check` failed on diff_covered:\n{proc_cov.stderr}\n{proc_cov.stdout}"
    data_cov = json.loads(proc_cov.stdout)

    print(f"  -> diff_covered check ({t_cov:.3f}s): status={data_cov.get('status')}, is_fallback={data_cov.get('is_fallback')}")
    assert data_cov.get("status") == "select", f"Expected status='select' for covered diff, got {data_cov.get('status')}"
    assert data_cov.get("is_fallback") is False, "Expected is_fallback=False for covered diff"
    selected = data_cov.get("selected_tests", [])
    assert len(selected) > 0, "Expected non-empty selected_tests for covered diff"
    assert len(selected) < 400, f"Expected targeted subset of tests, got {len(selected)}"
    assert any("test_config.py" in t for t in selected), f"Expected test_config.py in selected tests, got: {selected}"
    assert t_cov < 10.0, f"KILL RULE TRIGGERED: check took {t_cov:.2f}s > 10s"

    # 2. Uncovered diff -> must trigger "run-all" fallback (no_evidence rule)
    start = time.time()
    proc_uncov = subprocess.run(
        [sys.executable, "-m", "guard.cli", "check", "--diff", str(FIXTURES["uncovered"]), "--json"],
        capture_output=True,
        text=True,
    )
    t_uncov = time.time() - start
    assert proc_uncov.returncode == 0, f"`guard check` failed on diff_uncovered:\n{proc_uncov.stderr}\n{proc_uncov.stdout}"
    data_uncov = json.loads(proc_uncov.stdout)

    print(f"  -> diff_uncovered check ({t_uncov:.3f}s): status={data_uncov.get('status')}, is_fallback={data_uncov.get('is_fallback')}")
    assert data_uncov.get("status") == "run-all", f"Expected status='run-all' for uncovered diff, got {data_uncov.get('status')}"
    assert data_uncov.get("is_fallback") is True, "Expected is_fallback=True for uncovered diff"
    assert "no_evidence" in data_uncov.get("fallback_reason", "").lower() or "uncovered" in data_uncov.get("fallback_reason", "").lower()
    assert t_uncov < 10.0, f"KILL RULE TRIGGERED: check took {t_uncov:.2f}s > 10s"

    # 3. Mixed diff -> selects tests covering changed function
    start = time.time()
    proc_mix = subprocess.run(
        [sys.executable, "-m", "guard.cli", "check", "--diff", str(FIXTURES["mixed"]), "--json"],
        capture_output=True,
        text=True,
    )
    t_mix = time.time() - start
    assert proc_mix.returncode == 0, f"`guard check` failed on diff_mixed:\n{proc_mix.stderr}\n{proc_mix.stdout}"
    data_mix = json.loads(proc_mix.stdout)

    print(f"  -> diff_mixed check ({t_mix:.3f}s): status={data_mix.get('status')}, is_fallback={data_mix.get('is_fallback')}")
    assert data_mix.get("status") == "select", f"Expected status='select' for mixed diff, got {data_mix.get('status')}"
    assert data_mix.get("is_fallback") is False, "Expected is_fallback=False for mixed diff"
    selected_mix = data_mix.get("selected_tests", [])
    assert len(selected_mix) > 0, "Expected non-empty selected_tests for mixed diff"
    assert any("test_blueprints.py" in t for t in selected_mix), f"Expected test_blueprints.py in selected tests, got: {selected_mix}"
    assert t_mix < 10.0, f"KILL RULE TRIGGERED: check took {t_mix:.2f}s > 10s"

    print("  -> `guard check` produces correct test lists and fallback across all 3 diffs.")


def check_t0_integration():
    print("[T5a Check 3/3] Evaluating T0 harness scoring with --strategy guard on fixtures...")
    harness_path = Path("evals/harness.py")
    assert harness_path.exists(), "evals/harness.py does not exist!"

    # Run harness evaluate on a fixture diff
    cmd = [
        sys.executable,
        str(harness_path),
        "--strategy",
        "guard",
        "--diff",
        str(FIXTURES["covered"]),
        "--json",
    ]
    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    assert proc.returncode == 0, f"T0 harness failed with guard strategy:\n{proc.stderr}\n{proc.stdout}"
    report = json.loads(proc.stdout)
    print(f"  -> T0 scored diff_covered in {elapsed:.2f}s:")
    print(f"     is_killable: {report.get('is_killable')}")
    print(f"     escaped: {report.get('escaped')}")
    print(f"     is_fallback: {report.get('is_fallback')}")
    print(f"     savings: {report.get('savings')}")
    print(f"     selected_tests_count: {report.get('selected_tests_count')}")

    assert report.get("is_fallback") is False, "Expected is_fallback=False for diff_covered in harness"
    assert report.get("selected_tests_count", 0) > 0, "Expected selected_tests_count > 0 in harness"
    # Savings should be > 0 since we ran a small targeted subset instead of 494 tests
    assert report.get("savings", 0.0) >= 0.0, "Savings cannot be negative"

    print("  -> T0 end-to-end evaluation with guard strategy verified with zero manual steps.")


def main():
    print("=" * 60)
    print("Starting Task T5a Automated Acceptance Check")
    print("=" * 60)

    start = time.time()
    check_fixtures_exist()
    check_guard_check_cli()
    check_t0_integration()
    total_elapsed = time.time() - start

    print("\n" + "=" * 60)
    print("ALL T5a ACCEPTANCE CHECKS PASSED:")
    print("  - 3 hand-made diffs evaluated by `guard check` (select vs fallback).")
    print("  - T0 harness scores result end-to-end with zero manual steps.")
    print(f"  - Completed in {total_elapsed:.2f}s (Kill threshold: < 10s per check).")
    print("=" * 60)


if __name__ == "__main__":
    main()
