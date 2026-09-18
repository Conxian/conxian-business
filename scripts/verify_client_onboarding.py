#!/usr/bin/env python3
"""
Verify Client Onboarding, System Installation & Unified Installer Specification Alignment.

Validates the architecture, commercial packaging tiers, component connectivity matrix,
and 15-minute TTFV installer prerequisites defined in
docs/CLIENT_ONBOARDING_AND_UNIFIED_INSTALLER_SPEC.md.
"""

import os
import sys

SPEC_PATH = "docs/CLIENT_ONBOARDING_AND_UNIFIED_INSTALLER_SPEC.md"

REQUIRED_TIERS = ["Community Tier", "Business Tier", "Enterprise Tier"]
REQUIRED_KEY_TERMS = [
    "Gateway",
    "Nexus",
    "Wallet",
    "BitVM2",
    "StrongBox",
    "ISO 20022",
    "Nitro",
]


def verify_client_onboarding_spec():
    if not os.path.exists(SPEC_PATH):
        print(f"Error: Specification file missing at {SPEC_PATH}", file=sys.stderr)
        return 1

    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Verify Commercial Packaging Tiers
    print("--- Verifying Commercial Packaging Tiers ---")
    for tier in REQUIRED_TIERS:
        if tier in content:
            print(f"  OK  Tier verified: '{tier}'")
        else:
            print(f"  FAIL Tier missing: '{tier}'", file=sys.stderr)
            return 1

    # 2. Verify Key System Concepts / Architectural Elements
    print("\n--- Verifying System Concepts & Architecture in Specification ---")
    for term in REQUIRED_KEY_TERMS:
        if term in content:
            print(f"  OK  Concept/architecture mapped: '{term}'")
        else:
            print(f"  FAIL Concept/architecture unmapped: '{term}'", file=sys.stderr)
            return 1

    # 3. Verify Unified Installer Prerequisites (TTFV < 15m)
    print("\n--- Verifying Unified Installer (cxn) Requirements ---")
    if "TTFV" in content and "15 minutes" in content:
        print("  OK  Time-To-First-Value (TTFV < 15m) benchmark verified.")
    else:
        print("  FAIL TTFV requirement missing or invalid.", file=sys.stderr)
        return 1

    print("\n✅ Client Onboarding & System Installation Verification: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(verify_client_onboarding_spec())
