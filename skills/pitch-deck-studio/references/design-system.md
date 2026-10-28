# Design system

Target look: **sleek, minimalist, confident**. The reference set is the SpaceX 2026 roadshow (dark, cinematic, all-caps
light headlines, giant condensed numerals, hairline rules, one photo or one chart per slide), the classic Airbnb deck
(one warm accent, photography, every slide answers one question), and Stripe-style decks (white space, one vivid accent,
product UI, logo walls). What they share is restraint: one idea, one accent and one focal point per slide.

## Principles
1. **One focal point per slide.** It can be a number, a chart, a screenshot, a sentence or a photo. Everything else is quieter.
2. **Type does the heavy lifting.** Large headlines, a strict scale, generous margins (≥ 110 px on a 1920×1080 canvas).
3. **One accent colour**, used for meaning: the highlighted bar, the key number, the "us" dot. Never for decoration.
4. **Hairlines, not boxes.** Separate content with 1-2 px rules and space, not cards, shadows or gradients.
5. **Real imagery, full-bleed or framed.** Photos go edge to edge with a gradient for legibility, and UI goes in a device frame.
6. **Consistency is the brand.** Same header position, same number style and same footer on every slide.
7. **Density follows mode.** Presented decks can be very sparse. Send-ahead decks carry an extra sentence, never a wall of text.

## Presets (`assets/presets.json`)
| Preset | Look | Default for |
|---|---|---|
| `cosmos` | black, light uppercase Barlow, condensed numerals, photo-led | space, defense, deeptech, infrastructure, frontier AI, roadshows |
| `swiss` | white, Inter Tight, single vivid blue accent | B2B SaaS, payments, data, horizontal software |
| `mono` | black on white, huge type, signal-orange accent | AI apps, category creation, bold seed decks |
| `terminal` | near-black, Geist + Geist Mono, green accent | dev tools, open source, AI infra, security |
| `editorial` | warm paper, Instrument Serif, terracotta | D2C/CPG, food, media, creator economy, consumer brands |
| `warm` | white, Plus Jakarta Sans, coral, rounded, photo-led | marketplaces, travel, community, consumer apps |
| `lab` | clinical white, IBM Plex, teal | biotech, medtech, digital health, scientific deeptech |
| `ledger` | off-white, navy ink, money green, Manrope | fintech, insurance, B2B finance, regulated industries |
| `verdant` | sage paper, forest ink, green, Space Grotesk | climate, energy, agtech, sustainability |
| `mission` | dark slate, uppercase Archivo, amber | defense, dual-use, govtech, public safety |
| `noir` | near-black, ivory Fraunces serif, champagne | luxury, premium consumer, fashion, hospitality |

Choose by **audience expectation first, vertical second, founder taste third**. A climate-hardware company pitching
deeptech funds may suit `cosmos` better than `verdant`. Presets are starting points, so override any token in `brand.json`.

## brand.json
Comments below are for explanation only. The real file must be plain JSON.
```jsonc
{
  "name": "Acme",
  "preset": "swiss",
  "logo": "assets/logo.svg",          // optional; used on the title and closing slides
  "logo_small": "assets/mark.svg",    // optional; footer mark (falls back to logo, then the name)
  "mode": "light",                    // light | dark (from preset)
  "colors": {"bg": "#FFFFFF", "fg": "#0E1116", "muted": "#5E6673", "accent": "#2F5BFF",
             "surface": "#F4F5F7", "line": "#E3E5EA", "inv_bg": "#0E1116", "inv_fg": "#FFFFFF"},
  "fonts": {"display": "Inter Tight", "display_weight": 600, "display_case": "none", "display_tracking": "-0.03em",
            "body": "Inter", "numbers": "Inter Tight", "mono": "JetBrains Mono",
            "google_specs": {"Instrument Serif": "ital@0;1"},   // only if a family lacks weights 300-700
            "no_google_fonts": false},
  "on_accent": "#FFFFFF",             // text colour on accent backgrounds
  "h1_size": 84, "radius": 12, "padding": 120,
  "css": "/* optional extra CSS appended last */"
}
```
Only the keys you set override the preset. Fonts load from Google Fonts by default. For brand fonts that are not on Google
Fonts, set `"no_google_fonts": true` and add `@font-face` rules pointing to files in `assets/` via `"css"`.

## Creating a brand from nothing
1. **Name → personality.** Write three adjectives the founder would accept (for example "precise, calm, trustworthy").
2. **Accent colour with a reason.** Avoid the vertical's cliché only when standing out helps; otherwise fit in. Keep
   contrast ≥ 4.5:1 against the background for text uses. One accent, plus optional tints.
3. **Type pair.** A display face with character plus a neutral body face (or one family in two weights). Use Google Fonts so it renders anywhere.
4. **Wordmark.** The name set in the display face, tight tracking, optional single geometric mark (circle, slash,
   square, or the initial built from simple shapes) as SVG in `assets/mark.svg`. No gradients, no mascots, no clip-art.
5. **Write `brand.json`** and run `scripts/brand_sheet.py` so the founder gets a one-page brand sheet (palette, type,
   wordmark, usage). Tell them it is a starting identity, not a trademark-cleared logo.

## Mapping existing brand guidelines
Take hex values for background, text, accent and a muted grey. If the brand has several bright colours, choose **one** as
the deck accent and use the others only in charts. Use the brand fonts if they are web-available, or the closest
Google Font if not (and say so). Use the logo provided. Never redraw a client's logo.

## Layout rules the builder enforces (and you should respect)
- Canvas 1920×1080 (16:9). Content sits inside the padding. The footer (mark, confidentiality, page number) is automatic.
- Headlines ≤ 12 words; body text ≥ 24 px; labels in small caps with tracking; numbers in the numbers font.
- At most 5 bullets, at most ~60 words on a normal slide (the linter warns per layout).
- Charts: no gridlines, no 3D, no legends when direct labels work, and a highlighted point for the takeaway.
- Images: about 1 slide in 3. Use `@side` for half-bleed photos, `@bg` for full-bleed with an automatic legibility gradient (`@dim 0.4-0.97`,
  `@bg-focus`), `gallery` for captioned sets, and `screens` frames (browser + phone) for UI. See the image budget in `show-dont-tell.md`.

## Banned (the "AI slop" list)
Purple-to-blue gradients on everything; glassmorphism cards; emoji as icons; stock photos of handshakes, people pointing
at screens or glowing brains; isometric 3D blobs; rainbow charts; drop shadows on text; centred body paragraphs;
more than two typefaces; underlined headlines; decorative accent bars under every title; "Thank you" as a closing slide.
