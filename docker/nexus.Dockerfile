# Build Stage
FROM rust:1.94.0-slim-bookworm@sha256:a86cada82e36ebd7a9bffed7548792c55a952fdb20718eea9278a936bcb76e62 AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends pkg-config libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN cargo build --release --locked --bin conxian-nexus

# Runtime Stage
FROM debian:bookworm-slim@sha256:7b140f374b289a7c2befc338f42ebe6441b7ea838a042bbd5acbfca6ec875818

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libssl3 ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin nexus

COPY --from=builder /app/target/release/conxian-nexus /usr/local/bin/conxian-nexus
COPY --from=builder /app/migrations /app/migrations

EXPOSE 3000 50051

ENV RUST_LOG=info \
    REST_PORT=3000 \
    GRPC_PORT=50051

USER nexus

CMD ["conxian-nexus"]
