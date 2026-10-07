# QA10 / V2: sweep of every picker option (ceramics and fixtures)

Verifier V2. Report only: no tracked file was edited. Model: commit 6810263, built site at http://127.0.0.1:8791/
(index.html of 20:35). Scripts and the full shot set are in `/tmp/v2/` (about 1,300 screenshots). Evidence is in `V2_img/`.
Line numbers refer to `source/salon.html` at 6810263.

## What was run

| Check | How | Result |
|---|---|---|
| Fresh load | `probe.mjs`: every `<select>`, `fixState`, `cerState`, local and session storage; then pick a WC and a floor, reload | Pass. All 9 ceramic selects read `cur`, all 15 fixture selects show `FIX[id].def`, `fixState` = {}, every `cerState` = `cur`, storage empty. After a reload the picks are gone. No duplicate option values. |
| Every fixture option | `sweep.mjs fix`: all 163 options (wc 5, flush 6, tub 2, bathTap 18, basinTap 16, vanF 51, vanM 28, showerTap 9, head 4, rail 4, kSink 4, splashH 2, screens 2, doorHw 3, kTap 9), each in `FIX[id].view` plus 1 to 8 close-ups (529 shots) | State, select and info line correct for all 163. No console errors. Findings F1 to F8 below. |
| Every ceramic option | `detail.mjs`: all 551 options of the 9 spaces, checking `cerState`, the select, the info text (name), the swatch and the texture swap; then back to `cur` | Pass for all 551. After `cur` and after `cerReset()` every material has its original map and colour back. |
| Ceramic visuals | `sweep.mjs cer`: per space and catalog page the first, last, a glossy and a decor item (163 picks), view plus close-up | Findings C1 to C5. |
| Tile cuts | Geometry: every tiled face of the 4 wall spaces, piece size at every visible edge for each tile size (`walls.mjs`). Floors: a top-down mask render of each floor material with each tile grid (`floors.mjs`) | Findings C1 to C3. Floors of the living area, the bedrooms and the balcony have no piece under 5 cm. |
| Day / evening | 6 samples in evening mode (gold tap and silquartz sink, master vanity and wall tile, glossy floor, chrome door handles, screens) | No evening-only problem. |
| Console | captured over every run | The site logged no errors or warnings. The only messages (`Canvas2D ... willReadFrequently`) came from my own swatch readback in the test, not from the site. |

## Findings, most important first

### F1. Top-mount kitchen sinks: open black slit between the rim and the bowl (kSink `נירוסטה`, `סיליקוורץ`, `אקרילי`)
Evidence: `01_kSink_silq_rim_gap.jpg` (dark slits along both long sides and the back corners), `01b_kSink_steel_topmount.jpg`.
Cause: `fixKSink`, line 791. The bowl is a `RoundedBoxGeometry` whose top edge is rounded with radius .07 (.05 for steel) and
whose top sits at counter height (.92). The rim lip covers only 1 cm inside the hole (`a + .01` etc., line 790), so between the
lip and the rounded bowl top you look down into the dark cabinet.
Fix: after the bowl line, close the throat with four thin walls in the bowl material:
```js
const r = q ? .07 : .05, tm = ac ? mAcr : q ? mSilq : mat.sinkSteel;
[[a, a + .004, c, d], [b - .004, b, c, d], [a, b, c, c + .004], [a, b, d - .004, d]].forEach(([x1, x2, z1, z2]) => B(x1, x2, z1, z2, .92 - r, .92, tm, { cast: false }));
```
(or put the bowl centre at `.82 - r/2` with height `.2 + r` so the rounding sits above the counter top, hidden under the rim).

### F2. "הצג" for the bath tap opens a view where the tap cannot be seen (bathTap, all 18 options)
Evidence: `02_bathTap_view_bath2_tap_not_visible.jpg`. The tap is on the corridor wall at the tub end (x 4.11, z -1.395),
behind the `bath2` camera.
Cause: line 694, `bathTap: { ..., view: 'bath2' }`.
Fix: add a view and point the fixture at it, e.g. in `views` (line 2912)
`tub: { g: 'B', name: 'אמבטיה: ברז ומוט', pos: [3.1, 1.55, -3.0], tgt: [4.2, .95, -1.5], fov: 65 }` and `view: 'tub'` for
`bathTap` (the family rail is on the same wall and would also be seen there). `02b_bathTap_candidate_view.jpg` is that camera.
If a new view is unwanted (views are counted by `sitetest.mjs`, 33), the fixture row can carry its own camera instead.

### F3. Chrome, nickel and the Grohe finishes read as champagne or brass in both bathrooms
Evidence: `07_chrome_bathTap_nickel.jpg`, `07b_chrome_zen_basin_side.jpg`, `07c_chrome_head_nickel.jpg` (underside of the
nickel head reads as tan wood), against `07d_kitchen_nickel_for_comparison.jpg`, where the same material reads silver.
An architect choosing between black, nickel and gold will see "nickel" as gold.
Cause: `FINM.chrome` / `FINM.brushed` (line 670) are shared by every bath fixture and are in `PROBE_GLOSSY` (line 2606) with no
`PROBE_ZONE` entry, so they reflect the living-room probe at `.9 x PROBE_K 2.0`. In the warm-lit baths that reflection is mostly
beige wall and floor.
Fix (smallest): give the bath builders their own clones and zone them to the bath probe, e.g.
`const FINMB = { chrome: FINM.chrome.clone(), brushed: FINM.brushed.clone(), gold: FINM.gold.clone(), black: mat.blackMetal };`,
use `FINMB` in `fixMixer`, `fixWallMixer`, `fixHead`, `fixRail`, `fixFlush`, add them to `PROBE_GLOSSY` and
`PROBE_ZONE.set(FINMB.chrome, 'mbath')` etc. (one probe for both baths is enough to get a neutral grey), and lower
`userData.envDay` of the bath clones to about .5. Check the result against the kitchen nickel tap.

### C1. Shower and master-bath walls: a 1 cm strip at the north corner for every 30x60 and 20x60 pick (ensA, ensW)
Evidence: `06c_ensA_c3060_NWcorner_now.jpg`, `06_ensW_c3060_NEcorner_now.jpg` (with the proposed origins: `06d`, `06b`).
At normal distance the strip mostly hides in the corner shadow, but a tiler would never lay it.
Measured (geometry): ensA west wall of the shower (x 4.636) at z -4.98: 1.0 cm for c3060a/b/c and c2060 (the 25x75 page gives
61 cm). ensW east wall (x 6.844) at z -4.98: 1.0 cm, and the cistern-ledge side face (x 5.92) at z -4.98: 1.0 cm.
Cause: `CER_SPACES` lines 3444 and 3445, `o: [4.63, 0]`. The origin's u is an x coordinate, but on walls facing x (`worldUV`,
u = z) the same offset is applied to z, so the z grid lands at 4.63 mod 0.6 from z = 0, i.e. 1 cm from the wall at -4.98.
Fix: `ensA` `o: [5.155, 0]` (worst piece on any visible edge of the shower walls becomes 24.5 cm, from 1.0) and `ensW`
`o: [4.70, 0]` (worst becomes 7.0 cm, from 1.0; acceptable range is narrow: 4.690 to 4.716). Longer term, `cerApply` could take
a separate origin for x-facing faces, which needs an offset written into the UVs at merge time (`worldUV`, line 2627),
since one texture offset serves both wall directions.

### C2. Kitchen splash: cut pieces of 2.5 to 4.5 cm at both corners (kitB)
Evidence: `05_kitB_k2020_east_now.jpg` (narrow column at the window pier), `05c_kitB_k2020_west_now.jpg` (narrow column at the
inside corner), `05e_kitB_k1030_west_now.jpg`; with the proposed origin `05b`, `05d`.
Measured: south splash ends at the pier (x 7.265 to 7.28) with a 3.5 cm piece for k1030 (every other row), k2020, c3060 and
c2060; west splash (u = z) has 2.5 cm for k2020 at z 7.62 and 4.5 cm for k1030 at the corner z 8.79.
Cause: line 3447, `o: [3.645, .92]`, the same shared-offset effect as C1 (west wall u = z).
Fix: `o: [4.015, .92]`: worst visible piece 6.5 cm for all six pages. Valid windows are only about 5 mm wide (3.71, 4.01,
4.31 ... plus 0 to 5 mm), so keep the value exact.

### C3. Family-bath floor, 15x60 page: a 1.5 cm strip along the whole tub apron (bathF, all 12 w1560 items)
Evidence: `03_bathF_w1560_mask_red_slivers.jpg` (top-down mask; red = pieces under 5 cm): 1.5 cm along the apron
(x 3.745 to 3.76, 1.6 m long) and 2.5 cm along the east wall of the laundry niche.
Cause: line 3441, `o: [2.245, -3.575]`: 3.76 - 2.245 = 1.515 = 10 x 0.15 + 1.5 cm.
Fix: `o: [2.138, -3.575]`. Re-measured with the same mask: no w1560 piece under 5 cm; w30 pieces stay 12 cm or more at the
walls and the apron. (Both origins leave one 4 x 12 cm w30 piece at the end of the WC ledge, beside the vanity: hardly seen.)

### C4. Shower niche: thin rows under the sill and at the niche back (ensA, 25x75 and 20x60 pages)
Evidence: `04_ensA_niche_c2575_3cm_rows.jpg`, `04b_ensA_niche_c2060.jpg`.
Measured: the wall below the niche ends at 1.03, so the 25 cm and 20 cm rows leave a 3 cm strip right under the stone sill; with
20x60 the niche top (1.42) leaves 2 cm; with 25x75 the niche back has a 3 cm column at its east side.
Cause: the niche height (1.03 to 1.42, an estimate, lines 1075 and 1643) is fixed while the rows start at the floor (`o`
v = 0). No single origin fits all pages.
Fix options: accept (state it in the notes), or let the niche follow the tile module for a picked page (sill at a row line, e.g.
1.00 for 25 and 20 cm rows, 1.20 for 30 cm rows) when `cerApply` runs for ensA. Owner decision, since the niche size is not on a plan.

### C5. Marble veins draw as random white scribbles on dark and mid-tone marbles
Evidence: `08_veins_f60_matis_black.jpg` (מטיס בלאק), `08b_veins_c2575a_semper_black.jpg` (סמפר שחור); also visible on
קררה (c3060c). They read as hair or scratches rather than veining.
Cause: `cerVeins`, line 3289: each vein is a 22-step random walk with `ang += (R() - .5) * .6`, drawn as a 1 px line plus a faint
halo, so the line curls and doubles back.
Fix: keep the heading nearly straight and add width: e.g. `ang += (R() - .5) * .15`, start `ang` near one diagonal per tile
(`ang = base + (R() - .5) * .5`), draw 2 or 3 parallel strokes with decreasing alpha and `lineWidth` 2 to 4 x `wid`, and blur
(`g.filter = 'blur(1px)'`) the halo pass. Light-on-light marbles hide the problem; dark ones show it.

### F4. Insect screens: on/off is hard to see (screens)
Evidence: `10_screens_off_on_balcony.jpg` (off left, on right, close to balcony door A), `10b_screens_on_entry_view.jpg`.
The screen sash is there and darkens the glass by about 18% (measured mean 146 to 120 in that crop), but it has no mesh texture
and its frame lines up with the door frame, so from the `entry` view (the row's "הצג") nothing visibly changes; it reads as a
slightly tinted pane.
Cause: line 2075, `mScreen` is a flat 32% grey.
Fix: give `mScreen` an `alphaMap` of a fine grid (a 64 px canvas, 1 px lines every 4 px, `repeat` about 1 per 2 cm via world UVs or
`repeat.set(w / .02, h / .02)`), opacity around .55, and point `FIX.screens.view` (line 705) at a view that faces a screened window,
e.g. `master` or `balcony`.

### F5. Oakland vanity (vanF and vanM, all Oakland items): the drawer gap shows as a dotted line between the flutes
Evidence: `09_vanF_oakland_flute_gap_dashes.jpg`.
Cause: line 818: `gap()` draws the drawer split at `xf + .012..014`, behind the flute slats (`xf + .012..018`), so only the bits
between slats show.
Fix: break the slats at the split instead: in the flute loop, draw each slat as two boxes, `y0 + .01..ym - .003` and
`ym + .003..yT - .01`.

### F6. Silquartz and acrylic kitchen sinks look identical
Evidence: `11_kSink_silquartz.jpg`, `11b_kSink_acrylic.jpg`. `mSilq` `#e9e7e1` / .55 and `mAcr` `#f3f2ef` / .3 (line 667) are
both near white; the only visible difference is the rim width. Silquartz (granite composite) is usually grey, black or sand.
The colour of the spec's silquartz sink is not written: ask, or use a mid grey (e.g. `#8d8b87`, roughness .6) so the two choices read
differently. Low priority.

### F7. Kitchen splash 50 cm (splashH = 50): correct
Evidence: `12_splash50_painted_above.jpg`, `12b_splash50_with_k1030.jpg`. Clean painted wall from 1.42 to the cabinets, no
z-fighting, the return beside the hob follows. Open question for the owner: with a ceramic splash picked (kitB) the tile also
stops at 50 cm, because both use `mat.splash` (line 1561). That is consistent with d10 item 1 only if the 50 cm applies to tile too.

### F8. Small geometry notes (not visible in normal views)
- `זן` (square) basin mixer: the lever box starts at `x - .035` (line 744, `fixMixer`), 5 mm into the wall, because the mixer
  sits 3 cm from the wall (`fixVanity` `x0 + .03`, line 831; the default vanity `fixMixer(2.04, ...)`). Hidden by the tap body.
  Fix: `x - .028` like `פרו`.
- Master-bath north wall: in the committed file the comment on line 1075 (`// shower niche cut 9 cm into the wall`) swallows the
  wall segments after it (`W(6.015, ...)` to `W(8.91, 9.30, ...)`), so the window jambs, the wall east of the window and the
  closet north wall are missing behind the tile; my floor mask showed the floor running 3 cm behind the wall tile there.
  The working tree already splits that line (uncommitted change by another agent, `git diff source/salon.html`).

## Checked and fine
- WC (5 models) in both baths: on the wall / ledge face, nothing floating, no intersection (`14c_sheet_wc.jpg`).
- Flush plates (6): flat on the ledge faces in both baths.
- Tub (2): rectangular and rounded fit the tiled apron; drain at the tap end.
- Bath tap (18), shower tap (9), head (4), rail (4): on their walls, no intersections; the family rail and bath tap are on the
  corridor wall (see F2 for the view).
- Basin taps (16) in both baths: spouts end over the basin, 8 to 12 cm inside the bowl edge (`14d_sheet_basin_taps.jpg`).
- Vanities: all 51 family-bath and 28 master-bath options fit between the walls, the glass and the door, tops level, mirror
  cabinets clear (`14_sheet_vanF_all51.jpg`, `14b_sheet_vanM_all28.jpg`). Roma puts the basin on 2/3 by design.
- Kitchen taps (9): spouts over the bowl, clear of the wall cabinets, bases clear of the splash.
- Door hardware (3): handles, roses, escutcheons and bath turn-locks all follow the pick; evening fine.
- Ceramic textures: no stretching on any face (world UVs on every ceramic material, `userData.uv` set for all nine), grids
  continuous across adjacent pieces of the same plane, glossy items show the window highlight, decor reliefs (wave, cube, ribs,
  mosaic, lace, origami) render; Playground (k2020) and encaustic floors OK.
- Grout at floors of salon/kitchen/entry/corridor/mamad (80 and 60), bedrooms, balcony: no visible piece under 5 cm. The family
  bath with 33x33 and the master bath floors: none at visible edges.
- Reset button and `cerReset()`: every select, state and material back to the default; nothing persisted.
