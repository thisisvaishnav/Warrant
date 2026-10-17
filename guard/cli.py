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


def cmd_ingest_coverage(args) -> int:
    from guard.ingest.coverage import ingest_coverage

    res = ingest_coverage(
        repo_path=args.repo,
        graph_name=args.graph,
        commit_sha=args.commit_sha,
        num_runs=args.runs,
    )
    print(json.dumps(res.summary(), indent=2))
    return 0


def cmd_check(args) -> int:
    from guard.thin_slice import guard_check

    res = guard_check(
        diff_file=args.diff,
        repo_path=args.repo,
        graph_name=args.graph,
    )
    if args.json:
        print(json.dumps(res.to_dict(), indent=2))
    else:
        print(f"Status: {res.status}")
        print(f"Fallback: {res.is_fallback}")
        if res.fallback_reason:
            print(f"Reason: {res.fallback_reason}")
        print(f"Changed Functions ({len(res.changed_functions)}): {res.changed_functions}")
        print(f"Selected Tests ({len(res.selected_tests)}): {res.selected_tests}")
    return 0


def cmd_feedback(args) -> int:
    from guard import db
    from guard.feedback import record_miss

    g = db.get_graph(args.graph)
    res = record_miss(
        g,
        function_id=args.function,
        test_id=args.test,
        new_confidence=args.confidence,
    )
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Repaired: function='{res['function']}' -> test='{res['test']}'")
        print(f"Confidence: {res['old_confidence']} -> {res['new_confidence']} (source: {res['source']})")
    return 0


def cmd_run(args) -> int:
    from guard.agent_integration import run_agent_guard

    report, exit_code = run_agent_guard(
        diff_file=args.diff,
        repo_path=args.repo,
        graph_name=args.graph,
    )
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Status: {report['status']}")
        print(f"Forced Full Suite: {report['forced_full']}")
        if report['fallback_reason']:
            print(f"Fallback Reason: {report['fallback_reason']}")
        print(f"Tests Run ({report['tests_run_count']}): {report['tests_run']}")
        print(f"Passed: {report['tests_passed']} in {report['duration_s']}s")
        if report['output_summary']:
            print(f"Summary: {report['output_summary']}")
    return exit_code


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="guard")
    p.add_argument("--graph", default="guard")
    sub = p.add_subparsers(dest="cmd", required=True)

    rn = sub.add_parser("run")
    rn.add_argument("--diff", default=None, help="path to unified diff file")
    rn.add_argument("--repo", default=None, help="path to target repo")
    rn.add_argument("--json", action="store_true", help="output JSON")
    rn.set_defaults(fn=cmd_run)

    chk = sub.add_parser("check")
    chk.add_argument("--diff", default=None, help="path to unified diff file")
    chk.add_argument("--repo", default=None, help="path to repo to run git diff HEAD")
    chk.add_argument("--json", action="store_true", help="output JSON")
    chk.set_defaults(fn=cmd_check)

    fb = sub.add_parser("feedback")
    fb.add_argument("--function", required=True, help="Function ID where fault was missed")
    fb.add_argument("--test", required=True, help="Test ID that failed and was missed")
    fb.add_argument("--confidence", default=1.0, type=float, help="Confidence of repair edge (default: 1.0)")
    fb.add_argument("--json", action="store_true", help="output JSON")
    fb.set_defaults(fn=cmd_feedback)

    s = sub.add_parser("ingest-static")
    s.add_argument("repo")
    s.add_argument("--dry-run", action="store_true", help="parse only, no database")
    s.add_argument("--include-tests", action="store_true")
    s.add_argument("--commit-sha", default=None, help="commit SHA to associate with edges")
    s.set_defaults(fn=cmd_ingest_static)

    ic = sub.add_parser("ingest-coverage")
    ic.add_argument("repo")
    ic.add_argument("--runs", default=3, type=int, help="number of test runs for flake measurement")
    ic.add_argument("--commit-sha", default=None, help="commit SHA to associate with edges")
    ic.set_defaults(fn=cmd_ingest_coverage)

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
