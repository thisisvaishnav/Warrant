# Formal Eval Report: Task T2 - FalkorDB Graph Schema & Node/Edge Model

**Date**: 2026-10-16  
**Target Component**: [guard/db.py](file:///Users/bombermac/hackathon/warrant/guard/db.py)  
**Target Repository**: [target_repos/flask](file:///Users/bombermac/hackathon/warrant/target_repos/flask)  
**Database**: FalkorDB (localhost:6379)  
**Harness Script**: [evals/eval_t2.py](file:///Users/bombermac/hackathon/warrant/evals/eval_t2.py)  

---

## Evaluation Summary

| Metric | Target Threshold | Measured Score | Status |
| :--- | :---: | :---: | :---: |
| **Capability Pass@1** | $\ge 90\%$ | **100% (4/4)** | ✅ PASS |
| **Capability Pass^3 (Stability)** | $\ge 90\%$ | **100% (4/4)** | ✅ PASS |
| **Regression Pass@1** | $100\%$ | **100% (3/3)** | ✅ PASS |
| **Regression Pass^3 (Stability)** | $100\%$ | **100% (3/3)** | ✅ PASS |

---

## Detailed Evaluation Breakdown

### 1. Capability Evals (New Behaviors & Schema Contracts)
- **`c1_schema_indexes`**: **PASS**
  - Verified index creation for `Function(id)`, `Test(id)`, `File(path)`, and `Run(id)`.
  - Idempotency confirmed across repeated calls.
- **`c2_node_types_integrity`**: **PASS**
  - Created and validated all 4 node types in FalkorDB: `File`, `Function`, `Test`, `Run`.
  - Node attributes (`has_dynamic_dispatch`, `start`, `end`, `qualname`, `duration_ms`, `passed`, `failed`) verified.
- **`c3_edge_types_and_properties`**: **PASS**
  - Verified all 5 edge relationships:
    - `(:Function)-[:DEFINED_IN]->(:File)`
    - `(:Test)-[:DEFINED_IN]->(:File)`
    - `(:Function)-[:CALLS {source: 'static', confidence: 0.6, evidence_count: 0, last_verified_sha: ...}]->(:Function)`
    - `(:File)-[:IMPORTS {source: 'static', confidence: 0.6, last_verified_sha: ...}]->(:File)`
    - `(:Function)-[:COVERED_BY {source: 'coverage', confidence: 0.9, evidence_count: 1, last_verified_sha: ...}]->(:Test)`
    - `(:Test)-[:FAILED_IN {source: 'test_run', error_message: ..., commit_sha: ...}]->(:Run)`
- **`c4_traversal_queries`**: **PASS**
  - Multi-hop inbound callers query verified.
  - Confidence-filtered test coverage query verified.

### 2. Regression Evals (Safety & Non-Regression)
- **`r1_test_suite_passes`**: **PASS**
  - All 11 unit/integration tests in `tests/` pass in 0.14s.
- **`r2_flask_real_ingest`**: **PASS**
  - Full ingestion of target repo `pallets/flask` without parse errors.
  - Parsed 419 production functions, 1,043 test functions, 215 static call edges.
- **`r3_cli_stats_and_callers`**: **PASS**
  - `guard stats` and `guard callers` CLI commands execute cleanly on live target graph.
