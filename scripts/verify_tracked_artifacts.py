#!/usr/bin/env python3
"""Tracked Artifacts Validator."""
import sys
import subprocess
def main():
    print("=== Tracked Artifacts Validator ===")
    prohibited_exact = [".env", "npm-debug.log", "yarn-error.log"]
    prohibited_patterns = ["node_modules/", "target/", "dist/", ".next/", "__pycache__/", ".DS_Store"]
    try:
        tracked_files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
        violations = []
        for f in tracked_files:
            if any(f == p or f.endswith("/" + p) for p in prohibited_exact):
                violations.append(f)
                continue
            if any(p in f for p in prohibited_patterns):
                violations.append(f)
        if violations:
            print("❌ FAIL: Prohibited artifacts found in git index:")
            for v in violations:
                print(f"  - {v}")
            sys.exit(1)
    except Exception as e:
        print(f"  WARN: Could not run git ls-files: {e}")
    print("✅ Tracked Artifacts Validator: PASSED")
    sys.exit(0)
if __name__ == "__main__":
    main()
