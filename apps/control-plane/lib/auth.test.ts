import { describe, expect, it } from "bun:test";
import {
  canApprove,
  canOperate,
  canRead,
  getCurrentActor,
} from "./auth";
import type { ControlPlaneRole } from "./auth";

describe("getCurrentActor", () => {
  it("returns a bootstrap admin actor", () => {
    const actor = getCurrentActor();

    expect(actor.id).toBe("bootstrap-actor");
    expect(actor.name).toBe("Bootstrap Operator");
    expect(actor.role).toBe("admin");
  });
});

describe("canRead", () => {
  const allRoles: ControlPlaneRole[] = [
    "viewer",
    "operator",
    "approver",
    "admin",
  ];

  it("returns true for every defined role", () => {
    for (const role of allRoles) {
      expect(canRead(role)).toBe(true);
    }
  });
});

describe("canApprove", () => {
  it("returns true for approver and admin roles", () => {
    expect(canApprove("approver")).toBe(true);
    expect(canApprove("admin")).toBe(true);
  });

  it("returns false for viewer and operator roles", () => {
    expect(canApprove("viewer")).toBe(false);
    expect(canApprove("operator")).toBe(false);
  });
});

describe("canOperate", () => {
  it("returns true for operator, approver, and admin roles", () => {
    expect(canOperate("operator")).toBe(true);
    expect(canOperate("approver")).toBe(true);
    expect(canOperate("admin")).toBe(true);
  });

  it("returns false for viewer role", () => {
    expect(canOperate("viewer")).toBe(false);
  });
});
