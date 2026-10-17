"""Automated Acceptance Verification Script for Task T3: Static Graph Ingestion.

Acceptance criteria:
- 6 parser tests pass in `tests/test_static.py`.
- Dynamic-dispatch count is > 0 on target repo in FalkorDB.
- `guard callers <fn> --hops 4` matches expected callers for 5 predetermined functions:
    1. src/flask/app.py::Flask.make_response (includes finalize_request, wsgi_app, __call__)
    2. src/flask/app.py::Flask.ensure_sync (includes dispatch_request, handle_exception)
    3. src/flask/sansio/scaffold.py::Scaffold._method_route (includes get, post, delete)
    4. src/flask/sansio/blueprints.py::Blueprint.record_once (includes add_app_template_filter)
    5. src/flask/templating.py::_render (includes render_template, render_template_string)
- Kill rule: Parsing & ingest runtime must be < 60s without syntax crashes.
"""
import sys
import time
import subprocess
from guard import db


EXPECTED_CALLERS = {
    "src/flask/app.py::Flask.make_response": {
        "src/flask/app.py::Flask.finalize_request",
        "src/flask/app.py::Flask.wsgi_app",
        "src/flask/app.py::Flask.__call__",
    },
    "src/flask/app.py::Flask.ensure_sync": {
        "src/flask/app.py::Flask.dispatch_request",
        "src/flask/app.py::Flask.handle_exception",
    },
    "src/flask/sansio/scaffold.py::Scaffold._method_route": {
        "src/flask/sansio/scaffold.py::Scaffold.get",
        "src/flask/sansio/scaffold.py::Scaffold.post",
        "src/flask/sansio/scaffold.py::Scaffold.delete",
    },
    "src/flask/sansio/blueprints.py::Blueprint.record_once": {
        "src/flask/sansio/blueprints.py::Blueprint.add_app_template_filter",
        "src/flask/sansio/blueprints.py::Blueprint.after_app_request",
    },
    "src/flask/templating.py::_render": {
        "src/flask/templating.py::render_template",
        "src/flask/templating.py::render_template_string",
    },
}


def check_parser_tests():
    print("[T3 Check 1/3] Running parser unit tests (tests/test_static.py)...")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_static.py"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"Parser tests failed:\n{proc.stderr}\n{proc.stdout}"
    assert "6 passed" in proc.stdout, f"Expected 6 passed tests, got:\n{proc.stdout}"
    print(f"  -> All 6 static parser tests PASSED.")


def check_graph_counts_and_dynamic():
    print("[T3 Check 2/3] Checking ingested graph counts & dynamic-dispatch flag...")
    g = db.get_graph("guard")
    counts = db.get_schema_counts(g)
    
    print(f"  -> Nodes: Files={counts.get('File', 0)}, Functions={counts.get('Function', 0)}")
    print(f"  -> Edges: CALLS={counts.get('CALLS', 0)}, IMPORTS={counts.get('IMPORTS', 0)}, DEFINED_IN={counts.get('DEFINED_IN', 0)}")
    print(f"  -> Dynamic functions: {counts.get('dynamic_functions', 0)}")

    assert counts.get("File", 0) > 0, "No File nodes found in graph"
    assert counts.get("Function", 0) > 0, "No Function nodes found in graph"
    assert counts.get("CALLS", 0) > 0, "No CALLS edges found in graph"
    assert counts.get("dynamic_functions", 0) > 0, "KILL RULE/ACCEPTANCE VIOLATION: dynamic_functions count must be > 0"
    print("  -> Dynamic-dispatch count > 0 verified.")


def check_callers_for_sample_functions():
    print("[T3 Check 3/3] Asserting multi-hop callers for 5 predetermined functions...")
    g = db.get_graph("guard")

    for fn_id, expected_callers in EXPECTED_CALLERS.items():
        found = db.get_callers(g, fn_id, hops=4)
        found_callers = {c["caller"] for c in found}
        print(f"  -> Function: {fn_id}")
        print(f"     Found {len(found)} callers within 4 hops.")
        
        missing = expected_callers - found_callers
        assert not missing, f"Function {fn_id} is missing expected callers: {missing}\nFound: {found_callers}"
        print(f"     Verified expected callers present: {expected_callers}")

    print("  -> All 5 sample functions verified with multi-hop static callers.")


def main():
    print("=" * 60)
    print("Starting Task T3 Automated Acceptance Check")
    print("=" * 60)

    start = time.time()
    check_parser_tests()
    check_graph_counts_and_dynamic()
    check_callers_for_sample_functions()
    elapsed = time.time() - start

    assert elapsed < 60, f"KILL RULE TRIGGERED: verification took {elapsed:.2f}s > 60s"

    print("\n" + "=" * 60)
    print("ALL T3 ACCEPTANCE CHECKS PASSED:")
    print("  - 6 parser tests passed.")
    print("  - Dynamic-dispatch count > 0 in live FalkorDB.")
    print("  - Multi-hop callers verified for 5 sample functions.")
    print(f"  - Verified in {elapsed:.2f}s (Kill rule threshold: 60s).")
    print("=" * 60)


if __name__ == "__main__":
    main()
