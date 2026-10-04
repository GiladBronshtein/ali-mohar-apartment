# Re-check 3: plumbing and AC against the vector sheets

Sources: `materials/plans/vector/plumbing.pdf` (HADA plumbing plan), `ac.pdf` (HADA AC plan), with `construction.pdf`
(5/5/26, the newest sheet) for calibration and cross-checks. Model: `source/salon.html` as of this audit (line numbers
below are from the working copy, which already holds uncommitted edits; re-grep before applying).

W = a value written on a sheet. S = scaled off the drawing. Anything not on a sheet (unit heights, arm lengths, H = 2.60)
is an estimate. Crops are in `pl_crops/`.

## 1. Calibration

The PDFs carry no text layer; everything was read from 400 dpi renders.

| Item | Value |
|---|---|
| Scale, all three sheets | 315 px per metre at 400 dpi (1:50 sheets, checked on several written dimensions) |
| Registration | plumbing = construction + (291, -135) px; plumbing = AC + (-306, +47) px |
| Plumbing px to model (global) | x = (Px - 3150) / 315, z = (Py - 2626) / 315 |
| Method for every item | anchored to the nearest matching wall face, not the global origin. The sheet rooms differ from the model by 2 to 11 cm in places (see section 6), so a far anchor would carry that error |
| Repeatability | the same feature read on two sheets agrees within 1 to 2 cm; scaled positions are good to about +-3 cm |

## 2. Plumbing

| # | Item | Source (W/S) | Model | Delta | Verdict |
|---|---|---|---|---|---|
| P1 | Family bath WC axis | W 44 from the north wall | 44 (effective z -3.335) | 0 | OK |
| P2 | Family bath cistern | W "מיכל הדחה גבוה" (high cistern); construction draws a 14 x 41 cistern box | concealed-cistern ledge | type | Design choice, note only |
| P3 | Family bath riser 2, Ø110, in a box | S: NW corner, circle centre about (2.12, -3.67), box about 19 x 20 (plumbing); construction also has the riser symbol at the NW, no box at the SW | full-height box at the SW corner, z -1.605..-1.395 (L1519) | corner | Wrong corner. See change 1 |
| P4 | Family bath basin | W 72 from the south wall; waste also takes the AC condensate ("ניקוז מזגן עילי") | basin centre 72 from the south wall | 0 | OK |
| P5 | Washer point | W 35 from the north wall, water H-110, drain H-65 | washer stack under the laundry cabinet at the north | under 5 cm | OK |
| P6 | Bathtub | W 70 x 159-160 on the plumbing sheet, taps 35/35 and 15/20 from the east wall, H-85 / H-150 | 70 x 158.5, mixer 35 from the east wall at .85, rail from 1.50 | 1 to 2 cm | OK. The construction sheet writes 163 for the tub (geometry, section 6) |
| P7 | Family bath ceiling | W "הנמכת תקרה למיזוג אוויר -50" | BC = H - .50 | 0 | OK |
| P8 | Master bath WC axis | W 60 from the east partition; W "מיכל הדחה נמוך" (low cistern), construction draws a close-coupled cistern | axis 6.25, 60 from the closet wall 6.85; concealed ledge | 0 / type | Position OK, cistern type a design choice |
| P9 | Master shower drain | W 48 / 48 (construction), about 52 from the west | (5.16, -4.48): 53 from west, 50 from north | 1 to 2 cm | OK |
| P10 | Master shower mixer | W "אינטרפוץ 4 דרך למזלף ומוט H-105", 50 from the north end (plumbing) or 55 (construction) | z -4.49 (49 from north), centre h 1.05 | 1 / 6 cm | OK on plumbing; 6 cm off the construction figure (written values conflict) |
| P11 | Master shower head | W "ראש טוש H-210": a wall outlet on the west wall, 35 (plumbing) or 40 (construction) from the north end, 15 cm from the mixer | ceiling rain head on a rod, centre (5.16, -4.52) at h 2.05 (L1404) | type, 30 cm off the wall | Wrong type. See change 4 |
| P12 | Master shower size | W 110 x 96 (construction); plumbing 106 x 92 | 106 x 91 | 4 x 5 cm | Follows the room size; geometry item |
| P13 | Master basin | W 44 from the south wall, tap H-60, waste H-50, wall-hung cabinet | basin centre z -3.70, 44 from the south wall | 0 | OK |
| P14 | Niche floor drain 11 | S about (3.86, -4.33) | (3.85, -4.31) (L1523) | 2 cm | OK |
| P15 | Niche drain riser 4" | S (2.22, -4.94) | (2.21, -5.02) (L1528) | 8 cm, z | Off. See change 8 |
| P16 | Niche riser 1, "קולטן Ø110" | S circle at (4.04, -4.96), leader to the facade near x 4.24 | not modelled | missing | Optional, change 11 |
| P17 | Water heater | S Ø60, centre (4.00 to 4.04, -4.69) | Ø54, effective centre (4.04, -4.69) (L1539) | position 0 to 4 cm; Ø 6 cm | Position OK; diameter optional, change 10 |
| P18 | Niche screen | W "מסתור פתוח 80% נטו למעבר אויר" (80% net open) and "מעקה קל H=105" (light railing on the open edge) | blades every 10 cm, about 75% clear, at z -5.30..-5.26 | 5 points of openness | OK as an approximation. The sheet draws the open edge at z -5.11..-5.16; the facade line is geometry |
| P19 | Balcony floor drain 1 | S (8.89, 1.63): 1.19 from the facade line | (9.05, 1.5) (L1780) | dx -16, dz +13 | Off. See change 7 |
| P20 | Balcony floor drain 2 | S (8.89, 7.33 to 7.42) | (9.08, 7.3) | dx -19, dz 3 to 12 | Off. See change 7 |
| P21 | Balcony gas point | W 60 from the facade, H-30 | x 8.30, h .30 | 0 | OK |
| P22 | Garden tap "ברז גן 1/2"" | W a further 20, H-60 | x 8.50, h .60 | 0 | OK |
| P23 | Balcony downpipes "ניקוז מרפסת 4"" 1 and 2 | S outside the apartment line | not modelled | n/a | Outside the model, no change |
| P24 | Kitchen riser 3 / drain 13 / "FS" | S in the shaft by the lift on the west side of the kitchen, about x 3.2..3.4, z 7.8..8.2 (far anchor, +-10 cm) | not modelled | n/a | In the building core, west of the kitchen wall x 3.63: outside the model. Sink and dishwasher points are not written on the plumbing sheet; see the kitchen audit |

## 3. AC

| # | Item | Source (W/S) | Model | Delta | Verdict |
|---|---|---|---|---|---|
| A1 | Mini-central unit | W "יחידת מיזוג אויר מיני מרכזית INVERTER 52000 Btu/hr", 4.8 kW 3 ph to the condenser, rating C, "הנמכה בגובה 50 ס"מ ניתנת לפירוק או הנמכת גבס עם פתח גישה 60x60" | over the family bath, BC = H - .50, 60 x 60 access hatch | 0 | OK |
| A2 | Return grille "ת.א.ח. 80x60" in the corridor | S x 1.86..2.65 (east anchor) or 1.91..2.70 (west anchor); z -1.145..-0.545 (10 from the corridor north face, 44 from the south face) | x 1.80..2.60, z -1.0..-0.4 (L901-902) | z +14.5, x -6 to -10 | Off. Confirms the recheck2 "14 cm". See change 3 |
| A3 | Living bulkhead depth | S 78.1 from the TV wall face; W "הנמכה נדרשת h=35cm (netto)" | .80 deep, DROP = H - .35 | 2 cm | OK. The sheet runs it to the facade; the model stops at 7.06 for the curtain pocket (intentional) |
| A4 | Supply grille 1 "מ.א.ק. 90X15" | S centre x 2.22 to 2.29 | 2.20 (L1126) | 2 to 9 cm, anchor-dependent | OK |
| A5 | Supply grille 2 "מ.א.ק. 90X15" | S centre x 5.89 to 5.96 | 5.75 (L1126) | +14 to +21 | Off. See change 5 |
| A6 | Ducts | S Ø10" and Ø8" along the corridor and the bulkhead | inside the drop, not drawn | n/a | OK (hidden) |
| A7 | Rooms 1 and 2 transfer grilles | W "תריס משולב 80x20 עם להבי הטייה פנימיים פתח בקיר 85x25", supply and return arrows over the doors | grilles over the doors (L904) | not measured | Approach matches; exact x not scaled |
| A8 | Master split | W "מזגן עילי לתפוקה 12,300 BTU/hr 1.0 kw 1ph הזנה למאייד דירוג אנרגטי A". S a grey 20 x 84 unit on the east (room) face of the master door wall, over the door: x 4.26..4.46, z -1.14..-0.30, arrow pointing east into the room | on the west wall at x 4.61..4.83, z -2.295..-1.395 (L1752) | about 1.1 m in z | Wrong place. See change 2 |
| A9 | Master split condensate | S cleanout at the door jamb: plumbing sheet at the north jamb (W 15 from the corridor north face), AC and construction sheets at the south jamb | not drawn | n/a | Supports A8: the drain runs down the jamb to the corridor |
| A10 | Condenser(s) in the niche | S two overlapping outlines. Box A 100 x 45 (x 2.30..3.30, z -5.05..-4.60), one large fan, isolator "3x16A IP65": the 52,000 BTU condenser. Box B 84 x 40 (x 2.83..3.68, z -5.00..-4.60), smaller fan: most likely the master split condenser, stacked (interpretation). Fans drawn on the north side, toward the screen | one 89 x 34 x 63 box at effective x 2.30..3.19, z -5.25..-4.91, fan on the south face toward the bath window (L1530-1537) | z 20 to 30 cm north, size, fan faces the wrong way | Off. See change 6 |
| A11 | Mamad 8" sleeves | W "2* שרוול פלדה Ø8" תקן הג"א מהתקרה o.k.= 10 cm"; S x -1.547 and -0.95 | x -1.55, -0.95, top at H - .07 (L910) | 0 to 3 cm | OK |
| A12 | Mamad 4" relief sleeve | W "c.l.= 25 cm" under the concrete ceiling, with blast and pressure-relief valve; W 25 from the east inner face | x -0.52, h H - .25 (L914-915) | 2 cm | OK |
| A13 | Mamad filter sleeves (west wall) | W "שרוול פלדה Ø4" ... Rainbow 54R ... מהרצפה c.l.=150cm מהתקרה c.l.=30 cm, הזנת חשמל 0.1kw 1ph"; S leader hits the wall at z about 2.37 | z 2.335, h 1.50 and H - .30 (L1742) | 3 cm | OK |
| A14 | Mamad filter box | S 35 (off the wall) x 40, z 2.185..2.585, identical on both MEP sheets | 21 x 50, z 2.085..2.585 (L1739-1741) | 14 cm depth, 10 cm width | Off if the symbol is to size (not certain). Change 9 |
| A15 | "H=2.63" on the mamad notes | W on three sleeve notes (air conditioning, air release, 4" intake) that have different offsets under the ceiling | H = 2.60 (estimate) | 3 cm | It can only be the mamad ceiling (interpretation). Keep 2.60 (not changing a global estimate for 3 cm) |
| A16 | "S" box by the TV wall | S box on the living side near x 4.7, z 0.0 | not modelled | n/a | Probably the AC wall controller (not written). Electrical |

## 4. The recheck2 "Plumbing and AC" open list

| Open item | Outcome |
|---|---|
| Corridor return grille 14 cm south | Confirmed on the vector sheet: 14.5 cm south and 6 to 10 cm west (A2, change 3) |
| "H=2.63" | Mamad ceiling reference, 3 cm over the 2.60 estimate; no change (A15) |
| Passage 120 vs 98 | Written 120 on the construction sheet (yellow, a tenant change). Geometry agent (section 6) |
| Family bath pipe box NW vs SW | NW on both vector sheets (P3, change 1) |
| Master split position | Over the master door, on the room face of the door wall (A8, change 2) |
| Condenser outline | 100 x 45 main unit plus an 84 x 40 second unit (A10, change 6) |
| High/low cisterns vs concealed | Sheets draw exposed cisterns; the model's concealed ledges are a design choice (P2, P8) |
| Mamad filter size | 35 x 40 on both sheets (A14, change 9) |
| Bulkhead depth .73 vs .80 | 78 cm on the vector sheet: the model's .80 is right (A3) |
| Balcony drain 1 z | +13 cm, and both drains 16 to 19 cm too far east (P19, P20, change 7) |
| Blast door 4 to 9 cm west | Sheet door 79 wide at -2.03..-1.23 (east anchor): 4 to 5 cm, and the sign flips on the west anchor. No change |
| Master shower head | Wall outlet on the west wall at H-210 (P11, change 4) |
| Isolator 3x16A IP65 | In the niche next to the condenser. Electrical |
| Riser 1 | Behind the heater, (4.04, -4.96) (P16, change 11) |
| Kitchen riser 3 / drain 13 | In the building core by the lift, outside the model (P24) |
| Shower 50 + 46 vs 92 | 92 on plumbing, 96 on construction; the size follows the master bath room fix (P12) |
| "S" box | AC controller or electrical (A16) |

## 5. Not changed, for the record

- Master mixer: plumbing says 50 from the north end, construction 55. The model (49) matches the plumbing sheet; moving
  it 6 cm on the conflicting figure is not worth it.
- The heater is placed correctly; only its diameter is 6 cm small (optional change 10).
- The niche notes "מעקה קל H=105" and the open-edge line are architectural; the facade position belongs to geometry.

## 6. Notes for the other agents

| Item | Sheet | Model | Owner |
|---|---|---|---|
| Passage, corridor to living | W 120 (construction), east end matches the model, so the west end is at about x 1.77 | 1.99..2.97 = 98 (L892 `W(-0.25, 1.99, ...)`, L898 ceiling `B(1.99, 2.97, ...)`) | Geometry |
| Corridor width | W 105 (construction, probably the corridor); S 115 (AC) | 110 | Geometry |
| Family bath | W 246 x 253, tub 163 (construction) | 238 x 245, tub 158.5 | Geometry |
| Master bath | W 230 wide from a 6 cm lining, about 179 N-S (construction) | 222 x 172 | Geometry |
| Mamad | S about 3.66 wide, north wall 20 cm | 3.55, north wall 27 cm | Geometry |
| Balcony | S north inner face z 0.35, south inner face 8.80, facade outer face 7.67 | .34, 8.71, 7.70 | Geometry |
| Family bath south wall | W red note "יש לבנות קיר זה בגובה H=45" | full wall | Geometry / electrical |
| Niche isolator "3x16A IP65" and an outlet | S next to the condenser | not checked | Electrical |
| Modular cable transit, mamad east wall | W "מעבר מודולרי חורשתי למעברי כבילה ותשתיות", z 0.24..0.51 | not modelled | Electrical |
| DESIGN.md line 26 | still says `DROP = H - .25` | code is H - .35 | Docs |

## Proposed changes

Line numbers are from the current working copy. Positions in `withShift` blocks are written values (effective minus the
shift). Run `build_site.py`, `roomdims.py` and `clearance_audit.py` after changes 1, 2 and 6.

1. **Family bath riser box to the NW corner** (W symbol on two sheets, S position; confidence high).
   The riser sits inside the WC ledge (to 1.10) and behind the WC column cabinet (from UB = 1.55), so only the stretch
   between them shows. L1519:
   `B(2.01, 2.20, -1.605, -1.395, 0, H, mat.bathWall2);   // pipe box in the corner (plan), 19 x 21 cm`
   becomes
   `B(2.01, 2.20, -3.775, -3.575, 1.10, UB, mat.bathWall2);   // riser 2 box in the NW corner (plumbing + construction), 19 x 20; hidden by the WC ledge below and the cabinet above`
   The socket on the old box, L1755 `outlets('n', -1.605, 2.105, 1.10, 's')`, moves onto the wall face behind it:
   `outlets('n', -1.395, 2.105, 1.10, 's')` (or wherever the electrical audit puts it). The towel hooks at L1520 are
   unaffected.

2. **Master split over the master door** (S outline, arrow and drain points on two sheets; confidence medium-high).
   L1751-1752:
   `// MASTER: wall split for the bedroom (12,300 BTU on the AC plan) high on the west wall by the door, condensate drain to the corridor`
   `B(4.61, 4.83, -2.295, -1.395, 2.24, 2.52, M('#f4f4f2', .35), { round: .03 }); B(4.83, 4.833, -2.255, -1.435, 2.27, 2.31, mat.slot, { cast: false });`
   become
   `// MASTER: wall split (12,300 BTU on the AC plan) over the door on the room face of the door wall, blowing east; condensate down the jamb (AC plan)`
   `B(4.26, 4.46, -1.14, -0.30, 2.24, 2.52, M('#f4f4f2', .35), { round: .03 }); B(4.46, 4.463, -1.10, -0.34, 2.27, 2.31, mat.slot, { cast: false });`
   Unit height and depth stay estimates. Check that nothing else sits on that wall over the door (lights, curtain).

3. **Corridor return grille** (S; confidence medium). L901-902:
   `B(1.80, 2.60, -1, -.4, DROP - .006, DROP, grilleM, ...)` becomes `B(1.88, 2.68, -1.145, -.545, DROP - .006, DROP, grilleM, ...)`
   `for (let x = 1.84; x < 2.58; x += .035) B(x, x + .012, -.97, -.43, ...)` becomes
   `for (let x = 1.92; x < 2.66; x += .035) B(x, x + .012, -1.115, -.575, ...)` (rest of both lines unchanged).
   Check the corridor downlight at (1.03, -0.665) and the passage ceiling at x 1.99 for overlap (none expected).

4. **Master shower head on the west wall at 2.10** (W type and height, S position; confidence medium).
   Inside `withShift(.19, 0)`, so x 4.446 is the effective west wall 4.636. L1404:
   `C(4.97, -4.52, 2.05, 2.06, .15, mat.blackMetal); C(4.97, -4.52, 2.06, H, .008, mat.blackMetal, { seg: 6 });`
   becomes
   `B(4.446, 4.80, -4.595, -4.575, 2.09, 2.11, mat.blackMetal); C(4.80, -4.585, 2.04, 2.05, .15, mat.blackMetal);   // wall arm, head H-210 (plumbing plan), 37 cm from the north end`
   z -4.585 splits the two sheets (35 and 40 from the north end). The arm length (35 cm) is an estimate.

5. **Living supply grille 2** (S, +14 to +21 cm; confidence medium). L1126: `[2.20, 5.75].forEach(` becomes
   `[2.20, 5.90].forEach(`.

6. **Niche condenser to the drawn footprint, fan toward the screen** (S; confidence medium). Inside
   `withShift(.22, -.45)`, effective x 2.30..3.30, z -5.05..-4.60 means written x 2.08..3.08, z -4.60..-4.15.
   L1530 body: `B(2.08, 2.97, -4.80, -4.46, .03, .66, ...)` becomes `B(2.08, 3.08, -4.60, -4.15, .03, .98, ...)`
   (height .95 is an estimate for a single-fan 52,000 BTU unit). The fan disc and torus rings (L1530-1533) move to
   the north face: position z -4.605 instead of -4.455/-4.452, centre (2.48, .50) scaled to the taller body, radius up
   to about .30. The side slots (L1534) move to x 3.08 face or the south face, and the refrigerant pair (L1535,
   z -4.70) to z -4.30, starting at the new top .98. The drain tube start (L1536) follows. Optional: a second
   84 x 40 x 60 unit (the master split condenser) on brackets above it, effective x 2.83..3.68, z -5.00..-4.60
   (interpretation, low). Check the clothesline brackets at 1.95..2.05 still clear.

7. **Balcony floor drains** (S; confidence medium-low). L1780: `[[9.05, 1.5], [9.08, 7.3]]` becomes
   `[[8.89, 1.63], [8.89, 7.36]]`.

8. **Niche drain riser** (S, 8 cm; confidence low). L1528: `C(2.21, -5.02, 0, H, .055, ...)` becomes
   `C(2.21, -4.94, 0, H, .055, ...)`. Make sure it clears the condenser after change 6 (effective x 2.30 starts 3.5 cm
   east of the riser surface).

9. **Mamad filter box 35 x 40** (S symbol, identical on both sheets, may be schematic; confidence low-medium).
   L1739: `B(-3.8, -3.59, 2.085, 2.585, 1.22, 1.78, ...)` becomes `B(-3.8, -3.45, 2.185, 2.585, 1.22, 1.78, ...)`.
   L1740 louvres: `B(-3.59, -3.587, 2.145, 2.525, ...)` becomes `B(-3.45, -3.447, 2.215, 2.555, ...)`.
   L1741 panel: x `-3.587, -3.57` becomes `-3.447, -3.43`; screen x `-3.59, -3.587` becomes `-3.45, -3.447` and its
   z `2.165, 2.305` becomes `2.225, 2.345`; selector z `2.395, 2.455` stays. Run `clearance_audit.py` (14 cm more
   depth into the mamad).

10. **Optional: heater diameter 60** (S, 6 cm on size; low). L1539: radius `.27` becomes `.30` on the first `C(...)`.

11. **Optional: riser 1 "קולטן Ø110" behind the heater** (S; low). After the `withShift` block closes (after L1540):
    `C(4.04, -5.05, 0, H, .055, M('#d9d6cf', .6), { seg: 16 });   // riser 1, Ø110 (plumbing plan, scaled)`.
    Clearance to the heater (effective centre z -4.69): its north edge is at -4.96 (r .27) or -4.99 (r .30), the riser's
    south edge at -4.995, so a 3.5 cm gap now and 0.5 cm after change 10. With change 10, use z -5.07.

12. **Geometry agent: passage 120** (W; requires `roomdims.py` and `clearance_audit.py`). L892
    `W(-0.25, 1.99, -0.145, 0)` becomes `W(-0.25, 1.77, -0.145, 0)` and L898 `B(1.99, 2.97, ...)` becomes
    `B(1.77, 2.97, ...)`. After change 3 the return grille (x 1.88..2.68) sits wholly in the corridor, north of this
    wall, so the two do not clash.

Not proposed (under 5 cm on scaled positions, or conflicting written values): mamad door, master mixer, H = 2.63,
grille 1, bulkhead depth, filter sleeves, washer and tub points.
