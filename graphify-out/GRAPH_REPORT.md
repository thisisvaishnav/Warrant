# Graph Report - Warrant  (2026-10-18)

## Corpus Check
- 128 files · ~140,062 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 1012 nodes · 2252 edges · 84 communities (46 shown, 38 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df876fd1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- subprocess
- decide
- guard_cli/api.py
- guard_cli/state.py
- antigravity.py
- StaticResult
- build_safety_figure.mjs
- guard_cli/ingest/coverage.py
- harness.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- mutator.py
- App.tsx
- guard_cli/cli.py
- verify_s1.py
- get_hook_timeout
- guard/__init__.py
- scripts
- guard_cli/init_cmd.py
- ServerBackend
- dependencies
- guard_cli/integrations/claude.py
- EmbeddedBackend
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
- guard_cli/hook.py
- [0.1.2] - 2026-10-17
- guard_cli/backend.py
- Verification Reports README
- sys
- guard_cli/doctor_cmd.py
- pytest
- EyeTracker.tsx
- verify_t9.py
- figma-make-app
- time
- guard-cli
- verify_t1.py
- Warrant
- Warrant
- test_api_and_hook.py
- InstallTabs.tsx
- components.json
- run_stop_hook
- GraphBackend
- json
- verify_t4.py
- guard_cli/events.py
- verify_t0.py
- isolated_git_repo
- vercel.json

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
- `1. Scope & Acceptance Criteria Checked` --references--> `ServerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `DockerBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `1. Scope & Acceptance Criteria Checked` --references--> `EmbeddedBackend`  [INFERRED]
  reports/verify_packaging_and_init.md → guard_cli/backend.py
- `Fixed` --references--> `check()`  [INFERRED]
  CHANGELOG.md → guard_cli/api.py
- `Fixed` --references--> `run()`  [INFERRED]
  CHANGELOG.md → guard_cli/api.py

## Import Cycles
- None detected.

## Communities (84 total, 38 thin omitted)

### Community 0 - "subprocess"
Cohesion: 0.24
Nodes (5): temp_git_repo(), check_agent_runner_blocks_on_failure(), check_agent_runner_high_trust(), check_agent_runner_low_trust_forces_full(), main()

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "guard_cli/api.py"
Cohesion: 0.05
Nodes (25): Fixed, apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard(), check(), _extract_failures(), _format_reasons() (+17 more)

### Community 3 - "guard_cli/state.py"
Cohesion: 0.13
Nodes (15): resolve_diff_ref(), clear_last_passed_fingerprint(), clear_last_verified_sha(), get_baseline_sha(), get_ingest_sha(), get_last_verified_sha(), get_repo_baseline_sha(), get_repo_last_verified_sha() (+7 more)

### Community 4 - "antigravity.py"
Cohesion: 0.19
Nodes (9): cmd_hook_status(), write_integrations(), _contains_guard_hook(), get_hooks_file_path(), install(), status(), uninstall(), test_antigravity_install_adds_pre_invocation_hook() (+1 more)

### Community 5 - "StaticResult"
Cohesion: 0.06
Nodes (24): record_miss(), analyze_repo(), _Collector, _decorator_name(), FuncDef, is_test_file(), is_test_function(), module_name() (+16 more)

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard_cli/ingest/coverage.py"
Cohesion: 0.11
Nodes (12): compute_flakiness(), CoverageResult, ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, _write_to_falkordb() (+4 more)

### Community 8 - "harness.py"
Cohesion: 0.18
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 9 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution (+10 more)

### Community 10 - "package.json"
Cohesion: 0.12
Nodes (14): name, private, type, version, cn, @fontsource-variable/geist, oxfmt, shadcn (+6 more)

### Community 11 - "T3: Static graph"
Cohesion: 0.23
Nodes (12): S1: SPIKE: per-test coverage, T0: Evaluation harness, T1: Target repo and environment, T2: Schema, T3: Static graph, T4: Coverage evidence, T5: Decision engine, T5a: Thin slice (+4 more)

### Community 12 - "vite.config.ts"
Cohesion: 0.15
Nodes (5): figmaReactRefreshBoundaryFallback(), FigmaSiteConfiguration, @tailwindcss/vite, vite, @vitejs/plugin-react

### Community 13 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, oxfmt, tailwindcss, @tailwindcss/vite, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 14 - "mutator.py"
Cohesion: 0.33
Nodes (4): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants()

### Community 15 - "App.tsx"
Cohesion: 0.36
Nodes (6): App(), Arrow(), ProspectStack(), SectionTitle(), SignalIcon(), react-dom

### Community 16 - "guard_cli/cli.py"
Cohesion: 0.06
Nodes (33): callers(), covering_tests(), report_miss(), cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback() (+25 more)

### Community 17 - "verify_s1.py"
Cohesion: 0.27
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

### Community 18 - "get_hook_timeout"
Cohesion: 0.31
Nodes (5): check_hook_timeout(), get_hook_timeout(), test_doctor_warns_on_slow_suite(), test_hook_timeout_resolution_precedence(), test_timeout_event_logged()

### Community 19 - "guard/__init__.py"
Cohesion: 0.15
Nodes (7): feedback_test_graph(), check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main(), check_feedback_loop(), main()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "guard_cli/init_cmd.py"
Cohesion: 0.11
Nodes (12): check_pytest_cov(), find_repo_root(), find_test_environment(), record_state(), run_baseline_and_coverage(), run_init(), test_check_pytest_cov(), test_find_repo_root_invalid() (+4 more)

### Community 23 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+2 more)

### Community 24 - "guard_cli/integrations/claude.py"
Cohesion: 0.15
Nodes (11): cmd_hook_install(), cmd_hook_uninstall(), check_all_settings(), _contains_guard_hook(), get_settings_path(), install(), status(), uninstall() (+3 more)

### Community 30 - "test_commit_bypass_fresh_session.py"
Cohesion: 0.12
Nodes (6): _git(), repo_with_ingest(), test_committed_mutant_fresh_session_hook_exits_2(), test_committed_mutant_fresh_session_is_not_idle(), test_repo_last_verified_sha_wins_over_fresh_session_head(), test_session_start_records_repo_baseline_once()

### Community 56 - "guard_cli/hook.py"
Cohesion: 0.16
Nodes (13): check_idle_turn(), compute_turn_fingerprint(), is_working_tree_clean(), get_last_passed_fingerprint(), set_baseline_sha(), set_last_passed_fingerprint(), set_last_verified_sha(), test_committed_flask_mutant_hook_exits_2() (+5 more)

### Community 57 - "[0.1.2] - 2026-10-17"
Cohesion: 0.20
Nodes (9): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, [0.1.2] - 2026-10-17, Added, Added, Added, Changed, Changed (+1 more)

### Community 58 - "guard_cli/backend.py"
Cohesion: 0.13
Nodes (8): get_repo_graph_name(), load_config(), _parse_simple_toml(), save_config(), setup_backend(), test_config_save_and_load(), test_repo_graph_name(), test_resolve_backend_with_config()

### Community 59 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 60 - "sys"
Cohesion: 0.13
Nodes (4): main(), run_capability_evals(), run_regression_evals(), throwaway_repo()

### Community 61 - "guard_cli/doctor_cmd.py"
Cohesion: 0.10
Nodes (20): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_integrations(), check_target_repo(), CheckResult (+12 more)

### Community 62 - "pytest"
Cohesion: 0.12
Nodes (11): check_embedded_platform_support(), test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_resolve_backend_preference(), test_server_backend_describe_and_graph(), test_embedded_import_error_catches_glibc_link_failure() (+3 more)

### Community 63 - "EyeTracker.tsx"
Cohesion: 0.23
Nodes (11): clamp(), Eye, EyeTracker(), LINES, measure(), outline(), radii, SHAPES (+3 more)

### Community 64 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 66 - "time"
Cohesion: 0.57
Nodes (4): check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main()

### Community 70 - "verify_t1.py"
Cohesion: 0.53
Nodes (3): check_falkordb(), main(), run_flask_suite()

### Community 73 - "test_api_and_hook.py"
Cohesion: 0.14
Nodes (9): get_session_blocks(), record_session_block(), test_api_run_fail_open_check_skips_full_suite(), test_session_state_and_loop_guard(), test_stop_hook_clean_working_tree_exits_zero(), test_stop_hook_fail_open_on_exception(), test_stop_hook_fails_with_exit_2_and_stderr(), test_stop_hook_loop_guard_caps_at_3_blocks() (+1 more)

### Community 74 - "InstallTabs.tsx"
Cohesion: 0.14
Nodes (22): AgentIcon(), AgentIconProps, Badge(), LABELS, CodeBlock(), copyText(), Agent, ComingSoon() (+14 more)

### Community 75 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 76 - "run_stop_hook"
Cohesion: 0.16
Nodes (7): format_failure_summary(), _git_head_sha(), read_hook_input(), resolve_hook_context(), run_session_start_hook(), run_stop_hook(), test_stop_hook_fingerprint_cache_hit_skips_run()

### Community 77 - "GraphBackend"
Cohesion: 0.11
Nodes (7): GraphBackend, 1. Scope & Acceptance Criteria Checked, 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 78 - "json"
Cohesion: 0.21
Nodes (11): test_antigravity_hook_decision_protocol_continue_on_failure(), test_antigravity_hook_decision_protocol_pass(), test_antigravity_install_and_status(), test_antigravity_preserves_other_hooks_and_uninstalls(), test_claude_settings_merge_preserves_existing_config(), check_evaluation_results(), check_failure_case_and_unkillables(), check_frozen_claim() (+3 more)

### Community 79 - "verify_t4.py"
Cohesion: 0.53
Nodes (4): check_functions_evidence_or_flag(), check_known_covered_functions(), check_suite_runs_and_flakes(), main()

### Community 80 - "guard_cli/events.py"
Cohesion: 0.20
Nodes (4): get_guard_dir(), log_event(), read_events(), test_event_logging()

### Community 81 - "verify_t0.py"
Cohesion: 0.60
Nodes (3): main(), verify_harness_on_run_all(), verify_split_file()

## Knowledge Gaps
- **134 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 440 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `analyze_repo()` connect `StaticResult` to `guard_cli/cli.py`, `verify_s1.py`, `guard_cli/init_cmd.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _134 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `run()` connect `guard_cli/api.py` to `subprocess`, `time`, `test_api_and_hook.py`, `run_stop_hook`, `guard_cli/events.py`, `guard_cli/cli.py`, `get_hook_timeout`, `guard_cli/init_cmd.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `guard_cli/api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0504828797190518 - nodes in this community are weakly interconnected._
- **Why does `EmbeddedBackend` connect `EmbeddedBackend` to `guard_cli/backend.py`, `resolve_backend`, `GraphBackend`, `pytest`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Should `guard_cli/state.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13068181818181818 - nodes in this community are weakly interconnected._