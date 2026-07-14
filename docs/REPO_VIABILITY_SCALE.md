# Conxian Repository Viability Scale (RVS)
> **Purpose**: Standardized assessment framework for evaluating repository health, readiness, and strategic value
> **Version**: 1.0.0
> **Generated**: 2026-07-14
> **Alignment**: BOS v1.9.5, Unified Theory v2.0

---

## 1. Overview

The Repository Viability Scale (RVS) provides a **multi-dimensional scoring system** to assess repositories against Conxian's operational standards. It aligns with the **Unified Theory** metrics ($C_R$, $O_C$, $V_X$, $A_S$, $N_E$) and the **BOS Knowledge Framework**.

### 1.1 Scoring Philosophy

| Score Range | Classification | Action |
|-------------|----------------|--------|
| **90-100** | 🟢 **PRODUCTION READY** | Ship, scale, monitor |
| **70-89** | 🟡 **OPERATIONAL** | Enhance, automate, improve |
| **50-69** | 🟠 **DEVELOPMENT** | Accelerate, resource, prioritize |
| **30-49** | 🔴 **BLOCKED** | Remediate, align, resolve |
| **0-29** | ⚫ **ARCHIVE** | Deprecate, sunset, preserve |

---

## 2. Assessment Dimensions

Each repository is evaluated across **6 dimensions** totaling 100 points:

| Dimension | Code | Weight | Description |
|-----------|------|--------|-------------|
| **Security & Sovereignty** | $D_{SS}$ | 20 pts | Access control, key management, ZK compliance |
| **Operational Autonomy** | $D_{OA}$ | 20 pts | $A_S$ alignment, automation coverage |
| **Cost & Reproduction** | $D_{CR}$ | 15 pts | $C_R$ assessment, moat strength |
| **Execution Velocity** | $D_{EV}$ | 15 pts | $V_X$ alignment, CI/CD maturity |
| **Network Effects** | $D_{NE}$ | 15 pts | $N_E$ potential, adoption metrics |
| **Documentation** | $D_{DOC}$ | 15 pts | BOS alignment, knowledge capture |

---

## 3. Scoring Rubric

### 3.1 Security & Sovereignty ($D_{SS}$) — 20 pts

| Score | Criteria |
|-------|----------|
| **20** | DAO-governed, BYOK mandatory, ZK proofs active, zero admin keys |
| **16** | DAO transition in progress, BYOK supported, admin keys <5 |
| **12** | Multi-sig controls, partial BYOK, admin keys <20 |
| **8** | Admin-key controlled, no ZK, single operator |
| **4** | Known vulnerabilities (HIGH), no access control |
| **0** | Critical vulns unfixed, compromised state |

### 3.2 Operational Autonomy ($D_{OA}$) — 20 pts

| Score | Criteria |
|-------|----------|
| **20** | $A_S$ > 90%, fully automated ops, zero manual intervention |
| **16** | $A_S$ > 70%, mostly automated, rare manual fixes |
| **12** | $A_S$ > 50%, automation exists, gaps in coverage |
| **8** | $A_S$ > 30%, significant manual ops required |
| **4** | $A_S$ < 30%, mostly manual, scripted workarounds |
| **0** | No automation, fully manual operations |

### 3.3 Cost & Reproduction ($D_{CR}$) — 15 pts

| Score | Criteria |
|-------|----------|
| **15** | Proprietary moat (TEE, Clarity, hardware), hard to replicate |
| **12** | Strong moat, specialized integrations, niche expertise required |
| **9** | Moderate moat, some differentiation, forkable with effort |
| **6** | Weak moat, standard tech, easily replicated |
| **3** | No moat, commodity tech, trivial to fork |
| **0** | Open-source with no barriers |

### 3.4 Execution Velocity ($D_{EV}$) — 15 pts

| Score | Criteria |
|-------|----------|
| **15** | CI/CD green, tests >80%, PRs merged daily, $V_X$ maximized |
| **12** | CI/CD mostly green, tests >60%, weekly merges |
| **9** | CI/CD functional, tests >40%, sporadic merges |
| **6** | CI/CD partial, tests <40%, blocked releases |
| **3** | Manual releases, no tests, high regression risk |
| **0** | No CI/CD, releases blocked |

### 3.5 Network Effects ($D_{NE}$) — 15 pts

| Score | Criteria |
|-------|----------|
| **15** | $N_E$ > 5x, active external adoption, ecosystem growth |
| **12** | $N_E$ > 3x, internal adoption, partnership pipeline |
| **9** | $N_E$ > 1.5x, growing usage, retention strong |
| **6** | $N_E$ = 1x, stable users, no growth |
| **3** | $N_E$ < 1x, declining, churn risk |
| **0** | $N_E$ = 0, zero adoption |

### 3.6 Documentation ($D_{DOC}$) — 15 pts

| Score | Criteria |
|-------|----------|
| **15** | BOS aligned, AGENTS.md complete, all docs current,知识 graph updated |
| **12** | BOS mostly aligned, AGENTS.md exists, docs mostly current |
| **9** | Partial BOS alignment, basic docs, gaps identified |
| **6** | Minimal docs, no AGENTS.md, stale information |
| **3** | No docs, tribal knowledge only |
| **0** | Docs exist but are actively misleading |

---

## 4. Unified Theory Alignment

### 4.1 Dimension-to-Variable Mapping

```python
D_SS = Security & Sovereignty  # Protects C_R from erosion
D_OA = Operational Autonomy     # Directly maps to A_S
D_CR = Cost & Reproduction      # Directly maps to C_R
D_EV = Execution Velocity       # Directly maps to V_X
D_NE = Network Effects          # Directly maps to N_E
D_DOC = Documentation           # Reduces O_C through knowledge transfer
```

### 4.2 Total Score Formula

$$RVS_{total} = D_{SS} + D_{OA} + D_{CR} + D_{EV} + D_{NE} + D_{DOC}$$

### 4.3 Classification Thresholds (by Repo Type)

The scoring is **normalized by repo type** because a documentation/research repo (conxian-market) has different expectations than a production protocol (conxian-gateway).

| Class | Code Repo | Docs/Research Repo | Protocol Repo |
|-------|-----------|-------------------|---------------|
| 🟢 PRODUCTION | 80-100 | 70-90 | 85-100 |
| 🟡 OPERATIONAL | 60-79 | 50-69 | 65-84 |
| 🟠 DEVELOPMENT | 40-59 | 30-49 | 45-64 |
| 🔴 BLOCKED | 20-39 | 15-29 | 20-44 |
| ⚫ ARCHIVE | 0-19 | 0-14 | 0-19 |

### 4.4 Repo Type Classification

| Type | Description | Examples |
|------|-------------|----------|
| **Code** | Production code repositories | conxian-gateway, conxius-wallet, conxian-nexus |
| **Docs/Research** | Documentation and strategy | conxian-market, conxian-labs-site |
| **Protocol** | On-chain contracts | Conxian/, lib-conxian-core |

### 4.5 Score Normalization Formula

$$RVS_{normalized} = \left(\frac{RVS_{raw}}{D_{max}}\right) \times Type_{max}$$

Where:
- $D_{max}$ = 80 (maximum raw dimension score)
- $Type_{max}$ = 100 (code), 90 (docs/research), 100 (protocol)

---

## 5. Assessment Checklist

### 5.1 Pre-Assessment

- [ ] Repository cloned and accessible
- [ ] Last commit date verified
- [ ] CI/CD status checked
- [ ] Open issues/PRs reviewed
- [ ] Submodule dependencies confirmed

### 5.2 Security Assessment ($D_{SS}$)

- [ ] Access control model documented
- [ ] Admin-key audit completed
- [ ] ZK compliance verified
- [ ] BYOK support confirmed
- [ ] Vulnerability scan results reviewed

### 5.3 Autonomy Assessment ($D_{OA}$)

- [ ] Manual intervention frequency measured
- [ ] Automation coverage mapped
- [ ] BOS integration verified
- [ ] Error handling reviewed
- [ ] Fallback procedures documented

### 5.4 Documentation Assessment ($D_{DOC}$)

- [ ] AGENTS.md exists and current
- [ ] README complete with role-line
- [ ] BOS alignment confirmed
- [ ] OpenSpec specs linked
- [ ] Changelog maintained

---

## 6. Example Assessments

### 6.1 conxian-gateway (Estimated)

```yaml
repository: conxian-gateway
dimension_scores:
  D_SS: 14  # Multi-sig, partial BYOK, <20 admin keys
  D_OA: 12  # Mostly automated, some manual deployment steps
  D_CR: 12  # Strong ISO 20022 moat, specialized adapters
  D_EV: 14  # CI/CD green, good test coverage
  D_NE: 10  # Growing adoption, Fedimint/Citrea pending
  D_DOC: 13 # Good docs, AGENTS.md exists

total_score: 75
classification: 🟡 OPERATIONAL
phase: Phase 3 - Transitioning to autonomy
recommendation: Enhance Fedimint/Citrea adapters, reduce admin keys
```

### 6.2 conxian-market (Estimated)

```yaml
repository: conxian_market
dimension_scores:
  D_SS: 8   # Admin-key controlled (73+ vars), CON-1422
  D_OA: 6   # CON-1427 fee collection is no-op, manual ops required
  D_CR: 14  # Strong AI Labor Exchange moat, ERC-8183
  D_EV: 8   # Docs exist, code stubs, CON-1434 (33% non-functional)
  D_NE: 10  # High potential, sandbox pending (CON-1437)
  D_DOC: 12 # Good research docs, AGENTS.md needed

total_score: 58
classification: 🟠 DEVELOPMENT
phase: Phase 2 - Forge in progress
recommendation: Implement CON-1427, CON-1425, transition to DAO governance
```

### 6.3 conxian-nexus (Estimated)

```yaml
repository: conxian-nexus
dimension_scores:
  D_SS: 12  # Multi-sig controls, ZK proofs in development
  D_OA: 14  # High automation, Glass Node stable
  D_CR: 12  # Strong state verification moat
  D_EV: 14  # CI/CD solid, good test coverage
  D_NE: 12  # Core infrastructure, steady adoption
  D_DOC: 13 # Good docs, specs aligned with BOS

total_score: 77
classification: 🟡 OPERATIONAL
phase: Phase 3 - Transitioning to autonomy
recommendation: Complete ZK proof integration, expand MCP support
```

---

## 7. Implementation

### 7.1 Assessment Script

```bash
# Run repository viability assessment
python3 scripts/repo_viability_assessment.py --repo conxian-market

# Run full portfolio assessment
python3 scripts/repo_viability_assessment.py --all

# Generate report
python3 scripts/repo_viability_assessment.py --report --format markdown
```

### 7.2 CI Integration

Add to `conxian-unified-ci.yml`:

```yaml
- name: Repository Viability Check
  run: python3 scripts/repo_viability_assessment.py --repo ${{ github.event.repository.name }}
  continue-on-error: true
```

---

## 8. Governance

### 8.1 Assessment Cadence

| Repository Class | Assessment Frequency |
|-----------------|---------------------|
| Primary Strategic | Weekly (automated) |
| Supporting | Bi-weekly |
| Reference | Monthly |
| Internal Strategy | Quarterly |

### 8.2 Scoring Actions

| Score Drop | Action Required |
|------------|-----------------|
| >10 pts | Immediate escalation to Operations |
| >20 pts | Escalate to Conxian-Labs leadership |
| Crosses 70→69 | Add to next sprint backlog |
| Crosses 50→49 | Add to current sprint P0 |

---

## 9. Related Documents

- [BOS Knowledge Framework](BOS_KNOWLEDGE_FRAMEWORK.md)
- [Unified Theory v2.0](CONXIAN_UNIFIED_THEORY_v2.md)
- [Market BOS Integration Research](MARKET_BOS_INTEGRATION_RESEARCH.md)
- [Cross-Repo Dependency Map](CROSS_REPO_DEPENDENCY_MAP.md)

---

## 10. Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-14 | Initial framework aligned with Unified Theory v2.0 |

---

*Maintained by: Conxian-Labs Operations*
*Co-authored-by: openhands <openhands@all-hands.dev>*
