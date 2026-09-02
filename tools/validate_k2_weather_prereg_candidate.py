#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / 'knowledge'
DEFAULT_MANIFEST = K / 'K2_QIMEN_CDAF_H2_PREREGISTRATION_CANDIDATE_V01.json'
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
SHA40_RE = re.compile(r'^[0-9a-f]{40}$')
SHA64_RE = re.compile(r'^[0-9a-f]{64}$')

EXPECTED = {
    'candidate_id': 'K2PV-CDAF-H2-PREREG-CANDIDATE-V01',
    'status': 'PRE_BATCH_CANDIDATE_NOT_PREREGISTERED',
    'plan_id': 'K2PV-CDAF-H2',
    'active_gate_authority': 'knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_GATE_AMENDMENT_V04.md',
    'weather_protocol_ref': 'knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md',
    'sample_plan_ref': 'knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md',
    'generator_commit_sha': 'd9bd5b1afd10a6fa68713b756172177f5d0aa09b',
    'model_name': 'FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V03',
    'qimen_engine_blob_sha': '3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd',
    'qimen_ju_method': 'CHAI_BU_FUTOU',
    'official_start_boundary_hkt_display': '2026-09-07T22:41+08:00',
    'official_start_boundary_resolution': 'HKO_OFFICIAL_MINUTE_DISPLAY',
    'official_start_boundary_source': 'https://www.hko.gov.hk/en/gts/astron2026/files/2026cal09.pdf',
    'first_daily_freeze_date_hkt': '2026-09-08',
    'daily_freeze_time_hkt': '17:00',
    'minimum_segments': 48,
    'maximum_segments': 72,
    'prefix_48_end_sample_date': '2028-09-06',
    'maximum_72_end_sample_date': '2029-09-06',
    'calendar_sham_policy': 'WITHIN_COMPLETE_SOLAR_TERM_SEGMENT_CYCLIC_PLUS_MINUS_1_DAY',
    'candidate_schedule_sha256': '97f07e9d9368acbb1a3d72aa90c54276a7b460af87cef3b933b994adda6c60e5',
    'schedule_generator_ref': 'ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenWeatherCalendarEquivalenceAuditTest.kt',
    'station_panel_source': 'https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall',
    'station_panel_resource_kind': 'Daily Total Rainfall Current Year',
    'station_panel_snapshot_date': '2026-08-31',
    'station_panel_count': 25,
    'station_panel_sha256': '1c8a07eee9c566486a82c3aa5b1d28144391bd93415d50479ae3a2620419a80d',
    'outcome_proxy': 'HK_TERRITORY_RAIN10_RESEARCH_PROXY_V01',
    'outcome_completeness_required': 'C_FOR_ALL_FROZEN_STATIONS',
    'outcome_aggregation': 'SIMPLE_ARITHMETIC_MEAN_MM',
    'outcome_threshold_mm': 10.0,
    'preoutcome_info_threshold_per_contrast': 80,
    'hac_kernel': 'Bartlett',
    'hac_max_lag_civil_days': 30,
    'fwer_alpha': 0.05,
    'number_of_primary_contrasts': 3,
    'z_critical': 2.1280452342,
    'metadata_recheck_required_before_preregistration': True,
    'invalidate_if_station_panel_changes': True,
    'late_preregistration_policy': 'ROLL_TO_NEXT_OFFICIAL_SOLAR_TERM_BOUNDARY',
    'weather_forecast_data_used': False,
    'weather_outcome_data_used': False,
    'batch_created': False,
    'freeze_created': False,
    'future_batch_schedule_frozen': False,
    'empirical_credit': 'NONE',
    'claim_extraction': 'BLOCKED',
}


def canonical_sha256(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def fail(msg):
    print(f'k2-weather-prereg-candidate: FAIL: {msg}', file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'invalid JSON {path}: {exc}')


def load_jsonl(path):
    if not path.exists():
        return []
    rows=[]
    for n, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except Exception as exc:
            fail(f'invalid JSONL {path}:{n}: {exc}')
    return rows


def validate_manifest(m, repo=ROOT, generated=None):
    issues=[]
    if not isinstance(m, dict):
        return ['manifest must be an object']
    allowed=set(EXPECTED)|{'stations','bonferroni_one_sided_alpha'}
    if set(m) != allowed:
        issues.append(f'field set mismatch missing={sorted(allowed-set(m))} extra={sorted(set(m)-allowed)}')
    for key, value in EXPECTED.items():
        if m.get(key) != value:
            issues.append(f'{key} mismatch: {m.get(key)!r} != {value!r}')
    alpha=m.get('bonferroni_one_sided_alpha')
    if not isinstance(alpha,(int,float)) or isinstance(alpha,bool) or abs(alpha-(0.05/3))>1e-15:
        issues.append('bonferroni_one_sided_alpha must equal 0.05/3')
    if not SHA40_RE.match(str(m.get('generator_commit_sha',''))): issues.append('generator_commit_sha must be lowercase SHA-1')
    if not SHA40_RE.match(str(m.get('qimen_engine_blob_sha',''))): issues.append('qimen_engine_blob_sha must be lowercase SHA-1')
    if not SHA64_RE.match(str(m.get('candidate_schedule_sha256',''))): issues.append('candidate_schedule_sha256 must be lowercase SHA-256')
    if not SHA64_RE.match(str(m.get('station_panel_sha256',''))): issues.append('station_panel_sha256 must be lowercase SHA-256')

    for ref_key in ('active_gate_authority','weather_protocol_ref','sample_plan_ref','schedule_generator_ref'):
        ref=m.get(ref_key)
        if isinstance(ref,str) and not (repo/ref).is_file(): issues.append(f'{ref_key} path missing: {ref}')

    stations=m.get('stations')
    if not isinstance(stations,list):
        issues.append('stations must be an array')
    else:
        if len(stations)!=25: issues.append(f'stations must contain 25 rows, found {len(stations)}')
        names=[]; ids=[]
        for idx,row in enumerate(stations,1):
            if not isinstance(row,dict) or set(row)!={'station_name','resource_id'}:
                issues.append(f'station row {idx} fields invalid'); continue
            name=row.get('station_name'); rid=row.get('resource_id')
            if not isinstance(name,str) or not name.strip(): issues.append(f'station row {idx} name invalid')
            if not isinstance(rid,str) or not UUID_RE.match(rid): issues.append(f'station row {idx} resource_id invalid')
            names.append(name); ids.append(rid)
        if len(names)!=len(set(names)): issues.append('duplicate station_name')
        if len(ids)!=len(set(ids)): issues.append('duplicate resource_id')
        if m.get('station_panel_count') != len(stations): issues.append('station_panel_count does not match stations length')
        if m.get('station_panel_sha256') != canonical_sha256(stations): issues.append('station_panel_sha256 mismatch')

    plans=load_jsonl(repo/'knowledge/K2_PROSPECTIVE_TEST_PLANS.jsonl')
    plan=next((p for p in plans if p.get('plan_id')=='K2PV-CDAF-H2'),None)
    if not plan:
        issues.append('K2PV-CDAF-H2 plan missing')
    else:
        if plan.get('model_name') != m.get('model_name'): issues.append('candidate model_name does not match plan')
        controls=' '.join(plan.get('leakage_controls') or [])
        if 'HAC_MAX_LAG=30 civil days' not in controls: issues.append('plan no longer freezes HAC_MAX_LAG=30')
        if '48个完整节气段' not in controls: issues.append('plan no longer freezes 48-segment minimum')
        if '72段' not in controls: issues.append('plan no longer freezes 72-segment maximum')

    for filename, label in (
        ('K2_PROSPECTIVE_BATCHES.jsonl','Batch'),
        ('K2_PROSPECTIVE_FREEZES.jsonl','Freeze'),
        ('K2_PROSPECTIVE_OUTCOMES.jsonl','Outcome'),
    ):
        rows=load_jsonl(repo/'knowledge'/filename)
        if rows: issues.append(f'{label} rows already exist while candidate says not preregistered')

    if generated is not None:
        if not isinstance(generated,dict):
            issues.append('generated schedule must be object')
        else:
            checks={
                'candidate_scope':'OUTCOME_BLIND_PRE_BATCH_SCHEDULE_CANDIDATE_ONLY',
                'candidate_version':'K2PV-CDAF-H2-SCHEDULE-CANDIDATE-V01',
                'status':'PRE_BATCH_CANDIDATE_NOT_FROZEN',
                'plan_id':m.get('plan_id'),
                'model_name':m.get('model_name'),
                'qimen_engine_blob_sha':m.get('qimen_engine_blob_sha'),
                'qimen_ju_method':m.get('qimen_ju_method'),
                'official_start_boundary_hkt_display':m.get('official_start_boundary_hkt_display'),
                'official_start_boundary_resolution':m.get('official_start_boundary_resolution'),
                'official_start_boundary_source':m.get('official_start_boundary_source'),
                'first_daily_freeze_date_hkt':m.get('first_daily_freeze_date_hkt'),
                'daily_freeze_time_hkt':m.get('daily_freeze_time_hkt'),
                'minimum_segments':m.get('minimum_segments'),
                'maximum_segments':m.get('maximum_segments'),
                'prefix_48_end_sample_date':m.get('prefix_48_end_sample_date'),
                'maximum_72_end_sample_date':m.get('maximum_72_end_sample_date'),
                'calendar_sham_policy':m.get('calendar_sham_policy'),
                'candidate_schedule_sha256':m.get('candidate_schedule_sha256'),
                'weather_forecast_data_used':False,
                'weather_outcome_data_used':False,
                'batch_created':False,
                'freeze_created':False,
                'future_batch_schedule_frozen':False,
                'empirical_credit':'NONE',
            }
            for key,value in checks.items():
                if generated.get(key)!=value: issues.append(f'generated schedule {key} mismatch')
            segs=generated.get('segments')
            if not isinstance(segs,list) or len(segs)!=72:
                issues.append('generated schedule must contain exactly 72 segments')
            elif len({s.get('segment_id') for s in segs if isinstance(s,dict)})!=72:
                issues.append('generated schedule segment_id values must be unique')
    return issues


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest', default=str(DEFAULT_MANIFEST))
    ap.add_argument('--generated-schedule')
    args=ap.parse_args()
    generated=load_json(Path(args.generated_schedule)) if args.generated_schedule else None
    issues=validate_manifest(load_json(Path(args.manifest)), ROOT, generated)
    if issues: fail(f'issues={len(issues)} first={issues[0]}')
    print('k2-weather-prereg-candidate: PASS')
    print('candidate=K2PV-CDAF-H2-PREREG-CANDIDATE-V01 batch_created=false freeze_created=false outcome_data_used=false empirical_credit=NONE')
    print('schedule_sha256=97f07e9d9368acbb1a3d72aa90c54276a7b460af87cef3b933b994adda6c60e5 station_panel_sha256=1c8a07eee9c566486a82c3aa5b1d28144391bd93415d50479ae3a2620419a80d stations=25')

if __name__=='__main__': main()
