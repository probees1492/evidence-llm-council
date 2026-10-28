#!/usr/bin/env python3
"""Mechanical provenance guard. Not a semantic fact checker."""
import argparse
import json
import re
import sys
from pathlib import Path


def check(ledger, report):
    errors, warnings = [], []
    evidence = ledger.get('evidence')
    claims = report.get('claims')
    if not isinstance(evidence, list):
        return ['ledger.evidence must be a list'], warnings
    if not isinstance(claims, list):
        return ['report.claims must be a list'], warnings
    known = set()
    for n, e in enumerate(evidence, 1):
        if not isinstance(e, dict):
            errors.append(f'evidence[{n}] is not an object'); continue
        eid = e.get('id')
        if not isinstance(eid, str) or not re.fullmatch(r'E\d{3,}', eid):
            errors.append(f'evidence[{n}] invalid ID: {eid!r}')
        if eid in known:
            errors.append(f'duplicate evidence ID {eid}')
        known.add(eid)
        for field in ('source_type', 'title', 'locator', 'excerpt'):
            if not isinstance(e.get(field), str) or not e[field].strip():
                errors.append(f'{eid}: missing {field}')
        if not (e.get('url') or e.get('file_path')):
            errors.append(f'{eid}: missing url or file_path')
    seen_claims = set()
    for n, c in enumerate(claims, 1):
        if not isinstance(c, dict):
            errors.append(f'claim[{n}] is not an object'); continue
        cid, kind = c.get('id'), c.get('kind')
        if not isinstance(cid, str) or not re.fullmatch(r'C\d{3,}', cid):
            errors.append(f'claim[{n}] invalid ID: {cid!r}')
        if cid in seen_claims:
            errors.append(f'duplicate claim ID {cid}')
        seen_claims.add(cid)
        if kind not in ('F', 'I', 'U'):
            errors.append(f'{cid}: unknown kind {kind}')
        if not isinstance(c.get('text'), str) or not c['text'].strip():
            errors.append(f'{cid}: missing text')
        refs = c.get('evidence_ids', [])
        if not isinstance(refs, list):
            errors.append(f'{cid}: evidence_ids must be list'); continue
        for ref in refs:
            if ref not in known:
                errors.append(f'{cid}: missing evidence {ref}')
        if kind == 'F' and not refs:
            errors.append(f'{cid}: factual claim lacks evidence')
        if kind == 'I' and not refs and not c.get('assumptions'):
            errors.append(f'{cid}: interpretation lacks evidence or stated assumptions')
        if kind == 'I' and not refs:
            warnings.append(f'{cid}: assumption-only interpretation, manual review needed')
        if kind == 'U' and refs:
            warnings.append(f'{cid}: unknown claim has evidence; verify framing')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', required=True)
    parser.add_argument('--claims', required=True)
    args = parser.parse_args()
    try:
        ledger = json.loads(Path(args.ledger).read_text(encoding='utf-8'))
        report = json.loads(Path(args.claims).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as ex:
        print(f'FAIL: {ex}', file=sys.stderr)
        return 2
    errors, warnings = check(ledger, report)
    for w in warnings:
        print('WARN:', w)
    for e in errors:
        print('FAIL:', e)
    print(f'{"PASS" if not errors else "FAIL"}: {len(ledger.get("evidence", []))} evidence / {len(report.get("claims", []))} claims / {len(errors)} errors / {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
