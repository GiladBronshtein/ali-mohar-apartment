# Realism audit 5: exterior and environment

Scope: everything outside the apartment envelope as seen from the balcony, out of the windows and from the bird views:
neighbour facades, our own building shell, sky, haze, trees, ground, cars, street furniture, the balcony, evening
lighting and outdoor shadows. Report only: nothing in `source/salon.html` was changed.

Method: repo root served on 8793, `source/out/quick.mjs` at 1440x900 (desktop HQ path: TAA, GTAO, bloom), day and eve.
Built-in views `balcony, balcony2, view, inside, bird1, bird2, top, master, room2` plus four custom views
(`c_street` down onto the street, `c_north` along the street, `c_far` toward the tower and far blocks, `c_south` along
building A). Compared against the balcony photos in `materials/photos/` (contact sheets in
`source/out/real5/exterior/photos_0.jpg`, `photos_1.jpg`). No page errors in any run.

Shots (gitignored scratch):
- `source/out/qa/r5ext/desktop_{day,eve}_<view>.jpg`
- `source/out/qa/r5extc/desktop_{day,eve}_c_{street,north,far,south}.jpg`
- contact sheets `source/out/real5/exterior/sheet_*.jpg`

Line numbers below refer to `source/salon.html` at commit 16abbec.

## 1. What the photos show (the target)

- Big cumulus sky, partly cloudy, bright and slightly hazy toward the horizon.
- 6 to 9 storey white and cream blocks. Deep, dark, recessed loggias with glass or grey-frame railings. Roller shutters
  at different heights, AC condensers, red-tile roof accents and solar heaters. Strong sun and shadow contrast on every
  facade.
- The school: cream stone, framed and recessed windows, a PV roof.
- The lot north of the school: orange hamra soil.
- Small olive-like street trees. Grey patched asphalt. Red and pink concrete pavers that are greyed and dusty, not
  saturated.
- Real cars: glossy bodies and glass that mirror the sky.
- The tower: white with dark vertical loggia strips.
- Distance falls off into a pale blue-grey haze. The ground between the blocks is green courtyards, paving and parking,
  never bare tan.

## 2. Per-view scores (out of 10, photorealism of the exterior part of the frame)

| View | Day | Eve | Shot | Main tells |
|---|---|---|---|---|
| `view` (balcony toward the street) | 4 | 3.5 | `qa/r5ext/desktop_day_view.jpg` | Flat painted block facades. Tan desert ground running to a hard horizon with no haze. Toy cars with black glass. Saturated flat pink pavers. |
| `balcony` | 5.5 | 5 | `qa/r5ext/desktop_day_balcony.jpg` | The interior side is good. Soffit, walls and parapet are flat untextured grey. Repeating block facades behind. |
| `balcony2` | 5 | 4.5 | `qa/r5ext/desktop_day_balcony2.jpg` | Plants (glTF) and the egg chair hold up. Tower and blocks flat; tan horizon band. |
| `inside` (back toward the living room) | 6 | 5.5 | `qa/r5ext/desktop_day_inside.jpg` | Balcony facade is plain grey stucco with no texture or relief. |
| `bird1` | 5 | 4.5 | `qa/r5ext/desktop_day_bird1.jpg` | Building A is grey with 256 px painted windows. Shell top is a plain slab; cut wall caps are dark grey. |
| `bird2` | 3.5 | 3 | `qa/r5ext/desktop_day_bird2.jpg` | Floors 0-1 shell is a painted box. Tan ground. Broken bright and grey patches where the ±13 m shadow frustum cuts the 23 m building's shadow. The weeds lot reads gold. |
| `top` | 5.5 | 5 | `qa/r5ext/desktop_day_top.jpg` | Asphalt is good. Cars read as boxes from above. Tree cards show their X. West ground is flat tan. |
| `master`, `room2` (window views) | 5 | 4.5 | `qa/r5ext/desktop_day_master.jpg` | Neighbour facades seen close are flat, overbright painted grids. |
| `c_street` | 4.5 | 3.5 | `qa/r5extc/desktop_day_c_street.jpg` | Cars float: no contact shadow, no reflections. Accessible bay blue too saturated. Pavers uniform. No shadows from trees or poles. |
| `c_north` | 5 | 4 | `qa/r5extc/desktop_day_c_north.jpg` | The best exterior frame. Still flat painted blocks, cars without reflections, gold weeds strip. |
| `c_far` | 4 | 4 | `qa/r5extc/desktop_day_c_far.jpg` | Tower is a white box with black stripes. Far tree cards stand on bare tan. No aerial perspective at 60 to 200 m. |
| `c_south` | 4.5 | 4 | `qa/r5extc/desktop_day_c_south.jpg` | Our own balcony end wall fills half the frame as untextured flat grey (`mat.concrete`). |

Eve, all views: street lights glow but cast no light on the road. Every lit window is the same flat warm rectangle.
The school is dark. Facades are a dull uniform grey and the far ground goes murky. Sky colour is acceptable but very
purple and dark (`k .35`).

Overall exterior: about 4.5/10 day, 4/10 eve. The interior is clearly ahead of the exterior. The exterior is what
gives the model away in every balcony and bird frame.

## 3. Root causes (code level)

1. **No aerial perspective.**
   - `scene.fog = new THREE.Fog(0xdfe6ec, 90, 460)` (line 275) does nothing at 30 to 200 m, where almost every
     building sits.
   - The 500x500 ground plane (line 1805, `mat.ground` `#a7a49a`) ends at 250 m. It meets the sky in a hard tan line.
2. **Facades are one 256 px canvas bay.**
   - `facadeTex()` (line 416) is tiled over every block, building A and our floors 0-1. It has no depth, no
     roughness or normal map, no variation, and no shadow under the balcony slabs.
   - The blocks are `cast:false` and outside the shadow frustum, so their 1.6 m balcony slabs (line 1975) cast nothing.
3. **Exterior materials reflect a studio.**
   - `scene.environment` is a PMREM of `RoomEnvironment` (line 274).
   - Car paint (metalness .5, rough .3), window glass (`mWin`), glass rails and facades all reflect a grey studio
     instead of the blue sky. This is why car glass reads black and glossy paint reads plastic.
   - The photo skies only reach the path tracer (`skyEnv()`, around line 2360).
4. **Shadows only exist within ±13 m of the apartment** (line 2067), and almost all outside meshes are `cast:false`.
   - Trees, cars, poles and buildings cast nothing on the street.
   - In `bird2` the frustum edge slices building A's shadow into fragments.
5. **Trees are two crossed quads with up-pointing normals** (`treeCards()`, line 1999).
   - From above they show an X.
   - Every leaf is lit the same, with no sun side and no shade side, and nothing casts onto the ground.
6. **Cars are extruded profiles** (lines 1879 to 1897). One colour, flat glass, no wheel-arch shadow, no contact
   shadow.
7. **Ground near the street is canvas-painted.**
   - Pavers (`paverT`, `mPaver*`, line 1837) are flat, saturated pink, with no normal or roughness.
   - The accessible bay is pure `#3d6fa8`.
   - Asphalt, soil and turf already use CC0 photo sets (line 1839) and look right.
8. **Our own outside surfaces are `mat.concrete`** (`#e9e7e2`, rough .95, no map): balcony walls, soffit, upstand,
   floors 0-1 box and caps. The interior wall already has `white_stucco` PBR (line 584).
9. **Eve.** `setMode` (line 2330) only turns emissive maps on:
   - `litMats` at 1.0 (one 512 `litTex` per block, two warm colours, 30% lit).
   - `glowMats` at 2.5.
   - Nothing lights the ground, and no window varies in colour, curtain or brightness.

## 4. Ranked improvements (realism gain per cost)

Costs: "desktop" is the HQ composer path at about 20 fps forced; "phone" is the plain `renderer.render` path at about
37 fps. Download budget is about 12 MB and the site is at about 11.9 MB today (`assets/` 8.6 MB, `vendor/` 2.3 MB,
page about 0.3 MB plus fonts). So zero-download (procedural or canvas) items rank first. Anything that needs a new
download must replace an existing asset or be lazy-loaded on desktop after the first frame. All figures are estimates
until measured with the skill's fixed-pose benchmark.

### 1. Aerial perspective and the horizon (gain high, cost very low)

**Fake:** tan desert to a hard horizon, and no haze at any distance. See `view`, `c_far`, `c_south`, `balcony2`.

**Change:**
- Replace the linear fog (line 275) with a fog that starts where the exterior starts.
  - `THREE.Fog(col, 30, 420)` is enough as a first pass. Interior distances are under 15 m, so rooms are untouched.
  - Better: a small `onBeforeCompile` patch of `fog_fragment` that adds height falloff, denser near `GY`, thinner
    upward, so the roofs against the sky stay crisp and the street end fades.
  - Guard the chunk text with a throw, per the skill.
- Fog colour per mode, sampled from the sky texture's horizon row:
  - day: a pale blue-grey near `#cfd9e3` instead of `#dfe6ec`;
  - eve: the eve sky horizon tone, not `0x3a3f4f`, so the far blocks melt into the dusk instead of going murky.
- Close the horizon. Either:
  - shrink the visible ground: fade `mat.ground` to the fog colour past 150 m, which the fog does by itself once it is
    tuned; or
  - add a ring (open cylinder, radius about 320 m, height about 25 m, one draw call, `fog:false`, drawn before the
    sky) textured with a CC0 hazy-suburb skyline strip. Its alpha top edge breaks the line; its colour is pre-hazed to
    the fog.
- Draw the sky last at the far plane (`gl_Position.z = gl_Position.w` in the sky material, `renderOrder` high).
  This is a free GPU saving the skill measured at 4 to 8%. It pays for the rest.

**Cost:** desktop and phone about 0 ms (the fog is already in every shader). The ring is one draw call. Download 0 for
fog only; about 150 KB for a 2048x256 skyline WebP.

**Risk:**
- Window views (`master`, `room2`) gain some haze on the blocks 20 to 40 m away. Tune the start to about 30 m and
  check both.
- The path tracer ignores three.js fog, so PT frames will differ slightly.

### 2. Ground: courtyards, not desert (gain high, cost low)

**Fake:** the 500 m plane is one flat tan colour (line 1805). The courtyard trees stand on bare tan (`c_far`,
`view`, `bird2`).

**Change:**
- Give `mat.ground` a macro mask: a 512 px canvas noise map, about 2 to 4 m per texel, generated in JS with no
  download. It blends three detail sets already shipped or cheap:
  - `grass_ground` (loaded for turf at line 1839) for lawns;
  - `park_dirt` for dry patches;
  - a paver or concrete tile for courtyard paving.
- Do it as one `onBeforeCompile` patch on a separate ground material (feature code behind `#ifdef`, per the skill).
- Paint the courtyards around each `block()` green: the mask can be written from `foot` (the block footprints are
  already collected), with a 3 m paved apron around each block and lawn beyond.
- Add soft dark discs under the courtyard tree spots (see item 5).
- Keep the hamra lot as is until the owner confirms the soil colour (open question in PROJECT_MEMORY).

**Cost:** desktop and phone well under 0.3 ms (three texture taps on a plane that is mostly covered). Download 0 if the
existing sets are reused.

**Risk:** low. Tiling repetition at grazing angles; break it with the macro mask and the anisotropy that is already set.

### 3. Sky environment for exterior materials (gain high, cost low)

**Fake:** car glass is flat black, paint looks plastic, glass rails and window glass reflect a grey studio (`c_street`,
`c_north`, `view`).

**Change:**
- After the photo skies load (line 2018), build `envSkyDay = pmrem.fromEquirectangular(dayTex)` and the eve one.
  - Use a 256 or 512 px copy, not the 4096 px backdrop.
  - Undo the backdrop's `repeat`/`offset` crop. Rotate to match `skies.day.rot` (bake the rotation into a canvas copy,
    because PMREM has no rotation in r160).
- Assign as `material.envMap` on every exterior material only:
  - car paint, `mWin`, `mGlassRail`, `mGlassRailN`, `mHead`, `mPole`, block facades, tower `mT`, school;
  - the balcony railing (`mat.blackMetal` is shared with the interior, so split an exterior copy).
- Keep `scene.environment` (RoomEnvironment) for the interior. Swap per mode in `setMode`.
- Same PMREM size gives the same program key, so no extra shader compiles. This is a PMREM of a texture, not a
  browser cube capture (the skill's 8 s trap).
- This also fixes the sun-sky consistency for reflections: the sky that is seen is the sky that is reflected.

**Cost:** about 30 to 60 ms one-time at load; 0 per frame. Download 0.

**Risk:** low. Watch the facades' `envDay 1.1` value; with a bright sky env they may brighten, so retune to about .6.

### 4. Facade atlas v2: variety, glass, baked balcony shadows (gain very high, cost low to medium)

**Fake:** every block is the same 256 px bay. No shutters, no AC units, uniform dark glass, and no shadow under any
balcony. They read as painted boxes (`view`, `c_far`, window views, `bird1`).

**Change:**
1. Replace `facadeTex(kind)` (line 416) with a 1024x1024 atlas of 4x4 bay variants per kind. Variants:
   - roller shutters at 0, 30, 70 and 100% closed;
   - aluminium frames in light grey;
   - an AC condenser on some balconies;
   - a darker loggia recess (70% of the bay width, near-black at the back);
   - a drainpipe column.
   Draw it as canvas at load (download 0), or paint it in Blender and ship it as WebP (about 250 KB per kind at 1024,
   512 on phones).
2. Pick variants per bay in the shader. Patch the facade material so that `floor(vUv*repeat)` hashes to an atlas
   cell. Use one material per kind, as today, so no new draw calls.
3. Add a roughness channel: glass .08, frames .4, stucco .9. Use a second small canvas or the atlas alpha. With item 3
   the windows then mirror the sky and the facades stop reading as paper.
4. Bake the sun into the facade texture.
   - Under every balcony slab row (`block()` places slabs at every storey on one face, line 1975) draw a soft dark band
     about 1.2 m tall, shaped to the sun elevation of about 40°.
   - Darken the loggia backs.
   - Faces turned away from the sun (west and north faces in the 10:00 sun) get a lower base value.
   Realistic sun and shade contrast for zero runtime cost, since the sun never moves.
5. Give the balcony slabs on `block()` a 15 cm white front band and a grey-frame railing texture (CC0 railing
   alpha), instead of the near-invisible `mGlassRail` box.

**Cost:**
- Desktop and phone: one hash and one more texture tap on the facade materials, about 0.1 to 0.3 ms.
- Draw calls unchanged.
- Download 0 (canvas) or about 0.5 MB for 2 kinds at 1024 (WebP). On phones, half size.

**Risk:**
- Medium-low. The canvas atlas is code-heavy.
- The `litTex` emissive maps (line 1969) must be regenerated to line up with the new window cells; derive both from
  the same cell table.

### 5. Ground contact shadows from a fixed sun (gain high, cost low)

**Fake:**
- Cars, trees, poles and buildings cast nothing outside ±13 m. Cars float (`c_street`) and trees float (`c_far`).
- `bird2` shows broken shadow patches.

**Change:**
- Blob layer:
  - One merged mesh of quads at `GY + .02`, `MeshBasicMaterial`, black, `transparent`, `depthWrite:false`,
    `polygonOffset`, one 128 px radial alpha texture generated in JS.
  - Under each car: a soft rounded rectangle 4.6 x 2.0 m, plus a shifted copy along the sun direction.
  - Under each tree spot: a soft ellipse projected along the sun vector (offset `h * .5 * sunDir.xz / tan(elev)`).
  - Under each pole: a thin streak.
  - Data source: the existing spot arrays (`streetTrees`, `yardTrees`, the car lists at lines 1891 to 1893,
    `streetLight` calls).
- Building shadows: project every `block()` and `building()` box onto the ground plane along the sun direction. The
  2D hull of the 8 projected corners is a ShapeGeometry. Merge them into the same layer with a softer, lower opacity
  of about .35.
  - The sun is static per mode, so this is exact. In eve, hide the whole layer except a faint ambient-occlusion version
    under cars.
- Fix `bird2`: either widen the shadow camera when a bird view is active (switch `sun.shadow.camera` extents per
  view group in `setView`, ±30 m, `updateProjectionMatrix`), or keep ±13 m and let the projected building shadows
  cover the street.

**Cost:**
- One draw call. Small overdraw on the street, so phone cost is about 0.2 ms.
- Download 0.

**Risk:** low.
- The blobs must not double up with real shadows near the apartment. Skip spots inside the ±13 m frustum, or fade by
  distance from the sun target.

### 6. Our own shell and balcony surfaces (gain medium-high, cost very low)

**Fake:**
- Balcony walls, soffit and upstand are untextured `mat.concrete` (`c_south` is half a flat grey slab).
- The floors 0-1 box is a painted facade (`bird2`).
- Cut wall caps are dark grey in `bird1`.

**Change:**
- Add `mat.stuccoExt`, a copy of `mat.wall` with `white_stucco` (line 584) at a 1.5 m scale and colour `#ecebe6`.
  Use it for the balcony walls, soffit and upstand (lines 1656 to 1658) and the `B(BX1..)` box under the balcony.
  - World UVs already work through `userData.uv` and `mergeGroup`.
- Floors 0-1 (`building(-4.28, 9.30, -5.39, 9.11, ...)`, line 1820): replace the facade texture with `mat.stuccoExt`.
  - Add the real window openings: the same plan as floor 2, so repeat floor 2's window list at y -3.3 and -6.6 as
    15 cm recessed dark-glass panels with a frame.
  - Building A's east face gets the same treatment.
- Add a 2 cm drip-groove line and a 20 cm slab edge band on the balcony front face.
- Bars of the black railing: metalness .6, roughness .35, sky env (item 3).
  - The final railing is unknown: the photos show temporary red construction rails, and the black bars remain an
    estimate. Do not add detail that implies a known product.
- Egg chair: a 512 px rattan alpha and normal on the tubes, or leave it. It already reads correctly at balcony distance.

**Cost:** about 0 at runtime (the material is already loaded). A few hundred triangles for the window insets.
Download 0.

**Risk:** low.
- `roomdims.py` is unaffected (outside surfaces only).
- Run `clearance_audit.py` anyway if the balcony walls are touched.

### 7. Tree lighting now, impostors later (gain medium-high, cost low, then medium)

**Fake:** crossed cards show an X from `top` and `bird1`. Lighting is uniform because the normals point up (line
2008). Species are few.

**Change, step A (cheap, download 0):**
- Give each card vertex a normal pointing from the tree's crown centre (`x, GY + .6h, z`) to the vertex, blended 50/50
  with up. Sun-side leaves brighten and the far side darkens, which reads as volume.
- Add a per-tree tint attribute (±8% value, slight hue shift).
- Add a third horizontal quad at 0.6h for top views, using the crown's top view if one is rendered, otherwise the
  same atlas half.
- Add the ground blobs from item 5.

**Change, step B (desktop first):**
- Hemi-octahedral impostors, 8x8 frames, albedo plus alpha and a normal atlas.
- Baked in `.venv-bpy` like `treecards.py`, from the same Poly Haven trees plus an olive for the street trees.
- One `InstancedMesh` per species, frames blended per pixel, lit from the baked normals.
- Atlases 2048 on desktop, 1024 on phone.
- They replace the 1.55 MB of card atlases, so the net download change is small if limited to 2 to 3 species.

**Cost:**
- Step A: about 0 ms, download 0.
- Step B: desktop about 0.3 to 0.6 ms for about 120 trees; phone similar at half resolution.
- Download about +0.5 to +1 MB net, so lazy-load step B on desktop after the first frame.

**Risk:**
- Step A is low.
- Step B is medium: frame blending seams, and alphaTest AA under TAA. Keep impostors in `noAO`, like the cards.

### 8. Ground PBR near the street: pavers, kerbs, markings (gain medium, cost low)

**Fake:**
- Flat saturated pink pavers with no joints in relief and no roughness change (`c_street`, `view`).
- A pure blue accessible bay.
- Pristine lane lines.

**Change:**
- Replace `paverT`, `mPaver*` and `mPaverWalk` (line 1837) with one CC0 interlocking paving set (colour, normal,
  roughness).
  - Tint it to the photos' dusty grey-pink, and use the colour multiplier for the red and walk variants, so one
    texture set serves all three materials.
  - Kerbs: a concrete PBR.
- Accessible bay: lower saturation, about `#4a6f96` at 70%, with worn edges.
- Asphalt: keep `asphalt_02`. Add a decal layer (one merged mesh, alpha texture) with patch rectangles,
  manhole covers, oil stains under the parked cars and worn lane lines.

**Cost:**
- About 0.1 ms. One extra draw call for decals.
- Download about 400 KB at 1k (paving and kerb, WebP); phones use 512.

**Risk:** low. Keep the bay colours legible: they encode the plan's parking layout.

### 9. Evening: light on the ground, life in the windows (gain high in eve, cost low)

**Fake:**
- Street-light heads glow but the street under them is dark.
- Every lit window is the same flat amber.
- The school and building entrances are dark (all eve shots).

**Change:**
- Light pools: one merged mesh of additive quads (`AdditiveBlending`, `depthWrite:false`, `polygonOffset`) under
  each `streetLight` head (line 1873).
  - A 7 m warm ellipse on the asphalt and pavement, built from a radial texture generated in JS.
  - Visible in eve only, toggled in `setMode` next to `glowMats`.
  - Optional: a faint vertical cone sprite under each head on desktop only.
- Windows (`litTex`, line 1939):
  - three colour temperatures: 2700 K amber, 3500 K, and 4500 K cool white for about 15%;
  - a few blue-white TV windows;
  - curtain bands, a dimmer half on about 30% of lit windows;
  - per-window brightness .5 to 1.2.
  - Draw the light spill onto the balcony slab below a lit window into the same emissive map, as a faint row under
    each window. Download 0.
- School: two or three wall-pack lights over the entrances and a lit stairwell strip (emissive boxes plus pool
  quads). Building entrances get the same treatment.
- Facades in eve: the eve sky PMREM from item 3 adds the blue-hour tint that is missing. Check the eve sky brightness
  (`k .35`) against the exposure of 1.2. The far ground should read as dusk, not mud.
- Parked cars stay unlit. That is correct and should not be "fixed".

**Cost:** about 0.1 ms in eve on both paths. Bloom on desktop already catches the heads. Download 0.

**Risk:** low. Additive pools over shadowed balcony views can look like spotlights; keep them broad and below .25
intensity.

### 10. Cars: better body, or CC0 models (gain medium, cost medium)

**Fake:** extruded single-colour hatchbacks with box wheels. They read as toys, especially from `top` and
`c_street`.

**Change:**
- First, items 3 (sky reflections) and 5 (contact shadows). Most of the toy look is the lighting, not the shape.
- Then, either:
  - (a) improve `carProf`: side taper by scaling the extrusion's outer vertices in, wheel-arch cutouts as dark
    discs, separate window glass with the sky env, a dark lower sill band, and a per-car roughness of .2 to .35; or
  - (b) two or three CC0 realistic glTF cars (hatchback, SUV, van), 5 to 15k triangles each, meshopt plus a 512 WebP,
    shared materials, colour per instance via `InstancedMesh.setColorAt`, about 16 instances total. The single
    black SUV in the photos can be the close one.
- Avoid stylised kits (Kenney, Quaternius): they are CC0 but would read as more toy-like than the current cars.

**Cost:**
- (a) about 0, download 0.
- (b) desktop about 0.2 ms, phone about 0.3 ms with instancing. Download about 300 to 600 KB, lazy-load on desktop and
  keep (a) on phones.

**Risk:**
- Medium for (b): finding genuinely CC0, realistic, light car models is the hard part.
- (a) is low risk.

### 11. School and tower detail (gain medium, cost low-medium)

**Fake:**
- School windows are a dark slab on the face (line 1900 onward).
- The tower is a flat white box with black stripes. The louvres are near-black `#4a3a30`, so the photo's recessed
  loggia strips read as paint (`c_far`).

**Change:**
- School: inset the window glass 15 cm behind the frame, add a stone sill, use a light frame colour and give the glass
  the sky env. The facade stone gets `facadeTex` v2 in a 'school' kind with stone joints.
- Tower:
  - Lighten the louvres to a warm dark grey, about `#5d5048`, with sky env.
  - Add the loggia back wall 1.2 m behind the louvre plane, so parallax shows.
  - Bake a soft shadow column into `face` beside each strip, the same trick as item 4.
  - The many per-slat boxes (line 1950) become one texture strip: fewer triangles and the same look at 60 m.

**Cost:** about 0. Fewer triangles on the tower. Download 0.

**Risk:** low.

### 12. Interior mapping for close facades (gain medium, cost medium; desktop only)

**Fake:** window views (`master`, `room2`) and `bird1` look straight into neighbour windows that are flat dark paint.

**Change:**
- A separate facade material variant behind `#define INTERIOR_MAP`, used only by building A and the nearest 4 to 6
  blocks (within about 60 m).
- The fragment shader ray-casts a box room behind each window cell and samples a 2x2 or 4x4 room atlas (back wall,
  sides, floor and ceiling), with a random cell per window and curtains drawn in the atlas.
- Build the atlas in Blender from the apartment's own rooms (the model already exists) at 2048x1024.
- Phones keep atlas v2 (item 4).

**Cost:**
- Desktop about 0.3 to 0.8 ms (only facade pixels within 60 m).
- Download about 300 to 500 KB, lazy-loaded on desktop.
- Phone 0.

**Risk:** medium. Shader work, and interiors read wrong if the room scale does not match the 3.2 m storey. Do it
after items 1 to 9.

### 13. Sun and sky consistency check (gain low-medium, cost very low)

**State:**
- The sun light is at `(+25, 24, +14)` from the target: elevation about 40° (the comment says 45°), azimuth about 119°
  (ESE). That matches a 10:00 autumn sun at 32° N reasonably.
- The day sky is rotated -1.11 "so the sun matches".

**Change:**
- Verify once: render a debug marker at `sun.position - sun.target.position` on the sky sphere in the `view`
  direction, and check that it sits on the brightest part of the sky photo.
- Fix the comment (40°, not 45°), or raise the sun to 45° if the photo sun is higher.
- Use the same vector for the item 4 and 5 bakes, so the light, the sky, the projected building shadows and the
  painted balcony shadows all agree.
- Optional desktop-only: screen-space sky rays (24 to 48 samples, half resolution, sky mask) only when the sun is on
  screen, which it rarely is in these views. Low priority.

**Cost:** about 0. **Risk:** none.

### 14. Far-ring blocks as a backplate (gain low-medium, cost low)

**Fake:** the 150 to 300 m blocks (line 1980 onward) are the same painted boxes, just smaller, with crisp edges at
distance.

**Change:**
- Once item 1 is in, the fog does most of the work.
- Optional: replace the blocks beyond about 150 m with the skyline ring from item 1.
- Only if a real skyline photo strip is available (CC0, or the owner's own panorama from the balcony, which would be
  the best match).

**Cost:** fewer draw calls and triangles. Download about 150 to 250 KB. **Risk:** low.

### 15. Hamra soil (pending)

Photos show orange hamra on the lot north of the school. The model keeps neutral `park_dirt` until the owner confirms
(PROJECT_MEMORY open question). Not ranked. It is a one-line tint (`mSoil.color`) once confirmed.

## 5. Coverage checklist

| Topic | Item |
|---|---|
| Building facades: depth, balconies, materials, interior mapping | 4, 11, 12 |
| Our own shell in bird views | 6 |
| Sky, HDRI, sun consistency | 3, 13 |
| Haze and aerial perspective | 1, 14 |
| Trees (impostors vs cards) | 7 |
| Ground: grass, pavers, asphalt PBR | 2, 8 |
| Cars | 10 (plus 3, 5) |
| Street furniture: poles, lamps, fences | 5 (pole shadows), 9 (lamp pools), 8 (decals) |
| Balcony: railing, deck, plants, egg chair | 6 (deck tile is the ceramic picker's; plants are fine) |
| Eve: lit windows, street lights | 9 |
| Outdoor shadows | 5, 4 (baked facade shadows) |

## 6. Budget summary (estimates)

| Item | Desktop frame | Phone frame | Download |
|---|---|---|---|
| 1 Haze and horizon | about 0 (sky last saves 4 to 8%) | about 0 | 0 to 150 KB |
| 2 Ground mask | under 0.3 ms | under 0.3 ms | 0 |
| 3 Sky env | 0 (load +50 ms) | 0 | 0 |
| 4 Facade atlas v2 | 0.1 to 0.3 ms | 0.1 to 0.3 ms | 0 (canvas) or about 0.5 MB |
| 5 Contact shadows | about 0.2 ms | about 0.2 ms | 0 |
| 6 Shell stucco | 0 | 0 | 0 |
| 7A Tree normals | 0 | 0 | 0 |
| 7B Impostors | 0.3 to 0.6 ms | 0.3 to 0.6 ms | +0.5 to 1 MB net (lazy) |
| 8 Pavers and decals | about 0.1 ms | about 0.1 ms | about 400 KB |
| 9 Eve | about 0.1 ms | about 0.1 ms | 0 |
| 10 Cars (b) | about 0.2 ms | (a) on phones | 300 to 600 KB (lazy) |
| 12 Interior mapping | 0.3 to 0.8 ms | 0 | 300 to 500 KB (lazy) |

Items 1 to 6, 7A and 9 together add no download and roughly 0.5 ms per frame on a phone. That is the recommended
first pass. Items 7B, 8, 10b and 12 need about 1.5 to 2.5 MB. Either free it first or lazy-load it on desktop after
the first frame, so the initial download stays at about 12 MB:
- recompress the tree card atlases, which are replaced by 7B anyway;
- check `vendor/` for unused addons.

## 7. CC0 asset wants (for the parallel sourcing agent; target sizes)

| Want | Source to try | Target |
|---|---|---|
| Interlocking concrete pavers, grey-pink (colour, normal, roughness) | ambientCG PavingStones series, Poly Haven paving sets | 1024 desktop, 512 phone, WebP, about 250 KB set |
| Concrete kerb or cast-concrete | ambientCG Concrete, Poly Haven concrete | 512, about 100 KB |
| Exterior plaster or stucco (for the facade atlas base and the shell) | Poly Haven `white_plaster`, ambientCG Plaster | 1024, about 150 KB (or reuse the shipped `white_stucco`) |
| Cream limestone cladding (school, stone blocks) | ambientCG/Poly Haven stone wall tiles | 1024, about 200 KB |
| Roller shutter, aluminium window, AC condenser textures (to paint the atlas) | ambientCG metal and plastic sets, or model in Blender | 512 each, used only at bake time |
| Partly cloudy cumulus HDRI matching the photos | Poly Haven puresky set (for example `kloofendal_48d_partly_cloudy_puresky`) | 512 px equirect for PMREM, plus the existing 4096x1152 backdrop if replaced |
| Hazy suburban skyline strip for the horizon ring | CC0 photo strip or an owner panorama | 2048x256 WebP with alpha, about 150 KB |
| Olive tree and a second Mediterranean street tree (for impostors) | Poly Haven tree models (island_tree series is already used) | source models only; impostor atlas 2048 desktop / 1024 phone, about 400 to 600 KB per species |
| Realistic low-poly cars: hatchback, SUV, van | CC0 glTF realistic cars (avoid stylised kits) | 5 to 15k triangles each, meshopt, 512 WebP, about 150 to 250 KB each |
| Rattan or wicker weave (egg chair, optional) | ambientCG Wicker | 512, about 80 KB |
| Asphalt decals: patches, manholes, worn lines | ambientCG decals, or generated | one 1024 alpha atlas, about 150 KB |
| Room interiors atlas for interior mapping | bake from the apartment model in Blender (no download needed) | 2048x1024 desktop only, about 400 KB |
| Grey-frame balcony railing alpha | generated in canvas | 256, 0 KB |

Generated in JS at load (no asset needed): fog, ground macro mask, blob and pool radial textures, the `litTex` v2
window maps and the canvas facade atlas.

## 8. Order of work

1. Items 1, 3 and 13 together: haze, sky env, one sun vector. Then reshoot `view`, `c_far`, `c_street`.
2. Items 5 and 2: shadows and ground.
3. Items 4 and 6: facades and shell. Then reshoot every exterior view and the window views.
4. Item 9: eve.
5. Item 7A, then 8 and 11.
6. Desktop-only, lazy-loaded: 7B, 10b, 12.

After any of these, the exterior gallery renders and the Cycles exterior frames go stale. Note that in
PROJECT_MEMORY and the README limits, per the workflow.
