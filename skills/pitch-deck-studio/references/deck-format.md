# deck.md format

One plain-text file produces the whole deck. `python3 scripts/build.py <project>` turns `deck.md` + `brand.json` into
`deck.html` and prints a QA report. A complete worked example is `assets/templates/example-deck.md` (in this skill folder).

## File structure
```markdown
---
title: Acme — Seed 2026          # browser tab title
company: Acme
brand: brand.json                # default
preset: swiss                    # optional; overrides brand.json's preset
confidential: Confidential       # optional footer text
target_slides: 10-13             # optional; linter warns outside the range
purpose: fundraise               # fundraise (requires an ask slide) | customer | other
chrome: on                       # off hides footer mark and page numbers
lang: en
---

@layout title
# Acme
## The one-line value proposition.

---

@layout statement
# The next slide...

???
Speaker notes / reader text for this slide.
```
- Slides are separated by a line containing only `---`.
- **Directives** (`@key value`) go at the very top of a slide.
- **Notes** go after a line containing only `???`. Every slide should have them.

## Directives
| Directive | Effect |
|---|---|
| `@layout <name>` | see the layouts table; defaults to a guess from the content |
| `@kicker <text>` | small label above the headline (for example "Traction") |
| `@source <text>` | source footnote at the bottom (required when external numbers appear) |
| `@note <text>` | footnote without the "Source:" prefix |
| `@bg <image or color or accent>` | full-bleed background image (gradient added for legibility), a CSS colour, or `accent` |
| `@dim 0.4-1` | strength of the legibility gradient on background images |
| `@invert` | swap to the inverse palette for this slide (a dark slide in a light deck, and vice versa) |
| `@align center\|bottom` | alignment for statement, section and image slides |
| `@class <names>` | layout variants (see below) |
| `@cols <n>` | force the number of grid columns for stats, team, logos and steps |
| `@frame browser\|phone\|none` | device frame for `screens` |
| `@flip` | put the visual on the left in `split` / `screens` |
| `@x Low\|High`, `@y Low\|High`, `@us Name` | axis labels and the highlighted company for `matrix` |
| `@logo off` | hide the logo on a title slide |

## Content syntax
| Write | Renders |
|---|---|
| `# Headline` | slide headline (the takeaway) |
| `## Subhead` | muted sub-headline |
| `### Label` | small-caps label with a rule (column headers) |
| paragraph text | body text; `**bold**`, `*italic*`, `` `code` ``, `==accent==`, `[link](url)`, ` // ` = line break |
| `- item` / `1. item` | bullets / numbered list (max 5) |
| `value :: label :: note` | an **item**: a stat, team member, step, milestone, logo, use-of-funds row. Meaning depends on the layout |
| `![alt](assets/x.png)` | image; an image line directly above an item attaches to it (team photo, logo) |
| `> quote` then `> — Name, role` | pull quote with attribution |
| `\|\|\|` on its own line | column break |
| a pipe table | styled table; `✓` `✗` `~` render as ● ○ ◐; wrap the first cell in `==...==` to highlight your row |
| fenced `chart` block | SVG chart (see below) |
| fenced `html` block | raw HTML, an escape hatch for anything bespoke |

## Layouts
| Layout | Use for | Content |
|---|---|---|
| `title` | cover | `# Name`, `## one-liner`, paragraphs become the meta line (round · date) |
| `statement` | problem punchline, mission, insight | `# big sentence`, optional paragraph |
| `section` | dividers ("Our AI business", "Appendix") | `# title`, optional `@bg` photo |
| `image` | full-bleed photo with headline overlay | `![](photo.jpg)` or `@bg`, `# headline`, short paragraph |
| `default` | headline + text/bullets/code | anything |
| `split` | text left, image or chart right | text blocks + one image or chart |
| `screens` | product UI in a browser/phone frame | text + 1-2 screenshots; `@frame phone` for mobile |
| `stats` | key numbers grid; `@class rows` for the dense roadshow style; `@class plain` = no accent on the first number | items `value :: label :: note` |
| `chart` | one big chart | fenced chart block |
| `columns` | 2-4 parallel ideas | `\|\|\|` separated, `### Label` per column |
| `steps` | how it works, the loop | items `Title :: description` (auto-numbered) |
| `timeline` | milestones, roadmap; `@class past` fills all dots | items `date :: title :: description` |
| `team` | founders; `@class round` for round photos | `![Name](assets/x.jpg)` above `Name :: Role :: credential`; without a photo, an initials avatar is drawn |
| `logos` | customers, investors, press; `@class mono` single-colour logos | logo images (`![Ramp](assets/ramp.svg)`, best), or names as a bullet list (`- Ramp`) or items (`Ramp ::`) |
| `table` | comparisons, use of funds detail, financials | pipe table |
| `matrix` | competitive 2×2 | items `Name :: x(0-1) :: y(0-1)` + `@x`, `@y`, `@us` |
| `market` | bottom-up sizing | 3 items `value :: label` (outer → inner) + paragraphs with the math |
| `quote` | testimonials | quotes, `\|\|\|` between several |
| `ask` | the raise | first paragraph = amount (`$4M`); items `45% :: Use :: what it buys`; other blocks (a milestones list) go right |
| `closing` | last slide | `# Name`, `## mission line`, contact lines |
| `html` | anything else | fenced html block |

## Charts
````markdown
```chart type=bar prefix=$ suffix=M highlight=last caption="Revenue, $M" source="Company data"
2023: 4.4
2024: 11.2
2025: 20.7
```
````
- `type`: `bar` | `hbar` | `line` | `area` | `donut` | `stack`. For stacked, write `2025: 3, 5, 2` and add `series="A|B|C"`.
- `highlight`: `last` (default) | `all` | `none` | a label (`2025`) or several (`2024|2025`).
- `prefix`, `suffix` (or `unit`), `decimals`, `labels=off`, `labels=ends` (line), `pct=on` (donut shows %), `center="$4M"` (donut).
- Data lines are `label: value`. Numbers may contain `$ , % K M`; the first number is used.

## QA output
`build.py` prints the slide count, words per slide, the layout per slide and warnings: too many words, headline too long
or missing, more than 5 bullets, numbers without `@source`, placeholders left in (`lorem`, `TBD`, `TODO`, `XX`),
main-slide count (before the Appendix divider) outside `target_slides`, long headlines in half-width columns, missing ask slide,
and missing images. `build.py --outline` prints a slide table (layout, headline, source, placeholder count) for `brief.md`. `export.py --check` reports elements that
overflow their slide in a real browser. Fix all of them before delivering.
