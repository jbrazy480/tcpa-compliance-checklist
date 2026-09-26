"""Rebuild bundled data from a locally downloaded upstream metadata file."""
import json, pathlib, hashlib, sys
root=pathlib.Path('tcpa_toolkit/data')
zones={'America/Adak','America/Anchorage','America/Boise','America/Chicago','America/Denver','America/Edmonton','America/Fort_Nelson','America/Halifax','America/Juneau','America/Los_Angeles','America/New_York','America/North_Dakota/Center','America/Phoenix','America/Regina','America/St_Johns','America/Toronto','America/Vancouver','America/Winnipeg','Pacific/Honolulu'}
m={}
raw=pathlib.Path(sys.argv[1]).read_text()
for line in raw.splitlines():
    if line.startswith('#') or '|' not in line: continue
    prefix, names=line.split('|')
    names=set(names.split('&'))
    if prefix.startswith('1') and len(prefix)>=4 and names <= zones:
        m.setdefault(prefix[1:4],set()).update(names)
# Conservative overlay unions, documented in docs/timezone-data.md.
for codes in [('208','986'), ('812','930'), ('850','448')]:
    union=set().union(*(m.get(code,set()) for code in codes))
    for code in codes: m[code]=union.copy()
bc=set().union(*(m.get(code,set()) for code in ['250','604','778','236','672']))
bc.update({'America/Dawson_Creek','America/Fort_Nelson','America/Creston'})
m.setdefault('250',set()).update(bc)
for code in ['778','236','672','257']: m[code]=bc.copy()
m.setdefault('867',set()).update({'America/Whitehorse','America/Dawson','America/Rankin_Inlet','America/Cambridge_Bay','America/Inuvik','America/Iqaluit','America/Atikokan'})
(root/'npa_timezones.json').write_text(json.dumps({k:sorted(v) for k,v in sorted(m.items())},indent=2)+'\n')
(root/'NOTICE').write_text('Derived from Google libphonenumber resources/timezones/map_data.txt\nCopyright (C) 2012 The Libphonenumber Authors\nApache License 2.0, see LICENSE-libphonenumber.txt.\nSource: https://raw.githubusercontent.com/google/libphonenumber/master/resources/timezones/map_data.txt\nRetrieved 2026-09-26. Source SHA256: '+hashlib.sha256(raw.encode()).hexdigest()+'\nTransformation: see docs/timezone-data.md for conservative additions; union all US/Canada timezone entries sharing a +1 NPA; omit country-wide and non-geographic fallbacks.\n')
print('Bundled NPAs:',len(m))
