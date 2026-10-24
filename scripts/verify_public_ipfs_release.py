#!/usr/bin/env python3
"""Independently restore a pinned public CAR and compare it with pinned source."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

if __package__:
    from .build_public_artifact import ROOT, MANIFEST, build
else:
    from build_public_artifact import ROOT, MANIFEST, build

MAX_CAR_BYTES = 32 * 1024 * 1024


def verify(car: Path, source_sha: str, expected_cid: str, expected_car_sha256: str, kubo: str) -> dict:
    if (not re.fullmatch(r"[0-9a-f]{40}", source_sha)
            or not re.fullmatch(r"b[a-z2-7]{20,120}", expected_cid)
            or not re.fullmatch(r"[0-9a-f]{64}", expected_car_sha256)):
        raise ValueError("full source, CID and CAR digest pins are required")
    executable = shutil.which(kubo)
    if not executable:
        raise ValueError("verified Kubo executable required")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, timeout=10).decode().strip()
    if head != source_sha:
        raise ValueError("checkout does not match the requested source")
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--", MANIFEST, "public-docs"],
                   cwd=ROOT, timeout=10, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    manifest = json.loads((ROOT / MANIFEST).read_text())
    sources = [MANIFEST, *(item["source"] for item in manifest["files"])]
    subprocess.run(["git", "ls-files", "--error-unmatch", "--", *sources], cwd=ROOT,
                   timeout=10, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with tempfile.TemporaryDirectory(prefix="conxian-ipfs-verify-") as temp:
        root = Path(temp)
        expected = root / "expected"
        evidence = build(ROOT, expected)
        # Work from a bounded private copy. Never trust the archive's receipt,
        # adjacent site directory or an operator's existing Kubo datastore.
        pinned_car = root / "pinned.car"
        fd = os.open(car, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as source:
            info = os.fstat(source.fileno())
            if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_CAR_BYTES:
                raise ValueError("bounded regular CAR file required")
            data = source.read(MAX_CAR_BYTES + 1)
        if len(data) > MAX_CAR_BYTES or hashlib.sha256(data).hexdigest() != expected_car_sha256:
            raise ValueError("CAR digest mismatch")
        pinned_car.write_bytes(data)
        env = {"PATH": os.environ.get("PATH", ""), "IPFS_PATH": str(root / "fresh-kubo")}

        def run(*args: str) -> str:
            return subprocess.check_output([executable, "--offline", *args], env=env,
                                           timeout=120, stderr=subprocess.PIPE).decode().strip()

        version = run("version", "--number")
        run("init", "--profile=test")
        run("dag", "import", str(pinned_car))
        restored = root / "restored"
        run("get", expected_cid, "--output", str(restored))

        def files(directory: Path) -> dict:
            if not directory.is_dir() or directory.is_symlink():
                raise ValueError("expected a restored directory")
            result = {}
            for path in directory.rglob("*"):
                if path.is_symlink() or not (path.is_dir() or path.is_file()):
                    raise ValueError("unexpected restored entry")
                if path.is_file():
                    result[path.relative_to(directory).as_posix()] = path.read_bytes()
            return result

        if files(expected) != files(restored):
            raise ValueError("restored content does not match the pinned public source")
        return {"schema_version": 1, "source_sha": source_sha, "root_cid": expected_cid,
                "car_sha256": expected_car_sha256, "kubo_version": version,
                "public_files_verified": len(evidence["files"]), "offline_restoration_verified": True,
                "live_replication_verified": False, "operator_independence_verified": False,
                "production_acceptance": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("car", type=Path)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--expected-cid", required=True)
    parser.add_argument("--expected-car-sha256", required=True)
    parser.add_argument("--kubo", default="ipfs")
    args = parser.parse_args()
    try:
        result = verify(args.car, args.source_sha, args.expected_cid, args.expected_car_sha256, args.kubo)
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Independent restoration rejected ({type(exc).__name__}).\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
