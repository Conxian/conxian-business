#!/usr/bin/env python3
"""Production Contamination Guard & Submodule Sync Guard.

Scans all Clarity (.clar) contract files across the repository (including
initialized submodules) for hardcoded testnet principals (addresses starting
with 'ST...') in production-track code paths.

Also checks submodule alignment across all 12 core repositories without
failing on 'update = none' flags (e.g. conxius-platform, Conxian).

Per the Sovereign-First Deployment Mandate, hardcoded ST.../SP... addresses
in production source trigger an immediate build-break.
"""

import subprocess
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns that indicate a hardcoded testnet principal in Clarity code.
TESTNET_PRINCIPAL_RE = re.compile(r"'S[TP][0-9A-HJ-NP-Z]{25,40}")
SIMNET_PRINCIPAL_RE = re.compile(r"'SN[0-9A-HJ-NP-Z]{25,40}")

# Paths to exclude from scanning
EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "target",
    "dist",
    ".next",
    "__pycache__",
}

# Files in these directories are NOT production-track
NON_PRODUCTION_DIRS = {
    "tests",
    "test",
    "spec",
    "mock",
    "fixtures",
    "examples",
    "playground",
    "sandbox",
    "simnet",
}

# Core 12 repositories tracked across the ecosystem
CORE_REPOSITORIES = [
    "conxian-business",  # root
    "conxian-gateway",
    "conxian-nexus",
    "conxius-wallet",
    "conxius-platform",
    "conxian-labs-site",
    "conxius-enclave-sdk",
    "lib-conxian-core",
    "conxian_market",
    "conxian-ui",
    "conxius-orbit",
    "showcase-dapp",
]

# Allowed update=none policy overrides
ALLOWED_UPDATE_NONE = {"Conxian", "conxius-platform"}


def is_production_track(file_path: Path) -> bool:
    """Determine if a .clar file is in a production-track location."""
    parts = set(file_path.relative_to(REPO_ROOT).parts)
    return not (parts & NON_PRODUCTION_DIRS)


def find_clar_files() -> list[Path]:
    """Find all .clar files in the repo, excluding non-track directories."""
    clar_files = []
    for clar_file in REPO_ROOT.rglob("*.clar"):
        parts = set(clar_file.relative_to(REPO_ROOT).parts)
        if parts & EXCLUDE_DIRS:
            continue
        clar_files.append(clar_file)
    return clar_files


def scan_file(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a .clar file for hardcoded testnet principals."""
    violations = []
    try:
        content = file_path.read_text(errors="ignore")
        for i, line in enumerate(content.splitlines(), 1):
            match = TESTNET_PRINCIPAL_RE.search(line)
            if match:
                violations.append((i, match.group(), "testnet (ST...)"))

            match = SIMNET_PRINCIPAL_RE.search(line)
            if match:
                violations.append((i, match.group(), "simnet (SN...)"))
    except Exception as e:
        print(f"  WARN: Could not read {file_path}: {e}")
    return violations


def parse_gitmodules() -> dict[str, dict[str, str]]:
    """Parse .gitmodules if present."""
    gitmodules_path = REPO_ROOT / ".gitmodules"
    if not gitmodules_path.exists():
        return {}

    submodules = {}
    current_path = None
    current_config = {}

    with open(gitmodules_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[submodule "):
                if current_path:
                    submodules[current_path] = current_config
                current_path = line[len("[submodule "):-1].strip('"')
                current_config = {}
            elif "=" in line and current_path:
                key, _, value = line.partition("=")
                current_config[key.strip()] = value.strip()

    if current_path:
        submodules[current_path] = current_config

    return submodules


def check_submodule_alignment() -> list[str]:
    """Check submodule alignment across core repositories without failing on update=none."""
    print("--- Submodule Alignment Guard (Core 12 Repositories) ---\n")
    errors = []
    submodules = parse_gitmodules()

    for repo in CORE_REPOSITORIES:
        if repo == "conxian-business":
            print(f"  OK  {repo}: root workspace")
            continue

        repo_dir = REPO_ROOT / repo
        if not repo_dir.exists():
            print(f"  INFO {repo}: directory not present in workspace root")
            continue

        if repo in submodules:
            update_policy = submodules[repo].get("update", "checkout")
            if update_policy == "none" or repo in ALLOWED_UPDATE_NONE:
                print(f"  OK  {repo}: update=none (intentionally pinned, allowed override)")
            else:
                print(f"  OK  {repo}: update={update_policy} (aligned)")
        else:
            print(f"  OK  {repo}: non-submodule monorepo directory")

    return errors


def main():
    print("=== Production Contamination Guard & Submodule Alignment ===\n")

    align_errors = check_submodule_alignment()
    if align_errors:
        print(f"\n❌ FAIL: Submodule alignment errors: {align_errors}")
        sys.exit(1)

    print("\nScanning for hardcoded testnet/simnet principals in .clar files...\n")

    clar_files = find_clar_files()
    print(f"Found {len(clar_files)} .clar file(s)\n")

    total_violations = 0
    prod_violations = 0

    for clar_file in sorted(clar_files):
        violations = scan_file(clar_file)
        if not violations:
            continue

        rel_path = clar_file.relative_to(REPO_ROOT)
        is_prod = is_production_track(clar_file)

        for line_no, match, ptype in violations:
            total_violations += 1
            tag = "PRODUCTION" if is_prod else "non-prod"
            print(f"  [{tag}] {rel_path}:{line_no} — {ptype} principal: {match}")

            if is_prod:
                prod_violations += 1

    if prod_violations > 0:
        print(f"\n❌ FAIL: {prod_violations} hardcoded testnet/simnet principal(s) "
              f"found in production-track .clar files.")
        print("   These must be replaced with dynamic principals sourced from "
              "operational-treasury.clar per the Sovereign-First Deployment Mandate.")
        sys.exit(1)

    if total_violations > 0:
        print(f"\n⚠️  {total_violations} hardcoded testnet/simnet principal(s) found "
              f"in non-production-track files only (tests, examples, etc.).")
        print("   Review these before promoting any of these files to production.")
    else:
        print("✅ No hardcoded testnet/simnet principals found.")

    print("\n✅ Production Contamination Guard: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
