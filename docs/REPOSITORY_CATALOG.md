# Repository catalog

This catalog is the Conxian organization-level map of _what each repository is for_ and _how it should be presented publicly_.

The `conxian-business` repository is an umbrella repo that vendors key Conxian repositories as Git submodules (see `.gitmodules`).

## Categories

- **Platform**: user-facing dashboards/portals and operational UIs.
- **Wallet**: end-user, non-custodial wallet applications.
- **Gateway**: institutional middleware and API surfaces.
- **Website**: marketing, docs, and landing pages.
- **SDK**: libraries intended to be depended on by other repos.
- **Protocol**: smart contracts and protocol logic.
- **Ops/Admin**: governance, OpenSpec, audits, and internal tooling.

## Recommended pins (GitHub org profile)

If we can only pin a few repos on the GitHub org profile, these are the clearest entry points:

1. `conxius-wallet` (Wallet)
2. `conxian-gateway` (Gateway)
3. `conxian-ui` or `conxius-platform` (Platform)
4. `Conxian` (Protocol)
5. `lib-conxian-core` (SDK)
6. `conxian-labs-site` (Website)

## Repositories (as vendored submodules)

| Category | Repository | Primary audience | Notes |
| --- | --- | --- | --- |
| Gateway | `conxian-gateway` | Integrators, institutions | Rust gateway services and API surface. |
| Wallet | `conxius-wallet` | End users | Non-custodial wallet product. |
| Platform | `conxius-platform` | Operators, institutions | Platform services (admin dashboards, etc.). |
| Platform | `conxian-ui` | Operators, institutions | UI app(s) and specs. |
| Protocol | `Conxian` | Protocol engineers | Contracts + protocol logic. |
| State node | `conxian-nexus` | Operators | Nexus state node implementation. |
| SDK | `lib-conxian-core` | App / service developers | Shared core library. |
| SDK | `lib-conclave-sdk` | Integrators | Conclave/TEE-related SDK components. |
| Website | `conxian-labs-site` | Public | Marketing + public docs site. |
| Tooling | `stacksorbit` | Developers | Stacks deployment and monitoring CLI/tooling. |

## Public README expectations (per repository)

For all user-facing repos (Wallet, Gateway, Platform, Website, SDK), the README should include:

- `## Purpose`: a 2–5 line description of the repository’s job.
- `## Status`: one of `active`, `alpha`, `beta`, `stable`, `maintenance`, `archived`, plus a short “what’s safe to use”.
- `## Ownership`: pointer to CODEOWNERS/maintainers.
- `## Releases`: how versions/tags are produced and where to find release notes.

## Release discipline (minimum bar)

- Use SemVer tags: `vX.Y.Z`.
- Keep `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format with a top-level `## [Unreleased]` section.
- For user-facing behavior changes, do not merge without an entry in `CHANGELOG.md`.
