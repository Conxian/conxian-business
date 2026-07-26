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

        safe_text = "GitHub is authoritative. Historical Linear archive provenance only.\n"
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
        self._write(".github/ISSUE_TEMPLATE/config.yml", "blank_issues_enabled: false\n")

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
        self.assertIn("active intake still requires Linear authority", output)

    def test_issue_form_directing_new_linear_work_fails(self) -> None:
        self._write(
            ".github/ISSUE_TEMPLATE/extra.yml",
            "name: Extra\ndescription: Create a Linear issue first\n",
        )
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("issue intake must not direct users to new Linear work", output)

    def test_unqualified_linear_reference_fails(self) -> None:
        self._write("README.md", "Use Linear for coordination.\n")
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("must be explicitly historical/archive/migration context", output)


if __name__ == "__main__":
    unittest.main()
