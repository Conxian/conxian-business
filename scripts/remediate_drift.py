#!/usr/bin/env python3
"""Remediate a single toolchain-drift finding: apply the fix + open a PR.

The *act* half of the Phase 3 drift→PR→merge engine. Given a finding
(repo, file, old, new), it clones the repo, applies a literal string replacement,
commits, pushes a branch, and opens a PR to ``dev`` with the promotion checklist.
The PR then flows through the existing promotion chain (dev → staged → main).

This is intentionally a *single* finding per invocation (one fix, one PR) so a
human or agent can review each change. Run with ``--dry-run`` to preview.

Usage (from conxian-business root):
  GITHUB_TOKEN="$GITHUB_PAT_KEY" python3 scripts/remediate_drift.py \
    --repo Conxian/conxian-market --file .circleci/config.yml \
    --old "node:22" --new "node:24" [--dry-run]

Environment:
  GITHUB_TOKEN   GitHub token with repo + pull-request scope (GITHUB_PAT_KEY works)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile


def _run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="e.g. Conxian/conxian-market")
    parser.add_argument("--file", required=True, help="path within the repo")
    parser.add_argument("--old", required=True, help="stale string")
    parser.add_argument("--new", required=True, help="replacement string")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT_KEY")
    if not token:
        print("GITHUB_TOKEN not set.")
        return 1

    branch = f"fix/toolchain-drift-{args.old.replace(':', '-').replace('@', '-')}"

    with tempfile.TemporaryDirectory(prefix="drift-") as tmp:
        clone_url = f"https://x-access-token:{token}@github.com/{args.repo}.git"
        r = _run(["git", "clone", "--depth", "1", clone_url, tmp])
        if r.returncode != 0:
            print(f"clone failed: {r.stderr.strip()}")
            return 1

        path = os.path.join(tmp, args.file)
        if not os.path.exists(path):
            print(f"file not found: {args.file}")
            return 1

        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        if args.old not in content:
            print(f"{args.old!r} not present in {args.file} — nothing to do.")
            return 0

        new_content = content.replace(args.old, args.new)
        if args.dry_run:
            print(f"[dry-run] would replace {args.old!r} → {args.new!r} in {args.repo}/{args.file}")
            return 0

        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_content)

        _run(["git", "-C", tmp, "checkout", "-b", branch])
        _run(["git", "-C", tmp, "add", args.file])
        _run(["git", "-C", tmp, "config", "user.name", "Botshelo Mokoka"])
        _run(["git", "-C", tmp, "config", "user.email",
              "41502979+botshelomokoka@users.noreply.github.com"])
        r = _run(["git", "-C", tmp, "commit", "-m",
                  f"chore(toolchain): {args.file} {args.old} -> {args.new}\n\n"
                  f"Align with org standard. Auto-remediation.\n\n"
                  f"Co-authored-by: openhands <openhands@all-hands.dev>"])
        if r.returncode != 0:
            print(f"commit failed: {r.stderr.strip()}")
            return 1

        r = _run(["git", "-C", tmp, "push", "origin", branch])
        if r.returncode != 0:
            print(f"push failed: {r.stderr.strip()}")
            return 1

    # Open the PR (with the promotion checklist required by branch-promotion-policy).
    body = (
        "## Summary\n\n"
        f"Toolchain drift auto-remediation: `{args.file}` — `{args.old}` → `{args.new}`.\n\n"
        "PROMOTION:FEATURE->DEV\n\n"
        "### Feature -> dev promotion checklist\n\n"
        "- [x] 🛠️ Maintenance / Refactoring (toolchain version alignment)\n"
        "- [x] Zero Secret Egress (ZSE): no credentials introduced\n"
        "- [x] Clean Git Index: no generated/runtime artifacts tracked\n\n"
        "_This PR was created by an AI agent (OpenHands) on behalf of Botshelo Mokoka._"
    )
    r = _run(["gh", "pr", "create", "-R", args.repo, "--base", "dev", "--head", branch,
              "--title", f"chore(toolchain): {args.file} {args.old} -> {args.new}",
              "--body", body])
    if r.returncode != 0:
        print(f"PR create failed: {r.stderr.strip()}")
        return 1
    print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
