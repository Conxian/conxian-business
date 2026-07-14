#!/usr/bin/env python3
"""Focused local tests for the PR #887 CI gate helpers."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from ci import ci_summary_gate


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKOUT_HELPER = REPO_ROOT / "scripts" / "ci" / "checkout_pinned_submodules.sh"


class MarketCheckoutGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="conxian-ci-gate-")
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "source"
        self.source.mkdir()
        subprocess.run(["git", "init", "-q", str(self.source)], check=True)
        subprocess.run(
            ["git", "-C", str(self.source), "config", "user.name", "CI fixture"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.source), "config", "user.email", "ci-fixture@example.invalid"],
            check=True,
        )

        market_repo = self.root / "market-repo"
        market_repo.mkdir()
        subprocess.run(["git", "init", "-q", str(market_repo)], check=True)
        subprocess.run(
            ["git", "-C", str(market_repo), "config", "user.name", "CI fixture"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(market_repo), "config", "user.email", "ci-fixture@example.invalid"],
            check=True,
        )
        (market_repo / "README.md").write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(market_repo), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(market_repo), "commit", "-qm", "fixture"], check=True)

        subprocess.run(
            [
                "git",
                "-c",
                "protocol.file.allow=always",
                "-C",
                str(self.source),
                "submodule",
                "add",
                str(market_repo),
                "conxian-market",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.source),
                "config",
                "-f",
                ".gitmodules",
                "submodule.conxian-market.update",
                "none",
            ],
            check=True,
        )
        subprocess.run(["git", "-C", str(self.source), "add", ".gitmodules"], check=True)
        subprocess.run(["git", "-C", str(self.source), "commit", "-qm", "fixture"], check=True)
        subprocess.run(
            ["git", "-C", str(self.source), "submodule", "deinit", "-f", "-q", "conxian-market"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_helper(self, token: str | None) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if token is None:
            environment.pop("CI_SUBMODULES_PAT", None)
        else:
            environment["CI_SUBMODULES_PAT"] = token
        environment["GIT_TERMINAL_PROMPT"] = "0"
        environment["GIT_CONFIG_COUNT"] = "1"
        environment["GIT_CONFIG_KEY_0"] = "protocol.file.allow"
        environment["GIT_CONFIG_VALUE_0"] = "always"
        return subprocess.run(
            [str(CHECKOUT_HELPER), "market"],
            cwd=self.source,
            env=environment,
            text=True,
            capture_output=True,
        )

    def test_missing_token_fails_without_echoing_fixture_token(self) -> None:
        completed = self.run_helper(None)
        self.assertNotEqual(completed.returncode, 0)
        self.assertNotIn("fixture-token", completed.stdout + completed.stderr)
        self.assertFalse((self.source / "conxian-market" / "README.md").exists())

    def test_valid_local_pinned_checkout_overrides_update_none(self) -> None:
        completed = self.run_helper("fixture-token")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue((self.source / "conxian-market" / "README.md").is_file())


class SummaryGateTests(unittest.TestCase):
    def with_environment(self, environment: dict[str, str]) -> list[str]:
        old = os.environ.copy()
        try:
            os.environ.clear()
            os.environ.update(environment)
            return ci_summary_gate.blocking_jobs(ci_summary_gate.build_rows())
        finally:
            os.environ.clear()
            os.environ.update(old)

    def test_required_unavailable_market_is_blocking(self) -> None:
        blocked = self.with_environment(
            {
                "CODE_IMPACTING": "false",
                "MARKET_SUITE_REQUIRED": "true",
                "CHANGE_DETECTION_RESULT": "success",
                "REPO_HYGIENE_RESULT": "success",
                "MARKET_SUITE_RESULT": "unavailable",
            }
        )
        self.assertIn("Market Integration Suite", blocked)

    def test_non_required_skips_are_intentional(self) -> None:
        blocked = self.with_environment(
            {
                "CODE_IMPACTING": "false",
                "CHANGE_DETECTION_RESULT": "success",
                "REPO_HYGIENE_RESULT": "success",
                "GATEWAY_SUITE_RESULT": "skipped",
                "B2B_SUITE_RESULT": "skipped",
                "LIB_CORE_SUITE_RESULT": "skipped",
                "B2C_WALLET_SUITE_RESULT": "skipped",
                "AUDIT_DOCS_RESULT": "skipped",
                "TESTNET_SIMULATION_RESULT": "skipped",
                "MARKET_SUITE_RESULT": "skipped",
            }
        )
        self.assertEqual(blocked, [])

    def test_required_non_success_states_are_blocking(self) -> None:
        for state in ("skipped", "failure", "cancelled", "timed_out", "unavailable"):
            with self.subTest(state=state):
                blocked = self.with_environment(
                    {
                        "CODE_IMPACTING": "true",
                        "CHANGE_DETECTION_RESULT": "success",
                        "REPO_HYGIENE_RESULT": "success",
                        "GATEWAY_SUITE_RESULT": state,
                        "LIB_CORE_SUITE_RESULT": "success",
                        "B2C_WALLET_SUITE_RESULT": "success",
                    }
                )
                self.assertIn("Gateway Suite", blocked)


if __name__ == "__main__":
    unittest.main()
