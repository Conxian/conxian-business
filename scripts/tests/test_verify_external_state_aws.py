"""Prove rejected identities cannot reach KMS or EC2 diagnostics."""
import contextlib
import io
import os
import sys
import types
import unittest
from unittest.mock import Mock, patch

from scripts import verify_external_state as audit


class AwsIdentityBoundaryTests(unittest.TestCase):
    def tearDown(self):
        audit._results.clear()

    def run_probe(self, identity=None, error=None):
        sts = Mock()
        sts.get_caller_identity.return_value = identity
        sts.get_caller_identity.side_effect = error
        kms, ec2 = Mock(), Mock()
        client = Mock(side_effect=lambda service, **kwargs: {"sts": sts, "kms": kms, "ec2": ec2}[service])
        audit._results.clear()
        with patch.dict(os.environ, {"AWS_ACCESS_KEY_ID": "test-only", "AWS_SECRET_ACCESS_KEY": "test-only"}), \
                patch.dict(sys.modules, {"boto3": types.SimpleNamespace(client=client)}), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            audit.check_aws()
        return client, output.getvalue()

    def assert_stopped(self, identity=None, error=None):
        client, output = self.run_probe(identity, error)
        self.assertEqual([c.args[0] for c in client.call_args_list], ["sts"])
        self.assertTrue(any(status == audit.FAIL for status, _, _ in audit._results))
        return output

    def test_root_stops_before_downstream_clients(self):
        self.assert_stopped({"Account": audit.AWS_ACCOUNT, "Arn": f"arn:aws:iam::{audit.AWS_ACCOUNT}:root"})

    def test_wrong_account_stops_even_with_expected_user_name(self):
        self.assert_stopped({"Account": "000000000000", "Arn": f"arn:aws:iam::000000000000:user/{audit.AWS_IAM_USER}"})

    def test_unknown_user_stops(self):
        self.assert_stopped({"Account": audit.AWS_ACCOUNT, "Arn": f"arn:aws:iam::{audit.AWS_ACCOUNT}:user/other"})

    def test_assumed_role_session_name_cannot_impersonate_expected_user(self):
        self.assert_stopped({"Account": audit.AWS_ACCOUNT, "Arn": f"arn:aws:sts::{audit.AWS_ACCOUNT}:assumed-role/other/{audit.AWS_IAM_USER}"})

    def test_arn_account_must_match_even_when_account_field_matches(self):
        self.assert_stopped({"Account": audit.AWS_ACCOUNT, "Arn": f"arn:aws:iam::000000000000:user/{audit.AWS_IAM_USER}"})

    def test_missing_or_malformed_identity_stops(self):
        for identity in (None, {}, {"Account": audit.AWS_ACCOUNT}, {"Account": audit.AWS_ACCOUNT, "Arn": []}):
            with self.subTest(identity=identity):
                self.assert_stopped(identity)

    def test_sts_error_stops_without_printing_arbitrary_provider_text(self):
        output = self.assert_stopped(error=RuntimeError("synthetic-sensitive-provider-body"))
        self.assertNotIn("synthetic-sensitive-provider-body", output)

    def test_exact_expected_identity_preserves_existing_diagnostics(self):
        client, _ = self.run_probe({"Account": audit.AWS_ACCOUNT, "Arn": f"arn:aws:iam::{audit.AWS_ACCOUNT}:user/{audit.AWS_IAM_USER}"})
        self.assertEqual([c.args[0] for c in client.call_args_list], ["sts", "kms", "ec2"])

    def test_missing_credentials_is_failure_without_client_creation(self):
        client = Mock()
        audit._results.clear()
        with patch.dict(os.environ, {"AWS_ACCESS_KEY_ID": "", "AWS_SECRET_ACCESS_KEY": ""}), \
                patch.dict(sys.modules, {"boto3": types.SimpleNamespace(client=client)}), \
                contextlib.redirect_stdout(io.StringIO()):
            audit.check_aws()
        client.assert_not_called()
        self.assertEqual(audit._results[0][0], audit.FAIL)

    def test_missing_sdk_is_failure(self):
        audit._results.clear()
        with patch.dict(os.environ, {"AWS_ACCESS_KEY_ID": "test-only", "AWS_SECRET_ACCESS_KEY": "test-only"}), \
                patch.dict(sys.modules, {"boto3": None}), \
                contextlib.redirect_stdout(io.StringIO()):
            audit.check_aws()
        self.assertEqual(audit._results[0][0], audit.FAIL)

    def test_sts_client_failure_is_redacted_and_stops(self):
        client = Mock(side_effect=RuntimeError("synthetic-sensitive-client-error"))
        audit._results.clear()
        with patch.dict(os.environ, {"AWS_ACCESS_KEY_ID": "test-only", "AWS_SECRET_ACCESS_KEY": "test-only"}), \
                patch.dict(sys.modules, {"boto3": types.SimpleNamespace(client=client)}), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            audit.check_aws()
        self.assertEqual([c.args[0] for c in client.call_args_list], ["sts"])
        self.assertEqual(audit._results[0][0], audit.FAIL)
        self.assertNotIn("synthetic-sensitive-client-error", output.getvalue())


if __name__ == "__main__":
    unittest.main()
