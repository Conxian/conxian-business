from __future__ import annotations

import configparser
import subprocess
import sys
from pathlib import Path


def _run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        details = (proc.stderr or proc.stdout).strip() or f"exit code {proc.returncode}"
        raise RuntimeError(f"git {' '.join(args)} failed: {details}")

    return proc.stdout


def _parse_gitlinks() -> set[str]:
    output = _run_git(["ls-files", "--stage"])
    gitlinks: set[str] = set()

    for raw_line in output.splitlines():
        parts = raw_line.split("\t", 1)
        if len(parts) != 2:
            continue

        meta, path = parts
        mode = meta.split(" ", 1)[0]
        if mode == "160000":
            gitlinks.add(path)

    return gitlinks


def _parse_gitmodules_paths(gitmodules_path: Path) -> set[str]:
    if not gitmodules_path.exists():
        raise RuntimeError(".gitmodules not found")

    config = configparser.ConfigParser()
    config.read(gitmodules_path, encoding="utf-8")

    paths: set[str] = set()
    for section in config.sections():
        if not section.startswith('submodule "'):
            continue

        path = config.get(section, "path", fallback="").strip()
        if not path:
            continue
        paths.add(path)

    return paths


def verify() -> None:
    gitlinks = _parse_gitlinks()
    gitmodules_paths = _parse_gitmodules_paths(Path(".gitmodules"))

    missing_mappings = sorted(gitlinks - gitmodules_paths)
    extra_mappings = sorted(gitmodules_paths - gitlinks)

    if not missing_mappings and not extra_mappings:
        print("Success: .gitmodules mappings match gitlink entries.")
        return

    lines: list[str] = ["Submodule integrity check failed:"]
    if missing_mappings:
        lines.append("\nGitlinks in index with no .gitmodules entry:")
        lines.extend([f"  - {p}" for p in missing_mappings])
    if extra_mappings:
        lines.append("\n.gitmodules entries with no gitlink in index:")
        lines.extend([f"  - {p}" for p in extra_mappings])

    raise RuntimeError("\n".join(lines))


if __name__ == "__main__":
    try:
        verify()
    except Exception as e:
        print(str(e))
        sys.exit(1)
