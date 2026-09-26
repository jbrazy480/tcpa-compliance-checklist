from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytest
from tcpa_toolkit.calling_window import is_callable, next_allowed_time, timezone_map
from tcpa_toolkit.phones import normalize_phone


def dt(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


@pytest.mark.parametrize('at,allowed', [
    ('2026-01-10T12:59:59Z', False), ('2026-01-10T13:00:00Z', True),
    ('2026-01-11T01:59:59Z', True), ('2026-01-11T02:00:00Z', False),
    ('2026-07-10T11:59:59Z', False), ('2026-07-10T12:00:00Z', True),
    ('2026-07-11T00:59:59Z', True), ('2026-07-11T01:00:00Z', False),
    ('2026-03-08T06:59:59Z', False), ('2026-03-08T07:00:00Z', False),
    ('2026-03-08T11:59:59Z', False), ('2026-03-08T12:00:00Z', True),
    ('2026-11-01T05:30:00Z', False), ('2026-11-01T06:30:00Z', False),
    ('2026-11-01T12:59:59Z', False), ('2026-11-01T13:00:00Z', True),
])
def test_eastern_boundaries(at, allowed):
    assert is_callable('+12125550100', dt(at)).allowed is allowed


@pytest.mark.parametrize('at,offset', [('2026-03-08T06:59:00Z', '-05:00'),
    ('2026-03-08T07:00:00Z', '-04:00'), ('2026-11-01T05:30:00Z', '-04:00'),
    ('2026-11-01T06:30:00Z', '-05:00')])
def test_dst_local_offsets(at, offset):
    assert is_callable('+12125550100', dt(at)).local_times['America/New_York'].endswith(offset)


@pytest.mark.parametrize('phone,at,allowed', [
    ('+12085550100','2026-07-10T14:00:00Z',False),
    ('+12085550100','2026-07-10T15:00:00Z',True),
    ('+18125550100','2026-07-10T12:00:00Z',False),
    ('+18125550100','2026-07-10T13:00:00Z',True),
    ('+17095550100','2026-01-10T11:30:00Z',False),
    ('+17095550100','2026-01-10T12:00:00Z',True),
    ('+16025550100','2026-07-10T14:59:00Z',False),
    ('+16025550100','2026-01-10T15:00:00Z',True),
    ('+18085550100','2026-07-10T18:00:00Z',True),
])
def test_zone_intersections(phone, at, allowed):
    assert is_callable(phone, dt(at)).allowed is allowed


@pytest.mark.parametrize('at,expected', [
    ('2026-03-08T06:30:00Z','2026-03-08T12:00:00Z'),
    ('2026-11-01T05:30:00Z','2026-11-01T13:00:00Z'),
    ('2026-11-01T06:30:00Z','2026-11-01T13:00:00Z'),
    ('2026-07-11T01:00:00Z','2026-07-11T12:00:00Z'),
    ('2026-07-10T11:59:59.999999Z','2026-07-10T12:00:00Z'),
    ('2026-07-10T15:34:56.123456Z','2026-07-10T15:34:56.123456Z'),
])
def test_next_dst_and_precision(at, expected):
    assert next_allowed_time('+12125550100', dt(at)) == dt(expected)


def test_next_multizone():
    assert next_allowed_time('+12085550100',dt('2026-07-10T14:00:00Z')) == dt('2026-07-10T15:00:00Z')


def test_no_common_window():
    assert next_allowed_time('+12085550100',dt('2026-07-10T14:00:00Z'), '08:00', '08:01') is None


def test_unknown_and_override():
    result = is_callable('+19995550100',dt('2026-07-10T14:00:00Z'))
    assert not result.allowed and result.reason == 'unknown timezone, supply tz_override'
    assert next_allowed_time('+19995550100',dt('2026-07-10T14:00:00Z')) is None
    assert is_callable('+19995550100',dt('2026-07-10T14:00:00Z'),tz_override='America/New_York').allowed


def test_override_replaces_npa():
    assert not is_callable('+12125550100',dt('2026-07-10T13:00:00Z'),tz_override='America/Los_Angeles').allowed


def test_stricter():
    assert not is_callable('+12125550100',dt('2026-07-10T12:00:00Z'),'09:00','20:00').allowed
    assert next_allowed_time('+12125550100',dt('2026-07-10T12:00:00Z'),'09:00','20:00') == dt('2026-07-10T13:00:00Z')


@pytest.mark.parametrize('phone', ['2125550100','+11255550100','+12121550100','+442125550100','+12125550100x1','+121255501000','',None])
def test_invalid_phone(phone):
    with pytest.raises(ValueError):
        is_callable(phone,dt('2026-07-10T12:00:00Z'))


@pytest.mark.parametrize('start,end', [('07:00','21:00'),('08:00','22:00'),('21:00','08:00'),('09:00','09:00'),('8:00','21:00'),('08:60','21:00'),('25:00','21:00')])
def test_invalid_windows(start,end):
    with pytest.raises(ValueError):
        is_callable('+12125550100',dt('2026-07-10T12:00:00Z'),start,end)


def test_naive():
    with pytest.raises(ValueError):
        is_callable('+12125550100',datetime(2026,1,1))


def test_invalid_zone():
    with pytest.raises(ValueError):
        is_callable('+12125550100',dt('2026-01-01T12:00:00Z'),tz_override='Unknown/Zone')


def test_aware_non_utc():
    at = datetime(2026,7,10,8,tzinfo=ZoneInfo('America/New_York'))
    assert next_allowed_time('+12125550100',at) == dt('2026-07-10T12:00:00Z')
    assert next_allowed_time('+12125550100',at).tzinfo == timezone.utc


@pytest.mark.parametrize('phone', ['2125550100','1 (212) 555-0100','+1-212-555-0100','212.555.0100'])
def test_normalize(phone):
    assert normalize_phone(phone) == '+12125550100'


@pytest.mark.parametrize('phone', ['+2125550100','2125550100 ext 1','(012) 555-0100','2121550100','abc', '１２１２５５５０１００'])
def test_normalize_reject(phone):
    with pytest.raises(ValueError):
        normalize_phone(phone)


def test_data_resolves():
    mapping=timezone_map()
    assert len(mapping)>=400
    for npa,zones in mapping.items():
        assert len(npa)==3 and zones
        for zone in zones:
            ZoneInfo(zone)


@pytest.mark.parametrize('a,b',[('208','986'),('812','930'),('850','448')])
def test_overlay_zone_union(a,b):
    assert timezone_map()[a]==timezone_map()[b]


def test_territorial_fixed_zones():
    assert 'America/Whitehorse' in timezone_map()['867']
    assert 'America/Fort_Nelson' in timezone_map()['250']
    assert 'America/Dawson_Creek' in timezone_map()['257']
