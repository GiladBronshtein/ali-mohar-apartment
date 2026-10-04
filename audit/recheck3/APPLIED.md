# Third re-check: what was applied (2026-10-04)

Source: the owner's high-quality vector PDFs, copied to `materials/plans/vector/` (sales plan, construction plan
5/5/26, electrical, plumbing, AC, kitchen supplier sheet). The construction plan is new: it was not part of the
earlier re-checks. Four independent reports, crops in the `*_crops/` folders: `geometry.md`, `electrical.md`,
`plumbing_ac.md`, `kitchen.md`. This file records which proposals went into `source/salon.html`.

"Written" means a number on a sheet; "scaled" means measured on the vector sheet (1:50, about ±3 cm).

After the changes: `roomdims.py` +0 on every room (closet 485/175 is the known probe artifact), `clearance_audit.py`
0 issues, `sitetest.mjs` no issues on desktop and phone.

## Found while fitting the ceramics: bath tiles buried in the walls

Not from a report. The tile skins in both bathrooms were still at the wall faces of before the first re-check; the
walls had since moved 2.5 to 3 cm, so the tiles sat inside the walls and the plaster showed. They now sit on the
current faces: family bath x 2.01 / 4.46, z -3.775 / -1.395; master bath x 4.63 / 6.85, z -4.98 / -3.26.

## Applied

### Geometry (geometry.md, construction plan)

| Item | Now | Basis |
|---|---|---|
| Living facade heads | `HEAD` 2.30 to 2.35 | written |
| Living facade openings | door A .79..3.49, door B 4.29..6.99, kitchen window C 7.75..8.45 with sill 1.20; piers, sliders, shutters, kitchen blind and window lights follow | written |
| Room 1 window | z -2.81..-1.91, sill .15, head 2.35, one sash; curtains and shutter follow | written (sash drawn) |
| Room 2 window | x .365..1.265, sill .15, head 2.35, one sash (`windowX` gained a `panes` argument) | written (sash drawn) |
| Master east window | z -2.17..-1.27, sill .15, head 2.35, one sash; the fixed transom bar is gone, curtains, track, bars and shutter follow | written (sash drawn) |
| Master bath window | x 6.015..6.615, sill 1.25, head 2.35; tiles follow | written |
| Mamad window | z .48..1.48, sill 1.10, head 2.10; blast frame follows | written |
| Bath window to the laundry niche | x 2.375..3.575, sill 1.10; tiles follow | written |
| Corridor to living passage | 120 wide, x 1.80..3.00 (was 98); the TV-wall stretch starts at 3.00 | written on the construction plan, scaled 120 on both MEP sheets |
| Kitchen entry wall end | x 4.33 | written |

### Plumbing and AC (plumbing_ac.md)

| Item | Now | Basis |
|---|---|---|
| Family bath riser box | NW corner, x 2.01..2.20, z -3.775..-3.575, between the WC ledge and the cabinet (was full height in the SW corner) | symbol on two sheets, scaled |
| Master split | over the master door on the room face of the door wall, blowing east | scaled |
| Corridor return grille | x 1.88..2.68, z -1.145..-.545 | scaled |
| Master shower | head on a west-wall arm at 2.10 (was a ceiling rain head) | written type and height, scaled position |
| Living supply grille 2 | centre 5.90 | scaled |
| Niche condenser | 100x45 footprint, fan toward the louvre screen, height .98 (estimate) | scaled |
| Balcony floor drains | (8.89, 1.63) and (8.89, 7.36) | scaled |

### Electrical (electrical.md)

| Item | Now | Basis |
|---|---|---|
| Mamad socket and switch by the window | z 1.59 | written 120 |
| Corridor switch 3c | x 3.18 (clears the new passage jamb) | scaled |
| Consumption display | east of the panel, x 3.80..3.92 | scaled |
| Mamad low socket, TV group | z 2.33; z .89 | scaled |
| Corridor socket | x .65 | scaled |
| Balcony lights | (7.96, 2.14) and (7.96, 5.73) | scaled |
| Double socket and fibre point by the panel | added at x 3.57 (h 1.15) and 3.99 (h .40); heights estimates | scaled |
| Niche AC isolator, water heater switch | added, IP65 boxes at h 1.10 (estimate) | scaled |
| Pier switches and socket, kitchen switch 1d | follow the new pier (3.89) and wall end (4.17) | scaled |

### Kitchen (kitchen.md)

No wall, window or ceiling change. The 12 differences from the supplier sheet are owner design choices and stay.

## Not applied

| Item | Why |
|---|---|
| Room sizes from the construction plan (+5 to +8 cm per room, 10 to 15 cm partitions) | the model stays on the sales plan so `roomdims.py` stays +0 |
| Room 1 north face -5.01 | breaks roomdims (361 to 359) |
| Kitchen entry wall face z 5.54 | many dependents, not a probe; optional |
| Ceiling height | not written. Heads at 2.35 plus a 35 cm shutter box, and the mamad sleeves at H=2.63, point to 2.70 or more; the model keeps the 2.60 estimate |
| Balcony edge upstand | a 30 cm band is drawn, no height; the levels suggest a top about 5 cm above the floor, not the 0.45 estimate |
| Mamad blast leaf (drawn about 70, model 86), filter box 35x40, niche riser 8 cm, heater 60, riser 1 | low confidence |
| Washer/dryer sockets, pier socket offsets of under 5 cm | optional, low |
| Two kitchen sockets from the supplier sheet | the supplier layout is not the owners' kitchen |

## Still open

- Boxed "א" in each bedroom and the mamad: meaning unknown, ask the electrician.
- Blue box "1" over the entry door: chime or strike.
- Cones and an "S" box in the living room: alarm prep or an AC controller.
- Window C has no shutter motor on the electrical sheet; the model has a shutter.
- Cisterns are drawn exposed; the model's concealed ones are a design choice.
- Second condenser (84x40, the master split's) above the main unit: drawn, not modelled.
