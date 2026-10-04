# Interior realism audit 5 (2026-10-04)

Report only. Nothing in `source/salon.html` or any committed file was changed. Line numbers refer to `source/salon.html`
at commit 16abbec unless another file is named.

Shots (desktop 1440x900, HQ path: TAA still, GTAO, bloom, mirrors), 25 interior views, day and eve:
`source/out/real5/interior/shots/desktop_{day,eve}_<view>.jpg`. Contact sheets: `source/out/real5/interior/sheets/`.
Baked-light experiment: `source/out/real5/interior/exp/` (script `exp.mjs`). Phone shots were not taken (the machine was loaded);
phone scores below are estimates from the code path (no composer, no AO, no TAA, no mirrors).

## 1. Rubric (anchored)

Each view is scored on five areas, 0 to 10, with the anchors below. The view score is the weighted mean.

| Area (weight) | 3-4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| Lighting / GI (35%) | flat, no direction, light leaks obvious | uniform fill, some direction from windows, no bounce colour | competent three.js: key + fill, shadows from sun only | window-to-depth falloff, ceilings graded, contact darkening | soft bounce, colour bleed, correct night/day balance | reads as a photo at a glance |
| Materials (25%) | plastic or flat colour | textured but uniform gloss | roughness variation on main surfaces | believable wood, stone, tile; fabrics read soft | lacquer, metal, leather, glass each distinct | indistinguishable from photo materials |
| Geometry detail (15%) | blocky boxes, hard 90 deg edges | boxes with some trims | rounded edges on key furniture, proper fixtures | bevels catch highlights, sanitaryware shaped | small hardware, seams, gaps | no geometric giveaway |
| Props / clutter (10%) | empty showroom | a few generic props | props in main rooms | lived-in in every room | curated, scale-correct props | magazine styling |
| Post / camera (15%) | aliasing, banding, blown or muddy | correct exposure, no grading | AA clean, mild bloom | exposure matches interior photo practice (windows hotter than room) | grading, vignette, dither, no AO artefacts | lens and grade like a real photo |

Anchor for the whole view: 6 = competent three.js scene, 7 = one noticeable flaw, 8 = polished with minor nits,
9 = cannot tell from a photo at a glance.

## 2. Scores

Area means across the 25 views (desktop):

| | Lighting | Materials | Geometry | Props | Post | Weighted |
|---|---|---|---|---|---|---|
| Day | 4.5 | 5.5 | 6 | 5 | 5 | 5.1 |
| Eve | 6 | 5.5 | 6 | 5 | 6 | 5.8 |

Phone estimate: about 0.5 to 1 lower in both modes (no AO, no contact darkening anywhere, no mirror reflections, aliased edges).

Per view (desktop, overall score, main flaw):

| View | Day | Eve | Main flaw |
|---|---|---|---|
| entry | 5 | 6 | day: floor tile reads as cloudy concrete, uniform ceiling |
| photo | 5 | 6 | day: no falloff from the balcony glazing into the room |
| storage | 5 | 6.5 | flat fronts, no shadow line under shelves |
| island | 5.5 | 6 | eve: island hotspot; day: quartz shows no reflection |
| hall | 4.5 | 6 | day: flat grey, walls and ceiling same value |
| kitchen | 5 | 6 | no shadow band under wall cabinets on the backsplash |
| kitchen2 | 5 | 6 | fronts flat, steel reads as grey plastic |
| kitchen3 | 5 | 6 | countertop and floor reflect nothing from the windows |
| tvwall | 5 | 6.5 | sofa leather plastic, no contact shadow under the sofa |
| master | 6 | 6.5 | best room (oak slat wall photo); bed floats, no contact shadow |
| master2 | 4.5 | 5.5 | bedside globes glow but light nothing |
| closet | 5 | 5.5 | flat lighting, fronts uniform |
| mbath | 5 | 5.5 | GTAO speckled halo along the right wall |
| shower | 5.5 | 5.5 | glass reads as a flat tint, no reflection |
| bath | 5 | 5.5 | sanitaryware blocky, ceramic over-glossy without shape |
| bath2 | 4.5 | 5 | eve: ceiling blown near the lamp; day: AO grain top-left |
| room1 | 4.5 | 6 | day: no falloff, empty, no grounding under bed |
| room2 | 4.5 | 5.5 | AO halo around art frames; window wall as bright as the far wall |
| room3 | 4 | 5 | near-empty, flat |
| corridor | 4.5 | 5.5 | uniform grey ceiling and walls |
| sofa | 5 | 6 | sheers read as striped tubes |
| isle2 | 5.5 | 6 | fruit bowl plastic |
| bedtv | 6 | 6.5 | ok; fabrics without sheen |
| desk | 4 | 5 | empty desk, flat light |
| corr2 | 5 | 6 | eve: ceiling dark grey; AO halo around art |

Means: day 4.9, eve 5.8. What holds the scores down, in order: (1) uniform fill light (RoomEnvironment plus hemisphere) with
no window-to-depth falloff, (2) nothing touches the floor (no contact shadows, none at all on phones), (3) gloss is uniform
and no surface reflects the real room or the windows, (4) windows are not brighter than the room by day.

## 3. Findings on the current light paths

Day fill (lines 271-274, 2062-2085):
- `scene.environment` is a PMREM of the stock `RoomEnvironment` (a generic grey studio box lit from above, line 274).
- Every material samples it at `envMapIntensity` .3 (`ENV`, line 2062), on top of `HemisphereLight` .22 (line 2063).
- This fill is the same in every room and every position, which gives the uniform "SketchUp" value.
- Reflections in the quartz, the floor tile, the fronts and the mirror fallback show that studio box, not the apartment or its windows.

Window lights (lines 2070-2082):
- Eight `RectAreaLight`s. These have no shadows, so each one lights through walls into the neighbouring rooms (visible in
  `desktop_day_hall.jpg` and `desktop_day_corridor.jpg` as even light with no source).
- The forward shader evaluates all eight for every lit fragment, even when the light is behind a wall.

Eve lights (lines 2083-2085, 2330-2344):
- Eleven `PointLight`s, no shadows, `distance` 6, `decay` 2.
- Lights at intensity 0 are still evaluated by the shader, so the day mode pays for them too.
- Bedside globes at line 1366 (5.64/7.92, -.48, y 1.05) have no light near them. The nearest point is (6.8, -1.5) at the ceiling.
- The kids' bath point (3.2, -2.6) sits 30 cm under the lowered ceiling `BC` with k 2, which blows the ceiling (`desktop_eve_bath2.jpg`).

AO:
- GTAO (lines 288-295) is desktop only.
- With radius .3, 16 samples and a 2-ring Poisson denoise, it leaves grain and hairy halos at depth edges:
  - `desktop_day_bath2.jpg` top left
  - `desktop_day_mbath.jpg` right wall
  - the art frames in `desktop_day_room2.jpg` and `desktop_day_corr2.jpg`
- TAA accumulation (line 2471) does not average this away, because the GTAO noise pattern is fixed per pixel.

Exposure:
- ACES at .85 by day (line 255).
- The sky is a `MeshBasicMaterial` with colour scale 1 (lines 2016-2022) and is tone mapped, so it lands around mid grey.
- By day the view through the glazing is no brighter than the interior. A real interior photo at this exposure shows the windows hot.

Baked lightmaps (`?baked=1`, lines 2095-2160; `source/lm/`). Experiment shots: `exp/baked_g1_*.jpg` (gain 1) and
`exp/baked_gpi_*.jpg` (gain pi), sheet `sheets/baked.jpg`.
- The bake is stale: 91 of 154 targets matched, 63 missed. Missed meshes keep real-time light and render white next to baked
  neighbours, so the picture is patchy.
- Baked floors and ceilings are close to black even at gain pi (`exp/baked_gpi_entry.jpg`, `exp/baked_gpi_kitchen3.jpg`). Art,
  headboard and some fabrics go black.
- Scale bug:
  - Cycles `DIFFUSE` with `pass_filter={'DIRECT','INDIRECT'}` and no `COLOR` (`lm/bake.py` line 366) stores the light
    term, which is irradiance / pi.
  - The patched shader feeds it in as irradiance: `iblIrradiance += baked`, and three's `RE_IndirectSpecular_Physical`
    then multiplies by `RECIPROCAL_PI` again.
  - So the bake reads pi too dark before anything else.
- On top of that:
  - The bake sky is weak: `SKY_STRENGTH = .35` (line 303), with a sky radiance of about .6 to .9 before strength.
  - The ground below the horizon is near black: `gnd = [.30,.29,.27] * .35` (line 281).
  - So the indirect term from the balcony opening is a fraction of what the viewer's hemisphere plus env gives.
- Encoding:
  - Lightmaps are 8-bit sRGB WebP scaled to a 99.95 percentile range (`lm/publish.py`).
  - `lamps` has range 22.6, so the dim evening bounce is quantised into a few codes. That produces banding and
    blotches together with no denoising (`bake.py` line 30, `use_denoising=False`).
- One 2048 atlas for 154 targets at texel .03 is too coarse for contact shadows under furniture.

## 4. Ranked improvements (realism gain per cost)

Costs:
- Desktop is the HQ composer path, currently forced at about 20 fps.
- Phone is the direct `renderer.render` path, currently about 37 fps.
- "Download" counts against the about 12 MB desktop budget.

Gains are on the view score, averaged over the 25 views. They are estimates.

### 1. Contact shadow decals and the under-cabinet shadow band
- Looks fake now:
  - Everything floats.
  - Nothing under the sofa (`desktop_day_tvwall.jpg`), beds (`desktop_day_master.jpg`, `desktop_day_room1.jpg`), stools
    (`desktop_day_island.jpg`), toilets and vanities (`desktop_day_bath.jpg`), the desk (`desktop_day_desk.jpg`).
  - The backsplash under the wall cabinets is evenly lit (`desktop_day_kitchen.jpg`).
  - On phones there is no AO at all, so this is the only grounding they would get.
- Change:
  - Add `contactShadow(x1,x2,z1,z2,soft=.12,k=.55)` next to the geometry helpers (around line 741).
  - It writes a quad 2 mm above the floor (y .002) with UVs 0..1.
  - All quads share one 128x128 canvas texture: a rounded-rect alpha falloff (alpha k in the middle, 0 at `soft` beyond the footprint).
  - Material: `MeshBasicMaterial({ map, color:0x000000, transparent:true, opacity:1, depthWrite:false, polygonOffset:true, polygonOffsetFactor:-2 })`.
    Use the alpha from the map, `toneMapped:false`, `fog:false`.
  - Merge all quads into one mesh (one draw call) and push it to `noAO` so GTAO does not see it.
  - Call it beside every furniture builder:
    - sofa footprint (line 1147ff)
    - beds, island stools, coffee table, TV unit, desk, dining chairs
    - toilets and vanities
    - kitchen base run (a 4 cm band at the toe kick)
  - Backsplash: a vertical quad on the splash face, from the cabinet bottom down 18 cm, with a linear gradient alpha
    .35 to 0. One per wall-cabinet run.
  - Optional, more realistic: an LED strip under the wall cabinets (an emissive `mat.led` bar plus one `RectAreaLight`
    at eve, within the budget of item 4).
- Cost:
  - Desktop: one draw call, negligible.
  - Phone: one draw call plus overdraw on about 15 small quads, under 1 fps.
  - Download: 0 (canvas).
- Risk: low. Decals must be placed under moving or picker-swapped items, and the ceramics picker does not move
  furniture. Wrong-sized decals look worse than none, so size them from the same coordinates as the furniture.
- Gain: +0.4 desktop, +0.7 phone.

### 2. Daylight dynamic range: hot windows, dither, vignette
- Looks fake now:
  - The exterior through the balcony glazing is the same value as the room (`desktop_day_photo.jpg`,
    `desktop_day_sofa.jpg`, `desktop_day_kitchen3.jpg`).
  - Ceilings show 8-bit banding at low gradients on phones (expected, not shot).
  - There is no vignette, so the frame reads as a viewport.
- Change:
  - Line 2022: day sky `k: 1` to `k: 2.2` (eve stays .35).
  - Set the glass (line 508) to `opacity: .08`, `envMapIntensity: 1`, `metalness: 0`, `roughness: 0`.
    This keeps a Fresnel reflection without greying the view (see item 3 for what it reflects).
    Coordinate the sky and facade brightness with the exterior audit (`audit/realism5/exterior.md`), which owns the outside.
  - Dither: set `dithering = true` on `mat.wall`, `mat.ceil`, `mat.limewash` and the fabric materials in the `mat` table
    (lines 502-533). This is free in the shader.
  - Vignette:
    - Phone: a CSS overlay on `#stage`, `background: radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,.18) 100%)`,
      `pointer-events:none`. This costs 0 GPU.
    - Desktop: the same overlay, or the grading pass in item 13.
- Cost:
  - Desktop: 0.
  - Phone: 0.
  - Download: 0.
- Risk: low. A brighter sky raises bloom on the window edges by day. Bloom threshold .95 (line 296) and strength .1
  keep it subtle; check `desktop_day_photo` after the change.
- Gain: +0.3 day.

### 3. Room-local environment and irradiance (replace RoomEnvironment and flatten the hemisphere)
- Looks fake now:
  - The uniform fill and the studio-box reflections (section 3). Quartz, the tile floor, lacquer and steel reflect a grey
    box instead of the windows (`desktop_day_kitchen3.jpg`, `desktop_day_island.jpg`).
  - Ceilings are one value from window to back wall (`desktop_day_hall.jpg`, `desktop_day_corridor.jpg`).
  - At eve the windows do not mirror the lit room, which is the strongest night cue in a real apartment
    (`desktop_eve_sofa.jpg`).
- Change:
  - After the scene and the photo sets are ready (`photoReady`, line 580), capture one `CubeCamera` per zone:
    - living/kitchen
    - master
    - master bath
    - family bath
    - rooms 1, 2 and 3
    - mamad
    - corridor/entry
  - Use a 128 px `WebGLCubeRenderTarget` at HalfFloat, camera at 1.5 m in the room centre, with the sky visible.
  - Capture once per mode (day and eve), lazily for the zone the camera enters.
  - Run each cube through `pmrem.fromCubemap` and keep the result.
  - Swap `scene.environment` to the zone the camera stands in. Do this in `frame()` (line 2463) with the existing
    point-in-room data used by the views.
  - From the same cube, build `LightProbeGenerator.fromCubeRenderTarget(renderer, rt)`. Add one `LightProbe` to the scene
    and copy the zone's SH into it on zone change.
  - Then lower `HEMI` .22 to .06 (line 2062) and `ENV` .3 to .6.
    - The captured env carries real bright-window and dark-back-wall directions.
    - The SH probe grades the ceiling from window to back.
  - At eve the captured env sees the dark sky and the lit room, so the glass and glossy surfaces show the room. Keep
    `envMapIntensity` .12 at eve (line 2342) or raise it to .3 and re-check.
  - Before capturing, hide the reflectors, the labels and the GTAO-hidden cards.
  - Capture without fog. `RectAreaLight`s are seen through the walls they light, which is what is wanted.
- Cost:
  - Desktop: runtime 0 (same sampling as now). One-off about 6 renders x 128 px per zone, about 30-80 ms per zone,
    hidden behind the fly-to animation.
  - Phone: the same at 64 px. GPU memory about 1-2 MB for all zones.
  - Download: 0.
- Risk: medium.
  - A visible pop when the env swaps at a doorway. Mitigation: blend over 0.3 s by drawing two env intensities, or swap
    while the camera is moving.
  - An env captured from the room centre gives slightly wrong reflections near walls (no parallax correction).
    Acceptable for roughness 0.2 and up; the mirror keeps its Reflector on desktop.
  - The path tracer (`ptScene`, around line 2380) must keep its own environment.
  - The bake export must not see the probes.
- Gain: +0.6 day, +0.4 eve.

### 4. Window light gating and rebalance (fix leaks, free shader budget)
- Looks fake now:
  - Light with no source in the hall, the corridor and the closet. The room 2 window wall is as bright as the far wall
    (`desktop_day_room2.jpg`).
  - Eight area lights plus eleven points are evaluated everywhere, which also costs phone fps.
- Change:
  - Give each `winLight` (lines 2070-2082) and each `warm` point (line 2084) a `zone` tag.
  - On zone change, set the intensity of lights outside the current zone and its visible neighbours to 0. This removes
    the leaks.
  - To remove the cost too, fix the light count per platform at startup:
    - Phones get 3 area lights: living east (merge the two 2.70 m openings into one 5.4 m light at z 3.9), master, and one
      re-targetable "current room" light whose position, size and direction are set from the zone table.
    - Phones get 4 points, re-targeted the same way.
    - Changing light count triggers a recompile, so do it only once at load.
  - Raise the living east area light k 5 to 6.5. Drop the hemisphere as in item 3.
    Together this gives a steeper window-to-back gradient.
- Cost:
  - Desktop: saves about 15-25% fragment cost on light loops.
  - Phone: about +4-6 fps headroom if counts are cut. That headroom pays for items 6 and 9.
  - Download: 0.
- Risk: medium.
  - Views that see two rooms (`desktop_day_photo.jpg`, `desktop_day_hall.jpg`) need both zones on.
  - Zone table errors show as a dark doorway. Test all 33 views with `sitetest.mjs`.
- Gain: +0.3 day.

### 5. Static shadow map (budget enabler)
- Looks fake now: nothing. This is pure budget.
- Change:
  - After the scene loads, set `renderer.shadowMap.autoUpdate = false` and `renderer.shadowMap.needsUpdate = true`.
  - Set `needsUpdate = true` again in:
    - `setMode` (line 2330)
    - the fans and door animations (`anim`, `fansOn` in `frame()`)
    - the ceramics picker apply
    - ceiling toggle
  - The sun shadow at 4096 (line 2066) is then drawn once instead of every frame.
- Cost:
  - Desktop: saves one 4096 depth pass of the whole model per frame (several ms).
  - Phone: saves the 2048 pass, a few fps.
  - Download: 0.
- Risk: low. A stale shadow if a moving object is missed. The fan blades have `cast` set; keep them updating or turn
  off their shadow.
- Gain: 0 visual. It funds items 6 and 9 on phones.

### 6. Physical materials without new assets: lacquer, ceramic, leather, fabric sheen, brushed steel, glass
- Looks fake now:
  - Fronts are flat matte boxes (`desktop_day_kitchen2.jpg`, `desktop_day_storage.jpg`, `desktop_day_closet.jpg`).
  - Steel reads as grey plastic (`desktop_day_kitchen2.jpg`).
  - Sofa leather is plastic (`desktop_day_tvwall.jpg`, `desktop_day_sofa.jpg`).
  - Fabrics have no rim sheen (`desktop_day_bedtv.jpg`, `desktop_day_room1.jpg`).
  - Ceramic is uniformly glassy (`desktop_day_bath.jpg`).
  - Shower glass is a flat tint (`desktop_day_shower.jpg`).
- Change (desktop: `MeshPhysicalMaterial`; phone: keep `MeshStandardMaterial` unless noted). Use a helper
  `P(color, rough, extra)` next to `M()` at line 498 that returns a physical material on desktop and a standard one on
  phones, then:
  - `front`, `greigeFront`, `whiteFront`, `door` (lines 512, 514): satin lacquer (finish is an estimate, not on a plan).
    `roughness .5`, `clearcoat .45`, `clearcoatRoughness .28`.
  - `ceramic` (line 515): `roughness .25`, `clearcoat 1`, `clearcoatRoughness .05`.
    Glaze over a less glossy body reads as vitreous china. Applies on phones too.
  - `steel` (line 513): `metalness 1`, `roughness .32`, `anisotropy .85`, `anisotropyRotation 0`.
    The world UVs from `mergeGroup` give the tangent direction. Brush along the long axis of the handles and the hob trim.
    Phone: `metalness 1`, `roughness .35`.
  - Sofa leather `sf` (line 1147): `M('#2f2a28', .46)` becomes:
    - `roughness .55`
    - `clearcoat .25`, `clearcoatRoughness .45`
    - `sheen .3`, `sheenColor '#5a4d45'`, `sheenRoughness .5`
    - a grain normal from item 10's leather set, or the `caban` normal at scale .2 until then
  - All `fab()` materials (line 500, used at 516-518):
    - add `sheen .6`, `sheenRoughness .7`, `sheenColor` the fabric colour lightened 25%
    - rugs `sheen .4`
    - phones skip sheen
  - `glass`, `showerGlass` (lines 508-509): physical with `ior 1.5`, `roughness 0`, `metalness 0`, `specularIntensity 1`,
    `opacity .08` / `.12`, `envMapIntensity 1`.
    No `transmission` (it adds a full extra scene pass).
  - `fridge` (line 532): `clearcoat .6`, `clearcoatRoughness .15` over the metal.
- Cost:
  - Desktop: the physical shader adds about 10-20% fragment cost on those surfaces. Clearcoat and sheen each add a lobe.
  - Phone: about 0 (standard kept, only roughness values change).
  - Download: 0.
- Risk: low to medium. Without item 3, clearcoat reflects the studio box and can look worse; do item 3 first. Physical
  materials are clones in the baked path (`bakedMaterial` clones `source`); the patch still applies because the chunks
  are the same.
- Gain: +0.4 desktop, +0.1 phone.

### 7. Floor tile: photo roughness, less cloud, grout relief
- Looks fake now:
  - The large living and entry tile reads as cloudy, blotchy concrete. The 1400-dot speckle in `T.tile` (lines 326-334)
    is low frequency at 2.4 m per repeat.
  - The grout has no depth at grazing view.
  - It is in almost every shot (`desktop_day_entry.jpg`, `desktop_day_hall.jpg`, `desktop_day_kitchen3.jpg`,
    `desktop_day_corridor.jpg`).
- Change:
  - In `T.tile`, cut the speckle alpha by half and its size to 1-2 px. That keeps the colour field even, as real
    120 cm porcelain is.
  - Keep `pbrDetail` for the grout bump (line 557, bump .35), but make the bump come only from the grout lines. Pass a
    grout-only canvas instead of luminance, so the cloud does not emboss.
  - Add a photo roughness only. `photoPBR` (line 570) cannot be used as is: it sets `bumpMap = null` and three r160 uses
    either a normal map or a bump map, not both.
    - Add an option `{ roughOnly: true }` that loads only `rough.webp` and leaves the bump.
    - Call `photoPBR([mat.tile], '<porcelain or polished concrete set>', 1.2, { roughOnly: true })`.
  - Rescale the roughness through `roughness` .58 (line 504) to land at about .35-.5. The finish is an estimate.
  - With item 3 the floor then shows soft, broken window reflections, which is the main tile cue.
- Cost:
  - Desktop: 0 runtime.
  - Phone: 0 runtime.
  - Download: about 150-250 KB (1k roughness WebP).
- Risk: low. A visible photo repeat at 1.2 m: rotate the UV by 90 deg per tile in the canvas or pick a low-contrast set.
- Gain: +0.3.

### 8. GTAO cleanup or replacement (desktop)
- Looks fake now: grain and hairy halos at depth edges (section 3 shots). Contact AO under furniture is weak at radius .3.
- Change, step 1 (no new code):
  - `updatePdMaterial({ lumaPhi: 6, depthPhi: 2, normalPhi: 4, radius: 6, rings: 4, samples: 24 })` (line 290).
  - `updateGtaoMaterial({ radius: .45, distanceExponent: 1.2, thickness: .25, scale: 1.0, samples: 24 })` (line 289).
  - `gtao.blendIntensity = .85`.
  - Verify the halos on `bath2`, `mbath`, `room2`, `corr2`.
- Step 2 if halos remain:
  - Replace with N8AO (MIT, about 30 KB, `N8AOPostPass`).
  - Settings: `halfRes: true`, `aoRadius: .5`, `distanceFalloff: .4`, `intensity: 2.5`, `denoiseSamples: 8`,
    `denoiseRadius: 12`, `screenSpaceRadius: false`.
  - It jitters per frame, so the existing TAA accumulation (line 2471) converges it to a clean still.
  - Keep the `noAO` list by passing it to N8AO's transparency handling or a layer mask.
- Cost:
  - Desktop: step 1 about +10% AO pass. N8AO at half res is about the same as today.
  - Phone: none (AO stays off on phones; contact decals cover grounding).
  - Download: step 2 about 30 KB.
- Risk: medium for step 2 (a new vendored module; `build_site.py` vendor swap must include it).
- Gain: +0.2 desktop.

### 9. Evening lamps that light their surroundings
- Looks fake now:
  - The bedside globes glow but light nothing (`desktop_eve_master2.jpg`).
  - The downlights make no wall scallops, so the walls are flat (`desktop_eve_corridor.jpg`, `desktop_eve_hall.jpg`).
  - The point lights have no shadows, so the undersides of tables and shelves are lit (`desktop_eve_tvwall.jpg`).
  - The family bath ceiling is blown (`desktop_eve_bath2.jpg`).
  - The corr2 ceiling is dark grey (`desktop_eve_corr2.jpg`).
- Change:
  - Bedside: two `PointLight(0xffc98a, 1.2, 2.2, 2)` at the globe centres (line 1366, 5.64/7.92, -.48, 1.05), eve only.
    Give them a `zone` so item 4's gating keeps the count low.
  - Kids' bath: move warm point 11 (line 2084, `[3.2,-2.6,2,BC-.3]`) down to `BC - .55` and k 2 to 1.2.
  - Two shadowed key lights on desktop: turn the living downlight cluster and the corridor run into `SpotLight`s.
    - Angle 1.0 rad, penumbra .8, decay 2, `castShadow` with 512 maps, intensity from the matching `warm` entry.
    - Phones keep points.
    - Static shadow (item 5) applies, so they cost one draw only on change.
  - Scallops:
    - `SpotLight.map` (r160 supports light cookies on shadow-casting spots).
    - Use a 128 px canvas with a soft parabola cut-off, for the two corridor wall-washing spots.
  - corr2: add one zone point at (corridor centre, H-.3) with k 2.5, or point an existing one at it after the gating
    table.
- Cost:
  - Desktop: two 512 shadow maps (static), plus 2-3 points within the gating budget.
  - Phone: +2 points only if item 4 cut the count; otherwise -1 to -2 fps.
  - Download: 0.
- Risk: medium. Spot shadows from ceiling-height lights can acne on the ceiling (`bias -.0005`, `normalBias .02`).
  Light-count changes recompile shaders; set the count once at load.
- Gain: +0.4 eve.

### 10. CC0 photo sets for quartz, steel, leather and smudges
- Looks fake now:
  - The quartz countertop and splash are procedural with near-uniform gloss (`desktop_day_island.jpg`,
    `desktop_day_kitchen3.jpg`).
  - Leather has no grain.
  - Glossy fronts and steel are perfectly clean, which reads as CG.
- Change, through `photoPBR` (line 570) additions in `photoReady` (lines 580-586):
  - `photoPBR([mat.quartz, mat.splash], '<white quartz or fine marble set>', 1.6, { color: true, normal: .15 })`.
    Tinted to the current mean, so the palette is kept.
  - `photoPBR([steel], '<brushed metal set>', .5, { normal: .2 })`.
    The roughness carries the brush lines; with anisotropy (item 6) that is the full brushed look.
  - Leather: `photoPBR([sf], '<leather set>', .4, { normal: .4 })`.
  - Smudges: a grayscale imperfection map. Combine it into the fronts', fridge's and steel's `roughnessMap` channel at low
    contrast, or as `clearcoatRoughnessMap` on desktop.
- Cost:
  - Desktop: 0 runtime (texture samples only).
  - Phone: 0 runtime.
  - Download: about 1.2-1.6 MB total (see section 5).
- Risk: low. A visible repeat on the long countertop: use the 1.6 m repeat and rotate per run.
- Gain: +0.25.

### 11. Sheers and curtains
- Looks fake now: the sheers read as striped tubes, with regular sine folds and a hard vertical stripe texture
  (`desktop_day_sofa.jpg`, `desktop_day_photo.jpg`). They do not glow when backlit by day.
- Change:
  - `curtain()` (lines 757-763): fold count from `folds = 9` to 14 with `amp = .03`. Add a second harmonic
    (`+ .4 * amp * sin(u * 2 pi * 2.7 * folds * len / 1.2 + 1.3)`) and a slight hem flare (amp x 1.15 at the bottom row).
    Vertex count is unchanged at seg 48.
  - `sheerTex` (line 1037): replace the 2 px stripes with a fine woven noise (1 px, alpha .04-.08), or a CC0 sheer
    fabric 512 px alpha.
  - `sheer` material (line 1039): add a day emissive `#fffaf2` at .12, set in `setMode` (0 at eve), so the window side
    glows the way a backlit voile does. Opacity .72 to .6. Keep `depthWrite:false`.
- Cost:
  - Desktop: 0.
  - Phone: 0.
  - Download: 0 to 150 KB.
- Risk: low.
- Gain: +0.15 (large in the living room views).

### 12. Re-bake the lightmaps correctly (largest single gain, highest cost)
- Looks fake now: see section 3. The opt-in bake is stale (63 missed), dark and blotchy.
- Change:
  - Bake after the geometry is frozen. Every wall or furniture change invalidates the bbox and vertex-count match at
    line 2148.
  - `lm/bake.py`:
    - Multiply the stored light by pi at publish, or use `pass_filter={'DIRECT','INDIRECT','COLOR'}` divided by the
      albedo. The first is simpler: `rgb *= np.pi` in `lm/publish.py` before the range.
    - `SKY_STRENGTH` .35 to 1.0 (line 303), with the sky gradient renormalised so its mean equals the viewer's day sky.
    - Ground `gnd * .35` to a neutral `[.45,.43,.40]` at 1.0 (line 281). The street and yard bounce is what lights the
      ceilings.
    - Use the `hdri_sky` option with the same day sky the viewer shows (`assets/sky/day.webp`'s source HDRI). That keeps
      bake and real-time colour consistent.
    - Samples 64 to 256, `use_denoising = True` with OIDN (line 30).
    - Two 2048 atlases instead of one, with texel .03 to .015 for floors, so contact shadows under furniture resolve.
  - `lm/publish.py`: replace 8-bit sRGB WebP with RGBM (alpha holds a multiplier, range 8), or with two WebPs (low and
    high halves). That ends the banding in the lamp bake (range 22.6).
  - Viewer, lines 2107-2116: keep the patch, add a sanity gain in `LM.gain`, and drop the `?baked=1` opt-in only after
    the bake matches 154 of 154.
  - Phone fallback if the full bake is too heavy: load only the AO atlas and the UV file, and assign `aoMap = ao`,
    `aoMap.channel = 1`, `aoMapIntensity .8` to the clones (no lighting patch). That is grounding for phones at about
    650 KB.
- Cost:
  - Desktop: runtime 0 to slightly less (baked surfaces skip direct light).
  - Phone: the AO-only path is one extra texture sample.
  - Download: about +1.5-2.5 MB for two atlases of natural, lamps and AO plus UVs. Today it is about 1.3 MB but is not
    loaded by default.
  - Offline: needs `pip install bpy` (Blender 5.2 module, not installed on this Mac) and a CPU bake of several hours at
    256 spp.
- Risk: high. Stale-bake drift on every future geometry change, the build time, and a doubled maintenance surface with
  the path tracer.
- Gain: +1.0 to +1.5 when done right (bounce, colour bleed, contact shadows in all rooms). It is ranked here only
  because of cost and fragility.

### 13. Grading pass (desktop) and eve white balance
- Looks fake now: neutral, slightly grey day frames. Eve is good but the warm and cool split is weak (daylight .12
  RectAreaLights at eve are cool-ish already).
- Change:
  - A `ShaderPass` after the bloom (line 296) and before the `OutputPass` (line 297), working in linear HDR.
  - Lift shadows by +.01. Apply a white balance multiply: day `(1.0, .99, .97)`, eve `(1.04, 1.0, .93)`.
  - Saturation .95 day, 1.05 eve. Vignette .15. Grain .015 (animated only while moving, static in the TAA still).
  - Eve: lower the bloom threshold .95 to .85 and the radius .45 to .3, so lamps glow locally rather than as a wash.
  - Phone: the CSS vignette from item 2 only.
- Cost:
  - Desktop: one full-screen pass, about 0.5 ms.
  - Phone: 0.
  - Download: 0.
- Risk: low.
- Gain: +0.15.

### 14. Props and clutter (CC0 models)
- Looks fake now:
  - Rooms 1-3, the desk and the bath counters are near-empty (`desktop_day_room3.jpg`, `desktop_day_desk.jpg`,
    `desktop_day_bath.jpg`).
  - The fruit bowl is plastic (`desktop_day_isle2.jpg`).
- Change:
  - Load a small set of Poly Haven models lazily after the first still (desktop), through the existing `assetTex` and
    GLB path (around line 1718).
  - Candidates:
    - 2-3 ceramic vases
    - a book set
    - 2 potted plants
    - a wooden bowl with fruit
    - a towel stack
    - a throw on the sofa or bed
    - a kettle or coffee machine on the counter
    - a bath mat
  - Phone: skip, or load only 2 hero props with 512 textures.
  - Replace the procedural fruit with photo fruit or remove it.
- Cost:
  - Desktop: about 10-25k triangles total, under 1 ms.
  - Phone: 0 if skipped.
  - Download: about 1.5-3 MB at 1k textures. This is the item that most threatens the 12 MB budget; cap it at 2 MB.
- Risk: low to medium. Scale errors and style clash; every prop is a fiction not on the plans, so label it as styling.
- Gain: +0.3 desktop.

### 15. Geometry bevels and sanitaryware shapes
- Looks fake now: hard 90 deg edges on fronts, worktops and the island (no edge highlight). Toilets and basins are boxy
  (`desktop_day_bath.jpg`, `desktop_day_mbath.jpg`).
- Change:
  - Use the existing `B(..., { round: r })` (used by the sofa at line 1147) with `r .003` for fronts and doors, and
    `r .006` for the worktop edges.
  - Toilets and basins: `LatheGeometry` profiles (bowl about 20 points, 32 segments) instead of boxes, or a CC0 toilet
    and basin model if the asset agent finds one.
- Cost:
  - Desktop: a few thousand vertices.
  - Phone: the same.
  - Download: 0, or about 300 KB for the models.
- Risk: low. `roomdims.py` and `clearance_audit.py` do not depend on bevels, but re-run them if footprints change.
  `mergeGroup` UVs on rounded boxes need a check for stretched grain on oak fronts.
- Gain: +0.15.

### 16. Sun patches indoors (optional preset)
- Looks fake now: no sun on any interior floor by day. At about 10:00 and 45 deg elevation (line 2065) the balcony
  overhang shades the living room, which is plausible but removes the strongest realism cue.
- Change: an optional "morning" preset with the sun about 25 deg up from the east (`sun.position` y 12 instead of 24).
  This throws long patches across the living floor; the static shadow (item 5) refreshes once.
  The orientation follows the plan's north arrow; the hour is a choice, not a measurement.
- Cost:
  - Desktop: 0.
  - Phone: 0.
- Risk: low (UI addition). The bake (item 12) would need a matching sun.
- Gain: +0.3 for those views when chosen.

### 17. Sun shafts: not recommended
- Volumetric god rays (a raymarched pass or `GodRaysPass`) cost a full-screen pass and look staged in clean indoor air.
- If wanted, use 2-3 additive soft cards in the balcony openings, desktop only, opacity .04, in the morning preset only.
- Gain about +0.05.

## 5. New CC0 assets needed

At the time of writing `source/out/real5/assets/` was empty. Sizes are estimates for 1k WebP (the format of the current
`assets/tex/*`). The set names are placeholders for whatever the asset agent sources; Poly Haven and ambientCG both
publish CC0 sets of each kind.

| Use (item) | Maps | Size each | Total |
|---|---|---|---|
| Floor porcelain roughness (7) | rough 1k | 150-250 KB | about 0.2 MB |
| Quartz or fine marble (10) | diff, nor, rough 1k | 250 / 350 / 150 KB | about 0.75 MB |
| Brushed metal (10) | nor, rough 1k (diff not needed) | 300 / 150 KB | about 0.45 MB |
| Leather grain (6, 10) | nor, rough 1k | 300 / 150 KB | about 0.45 MB |
| Surface imperfections / smudges (10) | rough 1k grayscale | 150-250 KB | about 0.2 MB |
| Sheer voile (11, optional) | alpha or diff 512 | 100-150 KB | about 0.15 MB |
| Props (14) | GLB plus 1k textures | 0.2-0.6 MB each | cap 2 MB |
| Toilet and basin (15, optional) | GLB | about 150 KB each | about 0.3 MB |
| N8AO module (8, step 2) | JS | about 30 KB | 0.03 MB |

- Total for items 6-11: about 2.1 MB.
- With props: about 4 MB, which puts the desktop at about 16 MB.
- To stay near 12 MB:
  - ship the material sets at 1k and the props at 512
  - skip props on phones
  - drop the 1.3 MB baked set from the default deploy until item 12 is redone (it is not loaded unless `?baked=1`, so it costs nothing at runtime but sits in the repo)
- No HDRI is needed for the interior: item 3 captures the environment from the scene itself.

## 6. Expected outcome

| Step | Day | Eve |
|---|---|---|
| Items 1-5 (no assets, mostly 1-2 days of work) | about 5.9 | about 6.2 |
| Plus items 6-11 | about 6.6 | about 6.9 |
| Plus item 12 (correct bake) | about 7.3-7.5 | about 7.3-7.5 |

Phones should keep about 37 fps if items 4 and 5 land before items 6 and 9.

## 7. Verification for each change

- `python3 build_site.py`.
- Re-shoot with `source/out/quick.mjs` (one Chromium at a time) into a new tag. Compare against
  `source/out/real5/interior/shots/` in the same 25 views, day and eve.
- `sitetest.mjs` "no issues", and a phone fps check.
- `roomdims.py` and `clearance_audit.py` only if item 15 changes footprints.
- Item 7 and item 10 change surfaces seen in the gallery renders: mark those renders stale in PROJECT_MEMORY.
