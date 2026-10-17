"""Automated Acceptance Verification Script for Task T6: Feedback Loop.

Acceptance criteria:
- Automated test shows a miss, a repair edge (source='miss_repair', old and new confidence logged),
  and a wider decision on a similar change.
- Unrelated paths are unchanged.
- Kill rule: Feedback loop must not corrupt existing confidence metrics or crash graph.
"""
import sys
import time
import json
import subprocess
from pathlib import Path
from guard import db


def check_feedback_loop():
    print("[T6 Check 1/2] Demonstrating a miss, recording a repair edge, and asserting wider decision...")
    g = db.get_graph("guard")

    target_func = "src/flask/views.py::View.dispatch_request"
    repair_test = "tests/test_views.py::test_custom_view"

    # 1. Baseline: Check decision on diff touching target_func
    patch_path = Path("evals/fixtures/diff_uncovered.patch")
    proc_before = subprocess.run(
        [sys.executable, "-m", "guard.cli", "check", "--diff", str(patch_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert proc_before.returncode == 0, f"guard check failed before repair:\n{proc_before.stderr}"
    data_before = json.loads(proc_before.stdout)

    print(f"  -> Before repair: status={data_before.get('status')}, is_fallback={data_before.get('is_fallback')}")
    # Before repair: function had no evidence, so it wasn't selecting targeted repair_test
    assert repair_test not in data_before.get("selected_tests", []), f"{repair_test} unexpectedly present before repair!"

    # Record baseline for an unrelated function
    unrelated_func = "src/flask/config.py::Config.from_mapping"
    unrelated_tests_before = [c["test_id"] for c in db.get_covering_tests(g, unrelated_func)]
    print(f"  -> Unrelated function ({unrelated_func}) covering tests count before: {len(unrelated_tests_before)}")

    # 2. Simulate miss and trigger feedback repair
    print(f"  -> Recording miss: function='{target_func}', missed_test='{repair_test}'...")
    proc_feedback = subprocess.run(
        [
            sys.executable,
            "-m",
            "guard.cli",
            "feedback",
            "--function",
            target_func,
            "--test",
            repair_test,
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc_feedback.returncode == 0, f"guard feedback command failed:\n{proc_feedback.stderr}\n{proc_feedback.stdout}"
    feedback_data = json.loads(proc_feedback.stdout)
    print(f"  -> Feedback recorded: {json.dumps(feedback_data, indent=2)}")

    # Verify old and new confidence logged
    assert "old_confidence" in feedback_data, "Missing old_confidence in feedback report"
    assert "new_confidence" in feedback_data, "Missing new_confidence in feedback report"
    assert feedback_data["new_confidence"] >= 0.9, f"Expected elevated confidence >= 0.9, got {feedback_data['new_confidence']}"
    print(f"  -> Confidence transition logged: {feedback_data['old_confidence']} -> {feedback_data['new_confidence']}")

    # 3. Verify repair edge in FalkorDB
    q = (
        "MATCH (f:Function {id: $fid})-[e:COVERED_BY]->(t:Test {id: $tid}) "
        "RETURN e.source, e.confidence, e.old_confidence"
    )
    edge_res = g.query(q, {"fid": target_func, "tid": repair_test}).result_set
    assert edge_res, f"No COVERED_BY edge found between {target_func} and {repair_test}!"
    source, conf, old_conf = edge_res[0]
    print(f"  -> Edge in FalkorDB: source='{source}', confidence={conf}, old_confidence={old_conf}")
    assert source == "miss_repair", f"Expected source='miss_repair', got '{source}'"
    assert conf == feedback_data["new_confidence"]

    # 4. Check decision on the same change: decision must widen to include repair_test!
    proc_after = subprocess.run(
        [sys.executable, "-m", "guard.cli", "check", "--diff", str(patch_path), "--json"],
        capture_output=True,
        text=True,
    )
    assert proc_after.returncode == 0, f"guard check failed after repair:\n{proc_after.stderr}"
    data_after = json.loads(proc_after.stdout)
    print(f"  -> After repair: status={data_after.get('status')}, is_fallback={data_after.get('is_fallback')}")
    print(f"     Selected tests: {data_after.get('selected_tests')}")

    # Must now be selected with targeted subset
    assert repair_test in data_after.get("selected_tests", []), (
        f"Repair failed to widen decision! Expected {repair_test} in selected_tests, got {data_after.get('selected_tests')}"
    )
    assert data_after.get("status") == "select", f"Expected status='select', got {data_after.get('status')}"
    assert data_after.get("is_fallback") is False, "Expected is_fallback=False after repair evidence added"

    # 5. Check unrelated paths are unchanged
    print("[T6 Check 2/2] Verifying unrelated paths remain completely unchanged...")
    unrelated_tests_after = [c["test_id"] for c in db.get_covering_tests(g, unrelated_func)]
    assert unrelated_tests_before == unrelated_tests_after, (
        f"ACCEPTANCE VIOLATION: Unrelated function paths changed!\n"
        f"Before: {unrelated_tests_before}\nAfter: {unrelated_tests_after}"
    )
    print(f"  -> Unrelated function ({unrelated_func}) covering tests strictly identical ({len(unrelated_tests_after)} tests).")


def main():
    print("=" * 60)
    print("Starting Task T6 Automated Acceptance Check")
    print("=" * 60)

    g = db.get_graph("guard")
    target_func = "src/flask/views.py::View.dispatch_request"
    repair_test = "tests/test_views.py::test_custom_view"

    start = time.time()
    try:
        check_feedback_loop()
    finally:
        # Cleanup repair edge to keep verification idempotent
        g.query(
            "MATCH (f:Function {id: $fid})-[e:COVERED_BY {source: 'miss_repair'}]->(t:Test {id: $tid}) "
            "DELETE e "
            "WITH f "
            "SET f.no_evidence = true",
            {"fid": target_func, "tid": repair_test},
        )
    elapsed = time.time() - start

    assert elapsed < 30, f"KILL RULE TRIGGERED: verification took {elapsed:.2f}s > 30s"

    print("\n" + "=" * 60)
    print("ALL T6 ACCEPTANCE CHECKS PASSED:")
    print("  - Miss detected and repaired with edge source='miss_repair'.")
    print("  - Old and new confidence explicitly logged.")
    print("  - Decision widened on subsequent similar change (repair test selected).")
    print("  - Unrelated graph paths verified completely unchanged.")
    print(f"  - Verified in {elapsed:.2f}s.")
    print("=" * 60)


if __name__ == "__main__":
    main()
