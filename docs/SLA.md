# Conxian Service Level Agreement (SLA) — Version 1.0

| Metadata | Value |
|---|---|
| Classification | Public-safe SLA policy & Risk-Bounded Support Matrix |
| Version | 1.0 (v1.9.5 Era) |
| Effective Date | 2026-09-18 |
| Authority | Conxian Business Operations System (BOS) |

---

## 1. Core Reality & Open-Source Funding Boundaries

Commercial SLAs (e.g., guaranteed 99.9% network availability, 1-hour 24/7 incident response, or financially backed penalty credits) require round-the-clock dedicated NOC/incident response capacity. In early-stage sovereign protocol infrastructure:

- **Lumpy Funding & Lean Teams**: Pre-seed and grant budgets do not support 24/7/365 follow-the-sun engineering rosters.
- **Maintainer Bottleneck**: Forcing lean engineering teams into constant PagerDuty rotations diverts critical resources from core systems architecture and protocol hardening.
- **Asymmetric Security Risk**: Sovereign layers (Bitcoin L1 primitives in `lib-conxian-core`, TEE SDK `conxius-enclave-sdk`, and zero-custody wallets `conxius-wallet`) carry severe security implications. Rushed patches forced by arbitrary SLA windows risk introducing catastrophic regression or key-material exposure vectors.

---

## 2. Tiered Support & SLA Matrix

Conxian enforces a strict structural separation between open-source public protocol surfaces and paid enterprise/managed offerings:

| Tier / Surface | Target Repositories / Services | SLA Guarantee & Support Boundary |
|---|---|---|
| **Public Protocol / Core Layer** | `lib-conxian-core`, `conxius-enclave-sdk`, `conxius-wallet`, `conxian-nexus`, public `conxian.org` | **NO SLA**. Public repositories are provided "AS IS" under standard open-source licenses (Apache 2.0 / BSL). Support is provided on a community-best-effort basis via GitHub Discussions and Issues. |
| **Enterprise Gateway & Private Nodes** | B2B Private `conxian-gateway`, Private Nexus Nodes, custom ISO 20022 normalizers | **Contractual SLA**. Offered exclusively under signed B2B commercial agreements. SLA covers integration support, configuration assistance, and business-hours incident response times. |

---

## 3. Incident Response Severities & Target Response Times (B2B Contractual Tier)

For clients operating under signed B2B Enterprise Gateway contracts:

| Severity Level | Definition | Business Hours Response (09:00 - 18:00 UTC) | Target Advisory / Patch Window | Off-Hours Response |
|---|---|---|---|---|
| **SEV1 — Critical** | Complete service outage or data corruption affecting production gateway/settlement flows | **1 Hour Acknowledgment** | Target Patch Advisory within 24 Hours | Best Effort |
| **SEV2 — Major** | Degraded functionality or major feature impairment with no immediate workarounds | **4 Business Hours** | Next Business Day | Next Business Day |
| **SEV3 — Moderate** | Non-critical bug or minor feature issue with viable workaround | **1 Business Day** | Next Sprint Cycle | Next Business Day |
| **SEV4 — Minor** | Feature request, documentation clarification, or cosmetic issue | **2 Business Days** | Backlog Prioritization | Next Business Day |

*Business hours are strictly defined as 09:00 to 18:00 UTC, Monday through Friday.*

---

## 4. Explicit Exclusions & Force Majeure

Conxian's SLA commitments explicitly exclude outages, performance degradation, or state verification delays caused by external factors beyond platform control:

1. **L1/L2 External Network States**: Bitcoin L1 network congestion, mempool fee spikes, Stacks network consensus halts, or blockchain reorgs.
2. **Hardware Vendor & Firmware Deprecations**: Hardware Enclave firmware or API updates by third-party vendors (AWS Nitro, Android StrongBox/TEE, Apple Secure Enclave).
3. **External RPC & Infrastructure Outages**: Downtime caused by third-party RPC providers, cloud platform outages (AWS, Azure, Render, Supabase), or customer-operated infrastructure failures.
4. **Force Majeure**: Extreme network partitions, sovereign regulatory halts, or malicious zero-day attacks against underlying OS primitives.

---

## 5. Target Uptime & Remedy (Zero Financial Liability in v1)

- **Target Uptime**: Conxian targets a **99.5% monthly uptime percentage** for managed B2B Gateway endpoints, calculated over a calendar month excluding scheduled maintenance windows announced at least 24 hours in advance.
- **Financial Credits & Remedy**: For Version 1.0, **no financial service credits are issued**. Conxian commits to transparent incident discipline:
  - Root Cause Analysis (RCA) delivered within **5 business days** for all SEV1 incidents.
  - Public or private post-mortem published upon resolution.

---

## 6. Deferred Features & Future Scaling Trigger

To maintain operational realism during early adoption, the following enterprise SLA features are explicitly deferred:
- 24/7/365 dedicated live phone or NOC monitoring.
- Enterprise ticketing system integration (Jira/PagerDuty).
- Dedicated status page infrastructure (`status.conxian.org`).

**Trigger for Deferral Removal:** Enterprise SLA features will be enabled upon onboarding **Customer #3** or signing the first dedicated Enterprise Support contract.
