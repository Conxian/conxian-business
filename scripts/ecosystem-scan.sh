#!/bin/bash
# Multi-Dimensional Repository Ecosystem Scanner
# SPATIAL | RELATIONAL | OPERATIONAL | SECURITY | LOGICAL

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/ecosystem-scan-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "=============================================="
echo "Conxian Ecosystem Multi-Dimensional Scanner"
echo "=============================================="
echo "Output: $OUTPUT_DIR"
echo ""

# Initialize output files
> "$OUTPUT_DIR/01_SPATIAL_inventory.md"
> "$OUTPUT_DIR/02_RELATIONAL_dependencies.md"
> "$OUTPUT_DIR/03_OPERATIONAL_cicd.md"
> "$OUTPUT_DIR/04_SECURITY_vulnerabilities.md"
> "$OUTPUT_DIR/05_LOGICAL_context.md"
> "$OUTPUT_DIR/summary.json"

# Define all repos to scan (submodules + workspace packages)
declare -a REPOS=(
    "conxian-gateway"
    "conxius-wallet"
    "conxian-nexus"
    "conxian-ui"
    "Conxian"
    "conxius-platform"
    "conxius-orbit"
    "conxian-labs-site"
    "conxius-enclave-sdk"
    "lib-conxian-core"
    "apps/control-plane"
    "packages/client-sdk"
    "packages/schemas"
)

declare -a MAIN_REPO_CONTEXTS=(
    "showcase-dapp"
)

# ============================================
# 1. SPATIAL - Full Repository Inventory
# ============================================
echo "📦 [SPATIAL] Scanning repository structures..."

{
    echo "# SPATIAL - Full Repository Inventory"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    scan_repo_structure() {
        local repo_path="$1"
        local repo_name="$2"
        local full_path="$REPO_ROOT/$repo_path"
        
        if [ ! -d "$full_path" ]; then
            echo "## $repo_name (NOT FOUND: $repo_path)"
            echo "⚠️ Repository path does not exist"
            echo ""
            return
        fi
        
        echo "## $repo_name"
        echo "Path: \`$repo_path\`"
        echo ""
        
        # Source directories
        echo "### Source Directories"
        if [ -d "$full_path/src" ]; then
            echo "- \`src/\`: $(find "$full_path/src" -type f | wc -l) files"
            find "$full_path/src" -type f -name "*.ts" -o -name "*.tsx" -o -name "*.rs" -o -name "*.js" 2>/dev/null | head -5 | sed 's/^/  - /'
        fi
        if [ -d "$full_path/lib" ]; then
            echo "- \`lib/\`: $(find "$full_path/lib" -type f | wc -l) files"
        fi
        if [ -d "$full_path/contracts" ]; then
            echo "- \`contracts/\`: $(find "$full_path/contracts" -type f | wc -l) files"
        fi
        echo ""
        
        # Key config files
        echo "### Key Configuration Files"
        for cfg in Cargo.toml package.json package-lock.json pnpm-lock.yaml tsconfig.json Cargo.lock; do
            if [ -f "$full_path/$cfg" ]; then
                echo "- \`$cfg\` ✅"
            fi
        done
        echo ""
        
        # Test directories
        echo "### Test Directories"
        for test_dir in tests test __tests__ spec; do
            if [ -d "$full_path/$test_dir" ]; then
                echo "- \`$test_dir/\`: $(find "$full_path/$test_dir" -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l) test files"
            fi
        done
        echo ""
        
        # GitHub workflows
        if [ -d "$full_path/.github/workflows" ]; then
            echo "### GitHub Workflows"
            ls "$full_path/.github/workflows" 2>/dev/null | sed 's/^/- /'
            echo ""
        fi
        
        # README
        if [ -f "$full_path/README.md" ]; then
            local first_line=$(head -1 "$full_path/README.md" 2>/dev/null)
            echo "### Purpose (from README)"
            echo "$first_line"
            echo ""
        fi
        
        echo "---"
        echo ""
    }
    
    # Scan main repo
    echo "## main (conxian-business)"
    echo "Path: \`.\` (root)"
    echo ""
    echo "### Workspace Structure"
    echo "- Submodules: $(ls -d conxian-* Conxian conxius-* lib-conxian-core 2>/dev/null | wc -l) git submodules"
    echo "- Apps: $(ls -d apps/*/ 2>/dev/null | wc -l) applications"
    echo "- Packages: $(ls -d packages/*/ 2>/dev/null | wc -l) shared packages"
    echo ""
    echo "### Root Level Config Files"
    for cfg in Cargo.toml package.json pnpm-workspace.yaml Makefile; do
        [ -f "$cfg" ] && echo "- \`$cfg\` ✅"
    done
    echo ""
    echo "### GitHub Workflows"
    [ -d ".github/workflows" ] && ls ".github/workflows" | sed 's/^/- /'
    echo ""
    echo "---"
    echo ""
    
    # Scan submodules
    for repo in "${REPOS[@]}"; do
        scan_repo_structure "$repo" "$repo"
    done
    
} > "$OUTPUT_DIR/01_SPATIAL_inventory.md"

echo "✅ SPATIAL inventory complete"

# ============================================
# 2. RELATIONAL - Dependency Graph
# ============================================
echo "🔗 [RELATIONAL] Mapping dependencies..."

{
    echo "# RELATIONAL - Dependency Graph"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    extract_cargo_deps() {
        local repo_path="$1"
        local full_path="$REPO_ROOT/$repo_path"
        
        if [ ! -f "$full_path/Cargo.toml" ]; then
            return
        fi
        
        echo "### $repo_path (Rust/Cargo)"
        echo ""
        echo "\`\`\`toml"
        grep -A 50 '\[dependencies\]' "$full_path/Cargo.toml" 2>/dev/null | head -30 || echo "(no dependencies section)"
        echo "\`\`\`"
        echo ""
        
        # Check for workspace membership
        if grep -q "workspace = true" "$full_path/Cargo.toml" 2>/dev/null; then
            echo "*Member of Rust workspace*"
        fi
        
        # lib-conxian-core dependency
        if grep -q "lib-conxian-core" "$full_path/Cargo.toml" 2>/dev/null; then
            echo "*🔗 Depends on: lib-conxian-core*"
        fi
        echo ""
        echo "---"
        echo ""
    }
    
    extract_npm_deps() {
        local repo_path="$1"
        local full_path="$REPO_ROOT/$repo_path"
        
        if [ ! -f "$full_path/package.json" ]; then
            return
        fi
        
        echo "### $repo_path (Node.js/npm)"
        echo ""
        echo "\`\`\`json"
        cat "$full_path/package.json" 2>/dev/null
        echo "\`\`\`"
        echo ""
        
        # Check for workspace dependencies
        if grep -q "@conxian" "$full_path/package.json" 2>/dev/null; then
            echo "*🔗 Internal workspace deps:*"
            grep "@conxian" "$full_path/package.json" | sed 's/^/  - /'
        fi
        
        # Check for lib-conxian-core usage
        if grep -q "lib-conxian-core" "$full_path/package.json" 2>/dev/null; then
            echo "*🔗 Depends on: lib-conxian-core*"
        fi
        echo ""
        echo "---"
        echo ""
    }
    
    # Root Cargo.toml
    if [ -f "$REPO_ROOT/Cargo.toml" ]; then
        echo "## Root Level (conxian-business)"
        echo ""
        echo "### Cargo.toml"
        echo "\`\`\`toml"
        cat "$REPO_ROOT/Cargo.toml"
        echo "\`\`\`"
        echo ""
        echo "---"
        echo ""
    fi
    
    # Scan all repos for dependencies
    for repo in "${REPOS[@]}" "${MAIN_REPO_CONTEXTS[@]}"; do
        extract_cargo_deps "$repo"
        extract_npm_deps "$repo"
    done
    
    # Also scan apps and packages
    for pkg in apps/* packages/*; do
        if [ -d "$pkg" ]; then
            extract_npm_deps "$pkg"
        fi
    done
    
} > "$OUTPUT_DIR/02_RELATIONAL_dependencies.md"

echo "✅ RELATIONAL dependencies complete"

# ============================================
# 3. OPERATIONAL - CI/CD Inventory
# ============================================
echo "⚙️ [OPERATIONAL] Inventorying CI/CD workflows..."

{
    echo "# OPERATIONAL - CI/CD Inventory"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    scan_workflows() {
        local repo_path="$1"
        local repo_name="$2"
        local full_path="$REPO_ROOT/$repo_path"
        
        echo "## $repo_name"
        echo "Path: \`$repo_path\`"
        echo ""
        
        if [ ! -d "$full_path/.github/workflows" ]; then
            echo "No GitHub workflows found"
            echo ""
            return
        fi
        
        echo "### Workflows"
        echo ""
        
        for workflow in "$full_path/.github/workflows"/*.yml "$full_path/.github/workflows"/*.yaml; do
            if [ -f "$workflow" ]; then
                local wf_name=$(basename "$workflow" .yml)
                wf_name=$(basename "$wf_name" .yaml)
                echo "#### \`$wf_name.yml\`"
                echo ""
                
                # Extract triggers
                echo "**Triggers:**"
                grep -E "^(on:|push:|pull_request:|schedule:|workflow_dispatch:)" "$workflow" 2>/dev/null | head -5 || echo "(inline triggers)"
                echo ""
                
                # Extract jobs
                echo "**Jobs:**"
                grep "^  [a-zA-Z_-]*:" "$workflow" 2>/dev/null | sed 's/:$//' | head -10 || echo "(single job)"
                echo ""
                
                # Extract secrets/permissions
                if grep -q "secrets:" "$workflow"; then
                    echo "**🔒 Uses Secrets:** Yes"
                fi
                if grep -q "permissions:" "$workflow"; then
                    echo "**Permissions:**"
                    grep -A 5 "permissions:" "$workflow" 2>/dev/null | head -6 | sed 's/^/  /'
                fi
                echo ""
                
                # Key actions used
                echo "**Key Actions:**"
                grep -E "uses: .*/.*@" "$workflow" 2>/dev/null | sed 's/.*/  - &/' | head -8
                echo ""
                
                echo "---"
                echo ""
            fi
        done
    }
    
    # Main repo workflows
    scan_workflows "." "conxian-business (main)"
    
    # Submodules
    for repo in "${REPOS[@]}"; do
        scan_workflows "$repo" "$repo"
    done
    
} > "$OUTPUT_DIR/03_OPERATIONAL_cicd.md"

echo "✅ OPERATIONAL CI/CD complete"

# ============================================
# 4. SECURITY - Vulnerability Map
# ============================================
echo "🔒 [SECURITY] Scanning for vulnerabilities..."

{
    echo "# SECURITY - Vulnerability Map"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    echo "⚠️ Note: Full vulnerability scanning requires running \`cargo audit\` and \`npm audit\`"
    echo ""
    
    # Rust audit
    echo "## Rust Dependencies (Cargo)"
    echo ""
    
    for repo in . "${REPOS[@]}"; do
        full_path="$REPO_ROOT/$repo"
        if [ -f "$full_path/Cargo.toml" ]; then
            echo "### $repo"
            echo ""
            if [ -f "$full_path/Cargo.lock" ]; then
                # Check if cargo-audit is available
                if command -v cargo-audit &> /dev/null; then
                    echo "\`\`\`bash"
                    echo "$ cd $repo && cargo audit 2>&1 | head -30"
                    echo "\`\`\`"
                    echo ""
                    (cd "$full_path" && cargo audit 2>&1 | head -30 || echo "cargo audit not available")
                else
                    echo "*Cargo.lock present - run \`cargo install cargo-audit && cd $repo && cargo audit\` for full audit*"
                    echo ""
                    echo "**Key dependencies:**"
                    grep -E "^name = " "$full_path/Cargo.lock" 2>/dev/null | head -15 | sed 's/^name = "//;s/"$//' | sed 's/^/  - /'
                fi
            else
                echo "*No Cargo.lock - dependencies not locked*"
            fi
            echo ""
            echo "---"
            echo ""
        fi
    done
    
    # NPM audit
    echo "## Node.js Dependencies (npm)"
    echo ""
    
    for repo in . "${REPOS[@]}" "${MAIN_REPO_CONTEXTS[@]}" apps/* packages/*; do
        full_path="$REPO_ROOT/$repo"
        if [ -f "$full_path/package.json" ]; then
            echo "### $repo"
            echo ""
            if [ -f "$full_path/pnpm-lock.yaml" ] || [ -f "$full_path/package-lock.json" ]; then
                if command -v pnpm &> /dev/null; then
                    echo "*Run \`cd $repo && pnpm audit\` for full vulnerability scan*"
                elif command -v npm &> /dev/null; then
                    echo "*Run \`cd $repo && npm audit\` for full vulnerability scan*"
                fi
                
                echo ""
                echo "**Key dependencies:**"
                grep -E '"@conxian/' "$full_path/package.json" 2>/dev/null | sed 's/.*"/  - @conxian/' | sed 's/".*//'
                grep -E '"@(stacks|bitcoin|near|chia):' "$full_path/package.json" 2>/dev/null | sed 's/.*"/  - &/' | sed 's/".*//'
            else
                echo "*No lockfile - run \`pnpm install\` first*"
            fi
            echo ""
            echo "---"
            echo ""
        fi
    done
    
    # Gitleaks scan
    echo "## Secret Scanning"
    echo ""
    if [ -f "$REPO_ROOT/.gitleaks.toml" ]; then
        echo "**Gitleaks configured:** ✅"
        echo "Config: \`.gitleaks.toml\`"
        grep -E "^title|allow|paths" "$REPO_ROOT/.gitleaks.toml" 2>/dev/null | head -10
    fi
    echo ""
    
} > "$OUTPUT_DIR/04_SECURITY_vulnerabilities.md"

echo "✅ SECURITY vulnerabilities complete"

# ============================================
# 5. LOGICAL - Decision Context
# ============================================
echo "📝 [LOGICAL] Documenting decision context..."

{
    echo "# LOGICAL - Decision Context & Purpose"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    # Main repo
    echo "## conxian-business (Main Repository)"
    echo ""
    echo "### Purpose"
    if [ -f "$REPO_ROOT/README.md" ]; then
        head -20 "$REPO_ROOT/README.md" 2>/dev/null | grep -v "^#" | head -10
    fi
    echo ""
    echo "### Scope"
    echo "- Monorepo containing multiple submodules"
    echo "- Shared CI/CD and governance"
    echo "- Cross-repo dependency management"
    echo ""
    echo "### Team Ownership"
    echo "- Primary: Conxian Core Team"
    echo "- Branches: dev, staged, main (trunk-based)"
    echo ""
    echo "---"
    echo ""
    
    # Per-repo context from README
    declare -A REPO_PURPOSE=(
        ["conxian-gateway"]="API Gateway for Conxian services"
        ["conxius-wallet"]="User wallet interface and key management"
        ["conxian-nexus"]="Nexus - central coordination service"
        ["conxian-ui"]="Conxian UI - frontend application"
        ["Conxian"]="Core protocol implementation"
        ["conxius-platform"]="Platform services and infrastructure"
        ["conxius-orbit"]="Orbit - peripheral/edge services"
        ["conxian-labs-site"]="Conxian Labs website"
        ["conxius-enclave-sdk"]="SDK for secure enclave operations"
        ["lib-conxian-core"]="Shared Rust core library (🔗 dependency hub)"
    )
    
    for repo in "${REPOS[@]}"; do
        full_path="$REPO_ROOT/$repo"
        
        echo "## $repo"
        echo ""
        
        # Known purpose
        if [ -n "${REPO_PURPOSE[$repo]}" ]; then
            echo "### Known Purpose"
            echo "${REPO_PURPOSE[$repo]}"
            echo ""
        fi
        
        # Extract from README
        if [ -f "$full_path/README.md" ]; then
            echo "### Description (from README)"
            head -15 "$full_path/README.md" 2>/dev/null | grep -v "^#" | head -8
            echo ""
        fi
        
        # Language/tech stack
        echo "### Technology Stack"
        [ -f "$full_path/Cargo.toml" ] && echo "- **Language:** Rust"
        [ -f "$full_path/package.json" ] && echo "- **Language:** TypeScript/JavaScript"
        [ -f "$full_path/Cargo.toml" ] && [ -f "$full_path/package.json" ] && echo "- **Mixed:** Rust + TypeScript"
        [ -f "$full_path/Clarinet.toml" ] && echo "- **Blockchain:** Clarity (Stacks)"
        [ ! -f "$full_path/Cargo.toml" ] && [ ! -f "$full_path/package.json" ] && echo "- Unknown"
        echo ""
        
        # Dependencies on lib-conxian-core
        if [ -f "$full_path/Cargo.toml" ] && grep -q "lib-conxian-core" "$full_path/Cargo.toml" 2>/dev/null; then
            echo "### Dependencies"
            echo "- 🔗 **lib-conxian-core** (core shared library)"
        fi
        if [ -f "$full_path/package.json" ] && grep -q "lib-conxian-core" "$full_path/package.json" 2>/dev/null; then
            echo "### Dependencies"
            echo "- 🔗 **lib-conxian-core** (core shared library)"
        fi
        
        echo ""
        echo "---"
        echo ""
    done
    
} > "$OUTPUT_DIR/05_LOGICAL_context.md"

echo "✅ LOGICAL context complete"

# ============================================
# SUMMARY
# ============================================
echo ""
echo "📊 [SUMMARY] Generating summary..."

{
    echo "{"
    echo "  \"generated\": \"$(date -Iseconds)\","
    echo "  \"repository\": \"Conxian/conxian-business\","
    echo "  \"scan_summary\": {"
    echo "    \"total_submodules\": ${#REPOS[@]},"
    echo "    \"repos_scanned\": ["
    
    first=true
    for repo in "${REPOS[@]}"; do
        [ "$first" = true ] && first=false || echo ","
        echo -n "      \"$repo\""
    done
    echo ""
    echo "    ],"
    echo "    \"apps_scanned\": ["
    first=true
    for pkg in apps/*; do
        [ -d "$pkg" ] || continue
        [ "$first" = true ] && first=false || echo ","
        echo -n "      \"$pkg\""
    done
    echo ""
    echo "    ],"
    echo "    \"packages_scanned\": ["
    first=true
    for pkg in packages/*; do
        [ -d "$pkg" ] || continue
        [ "$first" = true ] && first=false || echo ","
        echo -n "      \"$pkg\""
    done
    echo ""
    echo "    ]"
    echo "  },"
    echo "  \"tech_stack\": {"
    echo "    \"languages\": [\"Rust\", \"TypeScript\", \"JavaScript\", \"Clarity (Stacks)\"],"
    echo "    \"package_managers\": [\"Cargo\", \"pnpm\", \"npm\"],"
    echo "    \"blockchain\": [\"Stacks (Clarity)\"]"
    echo "  },"
    echo "  \"output_files\": ["
    echo "    \"01_SPATIAL_inventory.md\","
    echo "    \"02_RELATIONAL_dependencies.md\","
    echo "    \"03_OPERATIONAL_cicd.md\","
    echo "    \"04_SECURITY_vulnerabilities.md\","
    echo "    \"05_LOGICAL_context.md\""
    echo "  ]"
    echo "}"
} > "$OUTPUT_DIR/summary.json"

echo "=============================================="
echo "✅ Ecosystem scan complete!"
echo "=============================================="
echo ""
echo "Output files:"
ls -la "$OUTPUT_DIR/"
echo ""
echo "Quick view commands:"
echo "  cat $OUTPUT_DIR/summary.json"
echo "  cat $OUTPUT_DIR/01_SPATIAL_inventory.md"
echo "  cat $OUTPUT_DIR/02_RELATIONAL_dependencies.md"
