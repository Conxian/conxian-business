#!/usr/bin/env python3
"""Validate the external semantic-source registry without network access."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlsplit


SCHEMA_FILENAME = "external-semantic-sources.schema.v1.json"
SCHEMA_VERSION = "1.0.0"
EVIDENCE_PREFIX = PurePosixPath("governance/evidence/external-semantic-sources")

STATES = {
    "research-only",
    "candidate",
    "selected",
    "adopted",
    "rejected",
    "retired",
}
DISPOSITIONS = {
    "pending",
    "approved-for-research",
    "approved-for-selection",
    "approved-for-adoption",
    "rejected",
    "retired",
}
STATE_DISPOSITIONS = {
    "research-only": {"pending", "approved-for-research"},
    "candidate": {"pending", "approved-for-research"},
    "selected": {"approved-for-selection"},
    "adopted": {"approved-for-adoption"},
    "rejected": {"rejected"},
    "retired": {"retired"},
}
IMPORT_STATUSES = {"not-evaluated", "not-applicable", "closed"}
TRANSFORMATION_STATUSES = {"not-evaluated", "none", "recorded"}
SBOM_STATUSES = {"not-ready", "handoff-ready"}

MANDATORY_NOT_SUPPORTED = {
    "registry presence alone as adoption",
    "legal advice",
    "endorsement",
    "certification",
    "partnership",
    "compliance evidence",
    "authority evidence",
    "attestation evidence",
    "candidate acceptance",
    "release approval",
    "BOS Gate 0-6 advancement",
}

PROHIBITED_SUPPORTED_CLAIMS = (
    re.compile(r"\b(?:legal advice|compliance|endorsement|certification|partnership)\b", re.I),
    re.compile(r"\b(?:authority|attestation)(?:\s+evidence)?\b", re.I),
    re.compile(r"\bcandidate\s+accept(?:ance|ed)\b", re.I),
    re.compile(r"\brelease\s+(?:approval|approved|acceptance|ready|readiness)\b", re.I),
    re.compile(r"\b(?:bos\s+)?gate(?:s)?(?:\s*[0-6](?:\s*[-–]\s*[0-6])?)?\s+(?:advance|advanced|advancement|approved|passed|satisfied)\b", re.I),
    re.compile(r"\bregistry\s+presence\b.*\badopt(?:ion|ed)?\b", re.I),
    re.compile(r"\b(?:endorsed|certified|partnered|compliant|authoritative|attested)\b", re.I),
)

SOURCE_KEYS = {
    "id",
    "name",
    "repositoryUrl",
    "commitSha",
    "archiveUrl",
    "archiveSha256",
    "observedDate",
    "state",
    "review",
    "selectedFiles",
    "importClosure",
    "notices",
    "extensionNamespace",
    "transformations",
    "sbomHandoff",
    "claims",
}


class DuplicateKeyError(ValueError):
    """Raised when JSON contains duplicate object keys."""


class RegistryValidator:
    def __init__(self, registry_path: Path) -> None:
        self.registry_path = registry_path.resolve()
        self.repo_root = self._find_repo_root(self.registry_path)
        self.errors: list[str] = []
        self.artifact_paths: set[str] = set()

    @staticmethod
    def _find_repo_root(registry_path: Path) -> Path:
        for parent in (registry_path.parent, *registry_path.parents):
            if (parent / ".git").exists():
                return parent.resolve()
        if registry_path.parent.name == "governance":
            return registry_path.parent.parent.resolve()
        return Path.cwd().resolve()

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{location}: {message}")

    def validate(self) -> list[str]:
        registry = self._load_json(self.registry_path, "registry")
        if registry is None:
            return self.errors

        schema_path = self.registry_path.with_name(SCHEMA_FILENAME)
        schema = self._load_json(schema_path, "schema")
        if schema is None:
            return self.errors

        self._validate_schema_contract(schema)
        self._validate_registry(registry)
        return self.errors

    def _load_json(self, path: Path, label: str) -> Any | None:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            self.error(label, f"cannot read {path}: {exc}")
            return None

        def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise DuplicateKeyError(f"duplicate JSON key {key!r}")
                result[key] = value
            return result

        try:
            return json.loads(text, object_pairs_hook=reject_duplicates)
        except (json.JSONDecodeError, DuplicateKeyError) as exc:
            self.error(label, f"invalid JSON: {exc}")
            return None

    def _validate_schema_contract(self, schema: Any) -> None:
        location = "schema"
        if not isinstance(schema, dict):
            self.error(location, "must be a JSON object")
            return
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            self.error(location, "must declare JSON Schema draft 2020-12")
        properties = schema.get("properties")
        if not isinstance(properties, dict):
            self.error(location, "properties must be an object")
            return
        schema_const = properties.get("$schema", {}).get("const") if isinstance(properties.get("$schema"), dict) else None
        version_const = properties.get("schemaVersion", {}).get("const") if isinstance(properties.get("schemaVersion"), dict) else None
        if schema_const != SCHEMA_FILENAME:
            self.error(location, f"$schema const must be {SCHEMA_FILENAME!r}")
        if version_const != SCHEMA_VERSION:
            self.error(location, f"schemaVersion const must be {SCHEMA_VERSION!r}")
        if schema.get("additionalProperties") is not False:
            self.error(location, "top-level additionalProperties must be false")
        if set(schema.get("required", [])) != {"$schema", "schemaVersion", "sources"}:
            self.error(location, "required fields do not match the registry contract")

    def _validate_registry(self, registry: Any) -> None:
        if not isinstance(registry, dict):
            self.error("registry", "must be a JSON object")
            return
        self._exact_keys(registry, {"$schema", "schemaVersion", "sources"}, "registry")
        if registry.get("$schema") != SCHEMA_FILENAME:
            self.error("registry.$schema", f"must equal {SCHEMA_FILENAME!r}")
        if registry.get("schemaVersion") != SCHEMA_VERSION:
            self.error("registry.schemaVersion", f"must equal {SCHEMA_VERSION!r}")
        sources = registry.get("sources")
        if not isinstance(sources, list):
            self.error("registry.sources", "must be an array")
            return

        seen_ids: set[str] = set()
        for index, source in enumerate(sources):
            location = f"registry.sources[{index}]"
            if not isinstance(source, dict):
                self.error(location, "must be an object")
                continue
            source_id = source.get("id")
            if isinstance(source_id, str):
                if source_id in seen_ids:
                    self.error(f"{location}.id", f"duplicate source id {source_id!r}")
                seen_ids.add(source_id)
            self._validate_source(source, location)

    def _validate_source(self, source: dict[str, Any], location: str) -> None:
        self._exact_keys(source, SOURCE_KEYS, location)
        source_id = self._string(source.get("id"), f"{location}.id")
        if source_id is not None and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id):
            self.error(f"{location}.id", "must be a lowercase kebab-case identifier")
        self._string(source.get("name"), f"{location}.name")

        repository_url = self._https_url(source.get("repositoryUrl"), f"{location}.repositoryUrl")
        commit_sha = self._commit_sha(source.get("commitSha"), f"{location}.commitSha")
        archive_url = self._https_url(source.get("archiveUrl"), f"{location}.archiveUrl")
        self._sha256(source.get("archiveSha256"), f"{location}.archiveSha256")
        self._date(source.get("observedDate"), f"{location}.observedDate")
        if archive_url and commit_sha:
            lowered = archive_url.lower()
            if commit_sha not in archive_url:
                self.error(f"{location}.archiveUrl", "must contain the full immutable commit SHA")
            if any(marker in lowered for marker in ("/refs/heads/", "/refs/tags/", "/tree/master", "/tree/main", "/latest")):
                self.error(f"{location}.archiveUrl", "must not use a branch, tag, latest, or other moving reference")
        if repository_url and commit_sha and repository_url.rstrip("/").endswith(f"/{commit_sha}"):
            self.error(f"{location}.repositoryUrl", "must identify the repository, not duplicate the archive identity")

        state = source.get("state")
        if state not in STATES:
            self.error(f"{location}.state", f"must be one of {sorted(STATES)}")

        review = source.get("review")
        disposition: str | None = None
        if isinstance(review, dict):
            self._exact_keys(review, {"disposition", "reference"}, f"{location}.review")
            disposition_value = review.get("disposition")
            if disposition_value not in DISPOSITIONS:
                self.error(f"{location}.review.disposition", f"must be one of {sorted(DISPOSITIONS)}")
            else:
                disposition = disposition_value
            reference = self._string(review.get("reference"), f"{location}.review.reference")
            if reference is not None and not self._valid_review_reference(reference):
                self.error(f"{location}.review.reference", "must be an HTTPS URL or a stable issue/decision token")
        else:
            self.error(f"{location}.review", "must be an object")

        if state in STATE_DISPOSITIONS and disposition not in STATE_DISPOSITIONS[state]:
            self.error(
                f"{location}.review.disposition",
                f"{disposition!r} is not valid for state {state!r}",
            )

        selected_files = self._path_array(source.get("selectedFiles"), f"{location}.selectedFiles")
        import_files = self._validate_import_closure(source.get("importClosure"), source_id, location)
        closure_files = set(selected_files) | import_files
        notice_files = self._validate_notices(source.get("notices"), source_id, location)
        namespace_owned = self._validate_namespace(source.get("extensionNamespace"), location)
        transformations_closed = self._validate_transformations(source.get("transformations"), source_id, location)
        sbom_closed = self._validate_sbom(source.get("sbomHandoff"), source_id, location)
        claims_closed = self._validate_claims(source.get("claims"), location)

        requires_complete_bundle = state in {"selected", "adopted"}
        if requires_complete_bundle:
            if not selected_files:
                self.error(f"{location}.selectedFiles", f"state {state!r} requires at least one selected file")
            closure = source.get("importClosure")
            if not isinstance(closure, dict) or closure.get("status") != "closed" or closure.get("evidence") is None:
                self.error(f"{location}.importClosure", f"state {state!r} requires closed import evidence")
            notices = source.get("notices")
            if not isinstance(notices, dict) or notices.get("rootLicense") is None:
                self.error(f"{location}.notices.rootLicense", f"state {state!r} requires root-license evidence")
            missing_notices = closure_files - notice_files
            extra_notices = notice_files - closure_files
            if missing_notices:
                self.error(f"{location}.notices.files", f"missing notice disposition for {sorted(missing_notices)}")
            if extra_notices:
                self.error(f"{location}.notices.files", f"contains undeclared files {sorted(extra_notices)}")
            if not namespace_owned:
                self.error(f"{location}.extensionNamespace", f"state {state!r} requires a Conxian-owned namespace")
            if not transformations_closed:
                self.error(f"{location}.transformations", f"state {state!r} requires closed transformation provenance")
            if not sbom_closed:
                self.error(f"{location}.sbomHandoff", f"state {state!r} requires immutable handoff-ready evidence")
            if not claims_closed:
                self.error(f"{location}.claims", f"state {state!r} requires all unsupported-claim boundaries")

    def _validate_import_closure(self, value: Any, source_id: str | None, parent: str) -> set[str]:
        location = f"{parent}.importClosure"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return set()
        self._exact_keys(value, {"status", "imports", "evidence"}, location)
        status = value.get("status")
        if status not in IMPORT_STATUSES:
            self.error(f"{location}.status", f"must be one of {sorted(IMPORT_STATUSES)}")
        imports = value.get("imports")
        import_files: set[str] = set()
        seen: set[tuple[str, str]] = set()
        if not isinstance(imports, list):
            self.error(f"{location}.imports", "must be an array")
        else:
            for index, mapping in enumerate(imports):
                item_location = f"{location}.imports[{index}]"
                if not isinstance(mapping, dict):
                    self.error(item_location, "must be an object")
                    continue
                self._exact_keys(mapping, {"from", "to"}, item_location)
                source_path = self._relative_path(mapping.get("from"), f"{item_location}.from")
                target_path = self._relative_path(mapping.get("to"), f"{item_location}.to")
                if source_path and target_path:
                    pair = (source_path, target_path)
                    if pair in seen:
                        self.error(item_location, f"duplicate import mapping {pair!r}")
                    seen.add(pair)
                    import_files.update(pair)
        evidence = value.get("evidence")
        if evidence is not None:
            self._artifact(evidence, source_id, f"{location}.evidence")
        if status == "closed" and evidence is None:
            self.error(f"{location}.evidence", "closed import status requires evidence")
        return import_files

    def _validate_notices(self, value: Any, source_id: str | None, parent: str) -> set[str]:
        location = f"{parent}.notices"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return set()
        self._exact_keys(value, {"rootLicense", "files"}, location)
        root_license = value.get("rootLicense")
        if root_license is not None:
            self._artifact(root_license, source_id, f"{location}.rootLicense")
        files = value.get("files")
        notice_paths: set[str] = set()
        if not isinstance(files, list):
            self.error(f"{location}.files", "must be an array")
            return notice_paths
        for index, notice in enumerate(files):
            item_location = f"{location}.files[{index}]"
            if not isinstance(notice, dict):
                self.error(item_location, "must be an object")
                continue
            self._exact_keys(notice, {"path", "notice"}, item_location)
            path = self._relative_path(notice.get("path"), f"{item_location}.path")
            if path:
                if path in notice_paths:
                    self.error(f"{item_location}.path", f"duplicate notice mapping for {path!r}")
                notice_paths.add(path)
            self._artifact(notice.get("notice"), source_id, f"{item_location}.notice")
        return notice_paths

    def _validate_namespace(self, value: Any, parent: str) -> bool:
        location = f"{parent}.extensionNamespace"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return False
        self._exact_keys(value, {"uri", "owner"}, location)
        uri = self._https_url(value.get("uri"), f"{location}.uri")
        owner = self._string(value.get("owner"), f"{location}.owner")
        if uri is None or owner is None:
            return False
        host = (urlsplit(uri).hostname or "").lower()
        host_owned = host == "conxian.io" or host.endswith(".conxian.io") or host == "conxian.com" or host.endswith(".conxian.com")
        owner_owned = "conxian" in owner.lower()
        if not host_owned or not owner_owned:
            self.error(location, "must use a Conxian-owned HTTPS namespace and identify Conxian as owner")
            return False
        return True

    def _validate_transformations(self, value: Any, source_id: str | None, parent: str) -> bool:
        location = f"{parent}.transformations"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return False
        self._exact_keys(value, {"status", "rationale", "records", "evidence"}, location)
        status = value.get("status")
        if status not in TRANSFORMATION_STATUSES:
            self.error(f"{location}.status", f"must be one of {sorted(TRANSFORMATION_STATUSES)}")
        rationale = self._string(value.get("rationale"), f"{location}.rationale")
        records = value.get("records")
        if not isinstance(records, list):
            self.error(f"{location}.records", "must be an array")
            records = []
        seen_outputs: set[str] = set()
        for index, record in enumerate(records):
            item_location = f"{location}.records[{index}]"
            if not isinstance(record, dict):
                self.error(item_location, "must be an object")
                continue
            self._exact_keys(record, {"input", "output", "tool", "toolVersion", "evidence"}, item_location)
            self._relative_path(record.get("input"), f"{item_location}.input")
            output = self._relative_path(record.get("output"), f"{item_location}.output")
            if output:
                if output in seen_outputs:
                    self.error(f"{item_location}.output", f"duplicate transformation output {output!r}")
                seen_outputs.add(output)
            self._string(record.get("tool"), f"{item_location}.tool")
            self._string(record.get("toolVersion"), f"{item_location}.toolVersion")
            self._artifact(record.get("evidence"), source_id, f"{item_location}.evidence")
        evidence = value.get("evidence")
        if evidence is not None:
            self._artifact(evidence, source_id, f"{location}.evidence")
        if status == "none" and records:
            self.error(f"{location}.records", "must be empty when status is 'none'")
        if status == "recorded" and not records:
            self.error(f"{location}.records", "must be non-empty when status is 'recorded'")
        return status in {"none", "recorded"} and rationale is not None and evidence is not None

    def _validate_sbom(self, value: Any, source_id: str | None, parent: str) -> bool:
        location = f"{parent}.sbomHandoff"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return False
        self._exact_keys(value, {"status", "evidence"}, location)
        status = value.get("status")
        if status not in SBOM_STATUSES:
            self.error(f"{location}.status", f"must be one of {sorted(SBOM_STATUSES)}")
        evidence = value.get("evidence")
        if evidence is not None:
            self._artifact(evidence, source_id, f"{location}.evidence")
        if status == "handoff-ready" and evidence is None:
            self.error(f"{location}.evidence", "handoff-ready status requires evidence")
        return status == "handoff-ready" and evidence is not None

    def _validate_claims(self, value: Any, parent: str) -> bool:
        location = f"{parent}.claims"
        if not isinstance(value, dict):
            self.error(location, "must be an object")
            return False
        self._exact_keys(value, {"supported", "notSupported"}, location)
        supported = self._string_array(value.get("supported"), f"{location}.supported")
        not_supported = self._string_array(value.get("notSupported"), f"{location}.notSupported")
        for index, claim in enumerate(supported):
            for pattern in PROHIBITED_SUPPORTED_CLAIMS:
                if pattern.search(claim):
                    self.error(
                        f"{location}.supported[{index}]",
                        "contains a prohibited positive claim",
                    )
                    break
        missing = MANDATORY_NOT_SUPPORTED - set(not_supported)
        if missing:
            self.error(f"{location}.notSupported", f"missing mandatory boundaries {sorted(missing)}")
        return not missing

    def _artifact(self, value: Any, source_id: str | None, location: str) -> None:
        if not isinstance(value, dict):
            self.error(location, "must be an artifact object")
            return
        self._exact_keys(value, {"path", "sha256"}, location)
        path_value = self._relative_path(value.get("path"), f"{location}.path")
        digest = self._sha256(value.get("sha256"), f"{location}.sha256")
        if path_value is None:
            return
        path = PurePosixPath(path_value)
        expected_prefix = EVIDENCE_PREFIX / source_id if source_id else EVIDENCE_PREFIX
        if not path.is_relative_to(expected_prefix):
            self.error(f"{location}.path", f"must be below {expected_prefix.as_posix()}/")
            return
        if path_value in self.artifact_paths:
            self.error(f"{location}.path", f"duplicate evidence artifact {path_value!r}")
        self.artifact_paths.add(path_value)

        disk_path = (self.repo_root / Path(*path.parts)).resolve()
        try:
            disk_path.relative_to(self.repo_root)
        except ValueError:
            self.error(f"{location}.path", "resolves outside the repository")
            return
        if not disk_path.is_file():
            self.error(f"{location}.path", "evidence artifact does not exist as a regular file")
            return
        if digest is not None:
            observed = hashlib.sha256(disk_path.read_bytes()).hexdigest()
            if observed != digest:
                self.error(f"{location}.sha256", f"does not match local artifact (observed {observed})")

    def _exact_keys(self, value: dict[str, Any], expected: set[str], location: str) -> None:
        actual = set(value)
        missing = expected - actual
        unknown = actual - expected
        if missing:
            self.error(location, f"missing required fields {sorted(missing)}")
        if unknown:
            self.error(location, f"contains unknown fields {sorted(unknown)}")

    def _string(self, value: Any, location: str) -> str | None:
        if not isinstance(value, str) or not value.strip():
            self.error(location, "must be a non-empty string")
            return None
        if value != value.strip():
            self.error(location, "must not contain leading or trailing whitespace")
            return None
        return value

    def _string_array(self, value: Any, location: str) -> list[str]:
        if not isinstance(value, list):
            self.error(location, "must be an array")
            return []
        result: list[str] = []
        seen: set[str] = set()
        for index, item in enumerate(value):
            text = self._string(item, f"{location}[{index}]")
            if text is None:
                continue
            if text in seen:
                self.error(f"{location}[{index}]", f"duplicate value {text!r}")
            seen.add(text)
            result.append(text)
        return result

    def _path_array(self, value: Any, location: str) -> list[str]:
        if not isinstance(value, list):
            self.error(location, "must be an array")
            return []
        result: list[str] = []
        seen: set[str] = set()
        for index, item in enumerate(value):
            path = self._relative_path(item, f"{location}[{index}]")
            if path is None:
                continue
            if path in seen:
                self.error(f"{location}[{index}]", f"duplicate path {path!r}")
            seen.add(path)
            result.append(path)
        return result

    def _relative_path(self, value: Any, location: str) -> str | None:
        text = self._string(value, location)
        if text is None:
            return None
        if "\\" in text:
            self.error(location, "must use POSIX separators and contain no backslashes")
            return None
        path = PurePosixPath(text)
        if path.is_absolute() or text.startswith("/"):
            self.error(location, "must be repository-relative")
            return None
        if any(part in {"", ".", ".."} for part in path.parts):
            self.error(location, "must contain no empty, current-directory, or traversal segments")
            return None
        return path.as_posix()

    def _sha256(self, value: Any, location: str) -> str | None:
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            self.error(location, "must be exactly 64 lowercase hexadecimal characters")
            return None
        return value

    def _commit_sha(self, value: Any, location: str) -> str | None:
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
            self.error(location, "must be a full 40-character lowercase hexadecimal commit SHA")
            return None
        return value

    def _date(self, value: Any, location: str) -> str | None:
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            self.error(location, "must be an ISO 8601 calendar date (YYYY-MM-DD)")
            return None
        try:
            parsed = dt.date.fromisoformat(value)
        except ValueError:
            self.error(location, "must be a valid calendar date")
            return None
        if parsed.isoformat() != value:
            self.error(location, "must use canonical YYYY-MM-DD form")
            return None
        return value

    def _https_url(self, value: Any, location: str) -> str | None:
        text = self._string(value, location)
        if text is None:
            return None
        parsed = urlsplit(text)
        if parsed.scheme != "https" or not parsed.netloc or parsed.hostname is None:
            self.error(location, "must be an absolute HTTPS URL")
            return None
        if parsed.username is not None or parsed.password is not None:
            self.error(location, "must not contain embedded credentials")
            return None
        if any(char.isspace() for char in text):
            self.error(location, "must not contain whitespace")
            return None
        return text

    @staticmethod
    def _valid_review_reference(value: str) -> bool:
        if value.startswith("https://"):
            parsed = urlsplit(value)
            return parsed.hostname is not None and parsed.username is None and parsed.password is None
        return re.fullmatch(r"(?:[A-Z][A-Z0-9]+-\d+|#[1-9][0-9]*|[A-Za-z0-9][A-Za-z0-9._:/-]{2,})", value) is not None


def validate_registry(registry_path: Path) -> list[str]:
    """Return deterministic validation errors for ``registry_path``."""

    return RegistryValidator(registry_path).validate()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "registry",
        nargs="?",
        default="governance/external-semantic-sources.json",
        type=Path,
        help="path to the registry JSON",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_registry(args.registry)
    if errors:
        print("external semantic-source registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"external semantic-source registry valid: {args.registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
