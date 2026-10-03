import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8791/ali-mohar-apartment/';
const out = process.argv[3] || 'out/site_';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const issues = [];
for (const [name, vp, mobile] of [['desktop', { width: 1440, height: 900 }, false], ['phone', { width: 390, height: 844 }, true]]) {
  const ctx = await b.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: mobile ? 2 : 1 });
  const p = await ctx.newPage();
  p.on('pageerror', e => issues.push(`${name} pageerror: ${e.message}`));
  p.on('console', m => { if (m.type() === 'error') issues.push(`${name} console: ${m.text().slice(0, 200)}`); });
  p.on('response', r => { if (r.status() >= 400) issues.push(`${name} HTTP ${r.status()} ${r.url()}`); });
  p.on('requestfailed', r => { const u = r.url(); if (!/fonts\.(googleapis|gstatic)/.test(u)) issues.push(`${name} failed ${u} ${r.failure()?.errorText}`); });
  const t0 = Date.now();
  await p.goto(BASE, { waitUntil: 'load', timeout: 120000 });
  await p.waitForFunction(() => window.__app && document.getElementById('loading').hidden, null, { timeout: 120000 });
  const ready = Date.now() - t0;
  await p.waitForTimeout(2500);
  await p.evaluate(() => { window.__pause = true; window.__app.renderOnce(); window.__app.renderOnce(); });
  await p.screenshot({ path: `${out}${name}.png`, timeout: 120000 });
  const info = await p.evaluate(async () => {
    const st = await (await fetch('renders/status.json')).json();
    const chk = async u => (await fetch(u)).status;
    return { title: document.title, gal: document.getElementById('btnGal').textContent, galDisabled: document.getElementById('btnGal').disabled,
      viewsC: document.querySelectorAll('#viewsC button').length, views: document.querySelectorAll('[data-k]').length,
      icons: { svg: await chk('favicon.svg'), png: await chk('favicon-32.png'), apple: await chk('apple-touch-icon.png'), manifest: await chk('site.webmanifest'), og: await chk('og.jpg'), i512: await chk('icon-512.png') },
      done: st.done.length };
  });
  console.log(name, 'ready in', ready, 'ms', JSON.stringify(info));
  // gallery: open, check the image loads, step through all
  await p.click('#btnGal'); await p.waitForTimeout(800);
  const imgs = await p.evaluate(async () => { const res = []; const n = document.querySelectorAll('#galName').length; for (let i = 0; i < 17; i++) { const im = document.getElementById('galImg'); await new Promise(r => { if (im.complete && im.naturalWidth) r(); else { im.onload = r; im.onerror = r; setTimeout(r, 4000); } }); res.push(im.naturalWidth > 0 ? 1 : 0); document.getElementById('galNext').click(); await new Promise(r => setTimeout(r, 150)); } return res; });
  console.log(name, 'gallery images loaded:', imgs.reduce((a, b) => a + b, 0), 'of', imgs.length);
  await p.screenshot({ path: `${out}${name}_gal.png`, timeout: 120000 });
  await p.click('#galClose');
  // one of the new views
  await p.evaluate(() => { window.__pause = true; window.__app.setView('bird2', true); window.__app.renderOnce(); }); await p.screenshot({ path: `${out}${name}_bird.png`, timeout: 120000 });
  await ctx.close();
}
await b.close();
console.log(issues.length ? 'ISSUES:\n' + issues.join('\n') : 'no issues');
