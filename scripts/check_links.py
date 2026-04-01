import re
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    'node_modules',
    '.git',
    '.next',
    '.venv',
    'build',
    'dist',
    'out',
    '__pycache__',
    'playwright-report',
    'test-results',
}


def _find_markdown_files() -> list[Path]:
    md_files: list[Path] = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.lower().endswith(('.md', '.markdown')):
                md_files.append(Path(root) / name)
    return md_files


def _repo_root_for(md_file: Path) -> Path:
    current = md_file.parent
    while True:
        if (current / '.git').exists():
            return current
        if current == current.parent:
            return REPO_ROOT
        current = current.parent

def check_links():
    md_files = _find_markdown_files()
    broken_links = []

    for md_file in md_files:
        repo_root_for_file = _repo_root_for(md_file)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find markdown links [text](target)
        links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', content)

        for link in links:
            link = link.strip()
            if not link:
                continue

            # Skip external URLs, anchors, and any other URI schemes (mailto:, ftp:, etc.)
            if link.startswith('#') or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue

            clean_link = link.split('#', 1)[0].strip()
            if not clean_link:
                continue

            href = clean_link.split()[0]
            href_lower = href.lower()

            # Only validate repository-local markdown files
            if not (href_lower.endswith('.md') or href_lower.endswith('.markdown')):
                continue

            if href.startswith('/'):
                target_path = (repo_root_for_file / href.lstrip('/')).resolve()
            else:
                target_path = (md_file.parent / href).resolve()

            if not target_path.exists():
                broken_links.append((md_file, link, target_path))

    for source, link, target in broken_links:
        rel_source = source.relative_to(REPO_ROOT)
        try:
            rel_target = target.relative_to(REPO_ROOT)
        except ValueError:
            rel_target = target
        print(f"Broken link in {rel_source}: {link} -> {rel_target}")

    if broken_links:
        sys.exit(1)

if __name__ == "__main__":
    check_links()
