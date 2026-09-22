#!/usr/bin/env python3
"""Provision the production KMS release-signing key (conxian-business #1076).

Creates (idempotently) an **asymmetric** `SIGN_VERIFY` KMS key, aliases it
``alias/conxian-prod-release``, and attaches a key policy that grants the scoped
``conxian-sdk-signer`` identity ``kms:Sign``/``kms:Verify``/``kms:GetPublicKey``/
``kms:DescribeKey``, plus the account root ``kms:*`` for administration/recovery.

This is the production companion to the dev Nitro recipient key
(``alias/conxian-nitro-release``, ``RSAES_OAEP_SHA_256``). Because a single KMS
key cannot be both ``SIGN_VERIFY`` and ``ENCRYPT_DECRYPT``, this key is
sign/verify only; recipient encryption stays on the dev key. The #1076 body's
``Encrypt``/``Decrypt`` grant is therefore intentionally NOT applied here.

Dry-run by default (prints the plan + effective key policy, creates nothing).
Pass ``--apply`` to actually create the key and alias.

Usage (from conxian-business root):

  AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY" \
  python3 scripts/provision_prod_kms.py            # dry-run (default)
  python3 scripts/provision_prod_kms.py --apply    # create key + alias

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys

ACCOUNT_ID = "692112933743"
REGION = "eu-central-1"
ALIAS_NAME = "alias/conxian-prod-release"
SIGNER_ARN = f"arn:aws:iam::{ACCOUNT_ID}:user/conxian-sdk-signer"
POLICY_PATH = os.path.join(os.path.dirname(__file__), "conxian-prod-release-key-policy.json")

KEY_SPEC = "ECC_NIST_P384"
KEY_USAGE = "SIGN_VERIFY"

# Signing algorithms accepted per key spec (defaults to the strongest supported).
_SIGNING_ALGORITHMS = {
    "ECC_NIST_P256": ["ECDSA_SHA_256"],
    "ECC_NIST_P384": ["ECDSA_SHA_384"],
    "ECC_NIST_P521": ["ECDSA_SHA_512"],
    "ECC_SECG_P256K1": ["ECDSA_SHA_256"],
    "RSA_2048": ["RSASSA_PSS_SHA_256"],
    "RSA_3072": ["RSASSA_PSS_SHA_256"],
    "RSA_4096": ["RSASSA_PSS_SHA_256"],
}


def _load_policy() -> dict:
    with open(POLICY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _validate_policy(policy: dict) -> None:
    principals = []
    for statement in policy.get("Statement", []):
        principals.append(statement.get("Principal", {}).get("AWS"))
    # The policy must grant the account root (recovery) and the signer.
    assert f"arn:aws:iam::{ACCOUNT_ID}:root" in principals, "policy missing account root principal"
    assert SIGNER_ARN in principals, "policy missing signer principal"


def _client(region: str):
    import boto3

    ak = os.environ.get("AWS_ACCESS_KEY_ID")
    sk = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not ak or not sk:
        raise SystemExit("AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY not set")
    return boto3.client(
        "kms", region_name=region,
        aws_access_key_id=ak, aws_secret_access_key=sk,
    )


def _existing_alias(kms) -> dict | None:
    try:
        return kms.describe_key(KeyId=ALIAS_NAME)["KeyMetadata"]
    except kms.exceptions.NotFoundException:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="actually create the key + alias (default: dry-run)")
    parser.add_argument("--key-spec", default=KEY_SPEC,
                        help=f"KMS key spec (default: {KEY_SPEC})")
    parser.add_argument("--region", default=REGION, help=f"AWS region (default: {REGION})")
    parser.add_argument("--policy-file", default=POLICY_PATH,
                        help="path to the key policy JSON")
    args = parser.parse_args()

    if args.key_spec not in _SIGNING_ALGORITHMS:
        raise SystemExit(f"unsupported --key-spec {args.key_spec!r}; "
                         f"choose from {sorted(_SIGNING_ALGORITHMS)}")

    policy = _load_policy()
    _validate_policy(policy)

    signing_algorithms = _SIGNING_ALGORITHMS[args.key_spec]
    plan = {
        "description": "Conxian production release-signing key",
        "key_spec": args.key_spec,
        "key_usage": KEY_USAGE,
        "signing_algorithms": signing_algorithms,
        "alias": ALIAS_NAME,
        "region": args.region,
        "policy": policy,
    }

    if not args.apply:
        print("DRY RUN — no AWS resources will be created. Pass --apply to create.\n")
        print("Plan:")
        print(f"  description:        {plan['description']}")
        print(f"  key spec:           {plan['key_spec']}")
        print(f"  key usage:          {plan['key_usage']}")
        print(f"  signing algorithms: {', '.join(plan['signing_algorithms'])}")
        print(f"  alias:              {plan['alias']}")
        print(f"  region:             {plan['region']}")
        print("\nEffective key policy:")
        print(json.dumps(plan["policy"], indent=2))
        return 0

    # --apply: create the key, alias it, and emit the public key.
    kms = _client(args.region)

    existing = _existing_alias(kms)
    if existing is not None:
        print(f"alias {ALIAS_NAME} already exists:")
        print(f"  key id:     {existing['KeyId']}")
        print(f"  key spec:   {existing['KeySpec']}")
        print(f"  key usage:  {existing['KeyUsage']}")
        print(f"  key state:  {existing['KeyState']}")
        print("no changes made")
        return 0

    created = kms.create_key(
        Description=plan["description"],
        KeySpec=plan["key_spec"],
        KeyUsage=plan["key_usage"],
        SigningAlgorithms=plan["signing_algorithms"],
        Policy=json.dumps(plan["policy"]),
        Tags=[{"TagKey": "conxian:role", "TagValue": "release-signing"}],
    )
    key_id = created["KeyMetadata"]["KeyId"]
    arn = created["KeyMetadata"]["Arn"]
    print(f"created key {key_id} ({arn})")

    kms.create_alias(AliasName=ALIAS_NAME, TargetKeyId=key_id)
    print(f"aliased {ALIAS_NAME} -> {key_id}")

    public_key = kms.get_public_key(KeyId=key_id)
    pub_b64 = base64.b64encode(public_key["PublicKey"]).decode()
    print("\nPROVISION COMPLETE")
    print(f"  key arn:    {arn}")
    print(f"  alias:      {ALIAS_NAME}")
    print(f"  key spec:   {plan['key_spec']}")
    print(f"  usage:      {plan['key_usage']}")
    print(f"  signing:    {', '.join(plan['signing_algorithms'])}")
    print(f"  public key (base64 DER):")
    print(f"    {pub_b64}")
    print("\n  NOTE: asymmetric KMS keys do NOT support automatic rotation.")
    print("        Rotate manually by creating a new key + updating the alias.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
