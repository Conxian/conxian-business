#!/usr/bin/env python3
"""Verify external release/signing state against the Conxian KB claims.

Cross-checks the Conxian knowledge base (AGENTS.md / release docs) against live
external systems, exercising every API the org relies on:

  * crates.io        — published crate versions + yanked names
  * GitHub           — tags, releases, and latest CI run per repo
  * AWS KMS / IAM    — Nitro release key + signing/encryption + IAM identity
  * Neon             — project inventory (id / region / Postgres version)

Required environment (secrets are auto-injected when referenced on the command
line):

  GITHUB_TOKEN         GitHub API token
  NEON_API_KEY         Neon console API token
  AWS_ACCESS_KEY_ID    AWS access key (source: AWS_ACCESS_KEY secret)
  AWS_SECRET_ACCESS_KEY AWS secret key (source: AWS_SECRET_KEY secret)

Usage (from conxian-business root):

  GITHUB_TOKEN="$GITHUB_TOKEN" NEON_API_KEY="$NEON_API_KEY" \
  AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY" \
  python3 scripts/verify_external_state.py

Exit code is non-zero when any verified claim fails.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

# ── Expected state (source of truth: release KB) ──────────────────────────────

# name -> (crate, expected published version, yanked-version names to confirm)
CRATES = {
    "conxius-enclave-sdk": ("conxius-enclave-sdk", "2.0.17"),
    "lib-conxian-core": ("lib-conxian-core", "0.3.3"),
    "lib-conclave-sdk": ("lib-conclave-sdk", None),   # yanked → max_version 0.0.0
    "anya-core": ("anya-core", None),                 # yanked → max_version 0.0.0
}

# repo -> expected latest tag + whether a release object must exist for it
GITHUB_REPOS = {
    "conxius-enclave-sdk": ("v2.0.17", True),
    "lib-conxian-core": ("v0.3.3", True),
}

AWS_ACCOUNT = "692112933743"
AWS_IAM_USER = "botshelo"
AWS_KMS_ALIAS = "alias/conxian-nitro-release"
AWS_KMS_REGION = "eu-central-1"

NEON_EXPECTED = {
    "Conxian Nexus": "orange-paper",
    "conxian-core": "sparkling-sunset",
    "Software dev kit": "weathered-night",
    "Gateway": "noisy-cloud",
    "Business Operating System": "noisy-flower",
    "market": "small-math",
}

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
_results: list[tuple[str, str, str]] = []


def record(status: str, label: str, detail: str = "") -> None:
    _results.append((status, label, detail))
    print(f"  [{status}] {label}" + (f" — {detail}" if detail else ""))


def _http_json(url: str, token: str | None = None, ua: str = "conxian-doc-audit") -> dict:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", ua)
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ── crates.io ─────────────────────────────────────────────────────────────────

def check_crates() -> None:
    print("\n== crates.io ==")
    for label, (crate, expected) in CRATES.items():
        url = f"https://crates.io/api/v1/crates/{crate}"
        try:
            data = _http_json(url)
        except Exception as exc:  # noqa: BLE001
            record(FAIL, f"{label}", f"crates.io API error: {exc}")
            continue
        max_ver = data.get("crate", {}).get("max_version")
        if expected is None:
            # Expected yanked: max_version collapses to 0.0.0
            if max_ver == "0.0.0":
                record(PASS, f"{label} yanked", "max_version 0.0.0")
            else:
                record(FAIL, f"{label} yanked", f"max_version={max_ver} (expected 0.0.0)")
        elif max_ver == expected:
            record(PASS, f"{label}@{expected}", "published")
        else:
            record(FAIL, f"{label}", f"published {max_ver}, expected {expected}")


# ── GitHub ────────────────────────────────────────────────────────────────────

def check_github() -> None:
    print("\n== GitHub ==")
    token = os.environ.get("GITHUB_TOKEN", "")
    for repo, (tag, need_release) in GITHUB_REPOS.items():
        base = f"https://api.github.com/repos/Conxian/{repo}"
        try:
            tags = _http_json(f"{base}/tags?per_page=20", token)
        except Exception as exc:  # noqa: BLE001
            record(FAIL, f"{repo} tags", f"API error: {exc}")
            continue
        tag_names = [t["name"] for t in tags]
        if tag in tag_names:
            record(PASS, f"{repo} tag {tag}", "present")
        else:
            record(FAIL, f"{repo} tag {tag}", f"missing; have {tag_names[:5]}")
        if need_release:
            try:
                rels = _http_json(f"{base}/releases?per_page=20", token)
            except Exception as exc:  # noqa: BLE001
                record(WARN, f"{repo} release {tag}", f"API error: {exc}")
                continue
            match = [r for r in rels if r["tag_name"] == tag and not r.get("draft")]
            if match:
                record(PASS, f"{repo} release {tag}", "published (non-draft)")
            else:
                record(FAIL, f"{repo} release {tag}", "missing or draft")
        # Latest CI run
        try:
            runs = _http_json(f"{base}/actions/runs?per_page=1", token)
        except Exception as exc:  # noqa: BLE001
            record(WARN, f"{repo} CI", f"API error: {exc}")
            continue
        wf = runs.get("workflow_runs", [])
        if wf:
            latest = wf[0]
            record(
                PASS if latest["conclusion"] == "success" else FAIL,
                f"{repo} latest CI",
                f"{latest['name']} → {latest['conclusion']} ({latest['head_branch']})",
            )
        else:
            record(WARN, f"{repo} CI", "no workflow runs")


# ── AWS KMS / IAM ─────────────────────────────────────────────────────────────

def check_aws() -> None:
    print("\n== AWS (KMS / IAM / EC2) ==")
    ak = os.environ.get("AWS_ACCESS_KEY_ID")
    sk = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not ak or not sk:
        record(WARN, "AWS", "AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY not set — skipping")
        return
    try:
        import boto3
    except ImportError:
        record(WARN, "AWS", "boto3 not installed — skipping")
        return

    # STS identity
    sts = boto3.client("sts", region_name="us-east-1",
                       aws_access_key_id=ak, aws_secret_access_key=sk)
    try:
        ident = sts.get_caller_identity()
    except Exception as exc:  # noqa: BLE001
        record(FAIL, "AWS STS", str(exc))
        return
    acct = ident["Account"]
    user = ident["Arn"].split("/")[-1]
    if acct == AWS_ACCOUNT:
        record(PASS, f"AWS account", acct)
    else:
        record(FAIL, f"AWS account", f"{acct} (expected {AWS_ACCOUNT})")
    if user == AWS_IAM_USER:
        record(PASS, f"IAM identity", user)
    else:
        record(WARN, f"IAM identity", f"{user} (expected {AWS_IAM_USER})")

    # KMS release key
    kms = boto3.client("kms", region_name=AWS_KMS_REGION,
                       aws_access_key_id=ak, aws_secret_access_key=sk)
    try:
        md = kms.describe_key(KeyId=AWS_KMS_ALIAS)["KeyMetadata"]
        record(
            PASS if md["KeyState"] == "Enabled" else FAIL,
            f"KMS {AWS_KMS_ALIAS}",
            f"{md['KeySpec']} / {md['KeyUsage']} / {md['KeyState']}",
        )
        # Encrypt (RSAES_OAEP_SHA_256) is the documented signing boundary.
        enc = kms.encrypt(KeyId=AWS_KMS_ALIAS, Plaintext=b"conxian-audit-probe",
                          EncryptionAlgorithm="RSAES_OAEP_SHA_256")
        record(PASS, "KMS encrypt", f"RSAES_OAEP_SHA_256 ok ({len(enc['CiphertextBlob'])} bytes)")
    except Exception as exc:  # noqa: BLE001
        record(FAIL, "KMS", str(exc)[:200])

    # EC2: describe is read-only; RunInstances DryRun proves authorization
    ec2 = boto3.client("ec2", region_name=AWS_KMS_REGION,
                       aws_access_key_id=ak, aws_secret_access_key=sk)
    try:
        ec2.describe_instances(MaxResults=5)
        record(PASS, "ec2:DescribeInstances", "authorized")
    except Exception as exc:  # noqa: BLE001
        record(WARN, "ec2:DescribeInstances", str(exc)[:150])
    try:
        # Real eu-central-1 Amazon Linux 2 AMI so DryRun reaches the authz result.
        ec2.run_instances(ImageId="ami-0c9354388bb36c088", InstanceType="t2.micro",
                          MinCount=1, MaxCount=1, DryRun=True)
    except Exception as exc:  # noqa: BLE001
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", "?")
        if code == "DryRunOperation":
            record(PASS, "ec2:RunInstances", "DryRunOperation → authorized")
        elif code in ("UnauthorizedOperation", "AccessDenied"):
            record(FAIL, "ec2:RunInstances", f"{code} → not authorized")
        else:
            record(WARN, "ec2:RunInstances", f"DryRun → {code}")


# ── Neon ──────────────────────────────────────────────────────────────────────

def check_neon() -> None:
    print("\n== Neon ==")
    token = os.environ.get("NEON_API_KEY", "")
    if not token:
        record(WARN, "Neon", "NEON_API_KEY not set — skipping")
        return
    try:
        data = _http_json("https://console.neon.tech/api/v2/projects", token)
    except Exception as exc:  # noqa: BLE001
        record(FAIL, "Neon projects", f"API error: {exc}")
        return
    projects = {p["name"]: p for p in data.get("projects", [])}
    for name, prefix in NEON_EXPECTED.items():
        p = projects.get(name)
        if not p:
            record(FAIL, f"Neon {name}", "missing")
            continue
        ok = p["id"].startswith(prefix)
        record(
            PASS if ok else FAIL,
            f"Neon {name}",
            f"{p['id']} · {p['region_id']} · pg{p.get('pg_version')}",
        )


def main() -> int:
    print(f"External state verification — {datetime.now(timezone.utc).isoformat()}")
    check_crates()
    check_github()
    check_aws()
    check_neon()

    fails = [r for r in _results if r[0] == FAIL]
    warns = [r for r in _results if r[0] == WARN]
    print(f"\nverify-external-state: {len(_results)} checks, "
          f"{len(fails)} fail, {len(warns)} warn")
    if fails:
        print("FAILURES:")
        for _, label, detail in fails:
            print(f"  - {label}: {detail}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
