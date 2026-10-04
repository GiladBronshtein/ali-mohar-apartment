# Geometry re-check 2: walls, rooms, openings (2026-10-04)

This is a read-only audit of `source/salon.html` (2365 lines) against the plans. No model file was edited and git was not run.
Everything below was derived again from the sources. The earlier audits were only compared at the end (section 9).

## Sources, method, baseline

- **Sales plan PDF** (`newBA_K1-4_DIRA_2-4-6-8_250701_123041.pdf`):
  - The PDF is one embedded JPEG. It was extracted with `pdfimages` to `geo_crops/pdf-000.jpg`.
  - Orientation: plan right is model -z, plan down is model +x. The colour photo is the same drawing rotated 180 deg.
- **Calibration**, per axis, from written dims far apart (877/879, 728, 361, 356, 365):
  - Isotropic 0.7873 px/cm.
  - px = 1373.5 - 78.73 z, py = 459.07 + 78.73 x.
- **Face convention:**
  - The wall face is taken 1.1 px inside the room from the outline edge (luminance 130).
  - With this convention the written interior dims fit within +/-0.3 cm: corridor 109.9, room 2 x 281.9, dining 276.9, kitchen x 365.3, master z 295.8, closet x 189.7, room 1 x 273.7 and z 360.9.
  - Without the 1.1 px shift, the exterior walls match the model exactly, but the interiors read about 2.5 cm small.
  - The resolution is therefore about +/-1.4 cm per face and +/-2.8 cm on a span. Only differences over about 3 cm, or qualitative differences, are flagged.
  - Faces compared with a neighbouring face (same image row or column) are good to about 1.5 cm.
- **Drawing vs written dims:** some rooms are drawn larger than their written dims:
  - family bath scales 248 x 241 (written 245 x 238)
  - master bath scales 175 x 225 (written 172 x 222)
  - mamad scales 359 x 265 (written 355 x 262)
  - room 2 z scales 354 (written 356)

  The model follows the written dims, as the project rule requires.
- **Plan note under the drawing (written):** "המידות הינן מידות בניה (ברוטו) מקיר לקיר לפני טיח, למעט מרפסת שמש בה המידות הן מקיר חוץ".
  - In English: the dimensions are gross construction dims, wall to wall before plaster. The sun balcony is the exception: its dims are taken from the outer wall.
  - This matches the model's brick-to-brick walls and its balcony measured from the facade outer face (BX1 = FO = 7.70).
- **MEP photos** (`electrical_IMG_8065`, `plumbing_IMG_8066`, `ac_IMG_8067`): used only where they bear on walls. Fixture and outlet offsets belong to the parallel electrical and plumbing/AC reports.
- **Baseline today:**
  - `roomdims.py`: +0 for every room. The closet z 485/175 is the known probe artifact.
  - `clearance_audit.py`: 0 issues.
- **Crops** are in `geo_crops/`. `ov_*` and `z_*` are PDF crops (3x to 8x) with the model walls at y 0.5 outlined in red. `pdf_full_small.jpg` is the whole sheet.

## 1. Written dimensions (sales plan)

| item | plan (written) | model | delta | verdict |
|---|---|---|---|---|
| mamad | 262 x 355 | 262 x 355 (z .125..2.745, x -3.80..-0.25) | 0 | OK |
| room 1 | 361 x 274 | 361 x 274 (z -5.035..-1.425) | 0 | OK. See 4.1 for the face position |
| room 2 | 356 x 282 | 356 x 282 | 0 | OK |
| dining | 277 | 277 | 0 | OK |
| corridor | 110 | 110 | 0 | OK |
| living x | 728 | 728 | 0 | OK |
| living + kitchen z | 879 | 879 | 0 | OK |
| kitchen x | 365 | 365 | 0 | OK |
| family bath | 245 x 238 | 245 x 238 | 0 | OK |
| master | 430 x 296 | 430 x 296 | 0 | OK |
| master bath | 222 x 172 | 222 x 172 | 0 | OK |
| closet | 190 x 175 | 190 (175 is the probe artifact) | 0 | OK |
| balcony | 884 x 275 | 884 (-0.13..8.71) x 275 (7.70..10.45) | 0 | OK. See section 5 |
| room labels (L2052-2053) | the numbers above (the plan has no room names) | same pairs | 0 | OK |

## 2. Facade openings (scaled, corrected convention)

| item | plan | model (line) | delta | verdict |
|---|---|---|---|---|
| living door A | z .788..3.438 | .78..3.45 (L847) | -1 / +1 | OK |
| pier A-B | 3.438..4.288 (zoom 3.452..4.26) | 3.45..4.26 | under 3 | OK |
| living door B | z 4.288..6.886 | 4.26..6.88 | -3 / -1 | OK |
| window C, kitchen | z 7.713..8.403 (8x zoom) | 7.70..8.39 (L847, slider L997) | -1 / -1 | OK |
| room 1 window | z -2.913..-1.963 | -2.92..-1.93 (L1507) | -1 / +3 | OK |
| mamad window | z .467..1.441 (zoom) | .47..1.44 (L1582) | 0 | OK |
| room 2 window | x .27..1.218 | .27..1.25 (L1528) | 0 / +3 | OK, at the noise limit |
| master east window | z -2.275..-1.329 | -2.27..-1.31 (L1329) | 0 / +2 | OK |
| master bath window | x 6.021..6.57 | 5.99..6.58 (L1349) | -3 / +1 | OK, at the noise limit |
| balcony doors A, B type | two offset tracks (sliding, 2 panes) | slider 2 panes | n/a | OK |
| sash type: room 1, room 2, master east, window C | one sash per window, drawn swung inward (casement or tilt-turn) | windowZ/windowX draw a centre mullion (2 panes) for room 1, room 2, master east and master bath. Window C and the mamad have 1 pane | qualitative | FIX, low (item 4) |
| master bath window type | single frame, no swing line | 2 panes | qualitative | FIX, low (item 4) |
| mamad window shutter | a steel shutter pocket runs inside the wall to the **south** (+z) of the opening, x about -4.09..-4.04 | frame only (L1583) | hidden in the wall | OK, not visible |
| sills and heads | not on any plan | estimates | n/a | estimate |
| master east window, sill 0 | same symbol as room 1 (no sill shown on any sheet checked) | floor length, comment "as in the plan" (L1329) | n/a | OPEN |

Without the 1.1 px shift, the window widths match within 1.5 cm. With it they read 2 to 4 cm narrower. This is the convention limit, not a finding.

## 3. Doors (scaled)

| item | plan | model (line) | delta | verdict |
|---|---|---|---|---|
| room 1 | x about -2.08..-1.23, hinge east, swings into room 1 | -2.06..-1.23, hinge -1.24 (L854, L931) | -2 / 0 | OK |
| room 2 | x .915..1.776, hinge east, into room | .93..1.77 (L856, L932) | +1.5 / -0.5 | OK |
| family bath | x 2.846..3.707, hinge east, into bath | 2.86..3.69 (L858, L933) | +1.5 / -1.5 | OK |
| master | z -1.159..-0.343 (8x zoom), hinge on the TV-wall side about -0.37, into master | -1.16..-0.34, hinge -0.35 (L864, L934) | 0 | OK |
| master door wall | x 4.148..4.264 (8x zoom) | 4.15..4.26 (L864) | 0 | OK |
| master bath | z about -4.095..-3.348, hinge about -3.40, into bath | -4.06..-3.36, hinge -3.365 (L863, L936) | -3.5 / +1 | OK |
| closet opening | x about 7.545..8.33 | 7.54..8.32 (L862) | 0 / -1 | OK |
| corridor to alcove passage | x 1.982..2.983 | 1.99..2.97 (L868) | +1 / -1 | OK |
| entry | x 1.563..2.564, hinge west, opens inward | 1.585..2.555, hinge west (L844) | +2 / -1 | OK |
| mamad blast door, rough opening | x -1.99..-1.19 (80) | -1.98..-1.19 (79) (L866) | 0 | OK |
| mamad blast door, hinge and swing | hinge at the west end (x -1.947), leaf open 90 deg into the corridor | hinge -2.0, opens into the corridor (L935) | 5 | OK |
| mamad blast door, leaf length | drawn leaf z -0.13..-0.857 = 72 cm; the arc ends at x -1.243 (radius about 70 to 72) | leaf .86 | -14 (scaled) | OPEN |

## 4. Walls and faces (scaled, relative to neighbours)

| item | plan | model (line) | delta | verdict |
|---|---|---|---|---|
| north facade inner face, rooms 1 and 2 | room 1 -5.013, room 2 -5.010: **flush** | room 1 -5.035, room 2 -5.01 (L834, L836) | room 1 -2.2 | FIX, low (item 3) |
| room 1 / corridor wall, x -2.36..-1.15 | about -1.404..-1.253 (8x zoom: about 11.5 thick) | -1.425..-1.245, 18 thick (L854) | room face -2.1 | FIX, low (item 3) |
| room 1 / room 2 wall | x -1.155..-1.00 | -1.15..-0.97 (L855) | 0 / +3 | OK. The written 282 governs |
| room 2 / corridor face | -1.253 | -1.245 | +1 | OK |
| TV wall, corridor stretch x 2.97..4.15 | 0 / -0.204 | 0 / -0.19 (L852) | +1.4 | OK |
| TV wall, panel recess | at z -0.07 the wall breaks over x 3.352..3.784. The wall reads 10.7 there | panel x 3.33..3.78 (electrical) | under 3 | OK, cross-check in the electrical report |
| TV wall, alcove and master stretches | -0.154 | -0.145 | +1 | OK |
| TV wall step beside the master door | x 4.27..4.781, about 8.5 deep | 4.26..4.76, z -0.24 (L865) | -2 | OK |
| entry wall, hall side | z 5.51 | 5.50 (L844) | -1 | OK |
| **entry wall, kitchen stretch x 3.63..4.30** | **z 5.51..5.61, about 11 thick, ends at x 4.30** (`z_entry_kitchen.jpg`; the profile at x 3.7, 3.9, 4.1, 4.25 shows 9 px with outlines) | **5.50..5.70, 20 thick, ends at x 4.26** (L844) | **kitchen face +9; end -4** | **FIX, medium (item 2)** |
| entry wall, lobby stretch x 1.19..3.63 | 5.51..5.76 (25) | 5.50..5.70; the lobby mass starts at 5.70 (L842) | hidden | OK |
| kitchen / lobby wall | kitchen face x 3.61 | 3.63 (L842) | +2 | OK. The written 365 governs |
| bath stub wall | z -3.004..-3.115 (11 thick), north end x 3.695 (8x zoom) | -2.98..-3.09, x 3.69 (L860) | -2.4, same thickness | OK |
| bath / laundry wall | -3.811..-4.037 | -3.775..-3.99 (L859) | +3.5 | OK. The written bath 238 governs |
| niche side wall, corridor west end | west face -2.395; room 1 niche depth 143 | -2.36; depth 145 (L840) | +3.5 / +2 | OK, at the noise limit, not written |
| mamad north wall | z .069..-.14 (21) | .125..-.145 (27) (L866) | +5.6 room side | OK. The written mamad 262 governs |
| mamad west face | -3.842 (drawn 359 long) | -3.80 | +4 | OK. The written 355 governs |
| laundry niche north wall | inner face about -5.15 | -5.11 (L835) | +4 (+2.5 with the convention) | OK, at the noise limit |
| master east facade | inner 8.92 | 8.91..8.92 | 0 | OK |
| exterior outer faces | +3.4 thicker with the corrected convention, exact without it | n/a | convention | OK |

## 5. Balcony (`ov_balcony.jpg`, L1588-1596)

| item | plan | model | delta | verdict |
|---|---|---|---|---|
| 884, written | the dim runs from the south wall inner face to the outer north edge line (z -0.113) | BZN -0.13 .. BZ2 8.71 | 0 | OK |
| 275, written, from the outer wall per the plan note | ticks at x 7.707 and 10.506 (scales 280) | FO 7.70 .. BX2 10.45 | written governs | OK. The scale is stretched about 2 % here |
| north wall (balcony side), x 7.70..9.30 | inner .355, outer -.154, ends at x 9.317 | BZ1 .34, BZN -.13, BN 9.30 | +1.5 / -2.4 / +2 | OK |
| south end wall | z 8.747..9.287, to x 10.11 | 8.71..9.20, to BS 10.07 | +3.7 inner (written 884 governs), +4 end | OK |
| east open edge | the deck stops at x 10.21. Lines follow at 10.26, 10.30, 10.40 and 10.50 (outer) | 15 cm parapet 10.30..10.45, 20 high, railing at 10.35..10.37, deck up to 10.30 | deck +9 | OPEN |
| north open edge, x 9.30..10.45 | the deck stops at z 0.18. Lines follow at 0.13, 0.08, -0.02 and -0.12 (outer) | parapet -0.13..0.02, deck up to 0.02 | deck +16 | OPEN |
| downpipes (⊕ in walls) | south end wall about (9.04, 8.99); master south-east about (9.08, 0.09) | none | hidden in the wall | OK |

The same edge pattern appears on both open sides: about 30 cm from the deck edge to the outer line. It could be an upstand, a planter, or a set-in railing. It is not written, so it stays OPEN.

## 6. Columns, shafts, niches, symbols

| item | plan | model | verdict |
|---|---|---|---|
| family bath pipe box, south-west corner | 19 x 21 box with a pipe circle | B(2.01, 2.20, -1.605, -1.395) (L1472) | OK |
| "column 2", north-west corner of the family bath (plumbing sheet) | the sales plan shows nothing in that corner (`z_col2.jpg`) | none | OPEN. The sheets still conflict |
| "column 1", laundry niche | two ⊕ stacks drawn free-standing at about (4.01, -5.00) and (4.25, -5.00), inside the heater circle; small pipe circles beside them (`z_col1.jpg`). No boxed column is drawn | not modelled as geometry | OPEN. This is a plumbing item, not a wall |
| drain stacks in the west facade | ⊕ at about x -4.08, z -0.87 and -1.10 | none | OK, inside the wall |
| drain stack, master north-east | ⊕ at about (9.12, -5.23) | none | OK, inside the wall |
| laundry niche | louvers on the facade, heater circle, washer circle | louvers, heater, washer/dryer | OK |
| lobby shafts and meter cabinets (3 stubs), stair, lobby door | outside the unit | solid lobby mass (L842) | OK, not visible |
| wardrobe niches (room 1, mamad) | room 1 niche z -0.81..-1.40 opens into room 1; mamad niche z .09..-.50 opens into the mamad | same | OK |
| steps and thresholds | none drawn (balcony doors drawn as sliders) | balcony deck at -0.04 (estimate) | OK, estimate |

## 7. Plan vs model presence

- **The plan has, the model lacks:**
  - Single inward-opening sashes (section 2).
  - The balcony edge zone of about 30 cm (section 5).
  - The two exposed drain stacks in the laundry niche.
  - All other plan items (downpipes inside walls, the mamad shutter pocket, lobby shafts) are hidden or outside the unit.
- **The model has, the plan lacks:**
  - The master east window at floor length (sill 0).
  - The 20 cm balcony parapet. Its height is an estimate, and so are all sills, heads and the ceiling.
  - No model wall without a plan counterpart was found. The TV-wall step, pipe box, bath stub, 19 cm corridor stretch and closet walls are all on the plan.

## 8. Proposed changes, ordered by confidence

1. **High. Info text L177 (no geometry).**
   - Replace "לא כתוב בשרטוט אם המידות כוללות טיח וחיפוי. אם לא, החדרים בפועל יהיו קטנים ב-2 עד 6 ס״מ" with the plan's own note: the dimensions are gross, wall to wall before plaster (the balcony from the outer wall). Then: "לכן החדרים הגמורים יהיו קטנים בערך ב-2 עד 6 ס״מ (הערכה)".
   - The 2 to 6 cm figure stays labelled as an estimate.
   - No roomdims effect.
2. **Medium. Entry wall, kitchen stretch (L844).**
   - Change `W(2.555, 4.26, 5.50, 5.70);` to `W(2.555, 3.63, 5.50, 5.70); W(3.63, 4.30, 5.50, 5.61);`.
   - Dependents:
     - kitchen floor L912 `[3.63, 4.26, 5.70, 8.78]` to `[3.63, 4.30, 5.61, 8.78]`
     - entry floor `[4.26, FX, 5.50, 8.78]` starts at 4.30
     - the fridge column and its trim L1212-1241: z 5.70/5.71/5.72 to 5.61/5.62/5.63. Alternatively, keep them and accept a 9 cm void behind the fridge, which is visible from x 4.29.
     - the skirting and wallBoxes entries for that face
   - The fridge already ends at x 4.29, which matches the plan's wall end of 4.30.
   - This does not move a measured room wall. The kitchen probe runs along x at z 6.89, and the living + kitchen probe runs at x 5.18, so roomdims stays +0.
   - Re-run `clearance_audit.py` (the island and fridge clearances).
3. **Low, invisible in practice. Room 1 faces flush with room 2, as drawn.**
   - North face -5.035 to -5.01, and the corridor-side face -1.425 to -1.40. 361 is kept.
   - This moves room walls. roomdims must stay +0: its probe at x -1.63 reads -5.01..-1.40 = 361.
   - Edits:
     - L834 `W(-4.28, -1.14, -5.39, -5.035)` to `-5.01`
     - L836 `W(-4.28, -3.89, -5.035, -2.92)` to `-5.01`. Optionally move the facade jog at -1.425 on L836 to -1.40.
     - L854 every `-1.425` to `-1.40` (keep `W(-1.15, -0.97, -1.45, -1.245)`)
     - L855 `W(-1.15, -0.97, -5.035, -1.425)` to `(-5.01, -1.40)`
     - L879 grille `[-1.425, -1.65]` to `[-1.40, -1.65]`
     - L914 floor `[-3.89, -1.15, -5.035, -1.425]` to `[-3.89, -1.15, -5.01, -1.40]`
     - L950 doorFrame z `-1.425` to `-1.40`
     - L962 plate `['n', -1.425, -2.18]` to `-1.40`
     - L931 room 1 leaf hinge z `-1.355` to `-1.33`
     - room 1 furniture on the north wall: +0.025
   - Re-run clearance: "room1 door leaf end <-> low unit" is at 0.04 today.
   - The delta is 2.1 to 2.2 cm, below the absolute threshold. It is listed only because the relative comparison (room 1 face vs room 2 face, same image row) is reliable to about 1.5 cm. Skip it if the churn is not worth it.
4. **Low. Window divisions (L1329, L1507, L1528, L1349).**
   - The plan draws one sash per window, not two.
   - Room 1: `windowZ(..., 2)` to `1`. Master east: `2` to `1`.
   - `windowX` (L792) always draws a centre mullion. Add a `panes = 2` parameter and pass 1 for room 2 (L1528) and the master bath (L1349).
   - The family bath to niche window (L1391) was not checked for a sash. Leave it.
   - The plan sash may be a generic symbol.
   - No roomdims effect.

## 9. Comparison with the earlier audits

- **`audit/recheck/geometry.md`:**
  - Its FIX items are all in the code now and agree with this check: room 2 door .93..1.77, entry 1.585..2.555, TV-wall corridor stretch -0.19, BZ1 .34.
  - Its entry wall reading (5.478..5.756, "hidden by the lobby mass") holds only for x < 3.63. It missed the thin, visible kitchen stretch (item 2).
  - Its balcony south wall (8.731..9.237) is close to this check (8.747..9.287).
  - It did not report the mamad leaf radius, the balcony edge zone, the single sashes, or the plan's plaster note.
- **`audit/report.md` (older):**
  - It already noted the casement sashes (room 1, window C). That agrees with item 4.
  - Its mamad hinge "wrong side" issue is fixed in the code and confirmed here.
  - Its D20/D21 balcony mismatches are fixed (884 x 275 now).

## OPEN

- Mamad blast-door leaf: drawn about 72 long (scaled), model .86. The opening is 80 on both.
- Balcony edge zone: the deck is drawn to x 10.21 and z 0.18 with about 30 cm of edge lines. The model has a 15 cm parapet with the deck up to it. Not written.
- Balcony 275 scales 280 to the outer line. The written value governs.
- Master east window sill 0: no plan source found. The symbol is the same as room 1's (model sill .95).
- "Column 1" (two exposed stacks in the laundry niche) and "column 2" (north-west bath corner: absent on the sales plan). For the plumbing report and the contractor.
- Entry wall end x 4.30 vs 4.26: inside item 2. On its own it is at the noise limit.
- Convention limit: +/-1.4 cm per face. Items under 3 cm are not findings, except item 3, which is relative.
