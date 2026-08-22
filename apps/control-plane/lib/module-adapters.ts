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

function withFallback<T>(items: T[], fallback: T[]): T[] {
  return items.length > 0 ? items : fallback;
}

function hasRuntimeBaseUrl(): boolean {
  return Boolean(
    process.env.CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim() ||
      process.env.ADMIN_RUNTIME_BASE_URL?.trim() ||
      process.env.NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim(),
  );
}

export async function getReleaseGovernanceData(): Promise<ReleaseArtifact[]> {
  if (!hasRuntimeBaseUrl()) return sampleReleaseArtifacts;
  return withFallback(await listReleaseArtifacts(), sampleReleaseArtifacts);
}

export async function getAuditData(): Promise<AuditEvent[]> {
  if (!hasRuntimeBaseUrl()) return sampleAuditEvents;
  return withFallback(await listAuditEvents(), sampleAuditEvents);
}

export async function getPolicyApprovalData(): Promise<GovernanceAction[]> {
  if (!hasRuntimeBaseUrl()) return sampleGovernanceActions;
  return withFallback(await listGovernanceActions(), sampleGovernanceActions);
}

export async function getEnvironmentData(): Promise<EnvironmentRecord[]> {
  if (!hasRuntimeBaseUrl()) return sampleEnvironments;
  return withFallback(await listEnvironments(), sampleEnvironments);
}
