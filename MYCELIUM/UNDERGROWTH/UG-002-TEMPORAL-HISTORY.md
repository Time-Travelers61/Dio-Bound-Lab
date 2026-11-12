# UG-002 — Temporal Evidence History

**Status:** Prototype committed; tests authored but not executed or independently qualified.

## Question
Can a knowledge system preserve what a source said before, what a later source says now, and why the record changed, without silently rewriting history or confusing the latest assertion with truth?

## Design
`temporal.py` creates an append-only SQLite `assertion_event` ledger. Every assertion records claim identity, revision, event kind, value, validity interval (optional), recording timestamp, source label, rationale and immediate predecessor. SQL triggers reject UPDATE and DELETE on history rows. Corrections and retractions append new events; `history()` returns the full sequence and `latest_state()` returns the most recently recorded event, explicitly not a verified truth claim.

`test_temporal.py` supplies seven synthetic unit tests covering correction lineage, retraction preservation, invalid transitions, claim identity, immutability and required provenance. No test execution is claimed.

## Limitations and unresolved seams
- Source labels and timestamps are caller-supplied; this does not authenticate witnesses, clocks or execution.
- Application-level sequential revision assignment is not safe for concurrent writers without a transaction/locking strategy.
- `recorded_at` and validity strings are not normalized to a trusted temporal format. `latest_state()` orders by revision, not by a trusted clock.
- Retraction semantics are preserved as an event but not interpreted by downstream query policy.
- Triggers are not tamper-proof against a database administrator or direct file replacement.
- No integration with the existing UG-001 schema, lineage engine or live Obsidian database is claimed.

## Next smallest gate
Execute the synthetic tests in a disposable environment; capture command, Python/SQLite versions, exits and results. Then test simultaneous writers and explicit `valid_time` versus `recorded_at` cases before integration. Preserve failures and dissent rather than promoting the design on the strength of a commit alone.

**Custody:** GitHub source additions only. No live database edits, service changes, deployment or new permissions. Human authority reserved.
