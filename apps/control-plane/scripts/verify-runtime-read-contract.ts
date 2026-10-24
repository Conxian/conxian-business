import { resolveControlPlaneRuntimeConfig } from "../lib/runtime-config";
import { CONTROL_PLANE_READ_PATHS, validateAdminRuntimePayload } from "../../../packages/client-sdk/src/runtime-contract";
import { basename } from "node:path";

async function boundedJson(response: Response): Promise<unknown> {
  const reader = response.body?.getReader();
  if (!reader) throw new Error("Empty response");
  const chunks: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > 1_048_576) throw new Error("Response exceeds probe limit");
      chunks.push(value);
    }
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } finally {
    await reader.cancel();
  }
}

/** Read-only operational probe. Does not publish payloads or perform admin writes. */
export async function verifyRuntimeReads(
  env: Record<string, string | undefined> = process.env,
  fetchImpl: typeof fetch = fetch,
) {
  const report = {
    observedAt: new Date().toISOString(),
    readContractPassed: false,
    sourceBindingVerified: false,
    durableWritesVerified: false,
    productionAcceptance: false,
    checks: [] as { path: string; anonymousDenied: boolean; authenticatedContractValid: boolean }[],
  };
  let config;
  try {
    // Remote probes always require HTTPS, even when launched from a developer host.
    config = resolveControlPlaneRuntimeConfig("read", { ...env, NODE_ENV: "production" });
  } catch {
    return report;
  }
  for (const path of CONTROL_PLANE_READ_PATHS) {
    const result = { path, anonymousDenied: false, authenticatedContractValid: false };
    for (const authenticated of [false, true]) {
      try {
        const response = await fetchImpl(config.runtimeBaseUrl + path, {
          method: "GET", redirect: "error", cache: "no-store", signal: AbortSignal.timeout(10_000),
          headers: authenticated ? { authorization: `Bearer ${config.token}`, accept: "application/json" }
            : { accept: "application/json" },
        });
        if (!authenticated) {
          result.anonymousDenied = !response.redirected && (response.status === 401 || response.status === 403);
          await response.body?.cancel();
        } else if (response.status === 200 && !response.redirected
          && response.headers.get("content-type")?.split(";")[0].trim() === "application/json") {
          validateAdminRuntimePayload(path, await boundedJson(response));
          result.authenticatedContractValid = true;
        } else {
          await response.body?.cancel();
        }
      } catch {
        // Do not print error messages: network/provider errors may contain private URLs or headers.
      }
    }
    report.checks.push(result);
  }
  report.readContractPassed = report.checks.every(check => check.anonymousDenied && check.authenticatedContractValid);
  return report;
}

if (process.argv[1] && basename(process.argv[1]) === "verify-runtime-read-contract.ts") {
  void verifyRuntimeReads().then(report => {
    console.log(JSON.stringify(report));
    process.exitCode = report.readContractPassed ? 0 : 1;
  });
}
