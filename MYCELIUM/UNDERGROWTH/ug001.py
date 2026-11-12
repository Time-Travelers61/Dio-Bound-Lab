"""UG-001: synthetic, disposable contradiction garden. Python standard library only.

Run: python3 ug001.py   (creates a temporary SQLite database and removes it)
No live project data, network access, or external database paths are used.
"""
import sqlite3
import tempfile
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE source (id TEXT PRIMARY KEY, title TEXT NOT NULL, upstream TEXT NOT NULL);
CREATE TABLE claim (id TEXT PRIMARY KEY, subject TEXT NOT NULL, predicate TEXT NOT NULL,
 value TEXT NOT NULL, valid_time TEXT, scope TEXT, source_id TEXT NOT NULL REFERENCES source(id));
CREATE TABLE conflict (id TEXT PRIMARY KEY, claim_a TEXT NOT NULL REFERENCES claim(id),
 claim_b TEXT NOT NULL REFERENCES claim(id), basis TEXT NOT NULL, status TEXT NOT NULL
 CHECK(status IN ('INCONCLUSIVE','RESOLVED')),
 CHECK(claim_a <> claim_b));
CREATE TABLE hypothesis (id TEXT PRIMARY KEY, explanation TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'UNVERIFIED' CHECK(status='UNVERIFIED'));
CREATE TABLE hypothesis_link (hypothesis_id TEXT REFERENCES hypothesis(id),
 claim_id TEXT REFERENCES claim(id), PRIMARY KEY(hypothesis_id, claim_id));
"""

def build(connection):
    connection.executescript(SCHEMA)
    connection.executemany('INSERT INTO source VALUES (?,?,?)', [
        ('S-A','Inventory Day 1','inventory-team'),
        ('S-B','Operations Day 1','operations-team')])
    connection.executemany('INSERT INTO claim VALUES (?,?,?,?,?,?,?)', [
        ('C-A','Lantern','status','ACTIVE','Day 1','whole-project','S-A'),
        ('C-B','Lantern','status','PAUSED','Day 1','whole-project','S-B')])
    connection.execute('INSERT INTO conflict VALUES (?,?,?,?,?)',
        ('K-1','C-A','C-B','Same subject, predicate, time, scope; different values','INCONCLUSIVE'))
    connection.executemany('INSERT INTO hypothesis(id,explanation) VALUES (?,?)', [
        ('H-1','Status may refer to distinct subsystems or definitions'),
        ('H-2','One source may be stale or incorrectly dated')])
    connection.executemany('INSERT INTO hypothesis_link VALUES (?,?)', [
        ('H-1','C-A'),('H-1','C-B'),('H-2','C-A'),('H-2','C-B')])
    connection.commit()

def candidate_conflicts(connection):
    """Return conflicting pairs only if subject/predicate/time/scope are fully specified and equal."""
    return connection.execute('''
      SELECT a.id,b.id FROM claim a JOIN claim b ON a.id < b.id
      WHERE a.subject=b.subject AND a.predicate=b.predicate
      AND a.valid_time IS NOT NULL AND b.valid_time IS NOT NULL
      AND a.scope IS NOT NULL AND b.scope IS NOT NULL
      AND a.valid_time=b.valid_time AND a.scope=b.scope AND a.value<>b.value
    ''').fetchall()

def report(connection):
    claims = connection.execute('''SELECT c.id,c.value,s.id,s.upstream FROM claim c
      JOIN source s ON s.id=c.source_id ORDER BY c.id''').fetchall()
    hypotheses = connection.execute('SELECT id,status,explanation FROM hypothesis ORDER BY id').fetchall()
    return {'claims': claims, 'conflicts': candidate_conflicts(connection),
            'hypotheses': hypotheses, 'disposition': 'INCONCLUSIVE'}

def main():
    with tempfile.TemporaryDirectory(prefix='undergrowth-ug001-') as directory:
        with sqlite3.connect(str(Path(directory) / 'synthetic.sqlite')) as db:
            db.execute('PRAGMA foreign_keys=ON')
            build(db)
            result = report(db)
            for label, rows in result.items():
                print(f'{label}: {rows}')

if __name__ == '__main__':
    main()
