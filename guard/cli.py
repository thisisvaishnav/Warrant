"""Guard CLI. Commands: ingest-static, callers, stats, covering-tests."""
from __future__ import annotations
import argparse
import json
import sys

from guard.ingest.static import analyze_repo


def cmd_ingest_static(args) -> int:
    res = analyze_repo(args.repo, include_tests=args.include_tests)
    print(json.dumps(res.summary(), indent=2))
    for err in res.parse_errors[:5]:
        print("parse error:", err, file=sys.stderr)
    if args.dry_run:
        return 0
    from guard import db

    g = db.get_graph(args.graph)
    db.reset_graph(g)
    g = db.get_graph(args.graph)
    db.ensure_schema(g)
    db.write_static(g, res, commit_sha=args.commit_sha)
    print(f"written to graph '{args.graph}'")
    return 0


def cmd_callers(args) -> int:
    from guard import db

    g = db.get_graph(args.graph)
    hops = int(args.hops)
    callers = db.get_callers(g, args.function, hops=hops, min_confidence=float(args.min_confidence))
    for c in callers:
        print(f"{c['hops']}  {c['caller']}")
    return 0


def cmd_stats(args) -> int:
    from guard import db

    g = db.get_graph(args.graph)
    counts = db.get_schema_counts(g)
    print("=== Nodes ===")
    for label in ("File", "Function", "Test", "Run"):
        print(f"{label}: {counts.get(label, 0)}")
    print("\n=== Edges ===")
    for rel in ("CALLS", "IMPORTS", "DEFINED_IN", "COVERED_BY", "FAILED_IN"):
        print(f"{rel}: {counts.get(rel, 0)}")
    print(f"\nDynamic functions: {counts.get('dynamic_functions', 0)}")
    return 0


def cmd_covering_tests(args) -> int:
    from guard import db

    g = db.get_graph(args.graph)
    tests = db.get_covering_tests(g, args.function, min_confidence=float(args.min_confidence))
    for t in tests:
        print(f"[{t['confidence']:.2f}] {t['test_id']} (source: {t['source']})")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="guard")
    p.add_argument("--graph", default="guard")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ingest-static")
    s.add_argument("repo")
    s.add_argument("--dry-run", action="store_true", help="parse only, no database")
    s.add_argument("--include-tests", action="store_true")
    s.add_argument("--commit-sha", default=None, help="commit SHA to associate with edges")
    s.set_defaults(fn=cmd_ingest_static)

    c = sub.add_parser("callers")
    c.add_argument("function", help="function id, e.g. pkg/mod.py::Class.method")
    c.add_argument("--hops", default=4, type=int)
    c.add_argument("--min-confidence", default=0.0, type=float)
    c.set_defaults(fn=cmd_callers)

    st = sub.add_parser("stats")
    st.set_defaults(fn=cmd_stats)

    cov = sub.add_parser("covering-tests")
    cov.add_argument("function", help="function id, e.g. pkg/mod.py::Class.method")
    cov.add_argument("--min-confidence", default=0.0, type=float)
    cov.set_defaults(fn=cmd_covering_tests)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
