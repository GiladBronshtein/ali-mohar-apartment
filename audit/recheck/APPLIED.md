# Blueprint re-check: what was applied (2026-10-04)

Sources: `materials/plans/originals/` (full-resolution photos of the HADA electrical, plumbing and AC sheets, 1:75 on
A3, and the coloured sales plan) and `materials/plans/` (sales plan PDF). Evidence and crops: `geometry.md`
(`geo_crops/`), `electrical.md` (`el_crops/`), `plumbing_ac.md` (`pl_crops/`). Those three reports end with
"proposed changes"; this file records which ones went into `source/salon.html`.

"Written" means a number on a sheet; "scaled" means measured from the photo or PDF, accurate to a few cm.

After the changes: `roomdims.py` +0 on every room (closet 485/175 is the known probe artifact), `clearance_audit.py`
0 issues, `sitetest.mjs` no issues on desktop and phone.

## Applied

### Geometry (geometry.md)

| Item | Before | Now | Basis |
|---|---|---|---|
| Entry door opening | x 1.62..2.52 | 1.585..2.555 (97), hinge west, handle east | scaled, plus the door symbol |
| Room 2 door opening | x 0.88..1.76 | 0.93..1.76 (83), leaf .82 | scaled |
| TV wall, corridor stretch x 2.97..4.15 | 14.5 cm | 19 cm; corridor panel, comms box and display moved with the face | scaled (item 5.3) |
| Balcony north wall | BZ1 .30 | .34 | scaled |
| Ensuite WC axis, room 1 west facade, balcony south wall | | unchanged, model was already right | items 5.1, 5.2, 5.4 |

### Plumbing and AC (plumbing_ac.md)

| Item | Now | Basis |
|---|---|---|
| Family-bath tub | 70 wide (x 3.76..4.46), mixer, spout and rail on the corridor (south) wall, screen at the tub's west edge | written 70, taps from the symbol |
| Family-bath basin and mirror cabinet | axis 72 from the wall (centre z -2.115) | written |
| Ensuite drain | point drain at about (4.97, -4.48), replaces the linear drain | symbol |
| Ensuite basin, tap, mirror | axis moved 4 cm | written 44 |
| Room 1 and room 2 AC grilles | combined 80x20 grille in an 85x25 opening | written |
| Living AC grilles | centres x 2.20 and 5.75, 90x15 | scaled, size written |
| Mamad 8" sleeves | x -1.55 and -0.95, over and east of the blast door | scaled |
| Mamad 4" relief sleeve | added at x -0.52 (symbol meaning not certain) | scaled |
| Laundry niche floor drain | added at (3.85, -4.31) | symbol |
| Balcony drains | (9.05, 1.5) and (9.08, 7.3) | scaled |
| Garden tap | h = 60 | written |

### Electrical (electrical.md)

| Item | Now |
|---|---|
| Switches | moved to the latch side; added room 2, TV wall, entry (east of the door, under the intercom), mamad door, closet, entry 1bc, kitchen 1d |
| Room 1 switch | z -2.18 |
| Family-bath and ensuite socket clusters | `kkk` at h 1.10 on the corridor face, `kk` in the ensuite |
| Master bed-head socket, master shutter switch | x 8.06; shutter switch on the west wall |
| Kitchen pier | `krr`, plus the kitchen-window shutter switch |
| Corridor spots | (-1.07, 1.03, 3.13) at z -0.665 |
| Closet spot, family-bath spot | (7.63, -3.80); single spot at (3.01, -3.10) |
| Ceiling fans | master (6.53, -1.745), room 2 (-1.89, 1.505) |
| Balcony soffit lights | (8.05, 2.2), (8.05, 5.7) |

### Audit script

`clearance_audit.py` follows the new geometry (front door, room 2 door, tub). Two limits changed:
- "entry commode face <-> door opening edge": -.15 to -.17, because the wider opening moved its east edge 3.5 cm. The
  commode still clears the leaf ("entry commode end <-> door leaf" passes).
- Added "corridor at the panel (TV wall 19 cm)", minimum .90; it measures 105.5.

## Not applied (open)

- Column 2: the plumbing and sales sheets put it in different places.
- Column 1 at about (4.08, -5.1): not modelled.
- Electrical panel x: electrical sheet 3.01..3.40, sales plan 3.33..3.78. The model follows the sales plan.
- Niche condenser: the AC sheet outline is 132x55; the modelled unit is 89x34. The outline may be a platform.
- Water heater: about 11 cm north of the model on one sheet only.
- "H=2.63" near the mamad: possibly its ceiling height, not labelled as such. Ceiling stays 2.60 (estimate).
- Living, entry and dining: the sheet shows single ceiling points; the model keeps downlights (design choice).
- TV-wall outlets at h 40/130, master TV position, splash socket 9, sockets "2", bathroom wall heaters 12 and 13,
  washer/dryer sockets (hidden inside the cabinet): not modelled.

## Next re-check

Re-run from the originals, not from this file. Use the same method: calibrate each sheet per axis on two written
dimensions, compare wall faces to a neighbouring face (the PDF registration has a constant 2 cm offset), then check
`roomdims.py`, `clearance_audit.py` and `sitetest.mjs`.
