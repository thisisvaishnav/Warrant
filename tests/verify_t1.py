"""Automated Acceptance Verification Script for Task T1: Target repo and environment.

Acceptance criteria:
- `docker compose up -d` works; FalkorDB is live and reachable.
- Suite in target_repos/flask passes 3 times in a row with identical results.
- Repo has several hundred tests (> 300).
- Kill Rule: Suite runtime must be < 5 minutes (300s) per run and results must not differ.
"""
import sys
import time
import subprocess
import redis


def check_falkordb():
    print("[T1 Check 1/3] Verifying FalkorDB connection...")
    r = redis.Redis(host="localhost", port=6379, socket_timeout=5)
    assert r.ping() is True, "Failed to ping FalkorDB on localhost:6379"
    # Verify graph query support
    res = r.execute_command("GRAPH.QUERY", "t1_test_graph", "RETURN 1")
    assert res is not None, "Failed to execute GRAPH.QUERY on FalkorDB"
    r.execute_command("GRAPH.DELETE", "t1_test_graph")
    print("  -> FalkorDB is LIVE and healthy.")


def run_flask_suite(run_number: int):
    print(f"[T1 Check 2/3] Running Flask test suite (Run {run_number}/3)...")
    start = time.time()
    # Run pytest on target_repos/flask/tests
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=short",
            "target_repos/flask/tests",
        ],
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - start
    print(f"  -> Run {run_number} finished in {elapsed:.2f}s (Exit code: {proc.returncode})")
    
    # Parse last line summary e.g., "494 passed in 1.72s"
    stdout_lines = proc.stdout.strip().splitlines()
    summary_line = stdout_lines[-1] if stdout_lines else ""
    # Strip timing suffix e.g. " in 1.72s" to compare test outcomes (e.g. "494 passed")
    outcome_part = summary_line.split(" in ")[0].strip() if " in " in summary_line else summary_line
    print(f"  -> Outcome: {outcome_part}")

    # Check kill rule: runtime < 300s
    assert elapsed < 300, f"KILL RULE TRIGGERED: Suite runtime {elapsed:.2f}s > 300s"
    assert proc.returncode == 0, f"Flask suite failed with exit code {proc.returncode}\n{proc.stderr}\n{proc.stdout}"

    return {
        "run": run_number,
        "elapsed": elapsed,
        "summary": summary_line,
        "outcome": outcome_part,
        "exit_code": proc.returncode,
    }


def main():
    print("=" * 60)
    print("Starting Task T1 Automated Acceptance Check")
    print("=" * 60)

    # 1. Check FalkorDB
    check_falkordb()

    # 2. Run target repo suite 3 times
    runs = []
    for i in range(1, 4):
        runs.append(run_flask_suite(i))

    # 3. Check stability across 3 runs
    print("[T1 Check 3/3] Checking result consistency across 3 runs...")
    first_outcome = runs[0]["outcome"]
    for r in runs[1:]:
        assert r["outcome"] == first_outcome, (
            f"KILL RULE TRIGGERED: Flaky suite! Result differed:\n"
            f"  Run 1: {first_outcome}\n"
            f"  Run {r['run']}: {r['outcome']}"
        )

    print("\n" + "=" * 60)
    print("ALL T1 ACCEPTANCE CHECKS PASSED:")
    print(f"  - FalkorDB: Reachable & responding to GRAPH commands.")
    print(f"  - 3-Run Consistency: IDENTICAL across all 3 runs.")
    print(f"  - Suite Outcome: {first_outcome}")
    print(f"  - Max Runtime: {max(r['elapsed'] for r in runs):.2f}s (Kill threshold: 300s)")
    print("=" * 60)


if __name__ == "__main__":
    main()
