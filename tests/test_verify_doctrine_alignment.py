import tempfile
import unittest
from pathlib import Path

from scripts.verify_doctrine_alignment import (
    find_custody_violations,
    github_heading_slug,
    heading_slugs,
    resolve_local_fragment,
)


class CustodyBoundaryFixturesTest(unittest.TestCase):
    def test_explicit_allow_patterns_and_risk_references_pass(self) -> None:
        allowed = (
            "Conxian-Labs does not custody participant assets.",
            "The service is non-custodial.",
            "Users retain self-custody and control of their keys.",
            "Protocol contract-held state is governed by DAO governance.",
            "Regulated partners remain responsible for regulated custody.",
            "Company wording could be misread as custody; the protocol defines the state.",
        )
        for fixture in allowed:
            with self.subTest(fixture=fixture):
                self.assertEqual(find_custody_violations(fixture), [])

    def test_affirmative_company_and_sab_claims_fail(self) -> None:
        rejected = (
            "Conxian-Labs takes custody of user funds.",
            "The company controls protocol funds.",
            "SAB custody is the operating model.",
            "The company is responsible for treasury assets.",
            "Conxian-Labs is the custodian of participant funds.",
            "Conxian-Labs acts as custodian for user assets.",
            "Conxian-Labs is non-custodial but controls protocol funds.",
            "The company is not simply an integrator; it controls protocol funds.",
            "A risk sentence can be followed by an affirmative claim; company controls protocol funds.",
            "The company controls protocol funds, a risk.",
        )
        for fixture in rejected:
            with self.subTest(fixture=fixture):
                self.assertNotEqual(find_custody_violations(fixture), [])

    def test_explicit_risk_analysis_does_not_exempt_affirmative_claims(self) -> None:
        allowed = (
            "The claim that the company controls protocol funds is a risk.",
            "Company custody wording could be misread as company control.",
            "Prototype language could imply company-controlled fund handling.",
            "Does the company control protocol funds?",
        )
        for fixture in allowed:
            with self.subTest(fixture=fixture):
                self.assertEqual(find_custody_violations(fixture), [])


class HeadingFragmentFixturesTest(unittest.TestCase):
    def test_slug_generation_handles_numbers_punctuation_unicode_and_duplicates(self) -> None:
        self.assertEqual(github_heading_slug("1. Release — issue #639"), "1-release-issue-639")
        self.assertEqual(github_heading_slug("Évidence — résumé"), "évidence-résumé")

        document = "\n".join(
            (
                "# Duplicate",
                "## 1. Release — issue #639",
                "### Duplicate",
                "## Évidence — résumé",
            )
        )
        slugs = heading_slugs(document)
        self.assertIn("duplicate", slugs)
        self.assertIn("duplicate-1", slugs)
        self.assertIn("1-release-issue-639", slugs)
        self.assertIn("évidence-résumé", slugs)

    def test_local_fragment_resolution_uses_generated_duplicate_slugs(self) -> None:
        document = "\n".join(
            (
                "# Duplicate",
                "## 1. Release — issue #639",
                "### Duplicate",
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.md"
            path.write_text(document, encoding="utf-8")
            self.assertTrue(resolve_local_fragment(path, "#duplicate"))
            self.assertTrue(resolve_local_fragment(path, "#duplicate-1"))
            self.assertTrue(resolve_local_fragment(path, "#1-release-issue-639"))
            self.assertFalse(resolve_local_fragment(path, "#duplicate-2"))
            self.assertFalse(resolve_local_fragment(path, "#missing"))


if __name__ == "__main__":
    unittest.main()
