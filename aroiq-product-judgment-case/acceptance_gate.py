from __future__ import annotations
import csv, json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT=Path(__file__).parent
REQUIRED_SEMANTICS={"separator_pressure","gas_flow","valve_state","flare_pilot_status"}
CONF_FIELDS=["detection_confidence","causation_confidence","quantification_confidence"]

def read_csv(path):
    with open(path,newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def parse_utc(v):
    if not v.endswith('Z'): raise ValueError('must end Z')
    return datetime.fromisoformat(v.replace('Z','+00:00'))

def validate_mapping(rows):
    reject=[]; review=[]; by_fac=defaultdict(list); active_keys=set()
    for i,r in enumerate(rows,start=2):
        by_fac[r['facility_id']].append(r)
        key=(r['facility_id'],r['canonical_semantic'],r['mapping_version'])
        if key in active_keys: reject.append(f"conflicting_mapping row {i}: {key}")
        active_keys.add(key)
        if r['status']!='approved':
            review.append(f"mapping_not_approved {r['facility_id']}:{r['source_tag']} -> {r['canonical_semantic']}")
        if r['source_unit']!=r['canonical_unit'] and r['transform'] in ('','direct'):
            reject.append(f"unit_transform_missing row {i}: {r['source_tag']} {r['source_unit']} -> {r['canonical_unit']}")
    for fac,items in by_fac.items():
        sem={x['canonical_semantic'] for x in items if x['status']=='approved'}
        for missing in sorted(REQUIRED_SEMANTICS-sem):
            review.append(f"required_semantic_unapproved {fac}:{missing}")
    return reject,review

def validate_events(rows,required_fields):
    reject=[]; review=[]
    if not rows: return ['empty_event_dataset'],[]
    missing=[x for x in required_fields if x not in rows[0]]
    if missing: return [f"schema_missing:{','.join(missing)}"],[]
    seen=set()
    for i,r in enumerate(rows,start=2):
        key=(r['customer_id'],r['event_id'])
        if key in seen: reject.append(f"duplicate_event_id row {i}:{r['event_id']}")
        seen.add(key)
        try:
            if parse_utc(r['end_utc'])<=parse_utc(r['start_utc']): reject.append(f"invalid_time_window row {i}")
        except Exception: reject.append(f"invalid_timestamp row {i}")
        try:
            lo=float(r['volume_low_m3']); est=float(r['volume_estimate_m3']); hi=float(r['volume_high_m3'])
            if lo<0 or not(lo<=est<=hi): reject.append(f"invalid_volume_range row {i}")
        except Exception: reject.append(f"invalid_volume row {i}")
        for field in CONF_FIELDS:
            try:
                v=float(r[field])
                if not 0<=v<=1: review.append(f"confidence_out_of_bounds row {i}:{field}")
            except Exception: review.append(f"confidence_missing row {i}:{field}")
        for field in ('method_version','mapping_version','provenance_id'):
            if not r[field].strip(): reject.append(f"missing_{field} row {i}")
    return reject,review

def rollups(rows):
    facility=defaultdict(float)
    for r in rows: facility[r['facility_id']]+=float(r['volume_estimate_m3'])
    return dict(facility),sum(facility.values())

def reconcile_rollups(rows,reference):
    issues=[]; facility,total=rollups(rows); tol=float(reference['demo_tolerance_pct'])/100
    for fac,exp in reference['facility_totals_m3'].items():
        act=facility.get(fac,0.0); mismatch=abs(act-exp)/(exp if exp else 1)
        if mismatch>tol:
            issues.append(f"facility_rollup_outside_tolerance {fac}: expected={exp:.2f} actual={act:.2f} delta={mismatch*100:.2f}%")
    exp=float(reference['portfolio_total_m3']); mismatch=abs(total-exp)/(exp if exp else 1)
    if mismatch>tol:
        issues.append(f"portfolio_rollup_outside_tolerance expected={exp:.2f} actual={total:.2f} delta={mismatch*100:.2f}%")
    return issues,facility,total

def reconcile_reference_events(events,refs):
    issues=[]; matches=[]; used=set()
    for ref in refs:
        candidates=[]; rs,re=parse_utc(ref['start_utc']),parse_utc(ref['end_utc'])
        for idx,e in enumerate(events):
            if idx in used or e['facility_id']!=ref['facility_id'] or e['event_type']!=ref['event_type']: continue
            es,ee=parse_utc(e['start_utc']),parse_utc(e['end_utc'])
            overlap=max(rs,es)<min(re,ee) or (rs==es and re==ee)
            if overlap: candidates.append((idx,e))
        if not candidates:
            issues.append(f"reference_event_unmatched {ref['reference_id']}"); continue
        idx,e=min(candidates,key=lambda x:abs(float(x[1]['volume_estimate_m3'])-float(ref['reference_volume_m3'])))
        used.add(idx)
        refv=float(ref['reference_volume_m3']); est=float(e['volume_estimate_m3']); delta=abs(est-refv)/(refv if refv else 1)*100
        matches.append({'reference_id':ref['reference_id'],'event_id':e['event_id'],'volume_delta_pct':round(delta,2),'reference_volume_m3':refv,'estimate_volume_m3':est})
        if delta>5.0: issues.append(f"reference_event_volume_review {ref['reference_id']}->{e['event_id']}: delta={delta:.2f}%")
    return issues,matches

def evaluate(root=ROOT):
    contract=json.loads((root/'canonical_event_contract.json').read_text())
    mapping=read_csv(root/'data'/'customer_tag_map.csv')
    events=read_csv(root/'data'/'model_events.csv')
    refs=read_csv(root/'data'/'reference_events.csv')
    ref_roll=json.loads((root/'data'/'reference_rollups.json').read_text())
    reject=[]; review=[]
    a,b=validate_mapping(mapping); reject+=a; review+=b
    a,b=validate_events(events,contract['required_fields']); reject+=a; review+=b
    a,facility,total=reconcile_rollups(events,ref_roll); review+=a
    a,matches=reconcile_reference_events(events,refs); review+=a
    status='REJECT' if reject else ('REVIEW' if review else 'ACCEPT')
    return {'status':status,'human_acceptance_required':True,'reject_reasons':reject,'review_reasons':review,'facility_rollups_m3':facility,'portfolio_rollup_m3':total,'reference_event_matches':matches,'versions':{'contract':contract['contract_version'],'reference':ref_roll['reference_version'],'mapping':sorted({r['mapping_version'] for r in mapping}),'methods':sorted({r['method_version'] for r in events})}}

if __name__=='__main__':
    print(json.dumps(evaluate(),indent=2))
