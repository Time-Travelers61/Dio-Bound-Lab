"""UG-002: append-only claim history for disposable SQLite experiments.

Records are historical assertions, not authenticated facts. No live database access.
"""
import sqlite3

HISTORY_SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS assertion_event (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT,
 claim_id TEXT NOT NULL,
 revision INTEGER NOT NULL CHECK(revision > 0),
 event_kind TEXT NOT NULL CHECK(event_kind IN ('ASSERT','CORRECT','RETRACT')),
 subject TEXT NOT NULL,
 predicate TEXT NOT NULL,
 value TEXT NOT NULL,
 valid_from TEXT,
 valid_to TEXT,
 recorded_at TEXT NOT NULL,
 source_id TEXT NOT NULL,
 rationale TEXT NOT NULL,
 supersedes_event_id INTEGER REFERENCES assertion_event(event_id),
 UNIQUE(claim_id, revision),
 CHECK(valid_to IS NULL OR valid_from IS NOT NULL),
 CHECK(valid_to IS NULL OR valid_to >= valid_from)
);
CREATE TRIGGER IF NOT EXISTS assertion_event_no_update
BEFORE UPDATE ON assertion_event BEGIN SELECT RAISE(ABORT, 'history is append-only'); END;
CREATE TRIGGER IF NOT EXISTS assertion_event_no_delete
BEFORE DELETE ON assertion_event BEGIN SELECT RAISE(ABORT, 'history is append-only'); END;
"""


def initialize(connection):
    connection.executescript(HISTORY_SCHEMA)


def append_event(connection, *, claim_id, event_kind, subject, predicate, value,
                 recorded_at, source_id, rationale, valid_from=None, valid_to=None):
    """Append an assertion or a correction/retraction referencing its immediate predecessor."""
    if not all((claim_id, subject, predicate, value, recorded_at, source_id, rationale)):
        raise ValueError('Required fields must be nonempty')
    if event_kind not in ('ASSERT', 'CORRECT', 'RETRACT'):
        raise ValueError('Unknown event kind')
    previous = connection.execute(
        'SELECT event_id,revision,subject,predicate FROM assertion_event '
        'WHERE claim_id=? ORDER BY revision DESC LIMIT 1', (claim_id,)
    ).fetchone()
    if (previous is None and event_kind != 'ASSERT') or (previous is not None and event_kind == 'ASSERT'):
        raise ValueError('ASSERT starts a claim; CORRECT or RETRACT follows an existing claim')
    if previous and (subject, predicate) != (previous[2], previous[3]):
        raise ValueError('Corrections cannot silently change claim identity')
    revision = previous[1] + 1 if previous else 1
    cursor = connection.execute('''INSERT INTO assertion_event
      (claim_id,revision,event_kind,subject,predicate,value,valid_from,valid_to,
       recorded_at,source_id,rationale,supersedes_event_id)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
      (claim_id, revision, event_kind, subject, predicate, value, valid_from,
       valid_to, recorded_at, source_id, rationale, previous[0] if previous else None))
    return cursor.lastrowid


def history(connection, claim_id):
    return connection.execute('''SELECT event_id,revision,event_kind,value,recorded_at,
      source_id,rationale,supersedes_event_id FROM assertion_event
      WHERE claim_id=? ORDER BY revision''', (claim_id,)).fetchall()


def latest_state(connection, claim_id):
    """Return latest recorded assertion, not a truth or independent verification verdict."""
    return connection.execute('''SELECT event_id,revision,event_kind,value,recorded_at
      FROM assertion_event WHERE claim_id=? ORDER BY revision DESC LIMIT 1''',
      (claim_id,)).fetchone()
