# Deviations Log

This file records any deviations from `PLAN.md` required by rules R5, R7, and Part D.
Every entry must include the date/timestamp, affected task, reason, and impact on frozen claims or metrics.

| Date | Task | Deviation | Reason | Approved By |
| --- | --- | --- | --- | --- |
| Initialized | - | None | - | - |
| 2026-10-16 | T1 | Marked status as pending verification instead of [x] | Rule R9 requires an independent verifier report ending in VERDICT: PASS before ticking [x] | System / Plan Update |
| 2026-10-16 | T5 | Built T5 before its dependency T5a (and before T4) | Human operator requested T5 on a separate branch. `guard/decision.py` is a pure engine (no DB, no diff wiring), so it does not consume T4 edges or T5a plumbing. Wiring T5 into an end-to-end path is still owned by T5a. | Human (operator) |
| 2026-10-16 | T5 | Defined `evidence_ratio` as the mean best covering-edge confidence per changed function (0.0 if none) | The literal "fraction of functions with evidence" makes the `<0.5 -> run all` policy tier unreachable under the frozen weights (it bottoms out at 0.7). Using edge confidence keeps the tier reachable and is consistent with per-edge confidence evidence. Weights/thresholds remain the frozen starting values and are still to be tuned on the calibration split. | Human (operator) |
