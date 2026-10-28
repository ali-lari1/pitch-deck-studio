# Live market sweep

The bundled vertical files are a **snapshot (October 2026)**. Investor expectations, benchmarks and the funding climate shift
every quarter, so each run refreshes them for this company. Default budget: 6-12 searches and 5-10 page reads (about 6 on the
fast path, or whatever the user allows). Stop when new searches stop changing the story.

## 0. Premise check (first two searches)
`{company} {year}` and `{company} funding OR acquired OR pivot OR license`. Confirm the current business model, licence (open source
or not), stage, latest round, headcount and any acquisition or pivot. If reality contradicts the materials or the user's framing,
follow the premise-check rule in SKILL.md before going further.

## 1. Classify
- **Vertical(s):** choose 1-2 files from `verticals/README.md`. Hybrids are normal (for example, AI for pharmacies =
  `ai-apps-agents` + `digital-health`). The *buyer's* vertical drives proof and tone, and the *technology* vertical drives
  moat questions.
- **Stage:** pre-seed, seed, Series A, Series B+, or growth/IPO.
- **Business model:** b2b-saas, usage-based, marketplace, consumer subscription, transactional/fintech, hardware, platform-bio,
  services-led, open-source.
- **Audience and geography:** see `audiences.md`.

## 2. Sweep (fill the placeholders: {sub_vertical}, {year}, {geo}, {stage}, {company}, {competitor})
Run, at minimum:
1. The vertical file's "Live sweep" queries (section 9).
2. `{sub_vertical} startup funding {year} {stage}`, to find who is raising, at what size, and from whom (comparable rounds).
3. `{company} competitors` and `{competitor} raises` / `{competitor} pricing`, to build the competitive frame.
4. `{sub_vertical} market size {year} report`, for **bottom-up inputs** (unit counts, prices, spend per customer) rather
   than headline TAMs.
5. `{investor_name} thesis {sub_vertical}`, when the deck targets named investors. Mirror their language and priorities.
6. `{sub_vertical} regulation {year} {geo}`, for regulated verticals only.

If web search is unavailable but a platform reader is installed (such as Agent Reach for X, Reddit, LinkedIn,
YouTube or GitHub), use it for founder and investor commentary. If nothing is available, say so and rely on the
snapshot.

## 3. Record
Write `research/sweep.md` with these sections:
- **Climate** (2-3 bullets with date and source): is this vertical hot or cold, are round sizes and valuations moving, and what themes are investors chasing?
- **What investors in this vertical scrutinize now:** update the vertical file's list.
- **Benchmarks to beat:** metric | stage | value | source | date. Compare the founder's numbers, and if a number is weak, change
  the framing (a different metric, the trend instead of the level, cohort quality), never the number.
- **Comparable raises:** company | round | amount | date | lead.
- **Competitors:** name | positioning | funding | the honest difference.
- **Market inputs:** for the bottom-up sizing.
- **Words to use and words to avoid:** the vocabulary investors in this space use now (for example "agentic", "outcome-based
  pricing", "dual-use", "non-dilutive") and terms that now read as red flags.

## 4. Use it
- Feed benchmarks and climate into the brief's **vertical adjustments** and **objections** sections.
- Every external number that reaches a slide goes through `facts.md` with its URL and date.
- If the sweep contradicts the bundled vertical file, the sweep wins. Mention material differences to the user. If you can
  write to the skill folder, offer to update the vertical file.

## Found material that is marked confidential
If a search surfaces the company's own deck, data room or memo marked confidential or not clearly published, do not use it
unless the founder supplied it. Use only clearly published sources.

## Source quality ladder
Primary data (Carta, PitchBook-NVCA, Crunchbase News, government statistics, company filings, peer-reviewed papers) >
reputable press (Reuters, FT, Bloomberg, TechCrunch, The Information, Sifted) > investor blogs and reports (a16z, Sequoia,
Bessemer, Point Nine, ICONIQ) > vendor blogs and aggregators. Prefer the most recent figure from the highest rung. Label
vendor or secondary figures as such in `facts.md`.
