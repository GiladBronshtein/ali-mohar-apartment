# Electrical sheet re-check 2 (2026-10-04)

Source: `materials/plans/originals/electrical_IMG_8065.jpg` (HADA, 9/2/2006, 1:75 on A3; photo 5712x4284, rotated
about 2 degrees, taken at an angle). Model: `source/salon.html` as of this date (working copy, line numbers as read
today). Evidence crops: `audit/recheck2/el_crops/` (overview.jpg is the whole sheet at 1/4).

## Method

- Model metres: x east, z south, y up. Origin = living face of the TV wall (z 0) at the dining/storage west face (x 0).
- The sheet is NOT to scale: written dims disagree with the pixel scale by up to 20 percent (corridor 105/210 imply
  190 and 244 px/m). Rule used: (W) = from a written number, tolerance 3 cm; (S) = scaled proportionally between the
  room's own wall faces (or a nearby pier/jamb), tolerance about 5 cm, 10 cm where symbols are crowded.
- Dimension ticks for outlet groups sit at the junction between two symbols (checked in rooms 1 and 2: the h=180 tick
  falls between the socket and the TV, the h=40 tick between socket and data). Proposed rows are centred to match.
- Model positions include the `withShift(dx, dz)` of their block. `outlets(face, wall, c, y, kinds)` = 8.5 cm pitch,
  centred on c, ordered along +x (faces s/n) or +z (faces e/w).
- No legend in the photo. Meanings below are by convention: crossed circle = ceiling point; circle with stem = switch;
  half circle = socket (with X = splash-proof); filled circle with arrow = shutter switch; filled dot at a window =
  shutter motor; half-filled circle = wall/waterproof light; hatched rectangle = wall heater; blue ת = data/phone;
  blue ט = probably TV/phone (modelled as 'd'). Unidentified: blue E, S, FO, VE, A; boxed double square "א" + "25";
  the "flag" (triangle on a bar).
- Heights written on the sheet: h=40, 60, 65, 110, 130, 140, 180, 200, 220. All other heights (switches 1.10,
  panel, intercom, balcony socket) are model estimates.

## Room 1 (crops r1.jpg, r1_tv.jpg)

| Symbol | Meaning | Sheet position | Model (value / line) | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 3b | ceiling point | (-2.55, -3.235) (W: 180 from N, 140 from E face -1.15) | fan (-2.51, -3.21) L1512 + shift | +4, +2.5 | OK |
| socket + ת h=40, W wall | socket, data | tick z -4.625 (W: 41) between them | 'sd' c -4.625 L1686 | 0 | OK |
| ת, socket 3, TV h=180, W wall | data, 1 socket, TV | tick -3.335 (W: 41+129) between socket and TV | 'sstd' c -3.31 L1686 | 2 sockets vs 1, data on the wrong side | FIX |
| socket + switch 3b h=65, N wall | bed head | s -2.25, k -2.14 (S) | 'sk' c -2.22 L1687 | <4 | OK |
| switch 3b | door switch, inside, latch side | x about -2.18 (S) | plate (-2.18, -1.425) L963 | 0 | OK |
| switch 3m | shutter switch at S jamb, W wall | z about -1.775 (S) | 'r' -1.80 h 1.10 (est.) L1687 | -2.5 | OK |
| motor 3m | window head | window -2.92..-1.93 | shutterZ L1721 | | OK |
| boxed "א" 25 | unidentified, mid-room | about (-2.64, -2.39) (S) | none | | OPEN |
| model extras | | | spots (-2.5,-3.8), (-2.5,-2.2) L972 | not on sheet | design |

## Room 2 (crops r2.jpg, r2_tv.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 2d | ceiling point | (0.47, -3.21) (W: 180, 144) | fan (0.45, -3.20) L1533 + shift | -2, +1 | OK |
| socket + ת h=40, E wall | | tick z -4.55 (W: 46) | 'sd' c -4.55 L1689 | 0 | OK |
| ת, socket 2, TV h=180, E wall | 1 socket | tick -2.82 (W: 46+173) between socket and TV | 'sstd' c -2.82 L1689 | 2 sockets vs 1, data side | FIX |
| switch 2d, socket 2, shutter 2n h=65, N wall | bed head | order k, s, r; drawn spread to about x 0.42 (S, weak) | 'ksr' c .02 L1689 | order OK | OK (spread is symbol size) |
| switch 2d | door switch | x about 0.80 (S) | plate (0.80, -1.45) L963 | 0 | OK |
| boxed "א" 25 | | mid-room | none | | OPEN |
| model extras | | | spots (0.45,-3.8), (0.45,-2.2) | | design |

## Mamad (crop mamad.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 3a | ceiling point | (-1.97, 1.395) (W: 183 from W -3.80, 135 from S 2.745) | fan (-1.97, 1.395) L1547 + shift | 0 | OK |
| socket 3 + switch 3a h=65, W wall | bed head | s 1.585, k 1.75 (S) | 'sk' c 1.66 L1691 | <4 | OK |
| ת, socket 3, TV h=180, E wall | 1 socket | ת 0.61, s 0.80, TV 1.0 (S) | 'sstd' c .855 L1691 | 2 sockets, data side | FIX |
| socket 3 + ת h=40, E wall | | s 2.22, ת 2.42 (S) | 'sd' c 2.235 L1691 | <5 | OK |
| socket 3 h=220 (filter) | socket on the SOUTH wall, half circle on the wall line | x about -3.63, z 2.745 (S) | 's' on the W wall at z 2.335 L1697 | wrong wall | FIX |
| filter outline | AC/blast filter | x -3.757..-3.435, z 2.20..2.545 (S) | box x -3.8..-3.59, z 2.085..2.585 | | OPEN (plumbing/AC re-check) |
| switch 3a | door switch inside, E of blast door | x about -1.03 (S) | plate (-1.10, .125) L962 | -7 | OK (crowded) |
| "25" near NE corner | dim or conduit size | | | | OPEN |
| boxed "א" 25 | | | none | | OPEN |
| model extras | | | spots (-2.7,1.4), (-1.1,1.4) | | design |

## Corridor (crops corr_w.jpg, corr_m.jpg, corr_e.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 3c x3 | ceiling points | x -1.07 / 1.03 / 3.13, z -0.665 (W: 105, 210, 210 from x -2.12; 58 from N) | cylinders same L977 | 0 | OK |
| switch 3c W | S wall corridor face | x about 0.20 (S) | plate (0.18, -.145) L962 | -2 | OK |
| socket 3 | S wall, no h | x about 0.67 (S) | 's' .72 h .40 (est.) L1699 | +5 | OK |
| 2ef + 4 + 12 | bath switches (two with pilot lamps) | N wall, x about 2.62..2.68 (S) | 'kkk' c 2.66 L1708 | 0 | OK |
| switch 3c E | TV-wall corridor face | x about 3.36 (S, 25 cm E of light 3) | plate (3.02, -.19) L962 | -34 | OPEN (tied to panel) |
| panel recess "לוח חשמל דירתי ... תיבת תקשורת ... צג דיגיטלי" | panel, comms box below, consumption display | starts about x 3.12 (S), right end unreadable | panel 3.33..3.78 L1701 (sales plan) | about -21 on the W edge | OPEN (drawings disagree) |
| double socket "x2" circuit 1 + "A" | near panel | x about 3.68 (S) | none | | OPEN / ADD low |
| blue FO | fibre? | x about 4.05 (S) | none | | OPEN |
| model extra | | | plate (1.86, -1.245) L962 | not on sheet | extra |

## Master bedroom (crops master.jpg, master_2m.jpg, tvwall_liv.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 2a | ceiling point | (6.73, -1.645) (W: 150, 218) | fan (6.73, -1.645) L1319 + shift | 0 | OK |
| bed head right h=60: switch 2a, socket, ט | | k 7.88 (S), s 8.02 (W: 89 from E), ט 8.28 (S) | 'sd' c 8.06 L1709 (s 8.0175) | switch missing | FIX/ADD |
| bed head left h=60: E, socket | | E 5.56 (S), s 5.82 (W: 89+220) | 'sd' c 5.87 L1709 (s 5.8275, d E of it) | s 0; data on the wrong side | FIX (minor) |
| boxed "א" h=60 + 25 | | about (5.65, -0.84) (S) | none | | OPEN |
| socket 2, TV, ת h=180, bath wall | 1 socket | s 6.75, TV 6.93, ת 7.13 (S) | 'sstd' c 6.90 L1710 | 2 sockets | FIX |
| TV screen | | sheet TV point 6.93 | screen x 5.13..6.29 L1324 area | about 1.2 m | OPEN (owner choice) |
| switch 2a | door switch, return face | x about 4.42, z -1.245 (S) | plate (4.42, -1.245) L963 | 0 | OK |
| switch 2m | shutter, E wall N of window | z about -2.50 (S, 20 cm N of jamb -2.27) | 'r' -2.45 L1710 | +5 | OK |
| motor 2m | window head | | shutterZ L1723 | | OK |
| model extras | | | plate (5.70,-3.095) h1.0 L1322; downlights x4; bedside pendants | not on sheet | extra |

## Closet

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 2c | ceiling point | (7.63, -3.795) (W: 120, 128) | spot (7.63, -3.80) L973 | 0 | OK |
| switches 2b + 13 | bath light + heater 13, closet side of x 7.01 | z about -4.20 (S) | 'kk' c -4.20 L1708 | 0 | OK |
| switch 2c | bedroom face of closet wall | x about 8.435 (S) | plate (8.40, -3.105) L962 | -3.5 | OK |
| closet opening | geometry | about 7.47..8.28 (S) | 7.54..8.32 | | note (geometry re-check) |

## Master bath (crops mbath.jpg, mbath2.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ◐ 2b | wall light over vanity, W wall | z -3.70 (W: 44 from S face -3.26) | mirror cabinet centre -3.71 with LED L1381 + shift | -1 | OK |
| socket 2 h=110 (X) | splash-proof, S wall by vanity | x about 4.72 (S) | none | | ADD |
| heater 13 h=200 | hatched, E wall x 6.85 | z about -4.27 (S), symbol about 30 cm | none | | ADD |
| ceiling point | none drawn | | spots (5.3,-3.7), (6.4,-3.9), (5.16,-4.27) | | extra (design) |

## Family bath and washer niche (crops svc.jpg, svc2.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ◐ 2f | waterproof ceiling light | x 3.01 (W: 100 from W 2.01), z about -3.09 (S) | spot (3.01, -3.10) h BC L973 | 0, -1 | OK |
| ◐ 2e | wall light over basin, W wall | z -2.115 (W: 72 from S face -1.395) | mirror cabinet axis -2.115 L1474 | 0 | OK |
| socket 2 h=110 (X) | splash-proof, SW corner | x about 2.19 on the S wall (S); the model's pipe box x 2.01..2.20 fills that corner | none | | ADD (on the pipe box N face) |
| heater 12 h=200 | hatched, S wall | centre x about 2.67 (S), symbol about 70 cm | none (towel ladder 2.42..2.76 below, h .55..1.25) | | ADD |
| circled "9" + bell-like mark | by the basin, about (2.5, -2.0) | | none | | OPEN |
| sockets 7, 10 h=140 (X) | washer, dryer, E wall x 4.46 in the niche | z about -3.61 and -3.34 (S) | none (stack x 3.84..4.44) | | ADD |

## Laundry screen niche

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| "9 3x16A IP65" | isolator (AC condenser or heater) | W wall, about (2.19, -5.0) (S) | none | | ADD/OPEN |
| big circle + IP65 + dots | water heater with its isolator, probably | about (4.10, -4.98) (S) | heater in the niche (plumbing) | | OPEN (plumbing re-check) |
| model extra | | | spot (3.2, -4.65) L973 | not on sheet | extra |

## Living, dining, entry, kitchen (crops dining_w.jpg, tvwall_liv.jpg, entry.jpg, kitchen_1d.jpg, liv_*.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| ⊗ 1b | living ceiling point | (4.98, 2.00) (W: 200 from z 0, 230 from FX) | owners' flush light (4.70, 2.20) L980 | -28, +20 | OPEN (lamp over the coffee table; box would need a canopy offset) |
| ⊗ 1c | dining ceiling point | (1.27, 1.305) (W: 127 from x 0, 147 from block face 2.775) | wave pendant, canopy x about 1.20, z 1.17..2.41 L1179 | box under the canopy | OK |
| ט + socket 1 h=40 | dining W face x 0 | ט z 0.65, s 0.89 (S) | none (inside the storage wall) | | ADD hidden, low |
| TV wall h=40: S, FO, ת, double socket 1, TV, ⊠ | living face z 0 | 4.69 / 5.00 / 5.29 / 5.43..5.63 / 5.85 / 6.05 (W anchor 185 from FX at the socket's W edge, rest S) | none | | ADD hidden, low |
| TV wall h=130: socket 1 + ⊠, 50ø conduit to the h=40 box | inset, drawn below the wall | about 5.30 / 5.83 (S, weak) | none (behind the TV 4.06..5.94, y .98..2.04) | | ADD hidden, low |
| model TV | | sheet outlets centre about 5.4..5.8 | TV centred 5.00 L1094 | | note |
| switch 1bc + flag | two-way for 1b/1c on block E face x 1.45 | z 2.955 (S); flag at z about 3.30 | plate (1.45, 3.0) L962 | +4.5 | OK; flag OPEN |
| ⊗ 1a | entry ceiling point | (2.10, 4.50) (W: 65 from x 1.45, 100 from z 5.50) | owners' cylinders (2.4, 3.9), (2.4, 5.0) L977 | nearest 58 cm | OPEN (design) |
| switch 1ad (on a box with a dot) | entry/kitchen two-way, front-door wall z 5.50 | x about 2.66, first item E of the latch jamb 2.555 (S) | plate (2.76, 5.50) L962 | +10 | FIX |
| blue VE | video intercom | x about 2.99, E of 1ad (S) | screen x 2.64..2.74 L925 | -30, order reversed | FIX (limited by the art at 2.86..3.26) |
| blue box with circle "1" | at the latch jamb, in the door width | about x 2.5 (S) | none | | OPEN (electric strike?) |
| "A-5" | door type label | | | | n/a |
| switch 1d | kitchen, z 5.50 face | x about 4.10 (S) | plate (4.11, 5.50) L962 | +1 | OK |
| ⊗ 1d | kitchen ceiling point | (5.88, 6.51) (W: 140 from FX, 228 from S wall 8.79) | frames pendant canopy x 5.83..5.91, z 5.66..6.96 L1294 | box under the canopy (centre 20 cm N) | OK |
| note "חשמל מטבח עפ חברת מטבחים" | kitchen electrics by the kitchen supplier | | kitchen plates | | not checkable |
| model extras | | | spots (1.0,1.0), (1.0,2.0), (3.8,0.9), (5.9,0.9), (3.8,2.6), (5.9,2.6), (3.1,1.6), (4.6,4.2), (6.4,4.2), (4.6,6.2), (4.6,7.6), (6.6,7.9) | not on sheet | design |

## Facade pier, balcony (crops pier.jpg, balcony_1e.jpg)

| Symbol | Meaning | Sheet position | Model | Delta | Verdict |
|---|---|---|---|---|---|
| switch 1e + flag | balcony light, pier inner face FX | z about 3.67 (S) | 'k' of 'krr' 3.765 L1725 | +9 (crowded) | OK |
| shutter switches 1m, 1n | pier inner face | z about 3.87 / 4.14 (S, spread) | 'rr' 3.85 / 3.935 | order OK | OK |
| socket 1 | pier inner face, no h | z about 3.94 (S) | 's' 3.85 h .40 (est.) L1725 | -9 | OK (crowded) |
| splash-proof socket 1 | pier balcony face, no h | z about 3.94 (S) | box (FO, 3.80..3.90) h .34..46 (est.) L1728 | -9 | OK |
| motor 1m | door A, at its S end | z about 3.40 | shutterZ .78..3.45 L1724 | | OK |
| motor 1n | door B, at its N end | z about 4.35 | shutterZ 4.26..6.88 | | OK |
| switch 1p | pier 6.88..7.70 inner face | z about 7.10 (S) | 'r' 7.20 L1725 | +10 | FIX (low) |
| motor 1p | drawn at the S end of door B (z about 6.75), none drawn at window C | | shutterZ on window C 7.70..8.39 | | OPEN (B with two shutters, or symbol displaced) |
| ⊕ 1e x2 | balcony ceiling lights | (7.93, 2.05), (7.93, 5.79) (S, 50 px = about 23 cm from FO; z from the piers) | (8.05, 2.2), (8.05, 5.7) L1727 | +12, +15 / +12, -9 | FIX (low) |
| two filled crossed dots, balcony S wall | gas point and tap (also on the plumbing sheet) | x about 8.27 / 8.48 (S) | gas 8.30, tap 8.50 | <3 | OK |
| flags | unidentified (pilot lamp, chime or speaker) | by 1bc, by 1e, living NE corner, by 1p | none | | OPEN |
| "FE-12ø" notes | earthing/lightning ring, outside | | | | n/a |
| model extras | | | balcony fan (9.30, 1.55) L1626; wall lights (FO, 3.82), (FO, 7.3) | not on sheet | extra |

## Comparison with audit/recheck/electrical.md

Most of its proposals (corridor lights, closet point, fans, door switches, shutter 2m, bath switches, entry/kitchen
plates, balcony points) are now in the model and check OK here. Disagreements:

1. h=180 TV groups (rooms 1, 2, mamad, master): it called them OK with 2 sockets; the sheet has one socket and the
   data point on the other side of it. FIX here.
2. Mamad filter socket: it read the box symbol at z 2.44 on the W wall; here the h=220 socket half circle sits on the
   SOUTH wall line at x about -3.63.
3. Entry: it proposed the 1ad plate at 2.76 "under the intercom"; the sheet has 1ad first from the jamb (about 2.66)
   and VE east of it.
4. Balcony 1e: it scaled 35 cm out from the facade (8.05); here about 23 cm (7.93) and z 2.05 / 5.79.
5. h=130 TV-wall group: it put socket/box at 5.84 / 6.09; here about 5.30 / 5.83. The group is an inset, weak either way.
6. Family-bath wall light 2e: it had z -2.115 (correct); the model now matches.
7. Kitchen-window shutter 1p: it accepted window C; here the 1p motor is drawn at door B, so it is OPEN.
8. Corridor east switch 3c: it scaled 3.21; here about 3.36. Both say the model's 3.02 is west of the sheet.

## Proposed changes (ordered by confidence)

High (written dims or clear symbol order):

1. L1686 `outlets('e', -3.89, -3.31, 1.80, 'sstd')` -> `outlets('e', -3.89, -3.38, 1.80, 'dst')` (room 1; s/t junction at the written -3.335).
2. L1689 `outlets('w', 1.85, -2.82, 1.80, 'sstd')` -> `outlets('w', 1.85, -2.86, 1.80, 'dst')` (room 2; junction at the written -2.82).
3. L1709 `outlets('n', -.19, 8.06, .60, 'sd')` -> `outlets('n', -.19, 8.02, .60, 'ksd')` (adds two-way 2a; socket stays at the written 8.02).
4. L1709 `outlets('n', -.19, 5.87, .60, 'sd')` -> `outlets('n', -.19, 5.78, .60, 'ds')` (E point W of the socket; socket 5.8225 vs written 5.82).
5. L1710 `outlets('s', -3.105, 6.90, 1.80, 'sstd')` -> `outlets('s', -3.105, 6.93, 1.80, 'std')`.
6. L1691 `outlets('w', -.25, .855, 1.80, 'sstd')` -> `outlets('w', -.25, .80, 1.80, 'dst')`.
7. L1697 `outlets('e', -3.8, 2.335, 2.20, 's')` -> `outlets('n', 2.745, -3.63, 2.20, 's')` (mamad filter socket on the S wall; check it clears the filter top).

Medium (symbol present, position scaled; heights from the sheet, sizes estimated):

8. ADD master bath heater 13: `B(6.77, 6.85, -4.46, -4.08, 1.90, 2.10, mat.whitePlate, { round: .01 })` (h=200 written; 38 cm width estimate; clear of the closet door -4.06).
9. ADD family bath heater 12: `B(2.45, 2.85, -1.475, -1.395, 1.90, 2.10, mat.whitePlate, { round: .01 })` (h=200 written; 40 cm width estimate; clear of the door frame 2.86).
10. ADD master bath socket 2: `outlets('n', -3.26, 4.72, 1.10, 's')` (h=110 written).
11. ADD family bath socket 2: `outlets('n', -1.605, 2.105, 1.10, 's')` (h=110 written; on the N face of the pipe box, which fills the corner the sheet points at).
12. ADD washer/dryer sockets: `outlets('w', 4.46, -3.61, 1.40, 's'); outlets('w', 4.46, -3.34, 1.40, 's')` (h=140 written; hidden behind the stack).
13. L962 `['n', 5.50, 2.76]` -> `['n', 5.50, 2.66]`, and L925 intercom `B(2.64, 2.74, ...)` -> `B(2.74, 2.84, 5.488, 5.50, 1.30, 1.48, ...)` (sheet order jamb, 1ad, VE; VE stays about 15 cm W of the sheet because of the art at 2.86..3.26; heights are estimates).

Low (crowded or weak scaling):

14. L1727 balcony lights `[[8.05, 2.2], [8.05, 5.7]]` -> `[[7.93, 2.05], [7.93, 5.79]]`.
15. L1725 `outlets('w', FX, 7.20, 1.10, 'r')` -> `outlets('w', FX, 7.10, 1.10, 'r')`.
16. ADD hidden outlets: dining `outlets('e', 0, .77, .40, 'ds')`; living TV wall `outlets('s', 0, 5.35, .40, 'dddsst')` (h=40) and `outlets('s', 0, 5.55, 1.30, 'sd')` (h=130, behind the TV). Only worth it if the storage wall or media console is ever opened.
17. ADD isolator "3x16A IP65" in the laundry niche W wall at about (2.19, -5.0); height not written.

Not proposed without a decision (OPEN): living point 1b vs the coffee-table lamp; entry point 1a vs the two cylinders;
master TV position; corridor switch 3c east and the panel recess (sheet starts about 3.12, sales plan 3.33);
1p motor at door B vs window C; boxed "א" 25 in four rooms; flags; blue E/S/FO/VE/A meanings; circled "9" in the
family bath; FO and "x2" socket near the panel; mamad "25" note; filter outline (AC re-check); removal of extra
downlights, pendants, balcony fan and wall lights (design).

No item above moves a wall; `roomdims.py` and `clearance_audit.py` are unaffected except by the heater boxes (check
clearance after 8 and 9).
