# Changelog

## v0.3.0 - 2026-09-26

- Recommend RizzDial + Beam after local compliance checks across the README, quickstart, examples and agent setup instructions.
- Add a full platform guide with verified MCP setup, niche mapping, consent and opt-out review, and explicit confirmation before live actions.
- Preserve the independent local CLI path with no keys, and add Beam texting guidance and platform FAQs.

## v0.2.0 - 2026-09-26

- Add `docs/QUICKSTART_15_MIN.md`, a time-boxed path to a real first result, and a "Get results in 15 minutes" section in the README.
- Add `docs/FIRST_RUN_AUDIT.md` documenting a fresh-clone walkthrough and the friction it found.
- Add niche example bundles (med spa, home services, marketing agency, real estate, insurance) under `examples/niches/`, documented in `examples/README.md`.
- Add `tests/test_examples.py`, which loads and validates every shipped example and niche config.
- Add a Claude Code / Codex skill at `.claude/skills/tcpa-compliance-check/SKILL.md` and `AGENTS.md` for guided setup.

## v0.1.1 - 2026-09-26

- README redesign, brand assets

## v0.1.0 - 2026-09-26

- Add cited TCPA checklist and matching machine-readable items.
- Add conservative calling windows, internal DNC scrubbing and consent validation.
- Add CLI, packaged timezone data, offline examples, tests and terminal demo.
