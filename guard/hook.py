"""Claude Code Stop Hook Adapter (Phase 1).

Executes when Claude Code attempts to stop/complete a turn:
1. Reads session info from stdin JSON.
2. Checks git diff; if working tree is clean, exits 0 immediately (idle turn).
3. Enforces loop guard: after 3 consecutive blocks, hands back control (exits 0).
4. Runs Guard's test selection via `guard.api.run()`.
5. On failure, outputs <= 30 line summary to stderr and exits 2 (blocking error).
6. Fail-open by default if Guard itself crashes.
"""
from __future__ import annotations
import json
import sys
import subprocess
from pathlib import Path
from typing import Any

import hashlib
from guard import api
from guard.events import log_event
from guard.state import (
    get_session_blocks,
    record_session_block,
    reset_session_blocks,
    get_last_passed_fingerprint,
    set_last_passed_fingerprint,
    clear_last_passed_fingerprint,
)


def read_hook_input() -> dict[str, Any]:
    """Reads stdin JSON safely if available."""
    if sys.stdin.isatty():
        return {}
    try:
        content = sys.stdin.read().strip()
        if not content:
            return {}
        data = json.loads(content)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def is_working_tree_clean(repo_path: Path) -> bool:
    """Returns True if the git working tree has no changes."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=5.0,
        )
        if proc.returncode == 0 and not proc.stdout.strip():
            return True
        return False
    except Exception:
        return False


def check_idle_turn(repo_path: Path, session_id: str = "default_session") -> tuple[bool, str, str | None]:
    """Checks whether the current turn is an idle turn that can skip test runs.
    
    Returns:
        (is_idle: bool, reason: str, fingerprint: str | None)
    """
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=5.0,
        )
        if proc.returncode != 0:
            return False, "git_status_error", None
            
        stdout = proc.stdout
        lines = [l for l in stdout.splitlines() if l.strip()]
        if not lines:
            return True, "clean_working_tree", None

        # Parse changed files to check for python files
        py_files: list[str] = []
        for line in lines:
            path_part = line[3:].strip()
            if " -> " in path_part:
                sub_paths = [p.strip() for p in path_part.split(" -> ")]
            else:
                sub_paths = [path_part]
                
            for sp in sub_paths:
                # Ignore .guard internal files if any
                norm = sp.replace("\\", "/")
                if norm.startswith(".guard/") or norm == ".guard":
                    continue
                if norm.endswith(".py"):
                    py_files.append(norm)

        # If no Python files were touched, skip running tests
        if not py_files:
            return True, "non_python_changes_only", None

        # Determine git HEAD SHA
        head_sha = ""
        try:
            head_proc = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                timeout=5.0,
            )
            if head_proc.returncode == 0:
                head_sha = head_proc.stdout.strip()
        except Exception:
            pass

        # Compute working-tree fingerprint
        raw_key = f"{head_sha}\n{stdout}"
        fingerprint = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]

        last_passed = get_last_passed_fingerprint(session_id, repo_path=repo_path)
        if last_passed and last_passed == fingerprint:
            return True, "fingerprint_cache_hit", fingerprint

        return False, "python_files_modified", fingerprint
    except Exception as exc:
        return False, f"error_{exc}", None


def format_failure_summary(report: dict[str, Any], max_lines: int = 30) -> str:
    """Formats a concise <= 30 line error summary for Claude's context."""
    lines = [
        "GUARD SAFETY CHECK FAILED (Exit 2 - Blocking Stop)",
        "==================================================",
        f"Trust Policy : {report.get('policy', 'unknown')} (Trust Score: {report.get('trust', 0.0):.2f})",
    ]
    
    overrides = report.get("overrides_triggered", [])
    if overrides:
        lines.append(f"Overrides    : {', '.join(overrides)}")
        
    reason = report.get("fallback_reason")
    if reason:
        lines.append(f"Reason       : {reason}")
        
    lines.append(f"Tests Run    : {report.get('tests_run_count', 0)}")
    
    failures = report.get("failures", [])
    if failures:
        lines.append("Failing Tests:")
        for f in failures[:12]:
            lines.append(f"  - {f}")
        if len(failures) > 12:
            lines.append(f"  ... and {len(failures) - 12} additional failures")
            
    summary = report.get("output_summary")
    if summary:
        lines.append(f"Summary      : {summary}")
        
    lines.append("--------------------------------------------------")
    lines.append("Fix the failing tests above before completing this task.")
    
    return "\n".join(lines[:max_lines]) + "\n"


def run_stop_hook(
    repo_override: str | Path | None = None,
    strict: bool = False,
    raw_input: dict[str, Any] | None = None,
) -> int:
    """Executes the Claude Code Stop hook workflow.
    
    Returns:
        0 on pass, clean tree, or loop-cap hand back (allow stop)
        2 on test failure (block stop)
    """
    hook_input = raw_input if raw_input is not None else read_hook_input()
    session_id = hook_input.get("session_id", "default_session")
    
    # Resolve working directory
    input_cwd = hook_input.get("cwd")
    if repo_override:
        cwd = Path(repo_override).resolve()
    elif input_cwd:
        cwd = Path(input_cwd).resolve()
    else:
        cwd = Path.cwd()

    stop_hook_active = bool(hook_input.get("stop_hook_active", False))

    # Log hook entry
    log_event(
        event="hook_fired",
        session_id=session_id,
        repo_path=cwd,
        details={"stop_hook_active": stop_hook_active},
    )

    # 1. Idle turn check: If working tree is clean, non-python only, or fingerprint cache hit
    is_idle, idle_reason, fingerprint = check_idle_turn(cwd, session_id=session_id)
    if is_idle or is_working_tree_clean(cwd):
        log_event(
            event="idle_turn",
            session_id=session_id,
            repo_path=cwd,
            details={"reason": idle_reason, "fingerprint": fingerprint},
        )
        return 0

    # 2. Loop guard check: Cap at 3 consecutive blocks
    prior_blocks = get_session_blocks(session_id, repo_path=cwd)
    if prior_blocks >= 3:
        msg = "Guard blocked 3 times, handing back to you\n"
        sys.stderr.write(msg)
        log_event(
            event="handed_back",
            session_id=session_id,
            repo_path=cwd,
            details={"consecutive_blocks": prior_blocks},
        )
        return 0

    # 3. Execute Guard run
    try:
        report, exit_code = api.run(
            repo_path=cwd,
            strict=strict,
            session_id=session_id,
        )
    except Exception as exc:
        if strict:
            sys.stderr.write(f"Guard error (strict): {exc}\n")
            return 2
        sys.stderr.write(f"Warning: Guard encountered an error: {exc}. Failing open.\n")
        log_event(
            event="fail_open",
            session_id=session_id,
            repo_path=cwd,
            details={"error": str(exc)},
        )
        return 0

    # 4. Handle test results
    if exit_code == 0:
        reset_session_blocks(session_id, repo_path=cwd)
        if fingerprint:
            set_last_passed_fingerprint(session_id, fingerprint, repo_path=cwd)
        return 0

    # Test failure: clear cached fingerprint and increment blocks
    clear_last_passed_fingerprint(session_id, repo_path=cwd)
    new_blocks = record_session_block(session_id, repo_path=cwd)
    if new_blocks >= 3:
        msg = "Guard blocked 3 times, handing back to you\n"
        sys.stderr.write(msg)
        log_event(
            event="handed_back",
            session_id=session_id,
            repo_path=cwd,
            details={"consecutive_blocks": new_blocks},
        )
        return 0

    # Format failure summary <= 30 lines to stderr
    summary_text = format_failure_summary(report, max_lines=30)
    sys.stderr.write(summary_text)
    
    log_event(
        event="blocked",
        session_id=session_id,
        repo_path=cwd,
        details={
            "consecutive_blocks": new_blocks,
            "policy": report.get("policy"),
            "failures": report.get("failures", []),
        },
    )
    return 2
