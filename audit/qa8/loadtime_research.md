# QA8: load time and time to first frame, research and prototypes

Scope: what cuts load time and time to first frame for this site (three.js r160, no build step, GitHub Pages), judged for
this code base with gain, effort and risk. Report only: no tracked file was edited. Prototypes ran on copies of the page in
`/tmp/qa8` (variants built with `build_site.py` into a scratch folder), served on 127.0.0.1:8796; scripts and raw JSON in
`source/out/qa8/` (gitignored): `lt.mjs` (A/B load runs), `progdiff.mjs` (programs compiled after the first frame),
`marks.mjs` (section timings), `live.mjs` (waterfall of the live site), `shots.mjs` (visual check).

Line numbers are `source/salon.html` at commit 4ec4d9d. Another session had uncommitted edits in the working copy while
this ran, so search for the quoted code if the numbers have moved.

Caveat on numbers: this Mac was shared with other agents (load average up to 30 during the later runs). Compare numbers
inside one run of `lt.mjs`, not across runs. Desktop = Playwright Chromium, Metal, 1440x900, HQ on; phone = 375x812 DPR 3,
Pixel 7 UA, CPU 4x throttled. Cache disabled in every run, so these are first-visit numbers (no HTTP cache, no GPU program
cache).

## What was measured

### GitHub Pages headers (curl, 2026-10-07)

| File | Cache-Control | Encoding | Notes |
|---|---|---|---|
| `/` (index.html) | max-age=600 | gzip (345 KB to 118 KB) | ETag `W/"6ac629e7-585b9"` |
| `vendor/three/build/three.module.js` | max-age=600 | gzip (1.27 MB to 257 KB) | `Accept-Encoding: br` alone gets the raw 1.27 MB: no brotli |
| `assets/tex/caban/nor.webp` | max-age=600 | none (already compressed) | |
| `assets/models/potted_plant_01.glb` | max-age=600 | gzip (1.27 MB to 1.09 MB) | |

- Every file gets `max-age=600` and there is no way to set headers on Pages (no `_headers`, no config; only community
  threads, no official doc). If-None-Match revalidation works (304).
- The ETag is `<hex of Last-Modified>-<hex of size>`, and Last-Modified is the deploy time for every file: `0x6ac629e7` =
  2026-10-07 11:15:51 UTC, also on `caban/nor.webp` (last changed in git on 2026-10-04) and `three.module.js` (2026-10-03).
  So every push changes every ETag, and after any push a returning visitor downloads the whole site again (9.4 to 11.8 MB).
  The owner pushes after each fix (7 commits in the last two days).
- HTTP/2 from the Fastly edge (`via: 1.1 varnish`).

### Live waterfall (https://giladbronshtein.github.io/ali-mohar-apartment/, desktop, cache off, 3 loads)

- HTML first byte 245 to 375 ms, end 344 to 540 ms. Google Fonts CSS ends at 480 to 666 ms.
- JS: the inline module's 16 static imports start when the HTML is parsed (354 to 556 ms); a second wave of 10 modules
  (Pass, CopyShader, ShaderPass, MaskPass, OutputShader, LuminosityHighPassShader, SSAARenderPass, GTAOShader,
  PoissonDenoiseShader, SimplexNoise) starts 95 to 200 ms later; all JS done at 580 to 1000 ms.
- **Every image texture request starts at DOMContentLoaded, 2115 ms**, after the whole module body has run, although
  `photoPBR` is called at line 600 near the top of the module. The GLB `fetch()` calls start mid-module (1.46 s). So none of
  the 4.4 MB of WebP downloads overlaps the 1.2 to 1.9 s module body. Textures finished at 2.7 s on this connection.
- No duplicate downloads: the browser's in-memory image cache serves the second `oak_veneer_01` and `white_stucco` request,
  but each still gets its own decode and GPU upload (QA7 finding 4).
- 69 requests, 9.4 MB transferred (the kitchen props are desktop only and late).

### A/B prototypes (median of 3 runs desktop, 2 runs phone; ms from navigation)

Variants: `ibl` = `THREE.ImageBitmapLoader` in `assetTex`; `early` = `renderer.compileAsync` started right after the
lights (line 2684) and awaited before the first frame; `photo` = also `await photoReady` before the final compile.

| Variant | First frame shown | Last long task ends (page settled) | Long tasks after the first frame | texSubImage2D | getProgramInfoLog (link wait) |
|---|---|---|---|---|---|
| desktop base | 2505 | 4912 | 2277 | 937 | 950 |
| desktop ibl | 2050 | 4271 | 1984 | 190 | 1057 |
| desktop early (no ibl) | 4265 | 4541 | 257 | 905 | 539 |
| desktop ibl + early | 2910 | 3659 | 767 | 182 | 603 |
| desktop ibl + early + photo | 3612 | 3612 | 82 | 174 | 506 |
| phone 4x base | 6149 | 11277 | 4849 | 3199 | 837 |
| phone 4x ibl | 4786 | 7582 | 2280 | 317 | 752 |
| phone 4x ibl + early + photo | 6997 | 6997 | 0 | 300 | 245 |

Reading: today the first frame comes at 2.5 s (desktop) but the page then stalls for another 2.3 s in long tasks
(24 more programs compiled, textures uploaded, `cerTex`), so it only runs smoothly from about 4.9 s (phone: 11.3 s).
ImageBitmap alone moves the first frame 0.45 s earlier (phone 1.4 s) and cuts upload time 5x to 10x. With compile and
photo sets done before the first frame, the page is smooth from the first frame on: 3.6 s desktop, 7.0 s phone 4x
(was 4.9 / 11.3 s settled). Visual check (`shots.mjs`, entry, balcony, bird1): base vs ibl + early + photo differ by a mean
0.4 to 1.7 of 255 per channel, 0.04 to 0.14% of pixels over 16, none over 48 (TAA noise): same image, ImageBitmap
orientation is correct.

### Programs compiled after the first frame (`progdiff.mjs`)

47 programs exist at the first frame, 71 to 80 a few seconds later. The keys show why:
- `envMapCubeUVHeight` 1024 vs 512: the room environment (`pmrem.fromScene`, cube 256, height 1024) and the exterior
  photo-sky environment (`equi`, line 2525, canvas 512 wide, cube 128, height 512) differ, so every exterior material
  recompiles when `extMats.forEach(m => { m.envMap = ...; m.needsUpdate = true; })` runs (line 2533).
- `photoPBR` (line 588) adds `normalMap` and removes `bumpMap` on arrival: new defines, new program per material.
- New materials arriving late: tree cards (line 2439), GLB plants and props (lines 1929-1957), the PMREM programs
  (`EquirectangularToCubeUV`, `SphericalGaussianBlur`) for the sky environment, shadow depth variants.

### Where the module body goes (`marks.mjs`, loaded machine, so read the shares)

Desktop, one run (sum about 3.2 s under load; QA7 measured the same body at about 1.9 s): procedural canvases plus
`pbrDetail` 0.70 s (22%), geometry 0.45 s (14%), outside 0.18 s, ground mask 0.65 s (20%), merge 0.55 s (17%),
contact capture 0.40 s (13%). After the first frame: `cerTex` 2.4 s (QA7 unloaded: 0.85 s), `meanLin` 0.54 to 0.62 s
(it is the synchronous WebP decode inside `drawImage`, line 581). Phone 4x: the module body is the single longest task
(3.6 to 4.1 s).

### Bytes

| Type | Files | Bytes | Notes |
|---|---|---|---|
| PBR WebP `assets/tex` | 37 files on disk, 29 loaded | 5.2 MB | 1024 except Leather, Metal, pavers (512). Exterior sets (asphalt, dirt, grass, pavers) 2.9 MB |
| Tree atlases | 3 | 1.5 MB | 2528x1024, 2568x1024, 1928x1024 (not power of two; fine in WebGL2, multiples of 4) |
| Skies | 2 | 176 KB | 4096x1152 (not power of two), about 25 MB GPU each with mips; `eve` loaded at start but used only in eve mode |
| GLB (meshopt, WebP inside) | 7 | 2.4 MB | the two balcony plants 1.27 + 0.74 MB |
| JS | 26 | 2.3 MB raw, about 0.47 MB gzip | `three.module.js` 1.27 MB (257 KB gz); `three.module.min.js` would be 0.67 MB (166 KB gz); `RectAreaLightUniformsLib.js` 314 KB (107 KB gz) |
| index.html | 1 | 364 KB (118 KB gz) | inline module about 3300 lines |

GPU memory of the photo textures (RGBA8 plus mips, 5.6 MB per 1024 texture): 22 distinct 1024 textures plus 5 duplicate
uploads plus 7 at 512, about 160 MB.

Already fine: the path tracer is a dynamic `import()` (line 2996); gallery renders load only when the gallery opens
(line 3045 fetches only `status.json`); light maps load only with `?baked=1` (line 2730); GLBs are meshopt with WebP
textures, and `GLTFLoader` already decodes their images with `ImageBitmapLoader` outside Safari.

## Prioritised list

| # | Change | Gain (measured or estimated) | Effort | Risk |
|---|---|---|---|---|
| 1 | `ImageBitmapLoader` in `assetTex`, memoised by path | measured: first frame -0.45 s desktop, -1.4 s phone 4x; uploads 0.94 to 0.19 s; settled 4.9 to 4.3 s / 11.3 to 7.6 s | low | low (Safari fallback) |
| 2 | Start texture downloads early (fetch-based loader plus `preload` for the 9 interior sets) | estimated: photo look 0.6 s+ earlier desktop, downloads fully hidden behind the module body on phones | low | low |
| 3 | `compileAsync` before the first frame, with stable program keys | measured with 1: jank after first frame 2.3 s to 0.08 s, settled 4.9 to 3.6 s desktop, 11.3 to 7.0 s phone | medium | medium (first frame later unless keys are stable) |
| 4 | Take `cerTex` off the critical path (idle per space, or worker) | 0.85 s desktop (QA7), 1.8 s+ phone of main-thread work after the first frame | low (idle) / high (worker) | low |
| 5 | Skip procedural work that is replaced at load | about 0.2 to 0.4 s desktop, about 1 s phone (estimate) | medium | low |
| 6 | One contact capture instead of two | about 0.37 s desktop (half of QA7's 0.74 s), more on phones | low | low |
| 7 | Service worker cache with a content-hash list | repeat visit after a push: about 9.4 MB not downloaded again (4 to 8 s on a 10 to 20 Mbps phone) | medium | medium |
| 8 | `modulepreload` links plus `three.module.min.js` | estimated 0.1 to 0.4 s to JS ready; -92 KB gzip, half the parse | low | low |
| 9 | Defer what the start view does not show (eve sky, exterior sets, trees, plants) | network-bound phones: interior sets get the link alone (up to about 2 s at 10 Mbps); -25 MB GPU for the eve sky | low to medium | low (pop-in from outside views) |
| 10 | Ground mask after the first frame or in idle time | about 0.28 s desktop (QA7), about 0.6 s phone | low | low |
| 11 | Poster image of the start view under the loading text | perceived first frame about 0.5 s | medium | stale image |
| 12 | Smaller exterior textures and plant GLBs | about 2 MB plus about 1.2 MB download | low | low (check from balcony) |
| 13 | KTX2 / Basis Universal | load time: none or negative here; GPU memory 4x to 8x lower | high | medium |
| 14 | Bundling, tree-shaking, splitting the inline module, brotli, custom headers | small or not possible on Pages | n/a | n/a |

## Details

### 1. ImageBitmapLoader for the photo textures (highest value per line of code)

Why: `TextureLoader` gives an `HTMLImageElement`, and Chrome decodes it synchronously on the main thread at
`texImage2D` (QA7: 1.16 s desktop, 3.2 s phone 4x) and again in `drawImage` for `meanLin` and `horizon`. `createImageBitmap`
on a Blob decodes off the main thread and the upload of a decoded bitmap is cheap. Measured above: texSubImage2D 937 to
190 ms desktop, 3199 to 317 ms phone.

How (lines 306-308):
```js
const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);   // same test as GLTFLoader r160
const texLoader = isSafari ? new THREE.TextureLoader() : new THREE.ImageBitmapLoader().setOptions({ imageOrientation: 'flipY', premultiplyAlpha: 'none' });
const texMemo = new Map();
const assetTex = (f, color = true) => texMemo.get(f) || (texMemo.set(f, new Promise(res => texLoader.load('assets/' + f, img => {
  const t = img.isTexture ? img : new THREE.Texture(img); t.needsUpdate = true;
  t.colorSpace = color ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.anisotropy = renderer.capabilities.getMaxAnisotropy(); res(t); }, undefined, () => res(null)))), texMemo.get(f));
```
- `imageOrientation: 'flipY'` replaces `texture.flipY`, which WebGL ignores for ImageBitmap (three.js docs). The prototype
  used exactly these options; screenshots match the base.
- The memo fixes QA7's double decode and upload of `oak_veneer_01` and `white_stucco` (lines 602-605): `photoPBR`'s `fit()`
  already clones, and clones share the `Source`, so one upload. About 28 MB GPU and 5 decodes less.
- `meanLin` (line 581), `horizon` and `treeCards` (`img.width`) accept an ImageBitmap; `lm/` (line 2733) can stay as is.
- Safari: three r160's own `GLTFLoader` avoids `ImageBitmapLoader` on Safari; keep `TextureLoader` there (or test Safari 17+
  and drop the check). Firefox 98+ supports the options.

Sources: [three.js ImageBitmapLoader docs](https://threejs.org/docs/pages/ImageBitmapLoader.html),
[MDN createImageBitmap](https://developer.mozilla.org/en-US/docs/Web/API/Window/createImageBitmap),
[Mozilla bug 1486454 (Chrome ImageBitmap upload 3x faster than Image)](https://bugzilla.mozilla.org/show_bug.cgi?id=1486454),
GLTFLoader r160 source (`node_modules/three/examples/jsm/loaders/GLTFLoader.js` lines 2526-2547).

### 2. Start the texture downloads early

Why: on the live site every image request starts at DOMContentLoaded (2.1 s), after the module body, while `fetch()`
requests (the GLBs) start as soon as the module reaches them. `ImageBitmapLoader` uses `fetch()`, so change 1 alone moves the
requests to the moment `photoPBR` runs (line 600, early in the module). A `preload` in the head moves them to the first
bytes of the HTML (about 0.3 s).

How: in `build_site.py`, add to `meta` one line per interior set file used by `photoReady` (lines 600-609 plus the leather at
line 1350, about 2.6 MB):
```html
<link rel="preload" href="assets/tex/laminate_floor_02/nor.webp" as="fetch" crossorigin>
```
`as="fetch" crossorigin` matches what `ImageBitmapLoader` sends (same-origin `fetch`, `credentials: 'same-origin'`). Check
in DevTools that there is no "preloaded but not used" warning (a mismatch downloads twice). Do not preload the exterior
sets (see 9). For Safari (TextureLoader) use `as="image"` instead or skip.

Sources: [web.dev Preload critical assets](https://web.dev/articles/preload-critical-assets),
[MDN rel=preload](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/preload).

### 3. compileAsync before the first frame, with stable program keys

Why: the first frame waits on the driver's link of each program (QA7: 2.35 s in `onFirstUse`; `getProgramInfoLog`
blocks until the link finishes). `renderer.compileAsync` (three r158+) creates all programs at once and polls
`COMPLETION_STATUS_KHR` (KHR_parallel_shader_compile, available in this Chromium), so links run in parallel in the GPU
process while the main thread continues. Measured: started at line 2684 it overlaps the remaining 1 s of the module body
(the final wait was 150 to 200 ms).

The catch, measured: compiling early does not help much on its own, because 24 to 33 programs are rebuilt after the first
frame anyway (see "Programs compiled after the first frame"). Make the keys stable first:
- `equi` (line 2525): `c.width = 1024; c.height = 512` so the exterior environment has the same cube size (256, height 1024)
  as the room environment; then swapping `envMap` (line 2533) reuses the programs. Check the exterior reflections.
- `photoPBR` (line 588): set the final defines synchronously before the `await`: a shared 1x1 flat normal texture
  `(128, 128, 255)` as `normalMap`, `bumpMap = null`, and a 1x1 white `map` for colour sets on materials without a map; keep
  the original maps aside for `meanLin` and for the failure path. (Prototyped as `ibl_early_ph`; it did not reduce the count
  yet because the environment mismatch above was still in, so verify with `progdiff.mjs` after both changes.)
- GLB plants and props (lines 1931-1956), tree cards (line 2439): before adding a loaded object, `await
  renderer.compileAsync(obj, camera, scene)` (the `targetScene` argument exists in r160).
- Until that is done, a bounded wait gives the measured result without risking a late first frame on slow links:
  `await Promise.race([photoReady, new Promise(r => setTimeout(r, 1500))])`.

How (end of the module, lines 3440-3445):
```js
// after the lights patch, line 2684: start the links while the rest of the module runs
renderer.setRenderTarget(hq ? composer.readBuffer : null); const compileP = renderer.compileAsync(scene, camera); renderer.setRenderTarget(null);
// before the first frame, replacing lines 3444-3445
await compileP;
renderer.setRenderTarget(hq ? composer.readBuffer : null); { const p = renderer.compileAsync(scene, camera); renderer.setRenderTarget(null); await p; }   // fixtures, cer swaps
document.getElementById('loading').hidden = true;
requestAnimationFrame(tick);
```
- The render target matters: in r160 the program key includes tone mapping and output colour space, which depend on
  `renderer.getRenderTarget()` (three.module.js lines 20659 and 20753: no tone mapping and linear output inside a render
  target). The HQ path renders the scene into the composer target, so compiling with the canvas as target would build the
  wrong variants. Phones (HQ off) render to the canvas: `null`.
- `window.__app` is assigned after these lines; `sitetest.mjs` and `exportglb.mjs` wait for it, so they keep working.
- What remains at the first frame: the post-processing passes (GTAO, bloom, TAA, output) and shadow depth programs, about
  0.5 s of link wait in the prototype. Do not set `renderer.debug.checkShaderErrors = false` to hide it: the wait only moves to
  `getUniforms`.
- Browsers without the extension: `compileAsync` still works (polls every 10 ms after a blocking compile), no regression.
- Repeat visits: Chrome's GPU program cache skips the driver compile when the shader source is identical, so stable keys and
  fewer variants also pay off on the second visit.
- Day/eve visibility switch of lights (QA7 item 11) becomes affordable with the same mechanism.

Sources: [three.js forum: Reducing shader compile time](https://discourse.threejs.org/t/reducing-shader-compile-time-on-scene-initialization/56572)
(compileAsync in r158; each distinct define such as a different `alphaTest` is its own program),
[three.js r160 WebGLRenderer source (compile, compileAsync)](https://raw.githubusercontent.com/mrdoob/three.js/r160/src/renderers/WebGLRenderer.js),
[MDN KHR_parallel_shader_compile](https://developer.mozilla.org/en-US/docs/Web/API/KHR_parallel_shader_compile),
[three.js issue 16321](https://github.com/mrdoob/three.js/issues/16321),
[Chromium GPU program caching design](https://docs.google.com/document/d/1Vceem-nF4TCICoeGSh7OMXxfGuJEJYblGXRgN9V9hcE/mobilebasic).

### 4. cerTex off the critical path

Fact check on QA7 finding 4: the ceramic defaults are not the built-in materials. In `CER_SPACES` (line 3347) eight of nine
spaces default to a spec tile (only `rooms` is `cur`), so `cerTex` really has to draw eight tile sets (0.85 s desktop in
QA7, up to 1024 px per repeat with per-pixel JS loops). Today it runs in `photoReady.then` (line 3395), that is right after
the first frame, which is part of the 2.3 s of long tasks after it.

How, cheapest first:
- Idle scheduling: in the loop at line 3437, apply the spaces seen from the start view first (`floor`, `kitB` for
  `entry`), then one space per `requestIdleCallback` (fallback `setTimeout(fn, 50)`); `cerSet` on a user pick stays
  immediate. The procedural original and the `cerTex` result have the same maps (`map`, `roughnessMap`, `bumpMap`, no
  `normalMap`), so no program recompiles. A bathroom reached in the first second shows the procedural tile briefly.
- Worker: `cerTex` is canvas 2D plus `ImageData` loops; `OffscreenCanvas` 2D runs in workers (Chrome 69, Firefox 105,
  Safari 16.4), and the eight spaces would run in parallel off the main thread. Needs `CER`, `cerRelief`, `rnd`,
  `cerHash`, `CER_FIN` in the worker (a Blob worker from the functions' source text keeps the no-build rule). High effort.
- Baking the eight default sets to WebP files costs download (three maps per space) to save CPU; not recommended while the
  defaults still change.

Source: [MDN OffscreenCanvas](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas),
[MDN requestIdleCallback](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback).

### 5. Procedural work that is thrown away at load

- `pbrDetail` (line 554, list at lines 574-577) runs on 16 materials. On the site, `planks`, `oak` and `quartz` get photo
  maps a moment later (lines 601-608, roughness and normal replace the derived maps), and `tile`, `terrazzo`, `bathWall2`,
  `bathFloor`, `bathWall`, `sage`, `splash` and `deck` are replaced by the `cerTex` defaults. 11 of 16 results are only
  needed for the "cur" option or the artifact fallback.
- The same holds for the `T.*` canvases behind those eight ceramic materials (lines 328-499).
- How: keep the canvas draw and `pbrDetail` as closures and run them when "cur" is picked (`cerApply`, line 3364, branch
  `!it`) or when the photo set fails to load (`photoPBR` failure branch). Gain estimate: about 70% of `pbrDetail` (QA7
  258 ms) plus part of the canvases and of the `rnd` LCG (341 ms self time in QA7, line 313): about 0.2 to 0.4 s desktop,
  about 1 s phone 4x. Medium effort because `cerOrig` (line 3366) must point at a lazy original.

### 6. One contact-shadow capture

`captureContact()` runs at line 2629 and again when the two balcony plants arrive (line 1938); QA7 measured 741 ms
total, 494 ms of it in the synchronous `readRenderTargetPixels`. On the site the plants nearly always load, so the first
capture is wasted. How: on the site, skip the call at line 2629 and capture once in the plants' `then` (and in the failure
case), or once after a 2 s timeout, whichever comes first; with change 3 that capture can sit before the first frame. A larger
change, removing all readbacks: do the max-combine with `THREE.MaxEquation` blending, draw the wall boxes into the same
target, and blur with two shader passes into the texture the floor planes read (no CPU copy).

### 7. Service worker cache keyed by content hash

Why: Pages sends `max-age=600` with no way to change it, and every push resets Last-Modified and the ETag of every file
(measured above), so the HTTP cache is useless for returning visitors after each push, and after 10 minutes every request
revalidates. A service worker sits in front of the HTTP cache and decides itself.

How (generated, so the no-build rule holds):
- `build_site.py` writes `sw.js` with a list of `[path, sha1]` for `vendor/`, `assets/` and the root icons (hash of the file
  bytes), and the version string = hash of that list. Install: cache the list in `cache-<version>` (or lazily on first use);
  fetch: cache-first for listed paths, network-first for `index.html` and `renders/status.json`; activate: delete old caches
  but copy entries whose hash did not change (or key the cache by `path?h=<sha1>` so unchanged files stay valid).
- Register at the end of the module: `if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js')`.
- Scope is `/ali-mohar-apartment/` by default (the script's folder): correct for Pages.
- Gain: a returning visitor after a push downloads only the changed files (usually `index.html`, 118 KB) instead of
  9.4 MB; offline works too. First visit unchanged.
- Risk: a buggy worker serves stale files; keep `index.html` network-first, test the update path in `sitetest.mjs`.
  Optional: precache the interior sets with low priority after the first frame.

Sources: [GitHub community discussion 11884 (Pages max-age=600, no custom headers)](https://github.com/orgs/community/discussions/11884),
[GitHub community discussion 21655 (no brotli, no precompressed files)](https://github.com/orgs/community/discussions/21655),
[web.dev Service worker caching and HTTP caching](https://web.dev/articles/service-worker-caching-and-http-caching),
[MDN Cache API](https://developer.mozilla.org/en-US/docs/Web/API/Cache).

### 8. modulepreload and the minified three.js

- The module graph has two waves (live: second wave starts 95 to 200 ms after the first) and starts only after the HTML is
  parsed. `<link rel="modulepreload">` for all 26 static modules in the head starts them at first byte and parses them as they
  arrive. Estimate 0.1 to 0.4 s off JS ready, more on high-latency mobile links.
- `vendor/three/build/three.module.min.js` (ships in the same npm package): 166 KB gzip instead of 257 KB, 0.67 MB to
  parse instead of 1.27 MB.
- How: in `build_site.py`, map the importmap entry for `three` to `./vendor/three/build/three.module.min.js` (copy it with
  `vendor.mjs`), and emit the preload list by scanning the `import ... from` lines of the vendored files reachable from the
  importmap (exclude the path tracer and three-mesh-bvh, which load lazily). Risk: none functional; stack traces point into
  minified code.
- The Google Fonts stylesheet does block module scripts until it loads (deferred and module scripts wait for pending style
  sheets), but on the live site it finished (480 to 666 ms) before the JS (580 to 1000 ms), so no gain today from `async` on
  the module or from self-hosting the fonts.

Sources: [web.dev modulepreload](https://web.dev/articles/modulepreload),
[MDN DOMContentLoaded (deferred and module scripts wait for stylesheets)](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event),
[WHATWG issue 3890](https://github.com/whatwg/html/issues/3890).

### 9. Defer what the start view does not need

- Eve sky: `assetTex('sky/eve.webp')` (line 2514) is decoded and uploaded at load (4096x1152, about 25 MB GPU with mips)
  but only used after the first switch to eve. Load it in `setMode` the first time, or in idle time after the first frame.
- Exterior: asphalt, park dirt, grass and pavers (line 2122-2123, 2.9 MB), the three tree atlases (line 2439, 1.5 MB) and the
  balcony plants (line 1936, 2.0 MB) are 6.4 MB of the 9.4 MB. For interior start views, request them after the first frame
  (or `fetch(url, { priority: 'low' })` in Chrome) so the 2.6 MB interior sets do not share the link with them. For start
  hashes that look outside (`balcony*`, `view`, `bird*`, street views) load them as now.
- Gain: only on network-bound clients (on a 10 Mbps phone link the interior sets finish about 2 s earlier); none on this Mac.
  Pop-in risk from the windows of interior views, about 1 s after the first frame.

### 10. Ground mask

The mask block (lines 2444-2506) draws and box-blurs three 2048 canvases on desktop (1024 on phones): QA7 0.28 s, 20% of the
body in the loaded run. It only affects the ground outside. Build it after the first frame (materials render unmasked for a
moment, only visible from outside views) or move the blur to the GPU like item 6. Desktop at 1024 (as phones) would cut it
by 4x; the blur radii are 0.12 to 1.2 m, so a 37 cm texel should still look the same (check from `bird1`).

### 11. Poster image under the loading text

Show a still of the start view behind "בונה את הדירה…" (a 1440x900 JPEG of `entry`, about 100 KB, captured by a Playwright
step next to `sitetest.mjs`), and fade to the canvas on the first frame. Perceived load drops to the HTML time (about 0.5 s);
real load unchanged. Risk: the still goes stale whenever the model changes, so regenerate it in the build.

Source: [web.dev Largest Contentful Paint](https://web.dev/articles/lcp).

### 12. Texture resolution and mipmaps

- Exterior sets are 1024 although they are seen from 6.6 m up or from the bird views: 512 cuts about 2 MB of download and
  3/4 of their decode and GPU memory. Rebuild in `assets.py`.
- `Marble021/nor.webp` (2 KB) and `Metal009/nor.webp` (2 KB) are nearly flat at 1024; `grass_ground/rough.webp` is 3.5 KB:
  512 or dropped, no visible change expected.
- Balcony plants: `gltf-transform resize --width 512 --height 512` on the embedded textures and `simplify`: estimate 2.0 to
  about 0.8 MB.
- Mipmaps are generated on the GPU (`generateMipmap`, cheap); not a load-time cost. The sky (4096x1152) could be 2048 wide
  at half the GPU memory; it is blurred by the haze anyway (check `view`).

### 13. KTX2 / Basis Universal: not for load time here

- File size: UASTC is 8 bpp before supercompression and about 4 to 6 bpp after RDO plus Zstandard, so a 1024 texture with
  mips is about 0.7 to 1.0 MB; the WebP files here are 0.1 to 0.56 MB (0.8 to 3.8 bpp). ETC1S (0.3 to 1.25 bpp) is as small
  as WebP but poor on normal maps, and most of the files here are normal and roughness maps.
- Decode: no main-thread decode and pre-built mips, but item 1 already removes the main-thread decode for free.
- Cost: `basis_transcoder.wasm` 500 KB plus 62 KB JS and worker start-up, `KTX2Loader` in `vendor/`, and KTX-Software
  (`toktx`) in the asset pipeline (not installed here).
- Where it would pay: GPU memory, 4x (UASTC to ASTC/BC7) to 8x (ETC1S) less than RGBA8, about 160 MB to 20 to 40 MB for
  the photo sets. Worth revisiting if phones run out of memory, not for speed.

Sources: [Khronos KTX artist guide](https://github.com/KhronosGroup/3D-Formats-Guidelines/blob/main/KTXArtistGuide.md),
[three.js KTX2Loader docs](https://threejs.org/docs/pages/KTX2Loader.html),
[Don McCurdy, Choosing texture formats for WebGL and WebGPU](https://www.donmccurdy.com/2024/02/11/web-texture-formats/),
[Basis Universal](https://binomialllc.github.io/basis_universal/),
[three.js forum: WebP vs KTX2](https://discourse.threejs.org/t/webp-vs-ktx2-for-web-textures/58651).

### 14. Judged and not recommended

- Brotli or longer cache headers on Pages: not possible (measured: `br` not served; no header config). Only a CDN in
  front (Cloudflare) or another host would change this; the service worker (7) gets the caching benefit without moving.
- Bundling and tree-shaking (esbuild or Rollup in `build_site.py`): three r160's `WebGLRenderer` pulls in most of the
  library, so the win over `three.module.min.js` is small; with `modulepreload` the request waterfall is already flat.
  It would break the "one file, readable vendor" setup for about 0.1 s.
- Splitting the inline module into `app.js`: V8 does not code-cache inline scripts, so an external file could skip
  compilation on hot loads, but with `max-age=600` and the per-push ETag churn the cache rarely survives; the module compiles
  lazily (tens of ms). Revisit together with the service worker.
- `RectAreaLightUniformsLib.js` (107 KB gzip of LTC tables as JS literals): needed before the first frame for the window
  lights; could be a binary file, gain tens of ms.
- `renderer.debug.checkShaderErrors = false`: moves the link wait, does not remove it.
- The LCG `rnd` (line 313, 341 ms self in QA7): the cost is the number of calls in canvas drawing, not the function; items
  4 and 5 remove most calls.

Sources: [V8 blog, Code caching for JavaScript developers](https://v8.dev/blog/code-caching-for-devs).

## Suggested order

1. Item 1 (ImageBitmapLoader plus memo) and item 6 (one contact capture): small, measured, no visual change.
2. Item 3 in two steps: stable keys (`equi` 1024, `photoPBR` placeholders, `compileAsync` for late objects), then the
   early `compileAsync` before the first frame. Verify with `source/out/qa8/progdiff.mjs` (target: no new programs after the
   first frame except post passes) and `lt.mjs`.
3. Items 4 and 2, then 8 and 9.
4. Item 7 (service worker) as its own change with an update test.
5. Items 5, 10, 11, 12 as time allows. Item 13 only for GPU memory.

After each: `python3 build_site.py`, `sitetest.mjs` no issues, shots at `entry`, `balcony`, `bird1`, day and eve, phone size.
