import { describe, expect, it } from "bun:test";
import { AutonomousRunRegistry } from "./autonomous-run";
import type { AutonomousRunRecord } from "./index";

const run: AutonomousRunRecord = {
  runId: "run-1",
  state: "PENDING",
  trigger: "test",
  attempt: 0,
  idempotencyKey: "idem-1",
  lastTransitionAt: "2026-08-22T00:00:00.000Z",
  policy: {
    decision: "ALLOW",
    reasonCode: "TEST",
    policyVersion: "policy-1",
    subject: "worker-a",
    requiredApprovals: 0,
    approvals: 0,
    evaluatedAt: "2026-08-22T00:00:00.000Z",
  },
};

describe("AutonomousRunRegistry", () => {
  it("rejects duplicate idempotency keys", () => {
    const registry = new AutonomousRunRegistry();
    registry.start(run);
    expect(() => registry.start({ ...run, runId: "run-2" })).toThrow(
      "Duplicate idempotency key",
    );
  });

  it("rejects transitions after terminal state", () => {
    const registry = new AutonomousRunRegistry();
    registry.start(run);
    registry.transition("run-1", "SUCCEEDED", "2026-08-22T00:01:00.000Z");
    expect(() => registry.transition("run-1", "RETRYING", "2026-08-22T00:02:00.000Z")).toThrow(
      "Terminal run cannot transition",
    );
  });
});
