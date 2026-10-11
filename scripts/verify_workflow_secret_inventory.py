#!/usr/bin/env python3
"""Reconcile GitHub Actions secret references with a reviewed metadata catalog."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

EXPRESSION = re.compile(r"\$\{\{(.*?)\}\}", re.DOTALL)
SECRET_REFERENCE = re.compile(
    r"\bsecrets(?:\.([A-Za-z_][A-Za-z0-9_]*)|\[['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\])"
)


def scan_workflow_references(workflows_dir: Path) -> dict[str, dict[str, Any]]:
    """Return each referenced name, whether it is required, and its workflow files."""
    references: dict[str, dict[str, Any]] = {}
    workflow_files = sorted(
        path for pattern in ("*.yml", "*.yaml") for path in workflows_dir.rglob(pattern)
    )

    for path in workflow_files:
        text = path.read_text(encoding="utf-8")
        for expression_match in EXPRESSION.finditer(text):
            expression = expression_match.group(1)
            for reference_match in SECRET_REFERENCE.finditer(expression):
                name = reference_match.group(1) or reference_match.group(2)
                optional = "||" in expression[reference_match.end():]
                entry = references.setdefault(name, {"required": False, "files": set()})
                entry["required"] = entry["required"] or not optional
                entry["files"].add(path.relative_to(workflows_dir.parent.parent).as_posix())

    return references


def load_inventory(path: Path) -> dict[str, dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schemaVersion") != 1:
        raise ValueError("credential inventory must have schemaVersion 1")
    if not isinstance(payload.get("entries"), list):
        raise ValueError("credential inventory must have an entries array")

    inventory: dict[str, dict[str, str]] = {}
    required_fields = {"name", "classification", "rotationPlan", "approval"}
    for entry in payload["entries"]:
        if not isinstance(entry, dict) or not required_fields.issubset(entry):
            raise ValueError("every inventory entry must include name, classification, rotationPlan, and approval")
        name = entry["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError("inventory names must be valid environment identifiers")
        if any(not isinstance(entry[field], str) or not entry[field].strip() for field in required_fields - {"name"}):
            raise ValueError(f"inventory metadata must be non-empty strings: {name}")
        if name in inventory:
            raise ValueError(f"duplicate credential inventory entry: {name}")
        inventory[name] = entry
    return inventory


def compare_inventory(
    references: dict[str, dict[str, Any]], inventory: dict[str, dict[str, str]]
) -> tuple[list[str], list[str]]:
    """Return undocumented workflow references and catalog entries no longer referenced."""
    reference_names = set(references)
    inventory_names = set(inventory)
    return sorted(reference_names - inventory_names), sorted(inventory_names - reference_names)


def _write_outputs(
    undocumented: list[str],
    stale: list[str],
    references: dict[str, dict[str, Any]] | None = None,
    inventory: dict[str, dict[str, str]] | None = None,
    error: str | None = None,
) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            has_findings = bool(undocumented or stale or error)
            output.write(f"has_findings={'true' if has_findings else 'false'}\n")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write("## Workflow credential reference audit\n\n")
        if error:
            summary.write(f"Audit incomplete: {error}\n")
            return

        summary.write(
            "This source-reference audit does not verify whether a live GitHub secret is configured, "
            "valid, or rotated at its provider. Secret values are never read.\n\n"
        )
        summary.write("| Name | Classification | Approval | Rotation plan | Status | Workflow references |\n")
        summary.write("|---|---|---|---|---|---|\n")
        reference_map = references or {}
        inventory_map = inventory or {}
        for name in sorted(set(reference_map) | set(inventory_map)):
            reference = reference_map.get(name)
            catalog_entry = inventory_map.get(name)
            if name in undocumented:
                status = "Undocumented reference"
            elif name in stale:
                status = "No longer referenced"
            else:
                status = "Catalogued"
            files = ", ".join(sorted(reference["files"])) if reference else "-"
            summary.write(
                f"| `{name}` | {catalog_entry['classification'] if catalog_entry else '-'} | "
                f"{catalog_entry['approval'] if catalog_entry else '-'} | "
                f"{catalog_entry['rotationPlan'] if catalog_entry else '-'} | {status} | {files} |\n"
            )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    workflows_dir = root / ".github" / "workflows"
    try:
        references = scan_workflow_references(workflows_dir)
        inventory = load_inventory(root / "ops" / "workflow-credential-inventory.json")
        undocumented, stale = compare_inventory(references, inventory)
    except (OSError, TypeError, ValueError) as exc:
        message = f"Workflow credential inventory could not be checked ({type(exc).__name__})"
        print(message, file=sys.stderr)
        _write_outputs([], [], error=message)
        return 2

    print(f"Scanned {len(references)} workflow secret names against {len(inventory)} catalog entries.")
    print("Secret values and live GitHub/provider configuration were not queried.")
    if undocumented:
        print("Undocumented workflow references: " + ", ".join(undocumented), file=sys.stderr)
    if stale:
        print("Catalog entries no longer referenced: " + ", ".join(stale), file=sys.stderr)
    _write_outputs(undocumented, stale, references=references, inventory=inventory)
    return 1 if undocumented or stale else 0


if __name__ == "__main__":
    sys.exit(main())
