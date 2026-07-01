#!/usr/bin/env python3
"""Production Contamination Guard."""
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Target ST (testnet) and SN (simnet) only. SP (mainnet) is allowed but discouraged.
TESTNET_PRINCIPAL_RE = re.compile(r"'ST[0-9A-HJ-NP-Z]{25,40}")
SIMNET_PRINCIPAL_RE = re.compile(r"'SN[0-9A-HJ-NP-Z]{25,40}")

EXCLUDE_DIRS = {".git", "node_modules", "target", "dist", ".next", "__pycache__"}
NON_PRODUCTION_DIRS = {"tests", "test", "spec", "mock", "fixtures", "examples", "playground", "sandbox"}

def is_production_track(file_path: Path) -> bool:
    parts = set(file_path.relative_to(REPO_ROOT).parts)
    return not (parts & NON_PRODUCTION_DIRS)

def find_clar_files() -> list[Path]:
    clar_files = []
    for clar_file in REPO_ROOT.rglob("*.clar"):
        parts = set(clar_file.relative_to(REPO_ROOT).parts)
        if any(exclude in parts for exclude in EXCLUDE_DIRS):
            continue
        clar_files.append(clar_file)
    return clar_files

def scan_file(file_path: Path) -> list[tuple[int, str, str]]:
    violations = []
    try:
        content = file_path.read_text(errors="ignore")
        for i, line in enumerate(content.splitlines(), 1):
            match = TESTNET_PRINCIPAL_RE.search(line)
            if match:
                violations.append((i, match.group(), "testnet (ST...)"))
            match = SIMNET_PRINCIPAL_RE.search(line)
            if match:
                violations.append((i, match.group(), "simnet (SN...)"))
    except Exception as e:
        print(f"  WARN: Could not read {file_path}: {e}")
    return violations

def main():
    print("=== Production Contamination Guard ===\n")
    clar_files = find_clar_files()
    print(f"Found {len(clar_files)} .clar file(s)\n")
    total_violations = 0
    prod_violations = 0
    for clar_file in sorted(clar_files):
        violations = scan_file(clar_file)
        if not violations:
            continue
        rel_path = clar_file.relative_to(REPO_ROOT)
        is_prod = is_production_track(clar_file)
        for line_no, match, ptype in violations:
            total_violations += 1
            tag = "PRODUCTION" if is_prod else "non-prod"
            print(f"  [{tag}] {rel_path}:{line_no} — {ptype} principal: {match}")
            if is_prod:
                prod_violations += 1
    if prod_violations > 0:
        print(f"\n❌ FAIL: {prod_violations} hardcoded testnet/simnet principal(s) found.")
        sys.exit(1)
    print("\n✅ Production Contamination Guard: PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
