#!/usr/bin/env python3
"""Retired unauthenticated admin-runtime emulator.

The canonical /admin/v1 API is owned by conxian-nexus. Repository metadata
cannot establish runtime readiness, attestations, or durable governance decisions.
This compatibility entrypoint deliberately starts no HTTP server.
"""

import sys


def main() -> int:
    print(
        "The local admin-runtime emulator is retired. Deploy the authenticated "
        "Conxian Nexus runtime and configure CONXIAN_ADMIN_RUNTIME_BASE_URL "
        "and the control-plane read/write credentials. See apps/control-plane/README.md.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
