"""Automated Spike Verification for S1: Per-Test Coverage on Target Repo.

Acceptance criteria:
- On 20 tests, `pytest --cov=flask --cov-context=test` finishes.
- Data successfully maps each test to executed functions in Flask.
- Slowdown versus plain run is recorded as a number.
- Kill rule: If slowdown > 3.0x or context tracking fails, trigger fallback to per-file.
- Output records choice (per-test vs per-file).
"""
import sys
import time
import os
import sqlite3
import subprocess
import ast
from pathlib import Path


SAMPLE_TESTS = [
    "target_repos/flask/tests/test_basic.py::test_options_work",
    "target_repos/flask/tests/test_basic.py::test_options_on_multiple_rules",
    "target_repos/flask/tests/test_basic.py::test_method_route[get]",
    "target_repos/flask/tests/test_basic.py::test_method_route[query]",
    "target_repos/flask/tests/test_basic.py::test_method_route[post]",
    "target_repos/flask/tests/test_basic.py::test_method_route[put]",
    "target_repos/flask/tests/test_basic.py::test_method_route[delete]",
    "target_repos/flask/tests/test_basic.py::test_method_route[patch]",
    "target_repos/flask/tests/test_basic.py::test_method_route_no_methods",
    "target_repos/flask/tests/test_basic.py::test_provide_automatic_options_attr_disable",
    "target_repos/flask/tests/test_basic.py::test_provide_automatic_options_attr_enable",
    "target_repos/flask/tests/test_basic.py::test_provide_automatic_options_arg_disable",
    "target_repos/flask/tests/test_basic.py::test_provide_automatic_options_method_disable",
    "target_repos/flask/tests/test_basic.py::test_request_dispatching",
    "target_repos/flask/tests/test_basic.py::test_disallow_string_for_allowed_methods",
    "target_repos/flask/tests/test_basic.py::test_url_mapping",
    "target_repos/flask/tests/test_basic.py::test_werkzeug_routing",
    "target_repos/flask/tests/test_basic.py::test_endpoint_decorator",
    "target_repos/flask/tests/test_basic.py::test_session_accessed",
    "target_repos/flask/tests/test_basic.py::test_session_path",
]


def build_function_line_map(repo_src: Path):
    """Maps (file_path, line_number) -> function_qualname using AST."""
    func_map = {}
    for py_file in repo_src.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except Exception:
            continue
        rel_path = str(py_file.resolve())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = node.lineno
                end = getattr(node, "end_lineno", start)
                for line in range(start, end + 1):
                    func_map[(rel_path, line)] = f"{py_file.name}::{node.name}"
    return func_map


def run_plain_suite():
    print("[S1] Running 20 tests without coverage...")
    start = time.time()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"] + SAMPLE_TESTS,
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - start
    assert proc.returncode == 0, f"Plain run failed:\n{proc.stderr}\n{proc.stdout}"
    print(f"  -> Plain run finished in {elapsed:.3f}s")
    return elapsed


def run_coverage_suite():
    print("[S1] Running 20 tests WITH --cov=flask --cov-context=test...")
    cov_file = Path(".coverage")
    if cov_file.exists():
        cov_file.unlink()

    start = time.time()
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--cov=flask",
        "--cov-context=test",
    ] + SAMPLE_TESTS
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    assert proc.returncode == 0, f"Coverage run failed:\n{proc.stderr}\n{proc.stdout}"
    print(f"  -> Coverage run finished in {elapsed:.3f}s")
    return elapsed


def inspect_coverage_mapping():
    import coverage
    cov_file = Path(".coverage")
    assert cov_file.exists(), ".coverage file was not generated!"

    cov = coverage.CoverageData(str(cov_file))
    cov.read()

    flask_src = Path("target_repos/flask/src/flask").resolve()
    ast_map = build_function_line_map(flask_src)

    test_to_funcs = {}
    total_test_contexts = set()

    for filepath_str in cov.measured_files():
        filepath = Path(filepath_str).resolve()
        # Only inspect flask source files
        if not str(filepath).startswith(str(flask_src)):
            continue

        contexts_by_line = cov.contexts_by_lineno(str(filepath))
        for lineno, ctx_list in contexts_by_line.items():
            func_name = ast_map.get((str(filepath), lineno))
            for ctx in ctx_list:
                if not ctx or "|" not in ctx:
                    continue
                test_id = ctx.split("|")[0]
                total_test_contexts.add(test_id)
                if func_name:
                    test_to_funcs.setdefault(test_id, set()).add(func_name)

    print(f"[S1] Found {len(total_test_contexts)} distinct test contexts covering Flask code.")
    print(f"[S1] Successfully mapped {len(test_to_funcs)} test contexts to specific Flask functions.")
    assert len(test_to_funcs) >= 20, f"Expected at least 20 test mappings, got {len(test_to_funcs)}"

    return test_to_funcs


def main():
    print("=" * 60)
    print("Starting S1 Spike: Per-Test Coverage Assessment")
    print("=" * 60)

    # 1. Plain run
    t_plain = run_plain_suite()

    # 2. Coverage run
    t_cov = run_coverage_suite()

    # 3. Slowdown calculation
    slowdown = t_cov / t_plain if t_plain > 0 else 1.0
    print(f"[S1] Slowdown factor: {slowdown:.2f}x (Plain: {t_plain:.3f}s, Cov: {t_cov:.3f}s)")

    # 4. Inspect test -> function mapping
    mapping = inspect_coverage_mapping()

    # 5. Print sample mappings
    print("\n[S1] Sample test -> function coverage mappings:")
    for i, (test_ctx, funcs) in enumerate(list(mapping.items())[:5]):
        sample_funcs = list(sorted(funcs))[:4]
        print(f"  Test {i+1}: {test_ctx}")
        print(f"    Covers {len(funcs)} functions: {sample_funcs} ...")

    # 6. Kill Rule Evaluation
    print("\n" + "=" * 60)
    if slowdown > 3.0:
        choice = "PER-FILE"
        print(f"KILL RULE TRIGGERED: Slowdown {slowdown:.2f}x exceeds 3.0x threshold!")
        print("Fallback required: Switching to PER-FILE contexts.")
    else:
        choice = "PER-TEST"
        print(f"KILL RULE CHECK PASSED: Slowdown {slowdown:.2f}x is <= 3.0x threshold.")
        print(f"Decision: {choice} coverage is USABLE and AFFORDABLE.")
    print("=" * 60)

    return choice, slowdown


if __name__ == "__main__":
    main()
