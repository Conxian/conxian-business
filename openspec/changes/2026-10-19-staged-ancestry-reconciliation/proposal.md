# Reconcile the staged ancestry without losing integrated fixes

Business promotion #1448 cannot merge because previously promoted controls were applied through different commit histories. A trial merge of current staged into dev conflicts only in CHANGELOG.md and the service packaging review method; the conflicting staged sides add no unique text. Preserve the complete current dev documents, including operation-level research, work-evidence distinctions and the reviewed control-plane container.

Reconcile both histories through an ordinary reviewed fix into dev. Prove that the resolved merge tree equals current tested dev before adding this proposal and its changelog entry. Run promotion/head-binding/preservation and billing/source-inventory tests. Do not alter the existing immutable promotion branch, submodule pins, runtime implementation, credentials, rates, deployment or release acceptance requirements. After integration, use the newly generated immutable promotion candidate and close superseded candidates only after proving their complete head remains included.

## Preserve the merge parents during integration

PR #1449 was squash-merged: its resulting tree matches the reviewed reconciliation tree, but the staged parent was removed. The next promotion #1450 remains conflicted. Restore the already-reviewed staged parent using a new two-parent reconciliation commit based on current dev, with only this explanatory proposal and changelog updated. Integrate this repair with a merge commit; squash and rebase discard the ancestry that this repair exists to retain. Verify after integration that staged is an ancestor of dev and the regenerated immutable promotion is mergeable. Keep runtime files, submodule pins, research, credentials and acceptance gates unchanged.

## Refresh against the current dev head

Merge current dev `6af4451af3bdf5561d7bd7ff45749e4c374a20ef` into the existing repair head, preserving both histories and all newly integrated activation/hosting research. Resolve only the CHANGELOG overlap by retaining the full current dev changelog plus the existing ancestry-repair note. Verify that only this proposal and the changelog differ from current dev and that staged remains an ancestor. The changed source requires fresh independent review and checks; merge-commit integration remains mandatory.
