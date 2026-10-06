# Re-check 5: plans d01, d05, d06 vs the model

Documents (staged in `source/out/docs5/`, not in git):

- d01: apartment sheet "1-4 A 2-8", AutoCAD vector PDF, file dated 21.5.24, PDF created 2024-06-16. Title block: "תכניות מכר - נספח ב'", building A, floors 1-4, apartments 2, 4, 6, 8, scale "1 : 50".
- d05: typical floor "TIPUSIT", same series and date, title "תכנית קומה טיפוסית 1-4", scale "1:100".
- d06: "הערות לתכניות מכר" (sales plan notes), same series and date. Text is vector glyphs; the embedded text layer is garbled, so all wording below was read from 260 to 900 dpi renders.

Model: `source/salon.html` as of commit 6b679fd (3105 lines). Line numbers refer to that state.

Method. d01 and d05 are vector PDFs, so wall faces and dimension ticks were read from the PDF geometry (PyMuPDF), not from pixels.
The 2025 sales plan (`materials/plans/newBA_K1-4_DIRA_2-4-6-8_250701_123041.pdf`) is a raster image only (2480 x 1754). I mapped
both into model coordinates (d01: x_pt = 257.3 + 38.06 x, y_pt = 431.4 + 38.22 z; sales: u = 1373.25 - 79 z, v = 457.5 + 79 x,
from `audit/report.md`) and overlaid them (crop 01), then drew the model's `W()` wall boxes on d01 (crop 02) and gridded d05 in
model metres (crops 08 to 10). "Written" = a number or word on the sheet. "Scaled" = measured on the drawing; d01 about +-6 cm,
d05 about +-20 cm. "Estimate" = mine.

Crops: `plans_crops/` (01 to 12).

## Proposed changes, priority order

1. **Mamad identification is now written.** d01 and d05 label the 355 x 262 room "חדר מס' 4 ממ"ד". Replace the "verify" note in the panel (L194) with a confirmed statement. Items 1.3, 1.4.
2. **Room numbers.** The developer numbers the rooms differently from the model: master = 1, middle north room = 2, NW room = 3, mamad = 4. Owner decision whether to adopt them in the UI strings L2460, L2488 to L2490, L2696 and the panel text L191, L194 to L196 (code comments can stay). Item 1.3.
3. **True north (conflict, confirm before changing).** The d01 compass needle points 15.5° west of sheet-up (vector geometry). The 2025 sheet has an axis-aligned schematic compass. If d01 is right, the balcony faces bearing about 105° (ESE), not 90°. Then the L1841 comment, the L195 panel text and `SUN_OFF` L1846 change (to keep the same true sun bearing: about `[27.8, 24, 6.8]`). Item 1.10.
4. **Building outline south of the apartment** (exterior, bird views and the view south from the balcony). `building(-4.28, 7.70, 9.11, 38, 23.1)` L1859 is one box. d05 shows a stepped building that runs to about z 43.3 (balcony to 44.2), a bedroom wing that projects to x about 8.35 for z 13.0..27.0, a west face mostly at x -0.9 to -2.2 (not -4.28), and a south wing to x about -10. Second balcony box L1860 `[26, 30.8]` should be about `[27.0, 31.4]`. Items 2.5 to 2.8.
5. **Gap in the core above floor 1** (by code reading, not rendered). Nothing in the model fills x -4.28..1.19, z 5.77..9.11 above y -0.45 (the floors 0-1 box ends there, `building()` starts at z 9.11, the wall masses at L898 stop at 5.77 or start at 1.19). d05 has the lift and lobby there, west face x about -3.55. Add a box x -3.55..1.19, z 5.77..9.11 with the building height, and start `building()` at x -3.55 up to z 11.1. Item 2.4.
6. **Floor levels (written, small).** d06 note 8: mamad floor "מוגבהים עד 3 ס"מ", wet rooms "מונמכים ... בכ-1 ס"מ"; note 9 and the d01 step symbols: balcony and entry thresholds. Model: all room floors at y 0.009 (L870 to L881), balcony deck -0.04 (L1677). Optional: mamad +up to 3 cm, both baths -1 cm (needs the base slab at L870 cut out under the baths, or every other floor raised 1 cm). Items 3.8, 3.9.
7. **Partition and mamad wall thickness (report only, owner decision).** d01 is the vector original of the sales drawing and draws partitions 10 and 15 cm and mamad walls about 20 cm, the same as the construction plan. The model has 15 to 20.5 cm partitions (L909 to L917) and 25 to 27 cm mamad walls (L922, L923), an artefact of scaling the 2025 raster. Thinning them while keeping the outer walls breaks `roomdims.py` +0. No change proposed. Item 1.6.
8. Low: optional hollow lobby behind the front door (L898 `W(1.19, 3.63, 5.70, 9.11)` fills the common lobby; with the door open the view hits a wall). Item 2.3. Small pipe chase in the closet NE corner (item 1.9). Both cosmetic.

No change needed for the corridor passage (120, construction plan wins over d01's 100), the family bath riser (NW, newer sheets win over d01's SW), the kitchen and furniture (d06 notes 7 and 11 make them illustrative).

## 1. d01 (apartment sheet)

### 1.1 Relation to the 2025 sales plan

| # | Point | Finding |
|---|---|---|
| 1.1.1 | Same drawing? | Yes. The 2025 sheet is a coloured rendering of the same CAD base. Overlay (crop 01): every wall, opening, door swing, window symbol, sanitary fixture, kitchen outline, wardrobe and the core coincide within the raster blur (2 to 4 cm). |
| 1.1.2 | Written dimensions | Identical set: 274, 361, 282, 356, 245, 238, 222, 172, 190, 175, 430, 296, 110, 355, 262, 728, 277, 879, 365, 884, 275. No number differs. |
| 1.1.3 | Orientation | d01 is drawn like the construction plan and the model (sheet right = east, down = south). The 2025 sheet is rotated 90° (balcony at the bottom). |
| 1.1.4 | Scale | Title says "1 : 50", but the print is about 1:74 (written chain 274 + 15 + 282 + 10 + 245 + 10 + 430 = 1266 cm over 487.2 pt). The drawing is not exactly to scale: single rooms scale 2.53 to 2.61 cm/pt. Use written numbers only. |
| 1.1.5 | Which wins | Where d01 and the 2025 sheet differ only in rendering, nothing to resolve. Where either differs from the construction plan (5/5/26) or the MEP vector sheets, those win: they are newer, they write the values, and the sales drawings are marked as preliminary (d01 note 2, d06 notes 3, 5, 6). d06 note 24 puts the sales spec and contract above all plans. |

### 1.2 Every difference between d01 (2024) and the 2025 sheet

| # | Item | d01 | 2025 sheet | Model impact |
|---|---|---|---|---|
| 1.2.1 | Room names | "חדר מס' 1" (master), "חדר מס' 2", "חדר מס' 3" (NW), "חדר מס' 4 ממ"ד", "אמבטיה כללית", "מקלחת הורים", "חדר דיור", "פ.אוכל", "מטבח", "מרפסת שמש", box "דירה מספר 2, 4, 6, 8" | no names, only dimensions | see 1.3 |
| 1.2.2 | Room areas | none written | none written | none |
| 1.2.3 | Legend | full legend, incl. "הצעה למיקום בלבד" for fridge, hob, washer, sink, AC unit | none | see 3 |
| 1.2.4 | Wall materials | grey = concrete (outer walls, mamad, core, niche walls, wardrobe-niche walls, an L at the room 2/room 3 corner, the column by the master door); white = block partitions | all walls one colour | item 1.6, 1.8 |
| 1.2.5 | Common areas | stair, lobby, lift hatched "שטח משותף לבניין" | plain | none |
| 1.2.6 | Neighbour | top of apartment 3, 5, 7, 9 shown south of ours | not shown | exterior, item 2 |
| 1.2.7 | Living furniture | 3-seat sofa, 2-seat sofa, rug | L sofa, round table, rug | none (illustrative, d06 note 7) |
| 1.2.8 | TV unit | none | low unit drawn under the TV wall | none |
| 1.2.9 | Room 2 wardrobe | ends at x about 0.90 | runs to about 1.05 | none (furniture) |
| 1.2.10 | Closet | wardrobe outline only | L wardrobes drawn | none |
| 1.2.11 | Master bath shower | plain tray rectangle | tray with a glass line | none |
| 1.2.12 | Washer in the family bath | solid circle in a square | dashed circle | none |
| 1.2.13 | Balcony | plain deck with board lines | deck, lounger, plants | none |
| 1.2.14 | Kitchen layout | sink on the west wall about 42% from the south wall, hob on the south wall near the window, fridge NW, island with 3 stools east | the same | none |
| 1.2.15 | Laundry niche | AC unit rectangle (north-west), solar heater circle with two pipes and solar pipe symbol (north-east), clothes rack on the bath-window wall, light screen lines on the north | the same | see 1.7.6 |
| 1.2.16 | Columns and risers | ⊕ symbols: family bath SW corner, two in the west wall at the wardrobe niches, master/closet NE corner, balcony NW and SW corners | the same positions | see 1.8 |
| 1.2.17 | Doors, windows, AC, shafts | no difference found | | |

### 1.3 Labels and names

| # | d01 written | Model now | Change |
|---|---|---|---|
| 1.3.1 | "חדר מס' 4 ממ"ד" on the 355 x 262 room (also on d05) | L2460 `'חדר 3 · ממ״ד'`; L194 "זיהיתי את חדר 3 כממ״ד ... כדאי לאמת" | L194: say it is written on the developer's sheets; drop "verify". PROJECT_MEMORY open issue "Room 3 as the mamad" can close. |
| 1.3.2 | "חדר מס' 3" = NW room (274 x 361) | `'חדר 1'` (L2460, L2488, L195, L196) | owner decision: relabel to 3 |
| 1.3.3 | "חדר מס' 2" = 282 x 356 | `'חדר 2'` | matches |
| 1.3.4 | "חדר מס' 1" = master (430 x 296) | `'חדר הורים'` | optional "(חדר 1)" |
| 1.3.5 | "אמבטיה כללית", "מקלחת הורים" | `'אמבטיה'`, `'מקלחת הורים'` L2461 | matches |
| 1.3.6 | "פ.אוכל" (dining table drawn) | `'קיר אחסון'` L2459 | owner design choice, keep |
| 1.3.7 | "מרפסת שמש" | `'מרפסת'` | matches |
| 1.3.8 | Apartments 2, 4, 6, 8 on floors 1-4 (title block) | apartment 4 on floor 2 (CLAUDE.md, L195) | consistent: 2, 4, 6, 8 = floors 1, 2, 3, 4 |

### 1.4 Written dimensions vs the model (`python3 roomdims.py`)

| # | d01 | Model (roomdims) | Verdict |
|---|---|---|---|
| 1.4.1 | Room 3 (NW) 274 x 361 | 274 x 361 | matches |
| 1.4.2 | Room 2 282 x 356 | 282 x 356 | matches |
| 1.4.3 | Mamad 355 x 262 | 355 x 262 | matches |
| 1.4.4 | Family bath 245 x 238 | 245 x 238 | matches |
| 1.4.5 | Master 430 x 296 | 430 x 296 | matches |
| 1.4.6 | Master bath 222 x 172 | 222 x 172 | matches |
| 1.4.7 | Closet 190 x 175 | 190 x 175 (script shows 485, the known probe artifact) | matches |
| 1.4.8 | Corridor 110 | 110 | matches |
| 1.4.9 | Dining alcove 277 | 277 | matches |
| 1.4.10 | Living 728 (x) | 728 | matches |
| 1.4.11 | Living + kitchen 879 (z) | 879 | matches |
| 1.4.12 | Kitchen 365 | 365 | matches |
| 1.4.13 | Balcony 275 x 884 | 275 (7.70..10.45) x 884 (L1677, dim at L2453) | matches |

These are the sales numbers the model was built on, so the match is expected. The construction plan writes 5 to 8 cm more per
room (`audit/recheck3/geometry.md` 2d); that conflict is unchanged by d01.

### 1.5 Openings scaled on d01 (written values from the construction plan already in the model)

| # | Opening | d01 scaled (model coords) | Model now | Verdict |
|---|---|---|---|---|
| 1.5.1 | Room 3 west window | z -2.91..-1.86, one inward sash | -2.81..-1.91 (L893, `windowZ` L1596), one sash | matches within scaling |
| 1.5.2 | Room 2 north window | x 0.29..1.35, one inward sash hinged east | 0.365..1.265 (L890), one sash | matches |
| 1.5.3 | Laundry niche north opening | x 2.14..3.66, thin screen lines | louvres 2.15..3.65 (L1560) | matches |
| 1.5.4 | Master bath window | x 5.90..6.66 (scaled), drawn as two lines | 6.015..6.615 (L891) | matches within scaling; construction written wins |
| 1.5.5 | Master east window | z -2.29..-1.24, one inward sash | -2.17..-1.27 (L907) | matches |
| 1.5.6 | Living facade | piers scaled 64, 64 and 57 cm; door A z 0.65..3.47, door B 4.11..6.94, window C 7.52..8.38 with one inward sash | construction written 80 / 270 / 80 / 270 / 76 / 70 (L903) | conflict d01 vs construction: construction is written and newer, keep the model |
| 1.5.7 | Mamad window | z 0.42..1.41, blast-shutter pocket south of it in the wall | 0.48..1.48 (L894) | matches |
| 1.5.8 | Bath window to the niche | two sliding sashes | `windowX(2.375, 3.575, ...)` L1466 | matches |
| 1.5.9 | Entry door | opening x 1.59..2.58, hinge west, opens into the apartment | 1.585..2.555, hinge west | matches |
| 1.5.10 | Mamad blast door | opening x -1.95..-1.19, hinge west, opens north into the corridor; leaf drawn about 70 cm | opening -1.98..-1.19, leaf 0.86 (L992) | opening matches; leaf drawn 70 on d01 and on the construction plan, still not written (low confidence) |
| 1.5.11 | Room 3, room 2, bath doors | hinge on the east jamb, open into the room | L988 to L990 hinges at the east jamb | matches |
| 1.5.12 | Master door | hinge at the south (TV wall) end, opens east | L991 | matches |
| 1.5.13 | Master bath door | in the bath/closet partition, hinge at the south end, opens into the bath | L993 | matches |
| 1.5.14 | Closet opening | in the closet south wall, x about 7.55..8.33 | 7.54..8.32 (L918) | matches |
| 1.5.15 | Corridor to living passage | gap x 1.99..2.97 (98 cm), same as the 2025 sheet | 1.80..3.00 (L924, L908), written 120 on the construction plan | **conflict**: d01 and 2025 = 100, construction = 120 written. Keep 120 (newer, written). |

### 1.6 Walls (d01 vector line spacing)

| # | Wall | d01 | Model | Note |
|---|---|---|---|---|
| 1.6.1 | Room 3 / room 2 | 5.76 pt = 15 cm | 18 (L911) | d01 = construction ("15") |
| 1.6.2 | Room 2 / corridor | 15 cm | 20.5 (L912) | d01 = construction |
| 1.6.3 | Room 2 / bath and niche | 3.84 pt = 10 cm | 16 (L913) | d01 = construction |
| 1.6.4 | Bath / master | 10 cm | 15 (L917) | d01 = construction |
| 1.6.5 | TV wall | 10 cm at x 0..2 and x 4.75..7.28; 15 cm on the corridor stretch x 2.98..4.15 | 14.5 / 19 / 14.5 (L908, L924) | construction: 10 / 20 / 10 |
| 1.6.6 | Mamad north and east | about 20 cm, grey | 27 (L922), 25 (L923) | construction north about 19.5 |
| 1.6.7 | Column by the master door | grey, x 4.15..4.75, face at z -0.255 | step `W(4.26, 4.76, -0.24, -0.145)` L921 | matches |

Conclusion: in its own CAD the sales drawing has the construction-plan wall thicknesses. The model's thicker partitions come from
the 2025 raster. Written room sizes plus the model's outer walls (which match the construction plan within 2 cm) cannot all hold
with 10 to 15 cm partitions: about 14 cm per room row is unaccounted for, which is the construction plan's +5 per room. Report
only; the project rule keeps `roomdims.py` at +0.

### 1.7 Fixtures and symbols (d06 notes 6 and 7: illustrative)

| # | Item | d01 | Model | Verdict |
|---|---|---|---|---|
| 1.7.1 | Family bath | WC west wall north, basin west wall south, washer NE corner, tub east wall south of a stub | same arrangement (L1458 to L1556) | matches |
| 1.7.2 | Master bath | shower tray NW about 110 x 95 (scaled), basin west wall south, WC centred under the window (axis x about 6.28) | shower 106 x 92, WC axis 6.25 | matches |
| 1.7.3 | Kitchen | sink west wall, hob south wall, fridge NW, island with 3 stools | owner's kitchen (sink and hob on the south run, tall west wall, island 160 x 90 with 4 seats) | differs by design; allowed by d06 notes 7 and 11 |
| 1.7.4 | Electrical panel symbol | TV wall corridor face, x 3.37..3.74 | 3.33..3.78 | matches |
| 1.7.5 | Mamad filter "מערכת סינון ואוורור דירתית" | dashed box on the west wall, z 2.15..2.56, pipe out through the wall | filter z 2.085..2.585 (L1793) | matches |
| 1.7.6 | Mamad vent pipes "צינור אוורור בקוטר 8"/4"" | on the mamad north wall at x about -1.64 (over the door), -1.04, and a dashed one at -0.44 | sleeves -1.55, -0.95, -0.52 | about 9 cm west on d01, within combined scaling; no change |
| 1.7.7 | Laundry niche rack "מתלה כביסה" | fixed rack on the niche's south wall in front of the bath window, projecting about 60 cm | pull-out lines at y 2.0 near the louvres (L1570, L1571) | differs; design choice, not written. Optional. |
| 1.7.8 | Niche AC unit "מזגן" | rectangle in the NW part of the niche ("הצעה למיקום בלבד") | condenser 100 x 45 in the NW part (L1563) | matches |
| 1.7.9 | Solar heater "דוד שמש" | circle in the NE corner of the niche with 2 risers and the solar pipe symbol | heater at about (4.04, -4.69) (L1572) | matches |
| 1.7.10 | Fire detector "גלאי אש", vent "ונטה", water meter "רכזת מים", drain "נקז", seepage pit | in the legend, not drawn inside our apartment | none | nothing to add |
| 1.7.11 | Step symbols "הפרשי גבהים בס"מ" | at the mamad door, family bath door, master bath door, entry door and both balcony doors; no numbers | all floors one level | see 3.8, 3.9 |

### 1.8 Columns, risers, structure

| # | Item | d01 | Model | Verdict |
|---|---|---|---|---|
| 1.8.1 | Family bath riser ⊕ with a small concrete square | SW corner, about (2.04, -1.47); same on the 2025 sheet | riser box in the NW corner (L1552), from the plumbing and construction sheets | **conflict** d01 + 2025 vs plumbing + construction. Keep NW (newer vector sheets). |
| 1.8.2 | Two ⊕ in the west wall | x about -4.02, z -1.14 and -0.90, inside the wall behind the room 3 wardrobe niche | none | inside the wall, nothing visible; no change |
| 1.8.3 | ⊕ at the balcony corners | in the master corner wall (9.04, 0.06) and in the balcony south wall (8.99, 8.84) | balcony floor drains (8.89, 1.63) and (8.89, 7.36) from the plumbing sheet | different items (downpipes in the walls); no change |
| 1.8.4 | ⊕ master/closet NE corner | in the wall corner (9.07, -5.20) | none | inside the wall |
| 1.8.5 | Grey concrete L | in the room 3 / room 2 partition from z -2.23 to the corridor, and along the corridor wall to x -0.63 (crop 06) | plain partition | info: structural, invisible after plaster |
| 1.8.6 | Closet NE corner chase | a step about 10 x 15 cm in the inner corner (x 8.81..8.96, z -5.07..-4.91), beside the ⊕ | square corner (L891 `W(7.01, 8.91, -5.39, -4.995)`) | low; optional box, hidden by the wardrobe anyway |

### 1.9 d01 sheet notes (bottom of the sheet)

1. "מותנה בקבלת היתר בניה ובכפוף לאישור היועצים והרשויות."
2. At this stage the project systems are "טרם הוטמעו": installation, structure, electrical, vertical and horizontal shafts, ledges, columns, beams, additional systems.
3. Common areas will be marked on updated plans after the permit.
4. "יתכנו שינויים בקולטנים, צמ"גים, עמודים, קורות, לוחות חשמל" per the consultants.

Effect: d01 is explicitly preliminary on systems and structure. MEP and construction sheets outrank it for any column, riser or panel.

### 1.10 North arrow

| # | Source | Reading |
|---|---|---|
| 1.10.1 | d01 title block compass (vector) | needle line (784.64, 232.92) to (779.72, 215.16) pt: north 15.5° counter-clockwise from sheet-up. In model terms true north = (-0.27, 0, -0.96); +x (the balcony) faces bearing 105.5°. Crop 07. |
| 1.10.2 | 2025 sales sheet | schematic compass with the needle exactly along the sheet axis |
| 1.10.3 | d05 | a plain arrow straight up at the top left (reads as a project north, no angle given) |
| 1.10.4 | Model | L1841 "-z is true north, the balcony faces EAST"; `SUN_OFF = [25, 24, 14]` L1846 (azimuth 119° in the model frame, 40° up) |

Conflict: d01 (15.5°) vs the 2025 schematic. Not resolved here. A map check of Ali Mohar street would settle it. If d01 holds and
the "10:00 autumn" sun should keep its true bearing, `SUN_OFF` becomes about `[27.8, 24, 6.8]`; the photo-based surroundings are
placed relative to the apartment, so they need no change.

## 2. d05 (typical floor, floors 1-4)

Scale: title "1:100", printed about 1:152 (the apartment's outer width 13.58 m spans 253.32 pt). Both d01 and d05 are printed
at about two thirds of the stated scale. Mapping used: x = (pt - 398.88) / 18.654, z = (pt - 193.9) / 18.654 (fits our outer walls
exactly; +-0.2 m elsewhere).

| # | Item | d05 (scaled, model coords) | Model now | Change |
|---|---|---|---|---|
| 2.1 | Our apartment | identical to d01; the NE (north) end of the building, entrance A | as built | none |
| 2.2 | Neighbours | north: none (end of the building). South: apartment 3, 5, 7, 9 across the kitchen south wall (z 8.79..9.11) and the balcony south wall; its balcony is next to ours. West: the stair (south of our mamad) and the core. | building box starts at z 9.11 | none for the interior |
| 2.3 | Stair, lift, lobby | stair hall x -4.1..1.2, z 2.95..5.6, door to the lobby at x -0.1..1.0. Lift x -3.4..-1.3, z 5.8..7.4, door on its east side. Lobby (hatched, common) about x -1.3..2.9, z 5.7..9.2. Our entry door at the lobby's NE (x 1.6..2.55), the neighbour's at its south (x 1.7..2.7, z 9.2). Four shaft cupboards x 2.9..3.4, z 5.8..9.0 against our kitchen west wall. Small shafts and a service room x -3.4..-1.3, z 7.6..9.6. | solid masses `W(-4.28, -0.25, 2.745, 5.77)`, `W(-0.25, 1.45, 2.775, 5.77)`, `W(1.19, 3.63, 5.70, 9.11)` L898 | optional, low: hollow lobby x 1.19..2.9 behind the front door so an open door shows a lobby; keep the shaft cells x 2.9..3.63 solid |
| 2.4 | Core west face | x about -3.55 for z 5.8..11.1 (stair part -4.28 for z 2.75..5.8) | nothing at x -4.28..1.19, z 5.77..9.11 above y -0.45 (code reading) | add a box x -3.55..1.19, z 5.77..9.11, building height; same material as `building()` |
| 2.5 | West face south of the core | -1.56 (z 11.1..16.0), -0.89 (16.0..18.6), notch to x about 2.8 (18.6..20.7), -0.89 (20.7..23.6), -2.2 (23.6..26.9), -1.56 (26.9..30.1), core B -3.67 (30.1..33.4), south wing -9.9 (33.4..41.0), mamad wall -8.5 (41.0..43.3) | -4.28 for z 9.11..38 (L1859) | replace the single box with stepped boxes along these lines (estimate +-0.2 m) |
| 2.6 | East face south of us | neighbour living facade 7.70 (z 9.1..13.0); bedroom wing outer face about 8.35 (z 13.0..27.0); living facade 7.70 (27.0..31.3); B kitchen wall about 8.33 (31.3..37.3); B living facade about 7.55 (37.3..41.0) | 7.70 everywhere | add the 65 cm bedroom wing (x 7.70..8.35, z 13.0..27.0) and the B kitchen bump. Visible from our balcony looking south. |
| 2.7 | East balconies | A neighbour: deck x 7.75..10.3, z 9.3..13.35 (outer line to about 10.55 and 13.6). B 3, 5, 7, 9: deck x 7.75..10.3, z 27.3..31.3 (outer about 27.0..31.6) | boxes `[9.25, 13.2]` and `[26, 30.8]`, x 7.70..10.2 (L1860) | first box matches; second to about `[27.0, 31.4]`; x2 10.2 can stay (within the outer line) |
| 2.8 | South end | building ends at about z 43.3; apartment 2, 4, 6, 8 of entrance B has a south-facing balcony x 1.9..8.3, z 41.0..44.2 | box ends at z 38, no south balcony | extend to z 43.3 and add the south balcony boxes (estimate) |
| 2.9 | North of the master bath and closet | thin outline x about 4.0..9.3, z -7.3..-5.39 with beam lines, also on d01 | none | it is drawn from below: a pergola over the ground-floor garden (d03 shows the garden). Hand to the d03 check; not on floors 1-4. |
| 2.10 | Storeys | sheet covers "קומה טיפוסית 1-4" only | 7 storeys (L1860, h 23.1 at L1859) | not decidable from d05; see the roof sheet d04 |
| 2.11 | Floors above us | floors 3 and 4 are the same typical plan | nothing above our apartment (needed for the open top views) | none |

d05 legend and notes are the same four notes and legend as d01 (1.9, 1.7).

## 3. d06 (sales plan notes), every note

Legend on the right is the same as d01. Crops 11 and 12.

| # | Note (short quote) | Affects the model? | Model now | Change |
|---|---|---|---|---|
| 3.1 | "כל המידות בס"מ ... מציינות את מידות הבניה ... בין קירות הבניה. מידות החללים תתקבלנה לאחר הפחתת עובי הטיח ו/או חיפוי." | yes: written dims are brick to brick | walls gross, the panel says rooms will be 2 to 6 cm smaller (L196, estimate) | matches |
| 3.2 | deviation "עד 2%" between plan and built dimensions is acceptable | context for every scaled check | | none |
| 3.3 | non-essential changes possible in openings: size, location, dimension, shape | openings | written construction values used | none |
| 3.4 | company may change the division of unsold units | no | | none |
| 3.5 | "לא מסומנים בתכניות כל העמודים, הקורות, הצנרת, הגומחות, הבליטות וההנמכות"; exposed pipes (sewer, ventilation, electricity, drainage, gas) may pass | yes: extra bulkheads and boxes may appear | corridor drop and bath drop from the AC sheet (L925 area, BC) | none; keep the "estimate" wording |
| 3.6 | location, size and shape of AC provisions, water heaters, solar collectors and sanitary fixtures (WC, baths, basins, taps, pipes, rainwater, drains, sewer risers) are "לצורך המחשה בלבד" | yes: fixture positions on d01 are illustrative | positions from the plumbing and AC sheets | none |
| 3.7 | equipment and furniture incl. fridge, hob, washers and dryers, AC condensers and evaporators, wardrobes are illustrative ("כהצעה למיקום") and not part of the sale unless specified | yes: furniture, kitchen and wardrobes are free | owner's own furniture and kitchen | none |
| 3.8 | mamad floor "מוגבהים עד 3 ס"מ"; WC, bath and shower floors "מונמכים ... בכ-1 ס"מ" | yes, small | all room floors at y 0.009 (L870 to L881) | optional: mamad floor up to +0.03 with a step at the blast door; both baths -0.01 (base slab L870 must not cover them). Written, small. |
| 3.9 | balcony exit may have a raised threshold; balcony floor may be higher or lower than the apartment | yes | deck BY -0.04 (L1677), no threshold | none (BY is an estimate; say so) |
| 3.10 | balconies and outdoor paving laid "בשיפועים הנדרשים לניקוז" | barely visible | flat deck | none |
| 3.11 | final kitchen cabinets, sink and hob position per the company | yes | owner's kitchen | none |
| 3.12 | sprinklers, AC condensers and evaporators and ceiling lowerings (if in the spec) may move | yes: sprinklers and drops | no sprinklers modelled | check the spec (d08) for sprinklers; not on any plan in this set |
| 3.13 | plot and development boundaries not final | exterior | surroundings are estimates | none |
| 3.14 | development, parking, storage, refuse rooms, fences, planting, gas, electricity set by the designers | exterior | estimates | none |
| 3.15 | external stairs, retaining walls not final | exterior | retaining wall from photos | none |
| 3.16 | niches for electricity, communications, water, refuse, gas set by consultants | exterior | | none |
| 3.17 | easements through parking areas | no | | none |
| 3.18 | refuse collection per authorities | no | | none |
| 3.19 | information outside the plot is "אינו מחייב" | exterior | estimates from photos | none |
| 3.20 | company may install facilities on roofs (water tanks, AC, antennas, generator) | roof views | | none |
| 3.21 | parking and storage locations may change | no | | none |
| 3.22 | changes per authorities; plans subject to the special annex | general | | none |
| 3.23 | roof apartments: right of access to technical systems | no | | none |
| 3.24 | "בכל מקרה של סתירה בין התכניות למפרט המכר ו/או לחוזה, יגבר ... האמור במפרט /בחוזה" | ranking rule: the sales spec (d08) beats every plan, including the construction plan | | use when the spec gives heights or finishes |

## 4. Items that cannot be shown in a 3D model

- d01 note 1 (permit), note 3 (common areas registration), d06 notes 2, 4, 13, 14, 16 to 18, 21 to 23: legal or procedural.
- Hatching that marks common property (stair, lobby): ownership, not geometry.
- "אלמנט בנוי / מבטון - לא סופי": a status, not a shape.
- The 2% tolerance (d06 note 2) and "illustrative only" status of fixtures (notes 6, 7): they change how to read the plans, not the model.
- Concrete vs block (1.8.5) and risers inside walls (1.8.2 to 1.8.4): hidden behind plaster.

## 5. Conflicts (not resolved here)

| # | Topic | Sources | Model follows |
|---|---|---|---|
| 5.1 | Passage width | d01 and 2025: about 100. Construction: 120 written. | construction |
| 5.2 | Family bath riser | d01 and 2025: SW corner. Plumbing and construction: NW. | NW |
| 5.3 | True north | d01: 15.5° west of sheet-up. 2025: axis-aligned schematic. | axis-aligned |
| 5.4 | Partitions, TV wall, mamad walls | d01 vector and construction: 10/15, 10, about 20. Model: 15 to 20.5, 14.5/19, 25 to 27 (2025 raster). | 2025 raster |
| 5.5 | Living facade piers | d01 drawn 64/64/57. Construction written 80/80/76. | construction |
| 5.6 | Room numbering | d01/d05: master 1, NW 3, mamad 4. Model: NW 1, mamad 3. | model's own |
| 5.7 | Stated vs printed scale | d01 "1:50" printed 1:74; d05 "1:100" printed 1:152 | n/a |
