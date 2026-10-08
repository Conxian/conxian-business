# Agentic Factory Roadmap

> Goal: make the Conxian org a **self-sensing, self-remediating, self-improving**
> software factory — where the machine does everything a machine *can* do, and
> humans are left only with what is *illegal or impossible* to automate.

## The diagnosis

The org already has most of a factory's scaffolding:

- **Detect** — a dozen `scripts/verify_*.py` checks (external state, cross-repo
  alignment, knowledge retention, domain topology, …).
- **Decide** — policy-as-code (`branch_promotion_policy.py`, BOS doctrine, promotion rules).
- **Act** — `auto-promotion.yml` + `reconcile_branches.py` (branch drift → PR → merge).

But the loop is **not closed**. Proof: the platform sat `build_failed` for 2 days with
no alert, no ticket, no fix — it was found by hand. The `act` layer exists for exactly
one surface (branches) and nothing else. That is the gap this roadmap closes.

## The loop (target architecture)

```
  SENSE ──► DECIDE ──► ACT ──► LEARN
    ▲                           │
    └───────────────────────────┘
```

1. **Sense** — scheduled probes: production URLs, DNS, CI status, published
   versions (crates.io/npm), Neon/Render/AWS surfaces, secrets presence, cost.
2. **Decide** — classify the finding against the trust tiers (below); emit a job card.
3. **Act** — for Tier 0/1, an agent applies the fix and opens a PR (→ auto-merge →
   deploy). For Tier 2, open + escalate a human-gated ticket with an SLA.
4. **Learn** — record the root cause + fix in the memory/KB so the next occurrence is
   detected faster (or pre-empted).

## The five surfaces to build

1. **Sense (observability as code)** — a single scheduled `sense` loop that probes
   everything and auto-opens issues on any red. *Seed: `uptime-check.yml`.*
2. **State-of-truth (one registry)** — one machine-readable registry (repos + versions
   + domains + topology + secrets-map); every verify script reads it and reconciles
   drift, not just reports it. *Seed: `domain-service-map.json` + `DEPLOYMENT_TOPOLOGY.md`.*
3. **Act (drift → PR → merge engine)** — generalize the branch-drift loop to every
   surface: version drift, domain drift, lockfile drift, template drift.
4. **Secrets & config hygiene** — one secret store (SOPS) + *generated* env templates
   (from `config.rs`/source) + a required-secret detector. Unblocks autonomous deploys.
5. **Orchestration** — make the CJCS/SIDL/SLA doctrine real: detectors emit job cards,
   a scheduler dispatches agents, the SLA enforcer tracks deadlines, a budget guardrail
   gates spending.

## Trust tiers (what autonomy is allowed to do)

| Tier | Scope | Action | Guardrail |
|------|-------|--------|-----------|
| **0 — auto** | drift fixes, lockfile bumps, doc/registry updates, DNS verify | fix → PR → auto-merge → deploy | none (reversible, low-risk) |
| **1 — auto + evidence** | anything touching `staged`/`main` | fix → PR → merge | Mainnet Acceptance Evidence Pack (enforced today) |
| **2 — human** | secrets rotation, KMS release signing, AWS root creds, trademarks, hardware attestation, npm-scope claims | open + escalate ticket | SLA + auto-reminder; never auto |

## Phases

### Phase 1 — Close the sense loop (now)
- Consolidate `verify_*.py` into one scheduled `sense` workflow.
- Auto-open a deduplicated issue on any red.
- **Exit**: an outage can never go silent again.

### Phase 2 — One state-of-truth registry
- `ecosystem-registry.json` (repos/versions/domains/topology/secrets-map).
- Verify scripts read from it and *reconcile* drift.

### Phase 3 — Drift → PR → merge engine
- Generic detector→fix→PR→merge pipeline for versions, domains, lockfiles, templates.
- **Exit**: a `node:22`→`node:24` fix like #1370 happens with zero human touch.

### Phase 4 — Secrets & config hygiene
- SOPS single store; generate `.env.example`/`render.yaml`/`docker-compose.yml` from source.
- Required-secret detector fails CI on absence.

### Phase 5 — Orchestration layer
- Job cards + scheduler + SLA enforcer + budget guardrail on top of 1–4.
- **Exit**: the gap register + detectors run as a self-dispatching queue.

## The honest boundary

Some work is *legally or physically* human and cannot be automated: AWS/Cloudflare
credential rotation, the production KMS release-signing key, FIBO/trademark, Nitro
hardware attestation, npm-scope claims. The factory handles these as **Tier 2**: tracked,
reminded, and escalated with SLAs — never silently dropped, never auto-executed.
