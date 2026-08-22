import {
  listAuditEvents,
  listEnvironments,
  listGovernanceActions,
  listReleaseArtifacts,
} from "@conxian/client-sdk";
import type { AuditEvent, EnvironmentRecord, GovernanceAction, ReleaseArtifact } from "@conxian/schemas";

function hasRuntimeBaseUrl(): boolean {
  return Boolean(
    process.env.CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim() ||
      process.env.ADMIN_RUNTIME_BASE_URL?.trim() ||
      process.env.NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim(),
  );
}

function requireRuntimeUrl(): boolean {
  return hasRuntimeBaseUrl();
}

export async function getReleaseGovernanceData(): Promise<ReleaseArtifact[]> {
  if (!requireRuntimeUrl()) return [];
  return listReleaseArtifacts();
}

export async function getAuditData(): Promise<AuditEvent[]> {
  if (!requireRuntimeUrl()) return [];
  return listAuditEvents();
}

export async function getPolicyApprovalData(): Promise<GovernanceAction[]> {
  if (!requireRuntimeUrl()) return [];
  return listGovernanceActions();
}

export async function getEnvironmentData(): Promise<EnvironmentRecord[]> {
  if (!requireRuntimeUrl()) return [];
  return listEnvironments();
}

export function getRuntimeConfigurationStatus(): { configured: boolean; source: "server" | "client" | "none" } {
  if (process.env.CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim() || process.env.ADMIN_RUNTIME_BASE_URL?.trim()) {
    return { configured: true, source: "server" };
  }
  if (process.env.NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim()) {
    return { configured: true, source: "client" };
  }
  return { configured: false, source: "none" };
}
