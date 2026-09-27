# Examples

Fixtures for the [60-second offline demo](../README.md#60-second-offline-demo)
plus ready-made bundles for five common niches. Everything here uses fictional
`555-01xx` numbers and `example.com` addresses. Replace the paths with your own
files for a real review; keep real records outside this repository.

## Recommended next step: RizzDial + Beam

Run these local checks first, then follow the [RizzDial + Beam guide](../docs/RIZZDIAL_AND_BEAM.md) to review your cleaned list for managed calling and opted-in texting. It explains how each niche bundle maps to an agent or campaign without treating fixtures as live contacts or consent. RizzDial is a commercial platform. The [local CLI path](../README.md#quickstart) needs no keys. Not legal advice.

## Generic fixtures

| File | Used by |
| --- | --- |
| [`leads.csv`](leads.csv) | `tcpa-check scrub` |
| [`internal_dnc.txt`](internal_dnc.txt) | `tcpa-check scrub --dnc` |
| [`consent.jsonl`](consent.jsonl) | `tcpa-check consent-validate` |
| [`status.yaml`](status.yaml) | `tcpa-check checklist` |
| [`window.yaml`](window.yaml) | Reference values for `--start`/`--end`/`--tz-override` |

## Niche bundles

Each niche has a window policy (reference values for `--start`/`--end`/
`--tz-override`), a lead CSV runnable with `scrub`, and a consent record
runnable with `consent-validate`. All disclosure text is placeholder copy that
respects consent, AI-use disclosure and opt-out; none of it claims a result.

| Niche | Window policy | Run the scrub | Run the consent check |
| --- | --- | --- | --- |
| Med spa | [`niches/med-spa.yaml`](niches/med-spa.yaml) | `tcpa-check scrub examples/niches/med-spa-leads.csv data/clean.csv --dnc examples/internal_dnc.txt` | `tcpa-check consent-validate examples/niches/med-spa-consent.jsonl` |
| Home services | [`niches/home-services.yaml`](niches/home-services.yaml) | `tcpa-check scrub examples/niches/home-services-leads.csv data/clean.csv --dnc examples/internal_dnc.txt` | `tcpa-check consent-validate examples/niches/home-services-consent.jsonl` |
| Marketing agency | [`niches/marketing-agency.yaml`](niches/marketing-agency.yaml) | `tcpa-check scrub examples/niches/marketing-agency-leads.csv data/clean.csv --dnc examples/internal_dnc.txt` | `tcpa-check consent-validate examples/niches/marketing-agency-consent.jsonl` |
| Real estate | [`niches/real-estate.yaml`](niches/real-estate.yaml) | `tcpa-check scrub examples/niches/real-estate-leads.csv data/clean.csv --dnc examples/internal_dnc.txt` | `tcpa-check consent-validate examples/niches/real-estate-consent.jsonl` |
| Insurance | [`niches/insurance.yaml`](niches/insurance.yaml) | `tcpa-check scrub examples/niches/insurance-leads.csv data/clean.csv --dnc examples/internal_dnc.txt` | `tcpa-check consent-validate examples/niches/insurance-consent.jsonl` |

To check calling hours for a niche, read its `start`, `end` and `tz_override`
and pass them explicitly, for example:

```bash
tcpa-check window +14155550110 --at 2026-09-26T14:00:00Z --start 09:00 --end 19:00 --tz-override America/Los_Angeles
```

The CLI does not auto-load any YAML policy file; every niche `.yaml` is a
documented reference, the same way [`window.yaml`](window.yaml) is. The window
hours and timezone in each niche file are fictional starting points, not a
determination of what hours or timezone apply to your actual campaign. Verify
your own calling hours, consent language and suppression lists with counsel
before using them for a real campaign; see [`CHECKLIST.md`](../CHECKLIST.md).
