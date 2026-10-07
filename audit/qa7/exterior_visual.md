# QA7: exterior visual check (exterior_visual)

Date 2026-10-07. Model: `source/salon.html` at e94c72c (outside as rebuilt in 51071c4), built site on http://localhost:8000/.
Report only, nothing edited.

Method: presets `view`, `balcony`, `balcony2`, `bird1`, `bird2`, `top`, day and eve, desktop 1280x800 and phone 390x844.
Custom cameras from every outside window, from the balcony looking down north, east and south, street level on Ali Mohar,
Tirtsa Atar and both junction corners, under the pilotis, the planter, both entrance gaps, the B wing, the ramp (top, south,
east, north, bottom, the parapet end), the car gate, the stalls, the floor-1 balcony, the garden apartment and pergola, overheads
of the lot, the junction, the street, the ramp, the SE corner, the west blocks and the north, 8 orbits at 30 m, 4 at 20 m and
4 at 40 m, and 14 eve cameras. A raycast probe for unclear pixels, and a scan of the whole scene for axis-aligned faces of
different materials that are coplanar or less than 8 mm apart (flicker candidates). Scripts and all captures:
`source/out/qa7_exterior_visual/` (`cams.mjs`, `probe.mjs`, `scan.mjs`, `scan.json`, sets `A`, `B`, `O`, `E`, `P`, `D`).
Defect crops: `audit/qa7/exterior_visual_img/`. No page errors in any run.

## Ratings (outside only)

- From the balcony: 6/10. Street, cars, school, street trees and sky read as a real street at a glance. Against it: every block
  is the same white box with painted windows, the cars are boxy, the ground is flat and clean, and the south-east half of the
  horizon is an empty lawn.
- From a bird view: 4/10. Our wing is a roofless three-storey stub next to a seven-storey bar, with the ceiling tops showing as
  a white patchwork. Floor 2 is lighter than floors 0-1, and at dusk it glows. The bar and core fill half of the top view on a
  phone. Lawns have no shrubs, and only one tree stands west of Ali Mohar.

## Five changes that would raise realism most

1. Build the storeys above us (floors 3-6 and the roof) as their own group, hidden in `top`/`bird*` views and when the camera
   is inside. Clad the floor-2 outer faces in exterior plaster. This removes the stub, the tone step and the eve glow
   (findings 4, 5, 13).
2. Close the empty south and south-east horizon with a ring of blocks, and put trees and hedges west and north of Ali Mohar
   and in our lot. The tree cards and the foot check already exist: extend the courtyard loop to x < 50 (finding 12).
3. Give the bar and blocks relief: real balcony slabs per flat on every face, window reveals 15 cm deep (or a normal/parallax
   term in the atlas shader), and rooftop parts on the bar (parapet, lift overrun, solar heaters as on the blocks).
4. Ground: replace the generic apron smear in our lot with explicit paving and planting, fill the junction corners, close the
   ramp gap and add a dropped kerb at the car gate (findings 1, 2, 8, 14).
5. Floors 0-1 windows and cars: windows with a reflective glass layer and a lighter interior colour instead of flat black
   slabs, and cars with real wheel arches and glass (a CC0 low-poly glTF set) (finding 11).

## Findings, most severe first

1. **See-through hole at the top of the ramp.** CONFIRMED. A sky-blue sliver at the south end of the ramp's east parapet,
   visible from the mamad window, from the south and from overhead (`ramp_gap`, `ramp_s`, `ov_ramp`, `w_mamad`). Images
   `01_ramp_gap_sky.jpg`, `01b_ramp_gap_from_south.jpg`.
   Cause, lines 2027 and 2245: the ground is open over x -21.86..-14.92, z -0.69..21.45, and the ramp plane covers
   x -21.86..-15.11. The east parapet `B(-15.11, -14.92, -.47, 20.90, ...)` stops at z 20.90, so x -15.11..-14.92,
   z 20.90..21.45 has no surface at all.
   Fix: `B(-15.11, -14.92, -.47, 21.45, GY - 3.0, GY + 1.0, mKerb, OUT);` (or keep 20.90 for the parapet and add a cap
   `B(-15.11, -14.92, 20.90, 21.45, GY - 3.0, GY, mKerb, OUT)`).

2. **Lawn in the road corners at the Ali Mohar / Tirtsa Atar junction (west side).** CONFIRMED. Grass in the carriageway
   corners: x 16.75..18.8, z 43.8..50.10 (between the near parking end, the Tirtsa north sidewalk and the asphalt) and
   x 16.75..18.8, z 60.18..62.18 south of Tirtsa (`corner_ne`, `junction`, `ov_junction`, `secorner_top`). Images
   `02_junction_corner_lawn.jpg`, `02b_junction_corners_overhead.jpg`.
   Cause: line 2095 ends the near parking at 43.8 and the sidewalk at 47.62, line 2030/2031 ends the Tirtsa sidewalks at
   x 16.75, and line 2096 starts the asphalt at x 18.8. Nothing covers the gap, so the ground plane with its lawn mask shows.
   Fix: `B(16.75, 18.8, 43.8, 62.18, GY, GY + .03, mat.asphalt, OUT);`. If d03's rounded parking end means a widened
   sidewalk, use `B(16.75, 18.8, 43.8, 47.62, GY, GY + .15, mPaver, OUT)` plus the asphalt for z 47.62..62.18.
   Related, minor: the south corner on the far side is notched. Ali Mohar's far sidewalk starts at kerb x 27.25, but the
   Tirtsa south sidewalk starts at 30.05 (line 2031). Use 27.25 there, as on the north side.

3. **Z-fighting on floor 1 west of the stair core.** CONFIRMED (scan and image). On floor 1, the core's facade atlas and the
   floor-1 plaster share the plane x = -3.55, z 5.77..9.11, y GY+3.15..GY+6.59. It shows as a blocky stippled panel, visible
   from the west orbits and from the outdoor stair (`d_core2`, `o30_4`, `core2`). Image `03_core_floor1_zfight.jpg`.
   Cause: QA6 split the floor-1 box (line 2045, `B(-3.55, FO, 5.77, 9.11, ...)`), whose west face now lies on the west face of
   `building(-3.55, 1.19, 5.77, 9.12, 23.1)` (line 2343).
   Fix: start the floor-1 box east of the core, `B(1.19, FO, 5.77, 9.11, GY + 3.15, GY + 6.59, mStuccoOut, OUT)`, since the
   core already fills x -3.55..1.19 there. Or start the core at x -3.56.

4. **Floor 2 is lighter than floors 0-1 by day and glows at dusk.** CONFIRMED. On the shadow (west and north) faces, the floor-2
   band reads light grey and the floors below mid grey, with a hard line at the floor-2 slab (`o30_4`, `o30_5`, `o20_2`). At
   eve our wing (walls, balcony, ceiling tops) stays light grey while the bar, floors 0-1 and the blocks go dark (`eve o30_0`,
   `o30_1`, `o30_4`, `o30_6`, `ov_street`, `am_s`). Images `04_floor2_vs_floor1_tone_day.jpg`, `04b_eve_floor2_glows.jpg`.
   Cause: the floor-2 outer faces are the `W()` walls in `mat.wall` (line 638), and the balcony walls, upstand and slab are
   `mat.stucco` (lines 1853-1855). Both are interior materials, so line 2467 keeps them out of `extMats` and they keep the bright
   room environment. Floors 0-1 use `mStuccoOut` with the photo-sky environment (QA6 finding 4 was fixed only for the new boxes).
   Fix: lines 1853-1855 to `mStuccoOut` (the balcony inner faces are outside too). For the floor-2 facade, add a 1 cm
   `mStuccoOut` skin on the outer planes (x -4.29, z -5.40, x 9.31 and the FO piers) with the same openings as the walls, or
   build it with `wallBox`. Until then, a stopgap: lower `mat.wall.envMapIntensity` in eve.

5. **Top view: the bar and the core fill the lower half of the screen; desktop `bird1` has the bar's facade in the corner.**
   CONFIRMED. On the phone the plan sits in the top third and the 17 m roofs of the core and bar cover the rest. On desktop the
   core's north face rises to 5 m under the camera (`top`, `ph_day_top`, `bird1`). Image `05_phone_top_bar_core_fill_half.jpg`.
   Cause: `building()` makes one box from the base to 23.1 m (lines 2032-2038, 2341-2343). `setView` (line 2766) hides only the
   ceiling for `top` views.
   Fix: in `building()`, split the box at GY + 9.9 (the top of floor 2): floors 1-2 stay in `outside`, and the upper box, its
   roof cap and the neighbours' balconies with f > 1 go into `const upper = new THREE.Group()` (merged on its own). The atlas
   UV code stays the same with `floors` per box. In `setView`, `upper.visible = !v.top;`. This also prepares change 1.

6. **Two residential blocks interpenetrate north-west of the lot (regression of QA6 finding 8).** CONFIRMED (geometry and
   image). Block `[-26, -10, -48, -34, 7]`, moved out of the hoarded plot in 51071c4, now overlaps block
   `[-40, -24, -40, -22, 7]` over x -26..-24, z -40..-34. Its south-face balcony slabs run into the other block. From room 2 the
   two read as one L-shaped mass with balconies stuck in its re-entrant corner (`d_blocks_w2`). Image
   `06_blocks_overlap_north_west.jpg`. Line 2335.
   Fix: `[-22, -8, -50, -36, 7]`. It must also clear the plot at x -6, the lot wall at x -22.06 and z -40 of the other block.
   Or move the other block to `[-44, -28, -40, -22, 7]`.
   The same script found two more overlaps:
   - block `[48, 64, -90, -72, 7]` faces west with 1.6 m balconies, but block `[35.2, 47.2, -90, -74, 6, 'stone']` stands only
     0.8 m away. Three balcony slabs run into the stone block, and the top one is coplanar with its roof at y 12.6 (scan). Fix:
     `[49, 65, -90, -72, 7]`.
   - block `[140, 158, 60, 82, 9]` stands 1.8 m on the Tirtsa south sidewalk (z 60.18..62.18, x to 160). Fix: z 63..85.
   - balcony slabs of `[35.2, 47.2, -90, -74]` (west face) and `[-20, -6, 63, 81]` (north face) hang over the public sidewalk.
     That is legal from 3.2 m up, so this is only a note.

7. **Two parked cars interpenetrate in the driveway by the tower.** CONFIRMED (scan and image). The cars at x 45.7 and 49.2,
   z 26.2 are 4.4 m long and 3.5 m apart, so they overlap by 0.9 m. Visible from the balcony and in `view` at the right
   (`d_cars`). Image `07_cars_interpenetrate.jpg`. Line 2183.
   Fix: `[[40.2, 1], [45.2, 3], [50.2, 6]]`.

8. **Lawn-mask smear south and west of the B wing.** CONFIRMED. QA6 finding 12 was fixed under the pilotis and in the east
   gardens. Between the B wing (z 42.6) and the lot wall (47.42), inside the rounded SE corner, and west of the B wing, the
   generic 3 m apron still blurs from beige into lawn (`secorner`, `secorner_top`, `ov_junction`, `ov_lot`). Image
   `08_lawn_smear_south_of_B.jpg`.
   Fix (estimate, d03 hatch): `B(-9.66, 8.27, 42.6, 43.8, GY, GY + .015, mPaver, OUT)` (paving at the wall) and
   `B(-9.66, 13.97, 43.8, 47.42, GY, GY + .02, mat.turf, OUT)`. Inside the arc, turf can stay because the wall clips it
   visually. A turf box `B(-15.11, -9.66, 21.45, 47.42, ...)` is not needed (driveway).

9. **Light seams in the baked ground shadow of the bar.** SUSPECTED. Thin light vertical bands at a regular spacing on the
   ramp's west wall, on the east parapet and in the shadow band in front of the west blocks (`w_room1`, `w_mamad`, `ramp_e`).
   The overhead `d_seam` is not conclusive.
   Likely cause: each bar segment is its own `sunBoxes` hull (line 2037). Where two hulls meet, the anti-aliased edges are
   drawn at alpha .85 twice. The seam pixel becomes 1-(1-.425)^2 = .67, against .85 inside, so a lighter line runs along the
   sun direction from every segment joint. The mask is also read on vertical faces (`mKerb` walls), which turns each seam into
   a vertical band.
   Fix: push one hull per bar (`[-2.13, 8.27, 9.11, 30.6, 23.7, .85, 3.3]` and the B wing as one box) instead of one per
   segment, or draw the sun canvas with `globalCompositeOperation = 'darken'` and alpha 1 into a separate layer, then multiply
   by .85.

10. **The south-east and south horizons are empty.** CONFIRMED. From `view` (right), `balcony2`, `b_down_s`, `ta_e` and
    `junction`, everything south of Tirtsa Atar and east of the tower is flat lawn to the horizon, with four blocks in total
    south of z 60. The block list (line 2331-2335) has nothing at z > 100. Image `10_empty_southeast.jpg`. Neve Zemer is built
    up on that side; this contradicts the photos, not a plan.
    Fix: a south ring (estimates), e.g. `[30, 48, 72, 92, 7], [-50, -32, 70, 90, 6, 'stone'], [70, 90, 110, 130, 8],
    [0, 20, 110, 128, 7, 'stone'], [110, 130, 96, 118, 7], [-80, -60, 100, 120, 8]`, and add their footprints to `foot` before
    the tree loop.

11. **Floors 0-1 windows and doors are flat black slabs.** CONFIRMED (`f1bal`, `gardenapt`, `pergola`, `o30_4`). `mDark`
    (`#2b3137`, roughness .08, line 2047) sits on a stucco face 1 cm proud, so by day it reads as a black void next to our lit
    floor-2 glass. Fix: colour `#56636c`, roughness .05, metalness .0, `envMapIntensity` 1.4 (it is in `extMats`, so it picks
    up the photo sky). Optionally add a second plane 20 cm behind in a light interior colour seen through
    `opacity .6` glass.

12. **No trees or shrubs west and north of Ali Mohar, nor in our lot beyond the one NW tree.** CONFIRMED (`o30_3`..`o30_5`,
    `o40_1`, `w_room1`, `w_room2`, `west_blocks`). The courtyard loop (line 2351-2352) only samples x 50..210, so the west
    blocks, the plot area and our lot lawns are bare. Fix: a second loop over x -80..14, z -140..140, with the same `foot`
    check (the lot is in `foot`, so add explicit spots inside it: e.g. along the north and west lot walls every 6 m, as
    hedges `B(..., GY, GY + 1.0, mat.leaf2)` or small tree cards).

13. **Our wing has no storeys above it.** CONFIRMED (QA6 finding 18, still open). From every orbit our wing is a three-storey
    stub with the interior ceiling tops as its roof, while d05/d08 have the same plan on floors 1-4 and seven floors. It is the
    largest single realism loss from outside. Fix: see change 1 and finding 5 (an `upper` group with floors 3-6 and a roof,
    hidden in `top`/`bird*` and while the camera is inside the apartment box).

14. **No dropped kerb or driveway apron at the car gate.** CONFIRMED (`gate`). The Tirtsa north sidewalk runs at full 15 cm
    height across the gate opening x -21.86..-17.74 (line 2030), so cars would climb a kerb. Fix: split the sidewalk at the gate
    and add `B(-21.86, -17.74, 47.62, 50.10, GY, GY + .03, mat.asphalt, OUT)`.

15. **Balcony slab corner sticks out past the south wall and into the neighbour's balcony.** CONFIRMED (probe). Line 1855: the
    slab `B(BX1, BX2, BZN, 9.20, ...)` runs to x 10.45 at z 8.71..9.20, past the south wall that ends at `BS` 10.07. It leaves a
    38 x 49 cm ledge in interior `mat.stucco` that is bright at eve (`b_down_s`, day and eve). The neighbour's balcony
    (line 2346) starts at z 9.13, so it overlaps our south wall by 7 cm. Fix: slab to z `BZ2` beyond x `BS`
    (`B(BX1, BS, BZ2, 9.20, ...)` plus `B(BX1, BX2, BZN, BZ2, ...)`) and the neighbour's first balcony from z 9.20.

16. **Coplanar kerb tops at the bay ends.** CONFIRMED (scan). The red-white kerb blocks at z -8.15..-8 and 3.2..3.35
    (line 2107, top GY + .16) share their top and side faces with the far kerb `B(27.25, 27.4, ...)` (line 2105) over
    x 27.25..27.4. The patch is only 15 x 15 cm. Fix: start the red-white run at x 27.4, or lift it to GY + .162.

17. **Minor.**
    - The rounded SE wall ends at z 47.35 (centre), the south wall's centre is 47.52: a 17 cm jog at x 6.15
      (line 2219-2220, R 7.85, centre z 39.5). Use centre z 39.67, or R 8.02 with centre x 6.05, so that both ends meet the
      wall centre lines. CONFIRMED (geometry), barely visible.
    - Flicker distances: the closest different-material ground layers are 5 mm apart (asphalt .03 vs fire pad, blue bays and
      centre line .035; pavers .015 vs turf .02 in front of A). With near 0.06 and a 24-bit depth buffer they hold up to about
      70 m looking straight down and much further at grazing angles, so no preset flickers. Only far overheads (`ov_lot` at
      126 m) can. If walking above the site becomes possible, raise the top layers to 1 cm.
    - Light leaks: thin vertical bright slivers at some bar corners at eve, where a lit bay is squeezed onto a narrow step face
      (`eve o30_6`, `o30_4`). Hash `fLit` to 0 when the face is narrower than one bay.

## Checked and fine (QA6 items verified as fixed)

- SE lot wall stands on the ground; Ali Mohar and Tirtsa Atar cross with no sidewalk through a road; no coplanar sidewalk
  overlaps left at the junction (scan).
- Tirtsa parking on grey pavers; near-side bays grey, distinct from the sidewalk.
- The bar uses the facade atlas with 3.3 m rows; the balcony slabs fall at the storey lines; the soffit is plain plaster; no
  balcony on the roof; storage blocks and lobby carry the west half; the columns are under the bar.
- Floor-1 balcony has north and east rails and a plaster slab edge; no ledge beside the core; floor-1 laundry opening present;
  no seam at the floor-1 north wall.
- Ramp reads as a lane sloping down to the basement gate, with walls and a barrier (except finding 1).
- Stalls 1-4 as 2x2, fire-truck pads, stalls 5-6, outdoor stair, A and B entrance paths, planter, B east garden and vent.
- Lamp poles clear of tree trunks; the bench has legs; the car gate has bars.
- Block shadows are back and fall west-north-west, consistent with the sun and with the bar and school shadows; no block on Ali
  Mohar or its sidewalks; no courtyard tree seen inside a block.
- No double shadow found: floor 2 is the only real-time caster, and floors 0-1, the bar and blocks are baked only. The edge
  between the sharp real-time part and the soft baked part of our building's shadow is visible but not a defect.
- Evening: lit windows on the bar and blocks in three warmths, street lamp heads glow, and the light pools sit under the heads.
  Exterior plaster (floors 0-1, bar, pilotis) goes dark at dusk as intended (except finding 4).
- Phone: all six exterior presets render, day and eve, with no errors.
