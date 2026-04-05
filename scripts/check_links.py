import re
import os
import configparser
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


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _submodule_dirs() -> list[Path]:
    gitmodules = REPO_ROOT / '.gitmodules'
    if not gitmodules.exists():
        return []

    config = configparser.ConfigParser(interpolation=None)
    config.read(gitmodules, encoding='utf-8')

    submodule_paths = [
        config.get(section, 'path')
        for section in config.sections()
        if config.has_option(section, 'path')
    ]

    return [(REPO_ROOT / p).resolve() for p in submodule_paths]


def _uninitialized_submodule_dirs() -> list[Path]:
    return [d for d in _submodule_dirs() if not (d / '.git').exists()]


def _is_within_uninitialized_submodule(path: Path, uninitialized_submodule_dirs: list[Path]) -> bool:
    return any(_is_relative_to(path, submodule_dir) for submodule_dir in uninitialized_submodule_dirs)


def _is_within_submodule(path: Path, submodule_dirs: list[Path]) -> bool:
    return any(_is_relative_to(path, submodule_dir) for submodule_dir in submodule_dirs)


def _find_markdown_files() -> list[Path]:
    md_files: list[Path] = []
    submodule_dirs = _submodule_dirs()

    for root, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root)

        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        if _is_within_submodule(root_path.resolve(), submodule_dirs):
            dirs[:] = []
            continue

        dirs[:] = [
            d
            for d in dirs
            if not _is_within_submodule((root_path / d).resolve(), submodule_dirs)
        ]

        for name in files:
            if name.lower().endswith(('.md', '.markdown')):
                md_files.append(root_path / name)

    return md_files


def _strip_fenced_code_blocks(text: str) -> str:
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'~~~.*?~~~', '', text, flags=re.S)
    return text


def _repo_root_for(md_file: Path) -> Path:
    current = md_file.parent
    while True:
        if (current / '.git').exists():
            return current
        if current == current.parent:
            return REPO_ROOT
        current = current.parent


def _extract_markdown_links(text: str) -> list[str]:
    links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
    links.extend(re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', text, flags=re.M))
    return links


def check_links():
    md_files = _find_markdown_files()
    broken_links = []
    uninitialized_submodule_dirs = _uninitialized_submodule_dirs()

    for md_file in md_files:
        repo_root_for_file = _repo_root_for(md_file)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        content = _strip_fenced_code_blocks(content)

        # Find markdown links [text](target)
        links = _extract_markdown_links(content)

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

            href = clean_link.split()[0].strip('<>')
            href_lower = href.lower()

            # Only validate repository-local markdown files
            if not (href_lower.endswith('.md') or href_lower.endswith('.markdown')):
                continue

            if href.startswith('/'):
                target_path = (repo_root_for_file / href.lstrip('/')).resolve()
            else:
                target_path = (md_file.parent / href).resolve()

            if not _is_relative_to(target_path, repo_root_for_file):
                broken_links.append((md_file, link, target_path))
                continue

            if not target_path.exists():
                if _is_within_uninitialized_submodule(target_path, uninitialized_submodule_dirs):
                    continue
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


if __name__ == '__main__':
    check_links()
