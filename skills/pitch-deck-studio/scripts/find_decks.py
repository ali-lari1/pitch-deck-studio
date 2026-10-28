#!/usr/bin/env python3
"""Find comparable decks in the bundled library (data/decks.json).

Usage:
    python3 find_decks.py [--vertical KEYWORD] [--stage seed] [--model marketplace] [--show-dont-tell]
                          [--min-design 4] [--since 2023] [--limit 8] [--full] [--json]

--vertical matches the playbook slug, vertical, sub-vertical or one-liner (case-insensitive; use | for OR,
e.g. "fintech|insurance"). --stage accepts pre-seed, seed, series-a, series-b, growth (and neighbours with --near).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGES = ["pre-seed", "seed", "series-a", "series-b", "growth"]


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    data = json.load(open(os.path.join(HERE, "..", "data", "decks.json"), encoding="utf-8"))["decks"]
    v, stage, model = opt("--vertical"), opt("--stage"), opt("--model")
    since, min_d, limit = int(opt("--since", 0)), int(opt("--min-design", 0)), int(opt("--limit", 8))
    res = []
    for d in data:
        hay = " ".join(str(d.get(k) or "") for k in ("playbook", "vertical", "sub_vertical", "one_liner", "company")).lower()
        if v and not any(t.strip().lower() in hay for t in v.split("|")):
            continue
        if stage:
            ok = [stage]
            if "--near" in argv and stage in STAGES:
                i = STAGES.index(stage)
                ok = STAGES[max(0, i - 1): i + 2]
            if d["stage"] not in ok:
                continue
        if model and model.lower() not in str(d.get("business_model", "")).lower():
            continue
        if "--show-dont-tell" in argv and not d.get("show_dont_tell"):
            continue
        if (d.get("year") or 0) < since:
            continue
        dq = d.get("design_quality")
        if min_d and not (isinstance(dq, int) and dq >= min_d):
            continue
        res.append(d)
    res.sort(key=lambda d: (-(d["design_quality"] if isinstance(d["design_quality"], int) else 0), -(d["year"] or 0)))
    res = res[:limit]
    if "--json" in argv:
        print(json.dumps(res, indent=1, ensure_ascii=False))
        return 0
    if not res:
        print("no matches - widen with --near, drop --stage, or try a broader keyword")
        return 0
    for d in res:
        amt = d["amount_usd"]
        amt = ("$%.0fM" % (amt / 1e6)) if isinstance(amt, (int, float)) and amt >= 1e6 else "n/a"
        print("■ %s (%s, %s %s, %s) design %s/5 · %s slides" % (d["company"], d["playbook"], d["round"], d["year"], amt,
                                                            d["design_quality"], d["slide_count"] or "?"))
        print("  %s" % (d.get("one_liner") or ""))
        print("  pattern: %s" % (d.get("narrative_pattern") or ""))
        if d.get("show_dont_tell_note"):
            print("  show-don't-tell: %s" % d["show_dont_tell_note"])
        moves = d.get("standout_moves") or []
        if moves:
            print("  standout: " + " / ".join(m if isinstance(m, str) else str(m) for m in moves[:3]))
        if "--full" in argv:
            print("  sequence: " + " → ".join(d.get("slide_sequence") or []))
            print("  design: %s" % json.dumps(d.get("design"), ensure_ascii=False))
            print("  weaknesses: %s" % "; ".join(str(w) for w in (d.get("weaknesses") or [])))
        print("  deck: %s" % d["deck_url"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
