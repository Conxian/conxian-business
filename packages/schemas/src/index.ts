export type GovernanceActionStatus = "draft" | "pending" | "approved" | "rejected";
export type ReleaseArtifactStatus = "draft" | "in_review" | "approved" | "published";

export interface GovernanceAction {
  id: string;
  title: string;
  status: GovernanceActionStatus;
  owner: string;
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
}

export interface TreasuryEvent {
  id: string;
  eventType: string;
  amount: string;
  asset: string;
  timestamp: string;
}
