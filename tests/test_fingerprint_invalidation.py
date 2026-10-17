"""Test verifying Fix 2: Fingerprint Contents and Invalidation.

Done when: Changing a file, staging it, or re-ingesting the graph each invalidates the cached "passed" result.
"""
import subprocess
import time
from pathlib import Path
import pytest

from guard_cli import db
from guard_cli.hook import check_idle_turn, compute_turn_fingerprint
from guard_cli.state import (
    set_last_passed_fingerprint,
    get_last_passed_fingerprint,
    clear_last_passed_fingerprint,
    set_baseline_sha,
    set_last_verified_sha,
)


@pytest.fixture
def isolated_git_repo(tmp_path):
    """Creates a real git repo with an initial commit and a Python file."""
    repo = tmp_path / "repo"
    repo.mkdir()

    subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "tester@test.com"], cwd=str(repo), check=True)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=str(repo), check=True)

    app_py = repo / "app.py"
    app_py.write_text("def hello():\n    return 'world'\n", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=str(repo), check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=str(repo), check=True)

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo), capture_output=True, text=True).stdout.strip()
    return repo, head


def test_fingerprint_invalidation_matrix(isolated_git_repo):
    repo, head_sha = isolated_git_repo
    session_id = "test_fp_sess"

    set_baseline_sha(session_id, head_sha, repo_path=repo)
    set_last_verified_sha(session_id, head_sha, repo_path=repo)

    # 1. Modify app.py in working tree
    app_py = repo / "app.py"
    app_py.write_text("def hello():\n    return 'changed 1'\n", encoding="utf-8")

    # Initial check -> not idle, generates fingerprint fp1
    is_idle, reason, fp1, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is False
    assert fp1 is not None

    # Simulate that tests passed on this state: cache fp1
    set_last_passed_fingerprint(session_id, fp1, repo_path=repo)
    assert get_last_passed_fingerprint(session_id, repo_path=repo) == fp1

    # Verify that a re-check without changes hits the cache
    is_idle, reason, cached_fp, _ = check_idle_turn(repo, session_id=session_id)
    assert is_idle is True
    assert reason in ("cached_pass", "fingerprint_cache_hit")
    assert cached_fp == fp1

    # --- Condition A: Changing a file invalidates cached passed result ---
    app_py.write_text("def hello():\n    return 'changed 2 - another edit'\n", encoding="utf-8")
    is_idle, reason, fp2, _ = check_idle_turn(repo, session_id=session_id)
    assert fp2 != fp1, "Expected changing a file to generate a new fingerprint"
    assert is_idle is False, "Expected changing a file to invalidate cached pass"
    assert reason == "python_files_modified"

    # Simulate pass on fp2
    set_last_passed_fingerprint(session_id, fp2, repo_path=repo)

    # --- Condition B: Staging a file (git add) invalidates cached passed result ---
    subprocess.run(["git", "add", "app.py"], cwd=str(repo), check=True)
    is_idle, reason, fp3, _ = check_idle_turn(repo, session_id=session_id)
    assert fp3 != fp2, "Expected staging a file to generate a new fingerprint"
    assert is_idle is False, "Expected staging a file to invalidate cached pass"

    # Simulate pass on fp3
    set_last_passed_fingerprint(session_id, fp3, repo_path=repo)

    # --- Condition C: Re-ingesting graph invalidates cached passed result ---
    # Create or update mock graph metadata / schema count in live backend
    g = db.get_graph(name="guard", repo_path=repo)
    fp_before = compute_turn_fingerprint(
        repo_path=repo,
        baseline_sha=head_sha,
        head_sha=head_sha,
        diff_baseline="",
        diff_cached="diff_staged",
        untracked_files=[],
        g=g,
    )
    set_last_passed_fingerprint(session_id, fp_before, repo_path=repo)

    # Simulate graph re-ingestion
    db.update_graph_meta(g)

    fp_after = compute_turn_fingerprint(
        repo_path=repo,
        baseline_sha=head_sha,
        head_sha=head_sha,
        diff_baseline="",
        diff_cached="diff_staged",
        untracked_files=[],
        g=g,
    )
    assert fp_after != fp_before, "Expected graph re-ingestion to change graph_state in fingerprint"

    # --- Condition D: Untracked python file invalidates cached passed result ---
    untracked_py = repo / "helper.py"
    untracked_py.write_text("def helper(): pass\n", encoding="utf-8")

    is_idle, reason, fp4, _ = check_idle_turn(repo, session_id=session_id)
    assert fp4 != fp3
    assert is_idle is False
    assert reason == "python_files_modified"
