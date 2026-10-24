/** Runtime checks for the control-plane contract; TypeScript casts are not evidence. */
export class AdminRuntimeContractError extends Error {
  constructor() {
    // Never reflect remote payloads, endpoint origins, tokens or private IDs.
    super("Admin runtime response does not satisfy the canonical contract.");
    this.name = "AdminRuntimeContractError";
  }
}

type RecordValue = Record<string, unknown>;
type Predicate = (value: unknown) => boolean;
const object = (value: unknown): value is RecordValue =>
  value !== null && typeof value === "object" && !Array.isArray(value);
const text = (value: unknown): value is string => typeof value === "string" && value.trim().length > 0;
const oneOf = (values: string[]): Predicate => value => typeof value === "string" && values.includes(value);
const instant: Predicate = value => text(value) && /(?:Z|[+-]\d{2}:\d{2})$/.test(value)
  && Number.isFinite(Date.parse(value));
const fields = (value: unknown, rules: Record<string, Predicate>): value is RecordValue =>
  object(value) && Object.entries(rules).every(([key, valid]) => valid(value[key]));
const status = oneOf(["ready", "degraded", "blocked", "unknown"]);
const evidence = {
  status,
  trustTier: oneOf(["nativeObservation", "proofVerified", "attesterVerified", "observerOnly", "unknown"]),
  evidenceLevel: oneOf(["none", "partial", "strong", "verified", "unknown"]),
  lastUpdated: instant,
};
const rows: Record<string, { key: string; rules: Record<string, Predicate> }> = {
  "/admin/v1/releases": { key: "releases", rules: {
    id: text, name: text, owner: text, updatedAt: instant,
    status: oneOf(["draft", "in_review", "approved", "published", "rejected"]),
  } },
  "/admin/v1/governance-actions": { key: "governanceActions", rules: {
    id: text, title: text, owner: text, updatedAt: instant,
    status: oneOf(["draft", "pending", "approved", "rejected", "changes_requested"]),
  } },
  "/admin/v1/audit-events": { key: "events", rules: {
    id: text, actor: text, summary: text, timestamp: instant,
    category: oneOf(["release", "policy", "environment", "governance"]),
  } },
  "/admin/v1/environments": { key: "environments", rules: {
    ...evidence,
    id: text, name: text, owner: text,
    classification: oneOf(["local", "staging", "production", "restricted"]),
    verificationStatus: oneOf(["pending", "verified", "restricted"]),
  } },
};

export const CONTROL_PLANE_READ_PATHS = [
  ...Object.keys(rows), "/admin/v1/runtime/health", "/admin/v1/runtime/readiness",
] as readonly string[];

/** Preserve compatible bare lists/envelopes and extension fields; reject invalid required fields. */
export function validateAdminRuntimePayload(path: string, value: unknown): void {
  const list = rows[path];
  if (list) {
    const entries = Array.isArray(value) ? value : object(value) ? value[list.key] : undefined;
    if (!Array.isArray(entries) || !entries.every(row => fields(row, list.rules))
        || new Set(entries.map(row => row.id)).size !== entries.length) {
      throw new AdminRuntimeContractError();
    }
  } else if (path === "/admin/v1/runtime/health") {
    if (!fields(value, { ...evidence, message: text })) throw new AdminRuntimeContractError();
  } else if (path === "/admin/v1/runtime/readiness") {
    if (!fields(value, { ...evidence, ready: v => typeof v === "boolean",
      blockers: v => Array.isArray(v) && v.every(text) })) throw new AdminRuntimeContractError();
    if (value.ready !== (value.status === "ready") || value.ready && (
      (value.blockers as unknown[]).length > 0 || ["none", "unknown"].includes(String(value.evidenceLevel))
      || ["unknown", "observerOnly"].includes(String(value.trustTier)))) {
      throw new AdminRuntimeContractError();
    }
  } else if (["/admin/v1/releases/request-approval", "/admin/v1/releases/decision",
    "/admin/v1/governance/decision"].includes(path)) {
    const id = path.endsWith("request-approval") ? "requestId" : "decisionId";
    if (!fields(value, { accepted: v => typeof v === "boolean", message: text,
      auditEventId: text, [id]: text })) throw new AdminRuntimeContractError();
  }
}
