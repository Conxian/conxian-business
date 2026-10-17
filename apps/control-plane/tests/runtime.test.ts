import assert from "node:assert/strict";
import { afterEach, test } from "node:test";
import { resolveControlPlaneRuntimeConfig } from "../lib/runtime-config";
import { runtimeRequestOptions } from "../lib/runtime-requests";
import { getAuditData, getEnvironmentData, getPolicyApprovalData, getReleaseGovernanceData } from "../lib/module-adapters";
import { requestReleaseApprovalV1, submitGovernanceDecisionV1, submitReleaseDecisionV1 } from "../lib/workflow-clients";

const keys = ["CONXIAN_ADMIN_RUNTIME_BASE_URL", "ADMIN_RUNTIME_BASE_URL", "CONXIAN_ADMIN_RUNTIME_READ_TOKEN", "CONXIAN_ADMIN_RUNTIME_WRITE_TOKEN"];
const originalEnvironment = Object.fromEntries(keys.map(key => [key, process.env[key]]));
const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
  for (const key of keys) {
    const value = originalEnvironment[key];
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
});

function configure() {
  process.env.CONXIAN_ADMIN_RUNTIME_BASE_URL = "https://runtime.example";
  process.env.CONXIAN_ADMIN_RUNTIME_READ_TOKEN = "test-read-token";
  process.env.CONXIAN_ADMIN_RUNTIME_WRITE_TOKEN = "test-write-token";
}

test("missing origin fails before any network request", async () => {
  for (const key of keys) delete process.env[key];
  globalThis.fetch = async () => { assert.fail("must not fetch without configuration"); };
  await assert.rejects(async () => getReleaseGovernanceData(), /CONXIAN_ADMIN_RUNTIME_BASE_URL/);
});

test("read and write credentials are independently required", () => {
  const env = { CONXIAN_ADMIN_RUNTIME_BASE_URL: "https://runtime.example", CONXIAN_ADMIN_RUNTIME_READ_TOKEN: "read-only" };
  assert.equal(resolveControlPlaneRuntimeConfig("read", env).token, "read-only");
  assert.throws(() => resolveControlPlaneRuntimeConfig("write", env), /WRITE_TOKEN/);
});

test("invalid origins never expose their contents in configuration errors", () => {
  const badOrigins = ["not-a-url", "https://user:private@runtime.example", "https://runtime.example/admin/v1", "https://runtime.example?secret=private", "https://runtime.example#private", "http://runtime.example", "ftp://runtime.example"];
  for (const origin of badOrigins) {
    assert.throws(() => resolveControlPlaneRuntimeConfig("read", {
      NODE_ENV: "production", CONXIAN_ADMIN_RUNTIME_BASE_URL: origin, CONXIAN_ADMIN_RUNTIME_READ_TOKEN: "test-only",
    }), error => error instanceof Error && !error.message.includes("private"));
  }
});

test("loopback HTTP is development-only; whitespace and legacy origin are normalized", () => {
  const env = { NODE_ENV: "development", ADMIN_RUNTIME_BASE_URL: " http://127.0.0.1:3900/ ", CONXIAN_ADMIN_RUNTIME_READ_TOKEN: " test-only " };
  assert.equal(resolveControlPlaneRuntimeConfig("read", env).runtimeBaseUrl, "http://127.0.0.1:3900");
  assert.throws(() => resolveControlPlaneRuntimeConfig("read", { ...env, NODE_ENV: "production" }), /HTTPS/);
});

test("all read adapters send read credentials and preserve empty API results", async () => {
  configure();
  const envelopes: Record<string, unknown> = {
    "/admin/v1/releases": { releases: [] },
    "/admin/v1/audit-events": { events: [] },
    "/admin/v1/governance-actions": { governanceActions: [] },
    "/admin/v1/environments": { environments: [] },
  };
  const seen: string[] = [];
  globalThis.fetch = async (input, init) => {
    const path = new URL(String(input)).pathname;
    seen.push(path);
    assert.equal(new Headers(init?.headers).get("authorization"), "Bearer test-read-token");
    assert.equal(init?.cache, "no-store");
    assert.equal(init?.redirect, "error");
    assert.ok(init?.signal instanceof AbortSignal);
    return Response.json(envelopes[path]);
  };
  for (const read of [getReleaseGovernanceData, getAuditData, getPolicyApprovalData, getEnvironmentData]) {
    assert.deepEqual(await read(), []);
  }
  assert.equal(seen.length, 4);
});

for (const status of [401, 403, 500, 503]) {
  test(`HTTP ${status} remains a failure instead of sample data`, async () => {
    configure();
    globalThis.fetch = async () => Response.json({ error: "unavailable" }, { status });
    await assert.rejects(getReleaseGovernanceData(), (error: unknown) =>
      error instanceof Error && "status" in error && error.status === status);
  });
}

test("transport failures remain failures", async () => {
  configure();
  globalThis.fetch = async () => { throw new TypeError("network unavailable"); };
  await assert.rejects(getAuditData(), /network unavailable/);
});

test("workflow clients use write credentials for every mutation", async () => {
  configure();
  const paths: string[] = [];
  globalThis.fetch = async (input, init) => {
    paths.push(new URL(String(input)).pathname);
    assert.equal(init?.method, "POST");
    assert.equal(new Headers(init?.headers).get("authorization"), "Bearer test-write-token");
    assert.equal(init?.redirect, "error");
    return Response.json({ accepted: true, message: "test response" });
  };
  await requestReleaseApprovalV1({ artifactId: "test", requestedBy: "test-actor", notes: "test" });
  await submitReleaseDecisionV1({ artifactId: "test", actorId: "test-actor", decision: "reject", notes: "test" });
  await submitGovernanceDecisionV1({ actionId: "test", actorId: "test-actor", decision: "reject", notes: "test" });
  assert.deepEqual(paths, ["/admin/v1/releases/request-approval", "/admin/v1/releases/decision", "/admin/v1/governance/decision"]);
});

test("request configuration does not retain a previous credential", () => {
  configure();
  const first = runtimeRequestOptions("read");
  process.env.CONXIAN_ADMIN_RUNTIME_READ_TOKEN = "rotated-test-token";
  const second = runtimeRequestOptions("read");
  assert.equal(new Headers(first.headers).get("authorization"), "Bearer test-read-token");
  assert.equal(new Headers(second.headers).get("authorization"), "Bearer rotated-test-token");
});
