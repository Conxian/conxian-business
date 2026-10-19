from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str], cwd: Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return proc.returncode, (proc.stdout or proc.stderr).strip()


def repos(org: str) -> list[dict[str, object]]:
    # Enumerate every page visible to this credential. Submodules are a pinned
    # dependency subset, never an authoritative substitute for organization access.
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", org):
        raise ValueError("invalid organization name")
    code, output = run([
        "gh", "api", "--paginate", "--slurp",
        f"/orgs/{org}/repos?per_page=100&type=all",
    ])
    if code:
        raise RuntimeError("authenticated repository enumeration failed")
    pages = json.loads(output)
    if not isinstance(pages, list) or not pages or any(not isinstance(p, list) for p in pages):
        raise ValueError("paginated repository list required")
    result, seen = [], set()
    for page in pages:
        for item in page:
            if not isinstance(item, dict):
                raise ValueError("invalid repository metadata")
            name = item.get("name")
            owner = item.get("owner")
            if (not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name)
                    or name in {".", ".."} or name.casefold() in seen
                    or not isinstance(owner, dict)
                    or not isinstance(owner.get("login"), str)
                    or owner["login"].casefold() != org.casefold()
                    or type(item.get("archived")) is not bool
                    or type(item.get("disabled")) is not bool):
                raise ValueError("duplicate, unscoped or incomplete repository metadata")
            seen.add(name.casefold())
            if item["archived"]:
                continue
            # Construct trusted GitHub URLs; never clone an arbitrary API value.
            url = f"https://github.com/{org}/{name}"
            result.append({"name": name, "html_url": url, "clone_url": url + ".git",
                           "archived": False, "disabled": item["disabled"],
                           "default_branch": item.get("default_branch"),
                           "description": item.get("description"),
                           "language": item.get("language")})
    if not result:
        raise ValueError("no visible active repositories; coverage is unknown")
    return result


def inspect(repo: dict[str, object], checkout: Path) -> dict[str, object]:
    code, revision = run(["git", "rev-parse", "HEAD"], cwd=checkout)
    if code or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise RuntimeError("source revision unavailable")
    files = [p for p in checkout.rglob("*") if not p.is_symlink() and p.is_file() and ".git" not in p.parts]
    names = {p.name for p in files}
    text_files = [p for p in files if p.suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".py", ".rs", ".go", ".java", ".yml", ".yaml", ".json", ".md"}]
    secret_hits: list[str] = []
    unsafe_hits: list[str] = []
    unreadable: list[str] = []
    for path in text_files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            unreadable.append(path.relative_to(checkout).as_posix())
            continue
        if any(marker in text for marker in ("BEGIN PRIVATE KEY", "AKIA", "ghp_", "sk_live_")):
            secret_hits.append(path.relative_to(checkout).as_posix())
        if any(marker in text for marker in ("dangerouslySetInnerHTML", "eval(", "child_process.exec(", "os.system(")):
            unsafe_hits.append(path.relative_to(checkout).as_posix())
    kb = sorted(str(p.relative_to(checkout)) for p in files if any(token in p.name.lower() for token in ("readme", "knowledge", "changelog", "governance", "architecture")))[:100]
    return {
        "name": repo["name"],
        "url": repo["html_url"],
        "default_branch": repo.get("default_branch"),
        "source_revision": revision,
        "languages": repo.get("language"),
        "file_count": len(files),
        "has_readme": "README.md" in names,
        "has_security": "SECURITY.md" in names,
        "has_codeowners": any(p.endswith("CODEOWNERS") for p in (str(f.relative_to(checkout)) for f in files)),
        "kb_candidates": kb,
        "secret_suspects": secret_hits,
        "unsafe_suspects": unsafe_hits,
        "unreadable_text_files": unreadable,
        "status": "attention" if secret_hits or unsafe_hits or unreadable or "README.md" not in names else "source-scan-complete",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan visible non-archived repositories; no runtime or security acceptance.")
    parser.add_argument("--org", default=os.environ.get("BOS_GITHUB_ORG", "Conxian"))
    parser.add_argument("--output", default="audit/bos-org-review.json")
    parser.add_argument("--markdown", default="audit/bos-org-review.md")
    args = parser.parse_args()
    root = Path.cwd()
    report = {"generated_at": dt.datetime.now(dt.UTC).isoformat(), "organization": args.org,
              "coverage_scope": "authenticated-visible-non-archived-default-branches",
              "exhaustive_security_audit": False, "runtime_qualification": False,
              "repositories": []}
    try:
        inventory = repos(args.org)
    except (OSError, RuntimeError, ValueError) as error:
        # Provider/process errors can contain credentials or private endpoints.
        print(f"Repository enumeration unavailable ({type(error).__name__}); no audit completed.", file=sys.stderr)
        return 1
    failed = False
    with tempfile.TemporaryDirectory(prefix="bos-org-review-") as temp:
        base = Path(temp)
        for repo in inventory:
            target = base / str(repo["name"])
            try:
                if repo["disabled"]:
                    raise RuntimeError("disabled repository")
                code, _ = run(["git", "clone", "--depth", "1", str(repo["clone_url"]), str(target)])
                if code:
                    raise RuntimeError("clone failed")
                observation = inspect(repo, target)
                if observation["unreadable_text_files"]:
                    failed = True
                report["repositories"].append(observation)
            except (OSError, RuntimeError, ValueError):
                failed = True
                report["repositories"].append({"name": repo["name"], "url": repo["html_url"], "status": "source_unavailable"})
    report["inventory_count"] = len(inventory)
    report["source_scan_complete"] = not failed
    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    rows = [f"# BOS organization review\n\nGenerated: `{report['generated_at']}`\n\n| Repository | Status | README | Security | CODEOWNERS | KB candidates |\n|---|---|---:|---:|---:|---:|"]
    for item in report["repositories"]:
        rows.append(f"| [{item['name']}]({item.get('url', '')}) | {item['status']} | {'yes' if item.get('has_readme') else 'no'} | {'yes' if item.get('has_security') else 'no'} | {'yes' if item.get('has_codeowners') else 'no'} | {len(item.get('kb_candidates', []))} |")
    rows.append("\nScope: authenticated-visible, non-archived default-branch source snapshots only. Other identities, branches, open PRs, dependencies, runtime connections and security acceptance require separate evidence. Findings are heuristic leads, not verified vulnerabilities. Keep reports restricted pending disclosure review.")
    rows.append(f"\nSource scan complete: {report['source_scan_complete']}. No repository, PR or merge was modified.")
    markdown_path = root / args.markdown
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Source scan {'incomplete' if failed else 'complete'} for {len(inventory)} visible repositories; reports require restricted review.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

