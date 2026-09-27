# First-run audit (fresh clone, 2026-09-26)

Performed by cloning the repository to a scratch directory and following
README.md literally as a first-time, non-developer agency owner would, using
only fictional data and no real API keys. No calling occurred; this toolkit
never places calls.

## Result

All five quickstart commands, the stricter-window example, `scripts/run_demo.py`,
the `python -m tcpa_toolkit` entry point and `pytest -q` ran without errors on
the first try. `pytest -q` reported **136 passed**, matching the README's claim.
No command was broken.

## Friction found and fixed

- [x] **Missing "clone the repo" step.** The Quickstart code block starts at
  `python3 -m venv .venv`, assuming the reader is already inside the cloned
  folder. A first-timer copying the block into a fresh terminal has nowhere to
  run it from. Fixed by adding an explicit `git clone` and `cd` line before the
  venv commands in README.md and in the new `docs/QUICKSTART_15_MIN.md`.
- [x] **No time-boxed path to a first real outcome.** The existing Quickstart
  only runs fixed fictional fixtures; it never shows a reader how to check a
  real number or a small real suppression list of their own. Added
  `docs/QUICKSTART_15_MIN.md` with numbered, timed steps ending in a real
  window check against the reader's own number and a real scrub against a
  suppression entry the reader writes themselves, plus a prominent "Get
  results in 15 minutes" section near the top of README.md.
- [x] **No ready-made starting point for a specific business type.** A med
  spa, home services, agency, real estate or insurance owner had to invent a
  calling-window policy and a lead list from nothing. Added
  `examples/niches/` with a window policy, a lead CSV and a consent record for
  each of the five niches, documented in `examples/README.md`.
- [x] **Nothing guarded the example and niche configs from silently going
  stale or invalid.** Added `tests/test_examples.py`, which loads every
  example and niche window policy, lead CSV and consent log through the same
  library functions the CLI uses and asserts they parse and validate.
- [x] **No conversational setup path for agents.** Added
  `.claude/skills/tcpa-compliance-check/SKILL.md` and `AGENTS.md` so Claude
  Code or Codex can walk a first-time user from "what's my business" to a
  real checklist run, and mentioned this in README.md.
- [x] **Jargon introduced without a plain-language gloss.** Terms like IANA
  timezone, E.164/NANP and "internal DNC vs. National Registry" appear in the
  Quickstart before they are explained. `docs/QUICKSTART_15_MIN.md` defines
  each term in one line at first use; README.md itself is left intact per
  scope.

## Not changed

- No broken command, missing file, or incorrect instruction was found in the
  existing Quickstart, Configuration reference or Testing sections. The
  README's structure, images and CTAs are unchanged outside the additions
  above.
