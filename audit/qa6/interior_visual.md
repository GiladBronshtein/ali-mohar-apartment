# QA6: interior, visual

Scope: the inside of the apartment as a visitor sees it, after re-check 5 (ceiling 2.70 and the interior items of commit
5167387, the glossy 80x80 page of d7c72b9). Built site at http://localhost:8000/ (index.html built from salon.html at
e94546d). Line numbers refer to `source/salon.html` at e94546d.

What was captured (all runs: no page errors, no console errors):
- 29 interior presets, day and eve, desktop 1440x900 (every key in `views` except bird1, bird2, top, view).
- 15 presets on a phone (375x812, Android UA, touch, DPR 2), day and eve.
- About 60 custom cameras at eye height: every room looking up at the ceiling and its edges, close-ups of every re-check 5
  item, door thresholds, doors closed (`setDoors(true)`), curtains closed (`setCurtains(true)`), and the glossy floor
  (`cerSet('floor', 'f80g|רוסו אפור|g')`, `cerSet('rooms', 'f80g|קררה|g')`).
- Scripts and raw shots: `source/out/qa6_interior_visual/` (cams.mjs, b1..b6 spec files and folders), presets in
  `source/out/qa/qa6_iv/`. Defect crops: `audit/qa6/interior_visual_img/`.

## Findings

1. **Both new sunk basins show the cabinet top, not a bowl.** CONFIRMED.
   Where: master bath vanity (custom cam pos [5.55,1.45,-3.65] tgt [4.9,.78,-3.7], also visible in presets `shower` and
   `closet`): the "bowl" is walnut wood 3 cm down. Family bath (pos [2.95,1.5,-2.1] tgt [2.25,.82,-2.1], preset `bath`):
   a flat cream tray 3 cm deep, no drain. Images `01_master_basin_walnut.jpg`, `01_family_basin_flat.jpg`.
   Cause: `ceramicTop()` (lines 1448-1453) leaves a hole in the top and draws the bowl from `y1 - .13` up, but the
   cabinet boxes under it run up to the top's underside and fill the bowl volume: line 1460
   `B(4.44, 4.92, -4.07, -3.39, .45, .80, mat.walnut, ...)` and line 1547 `B(2.01, 2.44, -2.695, -1.675, .10, .82, paint)`.
   Their top faces at .80 and .82 cover the bowl floor (.67 and .69) and the drain.
   Fix: stop each cabinet below the bowl and rebuild the rim around it.
   ```js
   // master (inside the withShift block), bowl hx 4.56..4.86, hz -3.96..-3.56, bowl floor .67
   B(4.44, 4.92, -4.07, -3.39, .45, .66, mat.walnut, { round: .006 });
   B(4.44, 4.92, -4.07, -3.96, .66, .80, mat.walnut); B(4.44, 4.92, -3.56, -3.39, .66, .80, mat.walnut);
   B(4.44, 4.56, -3.96, -3.56, .66, .80, mat.walnut); B(4.86, 4.92, -3.96, -3.56, .66, .80, mat.walnut);
   // family bath, bowl hx 2.12..2.40, hz -2.315..-1.915, bowl floor .69
   B(2.01, 2.44, -2.695, -1.675, .10, .68, paint);
   B(2.01, 2.44, -2.695, -2.315, .68, .82, paint); B(2.01, 2.44, -1.915, -1.675, .68, .82, paint);
   B(2.01, 2.12, -2.315, -1.915, .68, .82, paint); B(2.40, 2.44, -2.315, -1.915, .68, .82, paint);
   ```
   Also update the stale comment at lines 1542-1543 ("quartz top with a semi-recessed basin").

2. **Closet: an LED bar runs across the wardrobe doors 25 cm under the ceiling.** CONFIRMED.
   Where: closet, pos [7.95,1.6,-3.4] tgt [7.6,2.5,-4.9]; also preset `master2` eve (glowing line top right).
   Image `02_closet_led_across_doors.jpg`.
   Cause: line 1415 `B(7.02, 8.3, -4.395, -4.375, 2.42, 2.45, mat.led, ...)` is from the first commit, when the wardrobes
   were shorter. The wardrobes are now `h: H` (lines 1411-1412, 2.70), so the strip sits 2 cm proud of the door faces and
   crosses the door gaps. Built for the old ceiling.
   Fix: delete line 1415, or move it into the ceiling as a cove over the doors:
   `B(7.02, 8.3, -4.375, -4.345, H - .006, H, mat.led, { parent: ceilGroup, cast: false });`

3. **Laundry niche: both refrigerant pairs stop in mid-air at 2.35, 35 cm under the niche ceiling.** CONFIRMED.
   Where: pos [4.05,1.95,-4.15] tgt [2.7,2.45,-4.9]. Image `03_niche_pipes_end_midair.jpg` (left pipe, cut end).
   Cause: line 1575 `C(2.27, -4.30, .98, 2.35, ...)`, `C(2.20, -4.30, .98, 2.35, ...)` and line 1579
   `C(3.37, -4.30, 1.65, 2.35, ...)`, `C(3.30, -4.30, 1.65, 2.35, ...)`. The 2.35 is a fixed number, not tied to `H`.
   Fix: run them to the slab, where they enter the ceiling void toward the AC unit: replace `2.35` with `H` in all four
   calls (and optionally add an elbow into the bath wall at z -3.99 if the route is meant to go through the wall).

4. **Second condenser: its brackets have nothing to hold on to, and the unit is half beside the main one.** CONFIRMED
   (support), SUSPECTED (position).
   Where: pos [4.25,1.35,-4.15] tgt [3.1,1.15,-5.05]. Image `04_condenser_floating_bracket.jpg`.
   Cause: lines 1576-1577. With the `withShift(.22, -.45)` the upper unit is x 2.83..3.68, the main unit x 2.30..3.30. The
   upper unit overhangs the main one by 38 cm to the east. The "wall brackets" are two 4 x 5 cm blocks at y 1.00..1.05:
   the west one sits on the main unit's lid, the east one (x 3.55..3.59) floats in air. Their back end is at z -5.07; the
   niche back there is the open louvre screen at z -5.26..-5.30, so there is no wall. APPLIED.md and the AC sheet say "over
   the main unit".
   Fix: centre it over the main unit and stand it on a frame (local coordinates, inside the withShift block):
   ```js
   B(2.16, 3.00, -4.55, -4.15, 1.05, 1.65, M('#e9e8e4', .6), { round: .01 });                 // 84 x 40, centred on the main unit
   [[2.04, -4.64], [3.12, -4.64], [2.04, -4.11], [3.12, -4.11]].forEach(([x, z]) => B(x - .02, x + .02, z - .02, z + .02, 0, 1.05, mat.steel));   // floor stand
   B(2.02, 3.14, -4.66, -4.62, 1.01, 1.05, mat.steel); B(2.02, 3.14, -4.13, -4.09, 1.01, 1.05, mat.steel);   // rails
   ```
   and move its fan disc (line 1578, x 2.98) to x 2.58 and its pipe pair (line 1579) to x 2.86 / 2.93.

5. **Evening: a dark band on the floor in every door reveal, and over the master vestibule.** CONFIRMED.
   Where: eve only. Room 2 door pos [1.35,1.5,-0.55] tgt [1.35,0,-1.9]; room 1, family bath, mamad doors the same; master
   door pos [3.55,1.5,-.75] tgt [4.7,0,-.75] (band covers the vestibule planks x 4.26..4.56).
   Images `05_eve_dark_threshold_room2.jpg`, `05_eve_dark_threshold_master.jpg`.
   Cause: the room gate (lines 2409-2421) lights each room only inside its own box (+5 cm). The 15-30 cm of floor inside
   each wall reveal belongs to no box, so it gets no lamp light. The corridor box `corr = [-2.17, -1.29, 4.20, -.09]`
   stops short of all the reveals, and the master box starts at x 4.56.
   Fix: widen only the corridor lamp's box over the reveals and the vestibule (back-facing walls get no light from it, so
   nothing leaks through walls; at most a 5 cm floor strip inside the adjacent rooms):
   `corr = [-2.17, -1.46, 4.62, .14]` (line 2413).

6. **The `service` preset (re-check 5) shows nothing legible, on desktop and phone.** CONFIRMED.
   Where: preset `service`, line 2545 `pos: [3.45, 2.15, -4.02], tgt: [2.55, .75, -5.0], fov: 84`. The camera stands in the
   niche 3 cm past the bath wall, 50 cm above the new condenser, so the frame is two white boxes at odd angles and the
   window frame. Image `07_service_view.jpg`.
   Fix: look into the niche from the family bath, through its window, the way the owners will see it:
   `service: { g: 'B', name: 'מסתור כביסה', pos: [2.98, 1.65, -2.85], tgt: [2.9, 1.0, -5.0], fov: 70 },`
   Result: `07_service_alt_camera.jpg` (condensers, heater, louvres and lines all readable).

7. **Family bath ceiling hatch: the frame is offset from the panel, so it reads as two outlines.** CONFIRMED.
   Where: presets `bath`, `bath2` (eve shows it best). Image `06_hatch_frame_offset.jpg`.
   Cause: line 1508 panel x 2.83..3.43, z -2.875..-2.275; line 1509 frame x 2.80..3.40, z -2.90..-2.30. The frame is
   3 cm west and 2.5 cm north of the panel.
   Fix (line 1509): `[[2.826, 2.83, -2.879, -2.271], [3.43, 3.434, -2.879, -2.271], [2.826, 3.434, -2.879, -2.875], [2.826, 3.434, -2.275, -2.271]]`.

8. **The closet has no evening light.** CONFIRMED (eve presets `closet`, doors-closed `closet`: the room is much darker
   than the master next to it; only the LED bar of finding 2 glows).
   Cause: no entry in `warm` (line 2406) is in the closet, and no room box covers it (closet x 7.01..8.92,
   z -5.01..-3.23; the master box ends at z -3.15). The closet ceiling spot at (7.63, -3.80) (line 1029) is drawn but
   gives no light.
   Fix: add `[7.63, -4.1, 1.5]` to the `warm` list after the kids' bath entry, and the box
   `closet = [6.96, -5.06, 8.97, -3.18]` at the same index in `pts` (line 2414).

9. **"Curtains closed" does nothing in rooms 1 and 2.** CONFIRMED.
   Where: presets `room1`, `room2` with `setCurtains(true)`: the linen stacks stay open. Image
   `09_room2_curtains_closed_button.jpg`.
   Cause: lines 1608 and 1616 use plain `curtain()`, not `curtainPair()` with a closed variant, so they are in neither
   `curtOpen` nor `curtClosed`. The living sheers, the master voile and the kitchen zebra do respond.
   Fix: give each room a closed pair like the master (lines 1403-1405): for room 1, open stacks into `curtOpen`, plus
   `curtainPair(curtClosed, 'z', -2.93, -2.34, -3.82, .02, H - .03, mat.linenGrey, 6, .035)` and
   `curtainPair(curtClosed, 'z', -2.38, -1.79, -3.80, .02, H - .03, mat.linenGrey, 6, .035)`; room 2 the same along x at
   z -4.72. Low priority.

10. **Kitchen window C: the new sill top is coplanar with the wall below the window.** SUSPECTED (z-fight by geometry;
    not visible in still TAA frames, may shimmer while moving).
    Cause: line 1057 sill `B(FX - .02, FX + .03, 7.72, 8.48, 1.17, 1.20, ...)` and line 902 facade segment
    `[7.75, 8.45, 0, 1.20]` (x FX..FO). Both top faces are at y 1.20 over x 7.28..7.31.
    Fix: `B(FX - .02, FX + .03, 7.72, 8.48, 1.175, 1.205, mat.sill, { cast: false });`

## Checked and fine

- Ceiling 2.70 in every room, looked at from eye height: wardrobes in rooms 1, 2, mamad and closet reach the ceiling
  (`h: H`); kitchen tall wall and wall cabinets run to the ceiling; storage wall stops at the bulkhead line with its soffit
  above; TV wall bridge to `DROP`; living bulkhead, its grilles and the wall washer; living curtain track and pocket,
  master voile track, room 1 and 2 rods at the ceiling; fans hang from the ceiling (blades 2.45), balcony fan and soffit
  lights at the soffit; bedside globes, frames pendant and wave pendant cables reach their canopies (frames bottom about
  1.85, 93 cm over the island); master split 18 cm under the ceiling; corridor drop 2.35 with return grille and
  cylinders; family bath lowered ceiling 2.20 with the WC column and laundry cabinet to it; mamad sleeves and relief
  valve. No gap or floating item from the raise other than findings 2 and 3.
- Mamad: porcelain like the corridor, grout continuous through the blast door, no threshold strip by day; skirting in
  porcelain.
- Skirting 7 cm in the floor material: planks in rooms 1, 2, master, closet and vestibule; porcelain in living, kitchen,
  entry, corridor and mamad. It follows the picker (white tile skirting with the glossy floor on `rooms`).
- Kitchen window C: no shutter rails or box, sill at 1.20 above the counter, zebra blind open and closed.
- Master shower room window: one sash.
- Washer niche walls painted; the tiles end at the stub wall and the window jamb.
- Family bath: no rain head over the tub, rail and hand shower kept.
- White flush plates on both WC ledges.
- Deck mixers: master top 1.04 vs mirror cabinet 1.144 (10 cm), family 1.06 vs 1.144 (8 cm). No clash.
- Balcony socket + TV point on the pier next to the IP44 box, island socket on the drawer block side, all visible.
- Glossy 80x80 (f80g) on both floor spaces, day and eve: no clipping (floor median 201/255 by day vs 150 for the default),
  veins and joints visible in eve, light and calm by day. It reads matte (no reflection in the live view, as documented).
- Doors closed: leaves seat in their frames, no light gaps; mamad blast door closes.
- Phone subset: framing and lighting fine in all 15 presets except `service` (finding 6).
- No black or missing textures, no z-fighting seen in any capture, no flicker between the day and eve runs.
