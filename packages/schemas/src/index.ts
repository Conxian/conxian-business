export type GovernanceActionStatus = "draft" | "pending" | "approved" | "rejected" | "changes_requested";
export type ReleaseArtifactStatus = "draft" | "in_review" | "approved" | "published" | "rejected";
export type EnvironmentVerificationStatus = "pending" | "verified" | "restricted";

export interface GovernanceAction {
  id: string;
  title: string;
  status: GovernanceActionStatus;
  owner: string;
  updatedAt: string;
}

export interface AuditEvent {
  id: string;
  category: "release" | "policy" | "environment" | "governance";
  actor: string;
  summary: string;
  timestamp: string;
}

export interface EnvironmentRecord {
  id: string;
  name: string;
  classification: "local" | "staging" | "production" | "restricted";
  owner: string;
  verificationStatus: EnvironmentVerificationStatus;
}

export interface IdentityRecord {
  id: string;
  subject: string;
  source: string;
  status: "active" | "pending" | "revoked";
}

export interface ReleaseArtifact {
  id: string;
  name: string;
  status: ReleaseArtifactStatus;
  owner: string;
  updatedAt: string;
}

export interface TreasuryEvent {
  id: string;
  eventType: string;
  amount: string;
  asset: string;
  timestamp: string;
}

export interface HealthStatus {
  status: "bootstrap-ready" | "degraded";
  message: string;
}
