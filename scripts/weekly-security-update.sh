#!/usr/bin/env bash
# Weekly Security Update Script for Conxian BOS.
#
# The script is deliberately non-destructive to the caller's checkout: it
# fetches the protected source branch, creates a temporary worktree from its
# exact remote tip, and publishes a maintenance branch for review.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
FRAMEWORK_REL="docs/BOS_KNOWLEDGE_FRAMEWORK.md"
REMOTE="${REMOTE:-origin}"
BASE_BRANCH="${BASE_BRANCH:-dev}"
TODAY="$(date -u +%Y-%m-%d)"
MAINTENANCE_BRANCH="${MAINTENANCE_BRANCH:-automation/weekly-security-update-${TODAY}}"
TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/conxian-weekly-security.XXXXXX")"
WORKTREE_DIR="$TEMP_ROOT/worktree"

cleanup() {
  git -C "$REPO_DIR" worktree remove --force "$WORKTREE_DIR" >/dev/null 2>&1 || true
  rm -rf "$TEMP_ROOT"
}
trap cleanup EXIT

echo "Conxian weekly security update"
echo "=============================="

if [ "$BASE_BRANCH" != "dev" ]; then
  echo "ERROR: weekly updates must target the dev branch; got '$BASE_BRANCH'" >&2
  exit 1
fi

cd "$REPO_DIR"

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git status --porcelain --untracked-files=all)" ]; then
  echo "ERROR: caller checkout is dirty; refusing to mutate or reuse it" >&2
  exit 1
fi

echo "Fetching the exact remote tip for ${REMOTE}/${BASE_BRANCH}..."
git fetch --prune "$REMOTE" "$BASE_BRANCH"
BASE_SHA="$(git rev-parse "refs/remotes/${REMOTE}/${BASE_BRANCH}")"

CURRENT_BRANCH="$(git symbolic-ref --short -q HEAD || true)"
if [ "$CURRENT_BRANCH" = "$BASE_BRANCH" ] && [ "$(git rev-parse HEAD)" != "$BASE_SHA" ]; then
  echo "ERROR: local ${BASE_BRANCH} is not synchronized with ${REMOTE}/${BASE_BRANCH}; refusing to continue" >&2
  exit 1
fi

if git ls-remote --exit-code --heads "$REMOTE" "$MAINTENANCE_BRANCH" >/dev/null 2>&1; then
  echo "ERROR: maintenance branch already exists: ${MAINTENANCE_BRANCH}" >&2
  echo "       Set MAINTENANCE_BRANCH explicitly after reviewing the existing branch/PR." >&2
  exit 1
fi

echo "Creating an isolated worktree from ${REMOTE}/${BASE_BRANCH} at ${BASE_SHA}..."
git worktree add --detach "$WORKTREE_DIR" "$BASE_SHA" >/dev/null
FRAMEWORK_FILE="$WORKTREE_DIR/$FRAMEWORK_REL"

echo "Updating the framework date in the maintenance worktree..."
python3 - "$FRAMEWORK_FILE" "$TODAY" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
today = sys.argv[2]
text = path.read_text(encoding="utf-8")
updated, count = re.subn(r"Generated: \d{4}-\d{2}-\d{2}", f"Generated: {today}", text, count=1)
if count != 1:
    raise SystemExit(f"expected one framework Generated date in {path}")
path.write_text(updated, encoding="utf-8")
PY

if git -C "$WORKTREE_DIR" diff --quiet -- "$FRAMEWORK_REL"; then
  echo "No framework changes are required."
  exit 0
fi

git -C "$WORKTREE_DIR" switch -c "$MAINTENANCE_BRANCH" >/dev/null
git -C "$WORKTREE_DIR" add "$FRAMEWORK_REL"
git -C "$WORKTREE_DIR" commit -m "chore(bos): weekly security update ${TODAY}

- Updated the framework publication date
- Prepared from the exact remote dev tip

Co-authored-by: openhands <openhands@all-hands.dev>" >/dev/null
git -C "$WORKTREE_DIR" push --set-upstream "$REMOTE" "$MAINTENANCE_BRANCH"

cat > "$WORKTREE_DIR/pr_body.md" <<EOF
## Weekly security maintenance

This maintenance branch was created from \\`${REMOTE}/${BASE_BRANCH}\\` at \\`${BASE_SHA}\\` in an isolated worktree.

### Scope

- Refresh the BOS framework publication date.
- Run the repository's security, governance, and submodule checks in CI.
- Promote through \\`dev -> staged -> main\\`; no protected branch is pushed by this script.

### Verification

- [ ] Required CI checks are green for the exact candidate commit.
- [ ] No secrets or generated artifacts were added.

EOF

if ! command -v gh >/dev/null 2>&1; then
  echo "WARNING: gh is unavailable; branch pushed, but create a PR manually:" >&2
  echo "         ${MAINTENANCE_BRANCH} -> ${BASE_BRANCH}" >&2
  exit 0
fi

EXISTING_PR="$(gh pr list \
  --base "$BASE_BRANCH" \
  --head "$MAINTENANCE_BRANCH" \
  --state open \
  --json number \
  --jq '.[0].number // ""')"

if [ -n "$EXISTING_PR" ]; then
  gh pr edit "$EXISTING_PR" --title "chore(bos): weekly security update ${TODAY}" --body-file "$WORKTREE_DIR/pr_body.md"
  echo "Updated maintenance PR #${EXISTING_PR}."
elif gh pr create \
  --base "$BASE_BRANCH" \
  --head "$MAINTENANCE_BRANCH" \
  --title "chore(bos): weekly security update ${TODAY}" \
  --body-file "$WORKTREE_DIR/pr_body.md"; then
  echo "Created maintenance PR."
else
  echo "WARNING: the branch was pushed, but the current GitHub auth cannot create a PR." >&2
  echo "         Open a PR manually from ${MAINTENANCE_BRANCH} into ${BASE_BRANCH}." >&2
fi

echo "Weekly update prepared without any direct protected-branch push."
