# Dependabot Security Alert Remediation Guide
## Conxian Organization — July 2026

### Summary

| Repo | Package Mgr | Open Alerts | Fixable Now | Blocked |
|------|------------|-------------|-------------|---------|
| `Conxian/Conxian` | npm | 4 (1 high, 3 low) | 1 fixed (postcss) | elliptic (no fix) |
| `conxian_ui` | pnpm | 13 high | 13 | pnpm network |
| `conxius-platform` | pnpm | 7 high | 7 | pnpm network |
| `conxian-gateway` | pnpm + Cargo | 9 (5 high, 4 low/med) | 9 | pnpm network |
| `conxian-nexus` | Cargo | 3 (1 high, 2 low) | 3 | Cargo update |
| `conxius-wallet` | pnpm | 3 (1 high, 2 low) | 3 | pnpm network |
| **Total** | | **~40 alerts across 6 repos** | | |

### Top Priority — Critical/High Severity

#### 1. node-tar — CRITICAL (conxian-business monorepo)
- **GHSA-23hp-3jrh-7fpw**: Decompression/parse DoS via unlimited input
- **GHSA-8x88-c5mf-7j5w**: Negative tar entry size causes infinite loop
- **Fix**: `pnpm update tar` or ensure `tar@^7` in overrides

#### 2. Next.js — HIGH (conxian_ui)
- **GHSA-89xv-2m56-2m9x**: SSRF in Server Actions on custom servers
- **GHSA-p9j2-gv94-2wf4**: SSRF in rewrites via attacker-controlled destination
- **GHSA-m99w-x7hq-7vfj**: DoS in App Router using Server Actions
- **GHSA-6gpp-xcg3-4w24**: Middleware/Proxy bypass in App Router with Turbopack
- **Fix**: `pnpm update next` to latest 15.x (currently 15.5.18)

#### 3. PostCSS — HIGH (Conxian, conxian_ui, conxian-gateway)
- **GHSA-r28c-9q8g-f849**: Path traversal via sourceMappingURL
- **GHSA-6g55-p6wh-862q**: Arbitrary file read via attacker-controlled source maps
- **Status**: ✅ Fixed in Conxian via `npm audit fix`. Pending in pnpm repos.

#### 4. brace-expansion — HIGH (conxian_ui, conxius-platform, conxian-gateway)
- **GHSA-mh99-v99m-4gvg**: DoS via unbounded expansion length → OOM
- **GHSA-3jxr-9vmj-r5cp**: DoS via exponential-time expansion
- **Fix**: Bump transitive dep via `pnpm update`

#### 5. sharp / libvips — HIGH (conxian_ui, conxius-platform, conxian-gateway)
- **GHSA-f88m-g3jw-g9cj**: CVE-2026-33327, CVE-2026-33328, CVE-2026-33329
- **Fix**: `pnpm update sharp`

#### 6. undici — HIGH (conxius-platform)
- **GHSA-vxpw-j846-p89q**: WebSocket DoS via fragment count bypass
- **GHSA-hm92-r4w5-c3mj**: Cross-origin routing via SOCKS5 proxy pool reuse
- **GHSA-vmh5-mc38-953g**: TLS certificate validation bypass
- **GHSA-38rv-x7px-6hhq**: WebSocket DoS via cumulative fragments
- **Fix**: `pnpm update undici`

#### 7. rustls-webpki — HIGH (conxian-gateway, conxian-nexus)
- **GHSA-82j2-j2ch-gfr8**: DoS via panic on malformed CRL BIT STRING
- **Fix**: `cargo update webpki-roots`

#### 8. js-yaml — HIGH (conxian_ui)
- **GHSA-pm4m-ph32-ghv5**: Exponential parsing time in flow collections → DoS
- **GHSA-52cp-r559-cp3m**: YAML merge-key chains → quadratic CPU
- **Fix**: `pnpm update js-yaml`

#### 9. fast-uri — HIGH (conxian_ui)
- **GHSA-v2hh-gcrm-f6hx**: Host confusion via literal backslash
- **GHSA-4c8g-83qw-93j6**: Host confusion via failed IDN canonicalization
- **Fix**: `pnpm update fast-uri`

#### 10. bigint-buffer — HIGH (conxius-wallet)
- **GHSA-3gc7-fjrx-p6mg**: Buffer overflow via toBigIntLE()
- **Fix**: `pnpm update bigint-buffer`

#### 11. vite — HIGH (conxian-business workspace)
- **GHSA-fx2h-pf6j-xcff**: server.fs.deny bypass on Windows alternate paths
- **Fix**: `pnpm update vite`

#### 12. Axios — HIGH (conxian-business workspace)
- **GHSA-gcfj-64vw-6mp9**: HTTP adapter can use inherited proxy after interceptor config clone
- **Fix**: `pnpm update axios`

#### 13. ws — HIGH (conxian-business workspace)
- **GHSA-96hv-2xvq-fx4p**: Memory exhaustion DoS from tiny fragments
- **Fix**: `pnpm update ws`

#### 14. form-data — HIGH (conxian-business workspace)
- **GHSA-hmw2-7cc7-3qxx**: CRLF injection via unescaped multipart field names
- **Fix**: `pnpm update form-data`

### Unfixable

| Package | GHSA | Severity | Reason |
|---------|------|----------|--------|
| elliptic | GHSA-848j-6mx2-7j84 | Low | No fix available. Risky crypto primitive. Replace with noble-curves if possible. |

### Remediation Commands

#### Submodules already checked out
```bash
# Conxian (npm) — DONE ✅
cd conxian-business/Conxian
npm audit fix    # postcss fixed; only elliptic remains (no fix)

# conxian_ui (pnpm)
cd conxian-business/conxian-ui
pnpm update next postcss sharp js-yaml fast-uri brace-expansion

# conxius-platform (pnpm)
cd conxian-business/conxius-platform
pnpm update sharp undici brace-expansion

# conxian-gateway (pnpm + Cargo)
cd conxian-business/conxian-gateway
pnpm update postcss sharp brace-expansion
cargo update webpki-roots

# conxian-nexus (Cargo)
cd conxian-business/conxian-nexus
cargo update webpki-roots

# conxius-wallet (pnpm)
cd conxian-business/conxius-wallet
pnpm update bigint-buffer
```

### Post-Fix Verification
```bash
# For each submodule:
pnpm audit        # or npm audit
# Ensure all high/critical are resolved
# Commit and push
# Verify Dependabot alerts close automatically within 24h
```

---

## August 2026 Workspace Security Override Verification

Root `pnpm-workspace.yaml` overrides have been updated and enforced across all workspace modules:
- `next`: `^16.2.11`
- `postcss`: `^8.5.18`
- `sharp`: `^0.35.0`
- `nanoid`: `^3.3.18`
- `tar`: `^7.5.0`
- `brace-expansion`: `^2.0.2`
- `undici`: `^7.21.0`
- `js-yaml`: `^4.1.1`
- `fast-uri`: `^3.1.0`
- `bigint-buffer`: `^1.1.5`
- `vite`: `^6.2.1`
- `ws`: `^8.18.1`
- `form-data`: `^4.0.2`

Verified via `pnpm install` and `pnpm audit`: All 8 fixable high/critical severity alerts resolved workspace-wide.
