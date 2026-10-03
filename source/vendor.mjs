// copy the three.js files the page actually imports (and everything they import) into site/vendor, keeping paths
import fs from 'fs'; import path from 'path';
const NM = 'node_modules', OUT = (process.env.SITE || '..') + '/vendor';
const map = { 'three': 'three/build/three.module.js', 'three-mesh-bvh': 'three-mesh-bvh/build/index.module.js', 'three-gpu-pathtracer': 'three-gpu-pathtracer/build/index.module.js' };
const resolveSpec = (spec, from) => {
  if (map[spec]) return map[spec];
  if (spec.startsWith('three/addons/')) return 'three/examples/jsm/' + spec.slice(13);
  if (spec.startsWith('three/examples/jsm/')) return spec;
  if (spec.startsWith('.')) return path.posix.normalize(path.posix.join(path.posix.dirname(from), spec));
  throw new Error('unresolved ' + spec + ' from ' + from);
};
const seen = new Set(), queue = ['three', 'three-mesh-bvh', 'three-gpu-pathtracer',
  ...['controls/OrbitControls.js', 'geometries/RoundedBoxGeometry.js', 'environments/RoomEnvironment.js', 'renderers/CSS2DRenderer.js', 'lights/RectAreaLightUniformsLib.js',
      'postprocessing/EffectComposer.js', 'postprocessing/RenderPass.js', 'postprocessing/TAARenderPass.js', 'postprocessing/GTAOPass.js', 'postprocessing/OutputPass.js',
      'postprocessing/UnrealBloomPass.js', 'utils/BufferGeometryUtils.js'].map(p => 'three/addons/' + p)].map(s => resolveSpec(s, ''));
const bare = new Set();
while (queue.length) {
  const f = queue.shift(); if (seen.has(f)) continue; seen.add(f);
  const src = fs.readFileSync(path.join(NM, f), 'utf8');
  fs.mkdirSync(path.join(OUT, path.dirname(f)), { recursive: true }); fs.writeFileSync(path.join(OUT, f), src);
  const re = /(?:import|export)\s*(?:[^'"]*?\sfrom\s*)?['"]([^'"]+)['"]|import\(\s*['"]([^'"]+)['"]\s*\)/g; let m;
  while ((m = re.exec(src))) { const spec = m[1] || m[2]; if (!spec.startsWith('.')) bare.add(spec); queue.push(resolveSpec(spec, f)); }
}
console.log(seen.size, 'files; bare specifiers:', [...bare].join(', '));
