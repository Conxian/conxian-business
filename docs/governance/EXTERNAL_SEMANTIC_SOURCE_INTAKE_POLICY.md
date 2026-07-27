# External semantic-source intake policy

**Version:** 1.0

**Control:** [GitHub issue #955](https://github.com/Conxian/conxian-business/issues/955)

**Research context:** [GitHub issue #940](https://github.com/Conxian/conxian-business/issues/940)

## Purpose and boundary

This public-safe policy governs evidence intake for external semantic vocabularies, ontologies, schemas, and related source material. It does not authorize network retrieval, vendoring, parsing, transformation, redistribution, product use, or release use. Validation is standard-library-only, offline, deterministic, and fail-closed.

Registry presence is **not** adoption, legal advice, endorsement, certification, partnership, compliance or authority evidence, attestation evidence, candidate acceptance, release approval, or BOS Gate 0–6 advancement. A link, issue state, commit pin, archive hash, review token, or passing validator does not establish any of those claims.

## Controlled lifecycle

| State | Meaning | Allowed review disposition |
|---|---|---|
| `research-only` | Immutable identity may be recorded for bounded research; no selection or use. | `pending` or `approved-for-research` |
| `candidate` | Candidate may be compared; no selection or use. | `pending` or `approved-for-research` |
| `selected` | A bounded file set and import closure have been selected for review; not adopted. | `approved-for-selection` |
| `adopted` | The complete evidence bundle has an explicit adoption disposition. | `approved-for-adoption` |
| `rejected` | Candidate was rejected. | `rejected` |
| `retired` | A previously controlled record is no longer eligible for use. | `retired` |

Unknown states, dispositions, fields, or state/disposition combinations fail closed. `selected` and `adopted` records require the complete evidence bundle described below. Adoption is expressed only by the `adopted` state together with `approved-for-adoption`; registry presence alone never implies it.

## Immutable evidence bundle

Every record must identify an HTTPS repository, a full 40-character lowercase commit SHA, a commit-addressed HTTPS archive URL, an observed date, and an observed 64-character lowercase SHA-256 archive digest. Tags, branches, symbolic refs, abbreviated SHAs, uppercase digests, and moving URLs are rejected.

Evidence artifacts must be repository-relative paths below `governance/evidence/external-semantic-sources/<source-id>/`, contain no traversal or backslashes, exist locally, and match their recorded SHA-256. Network access is neither required nor permitted during validation.

For `selected` or `adopted` records, closure requires all of the following:

1. A non-empty selected-file list and a closed direct/transitive import map.
2. Immutable closure evidence and unique import mappings.
3. Root-license evidence plus a per-file notice disposition for every selected and imported file.
4. A Conxian-owned local extension namespace. Local terms must not be placed in or represented as controlled by an upstream or third-party namespace.
5. Transformation provenance. `none` still requires evidence and rationale; `recorded` requires deterministic input/output, tool, version, and evidence records.
6. A review-disposition token/reference to the authoritative review record.
7. An SBOM handoff marked `handoff-ready` with immutable evidence. This is a precondition boundary for a future SBOM component, not an SBOM component or release approval by itself.
8. Explicit supported and not-supported claim sets. The mandatory unsupported boundaries must remain present.

## Claims and review authority

Supported claims must stay factual and evidence-bounded, such as an observed immutable identity or a closed import manifest. Positive claims involving adoption-by-presence, legal advice, compliance, endorsement, certification, partnership, authority, attestation, candidate acceptance, release approval, or BOS Gate advancement are prohibited.

Each record must explicitly state that it does not support:

- registry presence alone as adoption;
- legal advice;
- endorsement or certification;
- partnership;
- compliance evidence;
- authority evidence;
- attestation evidence;
- candidate acceptance;
- release approval; or
- BOS Gate 0–6 advancement.

The public review reference is a traceability token only. Restricted legal or operational advice must remain in its authorized system under Zero Secret Egress; it must not be copied into this registry.

## Offline and unsupported behavior

The validator does not fetch URLs, resolve imports, parse RDF, infer licenses, or repair incomplete entries. Missing local evidence, malformed JSON, schema/version drift, undeclared imports, incomplete notices, unowned namespaces, unsupported positive claims, or unknown values cause a non-zero exit. An empty registry is valid and is the required initial state.

The canonical machine-readable artifacts are:

- [`governance/external-semantic-sources.json`](../../governance/external-semantic-sources.json)
- [`governance/external-semantic-sources.schema.v1.json`](../../governance/external-semantic-sources.schema.v1.json)
- [`scripts/validate_external_semantic_sources.py`](../../scripts/validate_external_semantic_sources.py)
