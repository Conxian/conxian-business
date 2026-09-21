#!/usr/bin/env python3
"""Detect and reconcile branch divergence across the promotion chain.

Promotion chain (forward): dev -> staged -> main.

Reverse drift happens when commits land directly on a higher branch without
going through the chain (e.g. direct-to-main `docs`/`chore`/`feat` merges, or
direct-to-staged merges). This script detects that drift and opens a
back-merge PR to re-sync the lower branch.

Resolution policy (learned from the 2026-09-20 org-wide reconciliation):
the higher branch is authoritative. On conflict, take the higher branch's
version and drop lower-branch-only files, so the result is an exact sync.

Forward-promotion artifacts (``PROMOTION:STAGED->MAIN`` / ``PROMOTION:DEV->STAGED``
merge commits) are legitimate and are excluded from drift detection.

Usage:
    reconcile_branches.py --detect          # list drift plans as JSON
    reconcile_branches.py --reconcile       # execute plans (open back-merge PRs)
    reconcile_branches.py --dry-run         # execute plans but do not push/open PRs

Requires ``gh`` CLI authenticated with ``GH_TOKEN`` and ``git`` in PATH.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass

ORG = os.environ.get("GITHUB_REPOSITORY_OWNER", "Conxian")

# Repos following the dev -> staged -> main chain. Repos with a single
# branch (e.g. conxian-org-site) are intentionally omitted.
PROMOTION_CHAIN_REPOS = [
    "conxius-wallet",
    "conxian-labs-site",
    "conxian-gateway",
    "lib-conxian-core",
    "conxius-platform",
    "conxian-nexus",
    "conxian-business",
    "conxius-enclave-sdk",
    "conxian_market",
    "conxian.github.io",
    ".github",
    ".github-private",
]

# Commit message markers for legitimate forward-promotion merge commits.
PROMOTION_MARKERS = (
    "PROMOTION:STAGED->MAIN",
    "PROMOTION:DEV->STAGED",
)


def _gh(*args: str) -> str:
    env = dict(os.environ)
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def _git(*args: str, cwd: str | None = None) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    return proc.stdout


def list_branches(repo: str) -> list[str]:
    data = json.loads(_gh("api", f"repos/{ORG}/{repo}/branches", "--paginate"))
    return [b["name"] for b in data]


def commits_ahead(repo: str, base: str, head: str) -> list[dict]:
    """Commits on ``head`` not reachable from ``base``."""
    data = json.loads(_gh("api", f"repos/{ORG}/{repo}/compare/{base}...{head}"))
    return data.get("commits", [])


def is_promotion_artifact(commit: dict) -> bool:
    msg = commit.get("commit", {}).get("message", "")
    return any(m in msg for m in PROMOTION_MARKERS)


@dataclass
class ReconcilePlan:
    repo: str
    source: str  # higher, authoritative branch
    target: str  # lower branch to re-sync
    n_drift: int  # non-promotion commits to re-sync

    def as_dict(self) -> dict:
        return {
            "repo": self.repo,
            "source": self.source,
            "target": self.target,
            "drift_commits": self.n_drift,
        }


def detect() -> list[ReconcilePlan]:
    plans: list[ReconcilePlan] = []
    for repo in PROMOTION_CHAIN_REPOS:
        branches = list_branches(repo)
        if "dev" not in branches or "staged" not in branches:
            continue

        # main -> staged: only non-promotion drift matters.
        if "main" in branches:
            ahead = commits_ahead(repo, "staged", "main")
            drift = [c for c in ahead if not is_promotion_artifact(c)]
            if drift:
                plans.append(ReconcilePlan(repo, "main", "staged", len(drift)))

        # staged -> dev: any staged-side commits need downward re-sync.
        ahead = commits_ahead(repo, "dev", "staged")
        if ahead:
            plans.append(ReconcilePlan(repo, "staged", "dev", len(ahead)))

    return plans


def _clone(repo: str, workdir: str) -> str:
    url = f"https://x-access-token:{os.environ['GH_TOKEN']}@github.com/{ORG}/{repo}.git"
    subprocess.run(
        ["git", "clone", "--quiet", url, repo],
        check=True, capture_output=True, text=True, cwd=workdir,
    )
    return os.path.join(workdir, repo)


def reconcile(plan: ReconcilePlan, dry_run: bool) -> dict:
    """Sync ``target`` to ``source`` (exact tree match) and open a back-merge PR."""
    result = plan.as_dict()
    result["status"] = "skipped"
    branch_name = f"backmerge/{plan.source}-to-{plan.target}"

    with tempfile.TemporaryDirectory(prefix="reconcile-") as tmp:
        repo_dir = _clone(plan.repo, tmp)
        _git("checkout", "-q", "-b", branch_name, f"origin/{plan.target}", cwd=repo_dir)

        # Deterministic exact sync: replace the target tree with the source
        # tree. Lockfiles and manifests are taken wholesale from the
        # authoritative branch; no per-file merge is attempted.
        subprocess.run(
            ["git", "rm", "-rfq", "."], check=True, capture_output=True, text=True, cwd=repo_dir,
        )
        subprocess.run(
            ["git", "checkout", f"origin/{plan.source}", "--", "."],
            check=True, capture_output=True, text=True, cwd=repo_dir,
        )
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True, text=True, cwd=repo_dir)
        subprocess.run(
            ["git", "commit", "-m", f"chore: back-merge {plan.source} -> {plan.target} (downward re-sync)"],
            check=True, capture_output=True, text=True, cwd=repo_dir,
        )

        if dry_run:
            result["status"] = "dry_run"
            result["branch"] = branch_name
            return result

        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            check=True, capture_output=True, text=True, cwd=repo_dir,
        )

        title = f"chore: back-merge {plan.source} -> {plan.target} (downward re-sync)"
        body = (
            f"Automated back-merge to clear {plan.n_drift} drifted commit(s) "
            f"from `{plan.source}` into `{plan.target}`.\n\n"
            f"> Generated by the org-wide reconciliation workflow."
        )
        out = _gh(
            "pr", "create",
            "--repo", f"{ORG}/{plan.repo}",
            "--base", plan.target,
            "--head", branch_name,
            "--title", title,
            "--body", body,
        )
        result["status"] = "opened"
        result["pr_url"] = out.strip()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--detect", action="store_true", help="Print drift plans as JSON and exit")
    mode.add_argument("--reconcile", action="store_true", help="Execute plans and open back-merge PRs")
    mode.add_argument("--dry-run", action="store_true", help="Execute locally without pushing or opening PRs")
    args = parser.parse_args()

    plans = detect()

    if args.detect:
        json.dump([p.as_dict() for p in plans], sys.stdout, indent=2)
        print()
        return 0

    if not plans:
        print("No reverse drift detected across the promotion chain.")
        return 0

    results = [reconcile(p, dry_run=args.dry_run) for p in plans]
    json.dump(results, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
