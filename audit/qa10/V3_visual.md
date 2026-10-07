# QA10 / V3: fresh-eyes visual sweep (edges, endings, lighting)

Model: commit `6810263`, built site on http://127.0.0.1:8791/. Report only, nothing in the repo was edited. Line numbers
refer to `source/salon.html` at that commit.

## Method

- 66 named-view shots (33 views, day and eve).
- 36 low corner close-ups: every corner of rooms 1, 2, the mamad, master, closet, master bath, family bath, living and
  kitchen, with the camera at 55 cm.
- 56 door shots: both faces of every interior door, open and closed, plus the foot of each casing.
- About 85 targeted shots: splash ends, window reveals and sills, storage and media wall ends, passage returns, corridor
  bases, bulkheads, the kids' bath ceiling, the entrance, the balcony bases, and top-mode close-ups of every zone.
- 15 eve and 8 day room-wide shots to look for lighting artefacts.
- Ray scans from `audit/qa9/F_scan`: `bases`, `floors`, `wet`, `ceilings`, `splash`. Each candidate was checked by eye.
  Most `bases` hits sit behind the storage wall, the wardrobes and the kitchen cabinets, so they are not visible.

I did not re-raise the owner questions in `audit/qa9/README.md`.

## Findings (ranked)

### 1. HIGH: the master bath's north wall (east of the shower niche), the closet's north wall and the NE corner block are missing

- **What you see.** In the `top`, `bird2` and every top-mode view, the 41 cm north facade has no wall and no dark cap from
  x 6.015 to 9.30:
  - over the master bath window, the WC ledge and the corner beside it;
  - along the whole closet;
  - at the 39x38 cm corner block at the NE corner.
- **What fills the gap.** Only the 1 cm exterior plaster skin stands there. From above you look straight past the wardrobe
  tops and the master bath window frame down to the floor-1 balcony railing.
- **Inside the rooms.** The room faces are still there (the bath tile skins, the wardrobes), so the gap does not show
  from eye height. It is very visible in the dollhouse views an architect will open first.
- **Evidence:** `V3_img/01_ne_wall_missing_top.jpg`, `01b_top_view_ne_crop.jpg` (the `top` view), `01c_top_baths.jpg`.
- **Root cause:** line 1075. Commit `40e8d72` (QA9 bath niches) put the comment
  `// shower niche cut 9 cm into the wall` in the middle of the line, so every call after it is commented out:
  `W(6.015, 6.615, -5.39, -4.98, 0, 1.25); W(6.015, 6.615, -5.39, -4.98, 2.35); W(6.615, 6.85, -5.39, -4.98); W(6.85, 7.01, -5.39, -5.01); W(7.01, 8.91, -5.39, -4.995); W(8.91, 9.30, -5.39, -5.01);`
- **Why the checks missed it.** `roomdims.py` reads the `W(` calls with a regex and does not skip comments, so the dead
  calls still count and it reports +0 (the closet z 485/175 line looks like the known probe artifact).
- **Fix:** end line 1075 after the comment and put the six calls back on their own line, unchanged (the same values as
  before `40e8d72`):
  ```js
  ... W(4.91, 5.41, -5.39, -5.07, 1.03, 1.42);   // shower niche cut 9 cm into the wall
  W(6.015, 6.615, -5.39, -4.98, 0, 1.25); W(6.015, 6.615, -5.39, -4.98, 2.35); W(6.615, 6.85, -5.39, -4.98); W(6.85, 7.01, -5.39, -5.01); W(7.01, 8.91, -5.39, -4.995); W(8.91, 9.30, -5.39, -5.01);
  ```
- **After the fix:** recheck `top`, `bird2` and the master bath window. Make `roomdims.py` strip `//` comments before
  parsing (for example `re.sub(r'//[^\n]*', '', seg)`), so a commented-out wall shows up as a dimension error.

### 2. MEDIUM: the kitchen stone splash stops at the window C jamb and leaves painted wall over the counter

- **Where.** The south counter runs into the east facade (x 7.28) under window C (z 7.75..8.45, sill 1.20). The return
  splash covers only z 8.45..8.775.
- **What you see.** Over the counter, z 8.19..8.45 and y 0.92..1.18, a patch about 26 x 26 cm of the grey facade paint
  sits between the worktop and the window sill, with the cut edge of the splash beside it. It is visible from
  `kitchen3`, `kitchen` and `isle2`.
- **Why it matters.** A wet zone next to the hob landing is left unfinished. The comment
  "(stone over the base units except the window)" explains the code but not the result.
- **Evidence:** `02_splash_missing_under_window_c.jpg`, `02b_..._close.jpg`, `02c_kitchen3_view.jpg`.
- **Root cause:** line 1562, `B(FX - .015, FX, 8.45, 8.775, .92, t, ...)`.
- **Fix:** add a piece under the sill in the same slot (so the 50 cm option keeps it):
  `B(FX - .015, FX, 8.19, 8.45, .92, 1.175, mat.splash, { cast: false });`. The sill underside is at 1.175 (the splash
  scan sees the `sill` from 1.175 to 1.205). The window reveal then needs nothing more, because the interior sill already
  covers the top.

### 3. MEDIUM-LOW (eve): a hard horizontal light band in the kids' bath

- **What you see.** In the evening the lamp light makes a bright, sharp-edged streak at about 1.65 m. In the `bath` view
  it falls on the open door leaf beside the camera; the walls and cabinet sides show a light/dark line at the same
  height (`ev_fb_walls`).
- **Why it looks wrong.** It reads as a light source hanging in mid-room, not a ceiling downlight.
- **Evidence:** `03_kids_bath_light_band_eve.jpg`, `03b_..._crop.jpg`.
- **Root cause:** line 2744. The kids' bath warm light is `[3.2, -2.6, 1.2, BC - .55]`: y 1.65, 55 cm under the lowered
  ceiling (BC 2.20) and about 45 cm from the open leaf. `WARM_DOWN` is 1 (a downward lobe), so anything level with or
  above the light gets 8% and anything below gets full light, which gives the hard edge.
- **Fix:** put the light just under the real downlight. That downlight is the `spot` at (3.01, -3.10), with ceiling BC:
  `[3.01, -3.10, 1.0, BC - .15]`, at y 2.05. The downward lobe keeps the ceiling from blowing out, which was the reason
  for the 0.55 offset. Re-shoot `bath` and `bath2` in eve.

### 4. MEDIUM-LOW: no skirting anywhere on the balcony

- **What you see.** The deck meets the facade piers (x 7.70), the north wall (z 0.34), the south fin (z 8.71) and the
  parapet upstand (x 10.30) with no skirting at all. Inside, every dry room now has the 7 cm skirting.
- **Spec.** d08 says skirting is "from the floor material" except at clad walls and facades. Whether the balcony
  plaster walls count as "facades" is a judgement call, but a skirting in the deck material on the balcony walls and the
  upstand is the usual finish and reads as finished.
- **Evidence:** `04_balcony_no_skirting_n.jpg`, `04b_..._s.jpg`, `04c_balcony_parapet_base.jpg`. In the `bases` scan,
  all the balcony runs hit bare `anon#ecebe6` plaster.
- **Root cause:** `skirtRoom` (lines 1162-1176) is called only for the interior rooms.
- **Fix (estimate, not on a plan):**
  - after line 1915, call
    `skirtRoom(BX1, BX2 - .15, BZ1, BZ2, mat.deck, BY)` and `skirtRoom(BN, BX2 - .15, BZN + .15, BZ1, mat.deck, BY)`;
  - first add the balcony faces to `wallBoxes`: the piers are already there; add the north wall
    `[BX1, BN, BZN - .013, BZ1]`, the south fin `[BX1, BS, BZ2, 9.20]` and the upstands
    `[BX2 - .15, BX2, BZN, BZ2]`, `[BS, BX2 - .15, BZ2 - .15, BZ2]`;
  - skip the two sliding-door thresholds (z .79..3.49 and 4.29..6.99 on x 7.70) and window C.

  Or leave it bare and list it among the owner questions.

### 5. LOW: the closet hamper front sits 2.5 cm proud of the wardrobe door, in a contrasting finish

- **What.** The "built-in pull-out laundry hamper" is a beige `oatDark` box. It is mounted on the face of the middle
  door of the north wardrobe (x 7.455..7.865, z -4.395..-4.37, y .10..52), so the door above cannot open as a separate
  leaf. It reads as a panel stuck on the grey door (`d_closet`, `master2`).
- **Evidence:** `05_closet_hamper_overlay.jpg`.
- **Root cause:** line 1634.
- **Fix:** make it a flush drawer front in the door plane and finish:
  `B(7.447, 7.873, -4.397, -4.393, .10, .52, mat.greyFront)`, 2 mm proud like the door gaps. Keep the gap line at .525
  and the pull. It then reads as a drawer under a shorter door.

### 6. LOW: the room 2 light switch is squeezed between the wardrobe and the door casing

- **What.** The plate (x .79..87, h 1.10, room face of z -1.45) has the wardrobe side at x .78 and the casing edge at
  x .881. That leaves 1 cm on each side, which is visible in `d_r2_A_closed`.
- **Evidence:** `06_room2_switch_squeezed.jpg`.
- **Root cause:** line 1233 (`['n', -1.45, 0.83]`) and the wardrobe at line 1853 (`place(-.95, .78, ...)`).
- **Fix:** take 6 cm off the wardrobe (`place(-.95, .72, ...)`; it is a 3-door, 173 cm unit; 167 cm still gives
  56 cm doors) and centre the switch at x .80. The switch stays on the room side, by the latch.

## Checked and clean (no finding)

- **Skirting:**
  - every room corner at floor level (rooms 1 and 2, mamad, master, vestibule, closet, living, entry, kitchen);
  - both passage returns, the TV-wall step by the master door, the entry stub, the entrance frame;
  - the casing feet on both faces of all five interior doors;
  - the mamad blast-door frame and the wardrobe niche jambs.

  Examples: `07_ok_master_corners.jpg`, `07b_ok_passage_corridor_bases.jpg`, `07c_ok_room1_casing_feet.jpg`,
  `07d_ok_vestibule_media_bases.jpg`. Apart from the balcony, the remaining `bases` scan hits are all behind cabinets,
  wardrobes or the storage wall.
- **Bath walls** (`wet` scan plus shots): tile reaches floor, ceiling, corners, window reveals and both niches. The only
  bare plaster is the painted washer niche, which is by design.
- **Floors** (`floors` scan): no gaps or lower surfaces. The material changes are under the closed leaves.
- **Ceilings:** the corridor drop, the AC bulkhead and curtain pocket, the kids' bath lowered ceiling and hatch. All
  meet the walls cleanly, day and eve.
- **Kitchen splash:** the south and west runs reach both ends, the coffee bar side and the corner. The only gap is
  item 2.
- **Doors:** leaves, hinges, roses, stops and casings on both faces, open and closed. The open leaves clear the tub
  screen and the towel ladders.
- **Windows:** sills and reveals in rooms 1 and 2, the master, the mamad, both baths and window C. All have interior
  sills and tiled reveals in the baths.

## Notes for the lead

- The six `W()` calls in item 1 are exactly the pre-`40e8d72` values. Restoring them does not change any room interior,
  so `roomdims` and `clearance_audit` stay as they are.
- Capture specs used: `/tmp/v3a.json`, `/tmp/v3b.json`, `/tmp/v3c.json`, `/tmp/v3d.json`, `/tmp/v3e.json`,
  `/tmp/v3f.json`. Raw shots are in `/tmp/v3/`.
