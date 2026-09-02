#!/usr/bin/env python3
import copy, importlib.util, json, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('validator', ROOT/'tools/validate_k2_weather_prereg_candidate.py')
v=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(v)
BASE=json.loads((ROOT/'knowledge/K2_QIMEN_CDAF_H2_PREREGISTRATION_CANDIDATE_V01.json').read_text(encoding='utf-8'))


def generated_from_manifest(m):
    return {
        'candidate_scope':'OUTCOME_BLIND_PRE_BATCH_SCHEDULE_CANDIDATE_ONLY',
        'candidate_version':'K2PV-CDAF-H2-SCHEDULE-CANDIDATE-V01',
        'status':'PRE_BATCH_CANDIDATE_NOT_FROZEN',
        'plan_id':m['plan_id'],
        'model_name':m['model_name'],
        'qimen_engine_blob_sha':m['qimen_engine_blob_sha'],
        'qimen_ju_method':m['qimen_ju_method'],
        'official_start_boundary_hkt_display':m['official_start_boundary_hkt_display'],
        'official_start_boundary_resolution':m['official_start_boundary_resolution'],
        'official_start_boundary_source':m['official_start_boundary_source'],
        'first_daily_freeze_date_hkt':m['first_daily_freeze_date_hkt'],
        'daily_freeze_time_hkt':m['daily_freeze_time_hkt'],
        'minimum_segments':m['minimum_segments'],
        'maximum_segments':m['maximum_segments'],
        'prefix_48_end_sample_date':m['prefix_48_end_sample_date'],
        'maximum_72_end_sample_date':m['maximum_72_end_sample_date'],
        'segment_count':72,
        'calendar_sham_policy':m['calendar_sham_policy'],
        'candidate_schedule_sha256':m['candidate_schedule_sha256'],
        'weather_forecast_data_used':False,
        'weather_outcome_data_used':False,
        'batch_created':False,
        'freeze_created':False,
        'future_batch_schedule_frozen':False,
        'empirical_credit':'NONE',
        'segments':[{'segment_id':f'{i:02d}:TEST'} for i in range(1,73)],
    }

GENERATED=generated_from_manifest(BASE)


def make_repo(tmp):
    root=Path(tmp)
    (root/'knowledge').mkdir(parents=True)
    for rel in [BASE['active_gate_authority'],BASE['weather_protocol_ref'],BASE['sample_plan_ref'],BASE['schedule_generator_ref']]:
        p=root/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('stub',encoding='utf-8')
    plan={"plan_id":"K2PV-CDAF-H2","model_name":BASE['model_name'],"leakage_controls":["HAC_MAX_LAG=30 civil days","48个完整节气段","MAX 72段"]}
    (root/'knowledge/K2_PROSPECTIVE_TEST_PLANS.jsonl').write_text(json.dumps(plan,ensure_ascii=False)+'\n',encoding='utf-8')
    return root


def validate(repo,m=None,g=None):
    return v.validate_manifest(copy.deepcopy(m or BASE), repo=repo, generated=copy.deepcopy(GENERATED if g is None else g))


def must_fail(repo, mutate, generated=False):
    m=copy.deepcopy(BASE)
    g=copy.deepcopy(GENERATED)
    mutate(g if generated else m)
    issues=v.validate_manifest(m,repo=repo,generated=g)
    assert issues, mutate

with tempfile.TemporaryDirectory() as td:
    repo=make_repo(td)
    assert not validate(repo), validate(repo)
    for case in [
        lambda m:m.__setitem__('candidate_schedule_sha256','0'*64),
        lambda m:m.__setitem__('station_panel_sha256','0'*64),
        lambda m:m.__setitem__('station_panel_count',24),
        lambda m:m['stations'].pop(),
        lambda m:m['stations'][1].__setitem__('resource_id',m['stations'][0]['resource_id']),
        lambda m:m.__setitem__('hac_max_lag_civil_days',7),
        lambda m:m.__setitem__('maximum_segments',60),
        lambda m:m.__setitem__('weather_outcome_data_used',True),
        lambda m:m.__setitem__('batch_created',True),
        lambda m:m.__setitem__('empirical_credit','POSITIVE'),
        lambda m:m.__setitem__('late_preregistration_policy','ALLOW_BACKDATE'),
    ]:
        must_fail(repo,case)
    must_fail(repo,lambda g:g.__setitem__('candidate_schedule_sha256','f'*64),generated=True)
    must_fail(repo,lambda g:g.__setitem__('weather_outcome_data_used',True),generated=True)
    (repo/'knowledge/K2_PROSPECTIVE_BATCHES.jsonl').write_text('{}\n',encoding='utf-8')
    assert validate(repo), 'nonempty Batch must fail candidate gate'

print('k2-weather-prereg-candidate-tests: PASS')
print('negative_cases=14 static_candidate_binding=PASS generated_schedule_binding=PASS outcome_blind=PASS')
