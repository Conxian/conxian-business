#!/usr/bin/env python3
"""Repository Viability Assessment Script (RVS)

Assesses repositories against the Conxian Repository Viability Scale (RVS)
aligned with Unified Theory v2.0 metrics.

Usage:
    python3 scripts/repo_viability_assessment.py --repo <repo_name>
    python3 scripts/repo_viability_assessment.py --all
    python3 scripts/repo_viability_assessment.py --report --format markdown
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class DimensionScore:
    """Individual dimension score with reasoning."""
    code: str
    name: str
    max_score: int
    score: int
    reasoning: list[str] = field(default_factory=list)


@dataclass
class RepoAssessment:
    """Complete repository assessment result."""
    repo_name: str
    repo_path: Path
    dimensions: list[DimensionScore]
    total_score: int
    classification: str
    phase: str
    recommendation: str
    assessed_at: str
    aligned_unified_theory: bool = True


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    ORANGE = "\033[38;5;214m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def run(cmd: list[str], cwd=None) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO_ROOT)


def detect_repo_type(repo_name: str, repo_path: Path) -> str:
    """Detect the repository type for score normalization."""
    # Docs/Research repos
    docs_research = ["conxian-market", "conxian-labs-site", "docs", "research"]
    if any(dr in repo_name.lower() for dr in docs_research):
        return "docs"
    
    # Protocol repos (Clarity contracts)
    protocol = ["conxian", "lib-conxian-core"]
    if any(p in repo_name.lower() for p in protocol):
        # Check for Clarity files
        if any(repo_path.glob("*.clar")):
            return "protocol"
    
    # Default to code repo
    return "code"


def get_normalized_score(raw_score: int, repo_type: str) -> int:
    """Normalize score based on repo type."""
    type_max = {
        "code": 100,
        "protocol": 100,
        "docs": 90,
    }
    return int((raw_score / 80) * type_max.get(repo_type, 100))


def get_classification(normalized_score: int, repo_type: str) -> tuple:
    """Get classification based on normalized score and repo type."""
    thresholds = {
        "code": [(90, "🟢 PRODUCTION READY", "Phase 4 - Sovereign State", "Ship, scale, monitor"),
                 (80, "🟢 PRODUCTION READY", "Phase 4 - Sovereign State", "Ship, scale, monitor"),
                 (70, "🟡 OPERATIONAL", "Phase 3 - Transitioning to Autonomy", "Enhance automation, monitor"),
                 (60, "🟡 OPERATIONAL", "Phase 3 - Transitioning to Autonomy", "Enhance automation"),
                 (50, "🟠 DEVELOPMENT", "Phase 2 - Forge in Progress", "Accelerate development"),
                 (40, "🟠 DEVELOPMENT", "Phase 2 - Forge in Progress", "Accelerate, automate"),
                 (30, "🔴 BLOCKED", "Phase 1-2 - Genesis/Forge", "Remediate critical issues"),
                 (20, "🔴 BLOCKED", "Phase 1-2 - Genesis/Forge", "Remediate critical issues"),
                 (0, "⚫ ARCHIVE", "Sunset", "Deprecate, preserve IP, archive")],
        "protocol": [(95, "🟢 PRODUCTION READY", "Phase 4 - Sovereign State", "Ship, audit, scale"),
                     (85, "🟢 PRODUCTION READY", "Phase 4 - Sovereign State", "Ship, audit, scale"),
                     (75, "🟡 OPERATIONAL", "Phase 3 - Transitioning to Autonomy", "Enhance, audit"),
                     (65, "🟡 OPERATIONAL", "Phase 3 - Transitioning to Autonomy", "Enhance protocol"),
                     (55, "🟠 DEVELOPMENT", "Phase 2 - Forge in Progress", "Accelerate, audit pending"),
                     (45, "🟠 DEVELOPMENT", "Phase 2 - Forge in Progress", "Complete protocol features"),
                     (30, "🔴 BLOCKED", "Phase 1-2 - Genesis/Forge", "Critical protocol gaps"),
                     (20, "🔴 BLOCKED", "Phase 1-2 - Genesis/Forge", "Protocol requires rewrite"),
                     (0, "⚫ ARCHIVE", "Sunset", "Protocol deprecated")],
        "docs": [(80, "🟢 PRODUCTION READY", "Phase 4 - Published", "Maintain, update regularly"),
                 (70, "🟢 PRODUCTION READY", "Phase 4 - Published", "Maintain, update regularly"),
                 (60, "🟡 OPERATIONAL", "Phase 3 - Maintained", "Keep current, expand coverage"),
                 (50, "🟡 OPERATIONAL", "Phase 3 - Maintained", "Maintain documentation"),
                 (40, "🟠 DEVELOPMENT", "Phase 2 - Drafting", "Complete documentation"),
                 (30, "🟠 DEVELOPMENT", "Phase 2 - Drafting", "Complete documentation"),
                 (20, "🔴 BLOCKED", "Phase 1 - Incomplete", "Complete core docs"),
                 (15, "🔴 BLOCKED", "Phase 1 - Incomplete", "Complete core docs"),
                 (0, "⚫ ARCHIVE", "Sunset", "Archive outdated docs")],
    }
    
    for threshold, classification, phase, recommendation in thresholds.get(repo_type, thresholds["code"]):
        if normalized_score >= threshold:
            return classification, phase, recommendation
    
    return "⚫ ARCHIVE", "Sunset", "Unclassifiable"


def get_git_info(repo_path: Path) -> dict:
    """Get git information for a repository."""
    info = {
        "last_commit": None,
        "commit_count": 0,
        "branch": None,
        "dirty": False,
    }
    
    result = run(["git", "rev-parse", "--short", "HEAD"], cwd=repo_path)
    if result.returncode == 0:
        info["last_commit"] = result.stdout.strip()
    
    result = run(["git", "rev-list", "--count", "HEAD"], cwd=repo_path)
    if result.returncode == 0:
        info["commit_count"] = int(result.stdout.strip())
    
    result = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path)
    if result.returncode == 0:
        info["branch"] = result.stdout.strip()
    
    result = run(["git", "status", "--porcelain"], cwd=repo_path)
    if result.returncode == 0 and result.stdout.strip():
        info["dirty"] = True
    
    return info


def check_agents_md(repo_path: Path) -> tuple[int, list[str]]:
    """Check for AGENTS.md file."""
    score = 0
    reasoning = []
    
    agents_md = repo_path / "AGENTS.md"
    if agents_md.exists():
        score += 5
        reasoning.append("AGENTS.md exists")
        
        content = agents_md.read_text()
        if len(content) > 500:
            score += 5
            reasoning.append("AGENTS.md is comprehensive")
        else:
            reasoning.append("AGENTS.md is minimal")
    else:
        reasoning.append("AGENTS.md missing")
    
    return score, reasoning


def check_readme(repo_path: Path) -> tuple[int, list[str]]:
    """Check README completeness."""
    score = 0
    reasoning = []
    
    readme = repo_path / "README.md"
    if readme.exists():
        score += 3
        content = readme.read_text()
        
        if len(content) > 500:
            score += 2
            reasoning.append("README is comprehensive")
        else:
            reasoning.append("README is minimal")
        
        if "##" in content:  # Has sections
            score += 1
            reasoning.append("README has sections")
    else:
        reasoning.append("README.md missing")
    
    return score, reasoning


def check_ci_cd(repo_path: Path) -> tuple[int, list[str]]:
    """Check CI/CD configuration."""
    score = 0
    reasoning = []
    
    github_dir = repo_path / ".github"
    workflows_dir = github_dir / "workflows" if github_dir.exists() else None
    
    if workflows_dir and workflows_dir.exists():
        workflows = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if workflows:
            score += 3
            reasoning.append(f"{len(workflows)} workflow(s) found")
            
            # Check for standard workflows
            workflow_names = [w.name for w in workflows]
            if any("ci" in w.lower() for w in workflow_names):
                score += 2
                reasoning.append("CI workflow present")
            if any("test" in w.lower() for w in workflow_names):
                score += 1
                reasoning.append("Test workflow present")
        else:
            reasoning.append("No workflows found")
    else:
        reasoning.append("No .github/workflows directory")
    
    return score, reasoning


def check_security(repo_path: Path) -> tuple[int, list[str]]:
    """Assess security posture."""
    score = 0
    reasoning = []
    
    # Check for security policy
    security_md = repo_path / "SECURITY.md"
    if security_md.exists():
        score += 2
        reasoning.append("SECURITY.md exists")
    
    # Check for vulnerability scanning
    result = run(["ls", "-la", repo_path / "Cargo.lock"], cwd=repo_path)
    if result.returncode == 0:
        score += 1
        reasoning.append("Rust dependencies (Cargo.lock)")
    
    result = run(["ls", "-la", repo_path / "pnpm-lock.yaml"], cwd=repo_path)
    if result.returncode == 0:
        score += 1
        reasoning.append("Node dependencies (pnpm-lock)")
    
    result = run(["ls", "-la", repo_path / "package-lock.json"], cwd=repo_path)
    if result.returncode == 0:
        score += 1
        reasoning.append("NPM dependencies (package-lock)")
    
    # Check .gitignore
    gitignore = repo_path / ".gitignore"
    if gitignore.exists():
        score += 1
        reasoning.append(".gitignore present")
    
    return score, reasoning


def assess_repository(repo_name: str, repo_path: Path) -> RepoAssessment:
    """Perform full assessment on a repository."""
    
    # Detect repo type for score normalization
    repo_type = detect_repo_type(repo_name, repo_path)
    
    dimensions = []
    
    # D1: Documentation (D_DOC) - 15 pts
    docs_score = 0
    docs_reasoning = []
    
    agents_score, agents_reasoning = check_agents_md(repo_path)
    docs_score += agents_score
    docs_reasoning.extend(agents_reasoning)
    
    readme_score, readme_reasoning = check_readme(repo_path)
    docs_score += readme_score
    docs_reasoning.extend(readme_reasoning)
    
    dimensions.append(DimensionScore(
        code="D_DOC",
        name="Documentation",
        max_score=15,
        score=min(docs_score, 15),
        reasoning=docs_reasoning
    ))
    
    # D2: CI/CD & Automation (D_EV) - 15 pts
    cicd_score = 0
    cicd_reasoning = []
    
    ci_score, ci_reasoning = check_ci_cd(repo_path)
    cicd_score += ci_score
    cicd_reasoning.extend(ci_reasoning)
    
    dimensions.append(DimensionScore(
        code="D_EV",
        name="Execution Velocity (CI/CD)",
        max_score=15,
        score=min(cicd_score, 15),
        reasoning=cicd_reasoning
    ))
    
    # D3: Security & Sovereignty (D_SS) - 20 pts
    sec_score = 0
    sec_reasoning = []
    
    sec_base, sec_base_reasoning = check_security(repo_path)
    sec_score += sec_base
    sec_reasoning.extend(sec_base_reasoning)
    
    # Check for governance documentation
    governance = repo_path / "GOVERNANCE.md"
    if governance.exists():
        sec_score += 3
        sec_reasoning.append("GOVERNANCE.md exists")
    
    # Check for ADRs (Architecture Decision Records)
    adrs_dir = repo_path / "docs" / "architecture" / "adrs"
    if adrs_dir.exists():
        sec_score += 2
        adrs_count = len(list(adrs_dir.glob("*.md")))
        sec_reasoning.append(f"{adrs_count} ADR(s) found")
    
    dimensions.append(DimensionScore(
        code="D_SS",
        name="Security & Sovereignty",
        max_score=20,
        score=min(sec_score, 20),
        reasoning=sec_reasoning
    ))
    
    # D4: Git Activity (Proxy for V_X) - 10 pts
    git_info = get_git_info(repo_path)
    activity_score = 0
    activity_reasoning = []
    
    if git_info["commit_count"] > 100:
        activity_score += 5
        activity_reasoning.append(f"{git_info['commit_count']} commits (high activity)")
    elif git_info["commit_count"] > 20:
        activity_score += 3
        activity_reasoning.append(f"{git_info['commit_count']} commits (medium activity)")
    else:
        activity_reasoning.append(f"{git_info['commit_count']} commits (low activity)")
    
    if not git_info["dirty"]:
        activity_score += 2
        activity_reasoning.append("Working tree clean")
    
    if git_info["branch"]:
        activity_score += 1
        activity_reasoning.append(f"On branch: {git_info['branch']}")
    
    dimensions.append(DimensionScore(
        code="D_ACT",
        name="Git Activity (V_X proxy)",
        max_score=10,
        score=min(activity_score, 10),
        reasoning=activity_reasoning
    ))
    
    # D5: Structure & Standards - 10 pts
    structure_score = 0
    structure_reasoning = []
    
    # Check for standard files
    standard_files = [
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
    ]
    
    for file in standard_files:
        if (repo_path / file).exists():
            structure_score += 1
            structure_reasoning.append(f"{file} exists")
    
    # Check for proper structure
    if (repo_path / "src").exists():
        structure_score += 2
        structure_reasoning.append("src/ directory present")
    
    if (repo_path / "tests").exists():
        structure_score += 1
        structure_reasoning.append("tests/ directory present")
    
    dimensions.append(DimensionScore(
        code="D_STR",
        name="Structure & Standards",
        max_score=10,
        score=min(structure_score, 10),
        reasoning=structure_reasoning
    ))
    
    # D6: Ecosystem Integration - 10 pts
    integration_score = 0
    integration_reasoning = []
    
    # Check if repo is registered in BOS
    bos_framework = REPO_ROOT / "docs" / "BOS_KNOWLEDGE_FRAMEWORK.md"
    if bos_framework.exists():
        content = bos_framework.read_text()
        if repo_name in content or repo_name.replace("-", "_") in content:
            integration_score += 4
            integration_reasoning.append("Registered in BOS_KNOWLEDGE_FRAMEWORK")
    
    # Check if repo is in PORTFOLIO
    portfolio = REPO_ROOT / "docs" / "PORTFOLIO_BUSINESS_UNIT_MAP.md"
    if portfolio.exists():
        content = portfolio.read_text()
        if repo_name in content:
            integration_score += 3
            integration_reasoning.append("Listed in PORTFOLIO_BUSINESS_UNIT_MAP")
    
    # Check for dependency map entry
    dep_map = REPO_ROOT / "docs" / "CROSS_REPO_DEPENDENCY_MAP.md"
    if dep_map.exists():
        content = dep_map.read_text()
        if repo_name in content:
            integration_score += 2
            integration_reasoning.append("Listed in CROSS_REPO_DEPENDENCY_MAP")
    
    dimensions.append(DimensionScore(
        code="D_INT",
        name="Ecosystem Integration",
        max_score=10,
        score=min(integration_score, 10),
        reasoning=integration_reasoning
    ))
    
    # Calculate total and normalize
    raw_score = sum(d.score for d in dimensions)
    normalized_score = get_normalized_score(raw_score, repo_type)
    classification, phase, recommendation = get_classification(normalized_score, repo_type)
    
    return RepoAssessment(
        repo_name=repo_name,
        repo_path=repo_path,
        dimensions=dimensions,
        total_score=normalized_score,
        classification=classification,
        phase=phase,
        recommendation=recommendation,
        assessed_at=datetime.now().isoformat(),
    )


def format_markdown(assessment: RepoAssessment) -> str:
    """Format assessment as markdown."""
    lines = [
        f"# {assessment.repo_name} - Repository Viability Assessment",
        "",
        f"**Assessed**: {assessment.assessed_at}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|---------|-------|",
        f"| **Total Score** | **{assessment.total_score}/80** |",
        f"| **Classification** | {assessment.classification} |",
        f"| **Phase** | {assessment.phase} |",
        "",
        f"> **Recommendation**: {assessment.recommendation}",
        "",
        "## Dimension Scores",
        "",
    ]
    
    for dim in assessment.dimensions:
        pct = (dim.score / dim.max_score) * 100 if dim.max_score > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        lines.append(f"### {dim.code}: {dim.name}")
        lines.append(f"`{dim.score}/{dim.max_score}` [{bar}] {pct:.0f}%")
        lines.append("")
        for reason in dim.reasoning:
            lines.append(f"- {reason}")
        lines.append("")
    
    return "\n".join(lines)


def format_console(assessment: RepoAssessment) -> str:
    """Format assessment for console output."""
    lines = [
        f"\n{Colors.BOLD}{'='*60}",
        f"  {assessment.repo_name} - Repository Viability Assessment",
        f"{'='*60}{Colors.RESET}\n",
        f"Assessed: {assessment.assessed_at}\n",
    ]
    
    for dim in assessment.dimensions:
        pct = (dim.score / dim.max_score) * 100 if dim.max_score > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        
        color = Colors.GREEN if pct >= 70 else Colors.YELLOW if pct >= 50 else Colors.RED
        lines.append(f"  {dim.code} {dim.name}")
        lines.append(f"  {color}{dim.score:2d}/{dim.max_score:2d}{Colors.RESET} [{bar}] {pct:.0f}%")
        for reason in dim.reasoning:
            lines.append(f"    {Colors.BLUE}→{Colors.RESET} {reason}")
        lines.append("")
    
    # Summary
    total_pct = assessment.total_score / 80 * 100
    if total_pct >= 90:
        summary_color = Colors.GREEN
    elif total_pct >= 70:
        summary_color = Colors.YELLOW
    elif total_pct >= 50:
        summary_color = Colors.ORANGE
    else:
        summary_color = Colors.RED
    
    lines.extend([
        f"{Colors.BOLD}─"*60,
        f"  TOTAL SCORE: {summary_color}{assessment.total_score}/80{Colors.RESET}",
        f"  Classification: {summary_color}{assessment.classification}{Colors.RESET}",
        f"  Phase: {assessment.phase}",
        f"",
        f"  {Colors.BOLD}Recommendation:{Colors.RESET} {assessment.recommendation}",
        f"{Colors.BOLD}─"*60,
    ])
    
    return "\n".join(lines)


def assess_all_repos() -> list[RepoAssessment]:
    """Assess all submodules and key directories."""
    assessments = []
    
    # Submodules from .gitmodules
    gitmodules = REPO_ROOT / ".gitmodules"
    if gitmodules.exists():
        content = gitmodules.read_text()
        current_path = None
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("[submodule "):
                current_path = line[len("[submodule "):-1].strip('"')
            elif line.startswith("path = ") and current_path:
                path = line[7:].strip()
                repo_path = REPO_ROOT / path
                if repo_path.exists() and any(repo_path.iterdir()):
                    assessment = assess_repository(current_path, repo_path)
                    assessments.append(assessment)
    
    # Also assess top-level modules
    top_level_dirs = [
        "Conxian", "conxian-gateway", "conxian-nexus", "conxian-ui",
        "conxius-wallet", "conxius-platform", "conxius-enclave-sdk",
        "lib-conxian-core", "conxian-market",
    ]
    
    for dir_name in top_level_dirs:
        repo_path = REPO_ROOT / dir_name
        if repo_path.exists() and any(repo_path.iterdir()):
            # Skip if already assessed as submodule
            if not any(a.repo_name == dir_name for a in assessments):
                assessment = assess_repository(dir_name, repo_path)
                assessments.append(assessment)
    
    return assessments


def main():
    parser = argparse.ArgumentParser(description="Repository Viability Assessment")
    parser.add_argument("--repo", help="Specific repository to assess")
    parser.add_argument("--all", action="store_true", help="Assess all repositories")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--format", choices=["console", "markdown", "json"], default="console")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.repo and not args.all:
        print("Error: Specify --repo <name> or --all")
        print("Usage: python3 scripts/repo_viability_assessment.py --all")
        sys.exit(1)
    
    if args.all:
        assessments = assess_all_repos()
        assessments.sort(key=lambda x: x.total_score, reverse=True)
        
        if args.format == "json":
            output = json.dumps([
                {
                    "repo": a.repo_name,
                    "score": a.total_score,
                    "classification": a.classification,
                    "phase": a.phase,
                }
                for a in assessments
            ], indent=2)
        else:
            lines = [
                f"\n{Colors.BOLD}{'='*70}",
                f"  Conxian Repository Portfolio - Viability Summary",
                f"{'='*70}{Colors.RESET}\n",
            ]
            
            for a in assessments:
                pct = a.total_score / 80 * 100
                if pct >= 90:
                    color = Colors.GREEN
                elif pct >= 70:
                    color = Colors.YELLOW
                elif pct >= 50:
                    color = Colors.ORANGE
                else:
                    color = Colors.RED
                
                lines.append(
                    f"  {color}{a.total_score:3d}/80{Colors.RESET} "
                    f"{a.repo_name:<35} {a.classification}"
                )
            
            output = "\n".join(lines)
        
    else:
        repo_path = REPO_ROOT / args.repo
        if not repo_path.exists():
            print(f"Error: Repository '{args.repo}' not found")
            sys.exit(1)
        
        assessment = assess_repository(args.repo, repo_path)
        
        if args.format == "json":
            output = json.dumps({
                "repo": assessment.repo_name,
                "score": assessment.total_score,
                "classification": assessment.classification,
                "phase": assessment.phase,
                "recommendation": assessment.recommendation,
                "dimensions": [
                    {
                        "code": d.code,
                        "name": d.name,
                        "score": d.score,
                        "max": d.max_score,
                        "reasoning": d.reasoning,
                    }
                    for d in assessment.dimensions
                ],
            }, indent=2)
        elif args.format == "markdown":
            output = format_markdown(assessment)
        else:
            output = format_console(assessment)
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
