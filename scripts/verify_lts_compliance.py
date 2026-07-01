#!/usr/bin/env python3
"""LTS Compliance Validator."""
import json
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
        sdks = lts.get("conxian_sdks", {})
        if not sdks:
            print("❌ FAIL: LTS file missing 'conxian_sdks' key")
            sys.exit(1)
        print(f"✅ Verified {len(sdks)} SDK profiles")
    except Exception as e:
        print(f"❌ FAIL: {e}")
        sys.exit(1)
    print("✅ LTS Compliance Validator: PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
