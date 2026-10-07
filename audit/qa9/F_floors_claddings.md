# QA9 F: floors, claddings, skirting, thresholds

Report only; no tracked file was changed. Checked against HEAD `5bea43a` (QA9 stage 4) and then `40e8d72` (niches). Three commits landed while this review ran, so
every finding below was re-scanned on the newer build. Two items were already fixed there and are not listed: the stone
return at the hob landing (line 1548), and the sage accent running to the glass on the north wall (line 1627). Line numbers
are for `source/salon.html` at `40e8d72`; the line count is the same as `5bea43a`.

## Method

- **Ray scan.** `F_scan/f_page2.js` and `F_scan/fscan.mjs` use the three-mesh-bvh pack from recheck4: 305k opaque triangles,
  doors closed and open. The scan covered:
  - downward rays every 5 mm in a 0.1-30 mm band along every room edge, plus a 5 cm grid inside the rooms (20 rooms,
    balcony included);
  - horizontal rays at y .02, .045 and .065 above each floor from a 30 cm band along every wall, to find bare wall bases;
  - 43k perpendicular rays on every bath wall, dense near the corners, the floor and the ceiling;
  - upward rays 2 mm, 1 cm and 3 cm from every wall;
  - an 89k-ray grid on the kitchen splash.
- **Skirting emulation.** The wall and skirting blocks of `salon.html` were run in Node with stub `B()`/`W()` calls, to list
  every skirting box and to test the fixes.
- **Grout layout.** `F_scan/grid.js` measures the piece left at each room edge for the default finishes and every spec size,
  and searches for better origins.
- **Shots.** 63 shots in `F_img/`: day and eve, low-angle edges, corners and thresholds. `F_scan/s3.json` adds spec picks
  through `F_scan/shots2.mjs`, which is `out/shots.mjs` plus a `"cer"` key.

`roomdims.py` probes at YH 2.4 and `clearance_audit.py` uses its own rectangles, so none of the fixes below touch either
check. No wall moves.

## Ranked findings

### Fix now (safe)

**F1. HIGH: the entry wall has no skirting over its whole 2.70 m.**
- **Where:** x 1.45, z 2.775..5.50. This is the wall with the commode and the round mirror, in the preset view "כניסה
  וקומודה".
- **Evidence:** `F_img/e6_hall_view_day.jpg`, `01_entry_westwall_base.jpg`, `e1_entry_westwall_eve.jpg`. The scan found bare
  wall at y .02 and .045 from z 2.805 to 5.465.
- **Root cause (line 1154):** `for (let t = a; t <= b + 1e-6; t += .01)`. When an edge is not a whole number of cm long
  (this one is 2.725 m), the last sample stops at 5.495, short of b. A run that is still open at the end of the edge is then
  dropped without a box. This is the only edge it hits today (emulated).
- **Fix:** line 1154 becomes `for (let t = a; t < b + .01 - 1e-6; t += .01) {`. Emulation shows it adds exactly one box,
  `B(1.45, 1.462, 2.785, 5.50)`, and changes nothing else.
- **Also needed, a corner filler:** hasWall is strict, so the new run starts at z 2.785 while the living run ends at x 1.45.
  That leaves a 1.2 x 2.2 cm notch on the outside corner at (1.45, 2.775). Add
  `B(1.45, 1.462, 2.763, 2.785, 0, SK, mat.tile, { cast: false });` after line 1168.

**F2. HIGH: the corridor's TV-wall stretch and both passage returns have no skirting.**
- **Where:**
  - corridor face z -0.19, x 3.00..4.15 (1.15 m, under the electrical panel);
  - the passage returns: the end face x 3.00 (z -0.19..0) and x 1.80 (z -0.145..0);
  - a 1 cm notch at the living-side corner (3.00, 0), because the living run starts at x 3.01.
- **Evidence:** `F_img/02_corridor_tvwall_base.jpg`, `04_passage_returns.jpg`. The scan found bare wall at z -0.190 for
  x 3.01..4.11, and on both return faces.
- **Root cause:** the corridor rectangle (line 1164) ends at z -0.145. Its skirting is therefore laid at z -0.157..-0.145,
  inside the 19 cm wall `W(3.00, 4.15, -0.19, 0)` (line 1087). The passage is in no skirting rectangle at all.
- **Fix (after line 1168; butt joints, no mitres, d08):**
  ```js
  B(2.988, 4.15, -.202, -.19, 0, SK, mat.tile, { cast: false });   // corridor face of the 19 cm TV-wall stretch
  B(2.988, 3.01, -.19, .012, 0, SK, mat.tile, { cast: false });    // passage east return, closes the living corner
  B(1.80, 1.812, -.157, .012, 0, SK, mat.tile, { cast: false });   // passage west return
  ```

**F3. HIGH/MED: the TV-wall step beside the master door has no skirting.**
- **Where:** the step is `W(4.26, 4.76, -0.24, -0.145)` (line 1100). Its face at z -0.24 (x 4.26..4.76) and its end face at
  x 4.76 (z -0.24..-0.145) are bare.
- **Evidence:** `F_img/03_master_step_base.jpg`, `e4_master_step_eve.jpg`.
- **Root cause:** the master and vestibule skirting is laid at z -0.157..-0.145, buried inside the step.
- **Fix (after line 1168):**
  ```js
  B(4.26, 4.772, -.252, -.24, 0, SK, mat.planks, { cast: false }); B(4.76, 4.772, -.24, -.145, 0, SK, mat.planks, { cast: false });
  ```
  The new run stays clear of the master-door casing, which ends at about z -0.29.

**F4. MED: the room 1 floor stops 2.5 cm short of the corridor wall.**
- **What shows:** the base porcelain at y 0 shows 9 mm below the planks. It is a 1.3 cm strip in front of the skirting at
  x -2.32..-2.14 (between the wardrobe niche and the door casing), and 2.5 cm wide at x -3.89..-3.81 and -1.23..-1.16.
- **Evidence:** `F_img/09_room1_door_strip.jpg`; floor scan, 316 samples at z -1.4475..-1.426.
- **Fix:** line 1048 becomes `floor(-3.90, -1.14, -5.035, -1.425, mat.planks);`. The wall face is -1.425 (line 1089). Room 2
  is correct: its wall face is -1.45.

**F5. MED: mamad threshold.**
- **What shows:** the raised reveal floor at y .02 starts at z -0.13. That is 1.5 cm short of the corridor face at -0.145,
  so a strip of base tile shows there (832 samples). The 2 cm step also has no riser, so it reads as a paper-thin edge.
- **Evidence:** `F_img/08_mamad_threshold_corr.jpg`, `08b_mamad_threshold_low.jpg`.
- **Fix:**
  - line 1053: the third call becomes `floor(-1.98, -1.19, -.145, .09, mat.tile, .02)`;
  - add a riser: `B(-1.98, -1.19, -.147, -.145, 0, .02, mat.blastDoor, { cast: false });`. This is the steel sill of the
    blast frame; its finish is an estimate (mat.tile works too).

**F6. MED: the default 120x120 grid leaves slivers along the corridor and the living facade.**
- **What shows:**
  - a 4.5 cm row along the whole corridor north wall (z -1.245..-1.20), in front of every bedroom and bath door;
  - an 8 cm row along the living facade and balcony doors (x 7.20..7.28).
- **Evidence:** `F_img/12_corridor_grout.jpg`, `e7_corr2_day.jpg`, `f6_threshold_corr.jpg`, `11_living_facade_grout.jpg`.
- **Root cause:** the cur `mat.tile` uses world UVs (`worldUV`, line 2603), with grout at x, z ≡ 0 (mod 1.2).
- **Fix:**
  - after the `T.tile` texture (lines 317-325), add `T.tile.offset.set(-.08 / 2.4, .045 / 2.4);`;
  - in `pbrDetail` (line 557), make the derived maps follow it: `t.offset.copy(m.map.offset); t.repeat.copy(m.map.repeat);`.
- **Result:**
  - grout lies on the corridor north wall line, and full tiles meet the balcony doors;
  - the 8 cm cut moves to x 0, under the storage wall (x 0..0.60, z 0..2.78), where it is hidden;
  - the kitchen west wall gets a 5 cm cut at x 3.63, behind the tall units;
  - every other visible edge piece is 20 cm or more: corridor west end 20, mamad west 28, entry wall 103, TV wall 115.5;
  - the skirting loses the dark grout line at its foot.
- Spec picks are unaffected; they use their own `sp.o`.

**F7. MED: hard light line across the open closet opening (day).**
- **Where:** z -3.15, x 7.54..8.32. The floor is lit on the bedroom side and dull on the closet side, on a straight line.
- **Evidence:** `F_img/c1_closet_threshold.jpg`.
- **Root cause:** the room gate box for the master window light, `master = [4.56, -3.15, 8.96, -.09]` (line 2727), ends
  inside the doorless opening. The passage had the same problem and was fixed with `SPILL` (line 2734).
- **Fix:** give rect light 6 a second spill term, for example
  `( 1. - smoothstep( 0., .25, max( 7.54 - gateW.x, gateW.x - 8.32 ) ) ) * ( 1. - smoothstep( 0., 1.0, -3.15 - gateW.z ) )`
  inside the closet box. Then pick the term per light, e.g. `rectSpill[i]` 1 = passage, 2 = closet. The fade lengths would
  be judged by eye, as for the passage.

**F8. MED: no skirting under kitchen window C.**
- **Where:** the facade x 7.28, z 7.75..8.19, between the pier skirting and the base-cabinet side.
- **Evidence:** `F_img/06_kitchen_windowC_base.jpg`.
- **Root cause:** the sub-sill wall is a `B()`, not a `W()`, and is missing from the pier list on line 1139.
- **Fix:**
  - line 1139: add the range `[7.75, 8.45]`;
  - line 1140: change noSkirt `[4.17, 7.32, 8.12, 8.83]` to `[4.17, 7.32, 8.19, 8.83]`.
  - Emulated: the pier run becomes z 7.00..8.20 (ends at the cabinet front) and nothing else changes.

**F9. MED: the entry wall stub has a bare end face.**
- **Where:** the stub is `W(3.63, 4.33, 5.50, 5.61)` (line 1079). Its end face at x 4.33 (z 5.50..5.61) is bare; its skirting
  is buried at x 4.30..4.312.
- **Evidence:** `F_img/05_entry_stub.jpg`.
- **Fix:** `B(4.33, 4.342, 5.50, 5.61, 0, SK, mat.tile, { cast: false });`

**F10. LOW: the sage accent stops 2.5 cm short of the fixed glass on the shower's west wall.**
- **Where:** the sage ends at z -4.10; the glass is at -4.08..-4.07.
- **Fix:** line 1626 becomes `tileX(-4.98, -4.075, 4.63, 1, 0, H, mat.sage); tileX(-4.075, -3.26, 4.63, 1, 0, H, mat.bathWall);`.
  The north wall was already fixed (5.69).

**F11. LOW: the corridor skirting runs through the blast-door frame jambs.**
- **What shows:** the skirting face (z -0.157) stands 5 mm proud of the steel frame (-0.152, line 1213). It runs to x -1.97
  and resumes at -1.18, both inside the jamb footprints (x -2.03..-1.98 and -1.19..-1.14).
- **Fix:** `noSkirt.push([-2.035, -1.145, -.17, -.14]);`. The runs then end at -2.03 and resume at -1.14, butting the frame.

**F12. LOW: the visible skirting is lower than the spec's 7 cm.**
- **What shows:** the boxes start at y 0 under the raised floors, so 6.1 cm shows in the plank rooms and 5 cm in the mamad.
- **Fix:** give skirtRoom a `y0` argument (`B(..., y0, y0 + SK, ...)`): .009 for the plank rooms (line 1167) and .02 for the
  two mamad rectangles (line 1165).

### Needs owner decision

**D1. Resolved in `40e8d72`, landed during this review: both niches are now real recesses.** The shower niche is 9 cm into the
facade wall and the tub niche 7 cm into the partition. Re-shot in `F_img/n1_master_niche_recessed.jpg` and
`n2_tub_niche_recessed.jpg`: they read as recesses and the back grout follows the wall grid. The before shot is
`F_img/b2_niche.jpg`.

**D2. LOW/MED: spec-pick grout origins leave slivers.**

| Space | Current `sp.o` | Size | Edge pieces under 10 cm |
|---|---|---|---|
| floor (line 3411) | [2.555, 5.70] | 80 | passage west return 4.5, mamad west 4.5, TV wall 10 |
| floor | same | 60 | entry stub 5.5, kitchen south 9 (behind cabinets), mamad south 4.5 |
| rooms (line 3413) | [4.60, -3.11] | 80 | room 1 door wall 8.5, room 2 door wall 6 |
| rooms | same | 60 | room 1 west 9, room 2 north 10, closet north 8.5 |
| bathF | | w1560 | east 4.4 |
| bathF | | w30 | south 6.4 |
| ensF | | w30 | south 6.4 |

Suggested origins (searched for 80 and 60 together; `grid.js` prints every edge):

| Space | Suggested `o` | Result |
|---|---|---|
| floor | [1.015, 0.51] | smallest piece 13.5 cm; corridor centred 15.5/14.5 for 80 |
| rooms | [1.25, 1.925] | smallest piece 22.5 cm |
| bathF | [2.245, -3.575] | |
| ensF | [4.75, -4.78] | |

- Also still open (PROJECT_MEMORY): `cerApply` uses `o[0]` as the u origin on x-facing walls too. On the master bath west
  wall (shower) the 30x60 and 20x60 picks leave a 1 cm column at the z -4.98 corner. With 60-wide picks the family bath
  z-walls get a 5 cm column at x 4.41..4.46.
- A fix needs a per-material shift for x-facing faces in `worldUV`.

**D3. LOW: default bath wall tile (60x120, laid from the floor).**
- A 5 cm strip sits above the master shower window head (grout at 2.40, head 2.35; `F_img/b5_window_reveal.jpg`).
- The top row is 30 cm.
- Starting the rows from the window head instead is a design choice.

**D4. LOW: shower floor.** The default floor is 60x120 with a central point drain and no slope cuts (`F_img/b7_shower_floor_corner.jpg`).
That is not buildable as drawn. Options: envelope cuts in the texture, or a linear channel (one was added at the glass in
stage 1-3).

**D5. LOW: per spec, but worth a look.**
- **Under window C:** plaster over the counter at z 8.16..8.45, y .92..1.20 (`k1_window_landing.jpg`). d10 item 1 says the
  stone stops at the window area, so this follows the spec.
- **Family bath washer niche:** painted (d08). The tile skin ends there with a raw 6 mm edge (`f3_washer_niche.jpg`). An
  edge profile is a detail choice.
- **Balcony:** no skirting on the deck. A wood deck normally has none; with a 33x33 spec pick, d08 wants one in the floor
  material.

## Passed

- **Floors:** no holes and no wrong material at floor level in any room, apart from F4 and F5. Rugs and bath mats only. Doors
  open and closed.
- **Thresholds:** the change of floor sits under the closed leaf for rooms 1 and 2, the family bath, the master and the
  master bath. Planks and terrazzo run into the doorways as intended.
- **Bath claddings:** 43k samples on all eight bath walls (corners, 1 mm above the floor, 3 mm under the ceiling) found no
  plaster. The tile reaches the floor plane and the ceiling, 2.70 in the master and 2.20 in the family bath. Window reveals
  are tiled in both baths.
- **Ceiling edges:** no gaps along any wall; only fittings near the edges (curtain track, grilles, sleeves).
- **Kitchen splash:** continuous on the south and west walls, from the worktop (.92) to the cabinet line (1.62), into the
  south-west corner. The new return at the landing is in.
- **TV-wall slab:** edges, LED reveal and the base meet cleanly (`t1`, `t2`, `t3`).
- **Balcony deck:** meets the facade, the side walls and the south corner cleanly (`d2`, `d3`).
- **Default grids in the baths:**
  - the default master bath floor (60x120 world grid) leaves no piece under 16 cm;
  - wall rows meet at the corners (`b7`).

## Scripts

- `F_scan/fscan.mjs` and `F_scan/f_page2.js`: the ray scans. Run them through `/tmp/gpu.sh`; set `DOORS=1` to close the doors.
- `F_scan/probe.mjs`: single rays.
- `F_scan/grid.js`: the grout layout.
- `F_scan/shots2.mjs` and `F_scan/s1-s4.json`: the shots.
