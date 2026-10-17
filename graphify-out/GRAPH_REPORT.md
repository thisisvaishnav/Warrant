# Graph Report - guard  (2026-10-17)

## Corpus Check
- 113 files · ~131,490 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 886 nodes · 1985 edges · 74 communities (37 shown, 37 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 139 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4faf0f0c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- guard_cli/init_cmd.py
- decide
- guard_cli/thin_slice.py
- eval_t2.py
- json
- EmbeddedBackend
- build_safety_figure.mjs
- guard_cli/ingest/coverage.py
- verify_s1.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- mutator.py
- App.tsx
- guard_cli/db.py
- harness.py
- run
- subprocess
- scripts
- pytest
- FigmaSiteConfiguration
- dependencies
- Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`
- sys
- FalkorDB Service
- resolve_backend
- test_integration_init_doctor.py
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
- [0.1.1] - 2026-10-17
- guard_cli/backend.py
- GraphBackend
- StaticResult
- guard_cli/doctor_cmd.py
- guard_cli/api.py
- time
- verify_t1.py
- figma-make-app
- verify_t3.py
- guard-cli
- verify_t4.py
- vercel.json
- verify_t9.py
- find_test_environment

## God Nodes (most connected - your core abstractions)
1. `run_stop_hook()` - 36 edges
2. `resolve_backend()` - 22 edges
3. `GraphBackend` - 21 edges
4. `decide()` - 21 edges
5. `run()` - 20 edges
6. `DockerBackend` - 19 edges
7. `EmbeddedBackend` - 19 edges
8. `check_idle_turn()` - 19 edges
9. `load_state()` - 19 edges
10. `ServerBackend` - 17 edges

## Surprising Connections (you probably didn't know these)
- `1. Scope & Acceptance Criteria Checked` --references--> `DockerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `EmbeddedBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `GraphBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `ServerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `test_server_backend_describe_and_graph()` --uses--> `ServerBackend`  [INFERRED]
  tests/test_backend.py → guard_cli/backend.py

## Import Cycles
- None detected.

## Communities (74 total, 37 thin omitted)

### Community 0 - "guard_cli/init_cmd.py"
Cohesion: 0.10
Nodes (14): check_pytest_cov(), find_repo_root(), record_state(), run_baseline_and_coverage(), run_init(), run_static_ingest(), setup_backend(), write_integrations() (+6 more)

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "guard_cli/thin_slice.py"
Cohesion: 0.08
Nodes (16): check(), _format_reasons(), ChangedFunction, CheckResult, guard_check(), parse_unified_diff(), resolve_changed_functions(), thin_slice_decision() (+8 more)

### Community 3 - "eval_t2.py"
Cohesion: 0.60
Nodes (3): main(), run_capability_evals(), run_regression_evals()

### Community 4 - "json"
Cohesion: 0.06
Nodes (31): _contains_guard_hook(), get_hooks_file_path(), install(), status(), uninstall(), check_all_settings(), _contains_guard_hook(), get_settings_path() (+23 more)

### Community 5 - "EmbeddedBackend"
Cohesion: 0.14
Nodes (6): check_embedded_platform_support(), EmbeddedBackend, test_embedded_import_error_catches_glibc_link_failure(), test_embedded_platform_glibc_below_2_39(), test_embedded_platform_macos_below_15(), test_embedded_platform_non_posix()

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard_cli/ingest/coverage.py"
Cohesion: 0.14
Nodes (10): compute_flakiness(), CoverageResult, ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, _write_to_falkordb() (+2 more)

### Community 8 - "verify_s1.py"
Cohesion: 0.27
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

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

### Community 16 - "guard_cli/db.py"
Cohesion: 0.06
Nodes (40): callers(), covering_tests(), report_miss(), cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback() (+32 more)

### Community 17 - "harness.py"
Cohesion: 0.19
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 18 - "run"
Cohesion: 0.15
Nodes (9): _extract_failures(), normalize_test_target_for_pytest(), run(), check_hook_timeout(), get_hook_timeout(), test_api_run_fail_open_returns_exit_code_zero(), test_doctor_warns_on_slow_suite(), test_hook_timeout_resolution_precedence() (+1 more)

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "pytest"
Cohesion: 0.25
Nodes (6): test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_resolve_backend_preference(), test_server_backend_describe_and_graph()

### Community 23 - "dependencies"
Cohesion: 0.67
Nodes (3): dependencies, react, react-dom

### Community 24 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.33
Nodes (5): 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 25 - "sys"
Cohesion: 0.11
Nodes (4): clean_test_graph(), test_normalize_test_id(), check_feedback_loop(), main()

### Community 56 - "test_api_and_hook.py"
Cohesion: 0.06
Nodes (38): get_guard_dir(), log_event(), read_events(), check_idle_turn(), compute_turn_fingerprint(), format_failure_summary(), is_working_tree_clean(), read_hook_input() (+30 more)

### Community 57 - "[0.1.1] - 2026-10-17"
Cohesion: 0.29
Nodes (6): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, Added, Added, Changed, Changelog

### Community 58 - "guard_cli/backend.py"
Cohesion: 0.15
Nodes (7): get_repo_graph_name(), load_config(), _parse_simple_toml(), save_config(), test_config_save_and_load(), test_repo_graph_name(), test_resolve_backend_with_config()

### Community 59 - "GraphBackend"
Cohesion: 0.10
Nodes (3): GraphBackend, ServerBackend, 1. Scope & Acceptance Criteria Checked

### Community 60 - "StaticResult"
Cohesion: 0.05
Nodes (25): record_miss(), analyze_repo(), _Collector, _decorator_name(), FuncDef, is_test_file(), is_test_function(), module_name() (+17 more)

### Community 61 - "guard_cli/doctor_cmd.py"
Cohesion: 0.11
Nodes (20): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_integrations(), check_target_repo(), CheckResult (+12 more)

### Community 62 - "guard_cli/api.py"
Cohesion: 0.16
Nodes (4): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard()

### Community 63 - "time"
Cohesion: 0.57
Nodes (4): check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main()

### Community 64 - "verify_t1.py"
Cohesion: 0.53
Nodes (3): check_falkordb(), main(), run_flask_suite()

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 66 - "verify_t3.py"
Cohesion: 0.53
Nodes (4): check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main()

### Community 70 - "verify_t4.py"
Cohesion: 0.53
Nodes (4): check_functions_evidence_or_flag(), check_known_covered_functions(), check_suite_runs_and_flakes(), main()

### Community 72 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

## Knowledge Gaps
- **92 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+87 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 375 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBackend` connect `GraphBackend` to `guard_cli/init_cmd.py`, `EmbeddedBackend`, `guard_cli/backend.py`, `resolve_backend`, `guard_cli/doctor_cmd.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _92 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `guard_cli/init_cmd.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1028225806451613 - nodes in this community are weakly interconnected._
- **Why does `analyze_repo()` connect `StaticResult` to `guard_cli/db.py`, `verify_s1.py`, `guard_cli/init_cmd.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `run_stop_hook()` connect `test_api_and_hook.py` to `guard_cli/db.py`, `run`, `subprocess`, `json`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `guard_cli/thin_slice.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08235294117647059 - nodes in this community are weakly interconnected._