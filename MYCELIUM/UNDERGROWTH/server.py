"""Local-only, read-only synthetic UG-001 viewer. Run: python3 server.py.
No live data paths, persistence, external dependencies or write endpoints.
"""
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from ug001 import build, candidate_conflicts

ROOT = Path(__file__).resolve().parent


def snapshot():
    with sqlite3.connect(':memory:') as db:
        db.execute('PRAGMA foreign_keys=ON')
        build(db)
        db.row_factory = sqlite3.Row
        def rows(sql):
            return [dict(r) for r in db.execute(sql)]
        return {
            'dataset': 'UG-001 synthetic in-memory fixture',
            'claims': rows('SELECT c.id,c.subject,c.predicate,c.value,c.valid_time,c.scope,c.source_id,s.title AS source_title,s.upstream FROM claim c JOIN source s ON s.id=c.source_id ORDER BY c.id'),
            'sources': rows('SELECT id,title,upstream FROM source ORDER BY id'),
            'conflicts': rows('SELECT id,claim_a,claim_b,basis,status FROM conflict ORDER BY id'),
            'detected_pairs': [list(pair) for pair in candidate_conflicts(db)],
            'hypotheses': rows('SELECT id,explanation,status FROM hypothesis ORDER BY id'),
            'hypothesis_links': rows('SELECT hypothesis_id,claim_id FROM hypothesis_link ORDER BY hypothesis_id,claim_id'),
            'disposition': 'INCONCLUSIVE',
        }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/snapshot':
            payload = json.dumps(snapshot()).encode('utf-8')
            mime = 'application/json; charset=utf-8'
        elif path in ('/', '/connected.html'):
            payload = (ROOT / 'connected.html').read_bytes()
            mime = 'text/html; charset=utf-8'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        self.send_error(405, 'Read-only interface')


if __name__ == '__main__':
    address = ('127.0.0.1', 8766)
    print(f'UNDERGROWTH synthetic viewer: http://{address[0]}:{address[1]}')
    ThreadingHTTPServer(address, Handler).serve_forever()
