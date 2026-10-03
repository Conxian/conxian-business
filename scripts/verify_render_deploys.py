#!/usr/bin/env python3
"""Verify Render deployments are healthy.

This is the detector that would have caught the conxius-platform outage: its Render
deploy sat in ``build_failed`` for two days while GitHub CI stayed green, and no one
was alerted. It lists every Render service and flags any whose latest deploy is
failed or whose service is suspended.

Required environment (secret auto-injected when referenced on the command line):
  RENDER_API_KEY   Render API token

Usage (from conxian-business root):
  RENDER_API_KEY="$RENDER_API_KEY" python3 scripts/verify_render_deploys.py

Exit code is non-zero when any deploy is failed/suspended.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

RENDER_API = "https://api.render.com/v1"
FAILED_STATUSES = {"build_failed", "update_failed", "canceled"}


def _http_json(url: str, token: str) -> list:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    token = os.environ.get("RENDER_API_KEY")
    if not token:
        print("RENDER_API_KEY not set — skipping Render deploy check.")
        return 0

    errors: list[str] = []
    try:
        services = _http_json(f"{RENDER_API}/services?limit=100", token)
    except Exception as exc:
        print(f"Render API error: {exc}")
        return 1

    for entry in services:
        svc = entry.get("service", {})
        name = svc.get("name") or svc.get("id")
        if svc.get("suspended") == "suspended":
            errors.append(f"{name}: suspended")
            continue
        try:
            deploys = _http_json(f"{RENDER_API}/services/{svc['id']}/deploys?limit=1", token)
        except Exception as exc:
            errors.append(f"{name}: cannot query deploys ({exc})")
            continue
        if not deploys:
            continue
        status = deploys[0].get("deploy", {}).get("status")
        if status in FAILED_STATUSES:
            errors.append(f"{name}: {status}")

    if errors:
        print("RENDER DEPLOY FAILURES:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Render deploys OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
