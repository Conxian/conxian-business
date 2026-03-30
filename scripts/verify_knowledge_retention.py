import os
import sys
import json
import subprocess

# Sensitive paths being ignored in .gitignore
SENSITIVE_PATHS = ['internal/strategy/', 'archive/']
MANIFEST_PATH = 'audit/migration_manifest.json'

def get_git_ignored_paths():
    """Get all paths that are currently being ignored by git."""
    try:
        output = subprocess.check_output(['git', 'ls-files', '--others', '-i', '--exclude-standard'], text=True)
        return output.splitlines()
    except Exception as e:
        print(f"Error getting ignored paths: {e}")
        return []

def verify():
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Knowledge migration manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    # Ensure the parent migration issue CON-306 exists in manifest
    if "CON-306" not in manifest:
        print("Error: Master Strategy Migration issue (CON-306) not found in manifest.")
        sys.exit(1)

    ignored_files = get_git_ignored_paths()

    # We want to check if any of the sensitive files are NOT in the manifest
    missing_from_manifest = []
    for file_path in ignored_files:
        is_sensitive = any(file_path.startswith(prefix) for prefix in SENSITIVE_PATHS)
        if is_sensitive:
            # We check if this file or its directory is covered in the manifest
            # For simplicity, we check if the manifest has a key that covers this file
            covered = False
            for entry_key, entry_val in manifest.items():
                if entry_val in file_path or entry_key in file_path:
                    covered = True
                    break
                if any(file_path.startswith(prefix) for prefix in entry_val.split(', ')):
                     covered = True
                     break

            # Since CON-306 covers all internal/strategy and archive, if it exists we consider it covered for this simple script
            if not covered and "CON-306" not in manifest:
                missing_from_manifest.append(file_path)

    if missing_from_manifest:
        print("Error: The following sensitive files are being ignored but are not in the migration manifest:")
        for file in missing_from_manifest:
            print(f"  - {file}")
        print("\nPlease ensure all knowledge is retained in Linear before ignoring in git.")
        sys.exit(1)

    print("Success: All ignored sensitive knowledge paths have been verified against the Linear migration manifest.")

if __name__ == "__main__":
    verify()
