# Guard

Graph-powered safety layer for AI coding agents, built on FalkorDB.
See PLAN.md for the full plan and the frozen claim.

## Quickstart (Day 1)

```bash
docker compose up -d                 # FalkorDB on :6379, browser UI on :3000
pip install -r requirements.txt
python -m pytest -q tests            # parser tests (no database needed)

python -m guard.cli ingest-static /path/to/target/repo --dry-run   # parse only
python -m guard.cli ingest-static /path/to/target/repo             # write to FalkorDB
python -m guard.cli stats
python -m guard.cli callers "pkg/mod.py::func" --hops 4
```

## Notes
- Static-only edges are capped at confidence 0.6. Only execution evidence raises it.
- Unresolvable dynamic behaviour (getattr, eval, custom decorators, ...) is flagged, not guessed.
- `calls_unresolved` in the ingest summary is mostly stdlib/third-party calls, which is expected.
