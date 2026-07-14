# Conxian Agent Session Feedback Framework
> **Purpose**: Standardized testing strategy and knowledge feedback loop for agent sessions
> **Version**: 1.0.0
> **Generated**: 2026-07-14

---

## 1. Overview

This framework establishes a **closed-loop system** for agent sessions:
1. **Test** → Before/After every change
2. **Validate** → Verify functionality
3. **Feedback** → Update knowledge base
4. **Issues** → Create Linear tickets for blockers

### 1.1 Session Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION START                                                   │
│  ├── Read AGENTS.md                                             │
│  ├── Read BOS_KNOWLEDGE_FRAMEWORK.md                           │
│  ├── Check active Linear issues                                 │
│  └── Pull latest code                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  TASK EXECUTION                                                  │
│  ├── Implement changes                                           │
│  ├── Run verification tests                                     │
│  └── Document findings                                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  SESSION END                                                    │
│  ├── Run full test suite                                       │
│  ├── Update BOS_KNOWLEDGE_GRAPH.md                           │
│  ├── Create/update Linear issues                                │
│  └── Crystallize learnings                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Testing Strategy

### 2.1 Test Categories

| Category | Purpose | Frequency | Tools |
|----------|---------|-----------|-------|
| **Unit** | Individual components | Every PR | pytest, cargo test |
| **Integration** | Cross-repo wiring | Every PR | verify scripts |
| **E2E** | Full workflows | Weekly | Manual + CI |
| **Security** | Vulnerabilities | Daily | npm audit, cargo audit |
| **Compliance** | BOS standards | Every PR | verify scripts |

### 2.2 Test Execution Matrix

| Change Type | Tests Required | Gate |
|-------------|---------------|------|
| **Code (Rust)** | cargo check, cargo test, cargo clippy | CI |
| **Code (TS/JS)** | pnpm lint, pnpm test, typecheck | CI |
| **Contracts** | clarinet check, clarinet test | CI |
| **Docs** | linkcheck, spellcheck | CI |
| **Config** | verify scripts, schema validation | CI |
| **Market Integration** | market_bos_mwp_test.py | CI |
| **Viability** | repo_viability_assessment.py | Weekly |

---

## 3. Pre-Session Checklist

### 3.1 Environment Verification

```bash
# 1. Pull latest
git checkout dev && git pull origin dev

# 2. Initialize submodules
git submodule update --init --recursive

# 3. Verify integrity
python3 scripts/verify_submodule_integrity.py

# 4. Check for regressions
python3 scripts/repo_viability_assessment.py --all
```

### 3.2 Active Issues Check

```bash
# Get active issues
gh issue list --state open --limit 20

# Filter by priority
gh issue list --state open --label "priority/high" --limit 10

# Check assigned issues
gh issue list --assignee @me --state open
```

---

## 4. Post-Session Testing

### 4.1 Mandatory Tests

```bash
#!/bin/bash
# post-session-tests.sh

set -e

echo "=== Post-Session Test Suite ==="

# 1. Integration Tests
echo "[1/7] Running Market Integration Tests..."
python3 scripts/verify_market_integration.py

# 2. MWP Test Suite
echo "[2/7] Running MWP Tests..."
python3 scripts/market_bos_mwp_test.py

# 3. Viability Assessment
echo "[3/7] Running Viability Assessment..."
python3 scripts/repo_viability_assessment.py --all

# 4. Submodule Integrity
echo "[4/7] Checking Submodule Integrity..."
python3 scripts/verify_submodule_integrity.py

# 5. Security Audit
echo "[5/7] Running Security Audit..."
if [ -f "pnpm-lock.yaml" ]; then
    pnpm audit || echo "pnpm audit failed (non-blocking)"
fi

# 6. CI Simulation
echo "[6/7] Simulating CI Checks..."
# Run relevant CI steps locally

# 7. Git Status
echo "[7/7] Checking Git Status..."
git status --short

echo "=== Test Suite Complete ==="
```

### 4.2 Test Results Template

```markdown
## Session Test Results

**Date**: YYYY-MM-DD
**Session ID**: [auto-generated]
**Agent**: OpenHands

### Test Summary

| Test | Status | Duration | Notes |
|------|--------|----------|-------|
| Market Integration | ✅/❌ | Xs | - |
| MWP Suite | ✅/❌ | Xs | - |
| Viability | ✅/❌ | Xs | - |
| Submodule Integrity | ✅/❌ | Xs | - |
| Security Audit | ✅/❌ | Xs | - |

### Changes Made

| File | Change | Test Impact |
|------|--------|------------|
| - | - | - |

### Issues Found

| Issue | Severity | Action |
|-------|----------|--------|
| - | - | - |

### Knowledge Updates

| Entity | Update Type | Details |
|--------|------------|---------|
| - | - | - |
```

---

## 5. Knowledge Base Feedback Loop

### 5.1 BOS Knowledge Graph Updates

After each session, update `BOS_KNOWLEDGE_GRAPH.md`:

```markdown
## Session Log

| Date | Session ID | Changes | Issues Created | Knowledge Added |
|------|------------|---------|--------------|----------------|
| 2026-07-14 | SESSION-001 | Market × BOS integration | #890, #891 | REPO-008 added |
```

### 5.2 Entity Extraction

For every session, extract:

| Entity Type | Example | Action |
|-------------|---------|--------|
| **People** | @username | Update stakeholder map |
| **Projects** | CON-XXXX | Link to Linear |
| **Libraries** | lib-conxian-core | Document version |
| **Decisions** | DEC-XXX | Update decision log |
| **Risks** | VULN-XXX | Add to registry |

### 5.3 Knowledge Update Checklist

```markdown
## Session: YYYY-MM-DD

### Entities Discovered
- [ ] Person: @username - Role/responsibility
- [ ] Project: CON-XXXX - Description
- [ ] Library: package-name - Version

### Decisions Made
- [ ] DEC-XXX: Topic - Rationale

### Risks Identified
- [ ] VULN-XXX: Package - Severity - Fix

### Documentation Updated
- [ ] File: docs/X.md - Updated
- [ ] File: docs/Y.md - Created

### Linear Issues
- [ ] #123: Title - Created
- [ ] #456: Title - Updated
```

---

## 6. Issue Creation Protocol

### 6.1 When to Create Issues

| Scenario | Priority | Labels |
|----------|----------|--------|
| Bug found during testing | High | `bug`, `priority/high` |
| Enhancement identified | Medium | `enhancement` |
| Vulnerability discovered | Critical | `security`, `priority/urgent` |
| Technical debt found | Low | `tech-debt` |
| Documentation gap | Medium | `docs` |

### 6.2 Issue Template

```markdown
## [Type] Brief Description

**Session**: SESSION-XXX
**Date**: YYYY-MM-DD
**Agent**: OpenHands

### Problem
Clear description of the issue.

### Impact
What breaks or is at risk.

### Evidence
- Test output
- Log snippets
- Screenshots

### Suggested Fix
How to resolve (if known).

### Related
- Linear: CON-XXXX
- Docs: docs/X.md
- PRs: #123
```

### 6.3 Issue Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Discovered │ ──▶ │  Created   │ ──▶ │  Assigned  │
│  in Session │     │  in Linear │     │  to Owner  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Document  │     │  Labeled   │     │  Tracked   │
│  in BOS    │     │  Properly  │     │  in Board  │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 7. Session Report Template

### 7.1 Full Session Report

```markdown
# Session Report: YYYY-MM-DD

## Session Metadata
| Field | Value |
|-------|-------|
| **Session ID** | SESSION-XXX |
| **Start Time** | HH:MM UTC |
| **End Time** | HH:MM UTC |
| **Duration** | Xh Xm |
| **Agent** | OpenHands |
| **Branch** | dev |

## Objective
What was the session goal?

## Execution

### Tasks Completed
1. [ ] Task 1
2. [ ] Task 2
3. [ ] Task 3

### Changes Made
```bash
# List of git changes
git diff --stat
```

### Tests Run
| Test | Result | Notes |
|------|--------|-------|
| - | - | - |

## Findings

### ✅ Successes
- What worked well

### ⚠️ Warnings
- Non-blocking issues found

### ❌ Blockers
- Critical issues that stopped work

## Knowledge Updates

### Entities
| Type | ID | Name | Status |
|------|-----|------|--------|
| - | - | - | - |

### Decisions
| ID | Topic | Decision | Rationale |
|----|-------|----------|-----------|
| - | - | - | - |

### Risks
| ID | Severity | Description | Mitigation |
|----|----------|-------------|------------|
| - | - | - | - |

## Issues Created/Updated

| Issue | Action | Priority |
|-------|--------|----------|
| - | - | - |

## Recommendations

### Immediate
1. Next action items

### Short-term
1. Follow-up items

### Long-term
1. Strategic improvements

## Sign-off
- [ ] Tests passed
- [ ] Knowledge updated
- [ ] Issues created
- [ ] Ready for review
```

---

## 8. Automated Testing Scripts

### 8.1 Full Test Suite

```python
#!/usr/bin/env python3
"""Full session test suite runner."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SessionTester:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()

    def run_test(self, name: str, command: str, critical: bool = True) -> bool:
        """Run a single test."""
        print(f"\n[TEST] {name}...")
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )

        passed = result.returncode == 0
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}")

        if not passed and result.stdout:
            print(f"  Output: {result.stdout[:200]}")
        if not passed and result.stderr:
            print(f"  Error: {result.stderr[:200]}")

        self.results.append({
            "name": name,
            "passed": passed,
            "critical": critical,
            "command": command,
        })
        return passed

    def run_suite(self):
        """Run full test suite."""
        print("="*60)
        print("  CONXIAN SESSION TEST SUITE")
        print("="*60)
        print(f"Started: {self.start_time.isoformat()}\n")

        # Integration tests
        self.run_test("Market Integration",
                      "python3 scripts/verify_market_integration.py")
        self.run_test("MWP Test Suite",
                      "python3 scripts/market_bos_mwp_test.py")

        # Viability
        self.run_test("Viability Assessment",
                      "python3 scripts/repo_viability_assessment.py --all",
                      critical=False)

        # Integrity
        self.run_test("Submodule Integrity",
                      "python3 scripts/verify_submodule_integrity.py")

        # Summary
        self.print_summary()

        return all(r["passed"] or not r["critical"] for r in self.results)

    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("  TEST SUMMARY")
        print("="*60)

        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])
        total = len(self.results)

        print(f"\nPassed: {passed}/{total}")
        print(f"Failed: {failed}/{total}")

        if failed > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r["passed"]:
                    print(f"  ❌ {r['name']}")
                    print(f"     Command: {r['command']}")

        print(f"\nDuration: {datetime.now() - self.start_time}")

if __name__ == "__main__":
    tester = SessionTester()
    success = tester.run_suite()
    sys.exit(0 if success else 1)
```

### 8.2 Quick Health Check

```bash
#!/bin/bash
# quick-health-check.sh

echo "=== Quick Health Check ==="
echo ""

# Git status
echo "[1/5] Git Status:"
git status --short | head -5
echo ""

# Modified files
echo "[2/5] Modified Files:"
git diff --name-only | head -5
echo ""

# New files
echo "[3/5] Untracked Files:"
git ls-files --others --exclude-standard | head -5
echo ""

# Last commit
echo "[4/5] Last Commit:"
git log -1 --oneline
echo ""

# Test summary
echo "[5/5] Quick Tests:"
python3 scripts/verify_market_integration.py 2>&1 | tail -3
echo ""

echo "=== Health Check Complete ==="
```

---

## 9. Integration with Linear

### 9.1 Session → Linear Sync

After each session, sync to Linear:

```bash
# Create issue for major finding
gh issue create \
  --title "[Session SESSION-XXX] Finding: Description" \
  --body "$(cat <<'EOF'
## Session Information
- Session: SESSION-XXX
- Date: YYYY-MM-DD
- Agent: OpenHands

## Finding
Description of the issue.

## Evidence
```bash
# Test output or evidence here
```

## Suggested Fix
How to resolve.

## Related
- Docs: docs/X.md
- PRs: #123
EOF
" \
  --label "session-feedback"
```

### 9.2 Linear → Session Info

At session start, fetch relevant issues:

```bash
# Get recently updated issues
gh issue list --state open --updated ">=2026-07-01" --limit 10

# Get issues by label
gh issue list --label "session-feedback" --state open
```

---

## 10. Continuous Improvement

### 10.1 Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test pass rate | >95% | Automated |
| Issue creation rate | Decreasing | Weekly |
| Knowledge doc freshness | <7 days | Manual |
| Regression rate | <5% | Per sprint |

### 10.2 Feedback Loop

```
Session → Tests → Results → Analysis → Improvements → Next Session
    ↑                                                      │
    └────────────────────────────────────────────────────┘
```

### 10.3 Quarterly Review

- Analyze session patterns
- Identify recurring issues
- Update test coverage
- Refine knowledge extraction

---

## 11. Related Documents

- [BOS Knowledge Framework](BOS_KNOWLEDGE_FRAMEWORK.md)
- [BOS Knowledge Graph](conxian-business/BOS_KNOWLEDGE_GRAPH.md)
- [Market BOS Integration Research](MARKET_BOS_INTEGRATION_RESEARCH.md)
- [Repository Viability Scale](REPO_VIABILITY_SCALE.md)
- [Vulnerability Remediation Plan](VULNERABILITY_REMEDIATION_PLAN.md)

---

## 12. Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-07-14 | Initial framework | OpenHands |

---

*Generated by OpenHands agent on behalf of Conxian-Labs (Pty) Ltd*
*Co-authored-by: openhands <openhands@all-hands.dev>*
