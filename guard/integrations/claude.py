"""Claude Code Stop Hook Integration Writer.

Installs, uninstalls, and checks status of Guard's Stop hook in Claude Code settings.
- By default writes to `.claude/settings.local.json` (uncommitted local settings).
- Supports `--shared` for `.claude/settings.json` (team committed settings).
- Merges into existing `hooks.Stop` array, preserving all other configuration.
- Creates `.bak` backups before modifying existing files.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any

HOOK_COMMAND = "guard hook stop"
DEFAULT_HOOK_TIMEOUT = 180


def get_settings_path(repo_path: str | Path | None = None, shared: bool = False) -> Path:
    """Returns the path to Claude Code settings file."""
    base = Path(repo_path).resolve() if repo_path else Path.cwd()
    if shared:
        return base / ".claude" / "settings.json"
    local_file = base / ".claude" / "settings.local.json"
    shared_file = base / ".claude" / "settings.json"
    if not local_file.exists() and shared_file.exists():
        return shared_file
    return local_file


def _contains_guard_hook(item: Any) -> bool:
    if isinstance(item, dict):
        if item.get("command") == HOOK_COMMAND:
            return True
        inner = item.get("hooks", [])
        if isinstance(inner, list):
            return any(isinstance(h, dict) and h.get("command") == HOOK_COMMAND for h in inner)
    return False


def status(repo_path: str | Path | None = None, shared: bool = False) -> dict[str, Any]:
    """Checks whether Guard Stop hook is installed in Claude settings."""
    settings_file = get_settings_path(repo_path, shared=shared)
    if not settings_file.exists():
        return {
            "installed": False,
            "target_file": str(settings_file),
            "exists": False,
            "shared": shared,
        }

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        hooks = data.get("hooks", {})
        stop_hooks = hooks.get("Stop", [])
        
        installed = any(_contains_guard_hook(h) for h in stop_hooks)
        return {
            "installed": installed,
            "target_file": str(settings_file),
            "exists": True,
            "shared": shared,
            "stop_hooks_count": len(stop_hooks),
        }
    except Exception as exc:
        return {
            "installed": False,
            "target_file": str(settings_file),
            "exists": True,
            "shared": shared,
            "error": str(exc),
        }


def check_all_settings(repo_path: str | Path | None = None) -> dict[str, Any]:
    """Checks whether Guard Stop hook is installed in either local or shared settings."""
    local_stat = status(repo_path=repo_path, shared=False)
    shared_stat = status(repo_path=repo_path, shared=True)
    installed = local_stat["installed"] or shared_stat["installed"]
    active_target = local_stat["target_file"] if local_stat["installed"] else (
        shared_stat["target_file"] if shared_stat["installed"] else local_stat["target_file"]
    )
    return {
        "installed": installed,
        "local": local_stat,
        "shared": shared_stat,
        "active_target": active_target,
    }


def install(repo_path: str | Path | None = None, shared: bool = False) -> tuple[bool, str]:
    """Installs the Guard Stop hook into Claude Code settings.
    
    Returns:
        (success: bool, message: str)
    """
    settings_file = get_settings_path(repo_path, shared=shared)
    settings_file.parent.mkdir(parents=True, exist_ok=True)

    data: dict[str, Any] = {}
    if settings_file.exists():
        # Backup original
        bak_file = settings_file.with_suffix(settings_file.suffix + ".bak")
        shutil.copy2(settings_file, bak_file)
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    data = {}
        except Exception as exc:
            return False, f"Failed to parse existing {settings_file}: {exc}"

    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        data["hooks"] = hooks

    stop_hooks = hooks.setdefault("Stop", [])
    if not isinstance(stop_hooks, list):
        stop_hooks = []
        hooks["Stop"] = stop_hooks

    # Configure command alias
    commands = data.setdefault("commands", {})
    if isinstance(commands, dict):
        commands["guard"] = "guard run"

    # Check if already present
    for h in stop_hooks:
        if _contains_guard_hook(h):
            return True, f"Guard Stop hook is already installed in {settings_file}"

    # Claude Code expects matcher objects with a 'hooks' list
    stop_hooks.append({
        "command": HOOK_COMMAND,
        "hooks": [
            {
                "type": "command",
                "command": HOOK_COMMAND,
                "timeout": DEFAULT_HOOK_TIMEOUT,
            }
        ]
    })

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True, f"Successfully installed Guard Stop hook into {settings_file}"


def uninstall(repo_path: str | Path | None = None, shared: bool = False) -> tuple[bool, str]:
    """Uninstalls Guard Stop hook from Claude Code settings.
    
    Returns:
        (success: bool, message: str)
    """
    settings_file = get_settings_path(repo_path, shared=shared)
    if not settings_file.exists():
        return True, f"Settings file {settings_file} does not exist, nothing to uninstall"

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return True, "No valid settings found"
    except Exception as exc:
        return False, f"Failed to read {settings_file}: {exc}"

    hooks = data.get("hooks", {})
    if not isinstance(hooks, dict) or "Stop" not in hooks:
        return True, "No Stop hooks found"

    stop_hooks = hooks["Stop"]
    if not isinstance(stop_hooks, list):
        return True, "No Stop hook array found"

    # Backup before modification
    bak_file = settings_file.with_suffix(settings_file.suffix + ".bak")
    shutil.copy2(settings_file, bak_file)

    initial_len = len(stop_hooks)
    hooks["Stop"] = [
        h for h in stop_hooks
        if not _contains_guard_hook(h)
    ]

    if len(hooks["Stop"]) == initial_len:
        return True, f"Guard Stop hook was not found in {settings_file}"

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True, f"Successfully removed Guard Stop hook from {settings_file}"
