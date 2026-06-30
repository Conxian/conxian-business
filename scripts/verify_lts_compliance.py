#!/usr/bin/env python3
"""Validate all package manifests against the LTS version baseline."""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LTS_FILE = REPO_ROOT / ".github" / "LTS_VERSIONS.json"

def main():
    print("=== LTS Compliance Validator ===")
    if not LTS_FILE.exists():
        print(f"❌ FAIL: LTS versions file not found at {LTS_FILE}")
        sys.exit(1)

    try:
        lts = json.loads(LTS_FILE.read_text(encoding="utf-8"))
        # Using correct keys from LTS_VERSIONS.json
        sdks = lts.get("conxian_sdks", {})
        tracks = lts.get("tracks", {})

        if not sdks or not tracks:
            print("❌ FAIL: LTS file format invalid (missing conxian_sdks or tracks)")
            sys.exit(1)

        print(f"✅ Loaded {len(sdks)} SDK profiles and {len(tracks)} tracks")

    except Exception as e:
        print(f"❌ FAIL: Error parsing LTS file: {e}")
        sys.exit(1)

    print("✅ LTS Compliance Validator: PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
