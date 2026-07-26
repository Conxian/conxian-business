#!/usr/bin/env python3
"""Enforce a minimum canonical surface for GitHub-native BOS authority.

The guard is intentionally bounded to active intake/templates and named policy
surfaces. It fails closed on those surfaces; review is still required for
historical documents outside this minimum scope.
"""

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
        "GitHub Issues and pull requests are authoritative for new BOS work",
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
    "AGENTS.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "docs/BOS_BUSINESS_BUILDOUT.md",
    "Sovereign-Ops-Orchestrator/LINEAR_WIRING.md",
    ".github/RELEASE_HYGIENE.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/weekly-viability-report.yml",
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

HISTORICAL_CONTEXT_MARKERS: tuple[str, ...] = (
    "archive",
    "archived",
    "historical",
    "legacy",
    "migration",
    "deprecated",
    "provenance",
)

ACTIVE_LINEAR_MANDATE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Linear-first policy", re.compile(r"\blinear[- ]first\b", re.IGNORECASE)),
    (
        "new/current work is required to use Linear",
        re.compile(
            r"\b(?:all\s+)?(?:new|current|active)\b.{0,80}"
            r"\b(?:must|shall)\s+(?!not\b).{0,80}\blinear\b",
            re.IGNORECASE,
        ),
    ),
    (
        "mandatory Linear ticket or record",
        re.compile(
            r"\blinear\b.{0,50}\b(?:ticket|issue|item|record)?\s*"
            r"(?:is\s+)?(?:required|mandatory)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "mandatory use of Linear",
        re.compile(
            r"\b(?:must|shall)\s+(?!not\b).{0,50}"
            r"\b(?:use|create|open|route|track|coordinat(?:e|ed)|record(?:ed)?)\b"
            r".{0,40}\blinear\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Linear mandated for active work",
        re.compile(
            r"\blinear\b.{0,40}\b(?:must|shall)\s+(?!not\b).{0,60}"
            r"\b(?:use|used|route|routed|track|tracked|coordinat(?:e|ed)|govern)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "imperative Linear intake directive",
        re.compile(
            r"\b(?:create|open|track)\s+(?:(?:all|new|current|active|a|an|the)\s+)?"
            r"linear\s+(?:issues?|items?|tickets?|records?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "work routed through Linear",
        re.compile(
            r"\broute\s+(?:(?:all|new|current|active)\s+)?work\s+through\s+linear\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Linear declared current authority",
        re.compile(
            r"\blinear\b\s+(?:is|remains)\s+(?:the\s+)?"
            r"(?:required|mandatory|canonical|authoritative|source\s+of\s+truth)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "sensitive records routed to Linear",
        re.compile(
            r"\b(?:keep|store|route|record|maintain)\b.{0,100}"
            r"\b(?:sensitive|restricted|protected)\b.{0,100}\blinear\b",
            re.IGNORECASE,
        ),
    ),
)

REQUIRED_ISSUE_FORM_AUTHORITY: dict[str, str] = {
    ".github/ISSUE_TEMPLATE/bos_work_intake.yml": (
        "GitHub Issues and pull requests are authoritative for new BOS work"
    ),
    ".github/ISSUE_TEMPLATE/governance_legal_decision.yml": (
        "GitHub Issues and pull requests are authoritative for new BOS work"
    ),
}

ISSUE_TEMPLATE_SUFFIXES: frozenset[str] = frozenset({".md", ".yml", ".yaml"})

NON_AUTHORITY_LINEAR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\b(?:do\s+not|never)\b.{0,120}\blinear\b", re.IGNORECASE),
    re.compile(r"\blinear\b.{0,120}\b(?:must|shall)\s+not\b", re.IGNORECASE),
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


def _linear_units(text: str) -> list[tuple[int, str]]:
    """Return sentence- or line-sized units containing a Linear reference."""
    units: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "linear" not in line.casefold():
            continue
        sentences = re.split(r"(?<=[.!?])\s+", line.strip())
        units.extend(
            (line_number, sentence.strip())
            for sentence in sentences
            if "linear" in sentence.casefold()
        )
    return units


def _normalized_markdown_units(text: str) -> list[tuple[int, int, str]]:
    """Return normalized paragraph/list-item units with their source line span."""
    units: list[tuple[int, int, str]] = []
    buffered: list[str] = []
    start_line = 0
    end_line = 0
    list_item_pattern = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")

    def flush() -> None:
        nonlocal buffered, start_line, end_line
        if buffered:
            units.append((start_line, end_line, " ".join(" ".join(buffered).split())))
        buffered = []
        start_line = 0
        end_line = 0

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if buffered and list_item_pattern.match(line):
            flush()
        if not buffered:
            start_line = line_number
        buffered.append(stripped)
        end_line = line_number
    flush()
    return units


def _active_mandate_reason(unit: str) -> str | None:
    for sentence in re.split(r"(?<=[.!?])\s+", unit):
        if _is_explicit_linear_non_authority(sentence):
            continue
        for reason, pattern in ACTIVE_LINEAR_MANDATE_PATTERNS:
            if pattern.search(sentence):
                return reason
    return None


def _is_explicit_linear_non_authority(unit: str) -> bool:
    return any(pattern.search(unit) for pattern in NON_AUTHORITY_LINEAR_PATTERNS)


def _check_active_linear_mandates(
    relative_path: str, text: str, errors: list[str]
) -> None:
    for line_number, unit in _linear_units(text):
        reason = _active_mandate_reason(unit)
        if reason is None:
            continue
        excerpt = " ".join(unit.split())
        errors.append(
            f"{relative_path}:{line_number}: active intake requires Linear "
            f"({reason}): {excerpt!r}"
        )


def _check_active_intake(root: Path, errors: list[str]) -> None:
    for relative_path in ACTIVE_INTAKE_FILES:
        text = _read(root, relative_path, errors)
        if text is None:
            continue
        _check_active_linear_mandates(relative_path, text, errors)

    issue_template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if not issue_template_dir.is_dir():
        errors.append("Missing issue-template directory: .github/ISSUE_TEMPLATE")
        return
    for path in sorted(issue_template_dir.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in ISSUE_TEMPLATE_SUFFIXES:
            continue
        relative_path = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"Cannot read {relative_path}: {exc}")
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "linear" not in line.casefold():
                continue
            excerpt = " ".join(line.split())
            errors.append(
                f"{relative_path}:{line_number}: active issue templates must not "
                f"reference Linear: {excerpt!r}"
            )

    for relative_path, authority_text in REQUIRED_ISSUE_FORM_AUTHORITY.items():
        text = _read(root, relative_path, errors)
        if text is not None and authority_text.casefold() not in text.casefold():
            errors.append(
                f"{relative_path}: missing required GitHub-authority language: "
                f"{authority_text!r}"
            )


def _check_linear_context(root: Path, errors: list[str]) -> None:
    for relative_path in LINEAR_CONTEXT_FILES:
        text = _read(root, relative_path, errors)
        if text is None:
            continue
        precise_active_lines: set[int] = set()
        for line_number, unit in _linear_units(text):
            reason = _active_mandate_reason(unit)
            if reason is None:
                continue
            precise_active_lines.add(line_number)
            excerpt = " ".join(unit.split())
            errors.append(
                f"{relative_path}:{line_number}: active Linear mandate cannot be "
                f"treated as historical ({reason}): {excerpt!r}"
            )

        active_spans: list[tuple[int, int]] = []
        for start_line, end_line, unit in _normalized_markdown_units(text):
            if "linear" not in unit.casefold():
                continue
            reason = _active_mandate_reason(unit)
            if reason is None or any(
                start_line <= line_number <= end_line
                for line_number in precise_active_lines
            ):
                continue
            active_spans.append((start_line, end_line))
            errors.append(
                f"{relative_path}:{start_line}: active Linear mandate cannot be "
                f"treated as historical ({reason}): {unit!r}"
            )
        for line_number, unit in _linear_units(text):
            if line_number in precise_active_lines or any(
                start <= line_number <= end for start, end in active_spans
            ):
                continue
            if _is_explicit_linear_non_authority(unit):
                continue
            context = unit.casefold()
            if not any(marker in context for marker in HISTORICAL_CONTEXT_MARKERS):
                errors.append(
                    f"{relative_path}:{line_number}: Linear reference must be explicitly "
                    "historical/archive/migration context in the same sentence or field"
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
