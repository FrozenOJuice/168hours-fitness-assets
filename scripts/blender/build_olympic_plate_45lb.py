"""Rebuild the A09-approved review plate and its local reference evidence.
Run with Blender 5.1.1 --background --factory-startup --python this_file.
No third-party geometry, fonts, add-ons, textures, barbell, or exercise scene.
"""
from pathlib import Path
import bpy
import bmesh
import hashlib
import json
import math
from mathutils import Matrix, Vector

REPO = Path(__file__).resolve().parents[2]
ID = '168h_equipment_olympic_plate_45lb_cast_iron'
ASSET = REPO / 'assets/equipment/free_weights' / ID
PREVIEWS = ASSET / 'previews'
SOURCE = ASSET / f'{ID}.blend'
RADIUS = 0.225
BORE_RADIUS = 0.0254
HALF_PITCH = 0.01651
SEGMENTS = 256
# Circumscribe the bore polygon so its minimum across-flats clearance is 50.8 mm.
BORE_VERTEX_RADIUS = BORE_RADIUS / math.cos(math.pi / SEGMENTS)
PRESET = 'plate_review_flat@0.1.0'

# The authorization is recorded in the specification and A09; do not promote
# these asset-local review choices to shared production standards.
ASSET.mkdir(parents=True, exist_ok=True)
PREVIEWS.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = ID + '__source'
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.unit_settings.length_unit = 'METERS'
scene.render.fps = 24
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.film_transparent = False
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.render_aa = '32'
shade = scene.display.shading
shade.light = 'FLAT'
shade.color_type = 'MATERIAL'
shade.show_shadows = False
shade.show_cavity = False
shade.show_specular_highlight = False
shade.show_object_outline = True
shade.object_outline_color = (0.015, 0.018, 0.022)
shade.background_type = 'WORLD'
scene.world = bpy.data.worlds.new(ID + '__world_reference')
scene.world.color = (1, 1, 1)
# Runtime-supported display transforms are dynamic; assignment is validated.
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1

asset = bpy.data.collections.new(ID)
scene.collection.children.link(asset)
geo = bpy.data.collections.new(ID + '__geo')
anchors = bpy.data.collections.new(ID + '__anchors')
asset.children.link(geo)
asset.children.link(anchors)
root = bpy.data.objects.new(ID + '__root', None)
asset.objects.link(root)
root.empty_display_type = 'PLAIN_AXES'
root.empty_display_size = .035
root['asset_id'] = ID
root['asset_version'] = '0.1.0'
root['interface'] = 'olympic_plate_bore@0.1.0'
root['nominal_weight_lb'] = 45.0
root['bore_diameter_m'] = BORE_RADIUS * 2
root['stack_pitch_m'] = HALF_PITCH * 2
asset.asset_mark()
asset.asset_data.description = 'Brand-neutral traditional cast iron 45 LB Olympic plate. Review prototype; exact 2 inch bore. See SPEC.md and asset.json.'
for tag in ['168Hours Fitness', 'equipment', 'free_weights', 'olympic_plate', '45_lb', 'review_prototype']:
    asset.asset_data.tags.new(tag)


def linear(v):
    return v / 12.92 if v <= .04045 else ((v+.055)/1.055)**2.4


def material(role, hex_color):
    rgb = tuple(linear(int(hex_color[i:i+2], 16)/255) for i in (0, 2, 4))
    mat = bpy.data.materials.new(ID + '__material_' + role)
    mat.diffuse_color = (*rgb, 1)
    mat.use_nodes = True
    node = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value = (*rgb, 1)
    node.inputs['Metallic'].default_value = 0
    node.inputs['Roughness'].default_value = 1
    return mat

palette_hex = {'cast_iron': '363A40', 'web': '454A51', 'rim': '2A2D32', 'hub': '50555C', 'lettering': '9CA1A8'}
mats = {key: material(key, value) for key, value in palette_hex.items()}
# A closed radial cross-section. The straight bore stays at exactly 25.4 mm
# radius; entrance chamfers open outward and never reduce the minimum bore.
back = [
    (BORE_VERTEX_RADIUS, -.01451), (.0274, -HALF_PITCH),
    (.057, -HALF_PITCH), (.061, -.01451), (.065, -.0105),
    (.191, -.0105), (.195, -.01451), (.199, -HALF_PITCH),
    (.223, -HALF_PITCH), (RADIUS, -.01451),
]
profile = back + [(r, -y) for r, y in reversed(back)]
verts = [(r*math.cos(2*math.pi*j/SEGMENTS), y,
          RADIUS+r*math.sin(2*math.pi*j/SEGMENTS))
         for r, y in profile for j in range(SEGMENTS)]
faces = []
for k in range(len(profile)):
    following = (k+1) % len(profile)
    for j in range(SEGMENTS):
        nj = (j+1) % SEGMENTS
        faces.append((k*SEGMENTS+j, k*SEGMENTS+nj,
                      following*SEGMENTS+nj, following*SEGMENTS+j))
mesh = bpy.data.meshes.new(ID + '__mesh_body_data')
mesh.from_pydata(verts, [], faces)
mesh.update()
bm = bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
bm.to_mesh(mesh)
bm.free()
body = bpy.data.objects.new(ID + '__mesh_body', mesh)
geo.objects.link(body)
body.parent = root
for key in ['cast_iron', 'web', 'rim', 'hub']:
    mesh.materials.append(mats[key])
for polygon in mesh.polygons:
    radial = sum(math.hypot(mesh.vertices[i].co.x, mesh.vertices[i].co.z-RADIUS)
                 for i in polygon.vertices) / len(polygon.vertices)
    radial = round(radial, 6)  # stable bands; avoid float-dependent alternating wedges
    polygon.material_index = 3 if radial < .065 else (1 if radial < .193 else 2)
    if abs(polygon.normal.y) < .2:
        polygon.material_index = 0
    # Smooth circular surfaces without inventing extra geometric detail.
    polygon.use_smooth = abs(polygon.normal.y) < .2

for facing in ['front', 'back']:
    font = bpy.data.curves.new(ID + '__font_temporary_' + facing, 'FONT')
    font.body = '45 LB'
    font.align_x = 'CENTER'
    font.align_y = 'CENTER'
    font.size = .055
    font.extrude = .00075  # symmetric extrusion; total relief 1.5 mm
    font.bevel_depth = .00015
    font.bevel_resolution = 2
    font.resolution_u = 8
    obj = bpy.data.objects.new(ID + '__mesh_label_' + facing, font)
    geo.objects.link(obj)
    font.materials.append(mats['lettering'])
    # Front camera on +Y sees screen-right = -X. Local text +Y is world +Z.
    basis = Matrix(((-1, 0, 0), (0, 0, 1), (0, 1, 0))) if facing == 'front' else Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0)))
    obj.matrix_world = basis.to_4x4()
    obj.location = (0, .0111 if facing == 'front' else -.0111, RADIUS + .105)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj = bpy.context.object
    transform = obj.matrix_world.copy()
    obj.data.transform(transform)
    obj.matrix_world = Matrix.Identity(4)
    obj.parent = root
    obj['raised_text'] = '45 LB'
    obj['source_font'] = 'Blender built-in Bfont, converted to mesh; no external font file'
    obj.select_set(False)
for data in list(bpy.data.curves):
    if data.users == 0:
        bpy.data.curves.remove(data)

anchor_positions = {
    'bore_center': (0, 0, RADIUS),
    'stack_front': (0, HALF_PITCH, RADIUS),
    'stack_back': (0, -HALF_PITCH, RADIUS),
    'floor_contact': (0, 0, 0),
}
for key, position in anchor_positions.items():
    obj = bpy.data.objects.new(ID + '__anchor_' + key, None)
    anchors.objects.link(obj)
    obj.parent = root
    obj.location = position
    obj.empty_display_type = 'ARROWS'
    obj.empty_display_size = .025
    obj['logical_anchor'] = key
    obj['frame'] = '+Y forward/axial; +Z up'

# Frame the saved source for a useful first-open view without a render camera.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.region_3d.view_perspective = 'ORTHO'
            space.region_3d.view_location = (0, 0, RADIUS)
            space.region_3d.view_distance = .75
            space.region_3d.view_rotation = Vector((0, -1, 0)).to_track_quat('-Z', 'Y')
            space.shading.type = 'SOLID'
            space.shading.light = 'FLAT'
            space.shading.color_type = 'MATERIAL'
            space.shading.show_shadows = False
            space.shading.show_cavity = False
            space.shading.show_specular_highlight = False
            space.shading.show_object_outline = True
            space.shading.object_outline_color = shade.object_outline_color
            space.shading.background_type = 'VIEWPORT'
            space.shading.background_color = (1, 1, 1)
            space.overlay.show_overlays = False
# Save only the reusable source, before creating any cameras or review fixtures.
bpy.context.view_layer.objects.active = root
root.select_set(True)
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE), check_existing=False)
source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()

# Transient reference setup. It is not saved into the reusable source.
references = bpy.data.collections.new(ID + '__reference_setup_transient')
scene.collection.children.link(references)
camera_data = bpy.data.cameras.new(ID + '__camera_reference')
camera = bpy.data.objects.new(ID + '__camera_reference', camera_data)
references.objects.link(camera)
camera.data.type = 'ORTHO'
camera.data.ortho_scale = .56
scene.camera = camera
center = Vector((0, 0, RADIUS))
views = {'front': (0, 1.2, 0), 'side': (1.2, 0, 0),
         'three_quarter': (.82, 1.05, .45), 'back': (0, -1.2, 0)}
settings = {
    'status': 'asset-local review preset; not approved globally', 'preset': PRESET,
    'blender_version': bpy.app.version_string, 'blender_build_hash': bpy.app.build_hash.decode(),
    'addons_required': [], 'engine': scene.render.engine,
    'source_sha256': source_hash,
    'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'resolution': [1024, 1024], 'format': 'PNG', 'color_mode': 'RGBA', 'bit_depth': 8,
    'view_transform': scene.view_settings.view_transform, 'look': scene.view_settings.look,
    'exposure': 0, 'gamma': 1, 'palette_srgb_hex': palette_hex,
    'material_versions': {m.name: '0.1.0' for m in mats.values()},
    'lighting': 'FLAT; no light objects', 'shadows': False, 'cavity': False,
    'ambient_occlusion': False, 'baked_textures': [], 'specular_highlight': False,
    'outlines': {'method': 'Workbench object silhouette outline', 'enabled': True,
                 'width': 'Workbench native width at 1024px; no exposed pixel-width control',
                 'color_linear_rgb': list(shade.object_outline_color)},
    'background': {'world_linear_rgb': [1, 1, 1], 'transparent': False},
    'antialiasing_samples': scene.display.render_aa, 'random_seed': 'N/A deterministic Workbench',
    'frame': 1, 'configuration': 'standing', 'camera_views': {},
}
scene.frame_set(1)
for view, offset in views.items():
    camera.location = center + Vector(offset)
    camera.rotation_euler = (center-camera.location).to_track_quat('-Z', 'Y').to_euler()
    path = PREVIEWS / f'{ID}__{view}__standing.png'
    scene.render.filepath = str(path)
    settings['camera_views'][view] = {
        'path': str(path.relative_to(REPO)), 'position_m': list(camera.location),
        'rotation_euler_xyz_radians': list(camera.rotation_euler),
        'projection': 'ORTHO', 'ortho_scale_m': .56,
        'target_m': list(center), 'clip_start_m': camera.data.clip_start,
        'clip_end_m': camera.data.clip_end,
    }
    bpy.ops.render.render(write_still=True)
(PREVIEWS/'render-settings.json').write_text(json.dumps(settings, indent=2)+'\n')
print('PLATE_BUILD_COMPLETE', str(SOURCE), source_hash)
