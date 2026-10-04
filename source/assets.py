# Build ../assets (published) from CC0 Poly Haven downloads in out/assets_src (gitignored).
#   python3 assets.py
# Sources (all CC0, https://polyhaven.com):
#   HDRIs  https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/<id>.jpg
#   Textures https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/<id>/<id>_<diff|nor_gl|rough|arm>_1k.jpg
#   Models https://polyhaven.com/a/<id> (glTF 1k)
import os, subprocess, shutil
from PIL import Image
SRC, OUT = 'out/assets_src', '../assets'
Image.MAX_IMAGE_PIXELS = None

def webp(img, path, q=82):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.png'; img.save(tmp); subprocess.run(['cwebp', '-quiet', '-q', str(q), tmp, '-o', path], check=True); os.remove(tmp)

# sky: upper hemisphere plus a margin below the horizon (the ground hides the rest); 4096 x 1152 of the 2:1 equirect
for src, dst in [('kloofendal_48d_partly_cloudy_puresky', 'day'), ('belfast_sunset_puresky', 'eve')]:
    im = Image.open(f'{SRC}/hdri/{src}_tonemapped.jpg').convert('RGB').resize((4096, 2048), Image.LANCZOS)
    webp(im.crop((0, 0, 4096, 1152)), f'{OUT}/sky/{dst}.webp', 80)

# PBR sets: colour (sRGB) only where the set's own colour is used, normal (OpenGL) + roughness always
SETS = {'laminate_floor_02': True, 'oak_veneer_01': True, 'white_stucco': False, 'caban': False, 'rough_linen': False,
        'asphalt_02': True, 'park_dirt': True, 'grass_ground': True}
for sid, color in SETS.items():
    for m, q in ([('diff', 82)] if color else []) + [('nor', 90), ('rough', 80)]:
        webp(Image.open(f'{SRC}/tex/{sid}/{m}.jpg').convert('RGB').resize((1024, 1024), Image.LANCZOS), f'{OUT}/tex/{sid}/{m}.webp', q)

# models: meshopt geometry (simplified 50%), WebP textures at 1k. Needs npx (@gltf-transform/cli 4)
for mid in ['potted_plant_01', 'potted_plant_02']:
    os.makedirs(f'{OUT}/models', exist_ok=True)
    subprocess.run(['npx', '-y', '@gltf-transform/cli@4', 'optimize', f'{SRC}/models/{mid}/{mid}.gltf', f'{OUT}/models/{mid}.glb', '--compress', 'meshopt',
                    '--texture-compress', 'webp', '--texture-size', '1024', '--simplify', 'true', '--simplify-ratio', '0.5', '--simplify-error', '0.002',
                    '--instance', 'false', '--join', 'false', '--flatten', 'false'], check=True)

# tree cards: the two Cycles views from treecards.py (out/tree_<id>_<0|1>.png) side by side, 1024 px tall, WebP with alpha
for tid in ['tree_small_02', 'jacaranda_tree', 'island_tree_02']:
    ims = [Image.open(f'out/tree_{tid}_{k}.png').convert('RGBA') for k in (0, 1)]
    atlas = Image.new('RGBA', (sum(i.width for i in ims), ims[0].height)); atlas.paste(ims[0], (0, 0)); atlas.paste(ims[1], (ims[0].width, 0))
    os.makedirs(f'{OUT}/trees', exist_ok=True); tmp = f'{OUT}/trees/{tid}.png'; atlas.save(tmp)
    subprocess.run(['cwebp', '-quiet', '-q', '82', '-alpha_q', '90', tmp, '-o', f'{OUT}/trees/{tid}.webp'], check=True); os.remove(tmp)

# realism pass 5: CC0 sets staged by out/real5/assets/_tools (ambientCG and Poly Haven WebP). Only the maps the viewer uses,
# resized so the extra download stays small: (id, maps, size)
for sid, maps, size in [('Metal009', ['nor', 'rough'], 512), ('Leather026', ['nor', 'rough'], 512), ('Marble021', ['nor', 'rough'], 1024),
                        ('interlocking_concrete_pavers', ['diff', 'nor', 'rough'], 512)]:
    for m in maps:
        im = Image.open(f'out/real5/assets/tex/{sid}/{m}.webp').convert('RGB')
        webp(im.resize((size, size * im.height // im.width), Image.LANCZOS), f'{OUT}/tex/{sid}/{m}.webp', {'diff': 82, 'nor': 88, 'rough': 80}[m])
# kitchen props (desktop only): already optimised GLBs from the same staging (meshopt, WebP, see audit/realism5/assets.md)
for mid in ['food_apple_01', 'lemon', 'food_pomegranate_01', 'wine_bottle_bordeaux', 'wooden_cutting_board']:
    shutil.copy(f'out/real5/assets/models/{mid}.glb', f'{OUT}/models/{mid}.glb')
