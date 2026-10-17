# Graph Report - Warrant  (2026-10-17)

## Corpus Check
- 103 files · ~126,770 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 52 file(s) not represented in the graph (top: .diff 40, (none) 6, .patch 4)

## Summary
- 810 nodes · 1831 edges · 67 communities (29 shown, 38 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0df3beba`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- EmbeddedBackend
- decide
- subprocess
- guard/state.py
- json
- guard/ingest/static.py
- build_safety_figure.mjs
- guard/ingest/coverage.py
- time
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- mutator.py
- App.tsx
- Verification Reports README
- guard/hook.py
- guard/events.py
- GraphBackend
- scripts
- test_backend.py
- FigmaSiteConfiguration
- dependencies
- Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`
- verify_t9.py
- FalkorDB Service
- temp_repo
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
- test_api_and_hook.py
- guard/db.py
- guard/backend.py
- test_stop_hook_fingerprint_cache_hit_skips_run
- guard/doctor_cmd.py
- resolve_backend
- ServerBackend
- figma-make-app
- guard-cli

## God Nodes (most connected - your core abstractions)
1. `run_stop_hook()` - 24 edges
2. `resolve_backend()` - 23 edges
3. `get_graph()` - 23 edges
4. `decide()` - 23 edges
5. `GraphBackend` - 22 edges
6. `StaticResult` - 22 edges
7. `DockerBackend` - 20 edges
8. `ServerBackend` - 19 edges
9. `Change` - 19 edges
10. `run_doctor()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `1. Scope & Acceptance Criteria Checked` --references--> `GraphBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `ServerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `DockerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `EmbeddedBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard/backend.py
- `Task T4 Verification Report` --references--> `FalkorDB Logo`  [INFERRED]
  reports/verify_t4.md → landing/public/assets/falkordb.svg

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Guard Thin Slice Flow** — plan_t3, plan_t4, plan_t0, plan_t5a [EXTRACTED 0.90]
- **Guard Verification Pipeline** — reports_verify_t4, reports_verify_t5, reports_verify_t5a, reports_verify_t6, reports_verify_t7, reports_verify_t8 [EXTRACTED 1.00]
- **Trust Score Calculation Components** — deviations_t5_metric, plan_t5, readme_concept [INFERRED 0.80]

## Communities (67 total, 38 thin omitted)

### Community 1 - "decide"
Cohesion: 0.09
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "subprocess"
Cohesion: 0.05
Nodes (23): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard(), callers(), check(), covering_tests(), _extract_failures() (+15 more)

### Community 3 - "guard/state.py"
Cohesion: 0.19
Nodes (8): clear_last_passed_fingerprint(), get_last_passed_fingerprint(), load_state(), record_session_block(), reset_session_blocks(), save_state(), set_last_passed_fingerprint(), _state_file()

### Community 4 - "json"
Cohesion: 0.08
Nodes (31): cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback(), cmd_hook_install(), cmd_hook_status(), cmd_hook_stop() (+23 more)

### Community 5 - "guard/ingest/static.py"
Cohesion: 0.09
Nodes (13): analyze_repo(), _Collector, _decorator_name(), is_test_file(), module_name(), _resolve_module(), make(), test_custom_decorator_flags_dynamic() (+5 more)

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard/ingest/coverage.py"
Cohesion: 0.14
Nodes (11): compute_flakiness(), CoverageResult, ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, _write_to_falkordb() (+3 more)

### Community 8 - "time"
Cohesion: 0.06
Nodes (29): main(), run_regression_evals(), apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests() (+21 more)

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

### Community 14 - "mutator.py"
Cohesion: 0.33
Nodes (4): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants()

### Community 15 - "App.tsx"
Cohesion: 0.39
Nodes (6): App(), Arrow(), ProspectStack(), SectionTitle(), SignalIcon(), react

### Community 16 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 17 - "guard/hook.py"
Cohesion: 0.14
Nodes (7): check_idle_turn(), format_failure_summary(), is_working_tree_clean(), read_hook_input(), run_stop_hook(), test_stop_hook_clean_working_tree_exits_zero(), test_stop_hook_non_python_change_skips_run()

### Community 18 - "guard/events.py"
Cohesion: 0.18
Nodes (4): get_guard_dir(), log_event(), read_events(), test_event_logging()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "test_backend.py"
Cohesion: 0.31
Nodes (4): test_api_check_strict_mode_raises(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_resolve_backend_preference()

### Community 23 - "dependencies"
Cohesion: 0.67
Nodes (3): dependencies, react, react-dom

### Community 24 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.29
Nodes (6): 1. Scope & Acceptance Criteria Checked, 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 25 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 56 - "test_api_and_hook.py"
Cohesion: 0.14
Nodes (8): get_session_blocks(), test_api_check_fail_open_by_default(), test_api_check_schema_version_and_keys(), test_api_run_fail_open_returns_exit_code_zero(), test_session_state_and_loop_guard(), test_stop_hook_fail_open_on_exception(), test_stop_hook_fails_with_exit_2_and_stderr(), test_stop_hook_loop_guard_caps_at_3_blocks()

### Community 57 - "guard/db.py"
Cohesion: 0.06
Nodes (39): run_capability_evals(), cmd_ingest_static(), cmd_stats(), _batches(), ensure_schema(), get_backend(), get_callers(), get_covering_tests() (+31 more)

### Community 58 - "guard/backend.py"
Cohesion: 0.12
Nodes (8): get_repo_graph_name(), load_config(), _parse_simple_toml(), save_config(), setup_backend(), test_config_save_and_load(), test_repo_graph_name(), test_resolve_backend_with_config()

### Community 61 - "guard/doctor_cmd.py"
Cohesion: 0.06
Nodes (34): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_integrations(), check_target_repo(), CheckResult (+26 more)

### Community 62 - "resolve_backend"
Cohesion: 0.18
Nodes (3): DockerBackend, resolve_backend(), test_docker_backend_describe()

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

## Knowledge Gaps
- **88 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 351 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBackend` connect `GraphBackend` to `EmbeddedBackend`, `ServerBackend`, `test_backend.py`, `Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor``, `guard/db.py`, `guard/backend.py`, `guard/doctor_cmd.py`, `resolve_backend`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08925979680696662 - nodes in this community are weakly interconnected._
- **Why does `analyze_repo()` connect `guard/ingest/static.py` to `guard/db.py`, `json`, `guard/doctor_cmd.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `subprocess` be split into smaller, more focused modules?**
  _Cohesion score 0.0547945205479452 - nodes in this community are weakly interconnected._
- **Why does `resolve_backend()` connect `resolve_backend` to `EmbeddedBackend`, `ServerBackend`, `time`, `GraphBackend`, `test_backend.py`, `guard/db.py`, `guard/backend.py`, `guard/doctor_cmd.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.0783744557329463 - nodes in this community are weakly interconnected._