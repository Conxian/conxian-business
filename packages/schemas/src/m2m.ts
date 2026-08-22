import type { M2MRequestContext } from "./index";

export type M2MValidationCode =
  | "INVALID_PROTOCOL"
  | "MISSING_FIELD"
  | "INVALID_TIME_WINDOW"
  | "INVALID_AUDIENCE"
  | "MISSING_SCOPE"
  | "REPLAY_DETECTED"
  | "DUPLICATE_REQUEST";

export interface M2MValidationFailure {
  ok: false;
  code: M2MValidationCode;
  field?: string;
}

export interface M2MValidationSuccess {
  ok: true;
  expiresAt: number;
}

export type M2MValidationResult = M2MValidationFailure | M2MValidationSuccess;

export interface M2MReplayStore {
  has(key: string): boolean | Promise<boolean>;
  remember(key: string, expiresAt: number): void | Promise<void>;
}

export interface ValidateM2MRequestOptions {
  expectedAudience: string;
  requiredScopes?: readonly string[];
  now?: number;
  maxLifetimeMs?: number;
  replayStore?: M2MReplayStore;
}

const REQUIRED_FIELDS: readonly (keyof M2MRequestContext)[] = [
  "clientId",
  "audience",
  "correlationId",
  "idempotencyKey",
  "nonce",
  "issuedAt",
  "expiresAt",
  "proofOfPossessionJkt",
  "attestationRef",
];

export async function validateM2MRequest(
  request: M2MRequestContext,
  options: ValidateM2MRequestOptions,
): Promise<M2MValidationResult> {
  if (request.protocolVersion !== "m2m.v1") {
    return { ok: false, code: "INVALID_PROTOCOL", field: "protocolVersion" };
  }

  for (const field of REQUIRED_FIELDS) {
    if (typeof request[field] !== "string" || request[field].trim() === "") {
      return { ok: false, code: "MISSING_FIELD", field };
    }
  }

  if (request.audience !== options.expectedAudience) {
    return { ok: false, code: "INVALID_AUDIENCE", field: "audience" };
  }

  const now = options.now ?? Date.now();
  const issuedAt = Date.parse(request.issuedAt);
  const expiresAt = Date.parse(request.expiresAt);
  const maxLifetimeMs = options.maxLifetimeMs ?? 5 * 60 * 1000;

  if (
    !Number.isFinite(issuedAt) ||
    !Number.isFinite(expiresAt) ||
    issuedAt > now ||
    expiresAt <= now ||
    expiresAt <= issuedAt ||
    expiresAt - issuedAt > maxLifetimeMs
  ) {
    return { ok: false, code: "INVALID_TIME_WINDOW", field: "expiresAt" };
  }

  for (const requiredScope of options.requiredScopes ?? []) {
    if (!request.scopes.includes(requiredScope)) {
      return { ok: false, code: "MISSING_SCOPE", field: "scopes" };
    }
  }

  const replayKey = `${request.clientId}:${request.nonce}:${request.idempotencyKey}`;
  if (options.replayStore) {
    if (await options.replayStore.has(replayKey)) {
      return { ok: false, code: "REPLAY_DETECTED", field: "nonce" };
    }
    await options.replayStore.remember(replayKey, expiresAt);
  }

  return { ok: true, expiresAt };
}

export class InMemoryM2MReplayStore implements M2MReplayStore {
  private readonly entries = new Map<string, number>();

  has(key: string): boolean {
    return this.entries.has(key);
  }

  remember(key: string, expiresAt: number): void {
    this.entries.set(key, expiresAt);
  }
}
