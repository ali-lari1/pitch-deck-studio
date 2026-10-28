# AI infrastructure / foundation models

Legend: linked = 2026 sweep (many secondary); unlinked names = background, verify; **[pre-2024]** = older benchmark.

## 1. Who funds it now
- Archetypes: mega-round crossover/growth funds (Thrive, a16z, Sequoia, Lightspeed, Index, Greenoaks); chip/cloud strategics (Nvidia/NVentures, Amazon, Qualcomm, Microsoft); sovereign funds (QIA, MGX, GIC, PIF); infrastructure/credit funds for GPU-backed debt; research-heavy seed funds (Conviction, Radical Ventures, Lux, Khosla).
- Evidence: Index Ventures raised $2B for AI; Accel $5B late-stage AI fund (Apr 2026) plus $3.5B ([PitchBook via TNW](https://thenextweb.com/news/pitchbook-q2-2026-megadeals-87-percent-us-venture-vintage-discount)); Neura Robotics' $1.4B round included Nvidia, Amazon, Qualcomm ([AI Business](https://aibusiness.com/robotics/neura-robotics-raises-1-4b-physical-ai)); Together AI reportedly valued at $8.3B ([Pebblous](https://blog.pebblous.ai/blog/together-ai-neocloud-8-3b-valuation/en/), blog); Nebius reported $6.3B raised ([newsletter](https://aifunding.me/insights/ai-infrastructure-funding-trends-2026)).
- Foundation-model rounds are priced differently: non-AI Series A post $55M vs foundation-model Series A post $300M (Carta Q1 2026 via [Waveup](https://waveup.com/blog/series-a-benchmarks/)).

## 2. What they scrutinize first
1. Compute strategy: committed capacity, cost per token/FLOP, who pays for training, reserved vs spot, vendor concentration.
2. Why the model/infrastructure is differentiated against labs and hyperscalers (benchmarks, data access, architecture efficiency, latency/cost curve).
3. Talent: named researchers, publications, retention, who left which lab.
4. Revenue model and margins: inference gross margin after compute; Series B investors demand ARR bridges that survive a big inference haircut ([beyondtmrw](https://beyondtmrw.org/article/ai-startup-funding-in-2026-dry-powder-revenue-multiples-and-the-infrastructure-tax), blog; number garbled in source).
5. Customer lock-in and demand durability (GPU rental prices fell 60-75% from peak per one analysis; commoditization risk).

## 3. Metrics and benchmarks
| Metric | Pre-seed | Seed | Series A | Source |
|---|---|---|---|---|
| Round size | $1-4M | $5-30M for lab-pedigree teams | $55M-300M post for FM; infra $15-50M | Carta Q1 2026 via Waveup; round sizes are context-dependent (verify) |
| Technical proof | prototype + eval | SOTA on named benchmark / cost-per-token advantage | production deployments, paid usage | n/a |
| Gross margin | n/a | n/a | AI product avg ~52% 2026E (ICONIQ Jan 2026 via [SaaStr](https://www.saastr.com/iconiqs-latest-state-of-ai-report-the-10-most-important-data-points-for-saas-founders)); inference ~23% of revenue | secondary |
| Compute cost | | | $/M tokens, utilization %, tokens/sec/$ | no public stage benchmark found |
| Utilization (neocloud) | | | fleet utilization and contract duration | CoreWeave/Nebius report accelerating revenue and margins ([podcast summary](https://podwise.ai/episodes/8671300)) |
| Concentration | | | top-3 customer % | context: $100M+ rounds took 87.5% of US venture dollars H1 2026 |

No credible stage-by-stage public benchmark for foundation-model startups was found; state that gap and use named comparables plus compute-per-capability curves.

## 4. Slide emphasis
- Ideal: 12-16 slides (often pitched live with a technical appendix).
- Promote: **technical edge slide** (benchmarks, ablations, scaling curve), **compute plan** (GPUs, cost, runway in training runs), **team pedigree**, margin bridge, customer demand.
- Add: **safety/eval & governance** (model cards, red-teaming, export-control posture), **data provenance/licensing**, sovereign/regulatory exposure.
- Demote/cut: generic AI market charts, long architecture prose in main deck (appendix).

## 5. Proof devices
Benchmark tables with dates and eval protocols; open-weights release downloads; side-by-side outputs; latency/cost charts; signed compute contracts; paying API customers; research paper links and independent reproductions.

## 6. Design and tone
Technical credibility: precise charts with axes labeled, minimal marketing gloss, researcher voice; one memorable cost/performance chart. Sober about risks.

## 7. Red flags investors cite
- No path to margin after inference; revenue concentrated in 1-2 labs; cloud credits as "economics".
- Benchmark cherry-picking / contamination; talent concentration risk.
- Capital need that outruns differentiation (secondary prints show some 2021 AI unicorns at 40-60% of last mark; [beyondtmrw](https://beyondtmrw.org/article/ai-startup-funding-in-2026-dry-powder-revenue-multiples-and-the-infrastructure-tax)).

## 8. 2025-26 context
- Feb 2026 was reported as the biggest funding month ever ($189B), mostly OpenAI/Anthropic/Waymo; private AI raised $225.8B in 2025 with $100M+ rounds 79% ([blog roundup citing CB Insights](https://blog.herond.org/ai-startup-funding/); verify).
- Q3 2026 total US deal value fell ~40% QoQ to $98.4B; AI share of Q3 deal value 65.9% ([SiliconANGLE](https://siliconangle.com/?p=849755)).
- Sovereign GPU/neocloud rounds and strategic chip-vendor money dominate ([Pebblous](https://blog.pebblous.ai/blog/together-ai-neocloud-8-3b-valuation/en/)); GPU rental price compression is the key margin risk.

## 9. Live sweep
1. `foundation model startup funding {year} {geo} round compute`
2. `neocloud OR GPU cloud funding {year} utilization gross margin`
3. `{investor_name} AI infrastructure fund {year}`
4. `AI inference cost per token {year} {sub_vertical} benchmark`
5. `open-weight model startup revenue model {year}`
