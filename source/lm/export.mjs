// Lightmap step 1: export the scene exactly as the browser builds it (after mergeGroup), in world space.
import { chromium } from 'playwright';
import fs from 'fs';
const work = process.argv[2] || 'lm/work';
fs.mkdirSync(work, { recursive: true });
let src = fs.readFileSync(process.env.SRC || 'salon.html', 'utf8').replaceAll('https://cdn.jsdelivr.net/npm/three@0.160.0/', '/node_modules/three/').replaceAll('https://cdn.jsdelivr.net/npm/three-mesh-bvh@0.7.6/', '/node_modules/three-mesh-bvh/').replaceAll('https://cdn.jsdelivr.net/npm/three-gpu-pathtracer@0.0.23/', '/node_modules/three-gpu-pathtracer/');
fs.writeFileSync('lm_local.html', '<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">' + src.replace('?baked', '?nobake'));
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 400, height: 300 } });
page.on('pageerror', e => console.log('ERR', e.message));
await page.addInitScript(() => { window.__pause = true; window.__nobake = true; });
await page.goto('http://localhost:8765/lm_local.html');
await page.waitForFunction(() => window.__app, null, { timeout: 180000 });
const out = await page.evaluate(() => {
  const A = window.__app, THREE = A.THREE;
  const avgCache = new Map();
  function texAvg(t) {   // mean linear colour of a procedural (canvas) texture
    if (!t || !t.image) return [1, 1, 1];
    if (avgCache.has(t)) return avgCache.get(t);
    const im = t.image, c = document.createElement('canvas'); c.width = 64; c.height = 64; const g = c.getContext('2d');
    try { g.drawImage(im, 0, 0, 64, 64); } catch (e) { return [1, 1, 1]; }
    const d = g.getImageData(0, 0, 64, 64).data; let r = 0, gg = 0, b = 0;
    const lin = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
    for (let i = 0; i < d.length; i += 4) { r += lin(d[i]); gg += lin(d[i + 1]); b += lin(d[i + 2]); }
    const n = d.length / 4, res = [r / n, gg / n, b / n]; avgCache.set(t, res); return res;
  }
  const names = new Map(); for (const k in A.mat) names.set(A.mat[k], k);
  const meshes = [], bufs = []; let off = 0;
  const push = arr => { const o = off; bufs.push(arr); off += arr.byteLength; return o; };
  const groups = [['root', A.root], ['ceil', A.ceilGroup], ['outside', A.outside], ['doors', A.doorGroup], ['fan', A.fanGroup], ['curt', A.curtGroup]];
  let id = 0;
  for (const [gname, grp] of groups) {
    grp.updateMatrixWorld(true);
    grp.traverse(o => {
      if (!o.isMesh || o.isReflector || !o.visible) return; let vis = true; for (let p = o; p; p = p.parent) if (!p.visible) vis = false; if (!vis) return;
      const m = o.material; if (!m || Array.isArray(m)) return;
      const transparent = m.transparent && m.opacity < .99;
      if (transparent && !m.map) return;                          // glass, sheers: light passes
      let g = o.geometry; if (g.index) g = g.toNonIndexed();
      const pos = g.attributes.position.clone(); pos.applyMatrix4(o.matrixWorld);
      const P = new Float32Array(pos.array);
      const tex = texAvg(m.map), col = m.color ? m.color.toArray() : [.8, .8, .8];
      const em = m.emissive ? m.emissive.toArray().map(v => v * (m.emissiveIntensity ?? 1)) : [0, 0, 0];
      const isStd = m.isMeshStandardMaterial;
      // role: static opaque standard surfaces of the apartment are lightmap targets
      const emitterMat = ['lamp', 'spot', 'led', 'ledWall'].includes(names.get(m));
      let role = 'occluder';
      if ((gname === 'root' || gname === 'ceil') && isStd && !transparent && !emitterMat && P.length >= 9) role = 'target';
      if (emitterMat) role = 'emitter';
      const rec = { id: id++, group: gname, role, name: names.get(m) || m.name || m.type, vertices: P.length / 3, triangles: P.length / 9,
        position: push(P), uuid: o.uuid,
        material: { color: col.map((c, i) => c * tex[i]), roughness: m.roughness ?? .8, metalness: m.metalness ?? 0, emission: em, side: m.side } };
      const bb = new THREE.Box3().setFromBufferAttribute(pos);
      rec.bbox = [bb.min.x, bb.min.y, bb.min.z, bb.max.x, bb.max.y, bb.max.z];
      meshes.push(rec);
    });
  }
  // lights
  const lights = [];
  A.scene.traverse(o => { if (!o.isLight) return;
    const L = { type: o.type, color: o.color.toArray(), intensity: o.intensity, k: o.userData.k ?? null, position: o.getWorldPosition(new THREE.Vector3()).toArray() };
    if (o.isDirectionalLight) L.target = o.target.getWorldPosition(new THREE.Vector3()).toArray();
    if (o.isPointLight) { L.distance = o.distance; L.decay = o.decay; }
    if (o.isHemisphereLight) L.groundColor = o.groundColor.toArray();
    lights.push(L); });
  // flatten buffers to base64 chunks
  const total = new Uint8Array(off); let p = 0; for (const b of bufs) { total.set(new Uint8Array(b.buffer, b.byteOffset, b.byteLength), p); p += b.byteLength; }
  let bin = ''; const CH = 0x8000; for (let i = 0; i < total.length; i += CH) bin += String.fromCharCode.apply(null, total.subarray(i, i + CH));
  return { meshes, lights, bin: btoa(bin) };
});
await browser.close();
fs.writeFileSync(work + '/scene.bin', Buffer.from(out.bin, 'base64'));
delete out.bin;
fs.writeFileSync(work + '/scene.json', JSON.stringify(out));
const by = {}; out.meshes.forEach(m => { by[m.role] = by[m.role] || [0, 0]; by[m.role][0]++; by[m.role][1] += m.triangles; });
console.log('meshes by role [count, triangles]', JSON.stringify(by), 'lights', out.lights.length);
