# Mainnet Readiness Gate & System Inventory (April 2026)

**Issue Reference:** CON-133, CON-416, CON-421
**Status:** READINESS AUDIT IN PROGRESS
**Auditor:** Jules (cxn-arch-guardian)

## 1. System Inventory (ZSE-safe)

This repository is public, and the ZSE policy in `GOVERNANCE.md` prohibits publishing actionable infrastructure maps in Git.

**Canonical inventory (provider/project identifiers, service IDs, schema/table names):** maintained in Linear under CON-416 / CON-421.

If any pre-publication drafts of this report contained infrastructure identifiers, remediation/rotation status is tracked under CON-416 / CON-421.

### A. Managed Postgres (Neon)
- **Status:** Active (PG 17).
- **Scope (high level):** institutional egress telemetry, treasury/runway monitoring, managed auth, and verifiable state commitment storage.

### B. Managed Postgres (Supabase)
- **Status:** Active (PG 17).
- **Scope (high level):** deployment/CI health metrics, runway metrics, yield events, IP/ZSE audit logging, and ERP sync event logging.

### C. Hosting / Compute (Render)
- **Status:** Operational.
- **Services:** maintained in Linear inventory (see CON-416 / CON-421).

## 2. Production Readiness Checklist

| Category | Item | Status | Notes |
| --- | --- | --- | --- |
| **Governance** | Branching Policy Enforcement | IN PROGRESS | `main`/`staged`/`dev` model defined. |
| **Security** | Zero Secret Egress (ZSE) | COMPLIANT | No secrets in Git; sensitive strategy migrated. |
| **Protocol** | Clarity 4 Alignment | PENDING | Audit identified `ST1...` principals and stubs. |
| **Gateway** | Institutional Egress | SIMULATED | ISO 20022 pacs.008 is formatted but OData is stubbed. |
| **Nexus** | State Authority | ENHANCED | ZKML and DLC are currently stubs; Nexus API is priority. |
| **Wallet** | Enclave Signing | VERIFIED | ZSE compliance in `services/identity.ts`. |

## 3. Critical Blockers for Mainnet Cutover
1. **Hardcoded Principals:** 76+ contracts still use devnet addresses. Must be remediated to dynamic RBAC (CON-61).
2. **Functional Stubs:** Settlement, ZKML, and DLC logic must move from simulation to production code.
3. **Branch Cleanup:** Non-production "contamination" (stubs/mocks) must be removed from the `main` branch.

---
**Verified by:** Jules (cxn-arch-guardian)
**Date:** April 5, 2026
