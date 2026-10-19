# Preserve promotion and reconciliation candidates

Parent: https://github.com/Conxian/conxian-business/issues/1415; coordination: #1390.

Generated promotion refs must remain at their encoded source SHA. On source, target or candidate drift, stop without updating, closing or deleting the candidate. Fresh evidence and a separately reviewed candidate are required.

Reconciliation must inspect existing PRs before publishing, retain existing branch refs, reject push races with a create-only ref lease and leave newly opened PRs for exact-head checks and applicable review. A merge strategy is not regression evidence. No admin merge, automatic review, production acceptance or branch protection change is included.

Verify with process-level workflow drift tests, existing-candidate preservation tests and isolated Git repositories for publication, retained refs and push races. Other repositories' workflow copies require separate normal promotion; this Business change does not claim an organization-wide deployed rollout.
