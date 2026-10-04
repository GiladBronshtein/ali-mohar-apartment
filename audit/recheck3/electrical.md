# Electrical re-check 3: vector electrical plan vs model

Source: `materials/plans/vector/electrical.pdf` (HADA electrical and lighting plan, AutoCAD vector, one A2 sheet).
Model: `source/salon.html` as of 2026-10-04 evening. salon.html was being edited while this audit ran; line numbers
below were re-grepped just before writing, and every change quotes the exact current string so it can be found even
if lines drift.

Crops: `el_crops/` (JPG). Coordinates: model metres, x east, z south, origin at the living face of the TV wall (z 0)
and the storage wall west face (x 0). Ceiling 2.60 and all heights not written on the sheet are **estimates**.

## 1. Method and calibration

| Item | Value |
|---|---|
| Sheet | 420 x 594 mm (A2). Title block says A3, 1:75: a template field not updated. The drawing itself measures 1:50 against written dims and wall faces |
| Raster used | 400 dpi, 314.96 px per metre (20.0 mm per metre = 1:50) |
| Mapping | x = (px - 3842.2) / 314.96, z = (py - 2612.0) / 314.96 |
| Reading | symbols extracted from the PDF vector paths by layer (pypdf); positions are path centres; written red dims (layer E2) read visually |
| Anchoring | each symbol measured from the nearest local wall face, then put on the model's face. Written dims win over scaling |
| Threshold | scaled differences under about 5 cm are not proposed |

Layers (no legend on the sheet, meanings by drafting convention and by the symbols themselves):

| Layer | Content |
|---|---|
| A_EL_INT3 | switches (circle on a stem, numbered by circuit), ceiling and wall light points (crossed circles) |
| A_EL_INT4 | sockets, TV outlets |
| A_EL_INT5 | boxed "א" marks, "FS" circle |
| A_EL_INT6 | blue data and comms: ת (phone), ט (TV/comms), FO (fibre), E, VE, crossed box |
| A_EL_INT7 | cone symbols and an "S" box: most likely alarm prep (PIR detectors and siren or panel). Not written |
| A_EL_INT1 | special points: "9" 3-phase point, niche isolator, "16" point |
| A_EL_INT8, INT8_BARAK | lightning conductor and earthing |
| A_EL_INT11_KARKA, PETAH_TIK, A_EL_DIM_ARONOT | lobby riser cabinets (outside the apartment) |
| E2 | red dimensions and notes |

Crop: `00_overview.jpg`.

## 2. Legend, title block and notes

**There is no legend on the sheet.** Symbol meanings above are inferred.

Title block (`01_title_block.jpg`), translated:

| Field | Text |
|---|---|
| Office | HADA |
| Project | Ali Mohar project 6-8, Raanana |
| Date | 9/2/2006 |
| Revision | 0 |
| Status | For construction (ticked); for approval, for review (not ticked) |
| Drawing name | Electrical plan |
| Sheet no. / size / scale | 2 / A3 / 1:75 (see calibration: the PDF is A2 at 1:50) |
| Unit | Building A, floor 2, apartment no. 4 |
| Distribution | table of consultants and trades with date and revision columns (blank) |

Notes on the plan, translated:

| Where | Note | Crop |
|---|---|---|
| Kitchen | Kitchen electrics per the kitchen company's plan | `60_kitchen_entry.jpg` |
| Corridor panel leader | Apartment panel, communications box below it; digital display for electricity consumption data | `22_panel_display_x2_fo.jpg` |
| Niche | "9 3x16A IP65" (isolator for the AC condenser); "4 IP65" (switch for the water heater) | `31_niche_isolator_boiler.jpg` |
| Family bath | "9": 3-phase point for the mini-central AC unit above the bath ceiling | `30_family_bath_9_3phase.jpg` |
| Mamad | thermal insulation per the thermal report, detail 82, option 3; acoustic detail 4 | `12_mamad.jpg` |
| Building corners (two) | "Fe-12ø: rises to the air-termination ring on the roof and connects to the lightning bonding rings on each floor" | `81_ne_lightning_note.jpg`, `86_nw_note.jpg`, `83_sw_note.jpg` |
| SW corner | "2 x ø32 (25 mm² Cu): TV antenna earthing, from the earth electrode to the upper roof" | `84_sw_antenna_earth_note.jpg` |
| Entry | "25ø": conduit from VE to the lobby riser | `60_kitchen_entry.jpg` |
| Living, TV wall | "50ø": conduit joining the h=130 socket and the crossed box behind the TV | `50_living.jpg` |

## 3. Wall faces: sheet vs model

| Face | Sheet | Model | Delta | Note |
|---|---|---|---|---|
| Most room faces | | | 1 to 4 cm | calibration holds |
| Mamad interior | 3.63 x 2.71 | 3.55 x 2.62 | 8 / 9 cm | items anchored to the nearest face |
| TV wall, corridor face | -0.199 | -0.19 | 1 cm | |
| TV wall, west end (passage jamb) | 3.002 | 2.97 | 3 cm | geometry P4b proposes 3.00 |
| Master south face (x 4.78..7.39) | -0.099 | -0.145 | 4.6 cm | geometry domain |
| Master east face | 8.966 | 8.91 | 5.6 cm | geometry domain |
| Master north face | -3.109 | -3.105 | 0 | |
| Closet opening | 7.57..8.37 | 7.54..8.32 | 3 to 5 cm | |
| Entry opening | 1.58..2.64 | 1.585..2.555 | 8.5 cm at the east jamb | geometry domain |
| Kitchen entry wall | x 3.58..4.33, z 5.544..5.645 | 3.63..4.30, 5.50..5.61 | 3 to 5 cm | geometry P5 proposes the end at 4.33 |
| Living pier | 3.49..4.29 | 3.45..4.26 | 3 to 4 cm | geometry P2a proposes 3.49..4.29 |

## 4. Room by room

Verdicts: OK (within about 5 cm or at a written dim), PROPOSE (see section 7), DESIGN (owner or designer choice,
report only), HIDDEN (behind furniture, no visible effect), OPEN (meaning unclear).

### Room 1 (`10_room1.jpg`)

| Symbol | Sheet (x, z) | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 3a | (-2.53, -3.21) | | fan at (-2.51, -3.21) | 2 cm | OK |
| Socket + ת, west wall | s z -4.61, ת z -4.39; written 41 from the north face | h=40 | `sd` centre -4.625 (s -4.67) | 4 cm at the written 41 | OK |
| TV group (ת, socket, TV) | z -3.64 / -3.42 / -3.22, centre -3.43; written 129 | h=180 | `dst` centre -3.38 | 5 cm | OK |
| Bed-head socket + switch 3b, north wall | s x -2.35, switch x -2.12 | h=65 | `sk` centre -2.22 | 1 cm | OK |
| Door switch 3b | x -2.12 at the jamb | not written | plate x -2.18 (h 1.10 estimate) | 6 cm, set by the door frame | OK |
| Shutter switch 3m | z -1.78 | not written | `r` z -1.80 | 2 cm | OK |
| Boxed א, "25" | (-2.53, -2.26) | | none | | OPEN |

### Room 2 (`11_room2.jpg`)

| Symbol | Sheet (x, z) | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 2d | (0.455, -3.205) | | fan at (0.45, -3.20) | 0 | OK |
| Socket + ת, east wall | centre z -4.53; written 46 | h=40 | `sd` centre -4.55 | 2 cm | OK |
| TV group | z -3.20 / -2.98 / -2.78; written 173 | h=180 | `dst` centre -2.86 (t -2.775) | t 0 | OK |
| Bed-head switch, socket, shutter switch 2n | x -0.01 / 0.22 / 0.46 (drawn spread) | h=65 | `ksr` centre 0.02 | schematic spread | OK, keep: the group must clear the window jamb |
| Door switch 2d | x 0.83..0.90 | not written | plate x 0.80 | 3 cm | OK |
| Boxed א, "25" | (0.33, -2.37) | | none | | OPEN |

### Mamad (`12_mamad.jpg`, `13_mamad_west_wall.jpg`, `14_mamad_written_120.jpg`, `93_glyph_120_mamad.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling point | room centre | | fan at (-1.97, 1.40) | under 5 cm | OK |
| Socket + switch by the blast window | written 120 from the south face to the socket | h=65 | `sk` centre 1.66, socket at 1.6175 = 113 from the south face 2.745 | 7 cm, written | PROPOSE 1 |
| Socket + ת, east wall | scaled from the south face | h=40 | `sd` centre 2.235 | 9.5 cm | PROPOSE 4 |
| TV group, east wall | scaled | h=180 | `dst` centre 0.80 | 9 cm from the north face, 3 cm from the south face (room 8 cm shorter in the model) | PROPOSE 7 (low) |
| Filter socket | | h=220 | `s` h 2.20 | | OK |
| Door switch | | not written | plate x -1.10 | | OK |
| "25" | | | | it is an AC sleeve dimension (MIZ-P), not electrical | no action |
| Boxed א | | h shown | none | | OPEN |

### Corridor and panel (`20_corridor_west.jpg`, `21_corridor_east_switch_3c.jpg`, `22_panel_display_x2_fo.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling points 3c | on the corridor axis | | cylinders at DROP | under 5 cm | OK |
| West switch | | | plate `['n', -.145, 0.18]` | | OK |
| Switch group to master side | | | `kkk` at 2.66 | | OK |
| Socket | scaled | h=40 | `s` x .72 | 7 cm | PROPOSE 5 |
| East switch 3c | circle (3.227, -0.304), stem meets the -0.199 face at x 3.17 | not written | plate x 3.02 | 15 cm | PROPOSE 2 (also clears the passage jamb if geometry P4b moves it to 3.00) |
| Panel | x 3.378..3.778 | not written | x 3.33..3.78 | 2 to 5 cm | OK |
| Comms box | under the panel | not written | x 3.35..3.73, h .35..0.85 | | OK |
| Consumption display | east of the panel, about x 3.86 | not written | x 3.14..3.26 (west of the panel) | 66 cm, wrong side | PROPOSE 3 |
| Double socket "x2" | x 3.55..3.59, between box and panel | not written | none | missing | PROPOSE 8 (low) |
| FO fibre point (blue) | x 3.99 | not written | none | missing | PROPOSE 9 (low) |
| "16" point (INT1) | (4.365, -0.179), SW corner of the master vestibule | not written | none | | Likely the 16 A feed for the master split; matches plumbing_ac.md A8 (split over the master door at x 4.26..4.46, z -1.14..-0.30). Apply only with that change |

### Family bath (`30_family_bath_9_3phase.jpg`, `90_glyph_9.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 2f, wall light 2e | | | spot (3.01, -3.10) and wall light | under 5 cm | OK |
| Splash-proof socket | on the pipe box | h=110 | `outlets('n', -1.605, 2.105, 1.10, 's')` | | OK. If plumbing_ac.md change 1 moves the box face, the socket follows it |
| Heater 12 | | h=200 | x 2.45..2.85 | limited by the door frame | OK |
| Washer and dryer sockets | z -3.55 and -3.29 | h=140 | z -3.61 and -3.34 | 5 to 6 cm | PROPOSE 12 (optional) |
| "9" | above the bath | | none | | RESOLVED: 3-phase point for the mini-central over the bath ceiling (hidden in the drop). No change |

### Laundry niche (`31_niche_isolator_boiler.jpg`, `91_glyph_65.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Isolator "9 3x16A IP65" | west wall, dot at x 2.21, z -4.876 | not written | none | missing | PROPOSE 10 (low) |
| Water heater | circle at (4.04, -4.70) | | (4.04, -4.69) after the shift | 1 cm | OK |
| Heater switch "4 IP65" | east wall, (4.28, -4.84) | not written | none | missing | PROPOSE 11 (low) |
| Ceiling point | none on the sheet | | spot (3.2, -4.65) | extra | report only |

### Master bath (`32_master_bath.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Mirror wall light 2b | written 42.5 from the south face, z -3.685 | | mirror cabinet centre z -3.71 | 2.5 cm | OK |
| Splash-proof socket | x 4.753 | h=110 | x 4.72 | 3 cm | OK |
| Heater 13 | centre z -4.25 | h=200 | z -4.27 | 2 cm | OK |
| Ceiling point | none on the sheet | | three downlights | extra | report only |

### Closet

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Switches 2b, 13 | z -4.135 / -4.156 | | `kk` -4.2425 / -4.1575 | door frame limited | OK |
| Ceiling 2c | written 120 / 128: (7.63, -3.795) | | spot (7.63, -3.80) | 0 | OK |
| Switch 2c | 8.7 cm from the jamb: x 8.41 | | plate x 8.40 | 1 cm | OK |

### Master bedroom (`40_master_bedroom.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 2a | written 150 / 218: (6.73, -1.645) | | fan at (6.73, -1.645) | 0 | OK |
| Bed heads | written 89 from the east face, 220 between: sockets at 8.02 and 5.82 | h=60 | `ksd` s 8.02, `ds` s 5.8225 | 0 | OK |
| Blue E by the west bed head | x 5.651 | h=60 | `d` of `ds` at 5.74 | drawn beside the socket | OK |
| TV group s / TV / ת | x 6.71 / 6.95 / 7.18 | h=180 | `std` s 6.845, t 6.93, d 7.015 | 2 cm on the centre | OK |
| TV screen | | | screen x 5.13..6.29, toward the door | the point is bare | DESIGN (owner choice) |
| Door switch 2a | (4.43, -1.15) | | plate 4.42 | 1 cm | OK |
| Shutter switch 2m | z -2.484 | | `r` z -2.45 | 3.4 cm | OK |
| Shutter motor | (9.17, -2.15) | | shutter on the window | | OK |
| Boxed א | (5.72, -0.775) | h=60 | none | | OPEN |
| Blue line on the east facade | | | | INT8_BARAK lightning conductor, outside | no action |

### Living (`50_living.jpg`, `51_living_1c.jpg`, `52_glyph_1c.jpg`, `92_int7_cones_pir.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 1c | written 127 / 147: (1.27, 1.305) | | wave pendant canopy x 1.20, z 1.17..2.41 | point lies under the canopy | OK |
| Ceiling 1b | written 200 / 230: (4.98, 2.00) | | flush light (4.70, 2.20) | 34 cm | DESIGN |
| Switch 1bc | z 3.024 | | plate z 3.0 | 2 cm | OK |
| Dining ט and socket "1" | x 0 face, z 0.668 / 0.914 | h=40 | none | | HIDDEN behind the storage wall |
| TV wall low row S, FO, ת, socket x2, TV, crossed box | written 185 from FX: model x 4.68 / 5.00 / 5.29 / 5.60 / 5.78 / 6.08 | h=40 | none | | HIDDEN behind the media base |
| TV wall socket + crossed box, 50ø conduit | x 5.82 / 6.07 | h=130 | none | | HIDDEN behind the TV |
| Cones (INT7) | (1.66, 3.35), (3.16, 0.19), (7.17, 0.21), (7.06, 3.40) | | none | | OPEN: likely alarm PIR prep |
| "S" box (INT7) | x 4.73 near z 0 | | none | | OPEN: alarm siren or panel (plumbing_ac.md A16 reads it as an AC controller) |

### Entry (`60_kitchen_entry.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Ceiling 1a | written 65 / 100: (2.10, 4.50) | | cylinders (2.4, 3.9) and (2.4, 5.0) | | DESIGN |
| Switch 1ad on the door unit box | circle x 2.793, box 2.644..2.894 at the jamb 2.64; 15.3 cm from the jamb | | plate x 2.66, 10.5 cm from the model jamb 2.555 | 4.8 cm | OK |
| Intercom (VE) | x 3.108, 46.8 cm from the jamb (model 3.02) | | intercom x 2.74..2.84 | 23 cm | DESIGN: the art at x 2.86..3.26 blocks it |
| Blue box with circle "1" | x 2.08, centred on the door, not at the latch | | none | | OPEN: an electric strike is unlikely; probably the door chime on circuit 1 |
| Lobby riser cabinets, "1050" | outside the door | | | | out of scope |

### Kitchen

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Switch 1d | (4.173, 5.473), 15.7 cm from the wall end 4.33 | | plate x 4.11, 19 cm from the end 4.30 | 3 cm relative | OK (see coordination, geometry P5) |
| Ceiling 1d | written 140 / 228: (5.88, 6.51) | | frames pendant canopy x 5.83..5.91, z 5.66..6.96 | under the canopy | OK |
| Kitchen sockets | "per the kitchen company" | | see kitchen.md | | n/a |
| FS circle | core at (3.17, 8.02) | | | probably a sprinkler flow switch, outside the apartment | out of scope |
| Everything south of z 9.11 | | | | neighbouring unit and lobby | out of scope |

### Facade and balcony (`70_balcony_facade.jpg`)

| Symbol | Sheet | Height | Model | Delta | Verdict |
|---|---|---|---|---|---|
| Balcony lights 1e | (7.985, 2.139), (7.985, 5.729); from the FO face 7.73 on the sheet | | (8.05, 2.2), (8.05, 5.7) | 6 to 9 cm | PROPOSE 6 |
| Pier switches k / r / r | z 3.646 / 3.870 / 4.122 (drawn spread) | | `krr` 3.765 / 3.85 / 3.935 | schematic | OK |
| Pier socket, room side | arc drawn into the room at (6.63, 3.94); pier-relative 3.90 | h=40 | z 3.85 | 5 cm | PROPOSE 13 (optional) |
| Balcony socket | (7.834, 3.934); pier-relative 3.91 | | z 3.80..3.90 (centre 3.85) | 6 cm | PROPOSE 13 (optional) |
| Switch 1p | z 7.172 | | `r` z 7.20 | 3 cm | OK |
| Shutter motors | 1m at the south end of door A (z 3.32); 1n at the north end of door B (z 4.48); 1p at the south end of door B (7.51, 6.83) | | shutters on doors A, B and window C | | OPEN: window C is drawn as a casement with no motor |

## 5. Recheck2 open electrical items

| Item | Result |
|---|---|
| Boxed "א 25" in rooms 1, 2, master and mamad | Still OPEN. One per bedroom, on INT5 with the "FS" circle. Candidates: AC room thermostat or sensor point, a circuit number, or a sprinkler or detector point. The mamad "25" is an AC sleeve dim, not part of the mark |
| Switch 3c by the panel | RESOLVED: x 3.17 (stem meets the wall face). PROPOSE 2 |
| Socket "x2" and blue FO by the panel | RESOLVED: x2 at x 3.55..3.59 between the comms box and the panel; FO at x 3.99. PROPOSE 8, 9 (heights not written) |
| "9" by the family basin | RESOLVED: 3-phase point for the mini-central above the bath ceiling. Hidden, no change |
| Niche isolator 3x16A IP65 | RESOLVED: west niche wall, z -4.876. PROPOSE 10. The heater switch "4 IP65" on the east wall is new: PROPOSE 11 |
| Ceiling points 1a and 1b vs the owners' lamps | Confirmed with written dims: 1a (2.10, 4.50), 1b (4.98, 2.00). DESIGN, no change |
| Blue box at the entry "latch" | It is centred on the door, not at the latch, labelled circle "1". Probably the chime. Still OPEN |
| Recheck2 balcony lights (7.93, 2.05) / (7.93, 5.79), from photos | Superseded by the vector reading (7.96, 2.14) / (7.96, 5.73). PROPOSE 6 |
| Recheck2 1p switch 7.20 to 7.10 | Not needed: the vector sheet gives 7.172. Keep 7.20 |
| Recheck2 proposal 16, hidden dining and TV-wall outlets | Positions now read (section 4, living), all hidden behind furniture. No change |

## 6. Model lights not on the sheet

The sheet has one ceiling point per room (two in the living area, 1b and 1c). These model lights have no point on
the plan; they are design estimates, not errors. Report only, no change proposed.

| Space | Extra model lights |
|---|---|
| Living | 12 downlights (1.0, 1.0) ... (3.1, 1.6) |
| Room 1, room 2 | 2 downlights each |
| Mamad | 2 downlights |
| Master bedroom | 4 downlights |
| Master bath | 3 downlights (one at (5.16, -4.27) after its shift) |
| Niche | 1 spot (3.2, -4.65) |
| Entry | 2 cylinders instead of point 1a (DESIGN) |

## 7. Proposed changes

All in `source/salon.html`. None moves a wall, so `roomdims.py` is unaffected; run `clearance_audit.py` after 1, 4, 7,
10 and 11 anyway. Heights not written on the sheet are estimates.

| # | Line | Current | Replacement | Basis | Conf. |
|---|---|---|---|---|---|
| 1 | 1737 | `outlets('e', -3.8, 1.66, .65, 'sk');` | `outlets('e', -3.8, 1.59, .65, 'sk');` | written 120 from the mamad south face (2.745) to the socket | high-medium |
| 2 | 986 | `['n', -.19, 3.02]` (in the switch list) | `['n', -.19, 3.18]` | scaled: stem meets the wall at 3.17; clears the panel at 3.33 | medium |
| 3 | 1750 | `B(3.14, 3.26, -.202, -.19, 1.47, 1.55, mat.whitePlate); B(3.155, 3.245, -.2035, -.202, 1.485, 1.535, mat.screen, { cast: false });` | `B(3.80, 3.92, -.202, -.19, 1.47, 1.55, mat.whitePlate); B(3.815, 3.905, -.2035, -.202, 1.485, 1.535, mat.screen, { cast: false });` | scaled: symbol east of the panel; height kept (estimate) | medium |
| 4 | 1737 | `outlets('w', -.25, 2.235, .40, 'sd');` | `outlets('w', -.25, 2.33, .40, 'sd');` | scaled from the mamad south face | medium-low |
| 5 | 1745 | `outlets('n', -.145, .72, .40, 's');` | `outlets('n', -.145, .65, .40, 's');` | scaled | medium-low |
| 6 | 1776 | `[[8.05, 2.2], [8.05, 5.7]].forEach(` | `[[7.96, 2.14], [7.96, 5.73]].forEach(` | scaled from the facade face; supersedes the recheck2 photo values | medium-low |
| 7 | 1737 | `outlets('w', -.25, .80, 1.80, 'dst');` | `outlets('w', -.25, .89, 1.80, 'dst');` | scaled from the north face; the south-face anchor gives only 3 cm | low |
| 8 | after 1750 | none | `outlets('n', -.19, 3.57, 1.15, 'ss');   // double socket "x2" between the comms box and the panel (height an estimate)` | scaled x; height estimate | low |
| 9 | after 1750 | none | `outlets('n', -.19, 3.99, .40, 'd');   // FO fibre point (height an estimate)` | scaled x; height estimate | low |
| 10 | after 1540 (outside the niche `withShift`) | none | `B(2.15, 2.20, -4.94, -4.82, 1.10, 1.24, M('#8e9194', .5), { round: .008 });   // AC isolator 3x16A IP65 (height an estimate)` | scaled; clears the riser at z -4.965 | low |
| 11 | after 1540 (outside the niche `withShift`) | none | `B(4.32, 4.37, -4.90, -4.78, 1.10, 1.24, M('#8e9194', .5), { round: .008 });   // water heater switch IP65 (height an estimate)` | scaled; clears the heater (edge x 4.31) | low |
| 12 | 1756 | `outlets('w', 4.46, -3.61, 1.40, 's'); outlets('w', 4.46, -3.34, 1.40, 's');` | `outlets('w', 4.46, -3.55, 1.40, 's'); outlets('w', 4.46, -3.29, 1.40, 's');` | scaled | optional, low |
| 13 | 1774, 1777 | `outlets('w', FX, 3.85, .40, 's');` and `B(FO, FO + .05, 3.80, 3.90, .34, .46,` | `outlets('w', FX, 3.90, .40, 's');` and `B(FO, FO + .05, 3.85, 3.95, .34, .46,` | scaled, pier-relative | optional, low |

## 8. Coordination with the other recheck3 reports

| Other change | Effect on electrical |
|---|---|
| geometry P4b (passage jamb 2.97 to 3.00) | the current 3c plate at 3.02 (2.98..3.06) would overlap the jamb; change 2 removes the clash |
| geometry P2a (pier 3.49..4.29, centre 3.89) | with it, also move `krr` and the pier socket to 3.89 (instead of change 13's 3.90); balcony lights stay as change 6 |
| geometry P2 (window C 7.75..8.45, sill 1.20) | 1p switch at 7.20 still sits between door B (6.99) and window C |
| geometry P3i (mamad window 0.48..1.48) | change 1 puts the `sk` plates at 1.51..1.67: 3 cm clear of the jamb |
| geometry P3e (master window -2.17..-1.27) | shutter switch at -2.45 still clear |
| geometry P5 (kitchen wall end 4.33) | switch 1d becomes 22 cm from the end vs 15.7 on the sheet; optionally move `['n', 5.50, 4.11]` to `4.17` |
| plumbing_ac.md change 2 (master split over the door) | the "16" point at (4.365, -0.179) then sits at the split's south end; add a plate there if wanted (height not written) |
| plumbing_ac.md change 1 (family bath pipe box) | the splash-proof socket moves with the box face |
| plumbing_ac.md change 6 (condenser outline) | isolator of change 10 at x 2.15..2.20 stays clear |

## 9. Still open

| Item | Note |
|---|---|
| Boxed "א" in rooms 1, 2, master, mamad | meaning unknown; ask the electrician |
| Blue box "1" over the entry door | chime or strike |
| INT7 cones and "S" box | alarm prep (probable) or AC controller |
| Shutter on window C | sheet shows a casement and no motor; the model has a shutter |
| Master TV screen vs point | screen toward the door, point at 6.93 bare: owner choice |
| Ceiling points 1a, 1b vs owners' lamps; extra model downlights | design choice |
