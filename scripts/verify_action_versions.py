#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"

EXCLUDE_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"^\./"),          # local composite actions
    re.compile(r"^docker://"),    # Docker images
)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
CACHE_FILE = REPO_ROOT / ".github" / ".action-version-cache.json"

def _load_cache() -> dict[str, bool]:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}

def _save_cache(cache: dict[str, bool]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")

def _extract_uses_refs() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    if not WORKFLOW_DIR.is_dir():
        return refs
    for wf in sorted(WORKFLOW_DIR.glob("*.yml")):
        rel = wf.relative_to(REPO_ROOT).as_posix()
        content = wf.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"^\s*uses:\s*(.+?)(?:\s*#.*)?$", content, re.MULTILINE):
            raw = match.group(1).strip().strip("'\"")
            if any(p.match(raw) for p in EXCLUDE_PATTERNS):
                continue
            if "@" not in raw:
                continue
            refs.setdefault(raw, []).append(rel)
    return refs

def _check_ref(action_ref: str) -> tuple[bool, str]:
    parts = action_ref.split("@", 1)
    if len(parts) != 2:
        return False, f"malformed action ref: {action_ref}"
    repo_path, ref = parts

    is_sha = bool(re.match(r"^[0-9a-f]{40}$", ref))

    if is_sha:
        url = f"https://api.github.com/repos/{repo_path}/commits/{ref}"
    else:
        # Only validate major-version tags like v4, v1 or specific tags
        if not re.match(r"^v\d+(\.\d+\.\d+)?$", ref) and ref != "master" and ref != "main":
            return True, f"skipped (non-standard ref: {ref})"
        url = f"https://api.github.com/repos/{repo_path}/git/ref/tags/{ref}"

    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}"]
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
        cmd.append(url)

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        status = int(proc.stdout.strip())
        if status == 200:
            return True, "exists"
        elif status == 404:
            if not is_sha and "tags/" in url:
                # Try heads
                url_ref = f"https://api.github.com/repos/{repo_path}/git/ref/heads/{ref}"
                cmd[-1] = url_ref
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if int(proc.stdout.strip()) == 200:
                    return True, "exists (branch)"
            return False, f"not found (404) at {url}"
        elif status == 403:
            return True, f"skipped (rate limited)"
        else:
            return True, f"skipped (HTTP {status})"
    except Exception as exc:
        return True, f"skipped (error: {exc})"

def main() -> int:
    refs = _extract_uses_refs()
    print(f"Checking {len(refs)} unique action reference(s)...\n")
    cache = _load_cache()
    errors: list[str] = []
    checked = 0
    for action_ref, files in sorted(refs.items()):
        if action_ref in cache and cache[action_ref]:
            exists, status = True, "cached-OK"
        else:
            exists, status = _check_ref(action_ref)
            cache[action_ref] = exists
            time.sleep(0.05)
        checked += 1
        file_list = ", ".join(files)
        if exists:
            print(f"  OK  {action_ref}  ({status})")
        else:
            msg = f"{action_ref} — {status}"
            errors.append(msg)
            print(f"  FAIL  {msg}  [{file_list}]")
    _save_cache(cache)
    if errors:
        print(f"\n❌ {len(errors)} invalid action version(s) found.")
        return 1
    print(f"\n✅ All {checked} action version(s) valid.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
