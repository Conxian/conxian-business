#!/usr/bin/env bash
# sync-kb-versions.sh — Auto-extract versions from Cargo.toml and flag stale doc references.
# Run from conxian-business root.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUSINESS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

declare -A REPO_MAP
REPO_MAP=(
    ["conxius-enclave-sdk"]="conxius-enclave-sdk"
    ["lib-conxian-core"]="lib-conxian-core"
    ["conxian-gateway"]="conxian-gateway"
    ["conxian-nexus"]="conxian-nexus"
)

extract_version() {
    local repo="$1"
    local cargo_toml="$BUSINESS_ROOT/$repo/Cargo.toml"
    if [ -f "$cargo_toml" ]; then
        grep -m1 '^version' "$cargo_toml" | sed 's/.*"\(.*\)"/\1/'
    else
        echo "N/A"
    fi
}

echo "=== Version State (from Cargo.toml) ==="
echo ""
printf "%-25s %s\n" "REPOSITORY" "VERSION"
printf "%-25s %s\n" "----------" "-------"

for repo in conxius-enclave-sdk lib-conxian-core conxian-gateway conxian-nexus; do
    ver=$(extract_version "$repo")
    printf "%-25s %s\n" "$repo" "$ver"
done

echo ""
echo "=== Stale Doc Check ==="
echo ""

stale_count=0

for repo in conxius-enclave-sdk lib-conxian-core conxian-gateway conxian-nexus; do
    ver=$(extract_version "$repo")
    readme="$BUSINESS_ROOT/$repo/README.md"
    changelog="$BUSINESS_ROOT/$repo/CHANGELOG.md"

    # Check README for stale version badges
    if [ -f "$readme" ]; then
        # Look for version patterns that don't match current
        grep -n "v${ver%.*}\." "$readme" 2>/dev/null || true | while IFS=: read -r line content; do
            in_ver=$(echo "$content" | grep -oP "v\d+\.\d+\.\d+" | head -1)
            if [ "$in_ver" != "v$ver" ] && [ -n "$in_ver" ]; then
                echo -e "${YELLOW}[STALE]${NC} $repo/README.md:$line — $in_ver (expected v$ver)"
                stale_count=$((stale_count + 1))
            fi
        done
    fi

    # Check CHANGELOG for latest version entry
    if [ -f "$changelog" ]; then
        latest_entry=$(grep -m1 "^## \[v" "$changelog" 2>/dev/null | sed 's/.*\[\(.*\)\].*/\1/' || true)
        if [ "$latest_entry" != "v$ver" ]; then
            echo -e "${YELLOW}[STALE]${NC} $repo/CHANGELOG.md — latest entry $latest_entry (expected v$ver)"
        fi
    fi
done

echo ""
echo "=== AGENTS.md Summary ==="
echo ""

for repo in conxius-enclave-sdk lib-conxian-core conxian-gateway conxian-nexus; do
    agents="$BUSINESS_ROOT/$repo/AGENTS.md"
    if [ -f "$agents" ]; then
        size=$(wc -c < "$agents")
        lines=$(wc -l < "$agents")
        ver_ref=$(grep -m1 "v[0-9]" "$agents" 2>/dev/null | head -1 | xargs)
        printf "%-25s %6d bytes %4d lines  %s\n" "$repo" "$size" "$lines" "${ver_ref:0:60}"
    fi
done
