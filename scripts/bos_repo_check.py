from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    label: str
    argv: tuple[str, ...]


CHECKS: tuple[Check, ...] = (
    Check("Knowledge retention (ZSE)", ("python3", "scripts/verify_knowledge_retention.py")),
    Check("Tracked artifacts", ("python3", "scripts/verify_tracked_artifacts.py")),
    Check(
        "BOS production boundary",
        ("python3", "scripts/verify_bos_production_boundary.py"),
    ),
    Check("Submodule integrity", ("python3", "scripts/verify_submodule_integrity.py")),
    Check("Release hygiene", ("python3", "scripts/verify_release_hygiene.py")),
    Check("Governance baseline", ("python3", "scripts/verify_repo_governance_baseline.py")),
    Check(
        "Contamination guard",
        ("python3", "scripts/verify_contamination_guard.py"),
    ),
)


def _run(check: Check) -> int:
    print(f"\n==> {check.label}")
    proc = subprocess.run(check.argv, check=False)
    return int(proc.returncode)


def main() -> int:
    failures: list[str] = []
    for check in CHECKS:
        status = _run(check)
        if status != 0:
            failures.append(f"{check.label} (exit {status})")

    if failures:
        print("\nBOS repo-check: FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nBOS repo-check: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
