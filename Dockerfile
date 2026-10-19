FROM node:24-bookworm-slim AS build
WORKDIR /workspace
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm install --global pnpm@10.28.0
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/control-plane ./apps/control-plane
COPY packages/client-sdk ./packages/client-sdk
COPY packages/schemas ./packages/schemas
RUN pnpm --filter @conxian/control-plane... install --frozen-lockfile --ignore-scripts
RUN pnpm --filter @conxian/control-plane test
RUN pnpm --filter @conxian/control-plane build

FROM node:24-bookworm-slim AS runtime
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 HOSTNAME=0.0.0.0 PORT=10000
WORKDIR /app
COPY --from=build --chown=node:node /workspace/apps/control-plane/.next/standalone ./
COPY --from=build --chown=node:node /workspace/apps/control-plane/.next/static ./apps/control-plane/.next/static
USER node
EXPOSE 10000
CMD ["node", "apps/control-plane/server.js"]
