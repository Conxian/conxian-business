# BOS Platform Specification: Business-as-a-Platform (BaaP)

> **Classification:** Supporting · Public-safe
> **Operating label:** Reference implementation
> **Maturity / claim state:** Target-state unless a section names `Implemented` or `Verified` evidence.
> **Doctrine boundary:** This is a public reference architecture. It describes infrastructure and protocol behavior, not Conxian-Labs custody, discretionary fund control, market operation, or user-data extraction.

**Version:** v2.3 (reference architecture)

## 1. Vision

The Conxian BOS is a **Business-as-a-Platform (BaaP)** reference architecture. It describes how third-party businesses could deploy, run, and govern autonomous operations using Conxian infrastructure. The architecture is anchored to Bitcoin for trust and security; it does not make Conxian-Labs a custodian, fund manager, exchange, or market participant.

## 2. Multi-Tenancy: Jurisdictional Sharding

To maintain sovereignty and security across multiple tenants, the BOS models **Jurisdictional Sharding**:

- **Sovereign Elastic Pools:** Shared compute resources (Akash) with isolated state shards (Kwil).
- **Namespace Isolation:** Each tenant is assigned a unique namespace (BNS name) for state anchoring.
- **M.A.S. Context Isolation:** Strategy Nexus (EXCO) uses a Supervisor-Worker M.A.S. pattern for per-tenant session isolation, with zero-data-leakage as the target control.
- **Resource Governance:** Tenants define their own policy guardrails (for example, timelocks and multi-signature thresholds) independently of the Conxian-Labs software vendor.

## 3. Sovereign Node Architecture (BiaB)

A “Sovereign Node” is a containerized “Business-in-a-Box” (BiaB) deployment instantiated from a declarative **BOS Blueprint**:

- **Strategy Nexus (EXCO):** Reference intelligence and M.A.S. supervisor.
- **Fiscal Vault (protocol/reference policy):** Contract- or tenant-defined treasury and yield constraints; not company custody or discretionary fund management.
- **Nakamoto Guardian (compliance):** Automated compliance and ZKML policy verification.
- **Sovereign Ops (ERP):** Labor coordination and industrial ERP integration.

### Deployment Stack

- **Compute:** Akash Network (managed via SDL).
- **Storage:** Kwil (relational) + Tableland (state roots).
- **Identity:** DID anchored to Bitcoin/Stacks.
- **Interface:** Model Context Protocol (MCP) v1.0.
- **Telemetry:** Nostr (Kind 26001–26003), subject to data minimization.

## 4. SDK Viewpoint: `conxius-enclave-sdk`

The `conxius-enclave-sdk` is a shared enclave and signing-abstraction reference component for BaaP integrations. Its interfaces do not, by themselves, establish hardware-backed production support or value-bearing settlement support.

- **Hardware enclave abstraction:** Native interfaces for StrongBox/TEE integrations.
- **Sovereign handshake:** Non-custodial signing interfaces for user- or tenant-authorized actions.
- **B2B identity:** Cryptographic identity primitives for sovereign partners and automated billing integrations.

## 5. Adoption context

This specification makes no market-share, revenue, competitive-capture, or asset-management claim. Commercial strategy and market analysis belong in the authorized GitHub organization. Public documentation should describe the technical boundary and its evidence, not a promise to operate or capture a market.

## 6. Enhancements and roadmap

The following remain **Target-state** architecture topics until their implementation and verification evidence is linked:

- Consolidated state: moving chain-polling responsibilities from middleware to the state/proof layer where validated.
- Alpen/Albert integration for ZK-rollup research and high-frequency protocol settlement.
- B2Network support for B2B integration paths.
- Regional onboarding experiments that preserve the non-custodial client and protocol boundaries.

---

Maintained as a public reference specification. Linked implementation and governance decisions must follow the [Doctrine Alignment Standard](../docs/DOCTRINE_ALIGNMENT_STANDARD.md).
