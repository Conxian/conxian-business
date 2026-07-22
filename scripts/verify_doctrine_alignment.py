#!/usr/bin/env python3
"""Validate the deterministic CON-1530 doctrine and public-boundary surface."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_REPOSITORIES = (
    "Conxian/.github-private",
    "Conxian/.github",
    "Conxian/Conxian",
    "Conxian/conxian_ui",
    "Conxian/conxius-orbit",
    "Conxian/conxius-wallet",
    "Conxian/conxian-labs-site",
    "Conxian/conxian-gateway",
    "Conxian/lib-conxian-core",
    "Conxian/conxius-platform",
    "Conxian/conxian-nexus",
    "Conxian/conxian-business",
    "Conxian/conxius-enclave-sdk",
    "Conxian/demo-repository",
    "Conxian/conxian.github.io",
    "Conxian/conxian_market",
)

OPERATING_LABELS = {
    "Production intent",
    "Reference implementation",
    "Research/experimental",
    "Internal only",
}
MATURITY_VALUES = {"Incubating", "Beta", "Stable", "Deprecated", "N/A"}
CLAIM_STATE_VALUES = {"Implemented", "Verified", "Target-state", "Deprecated"}
CLAIM_NA_EXCEPTION = "N/A — no public claim"
CLASSIFICATION_VALUES = {
    "Canonical",
    "Supporting",
    "Public-safe",
    "Public-safe stub",
    "Internal-only",
    "Deprecated",
    "Archive candidate",
}
DISPOSITION_MARKERS = (
    "Changed locally",
    "External follow-up required; link after issue creation",
    "No contradiction observed",
    "Evidence not verified",
)
HIGH_RISK_ARTIFACTS = (
    "Conxian/docs/WHITEPAPER.md",
    "Conxian/conxian_market/README.md",
    "docs/ITIL5_STRATEGIC_ANALYSIS_2026.md",
    "Top-level READMEs",
    "Company custody, treasury, or signer-control wording",
    "Protocol escrow, settlement, treasury, or yield descriptions",
    "Competitive or market-capture narratives",
    "User-data extraction implications",
)
CANONICAL_PATHS = {
    "standard": ROOT / "docs/DOCTRINE_ALIGNMENT_STANDARD.md",
    "register": ROOT / "docs/PORTFOLIO_DOCTRINE_REGISTER.md",
    "index": ROOT / "docs/DOCUMENTATION_ALIGNMENT_INDEX.md",
}
ITIL_STUB_PATH = ROOT / "docs/ITIL5_STRATEGIC_ANALYSIS_2026.md"
CUSTODY_BOUNDARY_PATHS = (
    ROOT / "README.md",
    ROOT / "docs/DOCTRINE_ALIGNMENT_STANDARD.md",
    ROOT / "docs/PORTFOLIO_DOCTRINE_REGISTER.md",
    ROOT / "docs/PORTFOLIO_BUSINESS_UNIT_MAP.md",
    ROOT / "docs/BOS_BUSINESS_BUILDOUT.md",
    ROOT / "docs/BOS_WALLET_CONTROL_MODEL.md",
    ROOT / "docs/SAB_DAO_HANDOFF_PROTOCOL.md",
    ROOT / "docs/PARTNER_OVERVIEW_AND_LAUNCH_FAQ.md",
    ROOT / "docs/PUBLIC_VISIBILITY_AUDIT_REPORT.md",
    ROOT / "docs/REPO_READINESS_GATES_BY_CONTROL_DOMAIN.md",
    ROOT / "docs/SAB_WALLET_ARCHITECTURE_AND_CONTROL_MATRIX.md",
    ROOT / "docs/WALLET_SIGNER_CONTROL_VERIFICATION_REPORT.md",
    ROOT / "docs/architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md",
    ROOT / "docs/architecture/BOS_TREASURY_AND_YIELD_INTEGRATION_ARCHITECTURE.md",
    ROOT / "conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md",
)
PROHIBITED_DISPLAY_ALIASES = (
    "Conxian Gateway",
    "Conxius Enclave SDK",
    "conxius_orbit",
)
HISTORICAL_ALIAS_URL_PATHS = {
    "docs/bounties/CON-231_BOUNTY_CLASSIFICATION_2026-04-12.md",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def split_table_row(line: str) -> list[str]:
    """Split a simple Markdown table row, preserving escaped pipes."""

    content = line.strip()
    if content.startswith("|"):
        content = content[1:]
    if content.endswith("|"):
        content = content[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in content:
        if character == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(character)
        escaped = character == "\\" and not escaped
        if character != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def parse_table_after_heading(text: str, heading: str) -> tuple[list[str], list[list[str]]]:
    lines = text.splitlines()
    heading_index = next(
        (index for index, line in enumerate(lines) if line.strip() == heading),
        None,
    )
    if heading_index is None:
        return [], []

    header_index = next(
        (
            index
            for index in range(heading_index + 1, len(lines))
            if lines[index].strip().startswith("|")
        ),
        None,
    )
    if header_index is None or header_index + 1 >= len(lines):
        return [], []
    headers = split_table_row(lines[header_index])
    separator = split_table_row(lines[header_index + 1])
    if not separator or not all(set(cell.replace(":", "").strip()) <= {"-"} for cell in separator):
        return [], []

    rows: list[list[str]] = []
    for line in lines[header_index + 2 :]:
        if not line.strip().startswith("|"):
            break
        row = split_table_row(line)
        if row:
            rows.append(row)
    return headers, rows


def classification_tokens(value: str) -> list[str]:
    tokens: list[str] = []
    for token in value.split(";"):
        token = token.strip()
        token = re.sub(r"\s*\([^)]*\)$", "", token)
        if token:
            tokens.append(token)
    return tokens


def tracked_markdown_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md", "*.markdown"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=False,
    )
    return [ROOT / item for item in result.stdout.decode().split("\0") if item]


def alias_match_is_allowlisted(text: str, path: Path, start: int, end: int) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    # A repository filename in a Markdown link destination is not rendered
    # display text, even when the historical filename contains an underscore.
    link_open = text.rfind("](", 0, start)
    link_close = text.find(")", link_open + 2) if link_open != -1 else -1
    if link_open != -1 and link_open < start and end <= link_close:
        return True
    code_open = text.rfind("`", 0, start)
    code_close = text.find("`", start)
    if code_open != -1 and code_close != -1 and end <= code_close:
        code_value = text[code_open + 1 : code_close]
        if "/" in code_value and re.search(r"\.(?:md|markdown)$", code_value, re.IGNORECASE):
            return True
    if relative not in HISTORICAL_ALIAS_URL_PATHS:
        return False
    for match in re.finditer(r"https?://[^\s)]+", text):
        if match.start() <= start and end <= match.end():
            return "linear.app" in match.group(0)
    return False


def scan_public_aliases(errors: list[str]) -> tuple[int, int]:
    scanned = 0
    allowlisted = 0
    for path in tracked_markdown_paths():
        if path.name == "AGENTS.md":
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        for alias in PROHIBITED_DISPLAY_ALIASES:
            for match in re.finditer(re.escape(alias), text, re.IGNORECASE):
                if alias_match_is_allowlisted(text, path, match.start(), match.end()):
                    allowlisted += 1
                    continue
                fail(
                    errors,
                    f"prohibited display alias in public Markdown {path.relative_to(ROOT)}: {match.group(0)}",
                )
    return scanned, allowlisted


def validate_local_links(errors: list[str], documents: dict[str, str]) -> int:
    checked = 0
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for name, text in documents.items():
        source = CANONICAL_PATHS[name]
        for match in pattern.finditer(text):
            target = match.group(1).strip().strip("<>").split()[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "//", "#")):
                continue
            checked += 1
            target_path = unquote(target.split("#", 1)[0])
            if not target_path:
                continue
            resolved = (source.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"canonical {name} link escapes repository: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"canonical {name} link target does not exist: {target}")
    return checked


def is_negated_or_qualified(text: str, start: int, end: int) -> bool:
    sentence_start = max(
        text.rfind("\n", 0, start),
        text.rfind(".", 0, start),
        text.rfind(";", 0, start),
        text.rfind("|", 0, start),
        text.rfind("?", 0, start),
    )
    sentence_end_candidates = [
        position
        for position in (
            text.find("\n", end),
            text.find(".", end),
            text.find(";", end),
            text.find("|", end),
            text.find("?", end),
        )
        if position != -1
    ]
    sentence_end = min(sentence_end_candidates, default=len(text))
    context = text[sentence_start + 1 : sentence_end + 1]
    if "?" in context:
        return True
    patterns = (
        r"\b(?:not|no|never|without|non[- ]custodial|user[- ]controlled|protocol[- ]level|contract[- ]held|contract principals?|DAO|regulated partner|target[- ]state|temporary|bounded|outside Git)\b",
        r"\b(?:does|do|did|will|would)\s+not\b",
        r"\b(?:can|could|may|might)\s+be\s+(?:misread|mistaken|read|interpreted)\b",
        r"\b(?:can|could|may|might)\s+(?:imply|suggest|establish)\b",
        r"\b(?:not|no)\s+(?:a\s+)?(?:claim|authority|custody|control)\b",
        r"\b(?:risk|contradiction|boundary|wording)\b",
    )
    return any(re.search(pattern, context, re.IGNORECASE) for pattern in patterns)


def scan_custody_boundaries(errors: list[str]) -> int:
    patterns = (
        re.compile(r"\b(?:Conxian(?:-Labs)?|company)(?:'s|[- ]controlled|[- ]owned)?\s+(?:custody|custodian|treasury|vaults?|funds?)\b", re.IGNORECASE),
        re.compile(r"\bSAB(?:'s|[- ]controlled|[- ]owned)?\s+(?:custody|treasury|vaults?|funds?)\b", re.IGNORECASE),
        re.compile(r"\b(?:Conxian(?:-Labs)?|company|SAB)\s+(?:may|can|will|does)\s+(?:exercise\s+)?(?:discretionary\s+)?(?:custody|control|manage|hold)\b", re.IGNORECASE),
    )
    checked = 0
    for path in CUSTODY_BOUNDARY_PATHS:
        if not path.is_file():
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            for match in pattern.finditer(text):
                if is_negated_or_qualified(text, match.start(), match.end()):
                    continue
                fail(
                    errors,
                    f"unqualified company/SAB custody or control phrase in {path.relative_to(ROOT)}: {match.group(0)}",
                )
    return checked


def validate_itil_stub(errors: list[str]) -> None:
    if not ITIL_STUB_PATH.is_file():
        fail(errors, "missing ITIL public-safe stub")
        return
    text = ITIL_STUB_PATH.read_text(encoding="utf-8")
    required = (
        "# ITIL5 Strategic Analysis 2026",
        "**Classification:** Public-safe stub",
        "**Operating label:** Internal only",
        "**Maturity / claim state:** Deprecated",
        "authorized Linear workspace",
        "This public-safe stub intentionally retains no sensitive strategy text.",
    )
    for phrase in required:
        if phrase not in text:
            fail(errors, f"ITIL stub is missing required structure or boundary phrase: {phrase}")
    representative_strategy = re.compile(
        r"\b(?:market[- ]capture|competitive strategy|competitive analysis|TAM|SAM|pricing model|revenue forecast|competitor map)\b",
        re.IGNORECASE,
    )
    if representative_strategy.search(text):
        fail(errors, "ITIL stub contains representative market-capture or competitive-strategy content")


def main() -> int:
    errors: list[str] = []
    documents: dict[str, str] = {}
    for name, path in CANONICAL_PATHS.items():
        if not path.is_file():
            fail(errors, f"missing canonical document: {path.relative_to(ROOT)}")
            continue
        documents[name] = path.read_text(encoding="utf-8")

    standard = documents.get("standard", "")
    register = documents.get("register", "")
    index = documents.get("index", "")

    for phrase in (
        "non-custodial software and infrastructure builder/operator",
        "not a market participant",
        "not a user-data extraction business",
        "protocol-level state transitions",
        "Implemented",
        "Verified",
        "Target-state",
        "Deprecated",
        "Production intent",
        "Reference implementation",
        "Research/experimental",
        "Internal only",
        "Canonical",
        "Supporting",
        "Public-safe",
        "Public-safe stub",
        "Internal-only",
        "Archive candidate",
    ):
        if phrase not in standard:
            fail(errors, f"doctrine standard is missing required phrase: {phrase}")

    for anchor in (
        "TRUST_AND_PROOF_MESSAGING.md",
        "CLAIM_EVIDENCE_MATRIX.md",
        "PORTFOLIO_BUSINESS_UNIT_MAP.md",
        "BOUNDARY_DECISION_LOG.md",
        "TECHNICAL_WHITEPAPER_OUTLINE.md",
    ):
        if anchor not in standard:
            fail(errors, f"doctrine standard does not link canonical anchor: {anchor}")

    for link in (
        "DOCTRINE_ALIGNMENT_STANDARD.md",
        "PORTFOLIO_DOCTRINE_REGISTER.md",
    ):
        if link not in index:
            fail(errors, f"documentation index does not cross-link: {link}")

    expected_headers = [
        "Repository",
        "One-sentence role",
        "Audience",
        "Operating label",
        "Maturity",
        "Claim state",
        "Document classification",
        "Contradiction / disposition",
        "Exact evidence pointer",
    ]
    headers, rows = parse_table_after_heading(register, "## Registered repositories")
    if headers != expected_headers:
        fail(errors, f"portfolio register has incorrect structural headers: {headers}")
    if len(rows) != len(EXPECTED_REPOSITORIES):
        fail(errors, f"portfolio register must contain exactly {len(EXPECTED_REPOSITORIES)} repository rows; found {len(rows)}")

    repositories: list[str] = []
    if headers == expected_headers:
        for row_number, row in enumerate(rows, start=1):
            if len(row) != len(expected_headers):
                fail(errors, f"portfolio register row {row_number} has {len(row)} columns; expected {len(expected_headers)}")
                continue
            repository = strip_code(row[0])
            repositories.append(repository)
            for column, value in zip(expected_headers, row):
                if not value.strip():
                    fail(errors, f"portfolio register row {row_number} has an empty {column} column")
            if row[3] not in OPERATING_LABELS:
                fail(errors, f"invalid operating label for {repository}: {row[3]}")
            if row[4] not in MATURITY_VALUES:
                fail(errors, f"invalid maturity for {repository}: {row[4]}")
            if row[5] not in CLAIM_STATE_VALUES and row[5] != CLAIM_NA_EXCEPTION:
                fail(errors, f"invalid claim state for {repository}: {row[5]}")
            if row[5] == CLAIM_NA_EXCEPTION and repository != "Conxian/.github-private":
                fail(errors, f"N/A claim-state exception is only allowed for Conxian/.github-private: {repository}")
            for token in classification_tokens(row[6]):
                if token not in CLASSIFICATION_VALUES:
                    fail(errors, f"invalid document classification for {repository}: {token}")
            if not any(marker in row[7] for marker in DISPOSITION_MARKERS):
                fail(errors, f"invalid contradiction/disposition for {repository}: {row[7]}")
            if not re.search(r"(?:\.md|README\.md|register|submodule|repository|canonical)", row[8], re.IGNORECASE):
                fail(errors, f"evidence pointer is not exact/path-based for {repository}: {row[8]}")

    if len(set(repositories)) != len(repositories):
        fail(errors, "portfolio register contains duplicate repository rows")
    if set(repositories) != set(EXPECTED_REPOSITORIES):
        missing = sorted(set(EXPECTED_REPOSITORIES) - set(repositories))
        unexpected = sorted(set(repositories) - set(EXPECTED_REPOSITORIES))
        if missing:
            fail(errors, f"portfolio register is missing repository rows: {', '.join(missing)}")
        if unexpected:
            fail(errors, f"portfolio register contains unexpected repository rows: {', '.join(unexpected)}")
    if CLAIM_NA_EXCEPTION not in register:
        fail(errors, "portfolio register does not document the N/A-no-public-claim exception")

    risk_headers, risk_rows = parse_table_after_heading(
        register,
        "## High-risk contradictions and dispositions",
    )
    expected_risk_headers = [
        "Artifact or surface",
        "Risk / contradiction",
        "Document classification",
        "Disposition",
        "Exact evidence pointer",
    ]
    if risk_headers != expected_risk_headers:
        fail(errors, f"high-risk table has incorrect structural headers: {risk_headers}")
    risk_artifacts = [strip_code(row[0]) for row in risk_rows if row]
    if set(risk_artifacts) != set(HIGH_RISK_ARTIFACTS):
        missing = sorted(set(HIGH_RISK_ARTIFACTS) - set(risk_artifacts))
        unexpected = sorted(set(risk_artifacts) - set(HIGH_RISK_ARTIFACTS))
        if missing:
            fail(errors, f"high-risk table is missing artifacts: {', '.join(missing)}")
        if unexpected:
            fail(errors, f"high-risk table contains unexpected artifacts: {', '.join(unexpected)}")
    for row_number, row in enumerate(risk_rows, start=1):
        if len(row) != len(expected_risk_headers):
            fail(errors, f"high-risk row {row_number} has {len(row)} columns; expected {len(expected_risk_headers)}")
            continue
        if not any(marker in row[3] for marker in DISPOSITION_MARKERS):
            fail(errors, f"high-risk row {row_number} has no valid disposition: {row[3]}")
        for token in classification_tokens(row[2]):
            if token not in CLASSIFICATION_VALUES:
                fail(errors, f"invalid high-risk document classification: {token}")
        if not row[4].strip():
            fail(errors, f"high-risk row {row_number} is missing an exact evidence pointer")
    whitepaper_rows = [row for row in risk_rows if row and "WHITEPAPER.md" in row[0]]
    if not whitepaper_rows or not any(
        "Archive candidate" in row[2] and "rewrite" in row[3].lower() for row in whitepaper_rows
    ):
        fail(errors, "old whitepaper is not classified as an archive/rewrite candidate")

    if "follow-up" not in register.lower() or "not company custody" not in register.lower():
        fail(errors, "portfolio register is missing explicit follow-up and non-company-custody boundaries")

    validate_itil_stub(errors)
    link_count = validate_local_links(errors, documents)
    markdown_count, allowlisted_alias_count = scan_public_aliases(errors)
    custody_count = scan_custody_boundaries(errors)

    if errors:
        print("Doctrine alignment check: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Doctrine alignment check: OK")
    print(f"- canonical documents loaded: {len(documents)}")
    print(f"- structurally parsed repository rows: {len(repositories)} (expected {len(EXPECTED_REPOSITORIES)})")
    print(f"- high-risk dispositions validated: {len(risk_rows)}")
    print(f"- local Markdown links checked in canonical docs: {link_count}")
    print("- ITIL public-safe stub structure and strategy-content exclusion: OK")
    print(
        f"- public Markdown display-alias scan: {markdown_count} files; "
        f"AGENTS.md normative text excluded; non-display link/URL allowlist entries: {allowlisted_alias_count}"
    )
    print(
        f"- company/SAB custody-boundary scan: {custody_count} canonical/public-safe docs; "
        "protocol escrow, DAO governance, user self-custody, and regulated-partner custody remain permitted"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
