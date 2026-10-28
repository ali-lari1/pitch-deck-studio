#!/usr/bin/env python3
"""Maintainer tool: regenerate the index part of references/deck-library.md from data/decks.json."""
import collections
import json
import os
import re
import statistics

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "pitch-deck-studio")
data = json.load(open(os.path.join(ROOT, "data", "decks.json"), encoding="utf-8"))
decks = data["decks"]


def second_move(seq):
    seq = [x for x in seq if not re.match(r"^\(?slide \d+\)?$|^title$", x.strip().lower())]
    if len(seq) < 2:
        return None
    s = seq[1].lower()
    for key, words in [("summary / proof up front (traction, at-a-glance, key numbers)", ["traction", "glance", "summary", "snapshot", "highlights", "tl;dr", "overview", "key numbers", "hook", "metric", "growth", "revenue", "arr"]),
                       ("team / pedigree", ["team", "founder", "pedigree"]),
                       ("problem / stat", ["problem", "pain", "challenge", "issue", "threat", "hard", "suck", "stat:", "broken", "it takes"]),
                       ("mission / vision / insight", ["mission", "vision", "insight", "opening statement", "quote", "definition", "opportunity", "why:", "future", "tomorrow", "will transform", "everyone can"]),
                       ("product / demo", ["product", "demo", "solution", "how it works", "platform", "photo", "studio", "autopilot"])]:
        if any(w in s for w in words):
            return key
    return "other (market, context, comparison)"


def money(v):
    if not isinstance(v, (int, float)):
        return "n/a"
    return "$%.0fM" % (v / 1e6) if v >= 1e6 else "$%.0fK" % (v / 1e3)


sc = [d["slide_count"] for d in decks if isinstance(d["slide_count"], int)]
q = sorted(sc)
moves = collections.Counter(filter(None, (second_move(d["slide_sequence"]) for d in decks)))
dense = collections.Counter((d.get("design") or {}).get("density", "unknown").split(" ")[0].split("-")[0] for d in decks)
sdt = sum(1 for d in decks if d["show_dont_tell"])
lines = []
lines.append("## The numbers (%d decks, rounds closed 2022-2026)\n" % len(decks))
lines.append("- Slide count: median **%d**, middle half %d-%d, range %d-%d (n=%d with known counts)." % (
    statistics.median(sc), q[len(q) // 4], q[3 * len(q) // 4], q[0], q[-1], len(sc)))
lines.append("- Use at least one show-don't-tell device (screenshots, product photos, charts, logo walls, before/after): **%d of %d**." % (sdt, len(decks)))
tot = sum(moves.values())
lines.append("- What slide 2 does (n=%d with a known slide 2): %s." % (tot, ", ".join("%s %d%%" % (k, round(100 * v / tot)) for k, v in moves.most_common())))
st = collections.Counter(d["stage"] for d in decks)
lines.append("- Stage mix: %s." % ", ".join("%s %d" % (k, v) for k, v in st.most_common()))
yr = collections.Counter(d["year"] for d in decks)
lines.append("- Year mix: %s." % ", ".join("%s: %d" % (k, v) for k, v in sorted(yr.items())))
lines.append("")
lines.append("## Index by playbook\n")
lines.append("Query it with `python3 scripts/find_decks.py --vertical <playbook or keyword> [--stage seed] [--show-dont-tell] [--min-design 4]`. "
             "Each entry in `data/decks.json` carries the slide sequence, narrative pattern, design notes, standout moves, weaknesses, sources and caveats.\n")
by = collections.defaultdict(list)
for d in decks:
    by[d["playbook"]].append(d)
for pb in sorted(by):
    lines.append("### %s (%d)\n" % (pb, len(by[pb])))
    lines.append("| Company | Round · year | Raised | Slides | Pattern | Deck |")
    lines.append("|---|---|---|---|---|---|")
    for d in sorted(by[pb], key=lambda x: (-(x["year"] or 0), x["company"])):
        pat = re.sub(r"\s+", " ", (d.get("narrative_pattern") or "")).replace("|", "/")
        if len(pat) > 90:
            pat = pat[:88].rsplit(" ", 1)[0] + "…"
        lines.append("| %s | %s · %s | %s | %s | %s | [link](%s) |" % (
            d["company"], d["round"], d["year"], money(d["amount_usd"]), d["slide_count"] or "?", pat, d["deck_url"]))
    lines.append("")
gen = "\n".join(lines)
path = os.path.join(ROOT, "references", "deck-library.md")
head = open(path, encoding="utf-8").read().split("<!-- GENERATED -->")[0] if os.path.exists(path) else ""
open(path, "w", encoding="utf-8").write(head + "<!-- GENERATED -->\n" + gen + "\n")
print("wrote", path)
