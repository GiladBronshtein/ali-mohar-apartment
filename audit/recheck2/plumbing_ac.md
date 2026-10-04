# Plumbing and AC sheets vs model (recheck2, 2026-10-04)

Sources: `materials/plans/originals/plumbing_IMG_8066.jpg`, `ac_IMG_8067.jpg` (HADA 1:75 on A3, 5712x4284, photographed at
an angle). Cross-checks: sales plan `sales_plan_colour_IMG_8061`, electrical `electrical_IMG_8065`.
Model: `source/salon.html` working tree as of this audit (it was being edited by other agents during the audit; line numbers are from the final read). Read-only: nothing in the model was changed. Proof crops: `pl_crops/` (grid
labels are full-resolution sheet pixels).

Value types: **W** written on the sheet (number or label), **S** scaled from the drawing (estimate, good to about 5 to
10 cm). Tolerance: W within 1 cm OK, S within 10 cm OK. Effective model positions include `withShift` offsets.
Ceiling H = 2.60 is an estimate (not on any plan).

## Calibration (local, per room, two drawn faces each)

The photos have perspective, so one global scale is off by up to 10 cm; every position below uses the nearest pair.
Black wall faces are used, not the thin finish lines (6 to 11 px inside).

| Sheet / area | Axis | Faces used (px = model) | px/cm |
|---|---|---|---|
| PL niche | x | 2157 = 2.15, 2649 = 4.37 | 2.216 |
| PL niche | z | 616 = -5.11 (solid facade), 861 = -3.99 | 2.19 |
| PL mamad | x | 895 = -3.80, 1670 = -0.25 | 2.183 |
| PL corridor | x | 2370 = 2.97, 2630 = 4.15 | 2.20 |
| PL balcony | x / z | 3447 = FO 7.70 / 1767 = 0.34, 3630 = 8.71 | 2.19 to 2.21 / 2.226 |
| AC corridor | x | 1178 = -2.12 (west end), 2542 = 4.15 (master door wall) | 2.175 |
| AC corridor | z | 1300 = -1.245, 1548 = -0.145; check 2206 = 2.775 (mamad south) | 2.255 |
| AC mamad | x / z | 816 = -3.80, 1568 = -0.25 / 1600 = 0.125, 2200 = 2.775 | 2.118 / 2.264 |
| AC living strip | x | 1616 = 0, 2545 = 4.15, 3222 = 7.28 (facade pier, outer line 3305 = 7.66) | 2.24 / 2.16 |
| AC niche | x / z | 2115 = 2.15, 2594 = 4.37 / 512 to 524 = -5.11, 752 to 759 = -3.99 | 2.158 / 2.10 to 2.14 |

Note: some faint mirrored text on the AC photo (H=2.63, 4" air inlet) is show-through of the plumbing notes from the back
of the sheet. The drop note "h=35cm(netto)" is bold, in its own box, and is not show-through.

## Corridor and living (AC)

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| Drop net height | W "הנמכה נדרשת h=35cm (netto)" (`z_ac_drop_box_raw`, `z_ac_drop_h35_*`); leaders to corridor and living strip | `DROP = H - .25` (L878), comments L877, L1106, info text L177 "25 ס״מ" | -10 | **FIX** |
| Ducts | W Ø10" main, Ø8" branches (corridor), Ø10" along the living strip | hidden | | OK (a 10" duct needs the 35) |
| Drop extent x | S -2.12 .. 4.15 (dotted area) | -2.12 .. 4.15 (L880) | 0 | OK |
| Return grille size | W ת.א.ח 80x60 | 80 x 60 | 0 | OK |
| Return grille position | S x 1.84..2.65, z -1.14..-0.55 (centre 2.25, -0.84); north edge about 10 cm off the corridor north face | x 1.80..2.60, z -1.00..-0.40 (L884-885) | x +4, z -14 | FIX (S, low) |
| Living grilles size | W מ.א.ק 90X15 (two) | 90 x 15 | 0 | OK |
| Living grille west centre | S 2.23 (rectangle px 2015..2215) | 2.20 (L1109) | +3 | OK |
| Living grille east centre | S 5.80 to 5.86 (rectangle px 2810..3020; depends on the east anchor) | 5.75 | +5 to +11 | OK (S, edge) |
| Living bulkhead depth | S 0.73 (strip south line px 1752, living face 1585) | 0.80 (L1108, also L1163) | -7 | OPEN (S, not written) |
| Room grilles | W "תריס משולב 80x20 עם להבי הטיה פנימיים, פתח בקיר 85x25" | 80 x 20 (L888) | 0 | OK |
| Room 1 grille centre | S -1.67 (over door -2.06..-1.23) | -1.65 | -2 | OK |
| Room 2 grille centre | S 1.25; door on the same sheet scales 0.88..1.72, so grille sits 5 cm west of door centre | 1.32 (door 0.93..1.77) | 3 cm relative | OK |
| Passage opening | S x 1.75..2.97 (AC) and 1.79..2.97 (PL), about 120 wide | 1.99..2.97 (98), wall `W(-0.25, 1.99, ...)` L876 | 20 to 24 | OPEN (geometry, check sales plan) |
| Red X boxes over door openings | on both sheets at room 2, family bath, master, passage | | | not an AC item (opening marking) |
| "S" box | S about (4.4, 0.1), living side of the master door corner | none | | OPEN (unidentified) |
| Corridor AC condensate cleanout | W 15 from the corridor north face, z -1.095; S x 4.20 (in the master door wall, drop void) | hidden | | OK |

## Mamad

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| 8" sleeves (2) | W "2* שרוול פלדה Ø8" תקן הג"א o.k.= 10 cm מהתקרה, מ.א.ק Ø8", ת.א.ח Ø8"" (`z_ac_mamad_all`) | top H-.10 (centre H-.20, r .10), L893 | 0 | OK |
| 8" sleeve x | S -1.52 and -0.94 (AC symbols px 1300 and 1422); PL leaders -1.69 and -1.11 (imprecise) | -1.55, -0.95 | +3, +1 | OK |
| Relief sleeve 4" | W "c.l.= 25 cm" מתקרה, "+שסתום הדף ושחרור לחץ"; S x -0.48 (AC), PL "25" from east face = -0.50 | x -0.52, H-.25 (L897) | +2 to +4 | OK |
| Filter sleeves 4" | W "Rainbow 54R c.l.=150cm מהרצפה, c.l.=30cm מהתקרה, 0.1kw 1ph" | 1.50 and H-.30 | 0 | OK |
| Filter box | S z 2.20..2.60 (AC), 2.20..2.57 (PL); 37 to 40 along the wall, 32 to 33 deep | z 2.085..2.585, 50 x 21 deep (L1720) | centre +5 | position OK, size OPEN |
| "H=2.63" | W on PL next to all three sleeve notes (AC, air inlet 4", relief) | H 2.60 (estimate) | +3 | OPEN |
| Blast door opening | S -2.02..-1.28 (AC), -2.02..-1.26 (PL) | -1.98..-1.19 | 4 to 9 | note for geometry |

H=2.63 cannot be each item's own height (the AC sheet puts them 10 top, 25 c.l. and 30 c.l. under the ceiling). The
consistent reading is a mamad ceiling of 2.63. Interpretation, not a written ceiling height.

## Family bath (kids')

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| AC unit ceiling | W "הנמכה בגובה 50 ס"מ ... פתח גישה 60x60"; hatched area covers the whole bath | `BC = H - .50`, hatch 60x60 | 0 | OK |
| Mini-central | W "INVERTER 52000 Btu/hr, 4.8 kW 3ph למעבה, דירוג C" | unit hidden above BC | | OK |
| WC axis | W 44; L "מיכל הדחה גבוה" | 42 (L1479 `place(2.05, 2.6, -3.405, -3.045, 'e')` in `withShift(.14, -.13)`, effective z -3.355) | -2 | FIX (W, low) |
| Basin axis | W 72 | 72 | 0 | OK |
| Washer | W 35, L water H-110, drain H-65 | 35 | 0 | OK |
| Tub | W 35+35, taps 15/20, L H-85 mixer, rail from H-150 | matches | 0 | OK |
| AC condensate | L "ניקוז מזגן עילי" at the basin | hidden | | OK |
| Riser 2 Ø110 box | S PL: box about 19 x 16 at the NW corner, x 2.01..2.20, z -3.775..-3.61; no SW box. Sales plan: grey box at the SW corner | SW box `B(2.01, 2.20, -1.605, -1.395, 0, H)` L1502 | | OPEN (sheets disagree) |

## Master bath

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| Shower tray | W 106 x 92 | 106 x 92 | 0 | OK |
| Shower drain | W 50 from north face (point) | 50 | 0 | OK; sheet 50+46 does not add up to 92 |
| Mixer | W 50 from north face, L "אינטרפוץ 4 דרך למזלף ומוט H-105" | 50, h 1.05 | 0 | OK |
| Second point | W 35 from north face, L "ראש טוש H-210" | ceiling head | | OPEN (wall arm at z -4.63, h 2.10?) |
| WC axis | W 60; L "מיכל הדחה נמוך" | 60, concealed ledge | 0 | OK; cistern type OPEN |
| Basin axis | W 44; L "ברז פרח H-60, ביוב H-50 לארון תלוי" | 44 | 0 | OK |
| Vanity length | S fills the 72 from shower front to south wall | 68 + 7 cm gap | | note |

## Master bedroom (AC)

| Item | Sheet | Model | Verdict |
|---|---|---|---|
| Split | W "מזגן עילי לתפוקה 12,300 BTU/hr 1.0 kw 1ph הזנה למאייד, דירוג A"; no unit symbol drawn | wall unit x 4.61..4.83, z -2.295..-1.395, h 2.24..2.52 (L1733) | capacity OK; position OPEN |

The only positional hint is the condensate cleanout in the corridor at z -1.095 (W 15), inside the master door wall (x 4.15
to 4.26). That fits a unit on the master face of the door wall (x 4.26) above the door better than one on the x 4.61 wall.
Not drawn; leave unless the owner knows.

## Laundry niche (מסתור)

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| Louvre openness | W "מסתור פתוח 80% נטו למעבר אויר" | slats .07 at .12 pitch, now tilted `.rotation.x = -.6` (L1510); front view about 33% open | | FIX (W) |
| Water heater | S PL centre (4.02, -4.69), AC (4.01, -4.69); Ø about 56 on both | (4.04, -4.80), r .27 | z +11 | FIX (S, two sheets agree) |
| Floor drain 11 "ניקוז מסתור" | S (3.89, -4.335) | (3.85, -4.31) L1507 | 4, 2.5 | OK |
| Condenser | AC outline S x 2.29..3.66, z -5.20..-4.65 (137 x 55), split in three parts; no size written | 89 x 34 at x 2.30..3.19, z -5.25..-4.91 | | OPEN |
| Isolator | W "3x16A IP65", circuit 9; S about (2.54, -4.99), inside the condenser outline | none | | OPEN (electrical) |
| Drain 4 "ניקוז תעלה 4" צ.מ.ג" | S ⊕ at the NW corner about (2.21, -5.0) | none | | ADD (low) |
| Riser 1 "קולטן Ø110" | S leader ends in the solid facade part near x 4.15, z -5.25 | none (inside the wall) | | OPEN (low) |

## Balcony and kitchen (plumbing)

| Item | Sheet | Model | Delta | Verdict |
|---|---|---|---|---|
| Gas point | W 60 from facade outer line = 8.30; L "נקודת גז H-30" | 8.30, h .30 | 0 | OK |
| Garden tap | W +20 = 8.50; L "ברז גן 1/2" H-60" | 8.50, h .60 | 0 | OK |
| Floor drain 1 | S (9.04, 1.60 to 1.66) | (9.05, 1.50) | z +10 to +16 | OPEN (S, low) |
| Floor drain 2 | S (9.05, 7.27 to 7.34) | (9.08, 7.30) | 0 to 4 | OK |
| Downpipes 1, 2, 5, 6, 12, 13 (4") | labels end in walls or facade | none | | not modelled (external) |
| Kitchen | no sink or dishwasher points drawn; riser 3 (Ø110) at the kitchen west face z about 7.49, drain 13 at z about 8.13 (S), in the core shaft | none | | OPEN (low) |

## Proposed changes (not applied), by confidence

High (written):
1. L878: `const DROP = H - .35;` (W h=35cm netto). Update comments L877 and L1106 and the info text on L177 ("הנמכה של 25
   ס״מ" to 35). Effects with H 2.60: corridor, passage and living strip ceiling at 2.25 (door heads 2.10 clear). Items that
   follow DROP and stay consistent: room grilles 2.27..2.47, living grilles 2.30..2.45, storage-wall niches (top 2.14), tall
   kitchen unit (top 2.215). The mamad 8" sleeves (bottom 2.27) and relief sleeve (bottom 2.295) stay above the drop on the
   corridor side. Visual check: TV-wall flute back L1092 shrinks to 2.22..2.25 (3 cm).

Medium:
2. L1510 louvres towards 80% open (W): thinner blades at a closer pitch, e.g. `for (let y = .1; y < H; y += .10) B(2.15, 3.65, -5.30, -5.28, y, y + .02, mat.louver, { cast: false }).rotation.x = -.6;` (about 72% open in front view with the tilt, 80% without it).
3. Water heater z (S, both sheets): L1520, in the `withShift(.22, -.45)` block, change `-4.35` to `-4.24` in the heater body and the
   two pipes: `C(3.82, -4.24, 1.0, 2.25, .27, ...)`, `C(3.82, -4.24, .7, 1.0, .015, ...)`, `C(3.92, -4.24, .7, 1.0, .015, ...)`
   (effective z -4.69).

Low:
4. Family bath WC +2 (W 44 from the north face z -3.775, effective axis z -3.335): L1479 `place(2.05, 2.6, -3.385, -3.025, 'e')`
   and L1480 flush plate `B(2.05, 2.055, -3.305, -3.105, .86, .98, ...)`.
5. Return grille z (S): L884 `B(1.80, 2.60, -1.14, -.54, DROP - .006, DROP, ...)`, L885 slots `z -1.11..-.57`.
6. Niche drain 4 (S): `C(2.21, -5.02, 0, H, .055, mat.steel)` or a boxed riser in the NW corner.

## OPEN

- H=2.63 on all three mamad sleeve notes (PL): most likely the mamad ceiling height. The only ceiling-related height on any
  sheet; the model uses H 2.60 (estimate).
- Riser 2 box: PL NW corner vs sales plan SW corner (model SW). Candidate: `B(2.01, 2.20, -3.775, -3.61, 0, BC, mat.bathWall)`.
- Master split position (not drawn; condensate point suggests above the master door, x 4.26 face).
- Condenser size (52000 BTU/h 3ph; no size written; the AC outline is 137 x 55 scaled).
- Cisterns: PL says high cistern (family) and low cistern (master); model uses concealed ledges in both.
- Mamad filter box: scaled 37 to 40 x 32 to 33, model 50 x 21.
- Passage opening: both MEP sheets scale it at about 1.77..2.97 (120); model 1.99..2.97 (98). Geometry agent to check the
  sales plan.
- Living bulkhead depth: scaled 0.73, model 0.80 (not written).
- Balcony drain 1 z: scaled 1.60 to 1.66 on PL, model 1.50.
- Master shower second point at 35 (H-210): wall-arm head vs model ceiling head.
- Isolator 3x16A IP65 in the niche, riser 1, kitchen riser 3 and drain 13 (hidden or external).
- Master shower tray: written 50 + 46 does not add up to 92.
- Mamad blast door scales 4 to 9 cm west of the model on both sheets (geometry).
- "S" box near the master door corner (living side): unidentified.

## Disagreements with `audit/recheck/plumbing_ac.md`

| Item | recheck | recheck2 | Note |
|---|---|---|---|
| Drop net height | read "h=25cm (netto)", OK | **h=35cm**, FIX | The two digits are a mirrored 3 (Ɛ) and a mirrored 5; mirrored in a crop they read "53=h", i.e. h=35. No 2. The model value 25 came from that misread. |
| Return grille | (2.24, -0.77), OK | (2.25, -0.84), FIX low | z from the corridor north face 1300 and south face 1548 on the same sheet |
| Red X over the master door | "possibly a transfer grille" | opening marking | The same red X appears over door openings on the plumbing sheet too (room 2, bath, master, passage) |
| Balcony drain 1 | proposed z 1.5 (mean of AC 1.38 and PL 1.6) | PL 1.60 to 1.66 | AC not re-measured here; left OPEN |
| Water heater | borderline | FIX medium | both sheets give z -4.69 |
| Louvres 80% | info only | FIX (written) | |
| 8" sleeve height | "o.k.= 10 cm", OK | same, OK | agree (my first read as c.l. was wrong) |
| H=2.63 | mamad ceiling, interpretation | same | agree |
| Condenser | proposed enlarging | OPEN | no size written |
| Passage width | not reported | 120 vs 98 | new |

Items in the old report's summary already applied in the model (verified): living grilles [2.20, 5.75], room grilles 80x20,
mamad sleeves [-1.55, -0.95], relief sleeve, tub 70 with taps on the corridor wall, basin 72 and 44, balcony drains near
x 9.05, garden tap h .60, point drain in the ensuite, niche floor drain.

## Crops

PL: `z_pl_niche*`, `g_pl_north`, `g_pl_corr`, `z_pl_passage`, `g_pl_mamad`, `z_pl_mamad_txt`, `z_pl_mamad_n*`,
`z_pl_mamad_sw`, `z_pl_kit_w`, `z_pl_gas`, `z_pl_bdrain1/2`, `g_pl_fbath2`, `z_pl_fbath`, `z_pl_mbath*`, `z_pl_shower`,
`z_pl_corr_drain`, `z_sales_fbath`, `g_el_fbath`.
AC: `z_ac_drop_box_raw`, `z_ac_drop_h35_raw`, `z_ac_drop_h35_mirrored`, `z_ac_corrW2`, `z_ac_corrE2`, `z_ac_passage`,
`z_ac_living`, `z_ac_mamad_sleeves`, `z_ac_mamad_all`, `z_ac_master`, `z_ac_niche2`, `z_ac_cond`, `g_ac_north`.
