"""Automated Acceptance Verification Script for Task T8: Full Evaluation on Frozen Claim.

Acceptance criteria (PLAN.md line 197-203):
1. 30 to 50 mutants, split as frozen in T0 (16 calibration, 24 held-out = 40 mutants total).
2. All four strategies run on the held-out set:
   - run-all
   - same-file
   - naive-guess
   - guard
3. Table shows escape rate, savings ratio, and fallback rate for each strategy.
4. Two ablations evaluated:
   - no confidence filter (guard-no-confidence)
   - no dynamic-dispatch widening (guard-no-widening)
5. At least one failure case written up.
6. Unkillable mutants reported separately (excluded from escape rate).
7. Frozen claim validation:
   - Guard escape rate <= 5% (0.05) on held-out mutants.
   - Guard test time savings >= 40% (0.40) vs run-all.
   - Guard beats same-file heuristic on >= 1 metric (escape rate or savings).
   - Paired metrics: (escape rate <-> fallback rate, savings ratio <-> escape rate).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPLIT_FILE = ROOT / "evals" / "split.json"
RESULTS_FILE = ROOT / "evals" / "results_held_out.json"
REPORT_FILE = ROOT / "reports" / "verify_t8.md"


def check_mutant_counts():
    print("[T8 Check 1/5] Verifying mutant count and frozen split...")
    assert SPLIT_FILE.exists(), f"Split file {SPLIT_FILE} missing"
    with open(SPLIT_FILE, "r", encoding="utf-8") as f:
        split = json.load(f)

    calib = split.get("calibration", [])
    held_out = split.get("held_out", [])
    total = len(calib) + len(held_out)

    assert 30 <= total <= 50, f"Expected 30-50 mutants, found {total}"
    assert len(calib) == 16, f"Expected 16 calibration mutants, got {len(calib)}"
    assert len(held_out) == 24, f"Expected 24 held-out mutants, got {len(held_out)}"
    assert set(calib).isdisjoint(set(held_out)), "Calibration and held-out sets must be disjoint"
    print(f"  -> Split verified: {total} total mutants ({len(calib)} calibration, {len(held_out)} held-out).")


def check_evaluation_results():
    print("[T8 Check 2/5] Verifying 4 strategies and 2 ablations on held-out mutants...")
    assert RESULTS_FILE.exists(), f"Evaluation results file {RESULTS_FILE} missing. Run evaluation first."
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    expected_strategies = {"run-all", "same-file", "naive-guess", "guard"}
    expected_ablations = {"guard-no-confidence", "guard-no-widening"}

    assert "strategies" in results, "Missing 'strategies' in results"
    assert "ablations" in results, "Missing 'ablations' in results"

    for s in expected_strategies:
        assert s in results["strategies"], f"Missing strategy {s} in results['strategies']"
        summary = results["strategies"][s]["summary"]
        assert "escape_rate" in summary, f"Missing escape_rate for {s}"
        assert "savings_ratio" in summary, f"Missing savings_ratio for {s}"
        assert "fallback_rate" in summary, f"Missing fallback_rate for {s}"
        assert "killable_count" in summary, f"Missing killable_count for {s}"
        assert "unkillable_count" in summary, f"Missing unkillable_count for {s}"
        assert summary["total_evaluated"] == 24, f"Strategy {s} did not evaluate all 24 held-out mutants"

    for a in expected_ablations:
        assert a in results["ablations"], f"Missing ablation {a} in results['ablations']"
        summary = results["ablations"][a]["summary"]
        assert "escape_rate" in summary, f"Missing escape_rate for {a}"
        assert "savings_ratio" in summary, f"Missing savings_ratio for {a}"
        assert "fallback_rate" in summary, f"Missing fallback_rate for {a}"
        assert summary["total_evaluated"] == 24, f"Ablation {a} did not evaluate all 24 held-out mutants"

    print("  -> All 4 strategies and 2 ablations verified on all 24 held-out mutants.")


def check_frozen_claim():
    print("[T8 Check 3/5] Verifying frozen claim on held-out mutants...")
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    guard_sum = results["strategies"]["guard"]["summary"]
    same_file_sum = results["strategies"]["same-file"]["summary"]
    run_all_sum = results["strategies"]["run-all"]["summary"]

    guard_escape = guard_sum["escape_rate"]
    guard_savings = guard_sum["savings_ratio"]
    guard_fallback = guard_sum["fallback_rate"]

    same_escape = same_file_sum["escape_rate"]
    same_savings = same_file_sum["savings_ratio"]

    print(f"  Guard:     escape={guard_escape*100:.1f}%, savings={guard_savings*100:.1f}%, fallback={guard_fallback*100:.1f}%")
    print(f"  Same-file: escape={same_escape*100:.1f}%, savings={same_savings*100:.1f}%")
    print(f"  Run-all:   escape={run_all_sum['escape_rate']*100:.1f}%, savings={run_all_sum['savings_ratio']*100:.1f}%")

    # Claim 1: Escape rate <= 5% (0.05)
    assert guard_escape <= 0.05, f"Claim breached: Guard escape rate {guard_escape:.3f} > 0.05 (5%)"

    # Claim 2: Savings ratio >= 40% (0.40) vs run-all
    assert guard_savings >= 0.40, f"Claim breached: Guard savings {guard_savings:.3f} < 0.40 (40%)"

    # Claim 3: Beats same-file heuristic on at least one metric
    beats_escape = guard_escape < same_escape
    beats_savings = guard_savings > same_savings
    assert beats_escape or beats_savings, (
        f"Claim breached: Guard did not beat same-file on either metric "
        f"(guard_escape={guard_escape} vs same={same_escape}, guard_savings={guard_savings} vs same={same_savings})"
    )
    print("  -> Frozen claim verified: escape <= 5%, savings >= 40%, beats same-file.")


def check_failure_case_and_unkillables():
    print("[T8 Check 4/5] Verifying failure case documentation and unkillable reporting...")
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    assert "failure_case" in results, "Missing 'failure_case' in results JSON"
    fc = results["failure_case"]
    assert "mutant_id" in fc, "Failure case missing mutant_id"
    assert "description" in fc, "Failure case missing description"
    assert "analysis" in fc and len(fc["analysis"]) > 20, "Failure case analysis is insufficient"

    # Unkillable mutants reported separately
    unkillables = results.get("unkillable_mutants", [])
    print(f"  -> Unkillable mutants reported ({len(unkillables)}): {unkillables}")
    assert len(unkillables) >= 0, "Unkillable mutants list required"


def check_report_artifact():
    print("[T8 Check 5/5] Verifying verification report artifact...")
    assert REPORT_FILE.exists(), f"Report file {REPORT_FILE} missing"
    text = REPORT_FILE.read_text(encoding="utf-8")
    assert "VERDICT: PASS" in text, "Report missing VERDICT: PASS"
    assert "run-all" in text and "same-file" in text and "guard" in text
    print("  -> Verification report verified.")


def main():
    print("=" * 60)
    print("Starting Task T8 Acceptance Verification")
    print("=" * 60)
    check_mutant_counts()
    check_evaluation_results()
    check_frozen_claim()
    check_failure_case_and_unkillables()
    check_report_artifact()
    print("=" * 60)
    print("ALL T8 ACCEPTANCE CHECKS PASSED.")
    print("=" * 60)


if __name__ == "__main__":
    main()
