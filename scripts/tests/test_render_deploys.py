import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("render_deploys", Path(__file__).parents[1] / "verify_render_deploys.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
OWNER, REPO = "tea-example", "Conxian/conxian-gateway"


def service(suffix="one"):
    return {"id": f"srv-{suffix}", "repo": f"https://github.com/{REPO}.git",
            "ownerId": OWNER, "suspended": "not_suspended"}


def live():
    return [{"deploy": {"status": "live", "commit": {"id": "a" * 40}}}]


class RenderDeployTests(unittest.TestCase):
    def test_live_metadata_records_source(self):
        observations, errors = MODULE.audit_services([service()], [REPO], "token", lambda *_: live())
        self.assertEqual(errors, [])
        self.assertEqual(observations[0]["commit"], "a" * 40)

    def test_every_nonlive_state_fails(self):
        for state in [None, "", "created", "queued", "build_in_progress", "build_failed",
                      "pre_deploy_in_progress", "pre_deploy_failed", "update_in_progress",
                      "update_failed", "deactivated", "canceled", "future_state"]:
            with self.subTest(state=state):
                response = live()
                response[0]["deploy"]["status"] = state
                self.assertTrue(MODULE.audit_services([service()], [REPO], "t", lambda *_: response)[1])

    def test_missing_and_malformed_deploys_fail(self):
        for response in [[], None, {}, [None], [{}], [{"deploy": []}]]:
            with self.subTest(response=response):
                self.assertTrue(MODULE.audit_services([service()], [REPO], "t", lambda *_: response)[1])

    def test_empty_inventory_and_missing_required_repo_fail(self):
        self.assertTrue(MODULE.audit_services([], [REPO], "t")[1])
        self.assertTrue(MODULE.audit_services([service()], ["Conxian/conxian-nexus"], "t", lambda *_: live())[1])

    def test_suspended_or_unknown_suspension_fails(self):
        for state in [None, "suspended", "unknown"]:
            value = service()
            value["suspended"] = state
            self.assertTrue(MODULE.audit_services([value], [REPO], "t", lambda *_: live())[1])

    def test_immutable_deployed_source_required(self):
        for commit in [None, {}, {"id": "main"}, {"id": "abc123"}]:
            response = live()
            response[0]["deploy"]["commit"] = commit
            self.assertTrue(MODULE.audit_services([service()], [REPO], "t", lambda *_: response)[1])

    def test_provider_error_redacted(self):
        def fail(*_):
            raise OSError("sensitive-token-value")
        _, errors = MODULE.audit_services([service()], [REPO], "t", fail)
        self.assertTrue(errors)
        self.assertNotIn("sensitive-token-value", str(errors))

    def test_services_paginate_to_empty_page_and_preserve_scope(self):
        calls = []
        pages = [[{"service": service(), "cursor": "first"}],
                 [{"service": service("two"), "cursor": "second"}], []]
        def fetch(url, _):
            calls.append(url)
            return pages.pop(0)
        self.assertEqual(len(MODULE.list_services(OWNER, "t", fetch)), 2)
        self.assertIn("ownerId=tea-example", calls[1])
        self.assertIn("cursor=first", calls[1])

    def test_duplicate_missing_cursor_wrong_owner_and_invalid_id_fail(self):
        bad = service()
        bad["ownerId"] = "tea-other"
        cases = [
            [[{"service": bad, "cursor": "a"}]],
            [[{"service": service()}]],
            [[{"service": service(), "cursor": "a"}], [{"service": service(), "cursor": "b"}]],
            [[{"service": service(), "cursor": "a"}], [{"service": service("two"), "cursor": "a"}]],
            [[{"service": {"id": "../../other", "ownerId": OWNER}, "cursor": "a"}]],
        ]
        for pages in cases:
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                MODULE.list_services(OWNER, "t", lambda *_: pages.pop(0))

    def test_pagination_limit_rejects_partial_success(self):
        index = 0
        def fetch(*_):
            nonlocal index
            index += 1
            return [{"service": service(str(index)), "cursor": str(index)}]
        with patch.object(MODULE, "MAX_PAGES", 2), self.assertRaises(ValueError):
            MODULE.list_services(OWNER, "t", fetch)

    def test_missing_credentials_or_scope_nonzero_without_network(self):
        for env in [{}, {"RENDER_API_KEY": "secret"}, {"RENDER_OWNER_ID": OWNER}]:
            with patch.dict(os.environ, env, clear=True), patch.object(MODULE, "list_services") as fetch:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main([]), 1)
                fetch.assert_not_called()
                result = json.loads(output.getvalue())
                self.assertFalse(result["metadata_checks_passed"])
                self.assertFalse(result["runtime_or_release_authority"])

    def test_exact_repository_origin(self):
        self.assertEqual(MODULE.repository_name(f"https://github.com/{REPO}.git"), REPO)
        for value in [None, 1, "https://evil.test/Conxian/conxian-gateway", f"https://github.com/{REPO}/extra"]:
            self.assertIsNone(MODULE.repository_name(value))

    def test_public_ci_summary_omits_infrastructure_details(self):
        with patch.dict(os.environ, {}, clear=True):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(MODULE.main(["--summary-only"]), 1)
            result = json.loads(output.getvalue())
            self.assertEqual(set(result), {"metadata_checks_passed", "runtime_or_release_authority", "error_count"})
            self.assertGreater(result["error_count"], 0)

    def test_authentication_redirect_is_not_followed(self):
        self.assertIsNone(MODULE.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.test"))


if __name__ == "__main__":
    unittest.main()
