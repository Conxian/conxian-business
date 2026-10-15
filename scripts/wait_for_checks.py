#!/usr/bin/env python3
"""Check every current check-run/status on one immutable PR head, fail closed.

Exit 0: checks satisfied; 1: failed check; 2: pending at timeout;
3: invalid/unavailable evidence, draft/closed PR or changed head.
Skipped/neutral runs are reported separately and cannot alone establish success.
Uses gh api --paginate --slurp (https://cli.github.com/manual/gh_api).
The caller must separately enforce reviews, release policy and an atomic merge
head lease (gh pr merge --match-head-commit SHA / REST sha).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

SHA = re.compile(r"[0-9a-f]{40}")


class EvidenceError(Exception):
    """Evidence is missing, malformed, inaccessible or changed."""


def api(endpoint: str, deadline: float, paginate: bool = False):
    command = ["gh", "api", "--hostname", "github.com", "--method", "GET", endpoint]
    if paginate:
        command += ["--paginate", "--slurp"]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=False,
            timeout=max(0.1, min(30.0, deadline - time.monotonic())),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise EvidenceError("GitHub CLI unavailable or request timed out") from exc
    if result.returncode:
        # Do not echo CLI stderr: it may contain credential/proxy context.
        raise EvidenceError(f"GitHub API retrieval failed (exit {result.returncode})")
    try:
        return json.loads(result.stdout)
    except (ValueError, TypeError) as exc:
        raise EvidenceError("GitHub API returned malformed JSON") from exc


def pull_head(repo: str, number: int, deadline: float) -> str:
    pull = api(f"repos/{repo}/pulls/{number}", deadline)
    if not isinstance(pull, dict) or pull.get("state") != "open" or pull.get("draft") is not False:
        raise EvidenceError("PR is not an open, ready-for-review candidate")
    sha = pull.get("head", {}).get("sha") if isinstance(pull.get("head"), dict) else None
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        raise EvidenceError("PR head SHA missing or malformed")
    return sha


def check_snapshot(repo: str, sha: str, deadline: float) -> tuple[int, int, int, int]:
    """Return successful, non-blocking, pending, failed counts."""
    pages = api(f"repos/{repo}/commits/{sha}/check-runs?filter=latest&per_page=100", deadline, True)
    if not isinstance(pages, list) or not pages:
        raise EvidenceError("Missing check-run pages")
    runs = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("check_runs"), list):
            raise EvidenceError("Malformed check-run page")
        total = page.get("total_count")
        if type(total) is not int or total < 0:
            raise EvidenceError("Missing check-run total")
        runs.extend(page["check_runs"])
    if any(p["total_count"] != len(runs) for p in pages):
        raise EvidenceError("Incomplete or changing check-run pagination; retry")

    successful = nonblocking = pending = failed = 0
    for run in runs:
        if not isinstance(run, dict) or run.get("head_sha") != sha or not run.get("name"):
            raise EvidenceError("Unbound or malformed check run")
        status, conclusion = run.get("status"), run.get("conclusion")
        if status in {"queued", "in_progress", "pending", "waiting", "requested"}:
            if conclusion is not None:
                raise EvidenceError("Inconsistent pending check run")
            pending += 1
        elif status == "completed":
            if conclusion == "success":
                successful += 1
            elif conclusion in {"neutral", "skipped"}:
                nonblocking += 1
            elif conclusion in {"failure", "cancelled", "timed_out", "action_required", "stale", "startup_failure"}:
                failed += 1
            else:
                raise EvidenceError("Unknown completed check conclusion")
        else:
            raise EvidenceError("Unknown check status")

    pages = api(f"repos/{repo}/commits/{sha}/statuses?per_page=100", deadline, True)
    if not isinstance(pages, list) or not pages or any(not isinstance(p, list) for p in pages):
        raise EvidenceError("Malformed commit-status pages")
    # REST returns newest first; compare IDs so a second page cannot overwrite
    # the current status with an old failure/success for the same context.
    latest = {}
    for page in pages:
        for item in page:
            if (not isinstance(item, dict) or not isinstance(item.get("context"), str)
                    or not item["context"] or type(item.get("id")) is not int):
                raise EvidenceError("Malformed commit status")
            if item["context"] not in latest or item["id"] > latest[item["context"]]["id"]:
                latest[item["context"]] = item
    for item in latest.values():
        state = item.get("state")
        if state == "success":
            successful += 1
        elif state == "pending":
            pending += 1
        elif state in {"failure", "error"}:
            failed += 1
        else:
            raise EvidenceError("Unknown commit-status state")
    if not runs and not latest:
        raise EvidenceError("No checks or commit statuses; no successful evidence")
    if not successful and not pending and not failed:
        raise EvidenceError("Only skipped/neutral checks; no successful evidence")
    return successful, nonblocking, pending, failed


def wait(repo: str, number: int, timeout: float, poll: float, expected: str | None) -> int:
    deadline = time.monotonic() + timeout
    sha = pull_head(repo, number, deadline)
    if expected is not None and sha != expected:
        raise EvidenceError("PR head differs from expected SHA")
    while True:
        if pull_head(repo, number, deadline) != sha:
            raise EvidenceError("PR head moved; inspect the new candidate")
        successful, nonblocking, pending, failed = check_snapshot(repo, sha, deadline)
        if pull_head(repo, number, deadline) != sha:
            raise EvidenceError("PR head moved while checks were read")
        if failed:
            print(f"wait_for_checks: {repo}#{number} head={sha}: {failed} failed; do not merge", file=sys.stderr)
            return 1
        if not pending:
            print(f"wait_for_checks: {repo}#{number} CHECKS SATISFIED head={sha} ({successful} successful, {nonblocking} skipped/neutral)")
            print("Merge must match this head SHA; review and release approval remain separate.")
            return 0
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            print(f"wait_for_checks: {pending} pending at timeout; do not merge", file=sys.stderr)
            return 2
        print(f"wait_for_checks: head={sha}: {pending} pending", flush=True)
        time.sleep(min(poll, remaining))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo")
    parser.add_argument("pr", type=int)
    parser.add_argument("timeout", type=float, nargs="?", default=2400)
    parser.add_argument("poll", type=float, nargs="?", default=30)
    parser.add_argument("expected_head_sha", nargs="?")
    args = parser.parse_args(argv)
    if (not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo)
            or args.pr < 1 or not 0 < args.timeout <= 86400 or not 0 < args.poll <= 60
            or args.expected_head_sha is not None and not SHA.fullmatch(args.expected_head_sha)):
        parser.error("Invalid repo, PR, timeout, poll or expected SHA")
    try:
        return wait(args.repo, args.pr, args.timeout, args.poll, args.expected_head_sha)
    except EvidenceError as exc:
        print(f"wait_for_checks: UNVERIFIED: {exc}; do not merge", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
