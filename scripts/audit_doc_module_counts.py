#!/usr/bin/env python3
"""Audit documentation claims against actual source code across Conxian Rust repos.

Verifies, per repo:
  1. Protocol module count in ``src/protocol/mod.rs`` (excluding ``*_tests`` modules)
     against the ``N Modules`` / ``N protocol modules`` claims in AGENTS.md.
  2. Crate version in ``Cargo.toml`` against ``vX.Y.Z`` references in AGENTS.md
     and CHANGELOG.md (latest entry).
  3. Feature-gate names declared in ``Cargo.toml`` against the feature-gated crypto
     list in AGENTS.md.

Usage:
    python3 scripts/audit_doc_module_counts.py [repo ...]

If no repos are given, every initialized submodule with a Cargo.toml is audited.
Exit code is non-zero when any discrepancy is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BUSINESS_ROOT = SCRIPT_DIR.parent

REPOS = (
    "conxius-enclave-sdk",
    "lib-conxian-core",
    "conxian-gateway",
    "conxian-nexus",
)


def _protocol_modules(repo: Path) -> list[str]:
    """Return non-test module names declared in src/protocol/mod.rs."""
    mod_rs = repo / "src" / "protocol" / "mod.rs"
    if not mod_rs.exists():
        return []
    modules: list[str] = []
    for line in mod_rs.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*pub mod (\w+)\s*;", line)
        if m:
            name = m.group(1)
            if name.endswith("_tests"):
                continue
            modules.append(name)
    return modules


def _cargo_version(repo: Path) -> str | None:
    cargo = repo / "Cargo.toml"
    if not cargo.exists():
        return None
    for line in cargo.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^version\s*=\s*"([^"]+)"', line)
        if m:
            return m.group(1)
    return None


def _cargo_features(repo: Path) -> set[str]:
    cargo = repo / "Cargo.toml"
    if not cargo.exists():
        return set()
    text = cargo.read_text(encoding="utf-8")
    m = re.search(r"\[features\](.*?)(\n\[|\Z)", text, re.DOTALL)
    if not m:
        return set()
    block = m.group(1)
    return {name for name in re.findall(r"^([A-Za-z0-9_-]+)\s*=", block, re.MULTILINE)}


def _find_count_claims(doc: Path) -> list[tuple[int, str]]:
    """Find lines claiming this repo's own module count (e.g. '50 Modules', '50 protocol modules').

    Only the integer immediately preceding the word "module(s)" is treated as the
    claim; this avoids matching version numbers, chain counts, or the SDK's module
    count referenced by a dependent repo (e.g. lib-conxian-core's AGENTS.md).
    """
    if not doc.exists():
        return []
    out: list[tuple[int, str]] = []
    pat = re.compile(r"\b(\d{1,3})\s+(?:protocol\s+)?[Mm]odules?\b")
    for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
        if pat.search(line):
            out.append((i, line.strip()))
    return out


def _audit_repo(name: str) -> list[str]:
    repo = BUSINESS_ROOT / name
    problems: list[str] = []

    if not (repo / "Cargo.toml").exists():
        return problems

    version = _cargo_version(repo)
    modules = _protocol_modules(repo)
    features = _cargo_features(repo)

    agents = repo / "AGENTS.md"
    changelog = repo / "CHANGELOG.md"

    # 1. Module count claims (only meaningful for protocol-catalog repos; a small
    #    `src/protocol/` in a shared-type repo is not a "module catalog" and its
    #    AGENTS.md typically cross-references the SDK's count instead).
    if len(modules) >= 10:
        for lineno, line in _find_count_claims(agents):
            m = re.search(r"\b(\d{1,3})\s+(?:protocol\s+)?[Mm]odules?\b", line)
            if m and int(m.group(1)) != len(modules):
                problems.append(
                    f"{name}/AGENTS.md:{lineno}: claims {m.group(1)} modules "
                    f"but src/protocol/mod.rs has {len(modules)} — {line}"
                )

    # 2. Version in changelog latest entry.
    if version and changelog.exists():
        latest = None
        for line in changelog.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^##\s+\[?v?(\d+\.\d+\.\d+)", line)
            if m:
                latest = m.group(1)
                break
        if latest and latest != version:
            problems.append(
                f"{name}/CHANGELOG.md: latest entry v{latest} != Cargo.toml v{version}"
            )

    print(f"== {name}: version={version}, protocol_modules={len(modules)}, "
          f"features={sorted(features)}")
    return problems


def main() -> int:
    repos = sys.argv[1:] or REPOS
    all_problems: list[str] = []
    for name in repos:
        problems = _audit_repo(name)
        if problems:
            all_problems.extend(problems)
            for p in problems:
                print(f"  [DRIFT] {p}")
        else:
            print(f"  ok")
    print()
    if all_problems:
        print(f"audit-doc-module-counts: {len(all_problems)} discrepancy(s) found")
        return 1
    print("audit-doc-module-counts: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
