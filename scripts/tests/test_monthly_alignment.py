import copy
import json
from pathlib import Path
import unittest

from scripts.verify_monthly_alignment import validate, validate_documents, ROOT, SNAPSHOT


class MonthlyAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(SNAPSHOT.read_text())

    def test_captured_alignment_and_documents(self):
        self.assertEqual(validate(self.data), [])
        self.assertEqual(validate_documents(ROOT, self.data), [])

    def test_scope_approval_cannot_grant_release_acceptance(self):
        for field in ['production_acceptance', 'independent_acceptance', 'exhaustive_semantic_audit']:
            changed = copy.deepcopy(self.data)
            changed[field] = True
            with self.subTest(field=field):
                self.assertTrue(validate(changed))

    def test_missing_or_duplicate_issue_is_rejected(self):
        self.data['issues'].pop()
        self.data['coverage']['public_open_issues'] -= 1
        self.assertTrue(validate(self.data))
        self.setUp()
        self.data['issues'].append(self.data['issues'][0])
        self.assertTrue(validate(self.data))

    def test_cross_repository_issue_number_cannot_be_rebound(self):
        self.data['issues'][0]['repo'] = 'Conxian/conxian-nexus'
        self.assertTrue(validate(self.data))

    def test_source_pin_and_claim_lineage_are_required(self):
        self.data['sources'][0]['commit'] = 'main'
        self.assertTrue(validate(self.data))
        self.setUp()
        self.data['claims'][0]['source_ids'] = ['unobserved']
        self.assertTrue(validate(self.data))

    def test_unqualified_production_claim_is_rejected(self):
        self.data['claims'][0]['state'] = 'production-ready'
        self.assertTrue(validate(self.data))

    def test_r5_and_itil_meanings_cannot_silently_change(self):
        self.data['phases'][-1]['name'] = 'Accepted production'
        self.assertTrue(validate(self.data))
        self.setUp()
        self.data['itil5_activities'] = ['Strategy', 'Design', 'Transition', 'Operation', 'Improvement']
        self.assertTrue(validate(self.data))

    def test_cycles_and_unknown_dependencies_are_rejected(self):
        self.data['groups'][0]['depends_on'] = [self.data['groups'][0]['id']]
        self.assertTrue(validate(self.data))
        self.setUp()
        self.data['groups'][0]['depends_on'] = ['new-authority']
        self.assertTrue(validate(self.data))

    def test_private_material_or_invented_project_mutation_is_rejected(self):
        self.data['sources'][0]['repository'] = 'Conxian/.github-private'
        self.assertTrue(validate(self.data))
        self.setUp()
        self.data['project_alignment']['mutation_performed'] = True
        self.assertTrue(validate(self.data))

    def test_fixture_recovery_cannot_become_independent_operation(self):
        self.data['recovery_fixture']['operator_independence_verified'] = True
        self.assertTrue(validate(self.data))


if __name__ == '__main__':
    unittest.main()
