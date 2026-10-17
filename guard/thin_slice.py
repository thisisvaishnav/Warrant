"""Thin slice end-to-end decision engine (Task T5a).

Parses a git diff, maps changed line numbers to FalkorDB Function nodes,
queries covering tests from COVERED_BY edges, and applies crude decision logic:
- If ANY changed function has no_evidence=true (or 0 covering tests) -> run all.
- Otherwise -> select the covering tests.
"""
from __future__ import annotations
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from guard import db


@dataclass
class ChangedFunction:
    id: str
    file: str
    name: str
    start: int
    end: int
    no_evidence: bool
    has_dynamic_dispatch: bool = False
    covering_tests: list[str] = field(default_factory=list)


@dataclass
class CheckResult:
    status: str  # "select" | "run-all"
    is_fallback: bool
    fallback_reason: str | None
    changed_functions: list[str]
    selected_tests: list[str]
    execution_time_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "is_fallback": self.is_fallback,
            "fallback_reason": self.fallback_reason,
            "changed_functions": self.changed_functions,
            "selected_tests": self.selected_tests,
            "selected_tests_count": len(self.selected_tests),
            "execution_time_ms": self.execution_time_ms,
        }


def parse_unified_diff(diff_text: str) -> dict[str, set[int]]:
    """Parses a unified diff into a map of {relative_file_path: set(modified_lines)}."""
    file_lines: dict[str, set[int]] = {}
    current_file = None
    current_line = 0

    hunk_regex = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            raw_path = line[6:].strip()
            # Normalize path: strip repo prefixes if present
            current_file = raw_path
            if current_file not in file_lines:
                file_lines[current_file] = set()
            current_line = 0
            continue
        elif line.startswith("+++ "):
            raw_path = line[4:].strip()
            if raw_path != "/dev/null":
                current_file = raw_path.lstrip("b/")
                if current_file not in file_lines:
                    file_lines[current_file] = set()
            current_line = 0
            continue

        if not current_file:
            continue

        hunk_match = hunk_regex.match(line)
        if hunk_match:
            current_line = int(hunk_match.group(1))
            continue

        if line.startswith("+") and not line.startswith("+++"):
            file_lines[current_file].add(current_line)
            current_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            # Deletion occurs at current_line
            file_lines[current_file].add(current_line)
        elif line.startswith(" "):
            current_line += 1

    return file_lines


def resolve_changed_functions(g, file_lines: dict[str, set[int]]) -> list[ChangedFunction]:
    """Queries FalkorDB to find Function nodes spanning the modified lines."""
    changed_funcs: dict[str, ChangedFunction] = {}

    for file_path, lines in file_lines.items():
        if not lines:
            continue

        # In FalkorDB, File nodes use paths like 'src/flask/config.py'
        # Query functions defined in this file
        q = (
            "MATCH (f:Function) "
            "WHERE f.file = $file OR f.file ENDS WITH $file OR $file ENDS WITH f.file "
            "RETURN f.id, f.file, f.name, f.start, f.end, coalesce(f.no_evidence, false), coalesce(f.has_dynamic_dispatch, false)"
        )
        res = g.query(q, {"file": file_path}).result_set

        for fid, ffile, fname, start, end, no_evidence, dyn in res:
            start_i = int(start)
            end_i = int(end)
            # Check if any modified line falls within [start, end]
            if any(start_i <= lineno <= end_i for lineno in lines):
                if fid not in changed_funcs:
                    changed_funcs[fid] = ChangedFunction(
                        id=fid,
                        file=ffile,
                        name=fname,
                        start=start_i,
                        end=end_i,
                        no_evidence=bool(no_evidence),
                        has_dynamic_dispatch=bool(dyn),
                    )

    return list(changed_funcs.values())


def thin_slice_decision(
    g,
    changed_functions: list[ChangedFunction],
    test_files_touched: bool = False,
    no_confidence_filter: bool = False,
    no_dynamic_widening: bool = False,
) -> CheckResult:
    """Decision logic:
    - If test files were touched or no functions matched -> run all.
    - If ANY changed function has no_evidence=true (and not no_confidence_filter) -> run all.
    - Otherwise -> collect covering tests via COVERED_BY edges (with confidence filter unless ablated).
    - If dynamic dispatch is present and widening enabled -> include module tests.
    """
    if test_files_touched:
        return CheckResult(
            status="run-all",
            is_fallback=True,
            fallback_reason="Test files were modified in diff",
            changed_functions=[f.id for f in changed_functions],
            selected_tests=["tests"],
        )

    if not changed_functions:
        return CheckResult(
            status="run-all",
            is_fallback=True,
            fallback_reason="No parsed functions matched diff line changes",
            changed_functions=[],
            selected_tests=["tests"],
        )

    # Hard override: If any function has no evidence -> fallback to run all (unless confidence filter ablated)
    if not no_confidence_filter:
        for fn in changed_functions:
            if fn.no_evidence:
                return CheckResult(
                    status="run-all",
                    is_fallback=True,
                    fallback_reason=f"Uncovered function has no_evidence=true: {fn.id}",
                    changed_functions=[f.id for f in changed_functions],
                    selected_tests=["tests"],
                )

    # Collect covering tests from graph
    all_tests = set()
    min_conf = 0.0 if no_confidence_filter else 0.8
    for fn in changed_functions:
        covering = db.get_covering_tests(g, fn.id, min_confidence=min_conf) if g is not None else []
        fn_tests = [c["test_id"] for c in covering]
        if not fn_tests and not no_confidence_filter:
            # No covering tests found
            return CheckResult(
                status="run-all",
                is_fallback=True,
                fallback_reason=f"No covering tests found with confidence >= 0.8 for: {fn.id}",
                changed_functions=[f.id for f in changed_functions],
                selected_tests=["tests"],
            )
        fn.covering_tests = fn_tests
        all_tests.update(fn_tests)

    # Dynamic dispatch widening
    if not no_dynamic_widening and g is not None:
        dynamic_funcs = [fn for fn in changed_functions if fn.has_dynamic_dispatch]
        if dynamic_funcs:
            for fn in dynamic_funcs:
                stem = Path(fn.file).stem
                mod_q = "MATCH (t:Test) WHERE t.file CONTAINS $mod_stem RETURN t.id"
                try:
                    mod_res = g.query(mod_q, {"mod_stem": f"test_{stem}"}).result_set
                    for r in mod_res:
                        all_tests.add(r[0])
                except Exception:
                    pass

    if not all_tests:
        return CheckResult(
            status="run-all",
            is_fallback=True,
            fallback_reason="No covering tests found",
            changed_functions=[f.id for f in changed_functions],
            selected_tests=["tests"],
        )

    sorted_tests = sorted(all_tests)
    return CheckResult(
        status="select",
        is_fallback=False,
        fallback_reason=None,
        changed_functions=[f.id for f in changed_functions],
        selected_tests=sorted_tests,
    )


def guard_check(
    diff_text: str | None = None,
    diff_file: Path | str | None = None,
    repo_path: Path | str | None = None,
    graph_name: str = "guard",
    no_confidence_filter: bool = False,
    no_dynamic_widening: bool = False,
) -> CheckResult:
    """Evaluates a diff and returns the test selection decision."""
    import time
    start_time = time.time()

    if diff_text is None:
        if diff_file:
            diff_text = Path(diff_file).read_text(encoding="utf-8")
        else:
            # Run git diff HEAD in repo_path
            cwd = str(repo_path) if repo_path else None
            proc = subprocess.run(["git", "diff", "HEAD"], cwd=cwd, capture_output=True, text=True)
            diff_text = proc.stdout

    file_lines = parse_unified_diff(diff_text)
    
    # Check if test files were touched
    test_files_touched = any(
        "test" in p.lower() or p.startswith("tests/")
        for p in file_lines.keys()
    )

    g = db.get_graph(graph_name)
    changed_funcs = resolve_changed_functions(g, file_lines)
    result = thin_slice_decision(
        g,
        changed_funcs,
        test_files_touched=test_files_touched,
        no_confidence_filter=no_confidence_filter,
        no_dynamic_widening=no_dynamic_widening,
    )
    result.execution_time_ms = round((time.time() - start_time) * 1000.0, 2)
    return result
