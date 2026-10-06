# Fifth re-check: site, ground floor, basement, roof and the apartment annex (site.md)

Date 2026-10-06. Model: `source/salon.html` at commit 6b679fd (3105 lines). Documents (staged in
`source/out/docs5/`): d03 ground floor ("תכנית קומת קרקע 1:150"), d02 basement ("תכנית מרתף 1:100"), d04 upper roof
("תכנית קומת גג עליון 1:100"), d11 apartment details annex (pages 2 and 3 only; page 1 holds personal data and is not
quoted or cropped). d05 (typical floor) and d08 (sale spec) belong to other reports; they are quoted here only where
they settle a site question. Crops: `audit/recheck5/site_crops/`.

"Written" = on the sheet as text or a drawn symbol. "Scaled" = measured on the vector PDF and converted with the
transforms in item 1. "Estimate" = mine, not on any sheet.

## Proposed changes, priority order

Ordered by how much they change what you see from inside the apartment.

1. **Below the balcony (items 7, 8, 9):** delete the floor-1 terrace, its glass rail and the stone podium (lines
   1899-1904). Replace the solid block under the balcony (line 1875) and the floor-1 part of the shell (line 1866) with
   (a) a floor-1 balcony identical to ours, one storey down, (b) a ground storey whose east face is at x 9.25 for
   z -5.39..8.9, and (c) garden at street level from x 9.25 outward.
2. **Ali Mohar, near side (item 12):** sidewalk x 14.3..16.9 (was 12.8..14.3), parallel parking on pavers x 16.9..18.8
   (was asphalt 14.3..16.6), carriageway from x 18.8 (was 16.6). Lines 1906, 1907, 1908, 1914 (kerb), 1949 (cars x 15.45
   to 17.85). To keep the 6.4 m carriageway, shift everything east of it by +2.2 m (estimate, see item 12).
3. **East garden strip, lot fence, entrances (items 10, 11, 13):** turf at GY for x 9.25..14.1, z -11.9..9.9; a
   boundary on x 12.7..12.9; the lot fence on x 14.1..14.3 with gaps at z 9.98..14.92 and 28.47..30.59; the A entrance
   stair x 10.75..12.85, z 9.97..13.01, and its landing x 12.85..14.3.
4. **North of the building (items 14, 15, 16):** move the weeds plot and its hoarding off our lot (line 2018: z -48..-6
   to z -48..-11.9; hoarding x 10.8 to x 14.3); paver strip line 2019 x 10.86..12.8 to x 14.3..16.9; add the lot fence
   on z -11.9, the private garden fences x -1.2 and 9.2, the pergola x 4.1..9.0, z -8.9..-5.4, and three smoke-vent boxes.
5. **Ground-storey windows (item 8):** in the repeat list (lines 1868-1870) the ground storey keeps room 2, room 1,
   mamad and the master east window, but the master bath window x 6.015..6.615 is wrong at ground level (there it is a
   3.7 m opening x 4.96..8.63); add the east openings at x 9.25.
6. **Panel text (items 2, 3, 7):** line 195 says "ומתחתינו המרפסת המרוצפת של קומה 1"; per the plans, floor 1 has a
   balcony like ours and the ground below is a garden. Update with the change.
7. **The rest of the building (items 5, 6, 17):** replace `building(-4.28, 7.70, 9.11, 38, 23.1)` (line 1859) with the
   floors 1-4 bar of d05: x -2.1..8.26, z 9.11..30.6, raised on a pilotis ground storey (columns at x 8.15, closed core
   x -1.3..5.3), plus building B's south wing x -9.65..8.26, z 30.6..42.6. Balcony boxes (lines 1860-1863) match.
8. **Tirtsa Atar (item 21):** lines 1851-1852 put the north kerb at z 42..44, inside the lot (lot edge z 48.0) and under
   building B (to z 42.9). Move: sidewalk z 48.0..50.5, parking on pavers z 50.5..52.5 for x -13.0..9.8, asphalt from
   z 52.5; `foot` entry line 2024 `[-160, 160, 42, 54]` to `[-160, 160, 48, 63]`.
9. **West side (item 20):** surface parking, fire-truck pads, the ramp and an outdoor stair, seen from the room 1 and
   mamad windows. Not in the model at all.
10. **Roof and floor 7 (items 4, 22, 23):** hip roof with collectors over the north end of A, one more storey. Not
    visible from inside; only if the building is ever drawn above floor 2.
11. **Orientation (item 2):** the AutoCAD compass puts true north 15.5 deg west of sheet-up; the sales plan and the model
    put it on sheet-up. Conflict, no change without the owner. Affects only the sun bearing (lines 1846, 2328).
12. **Header area (item 26):** d11 writes about 130 sqm; the header (line 129) writes 132. Conflict, owner decides.

Every change in 1 to 9 also needs its `sunBoxes` entry (baked ground shadows) updated, and the stale-render note.

## Items

### Method and orientation

1. **Scale and transforms (scaled).** The sheets are A3 reductions: d03 and d02 print at about 14.1 pt per metre
   (labelled 1:150 and 1:100, so in fact about 1:201); d05 and d04 at about 19.05 pt per metre (labelled 1:100, about
   1:149). Calibrated on walls the model already has from the sales plan (west outer -4.28, north outer -5.39, mamad east
   face x 0, master east outer 9.30, core z 2.745 and 5.77) and checked on the parking stalls, which scale to 5.0 m long.
   The lot outline is identical on d02 and d03 (offset 59.6 pt). Transforms, PDF points from the page top-left:
   - d03: x = (X - 380.0) / 14.1, z = (Y - 256.0) / 14.1
   - d02: x = (X - 439.6) / 14.1, z = (Y - 315.6) / 14.1
   - d05: x = (X - 398.0) / 19.05, z = (Y - 196.0) / 19.05
   - d04: x = (X - 360.0) / 19.05, z = (Y - 234.3) / 19.05 (aligned on the stair core, same size as on d05)

   Accuracy: about 0.15 m near the building, about 1.5 % of the distance further out (estimate). Check: the west-facade
   openings on d03 (room 1 window z -2.96..-1.90, mamad z 0.41..1.42) agree with the model (-2.81..-1.91, 0.48..1.48)
   within 0.15 m.
2. **North arrow (written, measured on the vector).** The title-block compass on d02, d03, d04, d05 (and d01) points
   15.5 deg west of sheet-up (arrow at 105.5 deg from the sheet x axis). Crop `d03_north_arrow.png`. With it, the
   model's -z faces bearing about 15 deg (NNE) and the balcony (+x) about 105 deg (ESE). The 2025 sales plan compass
   points exactly along sheet-up of d05, which is what the model uses (comment line 1841, panel line 195).
   **Conflict between documents (AutoCAD sheets vs sales plan).** Not resolved here. Geometry does not change. The sun:
   `SUN_OFF = [25, 24, 14]` (line 1846) is model bearing 119 deg, 40 deg up. Under the AutoCAD compass that is true
   bearing about 135 deg, which is roughly half an hour later in the morning (estimate). Change only if exact sun
   studies are wanted: rotate `SUN_OFF` by -15.5 deg about y to keep the same true sun.
3. **Facing (d11 p.2, written).** "הפונה לכיוונים צפון - מזרח". The sales plan says "צפון-מזרח-מערב". The model has
   windows to the north, east and west (room 1 and the mamad on the west facade, line 893-894), as every plan does.
   **Conflict d11 vs sales plan** in wording only. No geometry change.

### The building

4. **Floors (d08 cover and table 1.3, d05, d04, written).** d08: "ק 1, 2, 3, 4, 5, 6, 7 (ק. חללי גג)"; table: entrance
   floor with 1 garden apartment ("דירת גן + גינה פרטית"), typical floors 1-4 with 2 apartments (d05 is "קומה 1-4"),
   floor 5 and floor 6 with 1 apartment each, floor 7 a roof-space annex "עם תקרה משופעת", then the roof; 8 residential
   floors, 9 with the basement; A has 11 apartments, B 12; "שני בנייני מגורים מעל קומת קרקע ומרתף חניה". d04 shows a
   hipped tile roof over the north end of A, which fits the roof-space floor. No plan of floors 5, 6 or 7 is among the
   documents.
   Model: south mass 7 storeys at 3.3 m = 23.1 (line 1859, storey height an estimate), balcony boxes f = 0..6 (line
   1860), no floor 7 and no pitched roof; nothing above our own apartment (cut-away, so the bird views work). Change:
   optional, add one storey and the hip roof (item 22) to the mass. Not visible from inside.
5. **Floors 1-4 footprint (d05, scaled).** One continuous bar from z -5.4 to z 42.6 with a double line (expansion joint)
   at z about 19.6 between A and B (crop `d05_joint_A_B.png`). Our apartment x -4.2..9.15 (model -4.28..9.30). A's other
   apartment (3, 5, 7, 9) z 9.1..19.6 and B's (3, 5, 7, 9) z 19.6..30.6, both x about -2.1..8.26. B's south apartment
   (2, 4, 6, 8) x -9.65..8.26, z 30.6..42.6. East balconies: ours; A's z 8.8..13.1 and B's z 26.3..30.6, both to x 10.3.
   B's south apartment has its balcony on the south side, x 2.4..7.2, z 40.0..43.5.
   Model: `building(-4.28, 7.70, 9.11, 38, 23.1)` (line 1859): x range and south end are wrong. Balcony boxes
   `[9.25, 13.2]` and `[26, 30.8]`, x 7.70..10.2 (lines 1860-1863): match within 0.3 m.
   Change: x -2.1..8.26 for z 9.11..30.6, and a second box x -9.65..8.26, z 30.6..42.6; both from floor 1 up (item 6).
6. **Pilotis ground storey (d03, written symbols and scaled; d08 6.2.10).** Under the middle apartments the ground floor is
   an open paved passage (brick-pattern pavers, dashed "קו קומה/מרפסת/פרגולה מעל" over it). Columns along x 8.15 at
   z about 13.4, 16.6, 19.9, 23.2, 26.3 (about 0.4 x 0.8, scaled). Closed core in the middle: lobby A ("A" in a circle)
   x -1.3..5.3, z 5.5..13.2 with its main door on the east side at about (5.1, 11.0); storage rooms ("מחסן מספר 1") and
   unlabelled rooms; a smoke vent; lobby B. d08 6.2.10: "ריצוף קומת עמודים מפולשת; חומר: אבנים משתלבות".
   Model: the mass stands solid on the street (line 1859). Change: start the mass at floor 1 for z 9.11..30.6, add the
   core box and the columns, pavers under it.
7. **Directly below apartment 4 (d05, d03, written).** Floor 1: apartment 2, same type ("דירה מספר 2, 4, 6, 8" on the
   floors 1-4 sheet), so the same plan and the same open balcony. Ground: the garden apartment ("דירה מספר 1"), a
   different plan: its living room under our master bedroom, dining and kitchen along the east, its master bedroom
   under our kitchen. Its east facade runs straight at x 9.25 from z -5.35 to 8.9. d03 draws the balcony-above line at
   x 10.45 from z -0.16 southward. Crop `d03_buildingA_ground_and_gardens.png`.
   Model: shell `B(-4.28, 9.30, -5.39, 9.11, GY, GY + 6.15)` (line 1866) is right for the ground storey but also fills
   floor 1's balcony zone (x 7.70..9.30, z -0.13..9.11). `B(BX1, BX2, BZN, BZ2, GY, GY + 6.6 - .45)` (line 1875) fills
   the space under our balcony solid to x 10.45. Panel line 195 describes a tiled floor-1 terrace.
   Change (storey height 3.3 is the model's estimate):
   - shell: ground storey `B(-4.28, 9.25, -5.39, 8.9, GY, GY + 3.15)`; floor 1 `B(-4.28, 9.30, -5.39, -.13, -3.45, -.30)`
     plus `B(-4.28, 7.70, -.13, 9.11, -3.45, -.30)` (exact cut-up is free; the faces are what matter);
   - floor-1 balcony: a copy of our deck, upstand and pickets (lines 1677-1681) at y - 3.30, x 7.70..10.45, z -0.13..8.71,
     with the floor-1 living facade openings A, B, C at x 7.70 (same plan);
   - line 1875: delete; the strip x 9.25..10.45 under the floor-1 balcony is garden (item 10).
8. **Ground-storey openings (d03, scaled, about 0.15 m).** East face x 9.25: openings at z -2.33..-1.26, 1.54..3.10,
   4.66..6.23, 7.97..8.73. North face: x 0.29..1.35, 2.15..3.69, 4.96..8.63 (the living room onto its pergola). West
   face: same as ours. Model repeats (lines 1868-1870) at dy -6.6: room 2 `.365..1.265` matches; master east
   `-2.17..-1.27` matches; master bath `6.015..6.615` is wrong at this level. Change: for dy -6.6 only, replace the
   master bath entry with `['x', 4.96, 8.63, -5.39, -1, 0, 2.35]` (sill 0 and head 2.35 are estimates) and add
   `['x', 2.15, 3.69, ...]` and the four east openings on face x 9.25 (sill and head estimates). Floor 1 (dy -3.3) keeps
   the present list.
9. **Floor-1 terrace east of x 9.30 (model lines 1899-1904).** Not on any of my sheets: d05 gives floor 1 the same
   balcony as ours, and d03 has garden at street level east of the ground facade. Recheck2 (`environment.md`) already
   called the photo reading ambiguous. **Conflict: plans vs the photo-based model.** Change: delete the terrace tiles,
   glass rail, aluminium posts and cap, and the stone podium wall `B(12.50, 12.80, -5.39, 9.11, GY, -3.64)`.

### Lot, gardens, fences, streets

10. **East garden strip (d03, written symbols, scaled).** x 9.25..12.68: green with the diagonal hatch (common garden;
    the legend's "שטח משותף לבנין" hatch over green). A blue line x 12.68..12.88 runs from the north lot line z -11.7 to
    z 9.83, where a blue line z 9.82..9.97 turns west to x 5.44. Then a second hatched-green strip x 12.88..14.1 to the
    lot line. "קולט מי גשם" points (flush, not modelled). Blue lines are not in the legend: they read as fences or low
    walls; no height written. Crop `d03_east_strip_entrances_streets.png`.
    Model: no ground treatment there. Change: `mat.turf` at GY for x 9.25..14.1, z -11.9..9.9; a boundary on
    x 12.7..12.9 (estimate: a 0.4 m kerb wall or a 1.0 m metal fence; ask the developer).
11. **Lot boundary (d03 thick blue; the same outline on d02, scaled).** North z -11.8 (x -22.3..14.3). West x -22.3
    (z -11.8..48.0). East x 14.2 from z -11.8 to 39.7, with gaps at z 9.98..14.92 and 28.47..30.59 (the two pedestrian
    entrances). South z 47.9 from x -22.3 to 6.2. The south-east corner is an arc, radius about 8.2 m, from (14.3, 39.7)
    to (6.2, 48.0). Lot about 36.6 x 59.8 m, about 2,170 sqm (scaled, estimate). Height: not on d03; d08 6.2.9 "גדר
    בחזיתות אחרות של המגרש: ... בטון ו/או ... אבן טבעית ו/או מתכת ... בגובה ממוצע: משתנה לפי תכנית פיתוח". Model: no
    lot fence. Change: fence or wall on that outline; height an estimate (about 1.2 m).
12. **Ali Mohar near side (d03, scaled; names from the sales plan key plan).** d03 names no streets. The sales plan key
    plan writes "עלי מוהר" along the east and "תרצה אתר" along the south, as the model has. East of the lot line, d03
    draws: a light-hatched strip x 14.3..16.9 (sidewalk), herringbone pavers x 16.9..18.8 along the whole frontage,
    ending with a rounded end at z 43.8 (parallel parking bays), then a curved kerb line and the carriageway from x 18.8.
    The sheet stops at x 23.4, so the road width is not on it. No street trees and no lamp posts drawn. Crop
    `d03_se_corner_streets.png`.
    Model (lines 1905-1914, 1949): sidewalk 12.8..14.3, kerb 14.3..14.45, parking on asphalt 14.3..16.6, carriageway
    16.6..23.0, cars at x 15.45.
    Change: `B(14.3, 16.9, ...mPaver)`; parking `B(16.9, 18.8, ...)` on pavers (herringbone, estimate pattern); kerb
    `B(18.8, 18.95, ...)`; asphalt from 18.8; near cars to x 17.85. The far side (bays, red sidewalk, school fence at
    x 32, school `SX1 = 32.5` line 1959, street lights x 28.4 line 1933, trees x 28.7 line 1921, far cars lines 1950-1953,
    walkway, lot, tower) comes from photos at about 5 m accuracy. Keeping the carriageway at 6.4 m means all of it moves
    +2.2 m east. That is my estimate, not written; the alternative (a 4.2 m road) is too narrow for two-way traffic.
13. **Pedestrian entrances (d03, scaled).** From Ali Mohar: a landing x 12.85..14.3 and a 3.0 m wide stair x 10.75..12.85,
    z 9.97..13.01 for building A; the same at z 28.5..30.5 for building B. Six tread lines 0.30 m apart, with a rail:
    about 6 to 7 risers, so roughly 1.0 m of level change (estimate). Up or down is not written, and no level is
    written anywhere on d03. Then the pilotis passage (item 6). Planters: blue-bordered green x 8.35..11.17,
    z 13.1..27.1; orange-outlined green x 12.4..13.8, z 14.9..28.5 (orange is not in the legend); a paved path between.
    Model: none. The A stair is 1.3 to 4.3 m south of our balcony's south wall and about 7 m below; it shows when looking
    down to the south-east. Change: add (heights are estimates).
    Note: the level change matters for `GY = -6.6` (line 1845). If the entrance floor is about 1 m above the sidewalk,
    the street would be at about -7.6. Not written; keep -6.6 and ask.
14. **North garden (d03, written symbols, scaled).** Bright green private garden of the garden apartment, x -1.2..9.2,
    z -11.7..-5.39, fenced by blue lines at x -1.29..-1.09 and 9.09..9.29. A pergola (vertical hatch) north of its living
    room, x 4.1..9.0, z -8.9..-5.4. Common garden west of it (to x -22.3) and the strip east of it. Crop
    `d03_buildingA_ground_and_gardens.png`. This is what room 2's north window, the master bath window and the north end of
    the balcony look down on.
    Model: the weeds plot `B(-6, 10.8, -48, -6, ...)` and its blue hoarding (line 2018) reach 5.9 m into our lot; paver
    strip `B(10.86, 12.8, -160, -5.39, ...)` (line 2019) runs through the garden.
    Change: weeds plot and hoarding to z -48..-11.9, east hoarding to x 14.3 (the hoarding's own position is a photo
    estimate); paver strip to x 14.3..16.9; turf for the lot north of the building; fences x -1.2 and 9.2 (height
    estimate 1.2); pergola x 4.1..9.0, z -8.9..-5.4 (posts and slats, top about GY + 2.8, estimate; d08 note 9 says metal
    and/or concrete).
15. **Smoke-release vents "פתח שחרור עשן" (d02 and d03, written).** At ground level in the gardens: x -2.7..-1.25,
    z -11.7..-8.65 and z -7.05..-5.4 (north garden); x 9.3..12.0, z -11.7..-9.6 (north-east corner, seen from the balcony);
    more by the passage (4.4, 19.8), at (11.9, 35.5), (-2.3, 27.0) and (-12.1, 42.4). No height written. Change: low boxes
    with a grille top (height about 0.8, estimate).
16. **Trees (d03).** One unlabelled circle, about 3 m across, at (-18.1, -8.2) in the north-west common garden, drawn
    like a tree but not in the legend. No other tree, and none on the street side. Model: "no trees on our side"
    (comment line 1919) matches; the far-side street trees (line 1921) are outside d03.
17. **Building B (d03, d05, scaled).** Ground: garden apartment 1B, x -9.85..8.32, z 30.6..42.9, with a private garden on
    the west (x -13.9..-3.5, z 28.3..35.9) and a pergola. Upper floors: item 5. Model: no B; the mass ends at z 38.
    Partly visible from the balcony along the facade, behind A's balconies. Change: item 5.
18. **Garbage and gas (d03, d08 table).** d03 has no garbage room. d08 table 1.3 lists "מע' פנאומטית לפינוי אשפה" in the
    basement and "פיר אשפה" on the floors, so there are no bins to model. "צובר גז תת קרקעי" (underground gas tank) at
    x -2.3..2.2, z 46.3..47.4: flush, not visible. Crop `d03_south_buildingB_gas_gate.png`.
19. **Paving material (d08 6.2.1-6.2.3, 6.2.10).** Paths, ground surfaces and the pilotis floor: interlocking pavers "ו/או
    אחר". The model's red-brown paver sets (lines 1881-1895) fit; the plan's brick pattern is drawing hatch, not a colour.

### What the west windows see

20. **West of the building (d03, d02, scaled).** Crop `d03_west_parking_ramp.png`.
    - Surface stalls 1 to 4: x -14.1..-8.65, z -2.9..7.1 (5.0 m deep), 4 to 10 m from the room 1 and mamad windows.
    - Stalls 5, 6 and two accessible stalls: x -7.8..-2.9, z 15.4..28.1, with an unlabelled box with a cross at
      x -7.3..-2.9, z 23.1..25.6.
    - Fire-truck pads (diagonal, "רחבת כיבוי אש"): x -14.3..-8.2, z 7.5..19.6, and x -21.5..-15.3, z 32.7..44.8.
    - Two-lane ramp along the west lot line, x -22.2..-15.2, with arrows down and up: it leaves grade at a portal at
      z about 21.4 and descends north to the basement at z about -0.6 (d02 draws the ramp at z -0.4..21.5).
    - Vehicle entrance: a gate (black bar) on the south lot line at x -22.1..-18.1, with a trench grating to x -14.
      So cars enter from Tirtsa Atar at the south-west corner.
    - An outdoor stair between walls, x -6.9..-5.2, z 1.1..5.75, right below the mamad window (purpose not labelled).
    - The common garden north-west, with the tree of item 16.
    Model: nothing west of the building except the ground plane and far blocks. Change: add stalls with markings, the
    pads, the ramp walls and the portal, the gate, the stair walls (heights estimates).
21. **Tirtsa Atar (d03, scaled).** South of the lot line: light-hatched sidewalk z 48.0..50.5; herringbone parking
    z 50.5..52.5 for x -13.0..9.8 with rounded ends; carriageway from z 52.5 (sheet stops at z 56.6). Corner kerb arc from
    (18.9, 44.4) to (10.1, 52.5), radius about 8.5. Model lines 1851-1852: asphalt z 44..52, kerbs z 42..44 and 52..54
    (the north kerb is inside the lot and under building B). Change: sidewalk z 48.0..50.5; parking z 50.5..52.5; asphalt
    z 52.5..60.5 (8 m kept, width not written); far kerb z 60.5..62.5; `foot` (line 2024) as above.

### Roof

22. **Roof of building A (d04, written symbols, scaled).** Crop `d04_roof_buildingA.png`.
    - Hipped tile roof over the north end: plan x -3.54..7.66, z -4.77..3.93. Hips from the north-west and north-east
      corners meet at (2.03, 1.27); the ridge runs south at x 2.03 to z 3.93. Ridge height not written. d08 note 7: "חלק
      מגג הבניין משופע".
    - An unlabelled rectangle cut into the west slope, x -2.17..0.69, z -3.37..2.67 (a roof terrace or skylight, unknown),
      and a small hatch near the apex.
    - Roof edge: x -4.25..8.36 at z -5.49, flush with our west and north outer walls, but 0.9 m inside our master
      bedroom's east wall (9.30). A thin lower edge at x about 9.1 for z -5.4..-2.3. So the top floor is set back on the
      east (floors 5 to 7 plans missing).
    - Stair and lift core (hatched "שטח משותף"): x -4.15..1.36, z 2.71..5.58, matching the model's core (line 898).
    - Flat roof x 1.36..8.08, z 3.93..7.68. Hatched common roof x -1.24..8.08, z 7.68..15.3 with "מעבר צנרת. מיקום לא
      סופי" (pipe passage, location not final).
    - Parapet: drawn as a double outline, lines about 0.1 and 0.2 m in from the edge; no height written.
    Not visible from the apartment. Change only if the building above floor 2 is ever drawn.
23. **Roof equipment (d04, written symbols).** Solar collectors: 7 on the east slope of the hip roof (x 3.85..7.66,
    z -2.45..3.52) and 6 on the flat common roof (x 2.67..7.12, z 9.6..14.1); building B 16. Each about 1.4 x 1.9 m in
    plan (scaled). No "דוד שמש" symbol on the roof (it is in the legend), so the tanks are not on the roof: d08 3.6.2 puts
    the 150 l heater in the laundry hide or the floor lobby, and the model has it in the niche. "הצמדה לפנטהאוס עבור
    מערכות טכניות. מיקום לא סופי": x -1.83..1.28, z 7.38..9.53, the penthouse's AC units and heater. Our condensers are
    not on the roof (the model keeps them in the niche, consistent). A column of 1.4 m squares at x 8.4..10.4,
    z -2.4..13.1, drawn below the roof edge: probably a top-floor balcony pergola (unlabelled).
24. **Basement (d02).** It fills the lot outline. Parking rows, storage rooms 1 to 23, "מאגר מים", stairs and lifts. Only
    the smoke vents (item 15) and the ramp (item 20) show above ground. Crop `d02_parking_39_40_storage_8.png`.

### Apartment annex d11 (pages 2 and 3)

25. **Balcony (written).** "מרפסת שמש בשטח של כ- 23 מ"ר"; of the three options, "מקורה" is kept and "מקורה חלקית על ידי
    קורות דקורטיביות/לא מקורה" is struck through. Model: `BX1..BX2` x `BZ1..BZ2` = 2.75 x 8.37 = 23.0 sqm (line 1677):
    matches. Covered: the model has the floor-3 soffit at `FT`: matches. The header "מרפסת 275 × 884" (line 129) is the
    sales plan's outer size (24.3). `CERAMICS.md` says "כ-24 מ״ר"; d11 says 23; both are above the 20 sqm limit for the
    15 x 60 balcony tile, so that conclusion stands.
26. **Apartment area (written).** "בשטח של כ- 130 מ"ר", computed per spec section 5. Header line 129 "כ-132 מ״ר" (the
    contractor's figure, owner's choice per `PROJECT_MEMORY.md`). **Conflict: d11 vs the header.** The owner decides.
27. **Laundry hide (written).** "מסתור כביסה בשטח של כ- 2 מ"ר". Model niche floor x 2.15..4.37, z -5.30..-3.99
    (line 880) = 2.9 sqm, from the sales and construction plans. **Mismatch** (d11 may measure it differently, per spec
    section 6). No geometry change; ask.
28. **Building, floor, rooms (written).** "רחוב עלי מוהר 6 (בניין A - צפוני)"; "דירה מס' (זמני) 4, בקומה 2, בת 5
    חדרים (כולל ממ"ד)". Model comment line 1841 and the header: match.
29. **Parking and storage (written; d02 scaled).** Stalls 39 and 40, about 12 sqm each, covered ("מקורה" kept), basement
    -1; storage 8, about 5 sqm. On d02: stalls 39 and 40 in the west row beside the ramp, centres about (-12.2, 17.9) and
    (-12.2, 14.9), each about 5.0 x 2.75 m (13.7 sqm scaled, vs "כ- 12" written); storage 8 at about (-11.8, 20.4),
    just south of them. Underground: not modelled.

### What the apartment sees, per the plans (summary of items 7 to 21)

30. - **Balcony, looking down and east:** floor 1's balcony directly below (hidden by our deck); at street level the
      common garden x 9.25..12.7, a boundary at 12.7, more garden to the lot fence at 14.2, the sidewalk 14.3..16.9,
      parked cars on pavers 16.9..18.8, the road from 18.8. To the south-east, the A entrance stair and planters. To the
      north-east, the garden corner with a smoke-vent box and the lot fence at z -11.8, then the neighbour plot.
    - **Balcony, looking south:** A's next balcony stack from z 8.8, then the long bar of A and B to z 42.6.
    - **Room 2 (north) and the master bath:** the garden apartment's private garden and pergola, two storeys down, the
      fences at x -1.2 and 9.2, two smoke-vent boxes, the lot fence at z -11.8.
    - **Master bedroom east window:** the east garden strip and the street, as from the balcony.
    - **Room 1 and the mamad (west):** the north-west garden with a tree, surface stalls 1 to 4 just below, the fire pad,
      the ramp along the far lot line at x -22.3, and an outdoor stair under the mamad window.

## Not representable in the 3D model (listed so nothing is skipped)

- d11: delivery "40 חודשים מקבלת צו התחלת עבודה"; the area-calculation and deviation clauses (3.3 to 4); the parking and
  storage attachment terms.
- d03: rainwater collectors "קולט מי גשם", absorption boreholes "קידוח ספיגה Ø50 / Ø60", sewer manholes "ביוב", the
  underground gas tank (flush or buried), the sheet's four notes (subject to permit, systems not yet coordinated, the
  common area to be fixed in the permit plans, possible changes to columns, shafts, beams).
- d02: everything underground (stalls, storage rooms, water reservoir, lifts, stairs).
- d04: "מיקום לא סופי" notes; vent symbols "קולטן/צמ"ג/צינור אוורור" on the roof.
- Meanings that are not in any legend: blue boundary lines (fence or wall?), orange outlines, the yellow strip at
  x -13.4..-12.3, z 42.6..47.7 with blue cells beside it, the cross-marked box near the accessible stalls, the cut in the
  west roof slope.

## Conflicts, in one place

| # | Between | What |
|---|---|---|
| 2 | AutoCAD sheets d01-d05 vs 2025 sales plan | true north 15.5 deg west of sheet-up vs exactly sheet-up |
| 3 | d11 vs sales plan | facing "צפון - מזרח" vs "צפון-מזרח-מערב" |
| 9 | d03, d05 vs model (from photos) | no floor-1 terrace east of x 9.30 |
| 26 | d11 vs model header | about 130 vs 132 sqm |
| 27 | d11 vs model (from the plans) | laundry hide about 2 vs 2.9 sqm |
| 29 | d11 vs d02 scaled | stall about 12 sqm vs 5.0 x 2.75 = 13.7 |
| 1 | sheet labels vs print | d02/d03 print at about 1:201, d04/d05 at about 1:149 (A3 reductions); scale by features, not by the label |
