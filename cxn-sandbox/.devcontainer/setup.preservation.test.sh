#!/usr/bin/env bash

set -Eeuo pipefail

TEST_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=setup.test.sh
source "$TEST_SCRIPT_DIR/setup.test.sh"

test_existing_configuration_preserved() {
    local root output env_hash_before credential_hash_before
    root="$(make_fixture preserved)"
    mkdir -p "$root/.secrets"
    printf '%s\n' 'fixture-credential-value' > "$root/.secrets/postgres_password"
    chmod 640 "$root/.secrets/postgres_password"
    chmod 750 "$root/.secrets"
    cat > "$root/.env" <<'EOF'
POSTGRES_DB=conxian
POSTGRES_USER=conxian
DB_CREDENTIAL_FILE=./.secrets/postgres_password
DB_CONNECTION_URL=postgresql://conxian:fixture-credential-value@db:5432/conxian
REDIS_URL=redis://redis:6379
EOF
    env_hash_before="$(sha256sum "$root/.env" | cut -d' ' -f1)"
    credential_hash_before="$(sha256sum "$root/.secrets/postgres_password" | cut -d' ' -f1)"
    output="$root/output.txt"
    run_setup "$root" "$output"
    [[ "$(sha256sum "$root/.env" | cut -d' ' -f1)" == "$env_hash_before" ]] \
        || fail 'existing .env was changed'
    [[ "$(sha256sum "$root/.secrets/postgres_password" | cut -d' ' -f1)" == "$credential_hash_before" ]] \
        || fail 'existing credential file was changed'
    [[ "$(stat -c '%a' "$root/.secrets")" == '700' ]] || fail 'existing .secrets was not protected'
    [[ "$(stat -c '%a' "$root/.secrets/postgres_password")" == '600' ]] || fail 'existing credential file was not protected'
    assert_clean_git_status "$root"
    assert_no_credential_leak "$root" "$output"
}

test_incomplete_configuration_fails() {
    local root output
    root="$(make_fixture incomplete)"
    mkdir -p "$root/.secrets"
    printf '%s\n' 'fixture-credential-value' > "$root/.secrets/postgres_password"
    cat > "$root/.env" <<'EOF'
POSTGRES_DB=conxian
POSTGRES_USER=conxian
DB_CREDENTIAL_FILE=./.secrets/postgres_password
DB_CONNECTION_URL=
REDIS_URL=redis://redis:6379
EOF
    output="$root/output.txt"
    if run_setup "$root" "$output"; then
        fail 'incomplete existing configuration unexpectedly passed'
    fi
    [[ ! -f "$root/docker.log" || ! -s "$root/docker.log" ]] \
        || fail 'Compose ran for an incomplete configuration'
    assert_clean_git_status "$root"
    assert_no_credential_leak "$root" "$output"
}

test_missing_credential_configuration_fails() {
    local root output
    root="$(make_fixture missing-credential)"
    cat > "$root/.env" <<'EOF'
POSTGRES_DB=conxian
POSTGRES_USER=conxian
DB_CREDENTIAL_FILE=./.secrets/postgres_password
DB_CONNECTION_URL=
REDIS_URL=redis://redis:6379
EOF
    output="$root/output.txt"
    if run_setup "$root" "$output"; then
        fail 'configuration without a credential file unexpectedly passed'
    fi
    [[ ! -e "$root/.secrets/postgres_password" ]] \
        || fail 'bootstrap generated a credential for incomplete existing configuration'
    [[ ! -f "$root/docker.log" || ! -s "$root/docker.log" ]] \
        || fail 'Compose ran for configuration without a credential file'
    assert_clean_git_status "$root"
    assert_no_credential_leak "$root" "$output"
}
