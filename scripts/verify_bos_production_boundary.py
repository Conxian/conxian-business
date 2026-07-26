#!/usr/bin/env python3

"""Verify BOS production boundaries by scanning tracked files for forbidden paths."""

from __future__ import annotations

import os
import re
import subprocess
import sys

BOUNDARY_VALIDATOR_PATH = "scripts/verify_bos_production_boundary.py"


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def is_in_dir(rel_path: str, rel_dir: str) -> bool:
    rel_dir = rel_dir.rstrip("/")
    if not rel_dir:
        return False
    return rel_path == rel_dir or rel_path.startswith(rel_dir + "/")


def normalize_rel_path(rel_path: str) -> str:
    rel_path = rel_path.replace(os.sep, "/").replace("\\", "/")
    while rel_path.startswith("./"):
        rel_path = rel_path[2:]
    return rel_path


def is_boundary_validator(rel_path: str) -> bool:
    return normalize_rel_path(rel_path) == BOUNDARY_VALIDATOR_PATH


def git_index_entries(root: str) -> list[tuple[str, str]]:
    try:
        out = subprocess.check_output(
            ["git", "-C", root, "ls-files", "--stage", "-z"],
            stderr=subprocess.STDOUT,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(
            f"Failed to enumerate tracked files via git in {root}: {exc}"
        ) from exc

    entries: list[tuple[str, str]] = []
    for raw_entry in (entry for entry in out.split(b"\x00") if entry):
        metadata, separator, raw_path = raw_entry.partition(b"\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            raise RuntimeError("Failed to parse tracked Git index entries")
        mode = os.fsdecode(fields[0])
        entries.append((mode, os.fsdecode(raw_path)))
    return entries


def read_text(root: str, rel_path: str) -> str:
    full_path = os.path.join(root, rel_path)
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main() -> int:
    root = repo_root()
    this_script_rel = normalize_rel_path(
        os.path.relpath(os.path.abspath(__file__), root)
    )
    try:
        index_entries = git_index_entries(root)
        submodules = {path for mode, path in index_entries if mode == "160000"}
        excluded_dirs = {".idx"} | submodules
        excluded_paths = {p.rstrip("/") for p in excluded_dirs if p.rstrip("/")}
        repo_files = [
            path
            for _, path in index_entries
            if path not in submodules
            and not any(is_in_dir(path, ex) for ex in excluded_paths)
        ]
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    errors: list[str] = []

    # 1) Stub artifacts must be isolated.
    stub_files = [p for p in repo_files if p.endswith(".stub.json")]
    for stub_file in stub_files:
        if not is_in_dir(stub_file, "conxian-business"):
            errors.append(
                f"Stub artifact must be isolated under conxian-business/: {stub_file}"
            )

    # 2) Generated BOS audit outputs must never be committed.
    generated_files = [
        p for p in repo_files if is_in_dir(p, "conxian-business/.generated")
    ]
    if generated_files:
        errors.append(
            "Committed generated artifacts detected under conxian-business/.generated/: "
            + ", ".join(sorted(generated_files))
        )

    # 3) CI/runtime code must not depend on stub artifacts or local-only outputs.
    forbidden_substrings = [".stub.json", "conxian-business/.generated/"]
    code_exts = {".py", ".ts", ".js", ".mjs", ".cjs", ".sh", ".yml", ".yaml"}
    for rel_path in repo_files:
        if not os.path.isfile(os.path.join(root, rel_path)):
            continue
        _, ext = os.path.splitext(rel_path)
        if ext not in code_exts:
            continue
        if is_in_dir(rel_path, "docs") or is_in_dir(rel_path, "openspec"):
            continue
        text = read_text(root, rel_path)
        for needle in forbidden_substrings:
            # The boundary validator must name the stub suffix to enforce this policy,
            # but it should still be checked for every other forbidden reference.
            if needle == ".stub.json" and is_boundary_validator(rel_path):
                continue
            if needle == "conxian-business/.generated/" and rel_path == this_script_rel:
                continue
            if needle in text:
                errors.append(
                    f"Production/CI code must not reference {needle}: {rel_path}"
                )

    # 4) Avoid hard-coded testnet defaults in operational scripts.
    testnet_network_literal = re.compile(
        r"(?:networkFromName\(\s*['\"]testnet['\"]\s*\)|new\s+StacksTestnet\s*\()"
    )
    # Matches testnet principals like "ST..." or "ST....contract-name" (case-insensitive).
    testnet_principal_literal = re.compile(
        r"['\"](?:ST|SN)[0-9A-Z]{20,}(?:\.[a-zA-Z0-9-]{1,128})?['\"]",
        re.IGNORECASE,
    )
    for rel_path in repo_files:
        if not re.fullmatch(r"scripts/[^/]+\.ts", rel_path):
            continue

        if not os.path.isfile(os.path.join(root, rel_path)):
            continue

        text = read_text(root, rel_path)
        if testnet_network_literal.search(text):
            errors.append(
                f"Operational scripts must not hard-code testnet as the active network: {rel_path}"
            )
        if testnet_principal_literal.search(text):
            errors.append(
                f"Operational scripts must not embed testnet principals (require explicit flags): {rel_path}"
            )

    if errors:
        print("BOS production boundary violations found:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("BOS production boundary checks: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
