#!/usr/bin/env python3
"""Find and download openly licensed photos for a deck, and record credits.

Usage:
    python3 find_images.py "<query>" [--source openverse|nasa|unsplash|pexels] [--n 8]
                           [--preview-dir <dir>] [--download <project>/assets --pick 1,3] [--name problem]

Sources:
  openverse  CC-licensed images from Openverse (Flickr, Wikimedia...). No key. Commercial-use licences only.
  nasa       NASA Image Library: public domain, great for space, earth, aerospace, science. No key.
  unsplash   High-quality photos under the Unsplash License. Needs UNSPLASH_ACCESS_KEY.
  pexels     High-quality photos under the Pexels License. Needs PEXELS_API_KEY.
Default: unsplash if UNSPLASH_ACCESS_KEY is set, else pexels if PEXELS_API_KEY is set, else openverse.

Without --download it lists candidates (id, size, licence, preview URL), so look at the previews before choosing.
With --download it saves the picked results (default: first) as <name>-<n>.jpg in the folder, resizes to 1600px
wide if Pillow is installed, and appends attribution rows to <folder>/CREDITS.md.
Use photos for atmosphere and context (the customer, the place, the problem). Never present them as the company's
own product, team or customers.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = "pitch-deck-studio/1.1 (+https://github.com/ali-lari1/pitch-deck-studio)"


def get(url, headers=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40) as r:
        return r.read()


def openverse(q, n):
    u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "license_type": "commercial", "page_size": n, "size": "large"})
    out = []
    for r in json.loads(get(u))["results"]:
        out.append({"id": r["id"], "url": r["url"], "preview": r.get("thumbnail") or r["url"], "w": r.get("width"),
                    "h": r.get("height"), "title": r.get("title", ""), "author": r.get("creator") or "unknown",
                    "license": ("%s %s" if r.get("license") in ("cc0", "pdm") else "CC %s %s") % (
                        r.get("license", "").upper(), r.get("license_version", "")),
                    "page": r.get("foreign_landing_url", ""), "source": "Openverse/" + r.get("source", "")})
    return out


def nasa(q, n):
    u = "https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image"})
    out = []
    for it in json.loads(get(u))["collection"]["items"][:n]:
        md = it["data"][0]
        prev = [l["href"] for l in it.get("links", []) if l.get("rel") == "preview"]
        out.append({"id": md["nasa_id"], "url": None, "preview": prev[0] if prev else "", "w": None, "h": None,
                    "title": md.get("title", ""), "author": "NASA", "license": "Public domain (NASA media guidelines)",
                    "page": "https://images.nasa.gov/details/" + md["nasa_id"], "source": "NASA"})
    return out


def nasa_full(nid):
    files = [f["href"] for f in json.loads(get("https://images-api.nasa.gov/asset/" + urllib.parse.quote(nid)))["collection"]["items"]]
    for suffix in ("~large.jpg", "~orig.jpg", "~medium.jpg"):
        for f in files:
            if f.endswith(suffix):
                return f.replace(" ", "%20").replace("http://", "https://")
    return files[0]


def unsplash(q, n):
    key = os.environ["UNSPLASH_ACCESS_KEY"]
    u = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "landscape"})
    out = []
    for r in json.loads(get(u, {"Authorization": "Client-ID " + key}))["results"]:
        out.append({"id": r["id"], "url": r["urls"]["raw"] + "&w=1600&q=80&fm=jpg", "preview": r["urls"]["small"],
                    "w": r["width"], "h": r["height"], "title": r.get("alt_description") or "",
                    "author": r["user"]["name"], "license": "Unsplash License", "page": r["links"]["html"],
                    "source": "Unsplash", "_dl": r["links"].get("download_location")})
    return out


def pexels(q, n):
    key = os.environ["PEXELS_API_KEY"]
    u = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "landscape"})
    out = []
    for r in json.loads(get(u, {"Authorization": key}))["photos"]:
        out.append({"id": r["id"], "url": r["src"]["large2x"], "preview": r["src"]["medium"], "w": r["width"], "h": r["height"],
                    "title": r.get("alt") or "", "author": r["photographer"], "license": "Pexels License",
                    "page": r["url"], "source": "Pexels"})
    return out


def save(data, path):
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(data)).convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    except Exception:
        with open(path, "wb") as f:
            f.write(data)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    q = argv[1]
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    src = opt("--source") or ("unsplash" if os.environ.get("UNSPLASH_ACCESS_KEY") else
                              "pexels" if os.environ.get("PEXELS_API_KEY") else "openverse")
    n = int(opt("--n", 8))
    fn = {"openverse": openverse, "nasa": nasa, "unsplash": unsplash, "pexels": pexels}.get(src)
    if not fn:
        print("unknown source %s" % src, file=sys.stderr)
        return 1
    try:
        res = fn(q, n)
    except KeyError as e:
        print("%s needs the %s environment variable" % (src, e), file=sys.stderr)
        return 2
    except Exception as e:
        print("search failed (%s): %s" % (src, e), file=sys.stderr)
        return 3
    folder = opt("--download")
    if not folder:
        pdir = opt("--preview-dir")
        if pdir:
            os.makedirs(pdir, exist_ok=True)
        for i, r in enumerate(res, 1):
            size = "%sx%s" % (r["w"], r["h"]) if r["w"] else "size n/a"
            print("%d. [%s] %s | %s | %s | %s\n   preview: %s\n   page: %s" % (
                i, r["source"], r["title"][:70], r["author"], size, r["license"], r["preview"], r["page"]))
            if pdir and r["preview"]:
                try:
                    with open(os.path.join(pdir, "%02d.jpg" % i), "wb") as f:
                        f.write(get(r["preview"]))
                except Exception:
                    pass
        if pdir:
            print("previews saved in %s (open them to choose, then re-run with --download ... --pick N)" % pdir)
        return 0
    os.makedirs(folder, exist_ok=True)
    picks = [int(x) for x in opt("--pick", "1").split(",")]
    name = re.sub(r"[^a-z0-9-]+", "-", (opt("--name") or q).lower()).strip("-")[:40]
    credits = os.path.join(folder, "CREDITS.md")
    new = not os.path.exists(credits)
    with open(credits, "a", encoding="utf-8") as cf:
        if new:
            cf.write("# Image credits\n\n| File | Title | Author | Licence | Source |\n|---|---|---|---|---|\n")
        for k in picks:
            r = res[k - 1]
            url = r["url"] or nasa_full(r["id"])
            path = os.path.join(folder, "%s-%d.jpg" % (name, k))
            save(get(url), path)
            if r.get("_dl"):  # Unsplash API guidelines: trigger the download endpoint
                try:
                    get(r["_dl"], {"Authorization": "Client-ID " + os.environ["UNSPLASH_ACCESS_KEY"]})
                except Exception:
                    pass
            cf.write("| %s | %s | %s | %s | [%s](%s) |\n" % (os.path.basename(path), r["title"][:60].replace("|", "/"),
                                                           r["author"], r["license"], r["source"], r["page"]))
            print("saved %s  (%s, %s)" % (path, r["author"], r["license"]))
    print("credits: " + credits)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
