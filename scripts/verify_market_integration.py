#!/usr/bin/env python3
"""Verify conxian-market BOS integration and dependency wiring.

Validates that:
1. conxian_market is properly registered in BOS_KNOWLEDGE_FRAMEWORK.md
2. Cross-repo dependencies are documented in CROSS_REPO_DEPENDENCY_MAP.md
3. Market submodule is accessible (manually cloned)
4. Critical issues (CON-1427, CON-1425) are tracked
"""

import subprocess
import sys
import re
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
BOS_FRAMEWORK = REPO_ROOT / "docs" / "BOS_KNOWLEDGE_FRAMEWORK.md"
DEPENDENCY_MAP = REPO_ROOT / "docs" / "CROSS_REPO_DEPENDENCY_MAP.md"
MARKET_SUBMODULE = REPO_ROOT / "conxian-market"


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def run(cmd: list[str], cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO_ROOT)


def print_header(text: str) -> None:
    print(f"\n{Colors.BLUE}=== {text} ==={Colors.RESET}\n")


def print_success(text: str) -> None:
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str) -> None:
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text: str) -> None:
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def check_bos_framework_registration() -> list[str]:
    """Verify conxian-market is registered in BOS Knowledge Framework."""
    errors = []

    print_header("BOS Framework Registration Check")

    if not BOS_FRAMEWORK.exists():
        errors.append(f"BOS_KNOWLEDGE_FRAMEWORK.md not found at {BOS_FRAMEWORK}")
        return errors

    content = BOS_FRAMEWORK.read_text()

    # Check for conxian-market entry
    if 'conxian-market:' in content or '"conxian-market"' in content:
        print_success("conxian-market entry found in BOS framework")
    else:
        errors.append("conxian-market not registered in BOS_KNOWLEDGE_FRAMEWORK.md")
        return errors

    # Check for REPO-008 ID
    if re.search(r'id:\s*REPO-008', content):
        print_success("REPO-008 ID assigned to conxian-market")
    else:
        errors.append("REPO-008 ID not found for conxian-market")

    # Check for type
    if re.search(r'type:\s*marketplace', content):
        print_success("Type 'marketplace' assigned")
    else:
        errors.append("Type 'marketplace' not found for conxian-market")

    # Check for critical issues tracking
    if 'CON-1427' in content and 'CON-1425' in content:
        print_success("Critical issues (CON-1427, CON-1425) tracked in framework")
    else:
        errors.append("Critical issues CON-1427/CON-1425 not found in framework")

    # Check for 80/10/10 revenue matrix
    if '80/10/10' in content or 'revenue_matrix' in content:
        print_success("Revenue matrix (80/10/10) documented")
    else:
        errors.append("Revenue matrix not found")

    return errors


def check_dependency_map() -> list[str]:
    """Verify cross-repo dependency map exists and is properly structured."""
    errors = []

    print_header("Cross-Repo Dependency Map Check")

    if not DEPENDENCY_MAP.exists():
        errors.append(f"CROSS_REPO_DEPENDENCY_MAP.md not found at {DEPENDENCY_MAP}")
        return errors

    print_success("Dependency map exists")

    content = DEPENDENCY_MAP.read_text()

    # Check for key dependencies
    required_deps = [
        ('conxian-nexus', 'State verification'),
        ('conxian-gateway', 'Settlement rails'),
        ('conxius-wallet', 'User settlement'),
        ('conxius-platform', 'Builder sandbox'),
        ('lib-conxian-core', 'Crypto primitives'),
    ]

    for dep, desc in required_deps:
        if dep in content:
            print_success(f"{dep} dependency documented ({desc})")
        else:
            errors.append(f"{dep} dependency not documented")

    # Check for critical path section
    if 'CON-1427' in content and 'Revenue Capture' in content:
        print_success("Revenue capture path documented with blockers")
    else:
        print_warning("Revenue capture path may be incomplete")

    return errors


def check_market_submodule() -> list[str]:
    """Verify conxian-market submodule is accessible."""
    errors = []

    print_header("Market Submodule Check")

    if not MARKET_SUBMODULE.exists():
        errors.append("conxian-market directory does not exist")
        return errors

    print_success("conxian-market directory exists")

    # Check for README
    readme = MARKET_SUBMODULE / "README.md"
    if readme.exists():
        print_success("README.md found")
        content = readme.read_text()
        if 'Marketplace' in content or 'marketplace' in content:
            print_success("Marketplace content verified")
        else:
            print_warning("README may not contain marketplace content")
    else:
        errors.append("README.md not found in conxian-market")

    # Check for ROADMAP
    roadmap = MARKET_SUBMODULE / "ROADMAP.md"
    if roadmap.exists():
        print_success("ROADMAP.md found")
        content = roadmap.read_text()
        if 'Phase' in content and '80/10/10' in content:
            print_success("Phase structure and yield matrix documented")
    else:
        errors.append("ROADMAP.md not found in conxian-market")

    # Check for docs/research
    docs_dir = MARKET_SUBMODULE / "docs"
    if docs_dir.exists():
        print_success("docs/ directory found")
        research_dir = docs_dir / "research"
        if research_dir.exists():
            print_success("docs/research/ directory found")
            research_files = list(research_dir.glob("*.md"))
            print(f"  Found {len(research_files)} research documents")
    else:
        print_warning("docs/ directory not found")

    return errors


def check_critical_issues() -> list[str]:
    """Check status of critical integration issues."""
    errors = []

    print_header("Critical Issues Check")

    issues = {
        'CON-1427': 'Fee collection (80/10/10 yield)',
        'CON-1425': 'CXD stablecoin peg mechanism',
        'CON-1434': 'Contract stub ratio (33%)',
        'CON-1422': 'Admin-Key control (73+ vars)',
        'CON-1439': 'DAO governance transition',
        'CON-1440': '@conxian/sdk npm release',
        'CON-1437': 'Developer Sandbox launch',
    }

    # Check if issues are referenced in documentation
    docs_dir = REPO_ROOT / "docs"
    market_docs = MARKET_SUBMODULE / "docs" / "research"

    issue_audit = market_docs / "org_reality_issue_audit.md"
    if issue_audit.exists():
        content = issue_audit.read_text()
        for issue_id, desc in issues.items():
            if issue_id in content:
                print_success(f"{issue_id}: {desc}")
            else:
                print_warning(f"{issue_id}: {desc} (not in issue audit)")

    return errors


def check_integration_research_doc() -> list[str]:
    """Verify integration research document exists."""
    errors = []

    print_header("Integration Research Document Check")

    research_doc = REPO_ROOT / "docs" / "MARKET_BOS_INTEGRATION_RESEARCH.md"
    if research_doc.exists():
        print_success("MARKET_BOS_INTEGRATION_RESEARCH.md exists")
        content = research_doc.read_text()
        if 'CON-1427' in content and 'CON-1425' in content:
            print_success("Critical issues documented in research")
        if 'REPO-008' in content or 'conxian-market' in content.lower():
            print_success("Market repository documented")
    else:
        print_warning("MARKET_BOS_INTEGRATION_RESEARCH.md not found (may be optional)")

    return errors


def main() -> int:
    print(f"\n{Colors.BLUE}{'='*60}")
    print("  Conxian Market BOS Integration Verification")
    print(f"{'='*60}{Colors.RESET}\n")

    all_errors = []

    # Run all checks
    all_errors.extend(check_bos_framework_registration())
    all_errors.extend(check_dependency_map())
    all_errors.extend(check_market_submodule())
    all_errors.extend(check_critical_issues())
    all_errors.extend(check_integration_research_doc())

    # Summary
    print_header("Summary")

    if all_errors:
        print(f"{Colors.RED}✗ {len(all_errors)} error(s) found:{Colors.RESET}")
        for i, err in enumerate(all_errors, 1):
            print(f"  {i}. {err}")
        print(f"\n{Colors.YELLOW}⚠ Run 'git submodule update --init conxian-market' if submodule is empty{Colors.RESET}")
        return 1

    print_success("All integration checks passed!")
    print(f"\n{Colors.GREEN}Market BOS Integration: READY{Colors.RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
