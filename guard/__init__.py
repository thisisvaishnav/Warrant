import sys
import importlib
import guard_cli as _mod

sys.modules[__name__] = _mod

for _sub in (
    "doctor_cmd", "hook", "api", "backend", "db", "decision",
    "events", "feedback", "init_cmd", "state", "thin_slice",
    "agent_integration", "ingest", "integrations"
):
    try:
        _m = importlib.import_module(f"guard_cli.{_sub}")
        setattr(_mod, _sub, _m)
        sys.modules[f"guard.{_sub}"] = _m
    except Exception:
        pass
