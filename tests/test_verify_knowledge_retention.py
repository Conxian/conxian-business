from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = REPO_ROOT / "scripts" / "verify_knowledge_retention.py"
SPEC = importlib.util.spec_from_file_location("verify_knowledge_retention", VERIFIER_PATH)
assert SPEC and SPEC.loader
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class KnowledgeRetentionVerifierTests(unittest.TestCase):
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

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _write_manifest(self, paths: list[str] | None = None) -> None:
        manifest = {
            "CON-306": {
                "description": "Temporary test migration record",
                "paths": paths
                if paths is not None
                else ["internal/strategy/**", "archive/**"],
            }
        }
        self._write("audit/migration_manifest.json", json.dumps(manifest))

    @contextmanager
    def _in_repo(self):
        previous = Path.cwd()
        os.chdir(self.repo)
        try:
            yield
        finally:
            os.chdir(previous)

    def test_success(self) -> None:
        self._write_manifest()

        with self._in_repo():
            verifier.verify()

    def test_missing_manifest_fails_closed(self) -> None:
        with self._in_repo(), self.assertRaisesRegex(RuntimeError, "manifest not found"):
            verifier.verify()

    def test_required_coverage_missing_fails(self) -> None:
        self._write_manifest(["internal/strategy/**"])

        with self._in_repo(), self.assertRaisesRegex(RuntimeError, "archive/\\*\\*"):
            verifier.verify()

    def test_tracked_sensitive_root_file_fails(self) -> None:
        self._write_manifest()
        self._write("archive/placeholder.md", "innocuous test content\n")
        self._git("add", "audit/migration_manifest.json", "archive/placeholder.md")

        with self._in_repo(), self.assertRaisesRegex(RuntimeError, "tracked sensitive paths"):
            verifier.verify()

    def test_ignored_but_unmanifested_file_fails(self) -> None:
        self._write_manifest()
        self._write(".gitignore", "private-placeholder/\n")
        self._write("private-placeholder/note.md", "innocuous test content\n")

        roots = (*verifier.SENSITIVE_ROOTS, "private-placeholder")
        with (
            mock.patch.object(verifier, "SENSITIVE_ROOTS", roots),
            self._in_repo(),
            self.assertRaisesRegex(RuntimeError, "not covered"),
        ):
            verifier.verify()


if __name__ == "__main__":
    unittest.main()
