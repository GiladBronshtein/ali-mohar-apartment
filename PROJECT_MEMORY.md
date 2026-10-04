# Project memory

Running record of decisions, state and open issues. Newest first within each section. Update at the end of every
session; remove entries that are no longer true.

## Status (2026-10-04)

- Live site and the claude.ai artifact both reflect `source/salon.html` at commit `aae2b0f` (the only commit).
- Local checkout: `/Users/Gilad.Bronshtein/AliMohar`. Node deps and Playwright Chromium installed in `source/`.
- Verified locally: `build_site.py` rebuild is byte-identical; `sitetest.mjs` "no issues" on desktop and phone;
  `clearance_audit.py` 0 issues; `roomdims.py` +0 on all rooms except the closet probe artifact.
- Uncommitted: Chrome path fix in 5 Playwright scripts, `source/package-lock.json`, `.claude/launch.json`,
  `CLAUDE.md`, `DESIGN.md`, this file, `QA_BASELINE.md`, and the realism pass below (`salon.html`, `index.html`,
  `assets/`, `lm/`, `vendor/.../GLTFLoader.js` and `meshopt_decoder.module.js`, `source/assets.py`, `lm/bake.py`,
  `exportglb.mjs`, `vendor.mjs`).
- Realism pass verified 2026-10-04: `sitetest.mjs` no issues, `roomdims.py` +0, `clearance_audit.py` 0 issues,
  `out/qa_full.mjs ... after` 0 errors. Download 2.0 to 7.4 MB; forced-render fps desktop HQ 21 to 15, phone 40 to
  35; ready 1.8 s desktop, 2.6 s phone (warm cache). Shots in `source/out/qa/after/`.

## History

| Date | Event |
|---|---|
| 2026-10-04 | Realism pass, after a full QA baseline (`QA_BASELINE.md`). Installed skills: web3d-realism-performance, MengTo 3d, Impertio three.js. Added CC0 Poly Haven assets in `assets/` (photo skies, 5 PBR sets, 2 potted plant glTF models) with procedural fallback; day retune (ACES, exposure .85, hemi .22, env .3, sun 3.0); kids' bath eve lamp moved under its lowered ceiling. GPU lightmap bake works (Metal, proxies, HDRI) and is published in `lm/`, but stays opt-in (`?baked=1`). |
| 2026-10-04 | Moved from the claude.ai chat into a local Claude Code project. Replaced the sandbox Chromium path `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` with `process.env.CHROME_PATH` in `exportglb.mjs`, `icons.mjs`, `sitetest.mjs`, `qa_lm.mjs`, `lm/export.mjs`. Added preview config and these docs. |
| 2026-10-03 | Independent audit of the model against the plans (`audit/report.md`). Most findings were then fixed in `salon.html` (see below). |
| before | Built in a claude.ai cloud sandbox (Linux, 2 CPU cores, no GPU): viewer, GitHub Pages build, 17 Cycles renders, lightmap experiment. Initial commit `aae2b0f`. |

## Decisions

- Single-file viewer that doubles as the claude.ai artifact; the site is a build product of it.
- No CDN on the published site: `vendor/` holds only the files the page loads.
- Everything procedural (geometry and canvas textures) so the model is reviewable text and loads without assets.
  Since 2026-10-04 the site also loads optional CC0 assets from `assets/` (relative paths, null on failure); the
  claude.ai artifact has no `assets/` and keeps the procedural look.
- Laminate floor keeps the procedural plank colour and layout and takes only the photo normal and roughness maps:
  the full photo colour lost the plank seams and washed out in the master bedroom.
- Dining area replaced by a storage wall.
- Baked lightmaps off by default. The 2-core bake was dark and blotchy; the 2026-10-04 256 spp GPU bake still reads
  darker and blotchier than real-time even at 30x natural gain (brown-purple cast on ceilings, about 4 cm per texel).
  Real-time lighting is the shipped look.
- Path tracer kept in code but its button hidden.
- Phones run without the post-processing composer.

## Audit findings now fixed in salon.html

Checked against the current code on 2026-10-04; `audit/report.md` line numbers and file references are stale.

| Finding (audit 2026-10-03) | Now |
|---|---|
| Balcony 887×270 vs plan 884×275, north wall full depth | `BX2 = 10.45`, `BZ2 = 8.71`, north wall stops at 9.30 |
| Mamad blast door hinge on the wrong end, opens 180° | Hinge at the west end, opens 90° into the corridor |
| AC supply grilles 80×20 vs plan 90×15 | 90×15 |
| Ensuite shower 97×88 vs plan 106×92 | 106×92 |
| Missing family-bath pipe box 19×21 | Added |
| Missing electrical panel in the TV wall | Added (height is an estimate) |

## Open issues

- **Unconfirmed audit items:** ensuite WC axis to closet wall 49 vs plan 60 (-11 cm); west facade behind the room 1
  wardrobe 38 vs about 47 cm (niche about 8 cm too deep); TV wall corridor side 14.5 vs about 18 cm; balcony south
  wall thickness. Re-check each against the current code before claiming fixed.
- **Stale renders:** `shower-day`, `balcony-day`, `balcony2-day`, `view-day` predate the latest fixes. All 17
  renders also predate the realism pass (photo sky, PBR sets, glTF plants). `exportglb.mjs` serves `source/`, where
  there is no `assets/`, so a re-render would still use the procedural materials unless the export is pointed at
  the repo root.
- **Exterior** is the weakest part (box buildings, lollipop trees, orange ground, box cars). Not touched yet.
- **Baked light:** ideas not tried yet: a higher-resolution atlas or several atlases for ceilings, a brighter or
  neutral sky in the bake, window fill in the natural pass, or using only the AO map as `aoMap` on the real-time
  materials.
- **Phone fov 96** still distorts bird views; desktop fov 68 stretches frame edges (QA_BASELINE finding 8).
- **Mirrors and glass** still reflect only the blurred environment.
- **`render_all.sh` broken as committed:** writes to `source/renders/` (not `../renders/`), and never creates
  `source/logs/`, so every run fails at the log redirect. It also renders `bath-day` and `room1-day`, which are not
  in the gallery.
- **`roomdims.py` closet:** reports 485/175 because its probe at x 7.87 passes through the open closet doorway
  (x 7.54 to 8.32). Audit measures 175 exactly. Script probe position, not a model error. At `YH=1.0` the corridor
  probe also misreads (909/110).
- **README** still says to edit the Chromium path in `exportglb.mjs`; now it is `CHROME_PATH`.
- **`sitetest.mjs` default URL** assumes the repo is served under `/ali-mohar-apartment/` on :8791; pass the base
  URL explicitly.
- **Sandbox wording** remains in comments ("web3d-realism-performance skill" in `lm/bake.py` and `salon.html`), and
  `audit/report.md` references files not in the repo (`audit2/`, `measure.py`, `dims.json`).
- **Mamad sleeves:** per the AC plan they sit about 5 cm below the corridor drop ceiling if the ceiling is 2.60.
  Ask the contractor.
- **Room 3 as the mamad** is flagged in the panel notes as needing verification.
- `bpy` (Blender as a Python module) is installed locally for Cycles renders and lightmap bakes.

## Estimates (not on any plan)

Ceiling 2.60 m; window sills 0.95 / 1.0 / 1.05 / 1.5 / 1.0 / 0; window heads 2.0 to 2.2; door heads 2.10 interior,
2.30 balcony, 2.0 mamad; electrical panel height; railings; surroundings (from balcony photos, off by a few metres).

## Next steps

- Decide whether to commit the Chrome path fix, lockfile, docs and the realism pass (`assets/` and `lm/` get published).
- Exterior: an HDRI backplate plus simpler massing, CC0 tree models.
- More CC0 models where the QA saw primitives: sofas, sanitaryware, bed.
- Fix `render_all.sh` paths before the next render run; re-render the 4 stale images.
- Re-verify the unconfirmed audit items and refresh `audit/report.md`.
