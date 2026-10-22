import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import bos_org_review as audit


def repository(name="example", **changes):
    return {"name": name, "html_url": f"https://github.com/Conxian/{name}",
            "owner": {"login": "Conxian"}, "archived": False,
            "disabled": False, "default_branch": "dev", **changes}


class InventoryTests(unittest.TestCase):
    def enumerate(self, pages):
        with patch.object(audit, "run", return_value=(0, json.dumps(pages))):
            return audit.repos("Conxian")

    def test_all_pages_and_archive_boundary(self):
        pages = [[repository(f"repo-{i}") for i in range(100)],
                 [repository("last"), repository("history", archived=True)]]
        with patch.object(audit, "run", return_value=(0, json.dumps(pages))) as run:
            result = audit.repos("Conxian")
        self.assertEqual(len(result), 101)
        self.assertEqual(result[-1]["name"], "last")
        self.assertIn("--paginate", run.call_args.args[0])
        self.assertIn("--slurp", run.call_args.args[0])

    def test_auth_failure_never_substitutes_submodules_or_leaks_body(self):
        with patch.object(audit, "run", return_value=(1, "private-auth-value")) as run:
            with self.assertRaises(RuntimeError) as raised:
                audit.repos("Conxian")
        self.assertEqual(run.call_count, 1)
        self.assertNotIn("private-auth-value", str(raised.exception))

    def test_invalid_empty_incomplete_and_unscoped_inventory(self):
        samples = [[], [[]], {}, [[repository(archived=True)]], [[None]],
                   [[repository("../escape")]], [[repository("..")]],
                   [[repository(owner={"login": "other-org"})]],
                   [[repository(disabled=None)]], [[repository(archived="false")]],
                   [[repository("same")], [repository("SAME")]],
                   [[repository()], {"message": "late-page failure"}]]
        for pages in samples:
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                self.enumerate(pages)

    def test_api_clone_url_is_not_a_network_authority(self):
        result = self.enumerate([[repository(clone_url="https://untrusted.invalid/private")]])
        self.assertEqual(result[0]["clone_url"], "https://github.com/Conxian/example.git")


class ReportTests(unittest.TestCase):
    def test_kb_discovery_retains_candidates_beyond_one_hundred(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(audit, "run", return_value=(0, "a" * 40)):
            root = Path(temp)
            for index in range(125):
                (root / f"knowledge-{index:03}.md").write_text("documentation")
            result = audit.inspect(repository(), root)
        self.assertEqual(len(result["kb_candidates"]), 125)
        self.assertEqual(result["kb_candidates"][-1], "knowledge-124.md")

    def execute(self, root, *, clone_error=False, disabled=False, unreadable=False):
        def run(command, cwd=None):
            if command[:2] == ["gh", "api"]:
                return 0, json.dumps([[repository(disabled=disabled)]])
            if command[:2] == ["git", "clone"]:
                if clone_error:
                    return 1, "private-clone-output"
                target = Path(command[-1])
                target.mkdir()
                (target / "README.md").write_text("source example")
                return 0, ""
            if command[:2] == ["git", "rev-parse"]:
                return 0, "a" * 40
            self.fail(f"unexpected command: {command[:2]}")

        original_read = Path.read_text

        def read(path, *args, **kwargs):
            if unreadable and path.name == "README.md":
                raise OSError("private filesystem details")
            return original_read(path, *args, **kwargs)

        with patch.object(audit, "run", side_effect=run), \
                patch.object(audit.Path, "cwd", return_value=root), \
                patch.object(Path, "read_text", read), \
                patch("sys.argv", ["bos_org_review.py", "--output", "restricted/report.json",
                                   "--markdown", "other/report.md"]), \
                contextlib.redirect_stdout(io.StringIO()):
            code = audit.main()
        return code, json.loads((root / "restricted/report.json").read_text())

    def test_success_is_pinned_source_scope_not_runtime_or_security_acceptance(self):
        with tempfile.TemporaryDirectory() as temp:
            code, report = self.execute(Path(temp))
        self.assertEqual(code, 0)
        self.assertTrue(report["source_scan_complete"])
        self.assertEqual(report["inventory_count"], 1)
        self.assertFalse(report["runtime_qualification"])
        self.assertFalse(report["exhaustive_security_audit"])
        self.assertEqual(report["repositories"][0]["source_revision"], "a" * 40)
        self.assertEqual(report["repositories"][0]["status"], "source-scan-complete")

    def test_partial_clone_and_disabled_repositories_fail_closed(self):
        for options in ({"clone_error": True}, {"disabled": True}, {"unreadable": True}):
            with self.subTest(options=options), tempfile.TemporaryDirectory() as temp:
                code, report = self.execute(Path(temp), **options)
            self.assertEqual(code, 1)
            self.assertFalse(report["source_scan_complete"])
            self.assertNotIn("private-", json.dumps(report))

    def test_missing_cli_returns_failure_without_emitting_an_audit(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(audit.Path, "cwd", return_value=Path(temp)), \
                patch.object(audit, "run", side_effect=FileNotFoundError("private-cli-path")), \
                patch("sys.argv", ["bos_org_review.py"]), \
                contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(audit.main(), 1)
            self.assertEqual(list(Path(temp).iterdir()), [])
        self.assertNotIn("private-cli-path", stderr.getvalue())

    def test_unpinned_checkout_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(audit, "run", return_value=(0, "not-a-source-sha")):
            with self.assertRaises(RuntimeError):
                audit.inspect(repository(), Path(temp))

    def test_source_symlinks_cannot_read_outside_the_checkout(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(audit, "run", return_value=(0, "a" * 40)):
            root = Path(temp)
            outside = root / "outside.md"
            outside.write_text("synthetic ghp_ marker")
            checkout = root / "checkout"
            checkout.mkdir()
            (checkout / "README.md").write_text("source")
            (checkout / "linked.md").symlink_to(outside)
            result = audit.inspect(repository(), checkout)
        self.assertEqual(result["file_count"], 1)
        self.assertEqual(result["secret_suspects"], [])


if __name__ == "__main__":
    unittest.main()
