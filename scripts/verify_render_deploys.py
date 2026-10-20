#!/usr/bin/env python3
"""Audit scoped Render deployment metadata; never grant runtime acceptance.

Requires RENDER_API_KEY and RENDER_OWNER_ID (or --owner-id). Missing access,
services, deployment records and non-live states fail closed. Pagination follows
https://api-docs.render.com/reference/pagination.
Use --expected-deployments with a release-specific manifest to bind service,
repository and full source SHA. Metadata alone never grants runtime acceptance.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

RENDER_API = "https://api.render.com/v1"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCOPE = ROOT / "docs/operations/render-monitor-scope.json"
PAGE_SIZE, MAX_PAGES, MAX_BYTES = 20, 25, 2_000_000
SERVICE_ID = re.compile(r"srv-[a-z0-9]+")
OWNER_ID = re.compile(r"(?:tea|usr)-[a-z0-9]+")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the provider token to a redirected host.


def _http_json(url: str, token: str) -> list:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                                 "Accept": "application/json"})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=25) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("provider response exceeds limit")
    result = json.loads(raw.decode("utf-8"))
    if not isinstance(result, list):
        raise ValueError("provider list response required")
    return result


def _failure(exc: Exception) -> str:
    # Do not print arbitrary exception text or provider bodies.
    return f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__


def list_services(owner_id: str, token: str, fetch=_http_json) -> list[dict]:
    result, seen_ids, seen_cursors = [], set(), set()
    query = {"ownerId": owner_id, "limit": PAGE_SIZE}
    for _ in range(MAX_PAGES):
        page = fetch(f"{RENDER_API}/services?{urllib.parse.urlencode(query)}", token)
        if not isinstance(page, list):
            raise ValueError("service list required")
        if not page:
            return result
        for entry in page:
            service = entry.get("service") if isinstance(entry, dict) else None
            if (not isinstance(service, dict) or not isinstance(service.get("id"), str)
                    or not SERVICE_ID.fullmatch(service["id"])
                    or service.get("ownerId") != owner_id or service["id"] in seen_ids):
                raise ValueError("invalid, duplicate or out-of-scope service")
            seen_ids.add(service["id"])
            result.append(service)
        cursor = page[-1].get("cursor")
        if not isinstance(cursor, str) or not cursor or cursor in seen_cursors:
            raise ValueError("missing or repeated service cursor")
        seen_cursors.add(cursor)
        query["cursor"] = cursor
    raise ValueError("service pagination exceeds limit")


def repository_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"https://github\.com/(Conxian/[A-Za-z0-9_.-]+?)(?:\.git)?/?", value)
    return match[1] if match else None


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate manifest key")
        result[key] = value
    return result


def load_expected_deployments(path: Path, required: list[str]) -> list[dict]:
    with path.open("rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("release manifest exceeds limit")
    manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    if (not isinstance(manifest, dict) or set(manifest) != {"schema_version", "deployments"}
            or type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1
            or not isinstance(manifest["deployments"], list) or not manifest["deployments"]):
        raise ValueError("invalid release manifest")
    seen, repos = set(), set()
    for entry in manifest["deployments"]:
        if (not isinstance(entry, dict) or set(entry) != {"service_id", "repository", "commit"}
                or not isinstance(entry["service_id"], str)
                or not SERVICE_ID.fullmatch(entry["service_id"])
                or entry["service_id"] in seen
                or not isinstance(entry["repository"], str)
                or repository_name(f'https://github.com/{entry["repository"]}') != entry["repository"]
                or not isinstance(entry["commit"], str)
                or not re.fullmatch(r"[0-9a-f]{40}", entry["commit"])):
            raise ValueError("invalid release deployment entry")
        seen.add(entry["service_id"])
        repos.add(entry["repository"])
    if not set(required).issubset(repos):
        raise ValueError("release manifest omits required repository")
    return manifest["deployments"]


def bind_expected_deployments(observations: list[dict], expected: list[dict]) -> list[str]:
    observed = {entry["service_id"]: entry for entry in observations}
    errors = []
    for entry in expected:
        actual = observed.get(entry["service_id"])
        if actual is None:
            errors.append(f'{entry["service_id"]}: expected service missing from scoped inventory')
        elif (actual["repository"] != entry["repository"]
              or actual["commit"] != entry["commit"]
              or actual["deployment_status"] != "live"):
            errors.append(f'{entry["service_id"]}: expected live repository/source binding not established')
    return errors


def audit_services(services: list[dict], required: list[str], token: str,
                   fetch=_http_json) -> tuple[list[dict], list[str]]:
    errors, observations = [], []
    if not services:
        errors.append("empty service inventory; deployment health is unknown")
    observed = {repository_name(service.get("repo")) for service in services}
    errors.extend(f"required repository has no Render service: {repo}"
                  for repo in required if repo not in observed)
    for service in services:
        service_id = service["id"]
        observation = {"service_id": service_id, "repository": repository_name(service.get("repo")),
                       "deployment_status": "unavailable", "commit": None}
        observations.append(observation)
        if service.get("suspended") != "not_suspended":
            errors.append(f"{service_id}: suspended or unknown suspension state")
        try:
            entries = fetch(f"{RENDER_API}/services/{service_id}/deploys?limit=1", token)
            if not isinstance(entries, list) or not entries:
                errors.append(f"{service_id}: no deployment evidence")
                continue
            deploy = entries[0].get("deploy") if isinstance(entries[0], dict) else None
            if not isinstance(deploy, dict):
                errors.append(f"{service_id}: malformed deployment evidence")
                continue
            status = deploy.get("status")
            observation["deployment_status"] = status if isinstance(status, str) else "unknown"
            commit = deploy.get("commit")
            sha = commit.get("id") if isinstance(commit, dict) else None
            if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha):
                observation["commit"] = sha
            elif observation["repository"] is not None:
                errors.append(f"{service_id}: immutable deployed source commit missing")
            if status != "live":
                errors.append(f"{service_id}: latest deployment is not live")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors.append(f"{service_id}: deployment lookup unavailable ({_failure(exc)})")
    return observations, errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-id", default=os.environ.get("RENDER_OWNER_ID"))
    parser.add_argument("--scope", type=Path, default=DEFAULT_SCOPE)
    parser.add_argument("--expected-deployments", type=Path,
                        help="Release manifest of exact service/repository/commit bindings")
    parser.add_argument("--summary-only", action="store_true",
                        help="Omit infrastructure observations from public CI logs")
    args = parser.parse_args(argv)
    token = os.environ.get("RENDER_API_KEY")
    errors, observations, expected = [], [], None
    source_binding_passed = False if args.expected_deployments is not None else None
    if not token:
        errors.append("RENDER_API_KEY missing; provider audit unavailable")
    if not isinstance(args.owner_id, str) or not OWNER_ID.fullmatch(args.owner_id):
        errors.append("explicit valid Render owner scope required")
    try:
        scope = json.loads(args.scope.read_text())
        required = scope["required_repositories"]
        if (scope.get("schema_version") != 1 or type(scope.get("schema_version")) is not int
                or not isinstance(required, list) or not required
                or any(not isinstance(r, str) or repository_name(f"https://github.com/{r}") != r for r in required)
                or len(required) != len(set(required))):
            raise ValueError("invalid required repository scope")
    except (OSError, ValueError, TypeError, KeyError):
        errors.append("required repository scope unavailable or malformed")
    if not errors and args.expected_deployments is not None:
        try:
            expected = load_expected_deployments(args.expected_deployments, required)
        except (OSError, ValueError, TypeError, KeyError):
            errors.append("expected deployment manifest unavailable or malformed")
    if not errors:
        try:
            services = list_services(args.owner_id, token)
            observations, errors = audit_services(services, required, token)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            errors = [f"scoped provider inventory unavailable ({_failure(exc)})"]
    metadata_passed = not errors
    if expected is not None:
        binding_errors = bind_expected_deployments(observations, expected)
        source_binding_passed = metadata_passed and not binding_errors
        errors.extend(binding_errors)
    output = {"metadata_checks_passed": metadata_passed,
              "expected_source_checks_passed": source_binding_passed,
              "runtime_or_release_authority": False}
    if args.summary_only:
        output["error_count"] = len(errors)
    else:
        output.update({"services": observations, "errors": errors})
    print(json.dumps(output))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
