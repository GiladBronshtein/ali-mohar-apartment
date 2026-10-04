# Kitchen: supplier plan vs model (recheck3)

Read-only audit. Model = `source/salon.html` as of commit d6585e0 (line numbers below are from that file).
Coordinates: metres, x east, z south, y up, origin the living face of the TV wall. Plan values in cm unless marked.
Anything not written on a plan is an estimate and is marked "scaled" or "estimate".

## Sources and crops

| Source | What it gives | Crops (`ki_crops/`) |
|---|---|---|
| `materials/plans/vector/kitchen.pdf` (Regba, scanned A3, drawn sideways on the page) | Kitchen electrical and plumbing points, two wall elevations, notes | `ki_overview.jpg`, `ki_left_elev.jpg`, `ki_right_elev.jpg`, `ki_notes.jpg`, `ki_title.jpg`, `ki_zoom_drain_heights.jpg`, `ki_zoom_gas.jpg` |
| `materials/plans/vector/construction.pdf` (HADA execution plan, 1:50, 5/5/26) | Kitchen walls and window | `ki_construction_kitchen.jpg` |
| `materials/plans/vector/plumbing*.pdf` | Riser and drain in the kitchen wall | `ki_plumbing_kitchen.jpg`, `ki_plumbing_kitchen2.jpg` |
| `materials/plans/vector/electrical*.pdf` | Architect's indicative kitchen, ceiling point 1d, kitchen note | `ki_electrical_kitchen2.jpg` (`ki_electrical_kitchen.jpg` is an off-target first crop) |

## 1. What the supplier plan shows

### Title block and notes

| Field | Value |
|---|---|
| Supplier | Regba (רגבה) |
| Sheet title | "תכניות חשמל ואינסטלציה" (kitchen electrical and plumbing plans) |
| Project | Ali Mohar 6-8, Raanana, building A; handwritten "דירה 4 - בניין A" (apartment 4) |
| Date | planned and printed 05/03/2026; drawing 1 |
| Customer signature | blank (not confirmed) |
| Disclaimer | the drawing is for illustration and is not an exact rendering of the design |
| Note 1 | all dims in mm |
| Note 2 | heights from the finished floor |
| Note 3 | dims go to the centre of each point |
| Note 4 | three-phase socket installed horizontally, to the right |
| Note 5 | leave 1.2 m of pipe at the gas outlet |
| Note 6 | sockets in an island or by a floor-to-ceiling window: wires come out of the floor |
| Not written | materials, colours, counter depth, counter height, appliance brands or models, ceiling height |

### Layout

L-shaped kitchen on two walls, no island, no wall cabinets.

| Run | Modules, scaled from the drawing (cm from the corner) |
|---|---|
| South wall (left elevation, seen from the north, west wall at the right end) | corner return of the west run 0-58, filler about 10, sink cabinet 69-158 (about 90, sink centre about 113), dishwasher 158-218 (60), 3-drawer hob unit 218-303 (about 85) with a 4-burner gas hob 230-290 (centre about 260), end cabinet 303-363 (60) |
| West wall (right elevation, seen from the east, south wall at the left end) | corner return 0-58, filler to 68, double-door base 68-158, tall oven column 158-217 (60, built-in oven at about H 55-115), tall fridge niche 217-313 (side panel 8, clear about 88), end panel 312-320 |
| Heights (scaled) | plinth about 10, counter top about 89-90, tall units top about 216 (not to the ceiling), wall drawn about 269-270 high |
| Fronts | drawn with handles |

### MEP points (written on the sheet)

South wall, distance from the west wall; model x = 3.63 + d.

| Point (Hebrew label) | Written | Model x | Height |
|---|---|---|---|
| Service socket "שירות" | 200 | 3.83 | H 1100 |
| Drain "ביוב", pipe end up to 12 cm from the wall | 1000 | 4.63 | floor |
| Taps and dishwasher drain "מ.ברזים + פ.למדיח" | 1130 | 4.76 | H 500 |
| Protected dishwasher socket "ש.כח מוגן למדיח" | 1300 | 4.93 | H 600 |
| Hob ignition socket "הצתה לכיריים" | 2300 | 5.93 | H 600 |
| Gas outlet "יציאת צינור גז" | 3300 | 6.93 | about H 100 (scaled; the "100" dim reads as floor to plinth line, inference) |

West wall, distance from the south wall; model z = 8.79 - d.

| Point | Written | Model z | Height |
|---|---|---|---|
| Service socket "שירות" | 1250 | 7.54 | H 1100 |
| Microwave socket "למיקרו" | 1800 | 6.99 | H 1450 |
| Oven power socket "ש.כח לתנור" | 1950 | 6.84 | H 1450 |
| Fridge power socket "ש.כח למקרר" | 2900 | 5.89 | H 1700 |

There is no dedicated induction supply on the sheet (the hob is gas).

### Other sheets

| Sheet | Kitchen content |
|---|---|
| Construction (HADA) | kitchen 367 wide (written three times), 330 from the north face of the entry stub to the south structure, "10" inner layer on the south wall, facade "6 27", west wall 20 plus about 5 lining, stub about 9-10 thick ending 75 past the west wall line, total 884 TV wall to south (sales plan 879) |
| Plumbing | inside the kitchen only riser 3 "קולטן Ø110" (z about 7.49) and balcony drain 13 (z about 8.13) in the west wall shaft; no sink points |
| Electrical | architect's indicative kitchen: sink on the west wall, 4-burner hob near the east end of the south wall, island with 3 stools, ceiling point 1d (140 from FX, 228 from the south wall = x 5.88, z 6.51), shutter 1p, switch 1d on the stub; note "חשמל מטבח עפ חברת מטבחים" (kitchen electrics by the kitchen company), so the Regba sheet supersedes this sketch |

## 2. Item-by-item comparison

Verdicts: OK = matches; drift = within plan-to-plan scatter; owner = differs because of the owners' own design (group b); flag = worth a look, no change proposed here.

| # | Item | Plan value | Model value | Delta | Verdict |
|---|---|---|---|---|---|
| 1 | Kitchen width, west wall to facade | 367 (construction); 365 (sales plan); supplier frame scales about 370 | 365 (x 3.63 to FX 7.28) | -2 vs construction, 0 vs sales | drift; keep (roomdims rule) |
| 2 | Stub kitchen face to south wall | 320 (330 minus the 10 layer, construction); supplier west elevation scales 320 | 318 (z 5.61 to 8.79) | -2 | drift |
| 3 | TV wall to south wall | 884 (construction), 879 (sales) | 879 | -5 vs construction | drift; geometry topic (construction draws the TV wall about 10 thick vs model 14.5) |
| 4 | Entry stub length and thickness | ends 75 past the west wall line, about 9-10 thick | x 3.63-4.30 (67), z 5.50-5.61 (11) | about -4 to -8 length, +1 thickness | drift |
| 5 | Kitchen window C | sales plan z 7.67-8.40 (73); construction masonry gap scales about 84 with a casement frame about 64-73 inside it | z 7.70-8.39 (69), sill 1.0 and head 2.30 (estimates) | within 4 of the sales plan | OK; masonry width is a geometry topic |
| 6 | Window vs wall cabinet | supplier: no wall cabinets | cabinet z 8.44-8.79 ends 5 cm south of the window | n/a | OK (no clash) |
| 7 | Counter under the window | supplier end cabinet runs to the facade | south run to FX, top 0.92, sill 1.0 (estimate) | 8 cm sill above the top | OK |
| 8 | Riser 3 and drain 13 | west wall shaft, z about 7.49 and 8.13 | inside the core wall, behind the tall wall and west run | none | OK |
| 9 | Ceiling point 1d | x 5.88, z 6.51 | frames pendant canopy x 5.83-5.91, z 5.66-6.96 | point under the canopy | OK |
| 10 | Sink position | taps 4.76, drain 4.63 (sink cabinet about 4.32-5.21) | sink 80 at x 4.85-5.65, centre 5.25 | +49 east | owner |
| 11 | Dishwasher | about 5.21-5.81 | 5.65-6.25 | +44 east | owner |
| 12 | Dishwasher socket | x 4.93, H 0.60 | falls inside the model sink cabinet | none | OK (compatible) |
| 13 | Hob type and position | gas, centre about 6.23, ignition socket 5.93 H 0.60, gas outlet 6.93 | induction 6.25-6.85, centre 6.55 | +32 east; type differs | owner |
| 14 | Induction supply | not on the sheet | needed under the induction hob | missing point | owner (tell the supplier) |
| 15 | South end cabinet / landing | 303-363 from the west (x 6.93-7.26) | landing 6.85-7.28 (43) | about +8 | owner |
| 16 | Wall cabinets and hood, south wall | none | cabinets 1.62 to the ceiling, flush hood | added | owner |
| 17 | West base run | z 7.21-8.79 (158 from the south) | z 7.62-8.79 (117) | -41 | owner |
| 18 | Oven | tall column z 6.62-7.21, oven about H 0.55-1.15 | column z 6.42-7.02, oven H 0.30-0.90 | column 20 north; oven 25 lower | owner |
| 19 | Microwave | socket at H 1.45 (built-in above the oven implied) | microwave H 0.95-1.33 under the oven column top | lower | owner |
| 20 | Oven and microwave sockets | z 6.84 and 6.99, H 1.45 | inside the model oven column above the microwave | none | OK (hidden, compatible) |
| 21 | Fridge | niche clear about 88, z about 5.66-6.54 | fridge 70 in a 72 niche, z 5.71-6.41 | about -18 width | owner |
| 22 | Fridge socket | z 5.89, H 1.70 | behind the fridge (fridge to 2.00) | none | OK (hidden, compatible) |
| 23 | Coffee bar | not on the sheet | open lit niche z 7.02-7.62, H 0.90-1.57 | added | owner |
| 24 | West service socket | z 7.54, H 1.10 | no plate; position falls on the back of the coffee niche | missing plate | (a) small, see change 2 |
| 25 | South service socket | x 3.83, H 1.10 | no plate; position falls on the backsplash over the west run corner | missing plate | (a) small, see change 1 |
| 26 | Ninja grill socket | not on the sheet | plate at z 8.13, H 1.10 on the west backsplash (line 1289) | extra point | owner |
| 27 | Tall unit height | top about 2.16 (scaled) | to the ceiling | about +44 | owner |
| 28 | Counter height | about 0.89-0.90 (scaled, not written) | 0.92 | +2 | OK (estimate on both sides) |
| 29 | Plinth | about 0.10 (scaled) | 0.10 | 0 | OK |
| 30 | Island | none on the supplier sheet; architect sketch shows one with 3 stools | 160 x 90, x 5.42-6.32, z 5.51-7.11, 2+2 stools | added | owner |
| 31 | Finish | not written; fronts drawn with handles | white, graphite, black, handleless, no wood | n/a | owner |
| 32 | Ceiling height | wall drawn about 2.69-2.70 (scaled, low confidence) | 2.60 (estimate) | about +10 | flag; no plan writes a ceiling height |

Model clearances with the owners' island (for reference, not a plan item): island to the south run front 108, island to the tall-wall front 113.

## 3. Group (a): geometry and MEP facts the model must follow

| Fact | Status in the model |
|---|---|
| West wall, facade, south wall, entry stub | match the sales plan (roomdims +0); construction plan differs by 2-5 cm, which is drift between plans, not a change |
| Window C position and size | matches the sales plan within 4 cm; sill and head are estimates |
| Riser 3 and balcony drain 13 in the west wall shaft | inside the wall, nothing to show |
| Ceiling point 1d | under the owners' pendant canopy |
| Socket points that land on visible surfaces in the model layout | two are missing plates (south and west service sockets); see Proposed changes |
| Socket points that land behind appliances or cabinets in the model layout | dishwasher, oven, microwave, fridge, ignition: hidden, no change |
| Water, drain and gas points | hidden behind base cabinets in both layouts; their position depends on the sink and hob layout, which is an owner decision (group b) |

No wall, window or ceiling change is needed for the kitchen.

## 4. Group (b): owner-design differences (for the owner to decide, not proposed for change)

| # | Difference | Supplier sheet | Model (owners' design) | Practical consequence if the model layout is built |
|---|---|---|---|---|
| b1 | Sink position and size | cabinet about 90, sink centre x 4.76 | sink 80, centre x 5.25 | water, taps and drain points about 50 cm further east than the sheet |
| b2 | Dishwasher position | x 5.21-5.81 | x 5.65-6.25 | follows the sink; DW socket at 4.93 still fits inside the sink cabinet |
| b3 | Hob type and position | gas, centre 6.23 | induction, centre 6.55 | needs a dedicated induction supply (not on the sheet); gas outlet and ignition socket become unused |
| b4 | South wall upper cabinets and hood | none | cabinets to the ceiling plus a flush hood | hood needs power and an exhaust or recirculation choice; none drawn |
| b5 | Fridge | wide niche, about 88 clear | 70 fridge in a 72 niche | fridge socket at z 5.89 still sits behind the fridge |
| b6 | Tall wall content | oven column plus fridge niche | fridge, oven plus microwave column, coffee bar niche | oven and microwave sockets at H 1.45 sit above the model microwave, inside the carcass |
| b7 | Tall unit height | about 2.16 | to the ceiling | none for MEP |
| b8 | West base run length | 158 from the south wall | 117 from the south wall | less base storage on the west wall, coffee bar instead |
| b9 | Oven and microwave heights | oven about 0.55-1.15, microwave above | oven 0.30-0.90, microwave 0.95-1.33 | none for MEP |
| b10 | Island | none | 160 x 90 waterfall island, 2+2 stools, drawer block | any island socket needs floor wiring (supplier note 6); none drawn |
| b11 | Ninja grill socket | not drawn | plate at z 8.13, H 1.10 on the west backsplash | an extra point to add to the supplier sheet, or use the south service socket |
| b12 | Finish | handles drawn, materials not written | white, graphite, black, handleless | none for MEP |

## Proposed changes (group a only)

Both are small and optional. Neither touches walls, so roomdims and clearance_audit are unaffected.

1. **South wall service socket.**
   Line 1289, current:
   `plate('e', 3.645, 8.13, 1.10, .08, .08);`
   Replace with:
   `plate('e', 3.645, 8.13, 1.10, .08, .08); outlets('n', 8.79, 3.83, 1.10, 's');   // supplier service socket: 200 from the west wall, H 1100`
   Basis: Regba sheet, south elevation, "שירות" 200, H 1100. In the model it lands on the backsplash above the west run corner, below the wall cabinet (1.62).
   Confidence: high for the position on the sheet; medium that it is wanted, since the owners may move points when they settle their own layout.

2. **West wall service socket inside the coffee bar niche.**
   Line 1250 (the `KW(7.02, 7.62, 1.57, H);` line closing the coffee bar), current:
   `KW(7.02, 7.62, 1.57, H);`
   Replace with:
   `KW(7.02, 7.62, 1.57, H); outlets('e', 3.66, 7.54, 1.10, 's');   // supplier service socket: 1250 from the south wall, H 1100, on the niche back`
   Basis: Regba sheet, west elevation, "שירות" 1250, H 1100. In the model this falls on the fluted back of the coffee niche (back face x 3.658, niche H 0.90-1.57), which is where the coffee machines need power. Check the line number before editing; it is the last `KW(...)` of the coffee bar block.
   Confidence: high for the position on the sheet; medium for showing it on the fluted panel (the owners' niche design may route power differently).

Not proposed: moving the sink, dishwasher, hob, fridge or Ninja plate (group b); changing walls to the construction plan's 367 / 320 / 884 (sales plan rule, geometry topic); changing the 2.60 ceiling on the strength of a scaled 2.70 (no plan writes it).
