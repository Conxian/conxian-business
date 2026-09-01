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

Usage (from conxian-business root):

  AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="$AWS_SECRET_KEY" \
  python3 scripts/setup_conxian_signer.py

Exit code 0 on success. The generated access key is written to
``.conxian-sdk-signer.aws`` (chmod 600) in the repo root — do NOT commit it.
"""

from __future__ import annotations

import json
import os
import sys

USER_NAME = "conxian-sdk-signer"
POLICY_NAME = "conxian-sdk-signer-policy"

# Full Conxian SDK signing surface (derived from AGENTS.md AWS/Nitro notes).
POLICY_DOC = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2NitroLifecycle",
            "Effect": "Allow",
            "Action": [
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "ec2:CreateKeyPair",
                "ec2:CreateTags",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress",
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
                "iam:CreateRole",
                "iam:GetRole",
                "iam:CreateInstanceProfile",
                "iam:AddRoleToInstanceProfile",
                "iam:GetInstanceProfile",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "iam:PassRole",
                "iam:ListRoles",
                "iam:GetPolicy",
            ],
            "Resource": "*",
        },
        {
            "Sid": "KMSReleaseSigning",
            "Effect": "Allow",
            "Action": [
                "kms:CreateKey",
                "kms:CreateAlias",
                "kms:DescribeKey",
                "kms:ListAliases",
                "kms:GetPublicKey",
                "kms:Sign",
                "kms:Verify",
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:TagResource",
            ],
            "Resource": "*",
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
            "Resource": "arn:aws:iam::692112933743:user/conxian-sdk-signer",
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


def main() -> int:
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

    # 3. Programmatic access key.
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
