"""Automated Acceptance Verification Script for Task T9: Demo and Submission.

Acceptance criteria (PLAN.md line 214):
1. Demo runs cleanly:
   - change -> tests with graph path
   - dynamic widening
   - uncovered fallback
   - metrics table
2. README.md names the graph-native parts and the limits.
3. Verification report reports/verify_t9.md ends in VERDICT: PASS.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README_FILE = ROOT / "README.md"
REPORT_FILE = ROOT / "reports" / "verify_t9.md"
DEMO_SCRIPT = ROOT / "demo.py"


def check_demo_execution():
    print("[T9 Check 1/3] Running end-to-end demo script (demo.py)...")
    assert DEMO_SCRIPT.exists(), f"Demo script {DEMO_SCRIPT} missing"
    proc = subprocess.run([sys.executable, str(DEMO_SCRIPT)], capture_output=True, text=True, cwd=str(ROOT))
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
    assert proc.returncode == 0, f"Demo script failed with exit code {proc.returncode}"

    out = proc.stdout
    assert "Graph Path" in out or "COVERED_BY" in out, "Demo output missing graph path explanation"
    assert "Dynamic Widening" in out or "dynamic_dispatch" in out, "Demo output missing dynamic widening section"
    assert "Fallback" in out or "run-all" in out, "Demo output missing uncovered fallback section"
    assert "Metrics Table" in out or "Escape Rate" in out, "Demo output missing paired metrics table"
    print("  -> Demo script ran cleanly and covered all 4 required stages.")


def check_readme_content():
    print("[T9 Check 2/3] Verifying README.md content and graph-native documentation...")
    assert README_FILE.exists(), f"README {README_FILE} missing"
    text = README_FILE.read_text(encoding="utf-8")

    required_keywords = [
        "FalkorDB",
        "Escape Rate",
        "Savings Ratio",
        "Fallback Rate",
        "same-file",
        "COVERED_BY",
        "dynamic widening",
        "Limits",
    ]
    for kw in required_keywords:
        assert kw.lower() in text.lower(), f"README missing documentation for '{kw}'"
    print("  -> README.md verified with graph-native concepts, frozen metrics, and limits.")


def check_report():
    print("[T9 Check 3/3] Verifying verification report artifact...")
    assert REPORT_FILE.exists(), f"Report {REPORT_FILE} missing"
    text = REPORT_FILE.read_text(encoding="utf-8")
    assert "VERDICT: PASS" in text, "Report missing VERDICT: PASS"
    print("  -> reports/verify_t9.md verified.")


def main():
    print("=" * 60)
    print("Starting Task T9 Acceptance Verification")
    print("=" * 60)
    check_demo_execution()
    check_readme_content()
    check_report()
    print("=" * 60)
    print("ALL T9 ACCEPTANCE CHECKS PASSED.")
    print("=" * 60)


if __name__ == "__main__":
    main()
