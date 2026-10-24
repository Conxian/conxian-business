#!/usr/bin/env python3
"""Check the captured public claim/issue map; never grant operating acceptance."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/research/MONTHLY_ALIGNMENT_2026_10_24.json'
SHA = re.compile(r'[0-9a-f]{40}')
ACTIVITIES = ['Discover', 'Design', 'Acquire', 'Build', 'Transition', 'Operate', 'Deliver', 'Support']


def validate(data: dict) -> list[str]:
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    require(data.get('schema_version') == 1 and data.get('kind') == 'monthly-research-delivery-alignment', 'invalid monthly schema')
    for field in ['production_acceptance', 'independent_acceptance', 'exhaustive_semantic_audit']:
        require(data.get(field) is False, f'{field} cannot be inferred from a planning snapshot')
    require(data.get('public_safe') is True, 'public classification required')
    require('.github-private' not in json.dumps(data), 'private repository records cannot enter the public snapshot')
    require(data.get('itil5_activities') == ACTIVITIES, 'preserve the eight ITIL 5 activities')
    phases = {p['id']: p.get('name') for p in data.get('phases', [])}
    require(set(phases) == {f'R{i}' for i in range(6)} and len(data['phases']) == 6, 'phase set must remain R0..R5')
    require(phases.get('R5') == 'Deferred research and experiments', 'R5 cannot silently become sprint/release acceptance')
    repos = data.get('repository_baselines', [])
    names = [r['repository'] for r in repos]
    require(len(names) == len(set(names)) == data['coverage']['public_repositories'], 'repository coverage mismatch')
    for repo in repos:
        require(bool(SHA.fullmatch(repo.get('inspected_ref', ''))) and bool(SHA.fullmatch(repo.get('tree_sha', ''))), 'full repository/tree pins required')
        require(repo.get('inspected_ref') in repo.get('refs', {}).values(), 'inspected source must match a captured branch')
    sources = data.get('sources', [])
    source_ids = [s['id'] for s in sources]
    require(len(source_ids) == len(set(source_ids)), 'duplicate source identity')
    for source in sources:
        require(source.get('url', '').startswith('https://'), 'source URL required')
        if source.get('kind') == 'repository':
            commit, blob = source.get('commit', ''), source.get('blob', '')
            require(bool(SHA.fullmatch(commit)) and bool(SHA.fullmatch(blob)), 'repository source must pin commit and blob')
            require(source.get('url') == f"https://github.com/{source['repository']}/blob/{commit}/{source['path']}", 'source URL/pin mismatch')
    claims = data.get('claims', [])
    ids = [c['id'] for c in claims]
    require(len(ids) == len(set(ids)) and bool(ids), 'unique claim identities required')
    states = {'architecture-decision', 'implemented-bounded', 'tested-bounded', 'evidence-gap', 'specification', 'recommendation', 'research-only'}
    for claim in claims:
        require(claim.get('classification') in {'fact', 'inference', 'assumption', 'hypothesis', 'narrative', 'missing_evidence'}, 'claim classification required')
        require(claim.get('state') in states, 'unsupported claim maturity')
        require(claim.get('confidence') in {'low', 'medium', 'high', 'unknown'}, 'qualitative confidence required')
        require(bool(claim.get('source_ids')) and set(claim['source_ids']) <= set(source_ids), 'claim has absent/unknown source lineage')
    issues = data.get('issues', [])
    urls = [i['url'] for i in issues]
    require(len(urls) == len(set(urls)) == data['coverage']['public_open_issues'], 'issue count/uniqueness mismatch')
    require(set(urls) == set(data.get('observed_issue_inventory', [])), 'captured issue omitted or added without inventory refresh')
    groups = {g['id']: g for g in data.get('groups', [])}
    require(len(groups) == len(data.get('groups', [])), 'duplicate work group')
    for issue in issues:
        require(issue['url'] == f"https://github.com/{issue['repo']}/issues/{issue['number']}" and issue['id'] == f"{issue['repo']}#{issue['number']}", 'issue repository identity mismatch')
        require(issue['repo'] in names and issue.get('phase') in phases, 'issue has unknown owner repository/phase')
        require(bool(issue.get('existing_gap_ids')) and set(issue['existing_gap_ids']) <= set(groups), 'issue lacks existing work routing')
        require(bool(issue.get('owner_role')) and bool(issue.get('next_action')) and bool(issue.get('acceptance')), 'issue action, owner and acceptance required')
        require(issue.get('production_acceptance') is False, 'issue mapping cannot grant production acceptance')
    visiting, visited = set(), set()

    def visit(group):
        if group in visiting:
            errors.append('work dependency cycle')
            return
        if group in visited:
            return
        visiting.add(group)
        for parent in groups[group].get('depends_on', []):
            if parent not in groups:
                errors.append('unknown work dependency')
            else:
                visit(parent)
        visiting.remove(group)
        visited.add(group)

    for group in groups:
        visit(group)
    catalog = data.get('document_catalog', [])
    require(len(catalog) == data['coverage']['public_document_catalog'], 'document catalogue coverage mismatch')
    require(len({(s['repository'], s['path']) for s in catalog}) == len(catalog), 'duplicate catalogue source')
    for entry in catalog:
        require(entry['repository'] in names and bool(SHA.fullmatch(entry.get('commit', ''))) and bool(SHA.fullmatch(entry.get('blob', ''))), 'catalogue pin/owner missing')
    projects = data.get('project_alignment', {})
    require(projects.get('status') == 'unverified' and projects.get('mutation_performed') is False, 'do not invent Project access or mutations')
    recovery = data.get('recovery_fixture', {})
    require(recovery.get('fixture_only') is True and recovery.get('production_acceptance') is False and recovery.get('operator_independence_verified') is False, 'fixture restoration cannot become independent production recovery')
    return errors


def validate_documents(root: Path, data: dict) -> list[str]:
    errors = []
    paths = [root / 'docs/research/MONTHLY_RESEARCH_REVIEW_2026_10_24.md',
             root / 'docs/whitepaper/TECHNICAL_WHITEPAPER_EVIDENCE_DRAFT_2026_10_24.md',
             root / 'docs/architecture/ROADMAP_12_MONTH_CONTROL_PLANE.md']
    known = {c['id'] for c in data['claims']}
    for path in paths:
        text = path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://', '#')):
                continue
            if not (path.parent / target.split('#')[0]).resolve().is_file():
                errors.append(f'{path.name}: missing local document link')
        if path.name.startswith('TECHNICAL_WHITEPAPER_EVIDENCE'):
            if not {'candidate', '#1422', 'sprint-exit'} <= set(re.findall(r'candidate|#1422|sprint-exit', text)):
                errors.append('whitepaper publication gate required')
            for identity in re.findall(r'\bC\d{2}\b', text):
                if identity not in known:
                    errors.append('whitepaper has unmapped claim reference')
    return errors


def main() -> int:
    try:
        data = json.loads(SNAPSHOT.read_text())
        errors = validate(data) + validate_documents(ROOT, data)
    except (OSError, KeyError, ValueError, TypeError) as exc:
        errors = [f'invalid monthly input ({type(exc).__name__})']
    for error in errors:
        print('ERROR: ' + error, file=sys.stderr)
    if errors:
        return 1
    print('Monthly source/claim/issue alignment verified; no release or production authority granted.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
