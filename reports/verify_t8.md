# Task T8 Independent Verification Report

**Task Verified**: T8: Full Evaluation on Frozen Claim
**Status Evaluated**: `[ ]` -> `[x]`
**Target Repo**: `target_repos/flask` (`pallets/flask`)
**Date**: 2026-10-16

---

## 1. Frozen Claim & Acceptance Summary

### Claim (Frozen in `PLAN.md` line 25-28):
> On the held-out mutants of the target repo, Guard's selected tests have escape rate $\le 5\%$ and test-time saving $\ge 40\%$ versus `run-all`, and Guard beats the `same-file` heuristic on at least one of the two metrics.

### Verification Outcome:
- **Guard Escape Rate**: **0.0%** (target: $\le 5\%$) -> **PASS** (0 escapes / 17 killable mutants)
- **Guard Savings Ratio**: **67.3%** (target: $\ge 40\%$) -> **PASS**
- **Comparison vs `same-file`**:
  - `same-file` Escape Rate: **17.6%** (3 escapes)
  - `guard` Escape Rate: **0.0%** (0 escapes)
  - Guard strictly outperforms the `same-file` heuristic on escape rate (0.0% vs 17.6%) -> **PASS**
- **FalkorDB Graph Backing**:
  - 83 File nodes, 393 Function nodes, 1,038 Test nodes, 3 Run nodes
  - 22,015 `COVERED_BY` edges, 159 `CALLS`, 175 `IMPORTS`, 1,431 `DEFINED_IN`
  - All decisions executed against live FalkorDB instance (`guard` database).

---

## 2. Paired Metrics Results Table (Held-Out Mutants)

All 4 strategies and 2 ablations evaluated across the 24 held-out mutants (`m01`, `m03`, `m04`, `m06`, `m08`, `m11`, `m13`, `m14`, `m15`, `m16`, `m19`, `m20`, `m21`, `m22`, `m24`, `m26`, `m27`, `m29`, `m30`, `m32`, `m35`, `m36`, `m37`, `m38`).

| Strategy / Configuration | Escape Rate (Paired) | Savings Ratio (Paired) | Fallback Rate (Paired) | Killable Evaluated | Escaped Mutants |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`run-all`** (Ground Truth) | 0.0% (0/17) | 0.0% | 100.0% (24/24) | 17 | None |
| **`same-file`** (Heuristic) | 17.6% (3/17) | 77.3% | 0.0% (0/24) | 17 | `m08`, `m16`, `m30` |
| **`naive-guess`** (Agent Guess) | 17.6% (3/17) | 77.5% | 0.0% (0/24) | 17 | `m08`, `m16`, `m30` |
| **`guard`** (Full System) | **0.0% (0/17)** | **67.3%** | **25.0% (6/24)** | 17 | **None** |
| *Ablation 1: `guard-no-confidence`* | 0.0% (0/17) | 77.1% | 20.8% (5/24) | 17 | None |
| *Ablation 2: `guard-no-widening`* | 0.0% (0/17) | 73.3% | 25.0% (6/24) | 17 | None |

---

## 3. Unkillable Mutants

Per the frozen definitions (R3 / Part B), unkillable mutants (`run-all` test suite exhibits 0 failures) are excluded from the escape rate calculation and reported separately:
- **Total unkillable mutants**: 7
- **Mutant IDs**: `['m01', 'm04', 'm20', 'm21', 'm26', 'm27', 'm29']`
- **Total killable mutants**: 17

---

## 4. Failure Case Write-up: `m08` Escape Under `same-file`

- **Mutant ID**: `m08` (`src/flask/helpers.py:45`, invert `if not`)
- **Symptoms**:
  - `same-file` ran `tests/test_helpers.py` (30 tests) and reported **0 failures**. The mutant **escaped**.
  - `naive-guess` ran `tests/test_helpers.py` and reported **0 failures**. The mutant **escaped**.
  - `guard` queried the FalkorDB graph for `COVERED_BY` edges and discovered cross-module callers and dependent tests in `tests/test_basic.py`, `tests/test_blueprints.py`, and `tests/test_templating.py` (selecting 26 tests).
  - `guard` executed the selected tests: **1 failure caught**, escape prevented with 0.0% escape rate!
- **Root Cause Analysis**:
  - Many helper utilities in frameworks like Flask are primarily exercised through core lifecycle, templating, and blueprint dispatch tests rather than unit tests localized in `test_helpers.py`.
  - Simple lexical or file-stem matching (`same-file` / `naive-guess`) has blind spots for foundational utilities.
  - The graph-native per-test coverage topology in FalkorDB links functions directly to the exact tests that execute them regardless of filesystem folder boundaries.

---

## 5. Ablations Analysis

1. **Ablation 1 (`guard-no-confidence`)**:
   - Removes the confidence threshold ($\ge 0.8$) and `no_evidence` hard fallback.
   - Result: Fallback dropped from 25.0% to 20.8%, increasing savings to 77.1% while maintaining 0.0% escapes on this benchmark. However, on uncovered functions (e.g. `View.dispatch_request`), disabling confidence safety would eliminate the fallback safety net that guarantees safety when coverage evidence is missing.
2. **Ablation 2 (`guard-no-widening`)**:
   - Removes module widening on functions flagged with `has_dynamic_dispatch`.
   - Result: Savings increased to 73.3% while maintaining 0.0% escapes on the held-out split. Widening provides defensive margin when dynamic attributes (`getattr`, `wraps`, dynamic decorators) prevent complete static call graph resolution.

---

## 6. Protection Audits & Invariants
- Zero changes to protected files or frozen sections:
  - `CLAIM (FROZEN)` in `PLAN.md`: Unchanged.
  - `DEFINITIONS` in `PLAN.md`: Unchanged.
  - `evals/split.json`: Unchanged.
  - `tests/test_static.py`: Unchanged.
  - `tests/verify_t1.py`: Unchanged.
- Target repo working tree: Pristine and clean.
- Unit tests: All 32 unit tests pass (`pytest tests/`).

---

VERDICT: PASS
