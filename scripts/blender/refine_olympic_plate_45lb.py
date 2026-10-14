"""Refine the existing 0.1.0 plate mesh in place to review revision 0.1.1.
Does not run the original builder, delete geometry, or create replacement meshes.
Default input is the current source; --input supports replay from the archived
0.1.0 predecessor. A 0.1.1 input rerenders without applying edits twice.
"""
from pathlib import Path
import bpy
import hashlib
import json
import math
import sys
from mathutils import Vector

REPO=Path(__file__).resolve().parents[2]
ID='168h_equipment_olympic_plate_45lb_cast_iron'
ASSET=REPO/'assets/equipment/free_weights'/ID
SOURCE=ASSET/f'{ID}.blend'
VERSION='0.1.1'
PREDECESSOR_SHA256='ed507082be38912aee5a17623e077c524d6c95ea961d7b852c08a1823493cb74'
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
INPUT=Path(args[args.index('--input')+1]).resolve() if '--input' in args else SOURCE
settings=json.loads((ASSET/'previews/render-settings.json').read_text())
input_digest=hashlib.sha256(INPUT.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(INPUT))
scene=bpy.context.scene
root=bpy.data.objects[ID+'__root']
body=bpy.data.objects[ID+'__mesh_body']
mesh=body.data
assert len(mesh.vertices)==5120 and len(mesh.polygons)==5120
assert len(bpy.data.objects)==8 and len(bpy.data.meshes)==3


def topology_digest(data):
    return hashlib.sha256(json.dumps({'edges':[list(e.vertices) for e in data.edges],
       'polygons':[list(p.vertices) for p in data.polygons]},separators=(',',':')).encode()).hexdigest()


def coordinates_digest(data):
    return hashlib.sha256(json.dumps([list(v.co) for v in data.vertices],separators=(',',':')).encode()).hexdigest()


existing_pointers={o.name:{'object':o.as_pointer(),'data':o.data.as_pointer() if o.data else None}
                   for o in bpy.data.objects}
existing_topology={m.name:topology_digest(m) for m in bpy.data.meshes}
original_positions={o.name:list(o.location) for o in bpy.data.objects if 'anchor_' in o.name}
original_material_slots={o.name:[m.name for m in o.data.materials] for o in bpy.data.objects if o.type=='MESH'}
old_coordinates={m.name:coordinates_digest(m) for m in bpy.data.meshes}
R=.225
segments=256
bore_vertex_radius=.0254/math.cos(math.pi/segments)
# Keep every original radial ring/vertex/face. Only edit ring coordinates.
back=[(bore_vertex_radius,-.012),(.0274,-.0145),(.052,-.0145),
      (.056,-.012),(.061,-.0065),(.197,-.0065),
      (.202,-.0138),(.204,-.01651),(.223,-.01651),(.225,-.01451)]
profile=back+[(radius,-y) for radius,y in reversed(back)]
previous_version=root.get('asset_version')
if previous_version=='0.1.0':
    assert input_digest==PREDECESSOR_SHA256, 'Unexpected predecessor source; inspect before editing.'
    for k,(radius,y) in enumerate(profile):
        for j in range(segments):
            angle=2*math.pi*j/segments
            mesh.vertices[k*segments+j].co=(radius*math.cos(angle),y,R+radius*math.sin(angle))
    mesh.update()
    # Stable existing slot order: cast_iron, web, rim, hub. The darker bands
    # belong to actual structural shoulders/chamfers, not fake shadow textures.
    segment_materials=[0,3,0,2,1,2,0,0,3,2,3,0,0,2,1,2,0,3,0,2]
    for polygon in mesh.polygons:
        station=polygon.index//segments
        polygon.material_index=segment_materials[station]
        polygon.use_smooth=station in (9,19)
    for facing,sign in [('front',1),('back',-1)]:
        label=bpy.data.objects[ID+'__mesh_label_'+facing]
        assert label.type=='MESH' and label.get('raised_text')=='45 LB'
        data=label.data
        axial=[sign*v.co.y for v in data.vertices]
        low,high=min(axial),max(axial)
        # Preserve existing text topology. 0.3 mm intersection with web,
        # 3.5 mm exposed relief above the new +6.5 mm web face.
        for vertex in data.vertices:
            fraction=(sign*vertex.co.y-low)/(high-low)
            vertex.co.y=sign*(.0062+fraction*.0038)
            vertex.co.x*=1.06
            vertex.co.z=.330+(vertex.co.z-.330)*1.06
        if bpy.data.materials[ID+'__material_cast_iron'] not in list(data.materials):
            data.materials.append(bpy.data.materials[ID+'__material_cast_iron'])
        data.update()
        for polygon in data.polygons:
            polygon.material_index=0 if sign*polygon.normal.y>.8 else 1
        label['exposed_relief_m']=.0035
    root['asset_version']=VERSION
    root['web_thickness_m']=.013
    root['hub_thickness_m']=.029
    root['rim_recess_depth_m']=.01001
    root['refined_from_sha256']=PREDECESSOR_SHA256
elif previous_version==VERSION:
    assert root.get('refined_from_sha256')==PREDECESSOR_SHA256
else:
    raise RuntimeError('Unsupported input asset version: '+str(previous_version))

bpy.context.view_layer.update()
assert existing_pointers=={o.name:{'object':o.as_pointer(),'data':o.data.as_pointer() if o.data else None} for o in bpy.data.objects}, 'Object or data identity changed'
assert existing_topology=={m.name:topology_digest(m) for m in bpy.data.meshes}, 'Mesh topology was rebuilt'
assert original_positions=={o.name:list(o.location) for o in bpy.data.objects if 'anchor_' in o.name}
for name,slots in original_material_slots.items():
    actual=[m.name for m in bpy.data.objects[name].data.materials]
    assert actual[:len(slots)]==slots, 'Existing material slot reordered'
# Restore the exact recorded local render setup; never introduce lights/AO.
shade=scene.display.shading
assert scene.render.engine=='BLENDER_WORKBENCH' and shade.light=='FLAT'
assert not shade.show_cavity and not shade.show_shadows and not bpy.data.lights
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),check_existing=False)
source_digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
record={
 'version':VERSION,'predecessor_version':'0.1.0','predecessor_sha256':PREDECESSOR_SHA256,
 'input_sha256':input_digest,'source_sha256':source_digest,
 'operation':'existing mesh vertex edits and material assignments; no geometry reconstruction',
 'object_and_mesh_datablock_identity_preserved':True,'topology_preserved':True,
 'mesh_topology_sha256':existing_topology,'previous_coordinate_sha256':old_coordinates,
 'current_coordinate_sha256':{m.name:coordinates_digest(m) for m in bpy.data.meshes},
 'anchors_unchanged':True,'prior_material_slot_prefixes_unchanged':True,
 'axial_radial_profile_m':profile,'web_thickness_m':.013,'hub_thickness_m':.029,
 'rim_depth_above_web_m':.01001,'letter_exposed_relief_m':.0035,
 'letter_planar_scale_relative_to_0_1_0':1.06,
 'refinement_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'shared_standards_changed':False,
}
(ASSET/'refinement-record.json').write_text(json.dumps(record,indent=2)+'\n')
settings['source_sha256']=source_digest
settings['asset_version']=VERSION
settings['preset']='plate_review_flat@0.1.1'
settings['refinement_script']='scripts/blender/refine_olympic_plate_45lb.py'
settings['refinement_script_sha256']=record['refinement_script_sha256']
settings['predecessor_sha256']=PREDECESSOR_SHA256
settings['material_versions']={key:VERSION for key in settings['material_versions']}
settings['outlines']['edge_definition']='Existing native silhouette outlines plus dark flat materials on actual rim/hub shoulder surfaces and extruded letter sides; no AO or screen-width outline geometry.'
# Review cameras remain transient and the source is not saved again.
camdata=bpy.data.cameras.new(ID+'__camera_reference')
cam=bpy.data.objects.new(ID+'__camera_reference',camdata)
scene.collection.objects.link(cam)
scene.camera=cam
cam.data.type='ORTHO'
scene.frame_set(1)
for view,config in settings['camera_views'].items():
    cam.location=config['position_m']
    cam.rotation_euler=config['rotation_euler_xyz_radians']
    cam.data.ortho_scale=config['ortho_scale_m']
    scene.render.filepath=str(REPO/config['path'])
    bpy.ops.render.render(write_still=True)
(ASSET/'previews/render-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
print('PLATE_IN_PLACE_REFINEMENT_COMPLETE',source_digest)
