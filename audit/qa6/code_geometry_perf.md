# QA6: code, geometry and performance (code_geometry_perf)

Scope: code review of `git diff 6b679fd..HEAD -- source/salon.html` (re-check 5), a scan of the whole file for code hidden in
comments, a pre-merge geometry scan of the live page, performance and load numbers, and robustness. Line numbers are
`source/salon.html` at e94546d.

Method. A Playwright run served an in-memory copy of `index.html` that records every mesh's world box, material and source
line just before `mergeGroup` (5677 meshes, 4780 boxes). Python then looked for coplanar same-facing faces with different
materials (gap 1 mm inside, 3 mm outside; a face counts only if a point 2 mm in front of it is not inside another opaque box),
boxes inside other boxes, isolated objects, tops near the old ceiling, and sunBoxes without matching geometry. Shots, perf
and robustness came from separate runs, all through `/tmp/gpu.sh`. Scripts and raw output: `source/out/qa6_code_geometry_perf/`.

## Findings

1. **Basins and the kitchen sink are filled by their cabinets.** CONFIRMED. The new one-piece ceramic tops cut a bowl 13 cm
   deep (`ceramicTop`, line 1448), but the cabinet under them is a solid box up to the top's underside. In the master bath you
   look into the basin and see walnut 3 cm down; in the kids' bath the white cabinet top. The kitchen undermount sink
   (older code) shows the graphite cabinet top 4 cm under the counter, with the drain buried. Visible in the preset `closet`
   view too. Images: `code_geometry_perf_img/mbasin.jpg`, `kbasin.jpg`, `sink.jpg`, `closet.jpg`.
   Cause: line 1460 `B(4.44, 4.92, -4.07, -3.39, .45, .80, mat.walnut, ...)`, line 1547 `B(2.01, 2.44, -2.695, -1.675, .10, .82, paint)`,
   line 1303 `B(4.25, FX, 8.19, 8.79, .10, .88, mat.graphite)`. Fix: lower each carcass under the bowl and ring the hole:
   ```js
   // 1460 (master, inside the withShift)
   B(4.44, 4.92, -4.07, -3.39, .45, .66, mat.walnut, { round: .006 });
   [[4.44, 4.92, -4.07, -3.97], [4.44, 4.92, -3.55, -3.39], [4.44, 4.55, -3.97, -3.55], [4.87, 4.92, -3.97, -3.55]].forEach(([a, b, c, d]) => B(a, b, c, d, .66, .80, mat.walnut));
   // 1547 (kids' bath)
   B(2.01, 2.44, -2.695, -1.675, .10, .68, paint);
   [[2.01, 2.44, -2.695, -2.325], [2.01, 2.44, -1.905, -1.675], [2.01, 2.11, -2.325, -1.905], [2.41, 2.44, -2.325, -1.905]].forEach(([a, b, c, d]) => B(a, b, c, d, .68, .82, paint));
   // 1303 (kitchen; sink a..b = 4.90..5.60, c..d = 8.24..8.69, bottom .70)
   B(4.25, FX, 8.19, 8.79, .10, .69, mat.graphite);
   [[4.25, 4.90, 8.19, 8.79], [5.60, FX, 8.19, 8.79], [4.90, 5.60, 8.19, 8.24], [4.90, 5.60, 8.69, 8.79]].forEach(([a, b, c, d]) => B(a, b, c, d, .69, .88, mat.graphite));
   ```

2. **The rounded SE corner of the new lot wall floats 6.35 m above the street.** CONFIRMED (new in 96821de). From the corner
   of Ali Mohar and Tirtsa Atar it reads as a white curved band across building B at first-floor height. Image:
   `corner_street.jpg`. Cause, line 2058: `B(...)` puts the centre at `GY + wallH / 2`, then `w.position.set(x, 0, z)` resets
   y to 0, so the six pieces span y -0.25..0.25. Fix:
   `w.position.set(6.1 + R * Math.cos(am), GY + wallH / 2, 39.7 + R * Math.sin(am));`

3. **A 45 cm open slot runs around the shell between floor 1 and our floor.** CONFIRMED. The floor-1 and ground boxes stop
   at `GY + 6.15` (y -0.45) and our walls start at y 0. Nothing fills -0.45..0, and our floor plane is one-sided, so every
   outside view shows a lit band (the top of the floor-1 box seen through the gap) under the north, west and master east
   walls. Seen in the preset `bird2` view. Images: `bird2_slot.jpg`, `west_out.jpg`. The gap predates re-check 5 (ext6), but
   re-check 5 rebuilt these boxes and kept it. Fix, lines 1887-1888: top both boxes at `GY + 6.59` (1 cm under the floor plane,
   no z-fight) and push the sunBox with `6.59`.

4. **`block()` still has code inside a comment (the past bug pattern).** CONFIRMED. Line 2146 ends with
   `// whole bays per face (...) foot.push([x1, x2, z1, z2]); sunBoxes.push([x1, x2, z1, z2, h + 1.4]);`. Since 40ed7eb the 29
   residential blocks throw no baked ground shadow, get no base AO and no paved apron, and courtyard trees ignore them: 15 of
   the 81 courtyard trees stand inside a block and 5 more within 2 m of a wall (crowns through facades). Fix: move the two
   calls onto their own line after the `for` loop. Note: the courtyard trees then reshuffle (same RNG, different skips), and
   blocks start to shade the lawns, as the B2/B3 commits intended.
   The only other case in the file is line 1277, `// 9 cm filler against the entry wall KW(6.415, 6.42, .10, 2.00);`
   (since d6585e0). It is a 5 mm panel in the fridge air gap; delete it or restore it on its own line. No new case in the
   re-check 5 diff.

5. **605 duplicate materials cost about 1000 draw calls a frame.** CONFIRMED (measured). Materials made inside loops get
   one merged mesh each: school fence bars 356 (line 2004, `M('#d9d9d6', ...)` per bar, also line 2005), block solar panels
   87 (2153), block roof pergolas 30 (2152), block balcony slabs 29 (2147, `slab = M(...)` per call), condenser grille slots
   35 (1574), mamad unit louvres 8 (1806), kids' bath ceiling trim 4 (1509). Hiding the duplicates (upper bound of merging
   them): desktop HQ `entry` 1451 to 407 calls, `view` 874 to 172; phone `entry` 460 to 141, `view` 201 to 73. Fps on this Mac
   moved little (desktop is fill bound in HQ), but on real phones WebGL calls are CPU bound. Fix: hoist each material
   (`const mFenceBar = M('#d9d9d6', .5, { metalness: .4 })` before line 2004; module-level `mBlockSlab`, `mRoofTile`,
   `mSolar` for 2147/2152/2153; one material each for 1574, 1806, 1509).

6. **Path tracing (`__app.setPT(true)`) fails at once.** CONFIRMED, also on 6b679fd (not a re-check 5 regression). The
   console shows `TypeError: Cannot read properties of undefined (reading 'r') at MaterialsTexture.updateFrom`, and `ptOn`
   stays false. Cause: `setPT` hides the mirrors (`ptScene(true)`), then waits 30 ms (line 2741) with `ptOn` still false;
   `frame()` line 2807 re-shows every Reflector within 6 m, and `pt.setScene` then collects the Reflector's ShaderMaterial,
   which has no `.color`. Fix, line 2742:
   `mirrors.forEach(r => r.visible = false); pt.setScene(scene, camera); ptOn = true;`

7. **Saved ceramics with an old key are lost, and a corrupt `ali-cer` blocks the page.** CONFIRMED. Re-check 5 changed the
   finish of two items, so their keys changed: `c3060c|מילניום 7.5/15|g` is now `|u`, `k1030|וראנו טאופה|g` is now `|u`.
   An old key (or any unknown key) falls back to `cur` (the old 120x120 floor, the stone splash), not to the space default, and
   `cerSave` then overwrites the stored choice. Page-number changes are harmless (the page is not in the key). With
   `localStorage['ali-cer'] = 'null'` the module throws `Cannot read properties of null (reading 'floor')` and the page stays
   on the loading screen. Fix, lines 3123 and 3158:
   ```js
   const CER_MIG = { 'c3060c|מילניום 7.5/15|g': 'c3060c|מילניום 7.5/15|u', 'k1030|וראנו טאופה|g': 'k1030|וראנו טאופה|u' };
   const cerList = ..., cerSaved = (() => { try { const o = JSON.parse(localStorage.getItem('ali-cer') || '{}'); return o && typeof o === 'object' ? o : {}; } catch (e) { return {}; } })();
   // 3158
   CER_SPACES.forEach(sp => { let k = cerSaved[sp.id]; k = CER_MIG[k] || k; cerSet(sp.id, k === 'cur' || (typeof k === 'string' && cerItem(k)) ? k : sp.def); });
   ```

8. **Two items did not follow the 2.70 ceiling.** CONFIRMED.
   - Closet LED, line 1415: `B(7.02, 8.3, -4.395, -4.375, 2.42, 2.45, mat.led)` sticks 2 cm out of the wardrobe fronts, now 25 cm
     under the top (the wardrobes run to H). It reads as a glowing bar across the doors (`closet.jpg`). Fix: `H - .03, H` (a
     cove at the top), or remove it.
   - Refrigerant pipes in the laundry niche, lines 1575 and 1579, end at `2.35` in mid-air, now 35 cm under the ceiling.
     Fix: `y2 = H` on all four cylinders, so they run into the ceiling.
   Everything else near the ceiling follows `H` (fans at 2.45, mamad sleeves, corridor drop 2.35, kids' bath ceiling 2.20,
   curtain tracks, wardrobes, wall cabinets, light fittings).

9. **Panel text still says the skirting is white and 8 cm.** CONFIRMED. Line 174: "פאנל לבן 8 ס״מ". The model now uses 7 cm
   cut from the floor material (line 950, spec 33x7 or 60x7). Fix the sentence to say 7 cm in the floor material.

10. **Master bedroom south wall: two coplanar faces.** Geometry CONFIRMED, flicker SUSPECTED (not seen in stills). The
    balcony north wall (line 1691, `B(BX1, BN + .002, BZN - .015, ...)`, stucco) starts at z -0.145, the same plane as the
    room face of the TV wall `W(4.15, 9.30, -0.145, 0)`. The overlap x 7.70..9.30 is exposed in the bedroom at x 8.55..8.91
    (between the slat wall and the window). Fix: start the stucco at `BZN - .013` (2 mm behind the face) or at z 0.

11. **Kitchen window C sill top is coplanar with the wall top.** CONFIRMED by geometry (known open pattern from the fourth
    check, repeated in the new line 1057): sill `1.17..1.20` and the facade segment `[7.75, 8.45, 0, 1.20]` share y 1.20 over
    x 7.28..7.31. Fix: sill `1.17, 1.202`.

12. **Dead or hidden geometry.** CONFIRMED by the containment scan.
    - Tami4 and capsule-machine cups sit inside the machine bodies (lines 1294-1295, after the `withShift(.12, 0)`), so no
      cup shows (`tami4.jpg`). Fix: cup x `4.11` and the drip tray `B(3.94, 4.14, ...)`, or drop the cups.
    - 12 "warm LED seams in the fluting" (line 1133) are buried inside fluting slats (z `CD - .014..CD - .006` inside slats at
      `CD - .02..CD`). Fix: z `CD..CD + .002`, or only place them in slat gaps.
    - The basin drains (line 1452) are inside the cabinets until finding 1 is fixed.
    - Ali Mohar road strips (asphalt, centre line, kerbs) run on north through the T-junction block `[-5, 34, -118, -102]`
      and the cross street; two dashes sit inside the block and the dashes at z -98..-95 are coplanar with the cross-street
      asphalt top (y GY + .035). Fix: stop the line 1936 loop and the road boxes at z -100.

13. **Exterior coplanar faces (z-fighting).** CONFIRMED by geometry; far from the preset views, so low.
    - Stair core `building(-3.55, 1.19, 5.77, 9.11, ...)` (line 1876) and the floor-1/ground stucco boxes share the face
      z 9.11 over x -3.55..1.19 (about 29 m², exposed west of the bar and under its open ground floor). Fix: core `z2 = 9.12`.
    - Ali Mohar sidewalk `B(14.3, 16.9, -160, 160, GY, GY + .15)` overlaps both Tirtsa Atar sidewalks at the same top
      (z 48..50.5 and 60.5..62.5); its kerb at line 1942 shares the face x 16.9 with it for 320 m. Fix: sidewalk z range
      `-160, 48`, and kerb `B(16.75, 16.92, ...)`.

14. **Small floating or misplaced items.** CONFIRMED by the isolation scan.
    - The socket plate under the master TV (line 1395, inside `withShift(.20, .10)`) floats 1 cm off the bathroom wall
      (z -3.095 vs the wall face -3.105). Fix: `plate('s', -3.205, ...)` inside the shift, or move it out of the block.
    - Master window curtain track (line 1408) hangs 2 cm under the ceiling with no hangers. Fix: `H - .02, H`.
    - Room 2 TV point and socket at h 1.80 (line 1801, x 1.85, z -2.86) sit behind the full-height bookcase (lines
      1620-1622). A design conflict: move the bookcase or note it.
    - Knob balls (line 1560) and fridge handles (line 1275) float 4 mm off their stems and door. Cosmetic.

15. **Floor-1 balcony slab is tile all round.** CONFIRMED (shot `source/out/qa6_code_geometry_perf/shots/street.jpg`). Line 1927 builds the whole 36 cm slab in `mTerr`,
    so its edge and underside show floor tiles. Fix: `B(BX1, BX2, BZN, BZ2, BY + y - .36, BY + y - .012, mat.stucco, OUT)` plus a
    thin `mTerr` top `BY + y - .012..BY + y`.

16. **Docs out of date.** CONFIRMED. `DESIGN.md` line 24 still gives `H = 2.60 (estimate)` and the facade top as 10 cm above
    it (now equal). `PROJECT_MEMORY.md` still lists "model keeps 2.60" under the third re-check open issues, and its perf line
    (ready 1.8 s desktop, forced fps 21 to 15) does not reproduce on this Mac for either build (see below).

## Performance and load (this Mac, Metal, GPU lock, `localhost:8000`)

| | Desktop 1440x900 HQ | Phone (Pixel 7 emulation) |
|---|---|---|
| Ready (loading hidden), cache off | 7.4 s (9.2 to 12.2 s in other runs) | 4.5 s (3.7 to 4.6 s) |
| Transferred, cache off | 11.8 MB, 109 requests | 11.3 MB, 86 requests |
| Meshes / materials / programs | 927 / 794 / 68 | 919 / 786 / 47 |
| Draw calls per frame: entry, view, master, top | 1451, 874, 625, 739 | 460, 201, 162, 374 |
| Triangles per frame: entry, master, top | 0.29 M, 0.63 M, 0.65 M | 0.13 M, 0.11 M, 0.31 M |
| Forced fps (renderOnce + rAF): entry, view | 9 to 10, 10 to 13 | 18 to 21, 37 to 47 |
| rAF fps while turning (phone) | | 40 |
| JS heap | 157 MB | 97 MB |

- A/B against 6b679fd in the same session: same calls (1443 vs 1451 at `entry`), same fps, ready no slower. Re-check 5
  added no measurable cost. The phone figure of about 40 fps in PROJECT_MEMORY holds for rAF while moving; forced
  rendering at `entry` is about 20.
- Load profile (desktop, to ready): shader compile 2.5 s (68 programs), texture uploads 1.1 s, `cerTex` 0.9 s (line about
  3002, nine spaces built at load), `meanLin` 0.56 s (line 580, forces a decode of each photo texture), GPU read-backs
  0.58 s (contact shadows and ground mask), `boxBlur` 0.3 s. Options: build ceramic textures only for spaces whose choice is
  not `cur`/default until the panel opens, compute `meanLin` from a pre-baked mean in the asset manifest, `renderer.compileAsync`
  before the first frame.
- Biggest downloads: `three.module.js` 1.2 MB (gzip on Pages), `potted_plant_01.glb` 1.2 MB and `_02` 0.7 MB for two balcony
  plants, three tree atlases 0.4 to 0.6 MB each, ground normal maps 0.45 to 0.55 MB each.
- Console: no warnings on desktop or phone except the path tracer error (finding 6).

## Checked and fine

- No statement hidden after `//` in the re-check 5 diff; the comment-swallowed balcony slab is restored (line 1693).
- All 33 views, day and eve, load with no page error; dims, ceiling, doors, curtains and HQ toggles on and off with no error.
- No zero-size or NaN boxes; nothing inside the interior footprint above the ceiling plane except wall caps.
- sunBoxes moved with the far side (+2.2 m: cars, van, school, fence, sails, empty lot, retaining wall) all match their
  geometry; the floor-1 balcony box (base 2.9, top 6.6) matches the two slabs. Only the blocks are missing (finding 4).
- New window lists for floors 1 and 0 have correct outward signs on all four faces; the lot wall arc orientation is right
  (only its height is wrong).
- Island socket sits on the drawer-block face (x 5.428..5.44); balcony socket on the pier between doors A and B; deck mixers
  sit on the bowl axes with the spout over the bowl.
- Skirting now uses `mat.tile` (living, mamad) and `mat.planks` (bedrooms), so it follows the ceramic picker; grout lines fall
  above the 7 cm skirting for the default grids.
- Glossy floor handling (`envDay .45`, `bumpScale .15`) stays consistent with `setMode`, which reads the same `userData.envDay`.
- Old keys with a valid name (e.g. `f60|דקו סטון אפור|m`) and non-string values do not crash.
