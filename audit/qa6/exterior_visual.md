# QA6: exterior visual check (exterior_visual)

Date 2026-10-06. Model: `source/salon.html` at e94546d, built site on http://localhost:8000/. Report only, nothing edited.

Method: presets `view`, `balcony`, `balcony2`, `bird1`, `bird2`, `top`, day and eve. Custom cameras from every outside window
(room 1 and mamad west, room 2 and master bath north, master east, kitchen window C), from the balcony looking down north, east
and south, from street level on Ali Mohar and Tirtsa Atar, under the pilotis, 8 orbit views at 30 m, overheads of the lot, the
street and the junction, and detail views. Old state (6b679fd) served on 8792 for comparison (server stopped). Script and all
captures: `source/out/qa6_exterior_visual/` (`cams.mjs`, `set*.json`, `s1`..`s4`, `old`). Defect crops:
`audit/qa6/exterior_visual_img/`. No page errors in any run.

## Findings, most severe first

1. **The rounded SE lot wall floats 6.35 m above the ground.** CONFIRMED. A curved wall hangs in the air at about our floor
   level, seen from Tirtsa Atar, from the junction, from the floor-1 balcony and from our balcony (`jz1`). The lot corner at
   ground has no wall. Images `01_se_corner_wall_floating.jpg`, `01b_floating_arc_tirtsa_lawn_strip.jpg`.
   Cause, line 2058: `B()` already sets `position` to the box centre with y = GY + .25, then
   `w.position.set(6.1 + R * Math.cos(am), 0, 39.7 + R * Math.sin(am))` overwrites y with 0.
   Fix: `w.position.set(6.1 + R * Math.cos(am), GY + wallH / 2, 39.7 + R * Math.sin(am));`

2. **Ali Mohar's sidewalks and parking cross Tirtsa Atar, and the crossings z-fight.** CONFIRMED. The near sidewalk, the
   parking pavers, the far red sidewalk and its tactile strip run z -160..160, straight through the Tirtsa Atar carriageway.
   Tirtsa Atar's south sidewalk (z 60.5..62.5, x -160..160) runs across the Ali Mohar carriageway. Ali Mohar's centre line
   continues through the junction. Where the Tirtsa sidewalks overlap the Ali Mohar paver strip, both tops are at GY + .15 with
   different materials (mKerb, mPaver): visible stippled z-fighting (`jz2`, `jz1`). Same at the far red sidewalk x 27.4..34.2,
   z 60.5..62.5. Images `03_junction_sidewalks_cross_road_zfight.jpg`, `03b_junction_overhead.jpg`.
   Lines 1866-1867 (Tirtsa), 1934-1936 (near strips, asphalt, centre line), 1942 (near kerb), 1944 (far red sidewalk, kerb,
   tactile). Present before re-check 5 too, but now with the coplanar overlap at the new z.
   Fix: stop the N-S strips at the Tirtsa north kerb and restart past the south one, and keep asphalt continuous:
   near sidewalk `B(14.3, 16.9, -160, 48, ...)`; parking and its kerb end at z 43.8 (d03 draws the rounded end there, site.md
   item 12): `B(16.9, 18.8, -160, 43.8, ...)`, `B(16.75, 16.9, -160, 43.8, ...)`; in line 1944 use `[3.2, 48]` instead of
   `[3.2, 160]`; centre line loop `z < 46`; Tirtsa north sidewalk east part from x 27.4: `B(27.4, 160, 48, 50.5, ...)`;
   Tirtsa south sidewalk split into `B(-160, 16.75, 60.5, 62.5, ...)` and `B(30.2, 160, 60.5, 62.5, ...)` (whether Ali Mohar
   continues south is not on the sheets; if it ends there, keep the south sidewalk whole and end the Ali Mohar asphalt at 62.5).

3. **Tirtsa Atar: lawn strip instead of the parking on pavers, no kerb at the road.** CONFIRMED. Between the north sidewalk
   (z 48..50.5) and the asphalt (from 52.5) the model shows bare lawn (`ta1`, `ta3`, `ov_lot`, `ov_junction`). site.md item 8
   (from d03) has parking on pavers z 50.5..52.5 for x -13.0..9.8; APPLIED.md does not mention dropping it.
   Lines 1866-1867. Fix: `B(-160, 160, 50.5, 52.5, GY, GY + .03, mat.asphalt, OUT)` (or extend the street asphalt to 50.5) and
   `B(-13.0, 9.8, 50.5, 52.5, GY, GY + .04, mPaver, OUT)`, plus a kerb `B(-160, 16.9, 50.45, 50.6, GY, GY + .16, mKerb, OUT)`.

4. **Exterior stucco glows in the evening; the A/B bar has no lit windows.** CONFIRMED. At eve the bar balcony boxes, the
   pilotis columns, the lobby, the floor-1 and ground storeys and the garden apartment read light grey against a dark scene,
   while the bar facade is dark grey with no lit window at all; every other block has lit windows (`eve_am2`, `eve_orb0`).
   Image `04_eve_stucco_glows_bar_unlit.jpg`. The glow existed before (old `eve_orb0`) but re-check 5 added much more outside
   stucco. Causes: (a) the outside boxes use `mat.stucco`, which is also an interior material, so line 2280-2281 keeps it out of
   `extMats` and it keeps the bright room environment; (b) `building()` (line 1868-1872) makes a plain
   `MeshStandardMaterial({ map: facadeTex })`, never pushed to `litMats`.
   Fix (a): `const mStuccoOut = mat.stucco.clone();` and use it in lines 1877, 1878, 1880-1881, 1886-1887, 1928-1929.
   Fix (b): see finding 5 (atlas material is in `litMats`).

5. **The new A/B bar, B wing and core use the old flat facade texture, not the facade atlas; window rows do not match the
   storeys; the bar's soffit shows windows.** CONFIRMED.
   - `building()` line 1869: `t.repeat.set(Math.max(x2 - x1, z2 - z1) / 3.2, (h - base) / 3)`. Rows repeat every 3.0 m but the
     storeys and balcony slabs are 3.3 m, so window rows drift across the balcony slabs (`orb0`, `barnorth`, `roofbal`). The same
     horizontal repeat goes on every face, so the 10.4 m north and south faces of the bar get 6.7 squeezed bays and the core gets
     a partial bay. Image `05_balcony_on_roof_window_rows.jpg`.
   - The bar box starts at GY + 3.3; its bottom face carries the same map, so under the pilotis the ceiling is a field of dark
     window rectangles (`under1`, `under2`, `am1`). Image `02_bar_soffit_windows_no_west_support.jpg`.
   Fix: in `building()` use `blockMats[kind] ||= facadeAtlas(kind)` with the per-face UV code of `block()` (line 2145-2146),
   floors = `Math.round((h - base) / 3.3)`; and for `base > 0` add a soffit `B(x1, x2, z1, z2, GY + base, GY + base + .02,
   mStuccoOut, OUT)` and start the facade box at `GY + base + .02`.

6. **The bar hangs on one row of columns; lobby B is missing.** CONFIRMED (missing items), SUSPECTED (exact positions). Under
   z 13.2..30.6 the 10.4 m wide bar rests only on the five columns at x 8.15; its west half (x -2.1..about 3) floats with
   nothing under it (`under2`). site.md item 6 (d03) lists storage rooms, a smoke vent and lobby B in the closed core, not only
   lobby A. Lines 1877-1878. Fix: read lobby B and the west column line off d03 and add them; until then add estimate columns
   on the west edge, e.g. `[13.4, 16.6, 19.9, 23.2, 26.3].forEach(z => B(-2.1, -1.7, z - .4, z + .4, GY, GY + 3.3, mStuccoOut, OUT))`.

7. **Residential blocks throw no baked shadow, have no apron, and 15 courtyard trees stand inside them.** CONFIRMED. In
   `block()` line 2146 the statements `foot.push([x1, x2, z1, z2]); sunBoxes.push([x1, x2, z1, z2, h + 1.4]);` sit inside the
   trailing `//` comment (the same kind of bug as the balcony slab fixed in re-check 5; it dates from 40ed7eb). Result: no
   ground shadow west of any block while the bar and the school throw long ones (`ov_lot`, image
   `11_blocks_cast_no_baked_shadow.jpg`); no paved apron or base AO line at blocks; and the courtyard-tree loop does not avoid
   blocks. Measured on the live scene: 15 of 81 courtyard trees have their trunk inside a block footprint, 5 more within 2 m of a
   wall (crowns through the facade). Fix: move the two statements onto their own line after the `uv` loop.

8. **Blocks overlap the empty plot, the far sidewalk and the road.** CONFIRMED.
   - Block `[-14, 2, -48, -34, 7]` (line 2161) stands inside the hoarded empty plot north of our lot (line 2046, x -6..14.3,
     z -48..-11.9), seen from the room 2 and master bath windows. Its face is 1 m from a pallet; the blue hoarding at z -48 runs
     into it. Image `06_block_inside_hoarded_plot.jpg`. Fix: move the block west of x -8 (e.g. `[-26, -10, -48, -34, 7]`) or
     shrink the plot to x 3..14.3.
   - Block `[33, 45, -90, -74, 6, 'stone']` (line 2158): the +2.2 m shift moved the far red sidewalk to x 34.2, so the block now
     stands 1.2 m into the sidewalk (before it had a 1 m gap). Regression of 96821de. Image `07b_block_on_far_sidewalk.jpg`.
     Fix: start the block at x 35.2.
   - Ali Mohar's asphalt, sidewalks and centre line run z -160..160 straight into block `[-5, 34, -118, -102, 7, 'clad']` at
     the north T-junction and out the far side (`northT`, image `07_road_runs_into_block_block_on_sidewalk.jpg`). Lines
     1934-1944. Fix: end the Ali Mohar strips at the cross street (z -92), as in finding 2.
   - Block `[-20, -6, 62, 80, 7, 'stone']` starts at z 62, 0.5 m on the Tirtsa south sidewalk (to 62.5). Fix: z 63.

9. **One bar balcony per stack sits on the roof.** CONFIRMED. Line 1879 loops `f < 7`; the f = 6 slab is at y 16.15..16.4
   with its upstand and glass rail above the bar roof (16.5), a balcony with no storey behind it (`am2`, `roofbal`). It was so
   before too. Fix: `for (let f = 0; f < 6; f++)`.

10. **Floor-1 balcony: no rail on the north side; tile texture on its slab edge and soffit.** CONFIRMED. "Same plan as ours",
    but lines 1926-1931 copy only the east pickets and rails. Our balcony also has pickets and rails on the north upstand
    (lines 1696-1697); floor 1 has a bare 45 cm upstand there (`f1north`, image `08_floor1_balcony_no_north_rail_tile_edge.jpg`).
    The slab is one `mTerr` box (line 1927), so its 1.2 m overhang past the garden apartment shows terrazzo tiles on the
    underside and on the edge (`gardenapt`, image `08b_floor1_slab_soffit_tiles.jpg`).
    Fix: add `for (let x = BN + .07; x < BX2 - .12; x += .12) B(x - .01, x + .01, BZN + .08, BZN + .10, .47 + y, 1.05 + y, mat.blackMetal, OUT);
    B(BN, BX2 - .06, BZN + .06, BZN + .12, 1.05 + y, 1.09 + y, mat.blackMetal, OUT); B(BN, BX2 - .07, BZN + .07, BZN + .11, .45 + y, .49 + y, mat.blackMetal, OUT);`
    and split the slab: `B(BX1, BX2, BZN, BZ2, BY + y - .36, BY + y - .012, mStuccoOut, OUT); B(BX1, BX2, BZN, BZ2, BY + y - .012, BY + y, mTerr, OUT);`

11. **Near-side parking reads as sidewalk.** CONFIRMED. The sidewalk (14.3..16.9) and the parking strip (16.9..18.8) use the
    same `mPaver` (line 1934), separated only by a 15 cm kerb line, so from the master window and the balcony the parked cars
    seem to stand on the sidewalk (`w_master`, `b_down_e`). d03 draws herringbone pavers for the bays (site.md item 12), a
    different pattern from the sidewalk hatch. Fix: give the bays their own material, e.g. `const mPaverBay = TM(paverT('#8f8f8c',
    [140, 140, 136]), .9, 3.0)` (grey, estimate), add it to the `photoPBR` paver list and the site-mask `patch` list.

12. **Lawn-mask smear in our lot east of the bar; pilotis floor not paved.** CONFIRMED. South of the turf strip (z 9.9) the lot
    falls back to the generic ground: a 3 m grey apron blurred into lawn, so a muddy grey-green gradient runs along the pilotis
    and around the B wing (`am1`, `orb0`, `secorner`, image `12_lawn_mask_smear_by_pilotis.jpg`). d08 6.2.10 says the open
    pilotis floor is interlocking pavers (site.md item 6). Fix: `B(-2.1, 8.26, 13.2, 30.6, GY, GY + .02, mPaver, OUT)` under the
    bar, and turf `B(8.26, 14.1, 13.01, 39.7, GY, GY + .02, mat.turf, OUT)` (estimate: d03 hatch) so the lot no longer depends
    on the generic mask.

13. **Street light at z 38 grows through a tree.** CONFIRMED. Tree loop `z = -70 + 9k` puts a tree at z 38, x about 31; the
    lamp at line 1961 is at (30.6, 38). The pole runs through the trunk and crown (`lamp38`, image `09_lamp_pole_through_tree.jpg`).
    The lamp at z 12 is 1 m from the tree at z 11. Both moved together, so the shift kept the clash. Fix: lamps at
    `[-40, -14, 15.5, 33.5]`, or skip trees within 2 m of a lamp in the tree loop.

14. **Bench floats.** CONFIRMED. Line 2022 `B(33.2, 33.7, 9.6, 11.4, GY + .4, GY + .45, mat.walnut, OUT)` is a seat 25 cm
    above the red sidewalk (top at GY + .15) with no legs (`bench`, image `10_floating_bench.jpg`). Fix:
    `[9.75, 11.25].forEach(z => B(33.3, 33.6, z - .04, z + .04, GY + .15, GY + .4, mat.blackMetal, OUT));`

15. **Floor-1 box sticks out beside the core.** CONFIRMED (geometry), estimate either way. The floor-1 shell
    `B(-4.28, FO, -.13, 9.11, GY + 3.15, GY + 6.15)` (line 1887) fills x -4.28..-3.55, z 5.77..9.11, where floor 2 has nothing
    (the staircase mass ends at z 5.77 and the core starts at x -3.55). A 0.73 m ledge shows on floor 1's roof
    (`core2`, `orb4`, image `13_floor1_ledge_beside_core.jpg`). Floor 1 has our plan, so it should match floor 2. Fix: split it
    into `B(-4.28, FO, -.13, 5.77, ...)` and `B(-3.55, FO, 5.77, 9.11, ...)`.

16. **Floor 1 lacks the laundry louvre opening.** CONFIRMED (code and `orb6`, `pergola`). The dy -3.3 list (line 1891) has
    the room 2 and master bath windows but not the niche opening x 2.15..3.65 on the north face that floor 2 has. Fix: add a
    louvred or dark opening `['x', 2.15, 3.65, -5.39, -1, .15, 2.35]` to the floor-1 list (louvres optional).

17. **Seam at the floor-1 balcony north wall.** CONFIRMED (`f1north`: dashed vertical line at the corner). Line 1928 ends the
    wall at `BN + .002` (x 9.302); the floor-1 shell face is at 9.30, and both cover z -0.145..-0.13, 2 mm apart. Fix: wall
    `B(BX1, BN - .002, ...)` or start the wall at z `BZN` instead of `BZN - .015`.

18. **Smaller items.** CONFIRMED unless marked.
    - The B entrance gap (z 28.47..30.59) opens onto lawn: no path; the A gap has pavers only to z 13.01 of 14.92.
    - The ramp portal (line 2074) is a flat dark plate between 1.1 m walls; it does not read as a ramp going down. Estimate:
      a sloped plane from GY at z 21.4 to GY - 1.5 at z 17.4 would read.
    - The car gate (line 2059) is a plain black slab 1.6 m high; no bars.
    - Baked shadow (opacity .85) and the real-time shadow of floor 2 meet in the NW garden with a visible step in darkness
      (`nwshadow`). SUSPECTED minor.
    - Nothing above our apartment: from the street and the orbits our wing is a 3-storey stub beside a 7-storey bar, and the
      core box reads as a separate tower (`am2`, `orb6`). This is the documented cut-away, but it contradicts d05/d08 (floors
      1-4 same plan, 7 floors). Suggest an upper mass in its own group, hidden in `top`/`bird*` views and when the camera is
      inside.

## Checked and fine

- Garden apartment east face at x 9.25 with four openings at the d03 positions; north openings 0.29..1.35, 2.15..3.69 and the
  wide one under the pergola; west openings repeat ours.
- Floor-1 balcony walls, upstand and east pickets at the right height; our balcony slab now exists and its underside reads as
  plain plaster from floor 1.
- Private north garden turf, fences at x -1.19 and 9.19, pergola posts and slats, its baked slat-shadow polygon, three smoke
  vents with their shadows.
- North, west and east lot walls on the lot line; the A and B entrance gaps at the d03 z values; east garden strip turf and the
  two low walls; A entrance pavers.
- West parking stalls 1-6, both fire-truck pads, driveway, ramp walls, the outdoor stair under the mamad window, the NW tree.
- Pilotis columns at x 8.15 and the five z positions; lobby A box; B wing extents; bar extents.
- Near-side cars sit fully in the 16.9..18.8 strip (2 cm from the kerb); far-side nose-in cars inside their bays; parallel cars
  and the van in the far lane; no car on a kerb or in a wall.
- Far side moved as a whole: school, fence, signs, shrubs, cabinets, sails, turf, walkway, lamp, empty-lot fence and soil,
  driveway cars, street trees and lamps all at the new x; no object or baked shadow left at the old positions; tree, car, van,
  pole and school shadows follow the new positions (`ov_street`).
- Evening lamp pools follow the moved lamp heads (x 29.0 and the walkway lamp at 35.4, 8.0); no pool at the old x.
- No z-fighting between turf (GY + .02), pavers, asphalt (GY + .03) and the ground plane except the coplanar sidewalk overlaps of
  finding 2.
- Panel line 195 now describes floor 1's balcony and the garden apartment.
