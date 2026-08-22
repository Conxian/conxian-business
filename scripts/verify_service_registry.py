#!/usr/bin/env python3
"""Validate the BOS service registry without making network calls."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ops" / "service-registry.json"
SUBMODULES = ROOT / ".gitmodules"
REQUIRED = {"id", "repository", "role", "deployment", "hostname", "healthPath", "readinessPath", "auth", "safeTestMode"}
HOST_RE = re.compile(r"^[a-z0-9.-]+\.[a-z]{2,}$")

def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        gitmodules = SUBMODULES.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"service registry unreadable: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    services = data.get("services") if isinstance(data, dict) else None
    if data.get("schemaVersion") != "bos.service-registry.v1": errors.append("unsupported schema version")
    if not isinstance(services, list) or not services: errors.append("services must be non-empty")
    else:
        ids: set[str] = set(); repos: set[str] = set()
        for i, service in enumerate(services):
            missing = REQUIRED - service.keys() if isinstance(service, dict) else REQUIRED
            if missing: errors.append(f"services[{i}] missing {sorted(missing)}")
            if not isinstance(service, dict): continue
            sid = service.get("id")
            if sid in ids: errors.append(f"duplicate service id: {sid}")
            ids.add(sid)
            repos.add(service.get("repository", ""))
            host = service.get("hostname")
            if host is not None and not HOST_RE.match(host): errors.append(f"invalid hostname for {sid}: {host}")
            for key in ("healthPath", "readinessPath"):
                path = service.get(key)
                if path is not None and (not isinstance(path, str) or not path.startswith("/")):
                    errors.append(f"{sid}.{key} must be an absolute path or null")
            if service.get("role") != "public-web" and service.get("safeTestMode") is not True:
                errors.append(f"{sid}.safeTestMode must be true until independently certified")
    declared = set(re.findall(r'^\[submodule "([^"]+)"\]', gitmodules, re.MULTILINE))
    expected = {s.get("repository") for s in services or [] if isinstance(s, dict) and s.get("repository") not in {"conxian-business"}}
    missing = sorted(expected - declared)
    if missing: errors.append(f"registry repositories missing from .gitmodules: {missing}")
    if errors:
        print("service registry violations:\n- " + "\n- ".join(errors))
        return 1
    print(f"service registry: OK ({len(services)} services)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
