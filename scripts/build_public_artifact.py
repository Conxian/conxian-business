#!/usr/bin/env python3
"""Build an explicit public allowlist; never crawl the repository or follow links."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "docs/public-artifact.json"


def relative_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("invalid public artifact path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", ".."} or p.startswith(".") for p in value.split("/")):
        raise ValueError("public artifact paths must be explicit and relative")
    return path


def regular_source(root: Path, value: str) -> Path:
    path = relative_path(value)
    if path.parts[0] != "public-docs":
        raise ValueError("only reviewed public-docs sources may be published")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlinks are forbidden in public sources")
    if not current.is_file() or current.stat().st_size > 2_000_000:
        raise ValueError("public source missing or exceeds size limit")
    return current


def build(root: Path, output: Path) -> dict:
    root = root.resolve()
    output = output.absolute()
    # No recursive deletion or merge into an existing directory. In particular,
    # refuse the repo root, source directory, and symlinked destinations.
    if output.exists() or output.is_symlink() or output.resolve() != output:
        raise ValueError("output must be a new directory without symlink parents")
    if output == root or output in root.parents or root / "public-docs" in output.parents:
        raise ValueError("output must not replace source directories")
    manifest = json.loads((root / MANIFEST).read_text())
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), list) or not manifest["files"]:
        raise ValueError("nonempty versioned public allowlist required")
    files, names = [], set()
    for item in manifest["files"]:
        destination = str(relative_path(item["destination"]))
        if destination in names or destination == "artifact-manifest.json":
            raise ValueError("duplicate or reserved public destination")
        if PurePosixPath(destination).suffix not in {".html", ".css", ".svg", ".png", ".ico"}:
            raise ValueError("unsupported public file type")
        names.add(destination)
        data = regular_source(root, item["source"]).read_bytes()
        files.append((destination, data))
    if "index.html" not in names:
        raise ValueError("public index.html required")
    evidence = {"schema_version": 1, "classification": "public-safe",
                "files": [{"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
                          for path, data in sorted(files)]}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".public-build-", dir=output.parent) as temp:
        stage = Path(temp) / "site"
        stage.mkdir()
        for path, data in files:
            target = stage / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (stage / "artifact-manifest.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        stage.rename(output)
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        result = build(ROOT, args.output)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f"Public artifact build rejected ({type(exc).__name__}).\n")
    print(f"Built {len(result['files'])} explicitly allowlisted public files.")


if __name__ == "__main__":
    main()
