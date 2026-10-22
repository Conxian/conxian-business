# Require the shared billing export in propagation evidence

Owners: Business #1343/#1390, control gap #1415. Phase R1; release qualification remains R4.

Core's staged merge #466 removed the public billing module declaration while retaining the catalog and consumer pins. The offline propagation verifier must read the recorded Core revision's crate root and reject a missing/private/commented declaration. Existing source identity, units and authority checks stay mandatory. The record remains an immutable snapshot; it does not automatically track a moving development or staged branch.

Acceptance: reproduce the missing-export failure with otherwise valid catalog/pins, reject absent crate-root evidence, retain the valid snapshot result, and run the full Python suite. Native Cargo builds, integrated consumer checks and independent promotion evidence remain separate requirements. No pricing, quota, entitlement, fee, custody or deployment change is authorized.
