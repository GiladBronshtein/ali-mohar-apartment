# Project memory

Running record of decisions, state and open issues. Newest first within each section. Update at the end of every
session; remove entries that are no longer true.

## Status (2026-10-04)

- The GitHub Pages site is the canonical version (owner's decision, 2026-10-04). The claude.ai artifact is frozen at
  an older state and is no longer updated; Claude Code cannot write to it (HTML artifacts refuse docs-connector access).
- Third re-check against the owner's vector PDFs, including the construction plan (new), plus ceramics from the
  studio spec, 2026-10-04: `audit/recheck3/APPLIED.md`, `CERAMICS.md`.
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
| 2026-10-06 | Re-check 5 against 11 new owner documents (sale spec, addendum, annexes, studio spec 05/10/2026, sheets 1:75, typical floor, ground, basement, roof, notes), five agent reports in `audit/recheck5/` (summary `APPLIED.md`). Interior `5167387`: ceiling 2.70 (spec minimum), mamad porcelain, 7 cm skirting in the floor material, window C without shutter, master shower one sash, washer niche painted, no rain head over the bath, white flush plates, ceramic vanity tops with deck mixers, second condenser, balcony and island sockets. Ceramics `d7c72b9`: glossy 80x80 page, pages renumbered. Outside `96821de`: floor-1 balcony and garden apartment below us, A/B bar on pilotis, lot wall, gardens, west parking and ramp, near side of both streets from the ground sheet, far side +2.2 m. North kept: OpenStreetMap has both streets on the cardinal axes. The documents stay outside the repo (`source/out/docs5`, personal data); the studio slides crops too. |
| 2026-10-04 | Realism pass 5, from three agent reports (`audit/realism5/`: interior, exterior, CC0 assets), one commit per stage, each with `sitetest` no issues and phone shots. A `23a1166`: floor contact shadows, static shadow map, GTAO tune, fog and sky-lit exterior env, clearer glass, dithering, vignette, sheers, bedside and kids' bath lights. B1 `accb357`: physical finishes on desktop. B2 `2499dda`: baked ground mask (sun shadows, AO, lawns). B3 `40ed7eb`: facade atlas on the blocks (generic layouts, estimate). B4 `15e2108`: evening light pools and lit windows in three warmths. ext6 `891cdd3`: stucco on our shell, floors 0-1 under the apartment (same plan assumed). ext7A `c9b235c`: tree crown normals and tint. int4 `0a7de6e`: window and lamp lights gated to their room box (they leaked through walls). C1 `b48eabf`: CC0 steel, leather, quartz gloss and paver sets (tile and splash stay with the ceramic picker). C2 `eed100c`: CC0 kitchen props on desktop (fruit, wine bottle, cutting board). Dropped: int3 room env capture (flattened the image). Phone 40 fps after A. |
| 2026-10-04 | Fourth check, report only, by two agents (`audit/recheck4/visual.md`: 33 views day and eve; `geometry_scan.md`: ray scan of tiles, floors, ceilings, leaks, coplanar faces, all 530 ceramic options). Fixed: kitchen south splash now runs to the SW corner (63 cm of plaster, owner screenshot); ceramics moved to their own panel tab with swatches and fly-to-space; mirrors fall back to the env-mapped material beyond 6 m (the Reflector went black from about 8 m); master shower niche panel moved onto the tile face; family bath washer niche, stub face and window reveals tiled (estimate); master bath N tile to the window jamb; `windowZ` end stiles full width (2.5 cm unglazed slots at each end); mamad window `xIn` -3.80 so its sill shows; room 1 planks to the wall face -5.035; balcony N wall end no longer z-fights. `roomdims` +0, `clearance_audit` 0, `sitetest` no issues. |
| 2026-10-04 | Third re-check against the owner's vector PDFs (`materials/plans/vector/`, the construction plan is new), four reports in `audit/recheck3/` (summary `APPLIED.md`). Window and door sills and heads now written: `HEAD` 2.35, bedroom windows one sash with sill .15, baths 1.10/1.25, mamad 1.10..2.10, kitchen window C sill 1.20; living facade openings re-centred. Corridor-to-living passage 120 (was 98). Family bath riser box to the NW corner, master split over the master door, shower on a wall arm, return grille, condenser 100x45, balcony drains, 9 electrical items. Bath tile skins found buried 2.5 to 3 cm inside the moved walls, moved onto the faces. Ceramics from the studio spec (`CERAMICS.md`, names exact), with a per-space picker in the panel ("קרמיקה מהמפרט", saved in localStorage `ali-cer`, copy button). The vendor catalog PDF stays out of the repo. `roomdims` +0, `clearance_audit` 0, `sitetest` no issues. |
| 2026-10-04 | Second re-check, five parallel reports in `audit/recheck2/` (summary `APPLIED.md`). Corridor and living-strip drop 25 to 35 cm (AC sheet "h=35cm (netto)", Latin written mirrored, misread before), TV bridge now 2.19 to the drop; entry wall by the kitchen; 13 electrical items (socket heights 1.80/1.10/1.40/2.20, bed heads, bath heaters, entry plate); niche louvres 80% open, water heater z, kids' WC axis 44, niche drain riser. Interior: GTAO retune and transparent meshes off the AO pass, hollow tub, recessed niches, steel sink, gooseneck faucet, eve hotspots, slat grain, skirting, condenser, hob, handles. Environment from the balcony photos: tower moved SE, block rings, lit windows in eve, lot cut to z 9..22 with retaining wall and driveway, street parking, red pavers, street lights, school details, north plot. `roomdims` +0, `clearance_audit` 0, `sitetest` no issues. |
| 2026-10-04 | Wave pendant moved from the mamad to the living room, 60 cm in front of the storage wall and parallel to it (diffuser bottom about 2.06, estimate); the four cables now drop straight out of a canopy as long as the bar. Mamad back to its fan and spots. Then centred between the AC bulkhead and the south wall, and the ceiling LED grazer over the arch picture removed (owner). `clearance_audit` 0, `roomdims` +0, `sitetest` no issues. |
| 2026-10-04 | Owners' current furniture and lamps, from their photos (sizes estimated): living sofa as dark leather with flip-up headrests and chrome legs, shaggy rug with a diamond lattice (`T.berber`), rotating slab coffee table; balcony sofa on a slim aluminium frame with loose cushions, teak-top table; egg chair rebuilt as an open rattan teardrop on a C-stand. Lamps: frames pendant over the island (replaces the two cones), wave pendant (moved later the same day), flush three-frame light over the coffee table, black cylinder downlights in the corridor and entry (replace 5 recessed spots); three warm point lights moved under them. Footprints unchanged: `clearance_audit` 0, `roomdims` +0, `sitetest` no issues. |
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
- Header area is "כ-132 מ״ר", the contractor's figure (owner, 2026-10-04). The model measures about 113 net (inside the walls); 132 is a gross figure that includes walls.
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

- **Left from the fourth check** (`audit/recheck4/`): faint light line through wall-tile rows up close (`cerTex`); eve blown ceiling patch over the island pendant and a hall wall hotspot; top-view dimension labels overlap room names; AC pipes rise straight out of the condenser top; AO speckle on the mamad blast-door jamb; sill tops coplanar with the wall top (2 cm embed); ceramic offset uses the x origin on x-facing walls (vertical joints not from a corner).

- **Open from the third re-check** (`audit/recheck3/APPLIED.md`): ceiling height (heads 2.35 plus a 35 cm shutter
  box point to 2.70 or more, model keeps 2.60); boxed "א" marks in the bedrooms and mamad; blue "1" over the entry
  door; living-room cones and "S" box; window C shutter with no motor; second condenser 84x40 not modelled; balcony
  upstand height; room interiors on the construction plan are 5 to 8 cm larger than the sales plan (model stays on the
  sales plan).
- **Ceramics** (`CERAMICS.md`): tiles are drawn from the catalog images, not photos; baked mode (`?baked=1`) does not
  follow the swaps. Ask the studio: balcony 15x60 limit (20 sqm, ours about 24), vanity sizes (spec 60/80 and 100/120,
  model 100 and 70), unwritten finishes.
- **Open from the second re-check** (`audit/recheck2/APPLIED.md`): soil colour (photos show orange hamra, the model
  keeps the neutral colour until the owner confirms); cisterns. Passage width, master split, kids' bath pipe box and
  the condenser outline were resolved in the third re-check.
- **Renders stale (third re-check):** `room1`, master, living facade views (`sofa`, `kitchen`, `balcony`), `bath`,
  `shower` and the niche predate the new windows, passage, tiles and the bath tile fix.
- **Renders stale (second re-check):** every exterior render (`view`, `balcony`, `balcony2`, bird views) predates
  the new tower, blocks and street; `tvwall`, `sofa`, `entry` predate the 35 cm drop; `bath`, `shower`, `kitchen`
  predate the tub, niche, sink and hob changes.
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
- **Exterior:** our lot, building A and B, the gardens and the near side of both streets follow the ground and typical
  floor sheets (re-check 5); the far side of the streets and the other buildings come from the balcony photos. Blocks have a
  generic facade atlas, not their real elevations. Entrance steps, fence and wall heights, the street level and floors 5-7
  are not on any sheet.
- **Re-check 5 conflicts for the owner** (`audit/recheck5/APPLIED.md`): area 130 vs 132, laundry hide 2 vs 2.9 sqm, door and
  window sizes in the spec vs the plans, standard tile sizes, vanity sizes, master shower 80x80 vs 106x92, kitchen sink type,
  kitchen splash 50 vs 70, room numbering.
- **Kitchen props** (fruit, wine bottle, cutting board) load on desktop only; phones keep the procedural fruit.
- **No CC0 furniture found** for sanitaryware or a matching sofa on Poly Haven; those stay procedural.
- **Renders stale again:** none of the 17 show the tree cards, ground sets, cars or the new soil colour, nor the
  2026-10-04 blueprint fixes (`bath-day` tub and basin, `shower-day` drain and basin, `entry-day`/`kitchen` living
  grilles and entry door, `balcony-day` lights and drains).
- **Renders stale (fourth check, 2026-10-04):** no render shows the kitchen splash corner, the master shower niche, the tiled washer niche or the `windowZ` stiles.
- **Renders stale (re-check 5, 2026-10-06):** no render shows the 2.70 ceiling, the mamad porcelain, the new vanities, the second condenser or the new surroundings below the balcony.
- **Renders stale (realism pass 5, 2026-10-04):** no render shows any of it (contact shadows, ground mask, facade atlas, stucco, room-gated lights, new CC0 sets and props).
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
- **Room 3 as the mamad** is flagged in the panel notes as needing verification.
- `bpy` (Blender as a Python module) is installed locally for Cycles renders and lightmap bakes.

## Estimates (not on any plan)

Ceiling 2.70 m is the sale spec's written minimum ("לא פחות מ-2.70"), so the real height may be a little more; interior door heads 2.10; electrical panel height;
heights of the new panel socket, fibre point and niche switches; condenser height; railings; surroundings (from
balcony photos, off by a few metres). Window sills and heads are written on the construction plan since the third
re-check.

## Next steps

- Decide whether to commit the Chrome path fix, lockfile, docs and the realism pass (`assets/` and `lm/` get published).
- Exterior: facades with real window depth, or an HDRI backplate in place of the far blocks.
- CC0 sofas and sanitaryware from another source (ambientCG has none; check licences elsewhere).
- Fix `render_all.sh` paths before the next render run; re-render the 4 stale images.
- Refresh `audit/report.md` from `audit/recheck/` (its line numbers are stale).
- Ask the contractor: column 2, panel position, the actual ceiling height (spec: not less than 2.70), mamad relief sleeve,
  the boxed "א" marks, balcony and island socket positions (d10 item 10), entrance steps and street level.
- Ask the studio: balcony 15x60, vanity sizes (see `CERAMICS.md`).
