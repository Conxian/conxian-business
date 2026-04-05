import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIR_PARTS = {
    '.git',
    '.next',
    '.venv',
    '__pycache__',
    'build',
    'coverage',
    'dist',
    'node_modules',
    'out',
    'playwright-report',
    'test-results',
}


def _find_markdown_files() -> list[Path]:
    md_files: list[Path] = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
        for name in files:
            if name.lower().endswith(('.md', '.markdown')):
                md_files.append(Path(root) / name)

    return md_files

def check_links():
    md_files = _find_markdown_files()
    broken_links = []

    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8')

        # Find markdown links [text](target)
        raw_links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', content)

        for link in raw_links:
            link = link.strip()
            if not link:
                continue

            if link.startswith('#'):
                continue

            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue

            # Clean up link (remove fragments)
            clean_link = link.split('#', 1)[0].strip()
            if not clean_link:
                continue

            href = clean_link.split()[0]
            if not href.lower().endswith(('.md', '.markdown')):
                continue

            base_dir = REPO_ROOT if href.startswith('/') else md_file.parent
            target_path = (base_dir / href.lstrip('/')).resolve()

            if not target_path.exists():
                try:
                    target_rel = target_path.relative_to(REPO_ROOT)
                except ValueError:
                    target_rel = target_path

                broken_links.append(
                    (
                        md_file.relative_to(REPO_ROOT),
                        link,
                        target_rel,
                    )
                )

    for source, link, target in broken_links:
        print(f"Broken link in {source}: {link} -> {target}")

    if broken_links:
        sys.exit(1)

if __name__ == "__main__":
    check_links()
