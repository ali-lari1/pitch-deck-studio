#!/usr/bin/env python3
"""Scaffold a deck project: deck.md (outline for the chosen arc), brand.json, facts.md, brief.md, assets/.

Usage:
    python3 init_project.py <project_dir> --name "Acme" [--preset swiss] [--stage seed]
                            [--vertical b2b-saas] [--arc A] [--force]

Arcs (see references/narrative.md): A traction-led, B insight-led, C demo-led, D science/tech-led,
E mission, F consumer/marketplace loop, G roadshow/IPO. Without --arc, one is chosen from the vertical and stage.
Existing files are never overwritten unless --force is passed.
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "..", "assets", "templates")

VERTICAL_DEFAULTS = {  # vertical -> (arc, preset)
    "ai-apps-agents": ("C", "mono"), "ai-infra-foundation-models": ("D", "terminal"), "b2b-saas": ("A", "swiss"),
    "devtools-open-source": ("C", "terminal"), "cybersecurity": ("A", "terminal"), "fintech": ("A", "ledger"),
    "crypto-web3": ("C", "terminal"), "digital-health": ("A", "lab"), "biotech-therapeutics": ("D", "lab"),
    "medtech-devices": ("D", "lab"), "climate-energy": ("D", "verdant"), "hardware-robotics": ("D", "cosmos"),
    "defense-space": ("E", "mission"), "deeptech": ("D", "cosmos"), "consumer-apps-social": ("F", "warm"),
    "marketplaces": ("F", "warm"), "ecommerce-d2c-cpg": ("F", "editorial"), "edtech": ("B", "warm"),
    "proptech-construction": ("A", "swiss"), "mobility-logistics": ("A", "swiss"), "gaming": ("C", "noir"),
    "food-agtech": ("D", "verdant"), "hr-legal-vertical-saas": ("A", "swiss"),
}

# (layout, kicker, headline hint, body hint)
S = {
    "title": ("title", "{round} · {year}", "{name}", "## [[one-line value proposition: what, for whom]]"),
    "metric": ("stats", "Traction", "[[Headline that states the single strongest proof]]",
               "[[value]] :: [[label]] :: [[context]]\n[[value]] :: [[label]] :: [[context]]\n[[value]] :: [[label]] :: [[context]]"),
    "problem": ("statement", "The problem", "[[Who suffers, how much, in one sentence with ==one highlighted number==]]",
                "[[One supporting sentence.]]"),
    "insight": ("statement", "The insight", "[[What you know that others don't]]", ""),
    "whynow": ("columns", "Why now", "[[What changed that makes this possible now]]",
               "### [[Change 1]]\n[[One sentence, dated]]\n\n|||\n\n### [[Change 2]]\n[[One sentence]]\n\n|||\n\n### [[Change 3]]\n[[One sentence]]"),
    "product": ("screens", "The product", "[[What the product does, as an outcome]]",
                "- [[Benefit 1]]\n- [[Benefit 2]]\n- [[Benefit 3]]\n\n![Product screenshot](assets/[[screenshot.png]])"),
    "how": ("steps", "How it works", "[[It works in N steps, with the time or cost per step]]",
            "[[Step]] :: [[What happens]]\n[[Step]] :: [[What happens]]\n[[Step]] :: [[What happens]]"),
    "traction": ("chart", "Traction", "[[Headline that states the growth rate]]",
                 "```chart type=bar prefix=$ suffix=K highlight=last\n[[Q1]]: [[0]]\n[[Q2]]: [[0]]\n[[Q3]]: [[0]]\n```"),
    "signal": ("stats", "Early signal", "[[The demand is already here]]",
               "[[1,200]] :: [[Waitlist / LOIs / pilots]] :: [[context]]\n[[3]] :: [[Design partners]] :: [[names if allowed]]\n[[40%]] :: [[Week-4 retention]] :: [[cohort, n]]"),
    "units": ("stats", "Unit economics", "[[Every customer pays back in N months]]",
              "[[$]] :: [[ACV]]\n[[x]] :: [[LTV/CAC]]\n[[%]] :: [[Gross margin]]\n[[mo]] :: [[CAC payback]]\n[[%]] :: [[Net revenue retention]]\n[[%]] :: [[Logo churn]]"),
    "market": ("market", "Market", "[[A $X beachhead inside a $Y market]]",
               "[[$Y]] :: [[Total]]\n[[$X]] :: [[Serviceable]]\n[[$Z]] :: [[Target in 5 years]]\n\n**Bottom-up:** [[units]] × [[price]] × [[frequency]]."),
    "model": ("columns", "Business model", "[[Who pays, how much, how often]]",
              "### Pricing\n[[...]]\n\n|||\n\n### Margin\n[[...]]\n\n|||\n\n### Expansion\n[[...]]"),
    "competition": ("matrix", "Competition", "[[Why we win, in one line]]",
                    "{name} :: 0.85 :: 0.85\n[[Competitor A]] :: 0.3 :: 0.6\n[[Competitor B]] :: 0.7 :: 0.3\n[[Competitor C]] :: 0.2 :: 0.2"),
    "gtm": ("steps", "Go-to-market", "[[How the first N customers came, and how the next 1,000 will]]",
            "[[Channel 1]] :: [[proof it works, cost]]\n[[Channel 2]] :: [[...]]\n[[Channel 3]] :: [[...]]"),
    "loop": ("steps", "The growth loop", "[[Every user brings the next one]]",
             "[[Action]] :: [[...]]\n[[Action]] :: [[...]]\n[[Action]] :: [[...]]\n[[Action]] :: [[...]]"),
    "evidence": ("chart", "Evidence", "[[The result, vs the state of the art]]",
                 "```chart type=hbar highlight=first suffix=x\n{name}: [[0]]\n[[State of the art]]: [[0]]\n[[Baseline]]: [[0]]\n```"),
    "derisk": ("timeline", "De-risking plan", "[[Each milestone removes one risk]]",
               "[[Date]] :: [[Milestone]] :: [[Risk removed]]\n[[Date]] :: [[Milestone]] :: [[Risk removed]]\n[[Date]] :: [[Milestone]] :: [[Risk removed]]"),
    "moat": ("columns", "Moat", "[[Why this gets harder to copy over time]]",
             "### [[IP / data / network]]\n[[...]]\n\n|||\n\n### [[Cost / speed]]\n[[...]]"),
    "nof1": ("stats", "At a glance", "[[N of 1: the numbers that set the scale]]",
             "[[value]] :: [[label]]\n[[value]] :: [[label]]\n[[value]] :: [[label]]\n[[value]] :: [[label]]\n[[value]] :: [[label]]\n[[value]] :: [[label]]"),
    "mission": ("statement", "Mission", "[[The mission in one sentence]]", ""),
    "milestones": ("timeline", "Milestones", "[[What we've delivered, and what's next]]",
                   "[[Date]] :: [[Delivered]] :: [[...]]\n[[Date]] :: [[Delivered]] :: [[...]]\n[[Date]] :: [[Next]] :: [[...]]\n[[Date]] :: [[Next]] :: [[...]]"),
    "team": ("team", "Team", "[[Why this team wins this market]]",
             "[[Name]] :: [[Role]] :: [[The one credential that matters]]\n[[Name]] :: [[Role]] :: [[The one credential that matters]]\n[[Name]] :: [[Role]] :: [[The one credential that matters]]"),
    "roadmap": ("timeline", "Roadmap", "[[What this round buys: milestone by date]]",
                "[[Q]] :: [[Milestone]] :: [[...]]\n[[Q]] :: [[Milestone]] :: [[...]]\n[[Q]] :: [[Milestone]] :: [[...]]"),
    "ask": ("ask", "The ask", "[[Raising $X to reach milestone Y]]",
            "[[$X]]\n\n[[40%]] :: [[Use]] :: [[what it buys]]\n[[35%]] :: [[Use]] :: [[what it buys]]\n[[25%]] :: [[Use]] :: [[what it buys]]\n\n### Milestones this round reaches\n\n- [[...]]\n- [[...]]"),
    "closing": ("closing", "", "{name}", "## [[mission line]]\n\n[[email]]\n[[website]]"),
    "appendix": ("section", "", "Appendix", ""),
    "disclaimer": ("default", "Disclaimer", "Forward-looking statements",
                   "[[Counsel-approved disclaimer text. This is not legal advice.]]"),
    "offering": ("table", "Offering summary", "[[Offering summary]]",
                 "| Term | Detail |\n|---|---|\n| Issuer | [[...]] |\n| Offering size | [[...]] |\n| Use of proceeds | [[...]] |"),
    "financials": ("chart", "Financials", "[[Revenue grew X% while margins expanded]]",
                   "```chart type=bar prefix=$ suffix=B highlight=last\n[[2024]]: [[0]]\n[[2025]]: [[0]]\n```"),
    "segments": ("section", "", "[[Our first segment]]", ""),
}

ARCS = {
    "A": ["title", "metric", "problem", "product", "how", "whynow", "traction", "units", "market", "competition", "gtm", "team", "roadmap", "ask", "closing", "appendix"],
    "B": ["title", "problem", "insight", "whynow", "product", "signal", "market", "model", "competition", "team", "ask", "closing", "appendix"],
    "C": ["title", "product", "metric", "problem", "how", "whynow", "market", "model", "moat", "team", "ask", "closing", "appendix"],
    "D": ["title", "evidence", "problem", "how", "derisk", "market", "model", "moat", "team", "ask", "closing", "appendix"],
    "E": ["title", "mission", "nof1", "problem", "how", "market", "milestones", "segments", "traction", "team", "ask", "closing", "appendix"],
    "F": ["title", "problem", "product", "loop", "traction", "units", "market", "competition", "team", "ask", "closing", "appendix"],
    "G": ["title", "disclaimer", "offering", "mission", "nof1", "how", "market", "milestones", "segments", "traction", "financials", "roadmap", "closing", "appendix"],
}

STAGE_SLIDES = {"pre-seed": "8-11", "seed": "10-13", "series-a": "12-15", "series-b": "14-20", "growth": "14-20", "ipo": "30-60"}


def slide(key, ctx):
    layout, kicker, head, body = S[key]
    lines = ["@layout " + layout]
    if kicker:
        lines.append("@kicker " + kicker.format(**ctx))
    if layout in ("stats", "chart", "market") and key not in ("nof1",):
        lines.append("@source [[source, date]]")
    if layout == "matrix":
        lines += ["@x [[Axis low]]|[[Axis high]]", "@y [[Axis low]]|[[Axis high]]", "@us " + ctx["name"]]
    if key == "appendix" or key == "segments":
        lines.append("@bg accent" if key == "appendix" else "@invert")
    lines.append("")
    lines.append("# " + head.format(**ctx))
    if body:
        lines.append("")
        lines.append(body.format(**ctx))
    lines += ["", "???", "[[Speaker notes: 2-5 sentences a cold reader would understand.]]"]
    return "\n".join(lines)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = os.path.abspath(argv[1])
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    name = opt("--name", "Company")
    vertical = opt("--vertical", "b2b-saas")
    stage = (opt("--stage", "seed") or "seed").lower().replace(" ", "-")
    arc_d, preset_d = VERTICAL_DEFAULTS.get(vertical, ("A", "swiss"))
    if stage in ("pre-seed",) and arc_d == "A":
        arc_d = "B"
    if stage == "ipo":
        arc_d = "G"
    arc = (opt("--arc", arc_d) or arc_d).upper()
    preset = opt("--preset", preset_d)
    force = "--force" in argv
    os.makedirs(os.path.join(root, "assets"), exist_ok=True)
    os.makedirs(os.path.join(root, "research"), exist_ok=True)
    ctx = {"name": name, "round": stage.replace("-", " ").title(), "year": "[[year]]"}

    def write(fname, text):
        path = os.path.join(root, fname)
        if os.path.exists(path) and not force:
            print("kept   " + path)
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote  " + path)

    front = "---\ntitle: %s — %s\ncompany: %s\nconfidential: Confidential\ntarget_slides: %s\npurpose: fundraise\n---\n\n" % (
        name, ctx["round"], name, STAGE_SLIDES.get(stage, "10-14"))
    keys = ARCS.get(arc, ARCS["A"])
    write("deck.md", front + "\n\n---\n\n".join(slide(k, ctx) for k in keys) + "\n")
    write("brand.json", json.dumps({"name": name, "preset": preset}, indent=2) + "\n")
    for t in ("facts.md", "brief.md"):
        src = os.path.join(TPL, t)
        with open(src, encoding="utf-8") as f:
            write(t, f.read().replace("{name}", name).replace("{arc}", arc).replace("{preset}", preset)
                  .replace("{stage}", stage).replace("{vertical}", vertical))
    print("\narc %s, preset %s, %d slides scaffolded. Every [[placeholder]] must be replaced or listed in facts.md." % (
        arc, preset, len(keys)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
