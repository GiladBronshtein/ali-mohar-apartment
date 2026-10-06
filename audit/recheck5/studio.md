# Re-check 5: studio spec d07 against the ceramic picker

Document: d07, "מפרט מוצרים - סטנדרט", Ali Mohar 6-8, dated 05/10/2026, 31 slides (file title "including flooring in a
glossy finish"). Compared with `CERAMICS.md`, the `CER` catalog (salon.html 2781-2849), `CER_FIN` (2850), `CER_SPACES`
(3018-3033), `CER_FIXTURES` (3034-3043), the tile materials (515-516, 573) and the 3D fixtures they describe.

Method: per-page text (pdftotext) and every slide image read. The older catalog the picker was built from (10/02/2026,
30 slides, kept outside the repo) was diffed against d07 page by page, both as text and as rendered images (pixel diff
at 40 dpi, page-number corner masked). Swatch colours sampled from the slide images (median of the swatch, same method
as the existing hexes: for example the model's `פלזה אפור` #a8a7a5 equals the sample). A glossy floor was simulated in
the live site (floor roughness scaled to about 0.1) to see how it reads.

"Written" means printed in d07 (or the named document). "Estimate" means mine.

## Proposed changes, priority order

1. Add the new glossy 80x80 page as a catalog group `f80g` and offer it in the two dry-floor spaces (items 4, 5, 6).
   Insert after line 2795; add `'f80g'` to `cats` on lines 3019 and 3021. Code in item 6.
2. Renumber every catalog page from 5 on by +1, in `CER` (lines 2796, 2802, 2811, 2815, 2822, 2827, 2831, 2836, 2840,
   2844, 2848) and in `CER_FIXTURES` (3035-3042); update the spec date on 2775 and 3085 and in `CERAMICS.md` line 3
   (items 2, 3, 22).
3. Make a glossy floor actually look glossy: lower bump for gloss tiles (line 3012) and raise the day env intensity
   for gloss floors in `cerApply` (3045-3058); optionally a blended floor reflection on desktop HQ (item 7).
4. Flush plates: the model draws black plates (1442, 1530); the spec offers only chrome, brushed or white. Make them
   white square, as `CER_FIXTURES` already says (item 26).
5. Basin taps: the model draws wall spouts (1451, 1543); every basin tap in the spec is deck-mounted. Move to a short
   deck mixer behind the basin (item 23).
6. Bath tap text: `CER_FIXTURES` says "סוללה" (exposed bar mixer) but the model and the plumbing plan have a concealed
   4-way mixer and a filler through the overflow. Align the text (item 24).
7. Finish labels not written in the spec: `מילניום 7.5/15` (2839) and `וראנו טאופה` (2846) carry `f: 'g'`; set `f: 'u'`
   (items 15, 17).
8. Kitchen sink text: "נירוסטה" is the inset sink, the model draws an undermount bowl (1307). Pick one (item 28).
9. Open questions for the owner and the studio, not resolved here: glossy as default or not (item 5), 60x60 in dry rooms
   after the 80/80 annex (item 9), bedroom and mamad wood-look default (item 10), balcony 15x60 limit and the new
   "parquet-like" balcony option (item 13), vanity sizes (item 29), kitchen splash material and height (item 31).

## A. Version: same catalog plus one page

1. **Same spec, newer edition.** d07 p1: "מפרט מוצרים- סטנדרט", "05/10/2026", 23 units. `CERAMICS.md` line 3 and
   salon.html 2775/3085 cite "10/02/2026, 30 עמודים". Text of all 30 old pages equals the new text except the date and
   page numbers. Images: pixel-identical except old p8/new p9 (header moved about 1 px, same wording) and the cover date.
   No product was removed, renamed, resized or refinished. Model: built from the 10/02 edition. Change: date only
   (item 3) and the page shift (item 2).
2. **One page inserted: p5, "ריצוף חדרים יבשים | גרניט פורצלן | מידה: 80x80 ס"מ | גימור: מבריק".** Six products:
   מרפיל בז', רוסו אפור, לורה בג', ארמאני אפור בהיר, רוקי אפור, קררה. Everything after it moved by one page:
   old 5 to 6 (60x60), 7 to 8 (15x60), 8 to 9 (30x30/33x33), 10 to 11, 11 to 12, 12 to 13, 13 to 14, 14 to 15, 15 to 16,
   16 to 17 (kitchen), 19 to 20 (WCs), 20 to 21 (baths), 21 to 22 (accessories), 23 to 24 (Omega taps), 25 to 26
   (kitchen sinks), 26 to 27 (kitchen taps), 28 to 29 (Studio cabinet). Model: no glossy floor anywhere in `CER`
   (2781-2849). Crop: `studio_crops/d07_p5_glossy_80x80.png`.
3. **Page numbers shown to the user are now wrong.** `cerDesc` prints `עמ׳ ${CER[cat].page}` (2858) and the optgroups
   print it (3065). Change `page:` values: f60 5 to 6 (2796), w30 8 to 9 (2802), w1560 7 to 8 (2811), c2575a 10 to 11
   (2815), c2575b 11 to 12 (2822), c3060a 12 to 13 (2827), c3060b 13 to 14 (2831), c3060c 14 to 15 (2836), c2060 15 to
   16 (2840), k1030 16 to 17 (2844), k2020 16 to 17 (2848). f80a (p3) and f80b (p4) stay. Date "10/02/2026" to
   "05/10/2026" on 2775 and 3085. `CERAMICS.md`: date, "30 עמודים" to 31, and the page column (3 stays; 8 to 9, 11 to 12,
   16 to 17; fixtures 23 to 24, 21 to 22, 20 to 21, 19 to 20, 25 to 26, 26 to 27, 28 to 29).

## B. The glossy floor

4. **Which floors.** d07 p5 heading "ריצוף חדרים יבשים" (dry rooms), 80x80, "מבריק". d10 item 12 (annex to the technical
   spec) amends annex B section 11 items 1 and 2 to "כ 80/80 ס"מ ... כולל אפשרות לריצוף בגימור מבריק כמפורט במפרט
   סטודיו קרמיקה". In d08 those items are living room, kitchen and passages (1) and bedrooms and mamad (2). So the glossy
   option covers the model spaces `floor` (3019, `mat.tile`: living, kitchen, entry, corridor) and `rooms` (3021,
   `mat.planks`: bedrooms, mamad, closet). Written. It does not cover baths or the balcony (anti-slip pages only).
5. **Default.** d07 and d10 say "אפשרות" (an option); neither says the owners chose glossy. Model: `floor` default
   `f80a|מלרוז אפור|m` (matte, p3), `rooms` default `cur` (oak laminate, not from the spec). The default still matches
   the documents. Whether the owners want glossy as their pick is a question for them; I do not change the default.
6. **Products, sizes, colours.** All six are 80x80 porcelain, finish glossy (header). Swatch medians from the slide
   (sampled): מרפיל בז' #f6eee8 (plain stone, very fine speckle), רוסו אפור #e7e7e7 (white-grey marble, many thin grey
   veins), לורה בג' #eee6d9 (cream marble, faint lighter veins), ארמאני אפור בהיר #ece9e4 (white marble, tan veins),
   רוקי אפור #b8b8b8 (mid-grey stone, soft darker clouds), קררה #d8d8d8 on the slide (the matte `קררה מט משי` on p4
   samples the same and the model uses #e4e4e2 for it). Vein colours are my estimate from the 200 dpi crop.
   Note: מרפיל בז' also exists matte on p4 (model 2791); the glossy one is a separate product line on p5.
   Proposed group, after line 2795:
   ```js
   f80g: { t: 'ריצוף 80×80, מבריק', size: '80×80', page: 5, w: .8, h: .8, nx: 2, ny: 2, fin: 'g', items: [
     ["מרפיל בז'", '#f6eee8', 'stone'], ['רוסו אפור', '#e7e7e7', 'marble', { v: '#8e8984' }], ["לורה בג'", '#eee6d9', 'marble', { v: '#f8f2e8' }],
     ['ארמאני אפור בהיר', '#ece9e4', 'marble', { v: '#c9a98a' }], ['רוקי אפור', '#b8b8b8', 'marble', { v: '#a2a2a2' }],
     ['קררה', '#e4e4e2', 'marble', { v: '#8f8f8d' }]] },
   ```
   and `cats: ['f80a', 'f80b', 'f80g', 'f60']` on 3019 and 3021. Keys stay unique (`f80g|מרפיל בז'|g` vs
   `f80b|מרפיל בז'|m`); the option label gets "(מבריק)" from `CER_FIN.g` automatically (3066). Saved choices in
   `ali-cer` are unaffected.
7. **Does the model's gloss match?** Base floor: `mat.tile` roughness 0.58 (515), detail map range .42-.78 (573): matte,
   right for the default. A spec tile gets per-pixel roughness from `CER_FIN` (2850): `g` is .05-.14, which is the right
   range for a polished glazed porcelain (estimate). But the viewer cannot show it: I scaled the live floor to about 0.1
   roughness in the `sofa` view and the frame barely changed. Reasons: `mat.tile` is a `MeshStandardMaterial`, day
   `envMapIntensity` is `ENV = .3` (2325), the env is the generic `RoomEnvironment` (276) or the sky, and there is no
   floor reflection (the `Reflector` at 789-800 is used only for mirrors). Proposed, all estimates:
   - 3012: `bumpScale: reliefKind ? 1.1 : (CER_FIN[cerFin(cat, it)][0] === 'מבריק' ? .15 : .55)`; a polished face has no
     surface relief, and bump plus low roughness gives glitter.
   - `cerApply` (3051-3057): when the space is a floor and the finish is `g`, set `m.userData.envDay = .7` and
     `m.envMapIntensity = isEve ? .12 : .7`; clear it (`delete m.userData.envDay`) on any other choice. 2620 and 2626
     already honour `userData.envDay`.
   - Optional, desktop HQ only: a floor reflection blended at about 6 to 10 percent with a Fresnel rise (custom shader
     using the `Reflector` texture matrix; the stock `Reflector` output is opaque, so it cannot simply be laid on the
     floor). Without it a glossy floor reads as matte in the live view. The path-traced photo mode
     (`pt.updateMaterials`, 3058) should show the gloss correctly as is.
   - Baked mode (`?baked=1`) still ignores swaps (known, PROJECT_MEMORY).
8. **Grout and laying for 80x80.** d07 writes no grout width or colour and no pattern. d08 annex B writes "ישרה ולא
   באלכסון" (straight, not diagonal). Model: straight 2x2 grid per texture (`nx: 2, ny: 2`), joint about 3 mm
   (`gp`, 2944), grout colour derived from the tile (2946). Matches d08; widths are estimates.

## C. Spaces and options

9. **`floor` and `rooms`, 60x60 group.** d07 p6 lists 60x60 matte for dry rooms (18 products, model 2796-2800, all 18
   present, names as printed including "מונטריאול" with the extra vav). d08 annex B writes "כ 60/60" for these rooms, but
   d10 item 12 replaces that with "כ 80/80". Conflict between d07 (still offers 60x60) and d10 (contract size 80/80).
   Not resolved: keep `f60` in the list, or mark it in its optgroup label as replaced by the annex. Owner decision.
10. **`rooms` default is wood-look laminate.** Model 3021 `def: 'cur'` ("דמוי פרקט אלון ... לא מהמפרט"), floors 870-877
    including the mamad (873-874). d07 offers no wood-look tile for dry rooms (wood-look only on p8 15x60 and the p9
    "דמוי פרקט" 33x33, both wet rooms and balconies). d08 annex B: "בממ"ד: אין להתקין פרקט ו/או ריצוף דליק אחר".
    Conflict between the model default and d08 for the mamad at least. The label already says "not from the spec";
    a change would be to give the mamad its own floor (or `mat.tile`) so a wood look never shows there. Owner decision.
11. **`f80a` p3 and `f80b` p4.** 22 and 19 products, all present with exact names (2783-2795). Finish "מט" in the header;
    names with "משי" and "לאפטו" are inferred to silk and lappato by `cerFin` (2852). Matches.
12. **`bathF`, `ensF` (wet floors).** d07 p8 15x60 R10 and p9 30x30/33x33 R10/R11, both "אנטי סליפ". Model 3023 and 3025
    offer `w30` and `w1560`; 27 and 12 products present (2803-2814), names exact, finish `r`. d08: wet rooms "כ 33/33",
    anti-slip. Defaults לוגנו סטון and מלרוז אפור (33x33) match both documents. Model tile modelled 33 cm (`w: .33`); d07
    writes "30x30/33x33" without saying which product is which size.
13. **`balc`.** d07 p8 heading "R10 - מרפסות עד 20 מ"ר" for 15x60. Model 3031 offers w30 and w1560, default מלרוז אפור
    33x33, with the existing note that the balcony is about 24 m2. New: d10 item 12 adds for annex B item 4 (balconies)
    "כולל אפשרות לריצוף דמוי פרקט כמפורט במפרט סטודיו קרמיקה". In d07 the wood-look tiles are the p9 מדרה series (33x33,
    no size limit written) and the p8 15x60 series (limited to 20 m2). Suggested note text change on 3032: mention that
    the מדרה 33x33 series is the wood look with no area limit. Not a default change.
14. **`bathW`, `ensW`, `ensA` (wall cladding).** d07 p11 and p12 "חיפוי חדרים רטובים" (25x75), p13-p16 "חיפוי חדרים
    רטובים ומטבחים" (30x60, 20x60). Model `CER_WALL` (3017) = those six groups. All 20+15+10+12+11+12 products present,
    names exact. Per-item finishes on p11 (לבן מט / מבריק, דאלקי "ברילו" glossy, סמפר קררה מבריק, others not written)
    match 2816-2821. Orientation: model lays 25x75 and 30x60 landscape (`w: .75, h: .25`); d07 shows the swatches
    landscape but writes no direction (estimate). Defaults סהרה אייבורי, מיסטרל אייבורי, מיסטרל אייבורי דקור, all "מט"
    on p12. Matches.
15. **`c3060c` p15 finishes.** Printed: קררה and קררה דקור (no finish), מונה בז' מט, מונה בז' רלייף מט, וינה אפור מבריק,
    ליסה קרם מבריק, לבן מבריק, לבן מט, מילניום 7.5/15 (no finish), אוריגמי לבן and דקור לבן ריבועים (no finish). The
    מונה items are image labels only (absent from the text layer) but present on the slide. Model 2839 gives
    `מילניום 7.5/15` `{ f: 'g' }`, so the picker shows "(מבריק)", which the spec does not say. Change: `{ f: 'u' }` or drop
    the opt (group default is `u`). Crop: `studio_crops/d07_p15_millennium_no_finish.png`.
16. **`kitB` (between the kitchen cabinets).** d07 p17 "חיפוי מטבח": 20/20 פלייגראונד מט, 10/30 פסטל and וראנו; p13-p16 are
    also "ומטבחים". Model 3029 cats `k1030, k2020, c3060a, c3060b, c3060c, c2060`; the 25x75 wet-room-only groups are
    rightly excluded. Default וראנו לבן 10x30 glossy (written "מבריק"). Laying: model running bond (`bond: 'r'`, 2844);
    d07 writes none (the CERAMICS.md choice). Matches d07.
17. **`k1030` finishes.** Printed: פסטל לבן מבריק, פסטל שחור מבריק, פסטל אפור מט, פסטל איבורי מט, פסטל לבן מט, וראנו
    לבן / טורקיז / גרפיט מבריק, וראנו טאופה with no finish. Model 2846 gives `וראנו טאופה` `{ f: 'g' }`. Change to
    `{ f: 'u' }`. Crop: `studio_crops/d07_p17_kitchen_10x30_finishes.png`.
18. **Colours of existing products.** Pages are pixel-identical to the edition the hexes came from; spot checks (פלזה אפור,
    מרפיל אפור, דולמיט אפור) equal the slide medians. No change.
19. **Slip ratings.** d07 p8 R10, p9 R10/R11. Model: finish `r` roughness .7-.9 (2850). R ratings are a surface property
    the eye cannot judge; the high roughness is a fair stand-in. Matches.
20. **Cladding heights.** d07 writes none. d10 item 2: bath walls "עד גובה תקרה או עד תחתית הנמכה" (replacing d08's
    "כ 2.1 מ'"). Model: master bath tiles 0 to `H` 2.60 (1419-1423, no lowered ceiling there); family bath 0 to `H`
    behind a ceiling at `BC` 2.10 (1461-1465, 1497), so visible tile reaches the lowered ceiling. Matches d10.

## D. Sanitaryware and taps (d07 p19-p30)

21. **Guest WC basins, p19** (ארט 33/29, E.V.O 45/20, נפטון 48/25). No guest WC in the plan or the model. Not applicable.
22. **`CER_FIXTURES` page numbers** (3035-3042): 23 to 24 (Omega black, three places), 21 to 22 (accessories, two
    places), 20 to 21 (bath), 19 to 20 (WC), 25 to 26 (kitchen sink), 26 to 27 (kitchen tap), 28 to 29 (Studio cabinet).
23. **Basin taps.** `CER_FIXTURES` 3035: "סדרת אומגה שחור, פרח פיה קצרה". p24 shows it as a deck-mounted single-lever
    mixer; the spec has no wall-mounted basin tap at all (p23-p25). Model: black wall spouts, master 1451
    (`B(4.44, 4.56, -3.77, -3.75, 1.02, 1.04)`), family 1543 (`B(2.01, 2.2, -2.125, -2.105, 1.00, 1.02)`). Colour black
    matches. Change: replace each with a deck mixer on the vanity top behind the basin, about 16 cm tall with a 12 cm spout
    and a side lever (sizes estimate), in `mat.blackMetal`. Crop: `studio_crops/d07_p24_omega_black.png`.
24. **Bath tap.** `CER_FIXTURES` 3036: "סוללה (עמ׳ 23), עם מוט אומגה שחור". On p24 "סוללה" is an exposed wall bar mixer
    with spout and a rail. Model 1521-1523: a 10x10 cm plate with a knob at h .85 ("4-way mixer", from the plumbing plan),
    a filler through the overflow (1522), rail and hand shower from 1.50. That is the p24 "4 דרך" option plus p21
    "אביק אוטומטי פיית מילוי". Conflict between `CER_FIXTURES` text and the model/plumbing plan. Proposed text, if the
    owner keeps the plan: "סדרת אומגה שחור, 4 דרך (עמ׳ 24), עם אביק אוטומטי פיית מילוי (עמ׳ 21) ומוט אומגה שחור
    (עמ׳ 22)". Shape: Omega 4-way is a round plate with two handles; model plate is square (1521). Optional: round plate
    about 16 cm (estimate).
25. **Master shower.** `CER_FIXTURES` 3037: Omega black 3-way, head, arm, rod. Model 1436-1438: wall arm with a 30 cm
    disc head at 2.10, rail with hand shower, mixer as a 3.4 x 8 x 10 cm box (1438). Colour and parts match. Omega
    3-way is a round plate with one lever (p24); optional round plate. Head size not written (estimate).
    Family bath rain head hangs from the lowered ceiling on a pipe (1524); d07 offers only wall arms ("זרוע", p22).
    Minor, note only.
26. **Flush plates.** d07 p20: Geberit concealed cistern, plate "כרום / מוברש / לבן", "עגול / מרובע". No black.
    `CER_FIXTURES` 3039 picks "לחצן לבן מרובע". Model draws black plates: master 1442, family 1530 (`mat.blackMetal`,
    20 x 12 cm). Change: white, for example `M('#f1f1ef', .3)`, two square buttons drawn as a slightly raised inner
    pair (optional). Plate size is not written in d07; real Geberit plates are about 25 x 16 cm (estimate, product
    knowledge, not the document). Crop: `studio_crops/d07_p20_flush_plates.png`.
27. **WC bowls.** d07 p20: wall-hung, white, matching seat (נובה, מטרופול, אפולו, בסטיה גבריט, מטרופוליס). Model: wall-hung
    white bowls on concealed-cistern ledges (1441, 1529). Matches.
28. **Kitchen sink.** d07 p26 "כיור מטבח בודד": נירוסטה כרתה, סיליקוורץ, נירוסטה. `CER_FIXTURES` 3040 picks "נירוסטה";
    on the slide that one is an inset sink with a wide flat rim. Model 1306-1309: undermount single bowl 70x45 under the
    quartz. The "נירוסטה כרתה" photo looks like an undermount bowl (my reading of the photo; the slide writes no
    mounting). Conflict between the text and the model. Either change the text to "נירוסטה כרתה (עמ׳ 26)" or draw an
    inset rim. Bowl size not written.
29. **Bath cabinets.** d07 p28-p30 header: "מקלחת כללית מידות: 60, 80 ס"מ | מקלחת הורים מידות: 100, 120 ס"מ". Internal
    conflict in d07: no listed model comes in 120 (largest 100). All shown are wall-hung with a white integrated top
    basin. d10 item 3: "ארון אמבטיה קומפלט (משטח חרס כולל כיור), מידה עפ"י תכנית חברה". Model: family bath 100 cm
    standing shaker on a plinth with a quartz top and a semi-recessed basin (1536-1542); master 70 cm floating walnut
    with a travertine top and a vessel basin (1448-1450). Both sizes are outside d07's range for their room (already in
    PROJECT_MEMORY), and both tops differ from "משטח חרס כולל כיור". Conflict between d07, d10 and the plan the model
    follows. Not resolved. `CER_FIXTURES` 3042 text stays a question. Crop: `studio_crops/d07_p29_cabinet_sizes_header.png`.
30. **Bathtub.** d07 p21: acrylic, rectangular or rounded, "160x70 / 170x70", white, "כולל קונסטרוקציה". Model 1514-1519:
    160x70 rectangular, tiled apron. Matches. Kitchen tap: d07 p27 אומגה in black, nickel, brushed or gold, a gooseneck
    pull-down with a side lever; model 1315-1318 black gooseneck with side lever. Matches.

## E. Cross-document items that touch the picker (other reports own the details)

31. **Kitchen splash material and height.** d10 item 1 replaces the kitchen line with "חיפוי שיש בגובה כ 50 ס"מ מעל משטח
    ארון תחתון בלבד, למעט אזור חלון". d08 annex B: tiles "כ 10/30 ו/או כ 20/50" at "כ 50 ס"מ". d07 p17 offers tiles.
    Model: `kitB` default וראנו לבן tile; its "cur" option is a quartz slab like the counter (3029-3030); splash from .92 to
    1.62, 70 cm, filling up to the wall cabinets (1344). Conflicts: tile (d07, d08) vs stone (d10); 70 cm (model) vs about
    50 cm (d08, d10). Not resolved; the stone "cur" option may be the contract one.
32. **Skirting.** d08 annex B: skirting "מחומר הריצוף", "33x7 ו/או 60x7". Model: white 8 cm skirting `#e4e2dc` (951) that
    ignores the floor choice. Conflict with d08 (not with d07). Possible change: when `floor` or `rooms` holds a spec
    tile, tint the skirting with the tile's hex and use 7 cm.

## F. Items in d07 that cannot be shown in the 3D model

- p1 cover render and p2 studio introduction; divider photos p7, p10, p18, p31; lifestyle photos on most slides.
- The note on every slide that the studio may drop or add models with notice.
- "גרניט פורצלן" as a body material; R10/R11 slip classes as numbers.
- "כולל קונסטרוקציה" (tub frame), "מושב אסלה תואם", "מיכל הדחה סמוי גיבריט" (hidden in the wall).
- Alternatives not chosen: nickel series פרו, זן, רובי (p23), Omega nickel and brushed (p24), Grohe LOOP, BEUCURV, FLOW
  (p25), kitchen taps מודו, זן, פרו, טקסס, יערה (p27), accessories נובה, נפולי, רומא, סט מילנו, נקודת מים, ברז מים קרים (p22),
  other cabinet models and colours (p28-p30).

## G. Crops (spec slides only, no personal data)

`audit/recheck5/studio_crops/`: `d07_p5_glossy_80x80.png`, `d07_p15_millennium_no_finish.png`,
`d07_p17_kitchen_10x30_finishes.png`, `d07_p20_flush_plates.png`, `d07_p24_omega_black.png`,
`d07_p29_cabinet_sizes_header.png`.
