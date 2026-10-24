import assert from "node:assert/strict";
import { test } from "node:test";
import { AdminRuntimeContractError, CONTROL_PLANE_READ_PATHS, validateAdminRuntimePayload } from "../../../packages/client-sdk/src/runtime-contract";
import { requestAdminRuntimeJson } from "../../../packages/client-sdk/src/runtime-client";
import { verifyRuntimeReads } from "../scripts/verify-runtime-read-contract";

const now = "2026-10-23T15:00:00Z";
const health = { status: "unknown", message: "No qualified evidence", trustTier: "unknown",
  evidenceLevel: "none", lastUpdated: now };
const payloads: Record<string, unknown> = {
  "/admin/v1/releases": { releases: [] },
  "/admin/v1/governance-actions": { governanceActions: [] },
  "/admin/v1/audit-events": { events: [] },
  "/admin/v1/environments": { environments: [] },
  "/admin/v1/runtime/health": health,
  "/admin/v1/runtime/readiness": { ...health, ready: false, blockers: ["Not qualified"] },
};
const env = { CONXIAN_ADMIN_RUNTIME_BASE_URL: "https://private-origin.invalid",
  CONXIAN_ADMIN_RUNTIME_READ_TOKEN: "private-read-token" };

test("canonical empty lists and explicit unknown readiness remain truthful valid responses", () => {
  for (const path of CONTROL_PLANE_READ_PATHS) validateAdminRuntimePayload(path, payloads[path]);
  validateAdminRuntimePayload("/admin/v1/releases", []);
});

test("missing envelopes, invalid rows and duplicate IDs fail without reflecting payloads", () => {
  const path = "/admin/v1/releases";
  const valid = { id: "private-id", name: "A", owner: "operator", status: "draft", updatedAt: now };
  validateAdminRuntimePayload(path, { releases: [valid], futureExtension: true });
  for (const value of [undefined, null, {}, { releases: null }, { releases: ["private-value"] },
    { releases: [valid, valid] }, { releases: [{ ...valid, status: "healthy" }] },
    { releases: [{ ...valid, updatedAt: "2026-10-23" }] }]) {
    assert.throws(() => validateAdminRuntimePayload(path, value), error =>
      error instanceof AdminRuntimeContractError && !error.message.includes("private"));
  }
});

test("hard-coded ready without evidence and contradictory readiness cannot satisfy contract", () => {
  for (const value of [{ status: "ready", timestamp: now },
    { ...health, status: "ready", ready: true, blockers: [] },
    { ...health, ready: true, blockers: [] },
    { ...health, status: "ready", ready: false, blockers: [] }]) {
    assert.throws(() => validateAdminRuntimePayload("/admin/v1/runtime/readiness", value), AdminRuntimeContractError);
  }
});

test("environment strings cannot masquerade as canonical environment records", () => {
  assert.throws(() => validateAdminRuntimePayload("/admin/v1/environments",
    { environments: ["dev", "staging", "prod"] }), AdminRuntimeContractError);
  validateAdminRuntimePayload("/admin/v1/environments", { environments: [{ ...health,
    id: "env", name: "Staging", owner: "operator", classification: "staging", verificationStatus: "pending" }] });
});

test("mutations require explicit decision/request and audit identifiers without coercing accepted", () => {
  for (const path of ["/admin/v1/releases/request-approval", "/admin/v1/releases/decision", "/admin/v1/governance/decision"]) {
    assert.throws(() => validateAdminRuntimePayload(path, { accepted: true, message: "recorded" }), AdminRuntimeContractError);
    validateAdminRuntimePayload(path, { accepted: false, message: "Denied", requestId: "req", decisionId: "decision", auditEventId: "audit" });
  }
});

test("SDK validates actual HTTP payloads and disables credential forwarding through redirects", async () => {
  await assert.rejects(requestAdminRuntimeJson({ method: "GET", path: "/admin/v1/releases", options: {
    runtimeBaseUrl: env.CONXIAN_ADMIN_RUNTIME_BASE_URL,
    fetchImpl: async (_, init) => { assert.equal(init?.redirect, "error"); return Response.json({}); },
  } }), AdminRuntimeContractError);
});

test("missing or insecure probe configuration makes no network call", async () => {
  for (const config of [{}, { ...env, CONXIAN_ADMIN_RUNTIME_BASE_URL: "http://127.0.0.1:3000" }]) {
    const report = await verifyRuntimeReads(config, async () => { assert.fail("network must not be called"); });
    assert.equal(report.readContractPassed, false);
    assert.equal(report.checks.length, 0);
  }
});

test("probe checks anonymous denial and canonical reads without sending write requests or declaring acceptance", async () => {
  const calls: string[] = [];
  const report = await verifyRuntimeReads(env, async (input, init) => {
    const path = new URL(String(input)).pathname;
    calls.push(path);
    assert.equal(init?.method, "GET"); assert.equal(init?.redirect, "error");
    assert.equal(init?.cache, "no-store");
    assert.ok(init?.signal instanceof AbortSignal);
    const auth = new Headers(init?.headers).get("authorization");
    if (!auth) return new Response(null, { status: 401 });
    assert.equal(auth, "Bearer private-read-token");
    return Response.json(payloads[path]);
  });
  assert.equal(calls.length, 12);
  assert.equal(report.readContractPassed, true);
  assert.equal(report.sourceBindingVerified, false);
  assert.equal(report.durableWritesVerified, false);
  assert.equal(report.productionAcceptance, false);
  assert.doesNotMatch(JSON.stringify(report), /private-origin|private-read-token/);
});

test("anonymous success, redirects, HTML, missing routes and malformed or oversize data remain failures", async () => {
  for (const mode of ["anonymous-success", "redirect", "html", "missing", "schema", "oversize", "network"]) {
    const report = await verifyRuntimeReads(env, async (_, init) => {
      const authenticated = new Headers(init?.headers).has("authorization");
      if (!authenticated) return new Response(null, { status: mode === "anonymous-success" ? 200 : 403 });
      if (mode === "network") throw new Error("private-origin private-read-token");
      if (mode === "redirect") return new Response(null, { status: 302 });
      if (mode === "html") return new Response("login page", { headers: { "content-type": "text/html" } });
      if (mode === "missing") return Response.json({}, { status: 404 });
      if (mode === "oversize") return Response.json("a".repeat(1_048_577));
      return Response.json({ status: "ready" });
    });
    assert.equal(report.readContractPassed, false, mode);
    assert.doesNotMatch(JSON.stringify(report), /private-origin|private-read-token/);
  }
});
