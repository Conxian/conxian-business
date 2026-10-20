"""Run the actual capture workflow against real Git histories, without GitHub writes."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]


def git(directory, *args):
    return subprocess.check_output(["git", *args], cwd=directory, text=True, stderr=subprocess.PIPE).strip()


class PromotionLineageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.remote = self.directory / "remote.git"
        self.repo = self.directory / "repo"
        git(self.directory, "init", "--bare", "-b", "dev", str(self.remote))
        git(self.directory, "init", "-b", "dev", str(self.repo))
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Fixture")
        (self.repo / "base").write_text("retained\n")
        git(self.repo, "add", "base")
        git(self.repo, "commit", "-qm", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "branch", "staged")
        git(self.repo, "remote", "add", "origin", str(self.remote))

    def commit(self, name):
        (self.repo / name).write_text(name + "\n")
        git(self.repo, "add", name)
        git(self.repo, "commit", "-qm", name)

    def capture(self):
        git(self.repo, "push", "-q", "origin", "dev", "staged")
        before = git(self.remote, "show-ref")
        workflow = (ROOT / ".github/workflows/auto-promotion.yml").read_text()
        step = workflow.split("      - name: Capture exact candidate evidence\n", 1)[1].split("\n      - name:", 1)[0]
        script = textwrap.dedent(step.split("        run: |\n", 1)[1])
        output = self.directory / "output"
        output.write_text("")
        result = subprocess.run(["bash", "-c", script], cwd=self.repo,
            env={**os.environ, "SOURCE": "dev", "TARGET": "staged", "GITHUB_OUTPUT": str(output)},
            text=True, capture_output=True, timeout=15)
        self.assertEqual(git(self.remote, "show-ref"), before)
        self.assertNotIn("refs/heads/promotion/", before)
        return result, output.read_text()

    def test_current_linear_source_produces_exact_evidence(self):
        self.commit("feature")
        head = git(self.repo, "rev-parse", "HEAD")
        result, output = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skip=false\n", output)
        self.assertIn(f"source_sha={head}\n", output)
        self.assertIn(f"target_sha={self.base}\n", output)

    def test_old_event_skips_before_candidate_publication(self):
        self.commit("feature")
        git(self.repo, "checkout", "-q", "--detach", self.base)
        result, output = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skip=true\n", output)
        self.assertNotIn("promo_branch=", output)
        self.assertIn("Obsolete source event", result.stdout)

    def diverge(self):
        self.commit("feature")
        git(self.repo, "checkout", "-q", "staged")
        self.commit("accepted-target")
        git(self.repo, "checkout", "-q", "dev")

    def test_shared_base_does_not_authorize_omitted_target_history(self):
        self.diverge()
        result, output = self.capture()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("promo_branch=", output)
        self.assertIn("not an ancestor", result.stdout)

    def test_squash_retaining_target_content_is_insufficient(self):
        self.diverge()
        git(self.repo, "merge", "--squash", "staged")
        git(self.repo, "commit", "-qm", "squashed target content")
        self.assertEqual(git(self.repo, "show", "HEAD:accepted-target"), "accepted-target")
        result, output = self.capture()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("promo_branch=", output)
        self.assertIn("equal tree or squash does not retain ancestry", result.stdout)

    def test_real_target_parent_merge_allows_candidate(self):
        self.diverge()
        git(self.repo, "merge", "--no-ff", "-m", "retain target parent", "staged")
        result, output = self.capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skip=false\n", output)

    def test_fetch_error_fails_without_evidence(self):
        self.commit("feature")
        git(self.repo, "remote", "set-url", "origin", str(self.directory / "missing.git"))
        workflow = (ROOT / ".github/workflows/auto-promotion.yml").read_text()
        step = workflow.split("      - name: Capture exact candidate evidence\n", 1)[1].split("\n      - name:", 1)[0]
        script = textwrap.dedent(step.split("        run: |\n", 1)[1])
        output = self.directory / "output"
        output.write_text("")
        result = subprocess.run(["bash", "-c", script], cwd=self.repo,
            env={**os.environ, "SOURCE": "dev", "TARGET": "staged", "GITHUB_OUTPUT": str(output)},
            text=True, capture_output=True, timeout=15)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), "")


if __name__ == "__main__":
    unittest.main()
