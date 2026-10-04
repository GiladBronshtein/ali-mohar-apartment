# Visual QA, recheck 4 (2026-10-04)

All 33 views were shot in day and eve at 1440x900, desktop HQ, on a real GPU
(`--use-angle=metal`, the flags from `source/out/quick.mjs`), and every image was looked at. Close-ups and raycasts
come from `source/out/qa/vis4/probe*.mjs`, and the raycast hits are in `probe.json`. Images are in
`source/out/qa/vis4/` (`desktop_<mode>_<view>.jpg`, `probe_*.jpg`). Line numbers refer to `source/salon.html` at
92f6add. df7745d changed only the text inside line 1322, so every line number still holds.

The capture run produced no console errors.

## Checks

- `python3 roomdims.py`: every room is +0 on both axes. The only exception is closet z 485/175, the known probe
  artifact.
- `python3 clearance_audit.py`: TOTAL ISSUES: 0.

## Defects, ranked by visibility

### 1. Planar mirrors render black when the camera is far away (medium)

- **Where it shows**:
  - Entry round mirror: `inside` day and eve (black disc seen through the left balcony door,
    `desktop_day_inside.jpg` around px 600-650 / 390-440). Also `bird1` day and eve (black disc,
    `desktop_eve_bird1.jpg` around px 760-810 / 255-300).
  - Full-length mirror on the master-bath door (closet side): `bird2` day and eve (black rectangle,
    `desktop_day_bird2.jpg` around px 230-320 / 555-650).
- **Raycast**: the hit is the `Reflector` (ShaderMaterial) in both cases. Entry mirror at (1.473, 1.55, 3.60).
  Closet-door mirror at (6.58, 1.53, -3.39).
- **Diagnosis**:
  - Hiding the reflectors brings back the grey env-mapped mirror underneath (`probe_bird1_mirror_off.jpg`,
    `probe_inside_mirror_off.jpg`).
  - Glass is not the cause. Walking the camera from the balcony toward the mirror (`probe3_*.jpg`,
    `probe3_sheet.jpg`), the reflection is correct from camera x 9.0 and closer. That point is still outside the
    glass, about 7.5 m from the mirror plane. At x 10.2 (about 8.7 m) the mirror is empty.
  - From inside the flat, a camera 7.5 m away reflects correctly (`probe2_mirror_d*.jpg`).
  - So the Reflector's own render fails once the camera is more than about 8 m from the mirror plane. This is most
    likely the oblique near-plane clipping in three's Reflector. The views affected are the ones looking in from the
    balcony and from above.
- **Code**:
  - `reflector()` lines 771-776.
  - Entry mirror: `flatMirror(1.462, 1.52, 3.60, .40)` line 1233 (reflector at line 781).
  - Closet-door mirror: line 972, inside the `doorLeaf(...)` extra on line 971.
- **Suggested fix**: in the render loop, hide each reflector when the camera is farther than about 6 m from it, or
  on `top` views. The env-mapped `mat.mirror` underneath then shows, as it already does on phones.

### 2. Kitchen south backsplash stopped 63 cm short of the SW corner (medium; fixed in df7745d)

- **Where it shows**: `kitchen3` day and eve, and the close-up `probe_kitchen_sw_corner.jpg`. Bare plaster on the
  south wall between the west-wall splash and the subway run, above the corner counter (x 3.645..4.28,
  y 0.92..1.62). Raycast at px 1320/330 hits `wall` at x 4.22.
- **Code**: line 1322, `B(4.28, FX, 8.775, 8.79, .92, 1.62, mat.splash, ...)`. The counter (line 1282) and the
  west-wall splash (same line) start at 3.63/3.645.
- **Status**: commit df7745d, made by a parallel session after these shots, starts the run at 3.645. `kitchen3`
  has not been re-shot since that fix.

### 3. Family bath window reveals are plaster inside a fully tiled wall (low)

- **Where it shows**: `bath2` day and eve, and the close-up `probe_bath2_window.jpg`. The side reveals of the
  window opening, through the wall thickness, are white plaster. Tiles stop at the opening edge.
- **Code**: `windowX(2.375, 3.575, -3.775, -3.99, 1.10, 2.10)` line 1443. The tile skin with the window hole is the
  `tileZ(..., -3.775, ...)` calls on line 1440. There is no `tileX` on the two reveal faces (z -3.775..-3.99 at
  x 2.375 and x 3.575). The head is hidden by the lowered ceiling (BC = 2.10).
- In a wet room the reveal would normally be tiled. Whether it is here is not on the plans, so this is a finish
  estimate.

### 4. Speckled strip on the mamad blast-door reveal (low)

- **Where it shows**: `corridor` day and eve, at the far end left of the dark door (px 645-660 / 360-590). Also
  the close-up `probe_corridor_strip.jpg`, where it is a noisy light line 1-2 px wide.
- **Raycast**: the hit is `blastDoor` at x -1.955, z -0.11, the face of the reveal jamb. The wall at x -1.98 sits
  2.5 cm behind it.
- **Code**: line 992, `B(-1.98, -1.955, -.145, .125, 0, 2.0, mat.blastDoor, ...)`.
- **Likely cause**: AO noise or aliasing in the narrow slot between the jamb, the open leaf (line 970) and the
  frame (line 991). No coplanar face was found, so this is probably not z-fighting.

### 5. Faint light seam across the middle of each wall-tile row (low, close range only)

- **Where it shows**: master shower close-up (`probe_shower_crop.jpg`). A thin light line runs through each 30 cm
  row, between the real dark grout lines. At normal view distance it is barely visible.
- **Code**: the ceramic texture comes from `cerTex()` line 2659 and is applied by `cerApply()` line 2764. The
  likely cause is the bump/relief at a texture edge rather than geometry.
- The grout lines do meet correctly at the back-wall/side-wall corner.

### 6. Eve lighting hotspots (low)

- `kitchen` eve: a blown-out ceiling patch above the island pendant, at the top of the frame around px 830-900.
- `hall` eve: a bright wall hotspot at the top left.
- Both look like grazing spots or uplight close to a surface. Lighting levels are estimates in any case.

### 7. Dimension labels collide on the top view (low)

- `top` day and eve. "17x" is hidden under the closet label. "385" and "05" overlap the kitchen label near
  px 830-890 / 710-725. "262" and "277" touch.

### 8. Refrigerant pair stands on the condenser top (cosmetic)

- `service` day and eve. The two black lines rise straight out of the condenser lid. On a real unit they connect
  to service valves on the side.
- Line 1543, `C(2.92, -4.30, .98, 2.35, ...)` and `C(2.85, ...)` inside `withShift(.22, -.45)`.

## Checked and not defects

- **Plates at 1.80 m** in room 1, master (`master2`) and the mamad are the TV/data outlets from the electrical
  plan. See lines 1743, 1746, 1748 and 1772.
- **White box at the top right of `bath`** is the shaker cabinet above the washer. The raycast hits paint
  `#f0ede5` at y 1.90.
- **Bird views**: ceiling fans and pendants hang in the air because the ceiling is hidden. This is expected.
- **Room 3 eve**: the round black disc near the ceiling is a fixture, and it is placed sensibly.

## Clean views (no defect found)

- **Day**: entry, photo, storage, island, hall, kitchen, kitchen2, tvwall, balcony, balcony2, view, master,
  master2, closet, mbath, shower, bath, service, room1, room2, room3, sofa, isle2, bedtv, desk, corr2.
- **Eve**: entry, photo, storage, island, tvwall, balcony, balcony2, view, master, master2, closet, mbath, shower,
  bath, service, room1, room2, room3, sofa, isle2, bedtv, desk, corr2. The closet room reads dark in eve, which is
  plausible.

No wall gaps, light leaks, walls poking through, floating tiles, tiles crossing openings or missing textures were
found in any view. The 80x80 floor tiles read at the right scale in every room where they are laid.
