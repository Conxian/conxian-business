"""Negative conformance for the read-only immutable-head check gate."""
import contextlib
import io
import json
import subprocess
import unittest
from unittest.mock import patch

import wait_for_checks as gate

HEAD = "a" * 40
OTHER = "b" * 40


def run(conclusion="success", status="completed", sha=HEAD):
    return {"name": "CodeQL", "head_sha": sha, "status": status, "conclusion": conclusion}


def pages(runs):
    return [{"total_count": len(runs), "check_runs": runs}]


class CheckGateTests(unittest.TestCase):
    def snapshot(self, checks=None, statuses=None):
        with patch.object(gate, "api", side_effect=[pages([run()]) if checks is None else checks,
                                                    [[]] if statuses is None else statuses]):
            return gate.check_snapshot("owner/repo", HEAD, 100)

    def test_success_and_nonblocking_are_distinct(self):
        self.assertEqual(self.snapshot(pages([run(), run("skipped"), run("neutral")])), (1, 2, 0, 0))

    def test_no_checks_is_not_success(self):
        with self.assertRaises(gate.EvidenceError):
            self.snapshot(pages([]))

    def test_skipped_or_neutral_only_is_not_success(self):
        for conclusion in ["skipped", "neutral"]:
            with self.subTest(conclusion=conclusion), self.assertRaises(gate.EvidenceError):
                self.snapshot(pages([run(conclusion)]))

    def test_every_failed_conclusion_blocks(self):
        for conclusion in ["failure", "cancelled", "timed_out", "action_required", "stale", "startup_failure"]:
            with self.subTest(conclusion=conclusion):
                self.assertEqual(self.snapshot(pages([run(conclusion)]))[3], 1)

    def test_pending_waits(self):
        for status in ["queued", "in_progress", "pending", "waiting", "requested"]:
            with self.subTest(status=status):
                self.assertEqual(self.snapshot(pages([run(None, status)]))[2], 1)

    def test_unknown_or_inconsistent_run_blocks(self):
        for item in [run(None), run("invented"), run("success", "in_progress"), run(None, "unknown"), run(sha=OTHER), {}]:
            with self.subTest(item=item), self.assertRaises(gate.EvidenceError):
                self.snapshot(pages([item]))

    def test_incomplete_or_malformed_pages_block(self):
        for checks in [[], {}, [None], [{"check_runs": []}], [{"total_count": 2, "check_runs": [run()]}]]:
            with self.subTest(checks=checks), self.assertRaises(gate.EvidenceError):
                self.snapshot(checks)

    def test_second_page_failure_blocks(self):
        checks = [{"total_count": 2, "check_runs": [run()]},
                  {"total_count": 2, "check_runs": [run("failure")]}]
        self.assertEqual(self.snapshot(checks), (1, 0, 0, 1))

    def test_latest_commit_status_wins(self):
        statuses = [[{"id": 2, "context": "Vercel", "state": "failure"}],
                    [{"id": 1, "context": "Vercel", "state": "success"}]]
        self.assertEqual(self.snapshot(statuses=statuses)[3], 1)
        statuses.reverse()
        self.assertEqual(self.snapshot(statuses=statuses)[3], 1)

    def test_status_only_success_supported(self):
        self.assertEqual(self.snapshot(pages([]), [[{"id": 1, "context": "build", "state": "success"}]]), (1, 0, 0, 0))

    def test_status_errors_pending_unknown_and_malformed(self):
        for state, expected in [("error", (0, 0, 0, 1)), ("pending", (0, 0, 1, 0))]:
            self.assertEqual(self.snapshot(pages([]), [[{"id": 1, "context": "x", "state": state}]]), expected)
        for statuses in [[], [{}], [[{}]], [[{"id": 1, "context": "x", "state": "unknown"}]]]:
            with self.subTest(statuses=statuses), self.assertRaises(gate.EvidenceError):
                self.snapshot(statuses=statuses)

    def test_api_errors_never_become_success_even_with_valid_json(self):
        for code, stdout in [(1, ""), (1, "{}"), (4, "[]"), (0, ""), (0, "not-json")]:
            with self.subTest(code=code, stdout=stdout), patch.object(gate.subprocess, "run", return_value=subprocess.CompletedProcess([], code, stdout, "sensitive")):
                with self.assertRaises(gate.EvidenceError) as error:
                    gate.api("repos/owner/repo", 100)
                self.assertNotIn("sensitive", str(error.exception))

    def test_missing_cli_and_timeout_block(self):
        for error in [FileNotFoundError(), subprocess.TimeoutExpired("gh", 1)]:
            with self.subTest(error=error), patch.object(gate.subprocess, "run", side_effect=error):
                with self.assertRaises(gate.EvidenceError):
                    gate.api("repos/owner/repo", 100)

    def test_pagination_is_requested(self):
        with patch.object(gate.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "[[]]", "")) as call:
            gate.api("repos/owner/repo", 100, True)
            self.assertIn("--paginate", call.call_args.args[0])
            self.assertIn("--slurp", call.call_args.args[0])

    def test_draft_closed_and_missing_head_block(self):
        for value in [{"state": "closed", "draft": False, "head": {"sha": HEAD}},
                      {"state": "open", "draft": True, "head": {"sha": HEAD}},
                      {"state": "open", "draft": False}, {}, []]:
            with self.subTest(value=value), patch.object(gate, "api", return_value=value):
                with self.assertRaises(gate.EvidenceError):
                    gate.pull_head("owner/repo", 1, 100)

    def test_head_moves_before_or_after_snapshot(self):
        for heads in [[HEAD, OTHER], [HEAD, HEAD, OTHER]]:
            with self.subTest(heads=heads), patch.object(gate, "pull_head", side_effect=heads), patch.object(gate, "check_snapshot", return_value=(1, 0, 0, 0)):
                with self.assertRaises(gate.EvidenceError):
                    gate.wait("owner/repo", 1, 30, 1, None)

    def test_expected_head_mismatch_blocks(self):
        with patch.object(gate, "pull_head", return_value=HEAD), self.assertRaises(gate.EvidenceError):
            gate.wait("owner/repo", 1, 30, 1, OTHER)

    def test_success_emits_exact_head_and_separate_approval_gate(self):
        output = io.StringIO()
        with patch.object(gate, "pull_head", return_value=HEAD), patch.object(gate, "check_snapshot", return_value=(1, 1, 0, 0)), contextlib.redirect_stdout(output):
            self.assertEqual(gate.wait("owner/repo", 1, 30, 1, HEAD), 0)
        self.assertIn("head=" + HEAD, output.getvalue())
        self.assertIn("review and release approval remain separate", output.getvalue())

    def test_failed_and_timed_out_pending_are_nonzero(self):
        with patch.object(gate, "pull_head", return_value=HEAD), patch.object(gate, "check_snapshot", return_value=(1, 0, 0, 1)), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(gate.wait("owner/repo", 1, 30, 1, None), 1)
        with patch.object(gate, "pull_head", return_value=HEAD), patch.object(gate, "check_snapshot", return_value=(1, 0, 1, 0)), patch.object(gate.time, "monotonic", side_effect=[0, 31]), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(gate.wait("owner/repo", 1, 30, 1, None), 2)


if __name__ == "__main__":
    unittest.main()
