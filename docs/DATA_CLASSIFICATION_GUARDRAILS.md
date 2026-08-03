# Data Classification Guardrails — GitHub Public-Safe Boundary

| Metadata | Value |
|---|---|
| Classification | Public-safe, non-authorization |
| Status | Active from 2026-08-02 |
| Owner | BOS program steward |
| Authority | [Business issue #943](https://github.com/Conxian/conxian-business/issues/943) |

## Classification Tiers

### PROHIBITED (never in Git/GitHub)
Must never appear in any repository, issue, PR, project, wiki, attachment, or CI artifact:

- Private keys, seeds, mnemonics, passwords, API keys, tokens, credentials
- Custody/quorum/recovery/ceremony details
- Signer or admin identities, principal names, IAM roles with resource bindings
- Private endpoints, internal IPs, VPC/network topology
- Restricted legal, financial, identity, or PII records
- Security vulnerability details under active embargo
- Raw secret-bearing material of any kind

### RESTRICTED (non-Git successor only)
Must exist only in the approved non-Git restricted-record system under accountable ownership:

- Financial models, cap tables, revenue projections
- Legal agreements, contracts, NDAs
- Personnel/HR records
- Security incident post-mortems with operational detail
- Partner/vendor agreements and pricing

### PUBLIC-SAFE (allowed in GitHub)
May exist in GitHub repositories under standard review:

- Architecture, design, and specification documents
- Code, configuration (without secrets), build scripts
- Test fixtures (without real keys/credentials)
- Public API documentation
- Governance policies, branching standards, promotion rules
- Issue trackers and PR descriptions (sanitized)
- CI/CD workflow definitions
- AGENTS.md and agent guidance
- Documentation and runbooks (without operational secrets)

### CONDITIONAL (requires sanitization)
May exist in GitHub only after removing restricted content:

- Incident summaries → sanitize to public-safe post-mortem
- Deployment runbooks → remove endpoints, credentials
- Monitoring dashboards → remove internal URLs, access tokens
- Performance reports → aggregate, remove customer-identifiable data

## Token and Reference Safety

- Use `${{ secrets.SECRET_NAME }}` in CI — never hardcode
- Reference external systems by public URL or sanitized identifier only
- Use `[REDACTED]` or `[RESTRICTED — see non-Git successor]` for necessary boundary markers
- Do not use "TBD" or "placeholder" for restricted content that needs an accountable record

## Verification

- All PRs are subject to secret scanning (gitleaks via `.github/workflows/secret-scan.yml`)
- Commits containing prohibited content must be squashed/rewritten before merge
- The BOS knowledge graph tracks classification boundaries per repository

## Non-Authorization Boundary

This document defines classification guardrails only. It does not authorize production action, release, or acceptance. Compliance with these guardrails does not satisfy security review, legal review, or Gate 5 acceptance.

---

*Governed by [GitHub-first BOS research-cycle operating model](GITHUB_FIRST_BOS_OPERATING_MODEL.md).*
