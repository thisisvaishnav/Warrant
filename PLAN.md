# Guard: project plan (template v1)

Graph-powered safety layer for AI coding agents, built on FalkorDB.
Questions: (1) which tests to run after a change, (2) is the graph reliable enough to skip any, (3) what to do when it is not.

---------------------------------------------------------------------
## PART A: RULES (apply to every task)

R1 HOFSTADTER: No hours or days in this plan. Order by dependency and risk. "Done" = an automated check passes.
R2 PARKINSON: No time slots. Every task has a done-check and a kill rule.
R3 GOODHART: Tune only on the calibration split. Run the held-out split once. Every metric has a paired metric.
R4 GALL: Build the thin slice first, then deepen each part.
R5 MURPHY: Spike the riskiest unknown before building on it. Every task has a fallback.
R6 BROOKS: Parallel agents only on tasks that share no files or state. Each handoff has a written interface.
R7 CHESTERTON: Do not delete or weaken a test or check without a written reason in DEVIATIONS.md.
R8 SELF-GRADING: Acceptance checks are written BEFORE implementation. The agent never decides "done" alone.
R9 INDEPENDENT VERIFICATION: A task is ticked [x] only after a
  verifier report in reports/ ends with VERDICT: PASS.

---------------------------------------------------------------------
## PART B: PROJECT

GOAL: After an AI agent changes code, select the tests to run with a measured trust score, and run the full suite when trust is low.

CLAIM (FROZEN: do not edit after seeing results):
  On the held-out mutants of the target repo, Guard's selected tests have
  escape rate <= 5% and test-time saving >= 40% versus run-all, and Guard
  beats the same-file heuristic on at least one of the two metrics.

DEFINITIONS (frozen with the claim):
  - Killable mutant: run-all has at least one failing test.
  - Escape: a killable mutant where no selected test fails.
  - Unkillable mutants are excluded from escape rate and reported separately.
  - Savings = 1 - (time of selected tests, or full suite if fallback) / (time of full suite).

METRICS AND PAIRED METRICS (R3):
  - Escape rate  <-> fallback rate. (A low escape rate is meaningless if Guard always runs everything.)
  - Savings ratio <-> escape rate. (High savings is meaningless if it misses failures.)
  Report all three together, always.

SCOPE: One Python repo, pytest only, per-test coverage evidence, static call graph.
NON-GOALS: Other languages. Resolving dynamic calls (detect and widen instead). Multi-agent collision detection. A custom UI.

TARGET REPO: pallets/flask
BASELINES: run-all; same-file heuristic; naive agent guess.

PRIORITY
  Must:   T1, T3, S1, T4, T0, T5a, T5, T8
  Should: T6, T7
  Could:  T9 polish, graph visualization, collision detection
  Cut order when short: bottom first. Never cut done-checks or T8.

DEPENDENCY MAP
  T1 -> T2 -> T3 --------------------+
  T1 -> S1 -> T4 --------------------+-> T5a -> T5 -> T6 -> T7 -> T8 -> T9
  T1 -> T0 (eval harness, early) -----+-----------------------> T8

RISKIEST UNKNOWN: Per-test coverage may be too slow or unusable on the target repo.
SPIKE: S1 (below). Nothing that depends on coverage is built before S1 passes.

THIN SLICE (T5a): one git diff -> changed functions -> covering tests -> crude decision
  (select tests, or run all if any changed function has no evidence) -> result compared with run-all.

PARALLEL WORK (R6): S1 and T0 may run in parallel. They share no files. Interface: T0 consumes a
  "selected tests" JSON list and returns metrics. S1 produces coverage data only.

---------------------------------------------------------------------
## PART C: TASKS

Status: [ ] not started, [~] partly done, [pending verification] pending verification, [x] done

### T1 Target repo and environment   [x]
DEPENDS ON: none        PRIORITY: must
GOAL: A target repo is chosen and its suite passes on a clean checkout, with FalkorDB running.
ACCEPTANCE: `docker compose up -d` works; suite passes 3 times in a row with identical results; repo has several hundred tests.
NON-GOALS: Any Guard logic.
UNKNOWN: Whether the suite is flaky or too slow.
KILL RULE: If clean suite runtime > 5 minutes or results differ across 3 runs, kill target repo immediately.
FALLBACK: Choose another repo (e.g. requests or click). Do not fix a flaky repo.
PROTECTED: nothing yet.
DONE = acceptance passes.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T2 Schema   [x]
DEPENDS ON: none        PRIORITY: must
GOAL: Node and edge model and indexes exist (`guard/db.py`).
ACCEPTANCE: A sample graph can be written and read back from a live FalkorDB via automated test `tests/test_db.py`.
KILL RULE: If live FalkorDB is unreachable after 3 connection retries or container restart, kill live FalkorDB usage.
FALLBACK: In-memory networkx/SQLite graph backend conforming to same DB interface.
DONE = `pytest tests/test_db.py` passes on a live database.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T3 Static graph   [x]
DEPENDS ON: T1, T2      PRIORITY: must
GOAL: Functions, calls, imports, and dynamic-dispatch flags for the target repo are in FalkorDB.
ACCEPTANCE:
  - 6 parser tests pass (`tests/test_static.py`).
  - Automated verification script asserts `guard callers <fn> --hops 4` matches expected callers for 5 predetermined functions.
  - Dynamic-dispatch count is above 0 on the target repo.
NON-GOALS: Type inference for `obj.method()` calls. Unresolved calls stay unresolved.
UNKNOWN: How many calls the parser leaves unresolved on the target repo.
CHECKPOINT: after the first ingest, review the summary counts.
KILL RULE: If AST parsing of target repo takes > 60s or crashes on core syntax, kill static deep traversal.
FALLBACK: Accept lower call coverage; rely on coverage evidence (T4) for missing links.
PROTECTED: tests/test_static.py.
DONE = all three acceptance checks pass.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### S1 SPIKE: per-test coverage   [x]
DEPENDS ON: T1          PRIORITY: must (riskiest unknown)
GOAL: Learn whether per-test coverage is usable and affordable on the target repo.
ACCEPTANCE: On 20 tests, `pytest --cov --cov-context=test` finishes; data maps each test to functions; slowdown versus plain run is recorded as a number.
NON-GOALS: Writing to FalkorDB.
KILL RULE: If slowdown > 3.0x or memory explodes / context tracking fails, kill per-test coverage immediately.
FALLBACK: Per-file contexts (one coverage context per test file). Log in DEVIATIONS.md.
DONE = result and slowdown number written down, and choice (per-test or per-file) made.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T0 Evaluation harness (early)   [x]
DEPENDS ON: T1          PRIORITY: must
GOAL: A script that takes a mutant and a "selected tests" list and reports escape, time saved, and fallback.
ACCEPTANCE: With run-all strategy it reports escape = 0 and savings = 0 on 3 mutants. Mutants are split calibration / held-out by a frozen file (`evals/split.json`), written BEFORE any tuning.
NON-GOALS: Guard logic.
UNKNOWN: How long one mutant takes to run.
KILL RULE: If mutant runner takes > 3 minutes per mutant, kill dynamic mutation.
FALLBACK: Use real historical commits / git diffs instead of generated mutants.
PROTECTED: the split file and the metric definitions.
DONE = acceptance passes.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T4 Coverage evidence   [ ]
DEPENDS ON: S1, T3      PRIORITY: must
GOAL: COVERED_BY edges (source='coverage', confidence 0.9) and Run nodes are in the graph, flaky tests are measured.
ACCEPTANCE:
  - Automated script exits non-zero if any Function has neither a COVERED_BY edge nor no_evidence=true.
  - Automated script verifies 5 COVERED_BY edges match known covered functions.
  - Suite run 3 times; flake_rate set; flaky tests excluded from evidence.
NON-GOALS: Trust score. New edge types.
UNKNOWN: Whether coverage contexts survive the target repo's test setup.
CHECKPOINT: after the coverage reader produces rows, before writing to FalkorDB.
KILL RULE: If coverage ingest takes > 2 minutes or DB explodes, kill fine-grained edges.
FALLBACK: Per-file contexts (if not already chosen in S1).
DONE = all three checks pass.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T5a Thin slice   [ ]
DEPENDS ON: T3, T4, T0  PRIORITY: must
GOAL: End-to-end path with crude logic.
ACCEPTANCE: For 3 hand-made diffs, `guard check` outputs a test list or "run all"; T0 scores the result; the whole run needs no manual steps.
NON-GOALS: Trust formula, hard-override rules beyond "no evidence -> run all".
KILL RULE: If end-to-end plumbing fails on basic diff or takes > 10s per check, kill complex routing.
FALLBACK: Direct file-to-test mapping without multi-hop graph expansion.
DONE = acceptance passes.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T5 Decision engine   [ ]
DEPENDS ON: T5a         PRIORITY: must
GOAL: Trust score, hard overrides, and the three-level policy.
  trust = 0.5*evidence_ratio + 0.3*freshness + 0.2*(1 - uncertain_ratio)   (starting weights)
  Hard overrides first: no evidence -> run all; dynamic dispatch -> add module tests; test files touched -> run all + warning.
  Policy: trust >= 0.8 subset; 0.5-0.8 subset + module tests; < 0.5 run all.
ACCEPTANCE:
  - One automated test per hard override and per policy level.
  - Every skipped test has a queryable reason (edges and confidence).
  - Weights and thresholds are tuned on the calibration split only, then frozen.
NON-GOALS: Learning the weights automatically.
UNKNOWN: Whether the fallback rate makes savings too small.
CHECKPOINT: after the overrides work, before tuning thresholds.
KILL RULE: If 3-level policy causes savings < 20% on calibration split, kill medium tier.
FALLBACK: Simplify to two levels (subset or run all).
DONE = acceptance passes and thresholds are frozen.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T6 Feedback loop   [ ]
DEPENDS ON: T5          PRIORITY: should
GOAL: A missed failure repairs the graph and changes the next decision.
ACCEPTANCE: Automated test shows a miss, a repair edge (source='miss_repair', old and new confidence logged), and a wider decision on a similar change. Unrelated paths are unchanged.
NON-GOALS: Automatic retraining.
KILL RULE: If feedback loop corrupts existing confidence metrics or increases escape rate on calibration, kill feedback auto-update.
FALLBACK: Log misses and require manual repair.
DONE = acceptance passes.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T7 Agent integration   [ ]
DEPENDS ON: T5          PRIORITY: should
GOAL: An agent calls Guard before declaring a task done and obeys the result.
ACCEPTANCE: A test run calls `guard check`; low trust forces a full run; agent cannot skip it.
NON-GOALS: Supporting several agent frameworks.
KILL RULE: If MCP protocol integration blocks or is unstable, kill MCP wrapper.
FALLBACK: A git pre-commit hook instead of an MCP tool.
DONE = acceptance passes on a real agent run / hook.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T8 Evaluation   [ ]
DEPENDS ON: T5, T0 (T6 if built)   PRIORITY: must
GOAL: Results for the claim.
ACCEPTANCE:
  - 30 to 50 mutants, split as frozen in T0.
  - All four strategies run on the held-out set exactly once.
  - Table shows escape, savings, and fallback for each strategy.
  - Two ablations: no confidence filter; no dynamic-dispatch widening.
  - At least one failure case written up.
  - Unkillable mutants reported separately.
NON-GOALS: Re-tuning after seeing held-out results.
KILL RULE: If evaluation runtime exceeds 1 hour, kill remaining mutants and evaluate on current subset (minimum 20 mutants).
FALLBACK: Fewer mutants, with the smaller N stated.
PROTECTED: the claim, the split, the thresholds.
DONE = all items present. If the claim fails, report it as it is.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

### T9 Demo and submission   [ ]
DEPENDS ON: T8          PRIORITY: could (README is must)
GOAL: A demo and a README that name the graph-native parts and the limits.
ACCEPTANCE: Demo runs from a clean clone: change -> tests with graph path -> dynamic widening -> uncovered fallback -> metrics table.
KILL RULE: If live browser demo setup fails, kill live web demo.
FALLBACK: Recorded run and static screenshots from the FalkorDB browser.
DONE = acceptance passes.
VERIFIED BY: independent verifier session (fresh context). Human reads VERDICT only.

---------------------------------------------------------------------
## PART D: AGENT INSTRUCTIONS

1. Before any code, audit this plan against R1-R8. List violations. Wait for approval of changes.
2. Ask at most 3 questions. State assumptions for the rest.
3. Run S1 first. Report the result. Re-plan if it changes anything.
4. Build T5a before deepening any part.
5. For each task: write the acceptance check, implement, stop at the checkpoint, run the check, show the diff.
6. Never claim "done" without check output. Never change the frozen claim, split, or definitions.
7. Anything that contradicts the plan: stop, log in DEVIATIONS.md, ask.
8. Report failures and limits plainly.
