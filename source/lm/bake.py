# Lightmap step 2: unwrap, pack and bake in Cycles. Adapted from the web3d-realism-performance skill's reference bake.py.
#   python3 lm/bake.py <workdir> [--samples 64] [--size 2048] [--texel 0.03]
import bpy, bmesh, json, math, sys, os, time
import numpy as np
from mathutils import Vector
argv = sys.argv[1:]
work = argv[0]
opt = {'samples': 64, 'size': 2048, 'texel': 0.03, 'only': '', 'stop': '', 'device': 'CPU', 'hdri': ''}
for i, a in enumerate(argv):
    if a.startswith('--'): opt[a[2:]] = type(opt.get(a[2:], ''))(argv[i + 1])
SIZE, SAMPLES, TEXEL = int(opt['size']), int(opt['samples']), float(opt['texel'])
t0 = time.time()
def log(*a): print(f'[{time.time() - t0:7.1f}s]', *a, flush=True)
scene_json = json.load(open(os.path.join(work, 'scene.json')))
TO_IRRADIANCE = 1 / 0.3683
blob = open(os.path.join(work, 'scene.bin'), 'rb').read()
def arr(offset, count, dtype, width):
    return np.frombuffer(blob, dtype=dtype, count=count * width, offset=offset).reshape(count, width)
def to_blender(v): return np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
cy = scene.cycles
cy.device = 'CPU'
if opt['device'] == 'GPU':   # Apple silicon: Cycles on Metal
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for d in prefs.devices: d.use = d.type == 'METAL'
    cy.device = 'GPU'
cy.samples = SAMPLES
cy.use_denoising = False
cy.max_bounces = 6; cy.diffuse_bounces = 4; cy.glossy_bounces = 2; cy.transmission_bounces = 2; cy.transparent_max_bounces = 8
cy.caustics_reflective = False; cy.caustics_refractive = False
cy.sample_clamp_indirect = 6.0
cy.min_light_bounces = 2
scene.render.threads_mode = 'AUTO'
# eve emission strengths of the app's emitters (setMode(true)); multiplied by EMIT_GAIN in the lamp bake
EVE_EMIT = {'spot': 2.2, 'lamp': 1.5, 'led': 2.0, 'ledWall': 3.0}
EMIT_GAIN = 1.0
def principled(name, m, label):
    mat = bpy.data.materials.new(name)
    nt = mat.node_tree; bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    c = m.get('color', [.5, .5, .5])
    bsdf.inputs['Base Color'].default_value = (*c, 1)
    bsdf.inputs['Roughness'].default_value = max(.05, m.get('roughness', .5))
    bsdf.inputs['Metallic'].default_value = min(.9, m.get('metalness', 0))
    e = list(m.get('emission', [0, 0, 0]))
    if label in EVE_EMIT:
        base = [max(x, 1e-6) for x in e]; k0 = max(base)
        col = [x / k0 for x in base] if k0 > 1e-5 else [1, .85, .65]
        e = [x * EVE_EMIT[label] * EMIT_GAIN for x in col]
    if max(e) > 1e-4:
        k = max(e); bsdf.inputs['Emission Color'].default_value = (*[x / k for x in e], 1); bsdf.inputs['Emission Strength'].default_value = k
    mat['emission'] = list(e); mat['estrength'] = max(e)
    if m.get('side') == 2 or True: mat.use_backface_culling = False
    return mat
objects = {}
for rec in scene_json['meshes']:
    if opt['only'] and rec['role'] == 'target' and str(rec['id']) not in opt['only'].split(','): continue
    P = to_blender(arr(rec['position'], rec['vertices'], np.float32, 3))
    n = len(P) // 3
    I = np.arange(n * 3, dtype=np.int64).reshape(n, 3)
    me = bpy.data.meshes.new(f"{rec['role']}-{rec['id']}")
    me.vertices.add(len(P)); me.vertices.foreach_set('co', P.ravel())
    me.loops.add(len(I) * 3); me.loops.foreach_set('vertex_index', I.ravel().astype(np.int32))
    me.polygons.add(len(I)); me.polygons.foreach_set('loop_start', np.arange(0, len(I) * 3, 3, dtype=np.int32))
    me.update(calc_edges=True)
    me.shade_flat()
    ob = bpy.data.objects.new(me.name, me); scene.collection.objects.link(ob)
    mat = principled(me.name, rec['material'], rec['name'])
    me.materials.append(mat)
    ob['role'] = rec['role']; ob['rid'] = rec['id']; ob['label'] = rec['name']; ob['nsrc'] = rec['vertices']; ob['dup'] = []
    objects[rec['id']] = ob
targets = [ob for ob in objects.values() if ob['role'] == 'target']
log('built', len(objects), 'objects,', len(targets), 'targets')

def weights_for(ob, bm):
    bsdf = next(n for n in ob.data.materials[0].node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    base = .25 + .75 * (1 - bsdf.inputs['Metallic'].default_value)
    w = {}
    for f in bm.faces:
        c = f.calc_center_median(); n = f.normal
        k = base
        if n.z < -.5 and c.z < .3: k = .02                       # undersides at floor level
        elif n.z > .5 and c.z < .05: k = base * 1.6               # floors: where the eye lands
        elif n.z < -.5 and c.z > 2.3: k = base * .6               # ceilings: smooth light
        elif n.z < -.5: k = base * .35                            # undersides of furniture
        if k > .02:
            loc, hn, _, dist = bvh.ray_cast(c + n * 1e-4, n, 2.0)
            if loc is not None and (dist < .005 or hn.dot(n) > 0): k = .02
        w[f.index] = k
    return w
# One ray-tracing structure over the whole scene, for the covered-face test above.
from mathutils.bvhtree import BVHTree
_v, _f, _n = [], [], 0
for ob in objects.values():
    me = ob.data; co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co)
    vi = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', vi)
    _v.append(co.reshape(-1, 3)); _f.append(vi.reshape(-1, 3) + _n); _n += len(me.vertices)
bvh = BVHTree.FromPolygons(np.concatenate(_v).tolist(), np.concatenate(_f).tolist(), all_triangles=True)
del _v, _f
log('bvh built')

welded = []; targets_by_weld = []
for ob in targets:
    bm = bmesh.new(); bm.from_mesh(ob.data)
    # KEY (a UV layer, the one kind of loop data that survives welding and joining): the loop's index in the
    # three.js topology (triangle * 3 + corner) in x, and later the target it belongs to in y.
    kl = bm.loops.layers.uv.new('KEY')
    for f in bm.faces:
        for k, loop in enumerate(f.loops): loop[kl].uv = (f.index * 3 + k, 0)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    me = bpy.data.meshes.new(ob.name + '-weld'); bm.to_mesh(me); bm.free()
    wo = bpy.data.objects.new(me.name, me); scene.collection.objects.link(wo); wo['src'] = ob.name
    welded.append(wo); targets_by_weld.append(ob)
log('welded')

bpy.ops.object.select_all(action='DESELECT')
for wo in welded: wo.select_set(True)
bpy.context.view_layer.objects.active = welded[0]
for wo in welded: wo.data.uv_layers.active = wo.data.uv_layers.new(name='LM')
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.0, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
bpy.ops.object.mode_set(mode='OBJECT')
log('unwrapped')

# Islands, texel density and packing. Blender's own packer dropped thousands of tiny islands (collapsing them), so
# islands are sized and placed here: each island gets atlas area in proportion to its surface area times its
# importance, then a shelf packer places the bounding boxes (rotated to lie flat) at the largest scale that fits.
def islands(bm, uvl):
    # faces connected through shared UV coordinates at shared vertices
    parent = {f.index: f.index for f in bm.faces}
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) < 2: continue
        for i in range(1, len(lf)):
            a, b = lf[0], lf[i]
            ok = True
            for v in e.verts:
                ua = next(l[uvl].uv for l in a.loops if l.vert == v); ub = next(l[uvl].uv for l in b.loops if l.vert == v)
                if (ua - ub).length > 1e-6: ok = False; break
            if ok: parent[find(a.index)] = find(b.index)
    groups = {}
    for f in bm.faces: groups.setdefault(find(f.index), []).append(f)
    return list(groups.values())

records = {}  # welded object name -> list of [loop indices, uv in weighted metres]
area_total = 0.0
per_object_area = {}
for wo in welded:
    src = bpy.data.objects[wo['src']]
    bm = bmesh.new(); bm.from_mesh(wo.data); bm.faces.ensure_lookup_table()
    uvl = bm.loops.layers.uv['LM']
    w = weights_for(src, bm)
    recs = []; a_obj = 0.0
    for isl in islands(bm, uvl):
        k = max(w[f.index] for f in isl)
        loops = np.array([l.index for f in isl for l in f.loops])
        uv = np.array([l[uvl].uv[:] for f in isl for l in f.loops], np.float64)
        t = uv.reshape(-1, 3, 2)
        a_uv = np.abs((t[:, 1, 0] - t[:, 0, 0]) * (t[:, 2, 1] - t[:, 0, 1]) - (t[:, 2, 0] - t[:, 0, 0]) * (t[:, 1, 1] - t[:, 0, 1])).sum() / 2
        a3 = sum(f.calc_area() for f in isl)
        scale = math.sqrt(a3 * k / a_uv) if a_uv > 1e-14 and a3 > 1e-10 else 0.0
        uv = (uv - uv.min(0)) * scale
        recs.append([loops, uv]); a_obj += a3 * k
    bm.free()
    records[wo.name] = recs; per_object_area[wo.name] = a_obj; area_total += a_obj
    if os.environ.get('LM_DEBUG'): log('weighted', src['label'][:30], len(wo.data.polygons), 'faces', len(recs), 'islands', f'{a_obj:.1f} m2')
# How many atlases at the requested texel size, packing about 60% full; biggest objects first into the emptiest.
capacity = (SIZE * TEXEL) ** 2 * .6
n_atlas = max(1, math.ceil(area_total / capacity))
log(f'weighted area {area_total:.0f} m2 -> {n_atlas} atlas(es) of {SIZE}px at {TEXEL*100:.1f} cm')
bins = [[] for _ in range(n_atlas)]; load = [0.0] * n_atlas
for wo in sorted(welded, key=lambda o: -per_object_area[o.name]):
    i = load.index(min(load)); bins[i].append(wo); load[i] += per_object_area[wo.name]
PAD = 4 / SIZE  # atlas units between islands: 2 texels each side at full size, 1 at the -1k size
MIN = 3 / SIZE  # every island at least 3 texels across (a bevel narrower than a texel would bake no texel of its own)

def sparse_split(loops, uv, small):
    # Islands that fill little of their box (rings: an unrolled soffit or beam top) waste the atlas; cut them into
    # quadrants, recursively, until each piece is reasonably solid or small.
    t = uv.reshape(-1, 3, 2); lo = uv.min(0); wh = uv.max(0) - lo
    area = np.abs((t[:, 1, 0] - t[:, 0, 0]) * (t[:, 2, 1] - t[:, 0, 1]) - (t[:, 2, 0] - t[:, 0, 0]) * (t[:, 1, 1] - t[:, 0, 1])).sum() / 2
    if len(t) < 2 or max(wh) < small or area > .35 * wh[0] * wh[1]: return [(loops, uv)]
    c = t.mean(1) - lo; q = ((c[:, 0] > wh[0] / 2).astype(int) + 2 * (c[:, 1] > wh[1] / 2)).repeat(3)
    if len(np.unique(q)) < 2: return [(loops, uv)]
    return [p for i in range(4) if (q == i).any() for p in sparse_split(loops[q == i], uv[q == i], small)]

def shelf(boxes, S):
    # Shelves with the space beside each shelf's first (tallest) box packed again as smaller shelves, recursively:
    # plain shelves waste the height beside a big island such as the floor. boxes: (w, h), tallest first.
    # Returns positions, or None if they do not fit at scale S.
    dims = [(max(w * S, MIN) + PAD, max(h * S, MIN) + PAD) for w, h in boxes]
    pos = [None] * len(dims); min_w = min(d[0] for d in dims)
    def fill(order, x0, y0, x1, y1):
        # Place what fits in the rectangle, tallest first; return the indices left over, in order.
        if not order or x1 - x0 < min_w or y1 - y0 < dims[order[-1]][1]: return order
        left = []; y = y0; i = 0
        while i < len(order):
            if y1 - y < dims[order[-1]][1]: return left + order[i:]
            k = order[i]; W, H = dims[k]
            if W > x1 - x0 or H > y1 - y: left.append(k); i += 1; continue
            pos[k] = (x0, y); rest = fill(order[i + 1:], x0 + W, y, x1, y + H)
            y += H; order = rest; i = 0
        return left
    return pos if not fill(list(range(len(dims))), 0.0, 0.0, 1.0, 1.0) else None

for a, group in enumerate(bins):
    items = []
    # Long strips (a ring beam unrolls to 70 m) would set the scale on their own: cut them into pieces no longer than
    # a quarter of the atlas's side (a seam across a strip is hard to see).
    side = math.sqrt(sum(per_object_area[wo.name] for wo in group) / .7)
    for wo in group:
        bpy.data.objects[wo['src']]['atlas'] = a
        for loops, uv in records[wo.name]:
            wh = uv.max(0) if len(uv) else np.zeros(2)
            if wh[1] > wh[0]: uv = np.stack([uv[:, 1], wh[0] - uv[:, 0]], 1); wh = wh[::-1]
            n = int(math.ceil(wh[0] / (side / 4))) if wh[0] > side / 4 and wh[0] > 3 * wh[1] else 1
            if n > 1:
                cu = uv.reshape(-1, 3, 2)[:, :, 0].mean(1); part = np.minimum((cu / wh[0] * n).astype(int), n - 1).repeat(3)
                pieces = [(loops[part == i], uv[part == i]) for i in range(n) if (part == i).any()]
            else: pieces = [(loops, uv)]
            pieces = [q for pl, pu in pieces for q in sparse_split(pl, pu, side / 24)]
            for pl, pu in pieces:
                pu = pu - pu.min(0); pwh = pu.max(0)
                items.append((max(pwh[0], 1e-4), max(pwh[1], 1e-4), wo.name, (pl, pu)))
    items.sort(key=lambda it: -it[1])
    boxes = [(w, h) for w, h, *_ in items]
    lo, hi = 0.0, 4.0 / math.sqrt(max(sum(w * h for w, h in boxes), 1e-9))
    for _ in range(18):
        mid = (lo + hi) / 2
        if shelf(boxes, mid): lo = mid
        else: hi = mid
    S = lo; pos = shelf(boxes, S)
    used = sum(w * h for w, h in boxes) * S * S
    for (w, h, name, (loops, uv)), (x, y) in zip(items, pos):
        # Narrow islands are stretched across to the minimum (a lightmap may be anisotropic).
        sx, sy = max(w * S, MIN) / (w * S), max(h * S, MIN) / (h * S)
        rec_uv = uv * S * np.array([sx, sy]) + np.array([x + PAD / 2, y + PAD / 2])
        wo = bpy.data.objects[name]; lm = wo.data.uv_layers['LM']
        buf = np.zeros(len(wo.data.loops) * 2, np.float32); lm.data.foreach_get('uv', buf); buf = buf.reshape(-1, 2)
        buf[loops] = rec_uv; lm.data.foreach_set('uv', buf.ravel())
    log(f'atlas {a}: {len(group)} objects, {len(items)} islands, {used * 100:.0f}% used, {1 / (S * SIZE) * 100:.2f} cm per texel at weight 1')

if opt['stop'] == 'pack': bpy.ops.wm.save_as_mainfile(filepath=os.path.join(work, 'pack.blend')); log('stopping after pack'); sys.exit(0)
# Copy the packed UVs back to the three.js topology, corner by corner (KEY.x is the original loop).
for wo, ob in zip(welded, targets_by_weld):
    wm, me = wo.data, ob.data
    uv_src = np.zeros((len(wm.loops), 2), np.float32); wm.uv_layers['LM'].data.foreach_get('uv', uv_src.ravel())
    key = np.zeros((len(wm.loops), 2), np.float32); wm.uv_layers['KEY'].data.foreach_get('uv', key.ravel())
    out = np.full((len(me.loops), 2), -1.0, np.float32); out[np.round(key[:, 0]).astype(np.int64)] = uv_src
    # Faces the weld collapsed (zero area, never seen): borrow any UV of the same vertex, else the atlas corner.
    missing = np.where(out[:, 0] < 0)[0]
    if len(missing):
        vi = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', vi)
        known = {}
        for li in range(len(me.loops)):
            if out[li, 0] >= 0: known.setdefault(vi[li], out[li])
        for li in missing: out[li] = known.get(vi[li], np.zeros(2, np.float32))
    lm = me.uv_layers.new(name='LM'); lm.data.foreach_set('uv', out.ravel())
    me.uv_layers.active = lm
    bpy.data.objects.remove(wo)
log('uv2 copied back')

# ---------------- lights ----------------
L = scene_json['lights']
sunL = next(x for x in L if x['type'] == 'DirectionalLight')
d3 = np.array(sunL['position']) - np.array(sunL['target']); d3 /= np.linalg.norm(d3)
SUN = Vector((d3[0], -d3[2], d3[1])).normalized()
SUN_STRENGTH = sunL['intensity'] or 2.3   # same as the viewer's sun
world = bpy.data.worlds.new('sky'); scene.world = world
wn = world.node_tree.nodes; bg = next(n for n in wn if n.type == 'BACKGROUND')
def sky_image(w=512, h=256):
    # simple clear-sky gradient (zenith blue, bright horizon, a soft glow around the sun), dark ground below the horizon
    u = (np.arange(w) + .5) / w; v = (np.arange(h) + .5) / h
    U, V = np.meshgrid(u, v)
    phi = (U - .5) * 2 * math.pi; th = (V - .5) * math.pi        # Blender equirect: v up = +z
    x, y, z = np.cos(phi) * np.cos(th), np.sin(phi) * np.cos(th), np.sin(th)
    zen = np.array([.36, .56, .90]); hor = np.array([.86, .90, .95]); gnd = np.array([.30, .29, .27]) * .35
    t = np.clip(z, 0, 1)[..., None] ** .6
    c = hor + (zen - hor) * t
    cosg = np.clip(x * SUN.x + y * SUN.y + z * SUN.z, -1, 1)[..., None]
    c = c * (1 + .9 * np.maximum(cosg, 0) ** 6)
    c = np.where(z[..., None] > 0, c, gnd)
    img = bpy.data.images.new('sky', w, h, float_buffer=True)
    img.pixels.foreach_set(np.concatenate([c, np.ones((h, w, 1))], -1).astype(np.float32).ravel()); return img
def hdri_sky(path, ref):
    # the viewer's photo sky (Poly Haven puresky HDRI): turned so its sun sits at the sun light's azimuth, the sun disc clipped
    # (the sun lamp supplies it), scaled to the same upper-hemisphere mean as the gradient sky so the bake balance holds
    im = bpy.data.images.load(path); w, h = im.size
    px = np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4)[..., :3]
    j, i = np.unravel_index(px.sum(2).argmax(), (h, w))
    u_target = .5 - math.atan2(SUN.y, SUN.x) / (2 * math.pi)
    px = np.roll(px, int(round((u_target - i / w) * w)) % w, axis=1)
    px = np.minimum(px, 8.0); up = px[h // 2:]; px[:h // 2] = np.array([.30, .29, .27]) * .35   # ground as in sky_image
    rp = np.array(ref.pixels[:], dtype=np.float32).reshape(ref.size[1], ref.size[0], 4)[ref.size[1] // 2:, :, :3]
    px[h // 2:] = up * (rp.mean() / up.mean())
    img = bpy.data.images.new('hdri', w, h, float_buffer=True)
    img.pixels.foreach_set(np.concatenate([px, np.ones((h, w, 1), np.float32)], -1).ravel()); return img
env = wn.new('ShaderNodeTexEnvironment'); env.image = hdri_sky(opt['hdri'], sky_image()) if opt['hdri'] else sky_image(); world.node_tree.links.new(env.outputs['Color'], bg.inputs['Color'])
SKY_STRENGTH = .35
sun_data = bpy.data.lights.new('sun', 'SUN'); sun_data.energy = SUN_STRENGTH; sun_data.angle = math.radians(.6)
sun_data.color = tuple(sunL['color'])
sun_ob = bpy.data.objects.new('sun', sun_data); scene.collection.objects.link(sun_ob)
sun_ob.rotation_euler = (-SUN).to_track_quat('-Z', 'Y').to_euler()
lamps = []
for x in L:
    if x['type'] != 'PointLight': continue
    p = x['position']; ld = bpy.data.lights.new('lamp', 'POINT')
    cd = x['k'] if x['k'] is not None else x['intensity']          # eve intensity (candela)
    ld.energy = 4 * math.pi * cd; ld.color = tuple(x['color']); ld.shadow_soft_size = .08
    lo = bpy.data.objects.new('lamp', ld); lo.location = (p[0], -p[2], p[1]); scene.collection.objects.link(lo); lamps.append(lo)
def natural(on):
    sun_ob.hide_render = not on; bg.inputs['Strength'].default_value = SKY_STRENGTH if on else 0.0
def lamps_on(on):
    for lo in lamps: lo.hide_render = not on
    for mat in bpy.data.materials:
        if 'emission' not in mat.keys() or not mat.node_tree: continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf and max(mat['emission']) > 1e-4:
            bsdf.inputs['Emission Strength'].default_value = mat['estrength'] if on else 0.0
# ---------------- bake ----------------
atlases = sorted({ob['atlas'] for ob in targets})
# Cycles re-syncs the whole scene for every object it bakes (about 5 s each on the M4, so 150 targets x 3 bakes took most
# of an hour). Each atlas is baked through one joined copy of its targets instead; the targets are hidden from render
# meanwhile and keep their own LM UVs for the export below.
def bake_proxies():
    out = []
    for a in atlases:
        copies = []
        for ob in targets:
            if ob['atlas'] != a: continue
            c = ob.copy(); c.data = ob.data.copy(); scene.collection.objects.link(c); copies.append(c)
        bpy.ops.object.select_all(action='DESELECT')
        for c in copies: c.select_set(True)
        bpy.context.view_layer.objects.active = copies[0]
        bpy.ops.object.join()
        j = bpy.context.view_layer.objects.active; j['atlas'] = a; out.append(j)
    for ob in targets: ob.hide_render = True
    return out
def bake(kind):
    imgs = {a: bpy.data.images.new(f'{kind}-{a}', SIZE, SIZE, float_buffer=True, alpha=True) for a in atlases}
    for img in imgs.values(): img.generated_color = (0, 0, 0, 0)
    for ob in proxies:
        for mat in ob.data.materials:
            # Each target has its own material, holding its atlas image as the active bake node.
            nt = mat.node_tree
            node = nt.nodes.get('LMBAKE') or nt.nodes.new('ShaderNodeTexImage'); node.name = 'LMBAKE'
            uvn = nt.nodes.get('LMUV') or nt.nodes.new('ShaderNodeUVMap'); uvn.name = 'LMUV'; uvn.uv_map = 'LM'
            nt.links.new(uvn.outputs['UV'], node.inputs['Vector'])
            node.image = imgs[ob['atlas']]; nt.nodes.active = node; node.select = True
    bpy.ops.object.select_all(action='DESELECT')
    for ob in proxies: ob.select_set(True)
    bpy.context.view_layer.objects.active = proxies[0]
    # No margin from Cycles: it grows each object's islands against that object alone, so with every target in one
    # image a neighbour's margin painted over texels already baked (triangular patches on a large sign panel). The
    # margin is grown afterwards over empty texels only (dilate).
    b = scene.render.bake; b.margin = 0; b.use_clear = True; b.target = 'IMAGE_TEXTURES'
    if kind == 'ao':
        world.light_settings.distance = 1.0
        bpy.ops.object.bake(type='AO', margin=0, use_clear=True)
    else:
        b.use_pass_direct = True; b.use_pass_indirect = True; b.use_pass_color = False
        bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT', 'INDIRECT'}, margin=0, use_clear=True)
    log('baked', kind)
    for a, img in imgs.items():
        dilate(img)
        px = denoise(img, f'{kind}-{a}')
        if kind != 'ao': px[..., :3] *= TO_IRRADIANCE
        np.save(os.path.join(work, f'{kind}-{a}.npy'), px.astype(np.float16))
    log('denoised', kind)

# Grows every island by up to 16 texels into empty space (alpha 0): each empty texel next to filled ones takes their
# mean. The islands keep their own texels, and filtering and mipmaps at their edges see their light, not black.
# Alpha stays the coverage of the bake itself.
def dilate(img, steps=16):
    w, h = img.size; px = np.zeros(w * h * 4, np.float32); img.pixels.foreach_get(px); px = px.reshape(h, w, 4)
    rgb = px[..., :3] * (px[..., 3:] > .5); have = (px[..., 3] > .5).astype(np.float32)
    for _ in range(steps):
        s = np.zeros_like(rgb); n = np.zeros_like(have)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            s += np.roll(rgb * have[..., None], (dy, dx), (0, 1)); n += np.roll(have, (dy, dx), (0, 1))
        grow = (have == 0) & (n > 0)
        if not grow.any(): break
        rgb[grow] = s[grow] / n[grow][:, None]; have[grow] = 1
    px[..., :3] = rgb; img.pixels.foreach_set(px.ravel())

# Intel Open Image Denoise, through the compositor of a throwaway empty scene (rendering it costs next to nothing).
def denoise(img, name):
    w, h = img.size
    sc = bpy.data.scenes.new('denoise'); sc.render.engine = 'CYCLES'; sc.cycles.samples = 1; sc.cycles.device = 'CPU'
    sc.render.resolution_x = w; sc.render.resolution_y = h; sc.render.resolution_percentage = 100
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    tree = bpy.data.node_groups.new('denoise', 'CompositorNodeTree'); sc.compositing_node_group = tree
    tree.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    src = tree.nodes.new('CompositorNodeImage'); src.image = img
    dn = tree.nodes.new('CompositorNodeDenoise'); out = tree.nodes.new('NodeGroupOutput')
    tree.links.new(src.outputs['Image'], dn.inputs['Image']); tree.links.new(dn.outputs['Image'], out.inputs[0])
    sc.render.use_compositing = True; sc.render.image_settings.file_format = 'OPEN_EXR'
    bpy.ops.render.render(write_still=False, scene=sc.name)
    path = os.path.join(work, f'{name}.exr')
    bpy.data.images['Render Result'].save_render(path, scene=sc)
    back = bpy.data.images.load(path); px = np.zeros(w * h * 4, np.float32); back.pixels.foreach_get(px)
    raw = np.zeros(w * h * 4, np.float32); img.pixels.foreach_get(raw)
    bpy.data.images.remove(back); bpy.data.scenes.remove(sc)
    # Alpha from the raw bake: 0 where nothing was baked (the margin included).
    return np.concatenate([px.reshape(h, w, 4)[..., :3], raw.reshape(h, w, 4)[..., 3:]], -1)

for ob in objects.values(): ob.select_set(False)
if opt['stop'] != 'maps':  # --stop maps: skip the three bakes (to test the probe)
    proxies = bake_proxies()
    natural(True); lamps_on(False); bake('natural')
    natural(False); lamps_on(True); bake('lamps')
    natural(True); lamps_on(False)
    cy.samples = max(32, SAMPLES // 4); bake('ao')


# ---------------- second UV set for the browser: per corner (the merged geometries are non-indexed) ----------------
meta = []; chunks = []
for ob in targets:
    me = ob.data
    uv = np.zeros((len(me.loops), 2), np.float32); me.uv_layers['LM'].data.foreach_get('uv', uv.ravel())
    q = np.clip(np.round(uv * 65535), 0, 65535).astype(np.uint16)
    rec = next(r for r in scene_json['meshes'] if r['id'] == ob['rid'])
    meta.append({'id': ob['rid'], 'group': rec['group'], 'name': rec['name'], 'vertices': rec['vertices'], 'bbox': rec['bbox'], 'atlas': ob['atlas'], 'count': len(q)})
    chunks.append(q.ravel())
np.concatenate(chunks).tofile(os.path.join(work, 'uv2.bin'))
json.dump({'size': SIZE, 'atlases': len(atlases), 'targets': meta}, open(os.path.join(work, 'uv2.json'), 'w'))
log('done')
