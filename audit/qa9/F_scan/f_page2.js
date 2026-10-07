// Injected into the built site (window.__app). Builds one opaque and one transparent BVH over the static interior
// (root, ceilGroup, doors, curtains, fans, loose scene meshes near the apartment) and runs the geometry checks.
// Report-only: nothing in the scene is modified except material.side during raycasts (DoubleSide passed to the BVH, so
// materials are not touched at all).
window.__f9 = (() => {
  const A = window.__app, THREE = A.THREE;
  const H = 2.70, DOORH = 2.10, DROP = H - .35, BC = H - .50, BY = -.04;
  const names = new Map();
  for (const [k, m] of Object.entries(A.mat)) if (!names.has(m)) names.set(m, k);
  const mname = m => names.has(m) ? names.get(m) : 'anon#' + (m.color ? m.color.getHexString() : 'x') + (m.map ? '+map' : '') + (m.transparent ? '+t' : '');
  const visChain = o => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
  let G = null, T = null, mats = [];
  const BOX = { x1: -4.7, x2: 10.8, z1: -5.8, z2: 9.5, y1: -.5, y2: 3.1 };

  function pack(meshes) {
    const tris = []; let n = 0;
    const v = new THREE.Vector3();
    for (const o of meshes) {
      const g = o.geometry, pos = g.attributes.position, idx = g.index, cnt = idx ? idx.count : pos.count;
      const m = Array.isArray(o.material) ? o.material[0] : o.material;
      let id = mats.findIndex(e => e.m === m); if (id < 0) { id = mats.length; mats.push({ m, name: mname(m), transparent: !!m.transparent }); }
      tris.push({ o, pos, idx, cnt, id }); n += Math.floor(cnt / 3);
    }
    const P = new Float32Array(n * 9), M = new Uint16Array(n); let t = 0;
    for (const { o, pos, idx, cnt, id } of tris) {
      const mw = o.matrixWorld;
      for (let i = 0; i + 2 < cnt; i += 3) {
        let x1 = 1e9, x2 = -1e9, z1 = 1e9, z2 = -1e9, y1 = 1e9, y2 = -1e9;
        for (let k = 0; k < 3; k++) {
          v.fromBufferAttribute(pos, idx ? idx.getX(i + k) : i + k).applyMatrix4(mw);
          P[t * 9 + k * 3] = v.x; P[t * 9 + k * 3 + 1] = v.y; P[t * 9 + k * 3 + 2] = v.z;
          x1 = Math.min(x1, v.x); x2 = Math.max(x2, v.x); y1 = Math.min(y1, v.y); y2 = Math.max(y2, v.y); z1 = Math.min(z1, v.z); z2 = Math.max(z2, v.z);
        }
        if (x2 < BOX.x1 || x1 > BOX.x2 || z2 < BOX.z1 || z1 > BOX.z2 || y2 < BOX.y1 || y1 > BOX.y2) continue;   // far outside: drop
        M[t] = id; t++;
      }
    }
    const pos = P.slice(0, t * 9), tm = M.slice(0, t);
    const nrm = new Float32Array(t * 3);
    for (let i = 0; i < t; i++) {
      const a = i * 9, ux = pos[a + 3] - pos[a], uy = pos[a + 4] - pos[a + 1], uz = pos[a + 5] - pos[a + 2], wx = pos[a + 6] - pos[a], wy = pos[a + 7] - pos[a + 1], wz = pos[a + 8] - pos[a + 2];
      let nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx; const l = Math.hypot(nx, ny, nz) || 1;
      nrm[i * 3] = nx / l; nrm[i * 3 + 1] = ny / l; nrm[i * 3 + 2] = nz / l;
    }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos.slice(), 3));
    return { geo, pos, tm, nrm, ntri: t };
  }

  async function build() {
    const mod = await import('three-mesh-bvh');
    A.scene.updateMatrixWorld(true);
    const groups = [A.root, A.ceilGroup, A.doorGroup, A.curtGroup, A.fanGroup].filter(Boolean);
    const set = new Set();
    groups.forEach(g => g.traverse(o => { if (o.isMesh && !o.isReflector && visChain(o)) set.add(o); }));
    const skip = new Set(); A.outside.traverse(o => skip.add(o));
    A.scene.traverse(o => {
      if (!o.isMesh || o.isReflector || set.has(o) || skip.has(o) || !visChain(o)) return;
      o.geometry.computeBoundingSphere(); const s = o.geometry.boundingSphere.clone().applyMatrix4(o.matrixWorld);
      if (s.radius < 30 && s.center.x > BOX.x1 && s.center.x < BOX.x2 && s.center.z > BOX.z1 && s.center.z < BOX.z2) set.add(o);
    });
    const all = [...set];
    const op = all.filter(o => !(Array.isArray(o.material) ? o.material[0] : o.material).transparent);
    const tr = all.filter(o => (Array.isArray(o.material) ? o.material[0] : o.material).transparent);
    G = pack(op); T = pack(tr);
    G.bvh = new mod.MeshBVH(G.geo); T.bvh = T.ntri ? new mod.MeshBVH(T.geo) : null;
    G.index = G.geo.index.array; if (T.bvh) T.index = T.geo.index.array;
    return { meshes: all.length, opaqueTris: G.ntri, transTris: T.ntri, materials: mats.map(m => m.name) };
  }

  const ray = new THREE.Ray(), DS = THREE.DoubleSide;
  function hinfo(S, h, d) {
    const t = Math.floor(S.index[3 * h.faceIndex] / 3), n = [S.nrm[3 * t], S.nrm[3 * t + 1], S.nrm[3 * t + 2]];
    return { d: h.distance, t, m: mats[S.tm[t]].name, back: n[0] * d[0] + n[1] * d[1] + n[2] * d[2] > 0, p: [h.point.x, h.point.y, h.point.z], n };
  }
  function first(S, o, d, far = 60) {
    if (!S || !S.bvh) return null;
    ray.origin.set(o[0], o[1], o[2]); ray.direction.set(d[0], d[1], d[2]);
    const h = S.bvh.raycastFirst(ray, DS, 0, far); return h ? hinfo(S, h, d) : null;
  }
  function all(S, o, d, far = 1) {
    if (!S || !S.bvh) return [];
    ray.origin.set(o[0], o[1], o[2]); ray.direction.set(d[0], d[1], d[2]);
    return S.bvh.raycast(ray, DS, 0, far).map(h => hinfo(S, h, d)).sort((a, b) => a.d - b.d);
  }
  const r4 = v => Math.round(v * 10000) / 10000;
  const DN = [0, -1, 0], UP = [0, 1, 0];
  const R = (x1, x2, z1, z2) => ({ x1, x2, z1, z2 });
  // room interiors (wall faces), expected floor material and its height
  const ROOMS = [
    { n: 'living', ...R(0, 7.28, 0, 2.775), m: 'tile', y: 0 }, { n: 'alcove', ...R(1.45, 7.28, 2.775, 5.50), m: 'tile', y: 0 },
    { n: 'entry+kitchen', ...R(4.30, 7.28, 5.50, 8.79), m: 'tile', y: 0 }, { n: 'kitchenW', ...R(3.63, 4.30, 5.61, 8.79), m: 'tile', y: 0 },
    { n: 'corridor', ...R(-2.12, 4.15, -1.245, -.145), m: 'tile', y: 0 }, { n: 'passage', ...R(1.80, 3.00, -.145, 0), m: 'tile', y: 0 },
    { n: 'mamad', ...R(-3.80, -.25, .125, 2.745), m: 'tile', y: .02 }, { n: 'mamadNiche', ...R(-3.83, -2.36, -.50, .125), m: 'tile', y: .02 },
    { n: 'mamadDoor', ...R(-1.98, -1.19, -.145, .125), m: 'tile', y: .02 },
    { n: 'room1', ...R(-3.89, -1.15, -5.035, -1.425), m: 'planks', y: .009 }, { n: 'room1Niche', ...R(-3.81, -2.36, -1.425, -.80), m: 'planks', y: .009 },
    { n: 'room2', ...R(-.97, 1.85, -5.01, -1.45), m: 'planks', y: .009 },
    { n: 'master', ...R(4.61, 8.91, -3.105, -.145), m: 'planks', y: .009 }, { n: 'vestibule', ...R(4.26, 4.61, -1.245, -.145), m: 'planks', y: .009 },
    { n: 'closet', ...R(7.01, 8.91, -4.995, -3.245), m: 'planks', y: .009 },
    { n: 'familyBath', ...R(2.016, 4.454, -3.769, -1.401), m: 'terrazzo', y: .009 }, { n: 'masterBath', ...R(4.636, 6.844, -4.974, -3.266), m: 'bathFloor', y: .009 },
    { n: 'laundry', ...R(2.15, 4.37, -5.11, -3.99), m: 'terrazzo', y: .003 },
    { n: 'balcony', ...R(7.70, 10.45, .34, 8.71), m: 'deck', y: -.04 }, { n: 'balconyN', ...R(9.30, 10.45, -.13, .34), m: 'deck', y: -.04 },
  ];
  // 1. floor: downward rays, dense near every edge, coarse inside. Flags: nohit, lower surface showing, wrong material at floor level
  function floors() {
    const out = [];
    for (const r of ROOMS) {
      const pts = [];
      const offs = [.001, .003, .006, .01, .015, .02, .03];
      for (let x = r.x1 + .0025; x < r.x2; x += .005) for (const o of offs) { pts.push([x, r.z1 + o]); pts.push([x, r.z2 - o]); }
      for (let z = r.z1 + .0025; z < r.z2; z += .005) for (const o of offs) { pts.push([r.x1 + o, z]); pts.push([r.x2 - o, z]); }
      for (let x = r.x1 + .05; x < r.x2; x += .05) for (let z = r.z1 + .05; z < r.z2; z += .05) pts.push([x, z]);
      let n = 0;
      for (const [x, z] of pts) {
        const h = first(G, [x, .5, z], DN, 1.2); n++;
        if (!h) { out.push({ room: r.n, x: r4(x), z: r4(z), k: 'nohit' }); continue; }
        const y = h.p[1];
        if (y > .03) continue;   // skirting, furniture, rugs: not a floor-level finding
        if (y < r.y - .002) out.push({ room: r.n, x: r4(x), z: r4(z), k: 'lower', m: h.m, y: r4(y) });
        else if (h.m !== r.m && !/rug|berber|mat\b|blackMetal/.test(h.m)) out.push({ room: r.n, x: r4(x), z: r4(z), k: 'mat', m: h.m, y: r4(y) });
      }
      out.push({ room: r.n, k: 'count', n });
    }
    return out;
  }
  // 2. wall bases: horizontal rays at y .035 (inside the 7 cm skirting) and .005 from a grid in every room, 4 directions
  function bases() {
    const out = [], seen = new Set();
    const dirs = [[1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 0, -1]];
    for (const r of ROOMS) for (const y of [.02, .045]) {
      const yy = y + Math.max(0, r.y);
      for (let x = r.x1 + .03; x < r.x2 - .029; x += .02) for (let z = r.z1 + .03; z < r.z2 - .029; z += .02) {
        if (x > r.x1 + .3 && x < r.x2 - .3 && z > r.z1 + .3 && z < r.z2 - .3) continue;
        for (const d of dirs) {
          const hs = all(G, [x, yy, z], d, .6); if (!hs.length || hs[0].back) continue;   // origin inside a solid: skip
          const h = hs[0];
          const key = `${y}|${h.m}|${Math.round(h.p[0] * 200)}|${Math.round(h.p[2] * 200)}|${d.join()}`; if (seen.has(key)) continue; seen.add(key);
          if (['wall', 'cap', 'concrete', 'stucco', 'limewash'].includes(h.m) || h.m.startsWith('anon#ecebe6')) out.push({ room: r.n, y: r4(yy), m: h.m, p: h.p.map(r4), d });
        }
      }
    }
    return out;
  }
  // 3. wet walls: perpendicular rays every 5 mm along the wall, dense near the ends, heights dense near floor and ceiling
  const WET = [
    { room: 'masterBath', x1: 4.63, x2: 6.85, z1: -4.98, z2: -3.26, top: H, fl: .009 },
    { room: 'familyBath', x1: 2.01, x2: 4.46, z1: -3.775, z2: -1.395, top: BC, fl: .009 },
  ];
  function wet() {
    const out = [];
    for (const R0 of WET) for (const wall of ['N', 'S', 'W', 'E']) {
      const X = wall === 'W' || wall === 'E', plane = { N: R0.z1, S: R0.z2, W: R0.x1, E: R0.x2 }[wall], inw = { N: 1, S: -1, W: 1, E: -1 }[wall];
      const [a1, a2] = X ? [R0.z1, R0.z2] : [R0.x1, R0.x2];
      const as = []; for (let a = a1 + .001; a < a2; a += (a - a1 < .03 || a2 - a < .03) ? .002 : .005) as.push(a);
      const ys = [R0.fl + .001, R0.fl + .004, .02, .05]; for (let y = .1; y < R0.top - .05; y += .05) ys.push(y); ys.push(R0.top - .03, R0.top - .01, R0.top - .003);
      for (const a of as) for (const y of ys) {
        const o = X ? [plane + inw * .25, y, a] : [a, y, plane + inw * .25], d = X ? [-inw, 0, 0] : [0, 0, -inw];
        const h = first(G, o, d, .4);
        if (!h) { out.push({ room: R0.room, wall, a: r4(a), y: r4(y), k: 'nohit' }); continue; }
        if (h.back) continue;
        if (!/bathWall|sage|nicheBack|nicheStone/.test(h.m)) out.push({ room: R0.room, wall, a: r4(a), y: r4(y), m: h.m, dist: r4(h.d - .25) });
      }
    }
    return out;
  }
  // 4. ceiling edge: upward rays 2 mm, 1 cm, 3 cm from each wall
  function ceilings() {
    const out = [];
    for (const r of ROOMS) { if (/balcony/.test(r.n)) continue;
      const pts = []; for (const o of [.002, .01, .03]) { for (let x = r.x1 + .005; x < r.x2; x += .01) { pts.push([x, r.z1 + o]); pts.push([x, r.z2 - o]); } for (let z = r.z1 + .005; z < r.z2; z += .01) { pts.push([r.x1 + o, z]); pts.push([r.x2 - o, z]); } }
      for (const [x, z] of pts) { const h = first(G, [x, 1.0, z], UP, 2.0); if (!h) { out.push({ room: r.n, x: r4(x), z: r4(z), k: 'nohit' }); continue; }
        if (h.p[1] > 1.95 && h.m !== 'ceil' && !/led|grille|spot|lamp|slot/.test(h.m)) out.push({ room: r.n, x: r4(x), z: r4(z), m: h.m, y: r4(h.p[1]) }); }
    }
    return out;
  }
  // 5. kitchen splash / TV wall: rays toward the wall, x/y grid
  function splash() {
    const out = [];
    for (let x = 3.646; x < 7.28; x += .005) for (let y = .915; y < 1.63; y += .01) { const h = first(G, [x, y, 8.5], [0, 0, 1], .4); out.push({ w: 'S', a: r4(x), y: r4(y), m: h ? h.m : 'nohit', d: h ? r4(8.5 + h.d) : null }); }
    for (let z = 7.55; z < 8.79; z += .005) for (let y = .915; y < 1.63; y += .01) { const h = first(G, [3.9, y, z], [-1, 0, 0], .4); out.push({ w: 'W', a: r4(z), y: r4(y), m: h ? h.m : 'nohit', d: h ? r4(3.9 - h.d) : null }); }
    for (let z = 7.5; z < 8.79; z += .005) for (let y = .915; y < 1.63; y += .01) { const h = first(G, [7.0, y, z], [1, 0, 0], .5); out.push({ w: 'E', a: r4(z), y: r4(y), m: h ? h.m : 'nohit', d: h ? r4(7 + h.d) : null }); }
    return out;
  }
  return { build, floors, bases, wet, ceilings, splash, first, all, allG: (o, d, far) => all(G, o, d, far), mats: () => mats.map(m => m.name) };
})();
