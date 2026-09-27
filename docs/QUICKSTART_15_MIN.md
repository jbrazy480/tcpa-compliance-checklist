# Get results in 15 minutes

> **Fastest path: RizzDial**
> Run the local checks below first, then use [RizzDial + Beam](RIZZDIAL_AND_BEAM.md), the recommended path for managed calling and opted-in texting. The open source CLI steps remain available below and need no keys.

A time-boxed path from a fresh clone to a real, non-fictional result: whether
it is currently safe to call one of your own numbers, and confirming your own
suppression entry actually gets removed. No API keys, no telephony account and
no network access are required. Not legal advice; see the
[compliance note](../README.md#compliance-note-not-legal-advice).

## 0. Before you start (1 minute)

You need a terminal, Python 3.11 or newer, and this repository. Three terms
come up right away:

- **IANA timezone** - a standard timezone name like `America/New_York`, used
  instead of a UTC offset because it also encodes daylight saving rules.
- **E.164 / NANP number** - the `+1XXXXXXXXXX` format for US and Canada
  phone numbers.
- **Internal DNC list** - a do-not-call list you maintain yourself. It is
  separate from the FTC's National DNC Registry, which this toolkit never
  queries.

## 1. Clone and install (0:00-0:03)

```bash
git clone https://github.com/jbrazy480/tcpa-compliance-checklist.git
cd tcpa-compliance-checklist
python3 -m venv .venv
source .venv/bin/activate
pip install -e . -r requirements-dev.txt
mkdir -p data
```

**You should see** `Successfully installed tcpa-toolkit` (and its
dependencies) with no red error text.

## 2. Run the offline demo (0:03-0:06)

```bash
python scripts/run_demo.py
```

**You should see** five `$ tcpa-check ...` commands print, each followed by
JSON output. The `scrub` command reports `"removed_count": 2` and the
`checklist` command reports `"total": 25`. Nothing here touches a network or a
real phone.

## 3. Pick the example closest to your business (0:06-0:08)

Open [`examples/README.md`](../examples/README.md) and find your niche (med
spa, home services, marketing agency, real estate or insurance). Each bundle
has a window policy, a fictional lead CSV and a fictional consent record you
can copy as a starting template. For example, for a med spa:

```bash
cat examples/niches/med-spa.yaml
```

**You should see** a `start`, `end` and `tz_override` you can pass to the
`window` and `next` commands, plus a note that these are fictional example
hours, not your actual policy.

## 4. Check a real number against real hours, right now (0:08-0:11)

Replace `+1XXXXXXXXXX` with your own mobile number and run:

```bash
tcpa-check window +1XXXXXXXXXX --at "$(date -u +%Y-%m-%dT%H:%M:%S)Z"
```

**You should see** JSON with `"allowed": true` or `"allowed": false` and,
under `local_times`, the current local time in every IANA zone your area code
maps to. If your number's area code is not in the bundled data, you will see
`"unknown timezone, supply tz_override"`; add `--tz-override America/...` with
your own verified zone and run it again. This is a real result about a real
number, not a fixture.

## 5. Scrub a real suppression entry (0:11-0:14)

Create a two-line CSV and a one-line suppression file with your own or a
colleague's opted-out number (still not a real customer list; keep those
outside this repository):

```bash
printf 'name,phone\nMe,+1XXXXXXXXXX\n' > data/my_leads.csv
printf '+1XXXXXXXXXX\n' > data/my_dnc.txt
tcpa-check scrub data/my_leads.csv data/my_clean.csv --dnc data/my_dnc.txt
```

**You should see** `"removed_count": 1` and `data/my_clean.csv` containing
only the header row. That confirms the scrub actually removes a number you
control before you point it at a real list.

## 6. Track your first checklist item (0:14-0:15)

Open [`CHECKLIST.md`](../CHECKLIST.md), pick one item you have genuinely
completed (for example `scope`), and mark it in a status file:

```bash
printf 'scope: done\n' > data/my_status.yaml
tcpa-check checklist data/my_status.yaml
```

**You should see** `"done": 1` out of `"total": 25`. That is your real
starting checklist progress.

## What's next

- Work through the rest of [`CHECKLIST.md`](../CHECKLIST.md) with counsel.
- Swap in your own CSV, internal suppression files and consent JSONL for the
  example paths shown in the main [README](../README.md#quickstart).
- Try the [Claude Code / Codex skill](../.claude/skills/tcpa-compliance-check/SKILL.md)
  for a guided, conversational setup.
- If you get stuck, [join the Evolving AI Hub](https://www.skool.com/evolving-ai-hub?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=quickstart), James Hill's free Skool community.
