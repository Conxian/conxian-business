# Conxian Organization SLA Policy

## Purpose

This document codifies Conxian's organization-level Service Level Agreement (SLA) posture and policy guidance for repository owners, contributors, and commercial partners. It enforces a strict structural separation between public, community-maintained open-source protocol surfaces and paid enterprise offerings where formal SLAs are provided under commercial contracts.

---

## 1. Scope & Structural Boundaries

1. **Public Open-Source Protocol Repositories (`conxian` org)**:
   - Covers: `lib-conxian-core`, `conxius-enclave-sdk`, `conxius-wallet`, `conxian-nexus`, `conxian_market`, and all open-source libraries.
   - Posture: **NO SLA**. All code is provided "AS IS" without uptime warranties or guaranteed resolution windows. Support is community-best-effort via GitHub Issues and Discussions.

2. **Enterprise B2B Gateway & Private Node Offerings (`conxian-labs.com`)**:
   - Covers: Managed B2B `conxian-gateway` deployments, Private Sovereign Nexus Nodes, and custom ISO 20022 banking normalizers.
   - Posture: **Contractual SLA**. SLA commitments (99.5% target uptime, SEV1 1-hour business hours acknowledgment) are strictly bounded to signed B2B contracts.

---

## 2. Policy Principles

- **No Protocol Uptime Commitments**: Never guarantee uptime for immutable decentralized layers (Bitcoin L1 / Stacks L2) or local hardware enclaves (AWS Nitro, Android StrongBox).
- **No Financial Liabilities in v1**: SLA remedies in v1.0 are limited to Root Cause Analysis (RCA) within 5 business days and prioritized patch advisory delivery. Financial service credits or cash penalties are explicitly excluded.
- **Force Majeure & Vendor Exclusions**: All SLA policies must explicitly exclude external network congestion, blockchain reorgs, cloud host outages, and hardware enclave firmware deprecations.

---

*LEGAL REVIEW REQUIRED: Any timelines or remediation commitments must be reviewed by legal counsel before inclusion in contractual language.*
