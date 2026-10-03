# Lightmap step 3: float maps -> sRGB WebP (fraction of a per-map range), UV file, manifest.
import numpy as np, json, os, sys, gzip, hashlib
from PIL import Image
work, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
meta = json.load(open(os.path.join(work, 'uv2.json')))
def srgb(x): return np.where(x <= .0031308, 12.92 * x, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - .055)
man = {'size': meta['size'], 'atlases': meta['atlases'], 'maps': {}, 'targets': meta['targets']}
for kind in ('natural', 'lamps', 'ao'):
    for a in range(meta['atlases']):
        p = os.path.join(work, f'{kind}-{a}.npy')
        if not os.path.exists(p): continue
        px = np.load(p).astype(np.float32)[::-1]            # Blender rows start at the bottom
        cov = px[..., 3] > .5
        rgb = np.clip(px[..., :3], 0, None)
        if kind == 'ao':
            rng = 1.0; img = (np.clip(rgb.mean(-1), 0, 1) * 255 + .5).astype(np.uint8)
            im = Image.fromarray(img, 'L').resize((meta['size'] // 2,) * 2, Image.LANCZOS)
        else:
            rng = float(np.percentile(rgb[cov].max(-1), 99.95)) if cov.any() else 1.0
            img = (np.clip(srgb(np.clip(rgb / rng, 0, 1)), 0, 1) * 255 + .5).astype(np.uint8)
            im = Image.fromarray(img, 'RGB')
        buf = __import__('io').BytesIO(); im.save(buf, 'WEBP', quality=92, method=6); data = buf.getvalue()
        name = f'{kind}-{a}-{hashlib.md5(data).hexdigest()[:8]}.webp'
        open(os.path.join(outdir, name), 'wb').write(data)
        man['maps'].setdefault(kind, []).append({'file': name, 'range': rng})
        print(kind, a, 'range', round(rng, 3), len(data) // 1024, 'kB')
raw = open(os.path.join(work, 'uv2.bin'), 'rb').read(); gz = gzip.compress(raw, 9)
uvname = f'uv2-{hashlib.md5(gz).hexdigest()[:8]}.bin.gz'
open(os.path.join(outdir, uvname), 'wb').write(gz); man['uv'] = uvname
json.dump(man, open(os.path.join(outdir, 'manifest.json'), 'w'))
print('uv', len(raw) // 1024, 'kB raw ->', len(gz) // 1024, 'kB gz;', len(meta['targets']), 'targets')
