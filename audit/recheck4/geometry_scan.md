# Geometry integrity scan (recheck 4)

Report only. Nothing in the repo was changed except the new scan files under `source/out/geo4/` and this report.
Line numbers refer to `source/salon.html` as of commit df7745d (2026-10-04 18:54).

## Method

- Playwright with Chromium on Metal (`--use-angle=metal --ignore-gpu-blocklist --enable-gpu`) against the built site at
  http://127.0.0.1:8791/.
- After load, every visible static mesh was packed into one opaque BVH (291,918 triangles) and one transparent BVH
  (688 triangles, glass and sheers), using three-mesh-bvh from the importmap. The groups were root, ceilGroup, doors,
  curtains and fans; the outside environment was excluded.
- Rays are double sided. A back-face hit means the ray origin is inside a solid.
- Scripts: `source/out/geo4/geo_page.js` (checks), `scan.mjs` (runner), `probe.mjs` (window bay probe). Raw output sits
  next to them as `*.json`.
- Page errors: 0 during load and 0 during the checks (`errors.json`).
- Timing: the tile and floor passes ran on the build just before df7745d. Leaks, coplanar, ceramics and the probe ran on
  df7745d. df7745d only changed the kitchen splash (see 1d).

## Summary

| # | Finding | Where (world, m) | Materials | Line | Verdict |
|---|---|---|---|---|---|
| 1 | Master bath niche back panel buried behind the tile | x 4.91..5.41, z -5.004..-4.998, y 1.05..1.40 | nicheBack behind sage | 1412 (in withShift(.19) at 1404) | real |
| 2 | Family bath washer niche untiled | N wall x 3.69..3.835 at z -3.775; E wall x 4.46 at z -3.775..-3.735 and -3.125..-3.09; y 0..1.80 | wall where bathWall2 is expected | 1439, 1440 (stub 894) | real |
| 3 | Master bath N wall plaster strip beside the window | x 5.99..6.015, z -4.98, y 0..2.60 (visible from about 1.10 up) | wall between bathWall and the reveal | 1397 | real |
| 4 | windowZ leaves an unglazed 2.5 cm slot at each end of the sash | room 1 (z -2.785..-2.76, -1.96..-1.935), mamad (z .505..530, 1.430..1.455), master E (z -2.145..-2.12, -1.32..-1.295), full glass height | frame / glass | 836-837 (calls 1382, 1572, 1647) | real |
| 5 | Mamad sill buried in the wall; z-fights with the wall top and face | x -3.85..-3.80, z .45..1.51, y 1.07..1.10 | sill / wall | 1647 (xIn -3.83, wall face -3.80 at 872) | real, cosmetic |
| 6 | Room 1 floor stops 2.5 cm short of the north wall | x -3.89..-1.15, z -5.023..-5.01 (after the skirting) | tile (y 0) shows instead of planks | 848 | real, minor |
| 7 | Balcony north wall end face z-fights | x 9.30, z -0.13..0, y 0..2.60 | concrete / wall | 1656 vs 886 | real, minor |
| 8 | Sill top coplanar with the wall top under every sill (2 cm embed) | room 2 z -5.03..-5.01 y .15; master bath z -5.00..-4.98 y 1.25; family bath y 1.10 | sill / wall, sill / tile edge | 826, 838 | tolerable, cosmetic |
| 9 | Hob texture plane 0.2 mm over the glass | x 6.255..6.844, z 8.245..8.735, y .926 | hob map plane / screen | 1298, 1305 | depth margin, see 4.3 |
| 10 | TV slab texture plane 0.5 mm in front of its box | x 4.02..5.98, z .09, y .705..2.16 | slab map plane / whiteFront | 1124, 1125 | depth margin, see 4.3 |
| (d) | Kitchen backsplash corner bare | z 8.79, x 3.645..4.28, y .92..1.62 | wall | 1322 | real, already fixed in df7745d |

The scan found no tile standing off a wall, no floor or ceiling holes, no floor z-fighting, and no wall that fails to
reach the floor or the ceiling. All 530 ceramic options apply correctly. roomdims is +0 everywhere (closet artifact
only) and clearance_audit reports 0 issues.

## 1. Tile skins vs walls

The scan covers the wet walls: master bath x 4.63..6.85, z -4.98..-3.26 (bathWall, sage); family bath x 2.01..4.46,
z -3.775..-1.395 (bathWall2); kitchen splash on the S wall (z 8.79) and W wall (x 3.63) between y .94 and 1.6. Sampling
is every 1 cm along each wall at several heights, looking at the wall from 30 cm inside the room.

- **20,254 samples:**

  | Category | Samples | What it means |
  |---|---|---|
  | tile | 13,868 | |
  | tile-object | 961 | Something stands in front of the tile |
  | other | 2,069 | Furniture or fixtures |
  | nohit / reveal | 1,739 | Windows and doors |
  | plaster-hidden | 837 | Behind the washer, the cabinet or the stub |
  | plaster | 776 | |
  | tile-in-opening | 4 | |

- **Standoff and backing pass.** Every tile hit sits flush on its wall: gap 0 in all 13,868 samples. Thickness is 6 mm
  (15 mm for the splash). There is no tile without a wall behind it.
- **Tile crossing an opening passes.** The 4 tile-in-opening samples are at a = 6.615 in the master bath, the jamb line
  itself. That is a sampling-boundary artifact, not a tile over the window.
- **Plaster winning over tile.** All 776 plaster samples fall into the four clusters below:
  - **1a. Master bath niche (line 1412).**
    - `B(4.72, 5.22, -5.004, -4.998, 1.05, 1.40, mat.nicheBack)` is shifted by .19, so it lands at world x 4.91..5.41.
      It sits inside the wall, behind the sage face at z -4.974.
    - Rays hit sage there, so the shower shows only the ledge and no niche. This one shows as tile, not plaster.
    - The family bath niche (line 1501, x 4.448..4.454) sits on its tile face and is correct. For the same result here,
      the master panel would need z -4.974..-4.968.
  - **1b. Family bath washer niche (lines 1439, 1440).**
    - `tileZ(3.575, 3.69, -3.775, ...)` stops at x 3.69.
    - `tileX(-3.775, -3.09, 4.46, -1, 1.80, H)` only starts at y 1.80.
    - The stub wall W(3.69, 4.46, -3.09, -2.98) (line 894) has no tile on its north face.
    - Plaster is visible on the N wall at x 3.69..3.835 (y 0 to about 1.72), with slivers at x 4.445..4.455. It is also
      visible on the E wall in the 4 cm strips beside the washer/dryer stack (z -3.775..-3.735 and -3.125..-3.09), and
      in the band between the stack top (about 1.72) and the cabinet bottom (LB 1.76, line 1478).
    - The rest of the niche is hidden behind the stack (x 3.84..4.44 after the shift).
    - In practice a wet niche is tiled. Read as a modelling gap.
  - **1c. Master bath N wall (line 1397).**
    - `tileZ(5.60, 5.99, -4.98, ...)` ends 2.5 cm short of the window jamb at x 6.015, so a 2.5 cm plaster strip runs
      the full height.
    - The cistern ledge hides it below y 1.08; it is visible above that.
  - **1d. Kitchen splash corner.** About 64 x 70 cm of plaster at x 3.645..4.28, z 8.79. Fixed in df7745d (line 1322 now
    starts at 3.645).
- **Tolerable artifacts.**
  - Plaster in the window and door reveals (nohit/reveal) is expected.
  - plaster-hidden counts origins inside furniture, so the wall behind is never seen. Two cases fall outside that flag:
    inside the laundry cabinet above y 1.76, and inside the stub at z -3.09..-2.98. Both were checked by hand and are
    hidden.

## 2. Floors and ceilings

Downward rays on a 10 cm grid over 18 floor rectangles, and upward rays on a 20 cm grid for the ceilings.

- **13,537 floor samples:**

  | Result | Samples |
  |---|---|
  | Expected material | 11,781 |
  | Covered by a rug or mat as designed | 1,726 |
  | Wrong material | 30 |

- **Holes: 0. Z-fighting within 2 mm: 0 candidates** across all rectangles.
- **Ceilings pass.** 2,845 samples with 0 holes:

  | Area | Height |
  |---|---|
  | Most rooms | 2.600 |
  | Corridor and passage | 2.250 (DROP) |
  | Family bath | 2.100 (BC) |

- **2a. Room 1 strip (real, minor; 28 of the 30 wrong samples).**
  - `floor(-3.90, -1.14, -5.01, -1.45, mat.planks)` (line 848) starts at z -5.01. The room 1 north wall face is at
    -5.035 (roomdims: room A z 361).
  - After the 1.2 cm skirting, a 1.3 cm strip of the base porcelain (`tile`, y 0, 9 mm below the planks) shows along
    x -3.89..-1.15.
  - Room 2 is correct because its wall face is at -5.01.
- **Balcony (tolerable; the other 2 wrong samples).** At (8.92, 1.66) and (8.92, 7.36), blackMetal sits at y -0.037,
  3 mm above the deck (door track).
- **Laundry niche.** The `service` floor sits 3 mm over the base tile. This comes from reading the code; the niche was
  outside the floor grid. It can only be seen through the louvres, so it is tolerable.

## 3. Leaks between walls

- **Setup.** Room-grid origins at heights .012, .05, 1.2, min(2.5, ceiling - .06) and ceiling - .01. Each origin casts
  7,200 horizontal rays (0.05 degree step).
  - **Escape:** a ray leaves the apartment envelope before its first opaque hit without crossing glass.
  - **Slit:** a ray travels more than 0.2 m further than both neighbours while the two neighbours agree with each other.
- **Volume.** 2,448,000 rays from 340 origin-height pairs. 90 pairs were skipped because the origin was inside furniture.
- **Escapes through walls: 0. Walls reach the floor (y .012) and the ceiling (ceiling - .01) everywhere: pass.**
- **Rays out through a known opening without glass: 72** (mamad 57, master 15). The bay probe (`probe.json`) traced the
  cause:
  - **3a. windowZ end bays (real; lines 836-837).**
    - The end stiles are `Math.max(z1, z - f/2)..Math.min(z2, z + f/2)`, so only 2.5 cm wide.
    - The glass runs from `z1 + f` to `z2 - f`, which leaves a 2.5 cm slot with no glass at each end, for the full
      sash height.
    - Probe results:
      - Mamad, z .5175, y 1.3: no opaque hit and no glass, so the slot sees straight outside.
      - Master, z -2.1325 and -1.3075: only the sheer is hit.
      - Room 1: covered by the drawn curtain.
    - windowX does not have this (its stiles are the full f), and the probes there hit the frame.
    - Affected calls: 1382 (master E), 1572 (room 1), 1647 (mamad).
- **Slits: 20, none of them in walls:**
  - 16 are at y 1.2, through the open weave of the balcony egg chair (anon#8e9091 rattan, around (9.26..10.0, 1.2,
    7.4..7.7), line 1687). This is by design, and the rays had already crossed the balcony glass.
  - 4 are at y 2.5, between parts of a black ceiling fitting at about (5.90, 2.5, 6.66). Object geometry, harmless.

## 4. Coplanar overlaps of different materials

- **Method.**
  - Axis-aligned triangles are binned at 0.6 mm with the same facing, and overlaps are clipped (minimum area 0.2 cm2).
  - The scan found 1,105 pairs in 120 material groups.
  - An overlap counts as visible only if a point 5 cm in front of it is free space inside the flat (no back face in any
    of the 6 axis directions) and the face is the first thing hit from there.
  - **18 groups survive, 2.5 m2 in total;** most of the area is in items 4.1 and 4.3.
  - The rest are hidden pairs: cap/ceil, rug bottoms at y 0, cabinet backs against tile, tile above the family bath
    ceiling.
- **4.1 Balcony north wall end (real, minor; 2,324 cm2 visible).**
  - `B(BX1, BN, BZN, BZ1, BY, 2.70, mat.concrete)` (line 1656) and `W(4.15, 9.30, -0.145, 0)` (line 886) overlap in
    volume.
  - Their +x faces coincide at x 9.30 over z -0.13..0, y 0..2.60, so concrete and plaster fight on the end face seen
    from the balcony.
  - A 1.5 cm sliver of the wall (z -0.145..-0.13) also shows there.
- **4.2 Sills (lines 826, 838, 1647).**
  - The window helpers put the sill box 2 cm into the wall, with its top at `sill`. That is exactly the height of the
    wall under the window, so the two tops are coplanar over the embed. Visible:

    | Window | Visible area |
    |---|---|
    | Room 2 (y .15) | 427 cm2 |
    | Master bath (y 1.25) | 120 cm2 |
    | Family bath tile edge (y 1.10) | 72 cm2 |
    | Master bath tile edge | 36 cm2 |

    Both materials are off-white, so this is tolerable.
  - **The mamad is worse (real, cosmetic).** It passes xIn -3.83 while its wall face is at -3.80 (line 872). The whole
    sill (x -3.85..-3.80) is inside the wall, and its top (740 cm2) and its front face at x -3.80 (300 cm2) both
    z-fight with the wall. No sill reads at all.
- **4.3 Thin offsets (depth margin, not seen at eye level).**
  - Two planes sit very close to the surface behind them:

    | Item | Plane | Surface behind | Gap |
    |---|---|---|---|
    | Hob | Texture plane at y .9262 (line 1305) | Glass box top at .926 (line 1298) | 0.2 mm |
    | TV slab | matSlab plane at z .0905 (line 1125) | whiteFront box face at .09 (line 1124) | 0.5 mm |

  - With near 0.06 and a 24-bit depth buffer, the depth step reaches 0.2 mm at about 14 m and 0.5 mm at about 22 m.
  - Every eye-level view is closer than that, so neither can flicker there.
  - The whole-flat `top` view (camera at y 22) is about 21 m from the hob, so the hob can shimmer while that camera
    moves. This was not confirmed in a render, and still frames are accumulated.
  - The TV slab is edge-on from above.
- **Negligible:**
  - charcoal/matteBlack at x 0 (robot garage side, line 1203; 97 cm2, both near black)
  - blastDoor/wall in the mamad window reveal (5 mm strips, line 1648; about 50 cm2 each)
  - black/fluteGrey at z .36 (31 cm2)
  - screen/steel at the hob edge (0.2 cm2)
  - black/matteBlack at x 4.294 (1.2 cm2)

## 5. Ceramics

Every option of every CER_SPACES picker was set with `cerSet`. 539 results: 530 tile options plus the 9 `cur` rows.

- **Errors pass.** 0 exceptions and 0 page errors.
- **Map pass.** All 530 options have a map, it is the ceramic texture (`mapIsCer`), and the map, roughness and bump
  textures agree (`mapsAgree`).
- **Repeat pass.** For all 530 options the repeat matches the tile size to 1 mm: tileU = uv / repeat.x / nx equals w,
  and tileV equals h. Examples:
  - floor f80: uv 2.4, repeat 1.5, 0.80 m
  - bathF w1560: uv .8, repeat .889 / .444, 0.15 x 0.60 m
  - kitB k1030: uv 1.6, repeat 1.333 / 2.0, 0.30 x 0.10 m
- **Size labels.** The only mismatches my check flagged are the 81 w30 rows. Their label reads "30×30 / 33×33" (the
  catalog states both) and the model uses 0.33. This is a parsing artifact of the check, not a defect.
- **Reset pass.** After `cerReset()`, all 9 spaces equal their defaults.
- **Note (tolerable).** `worldUV` maps u = z on x-facing walls. The `cerApply` offset (line 2774) uses the x origin
  `o[0]`. On the x-facing bath walls (x 2.01, 4.46, 4.63, 6.85), the vertical joints therefore start at an arbitrary
  phase instead of from a corner. Horizontal joints start at the floor as intended (v0 = 0).

## 6. Scripts

- `python3 roomdims.py`: every room +0. The closet z 485/175 is the known probe artifact.
- `python3 clearance_audit.py`: TOTAL ISSUES 0.
