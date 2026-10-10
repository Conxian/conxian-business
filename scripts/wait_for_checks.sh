#!/usr/bin/env bash
#
# wait_for_checks.sh — block until EVERY check on a PR has completed (no pending).
#
# Usage:  scripts/wait_for_checks.sh <owner/repo> <pr-number> [timeout_seconds]
#
# Exits:
#   0  all checks completed and green
#   1  at least one check failed
#   2  timed out waiting for checks to settle
#
# This is the merge gate: do NOT merge a promotion/fix PR until this script
# returns 0. It intentionally waits for slow informational checks (CodeQL
# "Analyze (Rust)", DKG ceremony, WASM evidence lanes) as well as required ones.
set -u

repo="${1:?usage: wait_for_checks.sh <owner/repo> <pr-number> [timeout_seconds]}"
pr="${2:?usage: wait_for_checks.sh <owner/repo> <pr-number> [timeout_seconds]}"
timeout="${3:-2400}"   # default 40 min (CodeQL on Rust can take ~30 min)
poll="${4:-30}"        # seconds between polls

deadline=$(( $(date +%s) + timeout ))

while true; do
  # gh pr checks emits a line per check; "pending" / "in_progress" means not done.
  pending=$(gh pr checks "$pr" --repo "$repo" 2>/dev/null | grep -ciE 'pending|in_progress' || true)

  if [ "$pending" -eq 0 ]; then
    break
  fi

  if [ "$(date +%s)" -gt "$deadline" ]; then
    echo "::error::wait_for_checks: timed out after ${timeout}s waiting for $repo#$pr (${pending} check(s) still pending)" >&2
    exit 2
  fi

  echo "wait_for_checks: $repo#$pr — ${pending} check(s) still pending; sleeping ${poll}s..."
  sleep "$poll"
done

fails=$(gh pr checks "$pr" --repo "$repo" 2>/dev/null | grep -ciE 'fail|error|action_required' || true)

if [ "$fails" -eq 0 ]; then
  echo "wait_for_checks: $repo#$pr — ALL CHECKS GREEN"
  exit 0
fi

echo "::error::wait_for_checks: $repo#$pr — ${fails} check(s) failed; do NOT merge" >&2
exit 1
