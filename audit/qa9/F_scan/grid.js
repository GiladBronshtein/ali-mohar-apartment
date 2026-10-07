// slivers: for each edge position e and grid origin o, size s: distance from e to the nearest grout line (on the room side ignored; we report min(d, s-d))
const fr = a => a - Math.floor(a);
const cut = (e, o, s, side) => { const d = fr((e - o) / s) * s; return side === 'min' ? (d < 1e-6 ? s : s - d) : (d < 1e-6 ? s : d); };
const SP = {
  floor: { x: { 0: 'storage wall x0 (hidden 0..0.6 by cabinets)', 7.28: 'living facade / balcony doors', 1.45: 'entry W wall', 4.30: 'entry stub', '-2.12': 'corridor W end', 4.15: 'corridor E end (master door)', 1.80: 'passage W', 3.00: 'passage E', '-3.80': 'mamad W', '-0.25': 'mamad E' },
           z: { '-1.245': 'corridor N wall', '-0.145': 'corridor S wall', 0: 'TV wall (living)', 2.775: 'alcove step', 5.50: 'entry door wall', 8.79: 'kitchen S wall', 0.125: 'mamad N', 2.745: 'mamad S' } },
  rooms: { x: { '-3.89': 'room1 W', '-1.15': 'room1 E', '-0.97': 'room2 W', 1.85: 'room2 E', 4.61: 'master W', 8.91: 'master/closet E', 7.01: 'closet W' },
           z: { '-5.035': 'room1 N', '-1.425': 'room1 S', '-5.01': 'room2 N', '-1.45': 'room2 S', '-3.105': 'master N', '-0.145': 'master S', '-4.995': 'closet N', '-3.245': 'closet S' } },
  bathF: { x: { 2.016: 'W', 4.454: 'E' }, z: { '-3.769': 'N', '-1.401': 'S' } },
  ensF: { x: { 4.636: 'W', 6.844: 'E' }, z: { '-4.974': 'N', '-3.266': 'S' } },
  balc: { x: { 7.70: 'facade', 10.30: 'upstand' }, z: { 0.34: 'N wall', 8.71: 'S wall' } },
};
const MINX = { floor: ['0', '1.45', '4.3', '-2.12', '3', '-3.8'], rooms: ['-3.89', '-0.97', '4.61', '7.01'], bathF: ['2.016'], ensF: ['4.636'], balc: ['7.7'] };
const MINZ = { floor: ['-1.245', '0', '2.775', '0.125'], rooms: ['-5.035', '-5.01', '-3.105', '-4.995'], bathF: ['-3.769'], ensF: ['-4.974'], balc: ['0.34'] };
const cases = [
  ['floor', 'cur 120 (world origin)', 1.2, 1.2, 0, 0], ['floor', 'cur 120 proposed', 1.2, 1.2, 0.08, -0.045],
  ['floor', 'f80 sp.o', .8, .8, 2.555, 5.70], ['floor', 'f60 sp.o', .6, .6, 2.555, 5.70],
  ['rooms', 'f80 sp.o', .8, .8, 4.60, -3.11], ['rooms', 'f60 sp.o', .6, .6, 4.60, -3.11], ['rooms', 'planks cur (x boards 0.2)', 0.2, 99, 0, 0],
  ['bathF', 'w30', .33, .33, 2.01, -3.775], ['bathF', 'w1560', .15, .6, 2.01, -3.775],
  ['ensF', 'w30', .33, .33, 4.63, -4.98], ['ensF', 'w1560', .15, .6, 4.63, -4.98], ['ensF', 'cur 60x120', .6, 1.2, 0, 0],
  ['balc', 'w30', .33, .33, 7.70, .34], ['balc', 'w1560', .15, .6, 7.70, .34],
];
for (const [sp, name, sx, sz, ox, oz] of cases) {
  const r = []; for (const [k, v] of Object.entries(SP[sp].x)) { const c = cut(+k, ox, sx, MINX[sp].includes(k) ? 'min' : 'max'); if (c < .1) r.push(`${v} ${(c * 100).toFixed(1)}cm`); }
  for (const [k, v] of Object.entries(SP[sp].z)) { const c = cut(+k, oz, sz, MINZ[sp].includes(k) ? 'min' : 'max'); if (c < .1) r.push(`${v} ${(c * 100).toFixed(1)}cm`); }
  console.log(sp.padEnd(6), name.padEnd(26), r.length ? 'SLIVERS <10cm: ' + r.join('; ') : 'ok');
}
console.log('--- search');
for (const [sp, s] of [['floor', .8], ['floor', .6], ['rooms', .8], ['rooms', .6]]) {
  let best = []; const ex = ['0'];
  for (let ox = 0; ox < s; ox += .005) for (let oz = 0; oz < s; oz += .005) {
    let worst = 9; for (const [k] of Object.entries(SP[sp].x)) { if (ex.includes(k) && sp === 'floor') continue; worst = Math.min(worst, cut(+k, ox, s, MINX[sp].includes(k) ? 'min' : 'max')); }
    for (const [k] of Object.entries(SP[sp].z)) worst = Math.min(worst, cut(+k, oz, s, MINZ[sp].includes(k) ? 'min' : 'max'));
    best.push([worst, ox, oz]);
  }
  best.sort((a, b) => b[0] - a[0]); console.log(sp, s, best.slice(0, 3).map(b => `min piece ${(b[0] * 100).toFixed(1)}cm at o=[${b[1].toFixed(3)}, ${b[2].toFixed(3)}]`).join(' | '));
}
console.log('--- joint');
for (const sp of ['floor', 'rooms']) {
  let best = [];
  for (let ox = 0; ox < 2.4; ox += .005) for (let oz = 0; oz < 2.4; oz += .005) {
    let worst = 9; for (const s of [.8, .6]) { for (const [k] of Object.entries(SP[sp].x)) { if (k === '0' && sp === 'floor') continue; worst = Math.min(worst, cut(+k, ox, s, MINX[sp].includes(k) ? 'min' : 'max')); }
      for (const [k] of Object.entries(SP[sp].z)) worst = Math.min(worst, cut(+k, oz, s, MINZ[sp].includes(k) ? 'min' : 'max')); }
    best.push([worst, ox, oz]);
  }
  best.sort((a, b) => b[0] - a[0]); console.log(sp, best.slice(0, 4).map(b => `min ${(b[0] * 100).toFixed(1)}cm o=[${b[1].toFixed(3)}, ${b[2].toFixed(3)}]`).join(' | '));
}
console.log('--- proposed');
for (const [sp, s, ox, oz] of [['floor', .8, 1.015, .51], ['floor', .6, 1.015, .51], ['rooms', .8, 1.25, 1.925], ['rooms', .6, 1.25, 1.925], ['bathF', .33, 2.10, -3.69], ['bathF', .15, 2.10, -3.69]]) {
  const r = []; for (const [k, v] of Object.entries(SP[sp].x)) r.push(`${v} ${(cut(+k, ox, s, MINX[sp].includes(k) ? 'min' : 'max') * 100).toFixed(1)}`);
  for (const [k, v] of Object.entries(SP[sp].z)) r.push(`${v} ${(cut(+k, oz, s, MINZ[sp].includes(k) ? 'min' : 'max') * 100).toFixed(1)}`);
  console.log(sp, s, r.join('; '));
}
