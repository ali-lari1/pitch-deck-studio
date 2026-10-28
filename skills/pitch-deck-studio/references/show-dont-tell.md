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

## Visual sources (in order of preference)
1. The founder's real product screenshots, photos, data and logos (ask for them; they beat anything you make).
2. Screenshots of the live website or app. If a headless browser is available, the agent can capture them, or the founder sends them.
3. Charts generated from `facts.md` data with the built-in `chart` blocks.
4. Clean UI or diagram mockups you draw as SVG. Label them "illustrative" if they are not the shipping product.
5. Stock or AI-generated imagery only for atmosphere (section dividers, title backgrounds), never as evidence. Use only
   images that are licensed for this use, and record the source in `assets/CREDITS.md`.

## Never
- Fake logos, invented testimonials, made-up customer names or invented data on charts.
- Clip-art icons that duplicate the text next to them.
- Screenshots too small to read. If it can't be read at 50% zoom, crop to the part that matters.
- A chart without a source line and a takeaway headline.
