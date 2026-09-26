# Timezone snapshot maintenance

The package ships static data and never downloads it during a check. Rebuild
from a local copy of the upstream file:

```bash
python scripts/build_timezone_data.py /path/to/map_data.txt
```

Preserve the Apache license and notice. Review changes manually, update the
retrieval date, and rerun all tests. The notice includes the source file hash.

The transformation unions every specific prefix sharing an NPA. It excludes
country-wide fallbacks and zones outside the US/Canada selection. Conservative
additions address incomplete upstream overlay and regional coverage:

- 208/986, 812/930 and 850/448 use unioned zones. See the
  [NANPA 2015 annual report](https://www.nationalnanpa.com/reports/2015_NANPA_Annual_Report.pdf)
  and [NANPA planning letters, PL-551](https://www.nanpa.com/npa-relief/planning-letters).
- British Columbia province-wide overlays 236/257/672/778 use the union of
  250 and 604, including Dawson Creek, Fort Nelson and Creston fixed-offset
  regions. The 250 hint is also conservatively expanded. See
  [CRTC 2023-135](https://crtc.gc.ca/eng/archive/2023/2023-135.pdf),
  [Canadian area-code maps](https://www.cnac.ca/area_code_maps/canadian_area_codes.htm)
  and [IANA timezone data](https://www.iana.org/time-zones).
- 867 includes additional territorial representative zones, including Yukon
  and fixed central-time possibilities. This intentionally errs toward fewer
  allowed times. See the Canadian maps and IANA sources above.

This is not a geolocation database. Included extra zones can reject a time that
would be acceptable at the actual location. Omitted new NPAs fail closed.
Use current system tzdata, and use a verified override for precise scheduling.
