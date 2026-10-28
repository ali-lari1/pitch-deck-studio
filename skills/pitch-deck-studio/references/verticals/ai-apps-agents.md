# AI apps / agents

Legend: linked = from 2026 sweep (many secondary/vendor; flagged); unlinked investor names = background knowledge, confirm in live sweep; **[pre-2024]** = older benchmark.

## 1. Who funds it now
- Archetypes: AI-specialist seed funds and operator-angels; multi-stage platforms (a16z, Sequoia, Lightspeed, General Catalyst, Khosla, Accel); accelerators (YC); strategics (Nvidia, Salesforce Ventures, CVCs); growth crossovers (Thrive, ICONIQ, Coatue) for breakouts.
- Named, with evidence: a16z, Khosla Ventures, General Catalyst, Y Combinator, Kleiner Perkins lead a seed-AI deal-count ranking (small site, no methodology) ([aifunding.me](https://aifunding.me/insights/most-active-seed-ai-investors)). Sequoia, Khosla, YC top 2026 unicorn-cohort investors, then Lightspeed, Founders Fund, a16z, Bessemer, Lux, General Catalyst, BoxGroup ([Crunchbase via Pipeline Road, Aug 2026](https://pipelineroad.com/news/20260819-sequoia-khosla-y-combinator-lead-2026-unicorn-investors)). Accel, Nvidia, NEA, Lightspeed, Spark, NFDG, Salesforce Ventures recur in consumer-AI rounds ([newmarketpitch tracker](https://newmarketpitch.com/blogs/news/consumer-ai-funding-analysis)).
- Background (verify): Index, Greylock, Conviction, Elad Gil, Menlo Ventures, Insight, Redpoint.
- Context: AI was 82.7% of US deal value YTD Q3 2026 ([SiliconANGLE/PitchBook-NVCA](https://siliconangle.com/?p=849755)).

## 2. What they scrutinize first
1. Is this a wrapper? What survives when the base model gets 10x better or the lab ships your feature (workflow depth, proprietary data, distribution, system-of-record position)?
2. Revenue quality: recurring/usage vs one-time pilots or services; durability of cohorts, not ARR headline. Revenue composition separates a term sheet from a pass ([summary of AI-startup investor views](https://aibusiness.vc/startups/ai-startup-metrics-investors-track), vendor blog).
3. Gross margin trajectory and inference cost per task; pricing model (seat vs outcome vs usage).
4. Speed: time to $1M / $10M ARR vs peers; sales cycle compression.
5. Team's ability to ship weekly and evaluate quality (evals, accuracy, human-in-loop cost).

## 3. Metrics and benchmarks
| Metric | Pre-seed | Seed | Series A | Source |
|---|---|---|---|---|
| ARR | design partners / LOIs | $100-500K, fast growth | $2-3M+ common, $3M+ for AI per several guides; $5-10M claimed at hot funds | [Crunchbase quoting Uncork, May 2026](https://waveup.com/blog/series-a-benchmarks/); [Angel Investors Network 2026](https://angelinvestorsnetwork.com/venture-capital/series-a-funding-requirements-for-ai-startups-2026) (vendor) |
| Growth | n/a | 3x+ YoY | AI-native median 110% vs B2B SaaS 40% at $1-5M ARR | High Alpha through Q2 2025, via Waveup |
| Gross margin | n/a | 50-60% acceptable if improving | AI products ~52% 2026E (45% 2025, 41% 2024) vs SaaS 75-85% | ICONIQ State of AI, Jan 2026, via [SaaStr](https://www.saastr.com/iconiqs-latest-state-of-ai-report-the-10-most-important-data-points-for-saas-founders) (secondary; a 53% figure from a July edition is unverified) |
| Inference cost | | | ~23% of revenue (or costs; wording unclear) at scaling AI B2B | ICONIQ via [SoftwareSeni](https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/) |
| Retention | usage WAU/DAU | logo + gross $ retention; AI-native GRR reported weak (one blog says ~40%, unverified) | NRR 110%+ ask; median NRR 101-106% broad SaaS | [Benchmarkit 2025 via Averi](https://www.averi.ai/blog/15-essential-saas-metrics-every-founder-must-track-in-2026-%28with-benchmarks%29) |
| Valuation | SAFE cap $10-15M | $24.3M post (software) | $78M AI vs $42M non-AI pre-money | Carta Jul 2026; PitchBook Q1 2026 via Waveup |
| Burn multiple | | <2x | <1.5-2x | Sacks 2020 **[pre-2024]**; [Waveup](https://waveup.com/blog/series-a-benchmarks/) |

## 4. Slide emphasis
- Ideal count: 10-12 + appendix.
- Promote: live product demo/screens (slide 2-3), "why not the model labs / why now", cohort retention, pricing and margin bridge, speed chart (ARR by month).
- Add: **moat slide** (data, workflow lock-in, integrations), **unit economics per task/agent run** (cost, accuracy, human-review rate), **safety/eval slide** (benchmarks, guardrails, SOC 2 when selling to enterprise), pilot-to-production conversion.
- Demote/cut: generic "AI will change everything" TAM, model-architecture detail, feature lists.

## 5. Proof devices
- Embedded 60-90s product demo or Loom; real customer workflow before/after with minutes saved and $ per task.
- ARR/usage chart by week since launch; pilot-to-paid conversion table; head-to-head eval vs incumbent/baseline; logos with named champion quotes; MCP/API integration count.

## 6. Design and tone
Product-forward, minimal text, dark or clean UI screenshots, one big number per slide. Confident, specific, no "revolutionary". Show the interface early; avoid stock robot imagery.

## 7. Red flags investors cite
- Thin wrapper on one model with no data/workflow moat; revenue that is mostly pilots, credits, or consulting ([Averi/AI-startup guides](https://aibusiness.vc/startups/ai-startup-metrics-investors-track)).
- Margins below ~50% with no path; cloud credits counted as durable economics ([beyondtmrw](https://beyondtmrw.org/article/ai-startup-funding-in-2026-dry-powder-revenue-multiples-and-the-infrastructure-tax), blog).
- Reported ARR that is annualized usage spikes ("ARR" not comparable across companies; [Mezha roundup](https://mezha.net/eng/?p=2977604)).
- Churn from novelty; no evals.

## 8. 2025-26 context
- AI took 82.7% of US deal value YTD through Q3 2026, though quarterly share fell to 65.9% in Q3 as total value dropped ~40% ([SiliconANGLE](https://siliconangle.com/?p=849755)).
- AI Series A pre-money roughly 2x non-AI ($78M vs $42.4M, Q1 2026); AI step-up 2.2x vs 1.6x ([PitchBook via TNW](https://thenextweb.com/news/pitchbook-q2-2026-megadeals-87-percent-us-venture-vintage-discount)).
- Fast-scaling reference points: Cursor ~$500M ARR; Sierra +$100M ARR in two quarters; Windsurf and Moveworks hit $100M ARR before being acquired ([CB Insights via search summary](https://www.cbinsights.com/research/?p=174434)); secondary prints show some 2021 AI unicorns at 40-60% of last mark (blog).

## 9. Live sweep
1. `{sub_vertical} AI agent startups funding {year} seed Series A investors`
2. `AI startup gross margin benchmark {year} ICONIQ OR Bessemer OR a16z`
3. `fastest growing AI startups ARR {year} {sub_vertical}`
4. `{investor_name} AI investment thesis {year} "what we look for"`
5. `AI wrapper moat investor diligence {year} {sub_vertical}`
