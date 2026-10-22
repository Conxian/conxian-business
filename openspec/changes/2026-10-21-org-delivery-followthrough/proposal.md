# Org delivery follow-through

Parent: Business #1390; release integrity #1415; independent acceptance #937.

The owner reports that routine stale candidates and stalled promotions required
manual prompting. The existing hourly task was paused. A tested implementation
was incorrectly treated as the end of a delivery session.

Restore the owner-authorized hourly task and add PR event wake-ups across the
accessible organization. Add a read-only deterministic snapshot audit and
regressions for incomplete inventory, paused execution, immutable-head/base drift,
missing diff/check/review evidence, workflow deltas, missed promotions, real soak,
candidate-bound acceptance and deployed-source mismatch.

22 October hardening: reproduce absent-status false completeness, malformed
collection crashes, invalid PR identity and promotion lane/target mismatch. Require
explicit typed evidence collections and current actual head/base observations;
retain actionable findings for other candidates after an invalid PR entry. Keep
the planner read-only and retain all existing release controls.

Preserve every existing CI/promotion/review/production gate. This proposal does
not change workflow files, grant approval authority, invent independent acceptance
or promise production qualification from a schedule or a green planner result.

Acceptance: tests pass; both execution tasks are enabled with read-back; direct
repo PR inventory is reconciled; every active candidate has an owner and concrete
next action under existing issues; normal dev/staged/main delivery remains active.
