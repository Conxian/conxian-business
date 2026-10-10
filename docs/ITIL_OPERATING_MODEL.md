# Conxian Operating Model — ITIL 5 (Version 5) aligned, lean 2-person build

> Version 2.0 · 2026-10-10 · Owner: CTO (OpenHands) + Owner
> Standard: **ITIL 5 Foundation (PeopleCert, released 2026-01-29)** — AI-native &
> data-driven, value co-creation, complex environments, governance, integrated
> product & service lifecycle. Retains the Four Dimensions + Service Value System
> from earlier versions, adapted for fast-changing, AI-native enterprises.
> Adopted **lean**: the value system + principles + a focused practice set, not
> full ITSM ceremony. Canonical KB: `.github-private` (this doc = operational reference).

---

## 0. Intent — why ITIL 5 fits Conxian natively

Conxian is a two-person build (owner + an **ephemeral AI CTO**) shipping a
turnkey, self-serve, fully-online BTC-native payment/identity stack (Rust infra +
Lightning + global-south fiat rails). ITIL 5's center of gravity is *exactly* our
operating reality:

- **AI-native & data-driven** — an AI agent *is* the delivery capability; automation
  and data-driven decisions (SLA enforcer, load oracle, fee model, rate-limit
  sentinel) are the product, not an add-on.
- **Value co-creation** — customers/agents co-create value through self-serve M2M
  keys, `conxian-agent-init`, and x402 subscription pointers.
- **Complex environments** — multi-chain (Stacks/Lightning/Bitcoin) + multi-rail
  (Stitch/Ozow/PAPSS pan-African fiat) + 13-repo dependency graph.
- **Governance** — branch policy, evidence packs, security gates, KB — the
  "prove it" layer that makes a 2-person build auditable.

The operating model answers one question at every step: **can we prove this change
is safe to ship, and prove it after the fact?** Everything below maps ITIL 5 onto
the tooling we already run. "Start where you are" — no new platforms.

---

## 1. Service Value System (SVS)

```
opportunity/demand ──►  GOVERNANCE (principles + practices + AI/data layer)
                         ──►  VALUE CO-CREATION (live, billed, auditable service)
```

- **Demand** = an agent/merchant wants the managed gateway (MoR), a wallet user
  wants turnkey keys, a regulator wants proof of security.
- **Value co-creation** = the customer/agent participates in producing the value
  (self-serve onboarding, M2M keys), not just receiving a delivered service.

---

## 2. Guiding Principles → Conxian rules (retained & adapted for AI-native)

| Principle | How we apply it |
|---|---|
| Focus on value | Every PR ties to a revenue / compliance / gap item (no change without a "why"). |
| Start where you are | Build on existing GitHub Projects, issues, CI, promotion pipeline, KB — don't rip up. |
| Progress iteratively with feedback | `dev→staged→main` + 24h dwell + auto-promotion; every hop re-verifies. |
| Collaborate & promote visibility | Public PR/CI evidence; "prove system & SDK security openly." |
| Think & work holistically | One source of truth per fact (fee↔billing↔rails↔treasury), no duplicated logic. |
| Keep it simple & practical | Lean practice subset (§5), no ITSM theater a 2-person team can't run. |
| Optimize & automate (AI-native) | auto-promotion, reconcile-branches, verify-* scripts, M2M, SLA enforcer — automation is the delivery mechanism, not a cost cut. |

---

## 3. Four Dimensions of Service Management (+ the AI/data layer)

1. **Organizations & People** — owner (final A on org/legal/partner) + AI CTO
   (R+A on build/change/release/security/knowledge). **Bus-factor-1** is the top
   risk → the KB/memory system is the mitigant (§6 Knowledge Management).
2. **Information & Technology** — 13 repos, CI (rust.yml, license-governance,
   hygiene, DKG), Neon, AWS, Stacks/Lightning, the promotion pipeline.
3. **Partners & Suppliers** — GitHub, Neon, AWS, Render, Cloudflare, Ramp Network,
   Stitch / Ozow / PAPSS, crates.io / npm.
4. **Value Streams & Processes** — the Service Value Chain (§4).

**Cross-cutting AI/data layer** (ITIL 5's differentiator): automation, AI, and
data-driven decisions run *through* all four dimensions — the load oracle, fee
model (volume-decay tiers), rate-limit sentinel, and SLA enforcer are all
data-driven controls, and the AI CTO is the automation fabric that executes
change/release/incident/knowledge end-to-end.

---

## 4. Service Value Chain (Integrated Product & Service Lifecycle)

The end-to-end lifecycle: strategy → design → delivery → continual improvement.

| Activity | Conxian mapping | Artifacts / tools |
|---|---|---|
| **Plan** (strategy) | Portfolio & roadmapping, gap register, capacity/fee forecasting | Projects "Portfolio—Ecosystem", "Change Backlog"; gap register G1–G8 |
| **Engage** (co-creation) | Customer/agent onboarding, MoR webhook, support intake, x402 | Issues, `conxian-agent-init`, M2M key store, `/verify-payment` |
| **Design & Transition** | Specs, ADRs, promotion + evidence packs | ADRs, `docs/`, branch_promotion_policy.py, immutable candidates |
| **Obtain / Build** (delivery) | Implementation + CI gates | `dev` PRs, rust.yml, license-governance, hygiene/contamination guards |
| **Deliver & Support** | Deploy, monitoring, incident response, SLA | Render/Cloudflare/Neon, SLA enforcer, rate-limit sentinel, runbooks |
| **Improve** (continual) | Audits, retrospectives, root-cause → durable lessons | gap register lifecycle, full-portfolio audit, MEMORY.md |

---

## 5. Lean Practice Set (14 of the full catalogue — the ones that produce value here)

### A. Change & Release
- **Change Enablement** = the promotion pipeline. Every change is a PR with a
  branch-policy prefix + evidence pack; `dev→staged→main` with immutable
  candidates. Reject bad candidates (close), never hand-edit them.
- **Release Management** = semver tags + publish (crates.io/npm) + the
  staged→main 24h dwell. Pinned SHAs/tags, lockfiles, changelogs.
- **Deployment Management** = deploy workflows (Render/Cloudflare/Neon), with
  rollback path and PR/CI evidence.

### B. Operate & Respond
- **Incident Management** = P0/P1/P2 runbooks; alerting via SLA enforcer
  (block-timestamp deadlines), load oracle, rate-limit sentinel, treasury KPIs.
- **Problem Management** = root-cause analysis → durable rules. Example: the
  `#400` compile break → the rule "nexus `dev` PRs get no Rust build — verify
  locally" → persisted to MEMORY.md.
- **Service Request Management** = turnkey/self-serve (M2M key store, onboarding,
  `conxian-agent-init`), automated fulfillment where possible.
- **Service Desk** = the AI CTO as single responder, fronted by automation.

### C. Plan & Govern
- **Service Level Management** = SLA enforcer + treasury KPI bands (runway /
  volume / revenue / stablecoin thresholds).
- **Risk Management** = gap register + full-portfolio audit + RUSTSEC/advisory
  triage (cargo-deny, cargo audit, Dependabot).
- **Information Security Management** = enclave P0s (#202/#240/#241), org 2FA,
  secret hygiene (ZSE / GitGuardian / no secret egress), cargo-deny license gate.
- **Service Configuration & Asset Management** = `ECOSYSTEM_REGISTRY.json`,
  repo taxonomy, Neon branches/keys, M2M key store.
- **Capacity & Performance** = load oracle, fee model (volume-decay tiers, rail
  floors), rate limits.

### D. Enable
- **Knowledge Management** = `.github-private` canonical KB + per-repo `AGENTS.md`
  + the `.openhands/memory/` system (MEMORY.md index + daily logs). The AI CTO is
  ephemeral → this is the only durable store.
- **Continual Improvement** = audits, retrospectives, gap-register lifecycle
  (identify → prioritize → implement → verify → retire).

---

## 6. Operational Mapping (the "working model" — tool ↔ practice)

| GitHub Projects v2 | Value-chain activity | Primary practices |
|---|---|---|
| Portfolio—Ecosystem | Plan / Engage | SLM, Supplier, Risk |
| Change Backlog | Plan | Risk, Improvement |
| Sprint—Nexus | Obtain/Build | Change, Release |
| Build & Test | Obtain/Build | Change, Deployment |
| Release Management | Deliver | Release, Deployment |
| Service Operations | Deliver & Support | Incident, Problem, Request, Capacity |

**Label taxonomy (ITIL-aligned)**: `change`, `release`, `deploy`, `incident`,
`problem`, `request`, `risk`, `security`, `knowledge`, `improvement`, `supplier`
+ priority `P0`–`P4`.

**Issue type → practice**: bug→Incident/Problem · feature→Change · dep-bump→Release
· advisory→Security/Risk · doc→Knowledge · audit→Improvement · onboarding→Request.

**Control points** (every promotion must pass): branch-policy prefix → evidence
pack → CI (rustfmt/clippy/build/test/coverage) → license-governance → hygiene →
24h staged dwell → deploy.

---

## 7. Operating Cadence

| Rhythm | What |
|---|---|
| **Continuous** | CI + auto-promotion + reconcile-branches + SLA enforcer |
| **Per-change** | PR → evidence pack → promotion (reject if any gate fails) |
| **Daily** | memory log, open PR/issue triage, dependabot/advisory triage |
| **Weekly** | KB refresh, gap-register review, stale-branch/prune sweep |
| **On-demand (P0)** | incident runbook (secure → diagnose → fix → root-cause → durable lesson) |

---

## 8. RACI-lite (two people)

| Domain | Owner | AI CTO (OpenHands) |
|---|---|---|
| Build / Change / Release / Deploy | C | **R+A** |
| Incident / Problem / Request / Capacity | C | **R+A** |
| Security / Knowledge / Improvement | C | **R+A** |
| Partners / Suppliers / Legal / Org-level (2FA, creds, external review) | **A+R** | C |

---

## 9. Definition of Done (a change is "shipped" only when)

1. PR is CI-green on the branch where the build actually runs (Rust: `main`/`staged`).
2. Evidence pack is filled (not placeholder headings).
3. License-governance + hygiene + security checks pass.
4. Promoted `dev→staged→main` with dwell, or deploy-from-`main` for site repos.
5. The durable lesson (if any) is written to memory/KB before the session ends.
