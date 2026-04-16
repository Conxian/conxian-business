# Docker Compose reference stack

This repository includes a root `docker-compose.yml` that serves as a baseline operator / internal testing deployment for the Conxian runtime.

It brings up:

- Postgres (`db`)
- Redis (`redis`)
- Conxian Nexus (`nexus`)
- Conxian Gateway (`gateway`)

## Prerequisites

1. Docker + Docker Compose
2. Clone with submodules (or initialize them after cloning):

```bash
git submodule update --init --recursive
```

## Usage

Start infrastructure only:

```bash
docker-compose up -d db redis
```

Start the full stack (builds Nexus + Gateway images locally):

```bash
docker-compose up --build
```

## Ports

- Gateway: `http://localhost:3000`
- Nexus REST: `http://localhost:3001` (mapped from container port `3000`)
- Nexus gRPC: `localhost:50051`

## Configuration

The compose file provides safe local defaults for required Gateway secrets (for example `API_TOKEN`, `FIAT_WEBHOOK_SECRET`).

For operator installs, override these using environment variables or an `.env` file in the repository root.

> Note
> The Gateway defaults `BITCOIN_RPC_URL` to `https://bitcoin-rpc.publicnode.com` when not set. For production, funds-bearing, or privacy-sensitive workloads, set `BITCOIN_RPC_URL` to a controlled node or vetted provider before running.
