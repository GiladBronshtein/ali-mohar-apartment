# QA baseline (2026-10-04)

The state of the walkthrough before the realism work. Captured with `source/out/qa_full.mjs` against the local
site (`http://localhost:8000/`), headless Chromium on the real GPU (`--use-angle=metal`, Apple M4), pixel ratio 1.
Shots and contact sheets: `source/out/qa/baseline/` (gitignored).

## Coverage

- Desktop 1440×900, HQ composer: all 33 views, in both day and eve.
- Phone 390×844 at DSF 2, no composer: entry, kitchen, master, bath, balcony and bird2, in both day and eve.
- 0 page errors, 0 console errors or warnings, 0 HTTP errors on both.

## Performance

| | Ready | FPS (forced render) | Meshes | Scene tris | Materials | Textures | Draw calls / frame tris | JS heap |
|---|---|---|---|---|---|---|---|---|
| Desktop HQ | 2.2 s (10.9 s cold) | 18 to 21 | 786 | 146k | 664 | 93 | n/a (composer) | 81 MB |
| Phone | 1.9 s (4.5 s cold) | 40 to 46 | 786 | 146k | 664 | 93 | 462 / 112k | 97 MB |

- **664 unique materials** for 786 meshes. Because `mergeGroup` merges by material, it barely reduces draw calls.
  Most of these are per-call `M(...)` instances with identical parameters.
- **Desktop HQ costs a lot:** GTAO, TAA and bloom on top of 8 RectAreaLights, 11 point lights and a 4096 shadow map
  give about 20 fps on an M4. That is acceptable only because rendering is on demand and TAA idles once still.
- The geometry budget is small (146k tris). There is room for better furniture meshes.

## Visual findings

Ranked by how much they hurt realism.

1. **Day lighting is flat and grey.** Exposure is 0.70 to stop white walls glaring, so whites read as mid-grey.
   - There is little light falloff from the windows and no visible bounce colour.
   - Corners and contact points have weak shadowing, even with GTAO.
   - Rooms look overcast rather than sunlit (entry, hall, storage, bedrooms, corridor).
   - Eve mode reads warmer and more convincing than day.
2. **The exterior is the weakest part.**
   - Buildings are boxes with a repeating window texture. Trees are lollipop spheres and cars are boxes.
   - The ground is flat orange dirt, and the sky is a gradient with painted clouds.
   - It dominates balcony, balcony2, view, island, isle2, bird1 and bird2.
   - Close facades seen through windows look like flat posters (room2, room3, shower, bath, service).
3. **Materials have no real PBR detail.** Every texture is a canvas pattern with bump derived from luminance.
   - Floors look painted: tiles barely reflect, and oak has no grain depth.
   - Fabrics have no sheen and stone has no veining depth.
   - Most surfaces share the same roughness response.
4. **Mirrors and glass do not reflect.** Mirrors show the blurred env map (flat grey). Shower glass and window glass
   have no reflection of the room.
5. **Furniture is primitive.**
   - Sofas and the bed are rounded boxes with no cushion seams.
   - Toilets and basins are blobs, and plants are low-poly spheres or cards.
   - Curtains are sine-displaced planes.
   - The kitchen, the TV wall and the bedroom slat wall hold up best.
6. **Ceiling hotspots in eve mode.** Downlights plus bloom blow out round patches (entry, photo, corridor,
   phone entry).
7. **Kids' bath ceiling is dark grey in eve mode.** The lowered ceiling sits under the AC unit and gets almost no
   light.
8. **Lens distortion.**
   - fov 68 stretches frame edges (storage, hall, closet, mbath).
   - Phone portrait at fov 96 is worse: bird2 is unreadable on a phone.
9. **Bird views:** the exterior shell is an untextured dark grey, and the surrounding blocks are blank boxes.
10. **Phone runs without post-processing.** There is no AO and no anti-aliasing beyond MSAA, so the phone shots
    look noticeably flatter than desktop.

## What already works

- The layout, proportions and composition match the plans (roomdims +0, clearance 0 issues).
- The kitchen, TV wall, master bedroom slat wall and room 1 read well.
- On-demand rendering and the phone fallback keep it usable.
- It is fully procedural and dependency-light, so it can still be published as a claude.ai artifact.

## Implications for the realism work

- The largest gain per effort is lighting and tone:
  - A neutral exposure with AgX or Neutral tone mapping instead of ACES at 0.70.
  - A real HDRI for environment light and window views.
  - Stronger contact AO.
  - Possibly a baked or path-traced still mode, using the M4 GPU instead of the old 2-core sandbox.
- The next largest gains:
  - Real PBR texture sets (CC0) on floors, stone, wood and fabric.
  - Better furniture meshes (CC0 glTF) for sofas, sanitaryware and plants.
- Exterior: replace it with an HDRI backplate plus simpler massing, rather than trying to model the city.
- Any external asset breaks the "single file, no assets" artifact property. Decide between keeping the artifact
  procedural and letting the site diverge, or dropping artifact parity.
- Budget: GitHub Pages has no hard per-file limit below 100 MB, but phones need about 10 MB or less on first load.
  Assets should be KTX2 or WebP at 1k, with 2k only for floors.
