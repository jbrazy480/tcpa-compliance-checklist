"""Every shipped example and niche config must load and validate offline."""
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pytest
import yaml
from tcpa_toolkit.calling_window import is_callable
from tcpa_toolkit.consent import validate_consent_log
from tcpa_toolkit.dnc import scrub_csv

ROOT = Path(__file__).resolve().parents[1]
NICHE_DIR = ROOT / 'examples' / 'niches'
NICHES = ['med-spa', 'home-services', 'marketing-agency', 'real-estate', 'insurance']
AT = datetime(2026, 9, 26, 14, tzinfo=timezone.utc)


def _check_window_policy(path):
    policy = yaml.safe_load(path.read_text())
    assert {'start', 'end', 'tz_override'} <= set(policy)
    ZoneInfo(policy['tz_override'])  # raises ZoneInfoNotFoundError if unknown
    result = is_callable('+12125550100', AT, start=policy['start'],
                          end=policy['end'], tz_override=policy['tz_override'])
    assert result.reason in ('within all local windows', 'outside one or more local windows')


def test_root_window_yaml_loads_and_validates():
    _check_window_policy(ROOT / 'examples' / 'window.yaml')


@pytest.mark.parametrize('niche', NICHES)
def test_niche_window_policy_loads_and_validates(niche):
    _check_window_policy(NICHE_DIR / f'{niche}.yaml')


@pytest.mark.parametrize('niche', NICHES)
def test_niche_leads_csv_scrubs(niche, tmp_path):
    report = scrub_csv(NICHE_DIR / f'{niche}-leads.csv', tmp_path / 'clean.csv',
                        [ROOT / 'examples' / 'internal_dnc.txt'], 'phone')
    assert report['total'] == 4
    assert report['kept'] == 2
    assert report['removed_count'] == 2


@pytest.mark.parametrize('niche', NICHES)
def test_niche_consent_log_validates(niche):
    result = validate_consent_log(NICHE_DIR / f'{niche}-consent.jsonl')
    assert result['valid'], result['errors']
    assert result['records'] == 1
