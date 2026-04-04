This is an audit artifact for CON-135.

Snapshot date: 2026-04-04 (UTC)

Scope: open CON system issues, operationally defined as issues in states Triage/Todo/In Progress/In Review/Backlog that have at least one of these labels: `Release`, `Governance`, `Security`, `Hygiene`, `Bounty`.

Query (as of snapshot): union of `ch-linear issue list -T CON -l <LABEL> -s Triage -s Todo -s "In Progress" -s "In Review" -s Backlog --json` for each label in [`Release`, `Governance`, `Security`, `Hygiene`, `Bounty`], de-duplicated by `identifier` (use pagination / a sufficiently high limit so results are not truncated).

## Operating definitions

- **Claim-open now**: `state == Todo` AND category `community-claimable` AND label `Bounty Open` AND unassigned.
- **Community-claimable**: safe to execute externally (docs/repo hygiene), with no privileged deploy/wallet/treasury access required. For governance/content work, this only applies when the issue has concrete acceptance criteria and maintainers retain final approval.
- **Internal-only**: security-sensitive, deployment-sensitive, wallet/treasury/signer, or release-gating work.
- **Blocked**: intended work, but can't proceed until a prerequisite is resolved.
- **Not suitable for bounty execution**: decision-heavy, underspecified, or otherwise not a good fit for external bounty execution as-is.

> Note: `community-claimable` is a safety classification only. An issue is actually open to community claiming only when it also meets the `Claim-open now` conditions (state `Todo`, unassigned, and labeled `Bounty Open`). Other `community-claimable` issues remain maintainer-gated until they are promoted to `Claim-open now`.

## Payout alignment

- Claim intake and maintainer review can proceed before payout readiness exists.
- **Payout-enabled bounty execution begins only after**:
  - ConxianCSF full system deployment is verified on Stacks mainnet
  - ALEX launch funding path is live and confirmed as the bounty source
  - signer, wallet, and approval controls are verified internally
  - post-deploy verification and rollback expectations are documented
- All bounty funds must be sourced exclusively from the ALEX launch pathway once deployment is live; do not use ad hoc or implied treasury commitments before that point.
- **A claim is not a payout commitment** until all of the above are satisfied and the ALEX-funded payout path is verified end-to-end with internal signer/wallet/approval controls.
- Until those checks are complete, issues may be claim-screened and worked only under explicit maintainer approval and without any implied payout commitment.

## Summary

- Total issues in scope: **90**
- Community-claimable: **14**
- Internal-only: **55**
- Blocked: **1**
- Not suitable for bounty execution: **20**
- Claim-open now (subset): **8**

## Claim-open now

| Issue | Title | Assignee | Labels |
| --- | --- | --- | --- |
| CON-178 | Release hygiene — .github | (unassigned) | Bounty, Bounty Open, Release |
| CON-182 | Release hygiene — Conxian | (unassigned) | Bounty, Bounty Open, Release |
| CON-186 | Release hygiene — Conxian_UI | (unassigned) | Bounty, Bounty Open, Release |
| CON-198 | Release hygiene — conxian-labs-site | (unassigned) | Bounty, Bounty Open, Release |
| CON-214 | Release hygiene — lib-conclave-sdk | (unassigned) | Bounty, Bounty Open, Release |
| CON-218 | Release hygiene — lib-conxian-core | (unassigned) | Bounty, Bounty Open, Release |
| CON-222 | Release hygiene — stacksorbit | (unassigned) | Bounty, Bounty Open, Release |
| CON-78 | CON-75: [BOUNTY] Gateway Edge - Offline-First POS Sync | (unassigned) | Bounty, Bounty Open |

## Full classification

| Issue | State | Category | Labels | Title |
| --- | --- | --- | --- | --- |
| CON-129 | Todo | internal-only | Bounty, Release | CSF mainnet readiness gate |
| CON-131 | In Progress | not suitable for bounty execution | Bounty | Adopt stricter bounty workflow for Conxian-Labs |
| CON-132 | In Review | not suitable for bounty execution | Governance | Update conxian-business for BOS operating requirements |
| CON-133 | In Progress | internal-only | Governance, Release | Production deployment readiness audit for revenue-critical products |
| CON-135 | Todo | not suitable for bounty execution | Bounty, Governance, Release | Roll out claimable community workflow across system issues |
| CON-136 | Todo | internal-only | Release | ConxianCSF internal wallet and ALEX deployment readiness |
| CON-140 | Todo | internal-only | Release | Mainnet readiness checklist — Conxian/Conxian |
| CON-141 | Todo | internal-only | Release | Mainnet readiness checklist — conxius-wallet |
| CON-142 | Backlog | internal-only | Bounty, Release | Mainnet readiness checklist — conxius-platform |
| CON-143 | Backlog | internal-only | Release | Mainnet readiness checklist — conxian-gateway |
| CON-144 | Backlog | internal-only | Release | Mainnet readiness checklist — Conxian_UI |
| CON-146 | Backlog | internal-only | Release | Mainnet readiness checklist — stacksorbit |
| CON-148 | In Progress | not suitable for bounty execution | Governance | BOS business buildout — conxius-wallet |
| CON-149 | Todo | not suitable for bounty execution | Governance | BOS business buildout — conxius-platform |
| CON-150 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — Conxian_UI |
| CON-151 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — conxian-gateway |
| CON-152 | In Progress | not suitable for bounty execution | Governance | BOS business buildout — conxian-business |
| CON-153 | Todo | not suitable for bounty execution | Governance | BOS business buildout — Conxian/Conxian |
| CON-154 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — lib-conxian-core |
| CON-155 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — stacksorbit |
| CON-156 | In Review | not suitable for bounty execution | Governance | BOS business buildout — business units and portfolio separation |
| CON-161 | Todo | internal-only | Governance, Security | Extend treasury oracle schema for external settlement logs |
| CON-162 | Todo | internal-only | Governance, Security | Enforce proposal-only external settlement triggers in TEE |
| CON-165 | Todo | internal-only | Governance, Security | Enforce TEE proposal-only settlement attestation in treasury oracle |
| CON-166 | In Progress | internal-only | Governance, Release | Track global settlement ingress rollout |
| CON-167 | Todo | internal-only | Bounty | Maintainer payout enablement checklist for ALEX-funded bounties |
| CON-168 | Backlog | internal-only | Release | Mainnet readiness checklist — .github |
| CON-169 | Backlog | internal-only | Release | Mainnet readiness checklist — conxian-nexus |
| CON-171 | In Review | internal-only | Release | Mainnet readiness checklist — lib-conclave-sdk |
| CON-172 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — conxian-labs-site |
| CON-173 | Backlog | not suitable for bounty execution | Governance | BOS business buildout — conxian-nexus |
| CON-176 | Todo | internal-only | Governance | Security hardening — .github |
| CON-177 | Todo | internal-only | Security | Governance standardization — .github |
| CON-178 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — .github |
| CON-179 | Todo | internal-only | Hygiene | Security hardening — Conxian |
| CON-180 | Todo | internal-only | Governance | Secret and artifact cleanup — .github |
| CON-181 | Todo | internal-only | Security | Governance standardization — Conxian |
| CON-182 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — Conxian |
| CON-183 | Todo | internal-only | Hygiene | Secret and artifact cleanup — Conxian |
| CON-184 | Todo | internal-only | Governance | Security hardening — Conxian_UI |
| CON-185 | Todo | internal-only | Security | Governance standardization — Conxian_UI |
| CON-186 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — Conxian_UI |
| CON-187 | Todo | internal-only | Hygiene | Secret and artifact cleanup — Conxian_UI |
| CON-192 | Todo | internal-only | Governance | Security hardening — conxian-gateway |
| CON-195 | Todo | internal-only | Hygiene | Secret and artifact cleanup — conxian-gateway |
| CON-196 | Todo | internal-only | Governance | Security hardening — conxian-labs-site |
| CON-197 | Todo | internal-only | Security | Governance standardization — conxian-labs-site |
| CON-198 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — conxian-labs-site |
| CON-199 | Todo | internal-only | Hygiene | Secret and artifact cleanup — conxian-labs-site |
| CON-200 | Todo | internal-only | Governance | Security hardening — conxian-nexus |
| CON-201 | Todo | internal-only | Security | Governance standardization — conxian-nexus |
| CON-202 | Todo | internal-only | Release | Secret and artifact cleanup — conxian-nexus |
| CON-204 | In Review | community-claimable | Governance | Release hygiene — conxian-nexus |
| CON-205 | Todo | internal-only | Security | Security hardening — conxius-platform |
| CON-207 | Todo | internal-only | Hygiene | Secret and artifact cleanup — conxius-platform |
| CON-208 | Todo | internal-only | Governance | Security hardening — conxius-wallet |
| CON-210 | Todo | internal-only | Release | Security hardening — lib-conclave-sdk |
| CON-211 | In Review | internal-only | Hygiene | Secret and artifact cleanup — conxius-wallet |
| CON-212 | Todo | internal-only | Governance | Governance standardization — conxius-wallet |
| CON-214 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — lib-conclave-sdk |
| CON-215 | Todo | internal-only | Hygiene | Secret and artifact cleanup — lib-conclave-sdk |
| CON-216 | In Review | internal-only | Governance | Security hardening — lib-conxian-core |
| CON-217 | Todo | internal-only | Security | Governance standardization — lib-conxian-core |
| CON-218 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — lib-conxian-core |
| CON-219 | Todo | internal-only | Hygiene | Governance standardization — stacksorbit |
| CON-220 | Todo | internal-only | Governance | Security hardening — stacksorbit |
| CON-221 | Todo | internal-only | Security | Secret and artifact cleanup — lib-conxian-core |
| CON-222 | Todo | community-claimable | Bounty, Bounty Open, Release | Release hygiene — stacksorbit |
| CON-223 | Todo | internal-only | Hygiene | Secret and artifact cleanup — stacksorbit |
| CON-226 | In Progress | internal-only | Governance, Security | Create secret incident and remediation procedure |
| CON-227 | In Review | internal-only | Governance, Security | Map repo readiness gates by control domain |
| CON-229 | Todo | internal-only | Governance, Release | Run ConxianCSF mainnet go/no-go readiness review |
| CON-230 | Todo | internal-only | Bounty, Release | Confirm bounty funding and payout activation for mainnet |
| CON-231 | Backlog | blocked | Bounty, Governance | Decide which bounties can open before mainnet go-live |
| CON-232 | In Progress | internal-only | Release | Run mainnet countdown and launch communications plan |
| CON-233 | Todo | internal-only | Governance, Security | Verify wallets, signers, and approval controls for launch |
| CON-239 | In Review | community-claimable | Governance | Add purpose and status sections to flagship READMEs |
| CON-259 | Backlog | community-claimable | Governance | Improve clarity across public-facing Conxian repos |
| CON-260 | Backlog | not suitable for bounty execution | Governance | Clarify org portfolio and pinned repositories |
| CON-269 | Backlog | community-claimable | Governance | Audit Conxian_UI public-facing clarity |
| CON-294 | Backlog | not suitable for bounty execution | Governance | Define public repo taxonomy and site navigation |
| CON-296 | In Progress | not suitable for bounty execution | Governance | Define trust and proof messaging for public surfaces |
| CON-298 | Backlog | not suitable for bounty execution | Governance | Select and order pinned flagship repos |
| CON-299 | Backlog | community-claimable | Governance | Standardize flagship repo README structure |
| CON-300 | Backlog | not suitable for bounty execution | Governance | Draft trust, governance, and proof content |
| CON-301 | Backlog | community-claimable | Governance | Classify public repos by external role |
| CON-305 | Todo | internal-only | Security | Fix redaction scanner statefulness in conxius-wallet |
| CON-369 | Triage | internal-only | Release | Mainnet readiness checklist — conxian-business |
| CON-370 | Triage | not suitable for bounty execution | Governance | BOS business buildout — lib-conclave-sdk |
| CON-78 | Todo | community-claimable | Bounty, Bounty Open | CON-75: [BOUNTY] Gateway Edge - Offline-First POS Sync |

