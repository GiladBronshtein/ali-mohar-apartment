# Plumbing and AC sheets vs model (recheck, 2026-10-04)

Sources: `materials/plans/originals/plumbing_IMG_8066.jpg` and `ac_IMG_8067.jpg` (HADA, 1:75 on A3, 5712x4284, photographed at an angle).
Model: `source/salon.html` (2284 lines), line numbers as of this audit. Read-only: nothing in the model was changed.

Method: crops with full-resolution pixel gridlines (`pl_crops/*_grid.jpg`), registered per room on two drawn walls whose model
coordinates are known. Local scale 2.19 to 2.29 px/cm (perspective and paper folds); scaled positions are good to about
5 to 10 cm, written dimensions are exact.

Value types: **W** = written dimension or height on the sheet, **L** = label text (type, height "H-xx"), **S** = scaled from
the drawing (estimate). Tolerance: W within 3 cm OK, S within 10 cm OK.

Coordinates: metres, x east, z south, y up. Model ceiling H = 2.60 is an estimate (see Mamad).

## Summary of discrepancies (most important first)

| # | Item | Plan | Model | Diff | Type | Line |
|---|------|------|-------|------|------|------|
| 1 | Living supply grilles 90x15, centres x | ~2.20, ~5.76 | 3.60, 6.40 | -140, -64 cm | S | 1068 |
| 2 | Rooms 1 and 2 grilles | combined grille 80x20 in wall opening 85x25 | 90x15 | +10 w, -5 h | W | 864-866 |
| 3 | Mamad 8" sleeves, x | ~-1.50 to -1.65, ~-0.92 to -1.00 | -1.80, -1.37 | +20 to +30, +40 cm | S | 870 |
| 4 | Family bath tub width | 70 (35+35) | 77 | +7 | W | 1379-1380 |
| 5 | Family bath tub taps | on the south (corridor) wall, mixer 35 from east wall, filler 20 | on the east wall, north half | layout | W+L | 1381-1384 |
| 6 | Family bath basin axis to south wall | 72 | 63 | -9 | W | 1402-1403 |
| 7 | Balcony floor drains | (~9.03, ~1.4 to 1.6), (~9.08, ~7.15 to 7.5) | (8.6, 2.0), (8.6, 6.9) | about 45 cm in x | S | 1642 |
| 8 | Balcony garden tap height | H-60 | .80 | +20 | L | 1641 |
| 9 | Mamad pressure-relief sleeve 4" | c.l. 25 cm under ceiling, with blast and relief valve | missing | | W+L | |
| 10 | Ensuite shower drain | point drain at the tray centre, 50 from north wall | linear drain at north wall | type/position | W | 1302 |
| 11 | Ensuite basin axis to south wall | 44 | 40 | -4 | W | 1318-1320 |
| 12 | Niche floor drain (11) | at ~(3.85, -4.31) | missing | | S | |
| 13 | AC condenser in niche | outline ~132 x 55 at x 2.33..3.65, z -5.10..-4.55 | 89 x 34 at x 2.30..3.19, z -5.25..-4.91 | larger, 35 cm further south | S | 1421 |
| 14 | Column 2 (Ø110) location | NW corner of family bath (plumbing) vs SW corner (sales plan) | SW corner | sheets disagree | S | 1412 |

## Mamad (room 3)

Registration (AC sheet): east wall inner face px 1575 = x -0.25, north wall inner face py 1600 = z 0.125, south wall
py 2200 = z 2.745. Door opening on the sheet scales to x -1.93..-1.205 (model -1.98..-1.19): registration checks out.

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| 8" sleeves (2, supply + return, civil-defence standard), top below ceiling | W "o.k.= 10 cm מהתקרה" | top H-.10 | 0 | OK | 870 |
| 8" sleeve diameter | W ø8" | r .10 (Ø20) | 0 | OK | 870 |
| Sleeve 1, x | S -1.48 (AC), -1.65 (plumbing leader) | -1.80 | +17 to +32 | MISMATCH (S) | 870 |
| Sleeve 2, x | S -0.92 (AC, red line through the wall), -1.00 (plumbing leader) | -1.37 | +37 to +45 | MISMATCH (S) | 870 |
| Filter sleeves 4" (Rainbow 54R), lower | W "c.l.=150cm מהרצפה" | 1.50 | 0 | OK | 1607 |
| Filter sleeves 4", upper | W "c.l.= 30 cm מהתקרה" | H-.30 | 0 | OK | 1607 |
| Filter unit on west wall, centre z | S 2.37 (box z 2.19..2.55) | 2.335 | -3.5 | OK | 1604-1607 |
| Filter power | L 0.1 kW 1ph | socket h 2.20 | | not on sheet (height) | 1608 |
| Pressure-relief sleeve 4" with blast valve | W "c.l.= 25 cm מהתקרה", L "שסתום הדף ושחרור לחץ"; probable symbol at x ~-0.52 on the north wall (box on the mamad face, Π on the corridor face) | missing | | MISSING | |
| "H=2.63" (three labels: AC sleeve, air sleeve, filter air intake 4") | L H=2.63 | H 2.60 | +3 | see note | 227 |

Note on H=2.63: the three items it is attached to have different offsets from the ceiling on the AC sheet (10 cm top,
25 cm c.l., 30 cm c.l.), so it cannot be each item's own axis height. The consistent reading is the reference ceiling
height in the mamad, 2.63. The model's H = 2.60 is an estimate and sits 3 cm lower (edge of tolerance). Since every sleeve
in the model is placed relative to H, nothing breaks; if H is raised to 2.63 the sleeves follow. This is an interpretation,
not a written ceiling height.

Settled: the 8" sleeve height is correct (top 10 cm under the ceiling). The sleeve x positions are not: on both sheets
one sleeve sits over the east part of the door and the other about 25 cm east of the door jamb, not both over the door.

## Corridor and living (AC)

Registration: as for the mamad (same sheet area); facade inner face px 3245 = x 7.28 (2.22 px/cm along x).

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| Corridor drop, net height | W "הנמכה נדרשת h=25cm (netto)" | DROP = H-.25 | 0 | OK | 855 |
| Corridor drop, west end x | S -2.07 | -2.12 | -5 | OK | 857 |
| Corridor drop, east end x | S 4.08 | 4.15 | +7 | OK | 857 |
| Return grille size | W ת.א.ח 80x60 | 80 x 60 | 0 | OK | 861 |
| Return grille centre | S (2.24, -0.77) | (2.20, -0.70) | -4, +7 | OK | 861 |
| Living bulkhead depth (south edge z) | S 0.74 | 0.80 | +6 | OK | 1067 |
| Living bulkhead east end x | S 7.10 | 7.06 | -4 | OK | 1067 |
| Living supply grilles size | W מ.א.ק 90X15 (two) | 90 x 15 | 0 | OK | 1068 |
| Living grille 1 centre x (middle airflow arrow) | S 2.19 | 3.60 | +141 | MISMATCH (S) | 1068 |
| Living grille 2 centre x (drawn rectangle 2810-3020 px, 94 cm) | S 5.76 | 6.40 | +64 | MISMATCH (S) | 1068 |
| Rooms 1/2 supply grilles | W "תריס משולב 80x20 עם להבי הטייה פנימיים, פתח בקיר 85x25" | 90 x 15 | +10 w, -5 h | MISMATCH (W) | 864-866 |
| Room 1 grille centre x (red X in the wall over the door) | S -1.60 | -1.65 | -5 | OK | 864 |
| Room 2 grille centre x | S 1.32 | 1.32 | 0 | OK | 864 |
| Ducts | L ø10" main, ø8" branches in the drop | not modelled (hidden) | | n/a | |

The model comment at L863 ("90 x 15 as on the AC plan") took the living-room spec for rooms 1 and 2. The sheet gives only
two 90x15 grilles, both on the living bulkhead. Grille 1 sits near the corridor passage (x 1.99..2.97), grille 2 over the
east half of the TV wall.

## Family bath (kids')

Registration (plumbing sheet): bath walls x 2.01 / 4.46, z -3.775 / -1.395.

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| WC axis to window wall | W 44 | 42 | -2 | OK | 1389 |
| WC type | L "מיכל הדחה גבוה" (high cistern) | wall-hung on concealed-cistern ledge | | type note | 1388-1389 |
| WC projection | S ~63 | 73 | +10 | borderline (S) | 1389 |
| Basin axis to south (corridor) wall face | W 72 | 63 | -9 | MISMATCH (W) | 1402-1403 |
| Vanity extent z | S -2.58..-1.60 | -2.705..-1.665 | | within 10 (S) | 1398-1401 |
| Basin labels | L condensate drain "ניקוז מזגן עילי" at the basin | | | info | |
| Tub width | W 35 + 35 (tub west edge to mixer axis to east wall) = 70 | 77 | +7 | MISMATCH (W) | 1379-1380 |
| Tub mixer | W 35 from east wall (x 4.11) on the south wall, L "אינטרפוץ 4 דרך H-85" | east wall, filler at z -2.155 | | MISMATCH (layout) | 1382 |
| Tub filler | W 20 from east wall (x 4.26), L "אביק אוטומטי פיית מילוי פנימית" (fills through the overflow, no spout) | wall spout, east wall | | MISMATCH | 1382 |
| Hand shower rail | L "מוט+מזלף תחילת מוט H-150", south wall end | east wall z -2.665, .9-1.7 | | MISMATCH | 1383 |
| Water point | L "נקודת מים H-85" | | | info | |
| Glass screen | not drawn at the north end; taps are at the south end | north end x 3.68, z -2.98..-2.18 | | follows taps | 1381 |
| Corridor wall thickness | W 15 | 15 | 0 | OK | 843 |
| Column 2 Ø110 | S box ~18 x 16 at NW corner (x 2.01..2.19, z -3.775..-3.60), above the WC | box at SW corner (x 2.01..2.20, z -1.605..-1.395) | | CONFLICT between sheets | 1412 |
| Ceiling drop for AC unit | W "הנמכה בגובה 50" (AC sheet), "-50" (plumbing) | BC = H-.50 | 0 | OK | 856 |
| Access hatch | W 60x60 | 60 x 60 | 0 | OK (position not on sheet) | 1365 |
| Washer axis to east wall | W 35 | 32 | -3 | OK | 1338 |
| Washer water / drain | L water H-110, drain H-65 | not modelled | | info | |

The sales plan places the pipe box at the SW corner, the plumbing sheet labels column 2 at the NW corner by the window.
Ask the contractor; the model follows the sales plan.

Caveat for the tub change: with taps on the south wall the screen belongs at the south end, next to the door. The door
leaf hinges at x 3.68 (L915) and opens along that line, so a screen at x 3.75, z -2.20..-1.395 sits 3 to 7 cm from the open
leaf. Run `clearance_audit.py` after the change.

## Ensuite (master bath)

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| WC axis to ensuite/closet partition | W 60 | 60 (6.85 - 6.25) | 0 | OK, settled | 1308-1310 |
| WC type | L "מיכל הדחה נמוך" (low cistern, floor standing) | wall-hung on ledge | | type note | 1309, 1312 |
| Shower tray | W 106 x 92 | 106 x 92 | 0 | OK | 1300 |
| Shower drain | W point drain, "50" from north wall, at the tray centre in x: ~(5.16, -4.48) | linear drain at north wall z -4.95..-4.89 | ~45 cm, type | MISMATCH | 1302 |
| Mixer from north wall | W 35+15 = 50 | 49 | -1 | OK | 1306 |
| Mixer height | L "אינטרפוץ 4 דרך למזלף ומוט H-105" | 1.05 | 0 | OK | 1306 |
| Hand-shower rail point from north wall | W 35 | ~22.5 | -12.5 | minor (W vs S model) | 1305 |
| Shower head | L "ראש טוש H-210" | 2.05 | -5 | minor | 1304 |
| Basin axis to south wall z -3.26 | W 44 | 40 (centre -3.66) | -4 | MISMATCH (W, small) | 1318-1320 |
| Basin tap / waste | L "ברז פרח חמ/קר H-60", "מרכז ביוב H-50 לארון תלוי" | tap 1.02 on wall | | info (basin-mounted tap in model) | 1319 |
| Vanity | S ~79 x 54 | 70 x 50 | | within S tolerance | 1316 |
| Partition door | dashed opening in the lower part of the partition | door z -4.06..-3.36 | | OK | 848 |

## Master bedroom (AC)

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| Wall split | L "מזגן עילי לתפוקה 12,300 BTU/hr 1.0 kw 1ph, דירוג אנרגטי A" | split on west wall by the door | | capacity only; position is an estimate | 1617-1618 |
| Condensate | L "ניקוז מזגן עילי" (plumbing) in the corridor outside the bath door and at the bath basin | comment says drain to the corridor | | OK | 1617 |

## Laundry niche (מסתור)

Registration (AC sheet): niche inner faces px 2110 = x 2.15, px 2600 = x 4.37, py 500 = z -5.11, py 745 = z -3.99.

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| Facade openness | L "מסתור פתוח 80% נטו למעבר אויר" | louvers x 2.15..3.65 | | info | 1419 |
| Condenser outline | S x 2.33..3.65, z -5.10..-4.55 (132 x 55) | x 2.30..3.19, z -5.25..-4.91 (89 x 34) | east end -46, south face -36 | MISMATCH (S) | 1421 |
| Isolator | L "3x16 IP65" at the condenser west end | not modelled | | info | |
| Water heater centre | S (4.00, -4.69) AC, (3.91, -4.68) plumbing; Ø ~57 | (4.04, -4.80), Ø 54 | z +11 to 12 | borderline (S) | 1424 |
| Niche floor drain "ניקוז מסתור" (11) | S ~(3.85, -4.31) (hatched circle on both sheets) | missing | | MISSING | |
| Column 1 Ø110 | S NE corner ~(4.08, -5.1) | missing | | MISSING (likely boxed in the corner) | |
| Gutter drain 4" (4) "ניקוז תעלה צ.מ.ג" | S ~(2.1 to 2.2, -4.6 to -4.97) at the west wall | missing | | MISSING (minor) | |

## Balcony

Registration (AC sheet): facade outer face px 3300 = FO 7.70; north inner face py 1630 = z 0; south inner face py 3580 =
BZ2 8.71 (2.24 px/cm).

| Item | Plan value | Model value | Diff | Verdict | Line |
|------|-----------|-------------|------|---------|------|
| Gas point x | W 60 from FO = 8.30 (AC sheet S 8.35) | 8.30 | 0 | OK | 1640 |
| Gas point height | L "נקודת גז H-30" | .30 | 0 | OK | 1640 |
| Garden tap x | W +20 = 8.50 (AC sheet S 8.56) | 8.50 | 0 | OK | 1641 |
| Garden tap height | L "ברז גן ½" H-60" | .80 | +20 | MISMATCH | 1641 |
| Floor drain 1 | S AC (9.01, 1.38), plumbing (9.03, 1.6) | (8.6, 2.0) | x -43, z +40 to +60 | MISMATCH (S) | 1642 |
| Floor drain 2 | S AC (9.11, 7.15), plumbing (9.06, 7.5) | (8.6, 6.9) | x -48, z -25 to -60 | MISMATCH (S) | 1642 |
| Rainwater drains 4" (1, 2) | L "ניקוז מרפסת 4"" at the NW and SW balcony corners | not modelled | | info | |

The two sheets agree that the drains sit on the balcony centre line (about x 9.05); they differ by 20 to 35 cm in z, so z
is good to about ±20 cm only.

## Kitchen

No sink, water or drain points are drawn on the plumbing sheet. Column 3 Ø110 and balcony drain 13 are on the lobby side of
the kitchen west wall by the FS cabinet; "1050 1050" are the lobby meter cabinets. Model sink (x 4.85..5.65, L1158-1208) is
not verifiable from these sheets.

## Plan elements missing from the model (model coordinates, S unless noted)

| Element | Position | Notes |
|---------|----------|-------|
| Mamad pressure-relief sleeve 4" with blast valve | x ~-0.52, z 0..0.125 (north wall), axis H-.25 (W) | position S, low confidence on which symbol |
| Niche floor drain (11) | (3.85, -4.31), floor | |
| Column 1 Ø110 | ~(4.08, -5.1), niche NE corner | |
| Gutter drain 4" (4) | ~(2.15, -4.7), niche west wall | |
| Condenser isolator 3x16 IP65 | niche, west end of the condenser, ~(2.35, -4.95) | |
| Combined grilles 80x20 rooms 1/2 | replace the 90x15 at the same centres | W |

## Unreadable or unresolved

- `[א]` in a double box appears in rooms 1, 2, master and the mamad, free-standing about 1 m from the walls. No legend on
  the sheet. Probably a zone controller or thermostat tag; not modelled.
- "S" in a box on the living side at about (4.46, 0.25) beside the master door corner. Unidentified (AC sheet).
- Red X across the master door opening (x 4.15..4.26, z ~-1.03..-0.22). Same symbol as the room 1/2 grille openings, but
  no label; possibly a transfer grille over the master door.
- A short vertical dimension near the second 8" sleeve reads "25" or "125" (AC px ~1440, 1605). Not resolved.
- Ducts ø10" / ø8" routing is drawn but hidden behind the drop in the model; not compared.
- Lobby items (stairs 252/118, door 105, "ד.א." 30/30) are outside the apartment and were not compared.
- Family bath glass-screen position is not drawn; it follows the tap wall.

## Proof crops (`pl_crops/`)

Plumbing: `pl_ensuite_wc_60`, `pl_ensuite_shower_106x92`, `pl_ensuite_basin_44`, `pl_bath_wc_44`, `pl_bath_basin_72`,
`pl_bath_tub_35_35`, `pl_bath_tub_taps_15_20`, `pl_bath_west_wall`, `pl_baths_overview`, `pl_niche_drain_column1`,
`pl_balcony_labels`, `pl_balcony_labels2`, `pl_balcony_drains`, `pl_mamad`, `pl_mamad_H263_rot`, `pl_kitchen`,
`sales_bath_column`.
AC: `ac_mamad_sleeves`, `ac_mamad_north_sleeves_grid`, `ac_mamad_relief_sleeve_grid`, `ac_mamad_filter_grid`,
`ac_filter_rainbow_note`, `ac_mamad_filter_label_rot`, `ac_corridor_west`, `ac_corridor_east_drop25`,
`ac_living_grille_left`, `ac_living_grille_right`, `ac_rooms12_combined_grille`, `ac_unit_block`,
`ac_niche_condenser_grid`, `ac_master`, `ac_balcony_drain1`, `ac_balcony_drain2`, `ac_balcony_gas_tap`,
`ac_balcony_north`.
Grid crops carry full-resolution pixel coordinates (magenta every 100 px).

## Proposed code changes (not applied)

1. L1068: `[3.60, 6.40]` to `[2.20, 5.75]` (S).
2. L864-866: rooms 1/2 grilles to 80 x 20 (`c ± .40`, height `DROP + .02 .. DROP + .22`; wall opening 85x25), fix the L863
   comment. Check the grille still clears the door head (DOORH 2.10, DROP 2.35 at H 2.60).
3. L870: `[-1.80, -1.37]` to `[-1.55, -0.95]` (S). The second sleeve leaves the door span; the bookcase below it tops out at
   2.22, the sleeve bottom is H-.30 = 2.30, no clash.
4. L1379-1380: tub `B(3.76, 4.46, ...)`, inner `3.85..4.37` becomes `3.84..4.38` with the new apron; L1381-1384: move
   mixer to the south wall at x 4.11, y .85; drop the wall spout (overflow filler at x 4.26); rail on the south wall from
   y 1.50; screen and rain head to the south end.
5. L1402: basin `B(2.13, 2.41, -2.265, -1.965, ...)`, inner `-2.235..-1.995`; L1403 tap `-2.125..-2.105` (centres the basin
   under the mirror at -2.185 within 7 cm).
6. L1642: `[[9.05, 1.5], [9.08, 7.3]]` (S).
7. L1641: garden tap `y .57..63`, spout `C(8.50, BZ2 - .08, .54, .60, ...)`; update L1637 comment (h=60).
8. Add the mamad relief sleeve 4" at x ~-0.52, axis H-.25, on the north wall.
9. L1302: replace the linear drain with a point drain at local x 4.97 (5.16 after the .19 shift), z -4.48.
10. L1318-1320: ensuite basin, tap and mirror z -.04 only (shifting the whole vanity would hit the shower glass at z -4.045).
11. Niche: add floor drain at (3.85, -4.31); optionally enlarge the condenser towards 132 x 55 footprint (52000 BTU unit, size
    an estimate) and move the heater z to about -4.70.
12. Column 2: ask the contractor (plumbing NW vs sales plan SW).
