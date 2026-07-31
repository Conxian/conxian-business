# Conxian Ecosystem Dashboard — Session 46
## Generated: 2026-07-31 03:43 UTC

---

## 1. Repository Map (16 repos)

| Repo | Type | Issues | PRs | Dependabot |
|------|------|--------|-----|------------|
| `Conxian/Conxian` | Clarity/TS (npm) | 10 | 1 (#611) | 4 (1 fixed) |
| `Conxian/conxian-business` | Monorepo (submodules) | 13 | 1 (#978) | 61 (1 fixed) |
| `Conxian/conxius-wallet` | TS (pnpm) | 3 | 0 | 3 |
| `Conxian/conxius-orbit` | TS (pnpm) | 2 | 0 | 0 |
| `Conxian/conxian-gateway` | Rust/TS (cargo+pnpm) | 5 | 0 | 9 |
| `Conxian/lib-conxian-core` | Rust | 2 | 0 | 0 |
| `Conxian/conxian-nexus` | Rust (cargo) | 2 | 2 | 3 |
| `Conxian/conxius-platform` | TS (pnpm) | 5 | 0 | 7 |
| `Conxian/conxian_ui` | Next.js (pnpm) | 1 | 0 | 13 |
| `Conxian/conxian_market` | — | 2 | 0 | 0 |
| `Conxian/conxian-labs-site` | — | 2 | 0 | — |
| `Conxian/conxius-enclave-sdk` | — | 2 | 0 | — |
| `Conxian/conxian.github.io` | — | 1 | 0 | — |
| `Conxian/.github` | — | — | — | — |
| `Conxian/.github-private` | — | — | — | — |
| `Conxian/demo-repository` | — | 0 | 0 | — |
| **TOTAL** | | **48** | **4** | **~100** |

---

## 2. Priority Breakdown — Open Issues

### P0 (Critical)
| Issue | Repo | Title | Code Location | Status |
|-------|------|-------|---------------|--------|
| #480 | Conxian | Developer Sandbox: TTFV < 15 minutes | `cxn-sandbox/` uses old `@conxian/sdk` + `ConxianGateway`. Live SDK is `@conxian/client-sdk` at `packages/client-sdk/`. Sandbox inside gateway at `conxian-gateway/examples/developer-sandbox/` uses correct SDK. | Sandbox uses stale mock SDK. Gateway sandbox is current. |
| #943 | conxian-business | Establish GitHub-first operating model | Meta: BOS governance restructure | IN PROGRESS — Linear retired, GitHub now canonical tracker |

### P1 (High)
| Issue | Repo | Title | Code Location |
|-------|------|-------|---------------|
| #532 | Conxian | Partnership security, legal, and commercialization launch gate | Meta: needs legal/compliance sign-off |
| #530 | Conxian | Partnership gateway, Stacks.js SDK, event indexing | `contracts/partners/` (if exists) or new contract work |
| #529 | Conxian | Partner usage ledger and atomic split settlement | `contracts/treasury/revenue-distributor.clar`, `contracts/agents/fiscal-orchestrator.clar` |
| #527 | Conxian | Partnership fee policy, legal model, asset scope | Meta: business decision precedes code |
| #515 | Conxian | Enforce Main Branch Merge Gates, Reconcile CODEOWNERS | `.github/CODEOWNERS`, branch protection rules, `scripts/branch_promotion_policy.py` |
| #496 | Conxian | Partnership Fee Contracts | Fee collection: `contracts/treasury/` path; related to #488, #529 |
| #488 | Conxian | 2% Protocol Fee Collection | `contracts/treasury/revenue-distributor.clar`, `contracts/treasury/allocation-policy.clar` |
| #944 | conxian-business | Retire Linear-first references, publish migration map | Meta: BOS governance | IN PROGRESS — Linear references being retired, migration to GitHub underway |

### P2
| Issue | Repo | Title |
|-------|------|-------|
| #507 | Conxian | sBTC Vault Implementation |
| #500 | Conxian | Production oracle config + DEX wiring |

### BOS Governance Gates (#890 → #932–#938)

**Canonical tracker:** GitHub issue hierarchy (#932–#938) is now the authoritative tracking layer. Linear has been retired as system-of-record.

**Gate 0 blockers:** Accountable role assignment, accepted immutable baseline.
**Gate 1 blockers:** Divergent SHAs between main/dev/staged; two required business validators absent; CI migration to CircleCI in progress (GitHub Actions billing limit workaround); no candidate-wide green CI.
**Gates 4-5 blockers:** Hardware-backed signing/attestation depends on enclave-sdk issues #195, #200, #202.
**Gate 6:** Not authorized until all prior gates clear.

| Gate | Status | Title | Actual Blocker |
|------|--------|-------|----------------|
| #932 Gate 0 | BLOCKED | Re-baseline and accountable ownership | Accountable roles unassigned + immutable baseline not accepted |
| #933 Gate 1 | NOT MET | Reproducible candidate, pins, validators, green CI | SHA divergence + CI migration to CircleCI in progress + 2 validators absent |
| #934 Gate 2 | NOT MET | Safe authority-transfer semantics | Depends on Gate 0+1 |
| #935 Gate 3 | NOT MET | Testnet rehearsal, readback, failure drills | Depends on Gate 0-2 |
| #936 Gate 4 | BLOCKED | Hardware-backed signing/attestation | Depends on enclave-sdk #195, #200, #202 |
| #937 Gate 5 | BLOCKED | Independent security/release acceptance | Depends on Gate 4 |
| #938 Gate 6 | NOT AUTHORIZED | Mainnet handoff and post-state readback | All prior gates |

---

## 3. Session 46 PRs

| PR | Repo | Title | Addresses |
|----|------|-------|-----------|
| [#611](https://github.com/Conxian/Conxian/pull/611) | Conxian | Clarity fixes + service stubs | Chain-check compliance, test coverage |
| [#978](https://github.com/Conxian/conxian-business/pull/978) | conxian-business | Session 46 submodule pin + Dependabot guide | Submodule tracking, security documentation |

---

## 4. Dependabot Security Alerts — Status

| Status | Count | Detail |
|--------|-------|--------|
| ✅ Fixed | 1 | postcss GHSA-r28c-9q8g-f849 (Conxian/Conxian) |
| ⚠️ Unfixable | 1 | elliptic GHSA-848j — no patch (Conxian/Conxian) |
| 📋 Documented | ~60 | pnpm repos need local `pnpm update` (see `dependabot-fixes.md`) |

### Critical alert
- **node-tar** GHSA-23hp-3jrh-7fpw (critical): Fixed by updating tar transitive dep in pnpm workspace

### Top fix command (run locally)
```bash
cd conxian-business
for dir in conxian-ui conxius-platform conxian-gateway conxius-wallet; do
  (cd $dir && pnpm update)
done
cd conxian-gateway && cargo update webpki-roots
cd ../conxian-nexus && cargo update webpki-roots
```

---

## 7. Next Steps / Gaps

| Gap | Priority | Action |
|-----|----------|--------|
| Pnpm repos Dependabot | HIGH | Run `pnpm update` locally in conxian-ui, conxius-platform, conxian-gateway, conxius-wallet |
| Cargo Dependabot | HIGH | `cargo update` in conxian-gateway, conxian-nexus |
| CircleCI migration | P0 | Configure real CircleCI jobs for heavy CI (Clarity chain-check, cargo test); remove hello-world boilerplate |
| BOS Gate 0 (#932) | P0 | Assign accountable roles; accept immutable baseline (SHA pins from session 46 qualify) |
| BOS Gate 1 (#933) | P0 | Session 46: 18/18 tests green, submodule pins established in Conxian; needs candidate-wide CI on CircleCI |
| Sandbox #480 | P0 | Replace `@conxian/sdk` with `@conxian/client-sdk` or point to gateway sandbox |
| Conxian PR #611 merge | P1 | Needs review → merge → update submodule pin |
| conxian-business PR #978 merge | P1 | Needs review → merge |
| Linear retirement (#944) | P1 | Remove remaining Linear references from docs, workflows, AGENTS.md |
| GitHub operating model (#943) | P1 | Document GitHub-first workflow in GOVERNANCE.md |
| elliptic replacement | P3 | Replace elliptic with noble-curves (@noble/secp256k1) |


---

## 6. CI/CD Architecture

### Strategy: GitHub Actions + CircleCI split

| Workload | Platform | Reason |
|----------|----------|--------|
| Lightweight checks (lint, secret scan, dep review, docs validate) | GitHub Actions | Free for public repos, fast feedback on PRs |
| Heavy CI (Clarity chain-check, Rust cargo test/build, integration tests) | CircleCI | Lower cost for compute-heavy jobs, avoids Actions billing limits |
| Android build (wallet APK) | CircleCI | Requires Android SDK, heavy resource usage |
| Deployment (GCP Cloud Run, Firebase, Vercel) | CircleCI | Consolidated deploy pipeline with release markers |
| Gemini AI agent workflows | GitHub Actions | Lightweight API calls, needs GitHub context |
| Branch promotion policy | GitHub Actions | `pull_request_target` requires Actions |
| Secret scanning (gitleaks) | GitHub Actions | Pre-commit hook integration |

### CircleCI Configs (session 46)

| Config | Jobs | Status |
|--------|------|--------|
| `.circleci/config.yml` | 8 jobs: clarity-check, gateway-test, nexus-test, core-test, enclave-sdk-test, wallet-test, platform-test, ui-test | ✅ Validated |
| `.circleci/deploy.yml` | 3 jobs: gateway-cloud-run (GCP), firebase-deploy, vercel-deploy | ✅ Validated |
| `conxius-wallet/.circleci/config.yml` | 3 jobs: wallet-test, android-build, android-lint | ✅ Validated |

### GCP/Cloud Environment

| Secret | Used By | Status |
|--------|---------|--------|
| `GCP_PROJECT_ID` | CircleCI deploy, Actions gateway-cloud-run | Configured in GitHub Secrets |
| `GCP_SA_KEY` | GCP auth (service account JSON key) | Configured in GitHub Secrets |
| `GOOGLE_API_KEY` | Gemini agent workflows (6 workflows) | Configured in GitHub Secrets |
| `FIREBASE_TOKEN` | Firebase hosting deploy | Configured in GitHub Secrets |
| `VERCEL_TOKEN` + `VERCEL_ORG_ID` | Vercel docs deployment | Configured in GitHub Secrets |

### GCP Services
- **Cloud Run**: `conxian-gateway` (us-central1, 512Mi/1CPU, 0-2 instances, authenticated)
- **Container Registry**: `gcr.io/<project>/conxian-gateway`
- **Firebase**: Showcase DApp hosting (`showcase-dapp/out/` → static HTML)

### GitHub Actions Remaining (lightweight, 88 workflows total)
- `secret-scan.yml` — gitleaks
- `dependency-review.yml` — per-repo dep review
- `gemini-*.yml` (6 workflows) — AI agent dispatch/triage/review
- `branch-promotion-policy.yml` — promotion route enforcement
- `sovereign-guard.yml` — repo-level governance
- `action-version-audit.yml` — pinned action SHA audit

### GitHub Actions Workflows (20+ across monorepo)
- `Conxian/`: protocol-ci, deploy-mainnet, deploy-testnet, gitleaks, sovereign-guard, verify-deployment-evidence, scheduled-protocol-test, session-tracker, docs-validate, conxian-ui-ci, dependency-review
- `conxius-wallet/`: ci, android-release, deploy-proxy, secret-scan, dependency-review
- `conxian-labs-site/`: ci, deploy, dependency-review


---

## 8. Google AI Studio Integration (session 46)

### API Key
- **Project**: `conxian-platform`
- **Key type**: AI Studio API key (Gemini API v1beta)
- **Auth method**: `GOOGLE_API_KEY` → GitHub Secret → Gemini workflows
- **Usage dashboard**: https://aistudio.google.com/usage?project=conxian-platform

### Available Models (47 total)
| Tier | Models | Use Case |
|------|--------|----------|
| **Latest** | `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite` | Code review, triage, dispatch (fast + cheap) |
| **Pro** | `gemini-3.1-pro-preview`, `gemini-3-pro-preview` | Plan-execute, complex reasoning |
| **Thinking** | `gemini-2.5-pro`, `gemini-2.5-flash` | Deep analysis (all support `thinking: true`) |
| **Vision** | `gemini-3-pro-image`, `gemini-3.1-flash-image` | Image analysis, screenshot review |
| **Research** | `deep-research-pro-preview-04-2026` | In-depth codebase research |
| **Embedding** | `gemini-embedding-2` (8K tokens) | Semantic search, RAG |
| **Image Gen** | `imagen-4.0-generate-001`, `veo-3.1-generate-preview` | Asset generation |

### Recommended model per workflow
| Workflow | Model | Reason |
|----------|-------|--------|
| `gemini-triage.yml` | `gemini-3.6-flash` | Fast, cheap, 1M ctx window |
| `gemini-review.yml` | `gemini-3.5-flash` | Good balance speed/quality |
| `gemini-plan-execute.yml` | `gemini-3.1-pro-preview` | Complex planning needs pro |
| `gemini-dispatch.yml` | `gemini-3.6-flash` | Dispatch routing, simple |
| `gemini-scheduled-triage.yml` | `gemini-3.5-flash-lite` | Scheduled, cost-sensitive |
| `gemini-invoke.yml` | `gemini-3.6-flash` | General purpose |

### Configuration
- **GitHub Variable**: `vars.GEMINI_MODEL` = `gemini-3.6-flash` ✅ SET (2026-07-31)
- **GitHub Secret**: `secrets.GOOGLE_API_KEY` = API key
- **Fallback**: `secrets.GEMINI_API_KEY` (deprecated, unused)
- **Auth priority**: `GOOGLE_API_KEY` → `GEMINI_API_KEY` → Vertex AI WIF → GCA

### GCP Services (service account)
- `secrets.GCP_PROJECT_ID` — GCP project for Cloud Run
- `secrets.GCP_SA_KEY` — Service account JSON key for deployment auth
- **Cloud Run**: `conxian-gateway` (us-central1, 512Mi, 0-2 instances)
- **Artifact Registry**: `gcr.io/<project>/conxian-gateway`

### Switch Status (session 46)
| Repo | `GEMINI_MODEL` | API Test |
|------|---------------|----------|
| `conxian-business` | `gemini-3.6-flash` ✅ | 429 credits depleted — key works, billing needs top-up |
| `Conxian/Conxian` | `gemini-3.6-flash` ✅ | Same key |
| `conxius-enclave-sdk` | `gemini-3.6-flash` ✅ | Same key |
| `conxian-nexus` | `gemini-3.6-flash` ✅ | Same key |
| `lib-conxian-core` | `gemini-3.6-flash` ✅ | Same key |
| `conxius-platform` | `gemini-3.6-flash` ✅ | Same key |

**Action required**: Top up prepaid credits at https://ai.studio/projects to unblock Gemini workflows.
