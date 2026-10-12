export type RuntimeAccess = "read" | "write";

export class ControlPlaneRuntimeConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ControlPlaneRuntimeConfigError";
  }
}

export function resolveControlPlaneRuntimeConfig(
  access: RuntimeAccess,
  env: Record<string, string | undefined> = process.env,
) {
  const baseUrl = env.CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim() || env.ADMIN_RUNTIME_BASE_URL?.trim();
  if (!baseUrl) {
    throw new ControlPlaneRuntimeConfigError("Configure CONXIAN_ADMIN_RUNTIME_BASE_URL.");
  }
  let url: URL;
  try {
    url = new URL(baseUrl);
  } catch {
    throw new ControlPlaneRuntimeConfigError("Admin runtime base URL must be an absolute URL.");
  }
  const localHttp = env.NODE_ENV !== "production" && url.protocol === "http:" &&
    ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
  if (url.protocol !== "https:" && !localHttp) {
    throw new ControlPlaneRuntimeConfigError("Admin runtime requires HTTPS (local development may use loopback HTTP).");
  }
  if (url.username || url.password || url.search || url.hash || url.pathname !== "/") {
    throw new ControlPlaneRuntimeConfigError("Admin runtime base URL must be an origin without credentials, path, query, or fragment.");
  }
  const tokenKey = access === "read" ? "CONXIAN_ADMIN_RUNTIME_READ_TOKEN" : "CONXIAN_ADMIN_RUNTIME_WRITE_TOKEN";
  const token = env[tokenKey]?.trim();
  if (!token || /\s/.test(token)) {
    throw new ControlPlaneRuntimeConfigError(`Configure ${tokenKey} with a valid bearer token.`);
  }
  return { runtimeBaseUrl: url.origin, token };
}
