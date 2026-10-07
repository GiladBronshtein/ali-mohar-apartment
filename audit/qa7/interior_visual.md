# QA7: interior, visual (desktop and phone, day and eve, fixture picker)

Built site at http://localhost:8000/ (index.html from salon.html at e94c72c). Line numbers refer to `source/salon.html` at
e94c72c. All runs had no page errors and no console errors.

What was captured (scripts and raw shots in `source/out/qa7_interior_visual/`):
- 29 interior presets, day and eve, desktop 1200x800 (`p/`).
- 13 presets on a phone (375x812, Android UA, touch, DPR 2), day and eve, plus 7 phone fixture shots (`ph/`).
- 75 eye-height cameras: every room centre looking E, W, S, N (fov 85, ceiling and floor edges in frame) and up; 20 of
  them again in eve (`c/w_*`, `c/we_*`). Door thresholds open, closed, closed in eve (`c/th_*`). Curtains closed, day and
  eve (`c/cu_*`). Ceramics: the middle item of every catalog page on every space at a corner camera (`c/ce_*`). Glossy
  80x80 on both floor spaces, day and eve (`c/gl_*`).
- Fixture picker (`a/`, `b/`): every option of every FIX entry applied with `fixSet`, each from a close camera and a
  room camera (WC 5 x 5 cameras, flush 6 x 2, tub 2 x 10 incl. eve, bath tap 18 + 9, shower tap 9, head 4 x 2, rail 4 x 2,
  kitchen sink 3 x 7 incl. eve, kitchen tap 9 x 2, basin tap 16 x 2 plus side views of every swan). Vanities: all 50
  family-bath and all 27 master options with the default tap, every model also with the swan tap (front and side) and the
  Pro tap, eve, room views; the "cur" vanities with swan, Pro, LOOP, Zen and Ruby taps from the side and from above.
- `probe2.mjs`: reads material and bounding-box values from the live page (results quoted below).

## Findings

1. **Rounded tub (מעוגלת): the tub floor shows the apron's wall tiles, and its walls fight with the tile ring.** CONFIRMED.
   Where: `fixSet('tub','מעוגלת')`, any camera looking into the tub, desktop and phone, day and eve. From the tub end
   (pos [4.1,1.1,-3.0] tgt [4.1,.45,-1.6]) the whole floor is beige 60x120 tiles with grout; from above (pos
   [4.1,1.6,-2.4] tgt [4.1,.4,-2.0]) it is striped. Images `01_round_tub_floor_shows_tiles.jpg`,
   `01_round_tub_top_stripes.jpg`; phone `ph/ph_tub_round_top.jpg`.
   Cause: line 771. The back-face liner is `RoundedBoxGeometry(x2 - x1, .18, z2 - z1, 4, .085)` centred at y .49, so it
   spans exactly y .40..58 and x1..x2, z1..z2 (probe: `[3.84,4.38,0.4,0.58,-2.89,-1.485]`). Its floor (a back face, drawn)
   is coplanar with the top of the apron block `B(X1, X2, Z1, Z2, 0, .40, mat.bathWall2)` (line 769), and its four walls
   are coplanar with the inner faces of the tile `ring(...)` at .40..56 and the ceramic rim at .56..58. The rounded top
   edges also curve away from the rim, so a band of ring tile shows under the rim. The drain (line 774, y .41..414) floats
   1 cm over the liner floor.
   Fix: an open bowl with vertical walls, inset 4 mm, floor at .41, plus a deck plate over the rim corners:
   ```js
   const rrect = (w, h, r) => { const s = new THREE.Shape(), x = -w / 2, y = -h / 2; s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
     s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; };
   // in fixTub, rounded branch (line 771):
   const bw = x2 - x1 - .008, bd = z2 - z1 - .008, g = new THREE.ExtrudeGeometry(rrect(bw, bd, .085), { depth: .17, bevelEnabled: false, curveSegments: 8 });
   g.rotateX(-Math.PI / 2); const l = mesh(g, mTubIn, root, false); l.position.set((x1 + x2) / 2, .41, (z1 + z2) / 2); l.receiveShadow = false; noAO.push(l);
   const deck = new THREE.Shape(); deck.moveTo(-(x2 - x1) / 2, -(z2 - z1) / 2); deck.lineTo((x2 - x1) / 2, -(z2 - z1) / 2); deck.lineTo((x2 - x1) / 2, (z2 - z1) / 2); deck.lineTo(-(x2 - x1) / 2, (z2 - z1) / 2);
   deck.holes.push(rrect(bw, bd, .085)); const dg = new THREE.ExtrudeGeometry(deck, { depth: .004, bevelEnabled: false }); dg.rotateX(-Math.PI / 2);
   mesh(dg, mat.ceramic).position.set((x1 + x2) / 2, .58, (z1 + z2) / 2);
   ```
   (rotateX(-PI/2) turns the extrusion axis to +y; the bottom cap faces down, so the BackSide material draws it from
   above and culls the top cap.)

2. **Inset kitchen sinks (נירוסטה, סיליקוורץ): dark graphite and quartz patches flicker on the bowl walls.** CONFIRMED.
   Where: `fixSet('kSink','נירוסטה')` or `'סיליקוורץ'`, visible even from the `kitchen3` preset, desktop and phone, day and
   eve. Images `02_inset_sink_zfight_silq.jpg`, `02_inset_sink_zfight_steel.jpg`; phone `ph/ph_sink_silq.jpg`.
   Cause: line 783. The liner `RoundedBoxGeometry(b - a, .2, d - c, ...)` at y .82 spans exactly the counter hole a..b,
   c..d from .72 to .92. Its walls share planes with the inner faces of the counter pieces (line 1475, .88..92) and of the
   graphite cabinet rim pieces (line 1472, `[4.25, SK1 + .05, ...]` etc., .69..88). The rounded top edges also leave the
   counter edge visible under the rim, and the rim (line 782) sits outside the hole only.
   Fix: same shape as finding 1, inset 4 mm, and a rim that overlaps the hole edge:
   ```js
   const r = q ? .07 : .05, bw = b - a - .008, bd = d - c - .008, cx = (a + b) / 2, cz = (c + d) / 2;
   const g = new THREE.ExtrudeGeometry(rrect(bw, bd, r), { depth: .2, bevelEnabled: false, curveSegments: 8 }); g.rotateX(-Math.PI / 2);
   const l = mesh(g, mi, root, false); l.position.set(cx, .72, cz); l.receiveShadow = false; noAO.push(l);
   const rim = rrect(b - a + 2 * w, d - c + 2 * w, .01); rim.holes.push(rrect(bw, bd, r));
   const rg = new THREE.ExtrudeGeometry(rim, { depth: .008, bevelEnabled: false }); rg.rotateX(-Math.PI / 2); mesh(rg, m, root, false).position.set(cx, .92, cz);
   ```
   and drop the four rim boxes on line 782.

3. **Swan basin tap (ברבור) runs into the family-bath mirror cabinet.** CONFIRMED.
   Where: any family-bath vanity (cur or spec) with any `|swan` basin tap; side camera pos [2.55,1.2,-1.5] tgt
   [2.12,1.05,-2.15]. The arch disappears into the cabinet and the spout comes out below it. Image
   `03_swan_into_mirror_cabinet.jpg`. In the master bath the arch touches the cabinet underside.
   Measured (probe, Box3 of the tube): family top 1.173, cabinet bottom 1.15 (line 1711), LED strip 1.144..1.15, tube x
   2.024..2.179 inside the cabinet's x 2.01..2.15. Master top 1.153 against the cabinet bottom 1.15 (line 1624).
   Cause: line 734, the swan curve peaks at y + .31 (+ .011 tube radius) over tops at .85 (family) and .83 (master).
   Fix (line 734): lower the arch by 5 cm so it clears both cabinets:
   `[V(0, .11), V(0, .21), V(.04, .26), V(.1, .25), V(.13, .21)]` (top at about topY + .27: family 1.12, master 1.10).

4. **Metal finishes and new vanity colours change brightness with history: the same chrome plate is silver or charcoal.**
   CONFIRMED (probe).
   Where: pick a chrome flush plate: `envMapIntensity` 1.0. Call `setMode` once (any day or eve toggle): 0.3, and the plate
   reads near black. Image `04_chrome_flush_same_choice_two_looks.jpg` (same option, same lighting, before and after one
   setMode call). A vanity colour picked for the first time gets 1.0 while every other material has 0.3 by day and 0.12 by
   eve (probe: `newVanityColour [1]`, `others [0.3, 1]`). In eve, a metal that was not in the scene at the switch keeps
   its day value (shots `vanF_00_eve`: 0.12 and 0.30 mixed).
   Cause: line 2871 sets `envMapIntensity` once at load and line 2865 only on a mode switch, both by traversing the scene.
   FINM metals (line 670) are not in the scene at load (default taps are black), and `vanCol` (line 799) creates materials
   lazily. `fixDraw` never applies the current mode.
   Fix: in `fixDraw` (line 707), after the build:
   `s.g.traverse(o => { if (o.isMesh && 'envMapIntensity' in o.material) o.material.envMapIntensity = isEve ? .12 : (o.material.userData.envDay ?? ENV); });`
   and give the metals their own day value so chrome reads as chrome at ENV .3:
   `FINM.chrome.userData.envDay = .9; FINM.brushed.userData.envDay = .7; FINM.gold.userData.envDay = .8;` (estimates; tune by eye).

5. **Spec vanities in the family bath sit 7 cm off the mirror cabinet and the plumbing axis.** CONFIRMED.
   Where: every `vanF` option, camera pos [3.1,1.35,-2.12] tgt [2.15,.9,-2.15]; the 60 cm units look visibly shifted
   north under the 84 cm cabinet. Image `05_family_vanity_off_mirror_axis.jpg`.
   Cause: line 1702 centres spec vanities at z -2.185 (the centre of the old 100 cm unit). The basin axis on the plumbing
   plan is 72 cm from the south wall, z -2.115, which is where the "cur" basin and the mirror cabinet (line 1711, centre
   -2.115) are.
   Fix (line 1702): `fixVanity(2.01, -2.115, +v.split('|')[2] / 100, .85, v, t)`. The 80 then spans -2.515..-1.715, clear
   of the WC ledge (-2.955) and the hooks. The master one (centre -3.67 vs cabinet -3.71) cannot move north: at -3.71 it
   would hit the shower frame at z -4.035. Leave it.

6. **Kitchen tap "זן" is drawn as the round Omega gooseneck.** CONFIRMED.
   Where: `fixSet('kTap','זן')` is identical to `'אומגה ניקל'`. Image `07_kitchen_tap_zen_equals_omega_nickel.jpg`.
   Cause: line 787 maps every non-Omega key to chrome, and `fixKTap` has no branch for זן, so it falls through to the
   default gooseneck (line 795). Zen is the square series (TAPS line 673, body `square`).
   Fix: add a square branch before the gooseneck, e.g.
   `if (key === 'זן') { B(x - .016, x + .016, 8.724, 8.756, .92, 1.25, m); B(x - .011, x + .011, 8.53, 8.756, 1.22, 1.25, m); B(x - .011, x + .011, 8.53, 8.552, 1.17, 1.22, m); lever(); return; }`

7. **Pro and Grohe basin taps: the top lever runs 2.5 to 4.5 cm into the wall tile.** CONFIRMED by geometry (hard to see:
   the lever reads as touching the wall).
   Cause: line 739 `B(x - .075, ...)` and line 740 `B(x - .055, ...)` with the tap at x0 + .03 (line 823) or 3 to 4 cm from the wall in the "cur" vanities (lines 1623, 1709),
   so the lever ends at x0 - .045 and x0 - .025.
   Fix: `B(x - .028, x + .005, ...)` (line 739) and `B(x - .025, x + .01, ...)` (line 740).

8. **The nine bath bar mixers (סוללה) are one shape; the concealed mixers have two.** CONFIRMED.
   Where: `bathTap_*|bat` shots: Omega, Pro, Zen, Ruby and the three Grohe series differ only in finish. The picker lists
   them as separate products.
   Cause: `fixWallMixer` (line 743) returns the same bar for every series; the concealed plate is round or square only.
   Fix (low): at least vary the bar body by `st` (round tube for Omega and Grohe, square bar for Zen, thin for Ruby), the
   way `fixMixer` does. Or say in the panel note that the bar mixer is shown in one generic shape.

9. **Master shower niche is a flat taupe board on the tile.** CONFIRMED (realism).
   Where: preset `shower`, every `ensA` ceramics option (`c/ce_7_*`). It reads as a sticker, not a recess. Same in the
   family bath (line 1691).
   Cause: line 1600 `B(4.72, 5.22, -4.974, -4.968, 1.05, 1.40, mat.nicheBack ...)` is 6 mm thick with only a bottom ledge.
   Fix: frame it so it reads as a recess: add side and top returns in the wall-tile material, e.g.
   `[[4.72, 4.735], [5.205, 5.22]].forEach(([a, b]) => B(a, b, -4.98, -4.95, 1.05, 1.40, mat.sage)); B(4.72, 5.22, -4.98, -4.95, 1.385, 1.40, mat.sage);`
   (inside the shift block), and darken `nicheBack` slightly so the back reads as set in.

10. **Default porcelain floor (מלרוז אפור) is blurry and blotchy at close range.** CONFIRMED (realism).
    Where: every threshold shot (`c/th_*`), corridor, living. Large soft grey clouds, no fine grain; it reads as dirty
    concrete rather than a matt porcelain tile.
    Cause (SUSPECTED): `cerTex` case `'cem'` (line 3211) layers two `cerNoise` passes at alpha .2 and .22 (soft-light);
    the second pass at `big * 40` cells is what shows as clouds at 1 to 2 m.
    Fix: lower both alphas to about .08 to .1 and add one fine pass (several hundred cells, alpha .05) for grain.

11. **Tile joints on x-facing walls still do not start from a corner.** CONFIRMED (already open in PROJECT_MEMORY, still
    present).
    Where: shower walls (`c/ce_7_ensA_*`): the first vertical joint on the west wall is a part-tile from the corner.
    Cause: `CER_SPACES` offsets (line 3267 on) use `o: [x, 0]` for wall spaces, so walls along z take the x origin.
    Fix: give each wall space a z origin for x-facing walls (for example `oz: -4.98` for ensA, ensW) and use it in
    `cerApply` when the face normal is along x.

12. **Code: liner meshes pile up in `noAO`.** CONFIRMED by code. Each `fixDraw` of the tub or the sink pushes a new mesh
    to `noAO` (lines 771, 783); removed meshes stay in the array, so the GTAO hide loop grows with every pick.
    Fix: in `fixDraw`, before the build, `for (let i = noAO.length; i--;) if (!noAO[i].parent) noAO.splice(i, 1);`

## Room ratings (realism, 1 to 10) and the single change that would raise each most

| Room | Rating | Single change |
|---|---|---|
| Living and storage wall | 7.5 | Finer, calmer porcelain texture (finding 10). |
| Kitchen | 7 | Default undermount sink reads as flat pale-blue paint: brushed steel normal map and a higher envDay on `mat.sinkSteel`. |
| Entry and hall | 7 | Porcelain texture (finding 10). |
| Corridor | 6.5 | Porcelain texture (finding 10); the long run makes the blotches obvious. |
| Master bedroom | 8 | Bedding is rounded boxes: soft folds on the duvet and pillows. |
| Closet | 6 | Wardrobe fronts are plain dark-grey slabs: a subtle grain or panel and warmer light inside. |
| Master bath | 6.5 | Recessed niche (finding 9). |
| Family bath | 6.5 (4 with the rounded tub) | Fix the rounded tub (finding 1); with the default tub, the tub interior is a flat white box. |
| Laundry niche | 6 | Readable now through the window; little else to gain. |
| Room 1 | 7 | Bedding folds, as in the master. |
| Room 2 | 7 | Same. |
| Mamad | 6 | Steel blast window and door frames read as thin painted trims: give the window frame its real depth. |
| Balcony | 7.5 | Fine as is; the sofa cushions are the weakest item. |

## Checked and fine

- QA6 fixes are in and work: both basins are real bowls (cur and every spec vanity); closet LED is a ceiling cove; laundry
  pipes run to the slab; the second condenser is on a stand; no dark band in the door reveals in eve (`c/th_*_closed_eve`);
  `service` preset is readable on desktop and phone; family-bath hatch frame sits on its panel; the closet is lit in eve;
  curtains in rooms 1 and 2 close; kitchen sill no longer coplanar.
- WC: all 5 models in both bathrooms sit against the ledge, centred on the flush plate, no gaps or overlaps, no floating.
- Flush plates: all 6 centred on the WC axis, on the ledge face, below the ledge top.
- Shower tap, arm and head, rail and Milano set: on the wall, right height and side, no clipping with the glass or the
  niche; the family-bath rail stays clear of the glass screen.
- Bath tap: concealed 4-way with the overflow filler and the bar mixer sit on the corridor wall over the tub end, clear
  of the glass screen and of the open door leaf (leaf rests at x 3.68, screen at 3.76).
- Rectangular tub: clean from all 10 angles, day and eve.
- Undermount sink and all 9 kitchen taps: on the counter behind the bowl, spouts over the bowl, nothing in the splash.
- Spec vanities, all 77 options: no part in the wall, the shower frame (master: 1.5 cm gap) or the WC ledge; wall-hung
  bodies at .30, Millennium legs on the floor; Roma's shelf, Oakland's flutes, Melbourne's glass frame and the handles
  read correctly; basin and mixer aligned on every model (mixer on the basin axis, behind the bowl).
- Doors: every leaf closes into its frame with no gap; open leaves clear every fixture; thresholds clean (porcelain to
  plank at the wall line, no strip, no z-fight).
- Curtains closed: living sheers, master voile, rooms 1 and 2, kitchen zebra; day and eve.
- Ceramics: every catalog page on every space applies; grout lines reach the corners and the counter edge on floors, the
  kitchen splash and the bath walls (except finding 11); the balcony options replace the deck.
- Glossy 80x80 on both floor spaces: no clipping, joints visible, light by day, calm in eve.
- Skirting follows the floor material in every room; kids' items (desks, shelves, step and hooks in the family bath)
  intact.
- Phone: presets frame correctly above the bottom sheet; the same fixture defects appear on the phone (findings 1, 2, 4),
  nothing phone-only.
