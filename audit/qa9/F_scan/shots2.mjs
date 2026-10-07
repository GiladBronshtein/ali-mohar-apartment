// QA9 capture tool. Usage (always through the GPU lock):  bash /tmp/gpu.sh node out/shots.mjs <spec.json> <outdir>
// spec.json: [{ "name": "x", "view": "entry" } | { "name": "x", "pos": [x,y,z], "tgt": [x,y,z], "fov": 60 }, ...]
//   optional per shot: "mode": "day"|"eve" (default day), "doors": "closed"|"open", "curtains": "closed"|"open", "w": 1440, "h": 900, "dims": true
// Coordinates: three.js metres, y up, floor 0, ceiling 2.70 (see DESIGN.md "Coordinates"). Serves the built site at BASE (default http://127.0.0.1:8791/).
import { chromium } from '/Users/Gilad.Bronshtein/AliMohar/source/node_modules/playwright/index.mjs';
import fs from 'fs';
const [SPEC, OUT] = process.argv.slice(2); const shots = JSON.parse(fs.readFileSync(SPEC, 'utf8')); fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--enable-gpu'] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 200)); });
await p.goto(process.env.BASE || 'http://127.0.0.1:8791/', { waitUntil: 'domcontentloaded', timeout: 180000 });
await p.waitForFunction(() => window.__app && document.getElementById('loading').hidden, null, { timeout: 180000 });
await p.waitForTimeout(6000); await p.evaluate(() => window.__app.setPanel && window.__app.setPanel(false));
let mode = 'day', doors = 'open', curt = 'open', size = '1440x900';
for (const s of shots) {
  const sz = `${s.w || 1440}x${s.h || 900}`; if (sz !== size) { await p.setViewportSize({ width: s.w || 1440, height: s.h || 900 }); size = sz; await p.waitForTimeout(500); }
  const m = s.mode || 'day'; if (m !== mode) { await p.evaluate(m => { window.__app.setEve(m === 'eve'); window.__app.setMode(m === 'eve'); }, m); mode = m; await p.waitForTimeout(800); }
  const d = s.doors || 'open'; if (d !== doors) { await p.evaluate(c => window.__app.setDoors(c), d === 'closed'); doors = d; }
  const c = s.curtains || 'open'; if (c !== curt) { await p.evaluate(c => window.__app.setCurtains(c), c === 'closed'); curt = c; }
  await p.evaluate(v => window.__app.setDims(!!v), s.dims); await p.evaluate(c => { const A = window.__app; A.CER_SPACES.forEach(sp => { const want = (c || {})[sp.id] || 'cur'; let key = want; if (want !== 'cur' && !want.includes('|')) { const opt = [...document.querySelectorAll('#cerList option')].find(o => o.value.startsWith(want + '|')); key = opt ? opt.value : 'cur'; } if ((A.cerState[sp.id] || 'cur') !== key) A.cerSet(sp.id, key); }); }, s.cer); if (s.cer) await p.waitForTimeout(1500);
  await p.evaluate(s => { const A = window.__app; if (s.view) { A.setView(s.view, true); return; }
    A.setView(s.inView || 'entry', true); A.camera.position.set(...s.pos); A.controls.target.set(...s.tgt); A.camera.fov = s.fov || 60; A.camera.updateProjectionMatrix(); A.controls.update(); }, s);
  await p.waitForTimeout(2600);
  await p.screenshot({ path: `${OUT}/${s.name}.jpg`, type: 'jpeg', quality: 86 });
}
console.log(errs.length ? errs.join('\n') : 'no errors', '|', shots.length, 'shots ->', OUT);
await b.close();
