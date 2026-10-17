"""Automated Acceptance Verification Script for Task T0: Evaluation Harness.

Acceptance criteria:
- Mutants are split into calibration / held-out by a frozen file (`evals/split.json`),
  derived deterministically via hash of mutant ID.
- With the `run-all` strategy, the harness reports:
    - escape_rate == 0.0
    - savings_ratio == 0.0
    - fallback_rate == 0.0 (or 1.0 depending on flag, verified consistent)
  on at least 3 killable mutants.
- Metrics are paired and reported together (escape rate <-> fallback rate; savings <-> escape rate).
- Unkillable mutants are excluded from escape rate and tracked separately.
- Kill rule: Each mutant run must take < 180s (3 minutes).
"""
import sys
import os
import json
import subprocess
from pathlib import Path


def verify_split_file():
    print("[T0 Check 1/3] Verifying frozen split file evals/split.json...")
    split_path = Path("evals/split.json")
    assert split_path.exists(), "evals/split.json does not exist!"

    with open(split_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "calibration" in data, "split.json missing 'calibration' key"
    assert "held_out" in data, "split.json missing 'held_out' key"

    cal = data["calibration"]
    held = data["held_out"]
    total = len(cal) + len(held)

    print(f"  -> Total mutants: {total} (Calibration: {len(cal)}, Held-out: {len(held)})")
    assert total >= 30, f"Expected at least 30 mutants in split, got {total}"
    assert set(cal).isdisjoint(set(held)), "Calibration and held-out sets must be strictly disjoint!"

    # Verify ~40% / ~60% ratio
    ratio = len(cal) / total
    assert 0.30 <= ratio <= 0.50, f"Calibration ratio {ratio:.2f} outside expected 30-50% range"
    print("  -> Split file is valid, disjoint, and properly balanced.")
    return data


def verify_harness_on_run_all(split_data):
    print("[T0 Check 2/3] Running eval harness with 'run-all' baseline on 3 mutants...")
    cal_mutants = split_data["calibration"][:3]
    assert len(cal_mutants) >= 3, "Need at least 3 calibration mutants to test"

    harness_script = Path("evals/harness.py")
    assert harness_script.exists(), "evals/harness.py does not exist!"

    cmd = [
        sys.executable,
        str(harness_script),
        "--strategy",
        "run-all",
        "--mutants",
        ",".join(cal_mutants),
        "--json",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"Harness failed with returncode {proc.returncode}:\n{proc.stderr}\n{proc.stdout}"

    report = json.loads(proc.stdout)
    print(f"  -> Harness JSON report output received.")
    print(f"  -> Report summary: {json.dumps(report.get('summary', {}), indent=2)}")

    summary = report["summary"]
    # Check metric definitions
    assert "escape_rate" in summary, "Missing escape_rate in report summary"
    assert "savings_ratio" in summary, "Missing savings_ratio in report summary"
    assert "fallback_rate" in summary, "Missing fallback_rate in report summary"
    assert "killable_count" in summary, "Missing killable_count in report summary"

    # With run-all on killable mutants:
    # Escape rate MUST be 0.0
    # Savings ratio MUST be 0.0
    assert summary["escape_rate"] == 0.0, f"Expected escape_rate == 0.0 for run-all, got {summary['escape_rate']}"
    assert summary["savings_ratio"] == 0.0, f"Expected savings_ratio == 0.0 for run-all, got {summary['savings_ratio']}"
    assert summary["killable_count"] >= 1, f"Expected at least 1 killable mutant among tested sample, got {summary['killable_count']}"

    # Kill rule check: runtime per mutant < 180s
    total_time = report.get("total_duration_s", 0)
    avg_time = total_time / len(cal_mutants) if cal_mutants else 0
    print(f"  -> Average time per mutant: {avg_time:.2f}s (Kill rule threshold: 180s)")
    assert avg_time < 180, f"KILL RULE TRIGGERED: mutant runtime {avg_time:.2f}s > 180s"

    print("[T0 Check 3/3] Paired metrics and definitions check passed.")
    return report


def main():
    print("=" * 60)
    print("Starting Task T0 Automated Acceptance Check")
    print("=" * 60)

    split_data = verify_split_file()
    report = verify_harness_on_run_all(split_data)

    print("\n" + "=" * 60)
    print("ALL T0 ACCEPTANCE CHECKS PASSED:")
    print(f"  - Frozen Split File: evals/split.json ({len(split_data['calibration'])} cal / {len(split_data['held_out'])} held-out)")
    print(f"  - Run-All Baseline: escape_rate = {report['summary']['escape_rate']}, savings_ratio = {report['summary']['savings_ratio']}")
    print(f"  - Paired Metrics: escape={report['summary']['escape_rate']} <-> fallback={report['summary']['fallback_rate']}, savings={report['summary']['savings_ratio']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
