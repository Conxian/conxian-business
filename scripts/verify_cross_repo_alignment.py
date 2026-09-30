#!/usr/bin/env python3
"""Verify Business Repo Source-of-Truth & Cross-Repo Alignment.

Validates that:
1. Source-of-truth governance docs (GAPS.md, PORTFOLIO.md, SLA.md, ALIGNMENT.md, COMMERCIAL_PACKAGING_DOCTRINE.md) exist.
2. GAPS.md contains Pillar Alignment and candidate score matrix with 3.0 rejection threshold.
3. PORTFOLIO.md contains Capability x Chain matrix with Reference Customer column and BaaP pricing tiers.
4. SLA.md contains Tiered Support Matrix, 99.5% uptime, SEV1 response parameters, Force Majeure, no credits in v1, and scaling trigger.
5. ALIGNMENT.md lists all active submodules with pillar alignment.
6. COMMERCIAL_PACKAGING_DOCTRINE.md contains 3-layer BaaP monetization engine (Escrow split 80/10/10, SaaS licensing, x402 edge compute).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_file_exists(path: Path) -> bool:
    if not path.exists():
        print(f"  FAIL: File missing: {path.relative_to(REPO_ROOT)}")
        return False
    print(f"  OK  File exists: {path.relative_to(REPO_ROOT)}")
    return True


def check_file_content(path: Path, required_strings: list[str]) -> list[str]:
    errors = []
    if not path.exists():
        return [f"{path.name} missing"]
    content = path.read_text(encoding="utf-8")
    for req in required_strings:
        if req not in content:
            errors.append(f"{path.name}: missing required string '{req}'")
        else:
            print(f"  OK  {path.name} contains '{req}'")
    return errors


def verify_gaps():
    print("\n--- Verifying docs/GAPS.md ---")
    path = REPO_ROOT / "docs" / "GAPS.md"
    required = [
        "Pillar Alignment",
        "Vertical Sovereignty",
        "Operational Unification",
        "Nakamoto Readiness",
        "Weighted Total",
        "Rejected (< 3.0)",
        "GAP-SLA-01"
    ]
    return check_file_content(path, required)


def verify_portfolio():
    print("\n--- Verifying docs/PORTFOLIO.md ---")
    path = REPO_ROOT / "docs" / "PORTFOLIO.md"
    required = [
        "Capability × Chain Matrix",
        "Reference Customer / Lead Target",
        "Bitcoin L1",
        "Stacks L2",
        "conxian-gateway",
        "conxian-nexus",
        "conxius-wallet",
        "conxian_market",
        "lib-conxian-core",
        "conxius-enclave-sdk",
        "Business-as-a-Platform (BaaP)"
    ]
    return check_file_content(path, required)


def verify_sla():
    print("\n--- Verifying docs/SLA.md ---")
    path = REPO_ROOT / "docs" / "SLA.md"
    required = [
        "Tiered Support & SLA Matrix",
        "NO SLA",
        "Contractual SLA",
        "99.5% monthly uptime percentage",
        "SEV1 — Critical",
        "Force Majeure",
        "no financial service credits are issued",
        "Customer #3"
    ]
    return check_file_content(path, required)


def verify_commercial_packaging():
    print("\n--- Verifying docs/COMMERCIAL_PACKAGING_DOCTRINE.md ---")
    path = REPO_ROOT / "docs" / "COMMERCIAL_PACKAGING_DOCTRINE.md"
    required = [
        "Business-as-a-Platform (BaaP)",
        "2.0% gross market fee",
        "80% Developer Pool",
        "10% Operations Pool",
        "10% Network Pool",
        "Tiered Volume Fee Decay",
        "Enterprise BaaP Node Licensing",
        "HTTP 402"
    ]
    return check_file_content(path, required)


def verify_alignment():
    print("\n--- Verifying docs/ALIGNMENT.md ---")
    path = REPO_ROOT / "docs" / "ALIGNMENT.md"
    required = [
        "conxian-gateway",
        "conxian-nexus",
        "conxius-wallet",
        "conxian_market",
        "lib-conxian-core",
        "conxius-enclave-sdk",
        "conxius-platform",
        "conxian-labs-site",
        "Three Pillars"
    ]
    return check_file_content(path, required)


def main():
    print("=== Cross-Repo Alignment & Source-of-Truth Verification ===\n")
    errors = []

    errors.extend(verify_gaps())
    errors.extend(verify_portfolio())
    errors.extend(verify_sla())
    errors.extend(verify_commercial_packaging())
    errors.extend(verify_alignment())

    if errors:
        print(f"\n❌ {len(errors)} violation(s) found:")
        for err in errors:
            print(f"  • {err}")
        sys.exit(1)

    print("\n✅ Business Repo Source-of-Truth & Cross-Repo Alignment: PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
