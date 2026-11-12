# UG-004B — The Silent Forest

Date: 2026-11-12
Status: REPORTED synthetic experiment; independent reproduction INCONCLUSIVE.

## Purpose

Test whether a selective routing architecture misses contradictions that emerge across individually ordinary events. Compare (A) always-examine centralized baseline, (B) naive hybrid without cross-event aggregation, and (C) hybrid with a pattern accumulator.

## Reported results from group conversation

| Method | Cross-event contradictions detected | Simulated deep-reasoning invocations |
| --- | ---: | ---: |
| Centralized baseline | 100 / 100 | 10,000 |
| Naive hybrid | 0 / 100 | 0 |
| Hybrid with pattern accumulator | 100 / 100 | 100 |

These are conversation-reported outcomes, not independently reproduced measurements. No actual language-model inference or verified compute-cost measurement is established. The workload was constructed to expose cross-event contradictions; general reliability, latency, memory overhead, and real-world performance are not established. Reported execution was in memory and did not modify live databases. This commit only preserves the report.

## TRIDENT × MYCELIUM synthesis

- **SCAN:** The reported accumulator recovered the constructed contradictions missed by the naive hybrid.
- **IMMERSE:** The result is compatible with selective escalation but does not demonstrate superiority to conventional event-processing systems.
- **SQUIRREL — protected objection:** A pattern accumulator may only detect the classes of relationships it was designed to recognize. Correctness on a constructed workload does not establish safe routing on novel cases.
- **SYNTHESIZE:** The experiment motivates further controlled testing, not production admission.

## Next gate — UG-004C

Use reproducible synthetic fixtures with expected outcomes and a fixed random seed. Test duplicate and out-of-order events, stale source versions, conflicting event timestamps, dependency invalidation, and accumulated contradictions that cross entity boundaries. Compare false negatives, false positives, escalation counts, memory use, CPU time, and end-to-end latency. Preserve fixture hashes, source commit, execution command, environment, raw results, and deviations. Run only in an authorized disposable environment; do not touch live Obsidian data.

## Custody and limitations

This is a documentary commit, not a rerun or independent qualification. No execution, deployment, permission changes, or live database writes were performed for this record. Human authority reserved. Do not reopen unchanged findings without material new evidence.
