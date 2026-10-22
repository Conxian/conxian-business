#!/usr/bin/env python3
"""Validate a dated coordination snapshot; never grant runtime/release authority."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'docs/research_implementation_reconciliation_2026_10_15.json'
HISTORICAL = ROOT / 'docs/bos_research_candidate_ledger.json'
SHA = re.compile(r'^[0-9a-f]{40}$')


def validate(data: dict, historical: dict) -> list[str]:
    errors: list[str] = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)
    require(data.get('schema_version') == '1.0.0', 'unsupported schema')
    require(data.get('kind') == 'research-implementation-reconciliation', 'wrong artifact kind')
    for field in ('production_authorization', 'independent_acceptance', 'restricted_details_included', 'exhaustive_security_audit'):
        require(data.get(field) is False, f'{field} must remain false')
    phases = data.get('phases', [])
    phase_ids = [p['id'] for p in phases]
    require(len(phase_ids) == len(set(phase_ids)) and set(phase_ids) == {f'R{i}' for i in range(6)}, 'phase set must be R0..R5')
    gaps = data.get('gaps', [])
    gap_ids = [g['id'] for g in gaps]
    require(len(gap_ids) == len(set(gap_ids)), 'duplicate gap id')
    gap_set = set(gap_ids)
    by_id = {g['id']: g for g in gaps}
    allowed_states = {'coordination', 'evidence-missing', 'integration-missing', 'deferred-research', 'implemented-bounded'}
    for g in gaps:
        require(g.get('phase') in phase_ids, f'{g["id"]}: unknown phase')
        require(g.get('priority') in {'P0', 'P1', 'P2'}, f'{g["id"]}: invalid priority')
        require(g.get('state') in allowed_states, f'{g["id"]}: invalid state')
        require(bool(g.get('owner_repository')) and bool(g.get('next_action')) and bool(g.get('acceptance')), f'{g["id"]}: owner/action/acceptance required')
        require(bool(g.get('canonical_issues')), f'{g["id"]}: canonical tracker required')
        require(g.get('production_support') == 'not_established' and g.get('independent_acceptance') is False, f'{g["id"]}: unsupported acceptance grant')
        require(set(g.get('depends_on', [])) <= gap_set, f'{g["id"]}: unknown dependency')
        for s in g.get('sources', []) + g.get('implementation_evidence', []):
            require(bool(SHA.fullmatch(s.get('commit', ''))) and bool(SHA.fullmatch(s.get('blob', ''))), f'{g["id"]}: source pin must be immutable')
            require(f'/blob/{s.get("commit")}/' in s.get('url', ''), f'{g["id"]}: source URL must match pin')
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            errors.append('dependency cycle')
            return
        if node in visited or node not in by_id:
            return
        visiting.add(node)
        for parent in by_id[node].get('depends_on', []):
            visit(parent)
        visiting.remove(node)
        visited.add(node)
    for node in gap_ids:
        visit(node)
    expected = {c['id']: (c['scored'], c.get('total')) for c in historical['candidates'] + historical['unscoredGaps']}
    observed = {c['id']: (c['historical_scored'], c.get('historical_total')) for c in data.get('legacy_candidates', [])}
    require(observed == expected and len(data.get('legacy_candidates', [])) == len(expected), 'historical candidate set/scores must be preserved')
    for c in data.get('legacy_candidates', []):
        require(bool(c.get('gap_ids')) and set(c['gap_ids']) <= gap_set, f'{c["id"]}: unmapped candidate')
    issues = data.get('issue_alignment', [])
    issue_ids = [(i['repo'], i['number']) for i in issues]
    require(len(issue_ids) == len(set(issue_ids)), 'duplicate issue assignment')
    for i in issues:
        require(i.get('phase') in phase_ids and bool(i.get('owner_role')) and bool(i.get('next_action')), 'issue phase/owner/action required')
        require(bool(i.get('gap_ids')) and set(i['gap_ids']) <= gap_set, 'issue must map to known gaps')
        if i.get('restricted'):
            require(i.get('title') == 'Restricted review coordination', 'restricted issue title must be sanitized')
            require(not {'body', 'patch', 'reproduction', 'secret'} & set(i), 'restricted details cannot be embedded')
    for g in gaps:
        require(all((t['repo'], t['number']) in issue_ids for t in g['canonical_issues']), f'{g["id"]}: tracker absent from issue snapshot')
    coverage = data.get('coverage', {})
    require(coverage.get('open_issue_snapshot') == len(issues) and coverage.get('legacy_candidates') == len(expected), 'coverage counts do not match records')
    require(coverage.get('gaps') == len(gaps) and coverage.get('phases') == len(phases), 'work/phase counts do not match')
    manifest = data.get('catalog_manifest', {})
    require(manifest.get('entries') == coverage.get('catalog_entries') == sum(manifest.get('by_repository', {}).values()), 'catalog coverage mismatch')
    require(bool(re.fullmatch(r'[0-9a-f]{64}', manifest.get('sha256', ''))), 'catalog digest required')
    require(data.get('project_alignment', {}).get('mutation_performed') is False, 'no Project mutation may be invented')
    review = data.get('restricted_review', {})
    require(review.get('details_included') is False and review.get('public_issue_or_patch_created') is False, 'restricted review must remain sanitized')
    return errors


def main() -> int:
    try:
        errors = validate(json.loads(DEFAULT.read_text()), json.loads(HISTORICAL.read_text()))
    except (ValueError, KeyError, TypeError, OSError) as error:
        errors = [f'invalid reconciliation input: {error}']
    if errors:
        print('\n'.join('ERROR: ' + e for e in errors), file=sys.stderr)
        return 1
    print('Verified research/issue/phase snapshot; no runtime or release authorization granted.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
