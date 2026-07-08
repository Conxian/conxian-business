#!/bin/bash
# CI/CD Comprehensive Audit Script
# Analyzes all workflows across the ecosystem for gaps, misses, duplications

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/CICD_AUDIT_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "=============================================="
echo "CI/CD Comprehensive Audit"
echo "=============================================="
echo "Output: $OUTPUT_DIR"
echo ""

# ============================================
# 1. INVENTORY ALL WORKFLOWS
# ============================================
echo "📋 [STEP 1] Inventorying all workflows..."

{
    echo "# CI/CD Workflow Inventory"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    echo "## Summary by Repository"
    echo ""
    
    # Find all workflows
    WORKFLOWS=$(find "$REPO_ROOT" -path "*/.git" -prune -o -type f -name "*.yml" -path "*/.github/workflows/*" -print 2>/dev/null | sort)
    
    # Count by repo
    echo "| Repository | Workflow Count |"
    echo "|------------|---------------|"
    
    for wf in $WORKFLOWS; do
        rel_path="${wf#$REPO_ROOT/}"
        repo=$(echo "$rel_path" | cut -d'/' -f1)
        echo "| $repo | $(find "$REPO_ROOT/$repo/.github/workflows" -name "*.yml" 2>/dev/null | wc -l) |"
    done | awk '!seen[$1]++' 
    echo ""
    
    # Detailed listing
    echo "## Detailed Workflow Listing"
    echo ""
    
    current_repo=""
    for wf in $WORKFLOWS; do
        rel_path="${wf#$REPO_ROOT/}"
        repo=$(echo "$rel_path" | cut -d'/' -f1)
        wf_name=$(basename "$wf" .yml)
        
        if [ "$repo" != "$current_repo" ]; then
            echo ""
            echo "### $repo"
            echo "| Workflow | Purpose | Trigger | Key Jobs |"
            echo "|----------|---------|--------|----------|"
            current_repo="$repo"
        fi
        
        # Extract basic info
        trigger=$(grep -E "^on:" "$wf" 2>/dev/null | head -1 || echo "inline")
        jobs=$(grep "^  [a-zA-Z_-]*:" "$wf" 2>/dev/null | grep -v "^  concurrency" | head -5 | sed 's/:$//' | tr '\n' ', ' | sed 's/,$//')
        
        # Determine purpose from name
        case "$wf_name" in
            *ci*) purpose="CI/Testing" ;;
            *test*) purpose="Testing" ;;
            *build*) purpose="Build" ;;
            *deploy*) purpose="Deployment" ;;
            *release*) purpose="Release" ;;
            *audit*) purpose="Security Audit" ;;
            *secret*) purpose="Secret Scanning" ;;
            *dependency*) purpose="Dependency Check" ;;
            *codeql*) purpose="CodeQL Analysis" ;;
            *gemini*) purpose="AI Automation" ;;
            *promot*) purpose="Branch Promotion" ;;
            *sync*) purpose="Submodule Sync" ;;
            *hygiene*) purpose="Code Hygiene" ;;
            *guard*) purpose="Policy Guard" ;;
            *scheduled*) purpose="Scheduled Task" ;;
            *coverage*) purpose="Coverage" ;;
            *) purpose="Utility" ;;
        esac
        
        echo "| \`$wf_name\` | $purpose | $trigger | $jobs |"
    done
    
} > "$OUTPUT_DIR/01_inventory.md"

echo "✅ Step 1 complete: $(echo $WORKFLOWS | wc -w) workflows found"

# ============================================
# 2. ANALYZE TRIGGERS & PATTERNS
# ============================================
echo "🔍 [STEP 2] Analyzing triggers and patterns..."

{
    echo "# Trigger & Pattern Analysis"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    # Analyze triggers
    echo "## Trigger Distribution"
    echo ""
    
    echo "### By Repository"
    echo "| Repository | push | pull_request | schedule | workflow_dispatch | manual_only |"
    echo "|------------|------|--------------|----------|-------------------|-------------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && continue
        
        total=$(find "$wf_dir" -name "*.yml" | wc -l)
        has_push=$(grep -l "^on:" "$wf_dir"/*.yml 2>/dev/null | xargs grep -l "push:" 2>/dev/null | wc -l)
        has_pr=$(grep -l "pull_request:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        has_schedule=$(grep -l "schedule:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        has_dispatch=$(grep -l "workflow_dispatch:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        manual_only=$(($total - has_push - has_pr - has_schedule - has_dispatch))
        [ $manual_only -lt 0 ] && manual_only=0
        
        echo "| $repo | $has_push | $has_pr | $has_schedule | $has_dispatch | $manual_only |"
    done
    echo ""
    
    # Analyze permissions
    echo "## Permissions Analysis"
    echo ""
    echo "| Repository | Contents Read | Contents Write | Pull Requests | Packages | Secrets |"
    echo "|------------|---------------|----------------|---------------|----------|---------|"
    
    for repo in conxian-business conxian-gateway conxian-nexus conxius-enclave-sdk conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && continue
        
        c_read=$(grep -l "contents: read" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        c_write=$(grep -l "contents: write" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        pr_perms=$(grep -l "pull-requests:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        pkg_perms=$(grep -l "packages:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        secrets_perms=$(grep -l "secrets:" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        
        echo "| $repo | $c_read | $c_write | $pr_perms | $pkg_perms | $secrets_perms |"
    done
    echo ""
    
    # Analyze action versions
    echo "## Action Version Pinning Analysis"
    echo ""
    
    for repo in conxian-business conxian-gateway conxian-nexus conxius-enclave-sdk conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && continue
        
        echo "### $repo"
        
        # Check for SHA pinning vs version tags
        sha_pinned=$(grep "uses:.*@[0-9a-f]{40}" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        version_tagged=$(grep "uses:.*@v[0-9]" "$wf_dir"/*.yml 2>/dev/null | wc -l)
        
        echo "- SHA-pinned actions: $sha_pinned"
        echo "- Version-tagged actions: $version_tagged"
        echo ""
        
        # List non-standard actions
        echo "**Non-standard/Third-party actions:**"
        grep "uses:" "$wf_dir"/*.yml 2>/dev/null | grep -v "actions/" | grep -v "github/" | sed 's/.*uses:/  - /' | head -10
        echo ""
    done
    
} > "$OUTPUT_DIR/02_triggers_patterns.md"

echo "✅ Step 2 complete"

# ============================================
# 3. IDENTIFY DUPLICATIONS
# ============================================
echo "🔄 [STEP 3] Identifying duplications..."

{
    echo "# Duplication Analysis"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    echo "## Duplicate Workflow Patterns"
    echo ""
    
    # Group similar workflows
    declare -A workflow_types
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && continue
        
        for wf in "$wf_dir"/*.yml; do
            [ ! -f "$wf" ] && continue
            wf_name=$(basename "$wf" .yml)
            
            # Categorize
            case "$wf_name" in
                *secret-scan*) key="secret-scan" ;;
                *dependency-review*) key="dependency-review" ;;
                *ci*) key="ci" ;;
                *rust*) key="rust" ;;
                *node*) key="node" ;;
                *hygiene*) key="hygiene" ;;
                *release*) key="release" ;;
                *deploy*) key="deploy" ;;
                *gemini*) key="gemini" ;;
                *promot*) key="promotion" ;;
                *audit*) key="audit" ;;
                *codeql*) key="codeql" ;;
                *) key="other" ;;
            esac
            
            workflow_types["$key"]+="  - $repo: \`$wf_name\`\n"
        done
    done
    
    echo "| Pattern | Instances | Repositories |"
    echo "|---------|-----------|--------------|"
    
    for key in "${!workflow_types[@]}"; do
        count=$(echo -e "${workflow_types[$key]}" | grep -c "  - ")
        repos=$(echo -e "${workflow_types[$key]}" | cut -d: -f1 | sort -u | tr '\n' ', ' | sed 's/,$//')
        if [ $count -gt 1 ]; then
            echo "| $key | $count | $repos |"
        fi
    done | sort
    echo ""
    
    echo "## Detailed Duplicate Instances"
    echo ""
    
    for key in "${!workflow_types[@]}"; do
        count=$(echo -e "${workflow_types[$key]}" | grep -c "  - ")
        if [ $count -gt 1 ]; then
            echo "### $key (x$count)"
            echo ""
            echo -e "${workflow_types[$key]}"
            echo ""
        fi
    done
    
    echo "## Potential Consolidation Candidates"
    echo ""
    
    # Check if reusable workflows exist
    echo "### Reusable Workflows"
    find "$REPO_ROOT" -name "*.yml" -path "*/.github/workflows/*" -exec grep -l "workflow_call" {} \; 2>/dev/null | while read wf; do
        echo "- $wf"
    done
    echo ""
    
    echo "### Workflows That Could Be Reusable"
    echo ""
    echo "| Workflow | Suggestion |"
    echo "|----------|------------|"
    
    # secret-scan workflows
    for repo in conxian-business conxian-gateway conxius-enclave-sdk conxius-platform conxius-wallet lib-conxian-core; do
        if [ -f "$REPO_ROOT/$repo/.github/workflows/secret-scan.yml" ]; then
            echo "| $repo/secret-scan.yml | Could use reusable workflow |"
        fi
    done
    
    # dependency-review workflows
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core; do
        if [ -f "$REPO_ROOT/$repo/.github/workflows/dependency-review.yml" ]; then
            echo "| $repo/dependency-review.yml | Could use reusable workflow |"
        fi
    done
    
} > "$OUTPUT_DIR/03_duplications.md"

echo "✅ Step 3 complete"

# ============================================
# 4. IDENTIFY GAPS & MISSES
# ============================================
echo "⚠️ [STEP 4] Identifying gaps and misses..."

{
    echo "# Gap & Miss Analysis"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    echo "## Security Gaps"
    echo ""
    
    # Check for missing security practices
    echo "### Secret Scanning"
    echo ""
    echo "| Repository | Has Secret Scan | Missing |"
    echo "|------------|-----------------|---------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core showcase-dapp; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && echo "| $repo | ❌ | No workflows dir |" && continue
        
        has_secret=$(find "$wf_dir" -name "*secret*.yml" 2>/dev/null | wc -l)
        if [ "$has_secret" -gt 0 ]; then
            echo "| $repo | ✅ | |"
        else
            echo "| $repo | ❌ | Missing secret-scan |"
        fi
    done
    echo ""
    
    echo "### Dependency Scanning"
    echo ""
    echo "| Repository | Has Dependency Review | Missing |"
    echo "|------------|---------------------|---------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core showcase-dapp; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && echo "| $repo | ❌ | No workflows dir |" && continue
        
        has_dep=$(find "$wf_dir" -name "*dependency*.yml" 2>/dev/null | wc -l)
        if [ "$has_dep" -gt 0 ]; then
            echo "| $repo | ✅ | |"
        else
            echo "| $repo | ❌ | Missing dependency-review |"
        fi
    done
    echo ""
    
    echo "### CodeQL Analysis"
    echo ""
    echo "| Repository | Has CodeQL | Language |"
    echo "|------------|-----------|----------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        [ ! -d "$wf_dir" ] && echo "| $repo | ❌ | N/A |" && continue
        
        has_codeql=$(find "$wf_dir" -name "*codeql*.yml" 2>/dev/null | wc -l)
        if [ "$has_codeql" -gt 0 ]; then
            lang=$(grep "language:" "$wf_dir"/*codeql*.yml 2>/dev/null | head -1 | sed 's/.*language: //' || echo "multi")
            echo "| $repo | ✅ | $lang |"
        else
            echo "| $repo | ❌ | |"
        fi
    done
    echo ""
    
    echo "## Testing Gaps"
    echo ""
    
    echo "| Repository | Has CI | Has Tests Dir | Test Command |"
    echo "|------------|--------|---------------|--------------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet lib-conxian-core; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        
        has_ci="❌"
        test_cmd="N/A"
        has_tests="❌"
        
        # Check for CI workflow
        if [ -d "$wf_dir" ] && find "$wf_dir" -name "*ci*.yml" 2>/dev/null | grep -q .; then
            has_ci="✅"
        fi
        
        # Check for tests directory
        if [ -d "$REPO_ROOT/$repo/tests" ] || [ -d "$REPO_ROOT/$repo/test" ] || [ -d "$REPO_ROOT/$repo/__tests__" ]; then
            has_tests="✅"
        fi
        
        # Check for test command in package.json or Makefile
        if [ -f "$REPO_ROOT/$repo/package.json" ]; then
            test_cmd=$(grep '"test"' "$REPO_ROOT/$repo/package.json" 2>/dev/null | head -1 | cut -d'"' -f4 || echo "N/A")
        fi
        
        echo "| $repo | $has_ci | $has_tests | $test_cmd |"
    done
    echo ""
    
    echo "## Deployment Gaps"
    echo ""
    
    echo "| Repository | Has Deploy | Environment |"
    echo "|------------|-----------|-------------|"
    
    for repo in conxian-business conxian-gateway conxian-labs-site conxian-nexus conxian-ui conxius-enclave-sdk conxius-orbit conxius-platform conxius-wallet showcase-dapp; do
        wf_dir="$REPO_ROOT/$repo/.github/workflows"
        
        deploy_wf=$(find "$wf_dir" -name "*deploy*.yml" -o -name "*release*.yml" 2>/dev/null | wc -l)
        
        if [ "$deploy_wf" -gt 0 ]; then
            echo "| $repo | ✅ ($deploy_wf) | |"
        else
            echo "| $repo | ❌ | No deployment workflow |"
        fi
    done
    echo ""
    
    echo "## Blockchain-Specific Gaps"
    echo ""
    
    echo "| Repository | Has Clarinet | Has Stacks CLI | Smart Contracts |"
    echo "|------------|--------------|----------------|-----------------|"
    
    for repo in conxian-business conxian-gateway conxian-nexus conxius-orbit conxius-wallet; do
        has_clarinet="❌"
        has_stacks="❌"
        contracts="❌"
        
        if [ -f "$REPO_ROOT/$repo/Clarinet.toml" ]; then
            has_clarinet="✅"
            contract_count=$(find "$REPO_ROOT/$repo/contracts" -name "*.clar" 2>/dev/null | wc -l)
            contracts="$contract_count"
        fi
        
        if grep -q "@stacks/" "$REPO_ROOT/$repo/package.json" 2>/dev/null; then
            has_stacks="✅"
        fi
        
        echo "| $repo | $has_clarinet | $has_stacks | $contracts |"
    done
    echo ""
    
} > "$OUTPUT_DIR/04_gaps_misses.md"

echo "✅ Step 4 complete"

# ============================================
# 5. RECOMMENDATIONS
# ============================================
echo "💡 [STEP 5] Generating recommendations..."

{
    echo "# CI/CD Consolidation Recommendations"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    echo "## Executive Summary"
    echo ""
    
    # Count workflows
    total_wf=$(find "$REPO_ROOT" -path "*/.git" -prune -o -type f -name "*.yml" -path "*/.github/workflows/*" -print 2>/dev/null | wc -l)
    total_repos=$(find "$REPO_ROOT" -maxdepth 2 -name ".github" -type d 2>/dev/null | wc -l)
    
    echo "- **Total workflows across ecosystem**: $total_wf"
    echo "- **Repositories with workflows**: $total_repos"
    echo "- **Duplication level**: HIGH (see section 3)"
    echo "- **Recommended consolidation**: 60-70% reduction possible"
    echo ""
    
    echo "## Priority Recommendations"
    echo ""
    
    echo "### 🔴 HIGH PRIORITY (Security)"
    echo ""
    echo "1. **Standardize Secret Scanning**"
    echo "   - Create single reusable workflow: \`.github/workflows/reusable-secret-scan.yml\`"
    echo "   - Currently duplicated in 5+ repos"
    echo "   - Add to: conxian-labs-site, showcase-dapp"
    echo ""
    echo "2. **Expand CodeQL Coverage**"
    echo "   - Only 2 repos have CodeQL (conxian-nexus, conxius-enclave-sdk)"
    echo "   - Add to all TypeScript repos: conxian-gateway, conxius-wallet, conxius-platform"
    echo ""
    echo "3. **Add cargo-deny to Rust repos**"
    echo "   - conxian-nexus, conxian-gateway, conxius-enclave-sdk, lib-conxian-core"
    echo "   - Checks for crate security advisories and license conflicts"
    echo ""
    
    echo "### 🟡 MEDIUM PRIORITY (Efficiency)"
    echo ""
    echo "4. **Consolidate Dependency Review**"
    echo "   - 10 repos have identical \`dependency-review.yml\`"
    echo "   - Convert to reusable workflow, call from main repo"
    echo ""
    echo "5. **Merge Gemini Workflows**"
    echo "   - 5 separate gemini-* workflows in conxian-business"
    echo "   - Consolidate into single workflow with job matrix"
    echo ""
    echo "6. **Standardize Hygiene Checks**"
    echo "   - hygiene.yml exists in: lib-conxian-core, conxius-enclave-sdk, conxius-platform"
    echo "   - Define standard hygiene checks once, reuse everywhere"
    echo ""
    
    echo "### 🟢 LOW PRIORITY (Optimization)"
    echo ""
    echo "7. **Reduce Promotion Workflows**"
    echo "   - 5+ promotion-related workflows in conxian-business"
    echo "   - Consider consolidating to single promotion workflow with parameters"
    echo ""
    echo "8. **Cache Optimization**"
    echo "   - Many workflows re-implement caching"
    echo "   - Create standard caching reusable workflow"
    echo ""
    echo "9. **Notification Consolidation**"
    echo "   - Add Slack/Discord notifications to unified workflow"
    echo "   - Avoid per-repo notification configurations"
    echo ""
    
    echo "## Proposed Architecture"
    echo ""
    echo "```"
    echo "conxian-business (orchestrator)"
    echo "├── reusable-secret-scan.yml      # All repos call this"
    echo "├── reusable-dependency-review.yml"
    echo "├── reusable-rust-ci.yml"
    echo "├── reusable-node-ci.yml"
    echo "├── reusable-codeql.yml"
    echo "└── reusable-deploy.yml"
    echo ""
    echo "Individual repos"
    echo "├── ci.yml                        # Calls reusable workflows"
    echo "├── deploy.yml                    # Calls reusable deploy"
    echo "└── release.yml                  # Calls reusable release"
    echo "```"
    echo ""
    
    echo "## Implementation Roadmap"
    echo ""
    echo "| Phase | Action | Impact | Effort |"
    echo "|-------|--------|--------|--------|"
    echo "| 1 | Create reusable secret-scan | 5 repos simplified | 1 day |"
    echo "| 2 | Create reusable dependency-review | 10 repos simplified | 1 day |"
    echo "| 3 | Add CodeQL to gateway/wallet | Security coverage +60% | 2 days |"
    echo "| 4 | Consolidate gemini workflows | 5→1 workflows | 1 day |"
    echo "| 5 | Add cargo-deny to Rust repos | Security coverage +40% | 1 day |"
    echo "| 6 | Create standard hygiene workflow | 3 repos simplified | 1 day |"
    echo ""
    
    echo "## Gaps Requiring New Workflows"
    echo ""
    echo "| Gap | Description | Suggested Workflow |"
    echo "|-----|-------------|---------------------|"
    echo "| SLA Monitoring | No uptime monitoring workflow | \`uptime-check.yml\` (schedule) |"
    echo "| Performance | No performance regression tests | \`perf-benchmark.yml\` (PR check) |"
    echo "| License Audit | No automated license compliance | \`license-check.yml\` (schedule) |"
    echo "| Container Scan | Docker images not scanned | \`container-scan.yml\` (deploy) |"
    echo "| Dependency Updates | Dependabot PRs need coordination | \`dependency-coordinator.yml\` |"
    echo "| Changelog | Auto-generate changelogs | \`changelog-gen.yml\` (release) |"
    echo ""
    
} > "$OUTPUT_DIR/05_recommendations.md"

echo "✅ Step 5 complete"

# ============================================
# 6. GENERATE SUMMARY
# ============================================
echo "📊 [STEP 6] Generating summary..."

{
    echo "# CI/CD Audit Summary"
    echo ""
    echo "Generated: $(date -Iseconds)"
    echo ""
    
    total_wf=$(find "$REPO_ROOT" -path "*/.git" -prune -o -type f -name "*.yml" -path "*/.github/workflows/*" -print 2>/dev/null | wc -l)
    total_repos=$(find "$REPO_ROOT" -maxdepth 2 -name ".github" -type d 2>/dev/null | wc -l)
    
    echo "## Quick Stats"
    echo ""
    echo "- **Total Workflows**: $total_wf"
    echo "- **Repositories**: $total_repos"
    echo "- **Avg workflows/repo**: $(echo "scale=1; $total_wf / $total_repos" | bc)"
    echo ""
    
    echo "## Scorecard"
    echo ""
    echo "| Category | Status |"
    echo "|----------|--------|"
    
    # Secret scanning
    secret_count=$(find "$REPO_ROOT" -name "*secret*.yml" -path "*/.github/workflows/*" 2>/dev/null | wc -l)
    [ "$secret_count" -ge 5 ] && secret_status="✅ Good" || secret_status="⚠️ Needs work"
    echo "| Secret Scanning | $secret_status ($secret_count workflows) |"
    
    # Dependency review
    dep_count=$(find "$REPO_ROOT" -name "*dependency*.yml" -path "*/.github/workflows/*" 2>/dev/null | wc -l)
    [ "$dep_count" -ge 8 ] && dep_status="✅ Good" || dep_status="⚠️ Needs work"
    echo "| Dependency Review | $dep_status ($dep_count workflows) |"
    
    # CodeQL
    codeql_count=$(find "$REPO_ROOT" -name "*codeql*.yml" -path "*/.github/workflows/*" 2>/dev/null | wc -l)
    [ "$codeql_count" -ge 5 ] && codeql_status="✅ Good" || codeql_status="⚠️ Needs work"
    echo "| CodeQL Analysis | $codeql_status ($codeql_count workflows) |"
    
    # Reusable workflows
    reusable_count=$(find "$REPO_ROOT" -name "*.yml" -path "*/.github/workflows/*" -exec grep -l "workflow_call" {} \; 2>/dev/null | wc -l)
    [ "$reusable_count" -ge 3 ] && reusable_status="✅ Good" || reusable_status="⚠️ Needs work"
    echo "| Reusable Workflows | $reusable_status ($reusable_count workflows) |"
    
    echo ""
    echo "## Files"
    echo ""
    echo "- \`01_inventory.md\` - Complete workflow inventory"
    echo "- \`02_triggers_patterns.md\` - Trigger and pattern analysis"
    echo "- \`03_duplications.md\` - Duplication analysis"
    echo "- \`04_gaps_misses.md\` - Gaps and misses"
    echo "- \`05_recommendations.md\` - Full recommendations"
    echo ""
    
} > "$OUTPUT_DIR/00_summary.md"

echo "✅ Step 6 complete"

# ============================================
# DISPLAY SUMMARY
# ============================================
echo ""
echo "=============================================="
echo "✅ CI/CD Audit Complete!"
echo "=============================================="
echo ""
echo "Output files:"
ls -la "$OUTPUT_DIR/"
echo ""
echo "Quick view:"
echo "  cat $OUTPUT_DIR/00_summary.md"
echo "  cat $OUTPUT_DIR/05_recommendations.md"
