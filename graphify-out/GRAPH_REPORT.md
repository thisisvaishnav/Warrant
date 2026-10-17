# Graph Report - guard  (2026-10-18)

## Corpus Check
- 130 files · ~143,289 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 1046 nodes · 2365 edges · 86 communities (47 shown, 39 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a7e0ccd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- decide
- guard_cli/doctor_cmd.py
- guard_cli/hook.py
- antigravity.py
- EmbeddedBackend
- build_safety_figure.mjs
- ingest_coverage
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- EyeTracker.tsx
- App.tsx
- guard_cli/api.py
- harness.py
- subprocess
- scripts
- run_init
- verify_s1.py
- dependencies
- json
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
- Verification Reports README
- Changelog
- ServerBackend
- guard_cli/init_cmd.py
- time
- verify_t1.py
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
- check_idle_turn
- Any
- guard
- verify_t3.py
- log_event
- run_static_ingest
- get_graph
- check
- pytest
- run_session_start_hook
- StaticResult
- verify_t6.py
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
- `test_repo_graph_name()` --calls--> `get_repo_graph_name()`  [INFERRED]
  tests/test_backend.py → guard_cli/backend.py

## Import Cycles
- None detected.

## Communities (86 total, 39 thin omitted)

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "guard_cli/doctor_cmd.py"
Cohesion: 0.08
Nodes (23): GraphBackend, cmd_doctor(), apply_fixes(), check_backend(), check_environment(), check_freshness(), check_graph(), check_integrations() (+15 more)

### Community 3 - "guard_cli/hook.py"
Cohesion: 0.13
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

### Community 7 - "ingest_coverage"
Cohesion: 0.17
Nodes (8): compute_flakiness(), ingest_coverage(), normalize_test_id(), read_coverage_contexts(), run_pytest_once(), RunResult, test_compute_flakiness(), test_normalize_test_id()

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
Cohesion: 0.09
Nodes (10): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard(), _extract_failures(), _format_reasons(), CheckResult, guard_check() (+2 more)

### Community 17 - "harness.py"
Cohesion: 0.18
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 19 - "subprocess"
Cohesion: 0.27
Nodes (3): extract_guard_commands(), main(), temp_git_repo()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "run_init"
Cohesion: 0.16
Nodes (7): check_pytest_cov(), record_state(), run_baseline_and_coverage(), run_init(), test_check_pytest_cov(), test_record_state(), test_init_then_doctor_e2e()

### Community 22 - "verify_s1.py"
Cohesion: 0.27
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

### Community 23 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+2 more)

### Community 24 - "json"
Cohesion: 0.07
Nodes (29): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants(), cmd_hook_install(), cmd_hook_status(), cmd_hook_uninstall(), write_integrations() (+21 more)

### Community 25 - "sys"
Cohesion: 0.05
Nodes (18): main(), run_capability_evals(), run_regression_evals(), find_repo_root(), ChangedFunction, thin_slice_decision(), test_find_repo_root_invalid(), test_find_repo_root_valid() (+10 more)

### Community 30 - "test_commit_bypass_fresh_session.py"
Cohesion: 0.16
Nodes (5): _git(), repo_with_ingest(), test_committed_mutant_fresh_session_is_not_idle(), test_repo_last_verified_sha_wins_over_fresh_session_head(), test_session_start_records_repo_baseline_once()

### Community 56 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 57 - "Changelog"
Cohesion: 0.13
Nodes (14): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, [0.1.2] - 2026-10-18, [0.1.3] - 2026-10-18, [0.1.4] - 2026-10-18, Added, Added, Added (+6 more)

### Community 59 - "guard_cli/init_cmd.py"
Cohesion: 0.12
Nodes (9): get_repo_graph_name(), load_config(), _parse_simple_toml(), resolve_backend(), save_config(), get_backend(), setup_backend(), test_config_save_and_load() (+1 more)

### Community 60 - "time"
Cohesion: 0.31
Nodes (8): check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main(), check_agent_runner_blocks_on_failure(), check_agent_runner_high_trust(), check_agent_runner_low_trust_forces_full(), main()

### Community 61 - "verify_t1.py"
Cohesion: 0.53
Nodes (3): check_falkordb(), main(), run_flask_suite()

### Community 63 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.29
Nodes (6): 1. Scope & Acceptance Criteria Checked, 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 64 - "run"
Cohesion: 0.18
Nodes (8): normalize_test_target_for_pytest(), run(), check_hook_timeout(), get_hook_timeout(), find_test_environment(), test_doctor_warns_on_slow_suite(), test_hook_timeout_resolution_precedence(), test_timeout_event_logged()

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 66 - "guard_cli/cli.py"
Cohesion: 0.25
Nodes (11): cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_feedback(), cmd_hook_session_start(), cmd_hook_stop(), cmd_ingest_coverage(), cmd_init() (+3 more)

### Community 72 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 73 - "test_api_and_hook.py"
Cohesion: 0.06
Nodes (24): read_events(), format_failure_summary(), read_hook_input(), run_stop_hook(), get_session_blocks(), test_antigravity_hook_decision_protocol_continue_on_failure(), test_antigravity_hook_decision_protocol_pass(), _git() (+16 more)

### Community 74 - "InstallTabs.tsx"
Cohesion: 0.19
Nodes (15): Badge(), LABELS, CodeBlock(), copyText(), Agent, initialValue(), InstallSteps(), InstallTabs() (+7 more)

### Community 75 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 76 - "check_idle_turn"
Cohesion: 0.16
Nodes (13): check_idle_turn(), compute_turn_fingerprint(), is_working_tree_clean(), get_last_passed_fingerprint(), set_baseline_sha(), set_last_passed_fingerprint(), set_last_verified_sha(), test_committed_flask_mutant_hook_exits_2() (+5 more)

### Community 77 - "Any"
Cohesion: 0.16
Nodes (8): _batches(), get_graph_state(), set_backend(), write_coverage(), write_run(), CoverageResult, _write_to_falkordb(), test_coverage_write_to_graph()

### Community 79 - "verify_t3.py"
Cohesion: 0.53
Nodes (4): check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main()

### Community 80 - "log_event"
Cohesion: 0.29
Nodes (3): get_guard_dir(), log_event(), test_event_logging()

### Community 81 - "run_static_ingest"
Cohesion: 0.16
Nodes (9): cmd_ingest_static(), ensure_schema(), get_schema_counts(), reset_graph(), update_graph_meta(), write_static(), run_static_ingest(), seeded_guard_graph() (+1 more)

### Community 82 - "get_graph"
Cohesion: 0.18
Nodes (6): callers(), covering_tests(), report_miss(), get_callers(), get_covering_tests(), get_graph()

### Community 83 - "check"
Cohesion: 0.29
Nodes (3): check(), test_api_check_fail_open_by_default(), test_api_check_schema_version_and_keys()

### Community 84 - "pytest"
Cohesion: 0.11
Nodes (11): test_api_check_strict_mode_raises(), test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_repo_graph_name(), test_resolve_backend_preference(), clean_test_graph() (+3 more)

### Community 86 - "run_session_start_hook"
Cohesion: 0.31
Nodes (4): _capture_payload(), _git_head_sha(), resolve_hook_context(), run_session_start_hook()

### Community 88 - "StaticResult"
Cohesion: 0.06
Nodes (23): record_miss(), analyze_repo(), _Collector, _decorator_name(), FuncDef, is_test_file(), is_test_function(), module_name() (+15 more)

## Knowledge Gaps
- **139 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+134 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 455 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_stop_hook()` connect `test_api_and_hook.py` to `run`, `pathlib`, `guard_cli/cli.py`, `guard_cli/hook.py`, `check_idle_turn`, `log_event`, `subprocess`, `run_session_start_hook`, `json`, `test_commit_bypass_fresh_session.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _139 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `GraphBackend` connect `guard_cli/doctor_cmd.py` to `EmbeddedBackend`, `guard_cli/init_cmd.py`, `run_static_ingest`, `run_init`, `ServerBackend`, `DockerBackend`, `Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor``?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `guard_cli/doctor_cmd.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0824524312896406 - nodes in this community are weakly interconnected._
- **Why does `DockerBackend` connect `DockerBackend` to `guard_cli/doctor_cmd.py`, `pytest`, `ServerBackend`, `guard_cli/init_cmd.py`, `Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor``?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `guard_cli/hook.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13213213213213212 - nodes in this community are weakly interconnected._