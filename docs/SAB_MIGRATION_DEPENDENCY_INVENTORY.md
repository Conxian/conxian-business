# SAB migration dependency inventory

This inventory captures current Web2 dependencies that materially affect SAB sovereignty, verifiability, or operational control, and maps each to a target-state path.

This file is intentionally "program-level" (by dependency). Service-level Supabase/Neon usage is being expanded in https://linear.app/conxian-labs/issue/CON-337/inventory-current-supabase-and-neon-dependencies-by-service.

## Inventory

Columns:

- **System/service name**: the owning system (Nexus, Gateway, BOS, etc.)
- **Current provider**: hosted provider or third-party dependency
- **Business function**: what it enables
- **Data domain**: treasury, audit, routing, etc.
- **State type**: transactional, analytical, governance/audit, routing, or cache
- **Integrations / downstream consumers**: what depends on it
- **Migration target / candidate**: intended replacement path
- **Migration risk**: low/medium/high (first pass)
- **Rollback complexity**: low/medium/high (first pass)
- **Owner**: accountable owner for the migration surface
- **Notes / open questions**: anything blocking a clean target-state decision

| System/service name | Current provider | Business function | Data domain | State type | Integrations / downstream consumers | Migration target / candidate | Migration risk | Rollback complexity | Owner | Notes / open questions |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| BOS "state layer" | Supabase | Real-time financials, IP audit, exit velocity | BOS ops + audit | Analytical + governance/audit | Sovereign Ops Orchestrator, Fiscal Vault Oracle, Strategy Nexus | Sovereign/self-hosted SQL layer with on-chain checkpointing; treat as derived-only | High | Medium | Botshelo Mokoka | Identify which datasets are correctness-critical today vs "dashboard-only". |
| Fiscal Vault Oracle (runway + actions) | Supabase | `runway_metrics`, `treasury_actions`, `dlc_state_updates` read/write surfaces | Treasury | Analytical + governance/audit | OpenClaw TEE, dashboards, audit exports | Same as above; additionally enforce "144 blocks" commit cadence + deterministic checkpoints | High | Medium | Botshelo Mokoka | Confirm whether any downstream consumers treat Supabase rows as canonical (must be prohibited). |
| Fiscal Vault Oracle (state bridge) | Supabase (via MCP bridge) | Controlled interface for reads/writes to Supabase-backed tables | Treasury | Routing | OpenClaw TEE sandbox | MCP bridge to sovereign datastore (same call surface, different backend) | High | Medium | Botshelo Mokoka | Decide whether MCP remains the long-term abstraction boundary or is replaced by direct DB access. |
| Nexus derived read model | Neon (PostgreSQL) | Query-optimized derived read model for indexed L1 state | Transactional application state | Transactional | Nexus, Gateway, institutional egress exports | Sovereign/self-hostable PostgreSQL baseline (Neon is temporary) | High | High | Botshelo Mokoka | Inventory any Neon-specific assumptions (pooling, branching workflows, hosted-only extensions). |
| Audit/governance mirror (optional) | Tableland | Public mirror of audit and governance state | Audit + governance | Governance/audit | Dashboards, public verification surfaces | On-chain audit registry + optional non-authoritative mirror | Medium | Low | Botshelo Mokoka | Confirm which datasets are mirrored and whether anything depends on Tableland for correctness. |
| Ops dashboard hosting | Render | Hosts internal "Stitch" dashboard visualizing state | Ops / audit visualization | Routing | BOS internal dashboard | Self-hosted dashboard or sovereign hosting baseline (read-only, non-authoritative) | Medium | Low | Botshelo Mokoka | Dashboard should never be treated as evidence source; evidence must be commit-pinned and reproducible. |
| Gateway runtime hosting | Google Cloud (Cloud Run) | Hosts API surface and routing layer | Routing + interchain | Routing | External clients, internal services | Sovereign compute baseline (dedicated hosts / Kubernetes / enclave-adjacent constraints where required) | Medium | Medium | Botshelo Mokoka | Separate "sovereign compute" migration from datastore cutover to avoid coupled risk. |
| Showcase DApp deployment | Vercel | Deploys public Next.js surface | Public web surface | Routing | `showcase-dapp` | Sovereign static hosting (or any provider not in the correctness path) | Low | Low | Botshelo Mokoka | Not sovereignty-critical, but still a control-plane dependency. |
| Showcase DApp hosting | Firebase Hosting | Static hosting / rewrites | Public web surface | Routing | `showcase-dapp/out` artifacts | Sovereign static hosting | Low | Low | Botshelo Mokoka | Confirm whether Firebase is currently used for production, staging, or demo-only. |
| Execution engine | Linear | Programmatic task specs and automation triggers | Ops / governance | Governance/audit | Sovereign Ops Orchestrator | Explicitly accepted as "coordination dependency" (not data authority) or migrate to sovereign issue tracker | Low | Low | Botshelo Mokoka | Treat as workflow tooling, not a source of business truth. |
| Institutional market data | LSEG (via MCP bridge) | Pricing/volatility and compliance reference data | Treasury | Analytical | Fiscal Vault Oracle | Multi-source market data + cryptographic evidence trails; isolate provider trust | Medium | Medium | Botshelo Mokoka | Define failure mode: ability to halt safely without provider availability. |
