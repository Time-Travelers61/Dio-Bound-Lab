"""UG-002 synthetic history tests. Run: python3 -m unittest test_temporal.py"""
import sqlite3
import unittest
from temporal import initialize, append_event, history, latest_state


class TemporalTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        initialize(self.db)
        self.base = dict(claim_id='C1', subject='Lantern', predicate='status',
                         value='ACTIVE', recorded_at='2026-11-01T00:00:00Z',
                         source_id='S1', rationale='Initial source statement')

    def tearDown(self):
        self.db.close()

    def test_correction_preserves_prior_assertion(self):
        first = append_event(self.db, event_kind='ASSERT', **self.base)
        correction = dict(self.base, value='PAUSED', recorded_at='2026-11-02T00:00:00Z',
                          source_id='S2', rationale='New contradictory report')
        second = append_event(self.db, event_kind='CORRECT', **correction)
        entries = history(self.db, 'C1')
        self.assertEqual([x[3] for x in entries], ['ACTIVE', 'PAUSED'])
        self.assertEqual(entries[1][7], first)
        self.assertEqual(latest_state(self.db, 'C1')[0], second)

    def test_retraction_retains_evidence(self):
        append_event(self.db, event_kind='ASSERT', **self.base)
        append_event(self.db, event_kind='RETRACT', **dict(self.base, rationale='Source withdrew claim'))
        self.assertEqual(len(history(self.db, 'C1')), 2)
        self.assertEqual(latest_state(self.db, 'C1')[2], 'RETRACT')

    def test_no_correction_without_original(self):
        with self.assertRaises(ValueError):
            append_event(self.db, event_kind='CORRECT', **self.base)

    def test_no_duplicate_initial_assertion(self):
        append_event(self.db, event_kind='ASSERT', **self.base)
        with self.assertRaises(ValueError):
            append_event(self.db, event_kind='ASSERT', **self.base)

    def test_identity_change_rejected(self):
        append_event(self.db, event_kind='ASSERT', **self.base)
        with self.assertRaises(ValueError):
            append_event(self.db, event_kind='CORRECT', **dict(self.base, subject='Other'))

    def test_history_immutable(self):
        append_event(self.db, event_kind='ASSERT', **self.base)
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE assertion_event SET value='OTHER'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('DELETE FROM assertion_event')

    def test_required_provenance(self):
        with self.assertRaises(ValueError):
            append_event(self.db, event_kind='ASSERT', **dict(self.base, source_id=''))


if __name__ == '__main__':
    unittest.main()
