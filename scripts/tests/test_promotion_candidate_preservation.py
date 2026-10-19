"""Exercise preservation controls through real Git and workflow shell processes."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("reconcile_under_test", ROOT / "scripts/reconcile_branches.py")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def git(cwd, *args):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


class ReconciliationPreservationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "repo"
        git(self.root, "init", "--bare", "-b", "dev", str(self.remote))
        git(self.root, "init", "-b", "dev", str(self.repo))
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        (self.repo / "base").write_text("retained\n")
        git(self.repo, "add", "base")
        git(self.repo, "commit", "-qm", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "checkout", "-qb", "staged")
        (self.repo / "source").write_text("higher branch addition\n")
        git(self.repo, "add", "source")
        git(self.repo, "commit", "-qm", "source")
        self.source = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-q", "origin", "dev", "staged")
        git(self.repo, "fetch", "-q", "origin")
        self.branch = "backmerge/staged-to-dev"
        self.plan = module.ReconcilePlan("fixture", "staged", "dev", 1)

    def invoke(self, dry=False, gh=None):
        with patch.object(module, "_clone", return_value=str(self.repo)), patch.object(
            module, "_gh", side_effect=gh or ["0", "https://example.invalid/pr/1"]
        ) as calls:
            result = module.reconcile(self.plan, dry)
            return result, calls.call_args_list

    def test_existing_pr_returns_before_clone_or_git_mutation(self):
        with patch.object(module, "_gh", return_value="1"), patch.object(module, "_clone") as clone:
            self.assertEqual(module.reconcile(self.plan, False)["status"], "existing")
            clone.assert_not_called()

    def test_existing_branch_is_preserved_even_without_open_pr(self):
        git(self.repo, "push", "-q", "origin", f"dev:refs/heads/{self.branch}")
        git(self.repo, "fetch", "-q", "origin")
        result, calls = self.invoke()
        self.assertEqual(result["status"], "existing_branch")
        self.assertEqual(git(self.remote, "rev-parse", f"refs/heads/{self.branch}"), self.base)
        self.assertEqual(len(calls), 1)

    def test_new_candidate_keeps_both_histories_and_never_merges_target(self):
        result, calls = self.invoke()
        self.assertEqual(result["status"], "opened")
        head = git(self.remote, "rev-parse", f"refs/heads/{self.branch}")
        self.assertEqual(git(self.remote, "rev-parse", "refs/heads/dev"), self.base)
        self.assertEqual(git(self.remote, "rev-parse", f"{head}^{{tree}}"), git(self.repo, "rev-parse", f"{self.source}^{{tree}}"))
        self.assertEqual([c.args[:2] for c in calls], [("pr", "list"), ("pr", "create")])

    def test_dry_run_does_not_publish_or_open_pr(self):
        result, calls = self.invoke(dry=True)
        self.assertEqual(result["status"], "dry_run")
        self.assertEqual(len(calls), 1)
        self.assertEqual(git(self.remote, "for-each-ref", f"refs/heads/{self.branch}"), "")

    def test_racing_ref_creation_rejects_even_when_it_is_an_ancestor(self):
        run = subprocess.run

        def race(args, **kwargs):
            if args[:2] == ["git", "push"]:
                git(self.remote, "update-ref", f"refs/heads/{self.branch}", self.base)
            return run(args, **kwargs)

        with patch.object(module.subprocess, "run", side_effect=race):
            with self.assertRaises(subprocess.CalledProcessError):
                self.invoke()
        self.assertEqual(git(self.remote, "rev-parse", f"refs/heads/{self.branch}"), self.base)


class PromotionWorkflowProcessTests(unittest.TestCase):
    def scenario(self, drift, step_name="Leave promotion PR as draft for manual review"):
        workflow = (ROOT / ".github/workflows/auto-promotion.yml").read_text()
        marker = f"      - name: {step_name}\n"
        self.assertEqual(workflow.count(marker), 1)
        step = workflow.split(marker, 1)[1].split("\n      - name:", 1)[0]
        script = textwrap.dedent(step.split("        run: |\n", 1)[1])
        script = script.replace("${{ github.repository }}", "Conxian/fixture")
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            log = directory / "calls.jsonl"
            for name in ("gh", "git"):
                stub = directory / name
                stub.write_text(f"#!{sys.executable}\n" + '''import json, os, sys
from pathlib import Path
name = Path(sys.argv[0]).name
args = sys.argv[1:]
with open(os.environ['CALL_LOG'], 'a') as f: f.write(json.dumps([name, *args]) + '\\n')
if name == 'gh':
    if args[:2] == ['pr', 'list']: print('41')
    elif args[:2] != ['pr', 'comment']: sys.exit(41)
elif args[0] in ('fetch', 'branch'): pass
elif args[0] == 'ls-remote':
    if os.environ['DRIFT'] == 'unavailable': sys.exit(43)
    if os.environ['DRIFT'] == 'remote_changed': print('c' * 40 + '\\trefs/heads/promotion/fixture')
    if os.environ['DRIFT'] == 'remote_equal': print('a' * 40 + '\\trefs/heads/promotion/fixture')
elif args[0] == 'push':
    if '--force-with-lease=refs/heads/promotion/fixture:' not in args: sys.exit(44)
elif args[0] == 'rev-parse':
    key = {'origin/dev':'source', 'origin/staged':'target', 'origin/promotion/fixture':'candidate'}[args[1]]
    print('c' * 40 if os.environ['DRIFT'] == key else ('b' * 40 if key == 'target' else 'a' * 40))
else: sys.exit(42)
''')
                stub.chmod(0o755)
            env = {**os.environ, "PATH": str(directory) + os.pathsep + os.environ["PATH"],
                   "CALL_LOG": str(log), "DRIFT": drift, "SOURCE": "dev", "TARGET": "staged",
                   "PROMO_BRANCH": "promotion/fixture", "SOURCE_SHA": "a" * 40, "TARGET_SHA": "b" * 40}
            result = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, timeout=10)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            return result, calls

    def test_unchanged_candidate_only_fetches_reads_and_comments(self):
        result, calls = self.scenario("none")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c[1:3] for c in calls if c[0] == "gh"], [["pr", "list"], ["pr", "comment"]])

    def test_drift_stops_without_candidate_mutation(self):
        for drift in ("source", "target", "candidate"):
            with self.subTest(drift=drift):
                result, calls = self.scenario(drift)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual([c[1:3] for c in calls if c[0] == "gh"], [["pr", "list"]])
                self.assertFalse(any(c[1] in ("push", "merge", "reset") for c in calls if c[0] == "git"))

    def test_publisher_keeps_existing_refs_and_fails_closed_on_lookup_error(self):
        for drift, success in (("remote_changed", False), ("remote_equal", True), ("unavailable", False)):
            with self.subTest(drift=drift):
                result, calls = self.scenario(drift, "Publish immutable candidate ref")
                self.assertEqual(result.returncode == 0, success, result.stderr)
                self.assertFalse(any(c[0] == "git" and c[1] == "push" for c in calls))

    def test_publisher_creates_only_an_absent_ref(self):
        result, calls = self.scenario("none", "Publish immutable candidate ref")
        self.assertEqual(result.returncode, 0, result.stderr)
        pushes = [c for c in calls if c[0] == "git" and c[1] == "push"]
        self.assertEqual(len(pushes), 1)
        self.assertIn("--force-with-lease=refs/heads/promotion/fixture:", pushes[0])


if __name__ == "__main__":
    unittest.main()
