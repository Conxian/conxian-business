import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("billing_propagation", Path(__file__).parents[1] / "verify_billing_propagation.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BillingPropagationTests(unittest.TestCase):
    def setUp(self):
        self.record = {"schema_version": 1, "kind": "billing-propagation",
                       "production_accepted": False, "runtime_entitlement_implemented": False,
                       "new_prices_authorized": False, "projects_updated": False,
                       "sdk_resolution": {"core": True, "gateway": True, "nexus": False},
                       "sources": {key: {"repository": f"Conxian/{repo}", "commit": char * 40}
                                   for (key, repo), char in zip(MODULE.REPOS.items(), "abcd")}}
        catalog = {"schema": "conxian.billing.catalog", "schema_version": 1,
                   "policy_id": "legacy-billing-v1", "status": "configuration_only",
                   "confers_entitlement": False, "cross_product_entitlement": "unavailable",
                   "gateway": {"unit": "usd_cents"}, "nexus": {"upgrade_unit": "satoshis"}}
        self.files = {"core/spec/billing_conformance.v1.json": json.dumps(catalog),
                      "sdk/Cargo.toml": '[package]\nversion = "2.1.0"\n',
                      "core/Cargo.toml": '[package]\nversion = "0.3.3"\n[dependencies]\n'
                      'conxius-enclave-sdk = { git = "https://github.com/Conxian/conxius-enclave-sdk", '
                      f'rev = "{"a" * 40}", version = "2.1.0", default-features = false, optional = true }}\n'}
        self.record["catalog_sha256"] = hashlib.sha256(self.files["core/spec/billing_conformance.v1.json"].encode()).hexdigest()
        sdk_lock = '[[package]]\nname = "conxius-enclave-sdk"\nversion = "2.1.0"\n' + f'source = "git+https://github.com/Conxian/conxius-enclave-sdk?rev={"a" * 40}#{"a" * 40}"\n'
        core_lock = '[[package]]\nname = "lib-conxian-core"\nversion = "0.3.3"\n' + f'source = "git+https://github.com/Conxian/lib-conxian-core?rev={"b" * 40}#{"b" * 40}"\n'
        self.files["core/Cargo.lock"] = sdk_lock
        for consumer, table, path in [("gateway", "workspace.dependencies", "internal/engine/src/billing.rs"),
                                      ("nexus", "dependencies", "src/api/billing/mod.rs")]:
            self.files[f"{consumer}/Cargo.toml"] = f'[{table}]\n' + 'lib-conxian-core = { git = "https://github.com/Conxian/lib-conxian-core", ' + f'rev = "{"b" * 40}" }}\n'
            self.files[f"{consumer}/Cargo.lock"] = (sdk_lock if consumer == "gateway" else "") + core_lock
            self.files[f"{consumer}/{path}"] = "pub use lib_conxian_core::billing::billing_catalog;\n"

    def test_valid_configuration_is_not_authority(self):
        self.assertEqual(MODULE.validate_contents(self.record, self.files), [])

    def test_nonobject_records_and_boolean_versions_are_rejected(self):
        for value in [None, [], "", 0]:
            self.assertTrue(MODULE.validate_record(value))
        record = copy.deepcopy(self.record)
        record["schema_version"] = True
        self.assertTrue(MODULE.validate_record(record))

    def test_missing_immutable_source_is_rejected(self):
        for value in ["dev", "abc123", "A" * 40, None]:
            with self.subTest(value=value):
                record = copy.deepcopy(self.record)
                record["sources"]["core"]["commit"] = value
                self.assertTrue(MODULE.validate_record(record))

    def test_missing_wrong_or_extra_repository_is_rejected(self):
        for mutation in ["missing", "wrong", "extra"]:
            record = copy.deepcopy(self.record)
            if mutation == "missing":
                del record["sources"]["nexus"]
            elif mutation == "wrong":
                record["sources"]["sdk"]["repository"] = "other/repo"
            else:
                record["sources"]["extra"] = {}
            self.assertTrue(MODULE.validate_record(record))

    def test_authority_flags_are_not_coerced_or_granted(self):
        for key in ["production_accepted", "runtime_entitlement_implemented", "new_prices_authorized", "projects_updated"]:
            for value in [True, "false", 0, None]:
                record = copy.deepcopy(self.record)
                record[key] = value
                self.assertTrue(MODULE.validate_record(record))

    def test_changed_catalog_is_rejected(self):
        files = dict(self.files)
        files["core/spec/billing_conformance.v1.json"] += " "
        self.assertIn("catalog digest mismatch", MODULE.validate_contents(self.record, files))

    def test_catalog_authority_or_boolean_version_is_rejected_with_matching_digest(self):
        for key, value in [("confers_entitlement", True), ("schema_version", True),
                           ("cross_product_entitlement", "active")]:
            files = dict(self.files)
            catalog = json.loads(files["core/spec/billing_conformance.v1.json"])
            catalog[key] = value
            files["core/spec/billing_conformance.v1.json"] = json.dumps(catalog)
            record = copy.deepcopy(self.record)
            record["catalog_sha256"] = hashlib.sha256(files["core/spec/billing_conformance.v1.json"].encode()).hexdigest()
            self.assertIn("unsupported catalog identity or authority", MODULE.validate_contents(record, files))

    def test_wrong_asset_or_catalog_authority_is_rejected_even_with_new_digest(self):
        for key, value in [("unit", "X402"), ("unit", "satoshis")]:
            files = dict(self.files)
            catalog = json.loads(files["core/spec/billing_conformance.v1.json"])
            catalog["gateway"][key] = value
            files["core/spec/billing_conformance.v1.json"] = json.dumps(catalog)
            record = copy.deepcopy(self.record)
            record["catalog_sha256"] = hashlib.sha256(files["core/spec/billing_conformance.v1.json"].encode()).hexdigest()
            self.assertIn("billing units must remain separate", MODULE.validate_contents(record, files))

    def test_missing_or_wrong_locked_sources_are_rejected(self):
        for consumer in ["core", "gateway", "nexus"]:
            source_sha = ("b" if consumer == "nexus" else "a") * 40
            for replacement in ["", self.files[f"{consumer}/Cargo.lock"].replace(source_sha, "e" * 40)]:
                files = dict(self.files)
                files[f"{consumer}/Cargo.lock"] = replacement
                self.assertTrue(MODULE.validate_contents(self.record, files))

    def test_disabled_nexus_sdk_is_not_claimed_as_resolved(self):
        files = dict(self.files)
        files["nexus/Cargo.lock"] += self.files["core/Cargo.lock"]
        self.assertIn("nexus: optional SDK must remain unresolved", MODULE.validate_contents(self.record, files))

    def test_sdk_resolution_requires_exact_boolean_configuration(self):
        for value in [None, {}, {"core": True, "gateway": True, "nexus": True},
                      {"core": True, "gateway": True, "nexus": 0},
                      {"core": False, "gateway": True, "nexus": False}]:
            record = copy.deepcopy(self.record)
            record["sdk_resolution"] = value
            self.assertTrue(MODULE.validate_record(record))

    def test_moving_core_tag_or_branch_is_rejected(self):
        for field in ['tag = "v0.3.3"', 'branch = "dev"']:
            files = dict(self.files)
            files["gateway/Cargo.toml"] = files["gateway/Cargo.toml"].replace(f'rev = "{"b" * 40}"', field)
            self.assertTrue(MODULE.validate_contents(self.record, files))

    def test_sdk_default_features_or_version_drift_is_rejected(self):
        for before, after in [("default-features = false", "default-features = true"),
                              ("2.1.0", "2.0.17"), ("optional = true", "optional = false")]:
            files = dict(self.files)
            files["core/Cargo.toml"] = files["core/Cargo.toml"].replace(before, after)
            self.assertTrue(MODULE.validate_contents(self.record, files))

    def test_reintroduced_local_rates_are_rejected(self):
        files = dict(self.files)
        files["gateway/internal/engine/src/billing.rs"] += "pub const MANAGED_GATEWAY_BASE_FEE_CENTS: u64 = 20000;"
        self.assertIn("gateway: duplicate billing definition", MODULE.validate_contents(self.record, files))

    def test_missing_import_and_malformed_source_are_rejected(self):
        for content in ["", "not a shared billing module"]:
            files = dict(self.files)
            files["nexus/src/api/billing/mod.rs"] = content
            self.assertIn("nexus: shared billing import missing", MODULE.validate_contents(self.record, files))
        files = dict(self.files)
        del files["core/Cargo.toml"]
        self.assertTrue(MODULE.validate_contents(self.record, files))

    def test_process_fails_closed_for_invalid_record_or_missing_sources(self):
        for record in [{}, self.record]:
            with self.subTest(record=record), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "record.json"
                path.write_text(json.dumps(record))
                result = subprocess.run(
                    [sys.executable, str(Path(MODULE.__file__)), "--record", str(path),
                     "--source-root", str(Path(directory) / "missing")],
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 1)
                output = json.loads(result.stdout)
                self.assertIs(output["valid"], False)
                self.assertIs(output["runtime_or_release_authority"], False)
                self.assertTrue(output["errors"])


if __name__ == "__main__":
    unittest.main()
