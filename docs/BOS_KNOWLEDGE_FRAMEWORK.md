# Conxian BOS Knowledge Framework
> **Agentic-First Multi-Dimensional Knowledge Architecture**
> Version: 4.1 | Session: 71 | Generated: 2026-10-24
> **Design**: Machine-ingestible, AI-first, structured patterns
> **Upgradeable**: YES - See `## Knowledge Base Upgrade Guide`

---

## 🎯 Agentic Design Principles

This knowledge base is designed for **AI consumption and autonomous action**:

1. **Structured over Prose** - YAML/JSON tables, not paragraphs
2. **Actionable Patterns** - IF conditions → THEN actions
3. **Versioned Entries** - Every entity has `created`, `updated`, `version`
4. **Cross-Referenced** - Links between related entities
5. **Query-First** - Questions map directly to sections

---

### Query → Section Mapping

| Agent Question | Section |
|----------------|---------|
| "How do I fix CI failure?" | `## ci-failures` |
| "What secrets exist?" | `## secrets` |
| "Who owns this?" | `## stakeholders` |
| "Why was this decided?" | `## decisions` |
| "What's vulnerable?" | `## vulnerabilities` |
| "How do I deploy?" | `## deployments` |

---

## Entity Schema (Machine-Readable)

All entities follow this schema:

```yaml
entity:
  id: string           # Unique identifier (e.g., "SEC-001")
  type: string         # Entity type (repository, decision, vulnerability)
  name: string         # Human-readable name
  version: semver      # Schema version
  created: ISO8601      # Creation date
  updated: ISO8601      # Last update
  status: enum         # active | deprecated | superseded
  tags: [string]       # Searchable tags
  relations: [object]   # Links to other entities
  data: object         # Type-specific payload
```

---

## 📦 Repositories

```yaml
repositories:
  conxian-business:
    id: REPO-001
    type: knowledge-ops
    owner: Conxian-Labs
    visibility: public
    language: Mixed
    purpose: "Business ops, governance, AGENTS.md"
    related: [REPO-002, REPO-003, REPO-007]
    tags: [knowledge-base, governance, ci-cd]

  conxian-nexus:
    id: REPO-002
    type: protocol-core
    owner: Conxian-Labs
    visibility: public
    language: Clarity/Rust
    purpose: "Settlement layer, treasury operations"
    related: [REPO-007]
    tags: [protocol, clarity, dao]

  conxian-gateway:
    id: REPO-003
    type: protocol-bridge
    owner: Conxian-Labs
    visibility: public
    language: Rust
    purpose: "ISO 20022 bridge, Bitcoin/Stacks"
    related: [REPO-007]
    tags: [protocol, bridge, rust]

  conxius-wallet:
    id: REPO-004
    type: client-facing
    owner: Conxian-Labs
    visibility: private
    language: TypeScript
    purpose: "Android wallet, key management"
    tags: [wallet, mobile, tpm]

  conxius-platform:
    id: REPO-005
    type: developer-tool
    owner: Conxian-Labs
    visibility: private
    language: TypeScript
    purpose: "Dev orchestration"
    tags: [developer, deployment]

  conxius-enclave-sdk:
    id: REPO-006
    type: security-module
    owner: Conxian-Labs
    visibility: public
    language: Rust/WASM
    purpose: "TEE abstraction"
    tags: [security, tee, enclave]

  lib-conxian-core:
    id: REPO-007
    type: shared-library
    owner: Conxian-Labs
    visibility: public
    language: Rust
    purpose: "Crypto primitives, ZKC, SYI"
    tags: [library, crypto, rust]
    consumers: [REPO-002, REPO-003]
```

---

### Relational Dimension: Stakeholders

```yaml
stakeholders:
  Conxian-Labs:
    type: legal-entity
    role: operator
    owns:
      - conxian-business
      - conxian-nexus
      - conxian-gateway
      - conxius-wallet
      - conxius-platform
      - conxius-enclave-sdk
      - lib-conxian-core
    responsibilities:
      - protocol-development
      - compliance
      - security-operations

  Conxian.org:
    type: dao-entity
    role: governance
    responsibilities:
      - token-holder-governance
      - treasury-management
      - protocol-upgrades
```

### Security Dimension: Vulnerability Registry

```yaml
vulnerabilities:
  audit-date: "2026-07-08"
  version: "1.0"
  
  summary:
    total: 61  # GitHub Dependabot: 1 critical, 27 high, 27 moderate, 6 low (2026-07-31)
    critical: 1
    high: 27
    moderate: 27
    low: 6
    fixable: ~40  # npm/pnpm fixable; 1 cargo unfixable (rustls-webpki via bdk chain)
    unfixable: 2  # elliptic GHSA-848j (no patch), rustls-webpki (bdk transitive)

  # ACTIONABLE: IF vulnerability THEN action
  rules:
    - IF: "severity == high AND fixable == true"
      THEN: "pnpm update <package> OR add to PR checklist"
      
    - IF: "severity == high AND fixable == false"
      THEN: "Check decision DEC-002; if not covered, add to allowlist"
      
    - IF: "transitive == true AND chain contains 'bdk'"
      THEN: "Monitor bdk upstream; add to DEC-002"
      
    - IF: "severity == moderate"
      THEN: "Add to monitor list; fix in next sprint"
      
    - IF: "severity == low"
      THEN: "Acceptable risk; document in vulnerability section"

  # HIGH SEVERITY - REQUIRES ACTION
  high:
    - id: VULN-H001
      alert: "#148"
      pkg: form-data
      ecosystem: npm
      fixable: true
      fix: "pnpm update form-data"
      affects: [pnpm-lock.yaml]

    - id: VULN-H002
      alert: "#143"
      pkg: vite
      ecosystem: npm
      fixable: true
      fix: "pnpm update vite"
      affects: [pnpm-lock.yaml]

    - id: VULN-H003
      alert: "#149"
      pkg: ws
      ecosystem: npm
      fixable: true
      fix: "pnpm update ws"
      affects: [pnpm-lock.yaml]

    - id: VULN-H004
      alert: "#21"
      pkg: bigint-buffer
      ecosystem: npm
      fixable: false
      reason: "Transitive via bdk"
      chain: "bdk -> bigint-buffer"
      decision: DEC-002
      affects: [Cargo.lock]

    - id: VULN-H005
      alert: "#153"
      pkg: undici
      ecosystem: npm
      fixable: true
      fix: "pnpm update undici"
      affects: [pnpm-lock.yaml]

    - id: VULN-H006
      alert: "#146"
      pkg: undici
      ecosystem: npm
      fixable: true
      fix: "pnpm update undici"
      affects: [pnpm-lock.yaml]

    - id: VULN-H007
      alert: "#150"
      pkg: undici
      ecosystem: npm
      fixable: true
      fix: "pnpm update undici"
      affects: [pnpm-lock.yaml]

    - id: VULN-H008
      alert: "#58"
      pkg: rustls-webpki
      ecosystem: cargo
      fixable: false
      reason: "Transitive via bdk -> electrum-client"
      chain: "bdk -> electrum-client -> rustls-webpki"
      decision: DEC-002
      affects: [Cargo.lock]

  # MODERATE SEVERITY - MONITOR
  moderate:
    - id: VULN-M001
      alert: "#139"
      pkg: uuid
      ecosystem: npm
      affects: [pnpm-lock.yaml]

    - id: VULN-M002
      alert: "#60"
      pkg: postcss
      ecosystem: npm
      fixable: true
      fix: "pnpm update postcss"
      affects: [showcase-dapp/package-lock.json]

  # LOW SEVERITY - ACCEPTABLE RISK
  low:
    - id: VULN-L001
      alert: "#154"
      pkg: undici
      ecosystem: npm
      affects: [pnpm-lock.yaml]
```

---

## 🔍 CodeQL Alerts (External Repos)

```yaml
codeql-alerts:
  audit-date: "2026-07-08"
  requires-attention: true
  api-access: false  # Requires code Scanning API permissions

  # HIGH SEVERITY - REQUIRES FIX
  high:
    - id: CSQL-H001
      repo: Conxian
      rule: "Clear-text logging of sensitive information"
      file: "tests/hiro-api.test.ts:19"
      action: "Remove sensitive data from logs"
      
    - id: CSQL-H002
      repo: Conxian
      rule: "DOM text reinterpreted as HTML"
      file: "src/.../page.tsx:137"
      action: "Sanitize output with DOMPurify/textContent"
      
    - id: CSQL-H003
      repo: Conxian_UI
      rule: "DOM text reinterpreted as HTML"
      file: "src/.../page.tsx:137"
      action: "Sanitize output with DOMPurify/textContent"

  # MEDIUM SEVERITY - WORKFLOW PERMISSIONS
  medium:
    - id: CSQL-M001
      repo: conxius-wallet
      workflow: "secret-scan.yml"
      action: "Add permissions: {contents: read}"
      
    - id: CSQL-M002
      repo: conxius-wallet
      workflow: "ci.yml"
      action: "Add permissions: {contents: read}"
      
    - id: CSQL-M003
      repo: conxius-wallet
      workflow: "cleanup-artifacts.yml"
      action: "Add permissions: {contents: read}"
      
    - id: CSQL-M004
      repo: .github (Conxian org)
      workflow: "standard-ci.yml"
      action: "Add permissions block"
      
    - id: CSQL-M005
      repo: conxian-nexus
      workflow: "rust.yml"
      action: "Add permissions block"

  # FIX PATTERN
  workflow-permissions-fix:
    pattern: |
      # Add at top of workflow YAML
      permissions:
        contents: read  # Or specific: actions: read, contents: read, etc.
    example: |
      name: CI
      on: [push, pull_request]
      permissions:
        contents: read
        actions: read
      jobs:
        ...
```

### Temporal Dimension: Decision Log

```yaml
decisions:
  - id: DEC-001
    date: 2026-04-23
    topic: clarity-version
    decision: "Clarity 4 only"
    rationale: "Security + epoch features required"
    status: active
    
  - id: DEC-002
    date: 2026-07-08
    topic: vulnerability-allowlist
    decision: "Allowlist transitive Rust vulns"
    rationale: "No local upgrade path; upstream dependency"
    status: active
    affected:
      - rustls-webpki
      - bigint-buffer
      - crossbeam-epoch
      
  - id: DEC-003
    date: 2026-07-08
    topic: gitguardian-patterns
    decision: "Avoid PASSWORD/SECRET in env var names"
    rationale: "GitGuardian false positives on variable names"
    status: active
```

---

## 🔗 Relationship Map

### Conxian-Labs Operational View

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONXIAN-LABS OPERATIONS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │ conxian-     │◀─────── DEPENDS ON ───────┌───────────────┐ │
│  │ business     │                              │ lib-conxian- │ │
│  │ (Knowledge)  │                              │ core         │ │
│  └──────┬───────┘                              │ (Shared)     │ │
│         │                                          └──────▲──────┘ │
│         │                                                 │        │
│  ┌──────┴───────┐    ┌──────────────┐    ┌───────────┴────────┐ │
│  │ conxian-     │───▶│ conxian-     │───▶│ conxius-          │ │
│  │ nexus        │    │ gateway      │    │ enclave-sdk       │ │
│  │ (Protocol)   │    │ (Bridge)     │    │ (Security)        │ │
│  └──────────────┘    └──────────────┘    └───────────────────┘ │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ conxius-     │───▶│ conxius-     │     OWNED BY            │
│  │ wallet       │    │ platform     │     CONXIAN-LABS        │
│  │ (Client)     │    │ (DevOps)     │     (Pty) Ltd           │
│  └──────────────┘    └──────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CONXIAN.ORG GOVERNANCE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │ Treasury     │◀─────── GOVERNS ───────┌───────────────┐    │
│  │ Operations   │                         │ Protocol      │    │
│  └──────┬───────┘                         │ Upgrades      │    │
│         │                                  └───────────────┘    │
│  ┌──────┴───────┐                                               │
│  │ Token Holder │                                               │
│  │ Governance   │                                               │
│  └──────────────┘                                               │
│                                                                  │
│  RELATION: Conxian-Labs operates for Conxian.org               │
│             Conxian.org governs Conxian-Labs                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Dependency Graph (By Repo)

```
conxian-business
├── pnpm-lock.yaml
│   ├── undici ⚠️ [6 vulns] → fixable
│   ├── ws ⚠️ [2 vulns] → fixable
│   ├── form-data ⚠️ [1 vuln] → fixable
│   └── vite ⚠️ [1 vuln] → fixable
│
├── Cargo.lock (lib-conxian-core)
│   ├── rustls-webpki ⚠️ [1 vuln] → unfixable (bdk chain)
│   ├── crossbeam-epoch ⚠️ [1 vuln] → unfixable (sled chain)
│   └── bigint-buffer ⚠️ [1 vuln] → unfixable (bdk chain)
│
└── .github/workflows/
    ├── conxian-unified-ci.yml (cargo audit ignore list)
    └── secret-scan.yml (gitleaks v8.24.2)
```

---

## 📊 Query Indexes

### By Repository

| Repo | Type | Vulns | Fixable | Owner |
|------|------|-------|---------|-------|
| conxian-business | knowledge-ops | 23 | 11 | Conxian-Labs |
| lib-conxian-core | shared-lib | 3 | 0 | Conxian-Labs |

### By Severity

| Severity | Count | Fixable | Action |
|----------|-------|---------|--------|
| High | 8 | 6 | Fix now |
| Moderate | 8 | 0 | Monitor |
| Low | 7 | 0 | Accept |

### By Stakeholder

| Stakeholder | Responsibility | Active Issues |
|-------------|----------------|---------------|
| Conxian-Labs | Operations | 23 open |
| Conxian.org | Governance | 0 direct |

---

## 🔄 Change Log

### Session 62 Audit & Research Candidate Gap Scoring & Ledger Schema Remediation (September 2026)

- **Audit & Schema Remediation**: Remediated `docs/bos_research_candidate_ledger.json` schema rules (setting `exhaustiveEcosystemAudit: false`, updating `unscoredGaps` dispositions, and maintaining candidate totals).
- **Top Scored Research Candidates**:
  1. `lib-conxian-core#227` (Score: 88) - BDK std-only configuration (Selected Technical Candidate).
  2. `conxian-market-alignment#10` (Score: 87) - AI Marketplace & Agentic Commerce surface mapping.
  3. `conxian-nexus#169/pr#172` (Score: 86) - Nexus dependency remediation.
  4. `conxian-protocol-deprecation#612` (Score: 85) - Protocol deprecation alignment.
  5. `conxian-business#943` (Score: 84) - GitHub-first BOS research-cycle authority (Selected Authority Candidate).
  6. `core-nexus-rustsec-2026-0204` (Score: 83) - Crossbeam-epoch safety remediation.
  7. `unmaintained-bdk-sled-fxhash-instant-research` (Score: 81) - BDK persistence driver removal.
- **Verification Status**: All diagnostic suites (`verify_bos_research_candidate_ledger.py`, `verify_doctrine_alignment.py`, `verify_lts_compliance.py`, `bos_repo_check.py`) pass 100%.



```yaml
changelog:
  - version: 3.2
    date: 2026-09-07
    changes:
      - "Session 62: Research candidate ledger schema remediation & gap scoring synthesis"
      - "Remediated docs/bos_research_candidate_ledger.json schema rules (exhaustiveEcosystemAudit: false, unscoredGaps dispositions)"
      - "Verified 100% PASS on python3 scripts/verify_bos_research_candidate_ledger.py"
      - "Synchronized Knowledge Base, Knowledge Graph, and Changelog"

  - version: 3.1
    date: 2026-08-22
    changes:
      - "Session 61: Full multi-repo research synthesis & repo check integrity audit"
      - "Resolved SUMMARY.md broken link violation (Conxian/docs/ARCHITECTURE.md -> docs/CONXIAN_PROTOCOL_BOS_BUILDOUT.md)"
      - "Restored 100% PASS state on python3 scripts/bos_repo_check.py across all 7 verification suites"
      - "Verified research candidate scoring alignment: Core #227 (88/100) and Business #943 (84/100)"
      - "Confirmed Core PR #231 implementation readiness for BDK/rustls security overlay"

  - version: 3.0
    date: 2026-07-31
    changes:
      - "Session 46: Full Dependabot audit across 16 repos (61 alerts in monorepo)"
      - "Conxian/Conxian: postcss GHSA-r28c fixed via npm audit fix"
      - "Documented 40+ alerts in dependabot-fixes.md with per-repo fix commands"
      - "Clarity contracts: 8 fixed (non-ASCII, parens, type mismatches, contract-call? wrapping)"
      - "5 service stubs created (bip21, lightning, seed, storage, signer) — 18 excluded tests now pass"
      - "CXLP token re-assessed: fully functional (KB 'mint/burn broken' was outdated)"
      - "pausable.clar ACL gap documented (permissionless pause, dead code)"
      - "cxd-price-initializer stub gap documented"
      - "CON-383 Nexus stub status verified: all [STUB] markers removed, zero exclusions"
      - "BOS Knowledge Graph updated with code locations and gap details"

  - version: 2.3
    date: 2026-07-08
    changes:
      - "Fixed CodeQL alerts across 4 repos"
      - "Added weekly-security-update.sh script"
      - "Updated CodeQL status"

  - version: 2.2
    date: 2026-07-08
    changes:
      - "Added CodeQL Alerts Registry"
      - "Mapped alerts to submodules"
      - "Added remediation patterns"

  - version: 2.1
    date: 2026-07-08
    changes:
      - "Added Upgrade Guide section"
      - "Added Version Update Protocol"
      - "Added Entity ID Sequences"
      - "Upgradeable: YES"

  - version: 2.0
    date: 2026-07-08
    changes:
      - "Agentic-first redesign"
      - "Added IF-THEN action rules"
      - "Expanded vulnerability registry"
      - "Added Query -> Section mapping"
      - "Machine-readable schema"

  - version: 1.0
    date: 2026-07-08
    changes:
      - "Initial framework"
      - "Multi-dimensional structure"
      - "Repository registry"
      - "Vulnerability registry"
```

---

## 🔧 Knowledge Base Upgrade Guide

### Adding New Entities

```yaml
# 1. Assign next ID in sequence
# 2. Add to appropriate section
# 3. Update version and changelog
# 4. Add cross-references in relations

# Example: New Repository
repositories:
  new-repo:
    id: REPO-XXX  # Next available
    type: <type>
    owner: <owner>
    # ... other fields
    related: [<existing IDs>]
    tags: [<searchable tags>]

# Example: New Vulnerability
vulnerabilities:
  items:
    - id: VULN-XXX  # H001-H999, M001-M999, L001-L999
      alert: "#XXX"
      pkg: <package>
      ecosystem: <npm|cargo>
      severity: <high|moderate|low>
      fixable: <true|false>
      fix: "<command if fixable>"
      affects: [<affected files>]

# Example: New Decision
decisions:
  - id: DEC-XXX  # Next sequence
    date: <ISO8601>
    topic: <topic>
    decision: <decision>
    rationale: <why>
    status: <active|deprecated|superseded>
    superseded-by: <DEC-XXX if applicable>
```

### Version Update Protocol

```yaml
upgrade-protocol:
  trigger: "Any modification to knowledge base"
  
  steps:
    1: "Increment version number"
       - major: "Breaking changes to schema"
       - minor: "New entities or sections"
       - patch: "Corrections, typo fixes"
       
    2: "Update changelog"
       - add: "{version, date, changes[]}"
       
    3: "Cross-reference new entities"
       - update: "relations in related entities"
       - add: "tags for discoverability"
       
    4: "Verify machine-readability"
       - check: "YAML syntax valid"
       - check: "IDs unique and sequential"
       - check: "Dates in ISO8601"
```

### Entity ID Sequences

```yaml
id-sequences:
  repositories: "REPO-001 to REPO-999"
  vulnerabilities-high: "VULN-H001 to VULN-H999"
  vulnerabilities-moderate: "VULN-M001 to VULN-M999"
  vulnerabilities-low: "VULN-L001 to VULN-L999"
  decisions: "DEC-001 to DEC-999"
  secrets: "SEC-001 to SEC-999"
  stakeholders: "STAKE-001 to STAKE-999"
```

---

## 📋 Agent Checklist Template

When processing any task, agents should:

```yaml
agent-checklist:
  spatial:
    - Identify affected repository (REPO-XXX)
    - Check blast radius (what depends on this?)
    - Map file locations

  temporal:
    - Check decision log (DEC-XXX) for prior decisions
    - Note creation/update dates
    - Verify version compatibility

  relational:
    - Identify stakeholder (Conxian-Labs vs Conxian.org)
    - Check dependency chains
    - Note cross-repo impacts

  logical:
    - Retrieve decision rationale
    - Verify against operational standards
    - Check for superseding decisions

  security:
    - Scan vulnerability registry
    - Check for fixable vulnerabilities
    - Verify allowlist compliance

  operational:
    - Run appropriate CI checks
    - Follow commit protocol
    - Cherry-pick to PR branches if needed
```

---

*This document is the authoritative source for multi-dimensional knowledge.*
*Use for: diff, inspection, research, implementation, verification*
*AI-Ingestible: YES | Machine-Readable: YES | Versionable: YES*

---

## 🤖 Agent Evolvability Contract

**This framework is built FOR agents to evolve.**

```
Agent Permission:
├── Read any section
├── Add new entities (follow ID sequences)
├── Update version + changelog
├── Suggest improvements to structure
├── Fix errors immediately
└── Push changes to main + cherry-pick to PR

Session Protocol:
1. Start: Read BOS_KNOWLEDGE_FRAMEWORK.md
2. Work: Apply knowledge, update as needed
3. End: Crystallize new learnings back to framework
4. Commit: "Co-authored-by: openhands <openhands@all-hands.dev>"
```

**No permission needed** - the framework is designed for autonomous evolution.

---

## 🔄 Weekly Automation

```yaml
weekly-update:
  script: "scripts/weekly-security-update.sh"
  schedule: "Every Monday 06:00 UTC"
  actions:
    - "Fetch all submodules"
    - "Pull main"
    - "Check Dependabot alerts"
    - "Update CodeQL registry"
    - "Increment version"
    - "Commit + push"

  run-manually: |
    cd conxian-business
    ./scripts/weekly-security-update.sh
```

### Dependabot Alert Status (Updated 2026-07-31 — Session 46)

```yaml
dependabot-alerts:
  audit-date: "2026-07-31"
  
  Conxian/Conxian:
    open: 4
    fixed: 1  # postcss GHSA-r28c-9q8g-f849 via npm audit fix
    unfixable: 1  # elliptic GHSA-848j (low, no patch)
    remaining: 2  # postcss GHSA-6g55, brace-expansion GHSA-g7r4 (low, indirect)
    
  conxian-business (monorepo):
    open: 61  # 1 critical, 27 high, 27 moderate, 6 low
    note: "Submodule monorepo — alerts span all child repos"
    fixed_direct: 0  # pnpm repos blocked by sandbox network
    documented: "dependabot-fixes.md has per-repo remediation commands"
    
  conxian_ui:
    open: 13
    top_alert: "Next.js SSRF/DoS (GHSA-89xv, GHSA-p9j2, GHSA-m99w)"
    fix: "pnpm update next postcss sharp js-yaml fast-uri brace-expansion"
    
  conxius-platform:
    open: 7
    top_alert: "undici x4 (GHSA-vxpw, GHSA-hm92, GHSA-vmh5, GHSA-38rv)"
    fix: "pnpm update sharp undici brace-expansion"
    
  conxian-gateway:
    open: 9
    top_alerts: ["postcss (2 CVEs)", "sharp/libvips (3 CVEs)", "brace-expansion", "rustls-webpki"]
    fix: "pnpm update postcss sharp brace-expansion; cargo update webpki-roots"
    
  conxian-nexus:
    open: 3
    top_alert: "rustls-webpki GHSA-82j2 — CRL BIT STRING panic"
    fix: "cargo update webpki-roots"
    
  conxius-wallet:
    open: 3
    top_alert: "bigint-buffer GHSA-3gc7 — buffer overflow via toBigIntLE()"
    fix: "pnpm update bigint-buffer"

  # Critical alert
  critical:
    - id: DEP-CRIT-001
      alert: "GHSA-23hp-3jrh-7fpw"
      pkg: "node-tar"
      severity: "critical"
      fixable: true
      fix: "pnpm update tar"
      affects: ["conxian-business workspace (pnpm)"]
  
  # Unfixable
  unfixable:
    - id: DEP-UNF-001
      alert: "GHSA-848j-6mx2-7j84"
      pkg: "elliptic"
      severity: "low"
      reason: "No fix available. Recommendation: replace with @noble/secp256k1"
      affects: ["Conxian/Conxian (npm)"]
      
    - id: DEP-UNF-002
      alert: "#58"
      pkg: "rustls-webpki"
      severity: "high"
      reason: "Transitive via bdk -> electrum-client chain. Resolved by Core PR #231 (BDK std-only overlay)"
      affects: ["Cargo.lock (lib-conxian-core)"]
```

### CodeQL Alert Status (from prior session)
```yaml
codeql-fixes:
  Conxian: fixed (CSQL-H001, commit 19a207c)
  conxius-wallet: fixed (CSQL-M001-M003)
  .github (org): fixed (CSQL-M004)
  conxian-nexus: fixed (CSQL-M005)
  Conxian_UI: pending (CSQL-H003 DOM XSS — file location unclear)
```


## Session 64 Update (2026-09-08 — Client Onboarding Review, Unified Installer & Research Candidate Scoring Expansion)
- Conducted full system review of client purchase tiers (Community, Business, Enterprise), 9-submodule setup walkthrough, secret parameters, and connectivity matrix in `docs/CLIENT_ONBOARDING_AND_UNIFIED_INSTALLER_SPEC.md`.
- Recommended and specified the Rust-based **Conxian Unified Installer CLI (`cxn`)** to reduce Time-To-First-Value (TTFV) under 15 minutes.
- Expanded research candidate ledger analysis (`docs/bos_research_candidate_ledger.json` and `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`) incorporating client onboarding and unified installer gap dispositions.
- Executed 100% PASS verification across `python3 scripts/bos_repo_check.py` and `python3 scripts/verify_bos_research_candidate_ledger.py`.

## Session 63 Update (2026-09-08 — End-to-End Client Onboarding & System Setup)
- Created canonical  defining client purchase tiers, component setup, connectivity verification, and the unified  installer specification.
- Conducted full system review across all 9 core submodules (, , , , , , , , ).
- Verified zero submodule drift, release hygiene, and candidate research ledger alignment (Success: BOS research candidate ledger verified (/app/docs/bos_research_candidate_ledger.json).).

## Session 65 Update (2026-09-08 — Optimal BOS Setup, Multi-Tier Topology & Submodule Orchestration)
- **Optimal BOS Setup & Topology Architecture**: Consolidated multi-tier operational topology spanning Community (open-source/self-hosted), Business (dedicated cloud/SLA), and Enterprise (Nitro enclave/HSM) deployment profiles across the 9 active submodules (`conxian-gateway`, `conxian-nexus`, `lib-conxian-core`, `conxius-enclave-sdk`, `conxius-wallet`, `conxian-ui`, `conxius-platform`, `conxius-orbit`, `conxian_market`).
- **Unified Installer (`cxn`) Integration**: Integrated specifications for the zero-dependency Rust binary installer targeting Time-To-First-Value (TTFV) < 15 minutes with automated env validation, database schema migration, and enclave attestation verification.
- **Security & Domain Separation Firewall**: Reinforced strict boundary rules separating Developer Protocol Surface (`conxian.org`) from Corporate Governance Surface (`conxian-labs.com`) and enforced non-custodial hardware attestation standards.
- **Verification & Integrity**: Passed 100% verification across `python3 scripts/bos_repo_check.py`, `python3 scripts/verify_bos_research_candidate_ledger.py`, and `python3 scripts/verify_client_onboarding.py`.

## Session 66 Update (2026-09-26 — Organization-Wide SLA Positioning, Support Matrix & BaaP Commercial Pricing Architecture)
- **Organization-Wide SLA Realignment**: Re-aligned SLA positioning across the entire Conxian GitHub ecosystem. Enforced open-source community disclaimers (NO SLA, community best-effort) on public protocol surfaces (`conxian` org) while establishing contractual SLAs (99.5% uptime target, SEV1 1h ack) for B2B Enterprise Gateway deployments.
- **BaaP 3-Layer Pricing Architecture**: Codified 3-layer Business-as-a-Platform (BaaP) commercial monetization model covering Protocol Escrow Settlement (2.0% volume fee, 80/10/10 split, Tier 1-4 volume fee decay), Enterprise SaaS Node Licensing ($2,500–$40,000/mo), and Metered Edge Compute & x402 Attestation Fees.
- **Source-of-Truth Governance**: Updated `docs/SLA.md`, `docs/SLA_POLICY.md`, `docs/COMMERCIAL_PACKAGING_DOCTRINE.md`, `docs/GAPS.md`, and `docs/PORTFOLIO.md`.

## Session 67 Update (2026-10-11 — Phased Research & Org-Wide Business Operations System Expansion)
- **Phased Strategic Research Architecture**: Established a canonical 4-phase research methodology to structure BOS business logic, intelligence, and operations research:
  - *Phase 1: Strategic Intelligence & Business Systems Reconnaissance*: Comprehensive org-wide repository taxonomy across 4 business unit pillars (`conxian-gateway`, `conxian_market`, `conxian-nexus`, `conxius-enclave-sdk`), strict domain boundary separation (`conxian.org` developer protocol surface vs `conxian-labs.com` corporate surface), and submodule pin-to-parent alignment.
  - *Phase 2: BaaP Commercial Monetization & Financial Engineering*: Deepened 3-layer BaaP commercial financial model, 80/10/10 yield splitter (80% developer pool, 10% operations pool, 10% network pool), ADR-004 volume-based fee decay, cost-plus rail floors, and 12-month runway analytics.
  - *Phase 3: ISO 20022 / CJCS v2.0 Operational Integration & AI Agentic Commerce*: Field-level translation of legacy banking messages (`pacs.008`, `pacs.002`, `camt.053`) into Conxian Job Card Schema (CJCS) v2.0 intents, multi-chain settlement routing (BTC L1, Stacks L2, RGB, Babylon, Lightning, EVM), Model Model Protocol (MCP) inter-agent execution, and AI Marketplace rate/pricing controls.
  - *Phase 4: Knowledge Base & Research Candidate Scoring Ledger Synthesis*: Upgraded Knowledge Framework to Version 3.7, expanded research candidate ledger (`docs/bos_research_candidate_ledger.json`), updated `BOS_KNOWLEDGE_GRAPH.md`, and passed 100% of repository verification checks (`bos_repo_check.py`, `verify_bos_research_candidate_ledger.py`, `verify_cross_repo_alignment.py`, `verify_doctrine_alignment.py`, `verify_client_onboarding.py`).
- **Release Hygiene Remediation**: Resolved `conxius-enclave-sdk` CHANGELOG version mismatch, bringing all 8 core submodules into full release hygiene compliance.

## Session 71 Update (2026-10-24 — System-Wide Evaluation & Agentic Transformation Blueprint)
- **Agentic Transformation Blueprint Synthesis**: Formulated canonical specification `docs/research/AGENTIC_SYSTEM_WIDE_EVALUATION_AND_TRANSFORMATION_BLUEPRINT_2026.md` detailing Conxian's architectural transition from deterministic infrastructure into an AI-First Autonomous Business Stack.
- **CXIP Proposal Taxonomy Alignment**: Established unified improvement proposal taxonomy across all 8 active workspace repositories:
  - *CXMIP (`conxian_market`)*: Dynamic M2M agent bargaining protocol, TEE-isolated LLM dispute arbiters, and native MCP server exposing 33 SDK capabilities.
  - *CXBIP (`conxian-business`)*: Autonomous OpenSpec resolvers, active TEE executive agents, and automated 80/10/10 yield splits.
  - *CXGIP (`conxian-gateway`)*: AI-first liquidity & rail router, natural language to ISO 20022 (`pacs.008`/`pacs.002`/`camt.053`) synthesizer.
  - *CXCIP (`lib-conxian-core` / `conxius-enclave-sdk`)*: Ephemeral self-provisioning enclave keyrings and delegated EIP-7710 spending guardrails.
  - *CXNIP (`conxian-nexus`)*: Self-healing multi-chain state reorg monitor, automated RBF/CPFP fee bumping, and BitVM3 fraud proof challenges.
  - *CXWIP / CXPIP (`conxius-wallet` / `conxius-platform`)*: Delegated ERC-7710 agent command center and zero-secret-egress (ZSE) privacy filters.
- **3-Phase Execution Roadmap**: Defined actionable prioritization roadmap spanning Phase 1 (MCP & Agent Discovery, 1-30 Days), Phase 2 (Enclave Guardrails & Self-Provisioning, 30-90 Days), and Phase 3 (Autonomous Operations & Dispute Arbitration, 90+ Days).
- **Candidate Ledger & Indexing**: Expanded `docs/bos_research_candidate_ledger.json` (`agentic-system-wide-evaluation-blueprint-gap`), updated `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md`, `BOS_KNOWLEDGE_GRAPH.md`, and `SUMMARY.md`. Passed 100% of repository verification checks (`bos_repo_check.py`, `verify_bos_research_candidate_ledger.py`, `verify_cross_repo_alignment.py`, `verify_doctrine_alignment.py`, `verify_client_onboarding.py`).

## Evidence addendum (2026-10-15 — corporate identity and alert boundaries)
- [Corporate identity and alert routing research](research/ZOHO_MAIL_IDENTITY_AND_ALERT_ROUTING_FIREWALL_RESEARCH.md) distinguishes corporate correspondence, identity-provider authentication, application provisioning, workload authorization, and signing custody.
- These are proposed controls. No external SSO tenant, automatic application deactivation, session revocation, alert alias, or hardware qualification is established by this research. Keep implementation and evidence under business #1390; PR #1364 enters through dev with existing promotion policy and tests intact.
