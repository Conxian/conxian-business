from __future__ import annotations

import importlib.util
import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = REPO_ROOT / "scripts" / "verify_bos_production_boundary.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_bos_production_boundary", VERIFIER_PATH
)
assert SPEC and SPEC.loader
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)

STUB_SUFFIX = "." + "stub" + ".json"
GENERATED_DIR = "conxian-business/" + "." + "generated/"


class BosProductionBoundaryVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self._git("init", "--quiet")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def _write(self, relative_path: str, content: str = "test fixture\n") -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _track(self, *relative_paths: str) -> None:
        self._git("add", *relative_paths)

    def _run(self) -> tuple[int, str]:
        output = io.StringIO()
        with (
            mock.patch.object(verifier, "repo_root", return_value=str(self.repo)),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            status = verifier.main()
        return status, output.getvalue()

    def assert_passes(self) -> None:
        status, output = self._run()
        self.assertEqual(status, 0, output)
        self.assertIn("BOS production boundary checks: OK", output)

    def assert_fails_with(self, expected: str) -> None:
        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn(expected, output)

    def test_clean_case(self) -> None:
        self._write("src/service.py", "print('ready')\n")
        self._track("src/service.py")

        self.assert_passes()

    def test_misplaced_tracked_stub_fails(self) -> None:
        fixture = "fixtures/candidate" + STUB_SUFFIX
        self._write(fixture, "{}\n")
        self._track(fixture)

        self.assert_fails_with("Stub artifact must be isolated")

    def test_tracked_generated_artifact_fails(self) -> None:
        fixture = GENERATED_DIR + "report.json"
        self._write(fixture, "{}\n")
        self._track(fixture)

        self.assert_fails_with("Committed generated artifacts detected")

    def test_production_source_references_stub_or_generated_paths_fail(self) -> None:
        self._write("src/stub_loader.py", f'PATH = "candidate{STUB_SUFFIX}"\n')
        self._write(
            "src/generated_loader.py",
            f'PATH = "{GENERATED_DIR}report.json"\n',
        )
        self._track("src/stub_loader.py", "src/generated_loader.py")

        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn(f"reference {STUB_SUFFIX}", output)
        self.assertIn(f"reference {GENERATED_DIR}", output)

    def test_docs_and_openspec_references_are_exempt(self) -> None:
        self._write("docs/example.py", f'PATH = "candidate{STUB_SUFFIX}"\n')
        self._write(
            "openspec/specs/example.ts",
            f'const path = "{GENERATED_DIR}report.json";\n',
        )
        self._track("docs/example.py", "openspec/specs/example.ts")

        self.assert_passes()

    def test_top_level_verifier_stub_reference_is_exempt(self) -> None:
        self._write(
            "scripts/verify_fixture.py", f'PATH = "candidate{STUB_SUFFIX}"\n'
        )
        self._track("scripts/verify_fixture.py")

        self.assert_passes()

    def test_non_entrypoint_verifier_reference_fails(self) -> None:
        self._write(
            "scripts/helpers/verify_fixture.py",
            f'PATH = "candidate{STUB_SUFFIX}"\n',
        )
        self._track("scripts/helpers/verify_fixture.py")

        self.assert_fails_with(
            f"Production/CI code must not reference {STUB_SUFFIX}"
        )

    def test_top_level_typescript_active_testnet_defaults_fail(self) -> None:
        testnet_principal = "S" + "T" + ("A" * 20)
        self._write(
            "scripts/deploy.ts",
            "const network = networkFromName('testnet');\n"
            f'const deployer = "{testnet_principal}";\n',
        )
        self._track("scripts/deploy.ts")

        status, output = self._run()
        self.assertEqual(status, 1, output)
        self.assertIn("hard-code testnet as the active network", output)
        self.assertIn("embed testnet principals", output)

    def test_git_enumeration_failure_fails_closed(self) -> None:
        output = io.StringIO()
        with (
            mock.patch.object(verifier, "repo_root", return_value=str(self.repo)),
            mock.patch.object(
                verifier.subprocess,
                "check_output",
                side_effect=FileNotFoundError("git unavailable"),
            ),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            status = verifier.main()

        self.assertEqual(status, 1, output.getvalue())
        self.assertIn("Failed to enumerate tracked files via git", output.getvalue())

    def test_declared_submodule_contents_are_excluded(self) -> None:
        self._write(
            ".gitmodules",
            '[submodule "component"]\n'
            "\tpath = vendor/component\n"
            "\turl = https://example.invalid/component.git\n",
        )
        fixture = "vendor/component/candidate" + STUB_SUFFIX
        self._write(fixture, "{}\n")
        self._track(".gitmodules", fixture)

        self.assert_passes()


if __name__ == "__main__":
    unittest.main()
