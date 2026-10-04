import { chromium } from 'playwright'; import fs from 'fs';
const svg = fs.readFileSync((process.env.SITE || '..') + '/favicon.svg', 'utf8');
const mask = svg.replace('rx="14" ', '').replace('<g ', '<g transform="translate(32 32) scale(.72) translate(-32 -32)" ');
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH });
const p = await b.newPage();
for (const [name, size, src, bg] of [['favicon-32.png', 32, svg], ['apple-touch-icon.png', 180, mask, true], ['icon-192.png', 192, svg], ['icon-512.png', 512, svg], ['icon-512-maskable.png', 512, mask, true]]) {
  await p.setViewportSize({ width: size, height: size });
  await p.setContent(`<html><body style="margin:0;background:${bg ? '#2d5f7c' : 'transparent'}"><img style="display:block;width:${size}px;height:${size}px" src="data:image/svg+xml;base64,${Buffer.from(src).toString('base64')}"></body></html>`);
  await p.screenshot({ path: (process.env.SITE || '..') + '/' + name, omitBackground: !bg });
}
await b.close(); console.log('icons ok');
