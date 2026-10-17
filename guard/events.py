"""Append-only local event log for Guard.

Records lifecycle events (hook fired, blocked, passed, handed back, fail-open)
into `.guard/events.jsonl` in the repository root.
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_guard_dir(repo_path: str | Path | None = None) -> Path:
    """Returns the .guard directory path for a repo, ensuring it exists."""
    base = Path(repo_path).resolve() if repo_path else Path.cwd()
    guard_dir = base / ".guard"
    guard_dir.mkdir(parents=True, exist_ok=True)
    return guard_dir


def log_event(
    event: str,
    session_id: str | None = None,
    repo_path: str | Path | None = None,
    details: dict[str, Any] | None = None,
) -> Path | None:
    """Appends an event entry to `.guard/events.jsonl`.
    
    Guaranteed fail-safe: never raises an exception.
    
    Args:
        event: Event name (e.g. 'hook_fired', 'blocked', 'passed', 'handed_back', 'fail_open')
        session_id: Claude Code or agent session identifier
        repo_path: Working directory / repository root
        details: Additional context (selected tests, failures, policy, exit code, etc.)
        
    Returns:
        Path to the events.jsonl file if written, or None on failure.
    """
    try:
        guard_dir = get_guard_dir(repo_path)
        events_file = guard_dir / "events.jsonl"
        
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "session_id": session_id or "unknown",
            "details": details or {},
        }
        
        with open(events_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
            
        return events_file
    except Exception:
        # Event logging must never crash the tool
        return None


def read_events(repo_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Reads all recorded events from `.guard/events.jsonl`."""
    try:
        base = Path(repo_path).resolve() if repo_path else Path.cwd()
        events_file = base / ".guard" / "events.jsonl"
        if not events_file.exists():
            return []
            
        events = []
        with open(events_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events
    except Exception:
        return []
