"use server";

import { headers } from "next/headers";
import { requestReleaseApprovalV1, submitGovernanceDecisionV1, submitReleaseDecisionV1 } from "../../lib/workflow-clients";
import { auth, canApprove, getCurrentActor } from "../../lib/auth";
import { db } from "../../lib/db";
import { auditEvent } from "../../lib/db/schema";

const text = (value: unknown, max = 2000) => {
  if (typeof value !== "string") throw new Error("Invalid input");
  const trimmed = value.trim();
  if (!trimmed || trimmed.length > max) throw new Error("Invalid input");
  return trimmed;
};

async function actor() {
  const current = await getCurrentActor(await headers());
  return current;
}

async function recordAudit(current: Awaited<ReturnType<typeof actor>>, category: string, summary: string, entity: string, type: string) {
  await db.insert(auditEvent).values({ id: crypto.randomUUID(), category, actorId: current.id, actorName: current.name, summary, relatedEntityId: entity, actionType: type, outcome: "accepted" });
}

export async function requestReleaseApproval(input: { artifactId: string; notes: string }) {
  const current = await actor();
  const artifactId = text(input.artifactId, 200);
  const notes = text(input.notes || "No additional notes", 4000);
  const result = await requestReleaseApprovalV1({ artifactId, requestedBy: current.id, notes });
  if (result.accepted) await recordAudit(current, "release", "Release approval requested", artifactId, "request_release_approval");
  return result;
}

export async function submitReleaseDecision(input: { artifactId: string; decision: "approve" | "reject" | "request_changes"; notes: string }) {
  const current = await actor();
  if (!canApprove(current.role)) throw new Error("Forbidden");
  const artifactId = text(input.artifactId, 200);
  const notes = text(input.notes || "No additional notes", 4000);
  const result = await submitReleaseDecisionV1({ artifactId, decision: input.decision, actorId: current.id, notes });
  if (result.accepted) await recordAudit(current, "release", `Release decision: ${input.decision}`, artifactId, "release_decision");
  return result;
}

export async function submitGovernanceDecision(input: { actionId: string; decision: "approve" | "reject" | "request_changes"; notes: string }) {
  const current = await actor();
  if (!canApprove(current.role)) throw new Error("Forbidden");
  const actionId = text(input.actionId, 200);
  const notes = text(input.notes || "No additional notes", 4000);
  const result = await submitGovernanceDecisionV1({ actionId, decision: input.decision, actorId: current.id, notes });
  if (result.accepted) await recordAudit(current, "policy", `Governance decision: ${input.decision}`, actionId, "governance_decision");
  return result;
}
