"""Tests for Antigravity CLI (.agents/hooks.json) hook integration and protocol contract.

Validates:
1. Installation and status reporting in .agents/hooks.json.
2. Uninstallation and preservation of other configured hooks.
3. Hook decision protocol:
   - On test failure: stdout contains {"decision": "continue", "reason": "..."}, exit code 0.
   - On test pass / clean tree: stdout contains {"decision": "stop"}, exit code 0.
"""
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from guard_cli.integrations import antigravity
from guard_cli.hook import run_stop_hook


def test_antigravity_install_and_status(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    # Initial status -> not installed
    st = antigravity.status(repo)
    assert st["installed"] is False

    # Install hook
    ok, msg = antigravity.install(repo)
    assert ok is True
    assert "Successfully installed" in msg

    # Verify status -> installed
    st = antigravity.status(repo)
    assert st["installed"] is True
    assert st["hook_name"] == "guard-stop"

    # Verify file content
    hooks_file = repo / ".agents" / "hooks.json"
    assert hooks_file.exists()
    data = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert "guard-stop" in data
    assert "Stop" in data["guard-stop"]
    handlers = data["guard-stop"]["Stop"]
    assert len(handlers) == 1
    assert handlers[0]["type"] == "command"
    assert handlers[0]["command"] == "guard hook stop"
    assert handlers[0]["timeout"] == 180

    # Idempotent re-install
    ok2, msg2 = antigravity.install(repo)
    assert ok2 is True
    assert "already installed" in msg2


def test_antigravity_preserves_other_hooks_and_uninstalls(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    agents_dir = repo / ".agents"
    agents_dir.mkdir()
    hooks_file = agents_dir / "hooks.json"

    # Write other hook
    initial_data = {
        "user-linter": {
            "Stop": [{"type": "command", "command": "flake8"}]
        }
    }
    hooks_file.write_text(json.dumps(initial_data), encoding="utf-8")

    # Install Guard
    ok, _ = antigravity.install(repo)
    assert ok is True

    # Both hooks present
    data = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert "user-linter" in data
    assert "guard-stop" in data

    # Uninstall Guard
    ok_un, msg_un = antigravity.uninstall(repo)
    assert ok_un is True

    data_after = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert "user-linter" in data_after
    assert "guard-stop" not in data_after


def test_antigravity_hook_decision_protocol_pass(tmp_path, capsys):
    repo = tmp_path / "repo"
    repo.mkdir()

    raw_input = {
        "conversationId": "conv-test-1234",
        "workspacePaths": [str(repo)],
        "terminationReason": "goal_achieved",
        "fullyIdle": True,
    }

    with patch("guard_cli.hook.check_idle_turn", return_value=(True, "clean_tree", None, "sha1")):
        exit_code = run_stop_hook(repo_override=repo, raw_input=raw_input)
        assert exit_code == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out.strip().splitlines()[-1])
    assert payload.get("decision") == "stop"


def test_antigravity_hook_decision_protocol_continue_on_failure(tmp_path, capsys):
    repo = tmp_path / "repo"
    repo.mkdir()

    raw_input = {
        "conversationId": "conv-test-1234",
        "workspacePaths": [str(repo)],
        "terminationReason": "goal_achieved",
        "fullyIdle": True,
    }

    mock_report = {
        "status": "failed",
        "policy": "subset",
        "trust": 0.85,
        "tests_run_count": 2,
        "failures": ["tests/test_core.py::test_failing_case"],
        "output_summary": "1 failed, 1 passed",
    }

    with patch("guard_cli.hook.check_idle_turn", return_value=(False, "python_files_modified", "fp1", "sha1")), \
         patch("guard_cli.hook.get_session_blocks", return_value=0), \
         patch("guard_cli.api.run", return_value=(mock_report, 1)):
        exit_code = run_stop_hook(repo_override=repo, strict=True, raw_input=raw_input)
        # Antigravity expects exit code 0 with decision: continue
        assert exit_code == 0

    captured = capsys.readouterr()
    out_lines = [l for l in captured.out.strip().splitlines() if l.strip()]
    payload = json.loads(out_lines[-1])
    assert payload.get("decision") == "continue"
    assert "GUARD SAFETY CHECK FAILED" in payload.get("reason", "")
    assert "tests/test_core.py::test_failing_case" in payload.get("reason", "")
