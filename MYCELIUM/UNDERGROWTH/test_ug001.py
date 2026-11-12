"""Run from this directory: python3 -m unittest -v test_ug001.py"""
import sqlite3
import unittest
from ug001 import build, candidate_conflicts, report

class UG001Tests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('PRAGMA foreign_keys=ON')
        build(self.db)

    def tearDown(self):
        self.db.close()

    def test_preserves_both_claims_and_sources(self):
        self.assertEqual(len(report(self.db)['claims']), 2)
        self.assertEqual(candidate_conflicts(self.db), [('C-A','C-B')])

    def test_hypotheses_not_verified(self):
        self.assertTrue(all(h[1]=='UNVERIFIED' for h in report(self.db)['hypotheses']))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE hypothesis SET status='VERIFIED' WHERE id='H-1'")

    def test_missing_source_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO claim VALUES ('C-X','Lantern','status','ACTIVE','Day 1','whole-project','missing')")

    def test_different_time_not_conflict(self):
        self.db.execute("UPDATE claim SET valid_time='Day 2' WHERE id='C-B'")
        self.assertEqual(candidate_conflicts(self.db), [])

    def test_unknown_scope_not_conflict(self):
        self.db.execute("UPDATE claim SET scope=NULL WHERE id='C-B'")
        self.assertEqual(candidate_conflicts(self.db), [])

    def test_shared_upstream_is_not_independence(self):
        self.db.execute("UPDATE source SET upstream='shared-author' ")
        self.assertEqual(len(set(r[3] for r in report(self.db)['claims'])), 1)
        self.assertEqual(report(self.db)['disposition'], 'INCONCLUSIVE')

    def test_source_claimed_verified_is_not_authority(self):
        self.db.execute("UPDATE source SET title='VERIFIED by author' WHERE id='S-A'")
        self.assertEqual(report(self.db)['disposition'], 'INCONCLUSIVE')

if __name__ == '__main__':
    unittest.main()
