# Spec: Proposal-only external settlement triggers (TEE enforced)

Proposal-only external settlement triggers define how ISO 20022 / PAPSS / BRICS messages may enter the sovereign system.

## 1. Normative rules

1. **TradFi payloads are never execution authority**
   - A raw ISO 20022 / PAPSS / BRICS payload MUST NOT be consumed by any execution function.
   - Raw payloads MAY be parsed/normalized for audit and mapping.

2. **TEE verification is required before proposal emission**
   - A proposal MUST NOT be emitted unless a TEE/StrongBox/CloudTEE attestation verifies:
     - the payload digest (computed from `raw_payload_bytes` inside the TEE),
     - `normalized_settlement_hash` (computed inside the TEE) for each settlement transaction using a rail-specific canonical serialization:
       - JSON: RFC 8785 JSON Canonicalization Scheme (JCS)
       - XML: W3C XML Canonicalization 1.1
       - Additional requirement: rail-specific normalization MUST be envelope-agnostic: the same settlement transaction replayed in different envelopes/messages MUST yield the same `normalized_settlement_hash`, and envelope-level metadata (e.g., message identifiers, timestamps, routing fields) MUST NOT affect `normalized_settlement_hash`.
       - The normalized settlement transaction hashed to produce `normalized_settlement_hash` MUST satisfy the identifier inclusion/exclusion rules in §2.1.1.
       - Compatibility requirement: any implementation that previously computed `normalized_settlement_hash` using envelope/message-local identifiers (including `tx_index`) MUST coordinate a breaking upgrade before enabling this trigger kind on a shared network; implementations MUST NOT reuse the `external-settlement-trigger:v1` label with those draft semantics.
       - Note: Earlier internal drafts described including envelope/message-local identifiers (including `tx_index`) in `normalized_settlement_hash` inputs; those drafts are non-normative and MUST NOT be used for interoperability.
     - any digest/hash computed outside the TEE MUST be treated as untrusted; the TEE MUST recompute authoritative values from `raw_payload_bytes` and reject any mismatch with host-supplied claims
     - the oracle authenticity proof,
     - and the deterministic mapping to `asset_path`.

3. **Timelock is mandatory**
   - Verified external triggers MUST initiate the standard 144-block timelock.
   - The start height MUST use the same canonical chain-height source used by the native path.

4. **Timelock scheduling is owned by proposal emission**
   - The TEE MUST attest `timelock_delay_blocks = 144`.
   - Proposal emission MUST schedule the timelock after verifying TEE attestation.
   - Execution MUST NOT accept a `start_height` or `release_height` sourced from the raw TradFi payload.

5. **Multi-sig approvals are mandatory**
   - Verified external triggers MUST enter the same multi-sig approval policy as native proposals.

6. **Yield routing invariance**
   - Downstream yield routing MUST be identical for native vs external-triggered lock events.
   - Trigger source MUST NOT change the 5/5/90 productive streaming behavior.

7. **Idempotency / replay protection**
   - `trigger_id` MUST be computed deterministically as follows:
     - Canonicalization MUST use RFC 8785 JSON Canonicalization Scheme (JCS).
     - The canonicalized value MUST be the JCS output for the JSON object `{"rail": rail, "normalized_settlement_hash": normalized_settlement_hash}` (exact key names as shown).
     - The hash MUST be SHA-256 over `utf8("external-settlement-trigger:v1") || utf8(JCS({"rail": rail, "normalized_settlement_hash": normalized_settlement_hash}))`.
     - `trigger_id` MUST be the lowercase hex encoding of the SHA-256 digest.
     - NOTE (compatibility): The domain-separation label `external-settlement-trigger:v1` is bound to this spec’s normative definitions. Implementations MUST NOT reuse this label with different `normalized_settlement_hash` semantics.
   - Idempotency is enforced at the trigger granularity: at most one trigger is emitted per settlement transaction that exposes a canonical envelope-agnostic `transaction_reference` as defined in §2.1.1.
   - Proposal emission MUST be idempotent on `trigger_id`: duplicate triggers MUST NOT create additional proposals or timelocks.

## 2. Required artifacts

### 2.1 `AttestedExternalSettlementTrigger`

Minimum fields:

- `rail`
- `raw_payload_hash`
- `settlement_identifiers` (per-rail canonical set; see below)
- `normalized_settlement_hash`
- `trigger_id`
- `asset_path`
- `timelock_delay_blocks` (must equal `144`)
- `tee_attestation`
- `oracle_verification`

Prohibited fields:

- `raw_payload_bytes`
- Any full parsed external-settlement payload structure (XML/JSON) beyond `settlement_identifiers` itself; the allowed shape of `settlement_identifiers` is defined normatively in §2.1.1.

#### 2.1.1 `settlement_identifiers` (per-rail canonical set)

`settlement_identifiers` MUST be a JSON object with exactly two top-level keys: `transaction_identifiers` and `envelope_identifiers`. Both keys MUST be present and MUST map to JSON objects. If there are no envelope/message-local identifiers, `envelope_identifiers` MUST be an empty object.

NOTE (compatibility): Earlier internal drafts described a flat `settlement_identifiers` object with top-level `tx_index` / `transaction_reference` keys; that shape is non-normative and MUST NOT be used for interoperability.

NOTE: This schema is intentionally fixed; adding top-level keys or changing the nesting requires a versioned update to this spec.

- `transaction_identifiers`: envelope-agnostic identifiers for the settlement transaction.
- `envelope_identifiers`: envelope/message-local identifiers for audit/debug only.

`transaction_identifiers` and `envelope_identifiers` MUST contain only rail-defined identifier keys with string/integer values; they MUST NOT embed parsed XML/JSON fragments or other nested payload structures.

`transaction_identifiers` MUST be included in the normalized settlement transaction hashed to produce `normalized_settlement_hash`.

`envelope_identifiers` MUST NOT be included in the normalized settlement transaction hashed to produce `normalized_settlement_hash`.

Minimum required identifier set (by rail):

For all rails, `transaction_identifiers.transaction_reference` MUST be envelope-agnostic (it MUST NOT be derived from `tx_index` or other envelope/message-local metadata). If a rail does not provide a stable transaction reference, the rail spec MUST define an envelope-agnostic derivation; otherwise this trigger kind is unsupported for that rail.

For any rail, if the canonical `transaction_identifiers.transaction_reference` for a settlement transaction cannot be obtained from the payload or from a rail-defined envelope-agnostic derivation, the implementation MUST reject that settlement transaction and MUST NOT emit a trigger for it.

In messages that contain multiple settlement transactions (e.g., ISO 20022 `pacs.008` with multiple `CdtTrfTxInf` entries), this requirement applies per settlement transaction: transactions that expose a canonical `transaction_reference` MUST still be processed and MAY emit triggers even if other transactions in the same envelope are rejected.

Note: Earlier drafts described using `tx_index` as a fallback for `transaction_reference`; implementations MUST NOT use that fallback.

`tx_index` requirements (all rails):

- `tx_index` MUST be computed over the rail-defined settlement-transaction entries (e.g., ISO20022 `pacs.008` `CdtTrfTxInf` elements) in the exact sequence they appear in the received message payload, before any internal normalization or reordering. Implementations MUST NOT reorder transactions for indexing.
- The index MUST be computed over all transaction entries present in the received message payload, including any that are later rejected or skipped.

Example: if a message contains three settlement-transaction entries `[A, B, C]` and `B` is later rejected or skipped, any triggers emitted for `A` and `C` still use `tx_index = 0` and `tx_index = 2`.

- **ISO20022 (pacs.008)**
  - `transaction_identifiers.transaction_reference` (MUST use the first available in this order: `uetr`, else `end_to_end_id`)
  - `envelope_identifiers.tx_index`
- **PAPSS**
  - `transaction_identifiers.transaction_reference`
  - `envelope_identifiers.tx_index`
- **BRICS**
  - `transaction_identifiers.transaction_reference`
  - `envelope_identifiers.tx_index`

Canonical formatting requirements:

- `transaction_identifiers.transaction_reference` MUST be a UTF-8 string (Unicode NFC), MUST NOT contain `\n`, and MUST preserve case.
- `envelope_identifiers.tx_index` MUST be a non-negative integer.

### 2.2 `SovereignProposal` (trigger-kind)

Minimum fields:

- `proposal_kind = EXTERNAL_SETTLEMENT_TRIGGER`
- `trigger_id`
- `asset_path`
- `timelock` (start + release heights)
- `approval_policy`

Prohibited fields:

- Any “call data” / executable contract payload that is derived from the raw TradFi bytes.

## 3. Negative test cases (must exist)

1. Missing or invalid TEE attestation → proposal emission fails.
2. Valid payload but invalid oracle proof → proposal emission fails.
3. Any attempt to include `raw_payload_bytes` or a full external-settlement payload structure in `AttestedExternalSettlementTrigger` → rejected.
4. Any attempt to supply raw TradFi payload (bytes or parsed structure) to execution code → rejected.
5. Replay the same settlement transaction (same `trigger_id`) → no new proposal/timelock created.
6. Any attempt to skip multi-sig approvals → rejected.
7. Any attempt to change timelock away from 144 blocks (increase or decrease) → rejected.
