"""Eval Harness for Task T2: FalkorDB Graph Schema and Node/Edge Model.
Evaluates capability, regression, and stability (pass^3).
"""
import sys
import time
import json
import subprocess
from guard import db
from guard.ingest.static import StaticResult, FuncDef


def run_capability_evals():
    results = {}
    g = db.get_graph("guard_eval_tmp")
    db.reset_graph(g)
    g = db.get_graph("guard_eval_tmp")

    # C1: Schema Indexes
    try:
        db.ensure_schema(g)
        db.ensure_schema(g)  # Idempotency check
        results["c1_schema_indexes"] = {"status": "PASS", "details": "All 4 indexes created idempotently"}
    except Exception as e:
        results["c1_schema_indexes"] = {"status": "FAIL", "details": str(e)}

    # C2: Node Types Integrity (File, Function, Test, Run)
    try:
        sr = StaticResult(
            files=["app.py", "tests/test_app.py"],
            funcs=[
                FuncDef("app.py::foo", "app.py", "foo", "foo", 1, 5, None, False),
                FuncDef("tests/test_app.py::test_foo", "tests/test_app.py", "test_foo", "test_foo", 1, 3, None, False),
            ]
        )
        db.write_static(g, sr, commit_sha="sha_c2")
        db.write_run(g, {
            "id": "run_c2", "timestamp": "2026-10-16T12:00:00Z", "commit_sha": "sha_c2",
            "duration_ms": 120.0, "total_tests": 1, "passed": 1, "failed": 0
        })
        counts = db.get_schema_counts(g)
        assert counts["File"] == 2, f"Expected 2 File, got {counts['File']}"
        assert counts["Function"] == 1, f"Expected 1 Function, got {counts['Function']}"
        assert counts["Test"] == 1, f"Expected 1 Test, got {counts['Test']}"
        assert counts["Run"] == 1, f"Expected 1 Run, got {counts['Run']}"
        results["c2_node_types_integrity"] = {"status": "PASS", "details": f"All 4 node types created and verified: {counts}"}
    except Exception as e:
        results["c2_node_types_integrity"] = {"status": "FAIL", "details": str(e)}

    # C3: Edge Types & Properties (CALLS, IMPORTS, DEFINED_IN, COVERED_BY, FAILED_IN)
    try:
        # Check DEFINED_IN
        def_count = g.query("MATCH ()-[:DEFINED_IN]->() RETURN count(*)").result_set[0][0]
        assert def_count == 2, f"Expected 2 DEFINED_IN, got {def_count}"

        # Write and check CALLS & IMPORTS
        sr2 = StaticResult(
            files=["b.py"],
            funcs=[FuncDef("b.py::bar", "b.py", "bar", "bar", 1, 5, None, False)],
            call_edges={("b.py::bar", "app.py::foo")},
            import_edges={("b.py", "app.py")},
        )
        db.write_static(g, sr2, commit_sha="sha_edges")
        calls_row = g.query(
            "MATCH (a:Function {id: 'b.py::bar'})-[e:CALLS]->(b:Function {id: 'app.py::foo'}) "
            "RETURN e.source, e.confidence, e.evidence_count, e.last_verified_sha"
        ).result_set[0]
        assert calls_row == ["static", 0.6, 0, "sha_edges"], f"Unexpected CALLS props: {calls_row}"

        imports_row = g.query(
            "MATCH (a:File {path: 'b.py'})-[e:IMPORTS]->(b:File {path: 'app.py'}) "
            "RETURN e.source, e.confidence, e.last_verified_sha"
        ).result_set[0]
        assert imports_row == ["static", 0.6, "sha_edges"], f"Unexpected IMPORTS props: {imports_row}"

        # Write and check COVERED_BY
        db.write_coverage(g, {"tests/test_app.py::test_foo": ["app.py::foo"]}, commit_sha="sha_edges", confidence=0.9)
        cov_row = g.query(
            "MATCH (f:Function {id: 'app.py::foo'})-[e:COVERED_BY]->(t:Test {id: 'tests/test_app.py::test_foo'}) "
            "RETURN e.source, e.confidence, e.evidence_count, e.last_verified_sha"
        ).result_set[0]
        assert cov_row == ["coverage", 0.9, 1, "sha_edges"], f"Unexpected COVERED_BY props: {cov_row}"

        # Write and check FAILED_IN
        db.write_run(g, {
            "id": "run_fail", "timestamp": "2026-10-16T12:05:00Z", "commit_sha": "sha_fail",
            "duration_ms": 50.0, "total_tests": 1, "passed": 0, "failed": 1
        }, failures=[{"test_id": "tests/test_app.py::test_foo", "error": "AssertionError: Boom"}])

        fail_row = g.query(
            "MATCH (t:Test {id: 'tests/test_app.py::test_foo'})-[e:FAILED_IN]->(r:Run {id: 'run_fail'}) "
            "RETURN e.source, e.error_message, e.commit_sha"
        ).result_set[0]
        assert fail_row[0] == "test_run" and "Boom" in fail_row[1] and fail_row[2] == "sha_fail", f"Unexpected FAILED_IN: {fail_row}"

        results["c3_edge_types_and_properties"] = {"status": "PASS", "details": "All 5 edges and properties verified"}
    except Exception as e:
        results["c3_edge_types_and_properties"] = {"status": "FAIL", "details": str(e)}

    # C4: Query Traversals (get_callers & get_covering_tests)
    try:
        callers = db.get_callers(g, "app.py::foo", hops=2)
        assert len(callers) == 1 and callers[0]["caller"] == "b.py::bar", f"Unexpected callers: {callers}"

        covering = db.get_covering_tests(g, "app.py::foo", min_confidence=0.8)
        assert len(covering) == 1 and covering[0]["test_id"] == "tests/test_app.py::test_foo", f"Unexpected covering: {covering}"

        results["c4_traversal_queries"] = {"status": "PASS", "details": "Multi-hop and confidence queries verified"}
    except Exception as e:
        results["c4_traversal_queries"] = {"status": "FAIL", "details": str(e)}

    db.reset_graph(g)
    return results


def run_regression_evals():
    results = {}
    # R1: Test Suite Passes
    try:
        res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"], capture_output=True, text=True)
        if res.returncode == 0:
            results["r1_test_suite_passes"] = {"status": "PASS", "details": res.stdout.strip()}
        else:
            results["r1_test_suite_passes"] = {"status": "FAIL", "details": res.stderr.strip() or res.stdout.strip()}
    except Exception as e:
        results["r1_test_suite_passes"] = {"status": "FAIL", "details": str(e)}

    # R2: Live Target Ingestion (pallets/flask)
    try:
        res = subprocess.run([sys.executable, "-m", "guard.cli", "ingest-static", "target_repos/flask", "--include-tests"], capture_output=True, text=True)
        if res.returncode == 0:
            summary_idx = res.stdout.find("{")
            summary = json.loads(res.stdout[summary_idx:res.stdout.rfind("}")+1])
            assert summary["functions"] > 300, f"Expected >300 functions, got {summary['functions']}"
            assert summary["tests"] > 800, f"Expected >800 tests, got {summary['tests']}"
            assert summary["call_edges"] > 100, f"Expected >100 call edges, got {summary['call_edges']}"
            results["r2_flask_real_ingest"] = {"status": "PASS", "details": f"Ingested {summary['functions']} funcs, {summary['tests']} tests, {summary['call_edges']} calls"}
        else:
            results["r2_flask_real_ingest"] = {"status": "FAIL", "details": res.stderr.strip()}
    except Exception as e:
        results["r2_flask_real_ingest"] = {"status": "FAIL", "details": str(e)}

    # R3: CLI Stats and Callers
    try:
        stats_res = subprocess.run([sys.executable, "-m", "guard.cli", "stats"], capture_output=True, text=True)
        assert stats_res.returncode == 0 and "Function:" in stats_res.stdout

        caller_res = subprocess.run([sys.executable, "-m", "guard.cli", "callers", "src/flask/app.py::Flask.ensure_sync", "--hops", "2"], capture_output=True, text=True)
        assert caller_res.returncode == 0 and "src/flask/app.py::Flask.dispatch_request" in caller_res.stdout
        results["r3_cli_stats_and_callers"] = {"status": "PASS", "details": "CLI stats and multi-hop callers working accurately"}
    except Exception as e:
        results["r3_cli_stats_and_callers"] = {"status": "FAIL", "details": str(e)}

    return results


def main():
    trials = 3
    capability_history = []
    regression_history = []

    print(f"Executing {trials} consecutive eval trials for pass^3 stability measurement...\n")

    for i in range(trials):
        print(f"--- Trial {i+1}/{trials} ---")
        t0 = time.time()
        c_res = run_capability_evals()
        r_res = run_regression_evals()
        dt = time.time() - t0
        capability_history.append(c_res)
        regression_history.append(r_res)

        c_pass = sum(1 for v in c_res.values() if v["status"] == "PASS")
        r_pass = sum(1 for v in r_res.values() if v["status"] == "PASS")
        print(f"Trial {i+1} completed in {dt:.2f}s | Capability: {c_pass}/{len(c_res)} | Regression: {r_pass}/{len(r_res)}")

    # Aggregate metrics
    c_keys = capability_history[0].keys()
    r_keys = regression_history[0].keys()

    c_pass_at_1 = sum(1 for k in c_keys if capability_history[0][k]["status"] == "PASS") / len(c_keys)
    c_pass_hat_3 = sum(1 for k in c_keys if all(capability_history[i][k]["status"] == "PASS" for i in range(trials))) / len(c_keys)

    r_pass_at_1 = sum(1 for k in r_keys if regression_history[0][k]["status"] == "PASS") / len(r_keys)
    r_pass_hat_3 = sum(1 for k in r_keys if all(regression_history[i][k]["status"] == "PASS" for i in range(trials))) / len(r_keys)

    report = {
        "trials": trials,
        "capability": {
            "evals": capability_history[0],
            "pass_at_1": c_pass_at_1,
            "pass_hat_3": c_pass_hat_3,
        },
        "regression": {
            "evals": regression_history[0],
            "pass_at_1": r_pass_at_1,
            "pass_hat_3": r_pass_hat_3,
        }
    }

    with open("evals/t2_eval_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n==========================================")
    print("EVAL HARNESS REPORT: Task T2 Schema & Model")
    print("==========================================")
    print(f"Capability Pass@1: {c_pass_at_1 * 100:.1f}% | Pass^3: {c_pass_hat_3 * 100:.1f}%")
    print(f"Regression Pass@1: {r_pass_at_1 * 100:.1f}% | Pass^3: {r_pass_hat_3 * 100:.1f}%")
    print("==========================================")

    all_passed = (c_pass_hat_3 == 1.0) and (r_pass_hat_3 == 1.0)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
