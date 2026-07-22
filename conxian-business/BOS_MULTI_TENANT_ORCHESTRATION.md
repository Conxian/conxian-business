# BOS Multi-Tenant Orchestration Guide

> **Classification:** Supporting · Public-safe
> **Operating label:** Reference implementation
> **Maturity / claim state:** Target-state reference model; code snippets are illustrative, not production evidence.
> **Doctrine boundary:** This guide covers routing, isolation, and verification. Tenant treasury, yield, escrow, and settlement references are protocol/reference behaviors, not Conxian-Labs custody, discretionary fund control, market operation, or user-data extraction.

**Model:** Agent-as-a-Service (AaaS) reference pattern
**Alignment:** LangChain Multi-Agent / CrewAI Flow / Open Multi-Agent (TS)
**Version:** v2.2 (reference architecture)

## 1. Orchestration Pattern: Multi-Agent Systems (M.A.S.)

The BaaP model uses a hierarchical **Supervisor-Worker** M.A.S. pattern for multi-tenant isolation and goal decomposition.

### Supervisor Agent (Strategy Nexus - EXCO)

- **Role:** High-level goal decomposition, context switching, and task dispatching.
- **Isolation:** Injects the `TenantID` into every tool call.
- **Inter-Agent Communication:** Standardized via **MCP Tool Handshakes**.
- **Decision Logic:** Routes business intents to specialized worker crews based on the dynamic state-transition logic in `BOS_STATE_MACHINE.stub.json`.

### Worker Crews (Specialized EXCO Units)

- **Fiscal Vault policy crew:**
  - **Agents:** Liquidity analyst, payout policy, yield policy.
  - **Goal:** Apply per-tenant or protocol policy constraints, including timelocks; it does not take custody of tenant funds.
- **Nakamoto Guardian crew:**
  - **Agents:** Policy auditor, ZK-proof verifier, AML/KYC guardian.
  - **Goal:** Perform verifiable attestations (BitVM2/ZKML) without unnecessary PII exposure.
- **Sovereign Ops crew:**
  - **Agents:** ERP bridge, industrial labor coordinator, supply-chain oracle.
  - **Goal:** Bidirectional sync with SAP/Oracle via OData v4 and MCP.

## 2. Jurisdictional Sharding and Context Isolation

To prevent cross-tenant data leakage (“the contamination risk”), the BOS models multi-layer sharding:

### Layer 1: Identity and State Sharding

- **BNS/DID isolation:** Each tenant uses a unique Decentralized Identifier (DID) anchored to Bitcoin/Stacks.
- **Kwil namespace:** Relational state is logically isolated into tenant-specific schemas.
- **Tableland RLAC:** Public audit logs use Row-Level Access Control (RLAC) so authorized agents can read only the state roots within their policy boundary.

### Layer 2: Execution Isolation (the handshake)

All agentic execution must wrap tool calls in a secure `TenantContext`. The supervisor ensures that a worker crew receives only data relevant to its `tenant_id` and documented integration purpose.

```typescript
// Illustrative M.A.S. handshake via MCP; not a custody or settlement guarantee.
interface MASHandshake {
  source_agent: string;
  target_agent: string;
  tenant_id: string; // Mandatory for all BaaP operations
  intent_hash: string;
  payload: unknown;
}

async function performHandshake(handshake: MASHandshake) {
  const guardianResponse = await mcp.callTool("nakamoto_guardian", "verify_policy", {
    tenant_id: handshake.tenant_id,
    action: handshake.payload,
  });

  if (guardianResponse.approved) {
    // Protocol/reference policy call; not company-controlled fund execution.
    return await mcp.callTool("fiscal_vault", "execute_policy_action", handshake.payload);
  }
}
```

## 3. Sovereign Node (BiaB) Akash SDL Template

Tenants could deploy their own BOS instance using a standard **Sovereign Blueprint**. Secret material is mounted through the approved ZSE mechanism; no credential belongs in this public example.

```yaml
---
version: "2.0"
services:
  sovereign-node:
    image: conxian/sovereign-node:v2.2
    env:
      - TENANT_ID=YOUR_BNS_NAME
      - STACKS_PRIVATE_KEY=SECRET_MOUNTED_VIA_ZSE
      - TELEMETRY_PROTOCOL=nostr
      - PERSISTENCE_LAYER=kwil_hybrid
    expose:
      - port: 8080
        as: 80
        to:
          - global: true
profiles:
  compute:
    sovereign-node:
      resources:
        cpu:
          units: 2.0
        memory:
          size: 4Gi
        storage:
          size: 10Gi
  placement:
    akash:
      attributes:
        host: akash
      pricing:
        sovereign-node:
          denom: uakt
          amount: 100
deployment:
  sovereign-node:
    akash:
      profile: sovereign-node
      count: 1
```

## 4. Transparency and Governance Standard

- **Verifiable telemetry:** M.A.S. logs are emitted only as permitted by the tenant and data-minimization policy.
- **MMR state proofs:** A per-tenant Merkle Mountain Range (MMR) can provide inclusion proofs for historical events.
- **Sovereign portability:** A business can migrate its orchestration state between infrastructure providers when the documented state and key boundaries permit it.

---

Maintained as a public reference specification. See the [Doctrine Alignment Standard](../docs/DOCTRINE_ALIGNMENT_STANDARD.md) before promoting any target-state claim.
