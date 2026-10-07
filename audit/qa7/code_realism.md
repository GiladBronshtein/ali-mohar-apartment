# QA7: code review and realism (code_realism)

Scope: `source/salon.html` as a whole, with the diffs of 7289e1d (QA6 stage A), 51071c4 (QA6 stage B) and e94c72c
(fixture picker). Live site on http://localhost:8000/ (built from the committed `salon.html`). Shots in
`source/out/qa/qa7_cr/` (10 views, day and eve) and `source/out/qa7_code_realism/shots/`; probes in
`source/out/qa7_code_realism/all.mjs` (log `all.log`). Defect crops in `audit/qa7/code_realism_img/`.
Line numbers are `salon.html` as of e94c72c (3365 lines).

Checks run from `source/`: `python3 roomdims.py` +0 on every room (closet 485/175 is the known probe artifact);
`python3 clearance_audit.py` 0 issues (but see finding 10: it does not look at the model).

## Part 1: code review

1. **Fixtures in `fixRoot` keep box UVs: the tub apron tiles are squashed, wood grain is mis-scaled (default view).**
   CONFIRMED. `mergeGroup()` (line 2485) is what writes world-space UVs for every material with `userData.uv`
   (line 2494). `fixRoot` is never merged, so since e94c72c every fixture mesh uses the raw BoxGeometry UVs: one full
   texture repeat per face, whatever the face size. Probe: 10 fixture meshes use a `userData.uv` material, all with UV
   max 1.0 (the apron box is 0.70 x 0.40 x 1.59 m but carries one 1.2 m repeat per face). Visible by default:
   the family bath tub apron (`mat.bathWall2`, `fixTub`, line 767) shows thin stretched stripes next to the
   correctly tiled wall (`code_realism_img/01_tub_apron_box_uv.jpg`, camera pos [3.05,1.25,-1.55] tgt
   [4.1,.42,-2.3]); the master vanity walnut (`mat.walnut`, line 1620) and every oak front (`mat.oak` in `fixVanity`
   and `vanCol('עץ אלון')`) get one 0.8 m grain repeat squeezed into strips 0.04 to 0.14 m high (`06_walnut_box_uv.jpg`).
   A ceramic pick for the family bath walls also lands on the apron with the wrong grid and no corner offset.
   Fix (also fixes finding 7): merge each slot after it builds. In `fixDraw` (line 707), after the `try/finally`:
   ```js
   mergeGroup(s.g);   // world UVs (userData.uv) + one draw call per material
   s.g.children.forEach(o => { if (BACK.has(o.material)) { o.receiveShadow = false; noAO.push(o); } });
   ```
   with `const BACK = new Set([mTubIn, mSinkIn, mSilqIn])` next to line 668, and drop the per-mesh `noAO.push` /
   `receiveShadow = false` in `fixTub` and `fixKSink`. `mergeGroup` works on any group (it uses world matrices; `s.g`
   sits at identity under `fixRoot`).

2. **A vanity colour picked after load has the wrong environment strength (glows at night).**
   CONFIRMED. `vanCol()` (line 799) creates its material on first use, after the one-time env pass at line 2871. Probe
   in eve mode: the new grey vanity material had `envMapIntensity` 1 (should be .12 at eve, .3 by day) and
   `dithering` false; only the next day/eve toggle fixes it (it read .3 after `setMode(false)`). So a vanity picked in
   the evening is lit by the environment about 8x too strongly. Fix: in the fixture `set()` handler (line 3334), after
   `FIXS.filter(...).forEach(fixDraw)`, add
   `fixRoot.traverse(o => { if (o.isMesh) { const m = o.material; m.envMapIntensity = isEve ? .12 : (m.userData.envDay ?? ENV); m.dithering = true; } });`.
   Do not put this in `fixDraw`: `fixDraw` also runs at build time (line 1476 on), before `const ENV` (line 2570), and
   would throw a TDZ ReferenceError at load.

3. **Rounded tub (`tub` = מעוגלת): the basin floor z-fights with the apron block.**
   CONFIRMED (`02_round_tub_bottom_zfight.jpg`, pos [4.11,1.45,-1.75] tgt [4.11,.4,-2.35]). In `fixTub` (line 771)
   the back-face RoundedBox is .18 high centred at .49, so its floor is at y .40, the same plane as the top of
   `B(X1, X2, Z1, Z2, 0, .40, mat.bathWall2)`. From above the apron's tile texture shows through as stripes across
   the basin. Its long sides also sit exactly on the ring's inner faces (x1, x2). Fix:
   `mesh(new RoundedBoxGeometry(x2 - x1 - .004, .17, z2 - z1 - .004, 4, .085), mTubIn, root, false)` at
   `y = .495` (floor at .41, like the rectangular basin floor), or end the apron block at .395.

4. **Top-mount kitchen sinks (נירוסטה, סיליקוורץ): bowl walls z-fight with the sink cabinet rim.**
   CONFIRMED (`03_topmount_sink_zfight.jpg`, pos [5.25,1.45,7.75] tgt [5.25,.8,8.45]): dark jagged streaks on the
   side walls and a dark band on the back wall. `fixKSink` (line 783) makes the bowl exactly `b-a` x `d-c`, so its
   walls lie on the planes x = SK1+.05, SK2-.05 and z = 8.24, 8.69, which are also the faces of the graphite carcass
   rim added in 7289e1d (line 1472, `B(..., .69, .88, mat.graphite)` "sink cabinet open under the bowl") and of the
   counter edges. Fix: inset the bowl by 3 mm a side:
   `new RoundedBoxGeometry(b - a - .006, .2, d - c - .006, 4, q ? .07 : .05)`. Also the rounded bowl leaves open
   corners against the square hole; the rim (`w` .03/.045) is outside the hole, so add a 1 cm inner lip:
   `[[a, b, c, c + .01], [a, b, d - .01, d], [a, a + .01, c, d], [b - .01, b, c, d]]` at .918 to .928.

5. **Mamad: contact shadows are hidden under the raised floor (since 7289e1d).**
   CONFIRMED by code and measured. 7289e1d raised the mamad floor, its wardrobe niche and the door strip to y .02
   (line 1041, `floor(..., mat.tile, .02)`), but contact region 0 still draws its plane at y .014
   (`contacts`, line 2515, `y: .015`, plane at `r.y - .001`). The plane is depth-tested, so it sits under the mamad
   floor. On/off diff of the contact plane: mamad mean 0.25, max 23 grey levels; room 2 mean 0.62, max 58 (shots
   `mamad_contact_on/off.jpg`, `room2_contact_on/off.jpg`). The desk feet, chair base and bed in the mamad stand on the
   floor with no grounding. Fix: a third region for the mamad,
   `{ x1: -3.85, x2: -.20, z1: -.52, z2: 2.80, y: .026 }`, and keep region 0's mask from drawing there (its mask
   camera at .02 coincides with the mamad floor plane; give the mamad floors a small `.0205` and leave the mask
   camera at `r.y + .005` so region 0 masks them out cleanly).

6. **Spec vanities are centred off the plumbing axis and off the mirror cabinet.**
   CONFIRMED (code arithmetic, `04_family_vanity_basin_off_axis.jpg`). `fixVanity` puts the basin and mixer at
   `zb = zc` (line 802; `zs = z2` except Roma). Family bath: called with `zc = -2.185` (line 1702), the old 100 cm
   cabinet centre, so the basin axis is 79 cm from the corridor wall instead of the written 72 (the drawn design and
   the mirror cabinet use -2.115) and sits 7 cm north of the mirror cabinet axis. Master bath: zc -3.73 (+.06 shift)
   puts the basin 41 cm from the south wall instead of the written 44 and 4 cm off the mirror. Fix: add the axis as a
   parameter, `function fixVanity(x0, zc, W, topY, key, tap, axis = zc)`, use `zb = st === 'shelf' ? (z1 + zs) / 2 : axis`,
   and call it with `fixVanity(2.01, -2.115, W, .85, v, t)` in the family bath (60 and 80 both fit: z -2.515..-1.715)
   and `fixVanity(4.44, -3.73, .70, .83, v, t, -3.76)` in the master bath (the 70 body cannot move north: the shower
   frame is at z -4.035).

7. **The fixtures added up to 121 draw calls (58 in the `bath` view, +36 %).** CONFIRMED (see the count below). Before e94c72c these
   meshes were merged into the per-material root meshes; now each box is its own draw call in the main pass, the
   GTAO normal pass, the mirror passes and the contact capture. Phones run without the composer, but still pay the
   main pass. Fix: finding 1 (merge per slot) brings it back to one call per material per slot.

8. **`noAO` grows on every rebuild.** CONFIRMED by code. `fixTub('מעוגלת')` and `fixKSink` push the new basin into
   `noAO` (lines 771, 783) each time they build; `fixDraw` removes the old mesh but never takes it out of `noAO`,
   so every pick of those options leaks one mesh (geometry disposed, object kept) and grows the list GTAO walks every
   frame. Fix: in `fixDraw`, before rebuilding,
   `for (let i = noAO.length; i--;) { let p = noAO[i]; while (p && p !== s.g) p = p.parent; if (p === s.g) noAO.splice(i, 1); }`.

9. **"חזרה למצב המקורי" runs up to 12 rebuilds and 12 contact captures in one click.** SUSPECTED (not timed).
   `cerReset` (line 3343) calls `fixSet` per FIX entry; each changed one calls `captureContact()` (two GPU renders
   and `readRenderTargetPixels` of about 600 x 1200 px per region, plus CPU blurs) and flags the shadow map.
   Fix: let `set()` take a `batch` flag, collect the dirty slots, then call `captureContact()` and
   `renderer.shadowMap.needsUpdate = true` once at the end of `cerReset`.

10. **`clearance_audit.py` does not see the fixtures at all, and two of its numbers are stale.** CONFIRMED. The
    script never reads `salon.html` or the live scene: every footprint is typed in (`R = {...}`, lines 3-14). So the
    move into `fixSlot` callbacks changed nothing for it, and it checks only the default shapes. Stale values: line 52
    `family WC centre <-> window wall` uses -3.38 and -3.80 (0.42); the model has the WC centre at -3.335 and the wall
    at -3.775, so 0.44, which is the value re-check 2 found written (`audit/recheck2/APPLIED.md` line 42). `'fb wc'`
    (2.16, 2.71, -3.56, -3.20) vs model (2.19, 2.74, -3.515, -3.155). I checked the deepest variants by hand
    (Metropol front at local z .31): family WC to tub 0.99, master WC front 1.00, both still over 0.6. Fix: update the
    two entries; better, export the fixture boxes from the page (`fixRoot` bounding boxes per slot) to JSON with
    Playwright and let the script read them, for every option.

11. **Stale comments and text.** CONFIRMED.
    - Line 1692: "centre 42 cm from the window wall": the model and the written value are 44.
    - Line 1276: "two 90 cm fluted walnut storage towers": they are grey (`mat.fluteGrey`, `mat.fluteBack`), as the
      panel says.
    - Panel "קיר הטלוויזיה" says the wall starts 8 cm after the corridor passage; the model has `MX1 = 3.05` and the
      passage ends at 3.00 (line 1091): 5 cm.
    - `ceilingFan(x, z, h)` (line 978) is called with a fourth argument (`mat.walnut`, `mat.oak`, lines 1556, 1764,
      1787) that it ignores.
    - `DESIGN.md` lines 151-152 still say the ceramic choices persist in localStorage `ali-cer`; it has no section on
      `fixRoot` / `fixSlot` / `fixDraw` / `FIX`, and its "Test hooks" list lacks `FIX`, `fixSet`, `fixState`, `fixRoot`.
    - `exportglb.mjs` exports `fixRoot` but does not rename its meshes (`m_` prefix) and the fixture materials
      (`FINM.chrome`, `brushed`, `gold`, `vanCol`, `mSilq`, `mTubIn`, `mSinkIn`) have no `name`, so `cycles_render.py`
      (material lookup by name, line 28) gives them its default shader. `lm/export.mjs` (line 30) and the bake target
      list (line 2666) skip `fixRoot`, so `?baked=1` leaves the fixtures real-time lit and the bake has no fixtures
      as occluders.

12. **`fixDraw` has no catch.** SUSPECTED (no failing input found). `set()` writes `fixState[id]` before the redraw;
    if a builder throws (for example an unknown vanity name reaching `VANS.find(...)[2]`), the slot stays half built,
    the state claims the new key, and the shadow and contact refresh are skipped. Fix: `try { s.build(...) } catch (e)
    { console.error(e); } finally { root = r; }` and write `fixState` only after a successful draw.

13. Minor: the top-mount sink rim (`fixKSink`, line 782) runs to z 8.72 / 8.735 and the kitchen tap base (radius
    .028 at z 8.74, line 796) cuts through it. SUSPECTED visually small. Fix: move the tap base to z 8.755 when a
    top-mount sink is picked, or stop the back rim at `d + .02`.

Draw-call count (finding 7), measured (`source/out/qa7_code_realism/count.mjs`): `fixRoot` holds 121 meshes using 10 materials (the whole merged `root` is 151 meshes). In the `bath` view with HQ off, 221 draw calls with the fixtures, 163 with `fixRoot` hidden. After a per-slot merge it would be about 25 meshes in total.

### Checked and fine (part 1)

- Code hidden after `//`: scanned every comment in the module for calls, assignments and `);` patterns. None left.
  The laundry niche floor line (1047) has two comments in a row, harmless.
- TDZ at load: `fixSlot` first runs at line 1476; everything it touches (`FIX`, `fixState`, `tapOf`, `TAPS`, `FINM`,
  `noAO` at 297, `paint` at 1651, `ceramicTop`, `shaker`, `fanGroup` at 977 via `withShift`) is defined before. The
  only hazard is the one in finding 2 (do not use `ENV` inside `fixDraw`).
- `root` swap: `B`, `C`, `Sph`, `mesh`, `place`, `withShift` read `root` at call time, so slots build into their own
  group and nested `withShift` shifts only the slot (no double shift: the outer blocks capture the main root). Head,
  rail, mixer, WC and flush in the master bath (.19, 0), family WC and flush (.14, -.13) and the master vanity (.19,
  .06) match the pre-e94c72c positions. `captureContact` (2545, 2549), the bake list (2666), the path tracer glass
  toggle (2902), `extMats` (2467), `__app.root` (3364) and `exportglb.mjs` all run after the build and see the main
  root; `fixRoot` is added explicitly to the contact capture and the export.
- Materials per rebuild: none created except the cached `vanCol` ones; `FINM`, `mSilq`, `mTubIn`, `mSinkIn` are made
  once. `fixDraw` disposes every geometry it removes.
- Persistence: the only storage call left is `localStorage.removeItem('ali-cer')` (line 3355). No writes.
- Fixture UI: invalid keys fall back to the default (`sel.value` check), every FIX `view` exists, and arrow keys in a
  focused `<select>` do not walk the camera (line 2802).
- 51071c4: the new outside materials (`mStuccoOut`, `mPaverBay`, `mFenceBar`, block materials) are created once and
  are in the site patch list where needed (line 2440).
- `roomdims.py` +0, `clearance_audit.py` 0 issues; the WC variants keep the hand-checked clearances.

## Part 2: realism

### What the views show (shots `source/out/qa/qa7_cr/desktop_<day|eve>_<view>.jpg`)

- Day interiors read flat and evenly grey. `entry`, `sofa`, `kitchen`: walls and ceiling have almost the same value
  everywhere; light does not fall off from the glazing into the room, and the far corners are as bright as the
  window side. The fill comes from a uniform hemisphere (.22) plus a generic studio environment
  (`RoomEnvironment`, line 277, at `ENV` .3) that is the same in every room.
- No sun in the living room or kitchen is right (the balcony slab shades the east glazing at 10:00). The master's
  east window does get a sun patch (visible in `bird1`), hidden behind the bed in the `master` preset.
- Metals and gloss reflect an unrelated studio: black taps, the shower frame and chrome have the same soft grey
  highlights in every room; the floor porcelain shows no window reflection at all.
- Contact and ambient occlusion: GTAO is subtle (radius .45); the contact plane helps under the sofa and beds but
  is weak (room 2 on/off diff 0.6 grey levels on average). The wall-hung WCs, the beds and the bath cabinets still
  look placed rather than resting, and inside corners (ceiling to wall, cabinet to wall) carry almost no darkening.
- Eve: the warm point lights hang 0.30 m under the ceiling (line 2593) and light the ceiling as strongly as the
  floor, so every ceiling glows cream (`desktop_eve_entry.jpg`, `desktop_eve_kitchen.jpg`). Recessed downlights do
  the opposite: dark ceiling, pools on the floor, scallops on the walls.
- Eve glazing is fully clear: from the sofa the balcony and street show as by day, with no reflection of the lit room
  (`05_eve_glazing_no_reflection.jpg`). At night large glazing reads as a dark mirror; this is one of the strongest
  "real photo" cues in evening interiors.
- Outside: the blocks are boxes with a painted window atlas; from `view`, `balcony` and through every window they read
  as game assets (no window depth, no glass reflection, identical white).
- Fabric: the sheers are bright vertical strips with no translucency gradient; the leather sofa reads well.
- Scale cues: good (switches, sockets, grilles, books). Clutter is thin in bathrooms (no towels on the vanities, no
  toiletries) and on the kitchen counters, which is a design choice, not a defect.

### The 10 highest-value improvements, in order

Costs are estimates for this Mac (desktop HQ) unless measured. "Safe now" = a code-only change that can be shipped
after the usual checks and a day/eve/phone look, with no new asset pipeline.

1. **Eve: make the ceiling lights downlights (lobed point lights).** SAFE NOW.
   Gain: high for every eve view: ceilings fall dark, floors get pools, walls near the lights get scallops; this
   is most of what separates a lit interior photo from a CG one. Runtime: about 5 ALU per point light per pixel,
   no download. Plan: the room-gate patch already rewrites `lights_fragment_begin` (lines 2600-2607). Add a const
   array of light positions and a down flag next to `pointBox`, then after `getPointLightInfo(...)`:
   `vec3 Lw = normalize( gateW - pointPos[ i ] ); directLight.color *= mix( 1.0, .06 + .94 * smoothstep( .35, .8, -Lw.y ), pointDown[ i ] );`
   Flag the recessed and surface downlights (living spots, corridor and entry cylinders, kids' bath); leave the
   pendants (frames over the island, wave, bedside globes) omni. Move those lights up to `H - .05` so the lobe starts
   at the fixture. Keep `throw` guards as now. Check the exposure band (mean brightness 0.95-1.10 of the current eve).

2. **A scene-matched interior environment (baked probe), box-projected in the living space.** NOT SAFE NOW (needs
   a Cycles render). Gain: high: taps, frames, the black kitchen, ceramic, glass, the TV and the floor sheen reflect
   the real windows and room instead of a studio; fixes the eve metals that now go near black at `ENV` .12. Runtime:
   one extra PMREM texture (about 2 MB GPU), box projection about 10 ALU on glossy pixels; download about 150 KB per
   probe as RGBE PNG or 8-bit WebP with a scale. Plan: add a `pano` mode to `cycles_render.py` (camera
   `type = 'PANO'`, `panorama_type = 'EQUIRECTANGULAR'`, 1024 x 512, the current day and eve rigs) and render three
   probes from `apartment.glb`: living (pos [3.6, 1.4, 4.4]), master bath, family bath, day and eve. Publish to
   `assets/env/`. In `salon.html`, load them like the photo skies (the sky loader block that ends at line 2470), `pmrem.fromEquirectangular`,
   and set `m.envMap` on the interior materials (the `inside` set already built at line 2467, minus `extMats`);
   switch day/eve in `setMode` next to the `extEnv` swap (line 2860). Box projection for the living probe: patch
   `envmap_physical_pars_fragment` (reflect vector against the box [-.05, 7.28] x [0, 2.70] x [-.05, 8.79]) in an
   `onBeforeCompile` on the living materials only, with a `throw` guard like the room gate. Do not capture a cube
   in the browser (the skill measured 8 s of shader recompiles).

3. **Daylight balance: less uniform fill, more directional window light.** SAFE NOW (tuning, needs a look).
   Gain: medium-high: gradient from the glazing into the room, darker far corners, depth in `entry`, `sofa`,
   `kitchen`, `master`. Runtime: none. Plan: `HEMI` .22 to about .12 and the interior `ENV` .3 to about .2
   (line 2570); window lights (`winLight`, lines 2579-2591) up by 25-35 % and tilted 15 degrees down
   (`l.lookAt(lookX, y - .8, lookZ)`), so the floor near the glass is brighter than the ceiling, as with a real
   sky. Compensate with `EXPO.day` (line 256) to hold mean brightness in 0.95-1.10 of today. Review with the
   skill's before/after side by side on `entry`, `kitchen`, `master`, `room2`, `bath`, plus phone.

4. **Eve glazing as a dark mirror.** SAFE NOW for the cheap version, better after item 2. Gain: high in eve
   `entry`, `kitchen`, `sofa`, `master`. Runtime: none (one material). Plan: in `setMode` (line 2853) switch
   `mat.glass` at eve to `opacity .28`, `color #10151a`, `envMapIntensity 1.0` (now .12 for every material), and
   give it a Fresnel lift with `onBeforeCompile` (`gl_FragColor.a = mix(opacity, .75, pow(1. - dot(n, v), 4.))`).
   With the item 2 probe as its env map the glass shows the lit room; until then it shows `RoomEnvironment`, which
   still beats clear glass. Keep `depthWrite false`.

5. **Re-bake and use only the baked AO and indirect light on the real-time materials.** NOT SAFE NOW (re-bake).
   Gain: high: contact darkening in corners, under cabinets, behind the WCs and beds, the ceiling-wall line; works on
   phones where GTAO is off. Runtime: one texture fetch per pixel; about 1.3 MB download already budgeted (`lm/`).
   Plan: the geometry changed since the bake (2.70 ceiling, re-check 5, QA6), so `LM.missed` would be high: re-run
   `lm/export.mjs` (add `['fix', A.fixRoot]` to its group list, line 30, after finding 1 merges the slots),
   `lm/bake.py` at 2048 with two atlases (ceilings at 2 cm per texel), `lm/publish.py`. Then a new mode beside
   `bakedMaterial` (line 2616): keep real-time direct light, set `aoMap = bakedAoMap` with `aoMapIntensity .7` and add
   `.4 x` the natural indirect pass to `irradiance`. Make it the default only after a day/eve look.

6. **Facade depth on the residential blocks.** SAFE NOW (shader on one material set). Gain: medium-high for `view`,
   `balcony`, `balcony2`, `bird1/2` and every window view: windows read recessed with a dark glass and a sky
   reflection instead of painted squares. Runtime: one extra atlas fetch and a few ALU on facade pixels only. Plan:
   in `facadeAtlas()` (line 2260) draw a second channel with the window mask; in the facade shader offset the
   UV by `0.02 x viewDir.xy / viewDir.z` inside the mask (one-step parallax), darken the inset reveal, and mix in
   `extEnv.day` along the reflected view vector with Schlick F0 .04 on the glass.

7. **Contact shadows: fix the mamad and make them stronger near the contact.** SAFE NOW. Gain: medium: beds, desks,
   chairs and the WCs sit on the floor. Runtime: none per frame (the capture is static). Plan: finding 5 (third region
   for the mamad), then in `captureContact` (line 2558) weight the tight blur more (`tight * .7 + wide * .3`) and raise
   the plane opacity from .6 to .75 by day (line 2521), keeping .6 at eve. Add `fixRoot` meshes after finding 1 so
   the WC bowls cast their own small contact under the wall-hung pan (they are 24 cm up, so they fall into the 35 cm
   window already).

8. **Softer, contact-hardening sun shadows.** NOT SAFE NOW (shader patch on the shadow chunk, needs measuring).
   Gain: medium on the balcony, `view`, `bird1`: the railing stripes are razor sharp and evenly dark up to 3 m from
   the bars; real sun shadows soften with distance. Runtime: PCSS with 16 blocker and 16 filter taps, about +1 ms on
   this Mac on sunlit pixels only (the shadow map stays static). Plan: patch `shadowmap_pars_fragment` with the
   three.js PCSS example code for the sun only (light size about 0.5 degrees), guarded by a chunk check like the room
   gate; keep PCF on phones.

9. **Sheer curtains that transmit light.** SAFE NOW. Gain: medium in `entry`, `kitchen`, `sofa`, `master`, where
   the sheers fill a large part of the frame. Runtime: small. Plan: the sheers (`sheer` material, line 1229) get a weave normal (Poly Haven `fabric_pattern_05` or ambientCG `Fabric048`, both CC0, normal and
   roughness only, 1k WebP into `assets/tex/`), `transmission`-like back lighting by an emissive term scaled by
   `max(0, dot(-N, windowDir))` (window side brighter), and opacity varying with the fold normal (thicker at the
   folds). Keep `depthWrite false`.

10. **Subtle grade and highlight roll-off.** SAFE NOW (taste call for the owner). Gain: medium: today's day frames
    are cool grey with clipped whites on the ceiling; a mild warm-highlight, neutral-shadow grade and a softer
    shoulder read as photographed. Runtime: one LUT lookup in the existing `OutputPass` (about 0.2 ms at 1.5 DPR).
    Plan: add three's `LUTPass` before `OutputPass` (line 300) with a small 32^3 `.cube` made from a neutral LUT
    (warm +3 % in the top quarter, saturation -5 % in the shadows), day only; phones skip it with the composer.
    Compare against today with the mean-brightness band.

Not in the 10, worth noting: lacquered spec vanities could use `phys()` with clearcoat like the kitchen fronts
(`vanCol`, line 799, uses plain `M`); a few CC0 props (towels on the vanities, a soap dish) would add scale and life
in `bath`, `mbath`; the `master` preset could show the sun patch if its target moved to [8.0, .4, -2.6].
