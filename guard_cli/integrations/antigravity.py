"""Antigravity (App / CLI / IDE) Stop Hook Integration Writer.

Installs, uninstalls, and checks status of Guard's Stop hook in .agents/hooks.json.
- Merges into existing `hooks.json` config.
- Preserves all other configured hooks and handlers.

Format verified against official Antigravity docs (antigravity.google/docs/hooks):
the top level maps hook names to event configs; for Stop (like PreInvocation and
PostInvocation) handler objects sit directly under the event key (matcher is
ignored), each supporting {type: "command", command, timeout}. Stop hooks
re-enter the loop by emitting {"decision": "continue", "reason": ...} on stdout
(exit 0); any other decision (or silent exit 0) allows the stop.

EXPERIMENTAL: verified against the published schema and simulated stdin/stdout
only; a live Antigravity session has not yet confirmed end-to-end behavior.
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any

HOOK_COMMAND = "guard hook stop"
SESSION_START_COMMAND = "guard hook session-start"
DEFAULT_HOOK_TIMEOUT = 180


def get_hooks_file_path(repo_path: str | Path | None = None) -> Path:
    """Returns the path to Antigravity .agents/hooks.json."""
    base = Path(repo_path).resolve() if repo_path else Path.cwd()
    return base / ".agents" / "hooks.json"


def _contains_guard_hook(handlers: list[dict[str, Any]], command: str = HOOK_COMMAND) -> bool:
    for h in handlers:
        if isinstance(h, dict) and h.get("command") == command:
            return True
    return False


def status(repo_path: str | Path | None = None) -> dict[str, Any]:
    """Checks whether Guard Stop hook is installed in Antigravity .agents/hooks.json."""
    hooks_file = get_hooks_file_path(repo_path)
    if not hooks_file.exists():
        return {
            "installed": False,
            "target_file": str(hooks_file),
            "exists": False,
        }

    try:
        with open(hooks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"installed": False, "target_file": str(hooks_file), "exists": True}

        # Check all named hooks for a Stop event handler running HOOK_COMMAND
        for hook_name, hook_cfg in data.items():
            if isinstance(hook_cfg, dict):
                stop_handlers = hook_cfg.get("Stop", [])
                if isinstance(stop_handlers, list) and _contains_guard_hook(stop_handlers):
                    pre_handlers = hook_cfg.get("PreInvocation", [])
                    return {
                        "installed": True,
                        "target_file": str(hooks_file),
                        "exists": True,
                        "hook_name": hook_name,
                        "pre_invocation_installed": (
                            isinstance(pre_handlers, list)
                            and _contains_guard_hook(pre_handlers, SESSION_START_COMMAND)
                        ),
                    }
        return {"installed": False, "target_file": str(hooks_file), "exists": True}
    except Exception as exc:
        return {
            "installed": False,
            "target_file": str(hooks_file),
            "exists": True,
            "error": str(exc),
        }


def install(repo_path: str | Path | None = None) -> tuple[bool, str]:
    """Installs Guard Stop hook into .agents/hooks.json.
    
    Returns:
        (success: bool, message: str)
    """
    hooks_file = get_hooks_file_path(repo_path)
    hooks_file.parent.mkdir(parents=True, exist_ok=True)

    data: dict[str, Any] = {}
    if hooks_file.exists():
        bak_file = hooks_file.with_suffix(hooks_file.suffix + ".bak")
        shutil.copy2(hooks_file, bak_file)
        try:
            with open(hooks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    data = {}
        except Exception as exc:
            return False, f"Failed to parse existing {hooks_file}: {exc}"

    guard_hook = data.setdefault("guard-stop", {})
    if not isinstance(guard_hook, dict):
        guard_hook = {}
        data["guard-stop"] = guard_hook

    stop_list = guard_hook.setdefault("Stop", [])
    if not isinstance(stop_list, list):
        stop_list = []
        guard_hook["Stop"] = stop_list

    pre_list = guard_hook.setdefault("PreInvocation", [])
    if not isinstance(pre_list, list):
        pre_list = []
        guard_hook["PreInvocation"] = pre_list

    stop_present = _contains_guard_hook(stop_list)
    pre_present = _contains_guard_hook(pre_list, SESSION_START_COMMAND)
    if stop_present and pre_present:
        return True, f"Guard hooks are already installed in {hooks_file}"

    from guard_cli.hook import get_hook_timeout
    timeout = get_hook_timeout(repo_path)

    if not stop_present:
        stop_list.append({
            "type": "command",
            "command": HOOK_COMMAND,
            "timeout": timeout,
        })

    # agy has no SessionStart event; PreInvocation fires before every model call
    # and records the baseline on first use (see antigravity.google/docs/hooks).
    # PreInvocation takes a flat handler list (matcher ignored).
    if not pre_present:
        pre_list.append({
            "type": "command",
            "command": SESSION_START_COMMAND,
            "timeout": timeout,
        })

    with open(hooks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True, f"Successfully installed Guard hooks into {hooks_file}"


def uninstall(repo_path: str | Path | None = None) -> tuple[bool, str]:
    """Uninstalls Guard Stop hook from .agents/hooks.json."""
    hooks_file = get_hooks_file_path(repo_path)
    if not hooks_file.exists():
        return True, f"Hooks file {hooks_file} does not exist, nothing to uninstall"

    try:
        with open(hooks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return True, "No valid hooks config found"
    except Exception as exc:
        return False, f"Failed to read {hooks_file}: {exc}"

    modified = False
    for hook_name, hook_cfg in list(data.items()):
        if not isinstance(hook_cfg, dict):
            continue
        container_modified = False
        for event, command in (("Stop", HOOK_COMMAND), ("PreInvocation", SESSION_START_COMMAND)):
            orig = hook_cfg.get(event)
            if not isinstance(orig, list):
                continue
            new_list = [h for h in orig if not (isinstance(h, dict) and h.get("command") == command)]
            if len(new_list) != len(orig):
                if new_list:
                    hook_cfg[event] = new_list
                else:
                    del hook_cfg[event]
                container_modified = True
        if container_modified:
            modified = True
            if not hook_cfg:
                del data[hook_name]

    if not modified:
        return True, f"Guard Stop hook was not found in {hooks_file}"

    bak_file = hooks_file.with_suffix(hooks_file.suffix + ".bak")
    shutil.copy2(hooks_file, bak_file)

    with open(hooks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True, f"Successfully removed Guard Stop hook from {hooks_file}"
