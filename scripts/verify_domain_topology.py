#!/usr/bin/env python3
"""Verify the production surface: DNS records and URL liveness.

Source of truth for the *host* layer is docs/DEPLOYMENT_TOPOLOGY.md; the
authoritative domain map is conxius-platform/platform/domain-service-map.json.
This script is the CI enforcement half: it flags DNS drift and dead URLs so an
outage can never again go silent for days.

Checks:
  1. DNS — Cloudflare records for each public domain match the expected target.
  2. Liveness — each production URL returns its expected HTTP status.

Required environment (secrets auto-injected when referenced on the command line):
  CLOUDFLARE_API_TOKEN   Cloudflare API token (read-only on the two zones)

Usage (from conxian-business root):
  CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" python3 scripts/verify_domain_topology.py

Exit code is non-zero when any check fails.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

# ── Expected state (source of truth: docs/DEPLOYMENT_TOPOLOGY.md) ─────────────

# domain -> (expected record type, expected content, zone name)
EXPECTED_DNS = {
    "conxian-labs.com": ("A", "76.76.21.21", "conxian-labs.com"),          # Vercel apex
    "www.conxian-labs.com": ("CNAME", "cname.vercel-dns.com", "conxian-labs.com"),  # Vercel www
}

# url -> (expected status, description)
EXPECTED_URLS = {
    "https://www.conxian-labs.com": (200, "admin-dashboard (Vercel)"),
    "https://conxian-labs.com": (200, "admin-dashboard apex redirect"),
}

CF_API = "https://api.cloudflare.com/client/v4"


def _http_json(url: str, token: str | None = None, timeout: int = 25) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "conxian-domain-audit"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _status(url: str, timeout: int = 30) -> int:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "conxian-domain-audit"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return 0


def check_dns(token: str) -> list[str]:
    errors: list[str] = []
    for domain, (rtype, content, zone_name) in EXPECTED_DNS.items():
        try:
            zones = _http_json(f"{CF_API}/zones?name={zone_name}", token).get("result", [])
        except Exception as exc:
            errors.append(f"{domain}: cannot query zone ({exc})")
            continue
        if not zones:
            errors.append(f"{domain}: no Cloudflare zone found for {zone_name}")
            continue
        zone_id = zones[0]["id"]
        try:
            records = _http_json(
                f"{CF_API}/zones/{zone_id}/dns_records?name={domain}&per_page=50", token
            ).get("result", [])
        except Exception as exc:
            errors.append(f"{domain}: cannot query DNS ({exc})")
            continue
        match = [r for r in records if r.get("type") == rtype and r.get("name") == domain]
        if not any(m.get("content") == content for m in match):
            got = [m.get("content") for m in match]
            errors.append(f"{domain}: expected {rtype} {content}, got {got}")
    return errors


def check_urls() -> list[str]:
    errors: list[str] = []
    for url, (expected, label) in EXPECTED_URLS.items():
        code = _status(url)
        if code != expected:
            errors.append(f"{url} ({label}): expected {expected}, got {code}")
    return errors


def main() -> int:
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CLOUDFLARE_API_KEY")
    errors: list[str] = []

    if token:
        errors.extend(check_dns(token))
    else:
        print("CLOUDFLARE_API_TOKEN not set — skipping DNS check (liveness only).")

    errors.extend(check_urls())

    if errors:
        print("DOMAIN TOPOLOGY FAILURES:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Domain topology OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
