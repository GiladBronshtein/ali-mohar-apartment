# QA10 V1: does the model follow the plans? (independent verification, 2026-10-07)

Report only; no tracked file was edited. Model: `source/salon.html` at commit 6810263 (3542 lines; line numbers below are
from that file). Plans: `materials/plans/vector/{construction,plumbing,electrical,ac,kitchen}.pdf`, read on 300-600 dpi crops
with a model-coordinate grid and, for plumbing, electrical and AC, from the vector paths (`get_drawings`). All four sheets
were registered to the construction sheet on wall faces and agree within 1 cm:

| Sheet | PDF point = f(model x, z) |
|---|---|
| construction | X = 514.8 + 56.693 x, Y = 497.3 + 56.693 z |
| plumbing | X = 567.2 + 56.693 x, Y = 473.0 + 56.693 z |
| electrical (page.rect, rotated) | X = 691.6 + 56.693 x, Y = 470.2 + 56.693 z |
| AC | X = 622.3 + 56.693 x, Y = 464.5 + 56.693 z |

Priority used: construction plan 5/5/26 first, then plumbing, electrical, AC, sales plan. W = written on a sheet, S = scaled
(about +-2 cm on the vector sheets). KNOWN = already documented in PROJECT_MEMORY, recheck3/recheck5 APPLIED or the QA9
owner questions; listed, not re-raised. DELIB = moved off the plan on purpose by an earlier QA step.

Checks run today: `roomdims.py` +0 on every room (closet 485/175 = the known probe artifact); `clearance_audit.py` 0 issues.
Both are blind to finding G0 (see 3).

Evidence: key images copied to `audit/qa10/V1_img/`; the full sets stay in `/tmp/v1/` (geometry: `c_d_*.png`, `w_*.png`,
`img/*.jpg`), `/tmp/v1pl/` (plumbing) and `/tmp/v1el/` (electrical, AC) and are lost on reboot.

Status at the time of writing: the working tree (not this verifier) already holds an uncommitted fix for G0 (the six
walls on their own line after L1075) and the comment-stripping fix in `roomdims.py`. In that working copy every salon.html line
number after 1075 is one higher than quoted here.

## Summary of deviations

| # | Priority | Category | Deviation | Fix size |
|---|---|---|---|---|
| G0 | HIGH | walls | North facade x 6.015..9.30 (master bath window sill and lintel, closet north wall, NE corner) is not built: commented out by a misplaced `//` on L1075 since 40e8d72. Visible in `top` and every dollhouse view | one line |
| G1 | medium | windows | Room 1, room 2 and master E windows: the handle is on the hinge side (plan hinges S, E, S) | 2 functions + 3 calls |
| G2 | medium | windows | Kitchen window C: plan draws one inward side-hung sash hinged north; model has a slider | 3 lines |
| E1 | medium-high | electrical | Bath-door switch group in the corridor: 3 gangs, plan 4 (water-heater switch "4" with pilot and timer missing) | 1 line |
| E2, E3 | medium | electrical | Living switch 1bc and entry switch 1ad are 2-gang on the plan, single in the model | 1 edit |
| E5 | medium | AC | Family bath 60x60 access hatch 77 cm / 33 cm from the AC-sheet position | 2 lines |
| E6 = P3 | medium-low | AC | Second condenser (84x40) 44-45 cm west of its AC-sheet outline (found by both the plumbing and the electrical check) | 5 lines |
| P1 | medium | plumbing | Master shower head 9.5 cm north of the plan point (it belongs over the 4-way mixer at 50 from the north wall) | 4 lines |
| P4 | medium | plumbing | Balcony floor drains 16 cm too far west (x 8.89, plan 9.05-9.08) | 1 line |
| P2 | low-medium | plumbing | Niche 4" drain pipe 8 cm too far north (knock-on: AC isolator moves 5.5 cm) | 2 lines |
| E4 | medium-low | electrical | Family bath splash-proof socket 7.5 cm west (towel hooks follow) | 2 lines |
| G4 | low | doors | Master bath door gap 70, written 75 | 6 lines |
| G3 | low | doors | Entrance opening centred 3.5 cm west of the written rough opening | several lines |
| G7 | low | walls | Laundry niche opening east edge 3.65, written 3.685 | 4 places |
| G5, G6, E8 | low, optional | doors, electrical | Room 2 door 84 vs 82 (2.5 cm W), closet opening 78 vs 80, room 1 low socket 4 cm | small |
| E7 | decision | electrical | Water-heater point "4 IP65" 59 cm from the plan (QA9 moved it on purpose) | owner |

Fully matching: every door hinge side and swing direction (the lead's reading is confirmed for all seven leaves); every
window and balcony-door position, sill and head written on the construction plan; every written dimension sampled on the
walls apart from G0 and G7 (the 5-8 cm room-size difference to the construction plan is KNOWN: the model stays on the sales
plan); all written electrical heights (40, 60, 65, 110, 130, 140, 180, 200, 220); family bath and master bath WC and basin
axes, tub and tap positions and heights, shower drain; corridor and bath drops, grilles, master split, mamad sleeves, main
condenser.

Interactions between fixes: if G3 (entrance +3.5 cm) is applied, put the 2-gang 1ad of E3 at x 2.76, not 2.72 (plates
2.6775..2.8425 clear the moved frame at 2.64; the plan circle is at 2.79 on a box 2.64..2.89). P3 and E6 are the same
condenser: apply E6 (it moves the whole stand frame; P3 kept the west legs).

Docs to correct (not deviations of the model): PROJECT_MEMORY "electrical panel x (electrical sheet 3.01..3.40 ...)" is stale,
the vector sheet draws 3.37..3.78 = the model; QA9 owner question 12 should say the sheet has a timer switch for the water
heater in the corridor (E1) besides the IP65 point in the niche; QA9 owner question 13 ("window C type not written"): not
written, but drawn (G2).

## 1. Doors

Plan: `construction.pdf` (5/5/26), read on 400-600 dpi crops with a model-coordinate grid (calibration from recheck 3:
PDF pt X = 514.8 + 56.693 x, Y = 497.3 + 56.693 z, checked on wall faces here, residual about 1 cm). W = written, S = scaled.
Model: `doorLeaf(hx, hz, dx, dz, w, ..., cx, cz)` (open direction dx,dz; closed direction cx,cz) at salon.html L1197-1204,
wall gaps in the `// WALLS:` block, `FRAMES` L1149-1150. Plan-view captures: `/tmp/v1/img/t_nw_open.jpg`, `t_ne_open.jpg`,
`t_s_open.jpg` (doors open), `*_closed.jpg` (closed); plan crops `/tmp/v1/c_d_*.png`, `/tmp/v1/d_mbath.png`.

| Door | Plan opening (W/S) | Model opening | Plan hinge / swing / open leaf | Model hinge / swing / open leaf | Verdict |
|---|---|---|---|---|---|
| Entrance | W "105/210", rough x 1.58..2.63 (S), z 5.54 face | wall gap 1.585..2.555 (97), steel frame on the face 1.535..2.605, L1084, L1230 | hinge W (leaf S at x 1.64..1.69), opens N into the flat, leaf about 95 | closed slab only (L1184), handle at the E edge (L1186): hinge W implied; never shown open | Hinge OK. Opening centre 3.5 cm W of the plan (G3). Face z 5.50 vs 5.54: KNOWN (recheck 3, 3.10) |
| Mamad blast door | W "80", "2+200"; S x -1.98..-1.18 | -1.98..-1.19, lintel 2.00, L1106 | hinge W (x -1.91), opens N into the corridor, leaf drawn about 72 | hinge (-2.00, -0.195), opens N (0,-1), leaf 0.86 surface-mounted, L1203 | Hinge, swing OK. Leaf 86 vs drawn 72: KNOWN (recheck 3 3.5, recheck 5 Open). Head: "2+200" read as a 2 cm step + 200, model 2.00 over the corridor floor (1.98 clear from the mamad floor): INFO, 2 cm |
| Room 1 | W "82", "210"; chain 8 \| 82 \| 10 from the corridor W end: S -2.055..-1.23 | -2.06..-1.23 (83), L1094 | hinge E (x -1.27), opens N into the room, leaf along the E jamb | hinge (-1.24, -1.355), open (0,-1) N, closed (-1,0), L1197 | OK |
| Room 2 | W "82", "210"; chain 159 \| 82 \| 111: S 0.955..1.775 | 0.93..1.77 (84), L1096 | hinge E (x 1.72), opens N, leaf drawn 82 | hinge (1.76, -1.355), open N, L1198 | Hinge, swing OK. W jamb 2.5 cm W, gap 84 vs 82 (G5, minor) |
| Family bath | W "82", "210"; chain 111 \| 82 \| 48: S 2.875..3.70 | 2.86..3.69 (83), L1098 | hinge E (x 3.65), opens N into the bath, 90 deg | hinge (3.68, -1.315), opens about 85 deg N, L1199 | OK (85 deg so the lever clears the tub screen: design note, INFO) |
| Master | W "12 \| 82 \| 12", "210": S z -1.18..-0.36 in the x 4.17..4.29 wall | z -1.16..-0.34, wall 4.15..4.26, L1104 | hinge S (z -0.37), opens E into the master, leaf along the S jamb, about 78 | hinge (4.205, -0.35), open (1,0) E, closed (0,-1), leaf .80, L1202 | OK |
| Master bath (from the closet) | W "75/210": ticks z -4.06..-3.31 in the x 6.915..7.02 partition | z -4.06..-3.36 (70), L1103 | hinge S (z -3.38, bath face), opens W into the bath, leaf drawn about 64 | hinge (6.945, -3.365), open (-1,0) W, closed (0,-1), leaf .69, L1204 | Hinge, swing OK. Opening 70 vs written 75 (G4) |
| Closet opening (no leaf) | W "55 \| 80 \| 60" from the closet W face (plan 7.02): 7.57..8.37 | 7.54..8.32 (78), L1102 | open | open | Width 78 vs 80, E jamb 5 cm W (G6, minor) |
| Corridor-living passage (no leaf) | W "180 \| 120 \| 118": x 1.80..3.00 | 1.80..3.00, L1108, L1092 | open | open | OK |

The lead's reading of hinges and swings is confirmed for all seven leaves. Every leaf's open direction in the code matches the
plan (into the room for rooms 1, 2, family bath, master; west into the bath for the master bath; north into the corridor for
the mamad; into the flat for the entrance, which the model never opens).

## 2. Windows and balcony doors

Written values from the construction plan: east chain 310 \| 90 \| 152 \| 54 \| 270 \| 80 \| 270 \| 76 \| 70 from z -5.27; top chain
455 \| 90 \| 88 \| 154 \| 233 \| 60 \| 261 from x -4.185; west chain 246 \| 90 \| 239 \| 100 from z -5.27; UK/OK beside each opening.
Model: `windowX` / `windowZ` (L1023-1045), `slider` (L1278-1279), wall pieces in the `// WALLS:` block.

| Opening | Plan position (W) | Model position | Plan UK / OK (W) | Model sill / head | Plan type (drawn) | Model type | Verdict |
|---|---|---|---|---|---|---|---|
| Living door A | z 0.79..3.49 (270) | .79..3.49, L1087, L1279 | 0 / 235+35 | 0 / 2.35 | two sliders | two sliders | OK |
| Living door B | z 4.29..6.99 (270) | 4.29..6.99 | 0 / 235+35 | 0 / 2.35 | two sliders | two sliders | OK |
| Kitchen window C | z 7.75..8.45 (70) | 7.75..8.45 | 120 / 235+35 | 1.20 / 2.35 | ONE inward side-hung sash, hinge at the N jamb (z 7.78, x 7.30), swing arc to the S (crop `V1_img/g2_window_C_plan.jpg`) | two-sash slider, L1279 ("type not written, a slider like the others (estimate)") | DEVIATION (G2) |
| Master E window | z -2.17..-1.27 (90) | -2.17..-1.27, L1091, L1625 | 15 / 235+35 | .15 / 2.35 | one inward sash, hinge at the S jamb | one sash, handle at z -1.35 (S end = hinge side) | Position, heights OK; handle on the hinge side (G1) |
| Room 1 W window | z -2.81..-1.91 (90) | -2.81..-1.91, L1077, L1829 | 15 / 235+35 | .15 / 2.35 | one inward sash, hinge at the S jamb | one sash, handle at z -1.99 (S end = hinge side) | Position, heights OK; handle on the hinge side (G1) |
| Room 2 N window | x 0.365..1.265 (90) | .365..1.265, L1074, L1854 | 15 / 235+35 | .15 / 2.35 | one inward sash, hinge at the E jamb | one sash, handle at x 1.185 (E end = hinge side) | Position, heights OK; handle on the hinge side (G1) |
| Master bath N window | x 6.015..6.615 (60) | 6.015..6.615, L1647 | 125 / 235 | 1.25 / 2.35 | frame only, no sash drawn | one kip sash (d08) | OK. BUT the wall pieces under and over it are commented out (G0) |
| Family bath to laundry niche | 23 \| 120 \| 83: x 2.375..3.575 | 2.375..3.575, L1099, L1698 | 110 / 210 | 1.10 / 2.10 | two sliding sashes | sliding pair | OK |
| Mamad W window | z 0.48..1.48 (100) | .48..1.48, L1078, L1908 | 110 / 210 | 1.10 / 2.10 | blast window: outer steel leaf and inner frame, no sash swing drawn | one pane + steel blast frame | OK (type not drawn in detail: INFO) |
| Laundry niche N opening | 154: x 2.145..3.685 | 2.15..3.65 (louvres L1786, E wall L1075) | not written; "מעקה קל H=105" line at z -5.17 | full-height louvres at z -5.30 | light railing | louvres | E edge 3.5 cm short (G7, minor); railing vs louvres: KNOWN (recheck 3 open, AC sheet louvres) |

Hinged-sash frame depth (INFO, low): on the plan the frames of the three bedroom windows and window C sit at the inner face of
the wall (room 1 frame x -4.02..-3.93; room 2 z -5.10..-5.05; master E x 8.97..9.08; C x 7.30..7.38), so an inward sash can
swing. `windowZ` / `windowX` put the frame at the wall centre (room 1 x -4.09, room 2 z -5.20, master 9.11), 7 to 10 cm deeper.
Optional fix: add a frame-centre argument (`fc`) and use `const xc = fc ?? (xIn + xOut) / 2` (same for `zc`), called with
-3.975, -5.075, 9.025 for room 1, room 2, master E.

Not on any plan: outside safety bars on the master E window (L1626-1627, estimate; QA9 owner question 2, KNOWN).

## 3. Walls and room dimensions

`python3 roomdims.py` (today): every room +0 against the sales plan; closet 485/175 is the known probe artifact. 
`python3 clearance_audit.py`: 0 issues. Both tools are blind to G0: `roomdims.py` reads the `W(` calls with a regex and does
not strip `//` comments, so it still "sees" the commented-out north walls.

| Item | Plan (construction, W unless noted) | Model | Δ cm | Verdict |
|---|---|---|---|---|
| North facade x 6.015..9.30 (master bath window sill and lintel, master bath NE pier, bath/closet end, closet N wall, NE corner) | solid wall with the 60 window | NOT BUILT: the six `W(` calls sit after `//` on L1075 | | DEVIATION (G0, high) |
| Room 1 window reveal | -2.82..-1.91 (S) / 246 \| 90 | -2.81..-1.91 | 0..1 | OK |
| Room 2 window | 455 \| 90 → 0.365..1.265 | 0.365..1.265 | 0 | OK |
| Laundry niche opening | 88 \| 154 → 2.145..3.685 | 2.15..3.65 | 0 / -3.5 | G7 (minor) |
| Master bath window | 233 \| 60 → 6.015..6.615 | 6.015..6.615 | 0 | OK |
| Master E window | 310 \| 90 → -2.17..-1.27 | -2.17..-1.27 | 0 | OK |
| Living A / B / C | 270 \| 80 \| 270 \| 76 \| 70 | .79..3.49 / 4.29..6.99 / 7.75..8.45 | 0 | OK |
| Mamad window | 239 \| 100 → 0.48..1.48 | 0.48..1.48 | 0 | OK |
| Corridor-living passage | 180 \| 120 \| 118 → 1.80..3.00 | 1.80..3.00 | 0 | OK |
| Corridor S wall W of the passage | "10" | 14.5 (-0.145..0) | +4.5 | KNOWN (sales plan rule) |
| TV-wall stretch E of the passage | "20" | 19 (-0.19..0) | -1 | OK |
| Master door wall | x 4.17..4.29 (S) | 4.15..4.26 | -2 / -3 | OK |
| Bath / closet partition | x 6.915..7.02 (S, about 10.5) | 6.85..7.01 (16) | | KNOWN (sales plan: master bath 222 vs 230) |
| Mamad N wall | z -0.10..+0.10 (S) | -0.145..0.125 | | KNOWN (sales) |
| Room 1/2 partition, corridor walls | 15 / 10-15 | 18 / 18-20.5 | | KNOWN (sales) |
| Corridor width | 115 W / 105 E | 110 / 105.5 | | KNOWN (sales) / OK |
| Kitchen entry stub end | chain ends "75" → 4.33 | 4.33, L1084 | 0 | OK |
| Entry wall face | z 5.54 | 5.50 | -4 | KNOWN (recheck 3, 3.10) |
| Room interiors | +5 to +8 cm larger than the sales plan in every room | sales plan (roomdims +0) | | KNOWN (decision: model stays on the sales plan) |
| Balcony N face / depth | 0.35 / 280 from 7.63 | BZ1 .34 / 7.70..10.45 | -1 / 0 | OK |
| Room 1 N face | -5.01 | -5.035 | -2.5 | KNOWN (recheck 3, 3.7: fixing it breaks roomdims) |

### Deviations: doors, windows, walls (G)

#### G0 (HIGH, new). North facade walls from x 6.015 to 9.30 are not built: they are commented out

- Plan: solid north facade from the master bath window to the NE corner (top chain 233 \| 60 \| 261), window 6.015..6.615 with
  UK 125 / OK 235.
- Model: L1075. Commit 40e8d72 ("QA9 baths: both niches are real recesses") inserted the shower-niche pieces and the comment
  `// shower niche cut 9 cm into the wall` in the middle of the line, so the rest of the line became part of the comment:
  `W(6.015, 6.615, ..., 0, 1.25)` (sill wall), `W(6.015, 6.615, ..., 2.35)` (lintel), `W(6.615, 6.85, ...)`, `W(6.85, 7.01, ...)`,
  `W(7.01, 8.91, -5.39, -4.995)` (closet N wall), `W(8.91, 9.30, ...)` (NE corner) are never executed.
- Seen: in the `top` view and every dollhouse view the wall top is missing over the master bath east of the window and over the
  whole closet (light strip instead of the dark wall cap): `V1_img/g0_north_wall_missing_top.jpg`, `V1_img/g0_north_strip_top_view.jpg`. From
  inside the bath tiles, the closet wardrobes and the exterior plaster skin hide the gap, so a walk-through does not show it; the
  plan view the architect will look at does. `roomdims.py` and `clearance_audit.py` do not catch it (see section 3).
- Fix (L1075): move the comment to the end of the line, i.e. replace
  `W(4.91, 5.41, -5.39, -5.07, 1.03, 1.42);   // shower niche cut 9 cm into the wall W(6.015, 6.615, -5.39, -4.98, 0, 1.25); W(6.015, 6.615, -5.39, -4.98, 2.35); W(6.615, 6.85, -5.39, -4.98); W(6.85, 7.01, -5.39, -5.01); W(7.01, 8.91, -5.39, -4.995); W(8.91, 9.30, -5.39, -5.01);`
  with
  `W(4.91, 5.41, -5.39, -5.07, 1.03, 1.42); W(6.015, 6.615, -5.39, -4.98, 0, 1.25); W(6.015, 6.615, -5.39, -4.98, 2.35); W(6.615, 6.85, -5.39, -4.98); W(6.85, 7.01, -5.39, -5.01); W(7.01, 8.91, -5.39, -4.995); W(8.91, 9.30, -5.39, -5.01);   // shower niche (x 4.91..5.41) cut 9 cm into the wall`
  This restores the geometry as it was before 40e8d72 (which passed the checks). Re-shoot `top` and the master bath and closet.
- Tool fix (so this cannot recur silently), `roomdims.py` L8: after `seg=src.split('// WALLS:')[1].split('// corridor gypsum')[0]`
  add `seg=re.sub(r'//[^\n]*','',seg)`.

#### G1 (MEDIUM). Bedroom window handles on the hinge side (room 1, room 2, master E)

- Plan: one inward sash each; room 1 and master E hinge at the S jamb, room 2 at the E jamb (crops `V1_img/g1_room1_window_plan.jpg`,
  `g1_room2_window_plan.jpg`, `g1_master_window_plan.jpg`).
- Model: with `panes = 1` the lever goes to the far end of the span (`windowZ`: `z2 - .08`; `windowX`: `x2 - .08`), i.e. room 1
  z -1.99 (S), master z -1.35 (S), room 2 x 1.185 (E): the hinge side in all three.
- Fix: `windowX` (L1023) signature `..., kip = false)` -> `..., kip = false, latchLo = false)` and in its last line
  `panes > 1 ? mid + .05 : x2 - .08` -> `panes > 1 ? mid + .05 : latchLo ? x1 + .08 : x2 - .08`; `windowZ` (L1038) signature
  `..., panes = 2)` -> `..., panes = 2, latchLo = false)` and `panes > 1 ? z1 + (z2 - z1) / panes + .05 : z2 - .08` ->
  `panes > 1 ? z1 + (z2 - z1) / panes + .05 : latchLo ? z1 + .08 : z2 - .08`. Calls: L1625
  `windowZ(-2.17, -1.27, 8.92, 9.30, .15, 2.35, 1);` -> `windowZ(-2.17, -1.27, 8.92, 9.30, .15, 2.35, 1, true);`; L1829
  `windowZ(-2.81, -1.91, -3.90, -4.28, .15, 2.35, 1);` -> `windowZ(-2.81, -1.91, -3.90, -4.28, .15, 2.35, 1, true);`; L1854
  `windowX(.365, 1.265, -5.01, -5.39, .15, 2.35, 1);` -> `windowX(.365, 1.265, -5.01, -5.39, .15, 2.35, 1, false, false, true);`.
  Check the room 1 and master curtains still clear the lever.

#### G2 (MEDIUM). Kitchen window C is drawn as one inward side-hung sash, the model has a slider

- Plan: at z 7.75..8.45 one sash opening into the kitchen, hinge at the N jamb (z 7.78), swing arc to the S jamb; frame at the
  inner face (x 7.30..7.38). UK 120 / OK 235+35 written. Crop `V1_img/g2_window_C_plan.jpg`. (Recheck 3 section 3.9 read it the same way;
  QA9 owner question 13 calls the type "not written": it is not written, but it is drawn.)
- Model: L1279 `slider(7.75, 8.45, 1.20, HEAD)` "type not written, a slider like the others (estimate)".
- Fix: L1279 replace `slider(7.75, 8.45, 1.20, HEAD);` with `windowZ(7.75, 8.45, FX, FO, 1.20, HEAD, 1);` (default handle at
  z 8.37 = the S, latch, side); delete L1280 (`B(FX - .02, FX + .155, 7.72, 8.45, 1.175, 1.205, mat.sill ...)`: `windowZ`
  draws its own interior sill and the two would overlap); in the insect-screen slot L2079 drop `[7.75, 8.45, 1.20, HEAD]` from
  the slider list and add `panel('z', 7.75, 8.45, 7.54, 1.20, HEAD);` to L2080. The zebra blind (L1296-1311) hangs in the
  reveal at x 7.35, where an inward sash would swing: mount it on the sash or on the wall face above the opening (design call).

#### G3 (LOW). Entrance opening centred 3.5 cm west of the plan

- Plan: rough opening "105" between the chain stations 1.58 and 2.63 (…\| 15 \| 105 \| 95 \| 75 ending at 4.33).
- Model: wall gap 1.585..2.555 (97 net), face frame 1.535..2.605: centre 2.07 vs 2.105.
- Fix: shift every entrance x by +0.035: L1084 `W(1.19, 1.585, ...); W(1.585, 2.555, ..., DOORH); W(2.555, 3.63, ...)` ->
  `W(1.19, 1.62, ...); W(1.62, 2.59, ..., DOORH); W(2.59, 3.63, ...)`; L1230 `[[1.535, 1.585], [2.555, 2.605]]` ->
  `[[1.57, 1.62], [2.59, 2.64]]` and `B(1.535, 2.605, ...)` -> `B(1.57, 2.64, ...)`; L1184 `B(1.565, 2.575, ...)` ->
  `B(1.60, 2.61, ...)`; L1186-1188 hardware x +0.035 (2.470 -> 2.505, 2.505 -> 2.54, 2.478 -> 2.513, 2.497 -> 2.532, 2.36 -> 2.395,
  2.4875 -> 2.5225, 2.07 -> 2.105, 2.40 -> 2.435, 2.44 -> 2.475); the switch `['n', 5.50, 2.68]` (L1232) to 2.72 so its plate
  clears the frame at 2.64. Any skirting/noSkirt or floor entries at 1.585 / 2.555 follow.

#### G4 (LOW). Master bath door opening 70, written 75

- Plan: "75/210", ticks z -4.06..-3.31 (crop `V1_img/g4_master_bath_door_plan.jpg`), hinge at the S jamb, leaf drawn about 64.
- Model: gap -4.06..-3.36 (L1103), leaf .69 (L1204). Every other interior door uses the written figure as the wall gap
  (rooms 82 -> 83-84); this one does not.
- Fix: L1103 `W(6.85, 7.01, -4.06, -3.36, DOORH); W(6.85, 7.01, -3.36, -3.245);` -> `W(6.85, 7.01, -4.06, -3.31, DOORH); W(6.85, 7.01, -3.31, -3.245);`;
  L1150 `['z', -4.06, -3.36, 6.85, 7.01, -1, 6.945]` -> `['z', -4.06, -3.31, 6.85, 7.01, -1, 6.945]`; L1204
  `doorLeaf(6.945, -3.365, -1, 0, .69, ...` -> `doorLeaf(6.945, -3.315, -1, 0, .74, ...` (mirror width follows `w`); L1068
  floors `-4.06, -3.36` -> `-4.06, -3.31` (both); L1645 tiles `tileX(-4.06, -3.36, ...)`/`tileX(-3.36, -3.26, ...)` -> `-3.31`.
  The S jamb becomes 6.5 cm (to the partition face -3.245; the plan has 10 to -3.21, the 3.5 cm difference is the known
  sales-plan room size): check the closet-side casing (8.5 cm) against the bedroom partition corner.

#### G5 (LOW, optional). Room 2 door 84 wide and 2.5 cm west

- Plan: chain 159 \| 82 \| 111 -> 0.955..1.775. Model 0.93..1.77 (L1096, FRAMES L1149, leaf L1198). Within the 3 cm scaling
  tolerance; to match exactly: `W(-0.97, 0.955, ...); W(0.955, 1.775, ..., DOORH); W(1.775, 2.01, ...)`, FRAMES
  `['x', .955, 1.775, ...]`, floor L1066 `floor(.93, 1.77, ...)` -> `floor(.955, 1.775, ...)`, `doorLeaf(1.765, ...)`, leaf `.81`.

#### G6 (LOW, optional). Closet opening 78, written 80

- Plan: "55 \| 80 \| 60" from the closet W face. Model 7.54..8.32 (L1102, floor L1068, SPILL2 L2758). Fix: `W(7.01, 7.56, ...)`,
  `W(8.36, 8.91, ...)`, `floor(7.56, 8.36, ...)`, SPILL2 `7.54` -> `7.56`, `8.32` -> `8.36`, blind corner L1633 `B(8.32, ...` ->
  `B(8.36, ...`. (The 60 east part cannot hold: the model closet is 190, not 195, by the sales plan rule.)

#### G7 (LOW). Laundry niche opening east edge 3.65, written 3.685

- Plan: top chain 88 \| 154 -> 2.145..3.685. Model: E pier `W(3.65, 4.37, -5.39, -5.11)` (L1075), louvres `B(2.15, 3.65, ...)`
  (L1786), exterior lists `['x', 2.15, 3.65, ...]` (L2137, L2156).
- Fix: 3.65 -> 3.685 in those four places.

## 4. Plumbing and kitchen

Done as a separate verification pass (vector-path extraction, every symbol registered on two sheets where it appears on
both). Evidence names refer to `/tmp/v1pl/`.


Report only. Model: `source/salon.html` at HEAD 6810263 (line numbers from that file). Sheets:
`materials/plans/vector/{plumbing,construction,ac,kitchen}.pdf`. Evidence crops: `/tmp/v1pl/*.png` (model walls overlaid in
red, model points as magenta crosses where marked, labelled model grid).

W = written on a sheet. S = scaled. Verdicts: OK, DEV (deviation, fix proposed), KNOWN (documented conflict or design
choice in PROJECT_MEMORY / audit APPLIED files), INFO (not visible / outside the model).

### 4.1 Method and registration

- The vector PDFs have no text layer but do have vector paths. I extracted circles and lines with pymupdf
  (`get_drawings`, coordinates rotated with `page.rotation_matrix`) and mapped them to model metres. Scripts:
  `/tmp/v1pl/circles.py`, `/tmp/v1pl/lines.py`, `/tmp/v1pl/ov.py` (crop with model-wall overlay), transforms in
  `/tmp/v1pl/T.json`.
- Construction: X = 514.8 + 56.693 x, Y = 497.3 + 56.693 z (given). Plumbing: X = 567.2 + 56.693 x, Y = 473.0 + 56.693 z.
  AC: X = 622.3 + 56.693 x, Y = 464.5 + 56.693 z.
- Registration check (same symbol, both sheets): riser 2 plumbing (2.104, -3.713) vs construction (2.106, -3.712); water
  heater (4.037, -4.697) vs (4.036, -4.696); kitchen FS (3.169, 8.020) vs (3.170, 8.021); AC sheet heater (4.038, -4.698),
  riser 4 (2.220, -4.939) vs plumbing (2.219, -4.941). Walls: family bath west face 1.989 / 1.990 on plumbing / AC.
  Registration is good to 0.2 cm. The earlier "(291, -135) px at 400 dpi" offset is confirmed.
- The sheets' rooms are larger than the model (KNOWN: construction rooms 5 to 8 cm larger, model on the sales plan).
  Faces measured on the plumbing sheet (global frame): family bath x 1.989..4.518, z -3.811..-1.352 (253 x 246, the
  construction's written numbers); master bath x 4.618..6.919, z -5.012..-3.212 (230 x 180); niche x 2.148..4.408,
  z -5.122 (solid part) ..-3.962; balcony x 7.73 (facade), z 0.348..8.798. So every scaled item is measured from the
  nearest plan face and re-applied to the model face, as the earlier audits did.

### 4.2 Family bath (model x 2.01..4.46, z -3.775..-1.395)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| WC axis | W 44 from the north wall (plumbing, construction); bowl circle 43 from the plan face | 44: effective z -3.335 (L1755, `withShift(.14,-.13)`) | 0 | OK |
| Cistern | W "מיכל הדחה גבוה" (high cistern), 14 x 41 box drawn | concealed-cistern ledge, flush plate on the axis at .86-.98 (L1754, L1756) | type | KNOWN (d08 concealed cisterns, design choice) |
| Basin axis | W 72 from the south wall (plumbing; construction writes 72 three times) | basin hole centre and mixer z -2.115 = 72 (L1769, L1762) | 0 | OK |
| Basin heights | none written for this basin; waste also takes the AC condensate ("ניקוז מזגן עילי") | deck mixer on the .85 top | n/a | OK (nothing to check; condensate hidden) |
| Tub width | W 35 + 35 = 70 | 70 (X1 3.76..X2 4.46, L776) | 0 | OK |
| Tub length | not written on plumbing (S about 162); construction W 163 | 158.5 brick to brick | -3.5 / -4.5 | KNOWN (QA9 C, owner question "tub 157 vs 160"; walls on the sales plan) |
| Tub mixer | W 35 from the east wall, "אינטרפוץ 4 דרך H-85" | x 4.11 = 35 from 4.46, h .85, 4-way default (L1749) | 0 | OK |
| Overflow filler | W 15 + 20: point 20 from the east wall; note "אביק אוטומטי פיית מילוי פנימית" | filler disc on the overflow at x 4.26 = 20 from the wall, h .50 (L1750) | 0 | OK |
| Second wall point | "נקודת מים H-85" leader to the dot 20 from the east wall | none on the wall | n/a | INFO: concealed supply to the overflow filler (interpretation); nothing visible to model |
| Rail / hand shower | W "מוט+מזלף H-150 תחילת מוט" | rail 1.50..2.05 at x 3.935 (L1751) | 0 | OK |
| Tub drain | S: Ø5 circle 35 from the east face, 20.4 from the south face | (4.11, -1.60): 35 / 20.5 (L782) | 0 | OK |
| Riser 2 "קולטן Ø110" + box | S circle 11.5 from the west face, 9.8 from the north face; box about 19 x 19 in the corner | box x 2.01..2.20, z -3.775..-3.575, centre 9.5 / 10 from the faces (L1778) | under 2 | OK |
| Washer point | W 35 from the north wall, on the east wall, water H-110, drain H-65 | stack centre 34.5 from the north face, 32 from the east face (L1703); points behind the stack | under 3 | OK (points hidden) |
| Ceiling drop | W "הנמכת תקרה למיזוג אוויר -50" | BC = H - .50 (L1112) | 0 | OK |

### 4.3 Master bath (model x 4.63..6.85, z -4.98..-3.26)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| WC axis | W 60 from the closet wall (plumbing, construction) | 6.25 = 60 from 6.85 (L1664, shift .19) | 0 | OK |
| Cistern | W "מיכל הדחה נמוך" (low cistern) | concealed ledge (L1667) | type | KNOWN (design choice) |
| Basin axis | W 44 from the south wall | z -3.70 (hole -3.76 + .06, mixer L1681) = 44 | 0 | OK |
| Basin heights | W "ברז פרח ... H-60, מרכז ביוב H-50, לארון תלוי" | wall-hung walnut cabinet .45-.80, top .83 (L1679-1681): supply .60 and waste .50 fall inside the cabinet | n/a | OK (compatible, hidden) |
| Shower size | W 106 x 92 (plumbing); 110 x 96 (construction) | 106 x 91 | 0 / -4 x -5 | KNOWN (follows the room; spec 80x80 open question) |
| Shower drain | W 50 from the north wall (plumbing), 48 / 48 (construction); S 52.7 from the west face (dimension line at x 5.145) | (5.16, -4.48): 53 from the west, 50 from the north (L1658) | 0 to 2 | OK |
| Mixer | W "אינטרפוץ 4 דרך למזלף ומוט H-105", south dot: 35 + 15 = 50 from the north wall (plumbing); 40 + 15 = 55 (construction) | west wall, z -4.49 = 49 from the north, h 1.05 (L1661) | 1 (plumbing) / 6 (construction) | OK on plumbing. Type: model default 3-way (spec d08) vs plan 4-way: KNOWN (QA9 C_baths) |
| Shower head | W "ראש טוש H-210" is in the same note as the mixer and its leader goes to the south dot (50 from the north). The north dot (35, or 40 on construction) has its own label "נקודת מים H-105" (evidence `pl_mlabels.png`, `pl_shower.png`, `pl_north.png`) | wall arm at z -4.585 = 39.5 from the north, h 2.10 (L762-765 inside `withShift(.19,0)`, L1659) | 9.5 cm north of the plan point (head and mixer drawn 15 apart on both sheets' chain; model has them 9.5 apart and on different points) | P1. Recheck3 read the north dot as the head; the leaders say otherwise |
| Water point H-105 | north dot, 35 from the north wall (plumbing; 40 construction) | no outlet; rail at z -4.755, .90-1.75 (L1660) | n/a | INFO: likely the hand-shower outlet; not written what it serves, no change |
| Head type and height | wall outlet at H-210 | wall arm, arm at 2.09-2.11 | 0 | OK |

### 4.4 Laundry niche (model x 2.15..4.37, z -5.30..-3.99)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| Pipe 4 "ניקוז ... צ.מ.ג 4"" (triangle 4) | S circle (2.219, -4.941) on plumbing and AC, identical; 7 from the partition face, 18 from the solid north face, 98 from the bath wall | (2.21, -5.02): 6 / 9 / 103 (L1787) | z: 8 global, 9 north anchor, 5 south anchor | P2 (was "not applied, low confidence" in recheck3; the vector extraction on two sheets with local faces agreeing to 1-2 cm makes it solid) |
| Floor drain "ניקוז מסתור 11" | S (3.883, -4.340): 52.5 from the east face, 78 from the north face, 38 from the bath wall | (3.85, -4.31): 52 / 80 / 32 (L1783) | 0 to 3 on the near faces | OK |
| Water heater | S Ø60, centre (4.038, -4.698): 37 from the east face, 42 from the north face | Ø54, effective (4.04, -4.69): 33 / 42 (L1804) | Ø -6, position 0 to 4 | KNOWN (diameter "not applied, low" in recheck3 APPLIED) |
| Riser 1 "קולטן Ø110" (octagon 1) | S (4.029, -4.973): 15 from the north face, drawn partly inside the heater outline | not modelled | missing | KNOWN (recheck3 "not applied, low"). Note: it cannot sit where drawn without touching the heater and its straps (L1805, world x 4.00..4.08, z -5.12..-4.95): a plan conflict, ask |
| Main condenser (52,000 BTU) | S AC sheet box x 2.293..3.294, z -5.063..-4.612 (100 x 45), fans on the north side | world x 2.30..3.30, z -5.05..-4.60, fan to the north (L1789) | 0 to 1 | OK |
| Second condenser (master split) | S AC sheet box x 2.824..3.662, z -5.012..-4.612 (84 x 40), overlapping the main unit's east half | world x 2.38..3.22, z -5.00..-4.60, centred over the main unit (L1796-1800) | x -44 | P3. Re-check 5 wrote "AC plan outline" but centred it; the outline is offset east |
| AC isolator (electrical, context) | hatched circle (2.21, -4.88) on construction and AC | B x 2.15..2.20, z -4.94..-4.82 (L1807) | 0 | OK, but it would clash with pipe 4 once P2 is applied (the sheets draw the two symbols overlapping); see P2 |

### 4.5 Balcony (model x 7.70..10.45, z 0.34..8.71)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| Floor drain 1 | S circle (9.081, 1.623): 1.35 from the facade line 7.73, 1.40 from the east edge, 1.275 from the north face 0.348 (i.e. on the balcony's centre line) | (8.89, 1.63) (L2090) | x -16 (both side anchors give model x 9.05); z +1 | P4 |
| Floor drain 2 | S circle (9.081, 7.421): same x; 1.377 from the south face 8.798 | (8.89, 7.36) (L2090) | x -16; z +3 (south anchor 7.33) | P4 |
| Gas point | W 60 from the facade, "נקודת גז H-30" | x 8.30, h .24-.36 (L2087) | 0 | OK |
| Garden tap | W further 20, "ברז גן 1/2" H-60" | x 8.50, h .60 (L2089) | 0 | OK |
| Downpipes "ניקוז מרפסת 4"" 1 and 2 | inside the north wall corner (9.09, 0.12) and the south wall (9.06, 9.01) | not modelled | n/a | INFO (inside walls) |

P4 history: recheck3 P19/P20 read the drains at x 8.89 ("1.19 from the facade line") and that was applied. The vector
circle centre is 9.081 in the registered frame and the facade face line on the same sheet is 7.729 to 7.755 (door
openings at 7.729, first deck line at 7.755), so the drains are 1.33 to 1.35 m out, at the middle of the 2.73 m sheet
balcony. The pre-recheck3 model had (9.05, 1.5) and (9.08, 7.3).

### 4.6 Kitchen (model x 3.63..7.28, z 5.61..8.79)

The plumbing sheet has no kitchen water, drain or gas points; the only symbols near the kitchen (riser 3 "קולטן Ø110"
at (3.288, 7.836), balcony drain 13 at (3.281, 8.181), "FS" Ø35 at (3.17, 8.02)) are in the building-core shaft west of
the core wall (plan face about x 3.58), reached from the lobby: outside the apartment (INFO). Kitchen points come from the
Regba supplier sheet (south wall, distance from the west wall, model x = 3.63 + d; re-read on `ki_south.png`).

| Item | Supplier sheet (W) | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| Sink drain "ביוב" (pipe end up to 12 cm from the wall) | 1000, near the floor (x 4.63) | sink 80 at x 4.85..5.65, waste under the bowl (L1491, L1529) | about +60 | KNOWN (owner kitchen layout, PROJECT_MEMORY / recheck3 kitchen b1) |
| Taps + dishwasher drain | 1130, H 500 (x 4.76) | mixer at x 5.25 (L1535) | +49 | KNOWN (b1) |
| Dishwasher socket | 1300, H 600 (x 4.93) | inside the sink cabinet | compatible | OK |
| Dishwasher | supplier about 5.21..5.81 | 5.65..6.25 (DW2, L1491) | +44 | KNOWN (b2) |
| Hob | gas, ignition socket 2300 H 600, gas outlet "יציאת צינור גז" 3300 at about H 100 (x 6.93) | induction 6.25..6.85 (L1536); no gas outlet | type | KNOWN (b3) |
| Fridge | niche about 88 clear, socket z 5.89 H 1700 | 70 fridge, z 5.71..6.41 (L1494), socket hidden behind | -18 width | KNOWN (b5) |
| Service sockets | 200 / H 1100 south, 1250 / H 1100 west | plates at (3.83, 8.775) and (3.66, 7.54), h 1.10 (L1563) | 0 | OK |

### 4.7 Corridor and other symbols

| Item | Plan | Model | Verdict |
|---|---|---|---|
| Master split condensate point "ניקוז מזגן עילי" | plumbing (4.21, -1.105), 15 from the corridor north face; construction at the other jamb (4.212, -0.327) | not modelled (in the jamb) | INFO (concealed; sheets disagree on the jamb) |
| Family basin condensate | "ניקוז מזגן עילי" into the basin waste | hidden | OK |
| Facade downpipes: triangle 5 "צ.מ.ג 4"" (NE corner), drain 12 "ניקוז מרפסת" and "ניקוז תעלה" (west facade, x -4.05, z -1.09 / -0.86), NW corner circle (-4.11, -5.19) | inside the facade walls | not modelled | INFO (inside walls) |
| Water meter, gas meter | not on the sheets inside the apartment | none | n/a |
| Ø8.7 circles with a cross (e.g. (3.34, -4.85) "+2.70", (4.69, 6.60)) | level marks / the "Ø" glyph of "Ø110" labels | n/a | not plumbing |

### 4.8 Item count: every plumbing symbol on the plumbing sheet, apartment and its walls

| # | Symbol | Where | Modelled |
|---|---|---|---|
| 1 | Riser 1 "קולטן Ø110" | niche, behind the heater | no (KNOWN, plan conflict with the heater) |
| 2 | Riser 2 "קולטן Ø110" + box | family bath NW | yes |
| 3 | Riser 3 "קולטן Ø110" | core shaft by the kitchen | n/a (outside) |
| 4 | Pipe 4 "ניקוז צ.מ.ג 4"" | niche NW | yes, 8 cm off (P2) |
| 5 | Pipe 5 "צ.מ.ג 4"" | NE corner, in the wall | n/a |
| 6, 7 | Balcony downpipes 1, 2 "ניקוז מרפסת 4"" | balcony walls | n/a |
| 8 | Drain 11 "ניקוז מסתור" (floor drain) | niche | yes |
| 9 | Drain 12 "ניקוז מרפסת", "ניקוז תעלה" | west facade wall | n/a |
| 10 | Drain 13 "ניקוז מרפסת 4"", FS | core shaft by the kitchen | n/a |
| 11, 12 | Balcony floor drains | balcony | yes, 16 cm off in x (P4) |
| 13 | Gas point H-30 | balcony | yes |
| 14 | Garden tap 1/2" H-60 | balcony | yes |
| 15 | Family WC + high cistern, axis 44 | family bath | yes (concealed cistern KNOWN) |
| 16 | Family basin, axis 72, AC condensate | family bath | yes |
| 17 | Washer point H-110 / drain H-65, 35 | family bath | yes (hidden behind the stack) |
| 18 | Tub 70 wide, mixer 4-way H-85 at 35, rail from H-150 | family bath | yes |
| 19 | Overflow filler + water point H-85 at 20 | family bath | filler yes; wall point concealed |
| 20 | Tub drain | family bath | yes |
| 21 | Master WC + low cistern, axis 60 | master bath | yes (concealed cistern KNOWN) |
| 22 | Master basin, axis 44, H-60 / H-50 | master bath | yes |
| 23 | Shower drain 50 | master bath | yes |
| 24 | Shower 4-way mixer H-105 + head H-210 (same point, 50) | master bath | mixer yes; head 9.5 cm off (P1) |
| 25 | Water point H-105 at 35 | master shower | no visible outlet (INFO) |
| 26 | Water heater Ø60 | niche | yes (Ø54 KNOWN) |
| 27 | Master split condensate point | corridor, master door jamb | no (concealed, INFO) |

AC sheet, same area: main condenser (yes), second condenser (yes, 44 cm off in x: P3).

### Deviations

#### P1. Master shower head: on the mixer point, not on the "water point H-105"

- Plan: plumbing sheet note "אינטרפוץ 4 דרך למזלף ומוט H-105 / ראש טוש H-210" with one leader to the south dot on the west
  wall, 35 + 15 = 50 cm from the north wall (W). The north dot (35 W) carries a separate label "נקודת מים H-105". The
  construction sheet has the same two dots at 40 and 55 (W, chain 40 + 15 + 41 = 96). So the head belongs at 50
  (plumbing) or 55 (construction), straight over the mixer. Evidence: `/tmp/v1pl/pl_mlabels.png`, `pl_shower.png`,
  `con_shower.png`, `pl_north.png`.
- Model: head arm at z -4.585 (39.5 from the north face -4.98); mixer at z -4.49 (49). salon.html L762, L763, L764, L765
  (`fixHead`, called inside `withShift(.19, 0)` at L1659).
- Delta: 9.5 cm (plumbing) or 15.5 cm (construction); and the mixer-to-head spacing written as a 15 cm chain on both sheets
  is a different point, not the head.
- Fix: put the head over the mixer at z -4.49 (keeps the mixer and drain on the plumbing sheet; 1 cm from its 50).
  - L762 `const V = (a, b) => new THREE.Vector3(a, b, -4.585);` -> `const V = (a, b) => new THREE.Vector3(a, b, -4.49);`
  - L763 `C(4.80, -4.585, 2.04, 2.055, .125, m, { r2: .11 })` -> `C(4.80, -4.49, 2.04, 2.055, .125, m, { r2: .11 })`
  - L764 `a.position.set(4.623, 2.10, -4.585); C(4.80, -4.585, 2.04, 2.05, .125, m); C(4.80, -4.585, 2.05, 2.10, .008, m, { seg: 8 });`
    -> `a.position.set(4.623, 2.10, -4.49); C(4.80, -4.49, 2.04, 2.05, .125, m); C(4.80, -4.49, 2.05, 2.10, .008, m, { seg: 8 });`
  - L765 `B(4.446, 4.80, -4.595, -4.575, 2.09, 2.11, m); C(4.80, -4.585, 2.04, 2.05, .15, m); C(4.80, -4.585, 2.05, 2.09, .008, m, { seg: 8 });`
    -> `B(4.446, 4.80, -4.50, -4.48, 2.09, 2.11, m); C(4.80, -4.49, 2.04, 2.05, .15, m); C(4.80, -4.49, 2.05, 2.09, .008, m, { seg: 8 });`
  - Clearance: the 30 cm head then spans z -4.64..-4.34 at world x 4.99, h 2.04; the glass is at z -4.10 and below 2.00,
    the north wall at -4.98: clear. Optional comment edit on L760: "head over the 4-way mixer, 50 from the north wall".
- Confidence: high on the label reading; the arm length (35 cm) stays an estimate.

#### P2. Niche pipe 4 (4" "צ.מ.ג", triangle 4) 8 cm too far north

- Plan: circle centre (2.219, -4.941) on the plumbing sheet and (2.220, -4.939) on the AC sheet (S, vector). Local faces
  on the sheet agree with the model to 1 to 2 cm (partition face 2.148, bath wall face -3.962, solid north face -5.122).
  From the faces: 7 from the partition, 18 from the solid north face, 98 from the bath wall.
- Model: `C(2.21, -5.02, 0, H, .055, ...)`, L1787: 6 / 9 / 103.
- Delta: z 8 cm (north anchor 9, south anchor 5).
- Fix: L1787
  `C(2.21, -5.02, 0, H, .055, M('#d9d6cf', .6), { seg: 16 });   // 4" niche drain riser in the NW corner (plumbing plan, scaled)`
  -> `C(2.22, -4.95, 0, H, .055, M('#d9d6cf', .6), { seg: 16 });   // 4" niche drain pipe "צ.מ.ג" (plumbing and AC plans, scaled from the vector circle)`
- Knock-on: the AC isolator (L1807, x 2.15..2.20, z -4.94..-4.82) would overlap the pipe (pipe z -5.005..-4.895,
  x 2.165..2.275). The sheets draw the two symbols overlapping, so one has to give. Proposed: L1807
  `B(2.15, 2.20, -4.94, -4.82, 1.10, 1.24, ...)` -> `B(2.15, 2.20, -4.885, -4.765, 1.10, 1.24, ...)` (rest unchanged; 4.7 cm
  south of the scaled symbol centre -4.877, still on the partition face; height an estimate as before). The condenser
  stand legs (world (2.26, -5.09) and (2.26, -4.56)), the main condenser (from x 2.30) and its refrigerant pair (world x
  2.29 / 2.34 at z -4.75) stay clear; the condensate tube end (world (2.26, -5.00)) still meets the pipe.
- Confidence: medium-high (position); the isolator move is a judgement call.

#### P3. Second condenser 84 x 40 is centred over the main unit; the AC sheet draws it 44 cm further east

- Plan: AC sheet, black outline x 2.824..3.662, z -5.012..-4.612 (S, vector), overlapping the east half of the main unit
  outline x 2.293..3.294. Evidence `/tmp/v1pl/ac_niche.png`.
- Model: L1796 `B(2.16, 3.00, -4.55, -4.15, ...)` inside `withShift(.22, -.45)`: world x 2.38..3.22, z -5.00..-4.60.
  The stand (L1797-1798), fan (L1799) and its pipe pair (L1800) follow it.
- Delta: x -44 cm (z OK).
- Fix (all inside the existing `withShift(.22, -.45)`; local x = world - .22):
  - L1796 `B(2.16, 3.00, -4.55, -4.15, 1.05, 1.65,` -> `B(2.60, 3.44, -4.55, -4.15, 1.05, 1.65,` (comment: "offset east over the
    main unit as on the AC plan").
  - L1797 `[[2.04, -4.64], [3.12, -4.64], [2.04, -4.11], [3.12, -4.11]]` -> `[[2.04, -4.64], [3.48, -4.64], [2.04, -4.11], [3.48, -4.11]]`
  - L1798 `B(2.02, 3.14, -4.66, -4.62, 1.01, 1.05, mat.steel); [2.20, 2.96].forEach(` -> `B(2.02, 3.50, -4.66, -4.62, 1.01, 1.05, mat.steel); [2.64, 3.40].forEach(`
    and `B(2.02, 3.14, -4.13, -4.09, 1.01, 1.05, mat.steel)` -> `B(2.02, 3.50, -4.13, -4.09, 1.01, 1.05, mat.steel)`
  - L1799 `f.position.set(2.58, 1.35, -4.555)` -> `f.position.set(3.02, 1.35, -4.555)`
  - L1800 `C(2.93, -4.30, 1.65, H, ...); C(2.86, -4.30, 1.65, H, ...)` -> `C(3.37, -4.30, 1.65, H, ...); C(3.30, -4.30, 1.65, H, ...)`
  - Clearances (world): east legs at x 3.68..3.72 against the heater body from x 3.77 (it starts at h 1.0) and the floor
    drain at (3.85, -4.31): clear; the main unit's pair at x 2.29 / 2.34 is now well clear of the upper body (from 2.82);
    clothesline brackets at h 1.95 over the unit top 1.65: clear. Run `clearance_audit.py` (no rooms change).
- Confidence: medium (the outline is exact; whether the stack is offset in reality is for the AC installer; the sales plan
  calls equipment positions suggestions).

#### P4. Balcony floor drains 16 cm too far west

- Plan: plumbing sheet floor-drain symbols at (9.081, 1.623) and (9.081, 7.421) (S, vector, concentric 8 / 16 / 21 cm).
  Facade face on the same sheet x 7.729..7.755, balcony north face 0.348, south face 8.798. Drains are 1.33 to 1.35 m from
  the facade (the sheet balcony's centre line), 1.275 from the north face and 1.377 from the south face. Evidence
  `/tmp/v1pl/pl_bn.png`, `pl_bs.png`.
- Model: `[[8.89, 1.63], [8.89, 7.36]]`, L2090 (from recheck3 P19/P20, which read 1.19 from the facade).
- Delta: x -16 cm on both (facade anchor gives 9.04 to 9.05, east-edge anchor 9.05); z +1 and +3.
- Fix: L2090 `[[8.89, 1.63], [8.89, 7.36]].forEach(` -> `[[9.05, 1.62], [9.05, 7.33]].forEach(`
  - Drain 1 stays under the balcony table (x 8.65..9.15, z 1.45..2.35, L1946), as now; drain 2 is clear of the egg chair
    ring (x 9.17..10.13).
- Confidence: medium-high.

### Not deviations (for the record)

- Floor drain in the niche: 0 to 3 cm on the near faces (6 on the far south face); left as is.
- Water heater diameter 54 vs Ø60 symbol, riser 1 not modelled: KNOWN, recheck3 "not applied"; riser 1 also conflicts
  with the heater as drawn.
- Master mixer 49 vs construction 55: the two sheets differ (50 / 55); the model follows the plumbing sheet.
- Master shower 4-way (plan) vs 3-way (spec d08) mixer type; cisterns concealed; tub 158.5; shower 106 x 91; kitchen
  sink, dishwasher, hob, fridge positions: KNOWN.
- Kitchen water, drain and gas rough-ins (supplier sheet) sit about 50 cm west of the model's sink and under the model's
  base units: consequence of the owner layout, already in the recheck3 kitchen report (b1, b3).

## 5. Electrical and AC

Done as a separate verification pass (vector layers, symbol inventory `/tmp/v1el/inv_el.txt`). Evidence names refer to
`/tmp/v1el/`. Note: E6 is the same item as P3 above.


Report only. Model: `source/salon.html` at commit 6810263 (3542 lines). Sheets: `materials/plans/vector/electrical.pdf`,
`ac.pdf`, `construction.pdf`. Coordinates: model metres, x east, z south, y up. Heights not written on a sheet are
estimates (switches 1.10, unmarked sockets .40, isolators, panel).

### 5.1 Method

| Item | Value |
|---|---|
| Construction | PDF X = 514.8 + 56.693 x, Y = 497.3 + 56.693 z (given, used as the reference) |
| Electrical (rotated sheet, page.rect coords) | X = 691.6 + 56.693 x, Y = 470.2 + 56.693 z |
| AC | X = 622.3 + 56.693 x, Y = 464.5 + 56.693 z |
| Registration check | cross-correlation of the wall poche against the construction sheet in 6 windows (NW, NE, W, SE, niche, entry): electrical and AC shift 0 to 1 px at 150 dpi, i.e. under 1 cm. Both transforms are verified |
| Symbol positions | read from the vector paths by layer (pymupdf `get_drawings`, layers A_EL_INT1/3/4/5/6/7, E2 dims; AC layers MIZUG, MIZ-P, MIZ-HID, MIZ-petah, MIZ-HANMAHA, miz-miklat, MIKLAT). Scripts: `/tmp/v1el/inv.py` (clusters), `segs.py` (raw segments), `e2.py` (dims), `lay.py` (crops with layers toggled, model grid) |
| Symbol reading | switch = circle + arm(s) with a foot; the point-symmetric "Z" symbol is a two-way switch (every room light is two-way from door and bed); a V with two arms is a 2-gang switch (2ef, 1bc, 1ad); a crossed circle on an arm is a switch with pilot lamp (4, 12, 13); half circle = socket; hatched circle = IP65 point |
| Door switches | the box is taken at the circle, shifted off the casing where the door frame forces it (all within about 10 cm, see 3.x) |
| Threshold | written values win; scaled differences up to about 5 cm are OK; local wall anchors used where the sheet room differs from the model room (mamad 3.68 x 2.72 on the sheets vs 3.55 x 2.62 in the model, living facade 7.33 vs 7.28) |

Verdicts: OK, DEV (deviation, fix proposed in section 5), KNOWN (already documented, not re-raised as new), DELIB
(moved on purpose by an earlier QA step, off the plan), HIDDEN (behind furniture, no visible effect), EXTRA (in the model,
not on the plan; design).

### 5.2 Per-room count table

Counts are wall points (plates/gangs) as drawn; lights and AC listed separately.

| Room | Plan wall points | Model wall points | Plan ceiling/wall lights | Model lights | AC plan | AC model | Verdict |
|---|---|---|---|---|---|---|---|
| Room 1 | 9 (sd 2, dst 3, sk 2, shutter 1, door 1) | 9 | 1 (3b) | fan + 2 spots | 80x20 grille over the door | same | OK (2 spots EXTRA) |
| Room 2 | 9 (sd 2, dst 3, ksr 3, door 1) | 9 | 1 (2d) | fan + 2 spots | 80x20 grille | same | OK |
| Mamad | 9 (dst 3, sd 2, sk 2, filter socket h220 1, door 1) | 9 | 1 (3a) | fan + 2 spots | 2 x 8" sleeves, 4" relief, filter, cable transit | sleeves, relief, filter | Transit missing (KNOWN) |
| Corridor | 10 gangs (3c x2, socket 1, x2 double 2, FO 1, 2ef 2 + 12 + 4 with timer) + panel, comms box, display | 9 gangs + panel, box, display | 3 (3c) | 3 cylinders | return 80x60, drop 35 net | same | **DEV: water-heater switch "4" (+ timer) missing** |
| Master + vestibule | 12 (door 2a, W bed head s+E 2, E bed head k+s+ט 3, TV 3, shutter 1, closet switch 2c 1, "16" socket 1) | 11 | 1 (2a) | fan + 4 spots + 2 globes | split 12,300 over the door | same | "16" missing (KNOWN) |
| Closet | 2 (2b, 13 with pilot) | 2 | 1 (2c) | 1 spot | - | - | OK |
| Master bath | socket h110 1, heater 13 h200 | 1 + heater | 1 (2b mirror) | mirror LED + 3 downlights | - | - | OK (3 downlights EXTRA) |
| Family bath | socket h110 1, washer/dryer h140 2, heater 12 h200, "9" 3-ph point | 3 + heater ("9" hidden) | 2 (2f ceiling, 2e mirror) | 1 spot + mirror LED | drop -50, unit, hatch 60x60 | drop -50, hatch | **DEV: socket x, hatch position** |
| Laundry niche | isolator "9 3x16A IP65", point "4 IP65" | 2 | 0 | 1 spot | condenser 100x45 + 84x40 | both | **DEV: 2nd condenser x**; heater point DELIB |
| Living | 1bc (2 gangs), pier krr 3, pier socket 1, 1p 1; storage wall 2 + TV wall 9 (hidden) | 1bc 1 gang, krr 3, socket 1, 1p 1 (+ robot-garage socket) | 2 (1b, 1c) | wave pendant, flush light, 10 downlights | 2 supply 90x15, bulkhead 78 / h35 | same | **DEV: 1bc is single** |
| Entry | 1ad (2 gangs), VE, blue "1" box | 1 gang + intercom | 1 (1a) | 2 cylinders | - | - | **DEV: 1ad is single** |
| Kitchen | 1d 1 (sockets "per the kitchen company") | 1 (+ kitchen sockets) | 1 (1d) | frames pendant | none | none | OK |
| Balcony | IP socket 1 | IP box + d10 st 2 | 2 (1e) | 2 + 2 sconces | - | - | OK |
| Shutter motors | 6 (room 1, room 2, master, 1m door A, 1n + 1p both on door B) | 5 shutters | | | | | KNOWN (door B 2 motors) |

### 5.3 Electrical, per item

Line numbers are `source/salon.html` at 6810263. Plan = vector sheet (W written, S scaled).

#### 5.3.1 Room 1 (`e_room1.png`)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 3b | W 140 from E face, 180 from N face -> (-2.55, -3.235) | fan (-2.51, -3.21) via withShift(.09,-.21) (1826) | 4 / 2.5 cm | OK |
| Socket + phone h=40 | W 41 from N face to the socket centre (tick -4.609 = socket -4.606) -> socket z -4.625 | `outlets('e', -3.89, -4.625, .40, 'sd')` (2028): socket at -4.6675 | 4.25 cm vs a written dim | DEV-low (E8) |
| TV group h=180 | W 129 from the socket to the socket/TV pair centre -> -3.335 | `'dst'` -3.38 (2028): pair centre -3.3375 | 0.25 cm | OK |
| Bed head socket + 3b h=65 | S socket -2.349, switch -2.12 | `'sk'` -2.22 (2029): -2.2625 / -2.1775 | group centre 1.5 cm | OK (symbols spread) |
| Shutter switch 3m | S z -1.81 (circle) | `'r'` z -1.66 (2029) | 15 cm | DELIB (QA9 D #5, curtain stack) |
| Door switch 3b (two-way) | S circle -2.045 at the jamb; arm meets the wall at -2.14 | -2.18 (1233) | jamb/casing bound | OK |
| Boxed א "25" | (-2.53, -2.26) | none | | KNOWN |

#### 5.3.2 Room 2 (`e_room2.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 2d | W 144 from W face, 180 from N face -> (0.47, -3.21) | fan (0.45, -3.20) (1851) | 2 / 1 cm | OK |
| Socket + phone h=40 | W 46 (tick -4.552, between socket -4.629 and ת -4.433) | `'sd'` -4.55 (2031) | 0 on the written dim | OK |
| TV group h=180 | W 173 -> -2.82 | `'dst'` (1.82, -2.86) pair centre -2.8175 | 0.3 cm | OK |
| Bed head 2d / socket / 2n h=65 | S k -0.01, s 0.21, r 0.45 | `'ksr'` .20 (2031): .115/.20/.285 | spread | KNOWN (QA9 D #7, headboard; schematic spread) |
| Door switch 2d | S circle 0.90, arm at the wall 0.84 | 0.83 (1233) | | OK |
| Boxed א "25" | (0.33, -2.37) | none | | KNOWN |

#### 5.3.3 Mamad (`e_mamad.png`, `a_mamad.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 3a | W 182.5 from W face, 135 from S face | fan (-1.97, 1.395) (1865) | 3 cm | OK |
| Bedside socket + 3a h=65 | W 120 from S face to the socket -> 1.545 | `'sk'` 1.59 (2033): socket 1.5475 | 0.25 cm | OK |
| TV group h=180 | S pair centre 0.932 (S-face anchor 0.94) | `'dst'` 0.89 pair centre 0.9325 | 1 cm | OK |
| Socket + phone h=40 | S socket 2.349 (S-face anchor 2.304) | `'sd'` 2.33: socket 2.2875 | 1.7 cm local | OK |
| Filter socket h=220 | S south wall, x -3.653 | `outlets('n', 2.745, -3.63, 2.20, 's')` (2039) | 2.3 cm | OK |
| Door switch 3a | S circle -1.18 at the latch jamb | -1.10 (1232) | jamb bound | OK |
| Boxed א "25" | (-1.61, 0.52) | none | | KNOWN |

#### 5.3.4 Corridor and panel (`e_corr.png`, `z_fbath_door_panel.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 3c x3 | W 105 / 210 / 210 from W face, 58 from N face -> (-1.07, 1.03, 3.13; -0.665) | cylinders same (1250) | 0 | OK |
| Switch 3c west (two-way) | S circle (0.16, -0.245) | 0.18 (1232) | 2 cm | OK (QA9 D #21 used the arm tip 0.025; the circle convention gives 2 cm) |
| Switch 3c east | S circle 3.227; arm crosses the face at 3.145 | 3.18 (1232) | 3.5 cm | OK |
| Socket "3" | S x 0.647, height not written | 0.65 h .40 (2041) | 0 | OK (h estimate) |
| Panel "לוח חשמל דירתי" | S grey box x 3.37..3.78 | 3.33..3.78 (2043) | 4 cm W edge | OK. PROJECT_MEMORY "panel x conflict (electrical 3.01..3.40)" is stale: the vector sheet agrees with the model |
| Comms box under the panel | W note "and under it a communications box" | 3.35..3.73 h .35..0.85 (2045) | | OK (h estimate) |
| Consumption display | W note; S east of the panel | 3.80..3.92 (2046) | | OK |
| Double socket "x2", circuit 1 | S x 3.59 | `'ss'` 3.57 h 1.15 (2047) | 2 cm | OK (h estimate) |
| FO fibre point | S x 3.991 | `'d'` 3.99 h .40 (2048) | 0 | OK (h estimate) |
| Family bath door group | S on the corridor N face at x 2.65: **2-gang switch 2e/2f**, **switch 12 with pilot** (heater), **switch 4 with pilot and a timer symbol** (water heater, circuit 4 = "4 IP65" in the niche) | `'kkk'` 2.66 (2052) = 2e, 2f, 12 | 1 gang + timer missing | **DEV (E1)** |

#### 5.3.5 Master, vestibule, closet (`e_master.png`, `e_mbath.png`, `z_el_mdoor.png`, `z_16.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 2a | W 150 from S face, 218 from E face -> (6.73, -1.645) | fan (6.73, -1.645) (1611 in withShift) | 0 | OK |
| Door switch 2a (two-way) | S circle (4.43, -1.15), vestibule N face | (s, -1.245, 4.42) (1233) | 1 cm | OK |
| W bed head socket + E h=60 | W 220 between sockets, 89 from E face -> socket 5.82; E at 5.65 | `'ds'` 5.78: s 5.8225, d 5.7375 (2056) | 0 | OK; "E" read as audio intercom: KNOWN (QA9 D #20) |
| E bed head 2a + socket + ט h=60 | W socket 8.02; k 7.91, ט 8.31 | `'ksd'` 8.02 (2056) | 0 on the socket | OK |
| TV group h=180 | S s 6.71, TV 6.947, ת 7.176 (centre 6.94) | `'std'` 6.93 (2057) | 1 cm centre | OK; bare point beside the TV: KNOWN (QA9 D #16) |
| Shutter switch 2m | S z -2.487 on the E face | `'r'` -2.45 (2057) | 3.7 cm | OK |
| Closet switch 2c (master side) | S circle (8.42, -2.98) | (s, -3.105, 8.40) (1232) | 2 cm | OK |
| "16" socket | S half circle on the TV-wall step face, x 4.36, height not written; split feed | none | missing | KNOWN (recheck3, QA9 D #20) |
| Boxed א h=60 | (5.72, -0.78) | none | | KNOWN |
| Closet 2b + 13 (pilot) | S z -4.136 / -4.157 on the closet W wall | `'kk'` -4.22 (2052): -4.2625/-4.1775 | 7 cm | DELIB (QA9 D #3, casing) |
| Closet ceiling 2c | W 120 from N face, 128 from E face -> (7.63, -3.795) | spot (7.63, -3.80) (1246) | 0 | OK |
| Master bath mirror light 2b | W 44 from S face -> z -3.70, W wall | mirror cabinet LED centre -3.71 (1682-1683, withShift .19/.06) | 1 cm | OK |
| Master bath socket h=110 | S x 4.753 on the S wall | 4.72 (2053) | 3.3 cm | OK |
| Heater 13 h=200 | S z -4.452..-4.052, centre -4.252 | -4.50..-4.12, centre -4.31 (2055) | 5.8 cm | DELIB (QA9 D #2, casing) |
| Master bath ceiling | none on the sheet | 3 downlights | | EXTRA (KNOWN) |

#### 5.3.6 Family bath and laundry niche (`e_fbath.png`, `a_fbath_hatch.png`, `a_niche.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Ceiling 2f | W 100 from W face -> x 3.01; S z -3.158 | spot (3.01, -3.10) at BC (1246) | 0 / 6 cm global, 3 cm from the N face | OK |
| Wall light 2e (mirror) | S W wall z -2.085 | mirror cabinet LED centre -2.115 (1775) | 3 cm | OK |
| Splash-proof socket h=110 | S S wall, half circle centre **x 2.179** (18.3 from the W face) | `outlets('n', -1.401, 2.105, ...)` (2053) | **7.5 cm** (8.8 from the W face) | **DEV (E4)** (its old reason, the SW pipe box, moved to the NW corner in recheck3) |
| Washer / dryer h=140 | S z -3.579 / -3.323 on the E wall | -3.61 / -3.34 (2054) | 3.1 / 1.7 cm | OK (recheck3 change 12 not needed) |
| Heater 12 h=200 | S x 2.538..2.938 (centre 2.738) on the S wall, ends at the sheet jamb (2.92) | 2.39..2.79 (2055) | 15 cm centre; same relation to the jamb (flush to the casing) | DELIB (QA9 D #2) |
| "9" 3-phase point | S (2.53, -2.32), in the AC drop | none | | KNOWN, HIDDEN |
| Niche isolator "9 3x16A IP65" | S hatched circle (2.211, -4.876) on the W face | 2.15..2.20, z -4.94..-4.82 h 1.10..1.24 (1807) | 0.4 cm | OK (h estimate) |
| Niche point "4 IP65" (INT4, power point for the water heater) | S hatched circle (4.281, -4.845), between the heater and the E wall | 4.32..4.37, **z -4.31..-4.19** (1808) | **59 cm** | DELIB (QA9 D #10). Plan-faithful alternative in E7 |
| Water heater | S circle centre (4.04, -4.70) | (4.04, -4.69) | 1 cm | OK |
| Niche ceiling spot | none | spot (3.2, -4.65) | | EXTRA |

QA9 D #18 and the owner question "heater switch place" read the sheet as keeping the switch only in the niche. The
sheet has both: the IP65 point "4" beside the heater and a switch "4" with pilot and timer in the bath-door group in the
corridor (E1).

#### 5.3.7 Living, entry, kitchen, balcony (`e_living.png`, `z_1bc.png`, `z_entry.png`, `z_tvwall.png`, `e_kitchen.png`, `e_balc.png`)

| Item | Plan | Model | Delta | Verdict |
|---|---|---|---|---|
| Switch 1bc | S **2-gang** (V symbol) on the core face x 1.45, z 3.02 | single `'k'` in the list at 1232 (`['e', 1.45, 3.0]`) | 1 gang missing | **DEV (E2)** |
| Ceiling 1c | W 127 / 147 -> (1.27, 1.305) | wave pendant canopy x 1.17..1.23 | 4 cm off the canopy | KNOWN (design lamp) |
| Ceiling 1b | W 200 / 230 -> (4.98, 2.00) | flush light (4.70, 2.20) | 28 / 20 cm | KNOWN (DESIGN) |
| Storage wall ט + socket "1" h=40 | S x 0, z 0.667 / 0.911 | none | | HIDDEN, KNOWN |
| TV wall row h=40: S, FO, ת, x2, TV, crossed box | S x 4.73 / 5.05 / 5.34 / 5.65 / 5.87 / 6.12; W 185 from the facade | none | behind the media base (x 3.05..6.95, y .20..0.645) | HIDDEN, KNOWN |
| TV wall h=130 socket + crossed box, 50ø conduit | S x 5.65 / 6.12 | none | behind the TV / inside the fluted tower | HIDDEN, KNOWN |
| Cones x4, "S" box | INT7 | none | | KNOWN |
| Pier 1e + 1m + 1n | S z 3.62 / 3.87 / 4.12 | `'krr'` 3.89 (2082) | spread | OK |
| Pier socket, room side | S z 3.94 (drawn 60 cm into the room), h not written | 3.89 h .40 (2082) | 5 cm | OK |
| Balcony IP socket | S (7.83, 3.93) | box z 3.84..3.94 (2085) | 4 cm | OK |
| Balcony lights 1e | S (7.986, 2.139), (7.986, 5.729) | (7.96, 2.14), (7.96, 5.73) (2084) | 2.6 cm | OK |
| Switch 1p | S z 7.17 | 7.20 (2082) | 3 cm | OK |
| Entry switch 1ad | S **2-gang** (V) on a box at x 2.64..2.89 (circle 2.79), 1a + 1d | single `'k'` 2.68 (1232) | 1 gang missing; 11 cm on the circle | **DEV (E3)** |
| Rectangle with a dot under 1ad | unidentified | none | | OPEN (ask the electrician) |
| Intercom VE | S x 3.108 | 2.76..2.86 (1189) | 30 cm | KNOWN (prints, DESIGN) |
| Blue box "1" over the door | S x 2.085 | none | | KNOWN |
| Ceiling 1a | W 65 / 100 -> (2.10, 4.50) | cylinders (2.4, 3.9), (2.4, 5.0) | | KNOWN (DESIGN) |
| Kitchen switch 1d | S (4.185, 5.44) | 4.17 (1232) | 1.5 cm | OK |
| Kitchen ceiling 1d | W 140 / 228 -> (5.88, 6.51) | frames canopy x 5.83..5.91, z 5.66..6.96 | under the canopy | OK |
| Shutter motors 1m / 1n / 1p | S (7.47, 3.35) door A; (7.47, 4.48) and (7.47, 6.83) both door B | shutters on A and B | | KNOWN (door B two motors; window C none) |

Heights: every written height (40, 60, 65, 110, 130, 140, 180, 200, 220) matches the model.

### 5.4 AC, per item (`a_north.png`, `a_corr.png`, `a_miz_only.png`, `a_mamad.png`, `a_fbath_hatch.png`, `a_niche.png`)

| Item | Plan | Model (line) | Delta | Verdict |
|---|---|---|---|---|
| Mini-central unit | W "52000 Btu/hr, 4.8 kW 3 ph to the condenser, rating C, 50 cm drop, removable or gypsum with a 60x60 access opening"; S unit outline x 2.53..3.56, z -2.64..-1.95 over the bath | hidden above BC | | OK (hidden) |
| Family bath drop | W -50, hatched over the whole bath (x 1.99..4.52, z -3.81..-1.35) | `BC = H - .50` (1112), x 2.01..4.46 (1730) | 0 | OK |
| **Access hatch 60x60** | S dashed square **x 2.058..2.659, z -2.540..-1.942** (layer MIZ-petah), over the basin, beside the unit's W end | x 2.83..3.43, z -2.875..-2.275 (1731-1732) | **77 cm in x, 33 cm in z** | **DEV (E5)** |
| Corridor drop | W "h=35cm (netto)"; S outline x -2.13..4.18, z -1.25..-0.10 | `DROP = H - .35` (1111), x -2.12..4.15 (1113) | 0 / 3 cm | OK |
| Living bulkhead | S edge z 0.779, to x 7.33 | .80 deep, to 7.06 (1379) | 2 cm; ends at the curtain pocket | OK; short end KNOWN (recheck3 A3) |
| Return grille "ת.א.ח 80x60" | S red dashed x 1.891..2.669, z -1.145..-0.544 | x 1.88..2.68, z -1.145..-.545 (1125) | 1 cm | OK |
| Supply grille 1 "מ.א.ק 90X15" | S body x 1.827..2.727 (centre 2.277), on the bulkhead face z 0.767..0.843 | centre 2.20 (1380) | 7.7 cm global, 2.7 cm with the facade anchor | OK (anchor dependent, same anchor as grille 2) |
| Supply grille 2 | S x 5.502..6.401 (centre 5.952) | 5.90 (1380) | 5.2 global, 0 facade anchor | OK |
| Grille height | 15 on the 35 net face | DROP+.05..+.20 | | OK |
| Room 1 grille "80x20 in an 85x25 opening", over the door | S centre -1.673 | -1.65 (1128) | 2.3 cm | OK |
| Room 2 grille | S centre 1.356 | 1.32 (1128) | 3.6 cm | OK |
| Master split "12,300 BTU/hr, 1.0 kW 1ph, A" | S x 4.278..4.477, z -1.15..-0.307, arrow east | x 4.26..4.46, z -1.14..-0.30, y 2.24..2.52 (2050) | 1.5 cm | OK (size, height estimates) |
| Mamad 8" sleeves x2 (supply + return), "o.k. = 10 cm" under the ceiling | S x -1.500, -0.901 (E-face anchor -1.54 / -0.94) | -1.55, -0.95 (1134), top H-.10 | 1 cm local | OK |
| Mamad 4" relief sleeve, "c.l. = 25 cm", 25 from the E face | S x -0.465 (E anchor -0.50) | -0.52, H-.25 (1138) | 2 cm | OK |
| Mamad filter | S box 35 x 40 at z 2.24..2.64 on the W wall (S-face anchor centre 2.40) | 21 x 50, z 2.085..2.585 (2035) | 6 cm, size | KNOWN (recheck3 change 9, not applied, low) |
| Mamad filter sleeves | S leader to z 2.42 (S anchor 2.375) | z 2.335 (2038) | 4 cm | OK |
| Mamad cable transit "מעבר מודולרי" | S E wall z 0.22..0.52 | none | missing | KNOWN (recheck3 plumbing_ac, not modelled) |
| Condenser A (52,000) | S x 2.293..3.294, z -5.063..-4.612 (100 x 45) | effective 2.30..3.30, -5.05..-4.60 (1789, withShift .22/-.45) | 1 cm | OK |
| **Condenser B (84 x 40)** | S **x 2.824..3.662**, z -5.012..-4.612 | effective **2.38..3.22**, z -5.00..-4.60, on a stand over A (1796) | **45 cm in x** | **DEV (E6)** |
| Niche louvres "80% open" | W | 1786 | | OK |
| AC controller | none on the AC sheet ("S" box on INT7 only) | none | | KNOWN (QA9 D #19) |

### 5.5 Deviations and exact fixes

All in `source/salon.html` at 6810263. None moves a wall (`roomdims.py` unaffected); run `clearance_audit.py` after E5,
E6 and E7. Heights not on the sheets stay estimates.

**E1 (medium-high). Family bath door group lacks the water-heater switch "4" (pilot + timer).**
Plan: on the corridor face at x 2.65, the 2-gang 2e/2f plus switches 12 and 4 with pilot lamps and a timer symbol on 4.
Model: 3 gangs. Line 2052, keeping the east edge 2.785 (1.1 cm off the casing at 2.796), extending west:
`outlets('s', -1.245, 2.66, 1.10, 'kkk'); outlets('e', 7.01, -4.22, 1.10, 'kk');`
->
`outlets('s', -1.245, 2.6175, 1.10, 'kkkk'); outlets('e', 7.01, -4.22, 1.10, 'kk');`
and the comment on line 2051 `family bath 2e/2f/12 in the corridor` -> `family bath 2e/2f/12 and the water heater 4 (pilot, timer on the sheet) in the corridor`.
Plates 2.45..2.785; nothing else on that face.

**E2 (medium). Living switch 1bc is 2-gang on the plan, 1 in the model.** Line 1232: remove `['e', 1.45, 3.0], ` from the
list, i.e.
`[['n', -.145, 0.18], ['n', -.19, 3.18], ['n', 5.50, 2.68], ['s', .125, -1.10], ['s', -3.105, 8.40], ['e', 1.45, 3.0], ['n', 5.50, 4.17]].forEach(([f, w, c]) => outlets(f, w, c, 1.1, 'k'));`
->
`[['n', -.145, 0.18], ['n', -.19, 3.18], ['s', .125, -1.10], ['s', -3.105, 8.40], ['n', 5.50, 4.17]].forEach(([f, w, c]) => outlets(f, w, c, 1.1, 'k'));`
`outlets('e', 1.45, 3.02, 1.1, 'kk'); outlets('n', 5.50, 2.72, 1.1, 'kk');   // 2-gang switches 1bc (core wall) and 1ad (entry: 1a + kitchen 1d)`
(this one edit also covers E3). 1bc plates z 2.9375..3.1025: 8.6 cm clear of the entry mirror rim (z 3.188) and above the
commode top (.80).

**E3 (medium). Entry switch 1ad is 2-gang on the plan (1a + 1d), 1 in the model.** Covered by the E2 edit:
plates x 2.6375..2.8025 at h 1.06..1.14: 3.3 cm clear of the entrance frame (2.605), under the intercom (y 1.30..1.48, no
overlap). The plan circle is at 2.79 on a box 2.64..2.89.

**E4 (medium-low). Family bath splash-proof socket 7.5 cm west of the plan.** Line 2053:
`outlets('n', -3.266, 4.72, 1.10, 's'); outlets('n', -1.401, 2.105, 1.10, 's');`
->
`outlets('n', -3.266, 4.72, 1.10, 's'); outlets('n', -1.401, 2.18, 1.10, 's');`
and the towel hooks (line 1779) would then sit on the plate (hook at 2.20, h 1.08..1.12):
`[2.20, 2.31, 2.42].forEach(x => {` -> `[2.27, 2.355, 2.44].forEach(x => {`
(hooks 4 cm clear of the plate edge 2.22, last knob edge 2.451 vs the ladder at 2.47).

**E5 (medium). Family bath 60x60 access hatch in the wrong place.** AC sheet: dashed square x 2.058..2.659,
z -2.540..-1.942 (over the basin, at the unit's west end). Local W-face anchor gives x 2.08..2.68. Lines 1731-1732:
`B(2.83, 3.43, -2.875, -2.275, BC - .004, BC, mat.whitePlate, { parent: ceilGroup, cast: false });`
->
`B(2.08, 2.68, -2.54, -1.94, BC - .004, BC, mat.whitePlate, { parent: ceilGroup, cast: false });`
and
`[[2.826, 2.83, -2.879, -2.271], [3.43, 3.434, -2.879, -2.271], [2.826, 3.434, -2.879, -2.875], [2.826, 3.434, -2.275, -2.271]]`
->
`[[2.076, 2.08, -2.544, -1.936], [2.68, 2.684, -2.544, -1.936], [2.076, 2.684, -2.544, -2.54], [2.076, 2.684, -1.94, -1.936]]`
Clear of the WC column (z -3.775..-3.025) and the spot (3.01, -3.10); the mirror cabinet top is 1.89, the ceiling 2.20.

**E6 (medium-low). Second condenser (84 x 40) 45 cm west of its outline.** AC sheet: x 2.824..3.662. Inside
`withShift(.22, -.45)`, so written x = effective - .22 (2.61..3.45). Lines 1796-1800:
- 1796 `B(2.16, 3.00, -4.55, -4.15, 1.05, 1.65,` -> `B(2.61, 3.45, -4.55, -4.15, 1.05, 1.65,`
- 1797 `[[2.04, -4.64], [3.12, -4.64], [2.04, -4.11], [3.12, -4.11]]` -> `[[2.57, -4.64], [3.49, -4.64], [2.57, -4.11], [3.49, -4.11]]`
- 1798 `B(2.02, 3.14, -4.66, -4.62, 1.01, 1.05, mat.steel); [2.20, 2.96].forEach(x => B(x - .02, x + .02, -4.66, -4.09, 1.01, 1.05, mat.steel)); B(2.02, 3.14, -4.13, -4.09, 1.01, 1.05, mat.steel);`
  -> `B(2.55, 3.51, -4.66, -4.62, 1.01, 1.05, mat.steel); [2.65, 3.41].forEach(x => B(x - .02, x + .02, -4.66, -4.09, 1.01, 1.05, mat.steel)); B(2.55, 3.51, -4.13, -4.09, 1.01, 1.05, mat.steel);`
- 1799 `f.position.set(2.58, 1.35, -4.555)` -> `f.position.set(3.03, 1.35, -4.555)`
- 1800 `C(2.93, -4.30, 1.65, H, .014, ...); C(2.86, -4.30, 1.65, H, .011, ...)` -> `C(3.38, -4.30, ...); C(3.31, -4.30, ...)`
Checks: SE leg effective (3.71, -4.56) is 35.5 cm from the heater axis (r .27); the NE leg touches the solid facade face
(z -5.11); clotheslines (z -4.78..-4.42 written, y 2.0) stay clear of the unit top (1.65) and the pipes (z -4.30).
The stacking itself is an interpretation of two overlapping outlines (recheck3 A10, re-check 5).

**E7 (decision; DELIB). Water heater point "4 IP65" moved 59 cm from the plan.** Plan (4.28, -4.845), between the
heater and the east wall; QA9 moved it to z -4.25 so it is not boxed in. A plan-faithful position that is still reachable
is under the heater (heater body from y 1.0 up; height not on the sheet, estimate). Line 1808:
`B(4.32, 4.37, -4.31, -4.19, 1.13, 1.27, M('#8e9194', .5), { round: .008 });`
-> `B(4.32, 4.37, -4.90, -4.78, .66, .80, M('#8e9194', .5), { round: .008 });`
Apply only if the owner wants the plan position; with E1 the everyday switch is in the corridor anyway.

**E8 (low, optional). Room 1 low socket 4.25 cm off a written dim.** "41" runs from the north face to the socket
symbol; the model puts the group centre there. Line 2028:
`outlets('e', -3.89, -4.625, .40, 'sd');` -> `outlets('e', -3.89, -4.5825, .40, 'sd');`

**Deliberate deviations kept (QA9 moved them off the plan; list for the architect):** room 1 shutter switch -1.66 vs
-1.81 (curtain stack, QA9 D #5); heater 12 centre 2.59 vs 2.74 and heater 13 -4.31 vs -4.25 (door casings, QA9 D #2);
closet `kk` -4.22 vs -4.145 (casing, QA9 D #3); room 2 bed-head group centre .20 (headboard, QA9 D #7); heater point E7.

**Docs:** PROJECT_MEMORY "electrical panel x (electrical sheet 3.01..3.40 ...)" is stale: the vector sheet draws the panel
at 3.37..3.78, matching the model 3.33..3.78. QA9 D #18 / owner question 12 should say the sheet has a timer switch for
the water heater in the corridor bath-door group as well as the IP65 point in the niche.

### 5.6 Known items confirmed, not re-raised

Boxed "א" in rooms 1, 2, master (h=60 next to it) and mamad ("25"); living cones x4 and "S" box; blue box "1" over the
entry door; "16" socket by the master split (a socket on the TV-wall step face, x 4.36); master "E"; TV-wall h=40/h=130
and dining/storage-wall points (hidden); ceiling points 1a, 1b, 1c vs the owners' lamps; extra downlights in every room
and the niche spot; intercom 30 cm west of VE; door B has two motors (1n, 1p) and window C none; family bath "9" 3-phase
point in the drop; mamad filter size and cable transit; living bulkhead stops at 7.06; master TV beside its point.
Unidentified, new: the rectangle with a dot under 1ad at the entry (x 2.64..2.89).

### 5.7 Evidence (all in /tmp/v1el/)

Sheet crops with the model grid: `ov_construction.png`, `ov_electrical.png`, `ov_ac.png` (registration), `e_room1.png`,
`e_room2.png`, `e_mamad.png`, `e_corr.png`, `z_fbath_door_panel.png` (2ef / 4 / 12 group, panel, x2, FO, 2a),
`e_fbath.png`, `e_mbath.png`, `e_master.png`, `z_el_mdoor.png`, `z_con_mdoor.png`, `z_16.png`, `e_living.png`,
`z_1bc.png`, `z_entry.png`, `z_tvwall.png`, `e_kitchen.png`, `e_balc.png`, `a_north.png`, `a_corr.png`, `a_miz_only.png`,
`a_mamad.png`, `z_mamad_transit_ac.png`, `a_fbath_hatch.png`, `a_niche.png`. Symbol inventory: `inv_el.txt`.
Model shots (day): `img/m01_1bc_core_wall.jpg` (single plate), `img/m02_entry_1ad_intercom.jpg` (single plate),
`img/m03_fbath_door_group.jpg` (3 plates), `img/m05_niche_condensers.jpg` (B stacked flush with A's west end),
`img/m06..m08`.
