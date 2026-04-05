import re
from pathlib import Path
from urllib.parse import urlparse

def check_links():
    repo_root = Path(__file__).resolve().parents[1]
    md_files = list(repo_root.rglob('*.md'))
    broken_links = []

    for md_file in md_files:
        if 'node_modules' in str(md_file):
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        links = re.findall(r'\[.*?\]\((.*?)\)', content)

        for link in links:
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc:
                continue

            link_path = parsed.path

            # Only validate local markdown files; urlparse already strips fragments and queries.
            if not link_path or not link_path.endswith('.md'):
                continue

            # Resolve relative path
            if link_path.startswith('/'):
                target_path = (repo_root / link_path.lstrip('/')).resolve()
            else:
                target_path = (md_file.parent / link_path).resolve()

            if not target_path.exists():
                broken_links.append((md_file, link, target_path))

    for source, link, target in broken_links:
        print(f"Broken link in {source}: {link} -> {target}")

if __name__ == "__main__":
    check_links()
