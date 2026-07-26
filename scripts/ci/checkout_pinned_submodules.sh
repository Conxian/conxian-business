#!/usr/bin/env bash

set -Eeuo pipefail

MODE="${1:-all}"

case "$MODE" in
    all|market) ;;
    *)
        printf 'ERROR: usage: %s [all|market]\n' "$0" >&2
        exit 2
        ;;
esac

if [[ -z "${CI_SUBMODULES_PAT:-}" ]]; then
    printf '%s\n' 'ERROR: CI_SUBMODULES_PAT is required for pinned submodule checkout' >&2
    exit 1
fi

[[ -f .gitmodules ]] || {
    printf '%s\n' 'ERROR: .gitmodules is missing' >&2
    exit 1
}

export GIT_TERMINAL_PROMPT=0
git submodule sync --recursive

if [[ "$MODE" == 'all' ]]; then
    if ! git \
        -c submodule.Conxian.update=checkout \
        -c submodule.conxian-market.update=checkout \
        -c submodule.conxius-platform.update=checkout \
        submodule update --init --recursive; then
        printf '%s\n' 'ERROR: approved submodule checkout failed' >&2
        exit 1
    fi
else
    if ! git -c submodule.conxian-market.update=checkout submodule update --init conxian-market; then
        printf '%s\n' 'ERROR: pinned conxian-market checkout failed' >&2
        exit 1
    fi
fi

EXPECTED_MARKET_COMMIT="$(git rev-parse :conxian-market 2>/dev/null)" || {
    printf '%s\n' 'ERROR: conxian-market is not a pinned gitlink' >&2
    exit 1
}
ACTUAL_MARKET_COMMIT="$(git -C conxian-market rev-parse HEAD 2>/dev/null)" || {
    printf '%s\n' 'ERROR: conxian-market checkout is unavailable' >&2
    exit 1
}

if [[ "$EXPECTED_MARKET_COMMIT" != "$ACTUAL_MARKET_COMMIT" ]]; then
    printf '%s\n' 'ERROR: conxian-market checkout does not match the pinned gitlink' >&2
    exit 1
fi
