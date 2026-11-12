# UG-004A — TRIDENT × MYCELIUM method comparison

Date: 2026-11-12
Status: REPORTED EXPERIMENT; independent execution verification INCONCLUSIVE.

## Scope and provenance

This record preserves the results described in the group conversation for a synthetic 10,000-event routing exercise, following the UG-004 conceptual design and TRIDENT v1.2 adversarial review. This commit does not reproduce the experiment, independently authenticate execution, or establish measured AI compute savings. The living boundary snapshot distinguishes reported outcomes from verified execution.

## Reported experiment

- Centralized baseline: 10,000 simulated deep-reasoning invocations for 10,000 events.
- Hybrid reflex routing: 100 simulated deep-reasoning invocations for 100 explicitly labeled anomalies.
- Both methods reportedly identified all 100 labeled anomalies.
- Derived reduction in *simulated invocation count*: (10,000 - 100) / 10,000 = 99%.
- No actual model inference, token measurement, energy accounting, or independently verified benchmark.
- The event labels made anomaly detection straightforward; the test does not demonstrate detection of emergent cross-event contradictions.

## Method comparison

| Method | Distinct strength | Risk | Best role |
| --- | --- | --- | --- |
| TRIDENT v1.2 | Structured adversarial challenge; SCAN/IMMERSE/SQUIRREL and explicit synthesis | Repeated headings can masquerade as independent concurrency; consensus can erase dissent | Qualification gates, threat-modeling, disputed claims |
| MYCELIUM | Adaptive scope and exploration; SPORE/ROOT/CANOPY/FRUITING; hypothesis discovery and evidence inheritance | Speculative branching can become costly, unfocused, or confused with established facts | Exploratory design, cross-domain connections, iterative research |
| Combined | MYCELIUM explores and chooses depth; TRIDENT stress-tests consequential hypotheses | Double-review overhead and repeated analysis of unchanged evidence | Material architecture decisions and milestone gates |

## Open objections

1. Unlabeled contradictions spanning individually ordinary events may be missed by a simple reflex gate.
2. Gate misrouting can silently suppress necessary deeper examination.
3. Cached findings may become invalid when source versions, assumptions, or rules change.
4. Pattern accumulation introduces state, ordering, duplicate, and overhead concerns.
5. Neither the 99% simulated count reduction nor the conceptual design establishes actual cost or correctness advantages.

## Next controlled experiment — UG-004B

Compare identical synthetic streams across (A) always-examine baseline, (B) selective hybrid without aggregation, and (C) hybrid with bounded pattern accumulator. Include unlabeled multi-event contradictions, duplicates, out-of-order arrival, and stale cached evidence. Record true/false positives, missed contradictions, escalations, wall-clock/CPU costs, and source-version consistency. No live database integration or production claim until independently checked.

## Custody

Documentary preservation only. No new execution, permission changes, merges, deployment, or modification to live Obsidian databases. Human authority reserved. Reopen review only for material new evidence.
