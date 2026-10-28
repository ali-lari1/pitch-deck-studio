#!/usr/bin/env python3
"""Build a pitch deck: deck.md + brand.json  ->  deck.html (single file).

Usage:
    python3 build.py <project_dir> [--embed] [--out deck.html] [--preset NAME] [--quiet] [--json] [--outline]

--outline prints a markdown table of slides (layout, headline, source, placeholder count) to paste into brief.md.

Standard library only (Python 3.8+). The output is one HTML file that
presents in any browser (arrows / space / click), prints to a 16:9 PDF,
and has overview (O), speaker notes (N), reader mode (R) and fullscreen (F).

The deck.md syntax is documented in references/deck-format.md.
"""
import base64
import html
import json
import math
import mimetypes
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

LAYOUTS = {
    "title", "statement", "section", "default", "split", "image", "stats",
    "chart", "columns", "logos", "team", "timeline", "table", "quote",
    "market", "ask", "matrix", "screens", "steps", "html", "closing",
}

WORD_LIMIT = {  # on-slide words before the linter complains
    "title": 25, "statement": 30, "section": 20, "image": 30, "quote": 60,
    "default": 60, "split": 60, "columns": 80, "stats": 70, "chart": 50,
    "table": 120, "team": 90, "timeline": 80, "market": 60, "ask": 70,
    "matrix": 50, "logos": 30, "screens": 40, "steps": 70, "closing": 30,
    "html": 9999,
}


# ----------------------------------------------------------------- helpers

def esc(s):
    return html.escape(str(s), quote=True)


def load_json(path, default=None):
    if not path or not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def deep_merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        elif v not in (None, ""):
            out[k] = v
    return out


def inline(text):
    """Inline markdown: **bold**, *em*, `code`, ==accent==, [link](url), <br>."""
    t = esc(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"==([^=]+)==", r'<span class="hl">\1</span>', t)
    t = re.sub(r"~~([^~]+)~~", r"<s>\1</s>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = t.replace("&lt;br&gt;", "<br>").replace(" // ", "<br>")
    return t


def plain_words(text):
    t = re.sub(r"[#>*=`_\[\]()|:!-]", " ", text)
    return len([w for w in t.split() if any(c.isalnum() for c in w)])


class Resolver:
    """Resolves image paths relative to the project; optionally embeds them."""

    def __init__(self, root, embed):
        self.root, self.embed, self.missing = root, embed, []

    def __call__(self, src):
        if re.match(r"^(https?:|data:)", src):
            return src
        path = os.path.normpath(os.path.join(self.root, src))
        if not os.path.exists(path):
            self.missing.append(src)
            return src
        if not self.embed:
            return src
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


# ------------------------------------------------------------------ parsing

def split_front_matter(src):
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", src, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
        src = src[m.end():]
    return meta, src


def split_slides(body):
    slides, cur, fence = [], [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        if not fence and line.strip() == "---":
            slides.append("\n".join(cur))
            cur = []
        else:
            cur.append(line)
    slides.append("\n".join(cur))
    return [s for s in slides if s.strip()]


def parse_slide(text):
    """Return dict(directives, notes, blocks)."""
    notes = ""
    if re.search(r"^\?\?\?\s*$", text, re.M):
        text, notes = re.split(r"^\?\?\?\s*$", text, maxsplit=1, flags=re.M)
    lines = text.strip("\n").splitlines()
    d = {}
    while lines and (lines[0].startswith("@") or not lines[0].strip()):
        line = lines.pop(0).strip()
        if not line:
            continue
        key, _, val = line[1:].partition(" ")
        d[key.strip().lower()] = val.strip() or "true"
    blocks = parse_blocks(lines)
    return {"d": d, "notes": notes.strip(), "blocks": blocks, "raw": "\n".join(lines)}


IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")


def parse_blocks(lines):
    """Flat block list. Types: h1 h2 h3 p ul ol quote cite img item chart table col code html."""
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            info = s[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            kind, _, opts = info.partition(" ")
            if kind in ("chart", "html"):
                blocks.append({"t": kind, "opts": parse_opts(opts), "body": "\n".join(body)})
            else:
                blocks.append({"t": "code", "body": "\n".join(body)})
            continue
        if s == "|||":
            blocks.append({"t": "col"})
        elif s.startswith("### "):
            blocks.append({"t": "h3", "v": s[4:]})
        elif s.startswith("## "):
            blocks.append({"t": "h2", "v": s[3:]})
        elif s.startswith("# "):
            blocks.append({"t": "h1", "v": s[2:]})
        elif s.startswith("> "):
            v = s[2:]
            if re.match(r"^(—|--|-)\s", v):
                blocks.append({"t": "cite", "v": re.sub(r"^(—|--|-)\s*", "", v)})
            else:
                if blocks and blocks[-1]["t"] == "quote":
                    blocks[-1]["v"] += " " + v
                else:
                    blocks.append({"t": "quote", "v": v})
        elif s.startswith("|") and s.endswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c) for c in row if c):
                    rows.append(row)
                i += 1
            blocks.append({"t": "table", "rows": rows})
            continue
        elif re.match(r"^[-*] ", s):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]))
                i += 1
            blocks.append({"t": "ul", "items": items})
            continue
        elif re.match(r"^\d+[.)] ", s):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)] ", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)] ", "", lines[i]))
                i += 1
            blocks.append({"t": "ol", "items": items})
            continue
        elif " :: " in s or s.endswith(" ::"):
            blocks.append({"t": "item", "f": [p.strip() for p in s.split("::")]})
        elif IMG_RE.fullmatch(s) or (IMG_RE.match(s) and not IMG_RE.sub("", s).strip()):
            for m in IMG_RE.finditer(s):
                blocks.append({"t": "img", "alt": m.group(1), "src": m.group(2), "cap": m.group(3) or ""})
        else:
            if blocks and blocks[-1]["t"] == "p" and lines[i - 1].strip():
                blocks[-1]["v"] += " " + s
            else:
                blocks.append({"t": "p", "v": s})
        i += 1
    # attach an image directly preceding an item to that item (team photos, logos with captions)
    out = []
    for b in blocks:
        if b["t"] == "item" and out and out[-1]["t"] == "img" and not out[-1].get("_used"):
            b["img"] = out.pop()
        out.append(b)
    return out


def parse_opts(s):
    opts = {}
    for m in re.finditer(r'(\w[\w-]*)=("([^"]*)"|(\S+))', s):
        opts[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    return opts


# ------------------------------------------------------------------- charts

def num(s):
    s = str(s).strip().replace(",", "")
    m = re.search(r"-?\d+(\.\d+)?", s)
    return float(m.group(0)) if m else 0.0


def fmt(v, o):
    dec = int(o.get("decimals", "1" if abs(v) < 10 and v != int(v) else "0"))
    s = ("{:,.%df}" % dec).format(v)
    return "%s%s%s" % (o.get("prefix", ""), s, o.get("suffix", o.get("unit", "")))


def parse_series(body):
    rows = []
    for line in body.splitlines():
        if ":" not in line or not line.strip():
            continue
        k, v = line.rsplit(":", 1)
        rows.append((k.strip(), [num(x) for x in v.split(",")]))
    return rows


def chart_svg(opts, body):
    kind = opts.get("type", "bar")
    rows = parse_series(body)
    if not rows:
        return '<div class="chart-empty">chart: no data</div>'
    fn = {"bar": svg_bar, "hbar": svg_hbar, "line": svg_line, "area": svg_line,
          "donut": svg_donut, "stack": svg_bar}.get(kind, svg_bar)
    svg = fn(rows, opts, kind)
    cap = opts.get("caption", "")
    src = opts.get("source", "")
    extra = ""
    if cap:
        extra += '<div class="chart-cap">%s</div>' % inline(cap)
    return '<figure class="chart chart-%s">%s%s</figure>' % (esc(kind), svg, extra) + (
        '<div class="src">Source: %s</div>' % inline(src) if src else "")


def hl_index(opts, rows):
    h = opts.get("highlight", "last")
    if h == "none":
        return set()
    if h == "all":
        return set(range(len(rows)))
    if h == "last":
        return {len(rows) - 1}
    if h == "first":
        return {0}
    keys = [r[0] for r in rows]
    return {keys.index(x) for x in h.split("|") if x in keys}


def svg_bar(rows, o, kind):
    W, H, pad_b, pad_t = 1000, 560, 64, 70
    series = o.get("series", "").split("|") if o.get("series") else []
    stacked = kind == "stack" or len(rows[0][1]) > 1
    totals = [sum(v) if stacked else v[0] for _, v in rows]
    mx = max(totals + [0.0001])
    n = len(rows)
    gap = W / n
    bw = min(gap * 0.56, 150)
    hl = hl_index(o, rows)
    shades = ["var(--accent)", "color-mix(in srgb,var(--accent) 55%,var(--bg))",
              "color-mix(in srgb,var(--accent) 30%,var(--bg))", "var(--muted)"]
    parts = ['<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    parts.append('<line x1="0" y1="%d" x2="%d" y2="%d" class="axis"/>' % (H - pad_b, W, H - pad_b))
    for i, (k, vals) in enumerate(rows):
        x = gap * i + (gap - bw) / 2
        y0 = H - pad_b
        if stacked:
            for j, v in enumerate(vals):
                h = (H - pad_b - pad_t) * v / mx
                parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" style="fill:%s"/>' % (
                    x, y0 - h, bw, h, shades[j % len(shades)]))
                y0 -= h
        else:
            v = vals[0]
            h = (H - pad_b - pad_t) * v / mx
            cls = "bar hl" if i in hl else "bar"
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s"/>' % (
                x, y0 - h, bw, h, cls))
            y0 -= h
        if o.get("labels", "on") != "off":
            parts.append('<text x="%.1f" y="%.1f" class="val%s" text-anchor="middle">%s</text>' % (
                x + bw / 2, y0 - 16, " hl" if i in hl else "", esc(fmt(totals[i], o))))
        parts.append('<text x="%.1f" y="%d" class="cat" text-anchor="middle">%s</text>' % (
            x + bw / 2, H - pad_b + 40, esc(k)))
    parts.append("</svg>")
    legend = ""
    if stacked and series:
        legend = '<div class="legend">%s</div>' % "".join(
            '<span><i style="background:%s"></i>%s</span>' % (shades[j % len(shades)], esc(s))
            for j, s in enumerate(series))
    return "".join(parts) + legend


def svg_hbar(rows, o, kind):
    W = 1000
    rh = 64
    H = rh * len(rows) + 10
    mx = max([v[0] for _, v in rows] + [0.0001])
    hl = hl_index(o, rows)
    lw = 300
    parts = ['<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    for i, (k, v) in enumerate(rows):
        y = i * rh + 8
        w = (W - lw - 160) * v[0] / mx
        cls = "bar hl" if i in hl else "bar"
        parts.append('<text x="%d" y="%.1f" class="cat" text-anchor="end">%s</text>' % (lw - 20, y + rh / 2 + 4, esc(k)))
        parts.append('<rect x="%d" y="%.1f" width="%.1f" height="%.1f" class="%s"/>' % (lw, y + 8, w, rh - 22, cls))
        parts.append('<text x="%.1f" y="%.1f" class="val%s">%s</text>' % (
            lw + w + 14, y + rh / 2 + 4, " hl" if i in hl else "", esc(fmt(v[0], o))))
    parts.append("</svg>")
    return "".join(parts)


def svg_line(rows, o, kind):
    W, H, pb, pt, pl, pr = 1000, 560, 64, 60, 20, 120
    vals = [v[0] for _, v in rows]
    mx, mn = max(vals), min(0, min(vals))
    rng = (mx - mn) or 1
    n = len(rows)
    pts = []
    for i, v in enumerate(vals):
        x = pl + (W - pl - pr) * (i / max(n - 1, 1))
        y = H - pb - (H - pb - pt) * (v - mn) / rng
        pts.append((x, y))
    path = " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % p for i, p in enumerate(pts))
    parts = ['<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    parts.append('<line x1="0" y1="%d" x2="%d" y2="%d" class="axis"/>' % (H - pb, W, H - pb))
    if kind == "area" or o.get("fill") == "on":
        parts.append('<path d="%s L%.1f %d L%.1f %d Z" class="area"/>' % (path, pts[-1][0], H - pb, pts[0][0], H - pb))
    parts.append('<path d="%s" class="line"/>' % path)
    step = max(1, n // 8)
    for i, (k, _) in enumerate(rows):
        if i % step == 0 or i == n - 1:
            parts.append('<text x="%.1f" y="%d" class="cat" text-anchor="middle">%s</text>' % (pts[i][0], H - pb + 40, esc(k)))
    for i in sorted(hl_index(o, rows) | ({0} if o.get("labels") == "ends" else set())):
        x, y = pts[i]
        parts.append('<circle cx="%.1f" cy="%.1f" r="9" class="dot"/>' % (x, y))
        parts.append('<text x="%.1f" y="%.1f" class="val hl" text-anchor="middle">%s</text>' % (x, y - 24, esc(fmt(vals[i], o))))
    parts.append("</svg>")
    return "".join(parts)


def svg_donut(rows, o, kind):
    W, H, cx, cy, r, sw = 1000, 560, 280, 280, 210, 70
    tot = sum(v[0] for _, v in rows) or 1
    circ = 2 * math.pi * r
    mixes = [100, 70, 48, 32, 20, 12]
    parts = ['<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    off = 0.0
    for i, (k, v) in enumerate(rows):
        frac = v[0] / tot
        col = "color-mix(in srgb,var(--accent) %d%%,var(--bg))" % mixes[i % len(mixes)]
        parts.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke-width="%d" style="stroke:%s" '
                     'stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f" transform="rotate(-90 %d %d)"/>' % (
                         cx, cy, r, sw, col, max(frac * circ - 4, 0), circ, -off, cx, cy))
        off += frac * circ
        ly = 110 + i * 70
        parts.append('<rect x="600" y="%d" width="22" height="22" style="fill:%s"/>' % (ly - 18, col))
        parts.append('<text x="640" y="%d" class="cat" style="text-anchor:start">%s</text>' % (ly, esc(k)))
        parts.append('<text x="990" y="%d" class="val" text-anchor="end">%s</text>' % (
            ly, esc(fmt(v[0], o) if o.get("pct") != "on" else "%d%%" % round(100 * frac))))
    if o.get("center"):
        parts.append('<text x="%d" y="%d" class="donut-center" text-anchor="middle">%s</text>' % (cx, cy + 18, esc(o["center"])))
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------- rendering

def render_block(b, img):
    t = b["t"]
    if t == "h3":
        return '<h3>%s</h3>' % inline(b["v"])
    if t == "p":
        return '<p>%s</p>' % inline(b["v"])
    if t == "ul":
        return "<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in b["items"])
    if t == "ol":
        return "<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in b["items"])
    if t == "quote":
        return '<blockquote>%s</blockquote>' % inline(b["v"])
    if t == "cite":
        return '<div class="cite">%s</div>' % inline(b["v"])
    if t == "img":
        cap = '<figcaption>%s</figcaption>' % inline(b["cap"]) if b.get("cap") else ""
        return '<figure class="img"><img src="%s" alt="%s">%s</figure>' % (esc(img(b["src"])), esc(b["alt"]), cap)
    if t == "chart":
        return chart_svg(b["opts"], b["body"])
    if t == "html":
        return b["body"]
    if t == "code":
        return "<pre><code>%s</code></pre>" % esc(b["body"])
    if t == "table":
        return render_table(b["rows"])
    if t == "item":
        return render_item(b, img, "item")
    return ""


def cell(c):
    c2 = c.strip()
    if c2 in ("✓", "y", "yes", "Yes", "✔"):
        return '<span class="yes">●</span>'
    if c2 in ("✗", "n", "no", "No", "✘", "x"):
        return '<span class="no">○</span>'
    if c2 in ("~", "partial", "◐"):
        return '<span class="part">◐</span>'
    return inline(c2)


def render_table(rows):
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    h = "".join("<th>%s</th>" % inline(c) for c in head)
    trs = []
    for r in body:
        us = r and "==" in r[0]
        tds = "".join("<td>%s</td>" % cell(c.replace("==", "")) for c in r)
        trs.append('<tr%s>%s</tr>' % (' class="us"' if us else "", tds))
    return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, "".join(trs))


def render_item(b, img, kind):
    f = b["f"] + ["", "", ""]
    pic = ""
    if b.get("img"):
        pic = '<img src="%s" alt="%s">' % (esc(img(b["img"]["src"])), esc(b["img"]["alt"]))
    elif kind == "team" and f[0] and "[[" not in f[0]:
        initials = "".join(w[0] for w in re.findall(r"[A-Za-z\u00C0-\u024F]+", f[0])[:2]).upper()
        pic = '<div class="ava">%s</div>' % esc(initials)
    return ('<div class="it">%s<div class="a">%s</div><div class="b">%s</div>%s</div>' % (
        pic, inline(f[0]), inline(f[1]), '<div class="c">%s</div>' % inline(f[2]) if f[2] else ""))


def header_and_body(blocks):
    head, body, started = [], [], False
    for b in blocks:
        if not started and b["t"] in ("h1", "h2"):
            head.append(b)
        else:
            started = True
            body.append(b)
    return head, body


def render_head(head, d):
    out = []
    if d.get("kicker"):
        out.append('<div class="kicker">%s</div>' % inline(d["kicker"]))
    for b in head:
        tag = "h1" if b["t"] == "h1" else "h2"
        out.append("<%s>%s</%s>" % (tag, inline(b["v"]), tag))
    return '<header class="hd">%s</header>' % "".join(out) if out else ""


def columns(body):
    cols, cur = [], []
    for b in body:
        if b["t"] == "col":
            cols.append(cur)
            cur = []
        else:
            cur.append(b)
    cols.append(cur)
    return cols


def render_slide(sl, idx, total, meta, brand, img):
    d, blocks = sl["d"], sl["blocks"]
    layout = d.get("layout") or guess_layout(blocks)
    head, body = header_and_body(blocks)
    items = [b for b in body if b["t"] == "item"]
    imgs = [b for b in body if b["t"] == "img"]
    rest = [b for b in body if b["t"] not in ("item",)]
    R = lambda bs: "".join(render_block(b, img) for b in bs)
    inner = ""

    if layout == "html":
        inner = R(body)
    elif layout in ("title", "closing"):
        logo = brand.get("logo")
        lg = '<img class="logo" src="%s" alt="logo">' % esc(img(logo)) if logo and d.get("logo") != "off" else ""
        inner = '<div class="ttl">%s%s<div class="tb">%s</div></div>' % (
            lg, render_head(head, d), R([b for b in body if b["t"] != "img"]))
    elif layout in ("statement", "section"):
        inner = '<div class="center">%s%s</div>' % (render_head(head, d), R(rest))
    elif layout == "image":
        inner = '<div class="over">%s%s</div>' % (render_head(head, d), R([b for b in rest if b["t"] != "img"]))
    elif layout in ("stats", "timeline", "team", "steps", "logos"):
        if layout == "logos" and not items:
            for b in [x for x in rest if x["t"] == "ul"]:
                items += [{"t": "item", "f": [n]} for n in b["items"]]
            rest = [x for x in rest if x["t"] != "ul"]
        grid_items = items
        if layout == "logos" and not items:
            grid = "".join('<div class="it"><img src="%s" alt="%s"></div>' % (esc(img(b["src"])), esc(b["alt"])) for b in imgs)
            rest = [b for b in rest if b["t"] != "img"]
        else:
            grid = "".join(render_item(b, img, layout) for b in grid_items)
        n = max(len(grid_items) or len(imgs), 1)
        cols = d.get("cols") or str(n if n <= 4 else (3 if n in (5, 6, 9) else 4))
        if layout == "timeline":
            cols = str(n)
        inner = '%s<div class="body">%s<div class="grid" style="--cols:%s">%s</div></div>' % (
            render_head(head, d), R([b for b in rest if b["t"] not in ("img",) or layout != "logos"]), cols, grid)
    elif layout == "matrix":
        inner = render_head(head, d) + render_matrix(items, d) + R([b for b in rest if b["t"] != "item"])
    elif layout in ("split", "screens", "market", "ask", "chart", "default", "columns", "table", "quote"):
        cols_ = columns(body)
        if len(cols_) > 1:
            inner = '%s<div class="cols" style="--cols:%d">%s</div>' % (
                render_head(head, d), len(cols_), "".join('<div class="col">%s</div>' % R(c) for c in cols_))
        elif layout in ("split", "screens") and (imgs or any(b["t"] == "chart" for b in body)):
            vis = [b for b in body if b["t"] in ("img", "chart")]
            txt = [b for b in body if b["t"] not in ("img", "chart")]
            frame = d.get("frame", "browser" if layout == "screens" else "none")
            vis_html = "".join(
                '<div class="frame frame-%s">%s</div>' % (frame, render_block(b, img)) if b["t"] == "img" else render_block(b, img)
                for b in vis)
            inner = '<div class="splitwrap%s"><div class="txt">%s%s</div><div class="vis">%s</div></div>' % (
                " flip" if d.get("flip") else "", render_head(head, d), R(txt), vis_html)
        elif layout == "market":
            inner = render_head(head, d) + render_market(items, rest, img)
        elif layout == "ask":
            inner = render_head(head, d) + render_ask(items, rest, img)
        else:
            inner = '%s<div class="body">%s</div>' % (render_head(head, d), R(body))
    else:
        inner = '%s<div class="body">%s</div>' % (render_head(head, d), R(body))

    bg = d.get("bg")
    style = []
    cls = ["slide", "l-" + layout]
    if bg and bg != "accent":
        if re.match(r"^(#|rgb|hsl|var\(|linear-gradient|radial-gradient)", bg):
            style.append("--slide-bg:%s" % bg)
        else:
            style.append("--bgimg:url('%s')" % img(bg))
            cls.append("has-bg")
    if d.get("dim"):
        style.append("--dim:%s" % d["dim"])
    if d.get("mode") == "invert" or "invert" in d:
        cls.append("mode-invert")
    if bg == "accent":
        cls.append("on-accent")
    if d.get("align") in ("center", "left", "bottom"):
        cls.append("al-" + d["align"])
    if d.get("class"):
        cls.extend(d["class"].split())
    if layout == "image" and imgs and not bg:
        style.append("--bgimg:url('%s')" % img(imgs[0]["src"]))
        cls.append("has-bg")

    foot = []
    if d.get("source"):
        foot.append('<div class="src">Source: %s</div>' % inline(d["source"]))
    if d.get("note"):
        foot.append('<div class="src">%s</div>' % inline(d["note"]))
    chrome = ""
    if layout not in ("title", "closing", "section") and meta.get("chrome", "on") != "off":
        mark = brand.get("logo_small") or brand.get("logo")
        mk = '<img src="%s" alt="">' % esc(img(mark)) if mark else '<span>%s</span>' % esc(brand.get("name", ""))
        conf = '<span class="conf">%s</span>' % esc(meta["confidential"]) if meta.get("confidential") else ""
        chrome = '<div class="chrome"><div class="mark">%s</div>%s<div class="pg">%d</div></div>' % (mk, conf, idx + 1)
    notes = '<aside class="notes">%s</aside>' % "".join(
        "<p>%s</p>" % inline(p) for p in re.split(r"\n\s*\n", sl["notes"]) if p.strip()) if sl["notes"] else ""
    return ('<section class="%s" style="%s" data-i="%d"><div class="in">%s</div>%s%s</section>%s' % (
        " ".join(cls), ";".join(style), idx, inner, "".join(foot), chrome, notes), layout)


def render_matrix(items, d):
    xa = (d.get("x") or "Low|High").split("|")
    ya = (d.get("y") or "Low|High").split("|")
    us = d.get("us", items[0]["f"][0] if items else "")
    dots = []
    for b in items:
        f = b["f"] + ["0.5", "0.5"]
        x, y = max(0.0, min(1.0, num(f[1]))), max(0.0, min(1.0, num(f[2])))
        dots.append('<div class="dot%s" style="left:%.1f%%;bottom:%.1f%%"><i></i><span>%s</span></div>' % (
            " us" if f[0] == us else "", x * 100, y * 100, inline(f[0])))
    return ('<div class="matrix"><div class="ax-x"><span>%s</span><span>%s</span></div>'
            '<div class="ax-y"><span>%s</span><span>%s</span></div><div class="plane">%s</div></div>') % (
        inline(xa[0]), inline(xa[-1]), inline(ya[0]), inline(ya[-1]), "".join(dots))


def render_market(items, rest, img):
    rings = []
    for i, b in enumerate(items[:3]):
        f = b["f"] + ["", ""]
        rings.append('<div class="ring r%d"><div class="a">%s</div><div class="b">%s</div><div class="c">%s</div></div>' % (
            i, inline(f[0]), inline(f[1]), inline(f[2])))
    side = "".join(render_block(b, img) for b in rest if b["t"] != "item")
    return '<div class="market"><div class="rings">%s</div><div class="mside">%s</div></div>' % ("".join(rings), side)


def render_ask(items, rest, img):
    big = [b for b in rest if b["t"] == "p"][:1]
    other = [b for b in rest if b not in big]
    amount = '<div class="amount">%s</div>' % inline(big[0]["v"]) if big else ""
    vals = [num(b["f"][0]) for b in items]
    pct = all("%" in b["f"][0] for b in items) and items
    mx = 100.0 if pct else (max(vals) if vals else 1) or 1
    rows = []
    for b, v in zip(items, vals):
        f = b["f"] + ["", ""]
        rows.append('<div class="it"><div class="a">%s</div><div class="b">%s</div>%s<div class="bar"><i style="width:%.1f%%"></i></div></div>' % (
            inline(f[0]), inline(f[1]), '<div class="c">%s</div>' % inline(f[2]) if f[2] else "", 100 * v / mx))
    return '<div class="askwrap"><div class="aleft">%s%s</div><div class="aright">%s</div></div>' % (
        amount, '<div class="uses">%s</div>' % "".join(rows) if rows else "", "".join(render_block(b, img) for b in other))


def guess_layout(blocks):
    ts = [b["t"] for b in blocks]
    if "chart" in ts:
        return "split" if any(t in ("p", "ul") for t in ts) and "img" not in ts else "chart"
    if ts.count("item") >= 2:
        return "stats"
    if "table" in ts:
        return "table"
    if "quote" in ts:
        return "quote"
    if "img" in ts and len(ts) <= 3:
        return "image" if "p" not in ts and "ul" not in ts else "split"
    if "img" in ts:
        return "split"
    if ts in (["h1"], ["h1", "p"], ["h2"], ["h1", "h2"]):
        return "statement"
    return "default"


# ------------------------------------------------------------------- theme

def resolve_brand(root, meta, force_preset=None):
    presets = load_json(os.path.join(ASSETS, "presets.json"), {})
    brand = load_json(os.path.join(root, meta.get("brand", "brand.json")), {}) or {}
    pname = force_preset or meta.get("preset") or brand.get("preset") or "swiss"
    if pname not in presets:
        print("warning: unknown preset %r, using swiss" % pname, file=sys.stderr)
        pname = "swiss"
    merged = deep_merge(presets[pname], brand)
    merged["preset"] = pname
    return merged


def theme_css(b):
    c, f = b.get("colors", {}), b.get("fonts", {})
    v = {
        "--bg": c.get("bg"), "--fg": c.get("fg"), "--muted": c.get("muted"),
        "--accent": c.get("accent"), "--accent-2": c.get("accent2", c.get("accent")),
        "--surface": c.get("surface"), "--line": c.get("line"),
        "--inv-bg": c.get("inv_bg", c.get("fg")), "--inv-fg": c.get("inv_fg", c.get("bg")),
        "--f-display": "'%s', %s" % (f.get("display"), f.get("display_fallback", "system-ui, sans-serif")),
        "--f-body": "'%s', %s" % (f.get("body"), f.get("body_fallback", "system-ui, sans-serif")),
        "--f-mono": "'%s', ui-monospace, monospace" % f.get("mono", "JetBrains Mono"),
        "--f-num": "'%s', %s" % (f.get("numbers", f.get("display")), f.get("display_fallback", "system-ui, sans-serif")),
        "--d-weight": str(f.get("display_weight", 600)), "--d-case": f.get("display_case", "none"),
        "--d-track": f.get("display_tracking", "-0.02em"), "--d-lh": str(f.get("display_line_height", 1.05)),
        "--n-weight": str(f.get("numbers_weight", f.get("display_weight", 600))),
        "--b-weight": str(f.get("body_weight", 400)),
        "--label-case": f.get("label_case", "uppercase"), "--label-track": f.get("label_tracking", "0.14em"),
        "--radius": "%spx" % b.get("radius", 0), "--h1": "%spx" % b.get("h1_size", 84),
        "--pad": "%spx" % b.get("padding", 120), "--img-filter": b.get("image_filter", "none"),
        "--rule": "%spx" % b.get("rule", 1), "--on-accent": b.get("on_accent", c.get("on_accent")),
    }
    root = ":root{%s}" % ";".join("%s:%s" % (k, val) for k, val in v.items() if val is not None)
    families, specs = [], f.get("google_specs", {})
    for key in ("display", "body", "numbers", "mono"):
        fam = f.get(key)
        if fam and fam not in families:
            families.append(fam)
    link = ""
    if families and not f.get("no_google_fonts"):
        link = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        for fam in families:  # one request per family: an unsupported weight can't break the others
            link += '<link href="https://fonts.googleapis.com/css2?family=%s:%s&display=swap" rel="stylesheet">' % (
                fam.replace(" ", "+"), specs.get(fam, "wght@300;400;500;600;700"))
    return root + "\n" + (b.get("css") or ""), link


# -------------------------------------------------------------------- lint

NUM_RE = re.compile(r"(\$|€|£)?\d[\d,.]*\s?(%|x|k|K|M|B|T|bn|m)\b")


def lint(slides, layouts, meta):
    warns = []
    words_total = 0
    for i, (sl, lay) in enumerate(zip(slides, layouts)):
        text = sl["raw"]
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        w = plain_words(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text))
        words_total += w
        lim = WORD_LIMIT.get(lay, 60)
        if w > lim:
            warns.append("slide %d (%s): %d words on slide, limit %d - move detail to notes (???)" % (i + 1, lay, w, lim))
        h1 = [b["v"] for b in sl["blocks"] if b["t"] == "h1"]
        if h1 and plain_words(h1[0]) > 14:
            warns.append("slide %d: headline is %d words - aim for <= 12, make it the takeaway" % (i + 1, plain_words(h1[0])))
        if lay not in ("title", "closing", "section", "html", "image", "logos") and not h1:
            warns.append("slide %d (%s): no '# headline' - every slide needs a takeaway headline" % (i + 1, lay))
        bullets = sum(len(b["items"]) for b in sl["blocks"] if b["t"] in ("ul", "ol"))
        if bullets > 5:
            warns.append("slide %d: %d bullets - max 5; split or show it instead" % (i + 1, bullets))
        has_num = bool(NUM_RE.search(text)) or any(b["t"] == "chart" for b in sl["blocks"])
        if has_num and lay in ("stats", "chart", "market") and not (sl["d"].get("source") or sl["d"].get("note") or "source=" in text):
            warns.append("slide %d (%s): numbers without @source - cite or mark as internal data" % (i + 1, lay))
        ph = re.findall(r"\[\[[^\]]*\]\]", text + "\n" + sl["notes"])
        if ph:
            warns.append("slide %d: %d [[placeholder]]s left - fill from facts.md or list them for the founder" % (i + 1, len(ph)))
        if re.search(r"\blorem\b|\bTBD\b|\bTODO\b|\bXX\b", text):
            warns.append("slide %d: filler text left in (lorem/TBD/TODO/XX)" % (i + 1))
    n = len(slides)
    for i, (sl, lay) in enumerate(zip(slides, layouts)):
        h1 = " ".join(b["v"] for b in sl["blocks"] if b["t"] == "h1").lower()
        if lay == "section" and "appendix" in h1:
            n = i  # main deck ends at the appendix divider
            break
        if lay in ("split", "screens") and h1 and plain_words(h1) > 10:
            warns.append("slide %d (%s): headline is %d words in a half-width column - aim for <= 9" % (i + 1, lay, plain_words(h1)))
    target = meta.get("target_slides")
    if target:
        lo, _, hi = target.partition("-")
        lo, hi = int(lo), int(hi or lo)
        if not lo <= n <= hi:
            warns.append("deck: %d main slides (before the Appendix divider), target %s" % (n, target))
    if "ask" not in layouts and meta.get("purpose", "fundraise") == "fundraise":
        warns.append("deck: no @layout ask slide - investors expect the raise, use of funds and milestones")
    return warns, words_total


# -------------------------------------------------------------------- main

def build(root, embed=False, out=None, quiet=False, preset=None):
    src_path = os.path.join(root, "deck.md")
    with open(src_path, encoding="utf-8") as f:
        meta, body = split_front_matter(f.read())
    brand = resolve_brand(root, meta, preset)
    img = Resolver(root, embed)
    slides = [parse_slide(s) for s in split_slides(body)]
    rendered, layouts = [], []
    for i, sl in enumerate(slides):
        h, lay = render_slide(sl, i, len(slides), meta, brand, img)
        if lay not in LAYOUTS:
            print("warning: slide %d unknown layout %r" % (i + 1, lay), file=sys.stderr)
        rendered.append(h)
        layouts.append(lay)
    with open(os.path.join(ASSETS, "deck.css"), encoding="utf-8") as f:
        base_css = f.read()
    with open(os.path.join(ASSETS, "deck.js"), encoding="utf-8") as f:
        js = f.read()
    tcss, font_link = theme_css(brand)
    mode = brand.get("mode", "light")
    title = meta.get("title") or brand.get("name", "Pitch deck")
    doc = """<!doctype html>
<html lang="%s" data-mode="%s" data-preset="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="generator" content="pitch-deck-studio">
%s
<style>%s
%s</style>
</head>
<body>
<main class="deck">
%s
</main>
<div class="hud"><div class="bar"></div><div class="count"></div></div>
<script>%s</script>
</body>
</html>
""" % (esc(meta.get("lang", "en")), esc(mode), esc(brand.get("preset")), esc(title), font_link, base_css, tcss,
       "\n".join(rendered), js)
    out_path = os.path.join(root, out or "deck.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    warns, words = lint(slides, layouts, meta)
    for m in sorted(set(img.missing)):
        warns.insert(0, "missing image: %s" % m)
    report = {
        "output": out_path, "slides": len(slides), "on_slide_words": words,
        "words_per_slide": round(words / max(len(slides), 1), 1),
        "layouts": layouts, "preset": brand.get("preset"), "warnings": warns,
    }
    if not quiet:
        print("built %s  (%d slides, %d on-slide words, %.1f/slide, preset=%s)" % (
            out_path, len(slides), words, report["words_per_slide"], brand.get("preset")))
        print("layouts: " + " ".join("%d:%s" % (i + 1, l) for i, l in enumerate(layouts)))
        if warns:
            print("\nQA warnings (%d):" % len(warns))
            for w in warns:
                print("  - " + w)
        else:
            print("QA: clean")
    return report


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = os.path.abspath(argv[1])
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    preset = argv[argv.index("--preset") + 1] if "--preset" in argv else None
    rep = build(root, embed="--embed" in argv, out=out, quiet="--quiet" in argv, preset=preset)
    if "--json" in argv:
        print(json.dumps(rep, indent=2))
    if "--outline" in argv:
        print(outline(root))
    return 0


def outline(root):
    """Markdown outline table from deck.md, for brief.md and facts.md slide references."""
    with open(os.path.join(root, "deck.md"), encoding="utf-8") as f:
        meta, body = split_front_matter(f.read())
    rows = ["| # | Layout | Headline | Source | Placeholders |", "|---|---|---|---|---|"]
    for i, s in enumerate(split_slides(body)):
        sl = parse_slide(s)
        lay = sl["d"].get("layout") or guess_layout(sl["blocks"])
        h1 = next((b["v"] for b in sl["blocks"] if b["t"] == "h1"), "")
        ph = len(re.findall(r"\[\[[^\]]*\]\]", sl["raw"] + sl["notes"]))
        rows.append("| %d | %s | %s | %s | %s |" % (i + 1, lay, h1.replace("|", "/"), sl["d"].get("source", ""), ph or ""))
    return "\n".join(rows)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
