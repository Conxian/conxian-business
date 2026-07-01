#!/usr/bin/env python3
import sys
from pathlib import Path
def main():
    changelog = Path("CHANGELOG.md")
    if changelog.exists() and "## [Unreleased]" in changelog.read_text():
        print("PASS: Release hygiene OK")
        sys.exit(0)
    print("FAIL: Missing Unreleased section")
    sys.exit(1)
if __name__ == "__main__":
    main()
