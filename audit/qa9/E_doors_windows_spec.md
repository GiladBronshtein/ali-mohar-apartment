# QA9 E: doors, windows, openings, finish junctions, spec compliance, exterior pass

Scope: every door, window and opening of the apartment, the junctions around them, what the sale spec (d08), its addendum
(d10, prevails), d09 and d11 say about what is visible, and an exterior pass around our flat. Model as of commit `6241532`
(`source/salon.html`, 3486 lines). Report only; no tracked file edited.

Evidence: 96 captures in `audit/qa9/E_img/` (day and eve, doors open and closed), taken with `out/shots.mjs` through the GPU
lock. Image names below are relative to that folder. Spec items quoted by number only (the spec files hold personal data).
Two manufacturer pages were read for d10 items 4 and 5 (sources at the end).

Already listed as open in `audit/recheck5/APPLIED.md` and not raised again: door and window sizes (d08 vs plans), bedroom
windows one sash vs "fixed lower part", mamad leaf width, escape window vs the master bars, tile sizes, kitchen splash height.

## Ranked findings

### High

**H1. Entrance door is a featureless slab; the spec door (d10 item 4) has visible hardware the model lacks.**
Evidence: `d19_entrance_inside.jpg`, `d20_entrance_handle.jpg`, `e33_entrance_far.jpg`, `e12_entry_skirting_corner.jpg`.
- d10 item 4: model "גרדה", painted, nickel handle, by רב בריח or equal. The maker's page for "גארדה" lists: nickel
  "Coral" hardware, a hardened cylinder guard, multi-bolt lock, telescopic peephole, a silver Lipsky stopper, a security
  latch, steel frame (standard or flush), pipe or concealed hinges; the recessed horizontal grooves are on the outer skin.
- Model: L1163 one box `B(1.565, 2.575, 5.49, 5.55, 0, DOORH + .01, mat.entryDoor)`; L1164 handle = two steel boxes
  (an L-shaped block, 15.5 cm from the latch edge, no rose, no plate, no cylinder); no peephole; `mat.entryDoor` (L513) has
  `metalness: 0.3`, so a painted door reads as dull metal. The lobby face (where the grooves are) is inside the solid core
  block `W(1.19, 3.63, 5.70, 9.11)` (L1067) and cannot be seen from anywhere.
- Fix (positions and sizes are estimates; colour stays the architect's per d08 15 ד):
  ```js
  // L513: painted steel (d10 item 4 "צבועה"), not metal
  entryDoor: M('#55595d', 0.45),
  // replace L1164 (inside face z 5.49, latch edge x 2.555): Garda hardware in nickel
  { const nk = FINM.brushed;
    B(2.470, 2.505, 5.482, 5.490, .82, 1.22, nk);                                              // long escutcheon plate
    B(2.478, 2.497, 5.450, 5.482, 1.00, 1.02, nk); B(2.36, 2.497, 5.442, 5.456, 1.00, 1.02, nk, { round: .005 });   // lever toward the hinge
    const disc = (x, y, r, d) => { const c = C(0, 0, -d, d, r, nk, { seg: 20, cast: false }); c.rotation.x = Math.PI / 2; c.position.set(x, y, 5.482); };
    disc(2.4875, .90, .014, .004);                                                             // cylinder / thumb-turn rose
    disc(2.07, 1.50, .011, .006);                                                              // telescopic peephole
    B(2.40, 2.44, 5.478, 5.49, 1.38, 1.46, nk); }                                              // security latch
  ```
  Optional: a Lipsky floor stopper where the leaf stops; and (owner decision) a thin slice of the landing so the grooved
  outer face can be shown.

**H2. Interior doors read grey, not white, from inside the rooms (room 2, family bath, master, master bath).**
Evidence: `e03_room2_door_inside_closed.jpg`, `f10_room2_door_inside_closed_eve.jpg` (blue-grey against warm walls),
`f03_fbath_casing_tile.jpg`, `f04_mbath_casing_tile.jpg`, `d07_master_door_room_closed.jpg`; compare `f12_room1_door_inside_day.jpg`
(room 1, just inside its gate, reads white). The casings beside each leaf are white, so the leaf looks like a different
product. d10 item 5 is a white formica leaf (Pandor "אקווה ביאנקו").
- Root cause: the room gate (L2696) lights each surface only inside its room's box. The closed leaves sit in the doorway,
  outside the box: room 2 leaf room face z -1.375 vs `r2` z2 -1.40; family bath face -1.335 vs `fbath` -1.34; master face
  x 4.225 vs `master` x1 4.56; master bath face x 6.925 vs `mbath` x2 6.90. Room 1 (-1.375 vs -1.37) is just inside.
- Fix in L2696: `r1 = [-3.94, -5.08, -1.10, -1.33]`, `r2 = [-1.02, -5.06, 1.90, -1.33]`, `fbath = [1.96, -3.82, 4.51, -1.30]`,
  `mbath = [4.58, -5.03, 6.94, -3.21]` (each stops short of the corridor or closet face). The master box cannot simply move to
  x 4.17 (it would light the east end of the family bath, x 4.17..4.46, z < -1.37); give it a second box for the door
  vestibule `[4.17, -1.26, 4.62, -.09]` (this also lights the vestibule floor and walls, which are unlit today): add a
  `rectBox2`/`pointBox2` array (a far-away box `[9e3, 9e3, 9e3, 9e3]` for every other light) and gate with
  `max( G(rectBox[i]), G(rectBox2[i]) )`. Re-shoot the four rooms day and eve; check no light lands on the corridor faces.

**H3. Our own building's shaded plaster reads dark slate blue: balcony walls, north and west facades.**
Evidence: `e19_balcony.jpg`, `e20_balcony2.jpg`, `e18_view.jpg` (preset views), `x10_balcony_doors_from_balcony.jpg`,
`e16_street_tele.jpg`, `x07_north_facade_out.jpg`, `e32_west_out_bird.jpg`, `f06_north_elev.jpg`. The neighbours' blocks in the
same light stay off-white.
- Root cause: `mStuccoOut` (L593, colour `#ecebe6`) uses the default `ENV` .3 by day. The neighbour facade atlas materials
  (L2253, L2352) and the ground sets (L2130, "west faces we look at sit in sun shadow: lift them with the sky") get
  `userData.envDay = 1.1`; our shell does not, so every face out of the sun drops to about `#5a5f68`.
- Fix: after L593 add `mStuccoOut.userData.envDay = 1.0;` (try .8 to 1.1; check sunlit faces in `street` and `bird1` do not
  wash out). Applies to the balcony walls, upstand, soffit and all six storeys.

### Medium

**M1. Door hardware: levers without roses or key escutcheons; no free/occupied turn lock on the two bath doors.**
Evidence: `d16_room2_handle_close.jpg`, `e34_bath_handle_inside.jpg`, `d04_bath_door_corr_closed.jpg`.
- d08 annex B 15 ה: bathrooms get a "תפוס/פנוי" turn lock. Standard interior doors also carry a key escutcheon.
- Model: `doorLeaf` L1006 draws a bare 2 cm block plus a bar per face; nothing else.
- Fix: in `doorLeaf` after L1006 add a square rose and an escutcheon per face:
  ```js
  [-1, 1].forEach(s => { lb(P, w - .105, w - .055, s * (t / 2), s * (t / 2 + .008), .985, 1.035, mat.blackMetal);   // rose 5x5
    lb(P, w - .092, w - .068, s * (t / 2), s * (t / 2 + .006), .91, .94, mat.blackMetal); });                        // escutcheon 85 mm below
  ```
  Bath doors, through the `extra` argument: family bath (L1175, local +z is the bath side when closed): thumb turn
  `lb(P, w - .086, w - .074, t / 2 + .006, t / 2 + .024, .905, .945, mat.blackMetal)`, indicator on the corridor face
  `lb(P, w - .09, w - .07, -t / 2 - .004, -t / 2, .915, .935, M('#c8312b', .4))`. Master bath (L1178): the bath side is local
  -z (the mirror is on +z, the closet), so swap the signs. Hinges (3 per leaf, on the hinge edge) would complete it (L5).

**M2. The laundry screen exists only on floor 2; every other floor shows a glazed window in its place.**
Evidence: `f06_north_elev.jpg`, `e17_north_bird.jpg`, `x04_bird2.jpg`. A stacked service-balcony screen is what an architect
expects on this elevation.
- Root cause: L2086 `ours` includes `['x', 2.15, 3.65, -5.39, -1, .15, 2.35]`, drawn as dark glass with a frame and sill on
  floors 1 and 3-6; the louvres (L1745) are drawn for floor 2 only.
- Fix: remove that entry from `ours`; for each `dy` of `[-3.3, 3.3, 6.6, 9.9, 13.2]` draw a dark backing plate on the face
  (`B(2.15, 3.65, -5.392, -5.39, .05 + dy, 2.65 + dy, mDark, oo)`) and blades just outside it, as at L1745:
  `for (let y = .1; y < 2.7; y += .10) B(2.15, 3.65, -5.43, -5.40, y + dy, y + dy + .008, mat.louver, oo).rotation.x = -.45;`
  (`oo` = `upperG` above floor 2, `outside` below, as in the loop). The upper storeys are a solid mass behind the face, so
  the blades must sit outside it.

**M3. Master shower room: walls tiled to the ceiling (d10 item 2) but the window reveals are bare plaster.**
Evidence: `w10_mshower_window.jpg`, `e07_mshower_reveal.jpg`. The family bath reveals are tiled (L1656), so the two rooms differ.
- Fix after L1605 (frame inner face z -5.155, wall face -4.98):
  ```js
  tileX(-5.155, -4.974, 6.015, 1, 1.25, 2.35, mat.bathWall); tileX(-5.155, -4.974, 6.615, -1, 1.25, 2.35, mat.bathWall);
  B(6.015, 6.615, -5.155, -4.974, 2.344, 2.35, mat.bathWall, { cast: false });   // tiled reveals (estimate), like the family bath
  ```

**M4. Sliding openings are drawn as one plane with a centre mullion, not sash on sash.**
Evidence: `w02_slider_meeting.jpg`, `w03_slider_bottom_track.jpg`, `x10_balcony_doors_from_balcony.jpg`, `w11_fbath_window.jpg`.
d08 table 3 writes "נגרר כ.ע.כ" for the living doors and "כ.ע.כ" for the family bath window (annex B 15: a sash sliding over a
sash). `slider()` (L1232) and `windowX(..., slide = true)` (L1009) put both panes and the mullion in one 7 cm plane.
- Fix: two sashes on two tracks about 3.5 cm apart, each with its own 5 cm frame, overlapping 5 to 6 cm at the meeting
  stiles; the outer frame 9 cm deep. Keep the pull on the inner sash. Same change in `windowX` when `slide`.

**M5. Master bath door: the closet-side lever goes through the mirror frame.**
Evidence: `e06_mbath_mirror_handle.jpg` (the lever and its reflection overlap the black frame).
- L1179: mirror `.08..w - .08`, frame `.06..w - .06`; the lever spindle is at `w - .09..w - .07`.
- Fix: mirror `B(.08, w - .16, ...)`, frame `B(.06, w - .14, ...)`, reflector `new THREE.PlaneGeometry(w - .24, 1.7)` centred at
  `(w - .08) / 2`, so a 9 cm solid stile carries the handle.

**M6. Insect screens (d10 item 6) are not drawn.**
d10 item 6: the windows of the living room, kitchen, master, master shower room, rooms 2 and 3 and the mamad "יהיה כולל רשת";
the family bath is the only one left out. The panel says the screens are not drawn (L184), but its wording "חוץ מחלון חדר
הרחצה" is ambiguous with two bathrooms: write "חוץ מחלון האמבטיה הכללית". Drawing them is an owner decision (see below).

### Low

- **L1. Interior sills cover only the front 5 cm of a 15 to 20 cm reveal.** `windowX`/`windowZ` L1015, L1028 and the kitchen
  board L1241 are 5 cm deep; behind them the wall top shows as plaster to the frame. Evidence `e10_windowC_in_close.jpg`,
  `w07_room1_sill.jpg`. Fix: run the board from the frame's inner face to 2 to 3 cm proud of the wall (e.g. in `windowX`
  `B(x1 - .03, x2 + .03, zc + s * .03, zIn + s * .03, ...)`). d08 does not write sills; stone is an estimate either way.
- **L2. Master shower kip sash has its handle on the side stile at 1.60** (L1017 via L1605). A bottom-hung kip sash is
  operated from the top rail. Evidence `e07_mshower_reveal.jpg`. Fix: a `kip` flag that puts the rose on the top rail
  centre (`(x1 + x2) / 2`, about `head - .09`).
- **L3. Kitchen window C is a one-pane "slider" with a pull** (L1240 `slider(7.75, 8.45, 1.20, HEAD, 1)`): a single pane
  cannot slide. Evidence `e09_windowC_out.jpg`, `w05_kitchen_window_C.jpg`. Fix: `panes` 2, or a tilt sash with a lever.
  Type not written anywhere (estimate).
- **L4. No hinges on any leaf**, interior or blast door (`doorLeaf` L1001). The blast door opens outward, so its heavy
  hinges would be on the corridor face (`d10_mamad_door_corr_open.jpg`). Add 3 knuckles per leaf on the hinge edge.
- **L5. Floor 2's windows have no exterior sill, while every other storey's windows do** (L2094 draws sills only for the
  storeys above and below). Evidence `x07_north_facade_out.jpg` (crop: upper window with a projecting sill, ours recessed
  without). Fix: in the same block, for each `ours` entry with `sill > .1`, add the same `mat.sill` board at the outer face for
  floor 2 (`dy` 0). Related: only our master window has outside bars; the same window on floors 1 and 3-6 has none
  (`f08_east_elev_tele.jpg`). Part of the open escape-window question, so not changed here.
- **L6. Balcony railing spacing and height (estimate, worth a glance from the architect).** Bars 2 cm at 12 cm centres
  (L1879, L1881, L1884, L2141..L2147) leave 10 cm clear, the limit itself in the Israeli railing standard as I understand
  it (please verify SI 1142); 11 cm centres give 9 cm. The 45 cm upstand with a 15 cm top could count as a foothold, which
  leaves 64 cm of railing above it. Upstand and railing heights are estimates (recheck5 item 45).
- **L7. 3 to 4 cm skirting stubs between the room-side casing and the room corner** (rooms 1 and 2, east of the door).
  Evidence `f12_room1_door_inside_day.jpg`, `e03_room2_door_inside_closed.jpg`. Cosmetic; extend the `noSkirt` box to the
  corner (L1136) or leave as built.
- **L8. Panel text.** "שורגים" should be "סורגים" (L171 balcony, L189 master). Screen sentence, see M6.
- **L9. Balcony floor label.** CER `balc` (L3392) labels the default "דק עץ (לא מהמפרט)". d10 item 12, second paragraph,
  adds to annex B 11 item 4 (balconies) "כולל אפשרות לריצוף דמוי פרקט". A wood-look porcelain is therefore within the
  addendum. The default could be relabelled as wood-look porcelain (and drawn as tile planks with grout), or kept as is.

### Checked and correct

- Swings and hinge sides against the sales plan and the code comments: rooms 1, 2 and the family bath open into the room;
  the master door opens into the master, hinge on the TV-wall side; the master bath door opens into the bath; the mamad
  blast door opens outward into the corridor, hinge west, no inner door (d08). Open blast door parks at the corridor end
  as the panel says (`d01`, `e24`).
- New Pandor frames (L1134..L1195): jamb, stop, 7/8.5 cm casings with a step; the skirting stops under each casing edge
  without overlap (`d17_room2_casing_skirting.jpg`, `e01_room2_head_corr_wide.jpg`); casings over the bath tiles read
  correctly (`f03`, `f04`). Leaf 4 cm (Pandor PanPremium is 41 mm).
- Mamad: steel frame and lining, floor 2 cm up with the step in the doorway (`e05_mamad_threshold.jpg`); blast window 100 x
  100, sill 1.10, steel frame (`w12`, `e28`); no shutter visible is consistent with the pocket shutter and steel sash parked.
- Shutters: five electric shutters (rooms 1, 2, master, doors A, B) with rails outside the glass and the box hidden in the
  lintel; none on window C (d08, electrical sheet).
- Sills and heads as on the construction plan; master shower one kip sash; family bath window sliding with tiled reveals.
- Corridor drop ceiling, the 120 cm passage and the kitchen soffit junctions are clean (`j01`, `e14`, `e15`).
- Exterior: nothing floating or unfinished found near our flat in the 20 exterior captures, apart from H3, M2, L5.

## d10 (addendum) checklist

| # | Addendum item (summary) | Shown in the model | Note |
|---|---|---|---|
| 1 | Kitchen: stone splash about 50 cm above the base units, not in the window area | Yes, 70 cm | Owner decision (cabinets from 1.62), recorded in recheck5 |
| 2 | Bath wall tiles to the ceiling or to the underside of the drop | Yes | Family bath to the drop, master to the ceiling; master window reveals untiled (M3) |
| 3 | Complete vanity units with a ceramic top and basin in both baths | Yes | Recheck5 |
| 4 | Entrance door "גרדה", painted, nickel handle, רב בריח or equal | Partly | Painted dark leaf and a metal handle; no peephole, cylinder, plate, stopper; reads metallic; lobby face not modelled (H1) |
| 5 | Pandor "אקווה ביאנקו" white doors: master, master shower, rooms 2, 3, family bath | Yes, 5 leaves | White flush leaves, PanClassic frames; leaves render grey from inside 4 rooms (H2); bath locks missing (M1); the mirror on the master bath leaf is an owner addition |
| 6 | Screens on the windows of living, kitchen, master, master shower, rooms 2, 3, mamad | No (stated in the panel) | M6. The item names the kitchen, which supports keeping window C (recheck5 conflict C6) |
| 7 | Water point for a Tami4 bar | Not shown | Under the sink, not visible; nothing to draw |
| 8 | Garden tap on the balcony, cold only, no extra drain | Yes | South wall h=60 |
| 9 | Gas point preparation on the balcony | Yes | h=30 |
| 10 | Three-phase hob point under the hob; island socket; balcony socket and TV point | Yes | Hob point hidden (induction hob fits); sockets at estimated positions |
| 11 | Mini-central inverter 52,000 BTU for kitchen, living, dining, rooms 2, 3, mamad; corridor duct with gypsum drop; master split 12,000 | Yes | Unit over the family bath ceiling, corridor drop and grilles, master split over the door. The mamad has no AC grille; its air would come through the slotted sleeve plates (L1119..L1121). Confirm on the AC sheet |
| 12 | Tiles about 80/80 incl. glossy; balconies may take wood-look tile | Yes | Ceramic picker; balcony label, see L9 |
| 13 | Upgrade cost | n/a | Contract, not modelled |

## Needs owner decision

1. **Draw the insect screens?** (d10 item 6.) They are in the contract but darken the view. Options: a mesh sash parked
   behind one sash of each living door (third track) and fixed or roll-up screens on the other windows, or leave them out
   and keep the panel note (with the wording fixed).
2. **Interior door hardware finish.** The model uses matte black square levers; the spec names no finish for the interior
   doors (only nickel for the entrance). Keep black or match the entrance in nickel.
3. **Entrance door outer face.** Showing the grooved Garda skin means modelling a slice of the landing in front of the door
   (today it is inside the solid core block).
4. **Mamad AC.** d10 item 11 lists the mamad among the rooms the mini-central serves; the model shows no supply grille there.
   Check the AC sheet for whether it goes through a sleeve.
5. **Railing** (L6): keep the estimated spacing and upstand, or tighten to 11 cm centres pending the real detail.

## Sources (manufacturer pages, for d10 items 4 and 5)

- Rav Bariach, "גארדה" entrance door: https://www.rav-bariach.co.il/product/%D7%93%D7%92%D7%9D-%D7%92%D7%90%D7%A8%D7%93%D7%94/
- Pandor interior door collection (Aqua Bianco is the white formica finish; PanPremium leaf 41 mm, polymer frame):
  https://www.pandoor.co.il/door-collection, https://www.pandoor.co.il/panclassic
