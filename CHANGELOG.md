# Changelog

All notable changes to Guard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
