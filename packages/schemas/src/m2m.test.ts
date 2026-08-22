import { describe, expect, it } from "bun:test";
import {
  InMemoryM2MReplayStore,
  validateM2MRequest,
  type M2MRequestContext,
} from "./m2m";

const request: M2MRequestContext = {
  protocolVersion: "m2m.v1",
  clientId: "worker-a",
  audience: "admin-runtime",
  scopes: ["release:write"],
  correlationId: "trace-1",
  idempotencyKey: "idem-1",
  nonce: "nonce-1",
  issuedAt: "2026-08-22T00:00:00.000Z",
  expiresAt: "2026-08-22T00:04:00.000Z",
  proofOfPossessionJkt: "jkt-1",
  attestationRef: "attestation-1",
};

describe("validateM2MRequest", () => {
  it("accepts a scoped request and remembers its replay key", async () => {
    const store = new InMemoryM2MReplayStore();
    const result = await validateM2MRequest(request, {
      expectedAudience: "admin-runtime",
      requiredScopes: ["release:write"],
      now: Date.parse("2026-08-22T00:01:00.000Z"),
      replayStore: store,
    });
    expect(result.ok).toBe(true);
  });

  it("rejects a replay", async () => {
    const store = new InMemoryM2MReplayStore();
    const options = {
      expectedAudience: "admin-runtime",
      now: Date.parse("2026-08-22T00:01:00.000Z"),
      replayStore: store,
    };
    expect((await validateM2MRequest(request, options)).ok).toBe(true);
    const replay = await validateM2MRequest(request, options);
    expect(replay).toMatchObject({ ok: false, code: "REPLAY_DETECTED" });
  });

  it("rejects the wrong audience and missing capabilities", async () => {
    await expect(
      validateM2MRequest(request, { expectedAudience: "other-runtime" }),
    ).resolves.toMatchObject({ ok: false, code: "INVALID_AUDIENCE" });
    await expect(
      validateM2MRequest(request, {
        expectedAudience: "admin-runtime",
        requiredScopes: ["treasury:write"],
        now: Date.parse("2026-08-22T00:01:00.000Z"),
      }),
    ).resolves.toMatchObject({ ok: false, code: "MISSING_SCOPE" });
  });
});
