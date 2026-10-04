# Realism pass 5: staged CC0 assets

Staging folder (not committed): `source/out/real5/assets/` (paths below are relative to it).
Every item is CC0 1.0 (public domain): Poly Haven (https://polyhaven.com/license) or ambientCG
(https://docs.ambientcg.com/license/). Nothing CC-BY, nothing with an unclear licence.

Total staged: about 15.4 MB (models 5.5 MB, textures 5.4 MB, HDRIs 4.5 MB). With one HDRI instead of three, about
12.3 MB. Sizes are per item so the integrator can pick.

Already in the repo `assets/` and not duplicated here: textures `laminate_floor_02`, `oak_veneer_01`, `white_stucco`,
`rough_linen`, `caban`, `asphalt_02`, `grass_ground`, `park_dirt`; models `potted_plant_01/02`; tree cards
`jacaranda_tree`, `tree_small_02`, `island_tree_02`.

## How the models were made

- Source: Poly Haven glTF 1k. Converted with
  `npx @gltf-transform/cli@4 optimize <in> <out> --compress meshopt --texture-compress webp --texture-size 512|1024 --palette false --instance false`,
  plus `--simplify-ratio 0.5 --simplify-error 0.002` on the heavy ones (0.3 on the banana bunch). Load with
  GLTFLoader plus MeshoptDecoder, as the existing potted plants are loaded.
- Scale and axes: all are Y-up, in metres, real-world size (checked against the bounds below). Origin sits on the floor
  and at the x/z centre unless noted. Multi-variant Poly Haven files were split into one GLB per variant
  (`_tools/split.mjs`) and re-centred at x/z = 0.
- Materials are kept separate and named (palette off), so colours can be re-tinted in code.
- Exceptions: `lemon` origin is at its centre (lift by 0.052 m). `hanging_picture_frame_01` origin is at the centre of
  the frame (y runs -0.42 to +0.42), back face at z = 0, front towards +z. `modern_ceiling_lamp_01` spans y 0.221 to
  1.173 with the canopy at the top: set y = ceiling height - 1.173.
- Picture-frame glass: the Poly Haven files use the opaque frame colour map on a BLEND glass, which three.js draws as a
  black sheet. `_tools/fixglass.mjs` turns it into a clear untextured pane (applied to both frames).
- Triangles are counted after optimisation.

## Props (kitchen, dining, shelves)

| id | what it is | source | licence | tris | staged path | KB | use for |
|---|---|---|---|---|---|---|---|
| food_apple_01 | red apple, 10 cm | https://polyhaven.com/a/food_apple_01 | CC0 | 3,506 | models/food_apple_01.glb | 80 | fruit bowl on the island or the dining table |
| lemon | lemon, 9.5 cm (origin at the centre) | https://polyhaven.com/a/lemon | CC0 | 2,006 | models/lemon.glb | 108 | fruit bowl, beside the cutting board |
| food_lime_01 | lime, 7.5 cm | https://polyhaven.com/a/food_lime_01 | CC0 | 5,110 | models/food_lime_01.glb | 100 | fruit bowl |
| food_pomegranate_01 | pomegranate, 11.5 cm | https://polyhaven.com/a/food_pomegranate_01 | CC0 | 4,070 | models/food_pomegranate_01.glb | 96 | fruit bowl (local touch) |
| food_avocado_01 | avocado, 14 cm | https://polyhaven.com/a/food_avocado_01 | CC0 | 5,444 | models/food_avocado_01.glb | 100 | kitchen counter |
| bananas_bunch | banana bunch, 22 cm (split from `bananas`) | https://polyhaven.com/a/bananas | CC0 | 7,762 | models/bananas_bunch.glb | 112 | kitchen counter by the fridge |
| carved_wooden_plate | carved wooden bowl or plate, 27 cm | https://polyhaven.com/a/carved_wooden_plate | CC0 | 2,042 | models/carved_wooden_plate.glb | 68 | fruit bowl base on the island, coffee table |
| wooden_cutting_board | end-grain board, 45 x 25 cm | https://polyhaven.com/a/wooden_cutting_board | CC0 | 2,882 | models/wooden_cutting_board.glb | 84 | white quartz counter next to the hob, leaning on the backsplash |
| wine_bottle_bordeaux | red wine bottle, 30 cm (split from `wine_bottles_01`) | https://polyhaven.com/a/wine_bottles_01 | CC0 | 3,268 | models/wine_bottle_bordeaux.glb | 108 | kitchen counter, dining table (glass uses KHR_materials_transmission) |
| wine_bottle_champagne | green champagne bottle, 32 cm | https://polyhaven.com/a/wine_bottles_01 | CC0 | 4,342 | models/wine_bottle_champagne.glb | 100 | sideboard or open shelf |
| ceramic_vase_01 | white glazed bud vase, 40 cm | https://polyhaven.com/a/ceramic_vase_01 | CC0 | 5,148 | models/ceramic_vase_01.glb | 56 | TV unit, dining table centre |
| ceramic_vase_02 | white matte urn vase, 31 cm | https://polyhaven.com/a/ceramic_vase_02 | CC0 | 5,564 | models/ceramic_vase_02.glb | 100 | sideboard, master dresser, or as a pot for the calathea |
| ceramic_vase_04 | white jug vase with handle, 34 cm | https://polyhaven.com/a/ceramic_vase_04 | CC0 | 4,499 | models/ceramic_vase_04.glb | 76 | kitchen open shelf, bedside |
| standing_picture_frame_01 | black desk frame with a B/W photo, 25 cm | https://polyhaven.com/a/standing_picture_frame_01 | CC0 | 1,574 | models/standing_picture_frame_01.glb | 60 | bedside tables, desk in room 2, TV unit |
| hanging_picture_frame_01 | black A1 wall frame, 59 x 84 cm, white mount (grey typographic placeholder print: swap the artwork map) | https://polyhaven.com/a/hanging_picture_frame_01 | CC0 | 2,193 | models/hanging_picture_frame_01.glb | 104 | salon wall above the sofa, corridor, master |
| wicker_basket_01 | shallow woven tray, 38 x 30 x 12 cm | https://polyhaven.com/a/wicker_basket_01 | CC0 | 16,716 | models/wicker_basket_01.glb | 244 | towel or toiletry tray on the bath vanity, coffee table tray (heaviest prop in tris; skip if budget is tight) |
| throw_pillows_01 | two square cushions, 45 cm (orange chevron cloth: retexture with `curly_teddy_natural` or a plain tint) | https://polyhaven.com/a/throw_pillows_01 | CC0 | 3,684 | models/throw_pillows_01.glb | 188 | dark leather sofa, master bed |

## Furniture and lighting

| id | what it is | source | licence | tris | staged path | KB | use for |
|---|---|---|---|---|---|---|---|
| Ottoman_01 | black leather pouf, 89 x 62 x 62 cm | https://polyhaven.com/a/Ottoman_01 | CC0 | 4,010 | models/Ottoman_01.glb | 312 | salon, in front of the dark leather sofa (same leather look) |
| modern_arm_chair_01 | black leather armchair on a light wood frame, 82 x 102 x 99 cm | https://polyhaven.com/a/modern_arm_chair_01 | CC0 | 7,029 | models/modern_arm_chair_01.glb | 308 | salon reading corner, master bedroom corner |
| mid_century_lounge_chair | brown leather swivel lounge chair, 101 x 117 x 119 cm | https://polyhaven.com/a/mid_century_lounge_chair | CC0 | 5,800 | models/mid_century_lounge_chair.glb | 288 | alternative salon accent chair (warmer, larger) |
| dining_chair_02 | tufted dark brown leather dining chair, 43 x 97 x 58 cm | https://polyhaven.com/a/dining_chair_02 | CC0 | 11,005 | models/dining_chair_02.glb | 224 | dining set only if a classic look is wanted; the style is more traditional than the flat |
| modern_ceiling_lamp_01 | opal glass globe pendant on a rod, 43 cm globe, 95 cm drop | https://polyhaven.com/a/modern_ceiling_lamp_01 | CC0 | 5,456 | models/modern_ceiling_lamp_01.glb | 156 | bedroom or entry pendant (pair with a PointLight inside the globe) |
| outdoor_table_chair_set_01 | folding bistro set: square slatted wood table, 2 chairs, black metal frames; footprint 74 x 172 cm with chairs | https://polyhaven.com/a/outdoor_table_chair_set_01 | CC0 | 9,600 | models/outdoor_table_chair_set_01.glb | 404 | balcony, beside the egg chair |

## Plants (no pots unless noted)

| id | what it is | source | licence | tris | staged path | KB | use for |
|---|---|---|---|---|---|---|---|
| pachira_aquatica_01_d | money tree, 1.90 m tall, 1.05 m spread (variant d) | https://polyhaven.com/a/pachira_aquatica_01 | CC0 | 14,052 | models/pachira_aquatica_01_d.glb | 524 | salon corner by the balcony door, in `planter_pot_clay` scaled about 1.6x or a white pot |
| pachira_aquatica_01_c | money tree, 1.15 m (variant c) | https://polyhaven.com/a/pachira_aquatica_01 | CC0 | 10,275 | models/pachira_aquatica_01_c.glb | 496 | balcony corner, master by the window |
| anthurium_botany_01_b | anthurium leaves, 47 cm tall, 76 x 57 cm spread | https://polyhaven.com/a/anthurium_botany_01 | CC0 | 7,772 | models/anthurium_botany_01_b.glb | 212 | in `ceramic_vase_02`, TV unit or sideboard |
| anthurium_botany_01_c | anthurium, 36 cm tall | https://polyhaven.com/a/anthurium_botany_01 | CC0 | 4,536 | models/anthurium_botany_01_c.glb | 192 | dining table, kitchen window sill |
| calathea_orbifolia_01_a | calathea, round striped leaves, 42 cm | https://polyhaven.com/a/calathea_orbifolia_01 | CC0 | 2,951 | models/calathea_orbifolia_01_a.glb | 176 | bath vanity corner (humid-room plant), bedside |
| calathea_orbifolia_01_b | calathea, 30 cm | https://polyhaven.com/a/calathea_orbifolia_01 | CC0 | 1,722 | models/calathea_orbifolia_01_b.glb | 168 | kitchen shelf, desk |
| fern_02_b | fern, 99 x 89 cm spread, 43 cm tall, alpha-tested fronds | https://polyhaven.com/a/fern_02 | CC0 | 2,384 | models/fern_02_b.glb | 148 | balcony planters, hanging pot |
| potted_plant_04 | haworthia succulent in a white ribbed pot, 27 cm (pot included) | https://polyhaven.com/a/potted_plant_04 | CC0 | 5,898 | models/potted_plant_04.glb | 160 | window sills, bath shelf, desk |
| planter_pot_clay | terracotta pot, 27 cm wide, 22 cm tall (pot only) | https://polyhaven.com/a/planter_pot_clay | CC0 | 3,068 | models/planter_pot_clay.glb | 80 | pot for the pachira, fern and calathea; balcony |

## PBR texture sets

WebP, `tex/<id>/{diff,nor,rough}.webp` (some also `opacity`, `metal`). Colour (`diff`) is sRGB; `nor` (OpenGL
convention, green up) and `rough` are linear data, so load them without `SRGBColorSpace`. 1k unless noted.
ambientCG gives no physical size; Poly Haven sizes are given where known.

| id | what it is | source | licence | maps | staged path | KB | use for |
|---|---|---|---|---|---|---|---|
| Marble021 | white marble with faint grey veins | https://ambientcg.com/view?id=Marble021 | CC0 | diff nor rough | tex/Marble021/ | 92 | white quartz countertop and island top |
| Marble012 | grey veined marble | https://ambientcg.com/view?id=Marble012 | CC0 | diff nor rough | tex/Marble012/ | 280 | TV wall slab or backsplash option |
| Concrete034 | smooth light grey concrete | https://ambientcg.com/view?id=Concrete034 | CC0 | diff nor rough | tex/Concrete034/ | 128 | micro-detail for the light grey 80x80 porcelain (grout stays procedural), balcony tiles |
| PaintedPlaster017 | painted plaster | https://ambientcg.com/view?id=PaintedPlaster017 | CC0 | diff nor rough | tex/PaintedPlaster017/ | 228 | interior walls: use nor and rough only, keep the wall colour factor |
| Plaster001 | white exterior render | https://ambientcg.com/view?id=Plaster001 | CC0 | diff nor rough | tex/Plaster001/ | 424 | building facades, balcony parapet |
| Tiles143 | beige stone cladding blocks | https://ambientcg.com/view?id=Tiles143 | CC0 | diff nor rough | tex/Tiles143/ | 160 | Jerusalem-stone-like neighbour facades |
| Metal009 | brushed stainless steel | https://ambientcg.com/view?id=Metal009 | CC0 | diff nor rough metal | tex/Metal009/ | 128 | fridge, oven trim, hood, sink |
| Metal027 | dark painted metal | https://ambientcg.com/view?id=Metal027 | CC0 | diff nor rough metal | tex/Metal027/ | 180 | black railing, black fittings, window frames, light fixtures |
| Plastic012A | graphite matte plastic | https://ambientcg.com/view?id=Plastic012A | CC0 | diff nor rough | tex/Plastic012A/ | 192 | graphite kitchen fronts |
| Plastic010 | smooth light plastic (tint to white) | https://ambientcg.com/view?id=Plastic010 | CC0 | diff nor rough | tex/Plastic010/ | 52 | white lacquer fronts, white appliances |
| Leather026 | black leather | https://ambientcg.com/view?id=Leather026 | CC0 | diff nor rough | tex/Leather026/ | 252 | dark leather sofa |
| Wicker008A | rattan weave with cut-outs | https://ambientcg.com/view?id=Wicker008A | CC0 | diff nor rough opacity | tex/Wicker008A/ | 260 | rattan egg chair shell on the balcony (alphaTest with the opacity map) |
| Terrazzo005 | white terrazzo with dark chips | https://ambientcg.com/view?id=Terrazzo005 | CC0 | diff nor rough | tex/Terrazzo005/ | 464 | bathroom floors |
| WoodFloor010 | natural oak long planks; diff 2k, nor and rough 1k | https://ambientcg.com/view?id=WoodFloor010 | CC0 | diff nor rough | tex/WoodFloor010/ | 720 | bedroom oak floors (alternative to the current `laminate_floor_02`) |
| natural_walnut_veneer | mid-tone walnut veneer, 1 m tile | https://polyhaven.com/a/natural_walnut_veneer | CC0 | diff nor rough | tex/natural_walnut_veneer/ | 192 | master wooden slat wall, TV unit |
| curly_teddy_natural | ivory boucle fabric, 0.34 m tile, 512 | https://polyhaven.com/a/curly_teddy_natural | CC0 | diff nor rough | tex/curly_teddy_natural/ | 156 | cushions (retexture `throw_pillows_01`), bed throw, armchair |
| terry_cloth | towelling, 0.37 m tile, 512 (blue: use nor and rough with a white or grey colour factor) | https://polyhaven.com/a/terry_cloth | CC0 | diff nor rough | tex/terry_cloth/ | 176 | bathroom towels on the existing rails |
| hessian_230 | jute weave, 0.27 m tile, 512 | https://polyhaven.com/a/hessian_230 | CC0 | diff nor rough | tex/hessian_230/ | 240 | jute rug, balcony mat, laundry basket |
| Carpet016 | cream low-pile carpet, 512 | https://ambientcg.com/view?id=Carpet016 | CC0 | diff nor rough | tex/Carpet016/ | 180 | salon rug under the coffee table, bedroom rug |
| interlocking_concrete_pavers | interlocking pavers, 1.8 m tile (brownish: tint to grey) | https://polyhaven.com/a/interlocking_concrete_pavers | CC0 | diff nor rough | tex/interlocking_concrete_pavers/ | 416 | street sidewalk |
| PavingStones136 | light paving slabs | https://ambientcg.com/view?id=PavingStones136 | CC0 | diff nor rough | tex/PavingStones136/ | 292 | building forecourt and entrance path |
| Fingerprints002 | smudge and fingerprint mask (no colour map) | https://ambientcg.com/view?id=Fingerprints002 | CC0 | nor rough opacity | tex/Fingerprints002/ | 292 | roughness overlay on the glossy fridge, oven glass, lacquer and mirrors |

## HDRIs (environment lighting and reflections)

Poly Haven 1k Radiance `.hdr`, for RGBELoader into PMREM (in place of, or blended with, RoomEnvironment). `hdri/<id>_1k.hdr`.

| id | what it is | source | licence | staged path | KB | use for |
|---|---|---|---|---|---|---|
| kloofendal_48d_partly_cloudy | midday, partly cloudy, high contrast | https://polyhaven.com/a/kloofendal_48d_partly_cloudy | CC0 | hdri/kloofendal_48d_partly_cloudy_1k.hdr | 1,600 | day mode: window reflections, glossy kitchen, balcony; matches the day sky |
| suburban_parking_area | low sun, clear, suburban street, low contrast | https://polyhaven.com/a/suburban_parking_area | CC0 | hdri/suburban_parking_area_1k.hdr | 1,312 | softer day or golden-hour option with buildings in the reflections |
| stuttgart_suburbs | low sun, partly cloudy, suburban houses | https://polyhaven.com/a/stuttgart_suburbs | CC0 | hdri/stuttgart_suburbs_1k.hdr | 1,684 | eve mode reflections |

Not staged: `belfast_sunset` (https://polyhaven.com/a/belfast_sunset, CC0, 1.55 MB at 1k) is the closest match to the
current eve sky. 2k versions of all of these are about 6 MB each.

## Gaps (no CC0 model found)

- Bathroom: towels, soap dispenser, toothbrush cup, bath mat. Make towels procedurally (rounded box plus `terry_cloth`).
- Rugs: no CC0 rug model; use a thin plane with `Carpet016` or `hessian_230`.
- Rattan egg chair: no CC0 model. Build a lathe shell with `Wicker008A` (opacity) on a black metal stand (`Metal027`).
- Kitchen: no modern kettle (Poly Haven only has a vintage one), no toaster, no coffee machine.
- Books: `decorative_book_set_01` exists on Poly Haven but ships without glTF (blend, fbx, usd only). The scene's
  procedural books stay.
- Trees: no CC0 olive, palm or ficus with a usable licence and size.
- Kenney Furniture Kit (https://kenney.nl/assets/furniture-kit, CC0) has low-poly stand-ins for most of the above, but
  the flat-shaded style does not match. Not staged.

## Tree and plant impostor candidates (notes only, nothing staged)

All Poly Haven CC0, for baking into tree cards with `source/treecards.py`:

- `island_tree_01` (about 3.7M tris, render only), `island_tree_03`: broad street trees.
- `searsia_lucida`, `searsia_burchellii`: dense evergreen shrubs and small trees, read as Mediterranean.
- `othonna_cerarioides`, `wild_rooibos_bush`, `shrub_01` to `shrub_04`: low shrubs for planting strips and the forecourt.
- `quiver_tree_01`, `quiver_tree_02`: sculptural, for a single garden accent.
- `pachira_aquatica_01`: also staged as a real mesh above (indoor).
- Already used: `jacaranda_tree`, `tree_small_02`, `island_tree_02`.

## Regenerating

Scripts in `source/out/real5/assets/_tools/` (raw downloads go to `/tmp/r5/src`):

1. `python3 fetch.py`: downloads the Poly Haven glTFs, textures and HDRIs, and the ambientCG zips.
2. `node split.mjs <in.gltf> <out.glb> <node>[,<node>...]`: the variant splits (commands for each variant are in this
   file's plants and props rows: pachira c/d as bark plus leaves pairs, anthurium b/c, calathea a/b, fern b,
   bananas bunch, wine bordeaux/champagne, outdoor set with all three nodes), output to `/tmp/r5/split`.
3. `python3 process.py [tex|models [ids]]`: WebP textures, HDRI copy, gltf-transform optimisation and the frame glass fix.
4. `node stats.mjs ../models/*.glb`: triangles, bounds, materials. `node sheet.mjs <png> <base-url> <ids>` renders a
   contact sheet through `preview.html` (serve the repo root first).
