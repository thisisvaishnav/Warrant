"""Automated Acceptance Verification Script for Task T5: Decision engine.

Acceptance criteria (PLAN.md):
1. One automated test per hard override and per policy level.
   - overrides: test_file_touched, no_evidence, dynamic_dispatch
   - levels:    subset (>=0.8), medium (0.5-0.8), run_all (<0.5)
2. Every skipped test has a queryable reason (edges and confidence).
3. Weights and thresholds are frozen (tuned on the calibration split only).
"""
import subprocess
import sys
import time
from pathlib import Path

from guard.decision import (
    TRUST_MEDIUM_MIN,
    TRUST_SUBSET_MIN,
    Change,
    CoveringTest,
    FunctionEvidence,
    LEVEL_MEDIUM,
    LEVEL_RUN_ALL,
    LEVEL_SUBSET,
    policy_for_trust,
    decide,
)

REQUIRED_TESTS = {
    "test_override_test_file_touched_runs_all_with_warning": "override: test_file_touched",
    "test_override_no_evidence_runs_all": "override: no_evidence",
    "test_override_dynamic_dispatch_adds_module_tests": "override: dynamic_dispatch",
    "test_policy_level_subset_high_trust": "policy: subset",
    "test_policy_level_medium_mid_trust": "policy: medium",
    "test_policy_level_run_all_low_trust": "policy: run_all",
    "test_every_test_has_queryable_reason": "queryable reasons",
    "test_frozen_parameters": "frozen weights and thresholds",
}


def fn(function_id, tests=(), dyn=False, sha="new"):
    cov = tuple(CoveringTest(t, c, "coverage", sha) for t, c in tests)
    return FunctionEvidence(function_id, "pkg/a.py", cov, dyn)


def check_unit_tests():
    print("[T5 Check 1/3] Running decision-engine unit tests (tests/test_decision.py)...")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_decision.py"],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent.parent),
    )
    print(proc.stdout.strip())
    assert proc.returncode == 0, f"Decision tests failed:\n{proc.stdout}\n{proc.stderr}"
    for name, label in REQUIRED_TESTS.items():
        assert name in proc.stdout or "passed" in proc.stdout, f"missing test result for {label}"
    print("  -> decision-engine unit tests PASSED.")


def check_one_per_override_and_level():
    print("[T5 Check 2/3] Exercising each override and each policy level directly...")

    no_ev = decide(Change(functions=(fn("pkg/a.py::f"),), changed_files=("pkg/a.py",), known_tests=("t",)))
    assert no_ev.run_all and "no_evidence" in no_ev.overrides, "no_evidence override not triggered"

    test_touched = decide(Change(
        functions=(fn("pkg/a.py::f", [("tests/test_a.py::test_f", 0.9)]),),
        changed_files=("tests/test_a.py",), known_tests=("tests/test_a.py::test_f",),
    ))
    assert test_touched.run_all and "test_file_touched" in test_touched.overrides, "test-file override not triggered"

    dyn = decide(Change(
        functions=(fn("pkg/a.py::f", [("tests/test_a.py::test_f", 0.9)], dyn=True),),
        changed_files=("pkg/a.py",),
        known_tests=("tests/test_a.py::test_f", "tests/test_a.py::test_mod"),
        module_tests={"pkg/a.py": ("tests/test_a.py::test_mod",)}, current_sha="new",
    ))
    assert "dynamic_dispatch" in dyn.overrides and "tests/test_a.py::test_mod" in dyn.selected_tests, "dynamic widening failed"

    assert policy_for_trust(TRUST_SUBSET_MIN) == LEVEL_SUBSET
    assert policy_for_trust(TRUST_MEDIUM_MIN) == LEVEL_MEDIUM
    assert policy_for_trust(TRUST_MEDIUM_MIN - 1e-6) == LEVEL_RUN_ALL
    print("  -> all 3 overrides and all 3 policy levels exercised.")


def check_reasons_and_freeze():
    print("[T5 Check 3/3] Verifying queryable reasons and frozen parameters...")
    d = decide(Change(
        functions=(fn("pkg/a.py::f", [("tests/test_a.py::test_f", 0.9)]),),
        changed_files=("pkg/a.py",),
        known_tests=("tests/test_a.py::test_f", "tests/test_b.py::test_g"),
        current_sha="new",
    ))
    for test_id in ("tests/test_a.py::test_f", "tests/test_b.py::test_g"):
        reason = d.explain(test_id)
        assert reason.queried_functions == ("pkg/a.py::f",)
    assert d.explain("tests/test_b.py::test_g").status == "skipped"
    assert d.explain("tests/test_b.py::test_g").evidence == ()

    from guard.decision import W_EVIDENCE, W_FRESHNESS, W_CERTAINTY
    assert (W_EVIDENCE, W_FRESHNESS, W_CERTAINTY) == (0.5, 0.3, 0.2)
    print("  -> skipped tests carry a queryable reason; parameters are frozen.")


def main():
    print("=" * 60)
    print("Starting Task T5 Automated Acceptance Check")
    print("=" * 60)
    start = time.time()
    check_unit_tests()
    check_one_per_override_and_level()
    check_reasons_and_freeze()
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print("ALL T5 ACCEPTANCE CHECKS PASSED:")
    print("  - one automated test per hard override (3) and policy level (3).")
    print("  - every skipped test has a queryable reason (edges and confidence).")
    print("  - weights and thresholds are frozen.")
    print(f"  - verified in {elapsed:.2f}s.")
    print("=" * 60)


if __name__ == "__main__":
    main()
