#!/usr/bin/env python3
"""Plan delivery follow-through from a complete, source-bound connector snapshot.

Read-only: never merges, approves, deletes, or changes repository controls.
The result is a work plan, not a substitute for wait_for_checks or release policy.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

SHA = re.compile(r"[0-9a-f]{40}")
CANDIDATE = re.compile(r"promotion/(dev-to-staged|staged-to-main)-([0-9a-f]{40})")
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")


def is_sha(value: Any) -> bool:
    return isinstance(value, str) and SHA.fullmatch(value) is not None


def records(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, dict) for item in value)


def timestamp(value: Any) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timezone required")
    return result.astimezone(timezone.utc)


def dependency_preflight(pr: dict[str, Any]) -> bool:
    """Require an exact-source frozen/locked install observation, not green CI alone."""
    evidence = pr.get("dependency_validation")
    if not isinstance(evidence, dict) or evidence.get("head_sha") != pr.get("head_sha"):
        return False
    if not is_sha(evidence.get("head_sha")):
        return False
    changed = evidence.get("dependency_files_changed")
    if changed is False:
        return evidence.get("result") == "not_applicable" and bool(
            isinstance(evidence.get("rationale"), str) and evidence["rationale"].strip())
    return (changed is True and evidence.get("result") == "success"
            and evidence.get("frozen_or_locked") is True
            and isinstance(evidence.get("evidence_ref"), str)
            and bool(evidence["evidence_ref"].strip()))


def deployment_binding(repo: dict[str, Any], now: datetime) -> bool:
    """Compare intended release targets with fresh terminal provider observations.

    These are collector assertions, not signed provenance or runtime acceptance.
    Never emit target identifiers or raw observations in the public action plan.
    """
    targets, observed = repo.get("deployment_targets"), repo.get("deployment_observations")
    if (not records(targets) or not targets or not records(observed)
            or repo.get("deployments_complete") is not True):
        return False
    refs = repo.get("refs")
    main = refs.get("main") if isinstance(refs, dict) else None
    if not is_sha(main):
        return False
    keys = ("provider", "scope", "service", "environment")

    def identity(item):
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in keys):
            return None
        return tuple(item[k] for k in keys)

    intended, actual = {}, {}
    for items, index in ((targets, intended), (observed, actual)):
        for item in items:
            key = identity(item)
            if key is None or key in index:
                return False
            digest = item.get("artifact_digest")
            if (item.get("source_sha") != main or not isinstance(digest, str)
                    or not DIGEST.fullmatch(digest)):
                return False
            index[key] = item
    if set(intended) != set(actual):
        return False
    for key, target in intended.items():
        observation = actual[key]
        try:
            age = (now - timestamp(observation.get("observed_at"))).total_seconds()
        except (TypeError, ValueError, AttributeError):
            return False
        if (age < 0 or age > 3600 or observation.get("state") != "live"
                or observation.get("artifact_digest") != target["artifact_digest"]
                or not isinstance(observation.get("deployment_id"), str)
                or not observation["deployment_id"].strip()):
            return False
    return True


def audit(snapshot: dict[str, Any], now: datetime) -> dict[str, Any]:
    actions: list[dict[str, Any]] = []

    def add(code: str, repo: str | None = None, pr: int | None = None) -> None:
        item: dict[str, Any] = {"action": code}
        if repo is not None:
            item["repository"] = repo
        if pr is not None:
            item["pr"] = pr
        if item not in actions:
            actions.append(item)

    try:
        age = (now - timestamp(snapshot.get("captured_at"))).total_seconds()
    except (TypeError, ValueError, AttributeError):
        age = -1
    if age < 0 or age > 3600:
        add("REFRESH_SNAPSHOT")
    if snapshot.get("inventory_complete") is not True:
        add("COMPLETE_ORG_INVENTORY")
    expected = snapshot.get("expected_repositories", [])
    repos = snapshot.get("repositories", [])
    if (not isinstance(expected, list) or not expected
            or not all(isinstance(name, str) and name.strip() for name in expected)
            or not isinstance(repos, list)):
        return {"coverage_complete": False, "actions": [{"action": "COMPLETE_ORG_INVENTORY"}]}
    names = [r["name"] for r in repos
             if isinstance(r, dict) and isinstance(r.get("name"), str) and r["name"].strip()]
    if (len(names) != len(repos) or len(set(names)) != len(names)
            or len(set(expected)) != len(expected) or set(names) != set(expected)):
        add("COMPLETE_ORG_INVENTORY")
    if snapshot.get("delivery_loop_enabled") is not True:
        add("RESTORE_OWNER_AUTHORIZED_DELIVERY_LOOP")
    processed: set[tuple[str, int]] = set()
    for repo in repos:
        if not isinstance(repo, dict) or not isinstance(repo.get("name"), str):
            continue
        name = repo["name"]
        if repo.get("prs_complete") is not True or not isinstance(repo.get("prs"), list):
            add("COMPLETE_REPOSITORY_PR_READ", name)
            continue
        refs = repo.get("refs", {})
        if not isinstance(refs, dict):
            refs = {}
        if repo.get("promotion_chain") is True:
            if not all(is_sha(refs.get(b)) for b in ("dev", "staged", "main")):
                add("REFRESH_BRANCH_HEADS", name)
                refs = {}
        for pr in repo["prs"]:
            if not isinstance(pr, dict):
                add("COMPLETE_REPOSITORY_PR_READ", name)
                continue
            number = pr.get("number")
            if type(number) is not int or number <= 0 or (name, number) in processed:
                add("COMPLETE_REPOSITORY_PR_READ", name)
                continue
            processed.add((name, number))
            base_ref, head_ref = pr.get("base_ref"), pr.get("head_ref")
            if (not is_sha(pr.get("head_sha")) or not is_sha(pr.get("base_sha"))
                    or not isinstance(head_ref, str) or not head_ref
                    or not isinstance(base_ref, str) or not base_ref
                    or pr.get("base_sha") != refs.get(base_ref)):
                add("REFRESH_PR_IDENTITY", name, number)
            if not pr.get("next_action") or not pr.get("owner_issue"):
                add("RECORD_NEXT_ACTION_AND_OWNER", name, number)
            if pr.get("files_complete") is not True:
                add("READ_FULL_DIFF", name, number)
            if pr.get("protected_control_changes") and pr.get("separate_owner_workflow_request") is not True:
                add("SEPARATE_WORKFLOW_CHANGES_FROM_IMPLEMENTATION", name, number)
            match = CANDIDATE.fullmatch(head_ref) if isinstance(head_ref, str) else None
            if isinstance(head_ref, str) and head_ref.startswith("promotion/") and not match:
                add("REPAIR_PROMOTION_ROUTE", name, number)
            if match:
                if not dependency_preflight(pr):
                    add("COLLECT_EXACT_DEPENDENCY_VALIDATION", name, number)
                lane, source = match.groups()
                source_branch, target = ("dev", "staged") if lane == "dev-to-staged" else ("staged", "main")
                if base_ref != target or repo.get("promotion_chain") is not True:
                    add("REPAIR_PROMOTION_ROUTE", name, number)
                if pr.get("head_sha") != source or pr.get("source_sha") != source:
                    add("REPAIR_MUTATED_IMMUTABLE_CANDIDATE", name, number)
                if pr.get("target_base_sha") != pr.get("base_sha") or pr.get("base_sha") != refs.get(target):
                    add("REPLACE_STALE_TARGET_CANDIDATE", name, number)
                if source != refs.get(source_branch):
                    add("VERIFY_REPLACEMENT_AND_RETENTION", name, number)
            checks, statuses = pr.get("checks"), pr.get("statuses")
            if pr.get("checks_complete") is not True or not records(checks) or not checks:
                add("REFRESH_CHECK_EVIDENCE", name, number)
            else:
                for check in checks:
                    if check.get("head_sha") != pr.get("head_sha"):
                        add("REFRESH_CHECK_EVIDENCE", name, number)
                    elif check.get("status") != "completed":
                        add("FOLLOW_PENDING_CHECKS", name, number)
                    elif check.get("conclusion") not in {"success", "skipped", "neutral"}:
                        add("REMEDIATE_FAILED_CHECKS", name, number)
                # Neutral/skipped are preserved as observations, never called passes.
                if not any(c.get("conclusion") == "success" for c in checks):
                    add("OBTAIN_APPLICABLE_SUCCESSFUL_CHECKS", name, number)
            if pr.get("statuses_complete") is not True or not records(statuses):
                add("REFRESH_CHECK_EVIDENCE", name, number)
            else:
                for status in statuses:
                    if status.get("head_sha") != pr.get("head_sha") or status.get("state") != "success":
                        add("RESOLVE_COMMIT_STATUS", name, number)
            if pr.get("reviews_complete") is not True:
                add("REFRESH_REVIEW_EVIDENCE", name, number)
            if pr.get("review_gate") != "satisfied":
                add("COMPLETE_REQUIRED_REVIEW", name, number)
            if pr.get("base_ref") == "main" and repo.get("promotion_chain") is True:
                if repo.get("soak_satisfied") is not True:
                    add("FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", name, number)
                if pr.get("acceptance_head_sha") != pr.get("head_sha") or pr.get("main_acceptance") != "accepted":
                    add("COMPLETE_EXACT_MAIN_ACCEPTANCE", name, number)
        # Services without a promotion chain still need a source-bound deploy.
        if repo.get("deployment_required") is True:
            if not deployment_binding(repo, now):
                add("VERIFY_DEPLOYMENT_ARTIFACT_BINDING", name)
            main_sha = refs.get("main")
            if not isinstance(main_sha, str) or not SHA.fullmatch(main_sha):
                add("REFRESH_BRANCH_HEADS", name)
            elif repo.get("deployment_source_sha") != main_sha:
                add("VERIFY_OR_REMEDIATE_DEPLOYED_SOURCE", name)
        if repo.get("promotion_chain") is not True or not refs:
            continue
        # A merged dev PR is still unfinished while its content is absent on main.
        for source, target, lineage in (("dev", "staged", "staged_in_dev"), ("staged", "main", "main_in_staged")):
            if refs[source] == refs[target]:
                continue
            known = repo.get("lineage", {}).get(lineage)
            if known is not True:
                add("RECONCILE_ANCESTRY" if known is False else "VERIFY_ANCESTRY", name)
                continue
            if repo.get("trees", {}).get(source) == repo.get("trees", {}).get(target) and repo.get("trees", {}).get(source):
                continue
            if not any(isinstance(p, dict) and p.get("base_ref") == target
                       and p.get("head_sha") == refs[source] for p in repo["prs"]):
                if target == "main":
                    soak = repo.get("soak_satisfied")
                    add("GENERATE_CURRENT_MAIN_CANDIDATE" if soak is True else "FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", name)
                else:
                    add("GENERATE_CURRENT_STAGED_CANDIDATE", name)
    incomplete = {"COMPLETE_ORG_INVENTORY", "REFRESH_SNAPSHOT", "COMPLETE_REPOSITORY_PR_READ", "REFRESH_BRANCH_HEADS", "REFRESH_PR_IDENTITY", "READ_FULL_DIFF", "REFRESH_CHECK_EVIDENCE", "REFRESH_REVIEW_EVIDENCE"}
    return {"coverage_complete": not any(a["action"] in incomplete for a in actions),
            "repositories_read": len(names), "prs_read": len(processed), "actions": actions}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.snapshot.read_text()), datetime.now(timezone.utc))
    except (ValueError, TypeError, KeyError, OSError, AttributeError):
        print(json.dumps({"coverage_complete": False, "actions": [{"action": "REPAIR_INVALID_SNAPSHOT"}]}))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result["actions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
