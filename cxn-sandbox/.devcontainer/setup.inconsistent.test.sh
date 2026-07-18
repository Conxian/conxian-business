#!/usr/bin/env bash

set -Eeuo pipefail

TEST_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=setup.test.sh
source "$TEST_SCRIPT_DIR/setup.test.sh"

test_inconsistent_configuration_fails() {
    local root output
    root="$(make_fixture inconsistent)"
    mkdir -p "$root/.secrets"
    printf '%s\n' 'fixture-credential-value' > "$root/.secrets/postgres_password"
    cat > "$root/.env" <<'EOF'
POSTGRES_DB=conxian
POSTGRES_USER=conxian
DB_CREDENTIAL_FILE=./.secrets/postgres_password
DB_CONNECTION_URL=postgresql://conxian:wrong-value@db:5432/conxian
REDIS_URL=redis://redis:6379
EOF
    output="$root/output.txt"
    if run_setup "$root" "$output"; then
        fail 'inconsistent existing configuration unexpectedly passed'
    fi
    [[ ! -f "$root/docker.log" || ! -s "$root/docker.log" ]] \
        || fail 'Compose ran for an inconsistent configuration'
    assert_clean_git_status "$root"
    assert_no_credential_leak "$root" "$output"
}

test_inconsistent_configuration_fails
printf '%s\n' 'sandbox inconsistent bootstrap test passed'
