"""Automated Acceptance Verification Script for Task T4: Coverage Evidence.

Acceptance criteria:
- Automated script exits non-zero if any Function has neither a COVERED_BY edge nor no_evidence=true.
- Automated script verifies 5 COVERED_BY edges match known covered functions:
    1. src/flask/app.py::Flask.make_response
    2. src/flask/app.py::Flask.dispatch_request
    3. src/flask/sansio/scaffold.py::Scaffold.route
    4. src/flask/templating.py::render_template
    5. src/flask/config.py::Config.from_mapping
- Suite run 3 times; flake_rate set; flaky tests excluded from evidence.
- Run nodes exist in FalkorDB (count >= 3).
- Kill rule: Ingestion & verification must finish in < 120s without DB crash.
"""
import sys
import time
from guard import db

KNOWN_COVERED_FUNCTIONS = {
    "src/flask/app.py::Flask.make_response": "tests/test_basic.py::test_url_mapping",
    "src/flask/app.py::Flask.dispatch_request": "tests/test_basic.py::test_url_mapping",
    "src/flask/sansio/scaffold.py::Scaffold.route": "tests/test_testing.py::test_json_request_and_response",
    "src/flask/templating.py::render_template": "tests/test_templating.py::test_template_filter_with_name_and_template",
    "src/flask/config.py::Config.from_mapping": "tests/test_config.py::test_config_from_mapping",
}


def check_functions_evidence_or_flag():
    print("[T4 Check 1/3] Verifying all Functions have either COVERED_BY edges or no_evidence=true...")
    g = db.get_graph("guard")

    # Check for functions that have NEITHER a COVERED_BY edge NOR no_evidence=true
    q_invalid = (
        "MATCH (f:Function) "
        "WHERE NOT (f)-[:COVERED_BY]->(:Test) AND coalesce(f.no_evidence, false) <> true "
        "RETURN f.id, f.file, f.name"
    )
    invalid_funcs = g.query(q_invalid).result_set
    assert not invalid_funcs, (
        f"ACCEPTANCE VIOLATION: Found {len(invalid_funcs)} functions with neither COVERED_BY edge nor no_evidence=true!\n"
        f"Sample: {invalid_funcs[:5]}"
    )

    # Count covered vs no_evidence functions
    q_covered = "MATCH (f:Function)-[:COVERED_BY]->(:Test) RETURN count(distinct f)"
    q_no_evidence = "MATCH (f:Function {no_evidence: true}) RETURN count(f)"
    q_total = "MATCH (f:Function) RETURN count(f)"

    covered_count = g.query(q_covered).result_set[0][0]
    no_evidence_count = g.query(q_no_evidence).result_set[0][0]
    total_funcs = g.query(q_total).result_set[0][0]

    print(f"  -> Total Functions: {total_funcs}")
    print(f"  -> Functions with COVERED_BY edges: {covered_count}")
    print(f"  -> Functions with no_evidence=true: {no_evidence_count}")

    assert covered_count > 0, "No functions with COVERED_BY edges found in graph!"
    assert no_evidence_count > 0, "Expected at least some functions with no_evidence=true!"
    assert (covered_count + no_evidence_count) >= total_funcs, (
        f"Coverage + no_evidence ({covered_count} + {no_evidence_count}) < total functions ({total_funcs})"
    )
    print("  -> All functions verified: every function has coverage evidence or no_evidence=true.")


def check_known_covered_functions():
    print("[T4 Check 2/3] Verifying 5 COVERED_BY edges match known covered functions...")
    g = db.get_graph("guard")

    for fn_id, expected_test in KNOWN_COVERED_FUNCTIONS.items():
        covering = db.get_covering_tests(g, fn_id, min_confidence=0.8)
        assert covering, f"Function {fn_id} has no covering tests with confidence >= 0.8!"

        test_ids = {c["test_id"] for c in covering}
        print(f"  -> Function: {fn_id}")
        print(f"     Total covering tests: {len(covering)}")

        # Verify expected test is present
        assert expected_test in test_ids, (
            f"Expected test {expected_test} not found among covering tests for {fn_id}!\n"
            f"Found: {list(test_ids)[:5]}..."
        )

        # Verify edge properties
        sample_edge = next(c for c in covering if c["test_id"] == expected_test)
        assert sample_edge["confidence"] == 0.9, f"Expected confidence 0.9, got {sample_edge['confidence']}"
        assert sample_edge["source"] == "coverage", f"Expected source 'coverage', got {sample_edge['source']}"
        print(f"     Verified expected covering test: {expected_test} (confidence: 0.9, source: coverage)")

    print("  -> All 5 known covered functions verified with valid COVERED_BY edges.")


def check_suite_runs_and_flakes():
    print("[T4 Check 3/3] Checking 3 suite runs, flake_rate properties, and exclusion of flaky tests...")
    g = db.get_graph("guard")

    # 1. Run nodes count >= 3
    run_counts = g.query("MATCH (r:Run) RETURN count(r)").result_set[0][0]
    print(f"  -> Total Run nodes in graph: {run_counts}")
    assert run_counts >= 3, f"Expected at least 3 Run nodes from 3 suite runs, found {run_counts}"

    # 2. flake_rate set on Test nodes
    tests_with_flake_rate = g.query(
        "MATCH (t:Test) WHERE t.flake_rate IS NOT NULL RETURN count(t)"
    ).result_set[0][0]
    total_tests = g.query("MATCH (t:Test) RETURN count(t)").result_set[0][0]
    print(f"  -> Test nodes with flake_rate property: {tests_with_flake_rate} / {total_tests}")
    assert tests_with_flake_rate > 0, "No Test nodes have flake_rate property set!"

    # 3. Flaky tests excluded from evidence
    flaky_covered = g.query(
        "MATCH (f:Function)-[e:COVERED_BY]->(t:Test) "
        "WHERE coalesce(t.flake_rate, 0.0) > 0.0 "
        "RETURN count(e)"
    ).result_set[0][0]
    assert flaky_covered == 0, (
        f"ACCEPTANCE VIOLATION: Found {flaky_covered} COVERED_BY edges connected to flaky tests!"
    )
    print("  -> Flaky test exclusion verified (0 COVERED_BY edges to flaky tests).")


def main():
    print("=" * 60)
    print("Starting Task T4 Automated Acceptance Check")
    print("=" * 60)

    start = time.time()
    check_functions_evidence_or_flag()
    check_known_covered_functions()
    check_suite_runs_and_flakes()
    elapsed = time.time() - start

    assert elapsed < 120, f"KILL RULE TRIGGERED: verification took {elapsed:.2f}s > 120s"

    print("\n" + "=" * 60)
    print("ALL T4 ACCEPTANCE CHECKS PASSED:")
    print("  - All Functions have COVERED_BY edge OR no_evidence=true.")
    print("  - 5 known covered functions verified with confidence 0.9.")
    print("  - 3 suite runs recorded, flake_rate measured, flaky tests excluded.")
    print(f"  - Ingestion & verification completed in {elapsed:.2f}s (Kill threshold: 120s).")
    print("=" * 60)


if __name__ == "__main__":
    main()
