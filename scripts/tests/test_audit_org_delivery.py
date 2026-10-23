import copy
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.audit_org_delivery import audit

NOW = datetime(2026, 10, 21, 7, 0, tzinfo=timezone.utc)
D, S, M = "d" * 40, "a" * 40, "b" * 40


def fixture():
    return {"captured_at": "2026-10-21T07:00:00Z", "inventory_complete": True,
            "expected_repositories": ["Conxian/example"], "delivery_loop_enabled": True,
            "repositories": [{"name": "Conxian/example", "promotion_chain": True,
                              "prs_complete": True, "prs": [],
                              "refs": {"dev": D, "staged": S, "main": M},
                              "trees": {"dev": "t", "staged": "t", "main": "t"},
                              "lineage": {"staged_in_dev": True, "main_in_staged": True}}]}


def candidate():
    return {"number": 1, "head_ref": "promotion/dev-to-staged-" + D,
            "head_sha": D, "source_sha": D, "target_base_sha": S,
            "base_sha": S, "base_ref": "staged", "next_action": "verify scoped acceptance",
            "owner_issue": "https://github.com/Conxian/example/issues/2",
            "files_complete": True, "checks_complete": True, "statuses_complete": True,
            "reviews_complete": True, "review_gate": "satisfied", "statuses": [],
            "checks": [{"head_sha": D, "status": "completed", "conclusion": "success"}]}


class DeliveryAuditTests(unittest.TestCase):
    def setUp(self):
        self.s = fixture()
        self.r = self.s["repositories"][0]

    def actions(self):
        return {x["action"] for x in audit(self.s, NOW)["actions"]}

    def with_pr(self):
        p = candidate()
        self.r["prs"] = [p]
        return p

    def test_settled_repo_has_no_invented_work(self):
        self.assertEqual(self.actions(), set())

    def test_paused_loop_is_an_action_even_with_zero_prs(self):
        self.s["delivery_loop_enabled"] = False
        self.assertIn("RESTORE_OWNER_AUTHORIZED_DELIVERY_LOOP", self.actions())

    def test_missing_repo_is_not_empty_queue_success(self):
        self.s["expected_repositories"].append("Conxian/missing")
        self.assertFalse(audit(self.s, NOW)["coverage_complete"])

    def test_duplicate_repo_cannot_mask_missing_repo(self):
        self.s["repositories"].append(copy.deepcopy(self.r))
        self.assertIn("COMPLETE_ORG_INVENTORY", self.actions())

    def test_truncated_read_cannot_hide_other_repos(self):
        second = copy.deepcopy(self.r)
        second["name"] = "Conxian/other"
        second["prs_complete"] = False
        self.s["expected_repositories"].append(second["name"])
        self.s["repositories"].append(second)
        self.assertIn("COMPLETE_REPOSITORY_PR_READ", self.actions())

    def test_stale_snapshot_is_not_current_evidence(self):
        self.s["captured_at"] = "2026-10-20T07:00:00Z"
        self.assertIn("REFRESH_SNAPSHOT", self.actions())

    def test_mutated_head_is_caught_even_with_green_old_validator(self):
        p = self.with_pr()
        p["head_sha"] = "e" * 40
        p["checks"][0]["head_sha"] = p["head_sha"]
        self.assertIn("REPAIR_MUTATED_IMMUTABLE_CANDIDATE", self.actions())

    def test_stale_base_is_caught(self):
        p = self.with_pr()
        p["target_base_sha"] = M
        self.assertIn("REPLACE_STALE_TARGET_CANDIDATE", self.actions())

    def test_obsolete_source_requires_retention_proof_not_blind_close(self):
        self.with_pr()
        self.r["refs"]["dev"] = "f" * 40
        self.assertIn("VERIFY_REPLACEMENT_AND_RETENTION", self.actions())

    def test_empty_checks_fail_closed(self):
        self.with_pr()["checks"] = []
        self.assertIn("REFRESH_CHECK_EVIDENCE", self.actions())

    def test_checks_from_previous_head_are_not_current(self):
        self.with_pr()["checks"][0]["head_sha"] = M
        self.assertIn("REFRESH_CHECK_EVIDENCE", self.actions())

    def test_pending_and_failed_checks_have_distinct_actions(self):
        p = self.with_pr()
        p["checks"] += [{"head_sha": D, "status": "in_progress", "conclusion": None},
                        {"head_sha": D, "status": "completed", "conclusion": "failure"}]
        self.assertTrue({"FOLLOW_PENDING_CHECKS", "REMEDIATE_FAILED_CHECKS"} <= self.actions())

    def test_only_skipped_checks_are_not_called_success(self):
        self.with_pr()["checks"][0]["conclusion"] = "skipped"
        self.assertIn("OBTAIN_APPLICABLE_SUCCESSFUL_CHECKS", self.actions())

    def test_status_failure_is_not_hidden_by_green_checks(self):
        self.with_pr()["statuses"] = [{"head_sha": D, "state": "failure"}]
        self.assertIn("RESOLVE_COMMIT_STATUS", self.actions())

    def test_review_required_even_after_green_checks(self):
        self.with_pr()["review_gate"] = "blocked"
        self.assertIn("COMPLETE_REQUIRED_REVIEW", self.actions())

    def test_workflow_delta_requires_separate_owner_request(self):
        self.with_pr()["protected_control_changes"] = [".github/workflows/ci.yml"]
        self.assertIn("SEPARATE_WORKFLOW_CHANGES_FROM_IMPLEMENTATION", self.actions())

    def test_dev_merge_does_not_end_delivery(self):
        self.r["trees"]["dev"] = "new"
        self.assertIn("GENERATE_CURRENT_STAGED_CANDIDATE", self.actions())

    def test_equal_content_does_not_prove_missing_parent(self):
        self.r["lineage"]["staged_in_dev"] = False
        self.assertIn("RECONCILE_ANCESTRY", self.actions())

    def test_soak_is_preserved_and_followed(self):
        self.r["trees"]["staged"] = self.r["trees"]["dev"] = "new"
        self.r["soak_satisfied"] = False
        self.assertIn("FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", self.actions())
        self.r["soak_satisfied"] = True
        self.assertIn("GENERATE_CURRENT_MAIN_CANDIDATE", self.actions())

    def test_acceptance_cannot_be_reused_for_different_head(self):
        p = self.with_pr()
        p.update(base_ref="main", main_acceptance="accepted", acceptance_head_sha=M)
        self.assertIn("COMPLETE_EXACT_MAIN_ACCEPTANCE", self.actions())

    def test_deployment_must_match_main(self):
        self.r.update(deployment_required=True, deployment_source_sha=S)
        self.assertIn("VERIFY_OR_REMEDIATE_DEPLOYED_SOURCE", self.actions())

    def test_existing_main_candidate_still_requires_soak(self):
        p = self.with_pr()
        p.update(head_ref="promotion/staged-to-main-" + S, head_sha=S,
                 source_sha=S, target_base_sha=M, base_sha=M, base_ref="main",
                 main_acceptance="accepted", acceptance_head_sha=S,
                 checks=[{"head_sha": S, "status": "completed", "conclusion": "success"}])
        self.r["soak_satisfied"] = False
        self.assertIn("FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", self.actions())
        self.r["soak_satisfied"] = True
        self.assertNotIn("FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", self.actions())

    def test_non_chain_service_deployment_is_still_checked(self):
        self.r.update(promotion_chain=False, refs={"main": M},
                      deployment_required=True, deployment_source_sha=S)
        self.assertIn("VERIFY_OR_REMEDIATE_DEPLOYED_SOURCE", self.actions())
        self.r["deployment_source_sha"] = M
        self.assertNotIn("VERIFY_OR_REMEDIATE_DEPLOYED_SOURCE", self.actions())

    def test_non_chain_deployment_cannot_hide_missing_main(self):
        self.r.update(promotion_chain=False, refs={}, deployment_required=True)
        self.assertIn("REFRESH_BRANCH_HEADS", self.actions())
        self.assertFalse(audit(self.s, NOW)["coverage_complete"])

    def test_every_pr_needs_concrete_owner_and_next_action(self):
        self.with_pr().pop("next_action")
        self.assertIn("RECORD_NEXT_ACTION_AND_OWNER", self.actions())

    def test_missing_status_collection_is_incomplete_even_when_flag_is_true(self):
        self.with_pr().pop("statuses")
        self.assertIn("REFRESH_CHECK_EVIDENCE", self.actions())
        self.assertFalse(audit(self.s, NOW)["coverage_complete"])

    def test_invalid_status_collection_is_incomplete(self):
        for value in (None, {}, "success", [None]):
            with self.subTest(value=value):
                self.with_pr()["statuses"] = value
                self.assertIn("REFRESH_CHECK_EVIDENCE", self.actions())

    def test_invalid_check_collection_is_incomplete(self):
        for value in ({"conclusion": "success"}, "success", [None]):
            with self.subTest(value=value):
                self.with_pr()["checks"] = value
                self.assertIn("REFRESH_CHECK_EVIDENCE", self.actions())

    def test_promotion_lane_must_match_actual_target(self):
        self.with_pr()["base_ref"] = "dev"
        self.assertIn("REPAIR_PROMOTION_ROUTE", self.actions())

    def test_malformed_immutable_name_is_not_ordinary_work(self):
        for ref in ("promotion/dev-to-staged-short", "promotion/staged-to-main-" + D.upper()):
            with self.subTest(ref=ref):
                self.with_pr()["head_ref"] = ref
                self.assertIn("REPAIR_PROMOTION_ROUTE", self.actions())

    def test_missing_or_malformed_actual_head_requires_refresh(self):
        for value in (None, "short", 123):
            with self.subTest(value=value):
                self.with_pr()["head_sha"] = value
                self.assertIn("REFRESH_PR_IDENTITY", self.actions())
                self.assertFalse(audit(self.s, NOW)["coverage_complete"])

    def test_actual_base_must_match_current_target_for_feature_pr(self):
        p = self.with_pr()
        p.update(head_ref="fix/example", base_ref="dev", base_sha=M)
        self.assertIn("REFRESH_PR_IDENTITY", self.actions())

    def test_invalid_pr_entry_does_not_hide_other_candidates(self):
        p = self.with_pr()
        p["review_gate"] = "blocked"
        self.r["prs"].insert(0, None)
        self.assertTrue({"COMPLETE_REPOSITORY_PR_READ", "COMPLETE_REQUIRED_REVIEW"} <= self.actions())

    def test_nonpositive_or_boolean_pr_number_is_invalid(self):
        for number in (0, -1, True):
            with self.subTest(number=number):
                self.with_pr()["number"] = number
                self.assertIn("COMPLETE_REPOSITORY_PR_READ", self.actions())

    def test_invalid_inventory_name_is_not_complete_coverage(self):
        for value in (None, {}, ""):
            with self.subTest(value=value):
                self.s["expected_repositories"] = [value]
                self.assertFalse(audit(self.s, NOW)["coverage_complete"])

    def test_promotion_requires_separate_exact_dependency_validation(self):
        p = self.with_pr()
        action = "COLLECT_EXACT_DEPENDENCY_VALIDATION"
        self.assertIn(action, self.actions())
        p["dependency_validation"] = {
            "head_sha": D, "dependency_files_changed": True,
            "frozen_or_locked": True, "result": "success", "evidence_ref": "ci/run/1"}
        self.assertNotIn(action, self.actions())
        for key, value in (("head_sha", M), ("result", "skipped"),
                           ("result", "failure"), ("result", "pending"),
                           ("frozen_or_locked", False), ("evidence_ref", ""),
                           ("dependency_files_changed", None)):
            with self.subTest(key=key, value=value):
                original = copy.deepcopy(p["dependency_validation"])
                p["dependency_validation"][key] = value
                self.assertIn(action, self.actions())
                p["dependency_validation"] = original

    def test_dependency_nonapplicability_requires_bound_explicit_diff_rationale(self):
        p = self.with_pr()
        action = "COLLECT_EXACT_DEPENDENCY_VALIDATION"
        p["dependency_validation"] = {
            "head_sha": D, "dependency_files_changed": False,
            "result": "not_applicable", "rationale": "Full diff contains documentation only"}
        self.assertNotIn(action, self.actions())
        p["dependency_validation"]["rationale"] = " "
        self.assertIn(action, self.actions())

    def deployment(self):
        target = {"provider": "provider", "scope": "private-scope", "service": "private-service",
                  "environment": "production", "source_sha": M,
                  "artifact_digest": "sha256:" + "a" * 64}
        observed = dict(target, deployment_id="private-deploy", state="live",
                        observed_at="2026-10-21T07:00:00Z")
        self.r.update(deployment_required=True, deployment_source_sha=M,
                      deployments_complete=True, deployment_targets=[target],
                      deployment_observations=[observed])
        return target, observed

    def test_deployment_requires_more_than_matching_commit(self):
        self.r.update(deployment_required=True, deployment_source_sha=M)
        self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())
        self.deployment()
        self.assertNotIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_matching_source_does_not_hide_wrong_artifact_or_target(self):
        for key, value in (("artifact_digest", "sha256:" + "b" * 64),
                           ("provider", "other"), ("scope", "other"),
                           ("service", "other"), ("environment", "preview"),
                           ("source_sha", S), ("deployment_id", " ")):
            with self.subTest(key=key):
                _, observed = self.deployment()
                observed[key] = value
                self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_deployment_unknown_failed_or_pending_is_not_live(self):
        for state in (None, "", "unknown", "build_failed", "queued", "building"):
            with self.subTest(state=state):
                _, observed = self.deployment()
                observed["state"] = state
                self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_provider_observation_age_is_independent_of_snapshot_age(self):
        for observed_at in (None, "bad", "2026-10-21T07:00:00",
                            "2026-10-21T05:59:59Z", "2026-10-21T07:00:01Z"):
            with self.subTest(observed_at=observed_at):
                _, observed = self.deployment()
                observed["observed_at"] = observed_at
                self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_incomplete_empty_duplicate_or_malformed_deployments_fail_closed(self):
        for key in ("deployment_targets", "deployment_observations"):
            for value in (None, [], {}, [None]):
                with self.subTest(key=key, value=value):
                    self.deployment()
                    self.r[key] = value
                    self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())
            self.deployment()
            self.r[key] *= 2
            self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())
        self.deployment()
        self.r["deployments_complete"] = False
        self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_every_intended_service_must_be_observed(self):
        target, _ = self.deployment()
        self.r["deployment_targets"].append(dict(target, service="second-service"))
        self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_mutable_or_malformed_intended_digest_is_rejected(self):
        for value in (None, "latest", "sha256:short", "sha256:" + "A" * 64):
            with self.subTest(value=value):
                target, observed = self.deployment()
                target["artifact_digest"] = observed["artifact_digest"] = value
                self.assertIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())

    def test_action_plan_does_not_disclose_private_deployment_identifiers(self):
        _, observed = self.deployment()
        observed["state"] = "build_failed"
        result = str(audit(self.s, NOW))
        for private in ("private-scope", "private-service", "private-deploy", "sha256:"):
            self.assertNotIn(private, result)

    def test_governance_repo_does_not_require_invented_hosting(self):
        self.assertNotIn("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", self.actions())


if __name__ == "__main__":
    unittest.main()
