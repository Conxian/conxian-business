from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import tempfile
from pathlib import Path


def run(command: list[str], cwd: Path | None = None) -> tuple[int, str]:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return proc.returncode, (proc.stdout or proc.stderr).strip()


def repos(org: str) -> list[dict[str, object]]:
    # Use the authenticated gh repo surface, which is available in CI and local
    # operator sessions even when the raw API credential is not exported.
    code, output = run([
        "gh", "repo", "list", org, "--limit", "100",
        "--json", "name,url,isArchived,defaultBranchRef,description",
    ])
    if code:
        # A checked-out conxian-business clone may have repository access through
        # mounted submodules while gh API credentials are intentionally absent.
        path_code, path_output = run(["git", "config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"])
        url_code, url_output = run(["git", "config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.url$"])
        if path_code or url_code:
            raise RuntimeError(f"Unable to enumerate {org}: {output}")
        paths = {line.split(" ", 1)[0].removeprefix("submodule.").removesuffix(".path"): line.split(" ", 1)[1] for line in path_output.splitlines()}
        urls = {line.split(" ", 1)[0].removeprefix("submodule.").removesuffix(".url"): line.split(" ", 1)[1] for line in url_output.splitlines()}
        return [
            {
                "name": path.split("/")[-1],
                "html_url": urls[key],
                "clone_url": urls[key],
                "archived": False,
            }
            for key, path in paths.items()
            if key in urls
        ]
    data = json.loads(output)
    return [
        {
            "name": item["name"],
            "html_url": item["url"],
            "clone_url": f"https://github.com/{org}/{item['name']}.git",
            "archived": item.get("isArchived", False),
            "default_branch": (item.get("defaultBranchRef") or {}).get("name"),
            "description": item.get("description"),
        }
        for item in data
        if not item.get("isArchived")
    ]


def inspect(repo: dict[str, object], checkout: Path) -> dict[str, object]:
    files = [p for p in checkout.rglob("*") if p.is_file() and ".git" not in p.parts]
    names = {p.name for p in files}
    text_files = [p for p in files if p.suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".py", ".rs", ".go", ".java", ".yml", ".yaml", ".json", ".md"}]
    secret_hits: list[str] = []
    unsafe_hits: list[str] = []
    for path in text_files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
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
        "languages": repo.get("language"),
        "file_count": len(files),
        "has_readme": "README.md" in names,
        "has_security": "SECURITY.md" in names,
        "has_codeowners": any(p.endswith("CODEOWNERS") for p in (str(f.relative_to(checkout)) for f in files)),
        "kb_candidates": kb,
        "secret_suspects": secret_hits,
        "unsafe_suspects": unsafe_hits,
        "status": "attention" if secret_hits or unsafe_hits or "README.md" not in names else "reviewed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Review every non-archived repository in a GitHub organization.")
    parser.add_argument("--org", default=os.environ.get("BOS_GITHUB_ORG", "Conxian"))
    parser.add_argument("--output", default="audit/bos-org-review.json")
    parser.add_argument("--markdown", default="audit/bos-org-review.md")
    args = parser.parse_args()
    root = Path.cwd()
    report = {"generated_at": dt.datetime.now(dt.UTC).isoformat(), "organization": args.org, "repositories": []}
    with tempfile.TemporaryDirectory(prefix="bos-org-review-") as temp:
        base = Path(temp)
        for repo in repos(args.org):
            target = base / str(repo["name"])
            code, output = run(["git", "clone", "--depth", "1", str(repo["clone_url"]), str(target)])
            if code:
                report["repositories"].append({"name": repo["name"], "url": repo["html_url"], "status": "clone_failed", "error": output[:500]})
                continue
            report["repositories"].append(inspect(repo, target))
    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    rows = [f"# BOS organization review\n\nGenerated: `{report['generated_at']}`\n\n| Repository | Status | README | Security | CODEOWNERS | KB candidates |\n|---|---|---:|---:|---:|---:|"]
    for item in report["repositories"]:
        rows.append(f"| [{item['name']}]({item.get('url', '')}) | {item['status']} | {'yes' if item.get('has_readme') else 'no'} | {'yes' if item.get('has_security') else 'no'} | {'yes' if item.get('has_codeowners') else 'no'} | {len(item.get('kb_candidates', []))} |")
    rows.append("\nThis report is evidence and proposal input. It does not modify repositories, open PRs, or merge changes.")
    (root / args.markdown).write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Reviewed {len(report['repositories'])} repositories; wrote {args.output} and {args.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

