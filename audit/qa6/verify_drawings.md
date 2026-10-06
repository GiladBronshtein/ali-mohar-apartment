# QA6: verify_drawings (independent second pass over d01-d07)

Scope: d01 (apartment sheet), d05 (typical floor), d03 (ground), d02 (basement), d04 (roof), d06 (sales notes), d07 (studio
spec). Re-derived from the vector PDFs in `source/out/docs5/`. I did not use the numbers in `audit/recheck5/*.md`.
Working files (scripts, overlays, grids): `source/out/qa6_verify_drawings/`. Renders: `source/out/qa/qa6_vd/`.
Images that show a defect: `audit/qa6/verify_drawings_img/`.

## Calibration (used for every number below)

- d01 is printed at about 1:75, not at the 1:50 in its title block. The scale comes from the long written dimensions, tick to
  tick: 728 = 277.14 pt, 879 = 334.26 pt, 884 = 336.00 pt, so 38.07 pt/m in x and 38.03 pt/m in z. Short room dimensions
  scale 1 to 3% larger on the sheet (rounding on the drawing; d06 note 2 allows 2%).
- Model frame on d01: pt = (257.36 + 38.07 x, 429.30 + 38.03 z). The 728 and 879 ticks fall exactly on x 0 / 7.28 and z 0 / 8.79.
- Sheets registered line by line (vote over all heavy wall lines, sharp peak):
  d05 = 0.500 * d01 + (269.4, -21.6); d03 = 0.748 * d05 + (82.2, 110.8); d02 = 1.0035 * d03 + (59.5, 59.3) (lot outline).
- Result: d05 pt = (398.08 + 19.035 x, 193.05 + 19.015 z); d03 pt = (379.96 + 14.238 x, 255.20 + 14.223 z);
  d02 pt = (440.79 + 14.288 x, 315.39 + 14.273 z).
- Check: in this frame the ground-floor concrete on d03 lands on the d01 concrete within 5 mm (west -4.15, north -5.24/-5.25,
  east 9.16, kitchen south 8.89/8.89). Parking stalls scale to 4.96-4.97 m long.

## Findings (most severe first)

1. **Exterior scale of re-check 5 is about 1.3% too large; lot W and S lines and Tirtsa Atar are 0.32 to 0.42 m off.** CONFIRMED.
   - Cause: re-check 5 fitted the d03 concrete lines (west -4.15, north -5.25, east 9.16) to the model's clad outer faces
     (-4.28, -5.39, 9.30). That stretches d03 by about 1.5 to 2%. Its implied scale is about 14.05 pt/m against 14.23.
   - Errors (model vs d03 in the frame above): lot wall W x -22.5..-22.3 vs -22.09..-21.86 (0.42 m); lot wall S z 47.8..48.0 vs
     47.42..47.62 (0.38 m); Tirtsa Atar sidewalk z 48..50.5 vs 47.62..50.10 (0.38/0.40 m); road from 52.5 vs 52.18 (0.32 m).
     Near the building the error stays under 0.3 m (lot N 0.16, lot E 0.12, columns up to 0.17, Ali Mohar near side up to 0.22).
   - Image: `verify_drawings_img/d03_south_edge_vs_model.jpg` (red = model, sheet underneath).
   - Fix, salon.html 2054-2059 (OUR LOT):
     ```js
     lotWall(-22.06, 14.18, -11.74, -11.55); lotWall(-22.06, -21.86, -11.55, 47.62);
     [[-11.55, 9.95], [14.85, 28.28], [30.38, 39.45]].forEach(([a, b]) => lotWall(13.97, 14.17, a, b));
     lotWall(-17.74, 6.15, 47.42, 47.62);
     // rounded SE corner: centre (6.15, 39.5), R 7.95 (was (6.1, 39.7), R 8.1)
     B(-21.86, -17.74, 47.46, 47.54, GY, GY + 1.6, mFence, OUT);   // car gate (d03 bar x -21.89..-17.74)
     ```
     and 1866-1867 (Tirtsa Atar): sidewalk `B(-160, 16.9, 47.62, 50.10, ...)` and `B(34.2, 160, 47.62, 50.10, ...)`; asphalt from
     z 50.10 (d03 road hatch starts at the sidewalk edge); far kerb unknown, keep the 8 m road from 52.18 if wanted. See finding 6
     for the parking strip. Also line 2047: north fence and weeds stop at z -11.74 and x 14.18.

2. **Car-park ramp is drawn in the wrong place and as flat lawn.** CONFIRMED.
   - d03 draws an open ramp lane (dashed centre line, two arrows, side walls) from z -0.47 to z 21.45, x -21.86 (lot wall) to
     -15.11 (wall lines -15.11/-14.94/-14.92), with orange-hatched strips on both sides. A barrier bar sits at x -21.19..-18.16,
     z 20.95..21.45 on the down lane. d02 shows the same lane inside the basement with the drainage grille at z -0.4..0 and the
     basement gate (bar with motor) at z 0..0.4. So the ramp falls northwards from about z 21.4 to the basement gate at z 0.
   - Model 2074-2075: a flat grille "portal" at z 17.4..21.4 and nothing north of it, so the lane z 0..17.4 renders as lawn
     (ground mask). Image: `verify_drawings_img/d03_ramp_stalls_vs_model.jpg`, `model_ramp_stalls.jpg`.
   - Fix: delete 2074-2075. Cut a hole in the ground plane (1865) and add a sloped lane:
     ```js
     [[-240, 260, -250, -.69], [-240, 260, 21.45, 250], [-240, -21.86, -.69, 21.45], [-14.92, 260, -.69, 21.45]].forEach(([a, b, c, d]) => {
       const g = new THREE.PlaneGeometry(b - a, d - c); g.rotateX(-Math.PI / 2); g.translate((a + b) / 2, GY, (c + d) / 2); mesh(g, mat.ground, outside, false); });
     { const L = 21.92, D = 3.0;   // depth of the basement is not written (estimate)
       const m = mesh(new THREE.PlaneGeometry(6.75, Math.hypot(L, D)), mat.asphalt, outside, false);
       m.rotation.x = -Math.PI / 2 - Math.atan2(D, L); m.position.set(-18.485, GY - D / 2, 10.49); }   // north end low
     B(-15.11, -14.92, -.47, 20.90, GY - 3.0, GY + 1.0, mKerb, OUT);                // east ramp wall, parapet 1.0 (estimate)
     B(-21.86, -14.92, -.69, -.47, GY - 3.0, GY + .5, mKerb, OUT);                  // wall over the basement gate
     B(-21.19, -18.16, 20.95, 21.45, GY, GY + 1.0, mat.blackMetal, OUT);            // barrier at the top of the down lane
     ```

3. **Stalls 1-4 are marked in the wrong direction.** CONFIRMED.
   - d03: a 2 x 2 block. Columns x -13.95 | -11.27 | -8.59 (2.68 wide), rows z -2.80 | 2.17 | 7.14 (4.97 long). Cars park
     north-south, wheel stops at the north end of each row.
   - Model 2070: four 2.5 m bays stacked along z, 5 m deep in x (lines at constant z). Visible in `model_ramp_stalls.jpg`.
   - Fix:
     ```js
     B(-13.95, -8.59, -2.80, 7.14, GY, GY + .03, mat.asphalt, OUT);
     [-13.95, -11.27, -8.59].forEach(x => B(x - .05, x + .05, -2.80, 7.14, GY + .03, GY + .036, mWhiteLine, OUT));
     B(-13.95, -8.59, 2.12, 2.22, GY + .03, GY + .036, mWhiteLine, OUT);
     ```

4. **Building A bar outline is too big.** CONFIRMED (d05 heavy wall lines, d03 for the ground floor).
   - East face: model 8.26 for z 9.11..30.6. d05 has the 8.07/8.27 face only on z 12.91..26.82 (the two middle flats). The flats
     at z 9.13..12.91 and 26.82..30.6 have their facade at 7.28/7.70 like ours, with the balcony in front. In the model the bar
     face stands 0.56 m in front of their facade, so the neighbour balcony next to ours looks half buried (`model_afront.jpg`).
   - West face: model -2.1. d05: -1.44 (z 9.0..15.5), -0.74 (z 16..23.5), -2.13 (z 24..26.5), -1.44 (z 27..29.5). Up to 1.36 m off.
   - Second balcony stack [26, 30.8] (line 1879) starts on the middle flat's wall; d05 puts it at z 26.82..30.6.
   - Ground floor: d03 has two closed blocks under the bar, x -1.43..5.35, z 13.18..18.96 and x -0.74..5.35, z 20.77..24.81
     (storage rooms), beside lobby A. The model shows open pilotis there.
   - Fix, 1876-1879:
     ```js
     building(-1.44, 7.70, 9.11, 12.91, 23.1, 'white', 3.3); building(-1.44, 8.27, 12.91, 15.75, 23.1, 'white', 3.3);
     building(-0.74, 8.27, 15.75, 23.75, 23.1, 'white', 3.3); building(-2.13, 8.27, 23.75, 26.82, 23.1, 'white', 3.3);
     building(-1.44, 7.70, 26.82, 30.6, 23.1, 'white', 3.3);
     B(-1.43, 5.35, 13.18, 18.96, GY, GY + 3.3, mat.stucco, OUT); B(-0.74, 5.35, 20.77, 24.81, GY, GY + 3.3, mat.stucco, OUT);
     sunBoxes.push([-1.43, 5.35, 13.18, 18.96, 3.3], [-0.74, 5.35, 20.77, 24.81, 3.3]);
     // balcony stacks: [[9.13, 12.91], [26.82, 30.6]]
     ```
     Optional (under 0.3 m): columns x 7.89..8.19, centres z 13.36, 16.59, 19.88, 23.16, 26.24 (last one 1.0 long).

5. **Planter and garden strip in front of building A are missing (seen from our balcony looking south).** CONFIRMED.
   - d03: a planted bed with a blue low-wall border, x 8.22..11.15, z 12.97..26.99, in front of the columns; a low wall from it to
     x 12.75 at z 12.95..13.05; a green strip x 12.54..13.97, z 14.85..28.28 along the lot wall; paved walk between them.
   - Model: nothing south of z 9.97 between the bar and the lot wall except the lawn mask. Images: `d03_afront_planter.jpg`,
     `model_afront.jpg`.
   - Fix (OUR LOT block, heights are estimates):
     ```js
     [[8.22, 11.15, 12.97, 13.11], [8.22, 11.15, 26.90, 26.99], [8.22, 8.37, 13.11, 26.90], [11.06, 11.15, 13.11, 26.90], [11.06, 12.75, 12.95, 13.05]]
       .forEach(([a, b, c, d]) => B(a, b, c, d, GY, GY + .4, mKerb, OUT));
     B(8.37, 11.06, 13.11, 26.90, GY, GY + .3, mat.turf, OUT); B(12.54, 13.97, 14.85, 28.28, GY, GY + .02, mat.turf, OUT);
     ```

6. **Tirtsa Atar parking on pavers is missing.** CONFIRMED.
   - d03: herringbone strip x -13.50..10.07, z 50.10..52.18, between the sidewalk and the road. The model leaves z 50.5..52.5 as
     bare ground (lawn-tinted) and has no parking there. Image: `d03_south_edge_vs_model.jpg`.
   - Fix (after `mPaver` is defined, about line 1925, or inside OUR LOT): `B(-13.50, 10.07, 50.10, 52.18, GY, GY + .04, mPaver, OUT);`

7. **Building B footprint and gardens are simplified.** CONFIRMED geometry, low impact (far from the flat).
   - d05: B's west wing starts at z 32.94 (x -9.66..-3.5); z 30.6..32.9 there is an open terrace. Model 1876 fills it for 7 storeys.
   - d03: B's private garden (bright green, rounded NW corner) x -13.66..-3.54, z 28.12..35.63; B's east garden walls
     x 8.27..12.35 at z 37.25..37.45, x 12.15..12.35 at z 30.52..37.25, x 8.31..13.97 at z 30.38..30.52; smoke vent x 11.13..12.16,
     z 34.05..37.08; an unlabelled box with an X across stall row 5-6 at x -8.85..-2.79, z 22.98..25.52 (the model paints a stall
     there). None of these are in the model.
   - Fix: split B into `building(-3.5, 8.26, 30.6, 32.94, ...)` + `building(-9.66, 8.26, 32.94, 42.6, ...)` and add the walls as
     `mKerb` boxes 0.4 high (estimate).

8. **d06 note 8 and the d01 level marks are not modelled.** CONFIRMED, low.
   - Note 8: mamad floor up to 3 cm higher, WC/bath/shower floors about 1 cm lower. d01 draws the "הפרש גבהים" mark at the mamad
     door, both bath doors, the master bath door, the entrance and the balcony doors.
   - Model (lines 869-879): mamad at y 0 like the living room; family and master bath floors at 0.009, so 0.9 cm higher than the
     living room, the opposite sign. Only the balcony step (BY -0.04) follows note 9.
   - Fix: mamad `floor(-3.80, -.25, .125, 2.745, mat.tile, .03)` plus a 3 cm threshold strip in the blast-door opening; for the
     baths a 1 cm step strip in each doorway (or lower the bath floors and cut the base tile).

9. **Room numbering and one wrong claim in APPLIED.md.** CONFIRMED, documentation.
   - d01 writes: master "חדר מס' 1", middle north room "חדר מס' 2", NW room "חדר מס' 3", mamad "חדר מס' 4 ממ"ד".
   - Model labels (line 2518, views 2546-2548): NW room "חדר 1", mamad "חדר 3 · ממ״ד". The panel note (line 194) explains the mamad,
     but not that "חדר 1" is d01's room 3. `audit/recheck5/APPLIED.md` says "the mamad is room 3, written on d01"; d01 writes 4.
   - Fix: label the rooms with the d01 numbers, or add "(בתוכנית: חדר 3)" to the NW room label. Correct APPLIED.md.

10. **Vanity sizes still outside the studio spec.** CONFIRMED, already open in PROJECT_MEMORY.
    - d07 p28-30: family bath 60 or 80, master 100 or 120. Model: 100 in the family bath (spec max 80), 70 in the master (spec min
      100). The master wall between the shower glass (z -4.06) and the door (z -3.36) is only 70, so 100 does not fit there.
      CER_FIXTURES already states this. Ask the studio.

11. **Interior items that differ from d01 but were decided from newer sheets.** CONFIRMED, info only.
    - Corridor-to-living passage: d01 x 1.99..2.98 (99) in a 9.7 cm wall; model 1.80..3.00 (120) and a 14.5/19 cm TV wall
      (construction plan). d06 note 24 says the spec/contract wins in a conflict; d01 is annex B of the contract. Worth one line
      to the developer.
    - Family bath riser: d01 draws the riser symbol in the SW corner (x 2.02, z -1.40); model box in the NW (plumbing sheet).
    - Master bath door: d01 leaf 65 (arc), opening z -4.03..-3.37; model opening -4.06..-3.36, leaf 0.69. d08 also says 65.
      Fix if wanted: `doorLeaf(6.945, -3.365, -1, 0, .65, ...)` and the north jamb at -4.02.

12. **Roof (d04) not modelled.** SUSPECTED relevance, low.
    - d04 shows a hipped tiled roof with solar collectors over the north end of building A and technical rooftop housings. The
      model has no storeys above our flat (dollhouse cut) and flat concrete caps elsewhere. Only bird views show it.

## Checked and fine

- `python3 roomdims.py`: +0 on every room (closet 485/175 is the known probe artifact). `python3 clearance_audit.py`: 0 issues.
- Overlay of all W() walls and facade piers on d01 (`source/out/qa6_verify_drawings/ov_*.png`): every room face within the
  sheet's own drawing tolerance (the sheet draws small rooms 1-3% larger than written). Written dimensions all equal the model:
  274x361, 282x356, 245x238, 222x172, 190x175, 430x296, 110, 355x262, 728x879, 277, 365, 275x884.
- Openings on d01 (concrete gaps) contain the model's net openings: room 1 window -2.87..-1.82 (model -2.81..-1.91), mamad
  0.48..1.47 (model 0.48..1.48), room 2 0.29..1.34, laundry 2.13..3.66, master bath 5.90..6.65, master -2.24..-1.19, living A
  0.71..3.55, B 4.19..7.03, C 7.62..8.47 (model per construction plan: 2.70, 2.70, 0.70 wide inside these).
- Door hinges and swings match d01: room 1 and room 2 hinge east, family bath hinge east, master hinge south swinging into the
  room, mamad hinge west opening into the corridor, entrance hinge west opening inward, master bath hinge south opening into the
  bath. Mamad opening d01 -1.94..-1.21 vs model -1.98..-1.19. Closet opening within 4 cm.
- Fixtures vs d01: family bath WC and basin on the west wall, tub on the east, washer in the NE niche; master bath shower NW
  104x93 (model 106x92), WC north centre x 6.24 (model 6.25), basin west; water heater (3.99, -4.72) r 0.30 vs model (4.04,
  -4.69) r 0.27; condenser in the niche; mamad sleeves at x -1.63, -1.03 and relief -0.44 vs model -1.55, -0.95, -0.52; mamad
  filter on the west wall z 2.20..2.61 vs model 2.09..2.59; panel symbol x 3.35..3.72 vs model 3.33..3.78. Kitchen furniture on
  d01 is "suggested location only" (legend, d06 notes 7 and 11), so the owners' kitchen is not a conflict.
- Exterior within 0.3 m in the calibrated frame: lot N and E, entrance gaps (9.95..14.85, 28.28..30.39), garden-apartment east
  face and its openings (-2.25..-1.20, 1.58..3.13, 4.68..6.23, 7.96..8.71 vs model within 0.1), its north windows, private north
  garden x -1.08..9.00, fences x -1.17 and 9.10, pergola x 4.04..9.00 z -8.76..-5.29, smoke vents, east low wall 12.56..12.75,
  south low wall z 9.80..9.94, fire pads (-14.08..-8.03 x 7.50..19.53; -21.20..-15.15 x 32.6..44.6), stalls 5-6 and the
  accessible stalls (z 15.50, 18.18, 20.57, 23.06, 25.52, 27.93 vs model within 0.28), stair under the mamad (x -6.64..-5.35,
  z 1.10..4.16), Ali Mohar sidewalk 14.18..16.68 and paver parking 16.68..18.69 (model 14.3/16.9/18.8), B footprint west -9.66,
  south 42.6, east 8.27.
- Studio spec d07 vs CER (194 items): every name, size, catalog page (3, 4, 5, 6, 8, 9, 11-17) and finish matches the 05/10/2026
  edition, including page 5 (six glossy 80x80: לורה בג', רוסו אפור, רוקי אפור, קררה, מרפיל בז', ארמאני אפור בהיר) and the
  two "מונה בז'" tiles that exist only as image text on page 15. Spaces: 80x80 (incl. glossy) and 60x60 only on dry floors,
  15x60 and 30x30/33x33 on bath floors and the balcony, 25x75 only on bath walls (p11-12 say wet rooms only), 30x60 and 20x60
  on bath walls and the kitchen, 10x30 and 20x20 only in the kitchen. The 15x60 balcony limit (20 sqm) note is right; the balcony
  is 24.3 sqm (APPLIED.md says "about 23"). Page 5 swatch medians match the model colours within a few levels.
- d06 notes 1, 2, 6, 7, 9, 11: the panel already says room sizes are before plaster, the MEP items are indicative, and the
  balcony sits 4 cm lower.
