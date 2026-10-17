"""Guard decision engine (Task T5): trust score, hard overrides, 3-level policy.

This module is the *pure* decision core. It takes a change set plus the graph
evidence gathered for it and returns which tests to run and why. It performs no
database or subprocess work; wiring it to the live graph / a git diff is the job
of the thin slice (T5a).

Frozen starting parameters (PLAN.md, T5). These are tuned on the calibration
split only, then frozen. Changing any value requires a DEVIATIONS.md entry.

    trust = W_EVIDENCE * evidence_ratio
          + W_FRESHNESS * freshness
          + W_CERTAINTY * (1 - uncertain_ratio)

  where, over the changed functions:
    evidence_ratio  = mean of the best covering-edge confidence per function
                      (0.0 for a function with no covering edge)
    freshness       = fraction of covering edges whose last_verified_sha equals
                      the current SHA (unknown SHA on either side counts as fresh)
    uncertain_ratio = fraction of changed functions flagged dynamic dispatch

Hard overrides (applied before the trust policy):
    1. a changed test file                          -> run all + warning
    2. a changed function with no covering evidence -> run all
    3. a changed function flagged dynamic dispatch  -> add its module tests

Policy:
    trust >= TRUST_SUBSET_MIN   subset
    trust >= TRUST_MEDIUM_MIN   subset + module tests
    otherwise                   run all
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# --- frozen parameters -------------------------------------------------
W_EVIDENCE = 0.5
W_FRESHNESS = 0.3
W_CERTAINTY = 0.2
TRUST_SUBSET_MIN = 0.8
TRUST_MEDIUM_MIN = 0.5

LEVEL_SUBSET = "subset"
LEVEL_MEDIUM = "medium"
LEVEL_RUN_ALL = "run_all"

STATUS_SELECTED = "selected"
STATUS_SKIPPED = "skipped"


def is_test_file(path: str) -> bool:
    """True if a repo-relative path is a test file or lives under tests/."""
    parts = path.replace("\\", "/").split("/")
    name = parts[-1]
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or "tests" in parts[:-1]
    )


@dataclass(frozen=True)
class CoveringTest:
    """A COVERED_BY edge: Test -> covers -> Function (edge confidence)."""

    test_id: str
    confidence: float
    source: str = "unknown"
    last_verified_sha: str | None = None


@dataclass(frozen=True)
class FunctionEvidence:
    """Graph evidence for one changed function."""

    function_id: str
    file: str
    covering_tests: tuple[CoveringTest, ...] = ()
    has_dynamic_dispatch: bool = False

    @property
    def has_evidence(self) -> bool:
        return len(self.covering_tests) > 0

    @property
    def best_confidence(self) -> float:
        if not self.covering_tests:
            return 0.0
        return max(c.confidence for c in self.covering_tests)


@dataclass(frozen=True)
class Change:
    """Inputs to a decision: changed functions, changed files, and the known tests."""

    functions: tuple[FunctionEvidence, ...] = ()
    changed_files: tuple[str, ...] = ()
    known_tests: tuple[str, ...] = ()
    module_tests: dict[str, tuple[str, ...]] = field(default_factory=dict)
    current_sha: str | None = None

    def module_tests_for(self, file: str) -> tuple[str, ...]:
        return tuple(self.module_tests.get(file, ()))


@dataclass(frozen=True)
class EvidenceEdge:
    function: str
    source: str
    confidence: float
    fresh: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "function": self.function,
            "source": self.source,
            "confidence": self.confidence,
            "fresh": self.fresh,
        }


@dataclass(frozen=True)
class Reason:
    test_id: str
    status: str
    text: str
    evidence: tuple[EvidenceEdge, ...] = ()
    queried_functions: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "test_id": self.test_id,
            "status": self.status,
            "text": self.text,
            "evidence": [e.as_dict() for e in self.evidence],
            "queried_functions": list(self.queried_functions),
        }


@dataclass(frozen=True)
class Decision:
    run_all: bool
    policy_level: str
    trust: float
    evidence_ratio: float
    freshness: float
    uncertain_ratio: float
    selected_tests: tuple[str, ...]
    skipped_tests: tuple[str, ...]
    reasons: dict[str, Reason]
    overrides: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def explain(self, test_id: str) -> Reason:
        """Queryable reason for any test the engine considered."""
        if test_id not in self.reasons:
            raise KeyError(f"no decision recorded for test {test_id!r}")
        return self.reasons[test_id]

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_all": self.run_all,
            "policy_level": self.policy_level,
            "trust": round(self.trust, 6),
            "components": {
                "evidence_ratio": round(self.evidence_ratio, 6),
                "freshness": round(self.freshness, 6),
                "uncertain_ratio": round(self.uncertain_ratio, 6),
            },
            "selected_tests": list(self.selected_tests),
            "skipped_tests": list(self.skipped_tests),
            "overrides": list(self.overrides),
            "warnings": list(self.warnings),
            "reasons": {t: r.as_dict() for t, r in self.reasons.items()},
        }


def _fresh(edge_sha: str | None, current_sha: str | None) -> bool:
    if edge_sha is None or current_sha is None:
        return True
    return edge_sha == current_sha


def compute_trust(change: Change) -> tuple[float, float, float, float]:
    """Return (trust, evidence_ratio, freshness, uncertain_ratio)."""
    funcs = change.functions
    n = len(funcs)
    if n == 0:
        return 0.0, 0.0, 0.0, 0.0

    evidence_ratio = sum(f.best_confidence for f in funcs) / n
    uncertain_ratio = sum(1 for f in funcs if f.has_dynamic_dispatch) / n

    edges = [c for f in funcs for c in f.covering_tests]
    if edges:
        freshness = sum(1 for c in edges if _fresh(c.last_verified_sha, change.current_sha)) / len(edges)
    else:
        freshness = 0.0

    trust = (
        W_EVIDENCE * evidence_ratio
        + W_FRESHNESS * freshness
        + W_CERTAINTY * (1.0 - uncertain_ratio)
    )
    return trust, evidence_ratio, freshness, uncertain_ratio


def policy_for_trust(trust: float) -> str:
    """Map a trust score to one of the three policy levels."""
    if trust >= TRUST_SUBSET_MIN:
        return LEVEL_SUBSET
    if trust >= TRUST_MEDIUM_MIN:
        return LEVEL_MEDIUM
    return LEVEL_RUN_ALL


def decide(change: Change) -> Decision:
    """Apply the hard overrides, then the trust policy, to select tests."""
    funcs = list(change.functions)
    all_functions = tuple(f.function_id for f in funcs)

    overrides: list[str] = []
    warnings: list[str] = []

    # Base selection: covering tests of each changed function, with the edge that
    # justifies the selection so every decision stays queryable.
    base: dict[str, list[EvidenceEdge]] = {}
    for f in funcs:
        for c in f.covering_tests:
            base.setdefault(c.test_id, []).append(
                EvidenceEdge(f.function_id, c.source, c.confidence,
                             _fresh(c.last_verified_sha, change.current_sha))
            )

    # --- hard override 1: test files touched
    touched_test_files = sorted(p for p in change.changed_files if is_test_file(p))
    force_run_all = False
    if touched_test_files:
        force_run_all = True
        overrides.append("test_file_touched")
        warnings.append(
            f"test files changed ({', '.join(touched_test_files)}); running the full suite"
        )

    # --- hard override 2: any changed function with no covering evidence
    no_evidence = sorted(f.function_id for f in funcs if not f.has_evidence)
    if not funcs or no_evidence:
        force_run_all = True
        overrides.append("no_evidence")
        if no_evidence:
            warnings.append(f"no covering evidence for: {', '.join(no_evidence)}")
        else:
            warnings.append("no changed functions carried evidence; running the full suite")

    # --- hard override 3: dynamic dispatch widens to module tests
    dynamic_funcs = sorted(f.function_id for f in funcs if f.has_dynamic_dispatch)
    if dynamic_funcs:
        overrides.append("dynamic_dispatch")

    trust, ev_ratio, fresh, unc = compute_trust(change)

    if force_run_all:
        level = LEVEL_RUN_ALL
        run_all = True
        selected_set = set(change.known_tests)
    else:
        level = policy_for_trust(trust)
        run_all = level == LEVEL_RUN_ALL
        if run_all:
            selected_set = set(change.known_tests)
        else:
            selected_set = set(base)
            if level == LEVEL_MEDIUM or dynamic_funcs:
                for f in funcs:
                    selected_set.update(change.module_tests_for(f.file))

    # --- a queryable reason for every known test
    reasons: dict[str, Reason] = {}
    for test_id in change.known_tests:
        if test_id in selected_set:
            if run_all:
                text = "selected: full suite required"
                if force_run_all:
                    text = "selected: full suite (hard override)"
            elif base.get(test_id):
                text = "selected: covers a changed function"
            else:
                text = "selected: module test for a changed function's module"
            reasons[test_id] = Reason(
                test_id, STATUS_SELECTED, text,
                tuple(base.get(test_id, ())), all_functions,
            )
        else:
            reasons[test_id] = Reason(
                test_id, STATUS_SKIPPED,
                "skipped: no covering edge from any changed function",
                (), all_functions,
            )

    selected_tests = tuple(sorted(selected_set))
    skipped_tests = tuple(t for t in change.known_tests if t not in selected_set)

    return Decision(
        run_all=run_all,
        policy_level=level,
        trust=trust,
        evidence_ratio=ev_ratio,
        freshness=fresh,
        uncertain_ratio=unc,
        selected_tests=selected_tests,
        skipped_tests=skipped_tests,
        reasons=reasons,
        overrides=tuple(overrides),
        warnings=tuple(warnings),
    )
