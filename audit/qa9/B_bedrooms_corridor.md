# QA9 B: corridor, master bedroom, closet, rooms 1-2, mamad, master vestibule

Report only, nothing in `source/` was edited. Reviewed 2026-10-07, 18:50-19:35, against the served build (`index.html` from the
working tree). Line numbers refer to `source/salon.html` in the working tree as of 19:31, which already holds the lead's
uncommitted QA9 edits. Each item also gives a search anchor because the file is still changing.

Images are under `audit/qa9/B_img/`: `b1` named views and first close-ups, `b2` close-ups and the probe A/B, `b3`/`b4` fix
experiments run live in the page (JS, nothing saved), `b5` probe timing, `b6` re-check on the 19:31 build. The capture tool with
a `js` hook is `source/out/qa9B_shots.mjs` (gitignored); the shot lists are in `/tmp/qa9_B*.json`.

Walls are untouched in every proposal below, so `roomdims.py` and `clearance_audit.py` are not affected. The door-pivot fix (A4)
moves open leaves 3.7 cm, which is within the clearances the audit already checks.

## Already fixed in the working tree (verified)

- **Probe tint on white plates, white fronts and the porcelain floor.** In the committed build, `mat.whitePlate`, `mat.whiteFront`
  and `mat.tile` used the living-room probe as their env map. Every switch and socket read taupe-brown, the white nightstands,
  wardrobes and bookcases looked dirty beige, and the corridor floor went almost brown. The A/B is in
  `b2/ab_kkk.jpg`, `b2/ab_r2ns.jpg` and `b5/probe_corridor_with_without.jpg`. The working tree (L2572 `const PROBE_GLOSSY`) has
  dropped them, and `b6/cur_grid.jpg` shows white plates and fronts. Nothing more to do.
- Note on the hinge knuckles that were just added (L1011, `three hinge knuckles`): at `lb(P, -.012, .004, -.008, .008, ...)` they
  sit inside the jamb lining both open and closed, so they never show. A4 below gives a placement that does show.

## A. Fix now (safe)

### A1. High: a bright line along the top of every wall by day (sun leaking through the ceiling junction)
- Where: every room by day. The worst spots are the vestibule (`b1/c_vest_ac.jpg`), the master NW corner (`b2/c_master_ceiling_line.jpg`),
  `b1/v_master2.jpg`, the top of `b1/v_room1.jpg` and the mamad north wall (`b2/c_m3_sleeves.jpg`). It is still there on the 19:31
  build (`b6/cur_grid.jpg`, top right). It disappears in the evening (`b1/e_master2.jpg`), which pins it on the sun.
- Root cause: the ceiling is a single plane at H (L1219-1220) and walls stop at H. With `sun.shadow.bias = -.0004` and
  `normalBias = .02` (L2694), any wall point within about 2-3 cm of the occluder along the sun direction counts as lit. The result
  is a 1-2 cm sunlit strip under the ceiling that reads like a cove light or a gap.
- Test results: `b3/x_line_abc.jpg` shows default / bias -.0001 with normalBias .01 / occluder slab. Reducing the bias only thins
  the line. The slab removes it completely. With the slab, `b3/x_line_c_slab_living.jpg`, `..._master.jpg`, `..._room1.jpg` and
  `..._vest.jpg` show no side effects; the balcony sun patch is still there.
- Fix: add after L1220 (`master wing only`) a shadow-only slab whose shadow depth is its top face:
  ```js
  { const m = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false }); m.shadowSide = THREE.FrontSide;   // sun occluder above the ceiling: the plane alone let the sun through the top 2 cm of every wall (shadow bias)
    [[-4.3, FO, -5.4, 9.11], [FO, 9.30, -5.4, -.13]].forEach(([x1, x2, z1, z2]) => { const s = new THREE.Mesh(new THREE.BoxGeometry(x2 - x1, .25, z2 - z1), m);
      s.position.set((x1 + x2) / 2, H + .137, (z1 + z2) / 2); s.castShadow = true; s.receiveShadow = false; ceilGroup.add(s); }); }
  ```
  It lives in `ceilGroup`, so top views hide it like the ceiling. It stays off the balcony, whose x range is past FO south of
  -0.13. After adding it, check that `mergeGroup` keeps it as its own draw (unique material) and that `lm/export` does not mind
  one extra `ceil_` box above the ceiling. Run `sitetest`.

### A2. Medium-high: open curtains in rooms 1, 2 and the master are lit by the window light from 6-7 cm away (ragged, blown folds)
- Evidence: `b2/c_r1_window.jpg` shows the curtain stacks with a jagged lit edge, as if torn. The master curtains read blown
  white (`b1/v_master.jpg`). Fixed in place: `b3/x_win_r1.jpg` (left before, right after), `b3/x_win_master.jpg` and `b3/x_win_room2.jpg`.
- Root cause: the window RectAreaLights sit 1 cm inside the wall face (L2704 `winLight(-3.88, ...)`, L2705 `winLight(.815, -4.99, ...)`,
  L2707 `winLight(8.90, ...)`). The curtains hang at x -3.82, z -4.92 and x 8.83, so the folds straddle the one-sided light plane.
- Fix: move the light planes back into the reveal, toward the glass: room 1 `winLight(-4.03, -2.36, ...)`, room 2
  `winLight(.815, -5.14, ...)`, master `winLight(9.05, -1.79, ...)`. Leave the rest of each call unchanged. The room gate boxes are
  tested at the shaded point, so nothing else needs to change. Daylight levels looked the same in the test.

### A3. Medium: switches and sockets hidden or clipped by furniture and casings
Each one is a coordinate change. Plate width is 8 cm, rows are 8.5 cm apart.

| # | What | Evidence | Line / anchor | Fix |
|---|---|---|---|---|
| a | Room 2 light switch inside the door is 2 cm inside the wardrobe side (wardrobe ends at x .78, plate .76-.84) | `b2/c_r2_sw_wardrobe2.jpg`, `b6/cur_grid.jpg` (row 2 left) | L1214 `['n', -1.45, 0.80]` | `['n', -1.45, 0.83]` (plate .79-.87: 1 cm from the wardrobe, 1.1 cm from the 7 cm casing at .881) |
| b | Corridor switch at the room 2 door is 1.4 cm inside the new 8.5 cm casing (casing edge 1.834, plate 1.82-1.90) | `b1/c_corr_sw_186.jpg`, `b1/c_passage.jpg`, `b6/cur_grid.jpg` (row 2 right) | L1213 `['s', -1.245, 1.86]` | `['s', -1.245, 1.885]` (plate 1.845-1.925; the wall continues past 2.01) |
| c | Mamad switch by the blast door is half behind the bookcase upright (upright x -1.11..-1.09, 4 cm off the wall, plate -1.14..-1.06) | `b1/c_m3_sw_bookcase.jpg`, `b1/c_m3_to_door.jpg`, `b6/cur_grid.jpg` (row 3 left) | L1837-1840 (bookcase in `withShift(-.08, -.11)`) | The switch cannot move (latch jamb at -1.19), so narrow the bookcase from 83 to 75 cm. Replace every `-1.03` with `-.95` on L1837-1839, the side `B(-1.03, -1.01, ...)` with `B(-.95, -.93, ...)`, the back `B(-1.01, -.22, ...)` with `B(-.93, -.22, ...)`, the door split `B(-.617, -.613, ...)` with `B(-.577, -.573, ...)`, and on L1840 both `books({ g: root }, -.95, ...)` with `-.88`. The bookcase then starts at world x -1.03, 3 cm clear of the plate. |
| d | Room 2 bed-head light switch is completely behind the headboard; the socket and shutter switch are behind the nightstand books | `b1/c_r2_bedhead.jpg`, `b3/c_r2_headboard_sw.jpg`, `b6/cur_grid.jpg` (row 4 right) | L2008 `outlets('s', -5.01, .02, .65, 'ksr')`; nightstand L856/861, room 2 call L1814 | `outlets('s', -5.01, .14, .65, 'ksr')`: the first plate starts 0.5 cm past the headboard (headboard to x .01). Recheck 1 (`audit/recheck/electrical.md` L47) reads this row at x .01/.23/.45 with weak scaled evidence, so .14 is within what the plan shows. Also `function nightstand(P, { m = mat.oak, lampOn = true, books: bk = true } = {})`, `if (bk) books(P, hx - .2, .5, 0, .16, 'x', 4);`, and on L1814 `nightstand(P, { m: mat.whiteFront, lampOn: false, books: false })`. |
| e | Room 2 TV point and socket+data at h 1.80 (east wall, z -2.86) are buried in the bookcase back panel (back x 1.82-1.84, plate 1.838-1.85) | `b1/c_r2_tvpoint.jpg`, `b3/c_r2_tv_hidden.jpg` | L1824, last box `B(1.67, 1.69, -3.43, -2.07, .8, 2.0, mat.whiteFront)` | Stop the back at the 1.58 shelf: `B(1.67, 1.69, -3.43, -2.07, .8, 1.58, mat.whiteFront)`. The 1.60-1.98 bay is empty and open to the wall, so the plates show in it. |
| f | Room 1 shutter switch (west wall, z -1.80) is half behind the open curtain stack (stack to -1.79) | `b1/v_room1.jpg` | L1807-1809 | Track `B(-3.84, -3.79, -2.95, -1.87, ...)`; open stack `curtainPair(curtOpen, 'z', -2.15, -1.88, ...)`; second closed panel `(-2.38, -1.88)`. Closed still covers the window, which ends at -1.91. |

### A4. Medium: open leaves pass through their own jamb and casing (dashed line along every hinge edge)
- Evidence: a stippled vertical line on the hinge edge of every open interior leaf: `b2/c_r1_leaf_edge.jpg`, `b1/c_r1_door_in.jpg`,
  `b2/c_mdoor_hinge_top.jpg`, and the right casing in `b2/c_skirt_r2door.jpg`. It is still there at 19:31 (`b6/cur_grid.jpg`, row 4 left).
  Fixed live (open leaves only moved): `b4/y_hinge_r1.jpg`, `b4/y_hinge_m.jpg` and `b4/y_hinge_r2.jpg`. The line is gone, and the
  open leaf now stands on the jamb line the way a real 90-degree leaf does.
- Root cause: `doorLeaf` pivots on the leaf's centre plane (L1004 `g.position.set(hx, 0, hz)`). At 90 degrees the leaf is 4 cm thick
  around a pivot that sits 1.5 cm inside the jamb lining, so it intersects the lining (2.5 cm) and the casing (18 mm proud) of the
  rebuilt PanClassic frame.
- Fix: when open, shift the leaf by `c * (t/2 + .017)`, where c is the closed direction (toward the latch). The leaf's lining-side
  face then sits 2 mm off the lining and clears the casing. The blast door (surface-mounted, t .08) is excluded.
  ```js
  // L1005, after open/closed are computed:
  const po = cx === null || t > .05 ? null : [hx + cx * (t / 2 + .017), hz + cz * (t / 2 + .017)];   // open: the leaf face on the jamb line, clear of lining and casing
  if (po) g.position.set(po[0], 0, po[1]);
  doors.push({ g, open, closed, hx, hz, po });          // replaces doors.push({ g, open, closed })
  // L3107 setDoors:
  doors.forEach(d => { d.g.rotation.y = closed ? d.closed : d.open; if (d.po) d.g.position.set(closed ? d.hx : d.po[0], 0, closed ? d.hz : d.po[1]); });
  // L1011 knuckles: on the swing face, just past the lining, so they show closed and open
  const ks = Math.sign(cx * dz - cz * dx) || 1;
  [.25, 1.05, 1.85].forEach(y => lb(P, .016, .026, ks > 0 ? t / 2 : -t / 2 - .012, ks > 0 ? t / 2 + .012 : -t / 2, y, y + .10, mat.blackMetal));
  ```
  Furniture check for the 3.7 cm move: room 1 leaf vs the toy unit is unchanged, because the leaf does not move along its length
  and stays 1 cm away. Room 2 leaf vs the bookcase has 7.5 cm. The master leaf moves 3.7 cm away from the TV-wall step. The master
  bath leaf, which opens into the bath, stays clear of the towel ladder (x ≤ 5.90). The family bath leaf is outside my area: check
  it against the tub.

### A5. Medium: three-door wardrobes have no handle on the third door (all five wardrobes)
- Evidence: `b1/c_closet_handles.jpg`, `b3/c_closet_overview.jpg`, `b2/c_r2_wardrobe.jpg`, `b2/c_r1_wardrobe.jpg` and
  `b2/c_m3_wardrobe.jpg`. Each has one handle pair at the first gap and a bare third door.
- Root cause: L879 (`if (handles) for`) only places pairs, and the odd door is skipped (`i + 1 < n || n % 2 === 0`).
- Fix: after the loop on L879, add
  `if (handles && n % 2) { const x = -hx + (n - 1) * P.w / n + .025; lb(P, x - .006, x + .006, hz, hz + .02, 0.85, 1.35, mat.blackMetal); }`
  This gives the last door a single bar at its inner edge.

### A6. Medium: the mamad window seat blocks the wardrobe's west door
- The niche wardrobe (L1885 area, `place(-3.8, -2.36, -.465, .125, 's')`, 3 doors of 48 cm) opens south. Its west door, hinged at
  x -3.80, sweeps to z .605. The window seat (L1878-1881, `withShift(-.11, -.33)`) starts at world z .505 on x -3.80..-3.40, so the
  door stops at about 52 degrees. See `b2/t_mamad_open.jpg` and `b2/c_m3_wardrobe.jpg`.
- Fix: shorten the seat at its north end. On L1879, change `.835` to `.955` in both boxes (seat and drawer line). On L1880, change
  `.855` to `.975`. On L1881, move the first pillow from `1.035` to `1.15`. The seat becomes world z .625..1.365, 74 cm, and the door
  clears it by 2 cm. Moving it south instead would push the pillows into the desk return, which starts at z 1.345.

### A7. Low-medium: master bedside globe lights are 22 cm from their globes (evening)
- `b2/e_globes.jpg`: each glow sits beside its globe instead of in it. The globes are built inside `withShift(.20, .10)` (L1586),
  but the point lights are not shifted.
- Fix: L2713 `[[5.64, -.48], [7.92, -.48]]` becomes `[[5.84, -.38], [8.12, -.38]]`.

### A8. Low: small detail items
- Mamad roman blind floats 10 cm below the window head (`b2/c_m3_window.jpg`). L1883: change `1.72, 2.0` to `1.80, 2.095`.
- Closet hamper front crosses the middle door's gap line by 3 mm and sits on the face of a full-height door (`b1/c_closet_handles.jpg`).
  L1611: hamper `B(7.455, 7.865, ...)`, and add `B(7.443, 7.877, -4.395, -4.393, .525, .531, mGap, { cast: false })` so the door reads
  as ending above the drawer.
- Master slat wall: the walnut backing (L1581 `B(5.26, 8.29, ...)`) is 4 cm shorter than the last slat (slats run to 8.33 local).
  Change it to `B(5.24, 8.34, -.26, -.255, ...)`.
- Blast-door hinge side: the 4.3 cm gap between the open leaf end (z -0.195) and the frame shows a noisy white strip, the known
  "AO speckle". It is still very visible at the end of the corridor (`b1/v_corridor.jpg`, `b1/c_blast_open.jpg`). Visible hinge
  barrels fill it and read correctly for a blast door. After the blast frame (L1208-1210, `steel blast-door frame on the corridor face`) add
  `[.30, 1.00, 1.70].forEach(y => C(-2.035, -.172, y, y + .16, .02, mat.blastDoor, { seg: 16 }));` (estimate).
- Blast door: one ordinary lever, with no locking bars on the mamad face (`b1/c_m3_to_door.jpg`). Optional (estimate): pass `extra`
  to L1188, `(P, w, t) => [.55, 1.55].forEach(y => { lb(P, w - .20, w - .06, t / 2, t / 2 + .012, y - .02, y + .02, mat.steel); lb(P, w - .09, w - .07, t / 2 + .012, t / 2 + .05, y - .015, y + .015, mat.steel); })`.
  Local +z is the mamad side when closed.
- Master bed-head plates bridge the 3 cm slat gaps (`b2/c_master_ns_left.jpg`). Cosmetic. A 1 cm oak mounting strip behind each
  row, or plates centred on a slat, would fix it.

## B. Needs owner decision

### B1. High: the master TV is 1.27 m off the bed axis, and the TV point sits alone beside it
- `b1/v_master2.jpg`, `b1/e_master2.jpg`, `b2/t_master_open.jpg`: bed centre x 6.98, TV centre 5.71 (L1590, "hung toward the door
  corner"). The plan's TV point `std` at h 1.80 (L2034, x 6.93) is on the bed axis and shows as three loose plates on blank wall.
  Recheck 1 already flagged this as a design choice to confirm (`audit/recheck/electrical.md` L79). An architect will notice it.
- Proposed (inside `withShift(.20, .10)`): `B(6.175, 7.285, -3.205, -3.16, 1.20, 1.85, mat.screen, { round: .006 })`. That is a
  50" (1.11 m) TV at world x 6.375..7.485, centred on 6.93 and 5.5 cm clear of the closet opening at 7.54. Its bottom at 1.20 hides
  the `std` row (1.76-1.84) behind it. Delete `plate('s', -3.205, 5.50, 1.0, .14, .08)` on L1591, which would show under the TV, and
  update the panel note "הטלוויזיה תלויה קרוב יותר לפינה של הדלת, 52 ס״מ מהקיר".

### B2. Medium-high: the 15 cm-sill windows in rooms 1 and 2 have no fall protection, unlike the master
- The master has outside bars (L1603-1604, estimate). Rooms 1 and 2 (sill .15, one full-height sash) have nothing:
  `b1/v_room2.jpg`, `b2/c_r1_window.jpg`. d08 writes bedroom windows as "דריי קיפ, חלק תחתון קבוע או אחר" (fixed lower part or
  other) and forbids bars only on a designated escape window. Children's rooms on floor 2 with open 15 cm sills will draw a question.
- Option 1: the same bars as the master (estimate).
  Room 1: `B(-4.33, -4.29, -2.81, -1.91, 1.02, 1.06, mat.blackMetal); B(-4.33, -4.29, -2.81, -1.91, .17, .21, mat.blackMetal); [[-2.85, -2.81], [-1.91, -1.87]].forEach(([a, b]) => B(-4.33, -4.29, a, b, .15, 1.10, mat.blackMetal)); for (let z = -2.70; z < -1.96; z += .105) B(-4.32, -4.30, z - .01, z + .01, .21, 1.02, mat.blackMetal);`
  Room 2: `B(.365, 1.265, -5.44, -5.40, 1.02, 1.06, mat.blackMetal); B(.365, 1.265, -5.44, -5.40, .17, .21, mat.blackMetal); [[.325, .365], [1.265, 1.305]].forEach(([a, b]) => B(a, b, -5.44, -5.40, .15, 1.10, mat.blackMetal)); for (let x = .475; x < 1.22; x += .105) B(x - .01, x + .01, -5.43, -5.41, .21, 1.02, mat.blackMetal);`
  The posts start at .15, on the new outside sill. The master posts start at .11 and now cut into that sill, so change them to .15 as well.
- Option 2: a fixed lower pane, a transom at about 1.00 inside the frame, as d08 suggests. Say which window, if any, is the escape window.

### B3. Medium: a 4.5 cm floor-tile sliver along the whole corridor north wall
- `b3/t_corr_tiles.jpg`, `b2/c_skirt_r2door.jpg`: the default 120x120 floor (mat.tile, world UV `v = z / 2.4`, L503 and L2593)
  has joints at z = 1.2k. The corridor (z -1.245..-0.145) therefore gets a joint at -1.20, 4.5 cm off the skirting, for 6 m.
- Tested live (`b4/y_tile.jpg`, left image): `offset.y += .145 / 2.4` on `mat.tile.map`, `roughnessMap` and `bumpMap` puts the joint
  on the corridor's south face line (-0.145, also the passage threshold), and the corridor becomes one clean 110 cm row. Side
  effects: the living room's first row at the north wall becomes 105.5 cm instead of a full tile, and the mamad and kitchen rows
  shift (no new slivers below 34 cm; the mamad now has 93/120/49).
- The offset has to be applied after `photoReady` and again when `cerApply` restores the `cur` textures. The picker's spec tiles use
  their own origin `o: [2.555, 5.70]` and are not affected. It is a global floor layout choice, so it is listed here.

### B4. Low: the mamad bed-head switch ends up under the desk return
- The plan's "bed head h=65, W wall: socket 3, switch 3a" (L2006 area, `outlets('e', -3.8, 1.59, .65, 'sk')`) implies a bed along the
  window wall. The model puts the bed on the east wall, so the bed-light switch sits 3 cm under the desk top (`b2/t_mamad_open.jpg`).
  This is layout information for the owner, not a code bug.

## Checked and fine
- Door frames seat on the floor, skirting stops under every casing, and there is no casing/skirting overlap at the room 1 and 2,
  master, vestibule and closet-bath doors (`b2/c_skirt_*.jpg`, `b3/c_skirt_blastframe.jpg`). The 3 cm stubs next to the room 1/2
  casings are handled by the new `noSkirt.push` (L1144).
- Every switch is on the latch side and none sits behind an open leaf. Room 1, master vestibule (x 4.42), closet-bath (z -4.20) and
  mamad are correct, apart from the clearance items in A3.
- Door swings: room 1 leaf vs toy unit 1 cm, room 2 leaf vs bookcase 9.5 cm, master leaf vs TV-wall step and nightstand clear,
  blast door opens out into the corridor, master bath door opens into the bath clear of the ladder.
- Corridor drop 2.35 with the 80x60 return grille, grilles 80x20 over the room 1/2 doors at 2.37-2.57 clear of the 2.164 head
  casings, master split over the door at 2.24-2.52 clear of the casing, mamad 8" sleeves and the 4" relief above the bookcase.
- The master window, bars, curtain track and shutter switch, and the mamad blast window frame and sill match the construction
  plan and d08 (sliding steel plus hinged aluminium 100/100, the pocket not shown).
- Evening views in all rooms are free of blow-outs (`b1/e_grid.jpg`). Day/eve and doors open/closed views produced no page errors.
