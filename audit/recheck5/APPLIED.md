# Re-check 5: what was applied

Sources (owner, 2026-10-06; staged outside the repo because some pages hold personal data): the sale spec (d08), its
addendum (d10), annex C (d09), the apartment details annex (d11), the studio ceramics spec, 05/10/2026 edition (d07), the
apartment sheet 1:75 (d01), the typical floor (d05), ground (d03), basement (d02) and roof (d04) sheets, and the sales-plan
notes (d06). Reports: `spec_finishes.md`, `spec_systems.md`, `studio.md`, `plans.md`, `site.md`.

Checks after every commit: `sitetest.mjs` (GPU) no issues, `roomdims.py` +0 (closet probe artifact unchanged),
`clearance_audit.py` 0 issues, no page errors, phone 40 fps.

## Applied

Interior (commit 5167387)
- Ceiling 2.70: d08 3.1 "לא פחות מ-2.70". The corridor drop is now 2.35 (minimum written 2.30).
- Mamad floor porcelain like the living room: d08 annex B forbids parquet or any flammable floor in a mamad.
- Skirting 7 cm in the floor material (d08: 33x7 or 60x7).
- Kitchen window C: no shutter (d08 lists none, the electrical sheet has no motor); its interior sill moved to the 1.20 sill.
- Master shower room window: one kip sash (d08).
- Washer niche walls painted, not tiled (d08: plaster in the service corner).
- No fixed rain head over the bathtub (d08 table 4).
- White flush plates (the studio spec offers chrome, brushed or white).
- Vanities: one-piece ceramic top with the basin sunk in (d10 item 3), deck-mounted mixers (d08 table 4).
- Master split condenser 84x40 over the main unit in the laundry niche (d10 item 11, AC sheet outline); pipes moved.
- d10 item 10: socket and TV point on the balcony, socket on the island (positions not written, estimates).
- Panel: the mamad is the model's room 3, which d01 writes as "חדר מס' 4 ממ\"ד" (the developer numbers the master 1); ceiling text; fan blade height 2.45.

Ceramics (commit d7c72b9)
- The 05/10/2026 edition adds page 5, six glossy 80x80 floor tiles: new picker group for the living and bedroom floors.
  Glossy floors get less relief and a stronger day reflection (estimate; the live view has no floor reflection).
- Catalog pages from 5 on renumbered; two finishes the spec does not write marked "not written".
- Kitchen splash stone option labelled as the addendum's item; bath tap and kitchen sink notes match the model.

Outside (commit 96821de)
- Floor 1 has our plan with the same balcony; the ground floor is the garden apartment (east face x 9.25, openings
  scaled, sills and heads estimates), its private garden, fences and pergola. The photo-based floor-1 terrace and stone
  podium are gone.
- Building A and B: one bar x -2.1..8.26 to z 30.6 on an open ground floor (lobby core, columns at x 8.15), B's south wing
  to z 42.6, the stair and lift core beside our entry.
- Lot wall on the lot line with the two entrance gaps, the car gate and the rounded SE corner; garden strip and low walls
  on the east; smoke-release vents; surface stalls, fire-truck pads, the ramp portal and the stair under the mamad window.
- Ali Mohar near side per d03 (sidewalk 14.3-16.9, parking on pavers 16.9-18.8, road from 18.8). The far side (photos)
  moved 2.2 m east to keep a 6.4 m road (estimate). Tirtsa Atar sidewalk from z 48.
- Our balcony slab was inside a comment and hidden by the old solid box below; restored.

## Decided without a change

- North: the site sheets' compass is 15.5 deg west of sheet-up, the sales plan's is sheet-up. OpenStreetMap has Ali Mohar
  at bearing 0.1 deg and Tirtsa Atar at 89.9 deg, so sheet-up is true north; the sun stays.
- Master shower room tile height: d08 says about 2.10, d10 (prevails) says to the ceiling; the model keeps full height.
- Bedroom windows: d08 "דריי קיפ, חלק תחתון קבוע או אחר"; the construction plan draws one sash. Kept one sash.
- Corridor passage 120 and family bath riser NW: the newer construction and plumbing sheets win over d01.
- Kitchen splash height: d10 says stone about 50 cm; the owners' kitchen has wall cabinets from 1.62, so the model keeps
  the 70 cm splash between them. Owner decision.

## Open: for the owner, the developer or the studio

- Area: d11 and d08 write about 130 sqm, the header 132 (contractor's figure). Laundry hide: d11 about 2 sqm, plans 2.9.
- Door sizes: d08 interior 70/200 (master shower 65), entrance 80/200, mamad 70; the plans and the model 82-86/210, 97.
- Window sizes in d08 differ from the construction plan (living 200/210 vs 270 wide).
- d08 standard tiles 60/60 and 30/60 vs the studio's 80x80 and 25x75; d10 sets 80/80. 15x60 balcony tile limited to 20
  sqm (balcony about 23).
- Vanity sizes (studio 60/80 and 100/120 vs model 100 and 70); master shower 80x80 (d08) vs 106x92 (plumbing sheet).
- Kitchen sink: d08 acrylic, studio stainless inset, model stainless undermount.
- Room numbering: the developer calls the master 1, the middle north room 2, the NW room 3, the mamad 4.
- Not drawn: mamad floor up to 3 cm higher and wet rooms 1 cm lower (d06 note 8); entrance steps (up or down not
  written, street level unknown); planters; floors 5-7 and the hipped roof with collectors (no plans, not visible).
