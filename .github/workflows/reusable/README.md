# Reusable GitHub Workflows

Centralized CI/CD workflows for the Conxian ecosystem. All submodules should use these instead of duplicating workflow logic.

## Available Workflows

| Workflow | Purpose | Languages |
|----------|---------|-----------|
| `rust-ci.yml` | Rust CI pipeline | Rust |
| `node-ci.yml` | Node.js CI pipeline | TypeScript/JavaScript |
| `codeql.yml` | CodeQL security analysis | TypeScript, Rust |
| `secret-scan.yml` | Secret scanning | All |
| `dependency-review.yml` | Dependency vulnerability review | All |
| `hygiene.yml` | Code hygiene checks | All |

## Usage

### From Rust Repos

```yaml
name: CI

on:
  push:
    branches: [main, staged, dev]
  pull_request:
    branches: [main, staged, dev]

jobs:
  ci:
    name: Rust CI
    uses: Conxian/conxian-business/.github/workflows/reusable/rust-ci.yml@main
    # Optional inputs:
    # with:
    #   rust_version: "1.96.0"
```

### From Node.js Repos

```yaml
name: CI

on:
  push:
    branches: [main, staged, dev]
  pull_request:
    branches: [main, staged, dev]

jobs:
  ci:
    name: Node.js CI
    uses: Conxian/conxian-business/.github/workflows/reusable/node-ci.yml@main
    # Optional inputs:
    # with:
    #   node_version: "20"
    #   pnpm_version: "10"
```

### CodeQL Analysis

```yaml
jobs:
  codeql:
    name: CodeQL
    uses: Conxian/conxian-business/.github/workflows/reusable/codeql.yml@main
    with:
      languages: typescript  # or: rust, javascript
```

### Secret Scanning

```yaml
jobs:
  secret-scan:
    name: Secret Scan
    uses: Conxian/conxian-business/.github/workflows/reusable/secret-scan.yml@main
```

### Dependency Review

```yaml
jobs:
  dependency-review:
    name: Dependency Review
    uses: Conxian/conxian-business/.github/workflows/reusable/dependency-review.yml@main
```

### Hygiene Checks

```yaml
jobs:
  hygiene:
    name: Hygiene
    uses: Conxian/conxian-business/.github/workflows/reusable/hygiene.yml@main
```

## Unified CI

The `unified-ci.yml` workflow combines all checks:

```yaml
name: CI

on:
  push:
    branches: [main, staged, dev]
    paths-ignore:
      - '**.md'
      - 'docs/**'
  pull_request:
    branches: [main, staged, dev]
    paths-ignore:
      - '**.md'
      - 'docs/**'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  ci:
    name: CI
    uses: Conxian/conxian-business/.github/workflows/unified-ci.yml@main
```

## Key Features

### Built-in Optimizations

- **Concurrency Control**: Automatically cancels in-progress runs on new pushes
- **Path Filtering**: Skip CI on documentation-only changes
- **Caching**: Automatic caching for Cargo, pnpm, npm
- **Parallel Jobs**: Jobs run in parallel where possible

### Security

- **Secret Scanning**: Gitleaks + TruffleHog
- **Dependency Review**: Action dependency review
- **CodeQL**: Security vulnerability detection
- **cargo-deny**: Rust-specific security (license + advisories)

### Hygiene

- No merge conflict markers
- No debug statements in production
- No TODOs in source (configurable)
- No large binary files
- No trailing whitespace

## Migration

Run the migration script to update all submodules:

```bash
./scripts/migrate-to-reusable-workflows.sh
```

## Versioning

Workflows use semantic versioning via git tags:

- `@main` - Bleeding edge (may break)
- `@latest` - Stable (recommended)
- `@v1` - Major version
- `@v1.2.3` - Exact version

## Contributing

When modifying reusable workflows:

1. Test in a PR to `conxian-business`
2. Verify all calling repos work correctly
3. Update this README if adding new workflows
4. Tag a new version after merging
