# Spec: Autonomous Launch & Revenue Mechanics

## ADDED Requirements

### Proposal: Founder's Cut Fee Logic (Governance-Gated; Not Approved)
The historical launch proposal described a hardcoded 0.1% Founder’s Cut as a carve-out from captured protocol fees rather than an additive user fee. This text is preserved as proposal context only: it is not an executable, approved, or deployment-ready requirement.

The historical proposal defined **captured protocol fees** as the protocol-retained portion of a transaction fee after third-party distributions and described integer arithmetic equivalent to `founders_cut = captured / 1000`, with the remainder retained in the protocol treasury/vault. Those terms do not authorize an allocation or transfer.

CON-1542 MUST NOT activate, implement, configure, or represent this proposal as approved. Activation requires separate ratified governance that explicitly defines the beneficiary, custody route, rate, and allocation semantics, together with protocol implementation and deployment evidence. This handoff does not invent or approve an alternative fee schedule.

#### Scenario: CON-1542 preserves the governance gate
- **Given** the historical 0.1% Founder’s Cut proposal
- **When** CON-1542 classifies revenue-policy ownership and evidence
- **Then** no founder allocation or transfer is activated, and the proposal remains blocked pending separate ratified governance

### Requirement: ALEX AMM Integration
The backend MUST utilize the ALEX Lab SDK for liquidity provisioning.
#### Scenario: Automated Liquidity
- **Given** an IDO event on ALEX
- **When** the LBP concludes
- **Then** the system MUST pair 10% of proceeds in an ALEX AMM pool for 6 months.

### Requirement: sBTC & USDCx Support
The system MUST support sBTC (uncapped) and USDCx as primary collateral.
#### Scenario: Asset Validation
- **Given** a deposit request
- **When** the asset is sBTC or USDCx
- **Then** the system MUST accept the deposit without supply cap restrictions.

### Requirement: 5-5-5 Referral Engine
The system MUST implement a tiered referral system for autonomous growth.
#### Scenario: Referral Distribution
- **Given** a transaction via a referral link
- **When** the transaction is finalized
- **Then** distribute 5% of fees to the referrer, 5% to the referee, and lock 5% for protocol health.

### Requirement: Key Relinquishment Plan
The protocol MUST have a verifiable path to "Burning the Keys."
#### Scenario: DAO Handover
- **Given** 24 months post-launch
- **When** the ExecutorDAO is stable
- **Then** the admin principal MUST be set to 0x0 (burn-address).
