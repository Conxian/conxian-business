# Domain Alignment Issue Handoff

This file is the session-safe handoff for maintainers. It records the approved domain model and issue-ready work without claiming that GitHub issues have already been created.

## Approved model

- Labs: `www.conxian-labs.com`
- Team control: `control.conxian-labs.com`
- Open source: `conxian.org`
- Reserved future product/API identity: `conxian.io`

## Required implementation lanes

### Public Labs
Owns business messaging, service discovery, documentation links, client onboarding, and safe public routes for Nexus, Gateway, and Market.

### Control plane
Owns authenticated governance, release promotion, audit evidence, environment state, operator access, policy approvals, business assets, and links to runtime operations.

### Runtime services
Own execution and M2M contracts. They must not be implemented as UI-only placeholders or exposed through unauthenticated public routes.

### Open source
Owns public repositories, SDK documentation, contribution guidance, licenses, and community-facing technical material.

## Session handoff checklist

- [ ] Create/update DOMAIN-001 through DOMAIN-006 in GitHub with owners and acceptance criteria.
- [ ] Confirm Vercel project IDs and custom domains.
- [ ] Confirm DNS records and TLS for all approved hostnames.
- [ ] Confirm control-plane auth and operator role mapping.
- [ ] Confirm M2M broker configuration and runtime origins.
- [ ] Confirm `/nexus`, `/gateway`, and `/market` are public/client surfaces, while privileged operations stay in control.
- [ ] Confirm open-source catalog ownership on `conxian.org`.
- [ ] Record `conxian.io` as reserved; do not route production traffic there yet.
- [ ] Attach health/readiness and rollback evidence to the release record.

## Non-negotiable boundary

The public site may link to services and documentation, but it is not the authority for privileged business operations. The control plane is the operator authority; runtime services are execution authorities; the registry and signed contracts connect them.
