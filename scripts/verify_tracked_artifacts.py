#!/usr/bin/env python3
import sys
import subprocess
def main():
    prohibited_patterns = ["node_modules/", "target/", "dist/", ".next/", "__pycache__/"]
    try:
        tracked_files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
        violations = [f for f in tracked_files if any(p in f for p in prohibited_patterns)]
        if violations:
            print("FAIL: Prohibited artifacts found")
            sys.exit(1)
    except Exception:
        pass
    print("PASS: No prohibited artifacts")
    sys.exit(0)
if __name__ == "__main__":
    main()
