# BOS Multi-Tenant Orchestration Guide (public-safe stub)

Treat this repository as public for boundary purposes.

Sensitive/internal tenant isolation details, policy enforcement thresholds, and orchestration runbooks have been migrated to the Linear Virtual Office.

See:

- https://linear.app/conxian-labs
- https://linear.app/conxian-labs/issue/CON-530/replace-sensitive-files-with-safe-examples-and-docs
- https://linear.app/conxian-labs/issue/CON-256

## How to work locally (public-safe)

1. Use fake tenant identifiers and non-production namespaces.
2. Keep all local examples deterministic and free of real credentials.
3. Validate orchestration logic with mocked tools before integration.

### Local-safe pseudocode example

```python
def dispatch(task, tenant_id="tenant-local-example"):
    with TenantNamespace(tenant_id):
        return orchestrator.run(task, dry_run=True)
```

Internal: search Linear Virtual Office for "BOS Multi-Tenant Orchestration Guide".

This file is intentionally kept as a stub so existing links continue to resolve.
