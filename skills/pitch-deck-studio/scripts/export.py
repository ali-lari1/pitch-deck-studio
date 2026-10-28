#!/usr/bin/env python3
"""Export a built deck to PDF, per-slide PNGs and a contact sheet with headless Chromium.

Usage:
    python3 export.py <project_dir> [--pdf] [--png] [--sheet] [--check] [--only 3,7] [--browser PATH]

With no flag it does --pdf --sheet. --check reports elements that overflow a slide's safe area. Needs any Chromium-family browser
(Chrome, Chromium, Edge, Brave, Arc, or Playwright's bundled chromium).
Set CHROME_PATH to force one. Standard library only.

If no browser can run headless (some sandboxes), open deck.html in a normal
browser and press P (print -> Save as PDF, margins: none, background graphics: on).
"""
import glob
import os
import platform
import shutil
import subprocess
import sys
import tempfile

CANDIDATES_MAC = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Arc.app/Contents/MacOS/Arc",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
CANDIDATES_WIN = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
         "microsoft-edge", "msedge", "brave-browser", "brave"]


def playwright_browsers():
    roots = [os.path.expanduser("~/Library/Caches/ms-playwright"), os.path.expanduser("~/.cache/ms-playwright"),
             os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")]
    pats = ["chromium_headless_shell-*/chrome-*/headless_shell", "chromium_headless_shell-*/chrome-*/chrome-headless-shell",
            "chromium_headless_shell-*/*/chrome-headless-shell*", "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
            "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
            "chromium-*/chrome-linux*/chrome", "chromium-*/chrome-win*/chrome.exe"]
    out = []
    for r in roots:
        for p in pats:
            out += sorted(glob.glob(os.path.join(r, p)), reverse=True)
    return out


def find_browsers(explicit=None):
    found = []
    for c in [explicit, os.environ.get("CHROME_PATH")]:
        if c and os.path.exists(c):
            found.append(c)
    sysname = platform.system()
    found += [c for c in (CANDIDATES_MAC if sysname == "Darwin" else CANDIDATES_WIN if sysname == "Windows" else [])
              if os.path.exists(c)]
    found += [shutil.which(n) for n in NAMES if shutil.which(n)]
    found += playwright_browsers()
    seen, uniq = set(), []
    for f in found:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def run(browser, args, timeout=90):
    prof = tempfile.mkdtemp(prefix="pds-chrome-")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--hide-scrollbars", "--force-device-scale-factor=1", "--user-data-dir=" + prof,
           "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw"] + args
    if "headless_shell" in browser or "headless-shell" in browser:
        cmd[1] = "--headless"
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return r.returncode == 0, r.stderr.decode(errors="ignore")[-600:]
    except Exception as e:  # timeout, sandbox denial, missing libs
        return False, str(e)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def slide_count(html_path):
    with open(html_path, encoding="utf-8") as f:
        return f.read().count('<section class="slide')


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = os.path.abspath(argv[1])
    html_path = os.path.join(root, "deck.html")
    if not os.path.exists(html_path):
        print("no deck.html - run build.py first", file=sys.stderr)
        return 1
    flags = set(a for a in argv[2:] if a.startswith("--"))
    if not flags & {"--pdf", "--png", "--sheet", "--check"}:
        flags |= {"--pdf", "--sheet"}
    explicit = argv[argv.index("--browser") + 1] if "--browser" in argv else None
    only = None
    if "--only" in argv:
        only = [int(x) for x in argv[argv.index("--only") + 1].split(",")]
    url = "file://" + html_path.replace(os.sep, "/") if os.sep == "/" else "file:///" + html_path.replace("\\", "/")

    browsers = find_browsers(explicit)
    if not browsers:
        print("No Chromium-family browser found. Install Chrome/Chromium/Edge, set CHROME_PATH, or open deck.html "
              "and press P to print to PDF (margins none, background graphics on).", file=sys.stderr)
        return 2
    browser, err = None, ""
    for b in browsers:  # pick the first browser that actually runs headless here
        ok, err = run(b, ["--screenshot=" + os.path.join(tempfile.gettempdir(), "pds-probe.png"),
                          "--window-size=320,180", url + "?solo=1"], timeout=40)
        if ok:
            browser = b
            break
    if not browser:
        print("Found %s but none ran headless here (%s). Open deck.html and press P to save a PDF." % (
            ", ".join(browsers), err.strip()[-200:]), file=sys.stderr)
        return 3
    print("browser: " + browser)
    n = slide_count(html_path)

    if "--check" in flags:
        import html as _html, json as _json, re as _re
        prof = tempfile.mkdtemp(prefix="pds-chrome-")
        cmd = [browser, "--headless" if ("headless_shell" in browser or "headless-shell" in browser) else "--headless=new",
               "--disable-gpu", "--no-first-run", "--user-data-dir=" + prof, "--window-size=1920,1080",
               "--virtual-time-budget=8000", "--dump-dom", url + "?check=1"]
        try:
            out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90).stdout.decode(errors="ignore")
        except Exception as e:
            out = ""
            print("check failed: %s" % e)
        finally:
            shutil.rmtree(prof, ignore_errors=True)
        m = _re.search(r'<pre id="qa-result">(.*?)</pre>', out, _re.S)
        if not m:
            print("check: no result (fonts or scripts blocked?) - inspect visually instead")
        else:
            res = _json.loads(_html.unescape(m.group(1)))
            if res["issues"]:
                print("check: %d layout issue(s)" % len(res["issues"]))
                for it in res["issues"]:
                    print("  - slide %d: %s" % (it["slide"], it["what"]))
            else:
                print("check: no overflow on %d slides" % res["slides"])

    if "--pdf" in flags:
        out = os.path.join(root, "deck.pdf")
        ok, err = run(browser, ["--print-to-pdf=" + out, "--no-pdf-header-footer", "--print-to-pdf-no-header", url], 120)
        print(("pdf:   " + out) if ok and os.path.exists(out) else "pdf failed: " + err)
    if "--png" in flags:
        d = os.path.join(root, "slides")
        os.makedirs(d, exist_ok=True)
        for i in (only or range(1, n + 1)):
            out = os.path.join(d, "%02d.png" % i)
            ok, err = run(browser, ["--screenshot=" + out, "--window-size=1920,1080", "%s?solo=%d" % (url, i)])
            if not ok:
                print("png %d failed: %s" % (i, err))
        print("png:   %s/ (%d slides)" % (d, len(only or range(n))))
    if "--sheet" in flags:
        rows = (n + 3) // 4
        out = os.path.join(root, "contact-sheet.png")
        ok, err = run(browser, ["--screenshot=" + out, "--window-size=%d,%d" % (4 * 480 + 5 * 16, rows * 270 + (rows + 1) * 16),
                                url + "?grid=1"])
        print(("sheet: " + out) if ok else "sheet failed: " + err)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
