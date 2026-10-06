# Re-check 5: technical sale spec (d08), finishes, heights, doors and windows

Scope: d08 ("מפרט מכר", 30 pages, edition 1 dated 05.10.26, apartment 4 (temporary), floor 2, type 5 rooms), pages 1 to 15
and 22 to 30. Pages 16 to 21 (sanitary table, electrical, AC, gas) belong to another report and are only cross-referenced.
Compared against `source/salon.html` as of commit 6b679fd (3105 lines). Report only; no tracked file was edited.

Conventions:
- "Written" = the words or numbers in d08. "Estimate" = my reading, not written anywhere.
- "Construction plan" = the 5/5/26 construction plan used in the third re-check (`audit/recheck3/geometry.md`); "sales plan" =
  the 2025-07-01 sales plan. d08 is dated after both.
- d08 annex B note 5 (page 24) sets the order when documents disagree: "מפרטי המכר, תוכניות המכר", i.e. the sale spec ranks
  above the sales plans. That is the contract rule, not a judgement that the spec is more accurate. Many d08 values look like
  form values (see items 29, 30), so conflicts below are flagged, not resolved.
- Crops: `audit/recheck5/spec_finishes_crops/` (spec text only, no personal data).

## Proposed changes, priority order

1. **Ceiling height `H` 2.60 to 2.70** (items 9, 10, 11). Written minimum 2.70; the corridor minimum 2.30 is broken today
   (`DROP` = 2.25). L255 `const H = 2.60`; follow-ups: L927 `DROP` becomes 2.35, L928 `BC` becomes 2.20, panel note L196;
   check coplanar faces at 2.70 (L902 `FT`, L1679 balcony soffit, L1024 ceiling plane) and the hard-coded heights L1414
   (closet LED 2.42), L1808 (master split 2.24..2.52), panel fan text L180. The mamad may be lower (item 12, estimate).
2. **Mamad floor must not be laminate or parquet** (item 15). Written: no parquet or other flammable floor in the mamad; the
   floor is porcelain and higher than the corridor. L873, L874 and the doorway strip in L883 use `mat.planks`, which the CER
   "rooms" space (L3021) drives. Give the mamad its own porcelain floor material and a small step at the blast door (height
   not written, estimate 2 cm).
3. **Remove the shutter on kitchen window C** (items 34, 40). d08 lists no kitchen window and no kitchen shutter; the
   electrical sheet shows no motor (recheck3). L1829, third call `shutterZ(7.75, 8.45, ...)`.
4. **Stale interior sill under window C** (item 35, found in passing, not from d08). L1057 sill board at y .97..1.00,
   z 7.67..8.42, unchanged since the initial commit; window C is z 7.75..8.45 with sill 1.20. Move to y 1.17..1.20,
   z 7.72..8.48, or remove.
5. **Master shower room window as one kip sash** (item 37). L1424 `windowX(6.015, 6.615, ...)` uses the default `panes = 2`;
   d08 writes "קיפ", one window. Add `, 1`.
6. **Bedroom windows with a fixed lower part** (item 36). d08 writes "דריי קיפ, חלק תחתון קבוע או אחר" for the master and both
   bedrooms; L1405, L1596, L1617 draw one full-height sash from .15 to 2.35. Add a transom and a fixed lower pane; transom
   height not written (estimate about 1.00).
7. **Skirting 7 cm in floor material** (item 51). L951 `SK = .08`, white. Written 33x7 or 60x7 from the floor material. Set
   `SK = .07` and use the floor tile in tiled rooms (bedroom laminate skirting stays a design choice).
8. **Master shower room tile to about 2.10, paint above** (item 18). L1419..L1423 tile to `H`. Written "כ-2.1 מ' או עד תחתית
   הנמכה". Cap at 2.10, or record full height as an owner upgrade (owner decision).
9. **Washer niche walls painted, not tiled** (item 19). Written plaster with synthetic lime for the service corner. L1462
   `tileX(-3.775, -3.09, 4.46, ...)`, L1463 `tileZ(3.69, 4.46, -3.09, ...)` and the part of `tileZ(3.575, 4.46, -3.775, ...)`
   east of x 3.69. Low: the cabinet (L1506) and machines hide most of it.
10. **Panel text** (items 2, 14, 15, 9): L129 "כ-132 מ״ר" vs d08 "כ-130" (owner chose 132; keep or show both); L175 add that
    the mamad cannot take laminate; L194 the mamad identification is now supported by d08; L196 ceiling 2.70 per d08 3.1.
11. **No change; raise with the developer** (section I): door widths and heights, entrance door, window sizes, the kitchen
    window itself, mamad leaf width, escape window, kitchen sink type, floor and wall tile sizes, vanity units.

## A. Identification and rooms (pages 1 to 4)

1. **Type, number, floor.** p1-2: "5 חדרים (4 חד' + ממ"ד)", apartment 4 (temporary), floor 2, building "A (בניין צפוני)".
   Model: L129 "5 חדרים", building A north (comment L1841..L1843). Matches.
2. **Apartment area.** p2 section 5: "שטח הדירה הוא: כ-130 מ"ר" (to the outer faces of the exterior walls, half of party walls).
   Model: L129 "כ-132 מ״ר" (the contractor's figure, owner decision 2026-10-04); net inside the model about 113.
   Conflict: d08 130 vs header 132. Within the 2% tolerance of p3 section 7, but not equal. Owner decision; no geometry change.
3. **Balcony area.** p3 section 6.1: "מרפסת שמש (ביציאה מחדר דיור) בשטח: כ-23 מ"ר". Model floor L1678: 2.75 x 8.37 + 1.15 x 0.47
   = 23.6 m2. Matches. Access from the living room: doors A and B (L1056). Matches. It also confirms the CERAMICS.md concern:
   23 m2 is above the 20 m2 limit for 15x60 balcony tiles in the studio spec.
4. **Laundry screen.** p4 section 6.7: "מסתור כביסה בשטח של כ-2 מ"ר". Model niche L880: 2.22 x 1.31 = 2.9 m2 inside the walls.
   Larger than written; the area method is not stated. Low; check against the sales plan by the geometry report.
5. **Room list.** p2 section 4: "חדר דיור, מטבח, פינת אוכל, 4 חדרי שינה כולל ממ"ד... מקלחת הורים, פרוזדור, אמבטיה כללית כולל פינת
   שירות ומרפסת דיור (שמש)". Model has all of them; the dining corner is replaced by the storage wall (owner decision, recorded
   in PROJECT_MEMORY). Matches. d08 numbers the bedrooms (1) master, (2), (3), (4) mamad; the model calls them room 1, room 2,
   room 3 (mamad). Which model room is d08 (2) and which is (3) cannot be told from d08 (items 29, 36).
   Note: the town field on p2 names a different town than the site and than the plan number prefix on the same page. Likely a
   form error; no model impact. Not repeated here (address data).

## B. Building (pages 4 to 9)

6. **Storeys of building A.** p4-7 Table 1: basement; entry floor with one garden apartment; typical floors 1 to 4 with 2
   apartments each; floor 5 with 1; floor 6 with 1; floor 7 "קומת חללי גג" with a sloped ceiling, part of the apartment below;
   roof with solar collectors and plant. "סך כל הקומות למגורים 8". Annex B note 7 (p24): part of the roof is pitched.
   Building B (south) is a separate building with 12 apartments. Model L1859: `building(-4.28, 7.70, 9.11, 38, 23.1)`, a uniform
   7-storey box called "the rest of building A" south of us; nothing is drawn above our own apartment. Written: 8 levels above
   ground with a setback above floor 4 and a pitched top. Exterior only; hand to the d03/d04/d05 reports (whether the south mass is
   A or B, setbacks, the roof).
7. **Exterior finish.** p8 2.6.1: natural stone and/or render and/or ceramic, "שליכט צבעוני". Model: white stucco on our shell
   (L603, estimate). Allowed option. Elevations would decide.
8. **Party walls, stair walls.** p8 2.7, 2.8.1: "עובי: כ-20 ס"מ". Model core walls are gross plan walls. No change.

## C. Heights (page 9, section 3.1) - crop `p09_heights.png`

9. **Ceiling height.** "גובה הדירה מפני הריצוף עד תחתית התקרה: לא פחות מ-2.70 מ' (במקומות בהן תהיה הנמכה - הגובה יפחת)".
   Model L255 `H = 2.60` (estimate). Change to 2.70. This is the first written ceiling height in any document so far. It agrees
   with the earlier cues: heads 2.35 plus a 35 cm shutter box (recheck3), and the drop below (item 10).
   After the change: L902 `FT = 2.70` and the balcony soffit underside L1679 (2.70) meet the ceiling plane L1024 at the same
   height; check for coplanar faces in top and bird views. Hard-coded heights to review: L1414 closet LED strip 2.42,
   L1808 master split 2.24..2.52, L180 panel text "הלהבים בגובה 2.35" (fans hang from `H`, L813). Ceiling fans, wardrobes,
   kitchen tall units and curtains follow `H` automatically.
10. **Corridor height.** "גובה פרוזדור: לא פחות מ-2.30 מ' (גובה לא סופי - תלוי בהנמכה)". Model L927 `DROP = H - .35` = 2.25,
    below the written minimum. With `H` 2.70 it becomes 2.35, which meets 2.30 and keeps the 35 cm net drop written on the AC
    plan. The living-room bulkhead (L1157), the TV bridge (L1141) and the kitchen soffit (L1212) follow `DROP`; d08 allows lower
    heights where there is a drop, so those are fine.
11. **Kids' (family) bath ceiling.** Not written in d08. Model L928 `BC = H - .50` (AC plan "-50") gives 2.20 after the change.
    No other change.
12. **Mamad ceiling (estimate).** d08 gives no separate mamad height. The construction plan "H=2.63" by the mamad sleeves
    (recheck3 item 3.8) could be a lower mamad ceiling under a thicker protected slab. Not written as a ceiling height; ask.
    If confirmed, the mamad needs its own ceiling at 2.63 and the sleeves at L940..L946 follow it.

## D. Table 2, rooms and finishes (pages 10 to 12) - crops `p10_kitchen_row.png`, `p11_baths_rows.png`, `p12_mamad_row.png`

General for every dry room (entry, living, master incl. closet, bedrooms (2), (3), corridor): walls block or concrete;
finish "טיח ו/או בגר בגמר סיד סינטטי ו/או טיח גבס"; floor "קרמיקה (פורצלן)".

13. **Wall and ceiling finish, dry rooms.** Written: plaster with synthetic lime (annex B note 12: walls "סופרקריל", ceilings
    "סיד סינטטי לבן"). Model: `mat.wall` white, with the CC0 `white_stucco` normal map at 0.35 (L602), `mat.ceil` white (L514).
    Colour matches. The stucco relief suggests a textured render that the spec does not describe; optional: lower the normal
    scale to about 0.1 (estimate) for smooth painted plaster.
14. **Floors, dry rooms.** Written porcelain in all of them, incl. the bedrooms (see item 49 for the size). Model: porcelain in
    living, entry, kitchen, corridor (L869); laminate-look planks in the bedrooms and closet (L870..L877), recorded as not from
    the spec (L175, CER "rooms" L3021). Design choice everywhere except the mamad (item 15).
15. **Mamad.** p12: walls "בטון מזוין או אחר לפי הוראות הג"א"; finish "עפ"י דרישות פיקוד העורף"; floor "קרמיקה (פורצלן)";
    remark "ריצוף ממ"ד גבוה ביחס לגובה ריצוף מסדרון"; use "חדר שינה". Annex B p25: "בממ"ד: אין להתקין פרקט ו/או ריצוף דליק אחר
    לפי הנחיות תקנות התגוננות אזרחית". Model: L873, L874 and the doorway strip in L883 use `mat.planks`, and the CER "rooms"
    space (L3021) drives the mamad together with the bedrooms. Change: a separate porcelain floor for the mamad (it could be a
    wood-look porcelain if the owners want the look; that is allowed, laminate or parquet is not). Add a step: mamad floor a
    little above the corridor floor (height not written; estimate 2 cm), visible at the blast door L992.
    The identification of room 3 as the mamad (panel L194, "כדאי לאמת") is supported: d08's mamad window 100/100 matches only
    room 3's window (L1671, 100 x 100), and its door is the outward blast door 70/200 (item 31).
16. **Kitchen.** p10: splash "חיפוי כ-50 ס"מ מעל משטח ארון תחתון בלבד, למעט אזור חלון"; above it plaster with synthetic lime to
    the ceiling; floor porcelain. Annex B p25: kitchen tiles "כ-10/30 ס"מ ו/או כ-20/50", "לגובה כ-50 ס"מ". Model L1344 splash
    .92..1.62 (70 cm) on the south and west walls, up to the wall cabinets at 1.62 (L1339); none on the window wall. Window
    exclusion matches. Height 70 vs 50: owner design (the cabinets start at 1.62), but a standard 50 cm splash would leave a
    20 cm painted strip. Record as beyond standard; no change. The default splash tile in CER "kitB" (L3029, 10x30) matches
    the written 10/30.
17. **Bathrooms.** p11, master shower room and family bath: walls "חיפוי קירות לגובה כ-2.1 מ' או עד תחתית הנמכה", above it plaster
    with synthetic lime; floor ceramic. Family bath: model tiles to `H` behind a ceiling at `BC` (L1461..L1465, L1497), so the
    visible tile stops at the drop. Matches "עד תחתית הנמכה".
18. **Master shower room tile height.** Model L1419..L1423 tile from 0 to `H` with no drop ceiling in the room, i.e. 2.60 now,
    2.70 after item 9. Written about 2.10. Owner upgrade or a change: cap at 2.10 and paint above (the window head 2.35 then sits
    in plaster). Owner decision.
19. **Service corner.** p11: "פינת שירות (אזור שירות כחלק מאמבטיה כללית)": walls and ceiling "טיח ו/או בגר בגמר סיד סינטטי"
    (no tile); floor ceramic. Model tiles the washer niche (L1462, L1463, "washer niche tiled (estimate)", fourth check). Written
    plaster; propose paint (low, mostly hidden by the cabinet L1506 and the machines).
20. **Balcony.** p12: walls "לפי סעיף 2.5", finish "גמר חוץ לפי סעיף 2.6", floor porcelain. Model balcony walls `mat.stucco`
    (L1680), floor `mat.deck` with the CER default 33x33 (L3031). Matches.
21. **Table 2 note.** "ייתכן מעבר צינורות אנכיים ו/או אופקיים ו/או קורות ו/או בליטות ו/או עמודים בולטים". Generic; the model has
    the pipe boxes from the MEP sheets. No change.

## E. Cabinets, section 3.3 (page 13) - crop `p13_cabinets.png`

22. **Lower kitchen cabinet.** Written: doors and shelves, carcass "סיבית מצופה פורמייקה"; worktop quartz ("אבן קיסר דגם 3200 או
    3460 או 3550 או שו"ע"), edge "פאזה בדגם חצי עיגול ללא הגבהות", thickness "לא פחות מ-18 מ"מ", length "לפי ארון מטבח תחתון ולא
    יותר מ-5 מ"א". Model: quartz 4 cm (L1304..L1306, L1357), square edges, no upstand. Thickness and no-upstand match; the edge
    profile is a cosmetic difference. Worktop length in the model: west run 1.17 + south run 3.03 + coffee bar 0.60 + island 1.60,
    about 6.4 m, over the 5 m standard (owner kitchen; recheck3 kitchen.md already treats the kitchen as an owner design).
23. **Upper kitchen cabinet.** Written "כ-3 מ"א (מדוד לאורך הקיר) כולל יחידת B.I", handles "מתכת מבריק" (two catalogue codes).
    Model L1339: wall cabinets west 1.17 + south 3.27 + tall wall 2.01, about 6.5 m, handleless with a black grip channel.
    Owner design beyond standard. No change.
24. **Kitchen note.** Dishwasher counts as 1 m of lower cabinet, oven and microwave column as 2 m. Explains the 5 m limit; no
    model impact.
25. **Other cabinets.** 3.3.3: "ארונות אחרים: אין" (no wardrobes, no vanity units in the standard spec). Model wardrobes and
    vanities are owner furniture. Conflict to note: the studio spec (d07, CERAMICS.md) offers vanity units 60/80 and 100/120;
    d08 3.3.3 lists none. Probably an annex or upgrade item (d10); no model change.
26. **"מצ"ב תכנית רגבה".** The supplier sheet is the kitchen supplier drawing already compared in `audit/recheck3/kitchen.md`. No new
    information in d08.

## F. Laundry, section 3.4 (page 13)

27. **Drying rack.** Written "מוטות ניצבים + גלגלים (כולל חבלים)". Model L1570..L1571: two steel arms at about 2.0 with lines
    between. Matches in type; pulleys and ropes not drawn (detail).
28. **Laundry screen.** Written "אלמנטים אנכיים או אופקיים או מרובעים", aluminium, size per architect. Model L1560: horizontal
    blades, 80% open. Matches. Annex B note 8: service balcony walls "גמר סיד סינטטי על גבי טייח"; note 45: water heater and AC
    unit in the drying area reduce the space. The model has both there (L1563..L1572). Matches. Floor: annex B flooring item 3
    gives the service balcony 33/33 anti-slip ceramic; model L880 is a plain grey `mat.service` without joints (low).

## G. Table 3, doors, windows, shutters (pages 14, 15) - crops `p14_doors_windows.png`, `p15_mamad_openings.png`

29. **Size order.** The column header says "(גובה/רוחב)", but the values only make sense as width/height (entrance "80/200").
    I read every value as width/height. Annex B note 15 ג: the sizes are the built opening "לפני הלבשות, מסילות"; note *** on p15:
    the final clear opening is smaller.
    Written vs model (widths x heights in cm; construction plan values from recheck3):

    | Opening | d08 | Construction plan | Model | Status |
    |---|---|---|---|---|
    | Entrance | 1, steel security door, hinged, 80/200 | 105/210 rough | net 97 (L900), leaf 1.01 x 2.11 (L979) | conflict |
    | Living | 2 windows, aluminium, sliding sash on sash, 200/210 | A and B 270 each, head 235 | 270 x 235 each (L1056) | conflict |
    | Kitchen | none (all dashes) | window C 70, sill 120 | slider 70, sill 1.20 (L1056) + shutter | conflict |
    | Master (1) | door 1, wood, hinged, 70/200; window 1, tilt-turn, fixed lower part, 60/160 | door 82/210; window 90, sill 15, head 235 | door 82 x 210 (L991); window 90 x 220 one sash (L1405) | conflict |
    | Master shower room | door 1, wood, 65/200; window 1, kip, 40/50 | door 75/210 rough; window 60, sill 125, head 235 | door 70 (L993); window 60 x 110, two panes (L1424) | conflict |
    | Family bath | door 1, wood, 70/200; window 1, sliding, 80/80 | window 120, sill 110 | door 83 (L990); window 120 x 100, two panes (L1466) | conflict |
    | Bedroom (2) | door 70/200; window tilt-turn, fixed lower part, 60/180 | 90, sill 15, head 235 | rooms 1, 2: door 83; window 90 x 220 (L1596, L1617) | conflict |
    | Bedroom (3) | door 70/200; window tilt-turn, fixed lower part, 100/110 | as above | as above | conflict |
    | Mamad (4) | door 1, steel blast door, outward, no inner door, 70/200; window 1 aluminium hinged plus steel sliding and hinged, 100/100; shutter aluminium sliding into a pocket, 100/100 | door 80 rough, "2+200"; window 100, sill 110, head 210 | door opening 79 x 200, leaf 86 x 204 (L922, L992); window 100 x 100 (L1671) | window matches; door see item 31 |

30. **Doors, general.** Interior doors "עץ לבודות" (hollow-core plywood), hinged, 70/200 (65/200 for the master shower room).
    Annex B 15.1: wood = two plywood skins on a frame. Model: white flush leaves 4 cm (L988..L993), bondor frames (L999..L1011).
    Type matches. Widths: d08 70 vs construction plan and sales plan 82 to 83 (75 for the master shower room); d08 widths are
    about 10 to 12 cm less than the rough openings for every interior door, which looks like a leaf or clear size (estimate).
    Heights: d08 200 vs construction plan 210 and model `DOORH` 2.10 (L255). Conflict; do not change `DOORH` without the
    developer's answer. Annex B 15 ה: bathroom doors get a "תפוס/פנוי" turn lock; the model has plain levers on the two bath
    doors (detail, optional).
31. **Mamad door.** Written "מתכת - דלת הדף רסיסים לפי הג"א", "ציר (רגילה) פתיחה חוץ (ללא הכנה לדלת פנים)", 70/200. Model:
    outward, hinge west, no inner door, opening head 2.00 (L922). Type and height match. Width: the construction plan has an 80
    rough opening and a leaf drawn about 70 (recheck3 item 3.5); d08 70 agrees with the drawn leaf. The model leaf is 0.86 wide
    (L992), surface mounted over the 79 opening. A leaf that closes over the frame must be wider than the opening, so 70 is
    probably the clear passage (estimate). Leave the leaf; ask the developer for the leaf size.
32. **Entrance door.** Written "פלדה - דלת מגן", hinged, 80/200; note (ד) "דלת כניסה לדירה: חומר: מתכת, סוג פתיחה: רגילה",
    lock to SI 5044; annex B 15 ד: finish and colour by the architect. Model: dark grey steel leaf (L979, `mat.entryDoor`),
    hinged. Type matches. Size conflicts with the construction plan (105/210 rough, 97 net). No change.
33. **Living windows.** Written 2, aluminium glazed, "נגרר כ.ע.כ", "כ-200/210". Model: two sliders of two panes each (L1056).
    Count and type match. Size: d08 about 200 wide and 210 high vs construction plan 270 wide (written) and head 2.35. Conflict.
34. **Kitchen window.** d08 has no kitchen window and no kitchen shutter. The construction plan writes window C (70, sill 120),
    and the model has it (L903..L904 wall, L1056 slider, L1074 zebra blind). Conflict on the window itself: keep it (the
    construction plan is a drawing of the actual facade, d08 may have dropped it). On the shutter, d08 and the electrical sheet
    agree: no shutter. Remove `shutterZ(7.75, 8.45, FO - .08, 1.20, HEAD)` (L1829). The 'r' plate at z 7.20 on the pier
    (L1830) may then be the switch for door B only; check against the electrical report.
35. **Stale kitchen window sill (found in passing).** L1057 `B(FX - .02, FX + .03, 7.67, 8.42, .97, 1.0, mat.sill)` is unchanged
    since the initial commit. Window C now spans z 7.75..8.45 with sill 1.20, and `slider()` draws no sill of its own. The board
    sticks 2 cm out of the wall at 0.97 below the window. Move it to y 1.17..1.20, z 7.72..8.48 (or remove).
36. **Bedroom windows (master, (2), (3)).** Written "דריי קיפ, חלק תחתון קבוע או אחר", aluminium glazed, 1 each. Model: one
    full-height sash per window (`panes = 1`, L1405, L1596, L1617), the master transom bar removed in the third re-check. With a
    sill at .15 a fixed lower pane is the usual safety solution. Change: add a horizontal transom and fixed lower glazing in the
    three windows (the transom height is not written; estimate about 1.00, which also makes the master window's outside bars at
    L1406 redundant). Sizes conflict (60/160, 60/180, 100/110 vs 90 x 220 on the construction plan); not changed.
37. **Master shower room window.** Written "קיפ או אחר", 1, 40/50, no shutter. Model L1424 two panes with a centre mullion
    (default `panes = 2`), no shutter. Shutter matches. Set `panes = 1` (a kip window is one sash). Size conflict (40/50 vs 60
    wide, sill 1.25, head 2.35).
38. **Family bath window.** Written "כ.ע.כ" (sliding), 80/80, no shutter. Model L1466 two panes, no shutter. Type and shutter
    match. Size conflict (80/80 vs 120 x 100).
39. **Mamad window.** Written aluminium glazed hinged plus steel "נגרר + ציר", 100/100; shutter aluminium foamed slats
    "נגרר לכיס", 100/100. Model L1671 one hinged sash 100 x 100, steel blast frame L1672, no shutter. Matches (the steel sash and
    the pocket shutter sit in the wall pocket when open).
40. **Shutters.** Written "גלילה חשמלי", foamed aluminium slats, box included, in the living room (2), master, bedrooms (2), (3):
    5 electric shutters. Model L1826..L1829: room 1, room 2, master, A, B, plus window C. All match except C (item 34).
41. **Escape window.** p15 note *: a window defined as an escape window gets no bars and a manual shutter release. Which window
    is not stated. If it is the master window, the outside bars at L1406 would be wrong. Ask.
42. **Guest WC ventilation.** p15 note **: forced ventilation in a guest WC "ככל וקיים". There is no guest WC. No change.

## H. Annex B, general notes (pages 24 to 30) - crops `p24_notes_5_to_10.png`, `p24_flooring.png`, `p25_mamad_cladding_skirting.png`, `p27_sanitary.png`

43. **Note 1, gross dimensions.** "המידות המתוארות בתכנית הן מידות בניה (ברוטו) מקיר בניה לקיר בניה". Model walls are gross
    (DESIGN.md). Matches.
44. **Note 5, precedence.** Spec above sales plans. See the conventions at the top.
45. **Note 8, balcony railing.** "בנוי ו/או מתכת (מגלוונת וצבועה) ו/או אלומיניום ו/או מזוגג, ו/או משולב". Height not written.
    Model L1681..L1685: a 45 cm upstand (estimate) with black steel bars to 1.09 (1.13 above the deck at `BY` -0.04). Allowed
    option. The other balconies of the building are drawn with glass railings (L1860..L1863); one building would normally have one
    railing type, but d08 does not settle which. No change.
46. **Note 9, pergola.** Only if on the sales plans. None in the model. Matches.
47. **Note 10, level differences.** Between bathrooms, mamad and balconies and the next spaces; "יתכן סף מוגבה/מונמך" at balcony
    exits. Model: balcony deck 4 cm lower (L1677 `BY`), bathrooms flush, mamad flush (item 15). Heights not written.
48. **Note 11, tiles.** Slip resistance to SI 2279; no mitred corners in cladding or skirting; spare tiles. Not visible, except
    "ללא גרונגים", which the model's square tile edges already follow.
49. **Flooring sizes** (p24 items 1 to 4). Living, kitchen, passages "כ-60/60"; bedrooms and mamad "כ-60/60"; bathrooms and service
    balcony "כ-33/33" anti-slip; balconies "כ-33/33" anti-slip, "גמר הריצוף ייושם בשיפועים". Model CER defaults: living 80x80
    (L3019, studio catalogue), bathrooms and balcony 30x30/33x33 (matches), base texture 120x120 ("cur"). Conflict: d08 standard
    60/60 vs the studio spec's 80x80 for the main floor (d07, CERAMICS.md). Not resolved here; the d07 or d10 report should say
    which document governs. The balcony slope is not modelled (flat deck; fine at this scale).
50. **Wall cladding sizes** (p25). Bathrooms "כ-30/60 ס"מ ו/או כ-20/25"; kitchen "כ-10/30 ו/או כ-20/50", 50 cm high. Model CER wall
    options include 25x75 (studio) and 30x60. Same d08 vs d07 question as item 49. Straight laying, not diagonal: the model grids
    are straight. Matches.
51. **Skirting** (p25). "מחומר הריצוף... פנלים תואמי ריצוף בגודל 33x7 ס"מ ו/או 60x7"; none at clad walls, behind kitchen units,
    wardrobes or technical areas. Model L951: white skirting 8 cm (`SK = .08`, colour `#e4e2dc`) in the dry rooms, with
    `noSkirt` boxes at the kitchen, wardrobes and storage (L953). Exclusions match. Height and material do not: set `SK` to .07
    and use the floor material in tiled rooms (the bedroom laminate skirting is a design choice).
52. **Note 12, finishes.** Walls "סופרקריל או אחר", ceilings "סיד סינטטי לבן". See item 13.
53. **Note 14, kitchen.** Door colour from 3 standard colours, worktop from 3 samples. Owner kitchen; no change.
54. **Note 15, door and window definitions.** "ציר" hinged, "קיפ" bottom-hung tilt, "דריי קיפ" tilt-turn, "כ.ע.כ" sliding sash on
    sash or into a pocket, "גלילה" roller shutter, manual strap or electric. 15 ג: opening type, fixed glazed parts and number of
    sashes may change. Used for items 29 to 41.
55. **Note 16, gas.** Gas piping to and inside the apartment. Model: gas valve on the balcony (L1834, electrical sheet). The
    kitchen gas point is in Table 4 (p17, other report); the model hob is induction (owner choice). No change.
56. **Note 17, electrical.** Light point = lamp holder without bulb or shade; fittings "גוויס" or equal. The model plates are
    generic white. Not worth modelling.
57. **Note 39, sanitary** (p27). Kitchen sink "אקרילי, התקנה שטוחה", "כיור במטבח לבן"; basins and WC ceramic, WC wall-hung;
    kitchen tap "פרח/מיקס ברז נשלף"; bath mixer with a hand shower; shower "אינטרפוץ... בציפוי כרום ניקל + ראש מקלחת"; fixtures
    white. Model: stainless undermount sink 70x45 (L1305..L1309), black taps, wall-hung WCs with concealed cisterns. Conflict:
    d08 acrylic white kitchen sink vs the studio spec's stainless (CER_FIXTURES L3040, d07 page 25). Black taps are the studio
    picks (Omega black), not the chrome of d08. Owner choice from the studio; no change, but the sink type should be confirmed.
58. **Note 45, water heater and AC in the drying area.** Matches the model (item 28).
59. **Note 46, sprinklers.** Location per fire rules, if installed. d08 does not say the apartment has sprinklers, and no MEP
    sheet showed any. No change.
60. **Note 55, pipe boxes.** Pipes may need column-like or beam-like boxes or "ספסלים" by walls, ceilings and floors, not
    necessarily on the sales plan. Generic; the model has the boxes from the MEP sheets.
61. **Note 56, mechanical ventilation.** A fan in the bathrooms, if installed, switched with the light. The family bath window
    opens into the semi-closed laundry screen, so a fan is plausible, but not written. No change.
62. **Note 69, mamad filtration.** "במידה והותקנה מערכת סינון דירתית". The model has a filter unit on the mamad west wall
    (L1792). Allowed; whether one is supplied is not written.

## I. Conflicts, listed once

| # | Item | d08 | Other document | Model follows |
|---|---|---|---|---|
| C1 | Apartment area | 130 | contractor 132 | 132 (owner) |
| C2 | Interior door width | 70 (65 master shower) | 82 to 83 (75) construction and sales plans | plans |
| C3 | Door heights | 200 | 210 construction plan (200 for the mamad) | 2.10 (2.00 mamad) |
| C4 | Entrance door | 80/200 | 105/210 rough construction plan | 97 net |
| C5 | Living windows | 2 x 200/210 | 2 x 270, head 235 | construction plan |
| C6 | Kitchen window | none | window C 70, sill 120 | construction plan |
| C7 | Bedroom and bath windows | 60/160, 60/180, 100/110, 40/50, 80/80 | 90 x 220 (three), 60 x 110, 120 x 100 | construction plan |
| C8 | Mamad door width | 70 | 80 rough, leaf drawn about 70 | leaf 0.86 |
| C9 | Main floor tile | 60/60 | 80x80 studio spec (d07) | 80x80 default |
| C10 | Bath wall tile | 30/60 or 20/25 | 25x75 studio spec | 25x75 default |
| C11 | Kitchen sink | acrylic, white, flat | stainless, studio spec | stainless |
| C12 | Vanity units | none (3.3.3) | studio spec 60/80, 100/120 | owner units |
| C13 | Laundry screen area | about 2 m2 | model 2.9 m2 inside the walls | sales plan walls |

## J. Not shown in a 3D model (checked, no model impact)

Legal and identification data (plot, plan number, owners, buyers, designers, contacts; not copied here), parking and storage
attachments and their areas, area calculation rules and tolerances (p3-4, p24 note 2), building permit condition, lobby and
stair finishes, lifts, building entrance door, basement finishes, structure and slab materials (2.1 to 2.5), maintenance
documents (annex A), religious note, standards references, house committee and common property rules (9.5 to 9.7), payments
and credits (notes 16, 66; not copied), electrical fitting brand, TV antenna and cable, plot boundaries, easements, municipal
pillars and manholes, rockeries and planters, penthouse stairs, buyer changes and delays, sanitary replacement responsibility,
storage and parking ceilings, gas tank location, stone texture variation, cleaning on handover, maintenance access, concrete
floor cracks, paver settlement, access to technical areas, professional maintenance, building maintenance standard, electric
company area, model apartment disclaimer, separation wall integrity, AC warranty, gas vehicles in the basement, vehicle
dimensions.
