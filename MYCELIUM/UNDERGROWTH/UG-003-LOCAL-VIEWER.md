# UG-003 — Local SQLite evidence viewer

Status: IMPLEMENTED IN SOURCE; NOT EXECUTION-QUALIFIED.

This is a minimal bridge from the UG-001 SQLite fixture to a browser UI, without modifying the earlier standalone `index.html` demonstration.

## Run locally

From `MYCELIUM/UNDERGROWTH`, run `python3 server.py`, then open `http://127.0.0.1:8766/`. Python standard library only. The server binds to loopback only. Stop it with Ctrl-C.

`GET /api/snapshot` builds the existing UG-001 synthetic fixture in a fresh in-memory SQLite database, then returns claims, sources, recorded conflicts, computed candidate conflict pairs, hypotheses and links. The UI reads this JSON, supports claim search and view switching. POST is rejected. No live Obsidian data, arbitrary filesystem path, external API, persistent database or mutation route is supported.

## Verification boundaries

GitHub file creation and visibility are documentary evidence only. Server startup, browser interaction, test results and operational security have not been independently verified in this pass. No deployment or live-database integration is claimed.

## Next gate

Run a controlled local smoke test and compare JSON claims/conflicts/hypotheses with `ug001.report()`; verify loopback binding, POST rejection, browser rendering and no disk writes. Separately consider adding temporal history as a read-only endpoint after tests are run. Keep human authority for any future live-data integration.
