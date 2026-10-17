# Graph Report - guard  (2026-10-18)

## Corpus Check
- 131 files · ~143,282 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 53 file(s) not represented in the graph (top: .diff 40, (none) 5, .patch 4)

## Summary
- 1040 nodes · 2347 edges · 84 communities (47 shown, 37 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 141 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fb3d6bb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- guard/__init__.py
- decide
- guard_cli/doctor_cmd.py
- guard_cli/hook.py
- pathlib
- pytest
- build_safety_figure.mjs
- guard_cli/api.py
- guard_cli/thin_slice.py
- compilerOptions
- package.json
- T3: Static graph
- vite.config.ts
- devDependencies
- EyeTracker.tsx
- App.tsx
- guard_cli/cli.py
- harness.py
- guard_cli/agent_integration.py
- subprocess
- scripts
- guard_cli/init_cmd.py
- verify_s1.py
- dependencies
- json
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
- [0.1.2] - 2026-10-18
- resolve_backend
- Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`
- time
- verify_t1.py
- StaticResult
- run_session_start_hook
- run
- figma-make-app
- verify_t4.py
- guard-cli
- guard
- vercel.json
- verify_t9.py
- run_stop_hook
- InstallTabs.tsx
- components.json
- check_idle_turn
- GraphBackend
- guard
- verify_t3.py
- test_api_and_hook.py
- eval_t2.py
- verify_t6.py
- guard_cli/backend.py

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
10. `StaticResult` - 19 edges

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

## Communities (84 total, 37 thin omitted)

### Community 0 - "guard/__init__.py"
Cohesion: 0.15
Nodes (3): clean_test_graph(), test_normalize_test_id(), feedback_test_graph()

### Community 1 - "decide"
Cohesion: 0.08
Nodes (28): Change, compute_trust(), CoveringTest, decide(), Decision, EvidenceEdge, _fresh(), FunctionEvidence (+20 more)

### Community 2 - "guard_cli/doctor_cmd.py"
Cohesion: 0.09
Nodes (22): apply_fixes(), check_backend(), check_environment(), check_freshness(), check_hook_timeout(), check_integrations(), check_target_repo(), CheckResult (+14 more)

### Community 3 - "guard_cli/hook.py"
Cohesion: 0.13
Nodes (16): resolve_diff_ref(), clear_last_passed_fingerprint(), clear_last_verified_sha(), get_baseline_sha(), get_ingest_sha(), get_last_verified_sha(), get_repo_baseline_sha(), get_repo_last_verified_sha() (+8 more)

### Community 4 - "pathlib"
Cohesion: 0.14
Nodes (5): find_repo_root(), test_find_repo_root_invalid(), test_find_repo_root_valid(), test_find_test_environment(), throwaway_repo()

### Community 5 - "pytest"
Cohesion: 0.09
Nodes (14): check_embedded_platform_support(), EmbeddedBackend, test_api_check_strict_mode_raises(), test_docker_backend_describe(), test_embedded_backend_live(), test_embedded_backend_platform_check(), test_embedded_backend_version_gate(), test_repo_graph_name() (+6 more)

### Community 6 - "build_safety_figure.mjs"
Cohesion: 0.13
Nodes (25): at(), body, byDepth(), CARRIAGE, D(), DIAL, L(), MATRIX (+17 more)

### Community 7 - "guard_cli/api.py"
Cohesion: 0.17
Nodes (3): get_covering_tests(), get_graph_state(), get_schema_counts()

### Community 8 - "guard_cli/thin_slice.py"
Cohesion: 0.13
Nodes (11): ChangedFunction, CheckResult, guard_check(), parse_unified_diff(), resolve_changed_functions(), thin_slice_decision(), slice_test_graph(), test_parse_unified_diff() (+3 more)

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

### Community 16 - "guard_cli/cli.py"
Cohesion: 0.05
Nodes (37): callers(), covering_tests(), report_miss(), cmd_callers(), cmd_check(), cmd_covering_tests(), cmd_doctor(), cmd_feedback() (+29 more)

### Community 17 - "harness.py"
Cohesion: 0.18
Nodes (9): apply_mutant(), evaluate_diff(), evaluate_mutant(), main(), reset_repo(), resolve_strategy_tests(), run_evaluation(), run_pytest() (+1 more)

### Community 18 - "guard_cli/agent_integration.py"
Cohesion: 0.26
Nodes (4): apply_patch(), count_collected_tests(), reset_repo(), run_agent_guard()

### Community 19 - "subprocess"
Cohesion: 0.20
Nodes (4): extract_guard_commands(), main(), temp_git_repo(), isolated_git_repo()

### Community 20 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, format, preview

### Community 21 - "guard_cli/init_cmd.py"
Cohesion: 0.13
Nodes (11): check_pytest_cov(), record_state(), run_baseline_and_coverage(), run_init(), run_static_ingest(), setup_backend(), write_integrations(), test_check_pytest_cov() (+3 more)

### Community 22 - "verify_s1.py"
Cohesion: 0.29
Nodes (5): build_function_line_map(), inspect_coverage_mapping(), main(), run_coverage_suite(), run_plain_suite()

### Community 23 - "dependencies"
Cohesion: 0.20
Nodes (10): dependencies, @base-ui/react, class-variance-authority, cn, @fontsource-variable/geist, lucide-react, react, react-dom (+2 more)

### Community 24 - "json"
Cohesion: 0.06
Nodes (37): cmd_hook_install(), cmd_hook_status(), cmd_hook_uninstall(), _contains_guard_hook(), _find_guard_hook(), get_guard_executable(), get_hooks_file_path(), install() (+29 more)

### Community 30 - "test_commit_bypass_fresh_session.py"
Cohesion: 0.20
Nodes (4): _git(), test_committed_mutant_fresh_session_is_not_idle(), test_repo_last_verified_sha_wins_over_fresh_session_head(), test_session_start_records_repo_baseline_once()

### Community 56 - "Verification Reports README"
Cohesion: 0.29
Nodes (8): FalkorDB Logo, Verification Reports README, Task T4 Verification Report, Task T5 Verification Report, Task T5a Verification Report, Task T6 Verification Report, Task T7 Verification Report, Task T8 Verification Report

### Community 57 - "[0.1.2] - 2026-10-18"
Cohesion: 0.18
Nodes (10): [0.1.0] - 2026-10-17, [0.1.1] - 2026-10-17, [0.1.2] - 2026-10-18, Added, Added, Added, Changed, Changed (+2 more)

### Community 58 - "resolve_backend"
Cohesion: 0.11
Nodes (8): load_config(), _parse_simple_toml(), resolve_backend(), save_config(), ServerBackend, get_backend(), test_config_save_and_load(), test_resolve_backend_with_config()

### Community 59 - "Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`"
Cohesion: 0.29
Nodes (6): 1. Scope & Acceptance Criteria Checked, 2. Raw Test Suite Output, 3. Clean-Machine & CLI Verification, 4. Adversarial Fault Injection & Falsification (Rule 5), 5. Protected Files & Git Integrity (Rule 3), Independent Verification Report: Packaging, Backend Layer, `guard init`, and `guard doctor`

### Community 60 - "time"
Cohesion: 0.57
Nodes (4): check_fixtures_exist(), check_guard_check_cli(), check_t0_integration(), main()

### Community 61 - "verify_t1.py"
Cohesion: 0.53
Nodes (3): check_falkordb(), main(), run_flask_suite()

### Community 62 - "StaticResult"
Cohesion: 0.05
Nodes (25): update_graph_meta(), record_miss(), analyze_repo(), _Collector, _decorator_name(), FuncDef, is_test_file(), is_test_function() (+17 more)

### Community 63 - "run_session_start_hook"
Cohesion: 0.31
Nodes (4): _capture_payload(), _git_head_sha(), resolve_hook_context(), run_session_start_hook()

### Community 64 - "run"
Cohesion: 0.11
Nodes (10): check(), _extract_failures(), _format_reasons(), normalize_test_target_for_pytest(), run(), find_test_environment(), test_api_check_fail_open_by_default(), test_api_check_schema_version_and_keys() (+2 more)

### Community 65 - "figma-make-app"
Cohesion: 0.33
Nodes (5): Dependencies, Development Server, figma-make-app, Project Structure, Styling

### Community 66 - "verify_t4.py"
Cohesion: 0.53
Nodes (4): check_functions_evidence_or_flag(), check_known_covered_functions(), check_suite_runs_and_flakes(), main()

### Community 72 - "verify_t9.py"
Cohesion: 0.53
Nodes (4): check_demo_execution(), check_readme_content(), check_report(), main()

### Community 73 - "run_stop_hook"
Cohesion: 0.09
Nodes (17): format_failure_summary(), read_hook_input(), run_stop_hook(), get_session_blocks(), test_antigravity_hook_decision_protocol_continue_on_failure(), test_antigravity_hook_decision_protocol_pass(), _git(), test_item1_baseline_new_conversation_blocks_on_committed_change() (+9 more)

### Community 74 - "InstallTabs.tsx"
Cohesion: 0.19
Nodes (15): Badge(), LABELS, CodeBlock(), copyText(), Agent, initialValue(), InstallSteps(), InstallTabs() (+7 more)

### Community 75 - "components.json"
Cohesion: 0.09
Nodes (21): aliases, components, hooks, lib, ui, utils, iconLibrary, menuAccent (+13 more)

### Community 76 - "check_idle_turn"
Cohesion: 0.16
Nodes (13): check_idle_turn(), compute_turn_fingerprint(), is_working_tree_clean(), get_last_passed_fingerprint(), set_baseline_sha(), set_last_passed_fingerprint(), set_last_verified_sha(), test_committed_flask_mutant_hook_exits_2() (+5 more)

### Community 77 - "GraphBackend"
Cohesion: 0.14
Nodes (4): GraphBackend, check_graph(), test_check_graph_empty(), test_check_graph_populated()

### Community 79 - "verify_t3.py"
Cohesion: 0.53
Nodes (4): check_callers_for_sample_functions(), check_graph_counts_and_dynamic(), check_parser_tests(), main()

### Community 80 - "test_api_and_hook.py"
Cohesion: 0.11
Nodes (9): get_guard_dir(), log_event(), read_events(), test_api_run_fail_open_check_skips_full_suite(), test_event_logging(), test_session_state_and_loop_guard(), test_stop_hook_clean_working_tree_exits_zero(), test_stop_hook_fingerprint_cache_hit_skips_run() (+1 more)

### Community 81 - "eval_t2.py"
Cohesion: 0.60
Nodes (3): main(), run_capability_evals(), run_regression_evals()

### Community 86 - "guard_cli/backend.py"
Cohesion: 0.18
Nodes (5): find_mutation_candidates(), generate_diff(), main(), select_diverse_mutants(), get_repo_graph_name()

## Knowledge Gaps
- **137 isolated node(s):** `PLATE`, `MATRIX`, `NODES`, `CARRIAGE`, `POST` (+132 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 452 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `analyze_repo()` connect `StaticResult` to `guard_cli/cli.py`, `guard_cli/init_cmd.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `PLATE`, `MATRIX`, `NODES` to the rest of the system?**
  _137 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decide` be split into smaller, more focused modules?**
  _Cohesion score 0.08220211161387632 - nodes in this community are weakly interconnected._
- **Why does `StaticResult` connect `StaticResult` to `test_api_and_hook.py`, `eval_t2.py`, `guard_cli/cli.py`, `guard_cli/thin_slice.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Should `guard_cli/doctor_cmd.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09175377468060394 - nodes in this community are weakly interconnected._
- **Why does `run_stop_hook()` connect `run_stop_hook` to `run`, `guard_cli/hook.py`, `check_idle_turn`, `guard_cli/cli.py`, `test_api_and_hook.py`, `subprocess`, `json`, `test_commit_bypass_fresh_session.py`, `run_session_start_hook`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Should `guard_cli/hook.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13213213213213212 - nodes in this community are weakly interconnected._