"""Run in this directory: python3 -m unittest -v test_lineage.py"""
import sqlite3
import unittest
from ug001 import build
from lineage import lineage_assessment


class LineageTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('PRAGMA foreign_keys=ON')
        build(self.db)

    def tearDown(self):
        self.db.close()

    def test_distinct_declared_origins_not_proof(self):
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'C-B')['status'], 'INCONCLUSIVE')

    def test_common_origin(self):
        self.db.execute("UPDATE source SET upstream='shared-origin'")
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'C-B')['status'], 'SHARED_UPSTREAM')

    def test_same_source(self):
        self.db.execute("UPDATE claim SET source_id='S-A' WHERE id='C-B'")
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'C-B')['status'], 'SHARED_SOURCE')

    def test_unknown_origin(self):
        self.db.execute("UPDATE source SET upstream='' WHERE id='S-A'")
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'C-B')['status'], 'INCONCLUSIVE')

    def test_missing_claim(self):
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'missing')['status'], 'INCONCLUSIVE')

    def test_identical_claim_id(self):
        self.assertEqual(lineage_assessment(self.db, 'C-A', 'C-A')['status'], 'INCONCLUSIVE')


if __name__ == '__main__':
    unittest.main()
