# QA6 verify_spec: second pass over the sale spec (d08), annex C (d09), addendum (d10), apartment details (d11)

Method: every page of d08 (2 to 30), d09 (1 to 3), d10 (page 1 items 1 to 3 only, pages 2 to 3) and d11 (pages 2 to 3) read
as page images rendered at 150 dpi (`source/out/qa6_verify_spec/hi/`, not in git). Each item in `audit/recheck5/APPLIED.md`
re-checked against the page and against `source/salon.html` as it is now (3168 lines). No browser run was needed: every
finding below is read from the code. No personal data is quoted. Document crops (text only):
`audit/qa6/verify_spec_img/`.

Precedence used: d10 says its terms prevail over the agreement. d08 annex B note 5 puts the sale spec above the sales plans.

## Findings, most severe first

1. **Panel says the skirting is white, 8 cm. The model draws 7 cm in the floor material.** CONFIRMED.
   - Document: d08 p25, annex B: skirting from the floor material, "33x7 ס"מ ו/או 60x7" (crop `d08_p25_skirting.jpg`);
     d09 p1: "שיפולים (פנלים) דוגמת הריצוף, עד גובה 7 ס"מ".
   - Model: L950 `const SK = .07` and L971/L974 `skirtRoom(...r)` with `mat.tile` / `mat.planks` (applied in 5167387).
   - Panel L174: "פאנל לבן 8 ס״מ לאורך כל הקירות...". Stale since the re-check 5 change.
   - Fix L174: "פאנל 7 ס״מ מחומר הריצוף (במפרט: 33×7 או 60×7) לאורך כל הקירות בסלון, במטבח, בכניסה, במסדרון ובכל החדרים, עם
     הפסקה בכל פתח ודלת. בחדרי הרחצה אין, כי הם מחופים באריחים."

2. **Header area 132 m2; both contract documents write about 130.** CONFIRMED (listed as open in APPLIED, but the panel
   still shows only 132 and never mentions 130).
   - d08 p2 section 5: "שטח הדירה הוא: כ-130 מ"ר". d11 p2 3.1: "בשטח של כ-130 מ"ר".
   - Model L129: `<p class="sub">5 חדרים · כ-132 מ״ר · מרפסת 275 × 884</p>`.
   - Fix L129: `5 חדרים · כ-130 מ״ר (מפרט המכר) · מרפסת 275 × 884`, and add one sentence to the "מידות" note (L196): "שטח
     הדירה במפרט המכר ובנספח פרטי הדירה כ-130 מ״ר; הקבלן מסר 132." Owner decides which stays in the header.

3. **Master shower note presents the glass enclosure as from the plans. d08 says the shower has no enclosure, about
   80/80, floor slopes, and no fixed head.** CONFIRMED.
   - d08 p16 Table 4, column "חדר רחצה הורים": "כ- 80/80 (כ-0.65 מ"ר) ללא מקלחון", type "שיפועים ע"י ריצוף"; row "מקלחת ראש
     קבועה": "-" (crop `d08_p16_shower_bath_rows.jpg`). d08 p27 note 39(5): mixer "אינטרפוץ" plus a shower head on a rail.
   - Model: L1431 to L1434 fixed glass and a sliding door; L1437 wall arm with a head at 2.10. Panel L189: "מקלחון 106×92
     מהקירות, כמו בתוכנית האינסטלציה. זכוכית קבועה בצד האסלה ודלת הזזה בצד החדר."
   - The geometry choice is documented in spec_systems item 9 ("Note it in the panel"), but the note was never added.
   - Fix L189, append: "במפרט המכר המקלחת כ-80/80 בלי מקלחון ובלי ראש קבוע (שיפועים בריצוף, מוט ומזלף). הזכוכית והזרוע הן
     תוספת שלכם, לפי תוכנית האינסטלציה ומפרט הסטודיו."

4. **Family bath window drawn as a hinged window; d08 writes a sliding window.** CONFIRMED (code). spec_finishes item 38
   called the type a match; it is not.
   - d08 p14 Table 3, row "אמבטיה כללית (כולל אזור שירות)": 1 window, aluminium glazed, "כ.ע.כ", "כ- 80/80", no shutter
     (crop `d08_p14_family_bath_row.jpg`). Annex B p25 15.1: "ניגרר/כ.ע.כ = כנף נגררת על כנף".
   - Model L1476 `windowX(2.375, 3.575, -3.775, -3.99, 1.10, 2.10);` `windowX` (L842 to L849) draws a centre mullion and a
     tilt-turn lever (`lever(...)` L849). The sliders on the facade (`slider()`, L1048 to L1055) get a flat vertical pull instead.
   - Fix: give `windowX` a `pull` flag that draws the slider pull in place of the lever, e.g. at the end of `windowX`:
     `if (pull) B(mid + .03, mid + .05, zc + s * .03, zc + s * .05, sill + .3, sill + .6, mat.blackMetal); else lever(...)`,
     and call `windowX(2.375, 3.575, -3.775, -3.99, 1.10, 2.10, 2, true)`. Size stays (120 x 100 per the construction plan;
     the 80/80 conflict is already open).

5. **d10 item 6, insect screens, not drawn and not mentioned.** CONFIRMED.
   - d10 p2 item 6: windows of "חדר מגורים, מטבח, חדר שינה הורים (1), מקלחת הורים, חדר שינה (2), חדר שינה (3), ממ"ד (4) יהיה
     כולל רשת". The family bath is not on the list.
   - Model: no screen anywhere (no match for screen geometry near the windows; spec_systems item 82 left it "optional").
   - It is a contract item that shows on the two 270 cm living sliders. Fix (minimum): one sentence in the panel, e.g. in
     the "דלתות ווילונות" note: "לפי התוספת למפרט, בכל החלונות חוץ מחלון חדר הרחצה תהיה רשת נגד יתושים (לא מצוירת)". Better: a
     third, nearly transparent track leaf in `slider()` (a dark mesh at opacity about .15) on doors A and B and window C.
   - Side note: item 6 lists "מטבח", so d10 confirms a kitchen window exists. That settles C6 in spec_finishes (d08 Table 3
     has dashes for the kitchen) in favour of the model's window C.

6. **Mamad floor drawn flush with the corridor; d08 writes it higher.** CONFIRMED.
   - d08 p12 Table 2, mamad row, remarks: "ריצוף ממ"ד גבוה ביחס לגובה ריצוף מסדרון". d06 note 8 (APPLIED): up to 3 cm.
   - Model: L873 comment only; the mamad keeps the base floor from L869 `floor(-4.3, FX, -5.4, LZ, mat.tile, 0)` at y 0.
     APPLIED lists it as "not drawn".
   - Fix: `floor(-3.80, -.25, .125, 2.745, mat.tile, .02); floor(-3.83, -2.36, -.50, .125, mat.tile, .02);` plus a 2 cm
     threshold strip in the blast-door opening; raise the mamad skirting and furniture by .02 (or leave furniture; 2 cm is
     not visible on them). Height 2 cm is an estimate (written only "higher", d06 "up to 3").

7. **Basin bowls smaller than written, and the code comment misquotes d08.** CONFIRMED.
   - d08 p16 Table 4: "קערת רחצה ... כ-40/50 לפי יצרן" in both baths.
   - Model L1447 comment: "bowl about 40 (d08)". Bowls: master L1461 `ceramicTop(..., 4.56, 4.86, -3.96, -3.56)` = 30 x 40;
     family L1550 `ceramicTop(..., 2.12, 2.40, -2.315, -1.915)` = 28 x 40.
   - Fix: comment "basin about 40/50 (d08)"; widen the bowls to about 36 x 46 where the top allows (master top is 50 deep,
     so hx 4.52..4.88; family top is 48 deep, so hx 2.07..2.43), or keep and say in the comment that the bowl is the inner
     basin of a 40/50 unit (estimate).

8. **CER balcony note gives 24 m2; the documents give 23.** CONFIRMED.
   - d08 p3 6.1: "מרפסת שמש ... בשטח: כ- 23 מ"ר". d11 p2 3.2.1: "כ- 23 מ"ר". Model floor L1689 is 23.6 m2.
   - L3094: `note: 'במפרט ה-15×60 מיועד למרפסות עד 20 מ״ר. המרפסת כ-24 מ״ר, כדאי לברר עם הסטודיו.'`
   - Fix: "המרפסת כ-23 מ״ר (מפרט המכר)". The conclusion (above 20) does not change.

9. **Kitchen splash default is a ceramic tile; d10 item 1 replaced the ceramic with stone about 50 cm.** CONFIRMED,
   owner decision recorded in APPLIED, but the UI default still shows the non-contract option.
   - d10 p1 item 1: "חיפוי שיש בגובה כ-50 ס"מ מעל משטח ארון תחתון בלבד, למעט אזור חלון" (replaces d08 p10 and annex B p25
     "10/30 ... 20/50").
   - Model L3091 `def: 'k1030|וראנו לבן|g'`; the contract stone is only the "cur" option (L3092). Height L1344 .92..1.62.
   - Fix (if the owner wants the contract shown by default): `def: 'cur'`. Otherwise add to the kitB entry
     `note: 'בתוספת למפרט: חיפוי אבן כ-50 ס״מ. האריחים כאן מהסטודיו, לא פריט החוזה.'`

10. **Laundry-screen floor is plain grey; d08 gives it 33/33 anti-slip ceramic.** CONFIRMED (low; spec_finishes item 28
    noted it, never applied).
    - d08 p24 annex B flooring item 3: "ריצוף בחדרי רחצה ומרפסת שירות ... 33/33 ... אנטיסליפ".
    - Model L879 `floor(2.15, 4.37, -5.30, -3.99, mat.service, 0.003)`.
    - Fix: use the bathroom floor material there (`mat.terrazzo`, which the CER bathF space drives with 33x33) or a grey
      33x33 tile texture.

11. **Bathroom doors have plain levers; annex B asks for a vacant/engaged lock.** CONFIRMED (low).
    - d08 p25 15 ה: "בחדרי רחצה ושירותים, יותקן מנעול סיבובי 'תפוס/פנוי'".
    - Model L990 (family bath) and L993 (master bath) use `doorLeaf` (L834), which draws only levers (L839).
    - Fix: in the two calls add an `extra` that draws a small round turn (r .02, black) under the lever on the inner face.

12. **CER floor space name leaves out the mamad.** CONFIRMED (low, UI).
    - The mamad floor is `mat.tile` (L869, L873), which the `floor` space drives (L3081), named "ריצוף: סלון, מטבח, כניסה
      ומסדרון". A user who changes it changes the mamad too without being told.
    - Fix L3081: name "ריצוף: סלון, מטבח, כניסה, מסדרון וממ״ד".

13. **Stale comments that contradict the spec changes.** CONFIRMED (low).
    - L1523: "// glass screen and rain head at that (south) end": the rain head was removed (d08 Table 4 "-"). Change to
      "glass screen at that (south) end".
    - L1828: "(plans: תריס חשמלי at rooms 1-2, master, the two balcony doors and the kitchen window)": the kitchen shutter was
      removed (L1841). Change to "...the two balcony doors; none on the kitchen window (d08, electrical sheet)".
    - L1447: see item 7.

14. **Building A drawn as a flat 7-level bar; d08 Table 1 has 8 residential levels with a setback.** SUSPECTED as a
    visible issue (exterior only; APPLIED says floors 5 to 7 are not drawn, but the bar does reach floor 6).
    - d08 p5 to p7 Table 1, building A: entry floor 1 apartment, floors 1 to 4 two each, floors 5 and 6 one each, floor 7
      "קומת חללי גג" with a sloped ceiling; "סך כל הקומות למגורים 8"; annex B note 7 (p24): part of the roof pitched.
    - Model L1876 `building(-2.1, 8.26, 9.11, 30.6, 23.1, 'white', 3.3)`: full footprint to 23.1 m (ground plus 6), flat.
    - Fix (low): stop the full bar at 4 floors (h 16.5) and put a half-footprint mass for floors 5 to 6 plus a pitched or
      lower floor-7 mass on top; or keep and say in the L1873 to L1875 comment that floors 5 to 7 are not shaped.

15. **Small written items with no model counterpart** (low, all CONFIRMED absent):
    - d08 p18 3.7.1: one push button inside the apartment for the lobby light. Not drawn near the entry switch (L1018, `['n', 5.50, 2.66]`).
    - d08 p18 3.7.3: door bell (buzzer or gong). Not drawn.
    - d08 p16 Table 4: kitchen mixer "עם מתז נשלף" (pull-out spray). L1315 to L1318 draw a plain gooseneck.
    - d08 p18 Table 5: master intercom "1 שמע בלבד". Drawn as a data jack (L1826 'ds' group, x 5.74).
    - Room numbering: d08 and d10 number the rooms (1) master, (2), (3), (4) mamad, and d10 item 11 assigns the AC by those
      numbers. The view names (L2546 to L2548) say "חדר 1", "חדר 2", "חדר 3 · ממ״ד". Adding the contract number, e.g. "חדר 3 ·
      ממ״ד (במפרט: 4)", avoids confusion with the developer (APPLIED lists the mapping as open).

## Applied items re-checked against the page and the code (all fine)

- Ceiling 2.70: d08 p9 3.1 "לא פחות מ-2.70"; L255 `const H = 2.70`. Corridor minimum 2.30; L926 `DROP = H - .35` = 2.35.
  Panel L196 states both correctly.
- Mamad floor not parquet: d08 p25 "בממ"ד: אין להתקין פרקט ו/או ריצוף דליק"; L873 the mamad keeps `mat.tile`; panel L175
  says so.
- Skirting 7 cm in floor material: L948 to L974 (panel text wrong, item 1).
- Kitchen window C without shutter, sill at 1.20: L1841 comment, L1056 `slider(7.75, 8.45, 1.20, HEAD, 1)`, L1057 sill
  board at 1.17..1.20.
- Master shower window one kip sash: d08 p14 "קיפ או אחר", 1; L1425 `windowX(..., 1.25, 2.35, 1)`.
- Washer niche painted: d08 p11 service corner "טיח ו/או בגר"; niche walls no longer in the `tileX`/`tileZ` list (L1471
  to L1475).
- No fixed head over the bath: d08 p16 "-"; no head geometry left in L1523 to L1535 (comment stale, item 13).
- White flush plates: L1443, L1539 `mat.whitePlate`; d08 p27 39(7) fixtures white.
- One-piece ceramic tops and deck mixers: d10 p1 item 3 "ארון אמבטיה קומפלט (משטח חרס כולל כיור)", d08 Table 4 "בעמידה";
  L1447 to L1458, L1461, L1550.
- Master split condenser 84 x 40, pipes moved: d10 p2 item 11 (12,000 BTU split); L1576, pairs L1575 and L1579; comment
  L1819 cites 12,300 and 12,000.
- d10 item 10: island socket L1358, balcony socket + TV point L1846 ('st'). Three-phase hob point is under the induction
  hob (hidden, consistent).
- d10 items 7, 8, 9: Tami 4 on the coffee bar (panel L182), garden tap L1848 (cold, h .60), gas valve L1847.
- d10 item 2: tiles to the ceiling or to the drop in both baths: master L1419 to L1423 to `H`; family L1471 to L1475 to `H`
  behind the `BC` ceiling L1507.
- d10 item 11: mini-central for kitchen, living, dining, rooms (2), (3) and the mamad (room grilles L934 to L938, living grilles
  from L1156, mamad sleeves L941 to L944); corridor duct in a gypsum drop L928 to L929.
- d10 item 12: 80/80 with a glossy option (L3081 cats include `f80g`); wood-look 33x33 "מדרה" offered on the balcony (L2872,
  L3093).
- d10 items 4 and 5: entry door dark steel with a steel lever (L979 to L980); interior doors white `mat.door` (L525).
- Mamad: d08 p15 door steel blast door opening out, no inner door, 200 high; L992 leaf opens out, 2.04 tall over a 2.00
  opening. Window 100/100 with sliding steel and hinged aluminium; L1671 to L1672. Panel L194 correct.
- d11: balcony covered ("המרפסת מקורה"); balcony slab over it L1690 (2.70..2.95). Apartment faces north and east; panel
  L195 agrees.
- d08 Table 5 counts per room: I recounted the written points; every written point type has a model point or a documented
  hidden position, as in spec_systems section C. Extra fittings are design or from the electrical sheet. No new gap
  beyond item 15.
- d08 Table 1: ground floor is a garden apartment; floor 1 has our plan (panel L195, L1883 to L1886).
- d08 4.x, 5.x: no radiators, no floor heating, no sprinklers or smoke detectors in the apartment; none drawn.
- d08 3.6.2: 150 l solar tank in the laundry screen; L1583.
- d08 3.4: drying rack rods, aluminium louvers in the screen; louvers L1567, rack arms and lines L1581 to L1582.

## Open conflicts still standing (not model errors; already in APPLIED "Open", wording re-confirmed on the pages)

Door sizes (d08 p14 to p15: interior 70/200, master shower 65/200, entrance 80/200, mamad 70/200); window sizes (living
2 x 200/210, master 60/160, room (2) 60/180, room (3) 100/110, master shower 40/50, family bath 80/80); kitchen sink
acrylic white 40/60 flat (d08 p16, p27) vs stainless undermount; laundry screen about 2 m2 (d08 p3 6.7, d11 3.2.2) vs 2.9;
master shower 80/80 vs 106 x 92; dryer prep "אין" (d08 p17) vs the stacked dryer; worktop edge "חצי עיגול" (d08 p13) vs
square. Note: rooms (2) and (3) do differ in Table 3 (60/180 vs 100/110), contrary to spec_systems ("rows (2) and (3) are
identical in every table"); both kids' rooms in the model have 90 x 220 windows from the construction plan.
