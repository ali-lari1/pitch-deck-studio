# Examples

Two **fictional** companies, each built entirely from a `deck.md` + `brand.json` with Pitch Deck Studio. All numbers are illustrative.

| Example | Preset | Arc | Files |
|---|---|---|---|
| **Dispensa**: AI back office for independent pharmacies, seed | `swiss` (custom accent) | traction-led | [deck.md](dispensa/deck.md) · [deck.pdf](dispensa/deck.pdf) · [deck.html](dispensa/deck.html) |
| **Meridian**: in-orbit satellite refuelling, Series A | `cosmos` (roadshow style) | mission | [deck.md](meridian/deck.md) · [deck.pdf](meridian/deck.pdf) · [deck.html](meridian/deck.html) |

Open the PDFs on GitHub. To present the HTML, download it (or clone the repo) and open it in a browser. Use `O` for overview, `N` for notes and `R` for reader mode.

Rebuild after editing:
```bash
python3 ../skills/pitch-deck-studio/scripts/build.py dispensa
python3 ../skills/pitch-deck-studio/scripts/export.py dispensa
```
