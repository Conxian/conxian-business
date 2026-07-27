import copy
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.validate_external_semantic_sources import (
    MANDATORY_NOT_SUPPORTED,
    RegistryValidator,
    STATE_DISPOSITIONS,
    main,
    validate_registry,
)


COMMIT = "0123456789abcdef0123456789abcdef01234567"
DIGEST = "a" * 64


class SemanticSourceRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "governance").mkdir()
        schema_source = Path("governance/external-semantic-sources.schema.v1.json")
        (self.root / "governance/external-semantic-sources.schema.v1.json").write_text(
            schema_source.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self.registry_path = self.root / "governance/external-semantic-sources.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def registry(self, sources=None):
        return {
            "$schema": "external-semantic-sources.schema.v1.json",
            "schemaVersion": "1.0.0",
            "sources": [] if sources is None else sources,
        }

    def research_source(self, source_id="pinned-research-source"):
        return {
            "id": source_id,
            "name": "Pinned research source",
            "repositoryUrl": "https://example.org/upstream/source",
            "commitSha": COMMIT,
            "archiveUrl": f"https://example.org/upstream/source/archive/{COMMIT}.tar.gz",
            "archiveSha256": DIGEST,
            "observedDate": "2026-07-27",
            "state": "research-only",
            "review": {
                "disposition": "approved-for-research",
                "reference": "#940",
            },
            "selectedFiles": [],
            "importClosure": {
                "status": "not-evaluated",
                "imports": [],
                "evidence": None,
            },
            "notices": {
                "rootLicense": None,
                "files": [],
            },
            "extensionNamespace": {
                "uri": f"https://schema.conxian.io/semantic/{source_id}/",
                "owner": "Conxian-Labs (Pty) Ltd",
            },
            "transformations": {
                "status": "not-evaluated",
                "rationale": "No transformation is authorized for research-only intake.",
                "records": [],
                "evidence": None,
            },
            "sbomHandoff": {
                "status": "not-ready",
                "evidence": None,
            },
            "claims": {
                "supported": ["Immutable source identity observed for bounded research."],
                "notSupported": sorted(MANDATORY_NOT_SUPPORTED),
            },
        }

    def adopted_source(self, source_id="fully-evidenced-source"):
        def artifact(filename, content):
            relative = Path(
                "governance/evidence/external-semantic-sources"
            ) / source_id / filename
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            return {
                "path": relative.as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
            }

        return {
            "id": source_id,
            "name": "Fully evidenced source",
            "repositoryUrl": "https://example.org/upstream/source",
            "commitSha": COMMIT,
            "archiveUrl": f"https://example.org/upstream/source/archive/{COMMIT}.tar.gz",
            "archiveSha256": DIGEST,
            "observedDate": "2026-07-27",
            "state": "adopted",
            "review": {
                "disposition": "approved-for-adoption",
                "reference": "DECISION-955",
            },
            "selectedFiles": ["ontology/root.rdf"],
            "importClosure": {
                "status": "closed",
                "imports": [
                    {
                        "from": "ontology/root.rdf",
                        "to": "ontology/dependency.rdf",
                    }
                ],
                "evidence": artifact("import-closure.json", b"closed import graph\n"),
            },
            "notices": {
                "rootLicense": artifact("root-license.txt", b"license evidence\n"),
                "files": [
                    {
                        "path": "ontology/root.rdf",
                        "notice": artifact("root.notice.txt", b"root notice\n"),
                    },
                    {
                        "path": "ontology/dependency.rdf",
                        "notice": artifact("dependency.notice.txt", b"dependency notice\n"),
                    },
                ],
            },
            "extensionNamespace": {
                "uri": f"https://schema.conxian.io/semantic/{source_id}/",
                "owner": "Conxian-Labs (Pty) Ltd",
            },
            "transformations": {
                "status": "none",
                "rationale": "No transformed artifact is part of this fixture.",
                "records": [],
                "evidence": artifact("transformation-disposition.json", b"none\n"),
            },
            "sbomHandoff": {
                "status": "handoff-ready",
                "evidence": artifact("sbom-handoff.json", b"handoff evidence\n"),
            },
            "claims": {
                "supported": [
                    "The selected file and import manifest have immutable local evidence."
                ],
                "notSupported": sorted(MANDATORY_NOT_SUPPORTED),
            },
        }

    def write(self, registry):
        self.registry_path.write_text(
            json.dumps(registry, indent=2) + "\n",
            encoding="utf-8",
        )

    def assert_valid(self, registry):
        self.write(registry)
        self.assertEqual([], validate_registry(self.registry_path))

    def assert_invalid(self, registry, fragment):
        self.write(registry)
        errors = validate_registry(self.registry_path)
        self.assertTrue(errors, "expected registry validation to fail")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in errors: {errors}",
        )

    def test_empty_registry_passes(self):
        self.assert_valid(self.registry())

    def test_branch_tag_short_and_uppercase_commit_refs_fail(self):
        invalid_refs = ["main", "master_2026Q2", COMMIT[:12], COMMIT.upper()]
        for invalid_ref in invalid_refs:
            with self.subTest(commitSha=invalid_ref):
                source = self.research_source()
                source["commitSha"] = invalid_ref
                self.assert_invalid(self.registry([source]), "full 40-character lowercase")

    def test_malformed_digest_fails(self):
        for digest in ("a" * 63, "A" * 64, "g" * 64):
            with self.subTest(digest=digest):
                source = self.research_source()
                source["archiveSha256"] = digest
                self.assert_invalid(self.registry([source]), "64 lowercase hexadecimal")

    def test_adopted_source_missing_notices_fails(self):
        source = self.adopted_source()
        source["notices"]["files"] = source["notices"]["files"][:1]
        self.assert_invalid(self.registry([source]), "missing notice disposition")

    def test_adopted_source_missing_closure_evidence_fails(self):
        source = self.adopted_source()
        source["importClosure"]["evidence"] = None
        self.assert_invalid(self.registry([source]), "requires closed import evidence")

    def test_upstream_owned_namespace_fails(self):
        source = self.adopted_source()
        source["extensionNamespace"] = {
            "uri": "https://example.org/upstream/ontology/",
            "owner": "Upstream Foundation",
        }
        self.assert_invalid(self.registry([source]), "Conxian-owned HTTPS namespace")

    def test_selected_adopted_namespace_schema_validator_parity(self):
        schema = json.loads(
            Path("governance/external-semantic-sources.schema.v1.json").read_text(
                encoding="utf-8"
            )
        )
        selected_rule = next(
            rule
            for rule in schema["$defs"]["source"]["allOf"]
            if rule.get("if", {}).get("properties", {}).get("state", {}).get("enum")
            == ["selected", "adopted"]
        )
        namespace_properties = selected_rule["then"]["properties"][
            "extensionNamespace"
        ]["properties"]
        uri_pattern = re.compile(namespace_properties["uri"]["pattern"])
        owner_pattern = re.compile(namespace_properties["owner"]["pattern"])

        cases = (
            ("https://conxian.com/semantic", "Conxian", True),
            ("https://schema.conxian.io/semantic/source/", "Conxian-Labs (Pty) Ltd", True),
            ("https://conxian.com", "Conxian", False),
            ("https://conxian.com/", "Conxian", False),
            ("https://conxian.com/semantic", "conxian-labs", False),
            ("https://example.org/semantic", "Conxian-Labs (Pty) Ltd", False),
            (123, "Conxian-Labs (Pty) Ltd", False),
            ("https://conxian.io/semantic", ["Conxian"], False),
        )
        for state, disposition in (
            ("selected", "approved-for-selection"),
            ("adopted", "approved-for-adoption"),
        ):
            for uri, owner, expected in cases:
                with self.subTest(state=state, uri=uri, owner=owner):
                    schema_accepts = (
                        isinstance(uri, str)
                        and uri.startswith("https://")
                        and uri_pattern.search(uri) is not None
                        and isinstance(owner, str)
                        and bool(owner)
                        and owner_pattern.search(owner) is not None
                    )
                    self.assertEqual(expected, schema_accepts)

                    source = self.adopted_source()
                    source["state"] = state
                    source["review"]["disposition"] = disposition
                    source["extensionNamespace"] = {"uri": uri, "owner": owner}
                    self.write(self.registry([source]))
                    validator_accepts = validate_registry(self.registry_path) == []
                    self.assertEqual(schema_accepts, validator_accepts)

    def test_prohibited_supported_claim_fails(self):
        claims = [
            "This source proves regulatory compliance.",
            "Registry presence establishes adoption.",
            "BOS Gate 0-6 advancement is approved.",
        ]
        for claim in claims:
            with self.subTest(claim=claim):
                source = self.research_source()
                source["claims"]["supported"] = [claim]
                self.assert_invalid(self.registry([source]), "prohibited positive claim")

    def test_negative_not_supported_claims_are_allowed(self):
        source = self.research_source()
        source["claims"]["notSupported"].append(
            "This record is not certification or endorsement evidence."
        )
        self.assert_valid(self.registry([source]))

    def test_path_traversal_fails(self):
        source = self.adopted_source()
        source["importClosure"]["evidence"]["path"] = (
            "governance/evidence/external-semantic-sources/fully-evidenced-source/../escape.json"
        )
        self.assert_invalid(self.registry([source]), "traversal segments")

    def test_disallowed_evidence_path_fails(self):
        source = self.adopted_source()
        source["importClosure"]["evidence"]["path"] = "docs/import-closure.json"
        self.assert_invalid(self.registry([source]), "must be below")

    def test_duplicate_ids_fail(self):
        first = self.research_source("duplicate-source")
        second = copy.deepcopy(first)
        self.assert_invalid(self.registry([first, second]), "duplicate source id")

    def test_duplicate_import_mapping_fails(self):
        source = self.adopted_source()
        source["importClosure"]["imports"].append(
            copy.deepcopy(source["importClosure"]["imports"][0])
        )
        self.assert_invalid(self.registry([source]), "duplicate import mapping")

    def test_duplicate_artifact_fails(self):
        source = self.adopted_source()
        source["sbomHandoff"]["evidence"] = copy.deepcopy(
            source["transformations"]["evidence"]
        )
        self.assert_invalid(self.registry([source]), "duplicate evidence artifact")

    def test_invalid_state_and_disposition_fail(self):
        source = self.research_source()
        source["state"] = "unknown"
        source["review"]["disposition"] = "rubber-stamped"
        self.assert_invalid(self.registry([source]), "must be one of")

    def test_enum_boundaries_reject_non_strings_without_crashing(self):
        boundaries = (
            (("state",), "state"),
            (("review", "disposition"), "review.disposition"),
            (("importClosure", "status"), "importClosure.status"),
            (("transformations", "status"), "transformations.status"),
            (("sbomHandoff", "status"), "sbomHandoff.status"),
        )
        for key_path, fragment in boundaries:
            for malformed in ([], {}, None, True, False):
                with self.subTest(boundary=key_path, malformed=malformed):
                    source = self.research_source()
                    target = source
                    for key in key_path[:-1]:
                        target = target[key]
                    target[key_path[-1]] = malformed
                    self.assert_invalid(self.registry([source]), fragment)

    def test_cli_returns_nonzero_for_malformed_enum(self):
        source = self.research_source()
        source["state"] = []
        self.write(self.registry([source]))
        self.assertEqual(1, main([str(self.registry_path)]))

    def test_enum_boundaries_reject_unknown_strings(self):
        boundaries = (
            (("state",), "state"),
            (("review", "disposition"), "review.disposition"),
            (("importClosure", "status"), "importClosure.status"),
            (("transformations", "status"), "transformations.status"),
            (("sbomHandoff", "status"), "sbomHandoff.status"),
        )
        for key_path, fragment in boundaries:
            with self.subTest(boundary=key_path):
                source = self.research_source()
                target = source
                for key in key_path[:-1]:
                    target = target[key]
                target[key_path[-1]] = "unknown-status"
                self.assert_invalid(self.registry([source]), fragment)

    def test_every_lifecycle_disposition_mapping(self):
        valid_pairs = {
            "research-only": ("pending", "approved-for-research"),
            "candidate": ("pending", "approved-for-research"),
            "selected": ("approved-for-selection",),
            "adopted": ("approved-for-adoption",),
            "rejected": ("rejected",),
            "retired": ("retired",),
        }
        all_dispositions = {
            "pending",
            "approved-for-research",
            "approved-for-selection",
            "approved-for-adoption",
            "rejected",
            "retired",
        }
        for state, allowed in valid_pairs.items():
            for disposition in all_dispositions:
                with self.subTest(state=state, disposition=disposition):
                    source = (
                        self.adopted_source()
                        if state in {"selected", "adopted"}
                        else self.research_source()
                    )
                    source["state"] = state
                    source["review"]["disposition"] = disposition
                    if disposition in allowed:
                        self.assert_valid(self.registry([source]))
                    else:
                        self.assert_invalid(self.registry([source]), "is not valid for state")

    def test_schema_lifecycle_disposition_mapping_matches_validator(self):
        schema = json.loads(
            Path("governance/external-semantic-sources.schema.v1.json").read_text(
                encoding="utf-8"
            )
        )
        observed = {}
        for rule in schema["$defs"]["source"]["allOf"]:
            state_rule = rule.get("if", {}).get("properties", {}).get("state", {})
            state = state_rule.get("const")
            if state not in STATE_DISPOSITIONS:
                continue
            disposition_rule = rule["then"]["properties"]["review"]["properties"][
                "disposition"
            ]
            allowed = disposition_rule.get("enum")
            if allowed is None:
                allowed = [disposition_rule["const"]]
            observed[state] = set(allowed)

        self.assertEqual(STATE_DISPOSITIONS, observed)

    def test_internal_leaf_symlink_evidence_fails(self):
        source = self.adopted_source()
        evidence_path = self.root / source["importClosure"]["evidence"]["path"]
        target = evidence_path.with_name("import-closure-target.json")
        evidence_path.rename(target)
        evidence_path.symlink_to(target.name)
        self.assert_invalid(self.registry([source]), "must not use symlink indirection")

    def test_internal_parent_symlink_evidence_fails(self):
        source = self.adopted_source()
        source_dir = self.root / "governance/evidence/external-semantic-sources/fully-evidenced-source"
        target_dir = source_dir.with_name("fully-evidenced-source-target")
        source_dir.rename(target_dir)
        source_dir.symlink_to(target_dir.name, target_is_directory=True)
        self.assert_invalid(self.registry([source]), "must not use symlink indirection")

    def test_escaping_symlink_evidence_fails(self):
        source = self.adopted_source()
        evidence_path = self.root / source["importClosure"]["evidence"]["path"]
        outside = self.root.parent / f"{self.root.name}-outside-evidence.json"
        outside.write_bytes(b"closed import graph\n")
        self.addCleanup(outside.unlink, missing_ok=True)
        evidence_path.unlink()
        evidence_path.symlink_to(outside)
        self.assert_invalid(self.registry([source]), "must not use symlink indirection")

    def test_unexpected_internal_error_fails_closed_and_preserves_errors(self):
        self.write(self.registry())

        def fail_after_useful_error(validator, registry):
            validator.error("registry.sources", "useful validation message")
            raise TypeError("simulated defect")

        with mock.patch.object(
            RegistryValidator,
            "_validate_registry",
            autospec=True,
            side_effect=fail_after_useful_error,
        ):
            errors = validate_registry(self.registry_path)

        self.assertTrue(any("useful validation message" in error for error in errors))
        self.assertTrue(any("validation failed closed" in error for error in errors))

    def test_schema_registry_mismatch_fails(self):
        registry = self.registry()
        registry["schemaVersion"] = "2.0.0"
        self.assert_invalid(registry, "must equal '1.0.0'")

    def test_malformed_date_and_url_fail(self):
        source = self.research_source()
        source["observedDate"] = "2026-02-30"
        source["repositoryUrl"] = "http://example.org/source"
        self.assert_invalid(self.registry([source]), "valid calendar date")
        self.assert_invalid(self.registry([source]), "absolute HTTPS URL")

    def test_pinned_research_only_fixture_passes_without_corpus_or_adoption(self):
        source = self.research_source()
        self.assertEqual("research-only", source["state"])
        self.assertEqual([], source["selectedFiles"])
        self.assert_valid(self.registry([source]))

    def test_fully_evidenced_adopted_fixture_passes(self):
        self.assert_valid(self.registry([self.adopted_source()]))


if __name__ == "__main__":
    unittest.main()
