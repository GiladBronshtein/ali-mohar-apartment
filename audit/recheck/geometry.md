# Geometry re-check: walls, openings, rooms (2026-10-04)

Read-only audit of `source/salon.html` against the plans. No model file was edited.

## Sources and method

- **Sales plan PDF (architect):** this is a single 150 ppi raster image, not a vector PDF. The registration from the
  earlier audit was re-used: u = 1373.25 - 79.0 z, v = 457.5 + 79.0 x, so 1 px = 1.27 cm.
  - The image is rotated: right = north, down = east.
  - Wall fill reads about grey 114 and floor about 240. Runs were taken at threshold 130.
  - The registration has a constant offset of about 2 cm: the living face of the TV wall reads z -0.022 everywhere.
    Wall faces are therefore compared relative to a neighbouring face, not as absolute values.
  - The drawing scale is not uniform (the mamad and bath areas are stretched about 2 %). Every "scaled" value below
    carries +/- 2 to 5 cm. Written dimensions govern wherever they exist.
- **Contractor MEP sheets (HADA, 1:75 on A3):** these are photos, at `materials/plans/originals/*.jpg`.
  - Perspective makes the scale differ per axis (about 2.2 to 2.4 px per real cm).
  - Every photo measurement was calibrated against a written dimension next to it, on the same axis.
- **Model geometry:** parsed from the `W()` calls between `// WALLS:` and `// corridor gypsum`, plus the living facade
  piers (L831-832) and the balcony boxes (L1527-1530).
- **Baseline today:**
  - `roomdims.py`: +0 on every room. The closet z 485/175 is the known probe artifact.
  - `clearance_audit.py`: 0 issues.

Proof crops are in `geo_crops/`. On the `pdf_*` crops, model walls are outlined in red (full height) and blue (door
or window openings, partial height).

## 1. Written dimensions

| item | plan value | model | diff | verdict | code line |
|---|---|---|---|---|---|
| mamad z x x | 262 x 355 written (sales) | 262 x 355 | 0 | OK | L822-823, L851-852 |
| room 1 (NW) | 361 x 274 written | 361 x 274 | 0 | OK | L819, L822, L839-840 |
| room 2 | 356 x 282 written | 356 x 282 | 0 | OK | L840-842 |
| dining / alcove z | 277 written | 277 | 0 | OK | L827, L837 |
| corridor | 110 written (at x about 1.36, by the room 2 door) | 110 | 0 | OK | L841, L853 |
| living x | 728 written | 728 | 0 | OK | L831 |
| living + kitchen z | 879 written | 879 | 0 | OK | L829 |
| kitchen x | 365 written | 365 | 0 | OK | L827 |
| family bath | 238 x 245 written | 238 x 245 | 0 | OK | L843-847 |
| master | 296 x 430 written | 296 x 430 | 0 | OK | L836-837, L847 |
| master bath | 172 x 222 written | 172 x 222 | 0 | OK | L847-848 |
| closet x | 190 written | 190 | 0 | OK | L847-848 |
| closet z | 175 written | probe reads 485 | n/a | known probe artifact | roomdims.py |
| stair hall depth | 252 written (AC sheet) | core is a solid mass | n/a | not modelled (outside the unit). PDF scales 248, consistent | L827 |
| stair flight width | 118 written (AC sheet) | not modelled | n/a | outside the unit | L827 |
| ensuite WC axis to closet wall | 60 written (plumbing) | 60 (WC centre 6.25, wall face 6.85) | 0 | OK | L1295, L1309 |
| shower | 106 x 92 written (plumbing) | x 4.63..5.69, z -4.98..-4.06 = 106 x 92 | 0 | OK | L1296 |
| corridor return-air grille | 80 x 60 written (AC) | 80 x 60 | 0 | OK | L859 |
| entry door to light | 65 written (electrical, fixture offset) | n/a | n/a | fixture, not geometry | |

Crop: `ac_stair_252_118.jpg`, `pl_ensuite_wc_60.jpg`.

All the other written numbers on the electrical sheet that were read (41, 129, 180, 140, 144, 46, 173, 100, 44, 72, 120,
128, 218, 58, 105, 210, 183, 135, 25, 147, 127, 200, 185, 220, 150, 89, 230, 65) are outlet and fixture offsets, not
wall or opening dimensions. They belong to the electrical audit.

## 2. Facade openings (scaled from the PDF)

| item | plan value (scaled) | model | diff | verdict | code line |
|---|---|---|---|---|---|
| living window A | z 0.769..3.44 | 0.78..3.45 | +1 / +1 cm | OK | L831 |
| living window B | z 4.263..6.87 | 4.26..6.88 | 0 / +1 | OK | L831 |
| living window C (sill 1.0) | z 7.693..8.377 | 7.70..8.39 | +1 / +1 | OK | L831 |
| living piers | -0.142..0.769, 3.44..4.263, 6.87..7.693 | -0.13..0.78, 3.45..4.26, 6.88..7.70 | 1 cm or less | OK | L831 |
| room 1 window | z -2.915..-1.953 | -2.92..-1.93 | -1 / +2 | OK | L822 |
| mamad window | z 0.465..1.427 | 0.47..1.44 | 0 / +1 | OK | L823 |
| room 2 window | x 0.278..1.253 | 0.27..1.25 | -1 / 0 | OK | L819 |
| laundry niche opening | x 2.152..3.658 | 2.15..3.65 | 0 / -1 | OK | L819-820 |
| ensuite window | x 6.0..6.582 | 5.99..6.58 | -1 / 0 | OK. Plumbing sheet: about 60 wide, centred on the WC | L820 |
| master window | z -2.282..-1.32 | -2.27..-1.31 | +1 / +1 | OK | L836 |
| bath / laundry window | x 2.38..3.557 | 2.37..3.55 | -1 / -1 | OK | L845 |

Sill and head heights are not on any plan. They stay estimates.

## 3. Doors (scaled from the PDF unless noted)

| item | plan value | model | diff | verdict | code line |
|---|---|---|---|---|---|
| room 1 | x -2.06..-1.22, hinge east, opens into room | -2.06..-1.23, hinge -1.24 east, into room | 0 / -1 | OK | L839, L913 |
| **room 2** | **x 0.93..1.76 (83), hinge east, into room** | **0.88..1.77 (89)** | **west jamb -5 cm** | **FIX** | L811, L841, L914, L933 |
| family bath | x 2.88..3.70, hinge east, into bath | 2.86..3.69, hinge 3.68 | -2 / -1 | OK | L843, L915 |
| master | z -1.168..-0.345, hinge on the TV wall side | -1.16..-0.34 | 1 cm or less | OK | L849, L916 |
| ensuite (from the closet) | z -4.066..-3.345 | -4.06..-3.36 | 1 to 2 cm | OK | L848, L918 |
| closet opening | x 7.557..8.329 | 7.54..8.32 | -2 / -1 | OK | L847 |
| mamad blast door | x -1.975..-1.19, hinge west, opens 90 deg into the corridor | -1.98..-1.19, hinge -2.0 | 0 | OK | L851, L917 |
| corridor to alcove passage | x 2.0..2.975 | 1.99..2.97 | -1 / 0 | OK | L853 |
| **entry door, rough opening** | **x 1.582..2.557 (97.5) on the PDF. Electrical photo: about 97 to 101, leaf about 95, hinge west, opens inward** | **1.62..2.52 (90)** | **about -7.5 cm** | **FIX** | L829, L904, L906, L941, L943 |

The room 2 door on the PDF is drawn like the room 1 and bath doors (83 to 84 wall to wall). The model is the only one at
89. Crops: `pdf_room2_door.jpg`, `pdf_entry_door.jpg`, `el_entry_door.jpg`.

## 4. Wall thicknesses and faces (scaled, relative to a neighbouring face)

| item | plan value (scaled) | model | diff | verdict | code line |
|---|---|---|---|---|---|
| **TV wall, corridor section x 2.97..4.15** | **14 px = 17.8 cm. The corridor face sits 5 cm north of the alcove wall's corridor face (x -0.25..1.99)** | **14.5, flush with the alcove wall at -0.145** | **-3.3 to -5 cm** | **FIX (open item 3)** | L837 |
| TV wall, master section x 4.15..9.30 | 10 px = 12.7 | 14.5 | +1.8 | keep: the written master 296 governs | L837 |
| TV wall jog beside the master door | 18 px, face about -0.23 to -0.25 | -0.24 | 0 | OK | L850 |
| alcove / corridor wall x -0.25..1.99 | 10 px = 12.7 | 14.5 | +1.8 | keep: the written corridor 110 governs | L853 |
| west facade, room 1 proper | inner face -3.89 | -3.89 | 0 | OK | L822 |
| west facade, room 1 wardrobe niche | inner face -3.81 (47 thick). Electrical photo shows the face stepping in about 6 cm from room 1 | -3.81 (47) | 0 | OK (open item 2) | L822 |
| west facade, mamad niche | -3.823 | -3.83 | -1 | OK | L823 |
| mamad north wall | 22.7 | 27 | +4 | within scale noise; written mamad 262 governs | L851 |
| mamad / alcove wall | 21.5 | 25 | +3.5 | within noise; written 355 governs | L852 |
| room 2 / bath wall | 12.6 | 16 | +3.4 | within noise; written 282 and 245 govern | L842 |
| corridor south face | -1.269 | -1.245 | +2.4 | within noise; written 110 governs | L841 |
| entry wall | z 5.478..5.756 (28) | 5.50..5.70 (20) | -8 | outer face is inside the solid lobby mass, not visible. No change | L829 |
| **balcony north wall** | **z -0.142..0.339 (48), to x 9.304** | **-0.13..0.30 (43), to x 9.30** | **inner face -4 cm** | **minor FIX** | L1527, L1530 |
| balcony south wall | z 8.731..9.237 (50.6), to x 10.10 | 8.71..9.20 (49), to x 10.07 | 1 to 2 px | OK (open item 4) | L1527, L1530 |
| kitchen / living south outer face at x 7.28..7.70 | 9.237 | pier ends at 9.11 | -12.7 | exterior corner only. Cosmetic | L831 |
| stair hall north wall | z 2.756..3.047 (29) | inside the solid mass | n/a | not modelled | L827 |
| stair hall east wall | x 1.165..1.43 | living boundary at 1.45 | 2 cm | OK | L827 |

Crops: `pdf_tvwall_corridor.jpg`, `pdf_room1_niche_facade.jpg`, `el_room1_niche_facade.jpg`, `pdf_balcony_north.jpg`,
`pdf_balcony_south.jpg`.

Raw PDF profile across the TV wall (u 1360..1420, `#` is wall). Living face at u 1375 in both rows.

```
x 3.1  ...............##############...........   14 px (corridor section)
x 6.0  ...............##########...............   10 px (master section)
```

## 5. The four unconfirmed audit items

### 5.1 Ensuite WC axis, 49 vs 60: CONFIRMED 60, model already correct
- **Evidence:** the plumbing sheet writes "60" from the WC axis to the inner face of the closet wall.
- **Model:** WC centre 5.88..6.24 plus the 0.19 shift = 6.25. The wall face is at 6.85, so the axis is 60.
- **Code:** L1295, L1309.
- **Crop:** `pl_ensuite_wc_60.jpg`.

### 5.2 West facade behind the room 1 wardrobe, 38 vs about 47: CONFIRMED 47, model already correct
- **Evidence:**
  - The PDF inner face scales at -3.81.
  - The electrical photo shows the niche face stepping in from room 1 (-3.89) by about 6 cm.
- **Model:** L822 `W(-4.28, -3.81, -1.425, -0.50)`.
- **Crops:** `pdf_room1_niche_facade.jpg`, `el_room1_niche_facade.jpg`.

### 5.3 TV wall corridor side, 14.5 vs about 18: CONFIRMED THICKER, model wrong
- **Evidence:**
  - Over x 2.97..4.15 the PDF wall is 14 px (17.8 cm), against 10 px on the master section and on the alcove wall.
  - The living face is in one line along the whole wall, so the 4 px difference is all on the corridor face.
  - The corridor scales 85 px there, against 88 to 89 px at the written 110. That is about 106 cm.
  - The electrical panel recess (x about 3.38..3.79) sits inside this thicker section. The thickening covers the
    whole section, not just the panel, because x 3.1, 3.3, 3.9 and 4.1 all read 14 px.
- **Model:** L837 holds the whole wall at -0.145.
- **Proposed corridor face:** -0.19. This keeps the 5 cm step against the alcove wall within the scale noise, and the
  corridor becomes 105.5 there.
- **Code:** L837.
- **Crops:** `pdf_tvwall_corridor.jpg`, `pdf_panel_recess.jpg`, `el_tvwall_panel.jpg`.

### 5.4 Balcony south wall thickness: CONFIRMED about 50, model already correct
- **Evidence:** the PDF reads z 8.731..9.237 (50.6), ending at x 10.10.
- **Model:** 8.71..9.20 (49), ending at x 10.07. The difference is within 1 to 2 px.
- **Code:** L1527, L1530.
- **Crop:** `pdf_balcony_south.jpg`.

## 6. Plan elements missing from the model, and model elements not on the plan

| element | plan | model | note |
|---|---|---|---|
| stair hall (252 x 118 flight, fire door 30/30, lobby) | AC sheet and PDF | solid masses L827 | outside the unit. Acceptable as long as no view looks into it |
| electrical panel recess | about 10 cm recess in the thick corridor section, x about 3.38..3.79 | plate 0.7 cm proud of -0.145, x 3.33..3.78. The L1612 comment says "recessed" | after the L837 fix, put the door flush at the new face |
| column cores | electrical photo: the pier between living windows A and B has a concrete core of about 30 x 68 inside an outline of about 45 x 89 | pier 42 x 81 as one wall box | the core is structural and hidden. No change |
| entry wall thickness | 28 | 20 | hidden by the lobby mass. No change |
| L835 comment | n/a | says "TV wall (13 cm)" but the code is 14.5 | comment only |

No model wall was found that is absent from the plan. The jog (L850), the pipe box and the laundry stub wall (L845) all
appear on the plans.

## 7. Proposed changes (not applied)

1. **TV wall corridor section** (L837).
   - Change `W(2.97, 9.30, -0.145, 0);` to `W(2.97, 4.15, -0.19, 0); W(4.15, 9.30, -0.145, 0);`.
   - Move these from z -0.145 to -0.19 (shift every z by -0.045):
     - the switch plate `['n', -.145, 3.02]` on L943
     - the panel, its slot and the comms box on L1613-1615
     - the display on L1616
   - Unaffected:
     - The corridor drop ceiling (L857, L895) only overlaps inside the wall, so it stays hidden.
     - roomdims probes: corridor at x 1.18, master at x 5.72.
   - Re-run `clearance_audit.py`. The corridor is 105.5 there, against the 0.90 minimum.
2. **Entry door rough opening** (L829).
   - `W(1.19, 1.585, ...)`, `W(1.585, 2.555, ..., DOORH)`, `W(2.555, 4.26, ...)`.
   - Leaf on L904: `B(1.565, 2.575, ...)`.
   - Frame on L941: jambs `[1.535, 1.585]`, `[2.555, 2.605]`, head `1.535..2.605`.
   - Intercom on L906: move to x `2.64..2.74`.
   - Switch on L943: move `['n', 5.50, 1.53]` to `1.49`.
   - No roomdims effect.
3. **Room 2 door west jamb.**
   - Change 0.88 to 0.93 on L811 (floor strip), L841 (both W calls) and L933 (doorFrame).
   - Leaf width on L914: `.87` to `.82`. The hinge stays at 1.76.
   - No roomdims effect.
4. **Balcony north wall inner face** (L1527): `BZ1 = .30` to `.34`. This shortens the deck by 4 cm. Check that the
   balcony furniture still clears.
5. Comment fix on L835: "13 cm" to "14.5 cm".
