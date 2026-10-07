# Render a view of apartment.glb with Blender Cycles (path tracing + OIDN denoise)
import bpy, os, json, math, sys, time
from mathutils import Vector
view, mode, spp, W, H, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
expo = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
# 'lit' = daylight outside + the interior lights switched on (bathrooms with small windows)
DAY = mode in ('day', 'lit'); LIGHTS = mode in ('eve', 'lit')
V = json.load(open('views.json'))[view]
T2B = lambda p: Vector((p[0], -p[2], p[1]))   # three (x, y-up, z-south) -> blender (x, y, z-up)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='apartment.glb')
sc = bpy.context.scene

for o in list(sc.objects):
    if o.type == 'LIGHT':
        if not LIGHTS: bpy.data.objects.remove(o, do_unlink=True)
        else:
            o.data.energy = 35.0; o.data.color = (1.0, .78, .55); o.data.shadow_soft_size = .08
    elif view == 'top' and o.name.startswith('ceil'):
        o.hide_render = True

def bsdf(m):
    if not m.use_nodes: return None
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED': return n
for m in bpy.data.materials:
    b = bsdf(m); n = m.name.split('.')[0]
    if not b: continue
    if n in ('lamp', 'spot', 'led'):
        b.inputs['Emission Color'].default_value = (1.0, .80, .58, 1)
        b.inputs['Emission Strength'].default_value = ({'lamp': 6, 'spot': 25, 'led': 12}[n] if LIGHTS else 0)
    if n == 'ledWall':
        b.inputs['Emission Color'].default_value = (1.0, .70, .38, 1); b.inputs['Emission Strength'].default_value = (14 if LIGHTS else 5)
    if n == 'showerGlass':
        b.inputs['Alpha'].default_value = 1; b.inputs['Transmission Weight'].default_value = 1; b.inputs['Roughness'].default_value = 0; b.inputs['IOR'].default_value = 1.5
        b.inputs['Base Color'].default_value = (.95, .98, .98, 1)
    if n == 'mirror':
        b.inputs['Metallic'].default_value = 1; b.inputs['Roughness'].default_value = .02; b.inputs['Base Color'].default_value = (.92, .93, .93, 1)
    if n in ('tile', 'bathFloor', 'bathWall', 'quartz'):
        b.inputs['Roughness'].default_value = max(.18, b.inputs['Roughness'].default_value * .7)
    if n == 'glass':
        b.inputs['Alpha'].default_value = .06

# world: physical sky (no disc) + sun lamp
w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
sun_dir_three = Vector((25, 24, 14)).normalized(); sd = T2B(sun_dir_three).normalized()
elev = math.asin(sd.z)
try:
    sky = nt.nodes.new('ShaderNodeTexSky')
    items = [e.identifier for e in sky.bl_rna.properties['sky_type'].enum_items]
    sky.sky_type = 'NISHITA' if 'NISHITA' in items else ('MULTIPLE_SCATTERING' if 'MULTIPLE_SCATTERING' in items else items[0])
    if hasattr(sky, 'sun_disc'): sky.sun_disc = False
    sky.sun_elevation = elev if DAY else math.radians(-4)
    sky.sun_rotation = math.atan2(sd.x, sd.y)
    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = .30 if DAY else .6
except Exception as e:
    print('sky fallback', e); bg.inputs['Color'].default_value = (.55, .7, 1, 1); bg.inputs['Strength'].default_value = 1.0
if mode == 'eve':
    bg.inputs['Strength'].default_value = .04

if DAY:
    sl = bpy.data.lights.new('sun', 'SUN'); sl.energy = 4.0; sl.angle = math.radians(.6); sl.color = (1, .96, .9)
    so = bpy.data.objects.new('sun', sl); sc.collection.objects.link(so)
    so.rotation_euler = (-sd).to_track_quat('-Z', 'Y').to_euler()

# light portals at the openings (guide sky sampling into the rooms)
def portal(c, nrm, wd, ht):
    l = bpy.data.lights.new('portal', 'AREA'); l.shape = 'RECTANGLE'; l.size = wd; l.size_y = ht
    try: l.cycles.is_portal = True
    except Exception: return
    o = bpy.data.objects.new('portal', l); sc.collection.objects.link(o)
    o.location = T2B(c); o.rotation_euler = T2B(nrm).to_track_quat('-Z', 'Z').to_euler()
for c, n, wd, ht in [((7.40, 1.15, 2.065), (-1, 0, 0), 2.71, 2.3), ((7.40, 1.15, 5.57), (-1, 0, 0), 2.7, 2.3), ((7.40, 1.65, 8.04), (-1, 0, 0), .74, 1.3),
                     ((-4.10, 1.575, -2.025), (1, 0, 0), .95, 1.25), ((.61, 1.575, -4.92), (0, 0, 1), .98, 1.25), ((-3.85, 1.5, 1.13), (1, 0, 0), .82, 1.0),
                     ((8.83, 1.55, -1.95), (-1, 0, 0), 1.0, 1.3), ((5.87, 1.85, -5.12), (0, 0, 1), .86, .7)]:
    if DAY: portal(c, n, wd, ht)

# camera
cd = bpy.data.cameras.new('cam'); co = bpy.data.objects.new('cam', cd); sc.collection.objects.link(co); sc.camera = co
pos, tgt = T2B(V['pos']), T2B(V['tgt'])
co.location = pos; co.rotation_euler = (tgt - pos).to_track_quat('-Z', 'Y').to_euler()
fov = math.radians(V.get('fov', 68)); cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24; cd.lens = 12 / math.tan(fov / 2); cd.clip_start = .03; cd.clip_end = 800
if os.environ.get('PANO'):   # equirectangular probe at POS (three.js coords): image centre = three +x, right = +z, as three's equirect mapping
    px, py, pz = [float(v) for v in os.environ['POS'].split(',')]; co.location = T2B({'x': px, 'y': py, 'z': pz}) if False else Vector((px, -pz, py))
    co.rotation_euler = (math.pi / 2, 0, -math.pi / 2); cd.type = 'PANO'
    try: cd.panorama_type = 'EQUIRECTANGULAR'
    except Exception: cd.cycles.panorama_type = 'EQUIRECTANGULAR'
    cd.clip_start = .05

r = sc.render; r.engine = 'CYCLES'; r.resolution_x = W; r.resolution_y = H; r.resolution_percentage = 100
cy = sc.cycles; cy.device = 'CPU'
if os.environ.get('GPU'):   # Apple silicon: Cycles on Metal
    prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type = 'METAL'; prefs.get_devices()
    for d in prefs.devices: d.use = d.type == 'METAL'
    cy.device = 'GPU'
cy.samples = spp; cy.use_adaptive_sampling = True; cy.adaptive_threshold = .02
cy.use_denoising = True
try: cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
except Exception as e: print('denoise opt', e)
cy.max_bounces = 10; cy.diffuse_bounces = 5; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.transparent_max_bounces = 24
cy.sample_clamp_indirect = 8; cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0
r.threads_mode = 'AUTO'
try:
    if os.environ.get('PANO'): raise RuntimeError('probe: linear (Standard view), no tone curve')
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    try: sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    except Exception: pass
sc.view_settings.exposure = expo
try:
    sc.view_settings.use_white_balance = True; sc.view_settings.white_balance_temperature = {'day': 6900, 'lit': 5600}.get(mode, 4800)
except Exception as e: print('wb', e)
r.image_settings.file_format = 'PNG'; r.filepath = out
t = time.time(); bpy.ops.render.render(write_still=True); print('render s', round(time.time() - t, 1))
