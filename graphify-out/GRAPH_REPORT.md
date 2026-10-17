# Graph Report - guard  (2026-10-17)

## Corpus Check
- 70 files · ~114,349 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 52 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 512 nodes · 1014 edges · 58 communities (22 shown, 36 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1ac56047`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- db.py
- decide
- subprocess
- figma-make-app
- json
- static.py
- build_safety_figure.mjs
- coverage.py
- verify_t3.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- App.tsx
- Verification Reports README
- SafetyGate
- verify_t9.py
- FalkorDB Safety Layer
- scripts
- FalkorDB Graph Matrix
- FigmaSiteConfiguration
- dependencies
- ASD-STE100 Compliance
- Agent
- FalkorDB Service
- Gated Executor
- verify_prep.sh
- Formal Eval Report: Task T2
- Nokia Logo
- Mindflow Logo
- Freepik Logo
- Noota Logo
- Salesforce Logo
- MariaDB Logo
- Coral Glow Graphic
- G2 Logo
- Gojiberry Logo
- Hero Glow Background
- Louis Portrait
- Warrant Logo
- guard

## God Nodes (most connected - your core abstractions)
1. `decide()` - 23 edges
2. `StaticResult` - 22 edges
3. `get_graph()` - 21 edges
4. `Change` - 19 edges
5. `compilerOptions` - 17 edges
6. `FuncDef` - 16 edges
7. `guard_check()` - 16 edges
8. `run_capability_evals()` - 13 edges
9. `write_static()` - 13 edges
10. `analyze_repo()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Task T4 Verification Report` --references--> `FalkorDB Logo`  [INFERRED]
  reports/verify_t4.md → landing/public/assets/falkordb.svg
- `run_capability_evals()` --calls--> `ensure_schema()`  [EXTRACTED]
  evals/eval_t2.py → guard/db.py
- `run_capability_evals()` --calls--> `get_graph()`  [EXTRACTED]
  evals/eval_t2.py → guard/db.py
- `run_capability_evals()` --calls--> `reset_graph()`  [EXTRACTED]
  evals/eval_t2.py → guard/db.py
- `resolve_strategy_tests()` --calls--> `guard_check()`  [EXTRACTED]
  evals/harness.py → guard/thin_slice.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Guard Thin Slice Flow** — plan_t3, plan_t4, plan_t0, plan_t5a [EXTRACTED 0.90]
- **FalkorDB Safety States** — falkordb_state_blocked_png, falkordb_state_verified_png, falkordb_safety_light_png [EXTRACTED 0.95]
- **Graph Safety Interlock Flow** — falkordb_safety_layer_cypher_evaluation_gantry, falkordb_safety_layer_safetygate, falkordb_safety_layer_trip_latch [EXTRACTED 0.95]
- **Safety Verification Flow** — falkordb_graph_matrix, cypher, safety_policy, gated_executor [EXTRACTED 0.95]
- **Guard Verification Pipeline** — reports_verify_t4, reports_verify_t5, reports_verify_t5a, reports_verify_t6, reports_verify_t7, reports_verify_t8 [EXTRACTED 1.00]
- **Trust Score Calculation Components** — deviations_t5_metric, plan_t5, readme_concept [INFERRED 0.80]

## Communities (58 total, 36 thin omitted)

### Community 0 - "db.py"
Cohesion: 0.07
Nodes (30): main(), run_capability_evals(), run_regression_evals(), _batches(), get_callers(), get_covering_tests(), get_schema_counts(), write_coverage() (+22 more)

### Community 1 - "decide"
Cohesion: 0.09
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "subprocess"
Cohesion: 0.07
Nodes (31): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+23 more)

### Community 3 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 4 - "json"
Cohesion: 0.08
Nodes (32): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants(), cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_feedback() (+24 more)

### Community 5 - "static.py"
Cohesion: 0.07
Nodes (15): analyze_repo(), _Collector, _decorator_name(), is_test_file(), is_test_function(), module_name(), _resolve_module(), make() (+7 more)

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "coverage.py"
Cohesion: 0.15
Nodes (11): compute_flakiness(), CoverageResult, ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, _write_to_falkordb() (+3 more)

### Community 8 - "verify_t3.py"
Cohesion: 0.53
Nodes (4): check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main()

### Community 9 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+10 more)

### Community 10 - "package.json"
Cohesion: 0.17
Nodes (11): name, private, type, version, oxfmt, react-dom, tailwindcss, @types/node (+3 more)

### Community 11 - "T3: Static graph"
Cohesion: 0.23
Nodes (12): S1: SPIKE: per-test coverage, T0: Evaluation harness, T1: Target repo and environment, T2: Schema, T3: Static graph, T4: Coverage evidence, T5: Decision engine, T5a: Thin slice (+4 more)

### Community 12 - "vite.config.ts"
Cohesion: 0.22
Nodes (4): figmaReactRefreshBoundaryFallback(), @tailwindcss/vite, vite, @vitejs/plugin-react

### Community 13 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, oxfmt, tailwindcss, @tailwindcss/vite, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 15 - "App.tsx"
Cohesion: 0.39
Nodes (6): App(), Arrow(), ProspectStack(), SectionTitle(), SignalIcon(), react

### Community 16 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 17 - "SafetyGate"
Cohesion: 0.33
Nodes (6): Anatomy Drafting Stylus, Cypher Evaluation Gantry, FalkorDB Engine, Policy, SafetyGate, Trip Latch

### Community 18 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 19 - "FalkorDB Safety Layer"
Cohesion: 0.40
Nodes (5): FalkorDB Graph Safety Interlock, FalkorDB Safety Layer, FalkorDB Safety Light Diagram, FalkorDB Blocked State Screenshot, FalkorDB Verified State Screenshot

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "FalkorDB Graph Matrix"
Cohesion: 0.83
Nodes (4): Cypher, FalkorDB Graph Matrix, FalkorDB Safety Layer Light, GraphBLAS

### Community 23 - "dependencies"
Cohesion: 0.67
Nodes (3): dependencies, react, react-dom

## Knowledge Gaps
- **97 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+92 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 230 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `StaticResult` connect `db.py` to `static.py`, `coverage.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _97 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06965174129353234 - nodes in this community are weakly interconnected._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.09490196078431372 - nodes in this community are weakly interconnected._
- **Should `subprocess` be split into smaller, more focused modules?**
  _Cohesion score 0.06533646322378717 - nodes in this community are weakly interconnected._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.07541478129713423 - nodes in this community are weakly interconnected._
- **Should `static.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07396870554765292 - nodes in this community are weakly interconnected._