#!/usr/bin/env python3
"""Verify the production surface: DNS records and URL liveness.

Source of truth for the *host* layer is docs/DEPLOYMENT_TOPOLOGY.md; the
authoritative domain map is conxius-platform/platform/domain-service-map.json.
This script is the CI enforcement half: it flags DNS drift and dead URLs so an
outage can never again go silent for days.

Checks:
  1. DNS — Cloudflare records for each public domain match the expected target.
  2. Liveness — each production URL returns its expected HTTP status.
  3. Application readiness — mapped health JSON and BOS control identity.

Required environment:
  CLOUDFLARE_API_TOKEN   Cloudflare API token (read-only on the two zones)

Usage (from conxian-business root):
  CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" python3 scripts/verify_domain_topology.py

Exit code is non-zero when any check fails.
--http-only is an explicit partial diagnostic, never full topology evidence.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import os
import sys
import urllib.error
import urllib.request
import urllib.parse

# ── Expected state (source of truth: docs/DEPLOYMENT_TOPOLOGY.md) ─────────────

# domain -> (expected record type, expected content, zone name)
EXPECTED_DNS = {
    "conxian-labs.com": ("A", "76.76.21.21", "conxian-labs.com"),          # Vercel apex
    "www.conxian-labs.com": ("CNAME", "cname.vercel-dns.com", "conxian-labs.com"),  # Vercel www
    "control.conxian-labs.com": ("CNAME", "cname.vercel-dns.com", "conxian-labs.com"),
    "conxian.org": ("A", "76.76.21.21", "conxian.org"),                    # Vercel apex (org-site)
    "www.conxian.org": ("CNAME", "cname.vercel-dns.com", "conxian.org"),   # Vercel www
}

# url -> (expected status, description)
EXPECTED_URLS = {
    "https://www.conxian-labs.com": (200, "admin-dashboard (Vercel)"),
    "https://conxian-labs.com": (200, "admin-dashboard apex redirect"),
    "https://conxian.org": (200, "org-site (Vercel)"),
    "https://www.conxian.org": (200, "org-site www"),
    "https://control.conxian-labs.com": (200, "authenticated BOS control surface"),
}

# The retained Platform map explicitly requires this health contract. This does
# not settle its conflicting public-site ownership declarations or authorize DNS.
EXPECTED_HEALTH = {
    "https://www.conxian-labs.com/api/health": "mapped Platform persistence",
    "https://conxian-business-control-plane-zeta.vercel.app/api/health": "BOS auth/audit schema",
}
MAX_RESPONSE_BYTES = 512_000


class SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urllib.parse.urlsplit(req.full_url), urllib.parse.urlsplit(newurl)
        if (old.scheme, old.netloc) != (new.scheme, new.netloc):
            raise ValueError("cross-origin redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _surface(url: str, timeout: int = 10) -> tuple[int, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "conxian-domain-audit"})
    try:
        with urllib.request.build_opener(SameOriginRedirect).open(request, timeout=timeout) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise ValueError("surface response exceeds limit")
            return response.status, response.headers.get("Content-Type", ""), body.decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, "", ""


class PageTitle(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)

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


def check_urls(status_fetch=_status, surface_fetch=_surface) -> list[str]:
    errors: list[str] = []
    for url, (expected, label) in EXPECTED_URLS.items():
        code = status_fetch(url)
        if code != expected:
            errors.append(f"{url} ({label}): expected {expected}, got {code}")
    for url, label in EXPECTED_HEALTH.items():
        try:
            code, content_type, body = surface_fetch(url)
            if code != 200 or content_type.split(";")[0].strip().lower() != "application/json":
                raise ValueError("health response must be HTTP 200 JSON")
            payload = json.loads(body)
            if not isinstance(payload, dict) or payload.get("status") != "healthy":
                raise ValueError("health status is not healthy")
        except (OSError, ValueError, TypeError, UnicodeError):
            errors.append(f"{url} ({label}): application readiness not established")
    try:
        code, content_type, body = surface_fetch("https://control.conxian-labs.com")
        title = PageTitle()
        title.feed(body)
        if (code != 200 or not content_type.lower().startswith("text/html")
                or "Conxian BOS Control Plane" not in "".join(title.parts)):
            raise ValueError("control application identity mismatch")
    except (OSError, ValueError, TypeError, UnicodeError):
        errors.append("control.conxian-labs.com: BOS control application identity not established")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http-only", action="store_true", help="Diagnose HTTP only; does not establish DNS alignment")
    args = parser.parse_args(argv)
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CLOUDFLARE_API_KEY")
    errors: list[str] = []

    if args.http_only:
        print("HTTP-only diagnostic: DNS alignment not evaluated.")
    elif token:
        errors.extend(check_dns(token))
    else:
        errors.append("DNS evidence unavailable: CLOUDFLARE_API_TOKEN not set")

    errors.extend(check_urls())

    if errors:
        print("DOMAIN TOPOLOGY FAILURES:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("HTTP checks passed; DNS unverified." if args.http_only else "Domain topology OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
