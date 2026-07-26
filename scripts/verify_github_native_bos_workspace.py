#!/usr/bin/env python3
"""Fail closed when GitHub-native BOS authority or intake controls regress."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_CONTENT: dict[str, tuple[str, ...]] = {
    "docs/GITHUB_NATIVE_BOS_WORKSPACE.md": (
        "GitHub Issues and pull requests are authoritative for all new",
        "BOS — Portfolio Operations",
        "Linear references are immutable historical provenance or archive pointers only",
        "Private GitHub repositories are not secret stores",
        "Source-of-truth precedence",
    ),
    "docs/NEXUS_LICENSING_GOVERNANCE.md": (
        "Conxian/conxian-business#942",
        "Conxian/conxian-nexus/issues/174",
        "Conxian/conxian-nexus/pull/173",
        "Conxian/.github/issues/60",
        "Conxian/conxian-business/issues/933",
        "does not choose license terms",
    ),
    ".github/ISSUE_TEMPLATE/bos_work_intake.yml": (
        "Owning repository",
        "Accountable role",
        "Workstream / control domain",
        "Information classification",
        "Zero Secret Egress confirmation",
        "Acceptance criteria and evidence",
    ),
    ".github/ISSUE_TEMPLATE/governance_legal_decision.yml": (
        "Owning repository",
        "Accountable governance owner role",
        "Decision authority",
        "Workstream / control domain",
        "Information classification",
        "Zero Secret Egress confirmation",
        "Decision acceptance and evidence",
    ),
}

ACTIVE_INTAKE_FILES: tuple[str, ...] = (
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "docs/BOS_BUSINESS_BUILDOUT.md",
    "Sovereign-Ops-Orchestrator/LINEAR_WIRING.md",
    ".github/RELEASE_HYGIENE.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/doc_update.md",
    ".github/ISSUE_TEMPLATE/strategy_proposal.md",
    ".github/ISSUE_TEMPLATE/bos_work_intake.yml",
    ".github/ISSUE_TEMPLATE/governance_legal_decision.yml",
)

LINEAR_CONTEXT_FILES: tuple[str, ...] = (
    "README.md",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
    "SUMMARY.md",
    "docs/BOS_BUSINESS_BUILDOUT.md",
    "docs/OPERATING_MODEL_LIFECYCLE_CONTROL_OWNERSHIP.md",
    "Sovereign-Ops-Orchestrator/LINEAR_WIRING.md",
)

LINEAR_CONTEXT_MARKERS: tuple[str, ...] = (
    "archive",
    "archived",
    "historical",
    "legacy",
    "migration",
    "deprecated",
    "provenance",
)

BANNED_ACTIVE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"linear[- ]first", re.IGNORECASE),
    re.compile(r"(?:must|required to|ensure|every pull request must)\s+.{0,50}linear issue", re.IGNORECASE),
    re.compile(r"(?:create|open|route)\s+(?:a|an|the|new)\s+linear (?:issue|item|ticket)", re.IGNORECASE),
    re.compile(r"linear\s+(?:is|remains)\s+(?:the\s+)?canonical", re.IGNORECASE),
)

FORBIDDEN_FORM_TERMS: tuple[str, ...] = (
    "linear.app/",
    "create a linear",
    "open a linear",
    "linear-first",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read(root: Path, relative_path: str, errors: list[str]) -> str | None:
    path = root / relative_path
    if not path.is_file():
        errors.append(f"Missing required file: {relative_path}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Cannot read {relative_path}: {exc}")
        return None


def _check_required_content(root: Path, errors: list[str]) -> None:
    for relative_path, required_fragments in REQUIRED_CONTENT.items():
        text = _read(root, relative_path, errors)
        if text is None:
            continue
        for fragment in required_fragments:
            if fragment.casefold() not in text.casefold():
                errors.append(
                    f"{relative_path}: missing required authority/control language: {fragment!r}"
                )


def _check_active_intake(root: Path, errors: list[str]) -> None:
    for relative_path in ACTIVE_INTAKE_FILES:
        text = _read(root, relative_path, errors)
        if text is None:
            continue
        for pattern in BANNED_ACTIVE_PATTERNS:
            match = pattern.search(text)
            if match:
                excerpt = " ".join(match.group(0).split())
                errors.append(
                    f"{relative_path}: active intake still requires Linear authority: {excerpt!r}"
                )

    issue_template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if not issue_template_dir.is_dir():
        errors.append("Missing issue-template directory: .github/ISSUE_TEMPLATE")
        return
    for path in sorted(issue_template_dir.iterdir()):
        if not path.is_file() or path.name == "config.yml":
            continue
        try:
            text = path.read_text(encoding="utf-8").casefold()
        except OSError as exc:
            errors.append(f"Cannot read {path.relative_to(root)}: {exc}")
            continue
        for forbidden in FORBIDDEN_FORM_TERMS:
            if forbidden in text:
                errors.append(
                    f"{path.relative_to(root)}: issue intake must not direct users to new Linear work ({forbidden!r})"
                )


def _check_linear_context(root: Path, errors: list[str]) -> None:
    for relative_path in LINEAR_CONTEXT_FILES:
        text = _read(root, relative_path, errors)
        if text is None:
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if "linear" not in line.casefold():
                continue
            start = max(0, index - 2)
            end = min(len(lines), index + 3)
            context = " ".join(lines[start:end]).casefold()
            if not any(marker in context for marker in LINEAR_CONTEXT_MARKERS):
                errors.append(
                    f"{relative_path}:{index + 1}: Linear reference must be explicitly historical/archive/migration context"
                )

    registry = _read(root, "docs/DOCUMENTATION_ALIGNMENT_INDEX.md", errors)
    if registry is not None:
        required_registry_context = (
            "Historical Linear issue-linking provenance",
            "Archived Linear migration proposals",
            "Do not create these as new canonical Linear documents",
        )
        for fragment in required_registry_context:
            if fragment.casefold() not in registry.casefold():
                errors.append(
                    "docs/DOCUMENTATION_ALIGNMENT_INDEX.md: "
                    f"missing archive context for retained Linear references: {fragment!r}"
                )


def main() -> int:
    root = repo_root()
    errors: list[str] = []

    _check_required_content(root, errors)
    _check_active_intake(root, errors)
    _check_linear_context(root, errors)

    if errors:
        print("GitHub-native BOS workspace verification: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GitHub-native BOS workspace verification: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
