# Second re-check: what was applied (2026-10-04)

Five independent reports, each against the originals in `materials/plans/originals/`, the site photos and the live
model: `geometry.md`, `electrical.md`, `plumbing_ac.md`, `visual_interior.md`, `environment.md` (crops in the `*_crops/`
folders). This file records which proposals went into `source/salon.html`.

"Written" means a number on a sheet; "scaled" means measured from the photo, accurate to a few cm.

After the changes: `roomdims.py` +0 on every room (closet 485/175 is the known probe artifact), `clearance_audit.py`
0 issues, `sitetest.mjs` no issues on desktop and phone.

## Applied

### Geometry (geometry.md)

| Item | Now | Basis |
|---|---|---|
| Plan note on dimensions | The info text cites the plan note: dimensions are wall to wall before plaster and cladding (balcony: from the outer wall) | written |
| Entry wall by the kitchen | `W(2.555, 3.63, 5.50, 5.70)` plus `W(3.63, 4.30, 5.50, 5.61)`; floor strips, kitchen plinth and tall-unit trim follow, 9 cm filler on the tall unit | scaled |

### Electrical (electrical.md)

| Item | Now |
|---|---|
| Room 1, room 2, mamad socket groups | `dst` at h 1.80 at the scaled positions |
| Master TV wall | `std` at h 1.80, x 6.93 |
| Master bed heads | `ds` at x 5.78 and `ksd` at x 8.02, h .60 |
| Mamad filter socket | h 2.20 by the filter |
| Splash-proof sockets | h 1.10 in both bathrooms |
| Washer and dryer sockets | h 1.40 on the niche wall |
| Bathroom wall heaters | ensuite and family bath, h 1.90 to 2.10 (size an estimate) |
| Entry switch plate, intercom | plate at x 2.66, intercom x 2.74..2.84 |

### Plumbing and AC (plumbing_ac.md)

| Item | Before | Now | Basis |
|---|---|---|---|
| Corridor and living-strip drop ceiling | 25 cm | **35 cm** (ceiling 2.25 if H is 2.60). The note "h=35cm (netto)" has its Latin written mirrored; the first re-check read it as 25 | written |
| Bridge over the TV | 2.22 to the drop | 2.19 to the drop, LED strip under it at 2.175 (design element, keeps clear of the slab) | follows the drop |
| Niche louvres | 7 cm bars every 12 cm | thin blades every 10 cm, tilted about 26 deg, about 75% clear | written "80% open" |
| Water heater | z -4.80 effective | z -4.69 | scaled, both sheets |
| Kids' bath WC axis | 42 from the north wall | 44 | written |
| Niche drain riser | none | 4" riser in the NW corner of the niche | scaled |

Resolved by the drop: the mamad 8" sleeves (top 10 cm under the ceiling) now sit inside the ceiling void instead of
5 cm below the drop.

### Interior quality (visual_interior.md)

- GTAO: radius .3, thickness .4; curtains, glass and other transparent meshes and the bedside pendant cords hidden from
  the AO pass (no more barcode streaks on the sheers, fewer halos around thin dark objects).
- Family tub hollow (floor, four walls, drain, overflow); shower niches as recesses with a darker back panel; brushed
  steel sink with a steel drain ring; gooseneck faucet.
- Eve: wave pendant, island and master fan lights softer, island light raised to 2.3, eve bloom .24, downlights 1.8, TV
  screen roughness .24 (fewer hard discs in the screen and slab).
- Ceiling fill: hemisphere ground colour #cdc4b2.
- Slat wall: its own oak material with a finer figure and a less orange tone.
- Skirting #e4e2dc so it reads against the white wall.
- Service balcony: tilted louvre blades; condenser with a ring grille, side slots, an insulated refrigerant pair and a
  drain hose (routing an estimate).
- Induction hob with zone rings and a touch strip; kettle and an oil and salt tray on the counter.
- Black flush pulls on the balcony sliders, black levers on every window (positions an estimate).

### Environment (environment.md)

- Tower moved to the south-east beyond the lot: two stepped wings, panel facade with scattered square windows, two
  brown louvre strips, loggias, red roof element. The old block in its place removed.
- Eastern blocks pushed out, a far ring added at about 150 to 300 m, north closing blocks, blocks off the cross street,
  up to 80 courtyard trees kept clear of every footprint.
- Lit windows on every block and the tower in eve; facade windows smaller; light glass rails; red pergolas narrower.
- Lot: soil only from z 9 to 22, 1 m retaining wall, driveway with 3 cars south of it; the tent removed (a sukkah).
- Ali Mohar east side: perpendicular bays only in front of the school's south end with red-white kerbs; parallel lane,
  red-paver sidewalk and a yellow tactile strip elsewhere; parallel cars and a white van.
- Street lights with a curved arm; walkway lamp on a pole.
- School: near-white stone, a small accent panel, dark window frames, taller south volume with solar heaters, utility
  cabinets.
- North: weeds plot, corrugated grey-blue hoarding, pallets, cross street.
- Our balcony upstand .45 (estimate from the photos); Building A neighbour balconies as separate boxes (keyplan).
- Exterior ground envMap 1.1.

## Not applied (open)

- **Soil colour:** the photos show orange-red hamra (about #b06d40). The model keeps the earlier neutral colour
  because changing it reverses an earlier owner decision. Waiting for the owner.
- Geometry: room 1 shift of 2.2 cm and single-sash windows (low confidence); master east window sill; mamad blast door
  leaf (72 drawn vs 86); balcony open edges (a 30 cm band, upstand or planter, not written); columns 1 and 2.
- Electrical: the boxed "א 25" marks in rooms 1, 2, master and mamad; switch 3c by the panel; the socket "x2" and the
  blue FO mark by the panel; the "9" by the family basin; the niche isolator 3x16A IP65; ceiling points 1a and 1b vs
  the owners' lamps (design choice); the blue box at the entry latch (electric strike?).
- Plumbing and AC: return grille 14 cm (scaled, low); "H=2.63" next to the mamad sleeves (probably its ceiling height);
  passage width 120 scaled on both MEP sheets vs 98 in the model (sales plan to check); pipe box NW vs SW in the kids'
  bath; master split position (cleanout suggests above the master door); condenser outline 137x55 vs a 89x34 unit;
  high and low cisterns vs concealed ones; mamad filter 38x33 vs 50x21; living bulkhead depth .73 vs .80; balcony
  drain 1 z; mamad blast door 4 to 9 cm west; master shower wall-arm head at 2.10.
- Interior: sheer hems, rug pile, cabinet reveals, towels on the hooks and bath bottles left for later; the frames
  pendant cables still get some AO halo.
- Environment: facade cladding unknown (raw concrete); the floor-1 strip under the balcony is ambiguous; lot slope.

## Next re-check

Re-run from the originals, not from this file. Watch for mirrored Latin text on the AC sheet.
