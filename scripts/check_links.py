import os
import re
from pathlib import Path
import sys

def check_links():
    md_files = list(Path('.').rglob('*.md'))
    broken_links = []

    for md_file in md_files:
        if 'node_modules' in str(md_file):
            continue

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

            # Only validate repository-local markdown files
            if not clean_link.endswith('.md'):
                continue

            # Resolve relative path
            target_path = (md_file.parent / clean_link).resolve()

            if not target_path.exists():
                broken_links.append((md_file, link, target_path))

    for source, link, target in broken_links:
        print(f"Broken link in {source}: {link} -> {target}")

    if broken_links:
        sys.exit(1)

if __name__ == "__main__":
    check_links()
