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
body = (body.replace('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js', './vendor/three/build/three.module.js')
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
<meta property="og:type" content="website">
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
doc = f'<!doctype html>\n<html lang="he">\n<head>\n{meta}{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'
open(SITE + '/index.html', 'w').write(doc)
json.dump({"name": title, "short_name": "הדירה", "description": desc, "lang": "he", "dir": "rtl", "start_url": "./", "scope": "./", "display": "fullscreen",
           "background_color": "#e9ecef", "theme_color": "#2d5f7c",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}, {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]},
          open(SITE + '/site.webmanifest', 'w'), ensure_ascii=False, indent=1)
open(SITE + '/404.html', 'w').write(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="icon" href="/{repo}/favicon.svg"><meta http-equiv="refresh" content="2;url=/{repo}/"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;font-family:Arial,sans-serif;background:#e9ecef;color:#22272b}}a{{color:#2d5f7c}}</style></head><body><p>העמוד לא נמצא. <a href="/{repo}/">חזרה להדמיה</a></p></body></html>\n')
open(SITE + '/robots.txt', 'w').write('User-agent: *\nAllow: /\n'); open(SITE + '/.nojekyll', 'w').write('')
print('built', len(doc), 'bytes ->', base)
