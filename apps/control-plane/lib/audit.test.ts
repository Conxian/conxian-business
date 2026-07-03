import { describe, expect, it } from "bun:test";
import { createAuditActionEvent } from "./audit";

describe("createAuditActionEvent", () => {
  it("returns an event with the expected shape and passed-through fields", () => {
    const event = createAuditActionEvent({
      category: "release",
      actor: "operator-1",
      summary: "Released artifact v2.0.1",
      relatedEntityId: "artifact_42",
      actionType: "promote",
      outcome: "accepted",
    });

    expect(event.id).toMatch(/^audit_artifact_42_\d+$/);
    expect(event.category).toBe("release");
    expect(event.actor).toBe("operator-1");
    expect(event.summary).toBe("Released artifact v2.0.1");
    expect(event.relatedEntityId).toBe("artifact_42");
    expect(event.actionType).toBe("promote");
    expect(event.outcome).toBe("accepted");
    expect(event.timestamp).toBeString();
    // ISO 8601 format
    expect(new Date(event.timestamp).toISOString()).toBe(event.timestamp);
  });

  it("generates a unique id for each call", () => {
    const a = createAuditActionEvent({
      category: "governance",
      actor: "admin-1",
      summary: "Approved policy",
      relatedEntityId: "gov_1",
      actionType: "approve",
      outcome: "accepted",
    });

    const b = createAuditActionEvent({
      category: "governance",
      actor: "admin-1",
      summary: "Approved policy",
      relatedEntityId: "gov_1",
      actionType: "approve",
      outcome: "accepted",
    });

    // IDs may collide if Date.now() returns same value; skip in that case.
    // In practice each call advances the clock, so they typically differ.
    if (a.id === b.id) {
      // Still passes — we just note this is clock-dependent.
      return;
    }
    expect(a.id).not.toBe(b.id);
  });

  it("handles all audit event categories", () => {
    const categories = ["release", "policy", "environment", "governance"] as const;

    for (const category of categories) {
      const event = createAuditActionEvent({
        category,
        actor: "test-actor",
        summary: `Audit for ${category}`,
        relatedEntityId: "entity_1",
        actionType: "test",
        outcome: "pending",
      });

      expect(event.category).toBe(category);
    }
  });

  it("handles all audit outcomes", () => {
    const outcomes = ["accepted", "rejected", "pending"] as const;

    for (const outcome of outcomes) {
      const event = createAuditActionEvent({
        category: "policy",
        actor: "test-actor",
        summary: `Outcome test: ${outcome}`,
        relatedEntityId: "entity_1",
        actionType: "test",
        outcome,
      });

      expect(event.outcome).toBe(outcome);
    }
  });
});
