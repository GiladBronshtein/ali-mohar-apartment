# QA10: final verification (2026-10-07, night)

Owner: "verify everything"; sizes and everything follow the plans; studio and addendum alternatives are choices in the picker.
Three independent report-only verifiers: `V1_plans.md` (every door, window, wall, fixture and electrical point against the
construction, plumbing, electrical and AC sheets), `V2_options.md` (all 163 fixture and 551 ceramic options), `V3_visual.md`
(fresh-eyes pass, edges and endings). Evidence in `V*_img/`. Applied in three commits; after each: `roomdims.py` +0,
`clearance_audit.py` 0, `sitetest` no issues, phone 60 fps.

Before the verifiers: door swings checked against the construction plan (all seven match); a ray scan of every wall base for
skirting gaps (`audit/qa9/F_scan/fscan.mjs bases`); new picker choices: splash height, insect screens, door hardware, acrylic sink.

## Applied

- Regression: the north facade from x 6.015 to 9.30 was missing since `40e8d72` (a comment swallowed six wall calls);
  restored, and `roomdims.py` now strips comments so it fails on such a wall.
- To the plans: window C one inward sash hinged at the north jamb (blind on the sash); single-sash handles on the latch side;
  entrance centred on the written 105; master bath door 75; room 2 door and closet opening on the written chains; laundry niche
  edge; shower head over the 4-way mixer; niche drain pipe and isolator; second condenser on its AC outline; balcony drains;
  water-heater timer switch in the family bath door group; 2-gang 1bc and 1ad; bath socket; access hatch; room 1 socket.
- Visual: stone under window C; family bath evening light; flush hamper front.
- Picker: top-mount sink throat, silquartz grey, bath tap view, neutral metals in the baths, grid origins (shower and master
  bath walls, splash, family bath floor), marble veins, screen mesh, Oakland slats, square mixer lever.

## For the owner

1. Water-heater IP65 point: the plan puts it between the heater and the wall, where it cannot be reached; the model has it
   beside the heater (the timer switch is now also by the bath door, as on the sheet).
2. Balcony skirting: none on the wood deck (normal); a tiled balcony pick would want one.
3. Shower niche height (an estimate) leaves 2-3 cm tile rows with some spec tile sizes; it could follow the tile module.
4. With the 50 cm splash picked, a ceramic splash pick also stops at 50 cm (d10 item 1 names stone).
5. Window C's zebra blind is now on the sash (an inward sash would hit a blind in the reveal).
6. QA9 questions still open (`audit/qa9/README.md`): master TV off the bed axis, rooms 1-2 fall protection, shower door width,
   tub 157 vs 160, Roma vanity, shower floor drainage, mamad AC, unmodelled symbols, island seating.
