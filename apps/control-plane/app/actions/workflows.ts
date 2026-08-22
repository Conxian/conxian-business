"use server";

import { headers } from "next/headers";
import { requestReleaseApprovalV1, submitGovernanceDecisionV1, submitReleaseDecisionV1 } from "../../lib/workflow-clients";
import { canApprove, canOperate, getCurrentActor } from "../../lib/auth";
import { db } from "../../lib/db";
import { auditEvent } from "../../lib/db/schema";

const text = (value: unknown, max = 2000, optional = false) => {
  if (typeof value !== "string") {
    if (optional && (value === undefined || value === null || value === "")) return "";
    throw new Error("Invalid input");
  }
  const trimmed = value.trim();
  if (!trimmed && optional) return "";
  if (!trimmed || trimmed.length > max) throw new Error("Invalid input");
  return trimmed;
};

const decision = (value: unknown): "approve" | "reject" | "request_changes" => {
  if (value !== "approve" && value !== "reject" && value !== "request_changes") throw new Error("Invalid input");
  return value;
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
  if (!canOperate(current.role)) throw new Error("Forbidden");
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
  const selectedDecision = decision(input.decision);
  const result = await submitReleaseDecisionV1({ artifactId, decision: selectedDecision, actorId: current.id, notes });
  if (result.accepted) await recordAudit(current, "release", `Release decision: ${selectedDecision}`, artifactId, "release_decision");
  return result;
}

export async function submitGovernanceDecision(input: { actionId: string; decision: "approve" | "reject" | "request_changes"; notes: string }) {
  const current = await actor();
  if (!canApprove(current.role)) throw new Error("Forbidden");
  const actionId = text(input.actionId, 200);
  const notes = text(input.notes || "No additional notes", 4000);
  const selectedDecision = decision(input.decision);
  const result = await submitGovernanceDecisionV1({ actionId, decision: selectedDecision, actorId: current.id, notes });
  if (result.accepted) await recordAudit(current, "policy", `Governance decision: ${selectedDecision}`, actionId, "governance_decision");
  return result;
}
