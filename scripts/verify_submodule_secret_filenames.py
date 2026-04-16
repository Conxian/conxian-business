from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"Failed to determine repo root via git: {exc}") from exc
    return Path(out.strip())


def _read_submodule_paths(repo_root: Path) -> list[str]:
    gitmodules = repo_root / ".gitmodules"
    if not gitmodules.exists():
        return []

    paths: list[str] = []
    for raw_line in gitmodules.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line.startswith("path ="):
            continue
        _, value = line.split("=", 1)
        candidate = value.strip().strip("/")
        if candidate:
            paths.append(candidate)

    return sorted(set(paths))


def _git_ls_files(repo_dir: Path) -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "-C", repo_dir.as_posix(), "ls-files", "-z"],
            stderr=subprocess.STDOUT,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(f"Failed to enumerate tracked files via git: {exc}") from exc

    parts = [p for p in out.split(b"\x00") if p]
    return [os.fsdecode(p) for p in parts]


def _normalize_path(path: str) -> str:
    path = path.replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return path.strip("/")


def _secret_filename_violation(rel_path: str) -> str | None:
    rel_path = _normalize_path(rel_path)
    base = rel_path.rsplit("/", 1)[-1]

    lower = base.lower()
    is_example = any(token in lower for token in ("example", "sample", "template"))

    if base == ".env":
        return "Secrets and env files"
    if base.startswith(".env.") and not is_example:
        return "Secrets and env files"
    if base in {"secrets.json", "id_rsa", "id_ed25519"}:
        return "Secrets and env files"
    if base.endswith((".pem", ".key")):
        return "Secrets and env files"

    return None


def verify(targets: list[str]) -> None:
    repo_root = _repo_root()
    known_submodules = set(_read_submodule_paths(repo_root))

    unknown = sorted([p for p in targets if p not in known_submodules])
    if unknown:
        raise RuntimeError(
            "Unknown submodule path(s): "
            + ", ".join(unknown)
            + "\n\nKnown submodules:\n  - "
            + "\n  - ".join(sorted(known_submodules))
        )

    violations: dict[str, dict[str, list[str]]] = {}

    for submodule_path in targets:
        submodule_dir = repo_root / submodule_path
        if not submodule_dir.exists() or not (submodule_dir / ".git").exists():
            raise RuntimeError(
                f"Submodule not initialized: {submodule_path}\n"
                "Run: git submodule update --init --recursive"
            )

        for rel_path in _git_ls_files(submodule_dir):
            rel_path = _normalize_path(rel_path)
            label = _secret_filename_violation(rel_path)
            if not label:
                continue

            bucket = violations.setdefault(submodule_path, {})
            bucket.setdefault(label, []).append(rel_path)

    if not violations:
        print("Submodule secret filename hygiene: OK")
        return

    lines: list[str] = ["Submodule secret filename hygiene: FAILED", ""]
    for submodule_path in sorted(violations.keys()):
        lines.append(f"{submodule_path}:")
        for label, paths in sorted(violations[submodule_path].items()):
            lines.append(f"  {label}:")
            for p in sorted(set(paths)):
                lines.append(f"    - {p}")
        lines.append("")

    lines.extend(
        [
            "Remediation:",
            "  - Remove the file(s) from the submodule Git index.",
            "  - Prefer committed templates (`.env.example`) and local-only `.env` files.",
        ]
    )

    raise RuntimeError("\n".join(lines).rstrip())


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that selected submodules do not track secret-bearing filenames "
            "(e.g., .env, private keys)."
        )
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all submodules listed in .gitmodules.",
    )
    parser.add_argument(
        "--submodule",
        action="append",
        default=[],
        help="Submodule path to scan (repeatable). Default: conxian-nexus.",
    )

    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    try:
        repo_root = _repo_root()
        known = _read_submodule_paths(repo_root)

        if args.all:
            targets = known
        else:
            targets = args.submodule or (["conxian-nexus"] if "conxian-nexus" in known else [])

        if not targets:
            raise RuntimeError(
                "No submodules selected for scanning (and conxian-nexus is not present in .gitmodules)."
            )

        verify(targets)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
