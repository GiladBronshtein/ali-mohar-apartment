# Re-check 5: systems in the technical sale spec, annex C and the spec addendum

Agent: spec_systems. Report only, nothing in `source/salon.html` was changed.

Documents (staged in `source/out/docs5/`, not in git):

- d08, technical sale spec, edition 1, pages 16 to 21: Table 4 (sanitary), 3.6.1 to 3.6.8 (water, gas), 3.7 Table 5
  (electrical) and 3.7.1 to 3.7.10, 4 (AC and heating), 5 (fire), 6 to 9 (site, shared systems, shared property).
  A few annex B lines (pages 25, 27, 29, 30) and page 15 are cross-referenced where they touch the same items.
- d09, annex C: the credit and charge tables (prices are not reported here).
- d10, the addendum to the technical spec. It says that where it conflicts with the agreement, "הוראות התוספת
  תגברנה" (the addendum prevails). Page 1 holds personal data: it is quoted only by item number, not cropped.

Model: `source/salon.html` at commit 6b679fd (3105 lines). Line numbers below are from that file.

Earlier work read first: `audit/recheck3/electrical.md`, `plumbing_ac.md`, `APPLIED.md`, `PROJECT_MEMORY.md`,
`CERAMICS.md`, `DESIGN.md`. The model already follows the contractor's electrical, plumbing and AC sheets (HADA, dated
9/2/2006 as written); this report compares the spec against the current model.

Room names. The spec numbers the bedrooms: (1) master, (2) and (3) the two children's rooms, (4) the mamad. The model
calls them master, room 1, room 2 and room 3 (mamad). Rows (2) and (3) are identical in every table, so which one is
room 1 does not matter here.

"Written" means a word or number in the document. "Estimate" means mine. "Sheet" means the contractor's electrical,
plumbing or AC sheet in `materials/plans/vector/`.

Crops: `audit/recheck5/spec_systems_crops/` (spec tables and the d10 page 2 items, no personal data).

## Proposed changes, priority order

1. **Balcony: add a regular socket and a TV point** (d10 item 10, written; position estimate). Items 56, 79.
   After line 1833 add `outlets('e', FO, 4.12, .40, 'st');   // d10 item 10: regular socket + TV point on the balcony (position and height an estimate)`.
   This puts both plates on the balcony face of the pier (z 4.04..4.20), next to the IP44 box (z 3.84..3.94). Ask the
   developer where they go; d10 gives no position.
2. **Kitchen island: add a regular socket** (d10 item 10, written; position estimate). Items 31, 79.
   After line 1359 add `outlets('w', IX1 + .02, 6.90, .70, 's');   // d10 item 10: socket for the island, on the drawer block side (position an estimate)`.
3. **Basin mixers deck-mounted, and one-piece ceramic tops with the basin** (d08 Table 4 "בעמידה", d10 item 3
   "משטח חרס כולל כיור"). Items 6, 7, 80. Master bath lines 1449 to 1451, family bath lines 1541 to 1543: replace the
   stone top plus vessel or semi-recessed basin with one white ceramic top and a sunken bowl, and replace the wall
   spouts (1451, 1543) with a deck mixer behind the bowl. Bowl about 40/50 (d08); top size "עפ"י תכנית חברה" (not
   given). This also touches the open vanity-size question in `CERAMICS.md`.
4. **Second condenser in the laundry niche** (AC sheet outline 84 x 40, now backed by d10 item 11, which supplies the
   12,000 BTU master split). Items 60, 84. See item 60 for the code and the pipe clash it causes.
5. **Kitchen splash: correct the "cur" label, and decide the height with the owner** (d10 item 1: stone cladding about
   50 cm above the counter; the model has 70 cm). Items 77, 78. Line 3029 `cur: 'לוח קוורץ כמו המשטח (לא מהמפרט)'`:
   the stone option is in fact the contract item. Height: line 1344 (`.92` to `1.62`).
6. **Mamad floor material** (d08 annex B page 25: "בממ"ד: אין להתקין פרקט ו/או ריצוף דליק אחר"). Items 88, 105.
   Line 873 gives the mamad `mat.planks`, which the docs call laminate. Either give the mamad the porcelain tile, or
   state in the panel that the plank look is a porcelain parquet-look tile (allowed by d10 item 12).
7. **Rain head over the bathtub: remove or mark as owner choice** (d08 Table 4, "מקלחת ראש קבועה": "-"). Item 10.
   Line 1524 (`C(4.11, -1.72, 1.95, ...)` head and rod). No sheet shows it either.
8. **Comment and notes only** (no geometry): line 1807 says 12,300 BTU (AC sheet), d10 says 12,000 (item 59); record
   that the cisterns are concealed per d08 (item 8); the blue box "1" over the entry door is probably the bell
   (item 40); the master "E" point is probably the audio intercom (item 33); the developer delivers no shower
   enclosure and no bath heaters (items 9, 52).
9. **Optional, low**: lobby light push button by the entry switch (item 39); chime box over the entry door (item 40);
   pull-out spray on the kitchen faucet (item 5); insect screens (item 82).

None of these moves a wall, so `roomdims.py` is unaffected. Run `clearance_audit.py` after 2 and 3.

## A. Table 4, sanitary fixtures (d08 page 16 and 17)

Crops: `d08_p16_table4_sanitary.png`, `d08_p17_table4_cont.png`.

| # | Item | Written (d08) | Model now | Change |
|---|---|---|---|---|
| 1 | Kitchen sink size | "כ-40/60" | single bowl 70 x 45, lines 1305 to 1313 (`SK1`, `SK2`) | Conflict d08 vs the owner's studio choice (stainless, `CERAMICS.md`, d07 page 25). Keep; owner choice |
| 2 | Kitchen sink type | "סוג א' ... אקרילי, התקנה שטוחה"; annex B page 27: "כיור במטבח לבן" | undermount stainless (`mat.sinkSteel`) | Same conflict as 1. Keep |
| 3 | Basins, size | master bath and family bath "כ-40/50 לפי יצרן" | master: vessel 28 x 34 on a stone top (line 1450, in `withShift(.19, .06)`); family: semi-recessed 28 x 30 (line 1542) | Both bowls are smaller than 40/50. See change 3 |
| 4 | Basins, type | "א' (חרס)" | `mat.ceramic` | matches |
| 5 | Kitchen mixer | "פרח מטיפוס 'מערבל' עם מתז נשלף" (deck mixer with pull-out spray); annex B: "פרח/מיקס ברז נשלף" | deck gooseneck, side lever, lines 1315 to 1318 | Deck type matches. The pull-out spray is not drawn. Optional: a thicker spray head with a hose (low) |
| 6 | Basin mixers | both baths: "סוללה מטיפוס 'מערבל' בעמידה" (deck-mounted) | wall spouts: master line 1451 (`B(4.44, 4.56, -3.77, -3.75, 1.02, 1.04)`), family line 1543 (`B(2.01, 2.2, -2.125, -2.105, 1.00, 1.02)`) | Conflict. Replace with deck mixers (change 3). The studio pick in `CERAMICS.md` is also a deck type ("פרח פיה קצרה") |
| 7 | Vanity top | Table 4 silent; d10 item 3 (see 80) | stone tops (travertine 1449, quartz 1541) | change 3 |
| 8 | Toilets | both baths "כ-60/40 לפי יצרן", "חרס. מיכל הדחה סמוי"; annex B: "תלויה" | wall-hung bowls on concealed-cistern ledges with flush plates, master lines 1440 to 1444, family lines 1528 to 1531; bowl 36 x 53 | matches d08. **Conflict with the plumbing sheet** ("מיכל הדחה גבוה" / "נמוך"). d08 is the newer document; the open item "cisterns drawn exposed" in `PROJECT_MEMORY.md` can be closed as "concealed per d08" |
| 9 | Master shower | "כ-80/80 (כ-0.65 מ"ר) ללא מקלחון", "שיפועים ע"י ריצוף" | 106 x 92 tray area with fixed glass and a sliding door, lines 1428 to 1433; point drain line 1434 | **Three-way conflict on size**: d08 80/80, plumbing sheet 106 x 92, construction plan 110 x 96. Model follows the plumbing sheet; keep. d08 says no enclosure: the glass is an owner addition. Note it in the panel; no geometry change |
| 10 | Fixed head shower | master: "-"; bath: "-" | master: wall arm and head at 2.10 (line 1436, from the plumbing sheet "ראש טוש H-210"); bath: ceiling rain head on a rod at (4.11, -1.72), line 1524 | Master: conflict d08 vs plumbing sheet and the studio pick (head, arm and rod in `CERAMICS.md`); keep. Bath: no document shows a head; remove or label as owner choice (change 7) |
| 11 | Shower mixer | master: "מערבל 3 דרך" under plaster, with hand shower ("מזלף"), flexible hose and "מוט תליה" | concealed mixer line 1438, hand shower on a rail line 1437 | matches (the plumbing sheet writes "4 דרך"; not visible) |
| 12 | Bathtub | "כ-160/70", "א' אקרילי או אחר" | 158.5 x 70 hollow tub, line 1514 | matches |
| 13 | Bath mixer | "סוללה רגילה מהקיר"; annex B page 27: with "ראש מקלחת נייד (טלפון)" | wall mixer at .85 (line 1521), rail and hand shower from 1.50 (line 1523) | matches |
| 14 | Washer connection | service area "יש" | washer under the laundry cabinet in the family bath, lines 1468 to 1473; Table 5 puts the service area with the family bath | matches |
| 15 | Dryer connection | "הכנה לחיבור מייבש כביסה": "אין" | stacked dryer (line 1469) and a dryer socket h=140 (line 1812, electrical sheet) | Conflict d08 vs the electrical sheet, which draws two sockets. Table 5 gives 2 power points in this room (item 37), which supports two appliances. Keep; the dryer is the owner's. No vent is written (a condenser or heat-pump dryer needs none, estimate) |
| 16 | Dishwasher | kitchen "יש" (with sink connection and drain) | dishwasher front, lines 1303, 1319 | matches |
| 17 | Fridge water point | "אין" | plain fridge, line 1274 on | matches |
| 18 | Cooking gas point | kitchen "יש" | induction hob (line 1320 on), no gas valve drawn | Not visible (under the counter). d10 item 10 adds a 3-phase hob point. No change |
| 19 | Heating gas point | "אין" | none | matches |

## B. 3.6.1 to 3.6.8, water and gas (d08 page 17)

Crop: `d08_p17_3.6.1-3.6.8.png`.

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 20 | Water distribution cabinet | 3.6.1: "יתכן ארון למחלקי מים במרפסת שירות ו/או מיקום אחר" | none | Location not fixed by any document. Not modelled; ask the developer |
| 21 | AC prep routing | 3.6.1: condensate drain and gas/control piping from the condenser location to the evaporator; AC location "במרפסת שרות ו/או במסדרון ו/או אחר"; condenser "במסתור כביסה" | mini-central above the family bath (`BC`, line 928; hatch line 1498); condenser in the niche (line 1563); refrigerant pair line 1568 | matches (the bath ceiling counts as "אחר"; the AC sheet puts the unit there) |
| 22 | Hot water | 3.6.2: solar system "יש", tank "150" litres, "דוד שמש בגבוי חשמלי", location "במסתור כביסה או בלובי קומתי או במקום אחר", forced system "עם מחליפי חום בתוך הדוד" | tank Ø54 x 1.25 m on legs in the niche, line 1572 (effective centre (4.04, -4.69)) | Location matches. Size plausible for 150 l (estimate). The roof collectors are not modelled (outside the model) |
| 23 | Hot water to fixtures | 3.6.3: kitchen sink, basins, bath, shower, washer prep; "ללא כיור לנטילת ידיים בשירותי אורחים" | no guest WC in the plan | matches |
| 24 | Garden tap | 3.6.4: "כן" struck, "לא" kept (no tap) | tap at the balcony south wall, h .60, line 1835 | **Conflict d08 vs the plumbing sheet** ("ברז גן 1/2"" H-60). Resolved by d10 item 8, which adds it (item 81). Model matches d10 |
| 25 | Water meter prep | 3.6.5: "יש" | none | Outside the apartment (lobby riser cabinets). No change |
| 26 | Pipe materials | 3.6.6: metal and/or plastic; waste plastic | hidden | not visible |
| 27 | Gas pipe to the kitchen point | 3.6.7: "יש" | not drawn | hidden. d10 item 9 adds a balcony gas point (item 81) |
| 28 | Gas meter prep | 3.6.8: "יש" | none | outside the apartment |

## C. Table 5, electrical points, room by room (d08 page 18)

Crop: `d08_p18_table5_electrical.png`. Column headings as corrected in the table: "נקודת מאור קיר/תקרה" (light point),
"חיבור קיר רגיל" (regular socket, replaces "בית תקע מאור"), "חיבור קיר כוח" (power point, replaces "בית תקע מעגל
נפרד"), "בית תקע מוגן מעגל נפרד" (empty everywhere), "בית תקע עם דרגת הגנה IP44", TV, external phone, intercom,
other. The table has no switch column; switches are listed for completeness.

Model counts: a light point is any fixed ceiling or wall fitting (spot, downlight, pendant, fan light kit, wall
light); LED strips built into furniture are listed separately and not counted. Plates are from `outlets()`
(lines 1771 to 1838) and `plate()` (lines 1018, 1019, 1229, 1337, 1394). Coordinates are effective (after
`withShift`).

The general pattern: the model follows the electrical sheet, and the sheet has **more points than Table 5** in most
rooms (one extra phone point per bedroom, a corridor socket, a third corridor light). Table 5 is the minimum sold;
these extras are a table vs sheet conflict, not model errors. Light fittings beyond the sheet are the owners' design
(already recorded in recheck3 section 6).

| # | Room | Table 5 (written) | Model now | Surplus / missing vs Table 5 |
|---|---|---|---|---|
| 29 | Entry | light 1; intercom "1 T.V צג שחור לבן" | lights 3: cylinders (2.4, 3.9) and (2.4, 5.0) line 1033, picture-light bar x 2.92..4.16 z 5.43 h 2.02 line 986 (sheet: one point 1a at (2.10, 4.50)); intercom screen x 2.74..2.84, h 1.30..1.48, line 981; switch plate x 2.66 line 1018 | +2 lights (design). Intercom matches |
| 30 | Living | light 3, socket 3, TV 1, phone 2 | lights 9: spots (1.0, 1.0), (1.0, 2.0), (3.8, 0.9), (5.9, 0.9), (3.8, 2.6), (5.9, 2.6), (3.1, 1.6) line 1027; wave pendant line 1238; flush light (4.70, 2.20) line 1035; plus LED lines (media wall 1150, bulkhead slot 1161, ceiling grazer 1231). Sheet: 1b, 1c. Sockets visible 2: pier (FX, 3.89) h .40 line 1830, robot bay in the storage wall h .44 line 1229. TV and phone: none visible | +6 lights (design). Sockets, TV and phone: the sheet's TV-wall row (h=40), the h=130 socket and the dining socket and "ט" sit behind the media base, the TV and the storage wall (recheck3: HIDDEN). No change |
| 31 | Kitchen and dining | light 2, socket 1, power 3, phone 1; d10 adds an island socket and a 3-phase hob point | lights 6: spots (4.6, 4.2), (6.4, 4.2), (4.6, 6.2), (4.6, 7.6), (6.6, 7.9) lines 1027 to 1028, frames pendant line 1363 (sheet: 1d under it); LED: under-cabinet 1342, coffee bar 1290, island 1359. Socket 1: west splash (3.645, 8.13) h 1.10 line 1337. Power 3: behind the appliances, not drawn. Phone: the dining "ט" is behind the storage wall | +4 lights (design). **Island socket missing** (change 2). Hob point hidden |
| 32 | Corridor | light 2 | lights 3: cylinders at x -1.07, 1.03, 3.13 on `DROP`, line 1033. Socket x .65 h .40 line 1799. Panel x 3.33..3.78 lines 1801 to 1802, comms box line 1803, consumption display line 1804, double socket x 3.57 line 1805, fibre point x 3.99 line 1806. Switches x .18, 1.86, 3.18 (line 1018) and the bath group `kkk` at 2.66 (line 1810) | **Conflict Table 5 (2 lights) vs sheet (3 x "3c", 210 apart, crop `electrical_sheet_corridor_3c_x3.png`)**. Model follows the sheet; keep. Socket, double socket, fibre: on the sheet, not in the table; keep |
| 33 | Master (1) | light 1, socket 2, TV 1, phone 1, intercom "1 שמע בלבד" (audio only) | lights 7: fan light (6.73, -1.645) line 1391, spots (5.7, -1.9), (7.8, -1.9), (5.7, -0.8), (7.8, -0.8) line 1028, bedside globes (5.84, -0.38), (8.12, -0.38) line 1389. Sockets 3: `ds` 5.78, `ksd` 8.02 (h .60, line 1814), `std` 6.845 (h 1.80, line 1815); plus a 14 x 8 plate at (5.70, -3.095) h 1.0 below the TV, line 1394, not on the sheet. TV 1 (6.93). Low-voltage 3: x 5.74, 8.105, 7.015 | +6 lights (design). +1 socket vs the table (sheet), +1 unexplained plate (line 1394: remove, or keep as the owner's TV socket). Low-voltage: the sheet has "E" at the west bed head (h=60), "ט" at the east bed head and "ת" in the TV group. **Interpretation: "E" is the audio-only intercom** of Table 5 (it is on the blue comms layer, and the boxed "א" also appears in rooms that get no intercom). The model draws it as a data jack at x 5.74; a small intercom speaker unit would read better (optional) |
| 34 | Rooms (2) and (3) = model room 1 and room 2 | each: light 1, socket 2, TV 1, phone 1 | room 1: lights 3 (fan light (-2.51, -3.21) line 1593, spots (-2.5, -3.8), (-2.5, -2.2) line 1028); sockets 3, TV 1, phone 2 (lines 1786 to 1787). Room 2: lights 3 (fan line 1614, spots (.45, -3.8), (.45, -2.2)); sockets 3, TV 1, phone 2 (line 1789) | each room +2 lights (design), +1 socket and +1 phone vs the table (both on the sheet). Keep |
| 35 | Mamad (4) | light 1, socket 3, TV 1, phone 1, other "לפי דרישות הג"א" | lights 3 (fan line 1628, spots (-2.7, 1.4), (-1.1, 1.4)); sockets 4: `dst` .89 h 1.80, `sd` 2.33 h .40, `sk` 1.59 h .65 (line 1791), filter socket h 2.20 (line 1797); TV 1; phone 2 | +2 lights (design). The filter socket fits "לפי דרישות הג"א"; the other 3 match. +1 phone (sheet). Keep |
| 36 | Master bath | light 1 (protected), socket 1 (protected), other "1 עבור הכנה לתנור חימום" | lights 4: spots (5.3, -3.7), (6.4, -3.9) line 1029, spot (5.16, -4.27) line 1439, mirror-cabinet LED line 1453 (sheet: mirror wall light 2b). Socket x 4.72 h 1.10 line 1811. Heater box x 6.77..6.85, z -4.46..-4.08, h 1.90..2.10, line 1813. Switches in the closet, `kk` line 1810 | +3 ceiling lights (design). Socket and heater point match. The developer delivers only the heater prep (4.4 "אין", item 52): the drawn heater is the owner's |
| 37 | Family bath and service corner | light 1 (protected), socket 1 (protected), power 2, other heater prep 1 | lights: spot (3.01, -3.10) on `BC` line 1029, mirror-cabinet LED line 1549 (sheet: wall light 2e), niche spot (3.2, -4.65) line 1029 (not on the sheet); LED under the WC column (1504) and the laundry cabinet (1508). Socket (2.105, -1.395) h 1.10 line 1811. Power: washer and dryer sockets h 1.40 line 1812. Heater (2.45..2.85, south wall) line 1813. Niche: AC isolator line 1574, heater switch line 1575 | +1 wall light (sheet) and +1 niche light (design). Socket, power 2 and heater match (power 2 read as washer and dryer, interpretation) |
| 38 | Balcony | light 1 (protected), IP44 socket 1 (protected); d10 adds a regular socket and a TV point | lights 5: soffit lights (7.96, 2.14), (7.96, 5.73) line 1832 (sheet: two "1e"), wall lights on the facade at z 3.82 and 7.30, h 1.9..2.1, line 1838 (not on the sheet), fan light (9.30, 1.55) line 1707. IP44 box (FO, 3.84..3.94) h .34..46 line 1833 | +1 light vs the table (sheet has 2), +2 wall lights and the fan (design). **Socket and TV point missing** (change 1) |

Closet: no row in Table 5 (part of the master). Model: spot (7.63, -3.80) = sheet 2c (line 1029), wardrobe LED
line 1414, switch x 8.40 line 1018. No change.

Model fittings that need power but have no point in Table 5 or on the sheet: heated towel ladders (master bath line
1456, family bath line 1555), the furniture LED strips listed above, the robot bay. These are owner additions; a real
install needs a point for each (estimate). Report only.

## D. 3.7.1 to 3.7.10 (d08 page 18 and 19)

Crop: `d08_p18_3.7_notes.png`.

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 39 | Lobby light button | 3.7.1: "1 לחצן מתוך הדירה להדלקת אור בלובי קומתי", "יש" | no separate button. The sheet shows a double switch "1ad" and a box under it at the door; no push-button symbol | Optional, low: `plate('n', 5.50, 2.76, 1.10, .05, .05);   // lobby light push button (d08 3.7.1; position an estimate)` after line 1018 (clear of the switch plate 2.62..2.70 and the intercom from h 1.30) |
| 40 | Bell | 3.7.3: type "רגיל", ring "זמזם או גונג" | none. The sheet has a blue box with a circle "1" centred over the entry door (OPEN in recheck3) | Interpretation: that box is the chime. Optional, low: a small white box over the door head on the inside face, e.g. `B(2.03, 2.13, 5.488, 5.50, 2.24, 2.32, mat.whitePlate);   // chime (d08 3.7.3; height an estimate)` |
| 41 | External phone | 3.7.2: conduit only | phone points per the sheet | matches |
| 42 | Breakers | 3.7.4: per the developer, "גביס או שווה ערך" | inside the panel | not visible |
| 43 | Apartment panel | 3.7.5: "יש", "בקיר הפרדה או במבואה או אחר" per the architect and electrical consultant | on the TV wall (a partition), corridor face, x 3.33..3.78, h 1.45..2.05, lines 1801 to 1802 | matches the location type. Height is an estimate (not written anywhere) |
| 44 | Water heater point | 3.7.6: "כן" | IP65 switch in the niche, line 1575. The sheet also shows switch "4" with a clock symbol by the family bath door (interpretation: a timer switch for the heater), which falls inside the `kkk` group at x 2.66 (line 1810) | matches |
| 45 | Supply size | 3.7.7: 3-phase, "3x25" A | not visible | none |
| 46 | Intercom system | 3.7.8: "כן", "בכניסה לדירה ובכניסה לבנין + צג שחור לבן" | entry screen line 981 | matches inside the apartment. The building entrance unit is outside the model |
| 47 | CCTV | 3.7.9: "לא" | none | matches |
| 48 | Other installations | 3.7.10: "אין" | n/a | replaced by d10 item 10 (items 31, 38, 79) |

## E. 4, cooling and heating (d08 page 19)

Crop: `d08_p19_ac_heating.png`.

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 49 | Central AC | 4.1: "יש" struck, "אין" and "הכנה בלבד" kept: "הכנות בלבד כוללות: צנרת חשמל, צנרת ניקוז מים, צנרת גז). 1 נק' הכנה למזגן" | full mini-central: unit over the family bath (`BC` line 928, hatch line 1498), corridor drop (`DROP` line 927, ceiling line 929), return grille line 933, living grilles lines 1157 to 1159, room grilles lines 936 to 938, mamad sleeves lines 940 to 946, condenser line 1563 | d08 alone gives only a prep point. **Overridden by d10 item 11**, which supplies the system (item 83). Model matches d10 and the AC sheet |
| 50 | Split AC | 4.2: whole line struck ("אין") | master split over the door, line 1808 | Overridden by d10 item 11 (12,000 BTU split for the master). Matches |
| 51 | Gas or oil heater | 4.3: "אין" | none | matches |
| 52 | Electric heater | 4.4: "אין" ("הכנות בלבד" struck) | heater boxes drawn in both baths, line 1813 | Table 5 still gives a heater prep point in each bath. The drawn heaters are the owner's appliances on those points. Note only |
| 53 | Radiators, convectors | 4.5, 4.6: "אין" | none (towel ladders are owner fittings, see C) | matches |
| 54 | Underfloor heating | 4.7: "אין" | none | matches |
| 55 | Other | 4.8: "אין" | n/a | none |

## F. AC details from d10 item 11 against the model

| # | Item | Written (d10 item 11) | Model | Change |
|---|---|---|---|---|
| 56 | Balcony socket and TV | see item 79 | missing | change 1 |
| 57 | Mini-central | "מיני מרכזי אינוורטר תפוקה BTU 52,000", serving "מטבח, חדר מגורים, פינת אוכל, חדר מס' (2), חדר מס' (3), ממ"ד (4)" | unit over the family bath; living grilles 2.20 and 5.90 (blowing over living, dining and kitchen), room 1 and 2 grilles, mamad sleeves | matches (the AC sheet writes the same 52,000) |
| 58 | Corridor duct | "תעלה שרשורית להולכת אויר כולל הנמכת גבס" | gypsum drop at `DROP` over the corridor and passage, lines 929 to 930 | matches |
| 59 | Master split | "מזגן מפוצל עילי בתפוקה של BTU 12,000" | split body x 4.26..4.46, z -1.14..-0.30, h 2.24..2.52, line 1808; comment line 1807 says 12,300 (AC sheet) | Small conflict d10 (12,000) vs AC sheet (12,300). Size is not visible. Update the comment to cite both |
| 60 | Split electrical point and piping | "הכנת צנרת לנקודת מיזוג מפוצל אחת כולל נקודת חשמל במעבר או במיקום אחר" | no plate for the split; its condenser is not modelled | The electrical point is the sheet's "16" at (4.365, -0.179) (recheck3), hidden above the door; no change. **Condenser**: d10 supplies the split, so its outdoor unit exists; the AC sheet draws it as an 84 x 40 box over the main unit. Proposed (change 4), inside the `withShift(.22, -.45)` block after line 1572: `B(2.61, 3.46, -4.55, -4.15, 1.05, 1.65, M('#e9e8e4', .6), { round: .01 });   // master split condenser 84 x 40 (AC plan outline, d10 item 11); bracket height an estimate`. Effective x 2.83..3.68, z -5.00..-4.60: clear of the heater (x from 3.77) and the riser. **Clash**: the main unit's refrigerant pair at line 1568 (x 2.85 and 2.92, z -4.30, rising from .98) would pass through it. Move that pair to x 2.20 and 2.27 and add a second pair for the split from 1.65 to 2.35 at x 3.30 and 3.37. Laundry on the lines at h 2.0 (line 1570) would then hang just above the unit (practical note) |

## G. 5, fire safety (d08 page 19) and 7.2 (page 20)

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 61 | Sprinklers in the apartment | 5.1: "אין" | none | matches |
| 62 | Smoke detectors | 5.2: "אין"; 7.2.4: "אין" | none | matches |
| 63 | Sprinklers in the basement | 7.2.3: "יש", "במרתף" | outside the model | none. The sheet's "FS" circle in the core (recheck3) fits a flow switch |
| 64 | Stair pressurisation, smoke extraction | 7.2.1, 7.2.2: "אין" | n/a | none |

## H. 6 to 9, site, shared systems, shared property (d08 pages 19 to 21)

Nothing here is inside the apartment. The model's surroundings come from the balcony photos (estimates).

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 65 | Parking | 6.1: shared for both buildings; no parking outside the plot; basement parking with "1" level; also "בקומת הקרקע"; disabled parking at ground level; finish "אבנים משתלבות"; access from the road | street parking and bays from the photos; no basement | Outside the model. No change |
| 66 | Paths, terrace, paved areas | 6.2.1 to 6.2.3: concrete, granolith, asphalt or pavers | red and grey pavers outside (lines around 1879 to 1905) | consistent; no change |
| 67 | Gardens | 6.2.4 shared garden "יש"; 6.2.5 irrigation "אין"; 6.2.6 to 6.2.8 private garden "אין" | lawns and trees around the building | consistent |
| 68 | Plot fence | 6.2.9: concrete, stone-clad masonry, metal or mixed; height per the site plan | retaining wall and driveway to the south (exterior block) | not checkable without the site plan; no change |
| 69 | Pilotis floor | 6.2.10 paving "אבנים משתלבות"; 9.1.2: "קומה מפולשת: יש (חלקית)", "1 חלקית - קומת הכניסה (מסד)" | floors 0 and 1 under the apartment are a solid shell with our windows repeated, line 1866 (estimate, "same plan assumed") | Possible conflict if the partial pilotis is under our unit. Check against d03 (ground floor plan, another agent). No change from this document alone |
| 70 | Central gas | 7.1.1 central tank or cylinders; 7.1.2, 7.1.3 piping to and inside the apartment "יש"; annex B page 25 note 16 | balcony gas valve line 1834 | consistent |
| 71 | Mailboxes, AC, other shared | 7.4 central AC "אין" (building level); 7.5 one mailbox per apartment at the building entrance (standard 816); 9.1.4 to 9.1.7 lobbies, stairs, one lift | core masses only (lines 897 to 898) | outside the model |
| 72 | Roof | 9.1.8, 9.1.11: collectors, water heaters, antenna, generator, lift machinery, water tank, pumps, AC units; about 30 sqm attached to the top floor | our roof is not modelled | Our solar collectors (item 22) would sit there. No change |

## I. Mamad equipment and ventilation

| # | Item | Written | Model | Change |
|---|---|---|---|---|
| 73 | Mamad points | Table 5 "לפי דרישות הג"א" | 4 sockets incl. the filter socket h 2.20 (item 35) | matches |
| 74 | Filtration unit | annex B page 30 note 69: maintenance rules "במידה והותקנה מערכת סינון דירתית" (if installed) | filter unit on the west wall, lines 1793 to 1796, sleeves line 1796 (from the AC sheet, which writes the model) | d08 does not promise the unit; the AC sheet draws it. Keep |
| 75 | Mamad door and window | page 15 (cross-reference, not in my pages): door "70/200", steel blast door opening out; window "100/100" | blast leaf .86 wide, line 992; window 1.00 x 1.00 (sill 1.10, head 2.10), line 1671 | Window matches. **Door width conflict** (written 70 vs model 86; recheck3 also scaled about 70 on the sheet). For the doors and windows agent |
| 76 | Ventilation | page 15 note: forced ventilation only for a guest WC "(ככל וקיים)"; annex B page 29 note 56: a bath fan, if installed, runs with the light | no guest WC; both baths have windows; kitchen hood intake line 1343 | matches; no change |

## J. d10, the addendum (every item)

Crop of items 7 to 11: `d10_p2_items7-11.png`. Items 1 to 3 are on page 1, which also holds personal data, so they
are quoted only in short.

| # | d10 item | Written | Model | Change |
|---|---|---|---|---|
| 77 | 1, kitchen cladding | "חיפוי שיש בגובה כ-50 ס"מ מעל משטח ארון תחתון בלבד, למעט אזור חלון" (stone, about 50 cm, lower counter only, not at the window), up to a length cap | splash `.92` to `1.62` (70 cm) on the south and west walls, line 1344; default ceramic "וראנו לבן" from the studio (`CER_SPACES` kitB, line 3029), with the stone option labelled "לא מהמפרט" | **Conflict d10 (stone, 50 cm) vs the studio ceramic list (d07, `CERAMICS.md`)**. The model's stone option is the contract item: change the label (change 5). Height 70 vs 50: the owner decides; the strip from 1.42 to 1.62 would otherwise be paint. No window splash exists in the model (window C is on the east wall), so that part matches |
| 78 | 1, cap | a maximum length is written | about 5.0 m of splash (south 3.63 m, west 1.17 m) | within the cap (estimate from the model) |
| 79 | 10, electrical | kitchen: "הכנה לכיריים תלת פאזי. מיקום: מתחת למיקום כיריים"; "תוספת שקע רגיל עבור אי במטבח"; balcony: "תוספת שקע רגיל + נק' T.V" | hob point: hidden; island: no socket; balcony: IP44 only | add the island socket (change 2) and the balcony socket and TV point (change 1) |
| 80 | 3, bath cabinets | master bath "יש - 1" and family bath "יש - 1": "ארון אמבטיה קומפלט (משטח חרס כולל כיור)", size "עפ"י תכנית חברה", model per the supplier's display | master: 70 cm walnut cabinet, travertine top, vessel basin (lines 1448 to 1450); family: 100 cm painted shaker vanity, quartz top, semi-recessed basin (lines 1538 to 1542) | Cabinets are design. Tops conflict with "משטח חרס כולל כיור": change 3. Sizes still open (`CERAMICS.md`: studio 80 family, 100 master; model the reverse) |
| 81 | 7, 8, 9, water and gas | 7: "נק' מים עבור תמי 4"; 8: "נק' מים לברז גן (מים קרים בלבד) במרפסת שמש, ללא נק' ניקוז נוספת"; 9: "הכנה לנקודת גז במרפסת שמש (לא כולל חיבור מונים)" | Tami4 on the coffee-bar tray, line 1294 (water point hidden; location an estimate); garden tap line 1835; gas valve line 1834 | all three match. The garden tap now has a written basis that overrides d08 3.6.4 (item 24). The plumbing sheet's balcony drains (line 1836) stay: "ללא נק' ניקוז נוספת" means no extra drain beyond those |
| 82 | 6, insect screens | windows of living, kitchen, master, master bath, bedrooms (2) and (3), mamad: "יהיה כולל רשת" | none | Not modelled. Optional, low: a screen leaf in the living sliders' track and a screen cassette on the single-sash windows. The type is not written (estimate). The family bath window to the niche is not on the list |
| 83 | 11, AC | see section F | | items 57 to 60 |
| 84 | 11, master split supplied | see 59, 60 | | change 4 |
| 85 | 4, entry door | "דגם 'גרדה' צבועה כולל ידית ניקל" | dark grey steel leaf (`mat.entryDoor`, line 525) with a steel lever, lines 979 to 980 | colour not written; nickel lever reads as the steel one. Matches |
| 86 | 5, interior doors | bedroom (1), master bath, bedrooms (2) and (3), family bath: "אקווה ביאנקו בצבע לבן" | `mat.door` '#f2f0eb', plain leaves, lines 987 to 993 | white matches. Leaf pattern not known; no change |
| 87 | 2, bath wall tiles | "חיפוי קירות עד גובה תקרה או עד תחתית הנמכה" | master bath tiles 0 to `H` (lines 1419 to 1423); family bath tiles 0 to `H`, above its `BC` ceiling (lines 1460 to 1465) | matches |
| 88 | 12, floor tiles | 80/80 "כולל אפשרות לריצוף בגימור מבריק"; and "כולל אפשרות לריצוף דמוי פרקט" per the studio spec | floor picker offers 80 x 80 pages (`CER_SPACES` floor, line 3019); bedrooms keep oak planks labelled "לא מהמפרט" (line 3021) | 80 x 80 matches. A parquet-look porcelain is now a contract option, so the rooms label may change once the d07 agent names the item. **Mamad**: annex B page 25 forbids parquet or other flammable flooring there; the planks (line 873) must be read as porcelain or the mamad given tile (change 6) |
| 89 | 13 | agreed total of the upgrade | n/a | not reported (price) |

## K. d09, annex C (credit and charge tables)

d09 lists change options with unit prices. Prices are not reported. Nothing in it adds or removes an item from the
model; it confirms the base spec in places.

| # | Item | Written | Model | Note |
|---|---|---|---|---|
| 90 | Base floor tile | "ריצוף קרמיקה (פורצלן) במידות כ-60/60" for living, kitchen, corridor and rooms | 80 x 80 default per d10 item 12 | d10 replaces it with 80/80 (item 88). Consistent |
| 91 | Skirting | "שיפולים (פנלים) דוגמת הריצוף, עד גובה 7 ס"מ" | `SK = .08`, line 951, white (not tile pattern) | 1 cm and the material differ. For the finishes agent; low |
| 92 | Kitchen and bath cabinets | lower, island or half island, upper, built-in; bath cabinets with or without "כיור אינטגרלי" for both baths | owner's kitchen; vanities as item 84 | The "integral basin" rows support change 3 |
| 93 | Sanitary quantities | kitchen sink 1, basins 2, small hand basins 2, toilets with cistern and seat 2, bath 1; mixers: kitchen 1, basin 1, small basin 1, bath 1, shower 1 | 1 sink, 2 basins, 2 WCs, 1 tub, no hand basin | d09 is internally inconsistent (2 basins but 1 basin mixer; 2 hand basins although Table 4 and 3.6.3 give none). Generic table; no change |
| 94 | Electrical options | light point, socket, double-switch light point, cable TV point, separate-circuit socket (also protected), IP44 socket, external phone, intercom point, power point, "נקודת כח (פקט)": each as credit, move or add | n/a | options only. Refers back to the notes after Table 5 |

## L. Conflicts found (not resolved here)

| # | Between | Subject | Model follows |
|---|---|---|---|
| 95 | d08 Table 4 vs plumbing sheet | cisterns: concealed vs high/low | d08 (concealed) |
| 96 | d08 Table 4 vs plumbing sheet vs construction plan | master shower 80/80 vs 106 x 92 vs 110 x 96 | plumbing sheet |
| 97 | d08 Table 4 vs plumbing sheet and studio pick | fixed head in the master shower | plumbing sheet and studio |
| 98 | d08 Table 4 vs electrical sheet | dryer prep "אין" vs a dryer socket | electrical sheet |
| 99 | d08 3.6.4 vs plumbing sheet vs d10 item 8 | garden tap | d10 (addendum prevails) |
| 100 | d08 Table 5 vs electrical sheet | corridor lights 2 vs 3; one phone per bedroom vs two; corridor socket | electrical sheet |
| 101 | d08 Table 4 vs studio choice | kitchen sink acrylic white 40/60 vs stainless 70 x 45 | owner choice |
| 102 | d10 item 1 vs d07 studio list | kitchen splash stone 50 cm vs ceramic tiles | ceramic by default, 70 cm |
| 103 | d10 item 11 vs AC sheet | split 12,000 vs 12,300 BTU | n/a (not visible) |
| 104 | d08 page 15 vs model | mamad door 70 vs 86 | model (for the doors agent) |
| 105 | d08 annex B page 25 vs model | no parquet in the mamad vs plank look | open (change 6) |
| 106 | d08 9.1.2 vs model exterior | partial pilotis on the entrance floor vs a solid shell under the unit | open (check d03) |

None of these documents conflicts with the 2025 sales plan on a position: Table 4 and Table 5 give counts and types,
not positions.

## M. Items that cannot be shown in a 3D model

Listed so nothing is skipped silently: pipe materials (3.6.6); hot water to each fixture (3.6.3); forced solar system
with heat exchangers (3.6.2); water and gas meters (3.6.5, 3.6.8); gas piping in the apartment (3.6.7, 7.1.2,
7.1.3); kitchen cooking gas point and the 3-phase hob point (hidden under the counter); breakers (3.7.4); supply
3x25 A (3.7.7); external phone conduit (3.7.2); the building-entrance intercom (3.7.8); protected ("מוגן")
circuits and IP ratings beyond the boxes drawn; the split's electrical point "16" and its condensate route (hidden);
the AC unit capacity and brand; connections to water, sewer, power, phone and communications networks (8.1 to 8.5);
refuse removal (8.7); shared-property shares and rules (9.1 to 9.4); d09 prices; d10 parties, signatures and price.
