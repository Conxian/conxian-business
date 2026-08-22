import type { AutonomousRunRecord } from "./index";

const TERMINAL_STATES = new Set<AutonomousRunRecord["state"]>([
  "SUCCEEDED",
  "FAILED",
  "CANCELLED",
]);

export class AutonomousRunRegistry {
  private readonly runs = new Map<string, AutonomousRunRecord>();
  private readonly idempotency = new Map<string, string>();

  start(run: AutonomousRunRecord): AutonomousRunRecord {
    const existingRunId = this.idempotency.get(run.idempotencyKey);
    if (existingRunId && existingRunId !== run.runId) {
      throw new Error(`Duplicate idempotency key: ${run.idempotencyKey}`);
    }
    if (this.runs.has(run.runId)) throw new Error(`Run already exists: ${run.runId}`);
    this.idempotency.set(run.idempotencyKey, run.runId);
    this.runs.set(run.runId, run);
    return run;
  }

  transition(
    runId: string,
    nextState: AutonomousRunRecord["state"],
    now: string,
  ): AutonomousRunRecord {
    const current = this.runs.get(runId);
    if (!current) throw new Error(`Unknown run: ${runId}`);
    if (TERMINAL_STATES.has(current.state)) {
      throw new Error(`Terminal run cannot transition: ${runId}`);
    }
    const next = { ...current, state: nextState, lastTransitionAt: now };
    this.runs.set(runId, next);
    return next;
  }

  get(runId: string): AutonomousRunRecord | undefined {
    return this.runs.get(runId);
  }
}
