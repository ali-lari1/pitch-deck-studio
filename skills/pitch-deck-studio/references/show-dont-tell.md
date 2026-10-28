# Show, don't tell

Investors discount adjectives to zero. They believe artifacts. For every claim in the outline, ask what a person could
*see* that would make the claim unnecessary to state, then use that.

| Claim you want to make | Show this instead | Layout |
|---|---|---|
| "Customers love it" | named quote with role and context, or a retention curve | `quote`, `chart type=line` |
| "Fast-growing" | one bar chart, latest bar highlighted, headline states the rate | `chart` |
| "Easy to use" | the real UI in a browser or phone frame, 3 steps with time per step | `screens`, `steps` |
| "Big market" | bottom-up arithmetic visible on the slide | `market` |
| "Strong team" | faces + the one credential each + logos of prior companies | `team` |
| "Better than competitors" | 2×2 matrix on buyer-relevant axes, or a table with honest partial marks | `matrix`, `table` |
| "Proven technology" | benchmark chart vs the state of the art, prototype photo, lab data with n | `chart type=hbar`, `image` |
| "Trusted by enterprises" | logo wall (permission!), segmented by tier | `logos` |
| "Massive scale" | a grid of 4-12 hard numbers ("N of 1" slide) | `stats` (`@class rows` for dense) |
| "Capital efficient" | revenue vs cumulative raised, burn multiple trend | `chart`, `stats` |
| "Huge vision" | a timeline: delivered milestones (filled dots) → next milestones (hollow) | `timeline` |
| "Developers adopt it" | a 6-line code sample + GitHub stars or weekly downloads chart | `default` with code block, `chart` |
| "Hardware works" | photo of the physical product in use, full-bleed | `image` |
| "Clinical value" | primary endpoint chart with n, p-value or CI, comparator | `chart`, `table` |
| "Network effects" | the loop drawn as 3-4 steps or a cohort chart showing improvement with scale | `steps`, `chart` |

## How many images: the right amount
About **one slide in three** should carry a real image (photo or product screenshot). The rest are type, numbers and charts.
The linter warns when the main deck has none, when fewer than 1 in 5 slides have one, and when more than 60% do.
A typical 12-15 slide deck uses 4-5:

| Slot | Image | How |
|---|---|---|
| Title | the customer, the product or the place, half-bleed | `@side assets/x.jpg` (or `@bg` for a dark cinematic cover) |
| Problem | the pain made visible (paper stacks, a broken process, the place it happens) | `@side` next to a `statement` |
| Who we serve / the world | one full-bleed photo with a short headline | `@layout image` + `@bg`, `@invert` on light decks |
| Product | real screenshots: browser + phone together | `@layout screens` with `![](web.png)` and `![](app.png "phone")` |
| Customers / proof | a customer photo next to a quote, or a captioned gallery | `@side` on `quote`; `@layout gallery` |
| Section dividers / close | atmosphere for long or roadshow decks | `@layout section` + `@bg` |

Rules: never two full-bleed photos in a row; keep charts, stats, market, competition and ask slides image-free; one photo per slide
(galleries excepted); faces look into the slide, not off it (`@side-pos left|right`, `@side-focus 30% center`).

## Visual sources (in order of preference)
1. The founder's real product screenshots, photos, data and logos (ask for them; they beat anything you make).
2. Screenshots of the live website or app. If a headless browser is available, the agent can capture them, or the founder sends them.
3. Charts generated from `facts.md` data with the built-in `chart` blocks.
4. Clean UI or diagram mockups you draw as SVG. Label them "illustrative" if they are not the shipping product.
5. Openly licensed photos for context and atmosphere (the customer type, the place, the problem): run
   `python3 scripts/find_images.py "<query>" --preview-dir <project>/research/img` to see candidates, then
   `--download <project>/assets --pick N --name <slot>`. Sources: Openverse (CC, no key), NASA (public domain; space, earth,
   science), Unsplash or Pexels (with `UNSPLASH_ACCESS_KEY` / `PEXELS_API_KEY`). Credits are appended to `assets/CREDITS.md`.
   An image-generation tool, if installed, also works for atmosphere. Never present stock or generated people as the
   company's team, customers or product.

## Never
- Fake logos, invented testimonials, made-up customer names or invented data on charts.
- Clip-art icons that duplicate the text next to them.
- Screenshots too small to read. If it can't be read at 50% zoom, crop to the part that matters.
- A chart without a source line and a takeaway headline.
