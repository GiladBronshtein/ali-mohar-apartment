# Audit 2: salon.html model vs architect plans

Date: 2026-10-03. Read-only audit. Nothing outside `audit2/` was modified.

## 1. Sources and method

* **plan.pdf** is a single raster image (2480 x 1754 px, 150 ppi JPEG embedded in an A3 page). It has **no vector text**
  (`pdftotext` returns nothing), so every number was read visually from the native image (`img-000.png`), cropped and
  zoomed (crops `crop_*.png`, tick close-ups `tiles1.png`, `tiles2.png`). Rasterizing at 300 dpi adds no detail
  beyond the 150 ppi source.
* Plan note (bottom of sheet, Hebrew): dimensions are gross construction dimensions, wall to wall (concrete/block,
  no plaster), **except the balcony, where dimensions are measured from the outer wall**.
* Written numbers on plan.pdf: exactly 21. No wall thicknesses, door widths, window widths or heights are written.
  Those were only **scaled** from the drawing (see 3 and 4).
* Model: wall boxes parsed from `// WALLS:` section of salon.html (L754-L790) plus the living-facade piers B(FX,FO,..)
  (L770) and the balcony B() blocks (L1441-1447). Constants: H=2.60, HEAD=2.30, DOORH=2.10, FX=7.28, LZ=8.79 (L220);
  FT=2.70, FO=7.70 (L769). Model axes: x = plan downward (east), z = plan leftward (south).
* Model values computed by ray casting from a probe point inside each room to the nearest wall-box faces at y=0.5 m
  (`measure.py`, output `measure_out.txt`). Not hand-typed.
* Plan-to-model registration for scaled checks: model wall boxes were fitted to the plan wall fill (`fit.py`):
  plan px u = 1373.25 - 79.0 z, v = 457.5 + 79.0 x (0.79 px/cm, 1 px = 1.27 cm). Overlays: `ov_*.png`
  (red = full-height wall box, orange = wall below an opening, blue = wall above an opening).
* Scaled-value confidence: the drawing itself is not uniformly to scale. Drawn tick-to-tick spans give 0.794-0.796 px/cm
  in the living area (879, 728, 884) but 0.809-0.814 px/cm in the mamad and family bath (262, 238, 245). So scaled
  values carry about +-5 cm uncertainty and are never given an OK/MISMATCH verdict at the 1 cm level; they are only
  used to flag large or topological differences.

## 2. Written dimensions on plan.pdf vs model (verdict: OK if |diff| <= 1 cm)

Pixel positions are in the native plan image (img-000.png, origin top-left).

| ID | Plan (cm) | Where on plan | What it measures | Model (cm) | Model faces (wall element, salon.html line) | Diff (cm) | Verdict |
|---|---|---|---|---|---|---|---|
| D1 | 262 | Room 3 / mamad (top-left room next to stairs), horizontal, text at px (1260,305) | mamad net width: mamad north wall (corridor side) to staircase wall | 262.0 | z=0.125 [W(-1.19, -0.25, -0.145, 0.125) @L788] to z=2.745 [W(-4.28, -0.25, 2.745, 5.77) @L765] | +0.0 | OK |
| D2 | 355 | mamad, vertical, text at px (1318,290) | mamad net depth: west facade (window wall) to mamad/storage-alcove wall | 355.0 | x=-3.800 [W(-4.28, -3.80, 1.44, 2.78) @L761] to x=-0.250 [W(-0.25, 0, 0.125, 2.775) @L789] | +0.0 | OK |
| D3 | 274 | Room 1 (top-right room), vertical, text at px (1565,255) | room 1 net depth: west facade to room 1/room 2 wall | 274.0 | x=-3.890 [W(-4.28, -3.89, -5.035, -2.92) @L760] to x=-1.150 [W(-1.15, -0.97, -5.035, -1.425) @L778] | +0.0 | OK |
| D4 | 361 | Room 1, horizontal, text at px (1625,305) | room 1 net width: corridor wall to north facade | 361.0 | z=-5.035 [W(-4.28, -1.14, -5.39, -5.035) @L757] to z=-1.425 [W(-2.36, -2.12, -1.425, -0.80) @L763] | +0.0 | OK |
| D5 | 282 | Room 2 (right, middle), vertical, text at px (1565,490) | room 2 net depth: room1/room2 wall to room2/bath wall | 282.0 | x=-0.970 [W(-1.15, -0.97, -5.035, -1.425) @L778] to x=1.850 [W(1.85, 2.01, -3.80, -1.245) @L780] | +0.0 | OK |
| D6 | 356 | Room 2, horizontal, text at px (1625,550) | room 2 net width: corridor wall to north facade | 356.0 | z=-5.010 [W(-1.14, 0.27, -5.39, -5.01) @L757] to z=-1.450 [W(-0.97, 0.88, -1.45, -1.245) @L779] | +0.0 | OK |
| D7 | 277 | Dining / storage alcove, horizontal, text at px (1263,550) | dining zone width: staircase wall face to dining/corridor partition | 277.5 | z=0.000 [W(-0.25, 1.99, -0.145, 0) @L790] to z=2.775 [W(-0.25, 1.45, 2.775, 5.77) @L765] | +0.5 | OK |
| D8 | 110 | Corridor, horizontal, text at px (1428,550) | corridor net width: dining/corridor partition to bedroom-side corridor wall | 110.0 | z=-1.245 [W(-0.97, 0.88, -1.45, -1.245) @L779] to z=-0.145 [W(-0.25, 1.99, -0.145, 0) @L790] | +0.0 | OK |
| D9 | 728 | Living, vertical, text at px (1318,745) | living depth: mamad/alcove wall face (x=0) to living facade inner face | 728.0 | x=0.000 [W(-0.25, 0, 0.125, 2.775) @L789] to x=7.280 [facade B(FX,FO,-0.13,0.78,0,2.7) @L770] | +0.0 | OK |
| D10 | 879 | Living+kitchen, horizontal, text at px (1025,867) | living+kitchen width: TV wall face to kitchen outer (south) wall | 879.0 | z=0.000 [W(2.97, 9.30, -0.145, 0) @L775] to z=8.790 [W(3.59, 7.70, 8.79, 9.11) @L767] | +0.0 | OK |
| D11 | 365 | Kitchen, vertical, text at px (830,885) | kitchen depth: kitchen/lobby wall to living facade inner face | 365.0 | x=3.630 [W(1.19, 3.63, 5.70, 9.11) @L765] to x=7.280 [facade B(FX,FO,7.7,8.39,0,1.0) @L770] | +0.0 | OK |
| D12 | 245 | Family bath, vertical, text at px (1565,720) | family bath net depth: room2/bath wall to bath/master wall | 245.0 | x=2.010 [W(1.85, 2.01, -3.80, -1.245) @L780] to x=4.460 [W(4.46, 4.61, -3.23, -1.37) @L784] | +0.0 | OK |
| D13 | 238 | Family bath, horizontal, text at px (1578,752) | family bath net width: corridor wall to bath/laundry-niche wall | 238.0 | z=-3.775 [W(2.37, 3.55, -3.99, -3.775, 0, 1.05) @L782] to z=-1.395 [W(2.01, 2.86, -1.395, -1.245) @L781] | +0.0 | OK |
| D14 | 296 | Master bedroom, horizontal, text at px (1500,867) | master net width: TV wall to master/ensuite partition | 296.0 | z=-3.105 [W(4.61, 6.85, -3.26, -3.105) @L785] to z=-0.145 [W(2.97, 9.30, -0.145, 0) @L775] | +0.0 | OK |
| D15 | 430 | Master bedroom, vertical, text at px (1565,990) | master net depth: bath/master wall to east facade inner face | 430.0 | x=4.610 [W(4.46, 4.61, -3.23, -1.37) @L784] to x=8.910 [W(8.91, 9.30, -5.01, -2.27) @L774] | +0.0 | OK |
| D16 | 172 | Ensuite (master shower room), horizontal, text at px (1698,867) | ensuite net width: partition to north facade | 172.0 | z=-4.980 [W(4.63, 5.99, -5.39, -4.98) @L758] to z=-3.260 [W(4.61, 6.85, -3.26, -3.105) @L785] | +0.0 | OK |
| D17 | 222 | Ensuite, vertical, text at px (1680,912) | ensuite net depth: bath/ensuite wall to ensuite/closet wall | 222.0 | x=4.630 [W(4.37, 4.63, -5.39, -3.99) @L784] to x=6.850 [W(6.85, 7.01, -4.98, -4.06) @L786] | +0.0 | OK |
| D18 | 190 | Walk-in closet, vertical, text at px (1680,1092) | closet net depth: ensuite/closet wall to east facade inner face | 190.0 | x=7.010 [W(6.85, 7.01, -4.98, -4.06) @L786] to x=8.910 [W(8.91, 9.30, -5.01, -2.27) @L774] | +0.0 | OK |
| D19 | 175 | Walk-in closet, horizontal, text at px (1698,1120) | closet net width: closet/bedroom partition to north facade | 175.0 | z=-4.995 [W(7.01, 8.91, -5.39, -4.995) @L758] to z=-3.245 [W(8.32, 8.91, -3.245, -3.105) @L785] | +0.0 | OK |
| D20 | 884 | Balcony, horizontal, text at px (1033,1220); ticks at px u=681.7 (south balcony wall inner face) and u=1381.7 (outer slab line on the master side, beyond the end of the balcony/master wall) | balcony length: south balcony wall inner face to the outer edge on the north side | 887.0 | z=8.740 [B(BX1,BX2,BZ2,9.11) @L1444] to z=-0.130 [B(BX1,BX2,-.13,BZ1) outer face @L1444]; clear deck BZ1..BZ2 = 0.30..8.74 = 844 cm | +3.0 | MISMATCH |
| D21 | 275 | Balcony, vertical, text at px (1310,1180); ticks at living facade outer face (px v=1066) and outer slab line (px v=1286) | balcony depth: living facade outer face to balcony outer edge | 270.0 | x=7.700 [FO, facade outer face @L769] to x=10.400 [BX2 @L1441] | -5.0 | MISMATCH |

Notes on D20/D21 (balcony):
* D21: ticks are at the living facade outer face (px v=1066, model x=FO=7.70) and at the outermost slab line
  (px v=1286, scaled x=10.48). The model balcony ends at BX2=10.40 (L1441), so the depth is 270, not 275.
* D20: ticks are at the inner face of the south balcony wall (px u=681.7, scaled z=8.75; model BZ2=8.74) and at the
  outermost slab line on the north side (px u=1381.7, scaled z=-0.11), which lies past the end of the balcony/master
  wall. On the same basis the model gives 8.74 - (-0.13) = 887 (+3). The usable deck in the model is only
  BZ1..BZ2 = 0.30..8.74 = 844 cm because the model's north balcony wall runs the full balcony depth (see 5).
  The model comment at L1439 says "BALCONY 275 x 884 (x 7.70..10.40, z 0.30..8.74)", but those coordinates give 270 x 844.

Count: 19 OK, 2 MISMATCH (D20, D21).

## 3. Openings: position, width, swing (scaled from plan, +-5 cm)

| Opening | Plan scaled (model coords) | Model | Width plan/model (cm) | Swing / hinge vs plan |
|---|---|---|---|---|
| Room 1 window, west facade | z -2.92..-1.92 | z -2.92..-1.93 (L760, windowZ L1360) | 100 / 99 | casement drawn; model fixed 2-pane frame |
| Room 2 window, north facade | x 0.28..1.28 | x 0.27..1.25 (L757, windowX L1381) | 100 / 98 | casement drawn |
| Mamad window, west facade | z 0.48..1.43 (visual) | z 0.47..1.44 (L761, windowZ L1435) | 95 / 97 | sliding blast window into wall pocket (plan); model has steel frame L1436 |
| Room 1 door | x -1.97..-1.26 jamb lines, about 84 wide (visual) | x -2.06..-1.23 (L777), leaf L849 | 84 / 83 | plan: hinge at south (plan-bottom) end, opens into room 1. Model same. OK |
| Room 2 door | x 0.91..1.80 | x 0.88..1.77 (L779), leaf L850 | 89 / 89 | plan: hinge at south end, opens into room 2. Model same. OK |
| Family bath door | x 2.87..3.66 (visual) | x 2.86..3.69 (L781), leaf L851 | 80 / 83 | plan: hinge at south end, opens into bath. Model same. OK |
| **Mamad blast door** | x -1.97..-1.20 (visual) | x -1.98..-1.19 (L788), leaf L853 | 77 / 79 | **plan: hinge at the NORTH/west end (x about -1.92, plan-top end of the opening), leaf opens 90 deg out across the corridor. Model: hinge at the SOUTH end (x -1.17) and opens 180 deg flat along the corridor wall. MISMATCH (hinge side).** Evidence `ev_mamad_door.png` |
| Master door | z -1.19..-0.31 | z -1.16..-0.34 (L787), leaf L852 | 89 / 82 | plan: hinge on TV-wall side (z about -0.39), opens into master. Model hinge z -0.35. OK |
| Ensuite door (from closet) | z -3.37..-4.04 (visual) | z -3.36..-4.06 (L786), leaf L854 | 67 / 70 | plan: hinge at partition side, opens into ensuite. Model same. OK |
| Closet opening to master | x 7.56..8.37 | x 7.54..8.32 (L785) | 81 / 78 | no door (both) |
| Family bath window to laundry niche | x 2.35..3.58 | x 2.37..3.55 (L782, windowX L1248) | 123 / 118 | |
| Ensuite window, north facade | x 5.98..6.61 | x 5.99..6.58 (L758, windowX L1208) | 63 / 59 | |
| Master window, east facade | z -2.32..-1.32 | z -2.27..-1.31 (L774, windowZ L1188) | 100 / 96 | casement drawn |
| Entrance door | x 1.56..2.51 | x 1.62..2.52 (L767, B L840) | 95 / 90 | plan: hinge at north end (x about 1.6), opens into apartment. Model shows closed leaf, handle at x 2.4 (consistent) |
| Balcony opening A | z 0.74..3.47 | z 0.78..3.45 (L770, slider L882) | 272 / 267 | 2-panel slider (both) |
| Balcony opening B | z 4.26..6.91 | z 4.26..6.88 (L770, slider L882) | 265 / 262 | 2-panel slider (both) |
| Kitchen window C | z 7.67..8.40 | z 7.70..8.39 (L770, slider L882) | 73 / 69 | plan (and pl_kitchen) draw a hinged sash; model a single fixed pane |
| Corridor to dining passage | x 1.96..3.00 | x 1.99..2.97 (L790/L775) | 104 / 98 | |

The scaled widths are systematically 2-5 cm larger than the model because the black jamb outline is counted as opening;
none of these differences is beyond the scaled uncertainty. Only the mamad door hinge side is a real discrepancy.
Sill and head heights are not on any plan (see 7).

## 4. Wall thicknesses and wall faces (scaled, +-3 cm; full list in `thickness_out.txt`)

All 45 floor-to-ceiling W() walls and facade piers were measured across the plan wall fill. Facades (38-42 cm),
partitions (11-18 cm), mamad walls (23-27 cm) agree within 4.3 cm. Differences beyond the scaled noise:

| Location | Plan (scaled) | Model | Note |
|---|---|---|---|
| West facade behind the room 1 wardrobe niche, W(-4.28,-3.90,-1.425,-0.50) L760 | inner face x about -3.81 (wall about 47 cm, contains the two drain pipes drawn as circled crosses) | inner face x=-3.90 (38 cm) | model niche about 8 cm deeper. `ev_wardrobe_niches.png` |
| TV wall, corridor section x 2.97..4.15, W(2.97,9.30,-0.145,0) L775 | corridor face z about -0.19 (about 18 cm; holds the electrical panel) | z=-0.145 (14.5 cm) | about 4 cm; borderline. Master section measures 12.7 cm |
| Balcony south wall, B(BX1,BX2,BZ2,9.11) L1444 | z 8.73..9.24 (about 51 cm), ends at x about 10.09 | z 8.74..9.11 (37 cm), runs to x 10.40 | outer face outside the apartment |

## 5. Elements missing in the model, extra in the model, wrong side

MISSING (on plan, not in model):
1. **Pipe/shaft box in the family bath** NW inner corner (dark square with a circled cross), scaled x 2.00..2.19,
   z -1.39..-1.61 (about 19 x 21 cm), at the junction of W(1.85,2.01,..) L780 and W(2.01,2.86,..) L781. `ev_bath_corner_pipe.png`
2. **TV-wall jamb thickening on the master side of the master door**: plan wall face steps out to z about -0.24 for
   x about 4.26..4.76 (about 9-10 cm deep, 50 cm long), below W(4.15,4.26,-0.34,-0.145) L787. Model has only the
   14.5 cm TV wall there. `ev_tvwall_panel_jog.png`
3. **Electrical panel (lightning symbol, also labeled on el_living / el_mamad_corr "apartment electrical panel with
   communications box below")** recessed in the TV wall on the corridor side, scaled x 3.37..3.78. No such object in
   the model (searched for panel/לוח). `ev_tvwall_panel_jog.png`

EXTRA / different shape (in model, not on plan):
4. **Balcony north wall runs the full balcony depth**: model B(BX1,BX2,-.13,BZ1,BY,2.70) L1444 is a full-height 43 cm
   block from x 7.70 to 10.40. On the plan this wall stops at the master facade line (x about 9.29); beyond it the
   balcony is open and the deck/edge lines continue north to about z 0.18 (deck) / -0.11 (outer line). This is why the
   model deck is 844 long where the plan dimension 884 applies. `ev_balcony_master_corner.png`
5. **Balcony south wall about 30 cm longer** in the model (to x 10.40) than on the plan (ends at x about 10.09).
   `ev_balcony_left_end.png`
6. Public areas (staircase, lobby) are filled as solid blocks W(-4.28,-0.25,2.745,5.77), W(-0.25,1.45,2.775,5.77),
   W(1.19,3.63,5.70,9.11) L765. Outside the apartment, does not change any room, noted only.

WRONG SIDE:
7. **Mamad blast door hinge** on the wrong end (see 3). doorLeaf(-1.17, -.19, 1, 0, ...) L853: plan hinge is at the
   opposite end of the opening, x about -1.92.

Checked and matching: all other doors swing into the rooms on the hinge side drawn; stub wall between tub and washer
(L783); laundry niche reached only through the bath window (L782); closet open to master without a door; master
door hinge on TV-wall side.

## 6. Extra dimensions from plans/*.png

Orientation of these photos is rotated relative to plan.pdf; mapped by matching rooms. No window widths, door widths
or sill heights are written on any of them.

| Item | Source | Plan value | Model | Diff | Verdict |
|---|---|---|---|---|---|
| Corridor gypsum ceiling drop | ac_corr ("הנמכה נדרשת h=25cm (netto)") | 25 net | DROP = H-0.25 (L792) | 0 | OK |
| Family bath ceiling drop for AC unit | ac_unit ("הנמכה בגובה 50 ס"מ"), pl_bath | 50 | BC = H-0.50 (L793, box L1278) | 0 | OK |
| AC access hatch | ac_unit ("פתח גישה 60x60") | 60 x 60 | 60 x 60 (L1279) | 0 | OK |
| Return-air grille | ac_corr ("ת.א.ח 80x60") | 80 x 60 | 80 x 60 (L798) | 0 | OK |
| Mamad sleeves | ac_corr ("2* שרוול פלדה Ø8", o.k.=10 cm מהתקרה") | 2 x 8 in, top 10 cm below ceiling | 2 x r 0.10 m, top at H-0.10 (L806) | 0 | OK |
| **AC supply grilles** | ac_corr ("מ.א.ק. 90X15", two) | 90 x 15 | 80 x 20 (L801-L803) | -10 / +5 | MISMATCH |
| **Ensuite shower zone** | pl_bath (106 along x from the bath wall, 92 along z from the facade); plan.pdf drawing scales about 108 x 95 | 106 x 92 | glass at x 5.60 and z -4.10 (L1211-L1214): 97 x 88 from the walls (comment says 100 x 91) | -9 / -4 | MISMATCH |
| **Ensuite WC axis to closet wall** | pl_bath ("60"); plan.pdf drawing scales 58 | 60 | 49 (WC centre x 6.36, wall 6.85; L1222-L1223) | -11 | MISMATCH |

Fixture and outlet offsets on pl_bath / el_* (for example 44, 72, 35, 46, 50, 13, 128, 218, 140, 228, 183, 147, H-xx heights)
were not audited beyond the three rows above; they are fixture positions, not architecture.

## 7. Unreadable or not verifiable

UNREADABLE:
* ac_corr: number "2.63" in faint grey background text next to the mamad sleeve note; the word before it cannot be read,
  so it is unknown what it measures (it could be a height; the model ceiling is H=2.60). `ev_ac_corr_263.png`
* ac_corr: "25" with an arrow next to the sleeve symbols, and "שרוול ... 25 cm" at the left edge; the text is cut by
  the crop edge, so its reference is unknown. `ev_ac_corr_left.png`
* pl_kitchen: "60" at the bottom right; the dimension line runs off the crop, so its far end is unknown.
  `ev_pl_kitchen_60.png`
* plan.pdf: faint dashed double symbol crossing the mamad/corridor wall at x about -0.55..-0.35 (`ev_mamad_wall_mark.png`).
  Possibly the ventilation sleeves, but not identifiable at 150 ppi. The model puts the sleeves above the door at
  x -1.80 / -1.37.
* All 21 numbers on plan.pdf are legible. "1050 1050" on pl_kitchen / el_kitchen belongs to the lobby meter cabinets,
  outside the apartment (not compared).

NOT VERIFIABLE (no value on any plan): window sills (rooms 1-2: 0.95, mamad 1.0, bath 1.05, ensuite 1.5, kitchen 1.0,
master 0 floor-length), window heads 2.0-2.20, interior door head 2.10, balcony door head 2.30, ceiling height 2.60,
mamad door head 2.0, balcony slab and railing heights.

## 8. Evidence files

* `img-000.png`: native plan raster. `overview_small.png`: half size.
* `crop_bedrooms_top.png`, `crop_corridor_baths.png`, `crop_living.png`, `crop_master_balcony.png`, `crop_entry_service.png`: 2x crops used to read the numbers.
* `tiles1.png`, `tiles2.png`: 6x close-ups of the dimension-line ends with the model walls drawn on top.
* `ov_bedrooms.png`, `ov_corridor_baths.png`, `ov_living.png`, `ov_balcony.png`, `ov_entry.png`: model walls over the plan.
* `ev_*.png`: evidence for each finding above.
* Scripts: `model.py` (parse walls), `measure.py` (section 2), `openings.py` (section 3), `thick.py` (section 4),
  `fit.py` (registration), `overlay.py`, `tiles.py`. Outputs: `measure_out.txt`, `openings_out.txt`, `thickness_out.txt`, `dims.json`.
