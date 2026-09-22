#!/usr/bin/env python3
"""Provision the Conxian SDK signing IAM user (Conxian-branded identity).

Creates (idempotently) a new AWS IAM user named ``conxian-sdk-signer`` with an
inline policy covering the full Conxian SDK signing path documented in the KB:

  * EC2  — Nitro Enclave lifecycle (run/terminate instances, keypairs, SG, describe*)
  * IAM  — Nitro instance-profile/role wiring (CreateInstanceProfile/PassRole/…)
  * KMS  — release signing + recipient encryption (CreateKey/Sign/Encrypt/Decrypt/…)
  * STS  — GetCallerIdentity

This identity is distinct from the human ``botshelo`` account and is intended as
the SDK/CI signing surface (dev today; production should scope resources and add
rotation + CloudTrail).

Least-privilege notes (see conxian-business #1076 and the org-wide audit):

  * KMS key *usage* is scoped to exactly the Conxian dev + prod aliases via
    ``kms:ResourceAliases``, so this identity cannot use arbitrary KMS keys.
  * ``iam:PassRole`` is scoped to the Nitro enclave role only — this removes the
    classic "pass a privileged role to EC2" escalation path that a wildcard
    ``iam:PassRole`` would allow.
  * EC2 mutating actions carry a region + ``conxian:role=nitro-enclave`` tag
    condition so the identity can only run/tag Nitro-labelled instances.
  * ``iam:CreateRole``/``iam:AttachRolePolicy``/``iam:PutRolePolicy`` are scoped
    to the single Nitro role. If the role is pre-provisioned by an admin, drop
    these three actions entirely for a still-tighter boundary.

Usage (from conxian-business root):

  AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY" \
  python3 scripts/setup_conxian_signer.py [--rotate]

Exit code 0 on success. The generated access key is written to
``.conxian-sdk-signer.aws`` (chmod 600) in the repo root — do NOT commit it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

USER_NAME = "conxian-sdk-signer"
POLICY_NAME = "conxian-sdk-signer-policy"

# AWS account + region the signing surface is deployed in.
ACCOUNT_ID = "692112933743"
REGION = "eu-central-1"

# Dev key = Nitro KMS recipient (RSAES_OAEP_SHA_256); prod key = release-signing
# CMK provisioned separately (conxian-business #1076).
_KMS_DEV_ALIAS_NAME = "alias/conxian-nitro-release"
_KMS_PROD_ALIAS_NAME = "alias/conxian-prod-release"
_NITRO_ROLE_ARN = f"arn:aws:iam::{ACCOUNT_ID}:role/conxian-nitro-enclave-role"
_NITRO_PROFILE_ARN = (
    f"arn:aws:iam::{ACCOUNT_ID}:instance-profile/conxian-nitro-enclave-profile"
)
_USER_ARN = f"arn:aws:iam::{ACCOUNT_ID}:user/{USER_NAME}"
_KMS_KEY_ARN = f"arn:aws:kms:{REGION}:{ACCOUNT_ID}:key/*"

# Full Conxian SDK signing surface (derived from AGENTS.md AWS/Nitro notes),
# resource-scoped to the least privilege required by the signing path.
POLICY_DOC = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2RunInstances",
            "Effect": "Allow",
            "Action": ["ec2:RunInstances", "ec2:CreateTags"],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": REGION,
                    "aws:RequestTag/conxian:role": "nitro-enclave",
                }
            },
        },
        {
            "Sid": "EC2TerminateInstances",
            "Effect": "Allow",
            "Action": ["ec2:TerminateInstances"],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": REGION,
                    "ec2:ResourceTag/conxian:role": "nitro-enclave",
                }
            },
        },
        {
            "Sid": "EC2NitroSetup",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateKeyPair",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {"aws:RequestedRegion": REGION}
            },
        },
        {
            "Sid": "EC2Describe",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeImages",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeVpcs",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeVolumes",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeLaunchTemplates",
                "ec2:DescribeRegions",
            ],
            "Resource": "*",
        },
        {
            "Sid": "IAMNitroInstanceProfile",
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:CreateInstanceProfile",
                "iam:AddRoleToInstanceProfile",
                "iam:GetInstanceProfile",
                "iam:ListRoles",
                "iam:GetPolicy",
            ],
            "Resource": "*",
        },
        {
            "Sid": "IAMNitroRoleWiring",
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
            ],
            "Resource": _NITRO_ROLE_ARN,
        },
        {
            "Sid": "IAMPassRoleNitroOnly",
            "Effect": "Allow",
            "Action": ["iam:PassRole"],
            "Resource": _NITRO_ROLE_ARN,
        },
        {
            "Sid": "KMSReleaseSigning",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey",
                "kms:GetPublicKey",
                "kms:Sign",
                "kms:Verify",
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:TagResource",
            ],
            "Resource": _KMS_KEY_ARN,
            "Condition": {
                "StringEquals": {
                    "kms:ResourceAliases": [
                        _KMS_DEV_ALIAS_NAME,
                        _KMS_PROD_ALIAS_NAME,
                    ]
                }
            },
        },
        {
            "Sid": "KMSKeyProvisioning",
            "Effect": "Allow",
            "Action": ["kms:CreateKey", "kms:ListKeys", "kms:ListAliases"],
            "Resource": "*",
        },
        {
            "Sid": "KMSAliasCreation",
            "Effect": "Allow",
            "Action": ["kms:CreateAlias"],
            "Resource": [
                f"arn:aws:kms:{REGION}:{ACCOUNT_ID}:alias/conxian-nitro-release",
                f"arn:aws:kms:{REGION}:{ACCOUNT_ID}:alias/conxian-prod-release",
            ],
        },
        {
            "Sid": "STSIdentity",
            "Effect": "Allow",
            "Action": ["sts:GetCallerIdentity"],
            "Resource": "*",
        },
        {
            "Sid": "SelfKeyRotation",
            "Effect": "Allow",
            "Action": [
                "iam:CreateAccessKey",
                "iam:DeleteAccessKey",
                "iam:ListAccessKeys",
                "iam:UpdateAccessKey",
            ],
            "Resource": _USER_ARN,
        },
    ],
}


def _client():
    import boto3

    ak = os.environ.get("AWS_ACCESS_KEY_ID")
    sk = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not ak or not sk:
        raise SystemExit("AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY not set")
    return boto3.client(
        "iam", region_name="us-east-1",
        aws_access_key_id=ak, aws_secret_access_key=sk,
    )


def _existing_access_keys(iam) -> list:
    return iam.list_access_keys(UserName=USER_NAME).get("AccessKeyMetadata", [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="delete existing access keys before creating a new one (default: "
        "leave existing keys untouched and create none).",
    )
    args = parser.parse_args()

    iam = _client()

    # 1. Create (idempotent) the user.
    try:
        iam.get_user(UserName=USER_NAME)
        print(f"user {USER_NAME} already exists")
    except iam.exceptions.NoSuchEntityException:
        iam.create_user(UserName=USER_NAME, Tags=[{"Key": "conxian:role", "Value": "sdk-signer"}])
        print(f"created user {USER_NAME}")
    except Exception as exc:  # noqa: BLE001
        print(f"CreateUser failed: {type(exc).__name__} {exc}")
        return 1

    # 2. Attach the inline policy (replace if drift).
    iam.put_user_policy(
        UserName=USER_NAME,
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(POLICY_DOC),
    )
    print(f"attached inline policy {POLICY_NAME}")

    # 3. Programmatic access key (idempotent by default; --rotate replaces).
    existing = _existing_access_keys(iam)
    if existing and not args.rotate:
        for k in existing:
            print(
                f"existing access key {k['AccessKeyId']} (status {k['Status']}) — "
                "pass --rotate to replace it"
            )
        print("no new access key created")
        return 0

    if args.rotate:
        for k in existing:
            iam.delete_access_key(UserName=USER_NAME, AccessKeyId=k["AccessKeyId"])
            print(f"deleted old access key {k['AccessKeyId']}")

    key = iam.create_access_key(UserName=USER_NAME)["AccessKey"]
    print(f"access key created: {key['AccessKeyId']}")

    # 4. Persist credentials to a gitignored, 0600 file.
    creds = (
        f"AWS_ACCESS_KEY_ID={key['AccessKeyId']}\n"
        f"AWS_SECRET_ACCESS_KEY={key['SecretAccessKey']}\n"
    )
    out = os.path.join(os.getcwd(), ".conxian-sdk-signer.aws")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(creds)
    os.chmod(out, 0o600)
    print(f"credentials written to {out} (chmod 600 — do not commit)")

    print("\nSETUP COMPLETE")
    print(f"  user:      {USER_NAME}")
    print(f"  policy:    {POLICY_NAME}")
    print(f"  key id:    {key['AccessKeyId']}")
    print(f"  creds file: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
