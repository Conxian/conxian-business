#!/usr/bin/env bash
# Usage: wait_for_checks.sh owner/repo PR [timeout_seconds] [poll_seconds] [expected_head_sha]
# Read-only gate. A successful snapshot never substitutes for review or release approval.
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$script_dir/wait_for_checks.py" "$@"
