#!/usr/bin/env bash
# Setup script for the Conxian Sandbox devcontainer.

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SANDBOX_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd -- "$SANDBOX_ROOT"

ENV_FILE="$SANDBOX_ROOT/.env"
ENV_EXAMPLE="$SANDBOX_ROOT/.env.example"
SECRETS_DIR="$SANDBOX_ROOT/.secrets"
ENV_CREATED=0
TEMP_ENV_FILE=""

die() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

cleanup() {
    if [[ -n "$TEMP_ENV_FILE" && -e "$TEMP_ENV_FILE" ]]; then
        rm -f -- "$TEMP_ENV_FILE"
    fi
}

trap cleanup EXIT

env_key_count() {
    local key="$1"
    awk -v key="$key" \
        '$0 ~ "^[[:space:]]*" key "[[:space:]]*=" { count++ }
         END { print count + 0 }' \
        "$ENV_FILE"
}

env_value() {
    local key="$1"
    awk -v key="$key" '
        $0 ~ "^[[:space:]]*" key "[[:space:]]*=" {
            value = $0
            sub("^[[:space:]]*" key "[[:space:]]*=", "", value)
            sub("[[:space:]]+$", "", value)
            print value
            exit
        }
    ' "$ENV_FILE"
}

generate_credential() {
    if command -v openssl >/dev/null 2>&1; then
        openssl rand -hex 32
        return
    fi

    if command -v python3 >/dev/null 2>&1; then
        python3 - <<'PY'
import secrets

print(secrets.token_hex(32))
PY
        return
    fi

    die "cannot generate a local database credential: install openssl or python3"
}

write_generated_connection_url() {
    TEMP_ENV_FILE="$(mktemp "${ENV_FILE}.tmp.XXXXXX")"
    if ! DB_URL_TO_WRITE="$EXPECTED_DB_CONNECTION_URL" awk '
        BEGIN { updated = 0 }
        /^[[:space:]]*DB_CONNECTION_URL[[:space:]]*=/ {
            if (!updated) {
                print "DB_CONNECTION_URL=" ENVIRON["DB_URL_TO_WRITE"]
                updated = 1
            }
            next
        }
        { print }
        END {
            if (!updated) {
                print "DB_CONNECTION_URL=" ENVIRON["DB_URL_TO_WRITE"]
            }
        }
    ' "$ENV_FILE" > "$TEMP_ENV_FILE"; then
        die "could not prepare .env; remove the temporary file and retry"
    fi

    chmod 600 -- "$TEMP_ENV_FILE"
    mv -- "$TEMP_ENV_FILE" "$ENV_FILE"
    TEMP_ENV_FILE=""
}

printf '%s\n' 'Setting up Conxian Sandbox...'

[[ -f "$ENV_EXAMPLE" ]] || die "missing .env.example in sandbox root"
[[ -f "$SANDBOX_ROOT/.gitignore" ]] || die "missing sandbox .gitignore; refusing to create local secrets"
if ! grep -Eq '^[[:space:]]*\.secrets/[[:space:]]*(#.*)?$' "$SANDBOX_ROOT/.gitignore"; then
    die "sandbox .gitignore must protect .secrets/ before local credentials are created"
fi

if [[ -L "$SECRETS_DIR" ]]; then
    die ".secrets must be a real directory, not a symlink"
fi
if [[ -e "$SECRETS_DIR" && ! -d "$SECRETS_DIR" ]]; then
    die ".secrets exists but is not a directory"
fi
mkdir -p -- "$SECRETS_DIR"
chmod 700 -- "$SECRETS_DIR"

if [[ -L "$ENV_FILE" ]]; then
    die ".env must be a regular file, not a symlink"
fi
if [[ ! -e "$ENV_FILE" ]]; then
    printf '%s\n' 'Creating .env from .env.example...'
    cp -- "$ENV_EXAMPLE" "$ENV_FILE"
    chmod 600 -- "$ENV_FILE"
    ENV_CREATED=1
elif [[ ! -f "$ENV_FILE" ]]; then
    die ".env exists but is not a regular file"
fi

for required_key in DB_CREDENTIAL_FILE DB_CONNECTION_URL; do
    if [[ "$(env_key_count "$required_key")" != '1' ]]; then
        die ".env must contain exactly one ${required_key}= entry"
    fi
done

POSTGRES_DB="$(env_value POSTGRES_DB)"
POSTGRES_USER="$(env_value POSTGRES_USER)"
POSTGRES_DB="${POSTGRES_DB:-conxian}"
POSTGRES_USER="${POSTGRES_USER:-conxian}"
if [[ ! "$POSTGRES_DB" =~ ^[A-Za-z0-9_.-]+$ || ! "$POSTGRES_USER" =~ ^[A-Za-z0-9_.-]+$ ]]; then
    die "POSTGRES_DB and POSTGRES_USER must contain only URL-safe identifier characters"
fi

DB_CREDENTIAL_SETTING="$(env_value DB_CREDENTIAL_FILE)"
if [[ -z "$DB_CREDENTIAL_SETTING" ]]; then
    die "DB_CREDENTIAL_FILE is empty; set it to a file under .secrets/"
fi
case "$DB_CREDENTIAL_SETTING" in
    ..|../*|*/../*|*/..)
        die "DB_CREDENTIAL_FILE must not contain parent-directory segments"
        ;;
esac

case "$DB_CREDENTIAL_SETTING" in
    .secrets/*|./.secrets/*)
        CREDENTIAL_FILE="$SANDBOX_ROOT/${DB_CREDENTIAL_SETTING#./}"
        ;;
    /*)
        case "$DB_CREDENTIAL_SETTING" in
            "$SECRETS_DIR"/*) CREDENTIAL_FILE="$DB_CREDENTIAL_SETTING" ;;
            *) die "DB_CREDENTIAL_FILE must point inside .secrets/" ;;
        esac
        ;;
    *)
        die "DB_CREDENTIAL_FILE must point inside .secrets/"
        ;;
esac
case "$CREDENTIAL_FILE" in
    "$SECRETS_DIR"/*) ;;
    *) die "DB_CREDENTIAL_FILE must point inside .secrets/" ;;
esac

CREDENTIAL_DIR="$(dirname -- "$CREDENTIAL_FILE")"
mkdir -p -- "$CREDENTIAL_DIR"
chmod 700 -- "$CREDENTIAL_DIR"

if [[ -L "$CREDENTIAL_FILE" ]]; then
    die "DB_CREDENTIAL_FILE must not be a symlink"
fi

DB_CONNECTION_URL="$(env_value DB_CONNECTION_URL)"
if [[ "$ENV_CREATED" != '1' && ! -e "$CREDENTIAL_FILE" ]]; then
    if [[ -z "$DB_CONNECTION_URL" ]]; then
        die "existing .env is incomplete: create DB_CREDENTIAL_FILE and matching DB_CONNECTION_URL"
    fi
    die "existing .env has a DB_CONNECTION_URL but DB_CREDENTIAL_FILE is absent; create the matching file"
fi

if [[ ! -e "$CREDENTIAL_FILE" ]]; then
    printf '%s\n' 'Generating local database credential...'
    CREDENTIAL="$(generate_credential)"
    [[ -n "$CREDENTIAL" ]] || die "credential generator returned an empty value"
    if ! (umask 077; printf '%s\n' "$CREDENTIAL" > "$CREDENTIAL_FILE"); then
        die "could not create DB_CREDENTIAL_FILE"
    fi
elif [[ ! -f "$CREDENTIAL_FILE" ]]; then
    die "DB_CREDENTIAL_FILE exists but is not a regular file"
else
    if ! awk 'NR > 1 { exit 1 }' "$CREDENTIAL_FILE"; then
        die "DB_CREDENTIAL_FILE must contain exactly one line"
    fi
    CREDENTIAL="$(<"$CREDENTIAL_FILE")"
fi

[[ -n "$CREDENTIAL" ]] || die "DB_CREDENTIAL_FILE is empty"
if [[ "$CREDENTIAL" =~ [[:space:]] ]]; then
    die "DB_CREDENTIAL_FILE must not contain whitespace"
fi
chmod 600 -- "$CREDENTIAL_FILE"

EXPECTED_DB_CONNECTION_URL="postgresql://${POSTGRES_USER}:${CREDENTIAL}@db:5432/${POSTGRES_DB}"
if [[ -z "$DB_CONNECTION_URL" ]]; then
    if [[ "$ENV_CREATED" != '1' ]]; then
        die "existing .env has an empty DB_CONNECTION_URL; set it to match DB_CREDENTIAL_FILE"
    fi
    write_generated_connection_url
    DB_CONNECTION_URL="$EXPECTED_DB_CONNECTION_URL"
fi
if [[ "$DB_CONNECTION_URL" != "$EXPECTED_DB_CONNECTION_URL" ]]; then
    die "DB_CONNECTION_URL does not match DB_CREDENTIAL_FILE; update both values together"
fi

if ! command -v docker >/dev/null 2>&1; then
    die "Docker CLI is required; install Docker with the Compose plugin and retry"
fi

COMPOSE_COMMAND=(docker compose)
if ! docker compose version >/dev/null 2>&1; then
    if command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
        COMPOSE_COMMAND=(docker-compose)
    else
        die "Docker Compose is unavailable; install the Docker Compose plugin and retry"
    fi
fi

if ! command -v pnpm >/dev/null 2>&1; then
    if ! command -v npm >/dev/null 2>&1; then
        die "pnpm is unavailable and npm is not installed"
    fi
    printf '%s\n' 'Installing pnpm...'
    npm install -g pnpm
fi

printf '%s\n' 'Installing dependencies...'
pnpm install

printf '%s\n' 'Starting Docker services...'
"${COMPOSE_COMMAND[@]}" --env-file .env up -d db redis

WAIT_SECONDS="${CONXIAN_SANDBOX_WAIT_SECONDS:-5}"
[[ "$WAIT_SECONDS" =~ ^[0-9]+$ ]] || die 'CONXIAN_SANDBOX_WAIT_SECONDS must be a non-negative integer'
if (( WAIT_SECONDS > 0 )); then
    printf 'Waiting %s seconds for services...\n' "$WAIT_SECONDS"
    sleep "$WAIT_SECONDS"
fi

printf '%s\n' ''
printf '%s\n' 'Setup complete!'
printf '%s\n' ''
printf '%s\n' "Run 'pnpm run example:hello-world' to get started."
printf '%s\n' 'Visit http://localhost:3000 for Gateway docs.'
