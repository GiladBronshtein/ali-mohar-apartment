import { chromium } from '/Users/Gilad.Bronshtein/AliMohar/source/node_modules/playwright/index.mjs';
import fs from 'fs';
const CHECKS = (process.argv[2] || 'floors,bases,wet,ceilings,splash').split(',');
const b = await chromium.launch({ args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--enable-gpu'] });
const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('http://127.0.0.1:8791/', { waitUntil: 'domcontentloaded', timeout: 240000 });
await p.waitForFunction(() => window.__app && document.getElementById('loading').hidden, null, { timeout: 240000 });
await p.waitForTimeout(3000);
if (process.env.DOORS) await p.evaluate(() => window.__app.setDoors(true)); await p.waitForTimeout(1500); await p.evaluate(fs.readFileSync('/tmp/qa9/f_page2.js', 'utf8'));
console.log(JSON.stringify(await p.evaluate(() => window.__f9.build())).slice(0, 600));
for (const c of CHECKS) { const t = Date.now(); const r = await p.evaluate(c => window.__f9[c](), c); fs.writeFileSync(`/tmp/qa9/${c}.json`, JSON.stringify(r)); console.log(c, r.length, (Date.now() - t) / 1000 + 's'); }
console.log('errors', errs);
await b.close();
