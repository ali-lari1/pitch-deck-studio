#!/usr/bin/env python3
"""Screenshot a web page (e.g. the founder's product or site) for a `screens` or `image` slide.

Usage:
    python3 shot.py <url> <out.png> [--width 1440] [--height 900] [--mobile]

Uses the same headless-browser discovery as export.py and times out instead of hanging.
Only capture the founder's own product/site (or pages they point you to). Crop or annotate afterwards if needed.
--mobile uses a 390x844 viewport for phone-frame slides.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export  # noqa: E402


def main(argv):
    if len(argv) < 3 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    url, out = argv[1], os.path.abspath(argv[2])
    w = int(argv[argv.index("--width") + 1]) if "--width" in argv else 1440
    h = int(argv[argv.index("--height") + 1]) if "--height" in argv else 900
    if "--mobile" in argv:
        w, h = 390, 844
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for b in export.find_browsers():
        ok, err = export.run(b, ["--screenshot=" + out, "--window-size=%d,%d" % (w, h), url], timeout=60)
        if ok and os.path.exists(out):
            print("shot: %s (%dx%d) via %s" % (out, w, h, os.path.basename(b)))
            return 0
    print("Could not capture %s headlessly. Ask the founder for screenshots instead." % url, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
