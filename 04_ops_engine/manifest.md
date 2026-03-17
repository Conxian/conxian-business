# cnx-ops-engine: COO Module Manifest

## Function: Deployment Efficiency
Plugs directly into Linear via Stitch. Measures the precise gas-efficiency of operational execution and bottleneck resolution across all modules.

## Programmatic Logic
1. **Velocity Tracking**: Calculates "Operational Gas" (effort/time) per Linear cycle.
2. **Bottleneck Detection**: Identifies modules with stalled tickets or high churn.
3. **Resource Allocation**: Suggests agent reallocation based on current velocity goals.

## MCP Wiring
- **Linear**: Primary input for task and cycle data.
- **Stitch**: UI generation for operational reports.
- **Neon**: Logging metrics in `cnx_bos.operational_metrics`.
