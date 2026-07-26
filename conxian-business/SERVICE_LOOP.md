# Conxian BOS Service Loop

> **Classification:** Supporting · Public-safe
> **Operating label:** Reference implementation
> **Maturity / claim state:** Target-state reference model.
> **Doctrine boundary:** “Treasury”, “yield”, “settlement”, and “escrow” in this diagram describe protocol-, tenant-, or participant-level behavior. They do not describe Conxian-Labs custody, discretionary fund control, market operation, or user-data extraction.

This page shows how client intent, governance, routing, and verification could connect. It is not a description of a company-controlled financial workflow.

## Single-Tenant Operational Loop

```mermaid
graph TD
    subgraph BOS_CLIENT [Client / protocol intent]
        A[Gateway intelligence] --> B[Protocol yield policy]
        B --> C[Contract or tenant policy update]
    end

    subgraph BOS_SUPPLIER [Infrastructure / verification]
        D[Nexus governance] --> E[Protocol settlement state]
        E --> F[External Stacks / other protocol adapters]
    end

    C -.-> D
    F -.-> A
```

## Multi-Tenant Platform Orchestration (BaaP)

```mermaid
graph TD
    subgraph CONTROL_PLANE [Reference orchestration plane]
        CP[Orchestrator] --> T1[Tenant A BOS]
        CP --> T2[Tenant B BOS]
        CP --> T3[Tenant C BOS]
    end

    subgraph SHARED_RUNTIME [Decentralized infrastructure]
        T1 --> AK[Akash Network]
        T2 --> AK
        T3 --> AK
        T1 --> KW[Kwil / Tableland]
        T2 --> KW
        T3 --> KW
    end

    subgraph SETTLEMENT_LAYER [Bitcoin-anchored protocol layer]
        AK --> ST[Stacks L2]
        KW --> ST
        ST --> BTC[Bitcoin L1]
    end
```

The arrows represent routing and verification relationships. They do not imply that Conxian-Labs receives participant funds, controls tenant treasuries, or operates an investment or trading market.
