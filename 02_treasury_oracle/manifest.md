# cnx-treasury-oracle: CFO Module Manifest

## Function: Sovereign Runway Management
Monitors fiat (ZAR) burn rates against native yield generation. Enforces the strict rule: Locked principal must earn yield; yield is liquid. Tracks native Conxian-Labs Bonds used for ops financing.

## Programmatic Logic
1. **Runway Calculus**: Daily sync of fiat bank balances (via ERP) and on-chain multisig balances.
2. **Burn Rate Enforcement**: Alerts Exco via Linear if runway drops below 18 months.
3. **Yield Optimization**: Monitors `locked_principal` and ensures 100% utilization in liquidity pools.

## MCP Wiring
- **Neon**: Primary state storage for `cnx_bos.treasury_runway`.
- **Supabase**: Real-time balance syncing.
- **Linear**: Automated financial alerting.
