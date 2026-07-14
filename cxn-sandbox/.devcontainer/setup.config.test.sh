#!/usr/bin/env bash

set -Eeuo pipefail

TEST_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=setup.preservation.test.sh
source "$TEST_SCRIPT_DIR/setup.preservation.test.sh"

test_existing_configuration_preserved
test_incomplete_configuration_fails
test_missing_credential_configuration_fails
printf '%s\n' 'sandbox preservation and incomplete bootstrap tests passed'
