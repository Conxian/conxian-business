#!/usr/bin/env python3
"""Enforce the required-job result policy for Conxian Unified CI."""

from __future__ import annotations

import os
import sys
from collections.abc import Iterable


def as_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() == "true"


def result(name: str) -> str:
    value = os.environ.get(name, "unavailable").strip().lower()
    return value or "unavailable"


def build_rows() -> list[tuple[str, str, bool]]:
    code_impacting = as_bool("CODE_IMPACTING", default=True)
    b2b_required = as_bool("B2B_REQUIRED")
    market_required = as_bool("MARKET_SUITE_REQUIRED")
    audit_required = as_bool("AUDIT_DOCS_REQUIRED")
    simulation_required = as_bool("TESTNET_SIMULATION_REQUIRED")

    return [
        ("Change detection", result("CHANGE_DETECTION_RESULT"), True),
        ("Repo Hygiene (ZSE & Submodules)", result("REPO_HYGIENE_RESULT"), True),
        ("Gateway Suite", result("GATEWAY_SUITE_RESULT"), code_impacting),
        (
            "B2B Suite (Nexus & SDK)",
            result("B2B_SUITE_RESULT"),
            code_impacting and b2b_required,
        ),
        (
            "Core Library Suite (lib-conxian-core)",
            result("LIB_CORE_SUITE_RESULT"),
            code_impacting,
        ),
        ("B2C Wallet Suite", result("B2C_WALLET_SUITE_RESULT"), code_impacting),
        ("Transparency Audit & Docs", result("AUDIT_DOCS_RESULT"), audit_required),
        (
            "Testnet Simulation",
            result("TESTNET_SIMULATION_RESULT"),
            simulation_required,
        ),
        ("Market Integration Suite", result("MARKET_SUITE_RESULT"), market_required),
    ]


def blocking_jobs(rows: Iterable[tuple[str, str, bool]]) -> list[str]:
    return [name for name, job_result, required in rows if required and job_result != "success"]


def write_summary(rows: list[tuple[str, str, bool]], blocked: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        raise RuntimeError("GITHUB_STEP_SUMMARY is required")

    docs_only = as_bool("DOCS_ONLY")
    b2b_trigger = as_bool("B2B_TRIGGER")
    market_trigger = as_bool("MARKET_TRIGGER")

    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write("## Conxian Unified CI summary\n\n")
        summary.write(
            f"- PR classification: **{'docs-only' if docs_only else 'code-impacting'}**\n"
        )
        summary.write(f"- B2B trigger detected: **{'yes' if b2b_trigger else 'no'}**\n")
        summary.write(f"- Market trigger detected: **{'yes' if market_trigger else 'no'}**\n")
        if docs_only:
            summary.write(
                "- Docs-only PR detected: heavy implementation suites are intentionally skipped.\n\n"
            )
        else:
            summary.write(
                "- Code-impacting PR detected: core implementation suites are required for merge.\n\n"
            )

        summary.write("| Job | Result | Required for repo-content merge gate |\n")
        summary.write("| --- | --- | --- |\n")
        for name, job_result, required in rows:
            summary.write(
                f"| {name} | `{job_result}` | {'yes' if required else 'no'} |\n"
            )

        summary.write("\n### Merge gate result\n")
        if blocked:
            summary.write("❌ **Fail** — required repo-content checks did not succeed:\n")
            for job in blocked:
                summary.write(f"- `{job}`\n")
        else:
            summary.write("✅ **Pass** — all required repo-content checks succeeded.\n")


def main() -> int:
    rows = build_rows()
    blocked = blocking_jobs(rows)
    try:
        write_summary(rows, blocked)
    except OSError as exc:
        print(f"ERROR: could not write CI summary: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if blocked:
        print("Blocking repo-content check results: " + ", ".join(blocked))
        return 1

    print("CI summary gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
