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


def timestamp(value: Any) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timezone required")
    return result.astimezone(timezone.utc)


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
    if not isinstance(expected, list) or not expected or not isinstance(repos, list):
        return {"coverage_complete": False, "actions": [{"action": "COMPLETE_ORG_INVENTORY"}]}
    names = [r.get("name") for r in repos if isinstance(r, dict)]
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
        if repo.get("promotion_chain") is True:
            if not all(isinstance(refs.get(b), str) and SHA.fullmatch(refs[b]) for b in ("dev", "staged", "main")):
                add("REFRESH_BRANCH_HEADS", name)
                refs = {}
        for pr in repo["prs"]:
            number = pr.get("number")
            if type(number) is not int or (name, number) in processed:
                add("COMPLETE_REPOSITORY_PR_READ", name)
                continue
            processed.add((name, number))
            if not pr.get("next_action") or not pr.get("owner_issue"):
                add("RECORD_NEXT_ACTION_AND_OWNER", name, number)
            if pr.get("files_complete") is not True:
                add("READ_FULL_DIFF", name, number)
            if pr.get("protected_control_changes") and pr.get("separate_owner_workflow_request") is not True:
                add("SEPARATE_WORKFLOW_CHANGES_FROM_IMPLEMENTATION", name, number)
            match = CANDIDATE.fullmatch(pr.get("head_ref", ""))
            if match:
                lane, source = match.groups()
                source_branch, target = ("dev", "staged") if lane == "dev-to-staged" else ("staged", "main")
                if pr.get("head_sha") != source or pr.get("source_sha") != source:
                    add("REPAIR_MUTATED_IMMUTABLE_CANDIDATE", name, number)
                if pr.get("target_base_sha") != pr.get("base_sha") or pr.get("base_sha") != refs.get(target):
                    add("REPLACE_STALE_TARGET_CANDIDATE", name, number)
                if source != refs.get(source_branch):
                    add("VERIFY_REPLACEMENT_AND_RETENTION", name, number)
            if pr.get("checks_complete") is not True or pr.get("statuses_complete") is not True or not pr.get("checks"):
                add("REFRESH_CHECK_EVIDENCE", name, number)
            else:
                for check in pr["checks"]:
                    if check.get("head_sha") != pr.get("head_sha"):
                        add("REFRESH_CHECK_EVIDENCE", name, number)
                    elif check.get("status") != "completed":
                        add("FOLLOW_PENDING_CHECKS", name, number)
                    elif check.get("conclusion") not in {"success", "skipped", "neutral"}:
                        add("REMEDIATE_FAILED_CHECKS", name, number)
                # Neutral/skipped are preserved as observations, never called passes.
                if not any(c.get("conclusion") == "success" for c in pr["checks"]):
                    add("OBTAIN_APPLICABLE_SUCCESSFUL_CHECKS", name, number)
                for status in pr.get("statuses", []):
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
            if not any(p.get("base_ref") == target and p.get("head_sha") == refs[source] for p in repo["prs"]):
                if target == "main":
                    soak = repo.get("soak_satisfied")
                    add("GENERATE_CURRENT_MAIN_CANDIDATE" if soak is True else "FOLLOW_SOAK_AND_PREPARE_ACCEPTANCE", name)
                else:
                    add("GENERATE_CURRENT_STAGED_CANDIDATE", name)
    incomplete = {"COMPLETE_ORG_INVENTORY", "REFRESH_SNAPSHOT", "COMPLETE_REPOSITORY_PR_READ", "REFRESH_BRANCH_HEADS", "READ_FULL_DIFF", "REFRESH_CHECK_EVIDENCE", "REFRESH_REVIEW_EVIDENCE"}
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
