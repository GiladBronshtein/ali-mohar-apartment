# QA9: full pass before the architect's review (2026-10-07)

Six report-only review agents went over the whole flat, day and evening, doors open and closed, against the plans and the
spec (d08, d10, d11, d07): `A_living_kitchen.md`, `B_bedrooms_corridor.md`, `C_baths.md`, `D_electrical_hardware.md`,
`E_doors_windows_spec.md`, `F_floors_claddings.md`, with their evidence images in the `*_img/` folders. The lead applied
the "fix now" items in staged commits; after each one `roomdims.py` +0, `clearance_audit.py` 0 issues, `sitetest` (GPU
variant) no issues, phone emulation 60 fps.

Capture tool: `source/out/shots.mjs` (camera list in JSON, day/eve, doors and curtains), always through `/tmp/gpu.sh`.

## Applied

- Before the agents (owner's screenshots): baked AO off by default (seams between meshes, `?ao=1` keeps it); door frames
  rebuilt to the spec door (d10 item 5, Pandor PanClassic profile).
- Stages 1-3: probe only on metals, glass, screens and sanitaryware (white fronts, stone and plates were beige); balcony
  sofa cushions; corridor light box; our plaster and the balcony soffit; kitchen sockets, hob-return stone, no dishwasher
  bar; entry wall spacing, rocker marks; curtain 2 clear of the pier switches; railing 11 cm pitch; sliders sash on sash;
  deeper sills; kip handle; master shower reveals tiled; roses, escutcheons, hinges, bath turn locks; Garda entrance
  hardware (d10 item 4); room light boxes reach the closed leaves; laundry screen and outside sills on every floor;
  heaters, paper holder and switches clear of the casings; low book stacks at the bed heads; bedside light at the globes;
  spots out of the fan sweep; tub 40 cm deep; ladders and hooks; accent tile; bath door at 85 deg; pipes; shower channel.
- Stage 4: sun occluder over the ceiling (light line under every ceiling); window lights behind the curtains; open leaves
  on the jamb line; odd wardrobe door handles; mamad seat, blind; hamper; slat backing; blast-door hinges and bars.
- Evening: light under the kitchen wall cabinets; downlight points lower; softer pendant on the storage doors.
- Baths: both niches are real recesses (walls cut, not moved).
- Floors: skirting on every wall that lacked it (entry wall, corridor TV-wall stretch, passage returns, master step, stub,
  under window C) and on the finished floor (7 cm visible); room 1 planks and mamad threshold; corridor grid without the
  4.5 cm sliver; spec-pick grid origins; master daylight into the closet; sage to the glass.

## For the owner (not on a plan, or a design choice)

1. Master TV hangs toward the door corner, 1.27 m off the bed axis; the plan's TV point is on the axis (B1, D16).
2. Rooms 1 and 2 windows (15 cm sills) have no fall protection; the master has outside bars (B2). Which window is the
   escape window?
3. Shower door: the slider opens 46-49 cm (usual 55-60) (C-B).
4. Tub: the picker says 160x70, 157 cm fits between the tiles; the construction sheet writes a longer room (C-C).
5. Roma vanity in the master (shown 70 wide) puts the basin 9 cm off the axis: drop it from the options or accept (C-D).
6. Master shower floor: large tiles to a point drain cannot fall as drawn; spec small tiles or a linear drain (C-E, F-D4).
7. Insect screens (d10 item 6) are in the contract but not drawn (E-M6).
8. Interior door hardware finish: matte black in the model; the spec names nickel only for the entrance (E).
9. Entrance door's grooved outer face would need a slice of the landing (E).
10. Mamad AC: d10 item 11 lists the mamad, the model shows no grille (E); no AC wall controller is shown (D19).
11. Electrical symbols still not modelled: boxed "א" marks, living cones and "S" box, entry chime, "16" point, master
    audio intercom (D20).
12. Water heater switch: moved beside the heater (reachable); Israeli practice often puts it inside the flat (D18).
13. Balcony-side island seats leave about 0.4 m behind a seated diner (A-O1); window C type not written (A-O2).
14. Default bath wall tile rows from the floor leave a 5 cm strip over the master shower window (F-D3).
