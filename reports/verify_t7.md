# Task T7 Independent Verification Report

**Task Verified**: T7: Agent Integration
**Status Evaluated**: `[ ]` -> `[x]`
**Target Repo**: `target_repos/flask`
**Date**: 2026-10-16

---

## 1. Acceptance Criteria Review & Verification

### Acceptance: Test run calls `guard check`; low trust forces a full run; agent cannot skip it
- **Implementation**:
  - `guard/agent_integration.py` exposes `run_guard_agent_workflow()` and CLI command `guard run`.
  - When the diff has high trust (all modified functions covered with sufficient confidence), Guard selects a targeted test subset and executes only those tests (`policy="select"`, `forced_full=False`).
  - When the diff has low trust / uncovered modified functions (`no_evidence=True` or `confidence < threshold`), Guard detects the trust violation and enforces a full test suite run (`policy="run-all"`, `forced_full=True`). The agent runner cannot bypass this safety check.
  - If any test fails, Guard exits with non-zero code (exit code 1), blocking the agent from declaring the task complete.

### Acceptance Verification via `tests/verify_t7.py`:
1. **High-trust run**:
   - Change: touches `src/flask/config.py::Config.from_mapping`.
   - Policy: `select`, `forced_full=False`.
   - Execution: Ran 3 tests in 0.57s.
   - Result: PASS.
2. **Low-trust run**:
   - Change: touches `src/flask/views.py::View.dispatch_request` (uncovered / no evidence).
   - Policy: `run-all`, `forced_full=True`.
   - Execution: Guard overrides to full test suite (494 tests) in 1.59s.
   - Result: PASS.
3. **Failure blocking check**:
   - Change: intentional syntax/assertion breaking change.
   - Guard run result: Test fails, workflow exits with code 1, blocking completion.
   - Result: PASS.

---

## 2. Protection Audits & Test Results
- Zero changes to protected files or frozen sections:
  - `CLAIM (FROZEN)` in `PLAN.md`: Unchanged.
  - `evals/split.json`: Unchanged.
  - `tests/test_static.py`: Unchanged.
  - `tests/verify_t1.py`: Unchanged.
- Target repo working tree: Clean.
- Test suite: 32 passed in 0.25s (0 skipped, 0 xfailed, 0 warnings).

---

VERDICT: PASS
