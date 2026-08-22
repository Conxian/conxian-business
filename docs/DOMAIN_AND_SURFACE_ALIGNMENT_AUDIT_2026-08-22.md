# Domain and Surface Alignment Audit

**Date:** 2026-08-22  
**Source of truth:** `conxian-business`  
**Status:** Approved target model; implementation follows this boundary.

## Executive decision

Conxian needs one coordinated business surface, not one undifferentiated application. The public Labs site, client service entrypoints, authenticated team controls, runtime APIs, and open-source community assets have different trust and support requirements and must remain separate while sharing navigation and contracts.

## Canonical domain roles

| Domain | Audience | Canonical responsibility |
| --- | --- | --- |
| `www.conxian-labs.com` | public, prospects, clients | Public business site, service directory, documentation entrypoints, client onboarding, and `/nexus`, `/gateway`, `/market` informational/client surfaces |
| `control.conxian-labs.com` | internal team and approved operators | Authenticated BOS control plane: governance, audit, releases, environments, access, assets, and operational actions |
| `conxian.org` | developers and open-source community | Open-source repositories, SDKs, contribution guides, technical references, licenses, and community resources |
| `conxian.io` | future product/API identity | Reserved until product/API ownership, DNS, and security boundaries are explicitly approved |

## Surface contract

- Public pages explain capabilities and provide safe links; they do not expose privileged mutation endpoints.
- Client and machine-to-machine services use brokered authentication and explicit service contracts. Runtime APIs remain on independently deployed runtimes, even when linked from the Labs domain.
- Team operators enter through `control.conxian-labs.com`. The control plane is the business operating surface, not the runtime execution layer.
- Open-source assets remain discoverable from `conxian.org`; private governance, customer data, secrets, and operational evidence do not move there.
- The service registry is the deployable inventory. Every service needs an owner, repository, health/readiness contract, auth mode, safe-test status, and public path or hostname where applicable.

## Current repository alignment

`conxian-business` contains the control-plane application, admin-runtime boundary documentation, service registry, and organization-wide operating docs. The registry identifies `conxian-gateway`, `conxian-nexus`, `conxian-market`, `conxius-platform`, `conxius-orbit`, and `conxius-wallet` as independently deployed runtimes; `lib-conxian-core`, `conxius-enclave-sdk`, and `conxian-ui` remain libraries/packages.

## Rollout order

1. Confirm DNS ownership and Vercel project mapping for Labs and control domains.
2. Deploy the public Labs site separately from the control plane.
3. Deploy the control plane to `control.conxian-labs.com` with protection and BOS session authorization.
4. Assign runtime hostnames and route public paths `/nexus`, `/gateway`, and `/market` through the Labs navigation layer without proxying privileged APIs through the public site.
5. Verify M2M broker, health/readiness endpoints, safe-test mode, audit logging, and rollback evidence.
6. Publish the open-source catalog and documentation on `conxian.org`.
7. Defer `conxian.io` until a separate product/API domain ADR is accepted.

## Gaps requiring follow-up

- GitHub issue creation/update could not be performed in this session because repository access is read-only.
- Runtime hostnames for all independently deployed services need DNS and deployment confirmation.
- Authentication, tenant access, client onboarding, and asset-management modules are future control-plane work beyond the initial scaffold.
- The public Labs repository must implement the public paths; this control-plane repository should not absorb its presentation layer.

## Issue-ready work items

- **DOMAIN-001:** Map Vercel projects and DNS records for Labs, control, runtime, and reserved domains.
- **DOMAIN-002:** Build the public Labs service directory and client entrypoints for `/nexus`, `/gateway`, and `/market`.
- **DOMAIN-003:** Harden control-plane authentication, operator roles, protected deployment, and audit boundaries.
- **DOMAIN-004:** Publish the open-source catalog and contribution/documentation navigation on `conxian.org`.
- **DOMAIN-005:** Verify runtime health/readiness, M2M broker policy, safe-test mode, and rollback evidence across the registry.
- **DOMAIN-006:** Create an ADR for `conxian.io` only after product/API ownership and security requirements are known.

## Definition of aligned

A release is aligned when public, client/M2M, internal, and open-source users each have a clear entrypoint; no public page bypasses auth boundaries; every runtime has an owner and readiness contract; and the registry, deployment configuration, documentation, DNS, and runbooks agree.
