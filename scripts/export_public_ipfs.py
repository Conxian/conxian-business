#!/usr/bin/env python3
"""Create a reproducible CAR in isolated offline Kubo; never publish or update DNS."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

if __package__:
    from .build_public_artifact import ROOT, build
else:
    from build_public_artifact import ROOT, build


def export(output: Path, kubo: str) -> dict:
    executable = shutil.which(kubo)
    if not executable:
        raise ValueError("install an independently verified Kubo executable")
    output = output.absolute()
    if output.exists() or output.is_symlink() or output.resolve() != output:
        raise ValueError("export directory must be new and without symlink parents")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ipfs-export-", dir=output.parent) as temp:
        workspace = Path(temp)
        artifact = workspace / "release"
        artifact.mkdir()
        site = artifact / "site"
        evidence = build(ROOT, site)
        env = {"PATH": os.environ.get("PATH", ""), "IPFS_PATH": str(workspace / "kubo")}

        def run(*args: str) -> str:
            return subprocess.check_output([executable, "--offline", *args], env=env,
                                           stderr=subprocess.PIPE, timeout=120).decode().strip()

        version = run("version", "--number")
        # A new local repository prevents use of an operator's API/daemon,
        # pins, identity, credentials, bootstrap peers or existing datastore.
        run("init", "--profile=test")
        cid = run("add", "--recursive", "--quieter", "--cid-version=1", "--raw-leaves=true",
                  "--chunker=size-262144", "--hash=sha2-256", str(site))
        if not re.fullmatch(r"b[a-z2-7]{20,120}", cid):
            raise ValueError("expected one CIDv1 base32 directory root")
        car = artifact / "site.car"
        with car.open("wb") as handle:
            subprocess.run([executable, "--offline", "dag", "export", cid], env=env,
                           stdout=handle, stderr=subprocess.PIPE, timeout=120, check=True)
        receipt = {"schema_version": 1, "root_cid": cid, "kubo_version": version,
                   "car_sha256": hashlib.sha256(car.read_bytes()).hexdigest(),
                   "public_artifact": evidence, "network_publication": False,
                   "production_acceptance": False}
        (artifact / "release.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        artifact.rename(output)
        return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--kubo", default="ipfs", help="Path to verified Kubo executable")
    args = parser.parse_args()
    try:
        receipt = export(args.output, args.kubo)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Offline export rejected ({type(exc).__name__}).\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
