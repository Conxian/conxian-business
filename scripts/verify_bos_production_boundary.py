import os
import re
import sys


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def read_submodule_paths(root: str) -> list[str]:
    gitmodules_path = os.path.join(root, ".gitmodules")
    if not os.path.exists(gitmodules_path):
        return []

    paths: list[str] = []
    with open(gitmodules_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line.startswith("path ="):
                continue
            _, value = line.split("=", 1)
            candidate = value.strip()
            if candidate:
                paths.append(candidate)
    return paths


def is_in_dir(rel_path: str, rel_dir: str) -> bool:
    rel_dir = rel_dir.rstrip("/")
    if not rel_dir:
        return False
    return rel_path == rel_dir or rel_path.startswith(rel_dir + "/")


def iter_repo_files(root: str, excluded_dirs: set[str]) -> list[str]:
    excluded_paths = {
        p.rstrip("/").replace(os.sep, "/") for p in excluded_dirs if p.rstrip("/")
    }

    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""

        # If we've descended into an excluded path, stop scanning it entirely.
        if rel_dir and any(is_in_dir(rel_dir, ex) for ex in excluded_paths):
            dirnames[:] = []
            continue

        # Always prune standard noise and explicit exclusions.
        pruned: list[str] = []
        for d in dirnames:
            if d in {".git", "node_modules", ".next"}:
                continue

            child_rel_dir = f"{rel_dir}/{d}" if rel_dir else d
            if child_rel_dir in excluded_paths:
                continue

            pruned.append(d)
        dirnames[:] = pruned

        for name in filenames:
            full_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(full_path, root).replace(os.sep, "/")
            files.append(rel_path)
    return files


def read_text(root: str, rel_path: str) -> str:
    full_path = os.path.join(root, rel_path)
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main() -> int:
    root = repo_root()
    submodules = set(read_submodule_paths(root))
    excluded_dirs = {".idx"} | submodules

    repo_files = iter_repo_files(root, excluded_dirs)

    errors: list[str] = []

    # 1) Stub artifacts must be isolated.
    stub_files = [p for p in repo_files if p.endswith(".stub.json")]
    for stub_file in stub_files:
        if not is_in_dir(stub_file, "conxian-business"):
            errors.append(
                f"Stub artifact must be isolated under conxian-business/: {stub_file}"
            )

    # 2) Generated BOS audit outputs must never be committed.
    generated_dir = os.path.join(root, "conxian-business", ".generated")
    if os.path.isdir(generated_dir):
        generated_files: list[str] = []
        for dirpath, _, filenames in os.walk(generated_dir):
            for name in filenames:
                full_path = os.path.join(dirpath, name)
                rel_path = os.path.relpath(full_path, root).replace(os.sep, "/")
                generated_files.append(rel_path)
        if generated_files:
            errors.append(
                "Committed generated artifacts detected under conxian-business/.generated/: "
                + ", ".join(sorted(generated_files))
            )

    # 3) CI/runtime code must not depend on stub artifacts or local-only outputs.
    forbidden_substrings = [".stub.json", "conxian-business/.generated/"]
    code_exts = {".py", ".ts", ".js", ".mjs", ".cjs", ".sh", ".yml", ".yaml"}
    for rel_path in repo_files:
        _, ext = os.path.splitext(rel_path)
        if ext not in code_exts:
            continue
        if is_in_dir(rel_path, "docs") or is_in_dir(rel_path, "openspec"):
            continue
        if rel_path.startswith("scripts/verify_"):
            continue

        text = read_text(root, rel_path)
        for needle in forbidden_substrings:
            if needle in text:
                errors.append(
                    f"Production/CI code must not reference {needle}: {rel_path}"
                )

    # 4) Avoid hard-coded testnet defaults in operational scripts.
    testnet_network_literal = re.compile(r"networkFromName\(\s*['\"]testnet['\"]\s*\)")
    testnet_principal_literal = re.compile(r"['\"](?:ST|SN)[0-9A-Z]{20,}['\"]")
    for rel_path in repo_files:
        if not re.fullmatch(r"scripts/[^/]+\.ts", rel_path):
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
