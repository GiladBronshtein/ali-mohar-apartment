# Build the GitHub Pages copy of the viewer from salon.html (the artifact source): full HTML document, local three.js,
# icons, manifest, share card. Usage: python3 build_site.py [--repo ali-mohar-apartment] [--user giladbronshtein]
import re, sys, json, os
SITE = os.environ.get('SITE', '..')   # the published site is the repo root, one level up from source/
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
repo, user = args.get('--repo', 'ali-mohar-apartment'), args.get('--user', 'giladbronshtein')
base = f'https://{user}.github.io/{repo}/'
s = open('salon.html').read()
head, body = s.split('\n<div id="stage">', 1); body = '<div id="stage">' + body
title = re.search(r'<title>(.*?)</title>', head).group(1); desc = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
head = head.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
head = head.replace('html, body { height: 100%; }', 'html, body { height: 100%; margin: 0; padding: 0; }')
body = (body.replace('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js', './vendor/three/build/three.module.min.js')   # minified: 166 KB gzip instead of 257
            .replace('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/', './vendor/three/examples/jsm/')
            .replace('https://cdn.jsdelivr.net/npm/three-mesh-bvh@0.7.6/build/index.module.js', './vendor/three-mesh-bvh/build/index.module.js')
            .replace('https://cdn.jsdelivr.net/npm/three-gpu-pathtracer@0.0.23/build/index.module.js', './vendor/three-gpu-pathtracer/build/index.module.js'))
assert 'cdn.jsdelivr' not in body, 'CDN reference left'
meta = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2d5f7c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
{{preloads}}<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{base}">
<meta property="og:locale" content="he_IL">
<meta name="twitter:card" content="summary_large_image">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{title}">
'''
# start the module graph and the start view's photo textures at the first bytes of the page (QA8 load-time research)
mods = ['vendor/three/build/three.module.min.js'] + sorted('vendor/three/examples/jsm/' + m for m in set(re.findall(r"from 'three/addons/([^']+)'", body)))
sets = {'laminate_floor_02': 'nr', 'oak_veneer_01': 'dnr', 'white_stucco': 'nr', 'caban': 'nr', 'Metal009': 'nr', 'Marble021': 'nr', 'rough_linen': 'nr', 'Leather026': 'nr'}
texs = [f'assets/tex/{k}/{dict(d="diff", n="nor", r="rough")[c]}.webp' for k, v in sets.items() for c in v]
preloads = ''.join(f'<link rel="modulepreload" href="{m}">\n' for m in mods if os.path.exists(os.path.join(SITE, m))) + \
           ''.join(f'<link rel="preload" href="{t}" as="fetch" crossorigin>\n' for t in texs if os.path.exists(os.path.join(SITE, t)))
meta = meta.replace('{preloads}', preloads)
doc = f'<!doctype html>\n<html lang="he">\n<head>\n{meta}{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'
open(SITE + '/index.html', 'w').write(doc)
json.dump({"name": title, "short_name": "הדירה", "description": desc, "lang": "he", "dir": "rtl", "start_url": "./", "scope": "./", "display": "fullscreen",
           "background_color": "#e9ecef", "theme_color": "#2d5f7c",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}, {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
          open(SITE + '/site.webmanifest', 'w'), ensure_ascii=False, indent=1)
open(SITE + '/404.html', 'w').write(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="icon" href="/{repo}/favicon.svg"><meta http-equiv="refresh" content="2;url=/{repo}/"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;font-family:Arial,sans-serif;background:#e9ecef;color:#22272b}}a{{color:#2d5f7c}}</style></head><body><p>העמוד לא נמצא. <a href="/{repo}/">חזרה להדמיה</a></p></body></html>\n')
open(SITE + '/robots.txt', 'w').write('User-agent: *\nAllow: /\n'); open(SITE + '/.nojekyll', 'w').write('')
# service worker: cache-first for every static file, keyed by the hash of its bytes, so a return visit after a push downloads
# only what changed (GitHub Pages sends max-age=600 and resets every ETag on each push). index.html and renders/status.json
# stay on the network.
import hashlib
files = {}
for d in ['vendor', 'assets', 'lm', 'renders']:
    for r, _, fs in os.walk(os.path.join(SITE, d)):
        for f in fs:
            fp = os.path.join(r, f); rel = os.path.relpath(fp, SITE).replace(os.sep, '/')
            if rel.endswith('status.json') or f.startswith('.'): continue
            files[rel] = hashlib.sha1(open(fp, 'rb').read()).hexdigest()[:12]
for f in ['favicon.svg', 'favicon-32.png', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'icon-512-maskable.png', 'og.jpg']:
    if os.path.exists(os.path.join(SITE, f)): files[f] = hashlib.sha1(open(os.path.join(SITE, f), 'rb').read()).hexdigest()[:12]
sw = '''// generated by source/build_site.py: cache-first for static files keyed by content hash; everything else from the network
const H = %s;
const CACHE = 'ali-static';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil((async () => {
  const c = await caches.open(CACHE), keep = new Set(Object.entries(H).map(([p, h]) => p + '?h=' + h));
  for (const r of await c.keys()) { const u = new URL(r.url), k = u.href.slice(self.registration.scope.length); if (!keep.has(k)) await c.delete(r); }
  await self.clients.claim();
})()));
self.addEventListener('fetch', e => {
  const r = e.request; if (r.method !== 'GET' || r.headers.has('range')) return;
  const u = new URL(r.url); if (u.origin !== location.origin || !u.href.startsWith(self.registration.scope)) return;
  const p = decodeURIComponent(u.pathname.slice(new URL(self.registration.scope).pathname.length)), h = H[p]; if (!h) return;
  const key = self.registration.scope + p + '?h=' + h;
  e.respondWith((async () => { const c = await caches.open(CACHE), hit = await c.match(key); if (hit) return hit;
    const res = await fetch(r); if (res.ok && res.type === 'basic') c.put(key, res.clone()); return res; })());
});
''' % json.dumps(files, separators=(',', ':'))
open(SITE + '/sw.js', 'w').write(sw)
print('built', len(doc), 'bytes ->', base, '| sw.js lists', len(files), 'files')
