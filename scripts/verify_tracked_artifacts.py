#!/usr/bin/env python3
"""Verify that all critical repository artifacts are tracked and well-formed.

Validates:
1. All files referenced in SUMMARY.md exist and are tracked in git.
2. Key governance artifacts (SECURITY.md, GOVERNANCE.md, CHANGELOG.md, etc.) exist.
3. No orphaned generated artifacts outside of .gitignore-protected directories.
4. Evidence pack directory structure is consistent.
5. BOS buildout documentation index is complete.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ARTIFACTS = [
    "README.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "SUMMARY.md",
    "AGENTS.md",
    "BOS_KNOWLEDGE_GRAPH.md",
    "spec.md",
    "ecosystem-dashboard.md",
    "DEVELOPER_QUICKSTART.md",
    "RELEASING.md",
    "DEPENDENCY_BASELINE.md",
]

REQUIRED_DOCS = [
    "docs/BOS_BUSINESS_BUILDOUT.md",
    "docs/PORTFOLIO_BUSINESS_UNIT_MAP.md",
    "docs/CONXIAN_UNIFIED_THEORY_v2.md",
    "docs/DAO_GOVERNANCE_SPEC.md",
    "docs/TECHNICAL_READINESS_CERTIFICATION.md",
    "docs/UNIFIED_PRODUCTION_READINESS_GAP_REPORT.md",
    "docs/DEVELOPER_LED_GROWTH_STRATEGY.md",
    "docs/ISO_20022_INTEGRATION_SPEC.md",
    "docs/SAB_MIGRATION_READINESS_GATES.md",
    "docs/TECHNICAL_WHITEPAPER_OUTLINE.md",
]

GENERATED_DIRS = [
    "conxian-business/.generated",
    ".agent_tmp",
]

EVIDENCE_DIR = "audit/evidence"


def run(cmd: list[str], cwd: Path = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO_ROOT)


def get_tracked_files() -> set[str]:
    """Return the set of all files tracked by git."""
    result = run(["git", "ls-files", "-z"])
    if result.returncode != 0:
        print(f"ERROR: git ls-files failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return {f for f in result.stdout.split("\x00") if f}


def is_in_submodule(path: str, submodules: set[str]) -> bool:
    """Check if a path lives inside a git submodule directory."""
    for sm in submodules:
        if path == sm or path.startswith(sm + "/"):
            return True
    return False


def get_submodule_paths() -> set[str]:
    """Return the set of submodule directory paths."""
    gitmodules = REPO_ROOT / ".gitmodules"
    if not gitmodules.exists():
        return set()
    paths = set()
    with open(gitmodules) as f:
        for line in f:
            line = line.strip()
            if line.startswith("path = "):
                paths.add(line.split("=", 1)[1].strip())
    return paths


def parse_summary_links(summary_path: Path) -> list[str]:
    """Extract all markdown links from SUMMARY.md."""
    links: list[str] = []
    text = summary_path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r'\[([^\]]*)\]\(([^)]+\.md[^)]*)\)')
    for match in pattern.finditer(text):
        link = match.group(2).split("#")[0].split("?")[0]
        links.append(link)
    return links


def main() -> int:
    errors: list[str] = []

    tracked = get_tracked_files()

    # 1) Required root artifacts must exist and be tracked.
    print("--- Checking required root artifacts ---")
    for artifact in REQUIRED_ARTIFACTS:
        path = REPO_ROOT / artifact
        if not path.exists():
            errors.append(f"Required artifact missing from disk: {artifact}")
        elif artifact not in tracked:
            errors.append(f"Required artifact not tracked by git: {artifact}")
        else:
            print(f"  OK  {artifact}")

    # 2) Required docs must exist.
    print("\n--- Checking required documentation ---")
    for doc in REQUIRED_DOCS:
        path = REPO_ROOT / doc
        if not path.exists():
            errors.append(f"Required documentation missing: {doc}")
        elif doc not in tracked:
            errors.append(f"Required documentation not tracked by git: {doc}")
        else:
            print(f"  OK  {doc}")

    # 3) SUMMARY.md links must be valid.
    print("\n--- Validating SUMMARY.md links ---")
    summary_path = REPO_ROOT / "SUMMARY.md"
    submodule_paths = get_submodule_paths()
    if summary_path.exists():
        links = parse_summary_links(summary_path)
        broken = 0
        for link in links:
            target = REPO_ROOT / link
            if is_in_submodule(link, submodule_paths):
                # Submodule content lives in its own repo; skip file-exists check here.
                continue
            if not target.exists():
                errors.append(f"SUMMARY.md references missing file: {link}")
                broken += 1
            elif link not in tracked:
                errors.append(f"SUMMARY.md references untracked file: {link}")
                broken += 1
        print(f"  Checked {len(links)} link(s), {broken} broken")
    else:
        errors.append("SUMMARY.md not found")

    # 4) No generated artifacts committed outside exempt directories.
    print("\n--- Scanning for stale generated artifacts ---")
    generated_patterns = [".generated/", "__pycache__/", "node_modules/"]
    for f in tracked:
        for pattern in generated_patterns:
            if pattern in f:
                exempt = any(f.startswith(d + "/") for d in GENERATED_DIRS)
                if not exempt:
                    errors.append(f"Committed generated artifact: {f}")

    if not any(
        pattern in f
        for f in tracked
        for pattern in generated_patterns
        if not any(f.startswith(d + "/") for d in GENERATED_DIRS)
    ):
        print("  OK  No stale generated artifacts found")

    # 5) Evidence directory structure check.
    print("\n--- Checking evidence pack structure ---")
    evidence_path = REPO_ROOT / EVIDENCE_DIR
    if evidence_path.is_dir():
        evidence_files = list(evidence_path.rglob("*"))
        evidence_tracked = [str(f.relative_to(REPO_ROOT)) for f in evidence_files
                          if f.is_file() and str(f.relative_to(REPO_ROOT)) in tracked]
        if evidence_tracked:
            print(f"  OK  {len(evidence_tracked)} evidence file(s) tracked")
        else:
            print("  NOTE  No evidence files found (may be in subdirectories)")
    else:
        print(f"  NOTE  {EVIDENCE_DIR} directory not found (optional)")

    # 6) AGENTS.md must be reasonably sized (not truncated).
    print("\n--- Checking AGENTS.md integrity ---")
    agents_path = REPO_ROOT / "AGENTS.md"
    if agents_path.exists():
        agents_size = agents_path.stat().st_size
        if agents_size < 500:
            errors.append(f"AGENTS.md appears truncated ({agents_size} bytes)")
        else:
            print(f"  OK  AGENTS.md ({agents_size} bytes)")

    if errors:
        print(f"\n❌ {len(errors)} violation(s) found:")
        for err in errors:
            print(f"  • {err}")
        return 1

    print("\n✅ All tracked artifacts verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
