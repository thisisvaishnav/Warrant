"""Session state tracking for Guard Loop Protection.

Maintains block counts per session in `.guard/state.json` to prevent
infinite agent stop-hook loops (capping consecutive blocks at 3).
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any
from guard.events import get_guard_dir


def _state_file(repo_path: str | Path | None = None) -> Path:
    return get_guard_dir(repo_path) / "session_state.json"


def load_state(repo_path: str | Path | None = None) -> dict[str, Any]:
    """Loads current state dictionary from .guard/session_state.json."""
    sf = _state_file(repo_path)
    if not sf.exists():
        return {"sessions": {}}
    try:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"sessions": {}}
            data.setdefault("sessions", {})
            return data
    except Exception:
        return {"sessions": {}}


def save_state(state: dict[str, Any], repo_path: str | Path | None = None) -> None:
    """Saves state dictionary to .guard/session_state.json safely."""
    try:
        sf = _state_file(repo_path)
        tmp_file = sf.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        tmp_file.replace(sf)
    except Exception:
        pass


def get_session_blocks(session_id: str, repo_path: str | Path | None = None) -> int:
    """Returns the number of consecutive blocks for a session."""
    state = load_state(repo_path)
    session_data = state.get("sessions", {}).get(session_id, {})
    return int(session_data.get("consecutive_blocks", 0))


def record_session_block(session_id: str, repo_path: str | Path | None = None) -> int:
    """Increments and returns the consecutive block count for a session."""
    state = load_state(repo_path)
    sessions = state.setdefault("sessions", {})
    session_data = sessions.setdefault(session_id, {})
    
    current = int(session_data.get("consecutive_blocks", 0)) + 1
    session_data["consecutive_blocks"] = current
    session_data["last_blocked_at"] = time.time()
    
    save_state(state, repo_path)
    return current


def reset_session_blocks(session_id: str, repo_path: str | Path | None = None) -> None:
    """Resets consecutive blocks for a session back to 0."""
    state = load_state(repo_path)
    sessions = state.setdefault("sessions", {})
    if session_id in sessions:
        sessions[session_id]["consecutive_blocks"] = 0
        sessions[session_id]["last_passed_at"] = time.time()
        save_state(state, repo_path)


def get_last_passed_fingerprint(session_id: str, repo_path: str | Path | None = None) -> str | None:
    """Returns the working-tree fingerprint that last passed for this session."""
    state = load_state(repo_path)
    session_data = state.get("sessions", {}).get(session_id, {})
    return session_data.get("last_passed_fingerprint")


def set_last_passed_fingerprint(
    session_id: str,
    fingerprint: str,
    repo_path: str | Path | None = None,
) -> None:
    """Records working-tree fingerprint that passed tests for this session."""
    state = load_state(repo_path)
    sessions = state.setdefault("sessions", {})
    session_data = sessions.setdefault(session_id, {})
    session_data["last_passed_fingerprint"] = fingerprint
    session_data["fingerprint_passed_at"] = time.time()
    save_state(state, repo_path)


def clear_last_passed_fingerprint(session_id: str, repo_path: str | Path | None = None) -> None:
    """Clears cached passed fingerprint when a failure occurs."""
    state = load_state(repo_path)
    sessions = state.setdefault("sessions", {})
    if session_id in sessions and "last_passed_fingerprint" in sessions[session_id]:
        sessions[session_id].pop("last_passed_fingerprint", None)
        save_state(state, repo_path)
