#!/usr/bin/env python3
"""Detect toolchain drift (Node / Rust / pnpm) across the Conxian org.

The *detector* half of the Phase 3 drift→PR→merge engine. It searches the org for
stale base-image / manifest versions and reports every actionable hit (Dockerfiles,
CI configs, package.json, Makefile, docker-compose). Docs are ignored.

Required environment (secret auto-injected when referenced on the command line):
  GITHUB_TOKEN   GitHub API token (read scope is enough)

Usage (from conxian-business root):
  GITHUB_TOKEN="$GITHUB_TOKEN" python3 scripts/verify_toolchain_drift.py

Exit code is non-zero when drift is found.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

# stale pattern -> expected replacement (org standard: Node 24, Rust 1.98.1, pnpm 10.28)
STALE = {
    "node:22": "node:24",
    "node:20": "node:24",
    "rust:1.96": "rust:1.98.1",
    "rust:1.97": "rust:1.98.1",
    "pnpm@9": "pnpm@10.28",
}

# only report actionable files (skip docs/audit + release notes)
IGNORE_FRAGMENTS = ("docs/", "REMEDIATION_LOG", "CHANGELOG", ".md")


def _search(pattern: str, token: str) -> list[tuple[str, str]]:
    query = f'org:Conxian "{pattern}"'
    url = "https://api.github.com/search/code?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "conxian-drift-audit",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    out = []
    for item in data.get("items", []):
        repo = item.get("repository", {}).get("full_name", "")
        path = item.get("path", "")
        if repo and path and not any(frag in path for frag in IGNORE_FRAGMENTS):
            out.append((repo, path))
    return out


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT_KEY")
    if not token:
        print("GITHUB_TOKEN not set — cannot search for toolchain drift.")
        return 0

    findings: list[str] = []
    for pattern, expected in STALE.items():
        for repo, path in _search(pattern, token):
            findings.append(f"{repo} / {path}: {pattern} → {expected}")

    if findings:
        print("TOOLCHAIN DRIFT:")
        for f in findings:
            print(f"  - {f}")
        return 1

    print("No toolchain drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
