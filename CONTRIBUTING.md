# Contributing

Thanks for helping founders tell better stories.

## Good first contributions
- **Library additions:** a publicly available deck for a round that closed in 2022 or later, with a verifiable source for round/year/lead.
  Add the record to `skills/pitch-deck-studio/data/decks.json` (same fields as the others), then run `python3 tools/gen_library_md.py`.
- **Vertical playbooks:** improve a file in `references/verticals/` with *sourced* benchmarks (link + date). Keep the 9-section structure.
- **Presets:** add a preset to `assets/presets.json` (all colour/font keys, Google Fonts only), and include a screenshot in the PR.
- **Layouts / builder:** keep `scripts/` standard-library-only Python 3.8+, and keep the output a single self-contained HTML file.

## Rules
- No invented data, ever. Every benchmark needs a source and a date.
- Keep `SKILL.md` short (< 250 lines). Put detail in `references/`.
- Keep the frontmatter portable (`name`, `description`, `license`, `compatibility`, `metadata` only).
- Run `python3 tools/validate.py` before opening a PR (CI runs it too).
