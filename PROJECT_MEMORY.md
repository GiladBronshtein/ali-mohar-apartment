# Project memory

Running record of decisions, state and open issues. Newest first within each section. Update at the end of every
session; remove entries that are no longer true.

## Status (2026-10-04)

- The GitHub Pages site is the canonical version (owner's decision, 2026-10-04). The claude.ai artifact is frozen at
  an older state and is no longer updated; Claude Code cannot write to it (HTML artifacts refuse docs-connector access).
- Blueprint re-check committed and pushed as 9baf415 (2026-10-04).
- Commit and push after each reviewed fix without asking (owner, 2026-10-04).
- Local checkout: `/Users/Gilad.Bronshtein/AliMohar`. Node deps and Playwright Chromium installed in `source/`.
- Verified locally: `build_site.py` rebuild is byte-identical; `sitetest.mjs` "no issues" on desktop and phone;
  `clearance_audit.py` 0 issues; `roomdims.py` +0 on all rooms except the closet probe artifact.
- `CLAUDE.md` and `.claude/` stay uncommitted (listed in `.git/info/exclude`).
- Realism pass verified 2026-10-04: `sitetest.mjs` no issues, `roomdims.py` +0, `clearance_audit.py` 0 issues,
  `out/qa_full.mjs ... after` 0 errors. Download 2.0 to 7.4 MB; forced-render fps desktop HQ 21 to 15, phone 40 to
  35; ready 1.8 s desktop, 2.6 s phone (warm cache). Shots in `source/out/qa/after/`.

## History

| Date | Event |
|---|---|
| 2026-10-04 | Owners' current furniture and lamps, from their photos (sizes estimated): living sofa as dark leather with flip-up headrests and chrome legs, shaggy rug with a diamond lattice (`T.berber`), rotating slab coffee table; balcony sofa on a slim aluminium frame with loose cushions, teak-top table; egg chair rebuilt as an open rattan teardrop on a C-stand. Lamps: frames pendant over the island (replaces the two cones), wave pendant over the mamad desk, flush three-frame light over the coffee table, black cylinder downlights in the corridor and entry (replace 5 recessed spots); three warm point lights moved under them. Footprints unchanged: `clearance_audit` 0, `roomdims` +0, `sitetest` no issues. |
| 2026-10-04 | Tree cards hidden from the GTAO pass: its override material ignores alphaTest, so each card drew a dark rectangle on walls behind it and a light box around far trees (desktop HQ only). |
| 2026-10-04 | Blueprint re-check against full-resolution photos of the electrical, plumbing and AC sheets and the coloured sales plan (`audit/recheck/`, summary in `audit/recheck/APPLIED.md`). Fixed: entry door opening 97 hinge west; room 2 opening 83; TV wall 19 cm on the corridor stretch (panel kept flush); balcony north wall to z .34; family-bath tub 70 wide with taps on the corridor wall, basin and mirror axis 72; ensuite point drain and basin axis 44; room 1/2 grilles 80x20; living grilles moved; mamad sleeves moved and a 4" relief sleeve added; niche floor drain; balcony drains and garden tap h=60; corridor, closet, family-bath and balcony lights; two fans; switches to the latch side and 8 missing switches. `roomdims` +0, `clearance_audit` 0 issues, `sitetest` no issues. |
| 2026-10-04 | Exterior and mirrors: CC0 tree cards (Cycles renders of 3 Poly Haven trees on crossed quads), CC0 asphalt, dirt and grass sets, soil no longer orange, extruded car profiles; live `Reflector` mirrors on desktop HQ (4 mirrors); phone fov 96 to 84, narrow-screen top views step back. QA: `sitetest` no issues, `qa_full ... ext` 0 errors, desktop forced fps 20 (was 15, noisy), phone 37; desktop download 7.6 to 11.9 MB. |
| 2026-10-04 | Realism pass, after a full QA baseline (`QA_BASELINE.md`). Installed skills: web3d-realism-performance, MengTo 3d, Impertio three.js. Added CC0 Poly Haven assets in `assets/` (photo skies, 5 PBR sets, 2 potted plant glTF models) with procedural fallback; day retune (ACES, exposure .85, hemi .22, env .3, sun 3.0); kids' bath eve lamp moved under its lowered ceiling. GPU lightmap bake works (Metal, proxies, HDRI) and is published in `lm/`, but stays opt-in (`?baked=1`). |
| 2026-10-04 | Moved from the claude.ai chat into a local Claude Code project. Replaced the sandbox Chromium path `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` with `process.env.CHROME_PATH` in `exportglb.mjs`, `icons.mjs`, `sitetest.mjs`, `qa_lm.mjs`, `lm/export.mjs`. Added preview config and these docs. |
| 2026-10-03 | Independent audit of the model against the plans (`audit/report.md`). Most findings were then fixed in `salon.html` (see below). |
| before | Built in a claude.ai cloud sandbox (Linux, 2 CPU cores, no GPU): viewer, GitHub Pages build, 17 Cycles renders, lightmap experiment. Initial commit `aae2b0f`. |

## Decisions

- `materials/plans/originals/` (added 2026-10-04) holds the full-resolution photos (5712x4284) of the contractor's
  electrical, plumbing and AC sheets (HADA, 9/2/2006, 1:75 on A3) and of the coloured sales plan. They are the
  sources to re-check against; `materials/photos/22-24` are the same sheets at chat resolution. Re-check reports
  go to `audit/recheck/`.

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
| Ensuite WC axis 49 vs 60 (unconfirmed item) | Re-check 2026-10-04: model is 60, no change |
| Room 1 west facade 38 vs 47 (unconfirmed item) | Re-check 2026-10-04: model is 47, no change |
| TV wall corridor side 14.5 vs 18 (unconfirmed item) | 19 cm on x 2.97..4.15 |
| Balcony south wall thickness (unconfirmed item) | Re-check 2026-10-04: about 50, model 49, no change |

Note: the 2026-10-03 row "AC supply grilles 80x20 vs 90x15" applied the living-room spec to rooms 1 and 2. The AC sheet
writes 90x15 only for the two living grilles; rooms 1 and 2 get a combined 80x20 grille in an 85x25 wall opening (fixed
2026-10-04).

## Open issues

- **Open from the 2026-10-04 re-check** (details in `audit/recheck/APPLIED.md`): column 2 location (plumbing and
  sales sheets disagree); electrical panel x (electrical sheet 3.01..3.40, sales plan 3.33..3.78, model follows the
  sales plan); niche condenser outline 132x55 on the AC sheet vs a 89x34 unit (outline may be a platform); water heater
  about 11 cm north; column 1 at about (4.08, -5.1) not modelled; mamad relief sleeve x and symbol; "H=2.63" near the
  mamad (possibly its ceiling height, not written as such); living, entry and dining single ceiling points (model uses
  downlights, a design choice); TV-wall outlets h=40/130, master TV position, wet-room sockets and heaters, washer/dryer
  sockets not modelled.
- **Stale renders:** `shower-day`, `balcony-day`, `balcony2-day`, `view-day` predate the latest fixes. All 17
  renders also predate the realism pass (photo sky, PBR sets, glTF plants). `exportglb.mjs` serves `source/`, where
  there is no `assets/`, so a re-render would still use the procedural materials unless the export is pointed at
  the repo root.
- **Exterior:** trees, ground and cars improved 2026-10-04; buildings are still boxes with poster facades, and the
  bird-view shell is plain grey.
- **No CC0 furniture found** for sanitaryware or a matching sofa on Poly Haven; those stay procedural.
- **Renders stale again:** none of the 17 show the tree cards, ground sets, cars or the new soil colour, nor the
  2026-10-04 blueprint fixes (`bath-day` tub and basin, `shower-day` drain and basin, `entry-day`/`kitchen` living
  grilles and entry door, `balcony-day` lights and drains).
- **Renders stale (furniture, 2026-10-04):** `sofa`, `kitchen`, `balcony`, `balcony2`, entry eve and the `lm/` bake predate the owners' furniture and lamps.
- **Baked light:** ideas not tried yet: a higher-resolution atlas or several atlases for ceilings, a brighter or
  neutral sky in the bake, window fill in the natural pass, or using only the AO map as `aoMap` on the real-time
  materials.
- **Desktop fov 68** still stretches frame edges a little (QA_BASELINE finding 8); phones fixed 2026-10-04.
- **Mirrors** are live only on desktop HQ; phones and glass still reflect the blurred environment.
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
- Exterior: facades with real window depth, or an HDRI backplate in place of the far blocks.
- CC0 sofas and sanitaryware from another source (ambientCG has none; check licences elsewhere).
- Fix `render_all.sh` paths before the next render run; re-render the 4 stale images.
- Refresh `audit/report.md` from `audit/recheck/` (its line numbers are stale).
- Ask the contractor: column 2, panel position, ceiling height (2.63 near the mamad?), mamad relief sleeve.
