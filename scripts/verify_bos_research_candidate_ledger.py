#!/usr/bin/env python3
"""Validate the public-safe BOS research candidate ledger."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "docs/bos_research_candidate_ledger.json"
SCHEMA_VERSION = "1.0.0"
RUBRIC = (
    ("governance-risk-leverage", 25),
    ("portfolio-reuse-repeatability", 20),
    ("evidence-execution-readiness", 15),
    ("dependency-unblocking-value", 15),
    ("scope-containment-non-duplication", 15),
    ("autonomous-progress-without-owner-decision", 10),
)
RUBRIC_IDS = tuple(item[0] for item in RUBRIC)
RUBRIC_CAPS = dict(RUBRIC)
DISPOSITIONS = {
    "selected-technical",
    "retained-under-owner",
    "selected-authority",
    "retained-deferred-owner-admin-evidence",
    "independent-narrow-remediation",
    "research-only-deferred",
}
UNSCORED_DISPOSITIONS = {
    "tracker-required-before-scoring",
    "retained-existing-owner",
}
GAP_CLASSES = {
    "governance",
    "dependency-security",
    "evidence",
    "ci-infrastructure",
    "formatting-hygiene",
    "maintenance",
    "licensing-admin",
    "workflow-drift",
    "implementation",
    "owner-tracker",
}
DATED_CANDIDATES = {
    "lib-conxian-core#227": (88, "selected-technical"),
    "conxian-nexus#169/pr#172": (86, "retained-under-owner"),
    "conxian-business#943": (84, "selected-authority"),
    "android-first-attestation-owner-chain": (82, "retained-under-owner"),
    "conxius-platform#854": (78, "retained-deferred-owner-admin-evidence"),
    "conxius-platform#1082": (76, "retained-under-owner"),
    "conxian-nexus#178": (69, "independent-narrow-remediation"),
    "conxian-gateway#228": (65, "retained-under-owner"),
    "conxian-gateway#189": (60, "research-only-deferred"),
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._/#-]*$")


class DuplicateKeyError(ValueError):
    """Raised when JSON contains a duplicate object key."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _is_https_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username


def _require_text(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")


def _require_urls(value: Any, path: str, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, list) or (not value and not allow_empty):
        errors.append(f"{path}: must be a {'possibly empty ' if allow_empty else 'non-empty '}array")
        return
    for index, url in enumerate(value):
        if not _is_https_url(url):
            errors.append(f"{path}[{index}]: must be an HTTPS URL")


def _validate_rubric(data: dict[str, Any], errors: list[str]) -> None:
    rubric = data.get("rubric")
    if not isinstance(rubric, list):
        errors.append("rubric: must be an array")
        return
    observed: list[tuple[Any, Any]] = []
    for index, dimension in enumerate(rubric):
        if not isinstance(dimension, dict):
            errors.append(f"rubric[{index}]: must be an object")
            continue
        observed.append((dimension.get("id"), dimension.get("cap")))
        _require_text(dimension.get("label"), f"rubric[{index}].label", errors)
    if tuple(observed) != RUBRIC:
        errors.append(
            "rubric: must contain the exact six ordered dimension IDs and caps: "
            + repr(RUBRIC)
        )


def _validate_candidate(candidate: Any, index: int, errors: list[str]) -> tuple[str | None, int | None]:
    path = f"candidates[{index}]"
    if not isinstance(candidate, dict):
        errors.append(f"{path}: must be an object")
        return None, None

    candidate_id = candidate.get("id")
    if not isinstance(candidate_id, str) or not ID_RE.fullmatch(candidate_id):
        errors.append(f"{path}.id: must be a stable lowercase candidate ID")
        candidate_id = None
    for field in ("title", "ownerRepository", "nextGate", "uncertainty", "nonClaim"):
        _require_text(candidate.get(field), f"{path}.{field}", errors)
    if candidate.get("scored") is not True:
        errors.append(f"{path}.scored: must be true")
    disposition = candidate.get("disposition")
    if disposition not in DISPOSITIONS:
        errors.append(f"{path}.disposition: invalid scored disposition {disposition!r}")
    _require_urls(candidate.get("trackers"), f"{path}.trackers", errors)
    _require_urls(candidate.get("sourceLinks"), f"{path}.sourceLinks", errors)

    gap_classes = candidate.get("gapClasses")
    if not isinstance(gap_classes, list) or not gap_classes:
        errors.append(f"{path}.gapClasses: must be a non-empty array")
    else:
        unknown = sorted(set(gap_classes) - GAP_CLASSES)
        if unknown:
            errors.append(f"{path}.gapClasses: invalid values {unknown}")

    scores = candidate.get("scores")
    computed_total = 0
    if not isinstance(scores, list):
        errors.append(f"{path}.scores: must be an array")
        return candidate_id, None
    observed_ids: list[Any] = []
    for score_index, score in enumerate(scores):
        score_path = f"{path}.scores[{score_index}]"
        if not isinstance(score, dict):
            errors.append(f"{score_path}: must be an object")
            continue
        dimension_id = score.get("dimensionId")
        observed_ids.append(dimension_id)
        value = score.get("score")
        cap = RUBRIC_CAPS.get(dimension_id)
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{score_path}.score: must be an integer")
        elif cap is None or not 0 <= value <= cap:
            errors.append(f"{score_path}.score: must be within the dimension cap")
        else:
            computed_total += value
        _require_text(score.get("rationale"), f"{score_path}.rationale", errors)
        _require_urls(score.get("provenance"), f"{score_path}.provenance", errors)
    if tuple(observed_ids) != RUBRIC_IDS:
        errors.append(f"{path}.scores: must use the exact six ordered rubric dimensions")

    declared_total = candidate.get("total")
    if not isinstance(declared_total, int) or isinstance(declared_total, bool):
        errors.append(f"{path}.total: must be an integer")
        return candidate_id, None
    if declared_total != computed_total:
        errors.append(
            f"{path}.total: declared {declared_total} does not equal computed {computed_total}"
        )
    return candidate_id, declared_total


def _validate_unscored_gap(gap: Any, index: int, errors: list[str]) -> str | None:
    path = f"unscoredGaps[{index}]"
    if not isinstance(gap, dict):
        errors.append(f"{path}: must be an object")
        return None
    gap_id = gap.get("id")
    if not isinstance(gap_id, str) or not ID_RE.fullmatch(gap_id):
        errors.append(f"{path}.id: must be a stable lowercase gap ID")
        gap_id = None
    for field in ("title", "ownerRepository", "nextGate", "uncertainty", "nonClaim"):
        _require_text(gap.get(field), f"{path}.{field}", errors)
    if gap.get("scored") is not False:
        errors.append(f"{path}.scored: must be false")
    if "scores" in gap or "total" in gap:
        errors.append(f"{path}: unscored gaps must not contain scores or totals")
    disposition = gap.get("disposition")
    if disposition not in UNSCORED_DISPOSITIONS:
        errors.append(f"{path}.disposition: invalid unscored disposition {disposition!r}")
    trackers = gap.get("trackers")
    _require_urls(trackers, f"{path}.trackers", errors, allow_empty=True)
    if disposition == "tracker-required-before-scoring" and trackers != []:
        errors.append(f"{path}.trackers: must be empty until a canonical tracker exists")
    if disposition == "retained-existing-owner" and not trackers:
        errors.append(f"{path}.trackers: existing-owner gaps require at least one tracker")
    _require_urls(gap.get("sourceLinks"), f"{path}.sourceLinks", errors)
    gap_classes = gap.get("gapClasses")
    if not isinstance(gap_classes, list) or not gap_classes:
        errors.append(f"{path}.gapClasses: must be a non-empty array")
    elif set(gap_classes) - GAP_CLASSES:
        errors.append(f"{path}.gapClasses: contains invalid values")
    return gap_id


def validate_ledger(path: Path = DEFAULT_LEDGER) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except FileNotFoundError:
        return [f"ledger not found: {path}"]
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        return [f"ledger JSON is invalid: {exc}"]
    if not isinstance(data, dict):
        return ["ledger: top-level value must be an object"]

    if data.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"schemaVersion: must equal {SCHEMA_VERSION}")
    ledger_date = data.get("ledgerDate")
    if not isinstance(ledger_date, str) or not DATE_RE.fullmatch(ledger_date):
        errors.append("ledgerDate: must use YYYY-MM-DD")
    if data.get("exhaustiveEcosystemAudit") is not False:
        errors.append("exhaustiveEcosystemAudit: must be false")
    for field in ("authorityIssue", "authorityPullRequest"):
        if not _is_https_url(data.get(field)):
            errors.append(f"{field}: must be an HTTPS URL")

    _validate_rubric(data, errors)

    candidates = data.get("candidates")
    candidate_ids: list[str] = []
    totals: dict[str, int] = {}
    dispositions: dict[str, Any] = {}
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidates: must be a non-empty array")
    else:
        for index, candidate in enumerate(candidates):
            candidate_id, total = _validate_candidate(candidate, index, errors)
            if candidate_id is not None:
                candidate_ids.append(candidate_id)
                dispositions[candidate_id] = candidate.get("disposition")
                if total is not None:
                    totals[candidate_id] = total
        if len(candidate_ids) != len(set(candidate_ids)):
            errors.append("candidates: candidate IDs must be unique")
        if set(candidate_ids) != set(DATED_CANDIDATES):
            errors.append("candidates: must preserve the exact 2026-07-28 scored candidate set")
        for candidate_id, (expected_total, expected_disposition) in DATED_CANDIDATES.items():
            if totals.get(candidate_id) != expected_total:
                errors.append(
                    f"candidates: {candidate_id} must preserve dated total {expected_total}"
                )
            if dispositions.get(candidate_id) != expected_disposition:
                errors.append(
                    f"candidates: {candidate_id} must preserve disposition "
                    f"{expected_disposition}"
                )

    unscored = data.get("unscoredGaps")
    gap_ids: list[str] = []
    if not isinstance(unscored, list):
        errors.append("unscoredGaps: must be an array")
    else:
        for index, gap in enumerate(unscored):
            gap_id = _validate_unscored_gap(gap, index, errors)
            if gap_id is not None:
                gap_ids.append(gap_id)
        if len(gap_ids) != len(set(gap_ids)):
            errors.append("unscoredGaps: gap IDs must be unique")
        if set(candidate_ids) & set(gap_ids):
            errors.append("candidate and unscored gap IDs must not overlap")

    selection = data.get("selection")
    if not isinstance(selection, dict):
        errors.append("selection: must be an object")
    else:
        authority_id = selection.get("selectedAuthorityId")
        technical_id = selection.get("selectedTechnicalCandidateId")
        if authority_id == technical_id:
            errors.append("selection: authority and technical candidate must remain distinct")
        if dispositions.get(authority_id) != "selected-authority":
            errors.append("selection.selectedAuthorityId: must identify the selected-authority row")
        if dispositions.get(technical_id) != "selected-technical":
            errors.append(
                "selection.selectedTechnicalCandidateId: must identify the selected-technical row"
            )
        if technical_id in totals and totals and totals[technical_id] != max(totals.values()):
            errors.append("selection: selected technical candidate must be a scored maximum")

    artifact = data.get("selectedTechnicalArtifact")
    if not isinstance(artifact, dict):
        errors.append("selectedTechnicalArtifact: must be an object")
    else:
        if artifact.get("candidateId") != (
            selection.get("selectedTechnicalCandidateId") if isinstance(selection, dict) else None
        ):
            errors.append("selectedTechnicalArtifact.candidateId: must match the technical selection")
        for field in ("tracker", "decisionIssue", "downstreamEvidence"):
            if not _is_https_url(artifact.get(field)):
                errors.append(f"selectedTechnicalArtifact.{field}: must be an HTTPS URL")
        _require_urls(
            artifact.get("pullRequests"),
            "selectedTechnicalArtifact.pullRequests",
            errors,
        )
        for field in ("comparisonBaseCommit", "headCommit"):
            value = artifact.get(field)
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
                errors.append(f"selectedTechnicalArtifact.{field}: must be a full commit SHA")
        for field in (
            "changeBoundary",
            "localEvidence",
            "hostedEvidence",
            "immediateDecision",
            "strategicDecision",
            "proofBoundary",
            "scopeBoundary",
            "releaseGates",
            "nonClaim",
        ):
            _require_text(artifact.get(field), f"selectedTechnicalArtifact.{field}", errors)
        if artifact.get("comparisonBaseCommit") != "60eee84d3279dc73c02376bf2fe8abbfda5a88ce":
            errors.append("selectedTechnicalArtifact: merged PR #229 base commit must be current")
        if artifact.get("headCommit") != "7edcae397383bd99a9b7a97703d6cab1507a7657":
            errors.append("selectedTechnicalArtifact: PR #231 head commit must be current")
        if artifact.get("pullRequests") != [
            "https://github.com/Conxian/lib-conxian-core/pull/229",
            "https://github.com/Conxian/lib-conxian-core/pull/231",
        ]:
            errors.append("selectedTechnicalArtifact.pullRequests: must preserve PR #229/#231 order")
        immediate = artifact.get("immediateDecision", "")
        strategic = artifact.get("strategicDecision", "")
        proof = artifact.get("proofBoundary", "")
        scope = artifact.get("scopeBoundary", "")
        if "default-features = false" not in immediate or "no networking or persistence" not in immediate:
            errors.append("selectedTechnicalArtifact.immediateDecision: must preserve the std-only Core boundary")
        if "transport-neutral" not in strategic or "outside Core" not in strategic:
            errors.append("selectedTechnicalArtifact.strategicDecision: must preserve the backend boundary")
        if "TLS authenticates transport" not in proof or "chain-proof validation" not in proof:
            errors.append("selectedTechnicalArtifact.proofBoundary: must preserve transport/proof semantics")
        if "does not establish production-complete universal blockchain support" not in scope:
            errors.append("selectedTechnicalArtifact.scopeBoundary: must preserve the universal-support non-claim")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_LEDGER)
    args = parser.parse_args(argv)
    errors = validate_ledger(args.path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Success: BOS research candidate ledger verified ({args.path}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
