#!/usr/bin/env python3
"""Verify checked-in CON-1571 controls without overstating live GitHub settings."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from branch_promotion_policy import BOOTSTRAP_EXCEPTION


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DOCS = (
    ROOT / "openspec/specs/git-management/spec.md",
    ROOT / "docs/BRANCH_AND_PROMOTION_STANDARD.md",
    ROOT / "docs/BRANCHING_AND_PROMOTION_POLICY.md",
    ROOT / "docs/PROMOTION_CHECKLISTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "GOVERNANCE.md",
    ROOT / ".github/PULL_REQUEST_TEMPLATE.md",
    ROOT / ".github/RELEASE_HYGIENE.md",
)
POLICY_WORKFLOW = ROOT / ".github/workflows/branch-promotion-policy.yml"
TRUSTED_POLICY_REF = "ref: ${{ github.event.repository.default_branch }}"
FORBIDDEN_POLICY_REFS = (
    "merge_commit_sha",
    "github.event.pull_request.head.sha",
    "github.event.pull_request.head.ref",
    "github.head_ref",
)


import shutil

def _run(*args: str) -> subprocess.CompletedProcess[str]:
    if not shutil.which(args[0]):
        return subprocess.CompletedProcess(args=args, returncode=127, stdout='', stderr='binary not found')
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def verify_static(*, allow_unkeyed_bootstrap: bool) -> list[str]:
    errors: list[str] = []

    for path in CANONICAL_DOCS:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not re.search(
                r"\bdev\b[^.]{0,80}\b(?:GitHub\s+)?default branch\b",
                line,
                re.IGNORECASE,
            ):
                continue
            if re.search(r"\b(?:never|not|must not|isn't|is not)\b", line, re.IGNORECASE):
                continue
            errors.append(f"{path.relative_to(ROOT)} calls dev the GitHub default branch")
        if re.search(r"\bdefault (?:development|integration) branch\b", text, re.IGNORECASE):
            errors.append(f"{path.relative_to(ROOT)} uses ambiguous default-branch language for dev")

    standard = (ROOT / "docs/BRANCH_AND_PROMOTION_STANDARD.md").read_text(encoding="utf-8")
    required_standard_phrases = (
        "`main` is the GitHub default branch and the production branch",
        "`dev` is the non-production integration branch",
        "`staged` is the candidate branch",
        "administrator-verified",
    )
    for phrase in required_standard_phrases:
        if phrase not in standard:
            errors.append(f"operational standard is missing required phrase: {phrase}")

    workflow = POLICY_WORKFLOW.read_text(encoding="utf-8")
    for token in (
        "pull_request_target:",
        "contents: read",
        "pull-requests: read",
        TRUSTED_POLICY_REF,
        "fetch-depth: 1",
        "persist-credentials: false",
        "scripts/branch_promotion_policy.py",
        "opened, reopened, synchronize, edited, ready_for_review, converted_to_draft",
        "Enforce branch promotion rules",
    ):
        if token not in workflow:
            errors.append(f"branch policy workflow is missing: {token}")
    if "startsWith('promotion/')" in workflow or "promotion/*" in workflow:
        errors.append("branch policy workflow contains a broad promotion wildcard")
    if re.search(r"^\s+pull_request:\s*$", workflow, re.MULTILINE):
        errors.append("branch policy workflow uses pull_request instead of pull_request_target")
    for token in FORBIDDEN_POLICY_REFS:
        if token in workflow:
            errors.append(f"branch policy workflow references PR-controlled checkout data: {token}")
    if "${{ github.event.pull_request" in workflow:
        errors.append("branch policy workflow interpolates pull-request data into workflow commands")

    run_commands = re.findall(r"^\s+run:\s*(.+)$", workflow, re.MULTILINE)
    trusted_command = 'python3 scripts/branch_promotion_policy.py --event-path "$GITHUB_EVENT_PATH"'
    if run_commands != [trusted_command]:
        errors.append(
            "branch policy workflow must execute only the trusted default-branch policy "
            "against GITHUB_EVENT_PATH"
        )

    action_uses = re.findall(r"^\s+uses:\s*(\S+)", workflow, re.MULTILINE)
    if len(action_uses) != 1 or not action_uses[0].startswith("actions/checkout@"):
        errors.append("branch policy workflow may use only the pinned checkout action")

    auto = (ROOT / ".github/workflows/auto-promotion.yml").read_text(encoding="utf-8")
    for token in (
        "source_sha",
        "target_sha",
        "commit_window",
        "promotion/${SOURCE}-to-${TARGET}-${SOURCE_SHA}",
        "concurrency:",
        "manual promotion PR",
    ):
        if token not in auto:
            errors.append(f"auto-promotion workflow is missing: {token}")
    if "git push --force " in auto or "git push -f " in auto:
        errors.append("auto-promotion workflow uses a bare force push")

    if BOOTSTRAP_EXCEPTION.pr_number <= 0 and not allow_unkeyed_bootstrap:
        errors.append("finite bootstrap exception is not keyed to the draft PR number")

    return errors


def report_live_state() -> None:
    """Report observation separately; never convert it into a verification pass."""

    repo = _run("gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
    if repo.returncode != 0 or not repo.stdout.strip():
        print("Live branch protections: UNVERIFIED/BLOCKED (repository metadata inaccessible).")
        return

    inaccessible: list[str] = []
    observed: list[str] = []
    for branch in ("main", "staged", "dev"):
        result = _run("gh", "api", f"repos/{repo.stdout.strip()}/branches/{branch}/protection")
        if result.returncode != 0:
            inaccessible.append(branch)
        else:
            observed.append(branch)

    if inaccessible:
        print(
            "Live branch protections: UNVERIFIED/BLOCKED "
            f"(admin protection state inaccessible for: {', '.join(inaccessible)})."
        )
        return

    print(
        "Live branch protections: OBSERVED BUT NOT ADMINISTRATOR-VERIFIED "
        f"(read response available for: {', '.join(observed)}; no pass claim recorded)."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-unkeyed-bootstrap",
        action="store_true",
        help="stage-one only: allow PR number 0 before the draft PR exists",
    )
    args = parser.parse_args()

    errors = verify_static(allow_unkeyed_bootstrap=args.allow_unkeyed_bootstrap)
    if errors:
        print("Promotion controls static verification: FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        report_live_state()
        return 1

    print("Promotion controls static verification: OK")
    report_live_state()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
