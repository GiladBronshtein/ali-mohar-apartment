# QA7: flicker, shimmer and swimming (flicker)

Line numbers are `source/salon.html` in the working tree on 2026-10-07. Other QA7 agents are editing it at the same time
(uncommitted), so the numbers drift: search for the quoted code. At commit e94c72c the same lines sit 5 to 30 lines higher.

Method.
- Static scan: a Playwright run served an in-memory copy of `index.html` that tags every mesh with its creation stack. It dumped
  every world triangle of 1 cm2 or more: before `mergeGroup` for root, ceiling, outside, plants and trees; after load for every
  unmerged mesh (doors, curtains, fans, mirrors, contact planes, props, tree cards); and fixRoot for the defaults plus all 143
  fixture options, one at a time through `fixSet`. That is 490k triangles from 20.5k meshes. Python then looked for faces of
  different materials that face the same way and overlap in the plane. Effective facing counts BackSide as flipped and
  DoubleSide both ways. Planes had to be within 1 mm indoors. Outdoors the limit was 2 cm, checked against depth precision:
  near 0.06 with 24-bit depth means a gap g starts to fight beyond sqrt(g x 0.06 x 2^24 / 2), so 1 mm at 22 m, 5 mm at 50 m
  and 1 cm at 71 m. Overlaps buried in an opaque box, undersides below eye height and ceiling top faces were dropped.
- Temporal test, desktop HQ (1200x800, DPR 1), 25 poses by day (every room, balcony, outside, bird1), 10 by eve, and 12 phone
  poses (390x844, DPR 2, plain renderer). The RAF loop was paused (`window.__pause`) and every frame drawn with
  `__app.renderOnce`. Each pose captured four things. (a) 10 frames of pure yaw, 0.1 deg per step. A pure rotation is an exact
  homography, so each frame was warped back onto frame 0 with numpy/scipy. The per-pixel std that is left, minus an
  interpolation baseline, is real flicker (map F). (b) 7 frames of dolly, 4 mm per step, scored by second temporal difference.
  (c) The same pose rendered twice, for pure noise. (d) The first, second and 32nd TAA still frames. (e) A 3 px whole-pixel view
  offset, which finds patterns locked to the screen. Then 8 telephoto and close poses to check the scan hits.
- Scripts and raw data: `source/out/qa7_flicker/` (dump.mjs, scan.py, temporal.mjs, analyze.py, viz.py, crop.py,
  coplanar7_static.txt, coplanar7_all.txt, d_day/, d_eve/, p_day/, v_day/). Every crop strip shows frames R0, R3 and R6 aligned
  to R0, so only the flicker changes, then the F map in red, then the TAA still.

## Findings

1. **Every stop of the camera on desktop HQ makes the edges jagged, then they smooth out over about half a second.** CONFIRMED,
   in all 25 poses. While moving, `renderPass` draws into the composer target, which has MSAA 4x. On the first still frame
   `TAARenderPass` makes its "hold" image through `SSAARenderPass.render`, which draws the scene into `taa.sampleRenderTarget`.
   That target is created without `samples`, so the hold has no AA at all. It then weighs (32-k)/32 in the blend. Edge error
   against the converged still, mean of 25 poses: moving 6.6, first still frame 15.1, second 14.4 (luma 0..255). The jump on
   the edges from the last moving frame to the first still frame is 11.3. Image: `flicker_img/taa_stop_view.jpg` (last moving
   frame, first still frame, converged; balcony railing in `view`).
   Cause: line 289 `const taa = new TAARenderPass(scene, camera); taa.sampleLevel = 0; ...` together with lines 3023-3024
   (`frame()`). Fix: give TAA a multisampled sample target before its first use. In r160 an MSAA target keeps its colour
   between renders (only depth is invalidated), so the additive accumulation still works:
   ```js
   const taa = new TAARenderPass(scene, camera); taa.sampleLevel = 0; taa.accumulate = true; taa.enabled = false;
   taa.sampleRenderTarget = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 });   // hold frame keeps MSAA
   composer.addPass(taa);
   ```
   The composer's `setSize` resizes it (`SSAARenderPass.setSize`). After the fix, check that the S1 edge error falls to the
   moving level.

2. **Two parked cars overlap, and their shared side face z-fights.** CONFIRMED with a telephoto from the balcony (stippled
   black and white patch where the black car's flank and the white car's nose meet). Image: `flicker_img/cars_overlap_zfight.jpg`.
   Cause: line 2198 (at capture time) `[[40.2, 1], [45.7, 3], [49.2, 6]].forEach(([x, i]) => car(x, 26.2, 'x', carCols[i]));`. The cars are 4.28 m
   long but stand 3.5 m apart, so they overlap by 0.78 m. Both bodies have their side faces at z 27.09 and 25.31. Fix:
   `[[40.0, 1], [45.0, 3], [49.9, 6]]` (gaps of 0.7 m). The working tree now has `[[40.2, 1], [45.2, 3], [50.2, 6]]` (from
   another agent), which also clears the overlap; keep it.

3. **Tree cards sparkle while moving.** CONFIRMED in `view`, `street`, `streetS`, `balcony2` and the telephotos (the brightest
   blobs outside). Image: `flicker_img/tree_cards_sparkle.jpg`. Cause: line 2404, the card material uses `alphaTest: .45` with
   no coverage AA, so every leaf edge is a hard 1-sample cut. Mip levels also thin the alpha at a distance. Fix: in the same
   `MeshStandardMaterial` add `alphaToCoverage: true`. MSAA is on in the composer target and on the phone canvas, so it works
   on both. Optionally lower `alphaTest` to .3.

4. **Slats and bars thinner than a pixel give moire.** CONFIRMED, each with a crop:
   - Living-room supply grilles (`entry`, `tvwall`, `hall`, `photo`): line 1332, 1 cm slots every 3 cm. Image:
     `flicker_img/ac_grille_tvwall.jpg`.
   - Corridor return grille (`corridor`): line 1106, 12 mm slots every 35 mm. The slots break into dashes. Image:
     `flicker_img/return_grille_corridor.jpg`.
   - Room 1/2 combined grilles: line 1110, same pattern.
   - Tower louvre strips (`view`, `photo`, `street`, `balcony2`, at 55-60 m): line 2215, 7 cm slats every 25 cm, about 1 px
     each. Image: `flicker_img/tower_louvres_view.jpg`. The telephoto is clean, so this is pure pixel-size aliasing.
   - School fence (`street`, `view`): line 2181, 2.5 cm bars every 15 cm at 25-40 m. Image: `flicker_img/school_fence_street.jpg`.

   Fix: geometry cannot be filtered, but a mipmapped texture can. Draw each grid as one plate with a stripe canvas texture,
   as line 2095 already does for `mBlueFence`. For the grilles:
   ```js
   const slotTex = canvasTex(64, 8, (g, w, h) => { g.fillStyle = '#ecebe7'; g.fillRect(0, 0, w, h); g.fillStyle = '#2a2c2e'; for (let x = 0; x < w; x += 16) g.fillRect(x, 0, 6, h); });
   // 1332: one plate instead of the loop; repeat = slot count
   const t = slotTex.clone(); t.repeat.set(29, 1); t.needsUpdate = true; const m = mesh(new THREE.PlaneGeometry(.86, .12), new THREE.MeshStandardMaterial({ map: t, roughness: .6 }), root, false);
   ```
   Do the same for line 1106, line 1110 (rotated stripes), the tower slats at line 2215 (one box with a horizontal stripe
   texture), and line 2181: one plate with alpha stripes, `alphaTest` plus `alphaToCoverage`. Up close a grille can keep its
   slat boxes; the plate can sit 1 mm behind them.

5. **Door and drawer gap lines crawl and break into dots.** CONFIRMED in `kitchen3`, `kitchen2`, `storage`, `bird1` (the pantry
   reads as dotted lines from above) and the wardrobes. Image: `flicker_img/door_gaps_kitchen3.jpg`. Cause: gaps 3-4 mm wide
   in pure black: line 1484 (lower kitchen), line 1510 (upper kitchen), line 1472 (pantry), line 1287 (storage wall), line 880
   (wardrobe helper), and the vanity `gap()` at line 812. At 2-4 m a 4 mm gap covers 0.5-1 px. Fix: make them 6 mm and dark
   grey, so they cover at least 1 px and step less, e.g. line 1484
   `B(x - .003, x + .003, 8.185, 8.19, .12, .81, mGap, { cast: false })` with `const mGap = M('#45484b', .8)`; same at 1510,
   1472, 1287, 880. Finding 1 also makes them settle cleanly when still.

6. **TV-wall fluting and its warm LED seams shimmer.** CONFIRMED (`tvwall`, `entry`, `photo`; the eve run adds the 1 px
   under-cabinet LED line in the kitchen). Image: `flicker_img/fluting_tvwall.jpg`. The LED seams that QA6 found buried are
   now in front (line 1306, `CD..CD + .002`). At 12 mm wide and emissive with bloom, each one is a 1-2 px bright line that pulses
   as it moves across pixel centres. The flute edges (line 1298, 1314, plus line 1461 for the coffee bar) step in the same way.
   Fix: widen the seams to 2 cm and lower their emissive so bloom does not lift single pixels:
   `B(x - .01, x + .01, CD, CD + .002, ...)`, `mat.ledWall.emissiveIntensity` about 0.6x. Round the flute slats
   (`{ round: .004 }`) so the edges catch a soft gradient rather than a 1 px highlight.

7. **The open sheer stacks shimmer.** CONFIRMED (`entry`, `photo`, `inside`). Image: `flicker_img/sheer_entry.jpg`. Cause:
   line 1243 crams the open curtain into `Math.round((b - a) / .2) * 1.2 / st`, about 28 waves per metre (3.6 cm folds,
   amplitude 6 cm). Each fold is a light and a dark band 3-4 px wide. On top of that, the sheer texture at line 1233 draws a
   1 px stripe every 2 px (Nyquist rate). Fix: fewer, deeper folds when open, e.g. `Math.round((b - a) / .3) / st` with
   amplitude `.08`. Drop the 2 px stripe loop at line 1233; the speckle above it already gives the weave.

8. **Ambient occlusion grain is locked to the screen, so it swims while you walk.** CONFIRMED by measurement, desktop HQ only.
   After a whole-pixel 3 px view offset, the image should match itself shifted by 3 px. It does not in creases and corners:
   p99 2.5-6.4 (luma), up to 20 in the slat gaps of `bedtv`. Image: `flicker_img/ao_screenlocked_bedtv.jpg` (offset frame,
   shifted frame, difference x10). Cause: `GTAOPass` uses fixed screen-space noise textures (lines 291-293), and while moving
   there is no TAA to average it. Fix (cheap): more denoise,
   `gtao.updatePdMaterial({ lumaPhi: 6, depthPhi: 2, normalPhi: 4, radius: 9, rings: 4, samples: 32 })`, and
   `samples: 32` in `updateGtaoMaterial`. Or skip GTAO while moving and fade it in during the TAA accumulation.

9. **"Moda" (butcher) vanity: the oak side strips are coplanar with the carcass sides.** Geometry CONFIRMED. Flicker SUSPECTED:
   the close-up camera missed the vanity. Area 0.19 m2 on the visible side of the master-bath vanity (z -3.32, from the bedroom
   door) and 0.014 m2 in the family bath. Cause: line 824
   `[[z1, z1 + .025], [z2 - .025, z2]].forEach(([a, b]) => B(x0, xf + .013, a, b, y0, yT, oak))` shares the faces z1 and z2
   with the carcass `B(x0, xf, z1, zs, y0, yb, body)` and its rim boxes. Fix:
   `[[z1 - .001, z1 + .025], [z2 - .025, z2 + .001]]`. The other 142 fixture options have no visible coplanar faces.

10. **Window sills are still coplanar with the wall top under the window (the open item from the fourth check).** Geometry
    CONFIRMED. Not seen in the shots (2-3 cm strip). Six windows: room 1, room 2, master, master bath, family bath, mamad (their
    calls are on lines 1575, 1594, 1644, 1774, 1797, 1851). Cause: lines 1018 and 1031 put the sill top exactly at `sill`, the
    top of the wall segment under it. Fix on both lines: `sill - .03, sill + .002`. Kitchen window C (QA6 #11) is fixed.

11. **Windows of floors 0-1 under the flat: the dark pane shares faces with the frame boxes.** Geometry CONFIRMED (162 overlaps,
    all with gap 0). Flicker SUSPECTED: visible only from the bird views and from the street. Cause: line 2069
    `P(a1, a2, .01, sill, head, mDark)` starts at the same plane and the same ends as the four frame boxes on the next line.
    Fix: inset the pane, `P(a1 + .004, a2 - .004, .008, sill + .004, head - .004, mDark)`.

12. **The shared `mat.screen` is switched to DoubleSide by the iMac.** CONFIRMED in code. Line 1824 sets
    `scr.material.side = THREE.DoubleSide` on the shared material. From then on every screen is double-sided (TV line 1325, hob
    line 1489, monitor, fridge display, panel plate), and their back faces lie on the bodies they sit on (TV back 0.5 mm from its
    bezel, hob bottom on the quartz top). Today these are hidden, but it is a latent z-fight and costs extra shadow-map faces.
    Fix: `scr.material = mat.screen.clone(); scr.material.side = THREE.DoubleSide;`.

13. **Small exterior coplanar faces.** Geometry CONFIRMED, low (small, or not in any view):
    - Red/white kerb ends: line 2122 against the sidewalk box at line 2120 (faces z -8 and 3.2).
    - Stair core west face x -3.55 (line 2361) against the floor-0/1 stucco boxes (this west face is not in a view).
    - Ramp walls: line 2261 against 2262 (x -14.92).
    - Tower mullion against the window, 5 mm apart at 59 m (line 2174).
    - Kerb top 1 cm over the sidewalk (line 2110), tactile strip 6 mm over the red pavers (line 2120) and centre line 5 mm over
      the asphalt (line 2112). By the depth math these fight beyond 50-70 m. Telephotos from the balcony at 60 m (`tele_line`,
      `tele_tactile`, `tele_kerb`) showed no flicker, so no change is needed now. Keep any new exterior offset at 1 cm or more.

## Checked and fine

- No frame-to-frame noise at a fixed pose: the double render was bit-identical in all 47 desktop and phone captures. Nothing
  animates by itself.
- Phone path (no composer): no stop pop and no screen-locked grain. Its flicker is lower than desktop in every shared pose.
  Hotspots are the same items as findings 3-6.
- Sun shadows: the shadow map is static, so it does not swim with the camera. No acne or peter-panning found in any pose.
- Contact-shadow planes (polygonOffset, depthWrite false) do not fight the floors.
- QA6 coplanar fixes hold: balcony north stucco at `BZN - .013` (line 1860), stair core to 9.12 (line 2361), Ali Mohar
  sidewalk split at Tirtsa Atar (line 2110). Kitchen window C sill ends at 1.205 (line 1230).
- The ceiling is DoubleSide and coplanar with the tops of the 2.70 cabinets. Those faces only show from above, and top views
  hide the ceiling.
- Glass, shower glass, sheers and zebra blinds are transparent with depthWrite false. No sorting pop was seen in the shots.
- Eve run: lamps and bloom add no new flicker apart from the kitchen LED line in finding 6.
