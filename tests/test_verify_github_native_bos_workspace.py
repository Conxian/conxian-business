from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = REPO_ROOT / "scripts" / "verify_github_native_bos_workspace.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_github_native_bos_workspace", VERIFIER_PATH
)
assert SPEC and SPEC.loader
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class GitHubNativeBosWorkspaceVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self._write_valid_fixture()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _write_valid_fixture(self) -> None:
        for relative_path, fragments in verifier.REQUIRED_CONTENT.items():
            self._write(relative_path, "\n".join(fragments) + "\n")

        for (
            relative_path,
            authority_text,
        ) in verifier.REQUIRED_ISSUE_FORM_AUTHORITY.items():
            path = self.repo / relative_path
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            if authority_text.casefold() not in existing.casefold():
                self._write(relative_path, existing + authority_text + "\n")

        safe_text = (
            "GitHub is authoritative. Historical Linear archive provenance only.\n"
        )
        for relative_path in set(verifier.ACTIVE_INTAKE_FILES) | set(
            verifier.LINEAR_CONTEXT_FILES
        ):
            if relative_path not in verifier.REQUIRED_CONTENT:
                self._write(relative_path, safe_text)

        self._write(
            "docs/DOCUMENTATION_ALIGNMENT_INDEX.md",
            "# Registry\n"
            "## Historical Linear issue-linking provenance\n"
            "## Archived Linear migration proposals\n"
            "Do not create these as new canonical Linear documents.\n",
        )
        self._write(
            ".github/ISSUE_TEMPLATE/config.yml", "blank_issues_enabled: false\n"
        )

    def _run(self) -> tuple[int, str]:
        output = io.StringIO()
        with (
            mock.patch.object(verifier, "repo_root", return_value=self.repo),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            status = verifier.main()
        return status, output.getvalue()

    def test_valid_workspace_passes(self) -> None:
        status, output = self._run()
        self.assertEqual(status, 0, output)
        self.assertIn("GitHub-native BOS workspace verification: OK", output)

    def test_active_source_scope_includes_policy_and_workflow(self) -> None:
        self.assertIn("AGENTS.md", verifier.ACTIVE_INTAKE_FILES)
        self.assertIn("docs/AGENTS.md", verifier.ACTIVE_INTAKE_FILES)
        self.assertIn(
            ".github/workflows/weekly-viability-report.yml",
            verifier.ACTIVE_INTAKE_FILES,
        )

    def test_missing_canonical_policy_fails_closed(self) -> None:
        (self.repo / "docs/GITHUB_NATIVE_BOS_WORKSPACE.md").unlink()
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("Missing required file", output)

    def test_missing_required_authority_language_fails(self) -> None:
        path = self.repo / "docs/GITHUB_NATIVE_BOS_WORKSPACE.md"
        path.write_text("incomplete\n", encoding="utf-8")
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("missing required authority/control language", output)

    def test_linear_first_active_intake_fails(self) -> None:
        self._write(
            "CONTRIBUTING.md",
            "For new work use the Linear-first intake process. Historical archive.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("active intake requires Linear", output)

    def test_active_linear_mandate_variants_fail(self) -> None:
        variants = (
            "All new BOS work must use Linear for coordination.",
            "Linear ticket required.",
            "Route work through Linear.",
            "Linear is required for new work.",
            "Linear must be used for new work coordination.",
            "Current intake shall use Linear for coordination.",
            "Linear is mandatory for coordination.",
            "Linear is canonical for new intake.",
            "Linear is authoritative for current coordination.",
            "Linear is the source of truth for new work.",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                self._write("CONTRIBUTING.md", variant + "\n")
                status, output = self._run()
                self.assertEqual(status, 1, output)
                self.assertIn(
                    "CONTRIBUTING.md:1: active intake requires Linear", output
                )

    def test_agents_sensitive_record_linear_routing_fails(self) -> None:
        self._write(
            "AGENTS.md",
            "Keep sensitive logic and protected configs in Linear only.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("AGENTS.md:1: active intake requires Linear", output)

    def test_nested_agents_linear_virtual_office_migration_fails(self) -> None:
        self._write(
            "docs/AGENTS.md",
            "Before ignoring sensitive paths, all contained knowledge must be "
            "migrated to the Linear Virtual Office.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("docs/AGENTS.md:1: active intake requires Linear", output)

    def test_weekly_workflow_plural_linear_issues_mandate_fails(self) -> None:
        self._write(
            ".github/workflows/weekly-viability-report.yml",
            "steps:\n  - run: Create Linear issues to track remediation\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn(
            ".github/workflows/weekly-viability-report.yml:2: active intake "
            "requires Linear",
            output,
        )

    def test_issue_templates_reject_all_linear_references(self) -> None:
        variants = (
            "description: |\n  Linear ticket\n  required\n",
            "description: |\n  Route work through\n  Linear\n",
            "description: |\n  All new BOS work must use\n  Linear for coordination.\n",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                self._write(
                    ".github/ISSUE_TEMPLATE/extra.yml", "name: Extra\n" + variant
                )
                status, output = self._run()
                self.assertEqual(status, 1, output)
                self.assertIn(
                    ".github/ISSUE_TEMPLATE/extra.yml:",
                    output,
                )
                self.assertIn("must not reference Linear", output)

    def test_issue_template_config_rejects_linear_reference(self) -> None:
        self._write(
            ".github/ISSUE_TEMPLATE/config.yml",
            "blank_issues_enabled: false\ncontact_links:\n"
            "  - name: Historical Linear archive\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn(
            ".github/ISSUE_TEMPLATE/config.yml:3: active issue templates must not "
            "reference Linear",
            output,
        )

    def test_exact_historical_marker_bypass_fails(self) -> None:
        self._write(
            "README.md",
            "All new BOS work must use Linear for coordination. Historical context retained.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("README.md:1: active Linear mandate", output)

    def test_wrapped_current_mandate_precedes_later_archive_marker(self) -> None:
        self._write(
            "README.md",
            "All new BOS work must use\n"
            "Linear for coordination. Historical archive context retained.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("README.md:1: active Linear mandate", output)

    def test_adjacent_archive_line_does_not_exempt_current_mandate(self) -> None:
        self._write(
            "README.md",
            "Historical Linear records are archived provenance only.\n"
            "Linear ticket required for current BOS intake.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("README.md:2: active Linear mandate", output)

    def test_explicitly_historical_linear_url_passes(self) -> None:
        self._write(
            "README.md",
            "Historical provenance only: https://linear.app/example/issue/OLD-1 "
            "is archived and non-authoritative.\n",
        )
        status, output = self._run()
        self.assertEqual(status, 0, output)

    def test_missing_github_authority_in_required_issue_form_fails(self) -> None:
        path = ".github/ISSUE_TEMPLATE/governance_legal_decision.yml"
        self._write(path, "name: Governance decision\n")
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn(f"{path}: missing required GitHub-authority language", output)

    def test_unqualified_linear_reference_fails(self) -> None:
        self._write("README.md", "Use Linear for coordination.\n")
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("same sentence or field", output)


if __name__ == "__main__":
    unittest.main()
