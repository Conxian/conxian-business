# Documentation alignment index (conxian-business)

This page is a practical index of the documentation already present in this repository, focused on helping active work reference existing material instead of recreating it.

Portfolio doctrine is defined centrally in [`DOCTRINE_ALIGNMENT_STANDARD.md`](./DOCTRINE_ALIGNMENT_STANDARD.md) and [`PORTFOLIO_DOCTRINE_REGISTER.md`](./PORTFOLIO_DOCTRINE_REGISTER.md). This index is navigation and document disposition only; it must not introduce a competing role, maturity, claim-state, or classification taxonomy.

## Classification rules

- **Canonical**: the current “source of truth” for a domain. If two docs disagree, update the non-canonical doc to match the canonical one.
- **Supporting**: helpful context, audits, reports, briefs, or deep dives that clarify (but don’t define) the system.
- **Public-safe**: ok to link in public contexts and external conversations.
- **Public-safe stub (canonical in authorized Linear workspace)**: safe to link publicly; this repo file is a short pointer stub (see [ZSE stub template](./templates/ZSE_STUB_TEMPLATE.md)). It must not contain any operational, security, financial, legal, and strategic details beyond the pointer. The full canonical content is maintained in the authorized Linear workspace under ZSE.
- **Internal-only (canonical in authorized Linear workspace only)**: operational, security, financial, legal, and strategic material whose canonical document must live only in the authorized Linear workspace. If a repo link target must be preserved, use a **Public-safe stub (canonical in authorized Linear workspace)** (see [ZSE stub template](./templates/ZSE_STUB_TEMPLATE.md)) so existing links continue to resolve.

For the separate dimensions of claim state, operating label, maturity, and document classification, follow the [Doctrine Alignment Standard](./DOCTRINE_ALIGNMENT_STANDARD.md) and the [Portfolio Doctrine Register](./PORTFOLIO_DOCTRINE_REGISTER.md).

Notes:

- Treat this repo as public for boundary purposes; hosting visibility may differ by deployment. "Internal-only" material should not be stored here; when we preserve link targets we use public-safe ZSE stubs (see authorized Linear workspace issue CON-256).
- OpenSpec change sets typically have 4 layers: `proposal.md` (intent), `design.md` (architecture), `specs/*/spec.md` (requirements), `tasks.md` (execution).

## GAP-020 cross-link alignment (issue #724)

### Canonical documentation set

- `docs/DOCTRINE_ALIGNMENT_STANDARD.md`
- `docs/PORTFOLIO_DOCTRINE_REGISTER.md`
- `docs/REPO_PORTFOLIO.md`
- `docs/PORTFOLIO_BUSINESS_UNIT_MAP.md`
- `docs/DOCUMENTATION_ALIGNMENT_INDEX.md`

### README canonical-link coverage

| README | Coverage | Notes |
| --- | --- | --- |
| `conxian-business/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `Fiscal-Vault-Oracle/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `Nakamoto-Guardian/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `Sovereign-Ops-Orchestrator/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `Sovereign-Strategy-Nexus/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `cxn-grid-oracle/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |
| `showcase-dapp/README.md` | ✅ | Includes a `Canonical documentation` block with links to all GAP-020 canonical docs. |

### Archival candidates

- `docs/LINEAR_TASK_INVENTORY_2026-05-29.md` — public-safe stub; the dated planning snapshot moved to the authorized Linear workspace under CON-1530.
- `docs/RESEARCH_FINDINGS_2026-05-29.md` — public-safe stub; the dated research snapshot moved to the authorized Linear workspace under CON-1530.
- `docs/BUSINESS_ANALYSIS_2026-05-29.md` — public-safe stub; the dated analysis moved to the authorized Linear workspace under CON-1530.
- `docs/CONXIAN_MARKET_NARRATIVE_ONE_PAGER.md` — public-safe stub; the dated narrative moved to the authorized Linear workspace under CON-1530.
- `conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md` — public-safe stub; the research summary moved to the authorized Linear workspace under CON-1530.
- `docs/ITIL5_STRATEGIC_ANALYSIS_2026.md` — public-safe stub; the full internal strategy remains in Linear and the former competitive analysis is not retained here.

### CON-1530 public-safe stub dispositions

The following link-preserving stubs are intentionally retained in Git. Their canonical restricted sources are owned by Conxian-Labs (Pty) Ltd in the authorized Linear workspace; no removed detail is copied into another Git file.

| File | Classification | Ownership | Why content moved | Canonical pointer |
| --- | --- | --- | --- | --- |
| `docs/BUSINESS_ANALYSIS_2026-05-29.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Dated internal analysis is not a current public doctrine source. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |
| `conxian-business/BOS_BAAP_RESEARCH_SUMMARY.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Research detail belongs in the authorized workspace, not public Git. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |
| `docs/CONXIAN_MARKET_NARRATIVE_ONE_PAGER.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Dated positioning material is maintained outside the public repository. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |
| `docs/LINEAR_TASK_INVENTORY_2026-05-29.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Internal work-management detail belongs in active authorized systems. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |
| `docs/RESEARCH_FINDINGS_2026-05-29.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Dated findings are superseded and are not a current public doctrine source. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |
| `docs/ITIL5_STRATEGIC_ANALYSIS_2026.md` | Public-safe stub | Conxian-Labs (Pty) Ltd | Internal strategy remains in the authorized workspace under ZSE. | [CON-1530](https://linear.app/conxian-labs/issue/CON-1530/doctrine-alignment-sweep-across-portfolio-docs-whitepapers-readmes-and) |

## 1) Repo navigation (start here)

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `README.md` | Canonical | Public-safe | Repository entrypoint and overall orientation. |
| `SUMMARY.md` | Canonical | Public-safe | GitBook table of contents (used for docs navigation; Pages publishing is allowlisted). |
| `docs/README.md` | Supporting | Public-safe | “Docs hub” landing page. |
| `docs/BOS_BUSINESS_BUILDOUT.md` | Canonical | Public-safe | Repo business purpose, business-unit placement, governance + ownership model, and public/internal split. |
| `docs/GITHUB_FIRST_BOS_OPERATING_MODEL.md` | Canonical | Public-safe | Public-safe BOS research-cycle authority: lifecycle, scoring rubric, phase evidence, ownership boundaries, blockers, and refresh rules under [#943](https://github.com/Conxian/conxian-business/issues/943). |
| `docs/BOS_RESEARCH_CANDIDATE_LEDGER.md` | Supporting | Public-safe | Human-readable 2026-07-28 bounded candidate ledger, linked to its machine-readable companion and deterministic validator; not an exhaustive ecosystem audit. |
| `docs/PRIVATE_REPO_REPO_CHECK_WORKFLOW.md` | Canonical | Public-safe | Repo-check workflow for private repositories (boundary, secrets, hygiene, governance, release maturity). |
| `docs/BRANCH_AND_PROMOTION_STANDARD.md` | Canonical | Public-safe | Canonical `dev`/`staged`/`main` branch roles and promotion workflow. |
| `docs/PROMOTION_CHECKLISTS.md` | Canonical | Public-safe | Required checklists and evidence for feature -> `dev` -> `staged` -> `main` promotions. |
| `docs/INTEGRATED_SYSTEM_TESTNET_GATE.md` | Canonical | Public-safe | Full-system public-testnet gate for `dev` before promotion to `staged`/`main`. |
| `ARCHIVE_MIGRATION.md` | Canonical | Public-safe | ZSE placeholder + pointer to authorized Linear workspace for legacy material. |

## 2) BOS (Business Operations System)

These are the “operating-model” documents that explain how BOS components relate, how execution is intended to be wired into Linear, and what gets measured.

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `conxian-business/SERVICE_LOOP.md` | Supporting | Public-safe | BOS reference loop for client/protocol intent, routing, and verification. |
| `conxian-business/BOS_STATE_MACHINE.stub.json` | Supporting | Public-safe stub (canonical in Linear) | Public-safe BOS state machine pointer stub (standardized ZSE stub). |
| `Sovereign-Ops-Orchestrator/LINEAR_WIRING.md` | Canonical | Public-safe | ExCo Linear-first intake standard (required fields, triage flow, execution linkbacks) with sensitive details remaining in Linear under ZSE. |
| `Sovereign-Ops-Orchestrator/DEPLOYMENT_EFFICIENCY.md` | Supporting | Public-safe stub (canonical in Linear) | Bottleneck and deployment efficiency metrics (standardized ZSE stub). |
| `Sovereign-Strategy-Nexus/REALTIME_M&A_VELOCITY.md` | Supporting | Public-safe stub (canonical in Linear) | Strategy coordination pointer; full internal content remains in Linear (standardized ZSE stub). |
| `Sovereign-Strategy-Nexus/docs/SOVEREIGN_MOI_ALIGNMENT.md` | Canonical | Public-safe stub (canonical in Linear) | “MOI” alignment source for Strategy Nexus narratives (standardized ZSE stub). |
| `Sovereign-Strategy-Nexus/docs/ZK_DATA_ROOM_SCHEMA.md` | Canonical | Public-safe stub (canonical in Linear) | ZK data room schema (standardized ZSE stub). |
| `Sovereign-Strategy-Nexus/docs/SOVEREIGN_PITCH_DECK_NARRATIVE.md` | Supporting | Public-safe stub (canonical in Linear) | Pitch narrative scaffolding (standardized ZSE stub). |
| `Fiscal-Vault-Oracle/SOVEREIGN_RUNWAY.md` | Canonical | Public-safe stub (canonical in Linear) | Protocol/reference policy and oracle constraints (standardized ZSE stub). |
| `Fiscal-Vault-Oracle/LSEG_MCP_AUDIT.md` | Supporting | Public-safe stub (canonical in Linear) | LSEG MCP audit context for treasury/oracle integrity (standardized ZSE stub). |
| `docs/architecture/BOS_TREASURY_AND_YIELD_INTEGRATION_ARCHITECTURE.md` | Canonical | Public-safe | Protocol/tenant treasury and yield integration boundary: intent-based operations, oracle publishing, reconciliation, and failure handling (no dashboard-to-contract coupling). |
| `docs/architecture/BOS_SOVEREIGN_ENTERPRISE_IDENTITY_ARCHITECTURE.md` | Canonical | Public-safe | Enterprise identity + ERP session brokering architecture: hardware-backed keys, attestation, short-lived PoP-bound sessions, and recovery. |
| `docs/protocols/BOS_SELF_EXECUTING_CONTRACT_TRIGGER_V1.md` | Canonical | Public-safe | Verified CLM webhook → queued pending on-chain action with 144-block timelock → multisig finalization, with replay protection, cancellation semantics, monitoring, and audit traceability. |
| `docs/architecture/THREE_LANE_RUNTIME_DEPLOYMENT_ARCHITECTURE.md` | Canonical | Public-safe | Canonical runtime deployment model across community sovereign-node, business-managed, and enterprise/private-cloud lanes (controls, upgrade paths, and trust assumptions). |
| `docs/architecture/BOS_PRESERVE_ENHANCE_REPLACE_GAP_MATRIX.md` | Canonical | Public-safe | Control matrix for preserve/enhance/replace/defer decisions across BOS components (prevents destructive refactors; locks sequencing). |
| `docs/architecture/CONXIAN_L3_PROFILE_ADR.md` | Canonical | Public-safe | Decision ADR for the Conxian L3 profile (settlement model, Nakamoto vs sBTC signer boundary, compatibility-first dual lane, and promotion/rollback gates). |
| `docs/architecture/BITVM2_SBTC_BRIDGE_TARGET_ARCHITECTURE.md` | Canonical | Public-safe | Target-state BitVM2 + sBTC bridge architecture (components, trust boundaries, proof/verification flow, failure controls, and phased rollout checkpoints). |
| `docs/COMPATIBILITY_MATRIX_AND_ACCEPTANCE_GATE_CHECKLIST.md` | Canonical | Public-safe | Cross-repo compatibility matrix and objective acceptance-gate evidence checklist for the 13-repo migration set. |
| `Nakamoto-Guardian/ANTI_FRAGILITY_LOOP.md` | Canonical | Public-safe stub (canonical in Linear) | ATS enforcement + collision audits framing (standardized ZSE stub). |
| `cxn-grid-oracle/README.md` | Supporting | Public-safe | Grid oracle overview (agnostic). |

### GitHub-first BOS research-cycle ownership

[`GITHUB_FIRST_BOS_OPERATING_MODEL.md`](./GITHUB_FIRST_BOS_OPERATING_MODEL.md)
is canonical for the public-safe lifecycle and reusable score rubric. It links
to owning records rather than reproducing their implementation or restricted
content. [`BOS_RESEARCH_CANDIDATE_LEDGER.md`](./BOS_RESEARCH_CANDIDATE_LEDGER.md)
and [`bos_research_candidate_ledger.json`](./bos_research_candidate_ledger.json)
hold the dated bounded inventory, per-dimension provenance, score history, gap
classes, two-layer selection, uncertainty, and non-claims:

| Ownership area | Canonical records | Index boundary |
|---|---|---|
| Lifecycle/rubric authority and dated candidate evidence | [Business #943](https://github.com/Conxian/conxian-business/issues/943), [`GITHUB_FIRST_BOS_OPERATING_MODEL.md`](./GITHUB_FIRST_BOS_OPERATING_MODEL.md), [`BOS_RESEARCH_CANDIDATE_LEDGER.md`](./BOS_RESEARCH_CANDIDATE_LEDGER.md) | The operating model governs the cycle/rubric; the ledger records the bounded scan. Existing owner trackers remain canonical for implementation and acceptance. |
| Authority, migration, and branch governance | [Business #943](https://github.com/Conxian/conxian-business/issues/943), [#944](https://github.com/Conxian/conxian-business/issues/944), [#945](https://github.com/Conxian/conxian-business/issues/945), [Conxian/.github #61](https://github.com/Conxian/.github/issues/61) | Public-safe coordination only; Project authorization/name/schema and restricted-record successor remain human-owned. |
| Semantic-source cycle | [Business #940](https://github.com/Conxian/conxian-business/issues/940), [merged PR #956](https://github.com/Conxian/conxian-business/pull/956) | Existing bounded implementation; preserve its historical check state and non-adoption/non-acceptance boundary. |
| Attestation and independent acceptance | [Repository #240](https://github.com/Conxian/conxius-enclave-sdk/issues/240), [#241](https://github.com/Conxian/conxius-enclave-sdk/issues/241), [#242](https://github.com/Conxian/conxius-enclave-sdk/issues/242), [#202](https://github.com/Conxian/conxius-enclave-sdk/issues/202) | Implementation and acceptance stay in the owning repository; this index does not duplicate its threat model or phase plan. |
| Wallet consumer boundary | [Wallet #444](https://github.com/Conxian/conxius-wallet/issues/444) | Consumer enforcement remains wallet-owned and does not imply upstream acceptance. |
| Selected next technical candidate and CON-1573 architecture decision | [CON-1573](https://linear.app/conxian-labs/issue/CON-1573/security-provide-a-v02-compatible-core-candidate-without-legacy), [Core #227](https://github.com/Conxian/lib-conxian-core/issues/227), [merged PR #229](https://github.com/Conxian/lib-conxian-core/pull/229), [review-ready PR #231](https://github.com/Conxian/lib-conxian-core/pull/231) | Selected at 88/100 without displacing #943 authority. Immediate maintenance uses BDK std-only with no Core networking/persistence drivers; transport-specific backends remain opt-in outside Core. Final release and exact downstream repin/acceptance remain owner gates. |
| Independent Nexus remediation | [Nexus #178](https://github.com/Conxian/conxian-nexus/issues/178) | Separate narrow CI item, not part of the selected #943 implementation. |

Existing historical classifications elsewhere in this index remain unchanged.

## 3) OpenSpec (ground truth specs)

OpenSpec is the best place to point issue descriptions when work is “spec-first.”

### Canonical OpenSpec specs

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `openspec/specs/git-management/spec.md` | Canonical | Public-safe | Git hygiene, branching, and repo discipline expectations. |
| `openspec/specs/mainnet-acceptance-evidence-pack/spec.md` | Canonical | Public-safe | Canonical evidence pack required for promoting `staged` into `main`. |
| `openspec/specs/workspace-audit/spec.md` | Canonical | Public-safe | Workspace audit / cleanliness requirements. |
| `openspec/specs/sab-datastore-mapping/spec.md` | Canonical | Public-safe | SAB datastore mapping requirements (persistence + mapping rules). |

### OpenSpec change sets (proposal/design/spec/tasks bundles)

| Change set | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `openspec/changes/remediate-enterprise-sovereignty/*` | Canonical | Public-safe | Baseline enterprise sovereignty requirements. |
| `openspec/changes/sovereign-data-migration-sovereign-egress/*` | Canonical | Public-safe | Clean-break data migration + sovereign egress requirements. |
| `openspec/changes/csf-autonomous-launch/*` | Supporting | Public-safe | Launch mechanics and autonomous launch framing. |

### Audit docs that complement OpenSpec

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `audit/strategos-alignment.md` | Supporting | Internal-only | Audit of repo alignment to Strategos mandate + next steps. |
| `audit/nomenclature-alignment.md` | Supporting | Public-safe | Corporate vs product nomenclature separation rules. |

## 4) Architecture, PRDs, whitepapers, roadmaps

### Independent Lab Development Kit (ILDK)

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `docs/ILDK_README.md` | Canonical | Public-safe | Technical framework for external labs to build specialized Industrial Management modules. |
| `docs/STRATEGIC_GROWTH_MODEL_2026.md` | Canonical | Public-safe | Strategic comparison of growth models and governance-minimized scaling. |
| `docs/CONXIAN_UNIFIED_THEORY_v2.md` | Canonical | Public-safe | Foundational mathematical framework for capital, time, and code deployment (v2.0). |

These are the documents most likely to answer “what are we building?” and “how is it structured?”

### Platform / protocol

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `Conxian/PRD.md` | Archive candidate (deprecated) | Public-safe | Legacy protocol PRD (Conxian/Conxian is deprecated in favor of lib-conxian-core, conxian-gateway, conxian-nexus, conxian-business). |
| `conxian-market` | Supporting | Public-safe | AI Marketplace & Agentic Commerce surface mapped and integrated in conxian-business. |
| `Conxian/docs/ARCHITECTURE.md` | Canonical | Public-safe | Protocol architecture description. |
| `Conxian/docs/WHITEPAPER.md` | Archive candidate (rewrite required) | Public-safe | Historical protocol whitepaper surface; not a current doctrine source. Rewrite against `docs/TECHNICAL_WHITEPAPER_OUTLINE.md` and the portfolio doctrine before reclassification. External follow-up; no submodule content was changed here. |
| `Conxian/docs/ROADMAP.md` | Canonical | Public-safe | Protocol roadmap and phases. |
| `Conxian/GOVERNANCE_RECOVERY_REPORT.md` | Supporting | Public-safe | Governance + recovery status report (March 2026). |
| `Conxian/docs/DOCUMENTATION_STATE.md` | Supporting | Public-safe | Snapshot of protocol doc state. |

### Gateway / Nexus / SDK

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `conxian-gateway/PRD.md` | Canonical | Public-safe | `conxian-gateway` PRD (sovereign compliance pipe). |
| `conxian-nexus/docs/PRD.md` | Canonical | Public-safe | Nexus PRD (Glass Node). |
| `lib-conxian-core/docs/PRD.md` | Canonical | Public-safe | Core library PRD (shared models + gateway alignment). |
| `docs/CON-1512_HARDWARE_SIGNING_ATTESTATION_PHASE_PLAN.md` | Canonical | Public-safe | Current CON-1512 research, weighted gap map, split-provider decision, dependency graph, and phase/acceptance boundaries for hardware-backed signing and attestation. |
| `docs/CONXIUS_ENCLAVE_SDK_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and internal-only vs public-safe separation guidance for the SDK. |
| `docs/CONXIUS_PLATFORM_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for conxius-platform. |
| `docs/CONXIAN_PROTOCOL_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for Conxian protocol. |
| `docs/CONXIAN_GATEWAY_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for `conxian-gateway`. |
| `docs/CONXIAN_NEXUS_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for conxian-nexus. |
| `docs/CONXIUS_ORBIT_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for `conxius-orbit`. |
| `docs/CONXIAN_UI_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for `conxian_ui` (upstream slug retained). |
| `docs/GITHUB_GOVERNANCE_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for .github. |
| `docs/LIB_CONXIAN_CORE_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for lib-conxian-core. |
| `docs/CONXIAN_LABS_SITE_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and documentation separation guidance for conxian-labs-site. |
| `docs/MAINNET_READINESS_CONXIAN_PROTOCOL.md` | Supporting | Public-safe | Mainnet readiness checklist for Conxian protocol. |
| `docs/MAINNET_READINESS_CONXIUS_WALLET.md` | Supporting | Public-safe | Mainnet readiness checklist for conxius-wallet. |
| `docs/MAINNET_READINESS_CONXIAN_GATEWAY.md` | Supporting | Public-safe | Mainnet readiness checklist for `conxian-gateway`. |
| `docs/MAINNET_READINESS_CONXIUS_PLATFORM.md` | Supporting | Public-safe | Mainnet readiness checklist for conxius-platform. |
| `docs/WALLET_SIGNER_CONTROL_VERIFICATION_REPORT.md` | Supporting | Public-safe | Wallet and signer control verification report for mainnet launch. |
| `docs/PUBLIC_VISIBILITY_AUDIT_REPORT.md` | Supporting | Public-safe | Public visibility boundary audit report. |
| `docs/architecture/BITCOIN_LAYER_ARCHITECTURE_BOUNDARY_NOTE.md` | Canonical | Public-safe | Canonical Bitcoin layer boundary note (capability verbs, phase scope, and repo ownership rules). |
| `docs/architecture/PROTOCOL_ADAPTER_MATURITY_LANES.md` | Canonical | Public-safe | Protocol-adapter maturity lane taxonomy and default handling (`Research` when unspecified), plus intake schema, promotion criteria, and cross-repo handoffs. |
| `docs/protocols/SESSION_BROKER_NORMATIVE_SPEC.md` | Canonical | Public-safe | Normative session-broker boundary spec (actors, handshake, TTL semantics, PoP/mTLS binding, replay/idempotency, revocation/attestation checks, fail-closed behavior, errors, and audit requirements). |
| `conxius-platform/services/lib-conxian-core/docs/PRD.md` | Supporting | Public-safe | Service-local copy; treat `lib-conxian-core/docs/PRD.md` as canonical. |
| `conxius-wallet/lib-conxian-core/docs/PRD.md` | Supporting | Public-safe | Wallet-local copy; treat `lib-conxian-core/docs/PRD.md` as canonical. |

### Conxius wallet (B2C)

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `docs/CONXIUS_WALLET_BOS_BUILDOUT.md` | Supporting | Public-safe | BOS-level business role, governance controls, and internal-only vs public-safe separation guidance for the wallet. |
| `conxius-wallet/docs/business/PRD.md` | Canonical | Public-safe | Wallet PRD. |
| `conxius-wallet/docs/operations/ROADMAP.md` | Canonical | Public-safe | Wallet strategic roadmap (v1.6.0). |
| `conxius-wallet/docs/protocols/IMPLEMENTATION_REGISTRY.md` | Canonical | Public-safe | Protocol implementation registry (what’s integrated). |
| `conxius-wallet/docs/legal/RISK_REGISTRY.md` | Canonical | Public-safe | Risk registry (wallet). |
| `conxius-wallet/docs/archive/*` | Supporting | Internal-only | Historical context; useful for archaeology but shouldn’t drive new decisions. |

## 5) Industrial engine (CJCS / ATS / ERP)

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `docs/CJCS_v2.0_SPEC.md` | Canonical | Public-safe | Job Card schema (CJCS v2.0.1). |
| `docs/ERP_MCP_HANDSHAKE_SPEC.md` | Canonical | Public-safe | ERP handshake spec (SAP/Oracle mapping). |
| `docs/AGENTS.md` | Canonical | Public-safe | Agent operating rules (including knowledge retention rules). |
| `docs/ATS_v11.0_MASTER_BASELINE.md` | Supporting | Internal-only | Baseline snapshot and executive alignment language. |
| `docs/TEE_SECURITY_AUDIT.md` | Supporting | Public-safe | TEE security audit notes. |
| `docs/DASHBOARD_SPEC.md` | Supporting | Public-safe | Audit dashboard spec. |
| `docs/SOVEREIGN_SHARD_SPEC.md` | Canonical | Public-safe | Sharding spec (Sovereign Shard). |
| `docs/BUSINESS_COMPLIANCE_ALIGNMENT_2026.md` | Supporting | Internal-only | Strategy/compliance narrative for 2026 regulatory framing. |

## 6) Governance / repo operating model / runbooks

See `docs/BOS_BUSINESS_BUILDOUT.md` for repo business purpose, business-unit placement, governance + ownership model, and public/internal split.

| Document | Role | Visibility | What it’s for |
| --- | --- | --- | --- |
| `CONTRIBUTING.md` | Canonical | Public-safe | Contribution expectations and workflow. |
| `SECURITY.md` | Canonical | Public-safe | Security policy and reporting. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Supporting | Public-safe | PR checklist and norms. |
| `docs/governance/EXTERNAL_SEMANTIC_SOURCE_INTAKE_POLICY.md` | Canonical | Public-safe | Fail-closed lifecycle, immutable-evidence, notice/import, namespace, transformation, SBOM-handoff, offline, review, and unsupported-claim policy for external semantic sources. |
| `governance/external-semantic-sources.schema.v1.json` | Canonical | Public-safe | Versioned machine-readable registry contract; unknown fields and values are closed by policy and validator. |
| `governance/external-semantic-sources.json` | Canonical | Public-safe | Generic external semantic-source registry, intentionally initialized with `sources: []`; presence is not adoption or gate evidence. |
| `docs/governance/FIBO_PROVENANCE_RESEARCH_NOTE.md` | Supporting | Public-safe | Commit-addressed primary-source and observed archive-byte provenance research; records no FIBO/OMG corpus or adoption decision. |
| `docs/CSF_FIRST_OPERATING_SEQUENCE_AND_PROOF_GATES.md` | Canonical | Public-safe | Locks the CSF → economy → gateway operating order and the minimum proof gates that keep launch, economy design, and go-to-market claims aligned. |
| `docs/BOS_WALLET_CONTROL_MODEL.md` | Canonical | Public-safe | Canonical BOS signer and protocol/user control model; custody language must be read as an explicit boundary record, not as a claim that Conxian-Labs holds user assets. |
| `docs/CONXIAN_BUSINESS_PARENT_CONTROL_ALIGNMENT.md` | Canonical | Public-safe | CON-694 alignment baseline for `conxian-business`: scope boundaries, six-domain control mapping, evidence expectations, and rollback/accountability guardrails. |
| `docs/SAB_MIGRATION_WAVES.md` | Canonical | Public-safe | Canonical SAB migration sequencing (`W0`…`W6`) including reconciliation notes from the legacy 4-wave framing. |
| `docs/operations/SAB_MIGRATION_WAVES.md` | Supporting | Public-safe | Deprecated non-canonical pointer kept for link continuity; directs readers to `docs/SAB_MIGRATION_WAVES.md`. |
| `docs/operations/CON-681_PHASE6_PRODUCTION_ROLLOUT_RUNBOOK.md` | Canonical | Public-safe | Canonical CON-681 Phase 6 rollout runbook with staged gates, observability thresholds, rollback triggers/actions, and operator communication templates. |
| `docs/operations/CON-681_PHASE6_ROLLBACK_DRILL_SIMULATION.md` | Supporting | Public-safe | CON-681 rollback drill simulation artifact (scenario, timeline, observed metrics, RTO/RPO outcome, and corrective actions). |
| `docs/operations/CON-762_PARTNER_SCORECARD_AND_SHORTLIST.md` | Canonical | ZSE stub (canonical in Linear) | CON-762 partner scorecard model and artifact index — migrated to Linear under ZSE (Conxian/conxius-platform#1078). CSV artifacts under `docs/operations/con-762-partner-scorecard/*` are also ZSE stubs. |
| `docs/operations/CON-780_LIGHTNING_COVERAGE_TRACKER.md` | Canonical | Public-safe | Active GAP-009 Lightning coverage tracker (ownership split + matrix + milestones) aligned to `docs/architecture/BITCOIN_LAYER_ARCHITECTURE_BOUNDARY_NOTE.md` and `docs/COMPATIBILITY_MATRIX_AND_ACCEPTANCE_GATE_CHECKLIST.md`. |
| `docs/bounties/MAINTAINER_PAYOUT_ENABLEMENT_RUNBOOK.md` | Canonical | Public-safe stub (canonical in Linear) | How maintainer payouts are enabled and validated (standardized ZSE stub). |
| `admin/SECRETS.md` | Canonical | Public-safe stub (canonical in Linear) | Secret registry + pointers to Linear docs (standardized ZSE stub). |
| `dependabot-fixes.md` | Supporting | Public-safe | Dependabot security alert remediation guide and workspace override audit tracking. |
| `docs/SECURITY_PATTERNS.md` | Supporting | Public-safe | Security patterns, Clarity audit checklist, and workspace dependency security overrides. |

## 7) Known doc gaps / broken references (should not be re-created blindly)

These are referenced by current docs but are not present in the active Git index. Before recreating them from scratch, first check whether they were intentionally migrated to the authorized Linear workspace under ZSE.

- `docs/STRATEGOS_MANDATE.md` (referenced by `audit/strategos-alignment.md`, `Fiscal-Vault-Oracle/SOVEREIGN_RUNWAY.md`).
- `system_ip_audit.md` (referenced by `Sovereign-Strategy-Nexus/REALTIME_M&A_VELOCITY.md`).
- `RENDER_BOS_PAYLOAD.md` (referenced by `audit/nomenclature-alignment.md`).
- `Sovereign-Strategy-Nexus/SARB_MANDATE.md` (referenced by `audit/strategos-alignment.md`).

## 8) Issue-linking recommendations (current CON issues)

If an issue is in a planning or execution state, the description should link to the doc(s) below so the “why/spec” stays stable even as implementation details change.

| Issue | Add links to | Why |
| --- | --- | --- |
| https://linear.app/conxian-labs/issue/CON-343 | `openspec/changes/sovereign-data-migration-sovereign-egress/specs.md`, `openspec/changes/sovereign-data-migration-sovereign-egress/specs/sovereign-data-migration-sovereign-egress/spec.md`, `ARCHIVE_MIGRATION.md` | This issue is spec-first and directly tied to ZSE + migration. |
| https://linear.app/conxian-labs/issue/CON-158 | `docs/DOCUMENTATION_ALIGNMENT_INDEX.md`, `SUMMARY.md`, `openspec/changes/remediate-enterprise-sovereignty/specs.md` | This is the “alignment” umbrella; it should anchor to the index + baseline OpenSpec. |
| https://linear.app/conxian-labs/issue/CON-152 | `conxian-business/SERVICE_LOOP.md`, `Sovereign-Ops-Orchestrator/LINEAR_WIRING.md`, `conxian-business/BOS_STATE_MACHINE.stub.json` | BOS operating model work should reference the service loop + wiring + state machine. |
| https://linear.app/conxian-labs/issue/CON-157 | `Conxian/PRD.md`, `conxian-gateway/PRD.md`, `conxian-nexus/docs/PRD.md` | “Business-unit model” extraction should start from PRDs (what exists and how it’s separated). |
| https://linear.app/conxian-labs/issue/CON-160 | `conxian-gateway/PRD.md`, `lib-conxian-core/docs/PRD.md`, `openspec/changes/remediate-enterprise-sovereignty/specs/enterprise-sovereignty/spec.md` | Settlement ingress touches gateway/core-lib conventions + sovereignty requirements. |
| https://linear.app/conxian-labs/issue/CON-780 | `docs/operations/CON-780_LIGHTNING_COVERAGE_TRACKER.md`, `docs/architecture/BITCOIN_LAYER_ARCHITECTURE_BOUNDARY_NOTE.md`, `docs/COMPATIBILITY_MATRIX_AND_ACCEPTANCE_GATE_CHECKLIST.md` | GAP-009 Lightning coverage execution should anchor to the active tracker, service/adapter ownership boundary, and shared acceptance-gate criteria. |
| https://linear.app/conxian-labs/issue/CON-131 | `docs/bounties/MAINTAINER_PAYOUT_ENABLEMENT_RUNBOOK.md`, `CONTRIBUTING.md` | Bounty workflow should reference the payout runbook + repo workflow norms. |
| https://linear.app/conxian-labs/issue/CON-325 | `admin/SECRETS.md`, `ARCHIVE_MIGRATION.md`, `docs/AGENTS.md` (ZSE section) | Secrets removal work should anchor to the ZSE “where is it now?” docs. |
| https://linear.app/conxian-labs/issue/CON-326 | `openspec/specs/git-management/spec.md`, `CONTRIBUTING.md` | Repo discipline/categorization should cite the OpenSpec git rules + contributing norms. |
| https://linear.app/conxian-labs/issue/CON-327 | `openspec/specs/git-management/spec.md`, `SECURITY.md`, `.github/*` templates | Governance standardization needs the existing governance/security baselines. |

## 9) Proposed Linear documents to create (durable workspace access)

These are the highest-value sources to copy into Linear so day-to-day work stays stable even if the repo has to remove or relocate sensitive material.

1. **BOS Operating Model (canonical)**
   - Source: `conxian-business/SERVICE_LOOP.md`, `conxian-business/BOS_STATE_MACHINE.stub.json` (public-safe pointer; canonical BOS state machine definition is maintained in Linear).
2. **Execution wiring: Linear ↔ BOS state layer (canonical)**
   - Source: `Sovereign-Ops-Orchestrator/LINEAR_WIRING.md`.
3. **Zero Secret Egress (ZSE) + knowledge retention (canonical)**
   - Source: `ARCHIVE_MIGRATION.md`, `docs/AGENTS.md` (Knowledge retention & hygiene section), `admin/SECRETS.md`.
4. **OpenSpec: Enterprise Sovereignty baseline (canonical)**
   - Source: `openspec/changes/remediate-enterprise-sovereignty/specs/enterprise-sovereignty/spec.md`.
5. **OpenSpec: Sovereign Data Migration & Sovereign Egress (canonical)**
   - Source: `openspec/changes/sovereign-data-migration-sovereign-egress/specs/sovereign-data-migration-sovereign-egress/spec.md`.
6. **SAB datastore mapping rules (canonical)**
   - Source: `openspec/specs/sab-datastore-mapping/spec.md`.
7. **Conxian protocol PRD + roadmap (canonical)**
   - Source: `Conxian/PRD.md`, `Conxian/docs/ROADMAP.md`.
8. **Gateway / Nexus / Core-lib PRDs (canonical)**
   - Source: `conxian-gateway/PRD.md`, `conxian-nexus/docs/PRD.md`, `lib-conxian-core/docs/PRD.md`.
9. **CJCS v2.0.1 + ERP handshake (canonical)**
   - Source: `docs/CJCS_v2.0_SPEC.md`, `docs/ERP_MCP_HANDSHAKE_SPEC.md`.
10. **Maintainer payout enablement runbook (internal-only, but operationally critical)**
   - Source: `docs/bounties/MAINTAINER_PAYOUT_ENABLEMENT_RUNBOOK.md`.

## 10) Boundary & Commercial Doctrine (2026-07-03 Sprint)

These documents were created during the 2026-07-03 cross-issue boundary and doctrine sprint. They form a coherent set that defines repository boundaries, trust verification, operating lane assignments, commercial packaging, and technical communication strategy.

| Document | Role | Visibility | What it's for |
| --- | --- | --- | --- |
| `docs/DEVELOPER_QUICKSTART.md` | Canonical | Public-safe | Ecosystem architecture, submodule map, build/test commands for all 4 suites, CI/CD pipeline, promotion workflow, and contribution guide. |
| `docs/BOUNDARY_DECISION_LOG.md` | Canonical | Public-safe | Systematic boundary register classifying 20+ artifacts (strategy, BOS state, architecture, bounties, CI/CD) as public-safe, public-safe stub, or internal-only. |
| `docs/TRUST_AND_READINESS_VERIFICATION.md` | Canonical | Public-safe | Evaluator-facing trust audit against implementation truth. Separates `Implemented`, `Verified`, `Target-state`, and `Deprecated` claim states from maturity and defines an explicit non-claim boundary. |
| `docs/TRUST_AND_PROOF_MESSAGING.md` | Canonical | Public-safe | Standard framework for trust signals on public surfaces (security posture, governance, repo maturity, release discipline, audience fit, portfolio boundaries). |
| `docs/DOCTRINE_ALIGNMENT_STANDARD.md` | Canonical | Public-safe | Short doctrine source for company role, brand boundaries, custody/data boundaries, infrastructure posture, Bitcoin anchor, claim states, operating labels, classifications, and contradiction resolution. |
| `docs/PORTFOLIO_DOCTRINE_REGISTER.md` | Canonical | Public-safe | Central register for the 16-repository portfolio: role, audience, operating label, maturity/claim state, document classification, evidence, and unresolved contradiction disposition. |
| `docs/OPERATING_LANE_BOUNDARIES.md` | Canonical | Public-safe | Explicit lane boundaries for Packaging (doctrine), GTM (execution), and Operations (coordination). Includes escalation paths, anti-patterns, and cross-lane operating loop. |
| `docs/operations/WEEKLY_GROWTH_DRIVER_REVIEW.md` | Canonical | Public-safe | Weekly GTM metrics review template covering qualified conversations, demos, pilots, proofs, and responsiveness. Cross-references BOS operational metrics (CON-682). |
| `docs/TECHNICAL_WHITEPAPER_OUTLINE.md` | Canonical | Public-safe | 10-section flagship whitepaper outline with evidence references: system architecture, BOS state machine, security model, protocol layer, execution layer, compliance layer, client layer. |
| `docs/COMMERCIAL_PACKAGING_DOCTRINE.md` | Canonical | Public-safe | Offer structure (Gateway/Wallet/SDK), 3-tier packaging matrix, pricing doctrine, customer journey stages, pilot path, and executive one-pager template (pricing details in Linear per ZSE). |

### Cross-references

- `BOUNDARY_DECISION_LOG.md` ← `TRUST_AND_READINESS_VERIFICATION.md` ← `TRUST_AND_PROOF_MESSAGING.md`
- `OPERATING_LANE_BOUNDARIES.md` ← `WEEKLY_GROWTH_DRIVER_REVIEW.md` ← `COMMERCIAL_PACKAGING_DOCTRINE.md`
- `TECHNICAL_WHITEPAPER_OUTLINE.md` ← `DEVELOPER_QUICKSTART.md` ← `CONXIAN_UNIFIED_THEORY_v2.md`
- `PORTFOLIO_DOCTRINE_REGISTER.md` → `REPO_PORTFOLIO.md` → `PORTFOLIO_BUSINESS_UNIT_MAP.md`
- All documents cross-reference the central doctrine/register where portfolio role, maturity, claim state, or classification is relevant.
