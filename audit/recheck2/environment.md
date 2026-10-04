# Environment re-check (recheck2): surroundings vs site photos

Date 2026-10-04. Model state: commit 8cec3d9. I compared the photos in `materials/photos` with model shots taken from the
same spots, in `source/out/qa/rc2_ext/`:
- `desktop_{day,eve}_{p01,p06,p08,p10,p11,p12,p25,p26,view,bird1}.jpg`
- `desktop_day_{m26,top,m11}.jpg`

m26 is set up to match photo 26 (position [10.3,1.5,4], facing due east, 85 deg horizontal field of view). top is a plan
view centred on (45,10).

Coordinates are the model's metres: x is east, z is south, street level GY = -6.6. Every position below is an
**estimate** from photo projection (lens unknown, distortion uncorrected) unless it says "plan". Treat them as +-5 m
near the street and +-10 to 15 m for anything past 40 m.

The photos show the site under construction during Sukkot: raw concrete, a temporary red edge rail. The model shows the
finished flat, so construction items are not counted as differences.

## How positions were estimated

Photo 26 was used to calibrate the method, because it looks straight east from the rail. Three things the model already
places from the plan or from earlier photos line up within about 3 deg of bearing:
- the walkway entrance, bearing about 5 deg south of east (model z 3.2 to 8.6)
- the tent, 12 to 22 deg (model 11.7 to 21)
- the school corner

That bearing check is what places the tower (item 1).

## Per photo

| Photo | Real view | Model view | Gap |
|---|---|---|---|
| 26, east, straight down (m26) | Left: the school, near white. Centre: the walkway with bollards and a lamp. Right: the lot, orange-red soil, its south edge a concrete retaining wall at about z 18 to 24. Beyond the wall: a driveway with parked cars and a ramp down to an underground car park. Then the tower, at bearing 21 to 27 deg south of east and about 55 to 65 m away. Due east past the lot: 6 to 8 storey blocks, small, at about 100 m or more. | The lot runs to z 42 and is dusty brown. A 7-storey block at x 64 to 80, z 14 to 34 stands where the real tower is. The tower is at bearing 51 to 65 deg, out of frame. | Tower position, the lot's south edge, soil colour, the block that is too close |
| 11, ESE (m11, p11) | The tower fills the right third: white panels, two dark-brown louvre strips, stepped wings. Under it, the ramp and the driveway. The lot is orange. | A grey, shaded box at the frame edge with one black strip. A beige lot, and beige "desert" to the horizon behind a big block. | Tower, horizon fill, soil |
| 06 and 09, SE from the south end and the kitchen | The tower is centred right beyond the lot. To its left, 6 to 7 storey white blocks with glass balcony rails. | A 7-storey poster block and open desert. p09 shows only the kitchen blind; the view is blocked. | Tower, distant blocks |
| 01 and 03, living room through openings A and B (p01) | Opening A: distant white blocks, orange soil, green trees. Opening B: the tower's white face fills it. | Opening A: dark-gridded blocks close up. Opening B: block and sky. | The tower is the main thing seen from inside; the blocks are too heavy |
| 10, ENE (p10) | The school is near white, with dark-framed windows and only a small grey accent. Blocks behind it show 0.3 to 0.6 of the school's facade height above its roof. | The school is grey-beige, with a large dark grey panel. Blocks rise 0.6 to 0.9 of the school height above its roof. | Blocks too close by about 1.7x, school too dark |
| 08 and 12, NNE along the street (p08, p12) | North of the accessible bays the east side has parallel parking (a white van), a red-paver sidewalk with a yellow tactile edge, young trees with round shrubs at their bases, and lamp poles with a curved arm. The kindergarten has cream sails and a green net. Far blocks are small (150 to 250 m). | Perpendicular bays with cars along the whole school (z -60 to 30). Big blocks at 50 to 70 m tower over the school. | Parking layout, block distance |
| 25, north (p25) | Our north wall is raw concrete. Behind grey-blue corrugated hoarding: a plot of dry weeds and pallets. Ali Mohar ends at a T-junction about 80 to 100 m north, closed by 6 to 8 storey buildings, one with dark-brown cladding. The tiled strip below runs along the building with panels on brackets on its building side. | A blue fence (#4f7fae) at x 12.5, bare soil, and the street running into empty haze. | Hoarding colour and line, north vista |

Photos 02, 04, 05, 07, 13 to 24, 27 and 28 are plans, interiors or model screenshots, so they are not used here.

## Own building exterior

- **Balcony edge upstand.** The model has a 20 cm upstand (`B(BX2-.15,BX2,...,BY,.20)`) with pickets from 0.22 m. The
  photos (10, 11, 12, 25) show a concrete upstand about knee high. Estimate: 0.40 to 0.45 m. The final railing is not
  in any photo, because a temporary rail is fitted. Keep the black pickets as an assumption, but stand them on the
  higher upstand.
- **Neighbour balconies to the south.** The model has one continuous slab per floor, x 7.70 to 10.4, z 9.25 to 22. The
  keyplan (plan) shows separate balcony boxes about 4.4 m long, at z 8.8 to 13.2 and z 26 to 30.8, x about 7.4 to 10.2.
  This barely shows from inside (our solid south wall hides it); it shows in the bird views.
- **Facade cladding.** Raw concrete in every photo, so the final finish is unknown. Leave it as is and keep it labelled
  as an estimate.
- **Floor-1 strip below the balcony.** The photos show white large tiles (sample #b0b5b4 to #babab0 in an underexposed
  frame, so near white; the model's `terrTex` is fine). In photos 25 and 26:
  - no glass rail or aluminium cap is visible at the outer edge (model x 12.70 to 12.76)
  - panels on aluminium brackets stand on the building side of the tiles
  - cars park right at the tile edge, and the outline steps (wider to the north)
  
  It is ambiguous whether the tiles are the floor-1 terrace (with a temporary edge guard) or street-level paving.
  Leave as is until there is a street-level photo.

## Sky and lighting

- **Day sky.** The photo HDRI matches the photos well: bright cumulus, partly overcast. No change.
- **Facades across the street read too dark.**
  - Cause: the sun is ESE (`sun.position` +25,+24,+14) and we look east, so every face we see (west faces) is in sun
    shadow, lit only by hemi .22 and environment .3.
  - The school renders about #a9a294. In the same frames, the real school is the brightest surface after the sky (sample
    #bcbdb4 to #c5c5b8, against soil #a86c41 to #af744c).
  - The photos look diffuse and overcast.
  - Fix: raise `envMapIntensity` on the exterior materials only (school stone, block facades, tower, pavers, soil) to
    about 1.0 to 1.2. Interior materials do not change, and no light reaches the rooms.
  - Alternative: hemi .22 to about .4 by day. This also brightens the interior, so check the room shots.
- **Evening.** The neighbourhood is dead dark: no lit windows and no street lights. Light 25 to 35 per cent of the
  window cells in the block facades and the tower with warm emissive (#ffcf8f), on only in eve. Give the street-light
  heads emissive in eve.
- **Fog.** 90 to 460 with #dfe6ec is fine. The visible problem is the beige ground plane at the horizon (item 2), not the
  fog.

## Changes ranked by visible impact from inside the apartment

1. **Move the tower to the south-east, to the east end of the lot.**
   - Today: `B(34,50,56,74,GY,GY+31)`, across Tirtsa Atar at bearing 51 to 65 deg. It fills opening B in photo 01 and is
     the main SE object in 06, 09, 11 and 26.
   - New mass (estimate, plan about x 60 to 84, z 28 to 55):
     - a stepped mass of two wings: the west wing at x 60 to 72, z 28 to 40, projecting about 3 m toward us; the main
       wing at x 64 to 84, z 34 to 55
     - 9 storeys plus a roof storey, top at GY+30. Photo 26 shows 8 to 9 window rows, so 31 m is slightly tall.
   - Face:
     - white large-format panels, about #f0f0ec, with a 1.2 x 0.6 m joint grid in #d8d8d4
     - two dark-brown louvre strips, 1.4 to 1.6 m wide and full height, in about #4a3a30 (sample #353034, #19191b), on
       the face toward the balcony
     - small square windows, about 0.9 m, scattered, not in strips
     - recessed loggias on the main wing
     - a small red-tile roof element (#b5523b)
   - Remove block `[64,80,14,34,7]`, which stands where the tower is.
2. **Push the eastern block ring out and fill the horizon.** The blocks are 1.6 to 2x too prominent above the school
   roof, and beige ground shows through to the horizon (p11, p25). All values estimates:
   - `[62,78,-40,-20,7]` to about `[100,116,-46,-26,7]`
   - `[60,76,-14,6,6,'stone']` to about `[104,120,-16,4,6,'stone']`. Only its top 2 to 3 storeys should show over the
     school.
   - `[58,74,-72,-52,7]` to about `[90,106,-80,-60,7]`
   - Add 6 to 10 more blocks (6 to 9 storeys, varied) in a ring at 150 to 300 m, plus more courtyard trees, so no bare
     ground shows at the horizon.
   - In `facadeTex`, lighten the dark window and balcony area: currently #4f5961 over 50% x 60% of each cell. Reduce it
     to about 30% x 45%, and give balconies light glass rails (like `mGlassRail`) instead of the solid #6d7478 bars.
   - Red roof pergolas: cover about 20 per cent of the roof, not 45 per cent (they dominate the top view).
3. **Lot: soil colour and extent.**
   - Colour: the soil is orange-red hamra in every photo (sample #a86c41 to #af744c, about 0.9 / 0.58 / 0.37 of the
     school's brightness). Change `soilTex` base #9c8770 to about #b06d40, with flecks about #8e5530 and #c98a5a. Then
     either drop `color: true` on the `park_dirt` set for `mSoil`, or tint `mSoil.color` toward #d08850. This reverses
     the 2026-10-04 "no longer orange" change, so the owner should confirm.
   - Extent: shrink the lot from z 9 to 42 to about z 9 to 22, with a 1.0 m concrete retaining wall (#cfcac0) on its
     south edge.
   - South of the wall: a driveway at about z 22 to 28, x 33 to 80, with 2 to 3 parked cars. Next to it, a ramp down to
     the tower's car park, between concrete walls.
   - Optional: the lot slopes down eastward, by about 1 to 2 m (estimate).
4. **Parking on the east side of Ali Mohar.**
   - Keep perpendicular bays only in front of the school's south end, about z -8 to 3: the two accessible bays where they
     are, plus about 2 regular bays each side. End them with a red-white kerb at the walkway.
   - Bay lines: change the range from z -60 to 30 to about z -8 to 3.
   - Elsewhere on the east side:
     - a parallel-parking lane at x 23.0 to 25.2
     - a sidewalk at x 25.2 to 32
     - round shrubs about 0.4 m in radius at the tree bases
   - Cars: change the nose-in cars at z 15 and 20 to parallel, and add a white van parallel at about (24.1, -22).
   - South of the walkway, the photos do not show the kerb; parallel parking is assumed.
5. **Brighten what we look at.**
   - Exterior `envMapIntensity` to about 1.0 to 1.2, as in "Sky and lighting".
   - School stone: `stoneTex` base rgb(226,218,200) to a more neutral, near-white #e8e6dc, in 120 x 60 cm panels with
     softer joints.
6. **School details.**
   - The grey accent (`B(SX1-.02,SX1,-12,-7.5,...)`, #8d949a, full height) is much larger and darker than the real one.
     Make it about #b0b4b6 and limit it to one window bay.
   - Window frames: dark grey, about #4b5258, not #e9e8e4.
   - The south end is a taller volume, about 1.5 m higher, from z about -2 to 3.2, with solar water-heater tanks on it.
   - White utility cabinets along the fence near the walkway corner: x 32.0 to 32.6, z about -1 to 3, 1.5 m high,
     #ecebe6.
7. **Pavers and tactile edge.**
   - Change `paverTex` from #b9a99a toward a red-pink of about #b08a7c on the far sidewalk, and about #a87a6c on the
     walkway. Photo samples are #98867f to #a08e82 and #8b675e, in frames where the school reads #bcbdb4.
   - Add a 0.3 m yellow tactile strip, about #d4c27a, along the east kerb at x 28.0 to 28.3.
8. **North of the building.**
   - Hoarding: change `mBlueFence` from #4f7fae to grey-blue corrugated, about #8a979b (sample #869295).
   - Move its east line from x 12.5 to about x 10.8.
   - Ground: dry weeds, about #8a7656, with a few pallets, instead of soil.
9. **North vista.**
   - End Ali Mohar at a T-junction about z -90 to -100, with a cross street at about x -60 to 90.
   - Close the view with a 6 to 8 storey block across it, at about x -5 to 25, z -118 to -100. Give one block
     dark-brown balcony cladding, about #4a3a32.
   - Add 2 to 3 more cream sails (#e0cc9c) and a green net to the kindergarten.
10. **Evening life.** Lit windows on 25 to 35 per cent of the cells (warm #ffcf8f, eve only). Street-light heads emissive.
11. **Street lights.**
    - A single curved arm instead of the straight bar `B(26.6,28.4,...)`.
    - About 8 m tall (estimate), grey #9aa0a4, with a flat luminaire head.
    - Positions are fine.
12. **Own balcony upstand** from 0.20 to about 0.45 m, with the pickets on top (estimate; the final railing is unknown).
13. **Neighbour balconies to the south** as separate boxes, about 4.4 m long, at z 8.8 to 13.2 and z 26 to 30.8 (keyplan
    reading, x 7.4 to 10.2), instead of the continuous slab from z 9.25 to 22.
14. **Remove the tent and its turf** at x 33.4 to 37.6, z 9.4 to 13.2. It is a sukkah (reed roof, Sukkot-time photos), so
    it is temporary.

Not changed: the day sky, the fog, and the floor-1 strip (ambiguous, see above). The school's footprint, the walkway at z
3.2 to 8.6 and the accessible-bay position match the photos.

If any of items 1 to 4 or 6 is applied, the gallery renders that show the view become stale. Note that in
PROJECT_MEMORY and in README "מגבלות".
