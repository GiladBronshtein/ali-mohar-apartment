# Re-check 3: geometry vs the vector construction plan

Source: `materials/plans/vector/construction.pdf`, HADA "תכנית בינוי", dated 5/5/26 (PDF created 2026-07-15), one A2 sheet.
Model: `source/salon.html` as of 2026-10-04 evening. Line numbers below are from that state; the file is being edited
in parallel, so match on the quoted text, not the number.

Crops: `geo_crops/` (JPG). The overlay `08_overlay_model_on_sheet.jpg` draws the model walls (red) on the sheet.

## 1. Orientation, scale, method

| Item | Finding |
|---|---|
| Orientation | Sheet right = east (+x), sheet down = south (+z). No rotation or mirror. |
| Scale | Exact 1:50 on A2. 600 dpi raster = 4.7244 px/cm. |
| Transform | X_px(600 dpi) = 4290 + 472.44·x, Y_px = 4144 + 472.44·z (x, z in model metres). Checked on 12 wall faces, residual under 1 cm. |
| Exterior wall | Cladding about 10, black core 20, 6 cm thermal insulation inside ("ע"פ דו"ח תרמי פרט 3"). Written room dims run to the insulation face. |
| Partitions | Drawn 10 (most) and 15 (room 1/room 2, room 2/corridor). The model has 18 to 20 (sales plan). |
| UK / OK | Sill / head height from the floor. "+35" after OK = roller-shutter box above the head. |
| Yellow X boxes | Construction openings ("פתח בנייה"). The red note in room 2 ("פתח בנייה 84/24 ס"מ 10 ס"מ מתחת לבטון, ראה פרט A") points at the yellow box over the room 2 door: an 84 x 24 AC duct opening 10 cm below the slab. Yellow sits over every door (rooms 1 and 2, bath, master) and over the corridor-to-living gap. No legend on the sheet; this reading is inferred. |
| Method | Written figures transcribed from 400 to 800 dpi crops; drawn faces measured by dark-run scans on the 600 dpi raster (scaled, about ±1 cm). |

## 2. Written dimensions and notes

Δ = model minus construction, cm. Verdicts: OK (within 2 cm), DIFF (written, model differs), SALES (construction differs
from the sales plan; model follows sales by rule), INFO.

### 2a. Outer chains

| Item | Written | Model | Δ | Verdict |
|---|---|---|---|---|
| East chain (x 11.27), N to S | 310 \| 90 \| 152 \| 54 \| 270 \| 80 \| 270 \| 76 \| 70 \| 45 \| 29 \| 10, from z -5.27 | | | INFO |
| East chain absolute stations | -5.27, -2.17, -1.27, 0.25, 0.79, 3.49, 4.29, 6.99, 7.75, 8.45, 8.90, 9.19, 9.29 | | | INFO |
| Overall east chain | 1337, 879 (x 9.95), 538 (z -5.38..0) | | | INFO |
| Top chain, W to E | 455 \| 90 \| 88 \| 154 \| 233 \| 60 \| 261 = 1341, from x -4.185 | | | INFO |
| West chain, N to S | 246 \| 90 \| 239 \| 100 \| ..., from z -5.27 | | | INFO |
| Apartment label | "דירה 2, 5 חד', 133.1 מ"ר" | header 132 | | INFO (contractor figure 132 kept) |

### 2b. Openings in the outer walls

| Item | Written | Model | Δ | Verdict |
|---|---|---|---|---|
| Living door A, z | 0.79..3.49 (270) | 0.78..3.45 (267) | -1 / -4 | DIFF |
| Living door B, z | 4.29..6.99 (270) | 4.26..6.88 (262) | -3 / -11 | DIFF |
| Kitchen window C, z | 7.75..8.45 (70) | 7.70..8.39 (69) | -5 / -6 | DIFF |
| A, B: UK / OK | 0 / 235+35 | 0 / HEAD 2.30 | head -5 | DIFF |
| C: UK / OK | 120 / 235+35 | 1.00 / 2.30 | sill -20, head -5 | DIFF |
| Master east window, z | -2.17..-1.27 (90) | -2.27..-1.31 (96) | -10 / -4 | DIFF |
| Master east UK / OK | 15 / 235+35 | 0 / 2.20 | sill -15, head -15 | DIFF |
| Room 1 window, z | -2.81..-1.91 (90) | -2.92..-1.93 (99) | -11 / -2 | DIFF |
| Room 1 UK / OK | 15 / 235+35 | 0.95 / 2.20 | sill +80, head -15 | DIFF |
| Room 2 window, x | 0.365..1.265 (90) | 0.27..1.25 (98) | -9.5 / -1.5 | DIFF |
| Room 2 UK / OK | 15 / 235+35 | 0.95 / 2.20 | sill +80, head -15 | DIFF |
| Master bath window, x | 6.015..6.615 (60) | 5.99..6.58 (59) | -2.5 / -3.5 | DIFF (small) |
| Master bath UK / OK | 125 / 235 | 1.50 / 2.20 | sill +25, head -15 | DIFF |
| Mamad window, z | 0.48..1.48 (100) | 0.47..1.44 (97) | -1 / -4 | DIFF |
| Mamad UK / OK | 110 / 210 | 1.00 / 2.00 | sill -10, head -10 | DIFF |
| Mamad outer wall | "30" + "5" | 0.48 incl. finish | | OK (as drawn) |
| Sashes | single inward sash: room 1, room 2 (hinged E), master east (hinged S). Mamad single. A, B two sliders, C one | room 1, room 2, master east drawn as 2 panes | | DIFF (drawn, not written) |

### 2c. Interior

| Item | Written | Model | Δ | Verdict |
|---|---|---|---|---|
| Corridor south wall, W part | "10", x 0..1.80 (chain 180) | 14.5, x -0.25..1.99 | | see 3.1 |
| Corridor-to-living gap | "120", x 1.80..3.00, yellow box | passage 1.99..2.97 (98) | -22 | DIFF, see 3.1 |
| Corridor south wall, E part | "20", x 3.00..4.18 (chain 118) | 19, x 2.97..4.15 | -3 | OK |
| Column at TV wall | black, x 4.18..4.78, z -0.20..0 (chain 50 + 10) | step 4.26..4.76, z -0.24..-0.145 | +8 / -2; face 4 cm proud | INFO |
| TV wall E of column | drawn 10 | 14.5 | +4.5 | SALES |
| South chain under corridor | 15 \| 80 \| 118 \| 180 \| 120 \| 118 \| 50 \| 261 \| 158 \| 6 \| 120 | | | INFO |
| Mamad blast door opening | 80, x -1.98..-1.18; "2+200" | -1.98..-1.19, head 2.00 | 0 / -1 | OK |
| Mamad blast door leaf | drawn about 70 (hinge x -1.91) | leaf 0.86 | +16 | OPEN |
| Mamad north wall | black z -0.095..+0.10 | -0.145..0.125 | | SALES |
| Corridor width | 115 (W part), 105 (E of x 3.00) | 110 | | SALES |
| Room 1 / room 2 partition | "15", x -1.133..-0.98 | -1.15..-0.97 (18) | | SALES |
| Room 2 / corridor wall | "15", z -1.405..-1.255 | -1.45..-1.245 (20.5) | | SALES |
| Room 1 / corridor wall | 10, z -1.35..-1.25 | -1.425..-1.245 | | SALES |
| Room 2 door | 82 rough, x about 0.94..1.79 | 0.93..1.77 | | OK |
| Master door | 12 \| 82 \| 12, z -1.17..-0.34, 210 | -1.16..-0.34, 2.10 | | OK |
| Master bath door | 75 / 210, z about -4.06..-3.36 | -4.06..-3.36 (70), 2.10 | | OK (75 = rough) |
| Closet opening | 10 \| 55 \| 80 \| 60 \| 6, x 7.57..8.37 | 7.54..8.32 | -3 / -5 | OK (scaled within 5) |
| Bath to laundry niche window | 23 \| 120 \| 83, x 2.375..3.575 | 2.37..3.55 | 0 / -2.5 | DIFF (small) |
| Same, UK / OK | 110 / 210, two sliding sashes | 1.05 / 2.10, centre mullion | sill -5 | DIFF |
| Family bath tub zone | 80, x 3.72..4.52; stub at z about -3.0 | stub 3.69..4.46 at -3.09..-2.98 | | OK |
| Family bath WC axis | 44 from the north wall | | | OK (plumbing report) |
| Family bath ceiling | "הנמכת תקרה למיזוג אוויר -50" | BC = H - 0.50 | 0 | OK |
| Bath / corridor wall | red "יש לבנות קיר זה בגובה H=-45" | full height | | INFO (hidden above the -50 drop) |
| Electrical panel | grey box x 3.37..3.79, z -0.25..-0.05 | 3.33..3.78 | -4 / -1 | OK |
| Entry door | 105 rough at x 1.58..2.63, "105/210" | net 1.585..2.555 (97) | | OK (net = rough minus frames) |
| Lobby wall face | 5.54 (core 5.60..5.79, "20" + "5") | 5.50 | -4 | DIFF, see 3.10 |
| Kitchen entry stub | drawn x 3.575..4.329, z 5.543..5.643 (10); chain 105 \| 15 \| 105 \| 95 \| 75 \| 297 ends it at 4.33 | 3.63..4.30, z 5.50..5.61 | end -3, face -4 | DIFF |
| Lobby mass west face | 1.43 (143 \| 587) | 1.45 | +2 | OK |
| Laundry niche N edge | "מעקה קל H=105" line at z -5.175..-5.12, 15 from the core | full-height louvres z -5.30..-5.26 | | OPEN (AC plan shows louvres) |
| Laundry niche level | "+2.70" | | | INFO (meaning unclear) |
| Mamad air sleeves | H=2.63; "AC passage 4 cm from the ceiling" | ceiling H 2.60 (estimate) | | see 3.8 |
| Construction opening | "פתח בנייה 84/24 ס"מ 10 ס"מ מתחת לבטון, פרט A" over room doors | | | INFO (AC report) |
| Balcony N band | lines z -0.11, 0.0, 0.10, 0.15, 0.20 for x ≥ 9.33 | BZN -0.13 | | see 3.6 |
| Balcony E band | lines x 10.23, 10.28, 10.33, 10.43, 10.53 | BX2 10.45 | | see 3.6 |
| Balcony depth | "120" from 9.23 to 10.43; "280" from 7.63 to 10.43 | 7.70..10.45 (275) | +2 at E | OK |
| Balcony N wall face (x < 9.33) | 0.35 | BZ1 0.34 | -1 | OK |
| Balcony S wall | z 8.80..9.29 (core 8.90..9.19), ends x 10.13 | BZ2 8.71, BS 10.07 | | SALES (BZ2), OK (BS) |
| Levels | "+3.45" balcony NE edge, "+3.40" lobby | | | see 3.6 |

### 2d. Room interiors (construction written vs model, which equals the sales plan)

| Room | Construction | Model = sales | Δ | Verdict |
|---|---|---|---|---|
| Room 1 (NW) | 279 x 366 | 274 x 361 | -5 / -5 | SALES |
| Room 2 | 287 x 361 | 282 x 356 | -5 / -5 | SALES |
| Mamad | 363 x 270 | 355 x 262 | -8 / -8 | SALES |
| Family bath | 253 x 246 | 245 x 238 | -8 / -8 | SALES |
| Master | 435 x 301 | 430 x 296 | -5 / -5 | SALES |
| Master bath | 230 x 180 ("180" partly overprinted; scaled 179) | 222 x 172 | -8 / -8 | SALES |
| Closet (x) | 195 | 190 | -5 | SALES |
| Corridor | 115 / 105 | 110 | | SALES |
| Living (x) | 730 | 728 | -2 | SALES |
| Living, TV wall to entry wall | 554 | 550 | -4 | DIFF (no roomdims probe on this) |
| Living + kitchen (z) | 554 + 330 = 884 | 879 | -5 | SALES |
| Kitchen (x) | 367 | 365 | -2 | SALES |
| Dining (z) | 282 (287 at x 1.90) | 277 | -5 | SALES |

## 3. Open items

| # | Item | Resolution | Basis | Confidence |
|---|---|---|---|---|
| 3.1 | Passage width | 120, x 1.80..3.00. The corridor south wall is "10" from 0 to 1.80, then the yellow construction-opening box "120", then "20" block from 3.00 to 4.18. It is the only link from the corridor to the living. MEP sheets scaled about 120 (recheck2). Sales plan gives 100 (1.982..2.983). | written | medium (no legend for yellow) |
| 3.2 | Column 1 (laundry niche) | No boxed column drawn in the niche or at its corners. Only the light railing line and the louvre/AC notes. | drawn | medium |
| 3.3 | Column 2 (family bath SW) | No box at the SW corner; a vanity is drawn there. A pipe symbol (⊕) sits at the NW corner (x 2.10, z -3.71), not boxed. The model box `B(2.01, 2.20, -1.605, -1.395)` has no support on this sheet. Hand to the plumbing report. | drawn | medium |
| 3.4 | Electrical panel x | 3.37..3.79 vs model 3.33..3.78. Keep. | scaled | high |
| 3.5 | Mamad blast door | Opening 80 at -1.98..-1.18 confirmed, "2+200". Leaf drawn about 70 vs model 0.86. Leaf width not written; leave OPEN. | drawn | low |
| 3.6 | Balcony edges and upstand | A 30 cm band on the north (z -0.11..0.20) and east (x 10.23..10.53) edges, no height written. Levels "+3.45" at the edge vs "+3.40" in the lobby suggest a top only about 5 cm above the floor, not the model's 0.45 upstand (estimate). OPEN; do not change without the section. | drawn + levels | low |
| 3.7 | Room 1 2.2 cm shift | Room 1 north insulation face is drawn at -5.01, the same as room 2; model -5.035. Direction confirmed. Fixing it breaks roomdims room A (361 -> 359), so report only. | scaled | medium |
| 3.8 | H= notes | Bath "-50" drop: OK. Bath/corridor wall "H=-45": hidden, no change. Laundry railing "H=105": open vs louvres. Mamad sleeves "H=2.63" with "4 cm from the ceiling", and every head at 235 plus a 35 shutter box (= 2.70), both imply a slab at 2.70 or more. The model ceiling H = 2.60 is an estimate. Ceiling height is still not written; flag only. | written cues | medium |
| 3.9 | Sashes | Room 1 and room 2: one inward sash each (room 2 hinged east). Master east: one sash hinged south. Mamad: one. Window C: one. A and B: two sliders. | drawn | medium |
| 3.10 | Kitchen entry wall | Stub end at x 4.33 (chain ends "75"). Face at z 5.54, 10 thick, same face as the lobby wall (5.54). Model 5.50 with 4.30. The 554 figure is not a roomdims probe, so moving the whole z 5.50 line to 5.54 is possible but touches many lines. | written | high (4.33), medium (5.54) |
| 3.11 | Kids' (family) bath pipe box | See 3.3: nothing boxed at SW; pipe at NW. | drawn | medium |
| 3.12 | Master east window | -2.17..-1.27, 90 wide, sill 15, head 235. Concrete reveal -2.26..-1.20. The model's -2.27..-1.31 matched the reveal, not the frame. | written | high |

## 4. Construction plan vs sales plan

| Point | Construction (5/5/26, newer) | Sales (2025-07-01) | Model |
|---|---|---|---|
| Room interiors | +5 to +8 cm on both axes in every room (to the insulation face; 10 to 15 cm partitions) | values in 2d | sales (roomdims +0) |
| Partitions | 10 or 15 | about 18 to 20 | sales |
| TV wall | 10 thick E of the column | 14.5 | sales |
| Passage | 120 | 100 | 98 |
| Living length | 884 | 879 | 879 |
| Living facade openings | 270, 270, 70 | narrower | sales-derived |
| Sills / heads | written UK/OK everywhere | not given | estimates |

The construction plan is the newer document. Rule applied: written opening sizes, heights and positions are proposed;
room sizes stay on the sales plan so `roomdims.py` stays +0.

## 5. Proposed changes

All in `source/salon.html`. After any of P1 to P4: `python3 roomdims.py` (no probe touches these), `python3 clearance_audit.py`.

| # | Line | Current | Replacement | Basis | Conf. |
|---|---|---|---|---|---|
| P1 | 244 | `HEAD = 2.30` | `HEAD = 2.35` (used only by the living facade, L871, L1024, L1058, L1773, L2061-2062) | written OK=235 at A, B, C | high |
| P2a | 871 | `[[-.13, .78, 0, FT], [.78, 3.45, HEAD, FT], [3.45, 4.26, 0, FT], [4.26, 6.88, HEAD, FT], [6.88, 7.70, 0, FT], [7.70, 8.39, 0, 1.0], [7.70, 8.39, HEAD, FT], [8.39, 9.11, 0, FT]]` | `[[-.13, .79, 0, FT], [.79, 3.49, HEAD, FT], [3.49, 4.29, 0, FT], [4.29, 6.99, HEAD, FT], [6.99, 7.75, 0, FT], [7.75, 8.45, 0, 1.20], [7.75, 8.45, HEAD, FT], [8.45, 9.11, 0, FT]]` | written chain 270 / 80 / 270 / 76 / 70, UK=120 | high |
| P2b | 920 | `[[-.13, .78], [3.45, 4.26], [6.88, 7.70], [8.39, 9.11]]` | `[[-.13, .79], [3.49, 4.29], [6.99, 7.75], [8.45, 9.11]]` | as P2a | high |
| P2c | 1024 | `slider(.78, 3.45, 0, HEAD, 2); slider(4.26, 6.88, 0, HEAD, 2); slider(7.70, 8.39, 1.0, HEAD, 1);` | `slider(.79, 3.49, 0, HEAD, 2); slider(4.29, 6.99, 0, HEAD, 2); slider(7.75, 8.45, 1.20, HEAD, 1);` | as P2a | high |
| P2d | 1057 | `z1 = 7.715, z2 = 8.375, top = 2.20, bot = 1.045` | `z1 = 7.765, z2 = 8.435, top = 2.25, bot = 1.245` (keeps the 1.5 cm inset, 9.5 cm cassette, sill + 4.5) | as P2a | high |
| P2e | 1773 | `shutterZ(.78, 3.45, ...); shutterZ(4.26, 6.88, ...); shutterZ(7.70, 8.39, FO - .08, 1.0, HEAD);` | `shutterZ(.79, 3.49, ...); shutterZ(4.29, 6.99, ...); shutterZ(7.75, 8.45, FO - .08, 1.20, HEAD);` | as P2a | high |
| P2f | 2061-2062 | `winLight(FX - .02, 2.115, 2.67, ... 2.115, 5)`; `winLight(FX - .02, 5.57, 2.62, ... 5.57, 5)` | centre `2.14`, width `2.70`; centre `5.64`, width `2.70` (both centre arguments) | as P2a | high |
| P3a | 861 | `W(-4.28, -3.89, -5.035, -2.92); W(-4.28, -3.89, -2.92, -1.93, 0, .95); W(-4.28, -3.89, -2.92, -1.93, 2.20); W(-4.28, -3.89, -1.93, -1.425);` | `W(-4.28, -3.89, -5.035, -2.81); W(-4.28, -3.89, -2.81, -1.91, 0, .15); W(-4.28, -3.89, -2.81, -1.91, 2.35); W(-4.28, -3.89, -1.91, -1.425);` | written 246 \| 90, UK 15, OK 235 | high |
| P3b | 1561 | `windowZ(-2.92, -1.93, -3.90, -4.28, .95, 2.20, 2);` | `windowZ(-2.81, -1.91, -3.90, -4.28, .15, 2.35, 1);` | as P3a; 1 sash drawn | high (pos), medium (sash) |
| P3c | 858 | `W(-1.14, 0.27, -5.39, -5.01); W(0.27, 1.25, -5.39, -5.01, 0, .95); W(0.27, 1.25, -5.39, -5.01, 2.20); W(1.25, 2.15, -5.39, -5.01);` | `W(-1.14, 0.365, -5.39, -5.01); W(0.365, 1.265, -5.39, -5.01, 0, .15); W(0.365, 1.265, -5.39, -5.01, 2.35); W(1.265, 2.15, -5.39, -5.01);` | written 455 \| 90, UK 15, OK 235 | high |
| P3d | 1582 | `windowX(.27, 1.25, -5.01, -5.39, .95, 2.20);` | `windowX(.365, 1.265, -5.01, -5.39, .15, 2.35);` and, for the single sash, add `panes = 2` to `windowX` (L810) and skip the centre mullion when `panes === 1`, called with `1` | as P3c | high (pos), low-medium (sash) |
| P3e | 875 | `W(8.91, 9.30, -5.01, -2.27); W(8.91, 9.30, -2.27, -1.31, 2.20); W(8.91, 9.30, -1.31, -0.13);` | `W(8.91, 9.30, -5.01, -2.17); W(8.91, 9.30, -2.17, -1.27, 0, .15); W(8.91, 9.30, -2.17, -1.27, 2.35); W(8.91, 9.30, -1.27, -0.13);` | written 310 \| 90, UK 15, OK 235 | high |
| P3f | 1372 | `windowZ(-2.27, -1.31, 8.92, 9.30, 0, 2.20, 2);` | `windowZ(-2.17, -1.27, 8.92, 9.30, .15, 2.35, 1);` (comment "floor-length" no longer true) | as P3e | high (pos), medium (sash) |
| P3g | 859 | `W(4.63, 5.99, ...); W(5.99, 6.58, -5.39, -4.98, 0, 1.50); W(5.99, 6.58, -5.39, -4.98, 2.20); W(6.58, 6.85, ...)` | `W(4.63, 6.015, ...); W(6.015, 6.615, -5.39, -4.98, 0, 1.25); W(6.015, 6.615, -5.39, -4.98, 2.35); W(6.615, 6.85, ...)` | written 233 \| 60, UK 125, OK 235 | high |
| P3h | 1392 | `windowX(5.99, 6.58, -5.01, -5.39, 1.5, 2.2);` | `windowX(6.015, 6.615, -5.01, -5.39, 1.25, 2.35);` | as P3g | high |
| P3i | 862 | `W(-4.28, -3.80, 0.125, 0.47); W(-4.28, -3.80, 0.47, 1.44, 0, 1.0); W(-4.28, -3.80, 0.47, 1.44, 2.0); W(-4.28, -3.80, 1.44, 2.78);` | `W(-4.28, -3.80, 0.125, 0.48); W(-4.28, -3.80, 0.48, 1.48, 0, 1.10); W(-4.28, -3.80, 0.48, 1.48, 2.10); W(-4.28, -3.80, 1.48, 2.78);` | written 100, UK 110, OK 210 | high |
| P3j | 1636 | `windowZ(.47, 1.44, -3.83, -4.28, 1.0, 2.0, 1);` | `windowZ(.48, 1.48, -3.83, -4.28, 1.10, 2.10, 1);` | as P3i | high |
| P3k | 883 | `W(2.01, 2.37, ...); W(2.37, 3.55, -3.99, -3.775, 0, 1.05); W(2.37, 3.55, -3.99, -3.775, 2.10); W(3.55, 4.46, ...)` | `W(2.01, 2.375, ...); W(2.375, 3.575, -3.99, -3.775, 0, 1.10); W(2.375, 3.575, -3.99, -3.775, 2.10); W(3.575, 4.46, ...)` | written 23 \| 120 \| 83, UK 110 | high |
| P3l | 1434 | `windowX(2.37, 3.55, -3.80, -3.99, 1.05, 2.10);` | `windowX(2.375, 3.575, -3.80, -3.99, 1.10, 2.10);` | as P3k | high |
| P4a | 892 | `W(-0.25, 1.99, -0.145, 0);   // ... (passage 1.99-2.97)` | `W(-0.25, 1.80, -0.145, 0);   // ... (passage 1.80-3.00)` | written 180 \| 120 \| 118 | medium |
| P4b | 876 | `W(2.97, 4.15, -0.19, 0);` (and the L874 comment "x 2.97..4.15") | `W(3.00, 4.15, -0.19, 0);` | as P4a | medium |
| P4c | 898 | `B(1.99, 2.97, -.145, 0.0, DROP, H, ...)` | `B(1.80, 3.00, -.145, 0.0, DROP, H, ...)` | as P4a | medium |
| P4d | 1075 | comment "starts 8 cm past the corridor passage at 2.97" | "5 cm past the passage at 3.00" (MX1 3.05 unchanged) | as P4a | medium |
| P5 | 868 | `W(3.63, 4.30, 5.50, 5.61);` | `W(3.63, 4.33, 5.50, 5.61);` | written chain ends "75" at 4.33 | high |

Notes on the proposals:
- P2 and kitchen: window C sill 1.20 and door B to 6.99 sit next to the kitchen run; check against `kitchen.md` and run `clearance_audit.py` (door B now reaches z 6.99).
- P3 and P1: heads at 2.35 leave 25 cm to the estimated ceiling 2.60; the drawn 35 cm shutter box would not fit (see 3.8).
- P4: check the electrical report for switches beside the passage jambs.
- Report only, not proposed: room 1 north to -5.01 (breaks roomdims), all room interiors in 2d, TV wall 10 thick, column face -0.20 vs -0.24, the z 5.50 line to 5.54 (optional; no probe, but many dependents), blast door leaf, balcony band and upstand, laundry railing vs louvres, ceiling height.

## 6. Confirmed OK

- Orientation and the 1:50 scale; facade inner face 7.30 vs FX 7.28, outer 7.73 vs FO 7.70.
- Electrical panel x 3.37..3.79 (model 3.33..3.78).
- Mamad blast door opening -1.98..-1.18.
- Entry door position (rough 1.58..2.63 vs net 1.585..2.555).
- Room 2 door, master door, master bath door, closet opening (within 5 cm).
- Kitchen west face 3.63; lobby mass face 1.43 vs 1.45.
- Corridor wall E part 20 thick at 3.00..4.18; column at 4.18..4.78 (model step within 8 cm).
- Family bath -50 ceiling drop, WC 44, tub stub.
- Balcony north wall face 0.35, east extent 10.43, south wall end 10.13.
- Outer wall faces on the north and west: within 2 cm except room 1 north (3.7).
