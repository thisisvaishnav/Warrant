# Changelog

All notable changes to Guard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-10-17

### Added
- **PyPI Project Links**: `[project.urls]` block added so the PyPI page links to the repository, issue tracker, and changelog.
- **Antigravity Hook Subcommand Support**: `guard hook install|uninstall|status --antigravity` now manages stop hooks in Antigravity's `.agents/hooks.json` directly from the CLI.

### Changed
- **Antigravity Hook Schema Verification**: `.agents/hooks.json` writer verified against [Antigravity's official hook documentation](https://antigravity.google/docs/hooks). Stop handlers (matcher ignored, direct handler list) and the `{"decision": "continue", "reason": ...}` stdout contract are correct per the published schema; the integration remains **experimental** pending a live-session verification.
- **Claude Code Hook Format Cleanup**: `guard hook install` now writes the canonical Claude Code shape (`{"matcher": "", "hooks": [{type, command, timeout}]}`) under `hooks.Stop`, dropping the stray non-standard top-level `command` key. Status/uninstall still detect the legacy shape written by 0.1.x releases.
- Both the Claude Code and Antigravity Stop-hook integrations are labeled **experimental** in the README until a real live session passes.

### Fixed
- **Commit Bypass via Fresh Session ID (High)**: A new agent session ID no longer reset the diff baseline to the current HEAD, which let a broken commit look like a clean tree and pass the Stop hook. The baseline is now repo-level — `repo.last_verified_sha` (updated on every successful run), falling back to the SHA recorded at ingest in `.guard/state.json` — and is therefore independent of session IDs. The baseline is also recorded as early as possible: a Claude Code `SessionStart` hook and an Antigravity `PreInvocation` hook (agy has no `SessionStart` event per its docs) both run `guard hook session-start`. Regression test `tests/test_commit_bypass_fresh_session.py` commits a mutant under a fresh session ID and asserts exit 2.
- **Fail-open on unavailable database**: When `check()` cannot evaluate the diff (database/graph unreachable), `run()` no longer attempts the full-suite fallback — which could itself fail (and block the agent) on repositories whose own tests require FalkorDB. Guard now allows the stop with a loud stderr warning and records a `fail_open` event, matching the documented fail-open contract. Previously this path could log a `blocked` event carrying `policy: fail_open`.

## [0.1.1] - 2026-10-17

### Changed
- **BREAKING (Library imports)**: Migrated core implementation from top-level `guard` namespace to `guard_cli`. Top-level `guard/` is excluded from published wheels to resolve PyPI namespace collision with the unrelated `guard` package. CLI entry points (`guard` and `guard-cli`) remain unchanged and fully backward compatible. Local shims retained in source repo for legacy test suites.

### Added
- **Commit Bypass Defense**: Track `baseline_sha` and `last_verified_sha` in session state. When an agent commits changes to git, Guard diffs against the last verified commit rather than relying solely on `git status --porcelain`, preventing unverified commits from escaping.
- **Comprehensive Turn Fingerprint**: Turn cache key now binds modified files, staged changes (`git diff --cached`), untracked files, Guard version, and FalkorDB graph generation state to prevent stale cache passes.
- **Multi-Agent Stop Hook Architecture**: Support for Antigravity CLI (`.agents/hooks.json` returning JSON decision protocol `{"decision": "continue"|"stop"}`) alongside Claude Code (`.claude/settings.local.json` exit code 2 / 0).
- **Distinct Event Reasons**: Idle turn events in `.guard/events.jsonl` explicitly record specific reason strings: `clean_tree`, `non_python_only`, and `cached_pass`.
- **Configurable Hook Timeout & Doctor Warning**:
  - Hook timeout configurable via `GUARD_HOOK_TIMEOUT` environment variable or `.guard/config.toml` (`[hook] timeout = ...`).
  - Timeout occurrences log a dedicated `timeout` event in `.guard/events.jsonl`.
  - `guard doctor` warns when baseline test suite duration is near the timeout threshold ($\ge 70\%$).
- **Embedded Platform Compatibility Guard**: Clear, actionable error message (`no embedded build for this platform, use Docker or a server`) when FalkorDBLite embedded backend is used on Linux with glibc < 2.39 or macOS < 15.

## [0.1.0] - 2026-10-17

### Added
- Initial public release of Guard: graph-powered test selection and safety layer for AI coding agents.
- FalkorDB graph backend support: Server (`localhost:6379`), Docker (`guard-falkordb`), and Embedded (`falkordblite`).
- AST diff analyzer and call-graph traversal for Python codebases.
- Per-test dynamic coverage ingestion via pytest and `pytest-cov`.
- Pre-emptive hard safety overrides (touched test files, missing dynamic evidence, dynamic dispatch).
- Continuous Trust Score policy routing: Targeted Subset ($\ge 0.8$), Medium Expansion ($0.5 - 0.8$), and Full Suite fallback ($< 0.5$).
- Claude Code Stop hook integration with loop guard (capped at 3 consecutive blocks) and fail-open resilience.
- Self-healing feedback loop with `guard feedback` for missed test failure repairs.
- CLI commands: `guard init`, `guard doctor`, `guard run`, `guard check`, `guard hook`, `guard feedback`, `guard covering-tests`, `guard stats`.
