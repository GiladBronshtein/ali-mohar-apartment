# QA9 D: electrical and hardware, whole apartment

Report only. Scope: switches, sockets, TV/data points, plates, panel and comms box, intercom, AC (split, grilles,
sleeves, isolator), light fixtures and the lights behind them, door/window hardware, curtain rails.

Sources: `materials/plans/vector/electrical.pdf` read through `audit/recheck3/electrical.md` (sheet coordinates,
spot-checked on `recheck3/el_crops/00_overview.jpg`, `20_*`, `21_*`, `70_*`), sale spec table 5 (d08 §3.7) and the
addendum (d10 items 4, 10, 11). Model: `source/salon.html` as served on :8791 on 2026-10-07.

Method: (1) inventory from the code; (2) a ray test in the live page for every item (inward ray: does the plate sit
on the finished face; outward rays, 5 per item: is anything within 1.2 m in front of it), script `/tmp/qa9_ray.mjs`,
items `/tmp/qa9_D_items.mjs`, output `/tmp/qa9_ray.json`; (3) a casing-overlap calculation for every item beside a
`FRAMES` door (`/tmp/qa9_cas.py`); (4) 73 close-ups day/eve, doors and curtains open/closed (`/tmp/qa9_D/`, the
ones cited are copied to `audit/qa9/D_img/`).

**The lead edited salon.html while this ran.** Already fixed during the audit (verified in the second ray run and
shots 62/63/69/70): plates no longer take the living-room probe (`PROBE_GLOSSY` line 2553, they were beige/taupe:
`P1_panel_probe.jpg` vs `P1_panel_noprobe.jpg`); curtain 2 now gathers over door B, so the pier switches are visible
(line 1254); switches got a rocker mark; entry switch 2.68, intercom 2.76..2.86 with the prints moved east (6 cm gap
now); kitchen service sockets (line 1525), Ninja double socket, robot-dock socket; two living spots by the wave pendant
removed; entrance door hardware rebuilt in brushed nickel with cylinder rose and peephole (line ~1171, finding 17).
Shots 02, 05, 06, 09, 13, 14, 18, 21, 22, 24 were taken before the probe fix, so their plates look beige.
**Line numbers are approximate**: the file grew about 20 lines during the audit (e.g. the SW2 list moved from 1204
to 1213, the bedside lights from 2694 to 2713). Every finding quotes the exact code string, so search for that.
None of findings 1-15 was fixed at the time of writing.

## 1. Inventory vs plan and spec

Heights in brackets are estimates (not written on any sheet). "Plan" = electrical sheet as read in recheck 3.

| Room | Model (code) | Plan | Spec d08 table 5 (+ d10) | Verdict |
|---|---|---|---|---|
| Entry | switch 1ad x 2.68 h(1.10); intercom 10x18 x 2.76..2.86; 2 black downlights + picture-rail LED | 1a ceiling point, 1ad at the jamb, VE at x 3.11, blue box "1" over the door | 1 light, intercom with B/W monitor | OK. VE 30 cm west of the sheet (prints in the way, design). Chime "1" not modelled |
| Living | 1bc switch (1.45, z 3.0); pier `krr` + socket h40; 1p `r` z 7.20; 10 downlights, wave pendant, flush frames; 2 grilles 90x15 | 1b, 1c points; 1bc, 1e/1m/1n/1p; pier socket; TV-wall row h40, socket+box h130, dining socket and phone h40 | 3 lights, 3 sockets, 1 TV, 2 phone | TV-wall and dining points hidden behind the media base / storage wall (not drawn, acceptable). Only one living socket is visible. Cones and "S" box not modelled (open) |
| Kitchen | 1d switch x 4.17; island socket h(.70) (d10); service sockets S wall x 3.83, 4.50 (ss), W wall coffee niche, Ninja ss x 8.22; frames pendant | 1d, ceiling 1d; "per the kitchen company" | 2 lights, 1 socket, 3 separate-circuit, 1 phone; d10: island socket, 3-phase hob point | OK (hob point hidden). Phone point not shown |
| Corridor | 3c switches x 0.18 and 3.18; socket h40 x .65; panel, comms box, display, ss h(1.15), FO h(.40); 3 cylinders; return grille 80x60 | 3c x2, socket "3", panel, box, display, x2, FO, 3 ceiling points 3c, "16" point | 2 lights | West 3c about 15 cm east of the sheet symbol (low). "16" point not modelled |
| Room 1 | `sd` h40, `dst` h180, bed-head `sk` h65, shutter `r` z -1.80, door switch -2.18; fan + 2 spots; grille 80x20 | same | 1 light, 2 sockets, TV, phone | Positions OK; see findings 5, 9 (curtain, books) and 12 (spot in the fan sweep). Boxed "א" open |
| Room 2 | `ksr` h65 x .02, `sd` h40, `dst` h180 z -2.86, door switch .80; fan + 2 spots; grille | same | same | `dst` inside the bookcase, `k` behind the headboard (findings 6, 7); spot in the fan sweep |
| Mamad | `dst` h180, `sd` h40, `sk` h65 z 1.59, filter socket h220, door switch -1.10; fan + 2 spots; 2 x 8" sleeves, 4" relief valve; filter unit | same | 1 light, 3 sockets, TV, phone, per civil defence | Door switch behind the bookcase (finding 4); `sd` behind the bed (low) |
| Master | bed heads `ds` / `ksd` h60 on the slats, TV `std` h180 x 6.93, shutter `r`, door switch (4.42, -1.245), closet switch 8.40; fan, 4 spots, bedside globes; split 12,000 BTU over the door | same; "E" at the west bed head; "16" point | 1 light, 2 sockets, TV, phone, intercom audio only | Books hide the bed-head plates (finding 9); bare TV point beside the TV (owner); "E" drawn as a data plate |
| Closet | `kk` (bath light + heater 13) z -4.20; spot (7.63, -3.80); LED cove | 2b/13 at z -4.14, 2c | | `kk` overlaps the bath door casing (finding 3) |
| Master bath | splash socket h110 x 4.72; heater 13 h(1.90-2.10); mirror-cabinet LED; 3 spots | 2b mirror light, socket, heater 13 h200 | 1 light, 1 socket, heater prep | Heater intersects the door casing (finding 2); socket half buried in the tile (finding 13) |
| Family bath | `kkk` outside x 2.66; splash socket x 2.105 h110; heater 12 h(1.90-2.10); washer/dryer h140; ceiling spot at BC, hatch 60x60 | 2ef/12/4 group, socket h110, heater 12 h200, 7/10 h140, "9" 3-phase | 1 light, 1 socket, 2 separate, heater prep | Heater intersects the casing (finding 2); hooks collide with the towel ladder (finding 8) |
| Laundry niche | isolator 3x16A IP65 (2.15..2.20, z -4.88) h(1.10); heater switch IP65 (4.32..4.37, z -4.84) h(1.10); spot | 9 3x16A IP65, 4 IP65 | electric/solar heater point | Heater switch is boxed in behind the water heater (finding 10). Spot not on the plan |
| Balcony | 2 soffit lights (7.96, 2.14)/(7.96, 5.73); IP socket box z 3.89 h(.40); `st` z 4.12 h(.40) (d10); 2 wall sconces; fan | 2 x 1e, socket at z 3.93 | 1 protected light, 1 IP44 socket; d10 + socket + TV | OK. Sconces are extras (design) |

Light sources vs fixtures: 14 warm point lights checked against their fixtures. All have one within about 20 cm,
except the two bedside globes (finding 11) and two fill lights with no fixture above them: the master bath
(5.6, -4.2), 44 cm from the nearest spot, and the family bath (3.2, -2.6) at h 1.65 (low).

Plates on the finished face: every plate's back sits on the face it is mounted on (inward ray hit at 0), with none
floating or buried in plaster. The exceptions are the two bath sockets, which go 6 mm into the tile skin (finding 13).
Skirting and splash edges cut nothing.

## 2. Findings, ranked

### Fix now (safe; positions follow the plan or are design estimates)

**1. HIGH: room 2 curtains hang about 20 cm in front of their track and run into the nightstand.**
Evidence: `D_img/60_room2_window_head.jpg` (track at the window head, curtain tops on the bare ceiling in front of it),
`61_room2_window_closed.jpg`, `21_room2_bedhead.jpg`. Cause: lines 1801-1803 sit inside `withShift(.15, -.20)`.
The track (a `B` in `root`) gets shifted to x .32..1.29, z -4.935..-4.885. `curtainPair` moves the curtains into
`curtGroup`, which `withShift` does not touch (line 651: it only shifts `root`, `ceilGroup`, `fanGroup`), so they stay
at z -4.72, x .195..1.18. The open stack at x .195..0.435 passes through the nightstand (x .02..0.27, z -5.01..-4.63),
and the closed pair stops 8.5 cm short of the east jamb.
Fix: give the four `curtainPair` calls world coordinates on the shifted track, narrowed to clear the desk
(x 1.24..1.84, z -4.98..-3.78):
`curtainPair(curtOpen, 'x', .345, .565, -4.92, ...)`, `curtainPair(curtOpen, 'x', 1.02, 1.235, -4.92, ...)`,
`curtainPair(curtClosed, 'x', .345, .80, -4.92, ...)`, `curtainPair(curtClosed, 'x', .76, 1.235, -4.90, ...)`
(other arguments unchanged), and shorten the track to `B(.17, 1.09, -4.735, -4.685, ...)` (shifted: .32..1.24).
Then check with `"curtains":"closed"`.

**2. HIGH: both bathroom wall heaters intersect the new door casings.**
Evidence: `67_mbath_door_heater_close.jpg`, `68_fbath_heater_close.jpg`, `11_mbath_heater.jpg`, `12_fbath_doorwall.jpg`.
Cause: line 2016. Heater 13 is `B(6.77, 6.85, -4.46, -4.08, 1.90, 2.10)`; the master-bath casing (bath side, 7 cm)
runs over z -4.109..-4.039 up to 2.149, so 2.9 cm of the heater sits inside the casing. Heater 12 is
`B(2.45, 2.85, -1.475, -1.395, ...)`; the family-bath casing covers x 2.811..2.881, a 3.9 cm overlap. This is a
regression from 6241532 (casings 6 to 7/8.5 cm).
Fix: heater 13 to `B(6.77, 6.85, -4.50, -4.12, 1.90, 2.10, ...)` (centre -4.31, 6 cm from the scaled plan centre);
heater 12 to `B(2.40, 2.80, -1.475, -1.395, ...)`. Optionally the paper holder (line 1636 area,
`B(6.77, 6.85, -4.19, -4.11, ...)`, 1 mm from the casing) to z -4.25..-4.17. Heater sizes are estimates.

**3. MEDIUM: two switch plates are partly buried in door casings.**
Evidence: `70_corr_sw2_close.jpg`, `01_corr_sw2_room2door.jpg`, `69_closet_kk_close.jpg`, `10_closet_kk.jpg`.
- `['s', -1.245, 1.86]` (line 1204): the plate covers x 1.82..1.90 and the room-2 corridor casing ends at 1.834, a
  1.4 cm overlap. This switch is **not on the electrical sheet**: it is the original model's corridor-side room-2
  switch (aae2b0f), kept when the inside switch 2d (0.80) was added. Fix: delete this entry from the list.
- `outlets('e', 7.01, -4.20, 1.10, 'kk')` (line 2013): the plates cover z -4.2825..-4.1175 and the master-bath
  casing on the closet side ends at -4.124, a 0.6 cm overlap. Fix: centre `-4.22` (1.35 cm clear; the wardrobe front
  at -4.395 stays 9 cm away).
- The family-bath `kkk` (x 2.535..2.785) clears its casing (2.796) by only 1.1 cm. OK, but it looks tight.

**4. MEDIUM: the mamad door switch is behind the bookcase.**
Evidence: `06_mamad_sw5.jpg`, `64_mamad_sw5_close.jpg` (plate edge peeking out behind the side panel). The ray hits
the bookcase front 4 cm in front of the plate. Cause: lines 1821-1823, a bookcase at local x -1.03..-0.2 shifted by
-0.08, so world x -1.11..-0.28, over the switch at x -1.14..-1.06 (switch 3a on the sheet at about x -1.12, so the
switch is right).
Fix: narrow the bookcase from its west side: in lines 1821-1823 change `-1.03` to `-.95` (four places), the side
panel `B(-1.03, -1.01, ...)` to `B(-.95, -.93, ...)`, and the books' x `-.95` to `-.87`. World west edge -1.03,
plate 3 cm clear.

**5. MEDIUM: the room 1 shutter switch is behind the open curtain stack.**
Evidence: `19_room1_shutter_sw.jpg` (switch invisible). The ray hits linen 9 cm in front of the plate. Cause: line
1990, `outlets('e', -3.89, -1.80, 1.10, 'r')` covers z -1.84..-1.76; the open stack (line 1792 area) spans z
-2.13..-1.79 at x -3.82. Fix: `outlets('e', -3.89, -1.66, 1.10, 'r')`. That is 12 cm from the scaled 3m symbol,
and the wall runs to -1.425.

**6. MEDIUM: the room 2 TV group is hidden inside the bookcase.**
Evidence: `22_room2_east.jpg`, `76_room2_tvpoint_bookcase.jpg`. The ray hits the bookcase front 3 cm in front of the
plate. Cause: line 1992, `outlets('w', 1.85, -2.86, 1.80, 'dst')` sits behind the bookcase back panel
(`B(1.67, 1.69, ...)` shifted: x 1.82..1.84, h .8..2.0), between shelves 1.60 and 1.98.
Fix (plan position kept, mounted through the back panel as a joiner would): `outlets('w', 1.82, -2.86, 1.80, 'dst')`.

**7. MEDIUM: the room 2 bed-head group is half behind the headboard and the books.**
Evidence: `21_room2_bedhead.jpg`. Cause: line 1992, `outlets('s', -5.01, .02, .65, 'ksr')` puts the switch at
x -.105..-.025, behind the headboard (to x -0.01), and the shutter switch behind the nightstand books. The sheet
spreads the group over x -0.01..0.46 (schematic). Fix: centre `.20` (plates .075..0.325, 4 cm clear of the window
jamb at .365, and clear of the moved curtain in finding 1), together with finding 9.

**8. MEDIUM: the family bath towel hooks collide with the heated towel ladder.**
Evidence: `63_fbath_hooks_close.jpg`, `35_fbath_splash.jpg`. Cause: line 1740 puts hooks at x 2.32, 2.47 and 2.62,
h 1.08-1.12 (knob at z -1.425). Line 1742 puts the ladder at x 2.42..2.76 with a rung at y 1.11-1.124, z
-1.418..-1.402, so two hooks go through the top rung. Fix: two hooks at `[2.24, 2.34]` (9 cm from the socket at
2.145, 7 cm from the ladder rail at 2.42), or drop the hooks (the ladder holds the towels).

**9. MEDIUM: nightstand books stand in front of every bed-head socket (master both sides, room 1, room 2).**
Evidence: `13_master_bedhead_W.jpg`, `14_master_bedhead_E.jpg`, `18_room1_bedhead.jpg`, `51_master_bedside_eve.jpg`.
The ray finds books 13 cm in front of the plates. Cause: line 861 in `nightstand()`,
`books(P, hx - .2, .5, 0, .16, 'x', 4)`: four upright books 15-25 cm tall on a .50 top, in front of plates at
.56-.69 (plan h=60/65, written). Fix: a low flat stack at the far end:
`books(P, hx - .14, .5, .06, .08, 'stack', 3)` (about 10 cm high; eye-level sightlines clear the plates).

**10. MEDIUM: the water heater switch (IP65) is boxed in behind the water heater.**
Evidence: `31_niche_heater_sw.jpg`. The ray hits the heater 8-15 cm in front of it. Cause: line 1769,
`B(4.32, 4.37, -4.90, -4.78, ...)`; the heater (r .27 at (4.04, -4.69)) reaches x 4.31, leaving a 1 cm gap. The sheet
does draw "4 IP65" here, beside the heater circle. Fix (same wall, reachable): `B(4.32, 4.37, -4.31, -4.19, 1.13, 1.27, ...)`.
The height is an estimate. Owner may prefer it inside the flat; see section 3.

**11. LOW-MEDIUM: the bedside globe lights glow 20 cm away from their globes.**
Evidence: `51_master_bedside_eve.jpg` (the hotspot on the slats sits beside each globe, toward the headboard). Cause:
line 2694 puts the point lights at (5.64, -.48) and (7.92, -.48), but `pendantGlobe` is inside
`withShift(.20, .10)` (line 1563), so the globes are at (5.84, -.38) and (8.12, -.38). Fix: `[[5.84, -.38], [8.12, -.38]]`.

**12. LOW-MEDIUM: a downlight sits inside the ceiling-fan sweep in rooms 1 and 2.**
Evidence: `43_room1_ceiling.jpg`. Cause: line 1214, spots (-2.5, -3.8) and (.45, -3.8). The fans are at (-2.51, -3.21)
and (.45, -3.20) with blade tips at r .68 (blade .56 centred .40), so each spot is .59-.60 from its fan centre: under
the blades, which strobe in use. An architect would flag it. The spots are not on the plan (estimate). Fix:
(-2.5, -4.25) and (.45, -4.25), about 1.05 from the fans. The mamad (.73/.87) and master (over 1.0) are clear.

**13. LOW: the bath splash-proof sockets go 6 mm into the tile skin.**
Evidence: `34_mbath_splash.jpg`, `35_fbath_splash.jpg`; ray: tile at +6 mm, plate front at +12 mm. Cause: line 2014
mounts both on the wall plane, and `tileX/tileZ` add a 6 mm skin. Fix: `outlets('n', -3.266, 4.72, ...)` and
`outlets('n', -1.401, 2.105, ...)`.

**14. LOW: two frames-pendant cables land on the bare ceiling past the canopy.**
Evidence: `42_island_pendant.jpg`, `66_island_pendant_ends.jpg`. Cause: line 1547, canopy z 5.66..6.96; the end
cables are at z 5.63 and 6.995. Fix: `B(5.83, 5.91, 5.60, 7.03, H - .03, H, ...)`.

**15. LOW: stale comment.** Line 2012 ("bed-head sockets + phone h=60 ... TV point h=180") sits over the `kkk`/`kk`
line. The real bed-head line is 2017. Fix: "bath switch groups: family bath 2e/2f/12 in the corridor, master bath
2b/13 in the closet (latch sides)".

### Needs owner decision (not on any plan, or a design choice)

**16. The master TV hangs 64 cm from its TV point.** Evidence: `09_master_north_tv_closetsw.jpg`, `48_master_tvplate.jpg`.
The `std` group at h1.80, x 6.85..7.02 (line 2018) is bare beside the TV (x 5.13..6.29, inside `withShift`, line
1575), and a blank 14x8 plate sits under the TV (line 1576). Already DESIGN in recheck 3. An architect will ask.
Options: hang the TV centred on the point (x 6.35..7.51, 3 cm from the closet opening at 7.54), or move the point
behind the TV (off the sheet).

**17. Entrance door hardware: fixed by the lead during the audit.** `65_entry_door_handle.jpg` shows the old
`mat.steel` block lever reading bronze. The current code (line ~1171) has a brushed-nickel plate, lever, cylinder rose,
peephole and latch (d10 item 4). Not re-shot. Still open, low: the interior bath doors have no privacy turn or
indicator.

**18. Water heater switch location** (with finding 10): Israeli practice often puts the heater switch (with timer)
inside the flat, by the bath door. The sheet keeps it in the niche. Choose between the niche wall (finding 10 fix)
and the corridor.

**19. AC wall controller.** d10 item 11 supplies a mini-central. No thermostat or controller is modelled. Recheck 3
reads the "S" box at x 4.73 on the living face of the TV wall as alarm prep or an AC controller. That spot is behind
the media wall. If the owner wants one shown, an estimate is a 12x8 white controller at h 1.50 beside the 1bc switch
on the core wall (x 1.45 face, z 3.15).

**20. Open symbols from earlier rechecks (still not modelled):** boxed "א" in rooms 1, 2, master and mamad; living
cones and the "S" box (alarm prep?); blue box "1" over the entry door (chime, d08 §3.7.3); "16" point at
(4.365, -0.18) (split feed, it would sit behind the split); master "E" (d08 lists an audio-only intercom in the
master; the model shows a data plate there).

**21. Small items (low):** the mamad `sd` (z 2.33, h .40) is behind the bed side (the ray hits the mattress at 7 cm;
it is usable as a bedside socket). The kitchen corner socket at x 3.83 has the vase (line 1526) 12 cm in front of
its lower edge. The west corridor switch 3c sits about 15 cm east of the sheet symbol (x 0.18 vs about 0.02). The
master-bath and family-bath fill lights have no fixture over them. The bed-head plates straddle slat gaps. The d10
balcony socket and TV plates are indoor plates next to the IP box (d10 says "regular", so allowed; one IP double box
would look tidier).

## 3. Checked and fine

Switches are on the latch side at every door (rooms 1 and 2, family bath outside, master vestibule, master bath
from the closet, mamad, entry), all at h 1.10. Room 1/2/mamad TV and low groups, master bed-head heights, splash
sockets and washer/dryer sockets (behind the stack, as in reality) are at the written heights. The master shutter
switch clears its curtain by 4 cm. The panel, comms box, display, x2 socket and FO point are in the sheet order. The
split clears the head casing by 9 cm. Room AC grilles 80x20 sit over the doors, the living grilles 90x15 are in the
bulkhead, and the return grille 80x60 is in the corridor drop. Mamad sleeves and the relief valve are fine (the valve
cover is partly behind the bookcase top from low angles). The wave pendant's cables are straight into the canopy; the
flush frames' rods reach the ceiling; the corridor, entry and balcony fixtures light up in eve (`52`, `53`, `54`).
Window levers are on every hinged sash. Plates sit on the finished face (no floating, none in plaster) and no socket
is cut by skirting or a splash edge.
