# Graph Report - guard  (2026-10-18)

## Corpus Check
- 130 files · ~143,589 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 1044 nodes · 2357 edges · 94 communities (52 shown, 42 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82994b65`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- eval_t2.py
- decide
- test_doctor_cmd.py
- guard_cli/state.py
- antigravity.py
- EmbeddedBackend
- build_safety_figure.mjs
- guard_cli/ingest/coverage.py
- guard_cli/thin_slice.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- EyeTracker.tsx
- App.tsx
- guard_cli/api.py
- harness.py
- guard_check
- re
- scripts
- guard_cli/doctor_cmd.py
- verify_s1.py
- dependencies
- json
- sys
- FalkorDB Service
- resolve_backend
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
- Verification Reports README
- Changelog
- ServerBackend
- guard_cli/backend.py
- subprocess
- verify_t1.py
- guard_cli/ingest/static.py
- Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`
- run
- figma-make-app
- guard_cli/cli.py
- guard-cli
- guard
- vercel.json
- verify_t9.py
- test_api_and_hook.py
- InstallTabs.tsx
- components.json
- guard_cli/hook.py
- GraphBackend
- guard
- verify_t3.py
- os
- run_static_ingest
- callers
- check
- pytest
- FuncDef
- mutator.py
- record_miss
- StaticResult
- test_static.py
- verify_t8.py
- verify_t0.py
- _git
- isolated_git_repo

## God Nodes (most connected - your core abstractions)
1. `run_stop_hook()` - 48 edges
2. `resolve_backend()` - 22 edges
3. `load_state()` - 22 edges
4. `run()` - 21 edges
5. `GraphBackend` - 21 edges
6. `decide()` - 21 edges
7. `check_idle_turn()` - 20 edges
8. `DockerBackend` - 19 edges
9. `EmbeddedBackend` - 19 edges
10. `main()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `1. Scope & Acceptance Criteria Checked` --references--> `GraphBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `ServerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `DockerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `EmbeddedBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `test_server_backend_describe_and_graph()` --uses--> `ServerBackend`  [INFERRED]
  tests/test_backend.py → guard_cli/backend.py

## Import Cycles
- None detected.

## Communities (94 total, 42 thin omitted)

### Community 0 - "eval_t2.py"
Cohesion: 0.11
Nodes (9): main(), run_capability_evals(), run_regression_evals(), clean_test_graph(), feedback_test_graph(), check_functions_evidence_or_flag(), check_known_covered_functions(), check_suite_runs_and_flakes() (+1 more)

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "test_doctor_cmd.py"
Cohesion: 0.11
Nodes (20): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_integrations(), check_target_repo(), CheckResult (+12 more)

### Community 3 - "guard_cli/state.py"
Cohesion: 0.12
Nodes (16): resolve_diff_ref(), clear_last_passed_fingerprint(), clear_last_verified_sha(), get_baseline_sha(), get_ingest_sha(), get_last_verified_sha(), get_repo_baseline_sha(), get_repo_last_verified_sha() (+8 more)

### Community 4 - "antigravity.py"
Cohesion: 0.21
Nodes (10): _contains_guard_hook(), _find_guard_hook(), get_guard_executable(), get_hooks_file_path(), install(), status(), uninstall(), test_antigravity_install_and_status() (+2 more)

### Community 5 - "EmbeddedBackend"
Cohesion: 0.14
Nodes (6): check_embedded_platform_support(), EmbeddedBackend, test_embedded_import_error_catches_glibc_link_failure(), test_embedded_platform_glibc_below_2_39(), test_embedded_platform_macos_below_15(), test_embedded_platform_non_posix()

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard_cli/ingest/coverage.py"
Cohesion: 0.12
Nodes (11): compute_flakiness(), CoverageResult, ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, _write_to_falkordb() (+3 more)

### Community 8 - "guard_cli/thin_slice.py"
Cohesion: 0.14
Nodes (10): ChangedFunction, CheckResult, parse_unified_diff(), resolve_changed_functions(), thin_slice_decision(), slice_test_graph(), test_parse_unified_diff(), test_thin_slice_decision_fallback_on_no_evidence() (+2 more)

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

### Community 14 - "EyeTracker.tsx"
Cohesion: 0.23
Nodes (11): clamp(), Eye, LINES, measure(), outline(), radii, SHAPES, stillness() (+3 more)

### Community 15 - "App.tsx"
Cohesion: 0.17
Nodes (14): App(), Arrow(), GithubIcon(), ProspectStack(), SectionTitle(), SignalIcon(), AgentIcon(), AgentIconProps (+6 more)

### Community 16 - "guard_cli/api.py"
Cohesion: 0.15
Nodes (5): _batches(), get_graph_state(), get_schema_counts(), set_backend(), write_run()

### Community 17 - "harness.py"
Cohesion: 0.18
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 18 - "guard_check"
Cohesion: 0.18
Nodes (5): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard(), guard_check()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "guard_cli/doctor_cmd.py"
Cohesion: 0.11
Nodes (14): check_pytest_cov(), find_repo_root(), find_test_environment(), record_state(), run_baseline_and_coverage(), run_init(), write_integrations(), test_check_pytest_cov() (+6 more)

### Community 22 - "verify_s1.py"
Cohesion: 0.27
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

### Community 23 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+2 more)

### Community 24 - "json"
Cohesion: 0.16
Nodes (11): check_all_settings(), _contains_guard_hook(), get_settings_path(), install(), status(), uninstall(), test_claude_settings_install_creates_file_and_hook(), test_claude_settings_merge_preserves_existing_config() (+3 more)

### Community 30 - "test_commit_bypass_fresh_session.py"
Cohesion: 0.21
Nodes (4): _git(), repo_with_ingest(), test_committed_mutant_fresh_session_is_not_idle(), test_session_start_records_repo_baseline_once()

### Community 56 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 57 - "Changelog"
Cohesion: 0.15
Nodes (12): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, [0.1.2] - 2026-10-18, [0.1.3] - 2026-10-18, Added, Added, Added, Changed (+4 more)

### Community 59 - "guard_cli/backend.py"
Cohesion: 0.13
Nodes (8): get_repo_graph_name(), load_config(), _parse_simple_toml(), save_config(), setup_backend(), test_config_save_and_load(), test_repo_graph_name(), test_resolve_backend_with_config()

### Community 60 - "subprocess"
Cohesion: 0.22
Nodes (11): temp_git_repo(), check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main(), check_feedback_loop(), main(), check_agent_runner_blocks_on_failure() (+3 more)

### Community 61 - "verify_t1.py"
Cohesion: 0.53
Nodes (3): check_falkordb(), main(), run_flask_suite()

### Community 62 - "guard_cli/ingest/static.py"
Cohesion: 0.12
Nodes (6): analyze_repo(), _Collector, _decorator_name(), is_test_file(), module_name(), _resolve_module()

### Community 63 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.29
Nodes (6): 1. Scope & Acceptance Criteria Checked, 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 64 - "run"
Cohesion: 0.15
Nodes (9): _extract_failures(), normalize_test_target_for_pytest(), run(), check_hook_timeout(), get_hook_timeout(), test_api_run_fail_open_returns_exit_code_zero(), test_doctor_warns_on_slow_suite(), test_hook_timeout_resolution_precedence() (+1 more)

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 66 - "guard_cli/cli.py"
Cohesion: 0.22
Nodes (15): cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback(), cmd_hook_install(), cmd_hook_session_start(), cmd_hook_status() (+7 more)

### Community 72 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 73 - "test_api_and_hook.py"
Cohesion: 0.07
Nodes (22): format_failure_summary(), read_hook_input(), run_stop_hook(), get_session_blocks(), record_session_block(), test_antigravity_hook_decision_protocol_continue_on_failure(), test_antigravity_hook_decision_protocol_pass(), test_item1_baseline_new_conversation_blocks_on_committed_change() (+14 more)

### Community 74 - "InstallTabs.tsx"
Cohesion: 0.19
Nodes (15): Badge(), LABELS, CodeBlock(), copyText(), Agent, initialValue(), InstallSteps(), InstallTabs() (+7 more)

### Community 75 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 76 - "guard_cli/hook.py"
Cohesion: 0.12
Nodes (18): get_graph(), _capture_payload(), check_idle_turn(), compute_turn_fingerprint(), _git_head_sha(), is_working_tree_clean(), resolve_hook_context(), run_session_start_hook() (+10 more)

### Community 79 - "verify_t3.py"
Cohesion: 0.53
Nodes (4): check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main()

### Community 80 - "os"
Cohesion: 0.20
Nodes (5): get_guard_dir(), log_event(), read_events(), test_item5_database_down_allows_stop_and_logs_fail_open(), test_event_logging()

### Community 81 - "run_static_ingest"
Cohesion: 0.23
Nodes (7): cmd_ingest_static(), ensure_schema(), reset_graph(), write_static(), run_static_ingest(), seeded_guard_graph(), temp_repo()

### Community 82 - "callers"
Cohesion: 0.18
Nodes (5): callers(), covering_tests(), report_miss(), get_callers(), get_covering_tests()

### Community 83 - "check"
Cohesion: 0.18
Nodes (5): check(), _format_reasons(), test_api_check_fail_open_by_default(), test_api_check_schema_version_and_keys(), test_api_check_strict_mode_raises()

### Community 84 - "pytest"
Cohesion: 0.25
Nodes (6): test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_resolve_backend_preference(), test_server_backend_describe_and_graph()

### Community 85 - "FuncDef"
Cohesion: 0.27
Nodes (6): FuncDef, test_get_callers_multi_hop(), test_graph(), test_write_coverage_and_query_covering_tests(), test_write_run_and_failed_in(), test_write_static_creates_nodes_and_edges()

### Community 86 - "mutator.py"
Cohesion: 0.33
Nodes (4): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants()

### Community 87 - "record_miss"
Cohesion: 0.22
Nodes (5): update_graph_meta(), write_coverage(), record_miss(), test_record_miss_creates_repair_edge(), test_record_miss_elevates_existing_confidence()

### Community 89 - "test_static.py"
Cohesion: 0.46
Nodes (7): make(), test_custom_decorator_flags_dynamic(), test_dynamic_dispatch_is_flagged_not_guessed(), test_same_module_and_cross_module_calls(), test_self_method_calls(), test_syntax_errors_are_reported_not_fatal(), test_test_files_excluded_by_default()

### Community 90 - "verify_t8.py"
Cohesion: 0.43
Nodes (6): check_evaluation_results(), check_failure_case_and_unkillables(), check_frozen_claim(), check_mutant_counts(), check_report_artifact(), main()

### Community 91 - "verify_t0.py"
Cohesion: 0.60
Nodes (3): main(), verify_harness_on_run_all(), verify_split_file()

## Knowledge Gaps
- **138 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+133 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 454 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `StaticResult` connect `StaticResult` to `eval_t2.py`, `guard_cli/ingest/coverage.py`, `guard_cli/thin_slice.py`, `test_api_and_hook.py`, `run_static_ingest`, `FuncDef`, `record_miss`, `guard_cli/ingest/static.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _138 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `eval_t2.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._
- **Why does `analyze_repo()` connect `guard_cli/ingest/static.py` to `guard_cli/cli.py`, `run_static_ingest`, `guard_cli/doctor_cmd.py`, `verify_s1.py`, `StaticResult`, `test_static.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `run_stop_hook()` connect `test_api_and_hook.py` to `run`, `guard_cli/cli.py`, `guard_cli/state.py`, `guard_cli/hook.py`, `os`, `json`, `subprocess`, `test_commit_bypass_fresh_session.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `test_doctor_cmd.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10887096774193548 - nodes in this community are weakly interconnected._