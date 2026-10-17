"""Static ingestion: parse a Python repo into functions, calls, and imports.

Design rules (see PLAN.md):
  * Static-only edges get confidence 0.6 (capped; only execution evidence raises it).
  * Unresolvable dynamic behaviour is DETECTED and flagged, never guessed.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass, field
from pathlib import Path

DYNAMIC_NAMES = {
    "getattr", "setattr", "eval", "exec", "__import__",
    "import_module", "globals", "locals",
}
BENIGN_DECORATORS = {
    "staticmethod", "classmethod", "property", "abstractmethod",
    "wraps", "cached_property", "override", "overload",
}
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    "build", "dist", ".tox", ".mypy_cache", ".pytest_cache", "site-packages",
}


def is_test_file(rel: str) -> bool:
    parts = rel.split("/")
    name = parts[-1]
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
        or "tests" in parts[:-1]
        or "test" in parts[:-1]
    )


def is_test_function(file: str, qualname: str) -> bool:
    if is_test_file(file):
        return True
    parts = qualname.split(".")
    return any(p.startswith("test_") or p.startswith("Test") for p in parts)


def module_name(rel: str) -> str:
    parts = rel[:-3].split("/")
    if parts and parts[0] == "src":
        parts = parts[1:]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Call):
        node = node.func
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    return "?"


@dataclass
class FuncDef:
    id: str
    file: str
    qualname: str
    name: str
    start: int
    end: int
    cls: str | None
    dynamic: bool = False


class _Collector(ast.NodeVisitor):
    def __init__(self, rel: str):
        self.rel = rel
        self.scope: list[tuple[str, str]] = []  # (name, "class" | "func")
        self.cur: list[FuncDef] = []
        self.funcs: list[FuncDef] = []
        self.calls: dict[str, list[tuple]] = {}
        self.imports: dict[str, tuple] = {}  # local alias -> import descriptor

    # --- imports (module-wide) ---
    def visit_Import(self, node: ast.Import):
        for a in node.names:
            local = a.asname or a.name.split(".")[0]
            target = a.name if a.asname else a.name.split(".")[0]
            self.imports[local] = ("module", target)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for a in node.names:
            if a.name == "*":
                continue
            self.imports[a.asname or a.name] = (
                "from", node.level, node.module or "", a.name,
            )

    # --- definitions ---
    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope.append((node.name, "class"))
        self.generic_visit(node)
        self.scope.pop()

    def _func(self, node):
        qual = ".".join([n for n, _ in self.scope] + [node.name])
        direct_cls = self.scope[-1][0] if self.scope and self.scope[-1][1] == "class" else None
        fd = FuncDef(
            id=f"{self.rel}::{qual}", file=self.rel, qualname=qual, name=node.name,
            start=node.lineno, end=getattr(node, "end_lineno", node.lineno),
            cls=direct_cls,
        )
        # a non-benign decorator can replace the function at runtime
        if any(_decorator_name(d) not in BENIGN_DECORATORS for d in node.decorator_list):
            fd.dynamic = True
        self.funcs.append(fd)
        self.calls[fd.id] = []
        self.scope.append((node.name, "func"))
        self.cur.append(fd)
        self.generic_visit(node)
        self.cur.pop()
        self.scope.pop()

    visit_FunctionDef = _func
    visit_AsyncFunctionDef = _func

    # --- calls ---
    def visit_Call(self, node: ast.Call):
        if self.cur:
            fd = self.cur[-1]
            f = node.func
            if isinstance(f, ast.Name):
                if f.id in DYNAMIC_NAMES:
                    fd.dynamic = True
                self.calls[fd.id].append(("name", f.id))
            elif isinstance(f, ast.Attribute):
                if f.attr in DYNAMIC_NAMES:
                    fd.dynamic = True
                if isinstance(f.value, ast.Name):
                    self.calls[fd.id].append(("attr", f.value.id, f.attr))
                else:
                    self.calls[fd.id].append(("unresolved",))
            else:
                self.calls[fd.id].append(("unresolved",))
        self.generic_visit(node)


@dataclass
class StaticResult:
    files: list[str] = field(default_factory=list)
    funcs: list[FuncDef] = field(default_factory=list)
    call_edges: set[tuple[str, str]] = field(default_factory=set)
    import_edges: set[tuple[str, str]] = field(default_factory=set)
    total_calls: int = 0
    unresolved_calls: int = 0
    parse_errors: list[str] = field(default_factory=list)

    def file_rows(self):
        return [{"path": p} for p in self.files]

    def function_rows(self):
        return [
            {"id": f.id, "file": f.file, "name": f.name, "qualname": f.qualname,
             "start": f.start, "end": f.end, "dyn": f.dynamic}
            for f in self.funcs
            if not is_test_function(f.file, f.qualname)
        ]

    def test_rows(self):
        return [
            {"id": f.id, "file": f.file, "name": f.name, "qualname": f.qualname,
             "start": f.start, "end": f.end}
            for f in self.funcs
            if is_test_function(f.file, f.qualname)
        ]

    def call_rows(self):
        return [{"src": a, "dst": b} for a, b in sorted(self.call_edges)]

    def import_rows(self):
        return [{"src": a, "dst": b} for a, b in sorted(self.import_edges)]

    def summary(self) -> dict:
        total_tests = sum(is_test_function(f.file, f.qualname) for f in self.funcs)
        prod_funcs = len(self.funcs) - total_tests
        return {
            "files": len(self.files),
            "functions": prod_funcs,
            "tests": total_tests,
            "dynamic_functions": sum(f.dynamic for f in self.funcs if not is_test_function(f.file, f.qualname)),
            "call_edges": len(self.call_edges),
            "import_edges": len(self.import_edges),
            "calls_seen": self.total_calls,
            "calls_unresolved": self.unresolved_calls,
            "parse_errors": len(self.parse_errors),
        }


def _resolve_module(level: int, module: str, cur_module: str, is_pkg: bool) -> str:
    if level == 0:
        return module
    pkg = cur_module.split(".") if cur_module else []
    if not is_pkg:
        pkg = pkg[:-1]
    if level > 1:
        pkg = pkg[: len(pkg) - (level - 1)]
    return ".".join(pkg + ([module] if module else []))


def analyze_repo(root: str | Path, include_tests: bool = False) -> StaticResult:
    root = Path(root).resolve()
    res = StaticResult()
    parsed: dict[str, _Collector] = {}

    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in rel.split("/")):
            continue
        if not include_tests and is_test_file(rel):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (SyntaxError, UnicodeDecodeError) as e:
            res.parse_errors.append(f"{rel}: {e}")
            continue
        c = _Collector(rel)
        c.visit(tree)
        parsed[rel] = c
        res.files.append(rel)
        res.funcs.extend(c.funcs)

    mod_to_file = {module_name(rel): rel for rel in parsed}
    funcs_by_mod: dict[str, dict[str, str]] = {}
    for rel, c in parsed.items():
        funcs_by_mod[module_name(rel)] = {f.qualname: f.id for f in c.funcs}

    def lookup(mod: str, qual: str):
        return funcs_by_mod.get(mod, {}).get(qual) or funcs_by_mod.get(mod, {}).get(qual + ".__init__")

    for rel, c in parsed.items():
        cur_mod = module_name(rel)
        is_pkg = rel.endswith("__init__.py")

        # IMPORTS edges (file -> file)
        for desc in c.imports.values():
            if desc[0] == "module":
                tgt = mod_to_file.get(desc[1])
            else:
                _, level, mod, name = desc
                base = _resolve_module(level, mod, cur_mod, is_pkg)
                tgt = mod_to_file.get(f"{base}.{name}" if base else name) or mod_to_file.get(base)
            if tgt and tgt != rel:
                res.import_edges.add((rel, tgt))

        # CALLS edges (function -> function)
        fn_by_id = {f.id: f for f in c.funcs}
        for src_id, calls in c.calls.items():
            src = fn_by_id[src_id]
            for call in calls:
                res.total_calls += 1
                dst = None
                if call[0] == "name":
                    n = call[1]
                    dst = lookup(cur_mod, n)
                    if not dst and n in c.imports:
                        d = c.imports[n]
                        if d[0] == "from":
                            _, level, mod, name = d
                            dst = lookup(_resolve_module(level, mod, cur_mod, is_pkg), name)
                elif call[0] == "attr":
                    a, b = call[1], call[2]
                    if a in ("self", "cls") and src.cls:
                        prefix = src.qualname.rsplit(".", 1)[0]
                        dst = lookup(cur_mod, f"{prefix}.{b}")
                    elif a in c.imports:
                        d = c.imports[a]
                        if d[0] == "module":
                            dst = lookup(d[1], b)
                        else:
                            _, level, mod, name = d
                            base = _resolve_module(level, mod, cur_mod, is_pkg)
                            dst = lookup(f"{base}.{name}" if base else name, b) or lookup(base, f"{name}.{b}")
                    else:
                        dst = lookup(cur_mod, f"{a}.{b}")
                if dst and dst != src_id:
                    res.call_edges.add((src_id, dst))
                elif not dst:
                    res.unresolved_calls += 1
    return res
