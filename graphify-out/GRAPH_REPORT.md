# Graph Report - guard  (2026-10-17)

## Corpus Check
- 123 files · ~136,573 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 994 nodes · 2229 edges · 90 communities (52 shown, 38 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a358f2b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- guard_cli/doctor_cmd.py
- decide
- guard_cli/api.py
- guard_cli/state.py
- install
- pytest
- build_safety_figure.mjs
- guard_cli/ingest/coverage.py
- guard_cli/thin_slice.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- guard_cli/cli.py
- App.tsx
- guard_cli/db.py
- harness.py
- run
- subprocess
- scripts
- test_init_cmd.py
- verify_t6.py
- dependencies
- install
- sys
- FalkorDB Service
- DockerBackend
- test_commit_bypass_fresh_session.py
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
- check_idle_turn
- [0.1.2] - 2026-10-17
- resolve_backend
- Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`
- _Collector
- test_doctor_cmd.py
- guard_cli/agent_integration.py
- time
- verify_t1.py
- figma-make-app
- verify_t3.py
- guard-cli
- verify_t4.py
- vercel.json
- verify_t9.py
- test_api_and_hook.py
- InstallTabs.tsx
- components.json
- guard_cli/hook.py
- GraphBackend
- json
- StaticResult
- log_event
- eval_t2.py
- FuncDef
- Verification Reports README
- verify_s1.py
- guard_cli/ingest/static.py
- mutator.py
- test_static.py
- verify_t8.py
- CodeBlock.tsx

## God Nodes (most connected - your core abstractions)
1. `run_stop_hook()` - 40 edges
2. `run()` - 22 edges
3. `resolve_backend()` - 22 edges
4. `load_state()` - 22 edges
5. `GraphBackend` - 21 edges
6. `decide()` - 21 edges
7. `check_idle_turn()` - 20 edges
8. `DockerBackend` - 19 edges
9. `EmbeddedBackend` - 19 edges
10. `StaticResult` - 19 edges

## Surprising Connections (you probably didn't know these)
- `1. Scope & Acceptance Criteria Checked` --references--> `DockerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `EmbeddedBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `Fixed` --references--> `check()`  [INFERRED]
  CHANGELOG.md → guard_cli/api.py
- `Fixed` --references--> `run()`  [INFERRED]
  CHANGELOG.md → guard_cli/api.py
- `test_repo_graph_name()` --calls--> `get_repo_graph_name()`  [INFERRED]
  tests/test_backend.py → guard_cli/backend.py

## Import Cycles
- None detected.

## Communities (90 total, 38 thin omitted)

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "guard_cli/api.py"
Cohesion: 0.17
Nodes (5): _extract_failures(), _format_reasons(), normalize_test_target_for_pytest(), find_test_environment(), CheckResult

### Community 3 - "guard_cli/state.py"
Cohesion: 0.15
Nodes (12): get_guard_dir(), clear_last_passed_fingerprint(), clear_last_verified_sha(), get_last_passed_fingerprint(), get_last_verified_sha(), get_repo_last_verified_sha(), get_repo_state(), load_state() (+4 more)

### Community 4 - "install"
Cohesion: 0.20
Nodes (9): cmd_hook_install(), cmd_hook_status(), cmd_hook_uninstall(), _contains_guard_hook(), get_hooks_file_path(), install(), status(), uninstall() (+1 more)

### Community 5 - "pytest"
Cohesion: 0.09
Nodes (14): check_embedded_platform_support(), EmbeddedBackend, test_api_check_strict_mode_raises(), test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_repo_graph_name() (+6 more)

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard_cli/ingest/coverage.py"
Cohesion: 0.13
Nodes (7): compute_flakiness(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, test_compute_flakiness(), test_normalize_test_id()

### Community 8 - "guard_cli/thin_slice.py"
Cohesion: 0.15
Nodes (10): ChangedFunction, guard_check(), parse_unified_diff(), resolve_changed_functions(), thin_slice_decision(), slice_test_graph(), test_parse_unified_diff(), test_thin_slice_decision_fallback_on_no_evidence() (+2 more)

### Community 9 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+10 more)

### Community 10 - "package.json"
Cohesion: 0.11
Nodes (16): name, private, type, version, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist (+8 more)

### Community 11 - "T3: Static graph"
Cohesion: 0.23
Nodes (12): S1: SPIKE: per-test coverage, T0: Evaluation harness, T1: Target repo and environment, T2: Schema, T3: Static graph, T4: Coverage evidence, T5: Decision engine, T5a: Thin slice (+4 more)

### Community 12 - "vite.config.ts"
Cohesion: 0.15
Nodes (5): figmaReactRefreshBoundaryFallback(), FigmaSiteConfiguration, @tailwindcss/vite, vite, @vitejs/plugin-react

### Community 13 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, oxfmt, tailwindcss, @tailwindcss/vite, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 14 - "guard_cli/cli.py"
Cohesion: 0.14
Nodes (18): callers(), covering_tests(), report_miss(), cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback() (+10 more)

### Community 15 - "App.tsx"
Cohesion: 0.33
Nodes (7): App(), Arrow(), ProspectStack(), SectionTitle(), SignalIcon(), react, react-dom

### Community 16 - "guard_cli/db.py"
Cohesion: 0.07
Nodes (19): _batches(), ensure_schema(), get_backend(), get_callers(), get_covering_tests(), get_graph_state(), get_schema_counts(), reset_graph() (+11 more)

### Community 17 - "harness.py"
Cohesion: 0.18
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 18 - "run"
Cohesion: 0.15
Nodes (8): Fixed, check(), run(), test_api_check_fail_open_by_default(), test_api_check_schema_version_and_keys(), test_api_run_fail_open_returns_exit_code_zero(), test_hook_timeout_resolution_precedence(), test_timeout_event_logged()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "test_init_cmd.py"
Cohesion: 0.12
Nodes (12): check_pytest_cov(), find_repo_root(), record_state(), run_baseline_and_coverage(), run_init(), write_integrations(), test_check_pytest_cov(), test_find_repo_root_invalid() (+4 more)

### Community 23 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+2 more)

### Community 24 - "install"
Cohesion: 0.16
Nodes (10): check_all_settings(), _contains_guard_hook(), get_settings_path(), install(), status(), uninstall(), test_claude_settings_install_creates_file_and_hook(), test_claude_settings_merge_preserves_existing_config() (+2 more)

### Community 30 - "test_commit_bypass_fresh_session.py"
Cohesion: 0.14
Nodes (5): _git(), repo_with_ingest(), test_committed_mutant_fresh_session_is_not_idle(), test_repo_last_verified_sha_wins_over_fresh_session_head(), test_session_start_records_repo_baseline_once()

### Community 56 - "check_idle_turn"
Cohesion: 0.19
Nodes (11): check_idle_turn(), is_working_tree_clean(), set_baseline_sha(), set_last_passed_fingerprint(), set_last_verified_sha(), test_committed_flask_mutant_hook_exits_2(), read_last_event(), test_event_reason_cached_pass() (+3 more)

### Community 57 - "[0.1.2] - 2026-10-17"
Cohesion: 0.20
Nodes (9): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, [0.1.2] - 2026-10-17, Added, Added, Added, Changed, Changed (+1 more)

### Community 58 - "resolve_backend"
Cohesion: 0.18
Nodes (8): get_repo_graph_name(), load_config(), _parse_simple_toml(), resolve_backend(), save_config(), setup_backend(), test_config_save_and_load(), test_resolve_backend_with_config()

### Community 59 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.33
Nodes (5): 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 61 - "test_doctor_cmd.py"
Cohesion: 0.09
Nodes (20): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_hook_timeout(), check_integrations(), check_target_repo() (+12 more)

### Community 62 - "guard_cli/agent_integration.py"
Cohesion: 0.26
Nodes (4): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard()

### Community 63 - "time"
Cohesion: 0.31
Nodes (8): check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main(), check_agent_runner_blocks_on_failure(), check_agent_runner_high_trust(), check_agent_runner_low_trust_forces_full(), main()

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

### Community 73 - "test_api_and_hook.py"
Cohesion: 0.11
Nodes (12): run_stop_hook(), get_session_blocks(), record_session_block(), test_api_run_fail_open_check_skips_full_suite(), test_session_state_and_loop_guard(), test_stop_hook_clean_working_tree_exits_zero(), test_stop_hook_fail_open_on_exception(), test_stop_hook_fails_with_exit_2_and_stderr() (+4 more)

### Community 74 - "InstallTabs.tsx"
Cohesion: 0.19
Nodes (16): AgentIcon(), AgentIconProps, Badge(), LABELS, Agent, ComingSoon(), initialValue(), InstallSteps() (+8 more)

### Community 75 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 76 - "guard_cli/hook.py"
Cohesion: 0.14
Nodes (11): compute_turn_fingerprint(), format_failure_summary(), _git_head_sha(), read_hook_input(), resolve_diff_ref(), resolve_hook_context(), run_session_start_hook(), get_baseline_sha() (+3 more)

### Community 77 - "GraphBackend"
Cohesion: 0.12
Nodes (3): GraphBackend, ServerBackend, 1. Scope & Acceptance Criteria Checked

### Community 78 - "json"
Cohesion: 0.21
Nodes (10): run_doctor(), test_antigravity_hook_decision_protocol_continue_on_failure(), test_antigravity_hook_decision_protocol_pass(), test_antigravity_install_and_status(), test_antigravity_preserves_other_hooks_and_uninstalls(), test_run_doctor_json_mode(), test_init_then_doctor_e2e(), main() (+2 more)

### Community 79 - "StaticResult"
Cohesion: 0.19
Nodes (5): record_miss(), is_test_function(), StaticResult, test_record_miss_creates_repair_edge(), test_record_miss_elevates_existing_confidence()

### Community 80 - "log_event"
Cohesion: 0.32
Nodes (3): log_event(), read_events(), test_event_logging()

### Community 81 - "eval_t2.py"
Cohesion: 0.14
Nodes (5): main(), run_capability_evals(), run_regression_evals(), clean_test_graph(), feedback_test_graph()

### Community 82 - "FuncDef"
Cohesion: 0.27
Nodes (6): FuncDef, test_get_callers_multi_hop(), test_graph(), test_write_coverage_and_query_covering_tests(), test_write_run_and_failed_in(), test_write_static_creates_nodes_and_edges()

### Community 83 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 84 - "verify_s1.py"
Cohesion: 0.29
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

### Community 85 - "guard_cli/ingest/static.py"
Cohesion: 0.33
Nodes (4): analyze_repo(), is_test_file(), module_name(), _resolve_module()

### Community 86 - "mutator.py"
Cohesion: 0.33
Nodes (4): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants()

### Community 87 - "test_static.py"
Cohesion: 0.46
Nodes (7): make(), test_custom_decorator_flags_dynamic(), test_dynamic_dispatch_is_flagged_not_guessed(), test_same_module_and_cross_module_calls(), test_self_method_calls(), test_syntax_errors_are_reported_not_fatal(), test_test_files_excluded_by_default()

### Community 88 - "verify_t8.py"
Cohesion: 0.43
Nodes (6): check_evaluation_results(), check_failure_case_and_unkillables(), check_frozen_claim(), check_mutant_counts(), check_report_artifact(), main()

### Community 89 - "CodeBlock.tsx"
Cohesion: 0.67
Nodes (3): CodeBlock(), copyText(), lucide-react

## Knowledge Gaps
- **126 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 430 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GraphBackend` connect `GraphBackend` to `guard_cli/doctor_cmd.py`, `pytest`, `guard_cli/db.py`, `test_init_cmd.py`, `resolve_backend`, `DockerBackend`, `test_doctor_cmd.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _126 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `run()` connect `run` to `guard_cli/doctor_cmd.py`, `guard_cli/api.py`, `test_api_and_hook.py`, `guard_cli/cli.py`, `log_event`, `subprocess`, `guard_cli/agent_integration.py`, `time`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `pytest` be split into smaller, more focused modules?**
  _Cohesion score 0.08708708708708708 - nodes in this community are weakly interconnected._
- **Why does `run_stop_hook()` connect `test_api_and_hook.py` to `guard_cli/state.py`, `guard_cli/hook.py`, `guard_cli/cli.py`, `json`, `log_event`, `run`, `subprocess`, `check_idle_turn`, `test_commit_bypass_fresh_session.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `build_safety_figure.mjs` be split into smaller, more focused modules?**
  _Cohesion score 0.1310344827586207 - nodes in this community are weakly interconnected._