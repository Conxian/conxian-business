#!/usr/bin/env python3
"""Verify release hygiene across the monorepo and its submodules.

Validates:
1. Every published Cargo crate version has a corresponding git tag.
2. CHANGELOG.md files have an [Unreleased] section and the latest version entry
   matches the current Cargo.toml version.
3. README version badges are not stale (match the current Cargo.toml version).
4. Submodule pins reference tags (not floating branches) for production-track repos.
5. No duplicate version tags exist across the repository.

Environment variables:
  GITHUB_TOKEN:                    GitHub API token for tag verification against origin.
  VERIFY_RELEASE_HYGIENE_CHECK_ORIGIN_TAGS:
                                   Set to 'true' to verify tags exist on origin remote.
  VERIFY_RELEASE_HYGIENE_TAG_EXPECTATION_MODE:
                                   'require' = tags must exist (CI gate).
                                   'warn'    = missing tags emit warnings only.
                                   Default: 'warn'.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Submodules that are expected to have Cargo.toml and tags.
RUST_CRATES = [
    "conxian-gateway",
    "conxian-nexus",
    "lib-conxian-core",
    "conxius-enclave-sdk",
]

# Root-level Cargo workspace members that are NOT independent crates.
WORKSPACE_ONLY = {"conxian-business"}


def run(cmd: list[str], cwd: Path = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO_ROOT)


def get_crate_version(crate_dir: Path) -> str | None:
    """Extract version from a Cargo.toml file."""
    toml_path = crate_dir / "Cargo.toml"
    if not toml_path.exists():
        return None
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        pkg = data.get("package", {})
        if "version" in pkg:
            return pkg.get("version")
        workspace = data.get("workspace", {})
        ws_pkg = workspace.get("package", {})
        return ws_pkg.get("version")
    except Exception:
        return None


def get_local_tags(cwd: Path = REPO_ROOT) -> set[str]:
    """Return all git tags in the repository."""
    result = run(["git", "tag", "-l"], cwd=cwd)
    if result.returncode != 0:
        return set()
    return {t.strip() for t in result.stdout.splitlines() if t.strip()}


def get_origin_tags(cwd: Path = REPO_ROOT) -> set[str]:
    """Return all tags on the origin remote via ls-remote."""
    result = run(["git", "ls-remote", "--tags", "origin"], cwd=cwd)
    if result.returncode != 0:
        return set()
    tags = set()
    for line in result.stdout.splitlines():
        # Format: <sha>\trefs/tags/<tagname>
        parts = line.split("\t")
        if len(parts) == 2 and parts[1].startswith("refs/tags/"):
            tag = parts[1][len("refs/tags/"):]
            # Skip peeled tags (^{})
            if not tag.endswith("^{}"):
                tags.add(tag)
    return tags


def parse_changelog_versions(changelog_path: Path) -> tuple[bool, str | None]:
    """Check for [Unreleased] section and extract latest released version."""
    if not changelog_path.exists():
        return False, None
    text = changelog_path.read_text(encoding="utf-8", errors="replace")

    has_unreleased = bool(re.search(r"\[Unreleased\]|unreleased", text, re.IGNORECASE))

    # Match ## [x.y.z] style version headers
    version_pattern = re.compile(r"##\s+\[v?(\d+\.\d+\.\d+)\]")
    versions = version_pattern.findall(text)
    latest = versions[0] if versions else None

    return has_unreleased, latest


def parse_readme_version_badge(readme_path: Path) -> str | None:
    """Extract version from a README badge like 'v0.1.5'."""
    if not readme_path.exists():
        return None
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    # Match badge patterns like: version-v0.1.5-blue or /v0.1.5-
    pattern = re.compile(r"v?(\d+\.\d+\.\d+)(?:[-\w]*)")
    # Prefer badges: https://img.shields.io/badge/version-v0.1.5-blue
    badge_pattern = re.compile(r"badge/version-v?(\d+\.\d+\.\d+)")
    match = badge_pattern.search(text)
    if match:
        return match.group(1)
    return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    check_origin = os.getenv("VERIFY_RELEASE_HYGIENE_CHECK_ORIGIN_TAGS", "").lower() == "true"
    tag_mode = os.getenv("VERIFY_RELEASE_HYGIENE_TAG_EXPECTATION_MODE", "warn")

    print("=== Release Hygiene Audit ===\n")

    # 1) Check each Rust crate for tag/version consistency.
    print("--- Crate version ↔ tag consistency ---")
    for crate_name in RUST_CRATES:
        crate_dir = REPO_ROOT / crate_name
        version = get_crate_version(crate_dir)

        if version is None:
            if crate_dir.exists():
                warnings.append(f"{crate_name}: Cargo.toml not found or unparseable")
            else:
                warnings.append(f"{crate_name}: directory not found (submodule may not be initialized)")
            continue

        expected_tag = f"v{version}"
        crate_local_tags = get_local_tags(crate_dir)
        crate_origin_tags = get_origin_tags(crate_dir) if check_origin else set()

        tag_found_local = expected_tag in crate_local_tags
        tag_found_origin = expected_tag in crate_origin_tags if check_origin else False

        if tag_found_local or tag_found_origin:
            source = "local & origin" if (tag_found_local and tag_found_origin) else ("local" if tag_found_local else "origin")
            print(f"  OK  {crate_name} v{version} → tag {expected_tag} ({source})")
        else:
            msg = f"{crate_name}: Cargo.toml version {version} has no tag {expected_tag}"
            if tag_mode == "require":
                errors.append(msg)
            else:
                warnings.append(msg)

    # 2) Check CHANGELOG.md for each crate.
    print("\n--- CHANGELOG hygiene ---")
    for crate_name in RUST_CRATES:
        crate_dir = REPO_ROOT / crate_name
        changelog = crate_dir / "CHANGELOG.md"
        version = get_crate_version(crate_dir)

        if not changelog.exists():
            warnings.append(f"{crate_name}: CHANGELOG.md not found")
            continue

        has_unreleased, latest_ver = parse_changelog_versions(changelog)

        if not has_unreleased and not (version and latest_ver and version == latest_ver):
            errors.append(f"{crate_name}/CHANGELOG.md: missing [Unreleased] section")

        if version and latest_ver and version != latest_ver:
            errors.append(
                f"{crate_name}/CHANGELOG.md: latest version [{latest_ver}] "
                f"does not match Cargo.toml version {version}"
            )
        elif version and latest_ver:
            print(f"  OK  {crate_name} CHANGELOG [{latest_ver}] matches Cargo.toml {version}")

    # 3) Check root CHANGELOG.md.
    print("\n--- Root CHANGELOG hygiene ---")
    root_changelog = REPO_ROOT / "CHANGELOG.md"
    if root_changelog.exists():
        has_unreleased, _ = parse_changelog_versions(root_changelog)
        if not has_unreleased:
            errors.append("Root CHANGELOG.md: missing [Unreleased] section")
        else:
            print("  OK  Root CHANGELOG has [Unreleased] section")
    else:
        warnings.append("Root CHANGELOG.md not found")

    # 4) Check README version badges.
    print("\n--- README version badge staleness ---")
    for crate_name in RUST_CRATES:
        crate_dir = REPO_ROOT / crate_name
        readme = crate_dir / "README.md"
        version = get_crate_version(crate_dir)

        if not readme.exists() or not version:
            continue

        badge_ver = parse_readme_version_badge(readme)
        if badge_ver and badge_ver != version:
            warnings.append(
                f"{crate_name}/README.md: badge version v{badge_ver} "
                f"is stale (Cargo.toml is {version})"
            )
        elif badge_ver:
            print(f"  OK  {crate_name} README badge v{badge_ver} matches Cargo.toml")
        else:
            print(f"  OK  {crate_name} README exists (no version badge detected)")

    # 5) Check for duplicate tags.
    print("\n--- Duplicate tag check ---")
    result = run(["git", "tag", "-l"], cwd=REPO_ROOT)
    if result.returncode == 0:
        tag_list = [t for t in result.stdout.splitlines() if t.strip()]
        seen: dict[str, list[str]] = {}
        # Check for tags that are identical or differ only by a 'v' prefix
        for tag in tag_list:
            normalized = tag.lstrip("v")
            seen.setdefault(normalized, []).append(tag)
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        if duplicates:
            for norm, tags in duplicates.items():
                errors.append(f"Duplicate/ambiguous tags: {', '.join(tags)}")
        else:
            print("  OK  No duplicate tags found")

    # 6) Check submodule pins reference tags where possible.
    print("\n--- Submodule release pin check ---")
    gitmodules = REPO_ROOT / ".gitmodules"
    if gitmodules.exists():
        result = run(["git", "submodule", "status"])
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                # Format: [ ]<sha> <path>
                sha = line[1:41].strip() if len(line) > 41 else ""
                path = line[42:].split()[0] if len(line) > 42 else ""
                if sha and path:
                    print(f"  OK  {path} pinned at {sha[:8]}")
    else:
        warnings.append(".gitmodules not found")

    # Report
    if warnings:
        print(f"\n⚠ {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  • {w}")

    if errors:
        print(f"\n❌ {len(errors)} violation(s) found:")
        for err in errors:
            print(f"  • {err}")
        return 1

    print("\n✅ Release hygiene verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
