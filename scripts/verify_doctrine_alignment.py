#!/usr/bin/env python3
"""Validate the deterministic CON-1530 doctrine and public-boundary surface."""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CON_1530_URL = (
    "https://linear.app/conxian-labs/issue/CON-1530/"
    "doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and"
)

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
    "docs/BUSINESS_ANALYSIS_2026-05-29.md",
    "conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md",
    "docs/CONXIAN_MARKET_NARRATIVE_ONE_PAGER.md",
    "docs/LINEAR_TASK_INVENTORY_2026-05-29.md",
    "docs/RESEARCH_FINDINGS_2026-05-29.md",
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
PUBLIC_SAFE_STUB_PATHS = (
    ROOT / "docs/ITIL5_STRATEGIC_ANALYSIS_2026.md",
    ROOT / "docs/BUSINESS_ANALYSIS_2026-05-29.md",
    ROOT / "conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md",
    ROOT / "docs/CONXIAN_MARKET_NARRATIVE_ONE_PAGER.md",
    ROOT / "docs/LINEAR_TASK_INVENTORY_2026-05-29.md",
    ROOT / "docs/RESEARCH_FINDINGS_2026-05-29.md",
)
PROHIBITED_DISPLAY_ALIASES = (
    "Conxian Gateway",
    "Conxius Enclave SDK",
    "conxius_orbit",
)
HISTORICAL_ALIAS_URL_PATHS = {
    "docs/bounties/CON-231_BOUNTY_CLASSIFICATION_2026-04-12.md",
}
AGENTS_ALIAS_EXCEPTION = ROOT / "AGENTS.md"


@dataclass(frozen=True)
class LinkReference:
    source: Path
    target: str
    line: int


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def split_table_row(line: str) -> list[str]:
    """Split a Markdown table row while preserving escaped pipes."""

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


def is_heading(line: str) -> bool:
    return bool(re.match(r"^\s{0,3}#{1,6}(?:\s|$)", line))


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(
        bool(re.fullmatch(r":?-+:?", cell.strip())) for cell in cells
    )


def parse_table_after_heading(
    text: str,
    heading: str,
    expected_headers: list[str] | None = None,
) -> tuple[list[str], list[list[str]]]:
    """Parse exactly one table directly owned by a heading."""

    lines = text.splitlines()
    heading_index = next(
        (index for index, line in enumerate(lines) if line.strip() == heading),
        None,
    )
    if heading_index is None:
        return [], []

    header_index: int | None = None
    for index in range(heading_index + 1, len(lines)):
        line = lines[index]
        if is_heading(line):
            break
        if not line.strip() or not line.strip().startswith("|"):
            continue
        header_index = index
        break
    if header_index is None or header_index + 1 >= len(lines):
        return [], []

    headers = split_table_row(lines[header_index])
    separator = split_table_row(lines[header_index + 1])
    if not is_table_separator(separator) or len(separator) != len(headers):
        return [], []
    if expected_headers is not None and headers != expected_headers:
        return headers, []

    rows: list[list[str]] = []
    for index in range(header_index + 2, len(lines)):
        line = lines[index]
        if is_heading(line) or not line.strip():
            break
        if not line.strip().startswith("|"):
            break
        rows.append(split_table_row(line))
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


def extract_code_path(cell: str) -> str | None:
    match = re.search(r"`([^`]+)`", cell)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith(("http://", "https://")):
        return None
    return value


def indexed_document_classifications(index_text: str) -> dict[str, set[str]]:
    """Extract visibility/classification markers from index tables and bullets."""

    result: dict[str, set[str]] = {}
    lines = index_text.splitlines()
    in_archival_section = False
    for line in lines:
        if line.strip() == "### Archival candidates":
            in_archival_section = True
            continue
        if in_archival_section and line.startswith("## "):
            in_archival_section = False
        if in_archival_section and line.startswith("-"):
            path_match = re.search(r"`([^`]+)`", line)
            if path_match:
                result.setdefault(path_match.group(1), set()).add("Archive candidate")
            continue
        if not line.strip().startswith("|"):
            continue
        cells = split_table_row(line)
        if not cells or cells[0] in {"Document", "README", "---"}:
            continue
        path = extract_code_path(cells[0])
        if not path:
            continue
        joined = " | ".join(cells)
        markers = result.setdefault(path, set())
        if "Public-safe stub" in joined:
            markers.add("Public-safe stub")
        if "Public-safe" in joined:
            markers.add("Public-safe")
        if "Internal-only" in joined:
            markers.add("Internal-only")
        if "Archive candidate" in joined:
            markers.add("Archive candidate")
    return result


def path_matches_index_pattern(relative: str, pattern: str) -> bool:
    pattern = pattern.rstrip("/")
    if pattern.endswith("/*"):
        return relative.startswith(pattern[:-1])
    return relative == pattern


def public_safe_markdown_paths(index_text: str) -> tuple[list[Path], int, int]:
    """Return the public-safe policy scope derived from the alignment index."""

    classifications = indexed_document_classifications(index_text)
    paths = tracked_markdown_paths()
    included: list[Path] = []
    excluded = 0
    explicit = 0
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        matches = [
            markers
            for pattern, markers in classifications.items()
            if path_matches_index_pattern(relative, pattern)
        ]
        markers = set().union(*matches) if matches else set()
        if matches:
            explicit += 1
        is_stub = "Public-safe stub" in markers
        if (
            ("Internal-only" in markers or "Archive candidate" in markers)
            and not is_stub
        ) or "/archive/" in f"/{relative}/":
            excluded += 1
            continue
        included.append(path)
    return included, excluded, explicit


def iter_markdown_links(text: str) -> list[tuple[str, int]]:
    """Return Markdown link destinations outside fenced code blocks."""

    links: list[tuple[str, int]] = []
    in_fence = False
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        links.extend((match.group(1), line_number) for match in pattern.finditer(line))
    return links


def github_heading_slug(value: str) -> str:
    """Generate the GitHub-style base slug for a Markdown heading."""

    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"!?(\[([^\]]+)\])\([^)]*\)", r"\2", value)
    value = re.sub(r"[`*_~]", "", value)
    value = unicodedata.normalize("NFKC", value).casefold()
    kept: list[str] = []
    for character in value:
        category = unicodedata.category(character)
        if category.startswith("P") or category.startswith("S"):
            kept.append(" ")
        else:
            kept.append(character)
    value = "".join(kept)
    value = re.sub(r"\s+", "-", value.strip())
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def heading_slugs(text: str) -> dict[str, list[int]]:
    """Return generated GitHub anchors, including duplicate suffixes."""

    counts: dict[str, int] = {}
    slugs: dict[str, list[int]] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = github_heading_slug(match.group(1))
        if not base:
            continue
        suffix = counts.get(base, 0)
        slug = base if suffix == 0 else f"{base}-{suffix}"
        counts[base] = suffix + 1
        slugs.setdefault(slug, []).append(line_number)
    return slugs


def resolve_local_fragment(path: Path, fragment: str) -> bool:
    fragment = unquote(fragment).lstrip("#")
    if not fragment:
        return True
    if not path.is_file():
        return False
    return fragment.casefold() in {slug.casefold() for slug in heading_slugs(path.read_text(encoding="utf-8"))}


def validate_local_links(errors: list[str], documents: dict[str, str]) -> int:
    checked = 0
    for name, text in documents.items():
        source = CANONICAL_PATHS[name]
        for target_value, line_number in iter_markdown_links(text):
            target = target_value.strip().strip("<>").split()[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "//")):
                continue
            checked += 1
            target_path_value, separator, fragment = target.partition("#")
            target_path_value = unquote(target_path_value)
            target_path = source if not target_path_value else (source.parent / target_path_value).resolve()
            try:
                target_path.relative_to(ROOT)
            except ValueError:
                fail(errors, f"canonical {name} link escapes repository at line {line_number}: {target}")
                continue
            if not target_path.exists():
                fail(errors, f"canonical {name} link target does not exist at line {line_number}: {target}")
                continue
            if separator and not resolve_local_fragment(target_path, fragment):
                fail(errors, f"canonical {name} link fragment does not resolve at line {line_number}: {target}")
    return checked


def alias_match_is_allowlisted(text: str, path: Path, start: int, end: int) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    # AGENTS.md is normative instruction text. Its legacy names are retained
    # only to identify the prohibited names that the policy itself bans.
    if path == AGENTS_ALIAS_EXCEPTION:
        return True
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


def scan_public_aliases(errors: list[str], index_text: str) -> tuple[int, int, int, int]:
    scanned = 0
    allowlisted = 0
    excluded = 0
    explicit = 0
    paths, excluded, explicit = public_safe_markdown_paths(index_text)
    for path in paths:
        scanned += 1
        text = path.read_text(encoding="utf-8")
        for alias in PROHIBITED_DISPLAY_ALIASES:
            for match in re.finditer(re.escape(alias), text, re.IGNORECASE):
                if alias_match_is_allowlisted(text, path, match.start(), match.end()):
                    allowlisted += 1
                    continue
                fail(errors, f"prohibited display alias in public Markdown {path.relative_to(ROOT)}: {match.group(0)}")
    return scanned, excluded, explicit, allowlisted


COMPANY_SUBJECT = r"(?:Conxian(?:-Labs)?(?:\s+\(Pty\)\s+Ltd)?|Conxian Labs|the company|company|SAB)"
SUBJECT_REFERENCE = rf"(?:{COMPANY_SUBJECT}|it|they)"
CUSTODY_OBJECT = r"(?:(?<!non-)custod(?:y|ial|ian)|treasur(?:y|ies)|vaults?|funds?|assets?|(?:discretionary\s+)?control\s+(?:over|of)?\s*(?:user|participant|customer|protocol)?\s*(?:funds?|assets?|treasury|vaults?|custody|state))"
AFFIRMATIVE_VERBS = r"(?:has|have|holds?|takes?|assumes?|provides?|exercises?|controls?|manages?|custodies?|is\s+responsible\s+for|acts?\s+as|is|are|will|can|may|shall)"
AFFIRMATIVE_OPERATION_VERBS = r"(?:has|have|holds?|takes?|assumes?|provides?|exercises?|custodies?|is\s+responsible\s+for|acts?\s+as|will|can|may|shall)"
AFFIRMATIVE_CUSTODY_PATTERNS = (
    re.compile(rf"\b{COMPANY_SUBJECT}(?:'s|[- ]controlled|[- ]owned)?\s+{CUSTODY_OBJECT}\b", re.IGNORECASE),
    re.compile(
        rf"\b{COMPANY_SUBJECT}\b[^.;\n|]*?\b{AFFIRMATIVE_VERBS}\b[^.;\n|]*?\b{CUSTODY_OBJECT}\b",
        re.IGNORECASE,
    ),
)
PRONOUN_AFFIRMATIVE_CUSTODY_PATTERN = re.compile(
    rf"\b(?:it|they)\b[^.;\n|]*?\b{AFFIRMATIVE_VERBS}\b[^.;\n|]*?\b{CUSTODY_OBJECT}\b",
    re.IGNORECASE,
)
EXPLICIT_NEGATION = re.compile(
    rf"(?:\b(?:does not mean|do not mean|doesn't mean|not|no|never|without|does not|do not|did not|will not|would not|cannot|can't|is not|are not)\b[^.;\n|]*\b{SUBJECT_REFERENCE}\b[^.;\n|]*\b{CUSTODY_OBJECT}\b|\b{SUBJECT_REFERENCE}\b[^.;\n|]*\b(?:does not mean|do not mean|doesn't mean|does not|do not|did not|will not|would not|cannot|can't|never|is not|are not|not)\b[^.;\n|]*\b{CUSTODY_OBJECT}\b)",
    re.IGNORECASE,
)
EXPLICIT_ALLOW_PATTERNS = (
    re.compile(r"\bnon[- ]custodial\b", re.IGNORECASE),
    re.compile(r"\b(?:avoid|avoidance|prevent|prevents|without|exclude|excludes|reject|rejects)\b[^.;\n|]*\bcustodial\b", re.IGNORECASE),
    re.compile(r"\buser(?:s)?\s+(?:retain|keep|maintain)\s+(?:control|custody)\b", re.IGNORECASE),
    re.compile(r"\buser(?:s)?\s+self[- ]custody\b", re.IGNORECASE),
    re.compile(r"\b(?:contract|protocol|vault)[- ](?:held|defined)\b", re.IGNORECASE),
    re.compile(r"\bprotocol[- ]level\s+(?:state|accounting|behavior)\b", re.IGNORECASE),
    re.compile(r"\bDAO\s+governance\b", re.IGNORECASE),
    re.compile(r"\bregulated[- ]partners?\b[^.;\n|]*\b(?:responsible for|retain|provide)\b[^.;\n|]*\bcustod", re.IGNORECASE),
)
RISK_DIRECT_NOUN = r"(?<!non-)(?:custod(?:y|ial|ian)|treasur(?:y|ies)|vaults?|funds?|assets?|control)"
RISK_VERB_NOUN = r"(?<!non-)(?:custod(?:y|ial|ian)|treasur(?:y|ies)|vaults?|funds?|assets?|controls?)"
RISK_REFERENCE_PATTERNS = (
    re.compile(
        rf"\b(?:risk|claim|wording|implication|boundary|contradiction|analysis)\b[^.;\n|]*\b{SUBJECT_REFERENCE}\b[^.;\n|]*\b{RISK_VERB_NOUN}\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b{SUBJECT_REFERENCE}(?:'s)?\s+{RISK_DIRECT_NOUN}\b[^.;\n|]*\b(?:risk|claim|wording|implication|boundary|contradiction)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:could|can|may|might|would)\s+be\s+(?:misread|mistaken|read|interpreted)\s+(?:as|for)\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b(?:could|can|may|might|would)\s+(?:imply|suggest|establish|be\s+read\s+as)\b[^.;\n|]*\b{SUBJECT_REFERENCE}(?:[- ]controlled)?\b[^.;\n|]*\b{RISK_VERB_NOUN}\b",
        re.IGNORECASE,
    ),
)
OPERATIONAL_AFFIRMATIVE_PATTERN = re.compile(
    rf"(?:\b{SUBJECT_REFERENCE}\b[^.;\n|]*?\b{AFFIRMATIVE_OPERATION_VERBS}\b[^.;\n|]*?\b{CUSTODY_OBJECT}\b|\b{SUBJECT_REFERENCE}\b[^.;\n|]*?\b(?:controls?|manages?)\s+(?:user|participant|customer|protocol)?\s*(?:funds?|assets?|treasury|vaults?|custody|state)\b)",
    re.IGNORECASE,
)


def split_policy_clauses(text: str) -> list[str]:
    return [clause.strip() for clause in re.split(r"[;\n|]", text) if clause.strip()]


def risk_reference_allows(clause: str) -> bool:
    if not any(pattern.search(clause) for pattern in RISK_REFERENCE_PATTERNS):
        return False
    has_affirmative_verb = bool(OPERATIONAL_AFFIRMATIVE_PATTERN.search(clause))
    if not has_affirmative_verb:
        return True
    # A sentence such as "the claim that the company controls funds is a
    # risk" or "company controls funds could be misread" is analysis. A
    # trailing label such as "company controls funds, a risk" is still an
    # affirmative claim and must not be exempted.
    return bool(
        RISK_REFERENCE_PATTERNS[0].search(clause)
        or RISK_REFERENCE_PATTERNS[2].search(clause)
        or RISK_REFERENCE_PATTERNS[3].search(clause)
    )


def custody_match_is_allowed(clause: str, match: re.Match[str]) -> bool:
    context_start = max(0, match.start() - 100)
    context_end = min(len(clause), match.end() + 100)
    context = clause[context_start:context_end]
    if clause.rstrip().endswith("?"):
        return True
    if EXPLICIT_NEGATION.search(context):
        return True
    # These patterns describe a risk, label, or possible misreading rather
    # than asserting that the company/SAB actually has custody or control.
    if risk_reference_allows(clause):
        return True
    if any(pattern.search(context) for pattern in EXPLICIT_ALLOW_PATTERNS):
        # An explicit affirmative company/SAB verb in the same clause wins
        # over a generic adjective such as "non-custodial".
        if OPERATIONAL_AFFIRMATIVE_PATTERN.search(clause):
            return bool(EXPLICIT_NEGATION.search(context))
        return True
    return False


def find_custody_violations(text: str) -> list[str]:
    violations: list[str] = []
    previous_clause_named_company = False
    for clause in split_policy_clauses(text):
        patterns = AFFIRMATIVE_CUSTODY_PATTERNS
        if previous_clause_named_company:
            patterns = (*patterns, PRONOUN_AFFIRMATIVE_CUSTODY_PATTERN)
        for pattern in patterns:
            for match in pattern.finditer(clause):
                if custody_match_is_allowed(clause, match):
                    continue
                phrase = match.group(0).strip()
                if phrase not in violations:
                    violations.append(phrase)
        previous_clause_named_company = bool(re.search(rf"\b{COMPANY_SUBJECT}\b", clause, re.IGNORECASE))
    return violations


def scan_custody_boundaries(errors: list[str], index_text: str) -> tuple[int, int, int]:
    checked = 0
    excluded = 0
    explicit = 0
    paths, excluded, explicit = public_safe_markdown_paths(index_text)
    for path in paths:
        checked += 1
        text = path.read_text(encoding="utf-8")
        for phrase in find_custody_violations(text):
            fail(errors, f"unqualified company/SAB custody or control phrase in {path.relative_to(ROOT)}: {phrase}")
    return checked, excluded, explicit


SENSITIVE_REPRESENTATIVE_PATTERNS = (
    re.compile(r"\b(?:TAM|SAM|SOM)\b", re.IGNORECASE),
    re.compile(r"\bpricing\s+(?:model|tier|point|strategy|doctrine)\b", re.IGNORECASE),
    re.compile(r"\b(?:revenue forecast|revenue runway|funding round|competitive landscape|market[- ]capture)\b", re.IGNORECASE),
    re.compile(r"\b(?:allocation|runway|task inventory)\b", re.IGNORECASE),
)


def validate_public_safe_stub(errors: list[str], path: Path) -> None:
    if not path.is_file():
        fail(errors, f"missing public-safe strategy stub: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    required = (
        "**Classification:** Public-safe stub",
        "**Ownership:** Conxian-Labs (Pty) Ltd",
        "**Why this content moved:**",
        CON_1530_URL,
        "DOCTRINE_ALIGNMENT_STANDARD.md",
        "PORTFOLIO_DOCTRINE_REGISTER.md",
        "DOCUMENTATION_ALIGNMENT_INDEX.md",
        "This file is intentionally kept as a public-safe stub",
    )
    for phrase in required:
        if phrase not in text:
            fail(errors, f"public-safe stub {path.relative_to(ROOT)} is missing: {phrase}")
    for pattern in SENSITIVE_REPRESENTATIVE_PATTERNS:
        if pattern.search(text):
            fail(errors, f"public-safe stub {path.relative_to(ROOT)} retains representative sensitive strategy content: {pattern.pattern}")


def validate_strategy_stubs(errors: list[str]) -> None:
    for path in PUBLIC_SAFE_STUB_PATHS:
        validate_public_safe_stub(errors, path)


def validate_standard(errors: list[str], standard: str) -> None:
    required_phrases = (
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
        "Conxian-Labs (Pty) Ltd",
        "Conxian",
        "Conxius",
        "CSF / Conxian Finance Protocol",
        "Fusion",
        "Nexus",
        "Current technical artifacts use exact repository slugs in backticks",
        "AGENTS.md is normative instruction text",
    )
    for phrase in required_phrases:
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


def validate_register(errors: list[str], register: str) -> tuple[list[str], list[list[str]]]:
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
    headers, rows = parse_table_after_heading(register, "## Registered repositories", expected_headers)
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
            tokens = classification_tokens(row[6])
            if not tokens or any(token not in CLASSIFICATION_VALUES for token in tokens):
                fail(errors, f"invalid document classification for {repository}: {row[6]}")
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

    expected_risk_headers = [
        "Artifact or surface",
        "Risk / contradiction",
        "Document classification",
        "Disposition",
        "Exact evidence pointer",
    ]
    risk_headers, risk_rows = parse_table_after_heading(register, "## High-risk contradictions and dispositions", expected_risk_headers)
    if risk_headers != expected_risk_headers:
        fail(errors, f"high-risk table has incorrect structural headers: {risk_headers}")
    if len(risk_rows) != len(HIGH_RISK_ARTIFACTS):
        fail(errors, f"high-risk table must contain exactly {len(HIGH_RISK_ARTIFACTS)} rows; found {len(risk_rows)}")
    risk_artifacts = [strip_code(row[0]) for row in risk_rows if row]
    if len(set(risk_artifacts)) != len(risk_artifacts):
        fail(errors, "high-risk table contains duplicate artifact rows")
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
        if any(not value.strip() for value in row):
            fail(errors, f"high-risk row {row_number} contains an empty required cell")
        if not any(marker in row[3] for marker in DISPOSITION_MARKERS):
            fail(errors, f"high-risk row {row_number} has no valid disposition: {row[3]}")
        tokens = classification_tokens(row[2])
        if not tokens or any(token not in CLASSIFICATION_VALUES for token in tokens):
            fail(errors, f"invalid high-risk document classification: {row[2]}")
        if not row[4].strip():
            fail(errors, f"high-risk row {row_number} is missing an exact evidence pointer")

    if "follow-up" not in register.lower() or "not company custody" not in register.lower():
        fail(errors, "portfolio register is missing explicit follow-up and non-company-custody boundaries")
    for path in (
        "docs/BUSINESS_ANALYSIS_2026-05-29.md",
        "conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md",
        "docs/CONXIAN_MARKET_NARRATIVE_ONE_PAGER.md",
        "docs/LINEAR_TASK_INVENTORY_2026-05-29.md",
        "docs/RESEARCH_FINDINGS_2026-05-29.md",
    ):
        if path not in register:
            fail(errors, f"portfolio register does not explicitly disposition sensitive surface: {path}")
    return repositories, risk_rows


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
    validate_standard(errors, standard)
    if "DOCTRINE_ALIGNMENT_STANDARD.md" not in index or "PORTFOLIO_DOCTRINE_REGISTER.md" not in index:
        fail(errors, "documentation index does not cross-link both doctrine canonical documents")
    repositories, risk_rows = validate_register(errors, register)
    validate_strategy_stubs(errors)
    link_count = validate_local_links(errors, documents)
    alias_count, excluded_count, explicit_count, allowlisted_alias_count = scan_public_aliases(errors, index)
    custody_count, custody_excluded_count, custody_explicit_count = scan_custody_boundaries(errors, index)

    if errors:
        print("Doctrine alignment check: FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Doctrine alignment check: OK")
    print(f"- canonical documents loaded: {len(documents)}")
    print(f"- structurally parsed repository rows: {len(repositories)} (expected {len(EXPECTED_REPOSITORIES)})")
    print(f"- high-risk dispositions validated: {len(risk_rows)}")
    print(f"- local Markdown links and fragments checked in canonical docs: {link_count}")
    print(f"- public-safe strategy stubs validated: {len(PUBLIC_SAFE_STUB_PATHS)}")
    print(f"- public Markdown display-alias scope: {alias_count} files; explicitly indexed: {explicit_count}; excluded internal/archive: {excluded_count}; AGENTS.md normative exception and historical URL allowlist entries: {allowlisted_alias_count}")
    print(f"- company/SAB custody-boundary scope: {custody_count} files; explicitly indexed: {custody_explicit_count}; excluded internal/archive: {custody_excluded_count}; protocol/contract state, DAO governance, user self-custody, and regulated-partner custody are explicit allowances")
    return 0


if __name__ == "__main__":
    sys.exit(main())
