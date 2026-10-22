#!/usr/bin/env python3
"""Verify pinned billing sources offline; never grant runtime/release authority."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "docs/billing-propagation-2026-10-16.json"
REPOS = {"sdk": "conxius-enclave-sdk", "core": "lib-conxian-core",
         "gateway": "conxian-gateway", "nexus": "conxian-nexus"}
SHA = re.compile(r"^[0-9a-f]{40}$")
SDK_RESOLUTION = {"core": True, "gateway": True, "nexus": False}


def validate_record(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = []
    if record.get("schema_version") != 1 or type(record.get("schema_version")) is not int:
        errors.append("unsupported record schema")
    if record.get("kind") != "billing-propagation":
        errors.append("wrong record kind")
    resolution = record.get("sdk_resolution")
    if (not isinstance(resolution, dict) or set(resolution) != set(SDK_RESOLUTION)
            or any(resolution[key] is not expected for key, expected in SDK_RESOLUTION.items())):
        errors.append("SDK resolution must distinguish opt-in Core/Gateway from disabled Nexus")
    for flag in ("production_accepted", "runtime_entitlement_implemented",
                 "new_prices_authorized", "projects_updated"):
        if record.get(flag) is not False:
            errors.append(f"{flag} must remain false")
    sources = record.get("sources")
    if not isinstance(sources, dict) or set(sources) != set(REPOS):
        return errors + ["exact SDK/Core/Gateway/Nexus source set required"]
    for key, repo in REPOS.items():
        source = sources[key]
        if not isinstance(source, dict):
            errors.append(f"{key}: invalid source")
            continue
        if source.get("repository") != f"Conxian/{repo}":
            errors.append(f"{key}: wrong repository")
        if not isinstance(source.get("commit"), str) or not SHA.fullmatch(source["commit"]):
            errors.append(f"{key}: immutable full SHA required")
    digest = record.get("catalog_sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append("catalog SHA-256 required")
    return errors


def git(directory: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(directory), *args], capture_output=True,
                            check=True, timeout=30)
    if len(result.stdout) > 2_000_000:
        raise ValueError("source exceeds size limit")
    return result.stdout.decode("utf-8")


def read_sources(record: dict, source_root: Path) -> dict[str, str]:
    files = {}
    paths = {"sdk": ["Cargo.toml"],
             "core": ["Cargo.toml", "Cargo.lock", "src/lib.rs", "spec/billing_conformance.v1.json"],
             "gateway": ["Cargo.toml", "Cargo.lock", "internal/engine/src/billing.rs"],
             "nexus": ["Cargo.toml", "Cargo.lock", "src/api/billing/mod.rs"]}
    for key, repo in REPOS.items():
        directory = source_root / repo
        source = record["sources"][key]
        if git(directory, "rev-parse", "HEAD").strip() != source["commit"]:
            raise ValueError(f"{key}: checkout HEAD does not match recorded commit")
        expected = f"https://github.com/Conxian/{repo}"
        if git(directory, "remote", "get-url", "origin").strip().removesuffix(".git") != expected:
            raise ValueError(f"{key}: checkout origin does not match repository")
        for path in paths[key]:
            files[f"{key}/{path}"] = git(directory, "show", f"{source['commit']}:{path}")
    return files


def validate_contents(record: dict, files: dict[str, str]) -> list[str]:
    """Check the actual pinned manifests/lockfiles and absence of local rates."""
    errors = validate_record(record)
    if errors:
        return errors
    try:
        # A catalog file and valid consumer pins are insufficient if the crate
        # no longer exports billing (the staged #466 regression).
        # This is a source declaration check, not a substitute for Cargo/CI.
        core_root = re.sub(r"/\*.*?\*/|//[^\n]*", "", files["core/src/lib.rs"], flags=re.S)
        if not re.search(r"^\s*pub\s+mod\s+billing\s*;\s*$", core_root, re.M):
            errors.append("core: public billing module declaration missing")
        catalog_text = files["core/spec/billing_conformance.v1.json"]
        catalog = json.loads(catalog_text)
        if hashlib.sha256(catalog_text.encode()).hexdigest() != record["catalog_sha256"]:
            errors.append("catalog digest mismatch")
        if (catalog["schema"] != "conxian.billing.catalog" or catalog["schema_version"] != 1
                or type(catalog["schema_version"]) is not int
                or catalog["policy_id"] != "legacy-billing-v1"
                or catalog["status"] != "configuration_only"
                or catalog["confers_entitlement"] is not False
                or catalog["cross_product_entitlement"] != "unavailable"):
            errors.append("unsupported catalog identity or authority")
        if catalog["gateway"]["unit"] != "usd_cents" or catalog["nexus"]["upgrade_unit"] != "satoshis":
            errors.append("billing units must remain separate")
        sdk_version = tomllib.loads(files["sdk/Cargo.toml"])["package"]["version"]
        core_manifest = tomllib.loads(files["core/Cargo.toml"])
        core_version = core_manifest["package"]["version"]
        sdk = core_manifest["dependencies"]["conxius-enclave-sdk"]
        sdk_sha = record["sources"]["sdk"]["commit"]
        if (sdk.get("git") != "https://github.com/Conxian/conxius-enclave-sdk"
                or sdk.get("rev") != sdk_sha or sdk.get("version") != sdk_version
                or sdk.get("default-features") is not False or sdk.get("optional") is not True
                or {"tag", "branch", "path"} & set(sdk)):
            errors.append("Core must pin the opt-in SDK to the recorded source/version")
        sdk_source = f"git+https://github.com/Conxian/conxius-enclave-sdk?rev={sdk_sha}#{sdk_sha}"
        core_sha = record["sources"]["core"]["commit"]
        core_source = f"git+https://github.com/Conxian/lib-conxian-core?rev={core_sha}#{core_sha}"
        for consumer in ("core", "gateway", "nexus"):
            packages = tomllib.loads(files[f"{consumer}/Cargo.lock"])["package"]
            sdk_packages = [p for p in packages if p["name"] == "conxius-enclave-sdk"]
            pinned_sdk = [p for p in sdk_packages
                          if p.get("source") == sdk_source and p["version"] == sdk_version]
            if SDK_RESOLUTION[consumer] and len(pinned_sdk) != 1:
                errors.append(f"{consumer}: exact SDK lock source/version missing")
            if not SDK_RESOLUTION[consumer] and sdk_packages:
                errors.append(f"{consumer}: optional SDK must remain unresolved")
            if consumer == "core":
                continue
            manifest = tomllib.loads(files[f"{consumer}/Cargo.toml"])
            deps = manifest["workspace"]["dependencies"] if consumer == "gateway" else manifest["dependencies"]
            core = deps["lib-conxian-core"]
            if (core.get("git") != "https://github.com/Conxian/lib-conxian-core"
                    or core.get("rev") != core_sha or {"tag", "branch", "path"} & set(core)):
                errors.append(f"{consumer}: Core declaration is not the recorded immutable pin")
            locked = [p for p in packages if p["name"] == "lib-conxian-core"]
            if len(locked) != 1 or locked[0].get("source") != core_source or locked[0]["version"] != core_version:
                errors.append(f"{consumer}: exact Core lock source/version missing")
        for consumer, path in (("gateway", "internal/engine/src/billing.rs"), ("nexus", "src/api/billing/mod.rs")):
            source = files[f"{consumer}/{path}"]
            if "lib_conxian_core::billing" not in source:
                errors.append(f"{consumer}: shared billing import missing")
            if re.search(r"(?:pub\s+)?const\s+(?:MANAGED_GATEWAY_BASE_FEE_CENTS|RELAY_MESSAGE_COST_CENTS|"
                         r"RWA_VERIFICATION_COST_CENTS|SETTLEMENT_OP_COST_CENTS|ENTERPRISE_DISCOUNT_BPS|"
                         r"ENTERPRISE_RELAY_THRESHOLD|BILLING_PERIOD_SECONDS|FREE_TIER_SIGNATURE_LIMIT|"
                         r"PRO_TIER_SIGNATURE_LIMIT|ENTERPRISE_TIER_SIGNATURE_LIMIT|PRO_UPGRADE_SATS|"
                         r"ENTERPRISE_UPGRADE_SATS|INVOICE_EXPIRY_SECONDS)\s*:", source):
                errors.append(f"{consumer}: duplicate billing definition")
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        errors.append(f"missing or malformed source contract: {type(exc).__name__}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, default=DEFAULT)
    parser.add_argument("--source-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text())
        errors = validate_record(record)
        if not errors:
            errors = validate_contents(record, read_sources(record, args.source_root))
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        errors = [f"source verification unavailable: {type(exc).__name__}"]
    if errors:
        print(json.dumps({"valid": False, "errors": errors, "runtime_or_release_authority": False}))
        return 1
    print(json.dumps({"valid": True, "catalog_and_dependency_pins": "matched",
                      "runtime_or_release_authority": False}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
