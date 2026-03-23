# Conxian Service Loop: Strategos Mandate

## 1. Discovery & Intent (Gateway)
- External systems connect via **x402**.
- TEE Attestation verified at `POST /api/v1/verify-tee`.

## 2. Validation & Compliance (Guardian)
- Every agent checked against `agent-registry.clar`.
- LEI/DID mapping enforced.

## 3. Execution & Settlement (Executor)
- 1% Sovereign Tax stripped via `revenue-automation.clar`.
- Yield optimization via `yield-optimizer.clar`.

## 4. Monitoring & Transparency (Oracle/Scribe)
- Audit manifest anchored to Bitcoin via `transparency_custodian.py`.
- Telemetry visible in `sovereign-dashboard.clar`.

---
🛡️ **Sovereign Autonomous Business (SAB)**. © 2026 Conxian-Labs.
