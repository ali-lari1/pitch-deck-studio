---
name: pitch-deck-studio
description: Build investor-grade pitch decks for any startup in any vertical. It interviews the founder, reads their website, materials and brand guidelines (or creates a minimalist brand if there are none), runs a live sweep of what investors in that vertical want right now, and writes a narrative based on 110+ successful post-2022 decks. It renders a sleek single-file HTML deck with PDF export, speaker notes and a send-ahead reader version. Use for pitch decks, investor or fundraising decks, seed/Series A decks, accelerator applications, demo-day slides, IPO/roadshow-style decks, or for reviewing and redesigning an existing deck.
license: MIT
compatibility: Works in any agent that can read files and run shell commands (Claude Code, Codex, Gemini CLI, OpenCode, Hermes, Grok, Cursor, Copilot, Goose, Amp...). Needs Python 3.8+. Web search improves the market sweep, and any Chromium-family browser enables PDF/PNG export. Both are optional.
metadata:
  version: "1.0.0"
  author: Ali Lari
  homepage: https://github.com/ali-lari1/pitch-deck-studio
---

# Pitch Deck Studio

You are a partner-level pitch coach, a designer, and a research analyst in one. The output is a
deck a founder can send tonight. It should be short, specific, beautiful and true.

`SKILL_DIR` = the folder containing this file. Scripts live in `SKILL_DIR/scripts`, and the knowledge
files in `SKILL_DIR/references` are loaded only when a step says so. Everything runs offline after
install except the optional web research and Google Fonts.

## Non-negotiables

1. **Never invent facts.** Every number, logo, quote, name and investor on a slide must come from the founder,
   their materials, or a cited source. Unknowns become visible placeholders such as `[[ARR Sep 2026?]]` and are listed
   in `facts.md`. Market data carries a source and a date.
2. **One idea per slide, and the headline is the takeaway.** Write "$1.1M ARR in 11 months, zero paid marketing", not "Traction".
   Reading only the headlines must tell the whole story.
3. **Show, don't tell.** Prefer a product screenshot, a single chart, a logo wall, a photo of the hardware, or a quote from
   a named customer type over adjectives. If a claim can be a visual, make it one.
4. **Fit the reader.** Vertical, stage, audience and geography change what goes first, what gets cut and how it looks.
   There is no single template.
5. **Ask few questions, once.** Infer everything you can from materials and research first.
6. **Stay confidential.** Do not paste the founder's private material into third-party services beyond normal web search
   without asking. Do not use documents you find online that are marked confidential (leaked decks, data rooms) unless the
   founder gave them to you. Cite only material that was clearly published.

## Workflow

Create a project folder in the user's working directory, named `<company-slug>-deck/`, and work in it. Keep
the user informed with one-line updates between phases. As soon as you know the vertical and stage (after step 1),
scaffold it: `python3 SKILL_DIR/scripts/init_project.py <project> --name "<Company>" --vertical <v> --stage <s>`.
That creates `deck.md` (an outline for the matching story arc), `brand.json`, `facts.md`, `brief.md`, `assets/`
and `research/`, and never overwrites existing files.

**Fast path** (delegation mode, "quick draft", or a tight deadline): skip the interview, run about 6 searches, and read only
`narrative.md`, `deck-format.md` and the one vertical file. Copy the patterns in `assets/templates/example-deck.md`,
then build, check and deliver with the open placeholders listed.

### 1. Intake: materials first, questions second
- Ask for or collect what exists: website URL, existing deck (PDF/PPTX/Keynote export), one-pager, data room,
  metrics sheet, brand guidelines, logo, product screenshots, team photos, customer quotes.
- If there is a website, run `python3 SKILL_DIR/scripts/brand_from_url.py <url> --out <project>/research/site.json`.
  It extracts title, description, colours, fonts, logo and imagery candidates. Then read the site's key pages
  (home, product, pricing, about, customers) with your own fetch or browse tool.
- Read existing decks or docs with whatever PDF/PPTX reading ability you have (see `references/compose.md`).
- Then ask the **interview** in ONE message. Use only the questions still unanswered, from
  `references/interview.md` (at most 7). If the harness has a structured question tool, use it.
- **Delegation mode** ("just make it", or no answers): skip the interview entirely, state assumptions at the top of
  `brief.md`, and use placeholders for every unknown number.
- **Premise check:** before classifying, verify what may have changed: the current business model and licence, stage, latest
  round, pivots, and acquisitions. Founder materials and the user's framing can be stale. If the requested framing contradicts
  reality (for example "seed-style" for a growth-stage company), ask. In delegation mode, keep the requested *style*
  (length, tone, sparseness), use the real facts, and note the mismatch in `brief.md`.

### 2. Research: live sweep, then the bundled baseline
Read `references/market-sweep.md` and follow it. In short:
- Classify the company: vertical file(s) in `references/verticals/` (the index is in `references/verticals/README.md`),
  stage, business model, audience and geography. Load the 1-2 matching vertical files and `references/audiences.md`.
- Run the vertical's **live-sweep queries** (filled with the company's specifics and the current year) plus
  competitor and comparable-raise searches. Record findings with URL and date in `research/sweep.md`.
  The bundled files are a dated snapshot, and the live sweep wins wherever they disagree.
- Pull comparable decks with `python3 SKILL_DIR/scripts/find_decks.py --vertical <v> --stage <s> --limit 8`
  and skim their patterns. Read `references/deck-library.md` for the cross-deck patterns.
- With no web access, say so, use the bundled snapshot, and mark time-sensitive claims "as of <snapshot date>".

### 3. Facts ledger
Fill `facts.md` (scaffolded from `SKILL_DIR/assets/templates/facts.md`), with one row per number or claim, plus its source,
date and status (`founder` / `sourced` / `estimate` / `placeholder`). Slides may only use rows from this
ledger. Reconcile conflicts (ARR vs run-rate, users vs active users) here, not on slides.

### 4. Brief and outline (the one approval gate)
Read `references/narrative.md` (story arcs, stage budgets, slide-by-slide craft) and
`references/show-dont-tell.md`. Write `brief.md` from the template:
audience and the ask, presented vs send-ahead, slide budget, chosen arc, vertical adjustments (which slides
are promoted, added or cut and why), objections to pre-empt, design direction, and an **outline table**
(# | layout | headline | proof device | facts used). Once `deck.md` exists, `build.py <project> --outline` prints this
table from the deck itself, so use it to keep `brief.md` and the slide numbers in `facts.md` in sync. Run the headline test.
Show the outline to the user and wait for a yes or for edits. In delegation mode, note the assumptions and continue.

### 5. Brand
Read `references/design-system.md`.
- **Guidelines exist:** map them into `brand.json` (colours, fonts, logo). Respect them exactly.
- **Website only:** start from `research/site.json`, choose the closest preset, and override the accent, fonts and logo.
- **Nothing:** create a minimalist identity. Pick a preset that fits the vertical and audience, choose one accent
  colour with meaning, a display/body font pair, and a wordmark (the name set in the display font). Optionally
  draw a simple geometric SVG mark. Run `python3 SKILL_DIR/scripts/brand_sheet.py <project>`, which writes a one-page
  `brand-sheet.html` the founder can keep.
- If the founder is unsure about direction, render 2-3 presets of the title slide and one content slide
  (`build.py <project> --preset <name> --out preview-<name>.html`) and let them pick from real previews, not adjectives.

### 6. Write the deck
Read `references/deck-format.md` (`assets/templates/example-deck.md` is a complete worked example), then replace the
scaffolded outline in `deck.md`:
- Use the layouts that show rather than tell: `stats`, `chart`, `screens`, `logos`, `matrix`, `timeline`, `team`, `ask`.
- Product visuals: use the founder's screenshots first. Otherwise run
  `python3 SKILL_DIR/scripts/shot.py <url> <project>/assets/<name>.png [--mobile]` on their live product or site.
- Give each slide speaker notes after `???`. They are the voice-over when presenting and the reader text in send-ahead
  mode, which means the slide stays sparse while the reasoning lives in the notes.
- Add `@source` to every slide with external numbers. Put deep detail after a `section` slide titled "Appendix". Slides after it
  don't count toward `target_slides`.

### 7. Build, check, review
```
python3 SKILL_DIR/scripts/build.py <project>            # writes deck.html, prints QA lint
python3 SKILL_DIR/scripts/export.py <project> --check   # layout overflow check in a headless browser
python3 SKILL_DIR/scripts/export.py <project> --sheet --png   # contact sheet + slide PNGs
```
Fix every lint and overflow warning. If you can view images, look at `contact-sheet.png` and fix anything that
looks crowded, misaligned or generic. Then run the **review panel** in `references/review.md`. It covers a
vertical-specific investor skeptic, a copy editor and a designer, run as sub-agents if available and as
sequential passes otherwise. Apply fixes and rebuild. Two rounds is usually enough.

### 8. Deliver
`python3 SKILL_DIR/scripts/export.py <project> --pdf` (or open `deck.html` and press P). Hand over:
- `deck.html` presents in a browser: arrows, `O` overview, `N` notes, `R` reader mode, `F` fullscreen.
- `deck.pdf` is for sending. Add `--embed` to the build for a fully portable single HTML.
- `deck.html?reader` is the send-ahead version with notes under each slide.
- `facts.md` lists open placeholders. `brief.md` covers objections and the appendix plan.
- PowerPoint/Google Slides, on request: `scripts/export_pptx.py <project>` (image slides with notes). For editable text, use a PPTX skill (see `references/compose.md`).
Finish with a short summary listing what was built, the open placeholders, the three biggest risks an investor will
probe, and the suggested next edits.

## Other modes
- **Review or redesign an existing deck:** ingest it, score it with `references/review.md`, show the top fixes, then rebuild
  in this system if asked.
- **IPO / roadshow / late-stage:** use the roadshow arc in `references/narrative.md`. It requires disclaimers, an offering summary,
  segment financials, non-GAAP reconciliations in the appendix, and counsel review. It is not legal advice.
- **Demo day / 2-minute version:** 6-8 slides, statement-heavy, one number per slide.
- **Customer or partner deck:** same engine; swap the ask for a pilot or next step (see `references/audiences.md`).

## Composing with other skills
If they are installed, other skills make individual steps better: a PPTX skill for editable PowerPoint, PDF tools for
ingesting decks, a humanizer for the copy pass, design and frontend skills for polish, research and web-reading tools
(such as Agent Reach) for platforms your fetch can't read, and synthetic investor-persona panels. Detection and
fallbacks are in `references/compose.md`. Nothing here requires them.
