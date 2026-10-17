"""Evaluation Harness for Guard (T0).

Evaluates test selection strategies (run-all, same-file, guard) on mutants.
Computes paired metrics strictly adhering to Part B frozen definitions:
- Killable mutant: run-all has at least one failing test.
- Escape: a killable mutant where no selected test fails.
- Unkillable mutants are excluded from escape rate and reported separately.
- Savings = 1 - (time of selected tests, or full suite if fallback) / (time of full suite).
- Paired metrics: (escape rate <-> fallback rate; savings ratio <-> escape rate).
"""
import sys
import os
import time
import json
import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path("target_repos/flask").resolve()
MUTANTS_DIR = Path("evals/mutants").resolve()
SPLIT_FILE = Path("evals/split.json").resolve()


def apply_mutant(diff_file: Path) -> bool:
    """Applies a unified diff patch to the target repo."""
    cmd = ["git", "apply", str(diff_file)]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        # Fallback to patch utility if git apply has whitespace quirks
        patch_cmd = ["patch", "-p1", "-i", str(diff_file)]
        patch_proc = subprocess.run(patch_cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        return patch_proc.returncode == 0
    return True


def reset_repo():
    """Restores the target repo to pristine clean state."""
    subprocess.run(["git", "checkout", "--", "."], cwd=str(REPO_ROOT), capture_output=True)
    subprocess.run(["git", "clean", "-fdx"], cwd=str(REPO_ROOT), capture_output=True)


def run_pytest(test_targets=None) -> tuple[int, float, int]:
    """Runs pytest on given test_targets (or full suite).
    Returns (failures_count, duration_seconds, exit_code).
    """
    cmd = [sys.executable, "-m", "pytest", "-q", "--tb=no"]
    if test_targets:
        if isinstance(test_targets, str):
            cmd.append(test_targets)
        else:
            cmd.extend(test_targets)
    else:
        cmd.append("tests")

    start = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=15)
        duration = time.time() - start
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        return 1, duration, 1

    # Parse failures count
    # Output line usually ends with e.g. "1 failed, 493 passed in 1.1s" or "494 passed in 1.0s"
    stdout_lines = proc.stdout.strip().splitlines()
    summary = stdout_lines[-1] if stdout_lines else ""
    
    failures = 0
    if "failed" in summary:
        parts = summary.split(",")
        for part in parts:
            if "failed" in part:
                try:
                    failures = int(part.strip().split()[0])
                except Exception:
                    failures = 1
    elif proc.returncode != 0:
        failures = 1

    return failures, duration, proc.returncode


def resolve_strategy_tests(strategy: str, mutant_info: dict) -> tuple[list[str], bool]:
    """Resolves which tests to run for a given strategy.
    Returns (test_list, is_fallback).
    """
    if strategy == "run-all":
        return ["tests"], True

    elif strategy == "same-file":
        # Heuristic: map src/flask/<name>.py -> tests/test_<name>.py
        changed_file = mutant_info.get("file", "")
        stem = Path(changed_file).stem
        candidate = f"tests/test_{stem}.py"
        full_candidate = REPO_ROOT / candidate
        if full_candidate.exists():
            return [candidate], False
        # If no direct match, check if basic exists or fallback
        if (REPO_ROOT / "tests/test_basic.py").exists():
            return ["tests/test_basic.py"], False
        return ["tests"], True

    elif strategy == "naive-guess":
        # Naive agent guess: guesses test file from stem, or test_basic if not found.
        # Crucially: NEVER falls back (is_fallback=False), modeling an agent with no safety layer.
        changed_file = mutant_info.get("file", "")
        stem = Path(changed_file).stem
        candidate = f"tests/test_{stem}.py"
        full_candidate = REPO_ROOT / candidate
        if full_candidate.exists():
            return [candidate], False
        return ["tests/test_basic.py"], False

    elif strategy == "guard":
        from guard.thin_slice import guard_check
        diff_file = mutant_info.get("diff_file")
        if diff_file and Path(diff_file).exists():
            check_res = guard_check(diff_file=diff_file)
        elif "diff_text" in mutant_info:
            check_res = guard_check(diff_text=mutant_info["diff_text"])
        else:
            check_res = guard_check(repo_path=REPO_ROOT)
        return check_res.selected_tests, check_res.is_fallback

    elif strategy == "guard-no-confidence":
        from guard.thin_slice import guard_check
        diff_file = mutant_info.get("diff_file")
        if diff_file and Path(diff_file).exists():
            check_res = guard_check(diff_file=diff_file, no_confidence_filter=True)
        elif "diff_text" in mutant_info:
            check_res = guard_check(diff_text=mutant_info["diff_text"], no_confidence_filter=True)
        else:
            check_res = guard_check(repo_path=REPO_ROOT, no_confidence_filter=True)
        return check_res.selected_tests, check_res.is_fallback

    elif strategy == "guard-no-widening":
        from guard.thin_slice import guard_check
        diff_file = mutant_info.get("diff_file")
        if diff_file and Path(diff_file).exists():
            check_res = guard_check(diff_file=diff_file, no_dynamic_widening=True)
        elif "diff_text" in mutant_info:
            check_res = guard_check(diff_text=mutant_info["diff_text"], no_dynamic_widening=True)
        else:
            check_res = guard_check(repo_path=REPO_ROOT, no_dynamic_widening=True)
        return check_res.selected_tests, check_res.is_fallback

    raise ValueError(f"Unknown strategy: {strategy}")


def evaluate_diff(diff_file: Path, strategy: str) -> dict:
    """Evaluates a single diff file using the specified strategy."""
    diff_file = diff_file.resolve()
    assert diff_file.exists(), f"Diff file {diff_file} not found"
    reset_repo()
    applied = apply_mutant(diff_file)
    if not applied:
        return {"diff_file": str(diff_file), "status": "ERROR", "error": "Failed to apply diff"}

    try:
        full_failures, t_full, full_exit = run_pytest()
        is_killable = full_failures > 0

        mutant_info = {"id": diff_file.stem, "diff_file": diff_file}
        selected_tests, is_fallback = resolve_strategy_tests(strategy, mutant_info)

        if is_fallback or strategy == "run-all":
            sel_failures = full_failures
            t_sel = t_full
        else:
            sel_failures, t_sel, sel_exit = run_pytest(selected_tests)

        escaped = is_killable and (sel_failures == 0)
        savings = 0.0 if is_fallback else (max(0.0, 1.0 - (t_sel / t_full)) if t_full > 0 else 0.0)

        return {
            "diff_file": str(diff_file),
            "status": "OK",
            "strategy": strategy,
            "is_killable": is_killable,
            "escaped": escaped,
            "is_fallback": is_fallback,
            "selected_tests_count": len(selected_tests),
            "selected_duration_s": round(t_sel, 3),
            "full_duration_s": round(t_full, 3),
            "savings": round(savings, 4),
            "full_failures": full_failures,
            "selected_failures": sel_failures,
        }
    finally:
        reset_repo()


def evaluate_mutant(mutant_id: str, strategy: str) -> dict:
    diff_file = MUTANTS_DIR / f"{mutant_id}.diff"
    assert diff_file.exists(), f"Mutant diff {diff_file} not found"

    with open(MUTANTS_DIR / "index.json", "r", encoding="utf-8") as f:
        index = {m["id"]: m for m in json.load(f)}
    mutant_info = index.get(mutant_id, {"id": mutant_id})
    mutant_info["diff_file"] = diff_file

    # Ensure clean starting state
    reset_repo()

    # 1. Apply mutant
    applied = apply_mutant(diff_file)
    if not applied:
        return {
            "mutant_id": mutant_id,
            "status": "ERROR",
            "error": "Failed to apply mutant diff",
        }

    try:
        # 2. Run full suite to check killability (ground truth)
        full_failures, t_full, full_exit = run_pytest()
        is_killable = full_failures > 0

        # 3. Resolve selected tests
        selected_tests, is_fallback = resolve_strategy_tests(strategy, mutant_info)

        # 4. Run selected tests
        if is_fallback or strategy == "run-all":
            sel_failures = full_failures
            t_sel = t_full
        else:
            sel_failures, t_sel, sel_exit = run_pytest(selected_tests)

        # 5. Evaluate escape & savings
        # Frozen definition: Escape = a killable mutant where no selected test fails
        escaped = is_killable and (sel_failures == 0)

        # Frozen definition: Savings = 1 - (time of selected / time of full)
        if is_fallback:
            savings = 0.0
        else:
            savings = max(0.0, 1.0 - (t_sel / t_full)) if t_full > 0 else 0.0

        return {
            "mutant_id": mutant_id,
            "status": "OK",
            "strategy": strategy,
            "is_killable": is_killable,
            "escaped": escaped,
            "is_fallback": is_fallback,
            "selected_tests_count": len(selected_tests),
            "selected_duration_s": round(t_sel, 3),
            "full_duration_s": round(t_full, 3),
            "savings": round(savings, 4),
            "full_failures": full_failures,
            "selected_failures": sel_failures,
        }
    finally:
        reset_repo()


def run_evaluation(mutants: list[str], strategy: str) -> dict:
    results = []
    start_total = time.time()

    for mid in mutants:
        res = evaluate_mutant(mid, strategy)
        results.append(res)

    total_duration = time.time() - start_total

    # Compute paired aggregate metrics
    killable = [r for r in results if r.get("is_killable") is True]
    unkillable = [r for r in results if r.get("is_killable") is False]
    escapes = [r for r in killable if r.get("escaped") is True]
    fallbacks = [r for r in results if r.get("is_fallback") is True]

    killable_count = len(killable)
    unkillable_count = len(unkillable)
    escape_count = len(escapes)
    fallback_count = len(fallbacks)

    escape_rate = (escape_count / killable_count) if killable_count > 0 else 0.0
    fallback_rate = (fallback_count / len(results)) if results else 0.0

    # Average savings over killable mutants (or 0 if empty)
    savings_ratio = (sum(r.get("savings", 0.0) for r in killable) / killable_count) if killable_count > 0 else 0.0

    summary = {
        "strategy": strategy,
        "total_evaluated": len(results),
        "killable_count": killable_count,
        "unkillable_count": unkillable_count,
        "escape_count": escape_count,
        "escape_rate": round(escape_rate, 4),
        "fallback_count": fallback_count,
        "fallback_rate": round(fallback_rate, 4),
        "savings_ratio": round(savings_ratio, 4),
    }

    return {
        "summary": summary,
        "mutant_results": results,
        "total_duration_s": round(total_duration, 3),
    }


def main():
    parser = argparse.ArgumentParser(description="Guard Evaluation Harness")
    parser.add_argument(
        "--strategy",
        choices=["run-all", "same-file", "naive-guess", "guard", "guard-no-confidence", "guard-no-widening"],
        default="run-all",
    )
    parser.add_argument("--mutants", help="Comma-separated mutant IDs or 'calibration' or 'held-out'")
    parser.add_argument("--diff", help="Path to a single diff file to evaluate")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    if args.diff:
        res = evaluate_diff(Path(args.diff), args.strategy)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(json.dumps(res, indent=2))
        return

    # Resolve mutant list
    if args.mutants == "calibration" or args.mutants == "held-out":
        with open(SPLIT_FILE, "r", encoding="utf-8") as f:
            split_data = json.load(f)
        target_list = split_data["calibration"] if args.mutants == "calibration" else split_data["held_out"]
    elif args.mutants:
        target_list = [m.strip() for m in args.mutants.split(",") if m.strip()]
    else:
        with open(SPLIT_FILE, "r", encoding="utf-8") as f:
            split_data = json.load(f)
        target_list = split_data["calibration"]

    report = run_evaluation(target_list, args.strategy)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=" * 60)
        print(f"EVALUATION REPORT: Strategy '{args.strategy}'")
        print("=" * 60)
        s = report["summary"]
        print(f"Total Mutants Evaluated : {s['total_evaluated']}")
        print(f"Killable Mutants        : {s['killable_count']} (Unkillable: {s['unkillable_count']})")
        print(f"Escape Rate (Paired)    : {s['escape_rate']*100:.1f}% ({s['escape_count']}/{s['killable_count']})")
        print(f"Fallback Rate (Paired)  : {s['fallback_rate']*100:.1f}% ({s['fallback_count']}/{s['total_evaluated']})")
        print(f"Savings Ratio (Paired)  : {s['savings_ratio']*100:.1f}%")
        print(f"Total Evaluation Time   : {report['total_duration_s']}s")
        print("=" * 60)


if __name__ == "__main__":
    main()
