# cnx-arch-guardian: CTO Module Manifest

## Function: ATS Enforcement & IP Sovereignty
Runs automated collision audits across the codebase. Enforces the Sovereign Naming Matrix. Prevents off-spec logic from merging into the main branch.

## Programmatic Logic
1. **Lexicon Audit**: Scans all commits for legacy terminology (e.g., "POL", "stakeholder").
2. **Sovereignty Check**: Verifies that all wallet-related code adheres to the "Zero Secret Egress" principle (TEE/StrongBox only).
3. **Protocol Alignment**: Ensures all Clarity changes adhere to the CSF Standard Traits.

## MCP Wiring
- **Context7**: Retrieving latest protocol specs and standards.
- **GitHub**: Pre-commit / CI/CD hook integration.
