import os
import re

# Terminology Mapping
LEXICON_MAP = {
    r'\bdebt\b': 'POL',
    r'\bDebt\b': 'POL',
    r'\bloan\b': 'POL',
    r'\bLoan\b': 'POL',
    r'\binvestor\b': 'stakeholder',
    r'\bInvestor\b': 'Stakeholder',
    r'\bbond\b': 'Sovereign Bond',
    r'\bBond\b': 'Sovereign Bond',
    r'\badmin\b': 'executor',
    r'\bAdmin\b': 'Executor',
    r'\bfee\b': 'SAF',
    r'\bFee\b': 'SAF'
}

# Directories to skip
SKIP_DIRS = {'.git', 'node_modules', 'archive', '00_bos_core'}

def apply_lexicon(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    for pattern, replacement in LEXICON_MAP.items():
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated lexicon in: {file_path}")

def scan_and_enforce(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            if file.endswith('.md') or file.endswith('.txt'):
                file_path = os.path.join(root, file)
                apply_lexicon(file_path)

if __name__ == "__main__":
    scan_and_enforce('.')
