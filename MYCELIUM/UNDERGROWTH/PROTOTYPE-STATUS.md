# UG-001 — Prototype status (2026-11-12)

**Status:** Source committed; execution and test results **NOT VERIFIED** in this review. Human authority reserved.

## What exists

- `ug001.py`: standard-library SQLite experiment using a temporary disposable database, two fictional contradictory claims, source attribution, a conflict candidate query, and two explicitly UNVERIFIED hypotheses. No network, device, or live Obsidian/Langley access.
- `test_ug001.py`: seven authored tests for preserving claims, hypotheses, missing sources, time and scope mismatch, shared upstream provenance, and forged authority text.

## How to inspect or run (only on an authorized disposable environment)

From `MYCELIUM/UNDERGROWTH`:

```sh
python3 -m unittest -v test_ug001.py
python3 ug001.py
```

No test run is claimed by this commit. Tests describe intended checks, not independently verified results.

## Known limits / objections

- Conflict matching is deliberately narrow and does not solve semantic equivalence, clock granularity, or ontology differences. A candidate conflict is not proof either source is false.
- Hypotheses are fixture-authored; the system does not generate or evaluate new explanations autonomously.
- Source independence is represented by an `upstream` label, not established by evidence custody.
- There is no immutable event ledger, access control, source passage offsets, historical supersession, cryptographic custody, UI, or integration with MYCELIUM/Obsidian.
- SQLite CHECK constraints protect the prototype's hypothesis status, not a production authorization model.
- `candidate_conflicts` queries claims directly; the `conflict` table records the fixture conflict separately and is not automatically reconciled.

## Next bounded gate

Review the source and run the seven tests in a disposable authorized environment; record exact Python version, command, exit status, and results. Then design append-only event history and provenance-aware independence before expanding beyond synthetic records. Do not touch live project databases without separate authorization.
