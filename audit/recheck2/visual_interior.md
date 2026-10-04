# Visual review, interior (recheck2, 2026-10-04)

Scope: all 33 views, day and eve, desktop 1440x900, HQ on (TAA + GTAO + bloom), built site on 127.0.0.1:8791.
Screenshots: `source/out/qa/rc2_int/desktop_{day,eve}_<view>.jpg` (66) plus close-ups `close_day_*_6s.jpg`
(6 s settle) and `close_day_*_nohq.jpg` (HQ off, so no GTAO), and `desktop_day_tubC.jpg`.
Line numbers refer to `source/salon.html` at commit 8cec3d9. No geometry or wall changes are proposed.

Key finding: the grainy, streaky look on curtains, cables and thin dark frames is **GTAO**, not unconverged TAA.
It is still there after a 6 s settle and disappears completely with HQ off
(`close_day_curtC_6s` vs `close_day_curtC_nohq`, `close_day_isle2_6s` vs `close_day_isle2_nohq`).

## Defects, ranked by visible impact

| # | Views | What is wrong | Where | Fix |
|---|---|---|---|---|
| 1 | entry, photo, kitchen, tvwall, sofa, isle2, inside (day and eve) | The sheer living-room and kitchen curtains render as dark grey barcode streaks. With HQ off they are soft white. Cause: GTAO draws its depth and normal pass with an override material that ignores `transparent`/`opacity`. The 72% sheer (`depthWrite:false`, sine folds of ±6 cm) is treated as a solid folded surface, so the folds get deep AO stamped over the window behind them. | GTAO L262-269; `sheer` L1002; `curtain()` L729-736; `curtainPair` L1006 | Hide every curtain mesh from the AO pass: `noAO.push(c)` inside `curtain()` (this covers `curtainPair`, the master sheer L1326 and the room 1/2 linen L1508/L1516). It is the same mechanism already used for the tree cards. |
| 2 | island, isle2, kitchen, kitchen2, kitchen3, entry, photo, tvwall, corr2, desk, sofa | Grey smeared halos and speckle around thin dark objects against bright ceilings and walls: the frames pendant (cables and frames), the flush three-frame lamp, stool legs, chair edges, art frames in corr2, and the contact line under the TV base cabinet. The noise is static, so TAA does not average it out. | GTAO L263 (`radius .5, thickness 1.2, scale 1.2`), denoise L264 | (a) Push the pendant cables (radius ≤ 1 cm, `ceilGroup`) into `noAO`. (b) Lower `thickness` 1.2 to about .4 and `radius` .5 to about .3, so thin foreground objects stop occluding the wall 0.5 m behind them. (c) Raise denoise `radius` 6 to 8 and `depthPhi` 2 to 4. Then re-check a corner (room1) to make sure contact AO is kept. |
| 3 | bath2, bird2 | The family bathtub is a solid block filled to the brim. The inner "basin" box spans y .40-.585 and its top is 5 mm **above** the rim (.58), so the tub reads as a flat white slab with no water space (`desktop_day_tubC.jpg`). | L1439 | Build the basin hollow the way the kitchen sink is built (L1248-1249): a floor at .40-.42 and four 2 cm walls up to .58, each in `ceramicIn`. Add a drain disc and an overflow plate at the tap end (z about -1.5). |
| 4 | shower, mbath, closet, bath2 | Both shower niches are flat beige panels **floating 3-4 cm in front of the tile**, not recesses. Master: the panel at z -4.964..-4.945, with the tile face at -5.004 (withShift adds no z shift). Family bath: the panel at x 4.444-4.454, with the tile face at 4.484 (`close_day_nicheC_6s`). | L1360, L1445 | Put the back panel on the tile face (z -5.002 / x 4.486) in a slightly darker tone, and add four 1.5 cm reveal strips (top, bottom, sides) protruding 8 mm in `bathWall`, plus a 1 cm sill. This gives the shadow edge of a real recess without cutting the wall. Optional: two bottles on the sill. |
| 5 | storage eve, kitchen2 eve, isle2 eve, master2 eve, corr2 eve | Blown hotspots in eve. Three warm point lights at k=5 sit close to white surfaces: the wave pendant fill [1.2, y 1.95, z 1.79] is 0.6 m from the white storage doors; the island light [5.99, y 2.0, 6.31] is 1.1 m above the white quartz; the master fan light [6.8, -1.5] saturates the fan. Bloom (strength .3, threshold .95) then flares them. | `warm` list L1954, bloom L270 and L2197 | Set k to 2.5-3 for the first three entries, and raise the island light to y 2.3. Set the eve bloom threshold to 1.0, or strength .3 to .22. Check that the eve exposure (1.2) still lifts the corners. |
| 6 | balcony, balcony2, view, inside, isle2, bird1, bird2 (eve) | In eve the neighbouring facades stay a bright daylight beige under a dusk sky. Only a few lamp points are lit and no windows glow. (Overlaps with the exterior agent.) | `setMode` L2193-2207, outside materials | In `setMode(eve)`, scale the colour of the `outside` facade materials by about .35 and give a random subset of the window panes a warm emissive (k about 1.5). |
| 7 | kitchen2, kitchen3 | The kitchen sink reads as a flat dark-grey rectangle: uniform mid-grey steel (rough .62, metal .35), no visible depth cue, and a drain in `fluteBack` that vanishes on the dark steel. The faucet is a straight 8 mm post with a pale square block at the spout end (`close_day_sinkC_6s`). | sink L1248-1250, `sinkSteel` L504, faucet L1256 | Brushed steel `#b9bdc0`, rough .35, metal .8. Drain: a steel ring of 4.5 cm with a dark 3 cm centre. Faucet: a gooseneck arc (TubeGeometry, r 1.2 cm, about 25 cm reach) in place of the post and box. |
| 8 | room1, room2, room3, corridor, corr2, bedtv (day and eve) | Ceilings read mid-grey, clearly darker than the walls. The only light reaching a downward-facing surface is the hemisphere ground colour `#b3a58e` at .22. The window RectAreaLights face sideways. | L1933, `mat.ceil` L476 | Set the hemi ground colour to `#d9d2c4`, or give `mat.ceil` an emissive of about .04 in day and .02 in eve (switched in `setMode`). This stands in for floor bounce. It is an estimate, not a measured value. |
| 9 | entry, photo, tvwall, sofa (day) | The living room looks overcast. The sun (about 45 deg, ESE, L1935) is cut off by the covered balcony, so no sun patches reach the interior floor, while the deck outside is strongly sunlit. The contrast inside comes only from AO. | sun L1934-1938, `winLight` L1945-1946 | Either raise the two balcony `winLight` k from 5 to 6.5, or lower the sun to about 30 deg so a patch reaches the first metre of floor inside. The sun angle is an estimate anyway (PROJECT_MEMORY). |
| 10 | master, bedtv, bird2 | The slat wall grain is a large, orange, flame-figured veneer (photo `oak_veneer_01` at 1.83 m) on 6.2 cm slats. It reads as rotary plywood, and it turns very orange in eve. | slats L1309, `photoPBR` oak L555 | Give the slats their own clone of `mat.oak` with the map repeat ×3 across the slat (straight-grain look) and colour `#c9a77f`, or switch to `walnut` with a fine-grain canvas. |
| 11 | tvwall eve, sofa eve | Downlight emissives (`mat.spot` 2.2) reflect as hard white discs in the glossy TV screen and the porcelain slab, then bloom. | `mat.screen`, slab material L1088, `setMode` L2201 | Raise the TV screen roughness to about .25 and the slab to about .35, or lower `mat.spot` in eve from 2.2 to 1.6. |
| 12 | service, bird2 | The service-balcony louvres are flat untextured bars. The AC condenser is a plain box with a flat black disc and no grille, pipes or drain. | louvres L1480, condenser L1482 | Louvres: tilt each blade about 35 deg and give a slight gradient. Condenser: a ring grille (5 concentric thin tori), two copper/insulated pipes to the wall and a drain hose. |
| 13 | master | The right bedside pendant cord drops out at distance (r 4 mm, 6 segments). It shows in `bedtv` but not in `master`. | `pendantGlobe` L737 | Cord r .006 and add it to `noAO`. |
| 14 | hall, entry | The white skirting on white paint is practically invisible (`close_day_hallC_6s`), so walls look like they meet the floor directly. | skirt material L894 | Skirting tone `#e4e2dc`, or add a 5 mm dark shadow strip at its top (y .08). |
| 15 | balcony2 | A dark vertical stripe behind the egg chair at the north end of the balcony wall. It belongs to the exterior or facade geometry, so it is left to the exterior agent. | exterior section | See `audit/recheck2` exterior report. |

Checked and not a defect:
- Room 1: the four plates at 1.80 m (L1678, `'sstd'`) come from the electrical plan, so they belong to the electrical agent.
- Master2: the pale rectangle near the bed foot is a sun patch from the east window.
- The range hood is integrated flush in the wall cabinets (intake slot L1268).
- A hand shower on a rail exists in both showers.
- The kitchen sink bowl geometry exists; only its material reads flat.
- TAA convergence: 1.5 s vs 6 s makes no visible difference.

## Realism upgrades, ranked by payoff

| # | Views | Upgrade | Where | How |
|---|---|---|---|---|
| 1 | kitchen3, kitchen | Induction hob: today it is a plain black slab with a single blurred reflection | L1258 | Give `mat.screen` a canvas map with 4 thin grey zone rings (two of 18 cm, two of 14.5 cm) and a touch-control strip at the front edge, plus a 3 mm bevelled steel or black frame. |
| 2 | entry, inside, isle2, balcony, master, room1-3 | Slider and window handles: no aluminium slider or window has a handle | `slider()` about L990, `windowX/windowZ` | A 30 cm black flush pull on the active leaf of each slider (y 1.0-1.3) and a black lever handle at 1.25 m on each window sash. |
| 3 | bath, bath2, mbath, shower | Bath textiles and accessories: the towel ladders and hooks are bare, and there are no bottles | ladders L755, L1380, L1474; hooks L1455, L1471 | Folded towels on each ladder (a box with rounded 2 cm edges in `linen`/`sageFab`), one hanging towel per hook, a soap dispenser on each vanity, two bottles in each shower niche. |
| 4 | master, room1, room2, room3, closet | Rugs: flat 12 mm slabs with a woven `fab` canvas, which read as painted floor | `rug()` L711, `rugGrey/rugKid/rugBlue` L491 | 2 cm thickness with `round .01`, a pile-noise canvas, and a soft fringe on the two short ends for the master rug. The `berber` treatment in the living room shows how. |
| 5 | kitchen, kitchen2, kitchen3, island | Kitchen life: the counters are almost empty | south run L1255-1270 | A kettle, an oil/salt tray by the hob, a dish towel over the oven door, a small herb pot on the sill, a fruit bowl already on the island. Keep to 4-5 items. |
| 6 | all eve views | Lit-window night exterior (see defect 6) | `setMode` | Same fix. It is the largest single eve realism gain through the glass. |
| 7 | service, bird2 | AC condenser detail (see defect 12) | L1482 | Same fix. Add the pipe run from the master and kids' AC units if visible. |
| 8 | bath2, bath | Tub: drain, overflow, a filler spout at the tap end and a rounded inner corner radius (after defect 3) | L1439-1444 | Use rounded basin boxes (`round .03`). Place the filler spout at the drawn position (20 cm from the east wall). |
| 9 | tvwall, sofa, inside | Sheer realism after defect 1: a faint translucency gradient (top hem, bottom weighted hem) and slight sway | `sheerTex` L999-1001 | Add a 4 cm denser hem band at the bottom and a 6 cm heading tape at the top in the canvas. Optional: an idle 1-2 mm vertex wobble on the open stacks. |
| 10 | kitchen2, closet, master, room1-3 | Cabinet and wardrobe hardware: the wardrobes have bar pulls; the kitchen tall wall and the storage wall are intentionally handleless. Add push-latch shadow gaps so the doors read as doors | storage wall about L1142, kitchen tall wall L1204-1240 | A 3 mm dark reveal between every door (some already exist), widened to 4 mm with `mat.black`, plus a 1 cm finger-pull chamfer on the bottom edge of the upper kitchen doors. |

Already good, no action:
- door levers on interior doors
- switch and socket plates
- master AC indoor unit, corridor return grille
- mamad blast shutter box and filter unit
- washer/dryer stack
- reflective mirrors (desktop HQ)
- heated towel ladder in the ensuite
- under-cabinet LED in eve
- balcony plants and furniture
- integrated hood
- coffee bar niche lighting
- wave pendant and frames pendant shapes (only their AO noise is wrong)

## Suggested order

1. Defects 1 and 2: GTAO `noAO` for curtains and cables, then retune thickness and radius. This removes most of the visible noise in about 10 lines.
2. Defects 3, 4 and 7: tub, niches, sink material and faucet. Local geometry only, no walls touched.
3. Defects 5, 8 and 11: eve light levels and ceiling fill, then re-capture day and eve for all views.
4. Upgrades 1-5.

After the change: `build_site.py`, then re-capture `curtC`, `isle2`, `storage` eve, `bath2` and `shower` with
`out/quick.mjs`. Neither `roomdims.py` nor `clearance_audit.py` is affected unless the tub or niche boxes move.
