import { chromium } from 'playwright';
import fs from 'fs';
const src = fs.readFileSync(process.env.SRC||'salon.html','utf8').replaceAll('https://cdn.jsdelivr.net/npm/three@0.160.0/','/node_modules/three/').replaceAll('https://cdn.jsdelivr.net/npm/three-mesh-bvh@0.7.6/','/node_modules/three-mesh-bvh/').replaceAll('https://cdn.jsdelivr.net/npm/three-gpu-pathtracer@0.0.23/','/node_modules/three-gpu-pathtracer/');
fs.writeFileSync('local.html', '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body style="margin:0">'+src+'</body></html>');
const shots = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
page.on('pageerror', e => console.log('ERR', e.message));
await page.addInitScript(nb => { window.__pause = true; if (nb) window.__nobake = true; }, !!process.env.NOBAKE);
await page.goto('http://localhost:8765/local.html');
await page.waitForFunction(() => window.__app, null, { timeout: 60000 });
await page.evaluate(() => window.__app.LM && window.__app.LM.ready); console.log('LM', await page.evaluate(() => JSON.stringify({c: window.__app.LM?.count, m: window.__app.LM?.missed})));
if (process.env.GAIN) await page.evaluate(g => { const L = window.__app.LM; Object.assign(L.gain, g); }, JSON.parse(process.env.GAIN));
await page.addStyleTag({ content: '.panel,#show,#roomName{display:none!important}' });
await page.evaluate(e => window.__app.setMode(e), !!process.env.EVE);
for (const s of shots) {
  await page.evaluate(s => { const a = window.__app; a.setDoors(!!s.doors); a.setCurtains(!!s.curt); a.views.__qa = { g: 'X', name: '', pos: s.pos, tgt: s.tgt, fov: s.fov || 70 }; a.setView('__qa', true); if (s.noceil) a.ceilGroup.visible = false; a.renderOnce(); }, s);
  await page.waitForTimeout(200);
  await page.screenshot({ path: `out/qa_${process.env.TAG||''}${s.n}.png` });
}
await browser.close();
console.log('done', shots.length);
