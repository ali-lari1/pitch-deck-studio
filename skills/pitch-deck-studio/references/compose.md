# Composing with other skills and tools

Pitch Deck Studio is self-sufficient. When other skills or tools are installed, use them for the step they are best at.
Never fail because one is missing. Use the fallback.

## How to detect
1. **Your harness's skill list** (the most reliable): if a skill with that name appears in your available skills, use it.
2. **Filesystem probe**: look for `*/<name>/SKILL.md` under `~/.agents/skills`, `.agents/skills`, `~/.claude/skills`,
   `.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`, `~/.config/opencode/skills`, `.opencode/skills`,
   `~/.hermes/skills`, `~/.grok/skills`, `~/.cursor/skills`, `~/.copilot/skills`.
3. **CLIs**: `command -v <binary>`.

## The table
| Need | Use if installed | How | Fallback |
|---|---|---|---|
| Editable PowerPoint | a `pptx` skill (e.g. Anthropic's), `ppt-master` | hand it `deck.md` (content, layout per slide, notes) + `brand.json` tokens and ask for a native .pptx with the same structure | `scripts/export_pptx.py <project>` (needs `pip install python-pptx`): image slides + speaker notes that open in PowerPoint/Keynote/Google Slides; text is not editable |
| Read existing decks / data room | a `pdf` skill, `pdftotext`/`pdftoppm`, a `docx`/`xlsx` skill | extract text + render pages to images to see the design | your native file reading; ask the founder to paste key content |
| Web pages your fetch can't read (X/Twitter, LinkedIn, Reddit, YouTube transcripts, GitHub) | `agent-reach` skill/CLI | `agent-reach read <url>`, `agent-reach <channel> search "<q>"`, which is read-only | skip, and note it in `sweep.md` |
| Deep market research | `deep-research` or similar | run it on the sweep questions in `market-sweep.md` and merge results into `research/sweep.md` | the sweep procedure here |
| Copy polish | `humanizer` or a style-guide skill | run it on headlines + notes only; re-check numbers afterwards | the copy rules in `narrative.md` |
| Design polish / UI critique | `frontend-design`, `impeccable`, `theme-factory` | ask for a critique of `contact-sheet.png` against `design-system.md`; apply changes via `brand.json` and the `css` key, not by editing the base stylesheet | the designer pass in `review.md` |
| Diagrams (architecture, data flow) | `excalidraw-diagram`, `visual-explainer`, mermaid tools | export SVG into `assets/` and place with `split` or `image` | hand-written inline SVG in an `html` block |
| Investor-persona panel | `synth-personas` CLI (needs an API key; costs money) | **ask first**: it sends deck content to an external API | the review panel in `review.md` |
| Imagery | an image-generation tool | atmosphere only (section dividers, title backgrounds); never as evidence; record in `assets/CREDITS.md` | photo-free layouts (the presets work without imagery) |
| Founder data from other skills | files such as `founder/facts.md`, `fundraise-prep` outputs | read them as inputs to `facts.md` | interview |
| Brand from Figma/Canva | design-tool connectors | export colours, fonts and logo into `brand.json` and `assets/` | `brand_from_url.py` + manual |

## Rules when composing
- The facts ledger stays the single source of truth. Anything another skill produces is checked against `facts.md`.
- Ask before sending confidential material to any external API or service that isn't ordinary web search.
- Don't let another skill restyle the deck outside the design system. Bring its output back through `deck.md` and `brand.json`.
