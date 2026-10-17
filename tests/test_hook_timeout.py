"""Tests verifying Fix 6: Hook Timeout and Doctor Warning on Slow Suites.

Done when: Doctor warns on a slow suite, timeout is configurable, and timeout events are logged.
"""
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from guard_cli.doctor_cmd import check_hook_timeout
from guard_cli.hook import get_hook_timeout
from guard_cli.api import run as api_run


def test_hook_timeout_resolution_precedence(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    guard_dir = repo / ".guard"
    guard_dir.mkdir()

    # 1. Default fallback
    assert get_hook_timeout(repo) == 180

    # 2. Config from .guard/config.toml
    config_file = guard_dir / "config.toml"
    config_file.write_text("[hook]\ntimeout = 240\n", encoding="utf-8")
    assert get_hook_timeout(repo) == 240

    # 3. Environment variable override
    monkeypatch.setenv("GUARD_HOOK_TIMEOUT", "60")
    assert get_hook_timeout(repo) == 60


def test_doctor_warns_on_slow_suite(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    guard_dir = repo / ".guard"
    guard_dir.mkdir()

    # Case A: Fast baseline run (10s on 180s timeout limit) -> pass
    state_file = guard_dir / "state.json"
    state_file.write_text(json.dumps({"baseline_duration_s": 10.0}), encoding="utf-8")
    res_pass = check_hook_timeout(repo)
    assert res_pass.status == "pass"

    # Case B: Slow baseline run (150s on 180s timeout limit -> 83% of limit) -> warn
    state_file.write_text(json.dumps({"baseline_duration_s": 150.0}), encoding="utf-8")
    res_warn = check_hook_timeout(repo)
    assert res_warn.status == "warn"
    assert "near the hook timeout limit" in res_warn.message
    assert "Increase timeout" in res_warn.fix


def test_timeout_event_logged(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    guard_dir = repo / ".guard"
    guard_dir.mkdir()

    # Mock subprocess.run inside api.py to simulate TimeoutExpired
    with patch("guard_cli.api.check") as mock_check, \
         patch("guard_cli.api.count_collected_tests", return_value=1), \
         patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd=["pytest"], timeout=5.0)):
        mock_check.return_value = {
            "policy": "subset",
            "trust": 0.9,
            "selected_tests": ["test_foo.py::test_bar"],
            "reasons": {},
            "overrides_triggered": [],
            "fallback_reason": None,
            "changed_functions": [],
        }

        report, code = api_run(repo_path=repo, session_id="test_timeout_sess")
        assert code == 124
        assert report["status"] == "failed"
        assert any("timeout_expired" in f for f in report["failures"])

    # Verify event was logged in events.jsonl
    events_file = guard_dir / "events.jsonl"
    assert events_file.exists()
    events = [json.loads(line) for line in events_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    timeout_events = [e for e in events if e.get("event") == "timeout"]
    assert len(timeout_events) >= 1
    t_ev = timeout_events[0]
    assert t_ev["session_id"] == "test_timeout_sess"
    assert "timeout_s" in t_ev["details"]
    assert "duration_s" in t_ev["details"]
