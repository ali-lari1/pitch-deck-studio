#!/usr/bin/env python3
"""Repo checks: SKILL.md frontmatter (Agent Skills spec), manifests, data, and a build of every example."""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "skills", "pitch-deck-studio")
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


s = open(os.path.join(SK, "SKILL.md"), encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
check(m, "SKILL.md: missing frontmatter")
fm = m.group(1) if m else ""
name = re.search(r"^name:\s*(.+)$", fm, re.M)
desc = re.search(r"^description:\s*(.+)$", fm, re.M)
check(name and name.group(1).strip() == "pitch-deck-studio", "name must equal directory name")
check(name and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1).strip()), "name must be lowercase-hyphenated")
check(desc and 1 <= len(desc.group(1)) <= 1024, "description must be 1-1024 chars")
for key in re.findall(r"^(\w[\w-]*):", fm, re.M):
    check(key in {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}, "non-portable frontmatter key: " + key)
check(s.count("\n") < 250, "SKILL.md should stay under 250 lines")
for ref in set(re.findall(r"`references/([\w./-]+\.md)`", s)):
    check(os.path.exists(os.path.join(SK, "references", ref)), "SKILL.md references missing file: " + ref)

versions = set()
for f in [".claude-plugin/marketplace.json", ".claude-plugin/plugin.json", "gemini-extension.json"]:
    d = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
    versions.add(d.get("version") or d["plugins"][0].get("version"))
meta_v = re.search(r'version:\s*"([^"]+)"', fm)
versions.add(meta_v.group(1) if meta_v else None)
check(len(versions) == 1, "version mismatch across manifests: %s" % versions)

presets = json.load(open(os.path.join(SK, "assets", "presets.json"), encoding="utf-8"))
for p, v in presets.items():
    for k in ("bg", "fg", "muted", "accent", "surface", "line", "inv_bg", "inv_fg"):
        check(k in v["colors"], "preset %s missing colour %s" % (p, k))
lib = json.load(open(os.path.join(SK, "data", "decks.json"), encoding="utf-8"))
check(lib["count"] == len(lib["decks"]) >= 100, "deck library count mismatch or < 100")
for d in lib["decks"]:
    check(isinstance(d.get("year"), int) and d["year"] >= 2022, "deck %s: year must be >= 2022" % d.get("company"))
    check(d.get("deck_url", "").startswith("http"), "deck %s: missing deck_url" % d.get("company"))
    check(os.path.exists(os.path.join(SK, "references", "verticals", "%s.md" % d.get("playbook"))), "deck %s: unknown playbook" % d.get("company"))

for ex in sorted(os.listdir(os.path.join(ROOT, "examples"))):
    proj = os.path.join(ROOT, "examples", ex)
    if not os.path.exists(os.path.join(proj, "deck.md")):
        continue
    r = subprocess.run([sys.executable, os.path.join(SK, "scripts", "build.py"), proj, "--json", "--quiet"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(r.returncode == 0, "example %s failed to build: %s" % (ex, r.stderr.decode()[-300:]))
    if r.returncode == 0:
        rep = json.loads(r.stdout.decode())
        check(not [w for w in rep["warnings"] if "missing image" in w], "example %s has missing images" % ex)

for script in ("shot.py", "export_pptx.py", "find_decks.py", "init_project.py", "brand_sheet.py", "brand_from_url.py", "export.py", "build.py"):
    r = subprocess.run([sys.executable, os.path.join(SK, "scripts", script), "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(r.returncode == 0, "%s --help failed" % script)

if errors:
    print("FAIL")
    for e in errors:
        print(" - " + e)
    sys.exit(1)
print("OK: frontmatter, manifests, %d presets, %d decks, examples build" % (len(presets), len(lib["decks"])))
