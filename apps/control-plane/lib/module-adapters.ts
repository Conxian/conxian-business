import {
  listAuditEvents,
  listEnvironments,
  listGovernanceActions,
  listReleaseArtifacts,
} from "@conxian/client-sdk";
import type { AuditEvent, EnvironmentRecord, GovernanceAction, ReleaseArtifact } from "@conxian/schemas";
import { runtimeRequestOptions } from "./runtime-requests";

export function getReleaseGovernanceData(): Promise<ReleaseArtifact[]> {
  return listReleaseArtifacts(runtimeRequestOptions("read"));
}

export function getAuditData(): Promise<AuditEvent[]> {
  return listAuditEvents(runtimeRequestOptions("read"));
}

export function getPolicyApprovalData(): Promise<GovernanceAction[]> {
  return listGovernanceActions(runtimeRequestOptions("read"));
}

export function getEnvironmentData(): Promise<EnvironmentRecord[]> {
  return listEnvironments(runtimeRequestOptions("read"));
}
