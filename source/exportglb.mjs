import { chromium } from 'playwright';
import fs from 'fs';
const src = fs.readFileSync('salon.html','utf8').replaceAll('https://cdn.jsdelivr.net/npm/three@0.160.0/','/node_modules/three/').replaceAll('https://cdn.jsdelivr.net/npm/three-mesh-bvh@0.7.6/','/node_modules/three-mesh-bvh/').replaceAll('https://cdn.jsdelivr.net/npm/three-gpu-pathtracer@0.0.23/','/node_modules/three-gpu-pathtracer/');
fs.writeFileSync('local.html', '<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">'+src+'</body></html>');
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH, args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });   // desktop: under 640 px the page loads the phone model (no CC0 props, smaller textures)
page.on('pageerror', e => console.log('ERR', e.message));
await page.addInitScript(() => { window.__pause = true; window.__nobake = true; });   // Cycles relights the scene itself
await page.goto('http://localhost:8765/local.html', { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.waitForFunction(() => window.__app, null, { timeout: 600000 }); await page.waitForTimeout(8000);   // photo textures and ceramic defaults (idle) settle
await page.waitForFunction(() => !window.__app.procPlants.visible && !window.__app.procFruit.visible, null, { timeout: 180000 }).catch(() => console.log('CC0 props not loaded: exporting the procedural stand-ins'));
const b64 = await page.evaluate(async () => {
  const A = window.__app, THREE = A.THREE;
  const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
  for (const k in A.mat) A.mat[k].name = k;
  A.ceilGroup.visible = true;
  let i = 0; A.root.traverse(o => { if (o.isMesh) o.name = 'm_' + (o.material.name || 'x') + '_' + (i++); });
  A.ceilGroup.traverse(o => { if (o.isMesh) o.name = 'ceil_' + (o.material.name || 'x') + '_' + (i++); });
  A.outside.traverse(o => { if (o.isMesh) o.name = 'out_' + (i++); }); A.fanGroup.traverse(o => { if (o.isMesh) o.name = 'fan_' + (o.material.name || 'x') + '_' + (i++); });
  const lights = A.warm.map((p, j) => { const l = p.clone(); l.name = 'warm_' + j; l.visible = true; l.intensity = p.userData.k; return l; });
  const grp = new THREE.Group(); lights.forEach(l => grp.add(l));
  const ex = new GLTFExporter();
  A.curtGroup.children.filter(c => !c.visible).forEach(c => A.curtGroup.remove(c));
  const refl = []; A.doorGroup.traverse(o => { if (o.isReflector) refl.push(o); }); refl.forEach(o => o.parent.remove(o));   // live mirrors: Cycles has the mirror material
  A.doorGroup.traverse(o => { if (o.isMesh) o.name = 'm_' + (o.material.name || 'x') + '_d' + (i++); }); A.curtGroup.traverse(o => { if (o.isMesh) o.name = 'm_' + (o.material.name || 'x') + '_c' + (i++); });
  const props = [A.propGroup, A.procPlants, A.procFruit].filter(g => g.visible); props.forEach(g => g.traverse(o => { if (o.isMesh) o.name = 'prop_' + (i++); }));   // onlyVisible is off, so the hidden stand-ins stay out by hand
  const buf = await ex.parseAsync([A.root, A.fixRoot, A.ceilGroup, A.outside, A.fanGroup, A.doorGroup, A.curtGroup, ...props, grp], { binary: true, onlyVisible: false, maxTextureSize: 1024 });
  let bin = ''; const u = new Uint8Array(buf); for (let k = 0; k < u.length; k += 0x8000) bin += String.fromCharCode.apply(null, u.subarray(k, k + 0x8000));
  return btoa(bin);
});
fs.writeFileSync('apartment.glb.tmp', Buffer.from(b64, 'base64')); fs.renameSync('apartment.glb.tmp', 'apartment.glb');
const views = await page.evaluate(() => JSON.stringify(window.__app.views));
fs.writeFileSync('views.json', views);
console.log('glb bytes', fs.statSync('apartment.glb').size);
await browser.close();
