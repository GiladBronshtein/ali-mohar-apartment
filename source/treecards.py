# Tree cards for the exterior: Cycles renders CC0 Poly Haven trees (out/assets_src/models, gitignored) from two sides at 90
# degrees, orthographic, transparent background, lit by a uniform white sky only, so the pixel is albedo x sky occlusion
# (the viewer's sun and hemisphere light do the rest). Writes out/tree_<id>_<0|1>.png and out/treecards.json; assets.py packs
# them into ../assets/trees/<id>.webp, the two views side by side.
#   .venv-bpy/bin/python treecards.py        (bpy venv, see DESIGN.md; Metal GPU)
import bpy, os, math, json
from mathutils import Vector
SRC, H = 'out/assets_src/models', 1024
TREES = ['jacaranda_tree', 'tree_small_02', 'island_tree_02']
meta = {}
for tid in TREES:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.import_scene.gltf(filepath=f'{SRC}/{tid}/{tid}.gltf')
    obs = [o for o in sc.objects if o.type == 'MESH']
    pts = [o.matrix_world @ Vector(c) for o in obs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    ctr, size = (lo + hi) / 2, hi - lo
    w = max(size.x, size.y) * 1.02; h = size.z * 1.02
    W = int(round(H * w / h / 4)) * 4
    world = bpy.data.worlds.new('w'); world.node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1)
    sc.world = world
    cy = sc.cycles; sc.render.engine = 'CYCLES'; cy.samples = 96; cy.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for d in prefs.devices: d.use = d.type == 'METAL'
    cy.device = 'GPU'
    sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(w, h); cam.data.clip_end = 1000
    cam.data.shift_y = 0
    for k, a in enumerate([0, math.pi / 2]):
        d = Vector((math.sin(a), -math.cos(a), 0)) * (max(size) * 2 + 10)
        cam.location = ctr + d; cam.rotation_euler = (math.pi / 2, 0, a)
        f = f'out/tree_{tid}_{k}.png'; sc.render.filepath = os.path.abspath(f)
        if not os.path.exists(f): bpy.ops.render.render(write_still=True)
    meta[tid] = {'w': round(w, 2), 'h': round(h, 2)}
    print(tid, meta[tid], W, 'x', H)
json.dump(meta, open('out/treecards.json', 'w'))
