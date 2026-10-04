# Electrical plan re-check (2026-10-04)

Source: `materials/plans/originals/electrical_IMG_8065.jpg` (contractor HADA, 9/2/2006, 1:75 on A3, photo 5712x4284
taken at an angle). Model: `source/salon.html` as of this date (line numbers re-checked against the file).
Proving crops: `audit/recheck/el_crops/` (file names in each section).

## Method and conventions

- Model metres: x east (toward the balcony), z south (toward the kitchen), y up. Origin: living face of the TV wall
  (z = 0) at the west face of the dining alcove (x = 0).
- **(W)** = position from a number written on the plan (tolerance 3 cm). **(S)** = scaled from the photo (local scale
  about 2.2 to 2.3 px/cm at full resolution, varies with perspective; tolerance 10 cm). Symbols in crowded spots
  (bed heads, piers, next to the panel) are drawn spread out for legibility, so scaled positions there are weak.
- Dimension lines on this sheet are often drawn offset from the point they locate (for example the 230 line of light
  1b and the 218 line of light 2a); positions below use the written value and the wall it starts from, not the line.
- Model positions include the `withShift(dx, dz)` offset of the block they sit in. `outlets(face, wall, c, y, kinds)`
  centres the row on c with an 8.5 cm pitch, so element i is at c + (i - (n-1)/2) * 0.085.
- Heights written on the plan (h=40, 65, 60, 110, 140, 180, 200, 220, 130) are used as given. Heights the plan does
  not give (switches at 1.10, the panel) are model estimates.
- Symbol legend is not in the photo. Read as: crossed circle = ceiling point; circle with stem = light switch; half
  circle = socket; filled circle with arrow = shutter switch; small filled circle at a window = shutter motor
  (labelled "תריס חשמלי"); half-filled circle = wall or surface light; hatched rectangle at h=200 = bathroom wall
  heater; blue circle "ת" = phone/communications point. Blue "FO", "E", "U/ט", "VE", "S", "A", the boxed "א" with
  "25", and the black triangle are not identified (see Unreadable).

## Room 1 (crops `room1.jpg`, `r1sym.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 3b | (-2.55, -3.235) (W: 180 from N wall, 140 from E wall) | fan (-2.51, -3.21) | +4, +2.5 cm | OK in z, x 1 cm outside tolerance | L1443 in withShift(.09,-.21) |
| Socket h=40, W wall | z -4.625 (W: 41 to the socket stem) | socket -4.6675 (row centre -4.625) | -4.25 cm | Marginal: row centred on the socket dim | L1598 |
| Phone ת h=40 | below the socket (S) | d at -4.5825 | order matches | OK | L1598 |
| TV group h=180, W wall | dim tick at z -3.335 (W: 41+129); socket -3.43, TV -3.23, ת -3.66 (S) | s -3.4375, s -3.3525, t -3.2675, d -3.1825 | TV -4, ת on the other side (48 cm) | OK for TV; data order differs | L1598 |
| Bed head h=65, N wall | socket -2.32, switch -2.08 (S) | s -2.2625, k -2.1775 | +6, -10 | OK (crowded) | L1599 |
| Door switch 3b | latch (west) side, x about -2.12 to -2.17 (S); door hinge east | plate x -1.22, hinge side | about +95 cm | **MISMATCH** | L944 `['n', -1.425, -1.22]` |
| Shutter switch 3m, W wall | z about -1.77 (S) | 'r' at -1.80 h 1.10 | -3 | OK | L1599 |
| Shutter motor 3m | at the window | shutter rails z -2.92..-1.93 | | OK | L1632 |
| Boxed "א" + "25" | about (-2.55, -2.34) (S) | none | | Unidentified, not modelled | |

## Room 2 (crop `room2.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 2d | (0.47, -3.21) (W: 180, 144) | fan (0.45, -3.20) | -2, +1 | OK | L1464 in withShift(.15,-.20) |
| Socket h=40, E wall | z -4.55 (W: 46) | socket -4.5925 (row centre -4.55) | -4.25 | Marginal, same centring as room 1 | L1601 |
| TV h=180, E wall | z -2.82 (W: 46+173) | row centre -2.82, t -2.7775 | +4 on t | OK / marginal | L1601 |
| Bed head h=65, N wall: 2d switch, socket 2, shutter 2n | x 0.01 / 0.23 / 0.45 (S, spread) | k -0.065, s 0.02, r 0.105 | -8, -21, -35 | Weak scaled evidence; row may be about 20 cm west | L1601 |
| Door switch 2d | latch side, x about 0.88 (S) | 0.80 | -8 | OK | L944 |
| Shutter motor 2n | at the window | rails x .27..1.25 | | OK | L1633 |
| Boxed "א" + "25" | room centre-south (S) | none | | Unidentified | |

## Corridor (crops `corrW.jpg`, `corrE.jpg`, `mdoor2.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Light 3c west | (-1.07, -0.665) (W: 105 from x -2.12, 58 from N wall) | spot (-0.8, -0.70) | +27, -3.5 | **MISMATCH** | L953 |
| Light 3c middle | (1.03, -0.665) (W: +210) | spot (1.3, -0.70) | +27, -3.5 | **MISMATCH** | L953 |
| Light 3c east | (3.13, -0.665) (W: +210) | spot (3.3, -0.70) | +17, -3.5 | **MISMATCH** | L953 |
| Switch 3c west, corridor face of TV wall | x about 0.16 to 0.21, just east of the mamad corner (S) | none there; model has a plate on the N wall at x -1.15 | | **MISMATCH** (wall and position) | L943 `['s', -1.245, -1.15]` |
| Switch 3c east, by the panel | x about 3.21 (S, crowded) | plate 3.02 | -19 | Mismatch, weak (tied to panel position) | L943 `['n', -.145, 3.02]` |
| Family-bath switches 2ef + 4 + 12 (lights 2e/2f, boiler?, heater 12) | N wall corridor face, latch (west) side of the bath door, x about 2.78 (S) | single plate x 3.78, hinge side | about +100 | **MISMATCH**, also 1 plate vs 3 switches | L943 `['s', -1.245, 3.78]` |
| Plate N wall x 1.86 | not on plan | plate | | Extra | L943 |
| Socket "3", corridor face of TV wall | x about 0.65 to 0.67 (S), no h given | 's' at 0.72 h 0.40 | +6 | OK | L1611 |
| Panel recess ("לוח חשמל דירתי ומתחתיו תיבת תקשורת, צג דיגיטלי לניטור צריכת החשמל") | x about 3.01..3.40 (S) | x 3.33..3.78 | +32..+38 | Conflict: the sales plan puts it at 3.37..3.78 (audit/report.md); the two drawings disagree | L1613 |
| Blue "FO" on corridor face of TV wall | x about 3.97 (S) | none | | Missing (unidentified, perhaps fibre) | |
| "A" and a double socket "x2" near the panel | x about 3.5 (S) | none | | Missing / unidentified | |

## Master bedroom (crops `master.jpg`, `m_bedR.jpg`, `m_east.jpg`, `mdoor2.jpg`, `corrM.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 2a | (6.73, -1.645) (W: 150 from TV wall face -0.145, 218 from E wall 8.91) | fan (6.80, -1.65) | +7, -0.5 | **MISMATCH** (x) | L1258 in withShift(.20,.10) |
| Bed head left socket h=60 | x 5.82 (W: 220 + 89 from E wall) | s 5.8275 | +1 | OK | L1620 |
| Bed head right socket h=60 | x 8.02 (W: 89 from E wall) | s 7.8575 | -16 | **MISMATCH** | L1620 `outlets('n', -.19, 7.90, ...)` |
| Two-way switch 2a at right bed head | next to the right socket, x about 7.88 (S), h=60 | none | | Missing | |
| Blue "E" (left), "ט" (right) | W of left socket, E of right socket (S) | 'd' E of each socket | left order differs | Minor | L1620 |
| Boxed "א" h=60 + "25" by the left bed head | x about 5.6 (S) | none | | Unidentified, not modelled | |
| TV group h=180 on bathroom wall: socket 2, TV, ת | x 6.65 / 6.88 / 7.13 (S) | s 6.7725, s 6.8575, t 6.9425, d 7.0275 | TV +6 | OK; plan has 1 socket, model 2 | L1621 |
| TV screen | over the TV point, about x 6.9 (bed centre is 6.92 by the written socket dims) | screen x 5.13..6.29 ("toward the door corner") | about 1.2 m | Model is inconsistent with its own TV point; design choice to confirm | L1260 |
| Door switch 2a | stub face z -1.245, x about 4.40 (S), latch side | plate (4.42, -1.245) | +2 | OK | L944 |
| Shutter switch 2m, E wall | z about -2.47, NORTH of the window (window -2.27..-1.31) (S) | 'r' at z -1.15, south of the window | about +132 | **MISMATCH** (side of window is clear on the plan) | L1621 `outlets('w', 8.91, -1.15, 1.10, 'r')` |
| Shutter motor 2m | window head | rails z -2.27..-1.31 | | OK | L1634 |
| Pendants over the nightstands | not on plan | (5.84, -0.38), (8.12, -0.38) | | Extra (if kept, right one should follow the socket to about 8.04) | L1256 |
| Downlights | not on plan (only 2a) | (5.7,-1.9), (7.8,-1.9), (5.7,-0.8), (7.8,-0.8) | | Extra | L953 |
| Plate behind the TV (5.70, -3.095) | not on plan | plate .14 wide | | Extra | L1261 |

## Closet (crop `m_east.jpg`, `master.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 2c | (7.63, -3.795) (W: 120 from N wall -4.995, 128 from E wall 8.91) | spot (7.9, -4.2) | +27, -40 | **MISMATCH** | L954 |
| Switch 2c | master face of the closet wall (z -3.105, face 's'), just E of the opening, x about 8.32 to 8.40 (S) | none | | Missing | |

## Ensuite (crop `ensuite.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Wall light 2b over the vanity, W wall | z -3.70 (W: 44 from the partition -3.26) | mirror cabinet centre -3.67 (with its LED) | +3 | OK | L1315 block |
| Socket "2" h=110 | SW corner by the vanity, about (4.72, -3.30) (S) | none | | Missing | |
| Wall heater 13 h=200 | closet wall x 6.85, z about -4.3 (S) | none | | Missing | |
| Switches 2b + 13 | closet side of x 7.01, z about -4.2, latch side of the door (door -4.06..-3.36, hinge -3.365) (S) | none | | Missing | |
| Ceiling lights | none drawn | spots (5.16, -4.27), (5.3, -3.7), (6.4, -3.9) | | Extra | L1307 (withShift .19), L954 |

## Family bath (crops `fbath.jpg`, `corrE.jpg`, `ensuite.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Light 2f (half-filled circle, room centre) | x 3.01 (W: 100 from W wall 2.01); z about -3.1 (S, label unreadable, 62 to 70 cm from N wall) | 2 spots (2.8, -2.6), (3.6, -2.6) | 1 point vs 2; pair centre about 50 cm south | **MISMATCH** | L954 |
| Wall light 2e over the basin, W wall | z -2.115 (W: 72 from S wall -1.395) | mirror cabinet axis -2.185 | -7 | **MISMATCH** (written) | L1405 |
| Socket "2" h=110 | SW corner by the basin (S) | none | | Missing | |
| Splash-proof socket "9" (circled) | about (2.50, -2.31) (S) | none | | Missing | |
| Wall heater 12 h=200 | S (corridor) wall, x about 2.77 (S) | none (towel ladder at x 2.42..2.76 on that wall) | | Missing; would sit just E of the ladder | L1415 |
| Washer / dryer sockets 7 and 10, h=140 | NE niche, E wall, z about -3.4 / -3.6 (S) | washer-dryer stack, no sockets | | Missing | L1335 block |
| Laundry niche N of the window: "9 3x16A IP65" isolator; second niche: IP65 isolator + hatched circle (AC condenser?) | outside the bath | spot (3.2, -4.65), no isolators | | Spot extra; isolators missing | L954 |

## Mamad (crops `mamad.jpg`, `mamad_s.jpg`, `corrW.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 3a | (-1.97, 1.395) (W: 183 from W wall -3.80, 135 from S wall 2.745) | fan (-2.08, 1.39) | -11, 0 | **MISMATCH** in x. Caveat: the photo scales the room at about 368 cm vs model 355, so the 183 origin or the wall line is uncertain | L1478 in withShift(-.08,-.11) |
| TV group h=180, E wall: ת, socket 3, TV | z 0.555 / 0.73 / 0.97 (S) | s .7275, s .8125, t .8975, d .9825 | socket 0, TV -7, ת on the other side | OK for socket and TV; plan has 1 socket | L1603 |
| Socket 3 + ת h=40, E wall | z 2.245 / 2.53 (S) | s 2.1925, d 2.2775 | -5, -25 | OK for socket; data weak | L1603 |
| Bed head h=65, W wall: socket 3, switch 3a | z 1.57 / 1.79 (S) | s 1.6175, k 1.7025 | +5, -9 | OK | L1603 |
| Socket 3 h=220 (filter) | box centre about z 2.44 (S) | 's' at 2.335 | -11 | Marginal (box symbol may be the filter, not the socket) | L1609 |
| Door switch 3a | N wall inner face (z 0.125, face 's'), latch (east) jamb, x about -1.10 to -1.19 (S) | none | | Missing | |
| Boxed "א" + "25" | about (-1.52, 0.42) (S) | none | | Unidentified | |
| Downlights | not on plan | (-2.7, 1.4), (-1.1, 1.4) | | Extra | L953 |

## Living, dining, entry, kitchen (crops `corrM.jpg`, `dining.jpg`, `kitchen.jpg`, `overview.jpg`)

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling point 1b | (4.98, 2.00) (W: 200 from TV wall z 0, 230 from FX 7.28) | none; 5 spots (3.8,0.9), (5.9,0.9), (3.8,2.6), (5.9,2.6), (3.1,1.6) | | **Missing** point; spots extra | L952 |
| TV-wall group h=40, living face of TV wall | "S" box 4.70, FO 5.01, ת 5.31, dim tick 5.43 (W: 185 from FX), double socket "x2" circuit 1 about 5.56 to 5.70, TV about 5.82, blue X box about 6.06 (S) | none | | Missing (would be mostly behind the TV, x 4.06..5.94) | |
| TV-wall group h=130: socket 1 + X box, 50ø conduit to the h=40 box | x about 5.84 / 6.09 (S) | none | | Missing; X box would show just E of the TV edge 5.94 | |
| TV position | outlets centred about 5.8 | TV centred 5.0 (furniture images on the plan also centre about 5.0 to 5.1) | | Note only | L1062 |
| Dining point 1c | (1.27, 1.305) (W: 127 from x 0, 147 from lobby wall 2.775) | none; spots (1.0, 1.0), (1.0, 2.0) | nearest 41 cm | Mismatch (dining replaced by the storage wall, a recorded decision) | L952 |
| Dining socket 1 + ט h=40, alcove W wall | z about 0.86 (S) | inside the storage wall; robot-garage plate at z 0.405 h .44 | | Not applicable while the storage wall stays | L1133 |
| Entry point 1a | (2.10, 4.50) (W: 65 from entry W wall 1.45, 100 from entrance wall 5.50) | none; spots (2.4, 3.9), (2.4, 5.0) | nearest 58 cm | **Missing** point | L952 |
| Entry switch 1ad (switch on a box) | wall z 5.50 face 'n', EAST of the door, x about 2.76 (S); plan door hinge is west (arc) | plate x 1.53, west of the door | about -123 | **MISMATCH** | L943 `['n', 5.50, 1.53]` |
| Blue "VE" (video intercom?) | x about 3.10 (S) | intercom x 2.60..2.70 h 1.30..1.48 | about -45 | Mismatch, weak; 3.10 collides with the art at x 2.86..3.26 | L906 |
| Blue symbol "1" by the door | x about 2.09, in the door width (S) | none | | Unidentified | |
| Switch 1bc (+ black triangle) | entry W wall x 1.45 face 'e', z about 3.0 (triangle about 3.37) (S) | none (console at z 3.00..4.20, h 0.80) | | Missing | |
| Kitchen switch 1d | wall z 5.50 face 'n', x about 4.11 (S) | none | | Missing (below the art at x 3.82..4.22, h 1.305+) | |
| Kitchen point 1d | (5.88, 6.51) (W: 140 from FX, 228 from S wall 8.79) | island pendants (5.87, 5.95) and (5.87, 6.67), centre z 6.31 | x -1, z -20 | Pendant pair x OK; centre 20 cm north. "חשמל מטבח עפ חברת מטבחים": kitchen layout by the kitchen supplier | L1238 |
| Kitchen downlights | not on plan | (4.6, 6.2), (4.6, 7.6), (6.6, 7.9) | | Extra | L952 |
| South living downlights | not on plan | (4.6, 4.2), (6.4, 4.2) | | Extra | L952 |
| Kitchen plate W wall (3.645, 8.13) | kitchen supplier | plate | | Not checkable | L1213 |
| Kitchen-window shutter switch 1p | FX inner face, pier 6.88..7.70, z about 7.15 (S) | none | | Missing | |
| Lobby items (FS, 25ø, meters "1050 1050", VE by the stair) | stair hall, outside the flat | | | Out of scope | |

## Balcony and facade pier (crop `balcony.jpg`, `overview.jpg`)

Scale here calibrated on the two piers (z 3.855 and 7.29 in the model): 57.6 px/m on the overview, consistent with
the rest of the sheet.

| Item | Plan | Model | Diff | Verdict | Code |
|---|---|---|---|---|---|
| Ceiling points 1e (crossed circles, balcony) | about (8.05, 2.2) and (8.05, 5.7) (S), each in front of a door, about 35 cm out from the facade | soffit lights (8.75, 3.40), (8.75, 6.30) | +70, +120 / +60 | **MISMATCH** (scaled, but well outside tolerance) | L1638 |
| Balcony light switch 1e (+ triangle) | FX inner face, pier N end, z about 3.6 (S) | none | | Missing | L1636 |
| Shutter switches 1m, 1n | FX inner face, z about 3.81 / 4.09 (S, crowded) | 'rr' at 3.8075 / 3.8925 h 1.10 | 0 / -20 | OK (crowded) | L1636 |
| Socket 1, living side of pier | z about 3.86 (S) | 's' at 3.85 h .40 | -1 | OK | L1636 |
| Outdoor socket 1 (with ▷), balcony face of pier | z about 3.87 (S) | box (FO, 3.85) h .40 | -2 | OK | L1639 |
| Motors 1m, 1n, 1p | door A, door B, kitchen window | rails z .78..3.45, 4.26..6.88, 7.70..8.39 | | OK | L1635 |
| Ceiling fan | not on plan | (9.30, 1.55) h 2.70 | | Extra | L1550 |
| Facade wall lights | not on plan | (FO, 3.82), (FO, 7.3) h 1.9..2.1 | | Extra | L1644 |

## On the plan, missing from the model

1. Living ceiling point 1b (4.98, 2.00) (W). Entry point 1a (2.10, 4.50) (W). Dining point 1c (1.27, 1.305) (W,
   storage-wall decision).
2. Living TV-wall outlets at h=40 and h=130 with the 50ø conduit (S).
3. Switches: mamad door 3a; entry 1bc on x 1.45; kitchen 1d on z 5.50; closet 2c; ensuite 2b + 13 outside the door;
   balcony 1e on the pier; kitchen-window shutter 1p; master bed-head two-way 2a; family-bath cluster has 3 switches
   (2ef, 4, 12) where the model has one plate.
4. Bathrooms: heaters 12 (family bath) and 13 (ensuite) at h=200; sockets "2" h=110 in both; splash-proof socket 9;
   washer and dryer sockets 7 and 10 at h=140; IP65 isolators in the laundry niches.
5. Corridor: blue FO at x about 3.97; "A" and double socket near the panel.
6. Boxed "א" + "25" in rooms 1, 2, the mamad and the master (h=60 in the master).

## In the model, not on the plan

1. Downlights: living 5, south living 2, entry 2, kitchen 3, rooms 1 and 2 two each, mamad 2, master 4, ensuite 3,
   family bath 2 (plan has one point 2f), laundry niche 1. The plan has one ceiling point per room.
2. Ceiling fans use the room points (fine) plus the balcony fan (no point there).
3. Master pendants over the nightstands; plate behind the master TV; balcony facade wall lights.
4. Corridor plates at x -1.15 and x 1.86 on the north wall.

## Unreadable or unidentified

- Family bath 2f distance from the window wall: label not legible; scaled 62 to 70 cm.
- The item labelled "1?" at the TV-wall jog (x about 4.6) is hidden behind the black wall fill.
- No legend in the photo, so these stay unidentified: blue "FO", "E", "U/ט", "VE", "S", "A", "A-5", "FS"; the boxed
  "א" with "25" (25 may be a conduit size); the black triangle next to switches 1bc, 1e, 3c and at the living SE
  corner (a pilot-lamp marker or wall light are guesses).
- Panel position: this sheet (x about 3.01..3.40, scaled) and the sales plan (3.37..3.78) disagree. Needs the
  contractor or a site measurement.
- Notes outside the walls: "FE-12ø" bonding and "טבעת גישור הארקת ברקים בקומה 3 בלבד" (lightning ring on floor 3
  only); "קומות 1-3" box in the living room. Not modelled, not relevant to the interior.

## Proposed code changes (written evidence first)

| # | Line | Now | Proposed | Evidence |
|---|---|---|---|---|
| 1 | L953 | `[-0.8, -0.70], [1.3, -0.70], [3.3, -0.70]` | `[-1.07, -0.665], [1.03, -0.665], [3.13, -0.665]` | W: 105, 210, 210, 58 |
| 2 | L954 | `[7.9, -4.2]` | `[7.63, -3.80]` | W: 120, 128 |
| 3 | L1620 | `outlets('n', -.19, 7.90, .60, 'sd')` | `outlets('n', -.19, 8.06, .60, 'sd')` (socket at 8.02); optional bed-head two-way switch | W: 89 |
| 4 | L1258 | `ceilingFan(6.6, -1.75, ...)` | `ceilingFan(6.53, -1.745, ...)` | W: 150, 218 |
| 5 | L1478 | `ceilingFan(-2.0, 1.5)` | `ceilingFan(-1.89, 1.505)` (caveat on room width) | W: 183, 135 |
| 6 | L1405..1410 | mirror cabinet z -2.605..-1.765 | shift +0.07 (z -2.535..-1.695) to centre on 2e, if clearance allows | W: 72 |
| 7 | L944 | `['n', -1.425, -1.22]` | `['n', -1.425, -2.18]` | S, latch side clear |
| 8 | L1621 | `outlets('w', 8.91, -1.15, 1.10, 'r')` | `outlets('w', 8.91, -2.45, 1.10, 'r')` | S, side of window clear |
| 9 | L943 | `['s', -1.245, 3.78]` | `outlets('s', -1.245, 2.70, 1.10, 'kkk')` (2ef, 4, 12) | S, latch side |
| 10 | L943 | `['s', -1.245, -1.15]` | `['n', -.145, 0.18]` | S |
| 11 | L943 | `['n', 5.50, 1.53]` | `['n', 5.50, 2.76]` (under the intercom) | S, latch side |
| 12 | L1638 | `[[8.75, 3.40], [8.75, 6.30]]` | `[[8.05, 2.2], [8.05, 5.7]]` | S |
| 13 | L954 | `[2.8, -2.6], [3.6, -2.6]` | `[3.01, -3.10]` | W x, S z |
| 14 | new | | plates: mamad door `('s', .125, -1.10)`, closet `('s', -3.105, 8.40)`, ensuite `('e', 7.01, -4.17)` 'kk', entry 1bc `('e', 1.45, 3.0)`, kitchen 1d `('n', 5.50, 4.11)`; L1636 `'rr'` to `'krr'`; kitchen-window `outlets('w', FX, 7.20, 1.10, 'r')` | S |
| 15 | new | | heaters h=2.00: family bath on z -1.395 at x 2.77, ensuite on x 6.85 at z -4.3 | S |

Not proposed without a decision: living point 1b and TV-wall outlets (TV and lighting design), panel position
(drawings disagree), removal of extra downlights, pendants and fans (design choices), row-centring offsets of
4.25 cm in rooms 1 and 2 (dim may target the group).

After any wall-adjacent change run `roomdims.py` and `clearance_audit.py`; none of the above moves a wall.
