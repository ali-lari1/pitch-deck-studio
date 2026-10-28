# Review panel

Run this after the first full build, and again after fixes. If your agent can start sub-agents, run the three reviewers
in parallel with fresh context. Give them only `deck.md`, `facts.md`, `brief.md`, the relevant vertical file and
`contact-sheet.png` if available. Otherwise do three separate passes yourself, one hat at a time. Each reviewer returns at most 8
findings, ranked, each with the slide number and a concrete fix. Apply the fixes, rebuild, and stop after the second round
unless something critical is left.

## 1. The investor skeptic (vertical-specific)
Persona: a partner at a fund that invests in this vertical and stage (use names and theses from `research/sweep.md` if
available). They have read 30 decks this week.
- Within the first three slides, can I say what it is, for whom, and why it's interesting? If not, which slide fails?
- Which claim would I not believe? Which number lacks a definition, a date or a source?
- What would I ask in the first five minutes? Is it answered in the deck or the appendix? (Use the vertical file's
  "what they scrutinize first" and "red flags" lists.)
- Is the ask coherent? Does the money reach a milestone that makes the next round easy?
- Score 1-5: clarity, credibility, team-market fit, size of outcome, urgency to take the meeting.

## 2. The copy editor
- Headline test: list the headlines in order. Do they tell the story alone? Rewrite any label-headline.
- Cut every adjective a number could replace. Remove the banned words (see `narrative.md`).
- Check consistency of metric names, units, dates and the company name.
- Notes: does each slide have 2-5 sentences that a cold reader understands?
- Fewer words: find the three wordiest slides and halve them.
- If a humanizer or writing-style skill is installed, run it on headlines and notes (see `compose.md`).

## 3. The designer
Look at `contact-sheet.png` or the slide PNGs (or read `deck.md` if you can't view images).
- One focal point per slide? Is anything competing with the headline?
- Consistent rhythm: alternating dense and sparse slides, a section divider before the appendix, and at most 3 consecutive text-only slides.
- Show-don't-tell: which text slide should become a chart, screenshot, matrix or stats grid?
- Legibility: nothing under 20 px at 1920 width, contrast on image backgrounds, screenshots readable.
- Overflow or awkward wraps: run `export.py <project> --check` and fix every reported slide.
- Brand fidelity: are the client's colours, logo and fonts used correctly, with the accent used only for meaning?

## Scorecard (put it at the end of `brief.md`)
| Dimension | Score 1-5 | Note |
|---|---|---|
| Story clarity (headline test) | | |
| Evidence & honesty (facts ledger complete) | | |
| Fit to vertical & audience | | |
| Show-don't-tell | | |
| Visual quality & consistency | | |
| Ask & milestones | | |

Do not deliver below 4 on evidence & honesty. Open placeholders are fine if they are listed for the founder, but a guess
must never appear as fact.
