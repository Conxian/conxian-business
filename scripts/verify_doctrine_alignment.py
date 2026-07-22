#!/usr/bin/env python3
"""Validate the small, deterministic CON-1530 doctrine surface.

This is intentionally scoped to the canonical doctrine standard, register, and
documentation index. It does not attempt to semantically audit every portfolio
repository or ban protocol-level terms that are legitimate when qualified.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    paths = {
        "standard": ROOT / "docs/DOCTRINE_ALIGNMENT_STANDARD.md",
        "register": ROOT / "docs/PORTFOLIO_DOCTRINE_REGISTER.md",
        "index": ROOT / "docs/DOCUMENTATION_ALIGNMENT_INDEX.md",
    }

    documents: dict[str, str] = {}
    for name, path in paths.items():
        if not path.is_file():
            fail(errors, f"missing canonical document: {path.relative_to(ROOT)}")
            continue
        documents[name] = path.read_text(encoding="utf-8")

    standard = documents.get("standard", "")
    register = documents.get("register", "")
    index = documents.get("index", "")

    for phrase in (
        "non-custodial software and infrastructure builder/operator",
        "not a market participant",
        "not a user-data extraction business",
        "protocol-level state transitions",
        "Implemented",
        "Verified",
        "Target-state",
        "Deprecated",
        "Production intent",
        "Reference implementation",
        "Research/experimental",
        "Internal only",
        "Canonical",
        "Supporting",
        "Public-safe",
        "Public-safe stub",
        "Internal-only",
        "Archive candidate",
    ):
        if phrase not in standard:
            fail(errors, f"doctrine standard is missing required phrase: {phrase}")

    for anchor in (
        "TRUST_AND_PROOF_MESSAGING.md",
        "CLAIM_EVIDENCE_MATRIX.md",
        "PORTFOLIO_BUSINESS_UNIT_MAP.md",
        "BOUNDARY_DECISION_LOG.md",
        "TECHNICAL_WHITEPAPER_OUTLINE.md",
    ):
        if anchor not in standard:
            fail(errors, f"doctrine standard does not link canonical anchor: {anchor}")

    for link in (
        "DOCTRINE_ALIGNMENT_STANDARD.md",
        "PORTFOLIO_DOCTRINE_REGISTER.md",
    ):
        if link not in index:
            fail(errors, f"documentation index does not cross-link: {link}")

    required_repositories = (
        "Conxian/.github-private",
        "Conxian/.github",
        "Conxian/Conxian",
        "Conxian/conxian_ui",
        "Conxian/conxius-orbit",
        "Conxian/conxius-wallet",
        "Conxian/conxian-labs-site",
        "Conxian/conxian-gateway",
        "Conxian/lib-conxian-core",
        "Conxian/conxius-platform",
        "Conxian/conxian-nexus",
        "Conxian/conxian-business",
        "Conxian/conxius-enclave-sdk",
        "Conxian/demo-repository",
        "Conxian/conxian.github.io",
        "Conxian/conxian_market",
    )
    for repository in required_repositories:
        row_pattern = re.compile(
            r"^\| `" + re.escape(repository) + r"`(?: \(| \|)", re.MULTILINE
        )
        if not row_pattern.search(register):
            fail(errors, f"portfolio register is missing repository row: {repository}")

    for artifact in (
        "Conxian/docs/WHITEPAPER.md",
        "conxian_market/README.md",
        "docs/ITIL5_STRATEGIC_ANALYSIS_2026.md",
        "Top-level READMEs",
    ):
        if artifact not in register:
            fail(errors, f"portfolio register is missing high-risk disposition: {artifact}")

    whitepaper_lines = [
        line
        for line in (register + "\n" + index).splitlines()
        if "Conxian/docs/WHITEPAPER.md" in line
    ]
    if not whitepaper_lines:
        fail(errors, "whitepaper disposition row is missing")
    else:
        if not any("Archive candidate" in line and "rewrite" in line for line in whitepaper_lines):
            fail(errors, "old whitepaper is not classified as an archive/rewrite candidate")
        if any("| Canonical | Public-safe |" in line for line in whitepaper_lines):
            fail(errors, "old whitepaper still has the canonical/public-safe classification")

    for phrase in ("follow-up", "not company custody", "protocol-level"):
        if phrase not in register.lower():
            fail(errors, f"portfolio register is missing boundary/disposition phrase: {phrase}")

    # These aliases are not allowed in the current canonical doctrine surfaces.
    # Repository slugs such as `Conxian_UI` remain valid when cited verbatim.
    for alias in ("Conxian Gateway", "Conxius Enclave SDK", "conxius_orbit"):
        for name, text in (("standard", standard), ("register", register), ("index", index)):
            if alias in text:
                fail(errors, f"deprecated display alias appears in canonical {name}: {alias}")

    if errors:
        print("Doctrine alignment check: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Doctrine alignment check: OK")
    print(f"- canonical documents: {len(paths)}")
    print(f"- registered repositories: {len(required_repositories)}")
    print("- high-risk classifications and cross-links: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
