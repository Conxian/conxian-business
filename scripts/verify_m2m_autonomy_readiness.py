#!/usr/bin/env python3
"""Validate the canonical M2M/autonomy readiness gap ledger."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "audit" / "m2m_autonomy_gap_ledger.json"
LAB_MANIFEST = ROOT / "audit" / "bos_safe_lab_manifest.json"
ALLOWED = {
    "Implemented",
    "Verified",
    "Conditional",
    "Incubating",
    "Stub/Quarantined",
    "Blocked (human)",
    "Not Run",
}
REQUIRED = {"id", "severity", "domain", "owner", "status", "evidence", "gap", "acceptance"}


def main() -> int:
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"M2M readiness ledger is unreadable: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    try:
        lab = json.loads(LAB_MANIFEST.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"safe lab manifest is unreadable: {exc}")
        lab = {}
    if lab.get("production_execution") != "forbidden":
        errors.append("safe lab manifest must forbid production execution")
    if lab.get("mode") != "local-or-isolated-testnet-only":
        errors.append("safe lab manifest must be local-or-isolated-testnet-only")
    if not isinstance(data, dict) or not isinstance(data.get("gaps"), list):
        errors.append("ledger must be an object with a gaps array")
    else:
        ids: set[str] = set()
        for index, gap in enumerate(data["gaps"]):
            prefix = f"gaps[{index}]"
            if not isinstance(gap, dict):
                errors.append(f"{prefix} must be an object")
                continue
            missing = REQUIRED - gap.keys()
            if missing:
                errors.append(f"{prefix} missing: {', '.join(sorted(missing))}")
            gap_id = gap.get("id")
            if not isinstance(gap_id, str) or not gap_id:
                errors.append(f"{prefix}.id must be non-empty")
            elif gap_id in ids:
                errors.append(f"duplicate gap id: {gap_id}")
            else:
                ids.add(gap_id)
            if gap.get("status") not in ALLOWED:
                errors.append(f"{prefix}.status is not an approved status")
            if not isinstance(gap.get("evidence"), list) or not gap.get("evidence"):
                errors.append(f"{prefix}.evidence must be a non-empty list")
            if not isinstance(gap.get("acceptance"), str) or not gap.get("acceptance", "").strip():
                errors.append(f"{prefix}.acceptance must be non-empty")

    if errors:
        print("M2M/autonomy readiness ledger violations:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(f"M2M/autonomy readiness ledger: OK ({len(data['gaps'])} gaps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
