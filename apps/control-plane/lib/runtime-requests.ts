import type { AdminRuntimeRequestOptions } from "@conxian/client-sdk";
import { resolveControlPlaneRuntimeConfig, type RuntimeAccess } from "./runtime-config";

/** Called only by Server Components and authenticated server actions. */
export function runtimeRequestOptions(access: RuntimeAccess): AdminRuntimeRequestOptions {
  if (typeof window !== "undefined") throw new Error("Admin runtime access is server-only.");
  const { runtimeBaseUrl, token } = resolveControlPlaneRuntimeConfig(access);
  return {
    runtimeBaseUrl,
    headers: { authorization: `Bearer ${token}` },
    signal: AbortSignal.timeout(10_000),
    // Never cache operator data or forward credentials through a redirect.
    fetchImpl: (input, init) => fetch(input, { ...init, cache: "no-store", redirect: "error" }),
  };
}
