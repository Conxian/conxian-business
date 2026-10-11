import {
  listAuditEvents,
  listEnvironments,
  listGovernanceActions,
  listReleaseArtifacts,
} from "@conxian/client-sdk";
import type { AuditEvent, EnvironmentRecord, GovernanceAction, ReleaseArtifact } from "@conxian/schemas";

export function getReleaseGovernanceData(): Promise<ReleaseArtifact[]> {
  return listReleaseArtifacts();
}

export function getAuditData(): Promise<AuditEvent[]> {
  return listAuditEvents();
}

export function getPolicyApprovalData(): Promise<GovernanceAction[]> {
  return listGovernanceActions();
}

export function getEnvironmentData(): Promise<EnvironmentRecord[]> {
  return listEnvironments();
}
