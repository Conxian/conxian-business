import {
  listAuditEvents,
  listEnvironments,
  listGovernanceActions,
  listReleaseArtifacts,
} from "@conxian/client-sdk";
import type { AuditEvent, EnvironmentRecord, GovernanceAction, ReleaseArtifact } from "@conxian/schemas";
import {
  sampleAuditEvents,
  sampleEnvironments,
  sampleGovernanceActions,
  sampleReleaseArtifacts,
} from "./sample-data";

async function withFallback<T>(items: Promise<T[]>, fallback: T[]): Promise<T[]> {
  try {
    const resolved = await items;
    return resolved.length > 0 ? resolved : fallback;
  } catch {
    return fallback;
  }
}

export function getReleaseGovernanceData(): Promise<ReleaseArtifact[]> {
  return withFallback(listReleaseArtifacts(), sampleReleaseArtifacts);
}

export function getAuditData(): Promise<AuditEvent[]> {
  return withFallback(listAuditEvents(), sampleAuditEvents);
}

export function getPolicyApprovalData(): Promise<GovernanceAction[]> {
  return withFallback(listGovernanceActions(), sampleGovernanceActions);
}

export function getEnvironmentData(): Promise<EnvironmentRecord[]> {
  return withFallback(listEnvironments(), sampleEnvironments);
}
