# QA8: details that do not meet (NAME = details)

Scope: railings, walls, upstands, bars, fences and every object that should rest on, hang from or fix into something,
inside and outside, including the floor-1 balcony, floors 3-6 and the neighbours' balconies.

Line numbers: `source/salon.html` as of commit 4ec4d9d plus the working tree (3449 lines). Search the quoted code if they
drift. Images: `audit/qa8/details_img/`.

Method. A Playwright route hook (no file edited) recorded the world box and the creating line of all 5976 meshes just
before the merge, plus the live groups (doors, curtains, fixtures). Three passes over the boxes: (1) connected groups
that touch nothing (4 mm tolerance), (2) open ends of every long thin box (railings, rails, bars, beams, kerbs, strips),
(3) wall ends that meet nothing. Every hit was read in the code and the visible ones were shot with `cams6.mjs`.
Scripts to re-run: `source/out/qa8_details/` (`capture.mjs`, `comp2.py`, `ends.py`, `walls.py`).

## Findings, most severe first

### 1. Balcony railing: the corners still do not close (all six balconies). CONFIRMED
The owner's gap is now bridged by a return (upstand and rails along x 10.07..10.30), but:
- The east top and bottom rails still run the full z BZN..BZ2 (-0.13..8.71). The north rail sits at z -0.07..-0.01 and
  the new south return at z 8.59..8.65, so the east rails stick out 6 cm past both corners as a T end. Visible from the
  seating, beside the egg chair and from the street. Images `01_balcony_south_end_top.jpg`, `01b_east_rail_T_end.jpg`,
  `01c_ne_corner_overshoot_floor3.jpg`.
- The return rails start at x 10.07 but at z 8.59..8.65, 6 to 12 cm in front of the fin, which only begins at z 8.71. The
  rail ends hang in the air next to the fin corner (the open-end pass flags both ends, line 1879 and 2139). The upstand
  return touches the fin only along one vertical edge.

Cause: line 1874 (floor 2) and 2137 (floors 1, 3-6): `B(BX2 - .12, BX2 - .06, BZN, BZ2, 1.05, 1.09 ...); B(BX2 - .11, BX2 - .07, BZN, BZ2, .45, .49 ...)`.

Fix (line 1874, and the same with `+ y` and `OUT` on line 2137):
```js
B(BX2 - .12, BX2 - .06, BZN + .06, BZ2 - .06, 1.05, 1.09, mat.blackMetal); B(BX2 - .11, BX2 - .07, BZN + .07, BZ2 - .07, .45, .49, mat.blackMetal);
```
and after line 1879 (and after 2139 with `+ y`, `OUT`) an end post on the fin corner that the return rails fix into:
```js
B(BS - .005, BS + .02, BZ2 - .125, BZ2 + .005, .45, 1.09, mat.blackMetal);   // end post with wall plate at the fin corner
```

### 2. South fin: open slot at every upper slab, and a cut-off bottom on floor 1 (new street views). CONFIRMED
The south side wall of the balcony stack (x 7.70..10.07, z 8.71..9.20) is drawn per floor from `BY + y` to `y + 2.90`, but
the balcony slabs stop at z BZ2 (8.71), so nothing fills the fin at slab level. From the street there is a 31 cm deep
hole in the fin end at floor 3 (our soffit top 2.95 to the floor-3 wall at 3.26) and a 36 cm one at floors 4-6. On floor 1
the fin starts at -3.34 while its slab soffit is at -3.70, so the fin ends in a notch over the garden. Images
`03_south_fin_slot_floor3.jpg`, `03b_south_fin_bottom_floor1.jpg`.

Cause: line 2131 `B(BX1, BS, BZ2, 9.20, BY + y, y + 2.90, mStuccoOut, OUT)`.

Fix (line 2131): start the fin at the slab soffit:
```js
B(BX1, BS, BZ2, 9.20, BY + y - .36, y + 2.90, mStuccoOut, OUT);
```

### 3. Floor 2 balcony: a see-through slit between slab and upstand, all along the front. CONFIRMED
The slab top is at BY - .012 (-0.052), the deck is a one-sided plane at BY (-0.04), and the upstands and side walls start
at BY. On every outer face there is a 12 mm open slit. It reads as a dark line along the whole balcony front from the
street (also visible in the `street` view). Floor 1 and floors 3-6 have a tile layer and no slit. Image
`02_balcony_slab_slit.jpg`.

Cause: lines 1870, 1871, 1878 start the walls and upstands at `BY`.

Fix: start them inside the slab:
```js
// 1870
B(BX1, BN + .002, BZN - .013, BZ1, BY - .012, 2.70, mStuccoOut); B(BX1, BS, BZ2, 9.20, BY - .012, 2.70, mStuccoOut);
// 1871
B(BX2 - .15, BX2, BZN, BZ2, BY - .012, .45, mStuccoOut); B(BN, BX2 - .15, BZN, BZN + .15, BY - .012, .45, mStuccoOut);
// 1878, first box
B(BS, BX2 - .15, BZ2 - .15, BZ2, BY - .012, .45, mStuccoOut);
```

### 4. A 1 cm slit runs round the building at the foot of floor 2. CONFIRMED
Floor 1's boxes end at `GY + 6.59` (-0.01, kept below the porcelain floor plane at 0) and floor 2's new plaster skin starts
at 0. From the street there is a thin dark line round the west, north and east faces and at the foot of the living
facade on the balcony. Image `04_floor2_base_slit.jpg`.

Cause: line 2092, `skin` draws from 0.

Fix (line 2092): take the skin 11 mm down, except under openings that sit on the floor:
```js
let c = a1; holes.slice().sort((h, k) => h[0] - k[0]).forEach(([h1, h2, sl, hd]) => { P(c, h1, -.011, 2.71); P(h1, h2, sl ? -.011 : 0, sl); P(h1, h2, hd, 2.71); c = h2; }); P(c, a2, -.011, 2.71); };
```
(Raising floor 1 to 0 instead would z-fight with the floor plane.)

### 5. Office chairs: backrest floats, base floats, and the mamad chair faces away from the desk. CONFIRMED
- `officeChair()` (rooms 1 and 2): the backrest is a slab at y .60..1.04 with no spine; the seat top is .51, so it hangs 9 cm
  above the seat. The five legs are at y .06..09, 1 cm over the casters (0..05) and 1 cm under the column (.10). Image
  `06_office_chair_back_floats.jpg`.
- Mamad ergonomic chair: legs .07..10 over casters 0..06; the back spine starts at .55 and at z -.29..-.25, behind the
  seat edge (-.24), so back, spine and headrest float as one piece.
- The mamad chair is turned `Math.PI`: its back is toward the desk and the monitors (z 1.86 side), so the sitter faces the
  bed. Image `06b_mamad_chair_faces_away.jpg`.

Fix:
```js
// 903 (legs touch casters and column)
const l = lb(P, -.14, .14, -.015, .015, .05, .10, mat.blackMetal); l.position.set(Math.cos(a) * .14, .075, -Math.sin(a) * .14);
// after 901: spine from seat to back
lb(P, -.03, .03, -.26, -.20, .46, .66, mat.blackMetal);
// 1847: face the desk
g.rotation.y = 0;
// 1848: legs .06..10
l = lb(P, -.17, .17, -.02, .02, .06, .10, base); l.position.set(Math.cos(a) * .17, .08, -Math.sin(a) * .17);
// 1851: spine from the seat
lb(P, -.02, .02, -.27, -.23, .44, 1.20, base);
```

### 6. Master shower head hangs 4 cm under its arm (default fixture). CONFIRMED
`fixHead()` default "אומגה": the flat arm is at y 2.09..2.11, the head disc at 2.04..2.05, nothing between. The "נפולי" tube
also ends at y 2.08 over a head at 2.055. Image `07_shower_head_below_arm.jpg`.

Fix: line 764 add the drop `C(4.80, -4.585, 2.05, 2.09, .008, m, { seg: 8 });`. Line 762: last point `V(4.80, 2.055)`.

### 7. Laundry niche: water heater floats, pipes end in the air, upper condenser not on its stand. CONFIRMED
- Water heater (line 1760, inside `withShift(.22, -.45)`): tank at x 3.77..4.31, z -4.96..-4.42, y 1.0..2.25; the facade
  face is z -5.11 (15 cm away), the east wall x 4.37 (6 cm). No bracket. Its two pipes stop at y .70. Image
  `09_water_heater_floats.jpg`.
- Upper condenser 84x40 (line 1752) sits at y 1.05 between the two stand rails (line 1754, z -4.66..-4.62 and -4.13..-4.09),
  not on them: the unit spans z -4.55..-4.15 (pre-shift). It is held up by nothing.
- Lower condenser (line 1746) starts at y .03 with no feet.

Fix (all inside the shift block, pre-shift coordinates):
```js
// after 1760: two straps to the facade, pipes to the floor
[1.35, 1.95].forEach(y => B(3.78, 3.86, -4.67, -4.50, y, y + .04, mat.steel));
C(3.82, -4.24, .003, 1.0, .015, mat.steel, { seg: 8 }); C(3.92, -4.24, .003, 1.0, .015, mat.steel, { seg: 8 });   // replace the .7..1.0 pipes
// after 1754: cross bars under the unit
[2.20, 2.96].forEach(x => B(x - .02, x + .02, -4.66, -4.09, 1.01, 1.05, mat.steel));
// after 1746: rubber feet
[[2.12, -4.56], [3.04, -4.56], [2.12, -4.19], [3.04, -4.19]].forEach(([x, z]) => B(x - .03, x + .03, z - .03, z + .03, 0, .03, mat.black));
```

### 8. Picture light over the entry prints floats 4 cm off the wall. CONFIRMED
Line 1169: the bar is at z 5.40..5.46; the wall face is z 5.50. No arms. Image `05_picture_light_off_wall.jpg`.

Fix (after line 1169): two arms, `[3.0, 4.08].forEach(x => B(x - .01, x + .01, 5.46, 5.50, 2.025, 2.045, mat.blackMetal, { cast: false }));`

### 9. Curtains in rooms 1 and 2 hang from nothing. CONFIRMED
The curtain planes stop at H - .03 (2.67) and there is no track or rod in rooms 1 and 2 (the master and the living room have
one). Image `12_room1_curtain_no_rod.jpg`.

Fix: after line 1786 (room 1) `B(-3.84, -3.79, -2.95, -1.77, H - .03, H, mat.frame, { cast: false });   // ceiling track`.
After line 1795, inside room 2's shift: `B(.17, 1.14, -4.735, -4.685, H - .03, H, mat.frame, { cast: false });`.

### 10. Concealed mixers: the lever handle is detached from its spindle (both baths, default taps). CONFIRMED
`fixWallMixer()` line 756: the arm ends at y - .012 (3-way) or y - .037 (4-way), the handle starts at y - .02 or y - .045:
8 mm gap in the master shower, 24 mm on the bath tap. Image `08_bath_tap_lever_gap.jpg`.

Fix (line 756, second `P`): `P(a - .006, a + .006, .05, .06, y - .1, y - .012 - (ty === '4' ? .025 : 0));`

### 11. Decor balls float in the lit niches. CONFIRMED
TV niche: `Sph(3.85, 1.27, .20, .05)` bottom 1.22 over a shelf at 1.195 (2.5 cm). Storage niche: `Sph(.30, NY1 + .245, ...)`
bottom 1.24 over the book stack top 1.18 (6 cm). Images `11b_ball_tv_niche.jpg`, `11_ball_storage_niche.jpg`.

Fix: line 1318 `Sph(3.85, 1.245, .20, .05, ...)`; line 1405 `Sph(.30, NY1 + .185, a + .45, .055, ...)`.

### 12. Books, shelves and a nightstand that do not touch. CONFIRMED (measured; room 2 books visible)
- Room 2 bookcase: books at y .82 on a top at .80 (line 1802). Mamad bookcase: books at .87 on a top at .85 (line 1816). Image
  `13_room2_books_float.jpg`.
- Room 1 shelves (lines 1777-1778): x -3.88 after the shift, wall face -3.89: 1 cm gap, no brackets.
- Room 2 shelf (line 1796): 1 cm off the north wall and 1 cm off the room 1 wall.
- Room 2 nightstand (line 1791, wall-hung): back at z -5.00, wall -5.01.

Fix: 1802 `books({ g: root }, 1.54, .80, ...)`; 1816 `books({ g: root }, -.95, .85, ...)`; 1777 and 1778 `B(-3.98, -3.69, ...)`;
1796 `B(-1.12, -.31, -4.81, -4.58, 1.45, 1.47, mat.oak)`; 1791 `place(-.13, .12, -4.81, -4.43, 's')`.

### 13. Balcony garden tap: the spout floats 3 cm in front of its plate. CONFIRMED
Line 2030: plate at z 8.67..8.71, spout cylinder at z 8.618..8.642, nothing between. Image `10_garden_tap_spout.jpg`.

Fix (after it): `B(8.49, 8.51, BZ2 - .09, BZ2 - .04, .585, .615, mat.steel, { round: .005 });   // tap body`

### 14. Neighbours' balconies (building A): sides open above the 45 cm upstand. CONFIRMED
Line 2400 puts glass only on the east edge. The north side of the first balcony and both sides of the second open onto
x 8.27..10.2 with only the upstand. Seen from our balcony and the street. Image `14_neighbour_balcony_open_side.jpg`.

Fix (after line 2400):
```js
B(7.70, 10.14, a + .055, a + .095, y + .45, y + 1.05, mGlassRailN, OUT); B(7.70, 10.14, b - .095, b - .055, y + .45, y + 1.05, mGlassRailN, OUT);
```

### 15. Roof parapet stops in the air. CONFIRMED (bird and street views)
Line 2102: parapets on the north, west and the master wing east edge only; the east run ends at z -0.13 with an open end
and the east edge over the balcony stack and the whole south edge have none. Image `15_roof_parapet_end.jpg`. Parapet
height is an estimate.

Fix (add to the list on line 2102): `[9.17, 10.45, -.28, -.13], [10.30, 10.45, -.13, 9.20], [7.70, 10.45, 9.05, 9.20], [-4.30, 7.70, 8.96, 9.11]`.

### 16. Master bedroom: TV socket plate stands 1 cm off the wall. CONFIRMED
Lines 1572-1573 are inside `withShift(.20, .10)`: written at z -3.195, they land at -3.095, the wall face is -3.105. The TV
also hangs 1 cm off (acceptable for a mount); the plate's side shows. Image `16_master_tv_plate_off_wall.jpg`.

Fix: `B(4.93, 6.09, -3.205, -3.17, ...)` and `plate('s', -3.205, 5.50, 1.0, .14, .08)`.

### 17. Kids' bath: the cornice is a free fin above the mirror cabinet. CONFIRMED
Line 1733 `cornice(..., 1.89)` on a cabinet that ends at 1.85 (line 1728): the top 4 cm stand 14 cm in front of the wall
with open ends. Image `17_kids_cornice_fin.jpg`.

Fix: line 1728 `B(2.01, 2.15, -2.535, -1.695, 1.15, 1.89, paint, { round: .004 })`.

### 18. Dryer floats 2 cm over the washer. CONFIRMED
Line 1659: washer to .85, dryer from .87, no stacking kit; the dryer touches nothing. Image `20_dryer_gap.jpg`.

Fix (after it, inside the shift): `B(3.645, 4.235, -3.61, -3.01, .85, .87, M('#d9d8d3', .5));   // stacking kit`

### 19. Wall-hung WCs and the master flush plate stand off the cistern ledge. CONFIRMED (measured)
`fixWC()` starts every bowl at local z -.27 in a frame whose wall is at -.275 (5 mm). The master frame is also placed at z
-4.79 while the ledge face is -4.80, so the master bowl is 1.5 cm off; the kids' bowl 5 mm. The master flush plate
(line 1623, `fixFlush('z', -4.79, ...)`) is 1 cm off.

Fix: in `fixWC` (lines 718-724) replace `-.27` with `-.276`; line 1622 `place(5.88, 6.24, -4.80, -4.25, 's')`; line 1623
`fixFlush('z', -4.80, 1, ...)`.

### 20. Kitchen zebra blind cassette stops short of the reveal. CONFIRMED
Line 1272: z 7.755..8.445 in a 7.75..8.45 reveal, top 5 mm under the head; dark slots at both ends. Image
`19_zebra_cassette_gap.jpg`.

Fix: `B(FX + .02, FX + .115, z1 - .017, z2 + .017, top, HEAD + .002, mat.whitePlate, { round: .01 })`.

### 21. Outside: gate, fence ends and pergola without their supports. CONFIRMED
- Car gate (line 2269): 1.6 m gate between 0.5 m lot walls, no posts; top rail overhangs the end pickets. Image
  `18_car_gate_no_posts.jpg`. Fix: `[-21.92, -17.74].forEach(x => B(x, x + .06, 47.44, 47.56, GY, GY + 1.7, mFence, OUT));`
- Private garden fences (line 2279): the rail runs 5 cm past the last picket and ends over the low wall. Fix inside the
  forEach: `B(x - .03, x + .03, -11.55, -11.49, GY, GY + 1.15, mFence, OUT);`
- Pergola (line 2282): slats run from the north beam to z -5.40, 1 cm short of the facade, with no south beam or ledger.
  Image `21_pergola_no_ledger.jpg`. Fix: `B(3.98, 9.06, -5.51, -5.39, GY + 2.68, GY + 2.8, mFence, OUT);`

### 22. Mamad curved monitor is not attached to its pole. CONFIRMED (measured)
Line 1838: the pole is at z 2.62..2.66 up to the screen centre, the screen back at z 2.585: 3.5 cm gap, no arm.

Fix (after it): `B(cx - .04, cx + .04, cz + .02, cz + .065, cy - .06, cy + .02, frameM);   // VESA arm`

### 23. Small gaps, one line each (CONFIRMED by measurement, low visibility)
- Window handles float 2.5 cm in front of the glass beside the frame members (all `windowX`/`windowZ` windows). Lines 1022,
  1034: use `panes > 1 ? mid : x2 - .025` and `panes > 1 ? z1 + (z2 - z1) / panes : z2 - .025` so the rose sits on a stile.
- Sliding-sash pull (line 1021) 5 mm off the mullion: `B(mid + .01, mid + .025, ...)`. Living slider pulls (line 1236) 2 to 3 cm
  off any frame: `const zp = panes > 1 ? z1 + (z2 - z1) / panes - .013 : z2 - .037`.
- All art frames stand 12 mm off the wall (`art()` line 936, `o = .012`); the two storage-wall prints 18 mm (lines 1414-1415
  pass `.006` and `TW - .006` for walls at 0 and 2.775). Fix `o = .003`, `art('s', 0, ...)`, `art('n', 2.775, ...)`.
- Mamad window blind box (line 1859) 1 cm in front of the wall with nothing at its ends: `B(-3.80, -3.75, .48, 1.48, 1.72, 2.0, ...)`.
- Shaker knob stems start 7 mm off recessed panels (line 1677): `bx(-.001, .02, ...)`. Mirror cabinet knobs 8 mm off the doors
  (line 1731): x 2.165.
- Master towel hangs 1.7 cm in front of the ladder rungs (line 1644): z -3.298..-3.278.
- Fridge handles 4 mm off the door (line 1457): start at x 4.29.
- Master window bars (line 1585): posts sit inside the opening width, 1 cm proud of the skin, so they bear on nothing; widen
  to z -2.21..-1.23 (posts -2.21..-2.17 and -1.27..-1.23) and take them down to y .11 so they overlap the plaster.
- Floors 1, 3-6: north side wall ends at BN - .002, 2 mm short of the north rail (line 2131): use BN + .002 as on floor 2.
- Bath filler disc 6 mm off the tub end (line 1705): z -1.497.
- Solar heaters on the school (line 2201) float 12 cm over the roof, PV panels on the school and on our new roof (line 2405)
  float 3 to 7 cm at their low edge; no stands. Far away, low.
- Distant residential blocks: balcony slabs on north and south faces have no railing at all, west faces glass on the front
  only (`block()`). Far, low.

## Checked and fine
- Owner defect 1: the south end is now closed by an upstand and rail return (remaining issues in finding 1). Owner defect 2:
  the master bars now have a frame, posts and a bottom rail (only the overlap note in 23).
- Egg chair: ring base, stand tube, chain into the apex. Balcony sofa and table legs, cushions, fan, ceiling lights, wall
  lights, socket, gas valve, drains. Potted plants on the deck.
- Pendants and cables: wave pendant (cables into its canopy), island frames, bedside globes, corridor downlights, coffee-table
  frames, all fans.
- Wall-hung furniture: entry commode, master and kids' vanities and mirror cabinets, room 1 nightstand, master nightstands on
  the slat panel, AC split, electrical panel, heaters, every socket and switch plate except the master TV one.
- Shower glass, tub screen, towel ladders, towel hooks, paper holders, niches, rail and mixer roses on the walls.
- Living: sofa legs, coffee table (swivel stack, 5-10 mm gaps by design), media wall (the halo slab floats 3 cm off its backing
  as the design comment says), curtain track in its pocket, kitchen hood, handles, island pulls.
- Laundry louvres run wall to wall; clothesline brackets fix into the louvre screen.
- Walls: every wall end meets a wall or a frame. One hidden 16 x 3 cm shaft at x 6.85..7.01, z -5.01..-4.98 behind the closet
  wardrobe has no visual effect.
- Floor-1 balcony side walls meet our slab; floors 3-6 slabs carry a tile layer (no slit); shutter rails sit in the reveals.
- Lot walls, kerbs, sidewalks, bench (on the sidewalk), street lights, signs, school fence and empty-lot fence posts.
