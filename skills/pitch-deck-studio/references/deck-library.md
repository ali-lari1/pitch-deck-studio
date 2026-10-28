# Deck library: what 114 successful decks (2022-2026) and three house references teach

`data/decks.json` holds 114 publicly available pitch decks for rounds that closed in 2022 or later. They span 23 verticals,
from pre-seed to growth, including ElevenLabs, Mistral, EliseAI, Front, Honeycomb, Spade, Corti, 1X, IQM, Posh, Smalls and
ShopMy. Each round, year and lead was checked against news or press releases, and caveats sit in the record. Use the
library for **patterns and inspiration, never to copy**: pull 5-8 comparables for the company's playbook and stage, note
what their best slides did, and do it in this company's own words and brand.

## House references (the look we aim for)

**SpaceX IPO roadshow (June 2026, 60 slides).** This is the best example of "sleek and simple at scale".
- Black canvas, light uppercase grotesk headlines with slight tracking, small tracked-caps labels, and giant condensed numerals.
- The "N of 1" slide: three columns (one per business), each a stack of hairline-separated rows pairing a small caps label with a
  big number. Twelve facts and zero adjectives. Recreate it with `@layout stats` + `@class rows`.
- Section dividers are a full-bleed photo with a two-word title in the lower left ("OUR SPACE BUSINESS").
- Every chart is monochrome with one highlighted series, a title that states the conclusion, and a source line at the bottom.
- The rhythm alternates: stats grid → photo divider → chart → milestone timeline → photo divider.
- Disclaimers and the offering summary come first, and non-GAAP reconciliations and metric definitions go in the appendix.
  This is the roadshow arc (G).

**Airbnb seed deck (2009, a widely circulated redesign).** This is the classic story order: problem → solution → market
validation → market size → product → business model → adoption strategy → competition → advantages → team → press →
testimonials → financial ask.
- One coral accent and warm interior photography on half the slides.
- Market size is shown as three stacked numbers (total → serviceable → share), and the business model is reduced to one
  sentence plus two numbers.
- Competition is a 2×2 on two axes the customer cares about (affordable vs expensive, offline vs online).

**Stripe-style deck (a template redesign of public Stripe material).** Clean white with a single indigo accent.
- Big sentence-case headlines that make a claim ("The new standard in online payments").
- A logo-cloud slide ("You're in good company"), a product-stack diagram, and a mission statement on a dark accent slide.
- Lesson: the product and the customers do the talking.

What the three have in common: one accent colour, very few words, one focal point per slide, numbers set in display
type, real imagery, and consistent chrome. That is the default this skill produces.

## Cross-deck patterns (from the research teams' reads of every deck)
1. **Short wins.** The best-regarded recent decks run 7-15 slides. The long ones (30-90 slides) worked only with a strong reason
   (live revenue, physical-plant detail, a public-market audience) and drew reviewer criticism otherwise.
2. **The strongest proof comes first.** Many decks open slide 2 with a traction chart, an "at a glance" stats slide, a famous logo
   or a founder credential (Front, Hour One, OroraTech, Super.com, Haystack). In regulated or technical fields, "can they do
   this?" is answered before "why does it matter?".
3. **One idea and one giant number per slide.** Examples: EnCharge (150 vs 5-10 TOPS/W), Spade (<50 ms), Chef Robotics (44M servings),
   Unframe ("400% NRR"). Sentence headlines carry the claim (Juro).
4. **Show the artifact.** Annotated product screenshots, one per capability (Portkey, Screenloop, Kluster, Sazabi); a working
   prototype video at pre-seed (ElevenLabs); before/after data records (Spade); a chip die photo (EnCharge); thermal imagery of
   real fires (OroraTech); image-only before/after (Gendo).
5. **Consumer decks lead with a human insight and a single stat**, not a market-size chart (Pie, Posh, Howbout). The product is
   shown as a loop or four verbs (ShopMy's Discover/Engage/Collaborate/Track), and traction is one hockey-stick or retention curve.
6. **Brand carries consumer and D2C decks.** The strongest (900.care, Blume, Dutch, Smalls, Posh) reuse their packaging
   language: a one- or two-colour system, a distinctive display face, and full-bleed photography on the cover and close.
7. **Regulated and deep-tech decks de-risk explicitly**: a cost-parity slide (Terra CO2), trial data (Haystack), a
   challenges-and-mitigations slide (Aether), a pipeline or beachhead table (Georgiamune).
8. **2024-2026 design trend:** dark backgrounds with a single accent and a distinct brand look rather than a template
   (Portkey, Supernormal, Glyphic, EliseAI, Sazabi, Mave, Unframe, Stilta). Weak decks are dense and plain or look
   templated.
9. **Common misses:** no use-of-funds slide, vanity metrics (GitHub stars, waitlists without conversion), no competition
   slide, undefined metrics. This skill's linter and review panel target exactly these.

<!-- GENERATED -->
## The numbers (114 decks, rounds closed 2022-2026)

- Slide count: median **14**, middle half 11-18, range 7-90 (n=107 with known counts).
- Use at least one show-don't-tell device (screenshots, product photos, charts, logo walls, before/after): **100 of 114**.
- What slide 2 does (n=102 with a known slide 2): problem / stat 33%, mission / vision / insight 19%, summary / proof up front (traction, at-a-glance, key numbers) 18%, team / pedigree 15%, other (market, context, comparison) 14%, product / demo 2%.
- Stage mix: series-a 50, seed 33, series-b 20, growth 7, pre-seed 3, unknown 1.
- Year mix: 2022: 31, 2023: 50, 2024: 20, 2025: 7, 2026: 6.

## Index by playbook

Query it with `python3 scripts/find_decks.py --vertical <playbook or keyword> [--stage seed] [--show-dont-tell] [--min-design 4]`. Each entry in `data/decks.json` carries the slide sequence, narrative pattern, design notes, standout moves, weaknesses, sources and caveats.

### ai-apps-agents (12)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Harmony | Seed · 2026 | $34M | 15 | TL;DR upfront, founder-exit credibility, wedge (IT) -> expansion, fast-onboarding… | [link](https://www.businessinsider.com/harmony-pitch-deck-ai-startup-34-million-seed-founders-cisco-2026-7) |
| Unframe | Series B · 2026 | $50M | ? | One-idea-per-slide with giant type: market failure -> delivery gap -> mechanics -> NRR… | [link](https://www.businessinsider.com/unframe-raises-50-million-to-boost-enterprise-ai-pitch-deck-2026-6) |
| EliseAI | Series D · 2024 | $75M | 7 | Seven-slide growth deck: mission, traction, funding, two vertical product slides, team | [link](https://www.businessinsider.com/pitch-deck-eliseai-raises-series-d-unicorn-valuation-2024-8) |
| Gendo | Pre-seed · 2024 | $1M | 16 | Visual-first (before/after imagery) then process-diagram vision, then beta traction | [link](https://www.businessinsider.com/pitch-deck-gendo-raises-vc-funding-architecture-platform-2024-7) |
| Wondercraft | Seed · 2024 | $3M | 9 | Category analogy ('Canva of audio'), 3-audience problem, product, markets, social-proof… | [link](https://www.businessinsider.com/wondercraft-audio-ai-startup-raises-3-million-in-seed-funding-2024-1) |
| DeckMatch | Seed · 2023 | $1M | 14 | Problem-first: four slides escalate the pain, with gen-AI as both cause and solution | [link](https://techcrunch.com/2023/08/18/sample-seed-pitch-deck-deckmatch/) |
| Glyphic AI | Pre-seed · 2023 | $6M | 11 | Team-first, thesis, problem, then three product slides each with UI, then positioning | [link](https://www.businessinsider.com/glyphic-ai-ex-deepmind-staffers-secure-55-million-llm-startup-2023-6) |
| Scalestack | Seed · 2023 | $1M | 18 | Team-then-traction 'victory lap' opening, three-slide problem build, customer stories… | [link](https://techcrunch.com/2023/12/01/sample-seed-pitch-deck-scalestack/) |
| Supernormal | Seed · 2023 | $10M | 17 | Category claim then demo-led traction; ends with GTM and committed-round slide | [link](https://www.businessinsider.com/supernormal-generative-ai-startup-raises-10m-seed-round-2023-1) |
| Checkstep | Seed · 2022 | $5M | 7 | Seven-slide arc: opportunity -> cost/regulation -> platform -> product -> proof | [link](https://www.businessinsider.com/checkstep-ai-startup-raises-5-million-seed-round-pitch-deck-2022-5) |
| Hour One | Series A · 2022 | $20M | 11 | Compact summary-first: at-a-glance up front, product depth in the middle, case-study… | [link](https://techcrunch.com/2022/12/01/pitch-deck-teardown-hour-ones-20m-series-a-deck/) |
| Spinach | Seed · 2022 | $6M | 10 | Traction-led: lean 10-slide deck with a single growth chart doing the work | [link](https://techcrunch.com/2023/02/09/sample-seed-pitch-deck-spinach-io/) |

### ai-infra-foundation-models (7)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| RagaAI | Seed · 2024 | $5M | 10 | Market tailwind + failure examples -> platform vision -> differentiated 2x2 -> advisor… | [link](https://www.businessinsider.com/ragaai-ex-nvidia-raises-4-7-million-for-ai-startup-2024-1) |
| RapidCanvas | Seed · 2024 | $8M | 9 | Problem (talent gap) -> 2x2 white-space -> capabilities -> differentiated promise | [link](https://www.businessinsider.com/exclusive-rapidcanvas-emerges-from-stealth-with-7-5-million-raise-2024-3) |
| Aindo | Series A · 2023 | $6M | 13 | Company snapshot -> problem/solution/why-now -> platform -> market -> competitor matrix… | [link](https://www.businessinsider.com/aindo-pitch-deck-generative-ai-startup-secures-6-million-2023-10) |
| ElevenLabs | Pre-seed · 2023 | $2M | 14 | Cost/time pain with big numbers -> working prototype -> team -> TAM -> early-win proof | [link](https://www.businessinsider.com/elevenlabs-ai-voice-intelligence-startup-raises-2-million-2023-1) |
| Mistral AI | Seed · 2023 | $113M | 7 | FOMO-driven memo: hype -> scarcity of talent -> geopolitical gap -> team | [link](https://drive.google.com/file/d/1gquqRqiT-2Be85p_5w0izGQGgHvVzncQ/view) |
| Portkey | Seed · 2023 | $3M | 14 | Pain-led product tour: one feature per slide with its screenshot, then logos and… | [link](https://www.businessinsider.com/portkeyai-startup-businesses-build-ai-apps-with-3-million-2023-8) |
| V7 | Series A · 2022 | $33M | 41 | Product-experience-led ('show, don't tell') then logos/NRR proof, then… | [link](https://pitch.com/public/fd2b160f-2c7d-43f1-b625-11885bfe1f15) |

### b2b-saas (7)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Fibery | Series A · 2023 | $5M | 15 | Classic problem-solution-market arc ending in a concrete ask with MRR/ARR goals | [link](https://techcrunch.com/2023/05/11/sample-series-a-pitch-deck-fibery/) |
| Kluster | Series A · 2023 | $5M | 10 | Big-type claims -> three-step loop -> one screenshot per step -> PMF stats -> culture… | [link](https://www.businessinsider.com/kluster-pitch-deck-ai-startup-raises-5-million-series-a-2023-4) |
| Scrintal | Seed · 2023 | $1M | 19 | Testimonial-driven proof with an appendix for why-now/competition | [link](https://techcrunch.com/2023/01/19/sample-seed-pitch-deck-scrintal/) |
| Buynomics | Series A · 2022 | $13M | 14 | Category-OS vision, quantified results and case studies, then founder close | [link](https://www.businessinsider.com/series-a-pitch-deck-buynomics-raises-13-million-from-insight-2022-11) |
| Equals | Series A · 2022 | $16M | 15 | Story deck + separate 7-slide data deck: words first, numbers second | [link](https://wrap-text.equals.com/p/equals-series-a-deck) |
| Front | Series D · 2022 | $65M | 11 | Traction-led growth deck: numbers first, product/market proof, then vision | [link](https://techcrunch.com/2022/09/01/sample-series-d-pitch-deck-front/) |
| Unito | Series B · 2022 | n/a | 12 | Market-history framing replaces 'why now'; vertical-expansion story grows the TAM | [link](https://techcrunch.com/2023/07/28/sample-series-b-pitch-deck-unito/) |

### biotech-therapeutics (1)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Georgiamune | Series A · 2023 | $75M | 20 | Biological philosophy first -> platform + pipeline table -> leadership pedigree ->… | [link](https://startupfundraising.com/library/articles/georgiamune-pitch-deck-teardown) |

### climate-energy (8)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| AtmosZero | Series A · 2024 | $21M | 14 | Problem sizing via steam statistics -> drop-in hardware solution (inferred only from BI… | [link](https://www.businessinsider.com/pitch-deck-startup-atmoszero-raised-21-million-decarbonize-steam-2024-2) |
| Ineratec | Series B · 2024 | $129M | 19 | unknown | [link](https://www.businessinsider.com/green-shell-ineratec-secured-129-million-with-this-pitch-deck-2024-1) |
| Terra One | Seed · 2024 | $8M | 13 | Three-slide problem build (clean energy wasted) -> strategic solution ->… | [link](https://techcrunch.com/2024/05/24/sample-seed-pitch-deck-terra-one/) |
| Ebb Carbon | Series A · 2023 | $20M | 13 | Show the machine first (process diagram), then climate need, then mechanism, then… | [link](https://www.businessinsider.com/pitch-deck-ebb-carbon-carbon-emissions-ocean-acidification-20-million-2023-4) |
| HeatTransformers | Series A · 2023 | $16M | 10 | unknown | [link](https://www.businessinsider.com/exclusive-look-pitch-deck-heat-pump-startup-heattransformers-16-million-2023-3) |
| Plan A | Series A extension / growth (sources differ) · 2023 | $27M | 11 | unknown | [link](https://www.businessinsider.com/carbon-accounting-company-plan-a-lightspeed-venture-pitch-deck-2023-9) |
| Supercritical | Series A · 2023 | $13M | 11 | unknown | [link](https://www.businessinsider.com/pitch-deck-climate-tech-startup-supercritical-lightspeed-carbon-removal-2023-6) |
| Terra CO2 | Series A · 2022 | $46M | 25 | Industrial-credibility pitch: chemistry-grounded problem, third-party validation,… | [link](https://www.businessinsider.com/pitchdeck-terraco2-climatetech-green-cement-46million-seriesa-bill-gates-2022-8) |

### consumer-apps-social (8)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Howbout | Series A · 2024 | $8M | 12 | Zeitgeist problem (Gen Z is over feeds) -> product -> retention/engagement proof ->… | [link](https://www.businessinsider.com/pitch-deck-social-calendar-app-howbout-goodwater-capital-consumer-fund-2024-10) |
| Lost iN | Seed · 2024 | $4M | 14 | Media decline -> creator-first video model -> multi-revenue + roll-up plan -> team of… | [link](https://www.businessinsider.com/pitch-deck-lost-in-raised-seed-round-travel-media-2024-6) |
| Pie | Series A · 2024 | $12M | 31 | Macro social thesis (loneliness epidemic) -> product thesis -> proof in one city… | [link](https://www.businessinsider.com/pitch-deck-irl-social-startup-pie-raises-andy-dunn-bonobos-2024-10) |
| Checkmate | Series A · 2023 | $15M | 25 | Why-now market framing -> hard PMF numbers -> distinctive Gen-Z growth channels ->… | [link](https://www.businessinsider.com/fintech-checkmate-gen-z-online-shoppers-savings-chainsmokers-paris-hilton-2023-5) |
| Hype (formerly Pico) | Series A · 2023 | $10M | 13 | Definition hook -> category thesis -> three-part funnel (capture/nurture/revenue) ->… | [link](https://www.businessinsider.com/pitch-deck-example-creator-startup-hype-fundraising-vc-series-a-2023-4) |
| Layla | Seed · 2023 | $3M | 8 | Behaviour insight (people find trips on social) -> integrated journey -> product ->… | [link](https://www.businessinsider.com/layla-travel-startup-secures-3-million-pitch-deck-2023-11) |
| Sunnyside | Series A · 2023 | $12M | 10 | Under-served problem stat -> team -> product -> outcomes | [link](https://www.businessinsider.com/pitch-deck-healthtech-startup-sunnyside-raise-vc-funding-2023-11) |
| point.me | Series A · 2023 | $10M | 16 | Consumer pain (unredeemed points) -> self-serve + concierge product -> traction -> moat… | [link](https://techcrunch.com/2023/09/29/sample-series-a-pitch-deck-point-me/) |

### crypto-web3 (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| 0x Labs | Series B · 2022 | $70M | 20 | Macro thesis -> fragmentation problem -> layered product stack -> hockey-stick usage… | [link](https://startupfundraising.com/library/articles/0x-labs-pitch-deck-teardown) |
| Diamond Standard | Series A · 2022 | $30M | 11 | Mission-first cover, then solution before problem, market, product roadmap, ESG angle;… | [link](https://techcrunch.com/2023/04/13/sample-series-a-pitch-deck-diamond-standard/) |
| Space and Time | Strategic round (post-$10M seed) · 2022 | $20M | 14 | Missing-analytics-layer problem -> benchmarked solution -> interoperability ->… | [link](https://startupfundraising.com/library/articles/space-and-time-pitch-deck-teardown) |
| Yuga Labs | Seed (reported; teardown site labels it Series A) · 2022 | $450M | 90 | Culture-as-moat: social proof and celebrity holders first, then game/metaverse vision,… | [link](https://startupfundraising.com/library/articles/yuga-labs-pitch-deck-teardown) |

### cybersecurity (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Mave | Series A · 2026 | $28M | ? | Threat chart -> platform diagram -> one named-type customer story -> traction/funding | [link](https://www.businessinsider.com/mave-startup-cybersecurity-funding-ai-agents-pitch-deck-2026-10) |
| Nokod Security | Seed · 2023 | $8M | 21 | Team-first (two prior security exits), then trend-and-threat build, solution, TAM, GTM | [link](https://techcrunch.com/2023/07/07/sample-seed-pitch-deck-nokod-security/) |
| Protecto | Seed · 2023 | $4M | 14 | Problem/urgency then technology-explainer then use cases | [link](https://techcrunch.com/2024/03/22/sample-seed-pitch-deck-protecto/) |
| MedCrypt | Series B · 2022 | $25M | 12 | Regulatory-clock opportunity story (compliance deadline) with a four-product lineup | [link](https://techcrunch.com/2022/12/15/sample-series-b-pitch-deck-medcrypt/) |

### deeptech (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| EnCharge AI | Series B · 2025 | $100M | 9 | Market-timing (AI PC) + hard efficiency metric + founder/advisor pedigree; deliberately… | [link](https://www.businessinsider.com/encharge-ai-funding-tiger-global-pitch-deck-2025-2) |
| Aether (Aether Biomachines) | Series A · 2023 | $49M | 23 | Bold-future mission slide, then platform solution and quantified advantages, use cases,… | [link](https://techcrunch.com/2023/10/27/sample-series-a-pitch-deck-aether/) |
| IQM Quantum Computers | Series A2 · 2022 | $128M | 20 | unknown | [link](https://www.businessinsider.com/pitch-deck-quantum-computing-startup-world-fund-2022-7) |
| Scantinel Photonics | Series A (extended) · 2022 | $10M | 10 | Pedigree-first technology deck: skips the generic problem slide, leads with the… | [link](https://www.businessinsider.com/scantinel-photonics-raises-10-million-to-make-self-driving-safer-2022-11) |

### defense-space (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Deepnight | Seed · 2025 | $6M | unknown | unknown | [link](https://b17news.com/heres-the-pitch-deck-deepnight-used-to-raise-5-5-million-in-funding-to-make-military-night-goggles-cheaper-with-ai/) |
| Onebrief | Series C extension · 2025 | $20M | unknown | unknown | [link](https://www.businessinsider.com/exclusive-pitch-deck-onebrief-raised-defense-tech-unicorn-2025-6) |
| OroraTech | Series B · 2024 | $27M | 10 | Product-led: lead with scale metrics, then a full-bleed fire photo, product lifecycle,… | [link](https://www.businessinsider.com/pitch-deck-ororatech-funding-series-b-ai-wildfires-2024-10) |
| Open Cosmos | Series B · 2023 | $50M | 13 | unknown | [link](https://www.businessinsider.com/open-cosmos-space-tech-startup-raises-50m-to-expand-satellite-data-2023-9) |
| Sateliot | Series A · 2022 | $11M | 18 | Big coverage-gap problem -> team early -> standards-based solution -> why us ->… | [link](https://techcrunch.com/2022/11/17/sample-series-a-pitch-deck-sateliot/) |

### devtools-open-source (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Sazabi | Seed · 2026 | $8M | 11 | Brand-first manifesto: 3-step demo -> founder -> 2 weeks/50 customers ->… | [link](https://www.businessinsider.com/pitch-deck-sazabi-ai-observability-8-million-y-combinator-2026-6) |
| Honeycomb | Series D · 2023 | $50M | 18 | Category-creation with traction proof, then GTM and an explicit ask | [link](https://techcrunch.com/2023/04/20/sample-series-d-pitch-deck-honeycomb/) |
| Vespa.ai | Series A · 2023 | $31M | 12 | Deck-summary-first, technical credibility (20 years at Yahoo) and an explicit $15M… | [link](https://www.businessinsider.com/vespaai-yahoo-spinout-raises-31-million-series-a-2023-10) |
| Encore | Seed · 2022 | $3M | 24 | Team-credibility first, 4-slide problem build, diagram-driven product, community-led… | [link](https://techcrunch.com/2022/06/02/sample-seed-pitch-deck-encore/) |
| Netmaker | Seed · 2022 | $2M | 14 | Vision-forward OSS story with a growth-chart traction slide | [link](https://techcrunch.com/2023/06/16/sample-seed-pitch-deck-netmaker/) |

### digital-health (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Heidi Health | Series B · 2025 | $65M | 9 | Burnout problem -> adoption-is-the-battleground market thesis -> PLG proof (visit… | [link](https://www.businessinsider.com/exclusive-pitch-deck-ai-scribe-heidi-health-raise-65-million-2025-10) |
| Navina | Series C · 2025 | $55M | unknown | unknown | [link](https://www.businessinsider.com/navina-raised-55-million-goldman-sachs-series-c-pitch-deck-2025-3) |
| Corti | Series B · 2023 | $60M | 12 | Shock statistic -> macro cost crisis -> proprietary-data solution -> three quantified… | [link](https://startupfundraising.com/library/articles/corti-pitch-deck-teardown) |
| Eureka Health | Seed · 2023 | $7M | 12 | Open on the product itself, personal founder story, three-step cold-start flywheel, B2B… | [link](https://www.businessinsider.com/eureka-health-pitch-deck-raise-7-million-seed-khosla-ventures-2023-8) |

### ecommerce-d2c-cpg (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| 900.care | Series A · 2024 | $23M | 16 | Playful brand voice carries a serious thesis: plastic problem -> subscription refill… | [link](https://www.businessinsider.com/900-care-secures-22-7-million-for-its-refillable-products-2024-3) |
| Smalls | Series B · 2023 | $19M | 24 | Subscription-metric narrative: product -> how it works -> performance (CAC/churn/LTV)… | [link](https://techcrunch.com/2023/04/06/sample-series-b-pitch-deck-smalls/) |
| Blume | Seed (amount stated CAD-goal; USD ~1.8M) · 2022 | $2M | 13 | Consumer-brand story: simple problem -> hero product -> gap on a 2x2 -> traction ->… | [link](https://www.businessinsider.com/pitch-deck-startup-blume-used-raise-nearly-2-million-2023-1) |
| Dutch | Series A · 2022 | $20M | 17 | Brand-led story: cute cover -> boom market -> vet system failing -> own tech ->… | [link](https://techcrunch.com/2022/05/12/sample-series-a-pitch-deck-dutch/) |
| Rootine | Series A · 2022 | $10M | 29 | Masterclass 'data first' deck: summary + traction before story; product as loop;… | [link](https://www.slideshare.net/slideshow/pitch-deck-teardown-rootines-10m-series-a-deck/254755968) |

### edtech (6)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Ignite! Reading | Series A · 2023 | $10M | 9 | Big stat problem -> causes -> evidence-based solution -> customer quotes -> results ->… | [link](https://www.businessinsider.com/pitch-deck-edtech-ignite-reading-rethink-ken-griffin-2023-2) |
| Innovamat | Series A · 2023 | $21M | 13 | Category re-framing (learning experience vs textbook) -> satisfaction proof -> research… | [link](https://www.businessinsider.com/innovamat-edtech-math-startup-europe-vc-funding-reach-capital-2023-4) |
| Kira Learning | Series A · 2023 | $15M | 16 | Regulatory tailwind -> state-by-state data -> procurement forecast -> GTM wedge ->… | [link](https://www.businessinsider.com/kira-learning-edtech-startup-ai-computer-science-funding-nea-2023-5) |
| Schola | Series A · 2023 | $10M | 12 | Mission-first story that mirrors the investor's thesis -> two-sided problem -> why now… | [link](https://www.businessinsider.com/pitchdeck-edtech-startup-schola-charter-private-public-schools-2023-1) |
| StudentFinance | Series A · 2023 | $41M | 15 | Bold mission -> three-part problem -> solution flow -> benchmark business model ->… | [link](https://techcrunch.com/2023/03/16/sample-series-a-pitch-deck-studentfinance/) |
| Trala | unknown (BI reports $8M raise) · 2023 | $8M | 18 | Humanist origin story -> broken market -> product hybrid -> LTV and ARR proof ->… | [link](https://www.businessinsider.com/pitch-deck-music-lesson-startup-trala-used-raise-funding-2023-3) |

### fintech (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Dub | Series A · 2025 | $30M | 15 | Behavioral insight (retail wants agency but can't pick stocks) -> convergence of trends… | [link](https://www.businessinsider.com/pitch-deck-fintech-finance-influencer-startup-dub-raises-30-million-2025-4) |
| Arbol | Series B · 2024 | $60M | 13 | Credibility-first: elite team pedigree up front, then a macro 'paradigm shift' proof,… | [link](https://www.businessinsider.com/pitch-deck-ai-climate-insurance-startup-arbol-series-b-2024-5) |
| Faye | Series A · 2023 | $10M | 19 | Summary-first: four headline numbers up front, then team, problem, market comparison… | [link](https://techcrunch.com/2023/05/26/sample-series-a-pitch-deck-faye/) |
| Spade | Series A · 2023 | $10M | 13 | Legacy-plumbing problem -> concrete before/after proof -> latency benchmarks ->… | [link](https://www.businessinsider.com/fintech-spades-series-a-pitch-deck-raise-10-million-2023-12) |
| Super.com | Series C · 2023 | $85M | 17 | Traction-first flex (two traction slides before the team), then customer + market, then… | [link](https://techcrunch.com/2023/06/30/sample-series-c-pitch-deck-super-com/) |

### food-agtech (3)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Revi | Series A · 2024 | $14M | 17 | Operator pain -> product loop -> head-to-head win rates -> network density per market… | [link](https://www.businessinsider.com/pitch-deck-revi-secures-14-5-million-series-a-2024-7) |
| Lunchbox | Series B · 2022 | $50M | 15 | Cost pain -> all-in-one product -> case study -> why-now ghost kitchens -> Toast… | [link](https://techcrunch.com/2022/06/09/sample-series-b-pitch-deck-lunchbox/) |
| Next Gen Foods (TiNDLE) | Series A · 2022 | $100M | 21 | Climate thesis -> speed (blitzscale) -> product proof -> investors/board -> chef… | [link](https://www.businessinsider.com/pitch-deck-next-gen-used-to-raise-100-million-tindle-2022-2) |

### gaming (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Look North World | Seed · 2024 | $4M | 12 | Where attention is -> platformisation of games -> creator talent funnel -> focus areas… | [link](https://www.businessinsider.com/pitch-deck-gaming-studio-look-north-world-seed-funding-2024-7) |
| Allstar | Series A · 2023 | $12M | 7 | Behavioural insight (few gamers create) -> huge audience -> cloud solution ->… | [link](https://www.businessinsider.com/pitch-deck-mark-cuban-backed-gaming-creator-startup-allstar-2023-12) |
| Kinjo | Seed · 2023 | $6M | 16 | Generational shift -> 2x2 positioning -> platform logic -> loop diagrams -> early results | [link](https://www.businessinsider.com/pitch-deck-edtech-gaming-startup-kinjo-roblox-seed-venture-capital-2023-8) |
| Omada | Seed · 2023 | $8M | 9 | Cultural positioning -> retention metrics tied to each feature -> community -> ecosystem | [link](https://www.businessinsider.com/omada-sports-gaming-app-raises-75-million-round-led-by-felix-capital-2023-9) |

### hardware-robotics (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Multiply Labs | Series B · 2026 | $75M | unknown | unknown | [link](https://www.businessinsider.com/see-the-pitch-deck-drug-manufacturing-startup-used-raise-75m-2026-10) |
| Chef Robotics | Series A · 2025 | $21M | 12 | Labor-shortage macro -> why food is hard for AI (data moat) -> flywheel -> high-mix… | [link](https://www.businessinsider.com/pitch-deck-ai-robot-startup-chef-used-raise-20-6-2025-4) |
| 1X Technologies | Series B · 2024 | $100M | 13 | unknown | [link](https://www.businessinsider.com/1x-openai-robotics-startup-raises-100-million-from-eqt-ventures-2024-1) |
| ANYbotics | Series B · 2023 | $50M | 19 | Traction-forward growth pitch: mission and problem, industry evolution, product,… | [link](https://techcrunch.com/2023/08/11/sample-series-b-pitch-deck-anybotics-ag/) |
| Xpanceo | Seed · 2023 | $40M | 19 | Computing-history timeline -> AR failure diagnosis -> smart-lens solution/product ->… | [link](https://techcrunch.com/2024/04/12/sample-seed-pitch-deck-xpanceo/) |

### hr-legal-vertical-saas (5)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Stilta | Seed · 2026 | $10M | 7 | Traction-first (time-stamped weekly MRR chart), then problem/solution, market, team, ask | [link](https://www.businessinsider.com/stilta-ai-patent-law-legal-ai-seed-round-pitch-deck-2026-7) |
| Robin AI | Series B · 2024 | $26M | 8 | Bold prediction -> incumbent stack (Word/Outlook) -> market-cap gap vs other verticals… | [link](https://www.businessinsider.com/pitch-deck-legal-tech-startup-robin-ai-raise-series-b-2024-1) |
| Polimorphic | Seed · 2023 | $6M | 16 | Giant under-digitised market -> labour shortage -> product maturity ladder -> client… | [link](https://www.businessinsider.com/polimorphic-pitch-deck-ai-local-governments-raises-5-6-million-2023-11) |
| Juro | Series B · 2022 | $23M | 15 | Action-title story: every slide headline is a full-sentence claim, traction-heavy | [link](https://techcrunch.com/2022/11/25/sample-series-b-pitch-deck-juro/) |
| Screenloop | Seed · 2022 | $7M | 15 | Pain-quotes -> platform -> three annotated product screenshots with an outcome stat… | [link](https://www.businessinsider.com/screenloop-hiring-intelligence-startup-raises-7-million-pitch-deck-2022-6) |

### marketplaces (6)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Posh | Series A · 2024 | $22M | 12 | Founder story -> emotional problem (loneliness) -> proof via organizer cases -> scale… | [link](https://www.businessinsider.com/posh-raises-series-a-help-make-plans-friends-pitch-deck-2024-7) |
| ShopMy | Series A (add-on) · 2024 | $18M | 23 | Problem -> platform in 4 verbs (Discover/Engage/Collaborate/Track) -> supply & demand… | [link](https://www.businessinsider.com/read-pitch-deck-affiliate-marketing-startup-shopmy-used-series-a-2024-6) |
| Catch+Release | Series A (extension) · 2023 | $9M | 12 | Brand pain -> unmet supply (the internet) -> productised licensing in 3 steps ->… | [link](https://www.businessinsider.com/pitch-deck-content-licensing-startup-catch-release-raise-8-million-2023-8) |
| Creative Fabrica | Series B (equity + debt) · 2023 | $61M | 19 | Emotional hook -> flywheel -> demographics -> supply playbook -> positioning ->… | [link](https://www.businessinsider.com/creative-fabrica-raises-61-million-series-b-pitch-deck-2023-1) |
| HomeCooks | Seed (crowdfunding) · 2023 | $3M | 25 | Marketplace chicken-and-egg answered with network-effect loop; sustainability layer;… | [link](https://techcrunch.com/2023/12/22/sample-seed-pitch-deck-homecooks/) |
| Howdy | Series A + extension ($18M total) · 2022 | $18M | unknown | Short sampled deck: one-line positioning -> human proof -> local presence -> contact | [link](https://www.businessinsider.com/howdy-pitch-deck-ycombinator-tech-worker-staffing-developers-latam-2023-1) |

### medtech-devices (1)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Haystack Oncology | Series A · 2022 | $56M | 25 | Pedigree + repeat-winner team first, define the beachhead, then 20-year science moat,… | [link](https://www.businessinsider.com/see-haystack-oncologys-series-a-deck-for-cancer-blood-test-2022-11) |

### mobility-logistics (1)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Liefergruen | Series A · 2022 | $12M | 9 | Consumer pain in plain language -> large market stat -> consumer brand + network flywheel | [link](https://www.businessinsider.com/pitch-deck-startup-liefergrun-12-million-last-mile-delivery-greener-2022-9) |

### proptech-construction (4)

| Company | Round · year | Raised | Slides | Pattern | Deck |
|---|---|---|---|---|---|
| Kasa Living | Series C · 2023 | $70M | 33 | Lead with credibility (logos + quotes) -> step back to the story -> guest + owner value… | [link](https://www.businessinsider.com/kasa-livings-33-page-pitch-deck-that-raised-70-million-in-funding-2024-4) |
| Roami (deck titled 'Sextant') | Series A · 2023 | $14M | 22 | Counter-cyclical hook (+650% in 2020) -> how -> staged consumer pain photos -> category… | [link](https://www.businessinsider.com/pitch-deck-short-term-rental-startup-roami-raise-series-a-2023-5) |
| Ergeon | Series B · 2022 | $40M | 16 | Team-first opener -> flywheel + software scalability -> unit economics -> run rate ->… | [link](https://techcrunch.com/2022/06/16/sample-series-b-pitch-deck-ergeon/) |
| Rive | Series A · 2022 | $24M | 14 | Simple promise -> three services -> capability matrix -> product -> team | [link](https://www.businessinsider.com/pitch-deck-proptech-rive-raises-24-million-series-a-2022-11) |

