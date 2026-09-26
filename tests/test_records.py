import json
from pathlib import Path
import pytest
import yaml
from tcpa_toolkit.consent import validate_consent_log
from tcpa_toolkit.dnc import load_dnc, is_dnc, scrub_csv
from tcpa_toolkit.checklist import checklist_progress

ROOT=Path(__file__).resolve().parents[1]


def record():
    return json.loads((ROOT/'examples/consent.jsonl').read_text())


def validate(tmp_path, value):
    p=tmp_path/'consent.jsonl'
    p.write_text(json.dumps(value)+'\n')
    return validate_consent_log(p)


def test_valid_consent(tmp_path):
    assert validate(tmp_path,record()) == {'valid':True,'records':1,'errors':[]}


@pytest.mark.parametrize('field,value', [
    ('phone','2125550100'),('consent_type','implied'),('timestamp','yesterday'),
    ('timestamp','2026-09-25T15:00:00'),('timestamp','2026-02-30T00:00:00Z'),
    ('source',''),('source_url','not a URL'),('disclosure_text',''),
    ('ip_address','999.1.1.1'),('revoked_at','bad'),('evidence_reference',''),('extra','field'),
])
def test_invalid_fields(tmp_path,field,value):
    data=record(); data[field]=value
    result=validate(tmp_path,data)
    assert not result['valid'] and result['errors'][0]['line']==1


@pytest.mark.parametrize('field',['phone','consent_type','timestamp','source','disclosure_text','evidence_reference'])
def test_required(tmp_path,field):
    data=record(); del data[field]
    assert not validate(tmp_path,data)['valid']


def test_revoked_record_still_structural(tmp_path):
    data=record(); data['revoked_at']='2026-09-26T00:00:00Z'
    data['ip_address']='2001:db8::1'; data['user_agent']='demo'
    assert validate(tmp_path,data)['valid']


def test_revocation_order(tmp_path):
    data=record(); data['revoked_at']='2026-09-24T00:00:00Z'
    assert not validate(tmp_path,data)['valid']


@pytest.mark.parametrize('content',['','\n','not json\n','[]\n','null\n'])
def test_malformed_log(tmp_path,content):
    p=tmp_path/'log'; p.write_text(content)
    assert not validate_consent_log(p)['valid']


def test_log_line_numbers(tmp_path):
    p=tmp_path/'log'; p.write_text(json.dumps(record())+'\n{\n')
    result=validate_consent_log(p)
    assert result['records']==2 and result['errors'][0]['line']==2


def test_internal_scrub(tmp_path):
    output=tmp_path/'out.csv'
    report=scrub_csv(ROOT/'examples/leads.csv',output,[ROOT/'examples/internal_dnc.txt'],'phone')
    assert report=={'total':4,'kept':2,'removed_count':2,'removed':[{'row':4,'reason':'internal_dnc'},{'row':5,'reason':'invalid_phone'}],'scope':'internal lists only'}
    assert 'West Example' in output.read_text()
    assert 'Suppressed' not in output.read_text()


def test_load_normalize_union(tmp_path):
    a=tmp_path/'a'; b=tmp_path/'b'
    a.write_text('# comment\n\n(212) 555-0100\n')
    b.write_text('+12125550100\n4155550101\n')
    numbers=load_dnc([a,b])
    assert len(numbers)==2 and is_dnc('1-212-555-0100',numbers)
    assert not is_dnc('2125550102',numbers)


def test_bad_dnc_preserves_output(tmp_path):
    block=tmp_path/'block'; output=tmp_path/'out'
    block.write_text('typo\n'); output.write_text('original')
    with pytest.raises(ValueError):
        scrub_csv(ROOT/'examples/leads.csv',output,[block],'phone')
    assert output.read_text()=='original'


@pytest.mark.parametrize('content', ['name\nAlice\n','phone,phone\n1,2\n','phone,name\n2125550100\n','phone\n2125550100,extra\n'])
def test_invalid_csv(tmp_path,content):
    p=tmp_path/'in'; p.write_text(content)
    with pytest.raises(ValueError):
        scrub_csv(p,tmp_path/'out',[],'phone')
    assert not (tmp_path/'out').exists()


def test_same_path_rejected(tmp_path):
    p=tmp_path/'in'; p.write_text('phone\n2125550100\n')
    with pytest.raises(ValueError):
        scrub_csv(p,p,[],'phone')


def test_custom_column_and_empty(tmp_path):
    p=tmp_path/'in'; p.write_text('telephone,name\n')
    report=scrub_csv(p,tmp_path/'out',[],'telephone')
    assert report['total']==0


def test_progress():
    result=checklist_progress(ROOT/'examples/status.yaml')
    assert result['done']==2 and result['total']==25
    assert any(r['status']=='todo' for r in result['items'])


@pytest.mark.parametrize('content', ['unknown: done','scope: invalid','[]','scope: true',''])
def test_bad_progress(tmp_path,content):
    p=tmp_path/'status'; p.write_text(content)
    with pytest.raises(ValueError):
        checklist_progress(p)


def test_packaged_copies_and_ids():
    for name in ['checklist.yaml','consent_log.schema.json']:
        assert (ROOT/name).read_bytes()==(ROOT/'tcpa_toolkit/data'/name).read_bytes()
    checklist=yaml.safe_load((ROOT/'checklist.yaml').read_text())
    items=[i for g in checklist['groups'] for i in g['items']]
    ids=[i['id'] for i in items]
    assert len(ids)==len(set(ids))
    markdown=(ROOT/'CHECKLIST.md').read_text()
    for item in items:
        assert item['id']+':' in markdown and item['detail'] in markdown


@pytest.mark.parametrize('field,value', [
    ('timestamp','2026-09-25T15:00:00+01:99'),
    ('timestamp','2026-09-25T15:00:00+25:00'),
    ('timestamp','2026-09-25 15:00:00Z'),
    ('source_url','https://'),('source_url','https://example.com/%zz'),
    ('source_url','https://example.com:invalid/path'),
    ('source_url','ftp://example.com'),
])
def test_stdlib_formats_reject(tmp_path,field,value):
    data=record();data[field]=value
    assert not validate(tmp_path,data)['valid']


def test_lowercase_timestamp(tmp_path):
    data=record();data['timestamp']='2026-09-25t15:00:00z'
    data['revoked_at']='2026-09-25t16:00:00z'
    assert validate(tmp_path,data)['valid']
