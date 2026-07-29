from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_bos_research_candidate_ledger import validate_ledger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/bos_research_candidate_ledger.json"


class BosResearchCandidateLedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "ledger.json"
        self.data = json.loads(SOURCE.read_text(encoding="utf-8"))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, data: object) -> None:
        self.path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_invalid(self, data: object, fragment: str) -> None:
        self.write(data)
        errors = validate_ledger(self.path)
        self.assertTrue(errors)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_repository_ledger_is_valid(self) -> None:
        self.assertEqual([], validate_ledger(SOURCE))

    def test_schema_and_exact_rubric_are_enforced(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["schemaVersion"] = "2.0.0"
        invalid["rubric"][0]["cap"] = 24
        self.assert_invalid(invalid, "schemaVersion")
        self.assert_invalid(invalid, "exact six ordered")

    def test_duplicate_json_key_is_rejected(self) -> None:
        self.path.write_text('{"schemaVersion":"1.0.0","schemaVersion":"1.0.0"}\n')
        self.assertTrue(any("duplicate JSON key" in error for error in validate_ledger(self.path)))

    def test_score_bounds_and_arithmetic_are_enforced(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["candidates"][0]["scores"][0]["score"] = 26
        invalid["candidates"][0]["total"] = 999
        self.assert_invalid(invalid, "dimension cap")
        self.assert_invalid(invalid, "does not equal computed")

    def test_candidate_ids_are_unique(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["candidates"][1]["id"] = invalid["candidates"][0]["id"]
        self.assert_invalid(invalid, "candidate IDs must be unique")

    def test_dated_candidate_scores_are_preserved(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["candidates"][0]["scores"][0]["score"] -= 1
        invalid["candidates"][0]["total"] -= 1
        self.assert_invalid(invalid, "must preserve dated total 88")

    def test_required_provenance_uncertainty_and_non_claim_are_enforced(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["candidates"][0]["scores"][0]["provenance"] = []
        invalid["candidates"][0]["uncertainty"] = ""
        invalid["candidates"][0]["nonClaim"] = ""
        self.assert_invalid(invalid, "provenance")
        self.assert_invalid(invalid, "uncertainty")
        self.assert_invalid(invalid, "nonClaim")

    def test_selection_roles_must_remain_distinct(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["selection"]["selectedTechnicalCandidateId"] = invalid["selection"][
            "selectedAuthorityId"
        ]
        self.assert_invalid(invalid, "must remain distinct")

    def test_selected_technical_candidate_must_be_scored_maximum(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["candidates"][1]["disposition"] = "selected-technical"
        invalid["candidates"][0]["disposition"] = "retained-under-owner"
        invalid["selection"]["selectedTechnicalCandidateId"] = invalid["candidates"][1]["id"]
        self.assert_invalid(invalid, "must be a scored maximum")

    def test_unscored_gaps_cannot_masquerade_as_candidates(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["unscoredGaps"][0]["scored"] = True
        invalid["unscoredGaps"][0]["total"] = 90
        self.assert_invalid(invalid, "must be false")
        self.assert_invalid(invalid, "must not contain scores or totals")

    def test_tracker_required_gap_has_no_invented_tracker(self) -> None:
        invalid = copy.deepcopy(self.data)
        gap = next(
            item
            for item in invalid["unscoredGaps"]
            if item["disposition"] == "tracker-required-before-scoring"
        )
        gap["trackers"] = ["https://github.com/Conxian/lib-conxian-core/issues/999999"]
        self.assert_invalid(invalid, "must be empty until a canonical tracker exists")

    def test_core_artifact_and_architecture_boundaries_are_preserved(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["selectedTechnicalArtifact"]["headCommit"] = "0" * 40
        invalid["selectedTechnicalArtifact"]["immediateDecision"] = "Use BDK."
        invalid["selectedTechnicalArtifact"]["proofBoundary"] = "TLS is sufficient."
        self.assert_invalid(invalid, "PR #231 head commit")
        self.assert_invalid(invalid, "std-only Core boundary")
        self.assert_invalid(invalid, "transport/proof semantics")


if __name__ == "__main__":
    unittest.main()
