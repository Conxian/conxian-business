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
       - The normalized settlement transaction hashed to produce `normalized_settlement_hash` MUST include at least the canonical `transaction_identifiers` defined in §2.1.1, and MUST NOT include any `envelope_identifiers`.
     - any digest/hash computed outside the TEE MUST be treated as untrusted; the TEE MUST recompute authoritative values from `raw_payload_bytes` and reject any mismatch with host-supplied claims
     - `settlement_identifiers` MUST be derived/normalized inside the TEE from `raw_payload_bytes`. If the host supplies a `settlement_identifiers` object as an optimization hint, that object MUST be provided to the TEE as input and validated exactly as specified in §2.1.1 (including attestation refusal on mismatch and oversized hints)
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
   - Idempotency is enforced at the trigger granularity (one trigger per settlement transaction).
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

The TEE attestation MUST bind (directly or by digest) the canonical values of at least `{ rail, raw_payload_hash, normalized_settlement_hash, trigger_id, settlement_identifiers, asset_path, timelock_delay_blocks, oracle_verification }` so they cannot be altered after verification. The canonical `oracle_verification` value that the TEE attests MUST embed either the exact oracle proof bytes or a digest of those bytes, and proposal emission MUST verify only that same proof input, so a different proof cannot be substituted before or after attestation.

`oracle_verification` MUST NOT be a bare boolean. It MUST include (directly or by digest) the exact oracle proof bytes verified inside the TEE. At minimum, it MUST include `oracle_proof_digest`, defined as the lowercase hex encoding of SHA-256 over `utf8("oracle-proof:v1") || raw_oracle_proof_bytes`.

`raw_oracle_proof_bytes` MUST be the exact byte sequence provided to the TEE for oracle-proof verification, before any internal parsing, canonicalization, or transformation.

Proposal emission MUST recompute `oracle_proof_digest` from the exact `raw_oracle_proof_bytes` it provides to the TEE and MUST reject if the result differs from the `oracle_proof_digest` value bound by the TEE attestation.

Prohibited fields:

- `raw_payload_bytes`
- Any full parsed external-settlement payload structure (XML/JSON) beyond the canonical `settlement_identifiers`.

#### 2.1.1 `settlement_identifiers` (per-rail canonical set)

`settlement_identifiers` MUST be a JSON object with two namespaces:

- `transaction_identifiers`: envelope-agnostic identifiers for the settlement transaction.
- `envelope_identifiers`: envelope/message-local identifiers for audit/debug only.

Within `settlement_identifiers`, implementations MUST use only JSON objects with leaf values restricted to JSON strings and JSON numbers that MUST be integers in the range `[0, 9007199254740991]` (inclusive, i.e. `2^53-1`); arrays MUST NOT be used.

If the canonical `settlement_identifiers` derived from `raw_payload_bytes` fails to meet the structural and leaf-type constraints in this section, the TEE MUST refuse to produce a successful attestation.

`transaction_identifiers` MUST be included in the normalized settlement transaction hashed to produce `normalized_settlement_hash`.

`envelope_identifiers` MUST NOT affect `normalized_settlement_hash`.

`settlement_identifiers` MUST be derived/normalized inside the TEE from `raw_payload_bytes`.

Implementations MUST NOT treat any host-supplied `settlement_identifiers` as authoritative. If a host supplies any identifiers as an optimization hint:

- The host-supplied hint object MUST be provided to the TEE as input and MUST be treated as untrusted.
- If the hint fails JSON parsing or fails to meet the structural and leaf-type constraints in this section, the TEE MUST refuse to produce a successful attestation.
- The TEE MUST enforce bounds on the hint object before deep traversal. When encoded as UTF-8 JSON, the hint object MUST be ≤ 16384 bytes, have max nesting depth ≤ 8, and contain ≤ 128 leaf fields. If any bound is exceeded, the TEE MUST refuse to produce a successful attestation.
- The TEE MUST enforce bounds on the hint object before deep traversal. When encoded as UTF-8 JSON, the hint object MUST be ≤ 16384 bytes, have max nesting depth ≤ 8, and contain ≤ 128 leaf fields. A leaf field is a JSON key path (including nested objects) whose value is a JSON string or a JSON number. If any bound is exceeded, the TEE MUST refuse to produce a successful attestation.
- The TEE MUST recompute the canonical `settlement_identifiers` from `raw_payload_bytes` and compare any overlapping fields, defined as any JSON key path (including nested objects) present in both objects. For each overlapping field, the host-supplied JSON value MUST exactly equal the TEE-derived canonical JSON value (same JSON type and value). If any overlapping field differs, the TEE MUST refuse to produce a successful attestation.
- Any host-supplied extra fields MUST be ignored for canonicalization purposes.
- The `AttestedExternalSettlementTrigger.settlement_identifiers` included in the attested payload MUST be exactly the TEE-derived canonical object; host-supplied hints (including any extra fields) MUST NOT be forwarded or merged into the attested/returned identifiers.

Minimum required identifier set (by rail):

`tx_index` requirements (all rails):

- `tx_index` MUST be computed over the rail-defined settlement-transaction entries (e.g., ISO20022 `pacs.008` `CdtTrfTxInf` elements) in the exact sequence they appear in the received message payload, before any internal normalization or reordering. Implementations MUST NOT reorder transactions for indexing.
- The index MUST be computed over all transaction entries present in the received message payload, including any that are later rejected or skipped.

Example: if a message contains three settlement-transaction entries `[A, B, C]` and `B` is later rejected or skipped, any triggers emitted for `A` and `C` still use `tx_index = 0` and `tx_index = 2`.

- **ISO20022 (pacs.008)**
  - `transaction_identifiers.transaction_reference` (prefer `uetr`, else `end_to_end_id`, else `instruction_id`)
  - `envelope_identifiers.tx_index`
- **PAPSS**
  - `transaction_identifiers.transaction_reference`
  - `envelope_identifiers.tx_index`
- **BRICS**
  - `transaction_identifiers.transaction_reference`
  - `envelope_identifiers.tx_index`

Canonical formatting requirements:

- `transaction_identifiers.transaction_reference` MUST be a UTF-8 string (Unicode NFC), MUST NOT contain `\n`, and MUST preserve case.
- `envelope_identifiers.tx_index` MUST be a JSON number that is an integer in the range `[0, 9007199254740991]` (inclusive, i.e. `2^53-1`).

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
8. Host-supplied `settlement_identifiers` mismatch the TEE-derived identifiers (for any overlapping field) for the same `raw_payload_bytes` → proposal emission fails.
9. Host-supplied `settlement_identifiers` hints exceed the TEE bounds in §2.1.1 → proposal emission fails.
10. Oracle proof bytes do not hash to the `oracle_proof_digest` bound by the TEE attestation → proposal emission fails.
11. `settlement_identifiers` (canonical or host hint) violates the structural/leaf-type constraints in §2.1.1 → proposal emission fails.
