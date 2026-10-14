"""Appearance-only barbell 0.1.2 and five-per-sleeve linked example.
Manufacturer findings are written first. Never edits dimensions or plate.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import *
TARGET='0.1.2'
CAP_SOURCE=FIXTURE/(SID+'__capacity.blend')
EXAMPLE_SOURCE=FIXTURE/(SID+'__example.blend')
plan=read_json(ASSET/'contrast-example-plan.json')
assert digest(ASSET/plan['findings'])==plan['findings_sha256']
verify_plate()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
root=bpy.data.objects[ID+'__root'];before_version=root['asset_version']
assert before_version in ('0.1.1',TARGET)
if before_version=='0.1.1':assert digest(SOURCE)==plan['predecessor_sha256']
def geometry_hashes():
    return {mesh.name:hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in mesh.vertices],'faces':[list(p.vertices) for p in mesh.polygons],'material_indices':[p.material_index for p in mesh.polygons]},separators=(',',':')).encode()).hexdigest() for mesh in bpy.data.meshes}
before=geometry_hashes();frames={o.name:[list(row) for row in o.matrix_world] for o in bpy.data.objects}
identities={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
def srgb(x):return x*12.92 if x<=.0031308 else 1.055*x**(1/2.4)-.055
def linear(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
colors={}
for mat in bpy.data.materials:
    if '__material_steel_soft_' not in mat.name:continue
    old=tuple(srgb(float(x)) for x in mat.diffuse_color[:3])
    new=tuple(max(0,min(1,.72+1.18*(x-.72))) for x in old) if before_version=='0.1.1' else old
    rgb=tuple(linear(x) for x in new);mat.diffuse_color=(*rgb,1)
    node=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value=(*rgb,1)
    colors[mat.name]={'before_srgb':old,'after_srgb':new}
root['asset_version']=TARGET;root['appearance_update']='18 percent soft-steel swatch contrast increase around sRGB .72; no geometry change'
assert before==geometry_hashes()
assert frames=={o.name:[list(row) for row in o.matrix_world] for o in bpy.data.objects}
assert identities=={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,check_existing=False)
source_hash=digest(SOURCE)
write_json(ASSET/'contrast-record.json',{'version':TARGET,'predecessor_sha256':plan['predecessor_sha256'],'source_sha256':source_hash,'script_sha256':digest(__file__),'findings_sha256':plan['findings_sha256'],'dimension_changes':False,'all_mesh_coordinates_topology_face_slots_preserved':True,'all_object_transforms_and_anchors_preserved':True,'all_object_data_identity_retained':True,'mesh_geometry_sha256':before,'colors':colors,'contrast_factor':1.18,'pivot_srgb':.72,'material_slots_unchanged':True})
settings=read_json(ASSET/'previews/render-settings.json');settings.update(source_sha256=source_hash,asset_version=TARGET,preset='barbell_review_flat@0.1.2',contrast_script='scripts/blender/contrast_olympic_barbell_20kg.py',contrast_script_sha256=digest(__file__),material_interpretation='Existing soft-steel swatches contrast transformed by .72+1.18*(value-.72); broad smooth shading preserved; Workbench unlit, no reflections/shadows/AO',contrast_factor=1.18,contrast_pivot_srgb=.72)
settings['smooth_ramp'].update(srgb_low=[.5194,.54064,.5607],srgb_high=[.8734,.89464,.9147],contrast_transform='.72+1.18*(previous_srgb-.72)')
settings['camera_views']=add_views(bpy.context.scene)
write_json(ASSET/'previews/render-settings.json',settings)
# Refresh saved linked scene metadata/cache; transforms and instances preserved.
old_fs=read_json(FIXTURE/'previews/render-settings.json')
for path in [TEST_SOURCE,CAP_SOURCE]:
    bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.scene['asset_version']=TARGET
    bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True,check_existing=False)
fixture_hash=digest(TEST_SOURCE);cap_hash=digest(CAP_SOURCE)
# The example uses the existing ten-plate scene's first five instances.
bpy.ops.wm.open_mainfile(filepath=str(CAP_SOURCE));scene=bpy.context.scene
scene.name=SID+'__example';scene['configuration']='5 linked original 45lb plates per sleeve; illustrative partial load, not capacity limit'
for obj in list(scene.objects):
    if obj.library is None and (obj.type=='CAMERA' or (obj.instance_type=='COLLECTION' and obj.get('stack_index',-1)>=5)):
        bpy.data.objects.remove(obj,do_unlink=True)
views={}
entries={'example_side':((0,3,.225),(0,0,.225),2.50),'example_three_quarter':((2.7,3.6,1.8),(0,0,.225),2.50),'example_sleeve_detail':((1.38,.65,.55),(.89,0,.225),.68)}
for name,(pos,target,scale) in entries.items():
    cam=camera(scene,SID+'__camera_'+name,pos,target,scale)
    path=FIXTURE/'previews'/f'{SID}__{name}__5_per_sleeve.png'
    entry=camera_config(cam,path,target,'5_45lb_plates_per_sleeve')
    entry.update(source=str(EXAMPLE_SOURCE.relative_to(REPO)),plates_per_sleeve=5)
    views[name]=entry
scene.camera=bpy.data.objects[SID+'__camera_example_three_quarter'];viewport((0,0,.225),2.8)
bpy.ops.wm.save_as_mainfile(filepath=str(EXAMPLE_SOURCE),compress=True,check_existing=False)
example_hash=digest(EXAMPLE_SOURCE)
fs=dict(settings);fs.update(source_sha256=fixture_hash,camera_views={**old_fs['camera_views'],**views},secondary_sources=[{'path':str(CAP_SOURCE.relative_to(REPO)),'sha256':cap_hash,'configuration':'10_45lb_plates_per_sleeve','role':'diagnostic_maximum'},{'path':str(EXAMPLE_SOURCE.relative_to(REPO)),'sha256':example_hash,'configuration':'5_45lb_plates_per_sleeve','role':'requested_example'}],dependencies=[{'path':str(SOURCE.relative_to(REPO)),'sha256':source_hash},{'path':str((PLATE/(PID+'.blend')).relative_to(REPO)),'sha256':verify_plate()['source']['sha256']}])
for name,entry in fs['camera_views'].items():
    path=REPO/entry.get('source',str(TEST_SOURCE.relative_to(REPO)))
    bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    cam=camera(scene,'current_reference',entry['position_m'],entry['target_m'],entry['ortho_scale_m'])
    cam.rotation_euler=entry['rotation_euler_xyz_radians'];cam.data.clip_start=entry['clip_start_m'];cam.data.clip_end=entry['clip_end_m'];scene.camera=cam
    scene.render.filepath=str(REPO/entry['path']);bpy.ops.render.render(write_still=True)
write_json(FIXTURE/'previews/render-settings.json',fs)
m=read_json(ASSET/'asset.json');m.update(version=TARGET,source_revision_or_digest='sha256:'+source_hash)
m['standards'].update(style_preset=settings['preset'],style_preset_revision=digest(__file__))
m['reference_renders']=[]
for groups in [settings['camera_views'],fs['camera_views']]:
    for name,entry in groups.items():
        path=entry.get('source')
        sha=digest(REPO/path) if path else (source_hash if groups==settings['camera_views'] else fixture_hash)
        m['reference_renders'].append({'view':name,'configuration':entry['configuration'],'path':entry['path'],'source_revision_or_digest':'sha256:'+sha,'preset_revision':digest(__file__),'sha256':digest(REPO/entry['path'])})
write_json(ASSET/'asset.json',m)
fm=read_json(FIXTURE/'asset.json');fm.update(version=TARGET,source_revision_or_digest='sha256:'+fixture_hash,secondary_sources=fs['secondary_sources'],reference_renders=list(fs['camera_views'].values()),preferred_example_source=str(EXAMPLE_SOURCE.relative_to(REPO)))
fm['dependencies'][0].update(version=TARGET,sha256=source_hash)
for entry in fm['reference_renders']:entry['sha256']=digest(REPO/entry['path'])
write_json(FIXTURE/'asset.json',fm)
verify_plate();print('CONTRAST_EXAMPLE_COMPLETE',source_hash,fixture_hash,cap_hash,example_hash)
