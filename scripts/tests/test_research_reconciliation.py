import copy
import json
from pathlib import Path
import unittest

from scripts.verify_research_reconciliation import validate

ROOT = Path(__file__).resolve().parents[2]


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'docs/research_implementation_reconciliation_2026_10_15.json').read_text())
        self.historical = json.loads((ROOT / 'docs/bos_research_candidate_ledger.json').read_text())

    def test_current_snapshot_is_consistent(self):
        self.assertEqual(validate(self.data, self.historical), [])

    def test_cannot_turn_planning_into_production_acceptance(self):
        for field in ['production_authorization', 'independent_acceptance', 'restricted_details_included', 'exhaustive_security_audit']:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.data)
                changed[field] = True
                self.assertTrue(validate(changed, self.historical))

    def test_missing_issue_and_duplicate_assignments_fail(self):
        self.data['issue_alignment'].pop()
        self.assertTrue(validate(self.data, self.historical))
        self.setUp()
        self.data['issue_alignment'].append(self.data['issue_alignment'][0])
        self.assertTrue(validate(self.data, self.historical))

    def test_dependency_cycles_and_unknown_targets_fail(self):
        self.data['gaps'][0]['depends_on'] = [self.data['gaps'][0]['id']]
        self.assertIn('dependency cycle', validate(self.data, self.historical))
        self.data['gaps'][0]['depends_on'] = ['missing']
        self.assertTrue(validate(self.data, self.historical))

    def test_historical_scores_and_all_candidate_rows_are_preserved(self):
        self.data['legacy_candidates'][0]['historical_total'] += 1
        self.assertTrue(validate(self.data, self.historical))
        self.setUp()
        self.data['legacy_candidates'].pop()
        self.assertTrue(validate(self.data, self.historical))

    def test_mutable_source_pins_cannot_be_evidence(self):
        self.data['gaps'][0]['sources'][0]['commit'] = 'dev'
        self.assertTrue(validate(self.data, self.historical))

    def test_restricted_reproduction_cannot_enter_coordination(self):
        row = next(i for i in self.data['issue_alignment'] if i['restricted'])
        row['reproduction'] = 'restricted detail'
        self.assertTrue(validate(self.data, self.historical))

    def test_project_update_cannot_be_fabricated(self):
        self.data['project_alignment']['mutation_performed'] = True
        self.assertTrue(validate(self.data, self.historical))


if __name__ == '__main__':
    unittest.main()
