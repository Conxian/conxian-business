# FIBO provenance research note

**Accessed:** 2026-07-27

**Research tracker:** [GitHub issue #940](https://github.com/Conxian/conxian-business/issues/940)

**Generic intake control:** [GitHub issue #955](https://github.com/Conxian/conxian-business/issues/955)

## Boundary

This is a public-safe provenance observation for future research. It is not legal advice, adoption, endorsement, certification, partnership, compliance evidence, authority evidence, attestation evidence, candidate acceptance, release approval, or BOS Gate 0–6 advancement. No FIBO or OMG corpus, archive, ontology, or registry record is included in this repository by this note.

## Independently reproduced observations

The GitHub tag-reference API returned `refs/tags/master_2026Q2` as a direct commit reference to full commit `f59157fe156e3d91b1c045222d0a7dc06b7d78a2`. The commit API returned the same full SHA. Future evidence must use the commit identity, not the tag or a moving branch.

Primary references:

- Tag-reference API: <https://api.github.com/repos/edmcouncil/fibo/git/ref/tags/master_2026Q2>
- Commit API: <https://api.github.com/repos/edmcouncil/fibo/commits/f59157fe156e3d91b1c045222d0a7dc06b7d78a2>
- Commit: <https://github.com/edmcouncil/fibo/commit/f59157fe156e3d91b1c045222d0a7dc06b7d78a2>
- Commit-addressed license: <https://github.com/edmcouncil/fibo/blob/f59157fe156e3d91b1c045222d0a7dc06b7d78a2/LICENSE>
- Commit-addressed README: <https://github.com/edmcouncil/fibo/blob/f59157fe156e3d91b1c045222d0a7dc06b7d78a2/README.md>
- Commit-addressed aggregate source: <https://github.com/edmcouncil/fibo/blob/f59157fe156e3d91b1c045222d0a7dc06b7d78a2/AboutFIBOProd.rdf>
- Commit-addressed GitHub codeload archive: <https://codeload.github.com/edmcouncil/fibo/tar.gz/f59157fe156e3d91b1c045222d0a7dc06b7d78a2>
- Release metadata API: <https://api.github.com/repos/edmcouncil/fibo/releases/tags/master_2026Q2>

The commit-addressed GitHub codeload response was downloaded to a temporary directory, measured as `64,579,466` bytes, and observed with SHA-256 `c6c0c5102a47d2a281b8b2430fd201687f8cc8fad067740770c73094cae9a66d`. The temporary files were removed after verification. This digest is an **observed hash of GitHub-generated archive bytes**, not an upstream signed checksum, publisher attestation, release approval, or reproducible-build claim.

The release metadata API was reverified on 2026-07-27. It reported `immutable: false`, `target_commitish: master`, and zero release assets for `master_2026Q2`. The release/tag record is therefore a moving-platform metadata observation, not immutable artifact or checksum authority; only the full commit identity is suitable as the candidate source pin, and any archive digest remains separately observed evidence.

The root `LICENSE` at the pinned commit contains the MIT license and a notice for Enterprise Data Management Council. That root-license observation does not close the notice obligations for a selected file set or its direct and transitive imports. Per-file notices and any third-party terms must be reviewed against the exact selected/imported files.

The pinned `AboutFIBOProd.rdf` describes itself as loading the “very latest” production ontologies from GitHub rather than a specific quarterly version, and it contains many ontology imports. On that primary-source statement, it is not a deterministic pinned build root for Conxian use without a separately selected immutable file set and closed import graph.

The exact-source and notice disposition for any imported OMG Commons material remains unresolved. A future review must identify the precise commit/file identities, import paths, applicable terms, and retained notices before selection or adoption. This note makes no legal conclusion.

## Scored candidate decision

Score formula from [#940](https://github.com/Conxian/conxian-business/issues/940): `(value + urgency + readiness + (6 - risk)) / 4`.

| Candidate | Value / urgency / readiness / risk | Score | Disposition |
|---|---:|---:|---|
| Generic empty intake registry, schema, validator, and CI control | `5 / 4 / 5 / 2` | **4.50** | Selected for implementation in #955. |
| Notice-layout-only preparation | `4 / 4 / 4 / 3` | 3.75 | Deferred behind enforceable intake. |
| SBOM adapter | `4 / 3 / 3 / 3` | 3.25 | Deferred until a source is reviewed. |
| FIBO-specific lint | `3 / 3 / 3 / 4` | 2.75 | Rejected for now as premature specialization. |
| Direct corpus vendoring | `3 / 2 / 1 / 5` | 1.75 | Rejected while evidence and disposition remain incomplete. |

Generic intake precedes any future narrow domain-profile evaluation, including a possible LEI-oriented profile, because identity, notice, import-closure, namespace, transformation, review, SBOM-handoff, offline, and unsupported-claim controls apply to every external semantic source. No LEI-oriented or other domain profile is approved or selected by this research. Implementing those controls first avoids treating a possible future profile as accepted before the reusable evidence boundary exists.

## Reproduction commands

The observations above were reproduced with `curl`, Python's standard `json` module, `wc`, and `sha256sum` in a temporary directory. No downloaded file was copied into the repository. Future sessions should re-run the primary-source checks because GitHub-generated archive bytes are observations, not publisher-signed release artifacts.
