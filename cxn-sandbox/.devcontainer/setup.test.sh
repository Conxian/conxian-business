#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SANDBOX_SOURCE="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
SETUP_SCRIPT="$SANDBOX_SOURCE/.devcontainer/setup.sh"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/conxian-sandbox-bootstrap.XXXXXX")"

cleanup() {
    rm -rf -- "$TEST_ROOT"
}

trap cleanup EXIT

fail() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

make_fixture() {
    local name="$1"
    local root="$TEST_ROOT/$name"
    mkdir -p -- "$root/.devcontainer" "$root/bin" "$root/from-here"
    cp -- "$SANDBOX_SOURCE/.env.example" "$root/.env.example"
    cp -- "$SETUP_SCRIPT" "$root/.devcontainer/setup.sh"
    cat > "$root/.gitignore" <<'EOF'
.env
.secrets/
*.log
output.txt
status.txt
EOF

    cat > "$root/bin/pnpm" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
if [[ "${1:-}" == 'install' ]]; then
    : > "${FAKE_PNPM_MARKER:?}"
fi
EOF

    cat > "$root/bin/docker" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail

[[ "${1:-}" == 'compose' ]] || exit 2
shift
if [[ "${1:-}" == 'version' ]]; then
    exit 0
fi

[[ "${1:-}" == '--env-file' && "${2:-}" == '.env' ]] || exit 3
shift 2
[[ "${1:-}" == 'up' ]] || exit 4

[[ -d .secrets ]] || exit 5
[[ "$(stat -c '%a' .secrets)" == '700' ]] || exit 6
[[ -f .secrets/postgres_password ]] || exit 7
[[ "$(stat -c '%a' .secrets/postgres_password)" == '600' ]] || exit 8
DB_URL="$(awk -F= '$1 == "DB_CONNECTION_URL" { print substr($0, index($0, "=") + 1); exit }' .env)"
[[ -n "$DB_URL" ]] || exit 9
printf '%s\n' 'compose-ready' >> "${FAKE_DOCKER_LOG:?}"
EOF

    chmod +x "$root/bin/pnpm" "$root/bin/docker" "$root/.devcontainer/setup.sh"
    git -C "$root" init -q
    git -C "$root" config user.name 'CI fixture'
    git -C "$root" config user.email 'ci-fixture@example.invalid'
    git -C "$root" add .
    git -C "$root" commit -qm fixture
    printf '%s\n' "$root"
}

run_setup() {
    local root="$1"
    local output="$2"
    (
        cd -- "$root/from-here"
        PATH="$root/bin:$PATH" \
            FAKE_DOCKER_LOG="$root/docker.log" \
            FAKE_PNPM_MARKER="$root/pnpm.log" \
            CONXIAN_SANDBOX_WAIT_SECONDS=0 \
            bash "$root/.devcontainer/setup.sh"
    ) > "$output" 2>&1
}

assert_no_credential_leak() {
    local root="$1"
    local output="$2"
    if [[ -f "$root/.secrets/postgres_password" ]]; then
        local credential
        credential="$(<"$root/.secrets/postgres_password")"
        if grep -Fq -- "$credential" "$output"; then
            fail 'bootstrap output contains the generated credential'
        fi
        if [[ -s "$root/status.txt" ]] && grep -Fq -- "$credential" "$root/status.txt"; then
            fail 'git status contains the generated credential'
        fi
    fi
}

assert_clean_git_status() {
    local root="$1"
    git -C "$root" status --porcelain --untracked-files=all > "$root/status.txt"
    [[ ! -s "$root/status.txt" ]] || fail 'bootstrap left tracked or unignored files in git status'
}

test_clean_bootstrap() {
    local root output
    root="$(make_fixture clean)"
    output="$root/output.txt"
    run_setup "$root" "$output"
    grep -Fxq 'compose-ready' "$root/docker.log" || fail 'Compose was not invoked after config preparation'
    [[ -e "$root/pnpm.log" ]] || fail 'dependency installation did not run'
    [[ "$(stat -c '%a' "$root/.secrets")" == '700' ]] || fail '.secrets is not mode 0700'
    [[ "$(stat -c '%a' "$root/.secrets/postgres_password")" == '600' ]] || fail 'credential file is not mode 0600'
    grep -Eq '^DB_CONNECTION_URL=postgresql://conxian:[^@[:space:]]+@db:5432/conxian$' "$root/.env" \
        || fail 'generated DB_CONNECTION_URL is not populated'
    assert_clean_git_status "$root"
    assert_no_credential_leak "$root" "$output"
}


if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    test_clean_bootstrap
    printf '%s\n' 'sandbox clean bootstrap test passed'
fi
