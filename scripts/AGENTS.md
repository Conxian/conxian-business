# Merge check evidence

`wait_for_checks.sh` is a read-only evidence gate. Never suppress CLI/API failures, parse human text as successful check evidence, accept empty results, or follow a moving PR head. Retrieve every check/status page, fail closed on unknown states, and keep skipped/neutral results distinct from successful checks.

Exit 0 identifies one immutable head snapshot only. A merge must separately satisfy review, branch and release policies and submit the matching head SHA atomically. Do not weaken review requirements or forge promotion acceptance evidence to turn the gate green.
