#!/usr/bin/env python3
"""Release Hygiene Validator."""
import sys
from pathlib import Path
def main():
    print("=== Release Hygiene Validator ===")
    changelog = Path("CHANGELOG.md")
    if changelog.exists():
        content = changelog.read_text()
        if "## [Unreleased]" not in content:
            print("❌ FAIL: CHANGELOG.md missing [Unreleased] section")
            sys.exit(1)
    print("✅ Release Hygiene Validator: PASSED")
    sys.exit(0)
if __name__ == "__main__":
    main()
