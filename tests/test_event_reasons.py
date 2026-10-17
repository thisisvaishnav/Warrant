"""Tests verifying Fix 5: Event Reasons separation.

Done when: Each case (clean_tree, non_python_only, cached_pass) logs its own reason.
"""
import json
import subprocess
from pathlib import Path
import pytest

from guard_cli.hook import run_stop_hook, check_idle_turn
from guard_cli.state import set_last_passed_fingerprint, set_baseline_sha, set_last_verified_sha


def read_last_event(repo_dir: Path) -> dict:
    events_file = repo_dir / ".guard" / "events.jsonl"
    assert events_file.exists(), "events.jsonl was not created"
    lines = [l for l in events_file.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) > 0, "events.jsonl is empty"
    return json.loads(lines[-1])


@pytest.fixture
def temp_git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=str(repo), check=True)

    app_py = repo / "app.py"
    app_py.write_text("def hello():\n    return 'world'\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=str(repo), check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=str(repo), check=True)

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo), capture_output=True, text=True).stdout.strip()
    return repo, head


def test_event_reason_clean_tree(temp_git_repo):
    repo, head_sha = temp_git_repo
    session_id = "test_clean_tree_sess"

    set_baseline_sha(session_id, head_sha, repo_path=repo)
    set_last_verified_sha(session_id, head_sha, repo_path=repo)

    # 1. Clean tree check
    is_idle, reason, _, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is True
    assert reason == "clean_tree"

    # Stop hook runs and logs event
    exit_code = run_stop_hook(
        repo_override=repo,
        raw_input={"session_id": session_id, "cwd": str(repo)},
    )
    assert exit_code == 0

    event = read_last_event(repo)
    assert event["event"] == "idle_turn"
    assert event["details"]["reason"] == "clean_tree"


def test_event_reason_non_python_only(temp_git_repo):
    repo, head_sha = temp_git_repo
    session_id = "test_non_py_sess"

    set_baseline_sha(session_id, head_sha, repo_path=repo)
    set_last_verified_sha(session_id, head_sha, repo_path=repo)

    # Modify only non-python file
    readme = repo / "README.md"
    readme.write_text("# Test Docs\n", encoding="utf-8")

    is_idle, reason, _, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is True
    assert reason == "non_python_only"

    exit_code = run_stop_hook(
        repo_override=repo,
        raw_input={"session_id": session_id, "cwd": str(repo)},
    )
    assert exit_code == 0

    event = read_last_event(repo)
    assert event["event"] == "idle_turn"
    assert event["details"]["reason"] == "non_python_only"


def test_event_reason_cached_pass(temp_git_repo):
    repo, head_sha = temp_git_repo
    session_id = "test_cached_pass_sess"

    set_baseline_sha(session_id, head_sha, repo_path=repo)
    set_last_verified_sha(session_id, head_sha, repo_path=repo)

    # Modify python file
    app_py = repo / "app.py"
    app_py.write_text("def hello():\n    return 'modified'\n", encoding="utf-8")

    # Get fingerprint
    is_idle, reason, fp, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is False
    assert fp is not None

    # Cache this fingerprint as passed
    set_last_passed_fingerprint(session_id, fp, repo_path=repo)

    # Re-check idle turn -> now it should hit cache with cached_pass
    is_idle, reason, cached_fp, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is True
    assert reason == "cached_pass"
    assert cached_fp == fp

    exit_code = run_stop_hook(
        repo_override=repo,
        raw_input={"session_id": session_id, "cwd": str(repo)},
    )
    assert exit_code == 0

    event = read_last_event(repo)
    assert event["event"] == "idle_turn"
    assert event["details"]["reason"] == "cached_pass"
    assert event["details"]["fingerprint"] == fp
