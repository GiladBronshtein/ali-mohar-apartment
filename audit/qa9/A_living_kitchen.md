# QA9 A: living room, kitchen, entry, storage wall, TV wall, sun balcony

Report only; nothing in `source/` was edited. Model: `source/salon.html` at `6241532` (3486 lines). Line numbers below are from
that file.

How it was checked: 32 named-view shots (17 views, day and eve), 40 close-ups (eye level, low angles, eve and closed curtains),
and two A/B runs that change one thing at runtime so a root cause can be confirmed, not guessed. Evidence images are in
`audit/qa9/A_img/`; the raw shots are in `/tmp/qa9_A1` .. `/tmp/qa9_A4`. Plans and spec used: the Regba kitchen sheet
(`audit/recheck3/kitchen.md`), the electrical re-read (`audit/recheck3/electrical.md`), d08 table 5, d10 items 1, 4, 6-10.

Checks as of this report: `roomdims.py` +0 for every room (closet 485/175 is the known probe artifact), `clearance_audit.py`
0 issues. None of the fixes below moves a wall. Only F6 and F8 add geometry, both on wall faces; neither touches a
`clearance_audit` rectangle.

A/B tool (scratch, gitignored): `source/out/qa9A_shots_js.mjs` is `out/shots.mjs` plus an optional `"js"` field per shot,
evaluated in the page before the capture.

## Ranked findings

| # | Sev | Finding | Where | Group |
|---|---|---|---|---|
| F1 | high | Balcony sofa: the three back cushions on the long run are 70 cm tall and 42 cm wide (rotated 90 deg), so they read as three armchair backs | balcony, view, entry, photo, inside, bird1 | fix now |
| F2 | high | White finishes turn beige or taupe in shade (counter, cabinet sides, blind cassette, plates, the sofa's chrome legs read brown) because the warm living-room reflection probe also drives their diffuse light | kitchen, kitchen2, kitchen3, island, isle2, coffee bar | fix now |
| F3 | med | Eve: a bright 14 cm strip on the floor along the whole north wall of the living room (storage wall, passage, media base) | tvwall, hall, entry, storage (eve) | fix now |
| F4 | med | Balcony soffit is nearly black-brown by day; real white plaster over a sunlit deck reads light grey | balcony, balcony2, inside, view | fix now |
| F5 | med | Pier switches (light + shutters A/B) and the pier socket are hidden behind the open curtain stack | entry, tvwall, close-up | owner |
| F6 | med | Kitchen has no counter sockets except the Ninja plate (which is half hidden behind the grill); the Regba sheet's two service sockets were proposed in recheck 3 and never applied | kitchen3, kitchen2 | fix now |
| F7 | low-med | Eve: the under-cabinet LED strips glow but light nothing; the counter and splash stay dim | kitchen3, kitchen (eve) | fix now (tune by eye) |
| F8 | low-med | East return beside the hob landing has painted plaster from counter to cabinets: no splash on the 33 cm return | kitchen3, hob close-up | fix now |
| F9 | low | Integrated dishwasher has a protruding black bar handle in an otherwise handleless kitchen with a grip channel | kitchen3 | fix now |
| F10 | low | Large art on the alcove's north wall ends 2.5 cm from the passage corner | storage, passage close-up | fix now |
| F11 | low | Entry wall crowded: door switch 1.5 cm from the frame casing, intercom 2 cm from the first print | hall, entry door close-up | fix now |
| F12 | low | Switch plates by the doors are blank white squares (no rocker); the robot-garage socket is a blank plate too | hall, storage, commode close-up | fix now |
| F13 | low | Top view: "מטבח" sits on the 365 and 105 dimensions; "קיר אחסון" crowds 277 and 262 | top | fix now |
| F14 | low | Two recessed downlights 17-20 cm from the wave pendant's canopy | storage, pendant close-up | fix now |
| F15 | low | Eve hotspots: upper storage doors behind the wave pendant; halo on the ceiling around the entry cylinders | storage, photo (eve) | fix now (tune) |
| F16 | low | Open sheer stacks show stair-stepped vertical edges | kitchen, entry | optional |
| F17 | low | Dead or stale code: alcove LED grazer buried inside the AC bulkhead; stale comments | code | fix now |
| F18 | low | Entrance door hardware: the lever reads as a small brown block, no peephole or cylinder rosette (d10 item 4: painted Garda door with nickel handle) | entry door close-up | optional |
| O1 | - | Balcony-side island seats leave about 0.4 m behind a seated diner to the wall in front of door B | island, isle2 | owner |
| O2 | - | Window C: the construction plan draws one sash; an inward sash would hit the inside-reveal zebra blind | kitchen3 | owner |
| O3 | - | Balcony railing: 2 cm pickets at 12 cm centres leave exactly a 10 cm gap; the 49 cm upstand (estimate) is a toe ledge | balcony | owner / estimate |

---

## Fix now (safe)

### F1 (high) Balcony sofa back cushions rotated

- What: on the long run against the railing, each back cushion is a box 15 deep, 42 wide (along z) and 69 tall. The seat
  cushions are 76 wide, so the three cushions read as separate high-backed armchairs. The short return is correct (69 wide,
  42 tall). The cushions show in the default `entry` view through door A and dominate `view`.
- Evidence: `A_img/01_balc_sofa_backs.jpg`, `01b_view_day_sofa_backs.jpg`, `01c_bird1_sofa_backs.jpg`.
- Root cause: line 1899, the z and y extents are swapped:
  `const p = B(-.075, .075, -.21, .21, (a - b) / 2 + .005, (b - a) / 2 - .005, OS, { round: .05 });`
- Fix (line 1899):
  ```js
  const p = B(-.075, .075, (a - b) / 2 + .005, (b - a) / 2 - .005, -.21, .21, OS, { round: .05 }); p.position.set(10.07, BY + .64, (a + b) / 2); p.rotation.z = -.12; });
  ```
  Result: 69 wide, 42 tall, centre at BY+.64 (bottom .39 = seat-cushion top), leaning toward the railing like the return's.
  Footprint unchanged. No clearance effect.

### F2 (high) Warm reflection probe tints white finishes

- What: in shade, the quartz counter under the wall cabinets, the white cabinet sides (the coffee niche, the tall unit
  returns), the zebra-blind cassette and the switch plates read beige, taupe or brown. The walls beside them stay neutral
  grey-white. The sofa's "chrome" legs (steel) read dark bronze.
- Evidence: `A_img/02_probe_tint_kitchen2_AB.jpg` and `02b_probe_tint_coffee_AB.jpg` (left: as shipped; right: the same
  frame with the probe removed from `quartz, whiteFront, whitePlate, tile, splash, graphite` at runtime). Sampled at the
  same pixel: counter (166,165,161) to (201,201,199); blind cassette (98,91,81) to (123,122,118). Also
  `02c_blind_cassette_brown.jpg`, `02d_counter_taupe.jpg`, `17_sofa_legs_not_chrome.jpg`.
- Root cause: line 2551, `PROBE_GLOSSY` includes matte-white and stone finishes. In three.js r160, `material.envMap` feeds
  the diffuse IBL as well as the specular, so the Cycles living-room probe (leather, wood deck, warm eve) at `PROBE_K` 2.0
  becomes their ambient colour. That is the effect the 2026-10-07 decision kept off the walls ("a room probe darkened and
  warmed whole rooms"), and it is still on the white fronts.
- Fix (line 2551): keep the probe on metals, glass and screens only:
  ```js
  const PROBE_GLOSSY = new Set([mat.blackMetal, mat.steel, mat.ceramic, mat.ceramicIn, mat.sinkSteel, mat.screen, mat.frame, FINM.chrome, FINM.brushed, FINM.gold].filter(Boolean));
  ```
  (removed: `mat.quartz, mat.graphite, mat.whiteFront, mat.tile, mat.splash, mat.whitePlate`). `ceramic` and `ceramicIn`
  stay because they are on bath probes through `PROBE_ZONE`; that is area B's call. Expected cost: the quartz island top
  loses the faint room reflection. The A/B shows it still reads as polished stone under `RoomEnvironment`.
- Sofa legs, line 1354: `mat.steel` to `FINM.chrome` (defined at line 666, before use). The comment and the owners'
  photo say chrome legs.

### F3 (med) Eve light strip along the living room's north wall

- What: in eve, a lit band about 14 cm deep runs along the floor at z 0..0.14 from the storage wall past the passage to the
  media base, with a hard edge.
- Evidence: `A_img/03_corridor_light_strip_AB.jpg` and `03b_tvwall_eve_strip_AB.jpg` (right: corridor lamp `warm[4]` set
  to 0 at runtime, and the strip is gone). Also `03c_hall_eve_strip.jpg`.
- Root cause: line 2697, the corridor room box `corr = [-2.17, -1.46, 4.62, .14]` reaches 14 cm into the living room
  (its south face is z -0.145; the "+5 cm" rule would give -0.095, and the passage mouth is z 0). The corridor lamp
  (line 2690, entry 5 `[1.0, -.7, 3.5]`) adds its light on top of the living lamps in that strip.
- Fix (line 2697): `corr = [-2.17, -1.46, 4.62, .0]`. The passage floor (z -0.145..0) stays lit by the corridor lamp. The
  living lamps already reach z -0.05. `SPILL` (line 2703) uses only `corr[0..2]`, so the day spill does not change.

### F4 (med) Balcony soffit near-black by day

- What: the underside of the slab over the balcony renders about #45403a (dark olive-brown), under a sunlit deck and a
  white railing upstand. It is the darkest surface in every balcony view.
- Evidence: `A_img/04_balcony_soffit_AB.jpg` (right: the soffit material swapped at runtime for a clone with emissive
  #e9e6df at .22), `04b_soffit_dark.jpg`.
- Root cause: line 1875, the soffit boxes use `mStuccoOut`. It faces down, so it gets only the exterior env's ground half;
  there is no real-time bounce from the sunlit deck.
- Fix: give the soffit its own material and a day-only fill:
  - after line 593: `const mSoffit = mStuccoOut.clone(); mSoffit.emissive.set('#e9e6df'); mSoffit.emissiveIntensity = .22;`
    (white stucco under a lit balcony; strength by eye, matches the A/B)
  - line 1875: both `mStuccoOut` to `mSoffit`
  - line 2564: add `inside.delete(mSoffit);` so it gets the exterior env like the walls
  - line 3007 (`setMode`): add `mSoffit.emissiveIntensity = eve ? 0 : .22;`
  - photo PBR: `mSoffit` is cloned before `photoReady` runs, so add it to the stucco call on line 599:
    `photoPBR([mat.stucco, mStuccoOut, mSoffit], 'white_stucco', 1.5, { normal: .5 })`.

### F6 (med) Kitchen sockets

- What: along 3.0 m of counter on the south run and 1.2 m on the west run, the only visible outlet is the Ninja plate at
  z 8.13. It sits 3 cm behind the grill's edge (half hidden), and it is a blank plate with no socket holes. The kettle on the
  south counter has nothing to plug into. d08 table 5 gives the kitchen 1 regular plus 3 separate-circuit sockets; the Regba
  sheet adds two service sockets at H 1.10 (south wall 200 from the west wall, west wall 1250 from the south wall).
  `audit/recheck3/kitchen.md` proposed both; they are not in the code.
- Evidence: `A_img/06_kitchen_no_counter_sockets.jpg`, `06b_ninja_socket_hidden.jpg`.
- Fix:
  - line 1516: `plate('e', 3.645, 8.13, 1.10, .08, .08);` to `outlets('e', 3.645, 8.22, 1.10, 'ss');` (double socket clear
    of the grill, z 8.14..8.30)
  - after line 1523 (the splash): `outlets('n', 8.775, 3.83, 1.10, 's'); outlets('n', 8.775, 4.50, 1.10, 'ss');` (the Regba
    south service socket in the corner, and a double left of the sink over the flat stone tray; plates on the splash face
    z 8.763..8.775, under the 1.62 cabinet line)
  - after line 1481: `outlets('e', 3.66, 7.54, 1.10, 's');` (the Regba west service socket on the back of the coffee niche,
    behind the machines that need it; the fluted back face is x 3.658)
  - `outlets()` is a hoisted function declaration (line 1972), so calling it from the kitchen block is fine.

### F7 (low-med) Eve: under-cabinet strips light nothing

- What: the `mat.led` strips under the wall cabinets (line 1521) glow at 2.0 emissive in eve, but no light comes from them.
  The counter and the stone splash stay dim and brown-grey. In a real kitchen at night, this is the brightest surface.
- Evidence: `A_img/07_eve_undercab_no_light.jpg`, `07b_eve_counter_dim.jpg`.
- Fix (tune by eye, check eve perf). Add two warm lights with the downward lobe, gated to the living box:
  - line 2689: append `1, 1` to `WARM_DOWN` (14 entries)
  - line 2690: append `[4.75, 8.56, .6, 1.56], [6.30, 8.56, .6, 1.56]` to the light list, after the closet entry
  - line 2698: insert `LIV, LIV` before the two trailing `master` entries:
    `pts = [LIV, LIV, LIV, LIV, corr, master, r1, r2, mamad, mbath, fbath, closet, LIV, LIV, master, master]`
  - the explicit y 1.56 bypasses the ceiling placement in line 2691. The light-skip patch drops them by day. If the splash
    shows a hotspot, lower k to .4 or move z to 8.50.

### F8 (low-med) No splash on the east return

- What: the counter runs into the facade wall at x 7.28. Between the window's south jamb (z 8.45) and the splash corner
  (z 8.775), the wall from .92 to 1.62 is painted plaster beside the hob landing. d10 item 1 asks for stone over the base
  cabinets "except the window area", so the return is included and only the window is excepted.
- Evidence: `A_img/08_east_return_no_splash.jpg` (grey plaster left of the cutting board).
- Fix: after line 1523 add `B(FX - .015, FX, 8.45, 8.775, .92, 1.62, mat.splash, { cast: false });`. Then trim the interior
  window sill's south ear so it butts the stone, line 1241: `7.72, 8.48` to `7.72, 8.45`. The panel sits in the 3 cm gap
  between the wall cabinet end (x 7.25) and the wall. It shares `mat.splash`, so the ceramics picker (`kitB`) swaps it too.

### F9 (low) Dishwasher handle

- What: a 50 cm black bar stands proud on the dishwasher front at h .55-.57. The rest of the run is handleless with a
  continuous grip channel at .815-.845 that already serves the dishwasher.
- Evidence: `A_img/09_dishwasher_handle.jpg`.
- Fix: delete line 1498.

### F10 (low) Art tight to the passage corner

- What: the 95 x 120 print on the alcove's north wall spans x .825..1.775. The passage corner is at x 1.80, so the frame
  ends 2.5 cm from the corner.
- Evidence: `A_img/10_art_tight_to_corner.jpg`.
- Fix (line 1415): centre it on the visible wall between the cabinet front (.60) and the corner (1.80):
  `art('s', 0, 1.20, 1.55, .95, 1.20, 102, ...)`, which leaves 12.5 cm each side.

### F11 (low) Entry wall crowding

- What: the door switch (line 1202, `['n', 5.50, 2.66]`, x 2.62..2.70) is 1.5 cm from the entrance frame casing (x 2.605).
  The intercom (line 1165, x 2.74..2.84) is 2 cm from the first print (x 2.86).
- Evidence: `A_img/11_entry_switch_intercom_art.jpg`.
- Fix: line 1202 `2.66` to `2.68` (2.64..2.72). Line 1165 intercom `2.74, 2.84` to `2.76, 2.86`. Lines 1167-1169: prints
  at 3.12 / 3.56 / 4.00 (4 cm gaps, x 2.92..4.20). The picture light (line 1170, x 2.92..4.16) still covers them;
  optionally make it `2.90, 4.22` with its LED `2.92, 4.20` and arms at `2.98, 4.14`.

### F12 (low) Blank plates

- What: `plate()` alone draws a plain white square, so every switch by a door (lines 1202-1203) and the robot-garage socket
  (line 1412) show no rocker or holes. In the garage, the plate also sits against the LED strip.
- Evidence: `A_img/12_blank_switch_plate.jpg`, `12b_robot_socket_blank.jpg`.
- Fix: lines 1202-1203, `.forEach(([f, w, c]) => plate(f, w, c, 1.1))` to `.forEach(([f, w, c]) => outlets(f, w, c, 1.1, 'k'))`
  (same plate plus a rocker mark). Line 1412, `plate('e', .02, TMD - .058, .44, .06, .05);` to
  `outlets('e', .02, TMD - .07, .40, 's');`.

### F13 (low) Top-view labels overlap

- Evidence: `A_img/13_top_label_overlap.jpg` ("מטבח" over 365 and 105; "קיר אחסון" crowding 277 and 262).
- Fix (line 2847): `zone(5.0, 7.3, 'מטבח')` to `zone(6.75, 7.35, 'מטבח')`; `zone(1.2, 1.5, 'קיר אחסון')` to
  `zone(1.2, 2.3, 'קיר אחסון')`. Check in `top` at desktop and phone width (CSS2D labels scale with the screen).

### F14 (low) Downlights hugging the wave pendant

- What: recessed spots at (1.0, 1.0) and (1.0, 2.0) sit 17-20 cm west of the pendant canopy (x 1.17..1.23, z 1.17..2.41).
  They read as clutter, and the alcove already has the pendant.
- Evidence: `A_img/14_spots_by_pendant.jpg`.
- Fix (line 1211): remove `[1.0, 1.0], [1.0, 2.0]` from the spot list. Nothing else refers to them; the eve warm light for
  the alcove is the pendant's (line 2690, first entry).

### F15 (low) Eve hotspots

- Storage doors: the pendant's warm light `[1.2, 1.79, 2.5, 1.95]` (line 2690) sits 0.6 m from the white upper doors and
  blooms on them. Try k 2.5 to 1.8 and `WARM_DOWN[0]` .5 to .8. Evidence: `A_img/15_storage_eve_hotspot.jpg`.
- Entry: the ceiling halo between the two cylinders comes from warm light 4 `[2.4, 4.4, 4]`. Line 2691 places it at H-.08
  (8 cm under the ceiling, between the cylinders at z 3.9 and 5.0), and its upward lobe floor (.08) still lights the
  ceiling 8 cm away. Fix: in line 2691, place downlights at `- .20` instead of `- .08` (the corridor one at DROP too),
  or zero the upward floor for the cylinders (`.08 +` to `.0 +` in the gate patch, line 2709, if the other downlights
  look right without it). Evidence: `A_img/16_entry_ceiling_halo_eve.jpg`.

### F17 (low) Dead and stale code

- Line 1414: the alcove "LED grazer" box (x .62..1.97, z .03..06, y H-.012..H) lies inside the AC bulkhead box (line 1340,
  x 0..7.06, z 0..0.80, y 2.35..2.70) and never renders. Delete it, or move it under the bulkhead at
  `y DROP - .006 .. DROP`.
- Line 1070 comment: "Openings as in the plan: A 0.78-3.45, B 4.26-6.88, window C 7.70-8.39". The code uses .79-3.49,
  4.29-6.99, 7.75-8.45 (recheck 3, written chain).
- Line 1375 comment: "floor lamp beside the sofa, plant by the column". Neither is built.
- Line 1334 comment: "75" TV". Line 1335 builds the 85" (188 x 106).

---

## Needs owner decision

### F5 (med) Pier switches behind the open curtain

- What: curtain 2's open stack (line 1253: z 3.48..4.25 at x 7.14, floor to ceiling) covers the whole pier between doors
  A and B. Behind it are the `krr` switch row (line 2031: the living light and the A and B shutters, h 1.10) and the pier
  socket (h .40). An architect will ask where the light switch is.
- Evidence: `A_img/05_pier_switches_behind_curtain.jpg` (the plates show faintly through the sheer).
- Options:
  1. Stack curtain 2 just south of the pier, over door B's north frame and fixed pane. Line 1252: give each curtain an
     open start, `[[.02, 3.54, .76, .02], [3.48, 7.62, .55, 4.00]].forEach(([a, b, st, o]) => {`. Line 1253:
     `curtainPair(curtOpen, 'z', o, o + st, ...)`, other arguments unchanged. The closed curtains (line 1254) stay as they
     are. When open, about 21 cm of door B's glass is covered and the switches are clear.
  2. Keep the stack, and accept switches behind a sheer (common in practice, but visible in the presentation).
  3. Move the switch row to the pier's return or the column face. That departs from the electrical sheet (z 3.65 / 3.87 /
     4.12).

### F18 (low, optional) Entrance door hardware

- d10 item 4: a painted Rav Bariach Garda door with a nickel handle. The model's lever (line 1164) is 4 x 4 cm boxes that
  read brown in shade (F2 does not affect `mat.steel`). Optional: a 13 cm lever in `FINM.brushed`, a cylinder rosette
  20 cm below it, and a peephole at 1.50. The door panel design is not written anywhere; keep it plain.

### F16 (low, optional) Sheer stack edges

- The open sheers (`depthWrite: false`, 62% opacity, many overlapping folds) show stair-stepped vertical edges in
  `A_img/18_sheer_stairstep.jpg`. Optional: `alphaToCoverage: true` on `sheer` (line 1244) with `transparent: false`, or
  fewer folds on the open stacks (line 1253, `Math.round((b - a) / .3) / st` to about 60% of that). Test for flicker
  (QA7 notes) before shipping.

### O1 Island seating on the balcony side

- The island is 96 cm from the wall face in front of door B (z 4.29..6.99), and `clearance_audit` passes it (min .91).
  With stools at x 6.44 (seat edge 6.63), a seated diner leaves about 0.4 m to the wall, so nobody passes behind them, and
  door B's fixed half is the only way past. NKBA asks for 1.12 m behind seated diners where people walk.
  Owner's layout; mention it if the architect asks. A 2-seat island (fridge side only) would free the facade strip.
  Evidence: `A_img/19_island_balcony_side.jpg`.

### O2 Window C operation

- d08 lists no kitchen window. The construction plan draws one sash; the model builds a single fixed-looking slider pane
  with a pull (line 1240), with the zebra blind inside the reveal at FX+.07 (line 1272). If the sash opens inward
  (tilt-turn), it would hit the blind and sweep over the counter landing. Ask which type is ordered. If it is a tilt-turn,
  mount the blind on the sash ("perfect fit"), or use a slider.

### O3 Balcony railing (estimate)

- Line 1879: 2 cm pickets at 12 cm centres leave a 10 cm clear gap, exactly the usual limit (a 10 cm sphere must not pass).
  11.5 cm centres would give margin. The upstand (line 1877, top .45, 49 cm above the deck, an estimate from photos)
  leaves a 5 cm ledge in front of the pickets. Railing height is 1.13 m from the deck to the rail top. If the real upstand
  is that high, the railing height may need to count from the ledge. Ask the developer; the model shows an estimate.

---

## Verified, no action

- d10 item 10: the island socket (line 1537, drawer-block side, h .70) and the balcony socket plus TV point (line 2035) are
  present and visible (`A_img/22_island_socket_ok.jpg`, `21_balc_socket_tv_ok.jpg`). The 3-phase hob point is under the
  hob, hidden as expected.
- d10 items 8 and 9: the gas point (h .30) and garden tap (h .60) on the balcony's south wall are visible beside the big pot
  (`A_img/20_balc_gas_tap_pot.jpg`; the pot stands 16 cm in front of the valve and does not cover it).
- Window C has no shutter (d08, electrical sheet). The kitchen window blind fits inside the reveal; the wall cabinet stops
  at the jamb with no clash.
- Fridge, oven and microwave, coffee bar, hob and hood intake, island drawers and stools: no intersections or floating
  parts found at eye level or low angles. No z-fighting seen in these rooms in any shot.
- Media wall: tower tops meet the AC bulkhead cleanly. The 5 cm reveal to the passage jamb at x 3.00 is intentional. The
  TV centre at 1.51 m is about 7 deg above a seated eye at 3.4 m, which is fine.
- Balcony: the railing is closed at both ends, and the north side wall meets the railing correctly. Drains are on the
  deck (one sits under the table, which is acceptable). Wall lights and ceiling lights sit on the plan points within 3 cm.
- Entry commode: 32 cm clear of the door swing; mirror reflection correct.
