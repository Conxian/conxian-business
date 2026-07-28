from __future__ import annotations

import unittest

from scripts.branch_promotion_policy import (
    BOOTSTRAP_EXCEPTION,
    BootstrapException,
    PullRequestContext,
    validate_pull_request,
)


REPO = "Conxian/conxian-business"
SOURCE_SHA = "a" * 40
TARGET_SHA = "b" * 40

FEATURE_BODY = """<!-- PROMOTION:FEATURE->DEV -->
### Feature -> dev promotion checklist
- [x] scoped
"""
STAGED_BODY = """<!-- PROMOTION:DEV->STAGED -->
### Dev -> staged promotion checklist
- [x] wallet boundary
- [x] signer boundary
- [x] treasury boundary
- [x] deployment boundary
"""
MAIN_BODY = """### Mainnet acceptance evidence pack
#### Promotion metadata
#### Mainnet-only production scope
#### Contamination and residue proof
#### Successful production validation
#### Release-readiness sign-off
#### Owner accountability
"""
GENERATED_EVIDENCE = f"""
- Promotion source SHA: `{SOURCE_SHA}`
- Promotion target-base SHA: `{TARGET_SHA}`
- Promotion commit window: `{TARGET_SHA}..{SOURCE_SHA}`
"""


def context(
    head: str,
    base: str,
    body: str,
    *,
    number: int = 100,
    head_repo: str | None = REPO,
    actor: str = "contributor",
    head_sha: str = SOURCE_SHA,
    base_sha: str = TARGET_SHA,
) -> PullRequestContext:
    return PullRequestContext(
        number=number,
        base_ref=base,
        head_ref=head,
        base_sha=base_sha,
        head_sha=head_sha,
        base_repo=REPO,
        head_repo=head_repo,
        body=body,
        actor=actor,
    )


class BranchPromotionPolicyTests(unittest.TestCase):
    def assertAccepted(self, ctx: PullRequestContext, exception: BootstrapException | None = None) -> None:
        errors = validate_pull_request(ctx, exception or BootstrapException(0))
        self.assertEqual([], errors)

    def assertRejected(self, ctx: PullRequestContext, exception: BootstrapException | None = None) -> None:
        errors = validate_pull_request(ctx, exception or BootstrapException(0))
        self.assertTrue(errors)

    def test_ordinary_work_routes_to_dev(self) -> None:
        for head in (
            "feature/governance",
            "feat/governance",
            "fix/governance",
            "docs/governance",
            "chore/governance",
            "hotfix/governance",
            "dependabot/pip/pyyaml-7",
        ):
            with self.subTest(head=head):
                self.assertAccepted(context(head, "dev", FEATURE_BODY))

    def test_fork_ordinary_pr_routes_to_dev(self) -> None:
        self.assertAccepted(context("docs/governance", "dev", FEATURE_BODY, head_repo="fork/repo"))

    def test_dev_routes_to_staged(self) -> None:
        self.assertAccepted(context("dev", "staged", STAGED_BODY))

    def test_exact_generated_dev_candidate_routes_to_staged(self) -> None:
        self.assertAccepted(
            context(f"promotion/dev-to-staged-{SOURCE_SHA}", "staged", STAGED_BODY + GENERATED_EVIDENCE)
        )

    def test_staged_routes_to_main(self) -> None:
        self.assertAccepted(context("staged", "main", MAIN_BODY))

    def test_exact_generated_staged_candidate_routes_to_main(self) -> None:
        self.assertAccepted(
            context(f"promotion/staged-to-main-{SOURCE_SHA}", "main", MAIN_BODY + GENERATED_EVIDENCE)
        )

    def test_forked_promotion_is_rejected(self) -> None:
        self.assertRejected(context("dev", "staged", STAGED_BODY, head_repo="fork/repo"))

    def test_malformed_or_wildcard_promotion_is_rejected(self) -> None:
        for head, base, body in (
            ("promotion/dev-to-staged", "staged", STAGED_BODY),
            ("promotion/anything", "main", MAIN_BODY),
            (f"promotion/dev-to-staged-{'A' * 40}", "staged", STAGED_BODY),
        ):
            with self.subTest(head=head):
                self.assertRejected(context(head, base, body))

    def test_direct_dev_to_main_is_rejected(self) -> None:
        self.assertRejected(context("dev", "main", MAIN_BODY))

    def test_dependabot_to_main_is_rejected(self) -> None:
        self.assertRejected(
            context("dependabot/pip/pyyaml-7", "main", MAIN_BODY, actor="dependabot[bot]")
        )

    def test_missing_checklist_or_evidence_is_rejected(self) -> None:
        self.assertRejected(context("fix/no-checklist", "dev", ""))
        self.assertRejected(context("dev", "staged", ""))
        self.assertRejected(context("staged", "main", ""))

    def test_sha_body_mismatch_is_rejected(self) -> None:
        bad = GENERATED_EVIDENCE.replace(SOURCE_SHA, "c" * 40)
        self.assertRejected(
            context(f"promotion/dev-to-staged-{SOURCE_SHA}", "staged", STAGED_BODY + bad)
        )
        bad_target = GENERATED_EVIDENCE.replace(TARGET_SHA, "d" * 40)
        self.assertRejected(
            context(f"promotion/staged-to-main-{SOURCE_SHA}", "main", MAIN_BODY + bad_target)
        )

    def test_bootstrap_exception_accepts_only_exact_pr_head_base_and_repo(self) -> None:
        exception = BootstrapException(1234)
        exact = context(
            "promotion/con-1571-governance-bootstrap", "main", "", number=1234
        )
        self.assertAccepted(exact, exception)

        near_matches = (
            context("promotion/con-1571-governance-bootstrap", "main", "", number=1235),
            context("promotion/con-1571-governance-bootstrap-2", "main", "", number=1234),
            context("promotion/con-1571-governance-bootstrap", "staged", "", number=1234),
            context(
                "promotion/con-1571-governance-bootstrap",
                "main",
                "",
                number=1234,
                head_repo="fork/repo",
            ),
        )
        for candidate in near_matches:
            with self.subTest(candidate=candidate):
                self.assertRejected(candidate, exception)

    def test_configured_bootstrap_exception_is_pr_971_only(self) -> None:
        self.assertEqual(971, BOOTSTRAP_EXCEPTION.pr_number)
        exact = context(
            "promotion/con-1571-governance-bootstrap", "main", "", number=971
        )
        self.assertAccepted(exact, BOOTSTRAP_EXCEPTION)
        self.assertRejected(
            context("promotion/con-1571-governance-bootstrap", "main", "", number=970),
            BOOTSTRAP_EXCEPTION,
        )


if __name__ == "__main__":
    unittest.main()
