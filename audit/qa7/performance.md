# QA7: performance

Scope: load and frame cost on this Mac (Apple M4, Metal through ANGLE, Playwright Chromium, every run through `/tmp/gpu.sh`),
for desktop HQ (1440x900 at DPR 1, and at DPR 2 as on a Retina Mac), desktop with HQ off, phone emulation (375x812, DPR 3,
Pixel 7 user agent, touch) and the same phone with 4x CPU throttling. Then a profile of where the time goes and a prototype of
the biggest fix in a copy of `index.html` served from `/tmp/qa7perf` on port 8795 (server stopped afterwards). Scripts and raw
JSON: `source/out/qa7_performance/` (`load.mjs`, `frames.mjs`, `prof.mjs`, `analysis.mjs`, `abshots.mjs`, `*.json`).

Line numbers are `source/salon.html` at 3d9e6dc. The measurements ran on the built site while feda3a7 and 3d9e6dc landed;
the light-cost finding does not depend on those commits (the light setup and the room gate did not change).

Method for frame time: the app loop is paused (`window.__pause`), the camera is nudged 0.1 mm per frame so `frame()` takes the
"moving" branch (full composer in HQ), `renderOnce()` then a 1-pixel `readPixels` to wait for the GPU, 8 warm-up frames,
median of 40 (20 or 12 in the variant runs). The machine was shared with other QA agents (load average about 7), so single runs
move by up to 30%. Compare numbers inside one run, not across runs.

## Measured state

| | Desktop HQ @1 | Desktop HQ @2 (Retina) | Desktop, HQ off | Phone | Phone, CPU 4x |
|---|---|---|---|---|---|
| Drawing buffer | 1440x900 | 2160x1350 | 1440x900 | 375x812 (DPR forced to 1) | same |
| Ready (loading hidden), cache off | 3.0 s | | 3.0 s | 2.0 s | 4.8 s |
| First frame shown | 4.5 s (first tick 1.06 s) | | | 2.8 s | 6.7 s |
| Download, requests | 11.85 MB, 109 | | | 11.37 MB, 86 | 11.37 MB, 86 |
| JS heap after load | 102 to 120 MB | | | 86 to 133 MB | |
| Programs | 69 at load, 79 after 8 views | | | 48 | 49 |
| Draw calls entry / kitchen / master / top / bird1 | 714 / 813 / 428 / 900 / 818 | same | 356 / 407 / 215 / 464 / 411 | 166 / 272 / 154 / 451 / 434 | same |
| Triangles entry / master / top | 0.30 M / 0.64 M / 0.68 M | | | 0.13 M (entry) | |
| Forced frame, mean of 8 poses (day / eve) | 175 / 159 ms | 313 / 347 ms | 122 / 120 ms | 23.6 / 22.8 ms | 27.6 / 36.4 ms |
| Worst pose | kitchen 229 ms | kitchen 383 ms | kitchen 178 ms | kitchen 26 ms | kitchen 35 ms |
| CPU part of a frame | 8 to 15 ms | 6 to 13 ms | 5 to 9 ms | 4 to 6 ms | 6 to 14 ms (eve 12 to 20) |
| rAF fps while turning at entry | 6.1 | 3.1 | 9.3 (eve 7.6) | 56.8 | 51.4 (eve 41.5) |

Download per type (desktop): PBR WebP 5.1 MB (29 files), GLB 2.4 MB (7: two balcony plants 1.95 MB, kitchen props), JS 1.85 MB
(26 files, `three.module.js` 1.24 MB), tree atlases 1.5 MB, `index.html` 345 KB, fonts 120 KB, skies 176 KB.

GPU memory (estimate from sizes): sun shadow map 134 MB (4096², RGBA8 plus depth; phone 2048², 34 MB); each live mirror
59 MB (1024², half float, 4x MSAA colour and depth; four mirrors, allocated when first seen); textures 181 objects. The sky
is 4096x1152 (25 MB with mips), the three tree atlases 10 to 14 MB each.

Compared with PROJECT_MEMORY and `audit/qa6/code_geometry_perf.md`: draw calls fell from 1451 to 714 at `entry` (the QA6
material hoist worked: 251 materials, 215 distinct looks, was 794 materials). Ready is faster than QA6's 7.4 s (3.0 s here,
measured from navigation, cache off). Frame rate did not improve: QA6 read 9 to 13 forced fps on desktop HQ, this run 6 to 8.
The cause is not draw calls (CPU is 10 ms of a 175 ms frame); it is the fragment shader (finding 1).

## Findings

1. **The window and lamp lights make every pixel about 6x more expensive than it needs to be.** CONFIRMED (measured, desktop
   HQ off, same session, mean of 6 poses):

   | Variant | Mean frame |
   |---|---|
   | as built | 164 ms |
   | 9 RectAreaLights hidden | 25 ms |
   | 14 point lights hidden | 51 ms |
   | both hidden | 18.5 ms |
   | sun shadows off | 128 ms |
   | outside group hidden | 121 ms |
   | contact planes hidden | 116 ms (noise level) |
   | HQ: GTAO off / bloom off | 110 / 164 ms vs 119 base (noise level) |

   The frame scales with pixel count (phone 0.3 MP 23 ms, desktop 1.3 MP 122 ms, Retina HQ 2.9 MP 313 ms), so it is fragment
   bound. Every lit fragment (walls, floors, furniture, and also the street, lawns and blocks) runs 9 unrolled LTC area-light
   evaluations and 14 point-light BRDFs. The room gate (lines 2633-2643) multiplies each light's colour by 0 outside its room
   but still runs the full light code, and by day the 14 warm point lights are at intensity 0 (`setMode`, line 2896) yet still
   evaluated; at night the sun (intensity 0) still takes its PCF soft-shadow taps. Post passes, mirrors, contact shadows and
   draw calls are small next to this.

   Fix (prototyped and measured): skip a light whose colour is zero after the gate, and skip a directional or point light (and
   its shadow taps) when both normals face away from it. Insert after the room gate block, before the `// BAKED LIGHT` header
   (after line 2643):
   ```js
   { let ch = THREE.ShaderChunk.lights_fragment_begin; const P = (a, b) => { const n = ch.replace(a, b); if (n === ch) throw new Error('light skip: chunk changed'); ch = n; };
     P('IncidentLight directLight;', 'IncidentLight directLight;\n#ifdef STANDARD\n#define FACES_LIGHT ( max( dot( geometryNormal, directLight.direction ), dot( geometryClearcoatNormal, directLight.direction ) ) > 0.0 )\n#else\n#define FACES_LIGHT true\n#endif\n#define LIT_ ( FACES_LIGHT && dot( directLight.color, vec3( 1.0 ) ) > 0.0 )');
     P(/\( directLight\.visible && receiveShadow \)/g, '( directLight.visible && receiveShadow && LIT_ )');
     P(/RE_Direct\( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight \);/g, 'if ( LIT_ ) RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );');
     P('RE_Direct_RectArea( rectAreaLight,', 'if ( dot( rectAreaLight.color, vec3( 1.0 ) ) > 0.0 ) RE_Direct_RectArea( rectAreaLight,');
     THREE.ShaderChunk.lights_fragment_begin = ch; }
   ```
   Result (`proto.html?skip=1`): desktop HQ 144 to 54 ms (entry 127 to 53, kitchen 164 to 59, master 141 to 51), rAF fps
   while turning 6.2 to 21.8; desktop HQ off 103 to 20 ms, rAF 11 to 56 fps. Visual check at fixed poses (entry, master,
   bird1, day and eve, `abshots.mjs`): flat surfaces identical; the only differences are 1 px edge outlines from the TAA
   accumulation state at capture time (mean 0.16 to 0.62%), no shading change. It is exact by construction: a light with zero
   colour or with N.L <= 0 for both normals adds exactly 0 in `RE_Direct_Physical` (diffuse, specular, sheen and clearcoat all
   carry the N.L factor). The patch throws if the three.js chunk text changes.
   Further gain, larger change: in day mode set the warm lights `visible = false` and at night the window lights (the
   "14 point lights hidden" row: three times faster again before the skip). This changes the light count, so every program
   recompiles on each day/eve switch (about 1 to 2 s); only worth it with `renderer.compileAsync` behind a short spinner.

2. **Phones (and desktop with HQ off) render a new frame on every animation frame, even when nothing moves.** CONFIRMED by the
   code: `frame()` line 3037 `if (hq) composer.render(); else renderer.render(scene, camera);` has no dirty or moving check;
   only the HQ branch (lines 3024-3034) stops after TAA. On a phone that is a full scene render 60 times a second while the
   user reads the panel: battery and heat, and on slower phones it competes with touch input. (The idle measurement script
   timed out under the shared GPU lock, so the frame count per second was not measured; the code path is unambiguous.)
   Fix, line 3037:
   ```js
   if (hq) composer.render();
   else { const moving = camMoved() || anim || fansOn || dirty; dirty = 0; if (moving || camera.view && camera.view.enabled) renderer.render(scene, camera); }
   ```
   (Anything that changes the picture already sets `dirty = 1`: setMode, setView, cerApply, loaders.)

3. **Phones draw at DPR 1 whatever the screen.** CONFIRMED: `setHQ(hq)` (line 3395) with `hq = false` on phones calls
   `renderer.setPixelRatio(Math.min(devicePixelRatio, on ? 1.5 : 1))` (line 2865), so a DPR 3 phone renders 375x812 and the
   browser upscales it 3x: soft edges and blurry tile and wood detail. Line 261 sets 1.5 first, then line 2865 overrides it.
   After finding 1 the phone has headroom (emulation 23 ms at DPR 1 before the skip; about 4x cheaper after). Fix: on phones use
   a pixel budget, for example `Math.min(devicePixelRatio, Math.sqrt(1.6e6 / (innerWidth * innerHeight)))` (about 1.6 MP,
   DPR 1.9 on a 390x844 screen), and keep 1 when a first-second frame-time probe is over 40 ms. Quality gain, cost to verify on
   a real phone.

4. **First frame waits on shader compile and texture decode on the main thread.** CONFIRMED (CPU profile of the load,
   desktop, `prof_desktopHQ.json`, inclusive ms): first use of programs (`WebGLProgram.getUniforms` / `onFirstUse`, the
   driver's link stall) 2350 ms; texture uploads that decode WebP and canvases synchronously (`texSubImage2D`) 1160 ms
   (3.2 s with CPU 4x); `cerSet` at load (line 3392: `cerApply` 892 ms, of which `cerTex` 848 ms, nine spaces); contact
   shadow capture 741 ms (of which `readRenderTargetPixels` 494 ms); `photoPBR` / `meanLin` 308 ms; ground mask blur 280 ms;
   `mergeGroup` 162 ms. Ready 3.0 s desktop, first frame shown 4.5 s; phone with CPU 4x 4.8 s and 6.7 s.
   Fixes, by expected gain:
   - `cerSet(sp.id, sp.def)` at load (line 3392) builds a canvas texture set for every space although each default equals
     the built-in material. Skip `cerApply` when the key is the space default and the material is untouched, and build on
     the first pick. Expected about -0.85 s desktop, about -3 s on a slow phone. SUSPECTED that every default maps to the
     original texture: check `CER_SPACES[*].def` against `cur`.
   - Load photo textures with `THREE.ImageBitmapLoader` (decode off the main thread, `imageOrientation: 'flipY'` off and
     `texture.flipY = false`) in `assetTex` (line 307). Expected most of the 1.16 s upload time.
   - Call `await renderer.compileAsync(scene, camera)` once the lights exist (after line 2643), before the contact capture
     and the ceramics setup, so the GPU process links programs while the main thread keeps working. Expected part of the
     2.35 s stall; measure.
   - `oak_veneer_01` and `white_stucco` are loaded and uploaded twice (lines 602-605: `photoPBR` called twice with the same
     id, each call loads its own images). Memoise `assetTex` by path and clone the texture in `photoPBR` (clones share the
     `Source`, so one GPU upload): 5 fewer 1024² decodes and about 28 MB of texture memory.

5. **Live mirrors: 59 MB each and a full scene render each.** CONFIRMED (sizes from the render targets; frame cost within the
   noise of this shared machine: `noMirrors` variant not completed). `reflector()` line 965:
   `textureWidth: 1024, textureHeight: 1024, multisample: 4` on a half-float target for mirrors 40 to 80 cm across, which cover
   at most a third of the screen. Fix: `textureWidth: 512, textureHeight: 512, multisample: 0` (TAA smooths the still image),
   or size to the screen once: `Math.min(1024, renderer.getDrawingBufferSize(v).y / 2)`. Saves about 190 MB GPU memory with all
   four seen, and a quarter of the mirror pass fill. Check the vanity mirror close up before shipping.

6. **Sun shadow map 4096² on desktop: 134 MB.** CONFIRMED (size). The map is static (`autoUpdate = false`, line 265), so its
   cost is memory, and one redraw per door, curtain, fan frame or fixture pick (`WebGLShadowMap.render` 147 ms at load). The
   frustum is 26 x 26 m (line 2610) for an apartment about 15 x 14.5 m. Fix: fit the box to the apartment plus the balcony
   (about 17 m) and use 3072²: same texel size (5.5 mm vs 6.3 mm now), 75 MB. SUSPECTED no visible change; compare window
   patches in `entry` and `master`.

7. **Ground shader runs the street-lamp loop by day.** CONFIRMED by the code, gain not isolated (measured together with
   finding 1 and the mirror change: desktop HQ off 20 to 10.7 ms; the mirrors are off in that mode, so most of it is this
   change or noise). Line 2471: `for (int i = 0; i < N; i++) { ... }` over every street lamp on every ground, asphalt, kerb and
   lawn fragment while `uLampK` is 0. Fix: `vec3 lampE = vec3(0.); if (uLampK > 0.) for (int i = 0; ...`.

8. **The composer target and the canvas are both multisampled in HQ.** SUSPECTED waste (not measured: the `noMSAA` variant did
   not complete). Line 260 creates the canvas with `antialias: true` and line 285 the composer target with `samples: 4`; in HQ
   the canvas only receives the final full-screen pass, so its 4x MSAA buffer and resolve buy nothing. `preserveDrawingBuffer:
   true` (line 260) is not used by the app (no `toDataURL` in salon.html or the scripts). Fix: `antialias: isPhone` and
   `preserveDrawingBuffer: false`; desktop HQ off would then lose canvas MSAA, so keep `antialias: true` only when HQ starts
   off (phones). Measure before keeping.

9. **Idle desktop HQ still runs per-frame work.** CONFIRMED by the code, cost not measured. After TAA finishes, `frame()` still
   calls `controls.update()`, `camMoved()`, four `getWorldPosition` for the mirrors (line 3029) and `labelRenderer.render`
   (line 3033), which walks the whole scene and rewrites label styles every frame. Fix: return early when not moving and
   `taa.accumulateIndex >= 32`, after `controls.update()` and `camMoved()`.

10. **Fixture slots added about 120 draw calls; merged since.** CONFIRMED and already fixed in feda3a7. On the build before it,
    14 slots held 121 meshes; merging each slot after its build (prototype, `analysis.json`) left 31 meshes and cut calls
    at `entry` 574 to 452, `mbath` 368 to 325, `bath` 443 to 358. The fixtures in the bathrooms are drawn in the living-room
    views too (frustum culling only): a per-room visibility list would save more, low priority after finding 1.

## Prioritised list

| # | Change | Where | Gain (measured or expected) | Quality |
|---|---|---|---|---|
| 1 | Skip zero and back-facing lights in `lights_fragment_begin` | after line 2643 | measured: desktop HQ 144 to 54 ms, fps 6 to 22; HQ off 103 to 20 ms | identical |
| 2 | Render on demand when HQ is off | line 3037 | phones idle 60 renders/s to 0 | none |
| 3 | Skip `cerApply` for untouched defaults at load | line 3392 | about -0.85 s desktop, about -3 s slow phone | none |
| 4 | ImageBitmapLoader for photo textures; memoise `assetTex` | lines 307, 588-609 | most of 1.16 s upload; -28 MB | none |
| 5 | Ground lamp loop only at night | line 2471 | part of 20 to 10.7 ms (with 6) | none |
| 6 | Mirrors 512², no MSAA | line 965 | -190 MB GPU; less fill near mirrors | check close up |
| 7 | `compileAsync` before the first frame | after line 2643 | part of 2.35 s link stall | none |
| 8 | Phone pixel budget instead of DPR 1 | line 2865 | sharper phone image (costs frame time) | better |
| 9 | Shadow frustum 17 m at 3072² | line 2610 | -59 MB | same texel |
| 10 | Canvas MSAA off in HQ, no preserveDrawingBuffer | line 260 | not measured | none |
| 11 | Day/eve light visibility with compileAsync | `setMode` line 2888 | about 3x more after 1 | 1-2 s hitch per switch |

## Checked and fine

- No page errors or console errors in any of the five profiles, with or without the prototype patches.
- Material duplicates: 251 materials, 215 distinct looks (QA6 had 605 duplicates); the remaining 36 are not worth a change.
- CPU per frame 8 to 15 ms desktop HQ at 700 to 900 draw calls: not the bottleneck.
- New programs per view: kitchen compiles 6 and master 3 on first visit (about 0.3 to 0.4 s hitch on the first frame there);
  all other measured views reuse programs.
- GTAO, bloom and contact shadow planes: each within the run-to-run noise next to the light cost.
- Download unchanged since QA6 (11.8 MB); the largest single items are `three.module.js` and the two balcony plant GLBs
  (1.2 MB and 0.7 MB, desktop and phone).
