# Conxian Master Gap Register & Pillar Alignment

| Metadata | Value |
|---|---|
| Authority | [Business issue #943](https://github.com/Conxian/conxian-business/issues/943) |
| Standard | Conxian BOS v1.9.5 |
| Classification | Public-safe governance gap register |
| Last Updated | 2026-09-18 |

---

## Pillar Alignment Standard

All ecosystem gaps and candidate solutions are evaluated against the Conxian Three Pillars:
1. **Vertical Sovereignty**: Advances user-owned infrastructure from L1 to interface.
2. **Operational Unification**: Advances centralized gateway and shared cryptographic cores.
3. **Nakamoto Readiness**: Advances Stacks Epoch 3.0 alignment and Bitcoin L1 finality.

Any candidate scoring below **3.0 / 5.0** on the weighted matrix is rejected or deferred.

---

## Gap Register

| Gap ID | Function Area | As-Is State | To-Be State | Nature of Gap | Priority | Pillar Alignment | Source Reference | Status |
|---|---|---|---|---|---|---|---|---|
| `GAP-ID-01` | Identity | Machine identity uses ephemeral keys without TEE attestation binding | Nitro TEE backed machine identity with hardware attestation proofs | Technical / Security | High | Vertical Sovereignty | `conxius-enclave-sdk` | Open |
| `GAP-VER-01` | Verification | UCV-1 verification pipeline operates independently in Nexus | Integrated UCV-1 verification hooks in Gateway settlement pipeline | Technical / Integration | Critical | Operational Unification | `conxian-gateway` #102 | In Progress |
| `GAP-ESC-01` | Escrow | M2M market escrow relies on off-chain coordinator | DLC CET flow for Bitcoin-native non-custodial escrow | Cryptographic / Protocol | High | Vertical Sovereignty | `conxian_market` #9 | Open |
| `GAP-SET-01` | Settlement | BitVM2 settlement bridge handles single-tap proofs | BitVM3 / DLC multi-tap settlement with R32 fail-closed protection | Protocol / L1 | Critical | Nakamoto Readiness | `lib-conxian-core` #227 | In Progress |
| `GAP-DIS-01` | Discovery | Agent listings require manual registry entries | Automated agent discovery & registry via CJCS v2.0 endpoints | Platform / M2M | Medium | Operational Unification | `conxian_market` | Open |
| `GAP-TRU-01` | Trust Surface | Proof artifacts generated manually during build cycles | Automated attestation record & proof artifact generation | Compliance / Audit | High | Vertical Sovereignty | `docs/CLAIM_EVIDENCE_MATRIX.md` | Verified |
| `GAP-DOC-01` | Documentation | Cross-repo positioning and SLA commitments fragmented | Unified source-of-truth docs (`PORTFOLIO.md`, `SLA.md`, `ALIGNMENT.md`, `GAPS.md`) | Governance | Critical | Operational Unification | `docs/BOS_KNOWLEDGE_FRAMEWORK.md` | In Progress |
| `GAP-TST-01` | Test Coverage | Submodule unit tests run isolated without E2E Gateway-Nexus harness | E2E integration test harness spanning Gateway, Nexus, Core, and SDK | CI / QA | High | Operational Unification | `scripts/verify_client_onboarding.py` | Verified |
| `GAP-SLA-01` | SLA | Legacy SLA policy references external contracts without concrete v1 parameters | Realistic v1 SLA (99.5% uptime, business-hours SEV1, no financial credits) | Commercial | High | Operational Unification | `docs/SLA_POLICY.md` | In Progress |
| `GAP-LIC-01` | Licensing | GPL-3.0 business repo vs MIT/commercial tier boundaries unmapped | Dual-license commercial packaging doctrine (Community, Business, Enterprise) | Legal / Licensing | High | Vertical Sovereignty | `docs/COMMERCIAL_PACKAGING_DOCTRINE.md` | Verified |

---

## Candidate Evaluation & Weighted Score Matrix

### Scoring Weights
- **Pillar Alignment**: 25%
- **Gap Coverage**: 25%
- **Implementation Cost**: 15% (inverted: 5=low cost)
- **Risk**: 15% (inverted: 5=low risk)
- **Testability / Verifiability**: 10%
- **Architecture Alignment**: 10%

### Candidate Scores

| Candidate | Target Gap | Pillar (25%) | Gap Cov (25%) | Cost (15%) | Risk (15%) | Test (10%) | Arch (10%) | Weighted Total | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| `CAN-01` Core BitVM2/3 Bridge (#227) | `GAP-SET-01` | 5.0 | 5.0 | 3.0 | 3.0 | 4.0 | 5.0 | **4.30 / 5.0** | **Selected** |
| `CAN-02` Unified Source-of-Truth Docs | `GAP-DOC-01` | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | 5.0 | **5.00 / 5.0** | **Selected** |
| `CAN-03` Market M2M Escrow DLC | `GAP-ESC-01` | 5.0 | 4.0 | 3.0 | 3.0 | 4.0 | 4.0 | **3.95 / 5.0** | Retained under owner |
| `CAN-04` Legacy Monolith Preservation | `GAP-DOC-01` | 1.0 | 1.0 | 2.0 | 1.0 | 2.0 | 1.0 | **1.15 / 5.0** | **Rejected (< 3.0)** |
