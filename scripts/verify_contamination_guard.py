import os
import re
import subprocess
import sys


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def git_ls_files(root: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "-C", root, "ls-files", "-z"],
        stderr=subprocess.STDOUT,
    )
    parts = [p for p in out.split(b"\x00") if p]
    return [os.fsdecode(p) for p in parts]


def is_in_dir(rel_path: str, rel_dir: str) -> bool:
    rel_dir = rel_dir.rstrip("/")
    if not rel_dir:
        return False
    return rel_path == rel_dir or rel_path.startswith(rel_dir + "/")


def read_text(root: str, rel_path: str) -> str:
    full_path = os.path.join(root, rel_path)
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def scan_repo(root: str, label: str, excluded_dirs: set[str]) -> list[str]:
    code_exts = {
        ".rs",
        ".ts",
        ".tsx",
        ".js",
        ".mjs",
        ".cjs",
        ".py",
        ".sh",
        ".clar",
    }

    patterns: list[tuple[str, re.Pattern[str]]] = [
        ("MOCK_", re.compile(r"\bMOCK_[A-Z0-9_]+\b")),
        ("stub-func", re.compile(r"\bstub-func\b")),
        ("[STUB]", re.compile(r"\[STUB\]")),
    ]

    errors: list[str] = []
    for rel_path in git_ls_files(root):
        if any(is_in_dir(rel_path, ex) for ex in excluded_dirs):
            continue

        if rel_path.endswith("verify_contamination_guard.py"):
            continue

        _, ext = os.path.splitext(rel_path)
        if ext not in code_exts:
            continue

        text = read_text(root, rel_path)
        for label_text, pattern in patterns:
            if pattern.search(text):
                errors.append(f"{label}: prohibited marker '{label_text}' found in {rel_path}")
                break

    return errors


def main() -> int:
    root = repo_root()

    excluded_dirs = {
        "docs",
        "openspec",
        "audit",
        ".github",
        ".idx",
        "tests",
        "test",
    }

    errors: list[str] = []
    errors.extend(scan_repo(root, "conxian-business", excluded_dirs))

    for sub in ["lib-conxian-core", "lib-conclave-sdk"]:
        sub_path = os.path.join(root, sub)
        if not os.path.isdir(sub_path):
            continue
        errors.extend(scan_repo(sub_path, sub, {"docs", "tests", "test"}))

    if errors:
        print("Production contamination guard violations found:\n")
        for err in sorted(errors):
            print(f"- {err}")
        return 1

    print("Production contamination guard: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
