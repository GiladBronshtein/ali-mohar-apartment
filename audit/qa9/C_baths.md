# QA9 C: family bath, master shower room, laundry niche

Report only, nothing in `source/salon.html` was changed. Model as of `6241532`, served from the built site on :8791.
Line numbers refer to `source/salon.html` at `6241532` (`git show HEAD:source/salon.html`). The working tree had uncommitted
edits by the lead while I worked, so numbers there run about +17 to +20 from the line 1140 area on. Each fix also quotes the
code text, so search for it.

How it was checked:
- About 120 GPU captures, day and eve, at eye level and in low close-ups:
  - `C_img/b1`: views and details
  - `C_img/fix`: 51 fixture options, with bounding boxes in `fix/boxes.json`
  - `C_img/b3`: the studio's recommended ceramics plus details
  - `C_img/b4`: confirmation shots
- Plan check: the construction, plumbing and electrical crops in `audit/recheck3/` (`con_fbath`, `con_mbath`, `pl_fbath_n`,
  `30_family_bath`, `32_master_bath`).
- Spec check: d08 table 4 and table 5, and d10 items 2, 3 and 5.

Capture scripts, for re-running: `/tmp/qa9_fixshots.mjs` takes a `"fix": {id: key}` field per shot, and `/tmp/qa9_fixshots2.mjs`
also takes `"cer": {spaceId: key}`. Run both through `/tmp/gpu.sh`.

Image paths below are relative to `audit/qa9/C_img/`.

## Verified OK (no action)

Plan positions:
- Family bath WC axis 44 cm from the window wall. The flush plate is centred on it, at z -3.335.
- Basin axis 72 cm from the south wall. The mirror cabinet is centred on it.
- Tub 70 cm wide.
- Tub mixer 35 cm from the east wall at h .85, filler 20 cm from the east wall, tub drain about 20 cm from the south wall.
  All three match the "35 / 15-20" marks on the construction sheet.
- Washer 35 cm from the north wall.
- Riser box in the NW corner.
- Master WC axis 60 cm from the closet wall, under the window. The flush plate is centred on the WC (x 6.25).
- Master basin axis 44 cm from the south wall. The mirror is centred on it.
- Shower drain 53 / 50 cm (plan 52 / 48).
- Shower mixer at h 1.05.
- Head arm at h 2.10, 39 cm from the north wall.
- Niche floor drain, riser and water heater centre.

Electrical and spec:
- Wet-zone distances: no socket or heater within 60 cm of the tub or shower.
  - Family socket: 1.65 m from the tub.
  - Master socket: 80 cm from the shower.
  - Heaters: 0.9 to 1.1 m from the tub or shower.
- d08: concealed cisterns, deck mixers, a 3-way concealed shower mixer with rail, no fixed head over the tub.
- d10 item 2: tiles to the ceiling or to the underside of the drop. Both baths comply.

Fixture options:
- No hard intersections in any of the 51 option shots:
  - WC: all 5 models, in both baths
  - Flush plates: 6
  - Tub: round
  - Bath tap: bar and 4-way in every body style
  - Basin taps: swan and short spout
  - Vanities: 6 family-bath and 5 master options
  - Shower tap, head, rail
- Every spec vanity clears the shower frame by 1 cm (master), the paper holder (family) and the mirror cabinets.

## Fix now (safe)

Ranked by how fast an architect would see it.

### 1. HIGH: the bathtub is only 17 cm deep inside

- **Where:** family bath tub, both tub options.
- **Evidence:**
  - `b1/f_tub.jpg`
  - `fix/tub_round.jpg`
  - `fix/tub_round_low.jpg`
  - `b1/f_tub_taps.jpg`
- **What:** the basin floor is at y .40-.41 and the rim at .58, so the tub reads as a tray. A real 160x70 acrylic tub with an
  apron has its rim at about .55-.58 and an inside depth of about .38-.42.
- **Cause:** `fixTub`, L768-776. The solid apron fill runs to .40, and the basin floor and walls start there.
- **Fix:** replace L771-775 with:

```js
  B(X1, X2, Z1, Z2, 0, .17, mat.bathWall2); ring(X1, X2, Z1, Z2, .17, .56, mat.bathWall2); ring(X1, X2, Z1, Z2, .56, .58, mat.ceramic);
  if (key === 'מעוגלת') { const l = mesh(new RoundedBoxGeometry(x2 - x1 - .004, .40, z2 - z1 - .004, 4, .08), mTubIn, root, false); l.position.set((x1 + x2) / 2, .38, (z1 + z2) / 2); }   // seen from inside only
  else { B(x1, x2, z1, z2, .17, .18, mat.ceramicIn, { cast: false }); B(x1, x1 + t, z1, z2, .18, .56, mat.ceramicIn, { cast: false }); B(x2 - t, x2, z1, z2, .18, .56, mat.ceramicIn, { cast: false });
    B(x1, x2, z1, z1 + t, .18, .56, mat.ceramicIn, { cast: false }); B(x1, x2, z2 - t, z2, .18, .56, mat.ceramicIn, { cast: false }); }
  C(4.11, -1.60, .18, .184, .022, mat.blackMetal, { seg: 20, cast: false });   // drain at the tap end (plan: about 20 from the south wall)
```

- **Side effects:**
  - The rounded basin's top stays at .58. Its top face is a back face, so it is culled from above, as now.
  - Moving the drain from z -1.58 to -1.60 also fixes the round option, where the drain sat on the 8 cm corner radius.
  - The overflow filler at y .50 is still inside the basin.
  - Update the comment on L769 to "floor at .17".

### 2. HIGH: heater 13 runs into the master bath door casing

- **Evidence:**
  - `b1/m_heater_casing.jpg`
  - `b1/v_mbath_day.jpg`
  - `b3/cer_m_necorner.jpg`
- **What:** the heater box z -4.46..-4.08 at x 6.77..6.85, h 1.90-2.10, overlaps the new 7 cm swing-side casing, which runs
  z -4.109..-4.039 at x 6.832..6.85. It also overlaps the head casing, which starts at y 2.079.
- **Cause:** L2014, first `B(...)`. The heater was sized against the old, narrower frame. The electrical sheet draws it
  z -4.49..-4.10 (see `recheck3/el_crops/32_master_bath.jpg`).
- **Fix:** in L2014, replace `B(6.77, 6.85, -4.46, -4.08, 1.90, 2.10, …` with `B(6.77, 6.85, -4.50, -4.12, 1.90, 2.10, …`. This
  leaves 1 cm clear of the casing and moves it 4 cm along the wall (scaled on the plan).

### 3. HIGH: heater 12 runs into the family bath door casing

- **Evidence:**
  - `b1/f_heater_casing.jpg`
  - `b1/f_door_closed.jpg`
- **What:** the heater runs x 2.45..2.85 on the south wall at h 1.90-2.10. The swing-side casing starts at x 2.811, and the head
  casing runs y 2.079-2.149. They overlap by about 4 cm.
- **Cause:** L2014, second `B(...)`.
- **Fix:** replace `B(2.45, 2.85, -1.475, -1.395, 1.90, 2.10, …` with `B(2.39, 2.79, -1.475, -1.395, 1.90, 2.10, …`. That leaves
  2 cm clear of the casing. The plan draws it touching the door frame, so it is schematic.

### 4. MED-HIGH: the master toilet-paper holder touches the casing

- **Evidence:**
  - `b1/m_paper.jpg`
  - `b1/m_door_closed.jpg`
- **What:** the holder runs z -4.19..-4.11. The casing edge is at -4.109, so the clearance is 1 mm.
- **Cause:** L1627.
- **Fix:** `B(6.77, 6.85, -4.28, -4.20, .70, .72, mat.blackMetal);`. That is 8 cm clear of the casing, just in front of the WC
  front edge (z -4.265) and under the moved heater.

### 5. MED: in the family bath, the towel hooks go through the towel ladder, and the ladder rails sink into the tile

- **Evidence:**
  - `b1/f_hooks_ladder.jpg`
  - `b1/f_door_closed.jpg`
- **What:**
  - The hooks at x 2.47 and 2.62 (y 1.08-1.12) sit inside the ladder (x 2.42..2.76): the rung at y 1.11 passes through them.
  - The ladder uses wall = -1.37, but the wall face is -1.395 and the tile face -1.401. So the rails (z -1.42..-1.40) sit 1 mm
    into the tile and only 2 cm proud of it.
- **Cause:** L1738 (hooks) and L1740 (ladder and towel).
- **Fix:**

```js
[2.20, 2.31, 2.42].forEach(x => { B(x - .008, x + .008, -1.41, -1.395, 1.08, 1.12, knobM); Sph(x, 1.125, -1.425, .011, knobM); });
ladder('x', 2.47, 2.79, -1.395, -1, .55, 1.25); B(2.56, 2.78, -1.475, -1.455, .78, 1.12, mat.sageFab, { cast: false });
```

- **Clearances after the fix:**
  - Hooks: 4 cm from the socket at x 2.105 and 4 cm from the ladder.
  - Ladder: 2 cm from the casing (2.811), and it sits under the moved heater (2.39..2.79).
  - Rails: 2.4 cm off the tile.

### 6. MED: the master towel ladder rails sink into the tile, and the towel floats in front of them

- **Evidence:** `b1/m_ladder.jpg`
- **What:**
  - The ladder uses wall = -3.23, but the face is -3.26 (tile -3.266). The rails at z -3.28..-3.26 go 6 mm into the tile.
  - The towel (z -3.315..-3.295) floats 1.5 cm in front of the rails.
- **Cause:** L1645.
- **Fix:** `ladder('x', 5.40, 5.90, -3.26, -1, .55, 1.25); B(5.49, 5.87, -3.335, -3.315, .78, 1.12, mat.linenGrey, { cast: false });`.
  The open door leaf (x 6.255..6.945) is clear.

### 7. MED: the shower accent tile stops 9 cm short of the glass

- **Evidence:**
  - `b4/m_sage_strip.jpg`
  - `b3/m_ledge_slot.jpg`
  - `b1/v_shower_day.jpg`
- **What:** the sage accent on the north wall ends at x 5.60, but the WC-side glass is at x 5.685..5.695 after the `.19` shift. A
  9 cm strip of the room tile shows inside the shower, beside the glass.
- **Cause:** L1601 is outside the `withShift(.19, 0)` block, so it still uses the pre-shift glass position (5.49 + .11).
- **Fix:** in L1601, `tileZ(4.63, 5.60, …)` becomes `tileZ(4.63, 5.69, …)` and `tileZ(5.60, 6.015, …)` becomes
  `tileZ(5.69, 6.015, …)`. The joint then hides behind the glass edge.

### 8. MED: the "Roma" vanity puts the basin off the plumbing axis and the mirror (family bath)

- **Evidence:** `fix/vanF_רומא_שחור_80.jpg` (the master case is under owner decisions, item D)
- **What:** for the shelf model, `fixVanity` puts the basin at the middle of the drawer two-thirds (`zb = (z1 + zs) / 2` = zc - .17W)
  and ignores `axis`. In the family bath the basin sits 13.6 cm off the 72 cm axis and the mirror cabinet.
- **Cause:** L803 (`zb` for 'shelf') and L1721.
- **Fix (family bath only):** in L1721, call
  `fixVanity(2.01, v.startsWith('רומא') ? -2.115 + .17 * +v.split('|')[2] / 100 : -2.115, +v.split('|')[2] / 100, .85, v, t)`.
  At W .80 this gives z -2.379..-1.579, 18 cm off the south tile, with the basin on z -2.115.

### 9. MED: the master shower-room window reveals are bare plaster in a room tiled to the ceiling

**Status:** the lead's uncommitted working tree already has exactly this line after the `windowX` call. Check it in the next
build; nothing more to do if it is there.

- **Evidence:**
  - `b1/m_window.jpg`
  - `b3/cer_m_window.jpg`
  - `b4/m_sage_strip.jpg` (right side)
- **What:** the jambs and head (z -5.155..-4.98) are `mat.wall`. The family bath reveals are tiled (L1656).
- **Cause:** nothing after L1605.
- **Fix:** add after L1605:

```js
tileX(-5.155, -4.974, 6.015, 1, 1.25, 2.35, mat.bathWall); tileX(-5.155, -4.974, 6.615, -1, 1.25, 2.35, mat.bathWall); B(6.015, 6.615, -5.155, -4.974, 2.344, 2.35, mat.bathWall, { cast: false });   // tiled reveals (estimate)
```

- **Clearance:** the frame occupies z -5.215..-5.155 and the sill top is at 1.252, so neither overlaps.

### 10. MED: the open family bath door's handle stops 5 mm from the tub glass

- **Evidence:**
  - `b3/f_door_handle_glass.jpg`
  - `b1/f_tub.jpg`
- **What:** the leaf opens to 90° along x 3.68. The handle tip on the tub side is at x 3.755, and the screen glass at 3.76. In
  reality the handle would strike the glass every time the door opens fully.
- **Cause:** L1175.
- **Fix:**
  - Show the door at about 85°: `doorLeaf(3.68, -1.315, -.087, -.996, .81, mat.door, DOORH - .02, .04, -1, 0);`. The handle
    ends up about 6 cm from the glass.
  - Trim the bath mat so the leaf clears it: L1741 `B(3.09, 3.55, -2.625, -1.825, …`.
  - Tell the owner a door stop is needed (floor or wall).

### 11. LOW-MED: the master pipes pass through the upper condenser

- **Where:** laundry niche.
- **Evidence:**
  - `b1/n_pipes.jpg`
  - `b1/f_window.jpg`
  - `b1/n_down.jpg`
- **What:** the main condenser's refrigerant pair (local x 2.27 / 2.20, world 2.49 / 2.42 at z -4.75) rises from .98 straight
  through the master condenser body (world x 2.38..3.22, y 1.05-1.65) and its stand cross-bar.
- **Cause:** L1754.
- **Fix:** `C(2.12, -4.30, .98, H, .016, mat.black, { seg: 10 }); C(2.07, -4.30, .98, H, .012, mat.black, { seg: 10 });`. That puts
  the pipes at world x 2.34 / 2.29, clear of the upper unit (2.38), the stand legs and the bars.
- **Still open:** the upper unit's own pair still rises out of its top (already open since re-check 4).

### 12. LOW: the WC-side shower glass floats 2 cm above the floor with no channel

- **Evidence:**
  - `b1/m_glass_low.jpg`
  - `b3/m_glass_wcside_low.jpg`
- **What:** the room-side glass has a floor track, but the fixed WC-side panel (y .02..2.0) has nothing under it.
- **Cause:** L1613.
- **Fix:** inside the same `withShift(.19, 0)` block, after L1613, add
  `B(5.49, 5.51, -4.974, -4.10, 0, .02, mat.blackMetal, { cast: false });`, which lands at world x 5.68..5.70.

### 13. LOW: the condensate tube ends on the floor, at no drain

- **Evidence:** `b1/n_down.jpg`
- **What:** the white tube from the main condenser ends at world (2.17, .006, -4.55), 47 cm from the riser and 1.7 m from the
  floor drain.
- **Cause:** L1760.
- **Fix:** points `(2.15, .1, -4.30), (2.10, .1, -4.45), (2.04, .1, -4.55)`. In world coordinates, after the shift, that runs into
  the side of the 4" riser at (2.21, -5.02).

### 14. LOW: the family WC ledge stops 4 mm short of the window-wall tile

- **Evidence:** `b4/f_ledge_gap.jpg`
- **What:** after the shift, the ledge and its quartz top start at z -3.765. The tile face is -3.769, so the end face of the quartz
  shows in close-up.
- **Cause:** L1713.
- **Fix:** in both `B(...)` calls on L1713, change `-3.635` to `-3.639`.

### 15. LOW: the family paper holder is behind the user

- **Evidence:**
  - `b1/f_wc.jpg`
  - `b1/f_vanity.jpg`
- **What:** the holder is on the west wall at z -2.865, 26 cm past the side of the bowl and 15 cm behind the ledge face. From the
  seat it sits behind the hip. The usual position is the side wall, a little ahead of the bowl front.
- **Cause:** L1716.
- **Fix (optional):** move it to the window wall below the sill, `B(2.81, 2.89, -3.769, -3.689, .70, .72, mat.blackMetal);`.
  That is outside the shifted block, so use world coordinates. Both holders are flat slabs with no roll; a short white cylinder
  would read better.

### 16. LOW: the swan spout is an open tube end

- **Evidence:** `fix/vanM_romaswan_side.jpg`
- **What:** the end of the `TubeGeometry` is open, and in close-up the spout looks cut off.
- **Cause:** L735.
- **Fix:** add an aerator after the tube: `C(x + .13, z, y + .195, y + .212, .012, m, { seg: 12, cast: false });`.

## Needs owner decision

### A. MED-HIGH: both niches are frames stuck onto the tile, not recesses

- **Evidence:**
  - `b1/m_niche.jpg`
  - `b1/m_shower_in.jpg`
  - `b1/f_tub_niche.jpg`
  - `b3/cer_m_niche.jpg`
  - `b3/cer_f_tubniche.jpg`
- **What:** the "niches" are a taupe panel with 3-3.4 cm returns standing proud of the wall. The tile grid runs straight behind
  them, and the back is not tiled. An architect will read this as a stuck-on box. This is the most visible thing left in both
  baths.
- **Cause:** L1616-1617 (master) and L1709-1710 (family). The walls are solid `W` boxes, so a recess means cutting the wall and
  splitting the tile skin.
- **Proposed recess:** walls are cut, not moved. At `YH` 2.4 every cut segment stays full height, so `roomdims` is unchanged
  (+0). The baked AO is off by default (`6241532`), so the merged-wall bake mismatch does not show.
- **Master** (world x 4.91..5.41, y 1.03..1.42, 9 cm into the 41 cm facade wall):
  - L1060: `W(4.63, 6.015, -5.39, -4.98);` becomes
    `W(4.63, 4.91, -5.39, -4.98); W(5.41, 6.015, -5.39, -4.98); W(4.91, 5.41, -5.39, -4.98, 0, 1.03); W(4.91, 5.41, -5.39, -4.98, 1.42); W(4.91, 5.41, -5.39, -5.07, 1.03, 1.42);`
  - L1601, with item 7 applied: the sage `tileZ(4.63, 5.69, -4.98, 1, 0, H, mat.sage)` becomes
    `tileZ(4.63, 4.91, …); tileZ(5.41, 5.69, …); tileZ(4.91, 5.41, -4.98, 1, 0, 1.03, mat.sage); tileZ(4.91, 5.41, -4.98, 1, 1.42, H, mat.sage);`
  - Add the lining:
    `tileZ(4.91, 5.41, -5.07, 1, 1.05, 1.42, mat.sage); tileX(-5.07, -4.974, 4.91, 1, 1.03, 1.42, mat.sage); tileX(-5.07, -4.974, 5.41, -1, 1.03, 1.42, mat.sage); B(4.91, 5.41, -5.07, -4.974, 1.414, 1.42, mat.sage, { cast: false }); B(4.91, 5.41, -5.07, -4.96, 1.03, 1.05, mat.nicheStone);`
  - Delete L1616-1617.
- **Family** (z -2.055..-1.505, y 1.0..1.30, 7 cm into the 15 cm partition, leaving 8 cm):
  - L1086: `W(4.46, 4.61, -3.23, -1.37)` becomes
    `W(4.46, 4.61, -3.23, -2.055); W(4.46, 4.61, -1.505, -1.37); W(4.46, 4.61, -2.055, -1.505, 0, 1.0); W(4.46, 4.61, -2.055, -1.505, 1.30); W(4.53, 4.61, -2.055, -1.505, 1.0, 1.30)`
  - Split L1651 `tileX(-2.98, -1.395, 4.46, -1, 0, H, …)` the same way.
  - Line the recess with `mat.bathWall2`, add a stone sill, and delete L1709-1710.
- **Owner's call:** whether a 7 cm recess in that partition is acceptable. The cheaper alternative is to leave them as they are.

### B. MED: the shower entry is only about 46-49 cm clear

- **Evidence:** `b1/v_shower_day.jpg`
- **What:** with two 59 cm panels on a 106 cm front, the slider opens 46-49 cm. That is below the usual 55-60 cm.
- **Options:**
  - A hinged 57 cm door on the corner post, opening out. It clears the vanity front at x 5.11.
  - A fixed walk-in panel.
  - Keep the slider and say so in the notes.
- **Note:** d08 supplies no enclosure at all. The notes already say this.

### C. MED: a 160 cm tub does not fit the modelled opening

- **Evidence:** `b1/f_low_apron.jpg`
- **What:** the brick-to-brick length is 158.5 (stub wall to south wall, following the sales plan); tile to tile it is 157.3. The
  picker says "160×70". The construction sheet writes 163 with a 253 cm room. This is the known 238 vs 253 conflict.
- **Options:** ask the contractor, or label the tub as about 157 in the picker. Do not move walls.

### D. MED: the master Roma vanity basin is 9 cm off the axis, and the fix in item 8 cannot work there

- **Evidence:**
  - `fix/vanM_רומא_לבן_70.jpg`
  - `fix/vanM_romaswan_side.jpg`
- **What:** the master shows spec vanities at 70 cm. Centring Roma's basin on z -3.70 would push the cabinet past the south tile,
  and flipping it would hit the shower frame.
- **Options:** drop Roma from the `vanM` options (its spec sizes are 80/100, squeezed to 70 here), or accept the offset.

### E. LOW-MED: the master shower floor is 60x120 tiles at a point drain

- **Evidence:**
  - `b1/m_glass_low.jpg`
  - `b3/cer_m_floor.jpg`
- **What:** the default master floor (60x120, not from the spec) runs into the shower. d08 says the shower falls are made in the
  tiling ("שיפועים ע"י ריצוף"). Large format cannot fall to a point drain without envelope cuts. An architect will ask how it
  drains.
- **Options:**
  - Use the spec's 30x30 / 33x33 inside the shower.
  - Show a linear drain along the north wall.
  - Leave it and note it.

### F. LOW: the water-heater switch is behind the heater

- **Evidence:** `b1/n_heater.jpg`
- **What:** the IP65 switch is on the east niche wall at z -4.90..-4.78, 6 cm behind the heater body. That matches the electrical
  sheet (4.28, -4.84), but nobody can reach it.
- **Options:** keep it per the plan, or move it to z -4.30..-4.18, south of the heater, at L1767.

### G. LOW: the master condenser blocks the family bath window

- **Evidence:**
  - `b1/f_window.jpg`
  - `b1/v_bath2_day.jpg`
- **What:** the master condenser on its stand (y 1.05-1.65) stands 70 cm outside the window, at sill height. It follows the AC
  sheet's two outlines, and that window is also the only access to the niche. Note only.

### H. LOW: a 23 cm dead slot between the master shower glass and the cistern ledge

- **Evidence:** `b3/m_ledge_slot.jpg`
- **What:** the gap between the glass (x 5.69) and the ledge (x 5.92) is hard to clean.
- **Option:** extend the ledge to the glass, at L1626: `B(5.705, 6.85, …)` for both boxes. The WC and the plate stay at 6.25.

### I. Note: d08 says no dryer connection

- **What:** d08 writes "אין הכנה לחיבור מייבש כביסה" (no dryer connection prepared). The model shows a stacked washer and dryer.
  The electrical sheet has two sockets at h 140, so a condensing dryer works. Worth one line in the notes if the architect asks.

## Not reported (already open elsewhere)

- Vertical tile joints on x-facing walls do not start from a corner (`cerApply` uses the x origin), in PROJECT_MEMORY.
- AC pipes rising out of the condenser top.
- Water heater Ø54 vs Ø60 on the plan, and riser 1 not modelled (re-check 3, optional).
- Interior door leaf and casing colours belong to the door-frame owner. The family bath leaf reads grey next to a white casing
  in `b1/f_door_closed.jpg`; it is worth a look by whoever owns doors.
