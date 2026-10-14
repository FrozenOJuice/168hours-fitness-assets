"""Refine the existing 0.1.0 barbell to 0.1.1; never rebuild or write plate.
Preserves shaft, profile dimensions, object/data identities and anchor frames.
Adds circular subdivisions only to existing sleeve/cap mesh datablocks.
"""
from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import *
import bmesh
TARGET_VERSION='0.1.1'
CAPACITY_SOURCE=FIXTURE/(SID+'__capacity.blend')
plan=read_json(ASSET/'refinement-plan.json')
verify_plate()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
root=bpy.data.objects[ID+'__root']
assert root['asset_version'] in ('0.1.0',TARGET_VERSION)
if root['asset_version']=='0.1.0':assert digest(SOURCE)==plan['predecessor_source_sha256']
identities={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
anchor_frames={o.name:[list(row) for row in o.matrix_world] for o in bpy.data.objects if '__anchor_' in o.name}
def coord_hash(data):return hashlib.sha256(json.dumps([list(v.co) for v in data.vertices],separators=(',',':')).encode()).hexdigest()
shaft=bpy.data.objects[ID+'__mesh_shaft'];shaft_hash=coord_hash(shaft.data)
old_counts={m.name:len(m.vertices) for m in bpy.data.meshes}
for key in ['sleeve_l','end_cap_l']:
    mesh=bpy.data.objects[ID+'__mesh_'+key].data
    if root['asset_version']=='0.1.0':
        bm=bmesh.new();bm.from_mesh(mesh)
        radius_layer=bm.verts.layers.float.new('refinement_radius')
        for v in bm.verts:v[radius_layer]=math.hypot(v.co.y,v.co.z)
        edges=[e for e in bm.edges if abs(e.verts[0].co.x-e.verts[1].co.x)<1e-7 and abs(e.verts[0][radius_layer]-e.verts[1][radius_layer])<1e-7 and e.verts[0][radius_layer]>1e-7]
        bmesh.ops.subdivide_edges(bm,edges=edges,cuts=2,use_grid_fill=True)
        for v in bm.verts:
            length=math.hypot(v.co.y,v.co.z)
            if length>1e-9:
                scale=v[radius_layer]/length;v.co.y*=scale;v.co.z*=scale
        bm.verts.layers.float.remove(radius_layer)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update()
# Keep existing slots 0..7, add smooth silver ramp variants at indices 8..135.
# Workbench flat rendering uses actual swatches, no reflections/lights/shadows.
def linear(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
ramp=[]
for i in range(128):
    name=ID+'__material_steel_soft_'+str(i).zfill(3)
    mat=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    v=.55+.30*i/127
    rgb=tuple(linear(min(1,v+d)) for d in (0,.018,.035))
    mat.diffuse_color=(*rgb,1);mat.use_nodes=True
    node=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value=(*rgb,1);node.inputs['Metallic'].default_value=.85;node.inputs['Roughness'].default_value=.48
    ramp.append(mat)
for mat in bpy.data.materials:
    if mat.use_nodes:
        next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Roughness'].default_value=.48
for mesh in bpy.data.meshes:
    if len(mesh.materials)==8:
        for mat in ramp:mesh.materials.append(mat)
    assert len(mesh.materials)==136
    for p in mesh.polygons:
        c=p.center;n=p.normal;theta=math.atan2(c.z,c.y)
        # Broad, low-contrast shoulder rather than a hard white stripe.
        angle=(theta-.40+math.pi)%(2*math.pi)-math.pi
        value=.62+.12*(math.sin(theta)+1)/2+.075*math.exp(-(angle/.65)**2)
        if mesh==shaft.data:
            x=abs(c.x)
            if .455<=x<=.460:p.material_index=7;continue
            if x<.060 or .210<x<.655:
                if n.x>.035:value-=.028
                elif n.x<-.035:value+=.028
        else:
            # Axial planes must be a uniform swatch: polar color bands caused
            # the old segmented disk/chamfer appearance despite dense rings.
            if abs(n.x)>.995:value=.745
            elif abs(n.x)>.2:value=.72+.045*(math.sin(theta)+1)/2
            p.use_smooth=abs(n.x)<.995
        p.material_index=8+max(0,min(127,round((value-.55)/.30*127)))
root['asset_version']=TARGET_VERSION
root['refined_from_sha256']=plan['predecessor_source_sha256']
root['surface_refinement']='existing circular edges subdivided 3x; broad soft steel values; no profile/anchor changes'
bpy.context.view_layer.update()
assert identities=={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
assert anchor_frames=={o.name:[list(row) for row in o.matrix_world] for o in bpy.data.objects if '__anchor_' in o.name}
assert shaft_hash==coord_hash(shaft.data)
scene=bpy.context.scene;viewport()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,check_existing=False)
source_hash=digest(SOURCE)
record={'version':TARGET_VERSION,'predecessor_source_sha256':plan['predecessor_source_sha256'],'source_sha256':source_hash,'refinement_script_sha256':digest(__file__),'all_object_and_data_identity_retained':True,'anchors_unchanged':True,'shaft_coordinates_unchanged':True,'shaft_coordinate_sha256':shaft_hash,'old_mesh_vertex_counts':old_counts,'new_mesh_vertex_counts':{m.name:len(m.vertices) for m in bpy.data.meshes},'profile_dimensions_unchanged':True,'new_ramp_slots':[8,135],'existing_slots_0_to_7_preserved':True,'roughness':.48}
write_json(ASSET/'refinement-record.json',record)
settings=read_json(ASSET/'previews/render-settings.json')
settings.update(preset='barbell_review_flat@0.1.1',asset_version=TARGET_VERSION,source_sha256=source_hash,refinement_script='scripts/blender/refine_olympic_barbell_20kg.py',refinement_script_sha256=digest(__file__),helpers_sha256=digest(Path(__file__).with_name('barbell_20kg_common.py')),roughness=.48,material_interpretation='128 appended soft-steel value swatches; broad restrained radial shading and subtle knurl facet contrast under Workbench FLAT; not physically lit reflections',smooth_ramp={'slots':[8,135],'srgb_low':[.55,.568,.585],'srgb_high':[.85,.868,.885],'quantization':128,'existing_semantic_slot_prefix_preserved':8})
settings['camera_views']=add_views(scene)
write_json(ASSET/'previews/render-settings.json',settings)
m=read_json(ASSET/'asset.json');m.update(version=TARGET_VERSION,status='review',source_revision_or_digest='sha256:'+source_hash)
m['standards'].update(style_preset=settings['preset'],style_preset_revision=digest(__file__))
m['material_slots']['smooth_ramp']={'indices':[8,135],'semantic_role':'equipment_frame','source':'previews/render-settings.json','count':128,'note':'append-only; original slots 0..7 unchanged'}
write_json(ASSET/'asset.json',m)
# Regenerate the existing single-plate assembly using unchanged frame helper.
scene,bar,plate=make_fixture()
base_views=add_views(scene,assembled=True)
viewport((0,0,.225),2.8)
scene.camera=bpy.data.objects[SID+'__camera_assembled_with_plates']
scene['asset_version']=TARGET_VERSION
bpy.ops.wm.save_as_mainfile(filepath=str(TEST_SOURCE),compress=True,check_existing=False)
fixture_hash=digest(TEST_SOURCE)
# Derive stack capacity from actual linked geometry and sleeve-end anchors.
measure=plate_measurements(plate)
load=local_anchor(bar,ID,'load_l').matrix_world.translation
end=local_anchor(bar,ID,'sleeve_end_l').matrix_world.translation
length=(end-load).length;pitch=measure['pitch_m'];gap=plan['interplate_gap_m']
collar=plan['collar_reserve_m'];end_margin=plan['end_margin_m'];flange=plan['flange_gap_m']
capacity=math.floor((length-collar-end_margin-flange+gap)/(pitch+gap))
assert capacity==plan['expected_capacity_each']
capacity_record={'version':TARGET_VERSION,'sleeve_length_m':length,'measured_plate_pitch_m':pitch,'manufacturer_plate_thickness_m':1.3*.0254,'collar_reserve_m':collar,'end_margin_m':end_margin,'flange_gap_m':flange,'interplate_gap_m':gap,'plates_per_sleeve':capacity,'stack_axial_length_m':capacity*pitch+(capacity-1)*gap,'used_with_all_reserves_m':flange+capacity*pitch+(capacity-1)*gap+collar+end_margin,'spare_after_reserves_m':length-(flange+capacity*pitch+(capacity-1)*gap+collar+end_margin),'next_plate_excess_m':flange+(capacity+1)*pitch+capacity*gap+collar+end_margin-length,'formula':'floor((sleeve-collar-end_margin-flange_gap+interplate_gap)/(measured_pitch+interplate_gap))','scope':'digital axial packing with sourced collar footprint and explicit allowances, not load rating','collars_modeled':False,'sources':plan['sources'],'sensitivity':[]}
for reserve in [.038,.050,.070]:
    for intergap in [0,.0005]:
        n=math.floor((length-reserve-end_margin-flange+intergap)/(pitch+intergap))
        capacity_record['sensitivity'].append({'collar_m':reserve,'interplate_gap_m':intergap,'count':n,'collar_status':'sourced length' if reserve==.05 else 'hypothetical sensitivity only'})
write_json(ASSET/'capacity-calculation.json',capacity_record)
# Extend a separate linked scene to the calculated full stack, no mesh copies.
for obj in list(bpy.data.objects):
    if obj.library is None and obj.type=='CAMERA':bpy.data.objects.remove(obj,do_unlink=True)
scene.name=SID+'__capacity';scene['configuration']='10 linked 45lb plates per sleeve; collar space reserved, collars not modeled'
barinst=bpy.data.objects['barbell_primary']
for side in ['l','r']:
    for index in range(capacity):
        obj=bpy.data.objects['plate_'+side] if index==0 else instance(scene,plate,'plate_'+side+'_'+str(index+1).zfill(2))
        place_plate(scene,barinst,bar,plate,side,index=index,instance_obj=obj)
        outward=(barinst.matrix_world@local_anchor(bar,ID,'load_'+side).matrix_world).to_3x3()@Vector((0,1,0))
        obj.location+=outward*(index*gap);obj['stack_index']=index;obj['side']=side
bpy.context.view_layer.update()
entries={'loaded_side':((0,3,.225),(0,0,.225),2.50),'loaded_three_quarter':((2.7,3.6,1.8),(0,0,.225),2.50),'loaded_sleeve_detail':((1.38,.65,.55),(.89,0,.225),.68)}
capacity_views={}
for view,(pos,target,scale) in entries.items():
    cam=camera(scene,SID+'__camera_'+view,pos,target,scale)
    path=FIXTURE/'previews'/f'{SID}__{view}__10_per_sleeve.png'
    entry=camera_config(cam,path,target,'10_45lb_plates_per_sleeve')
    entry['source']=str(CAPACITY_SOURCE.relative_to(REPO));entry['plates_per_sleeve']=capacity
    capacity_views[view]=entry
scene.camera=bpy.data.objects[SID+'__camera_loaded_side'];viewport((0,0,.225),2.8)
bpy.ops.wm.save_as_mainfile(filepath=str(CAPACITY_SOURCE),compress=True,check_existing=False)
capacity_hash=digest(CAPACITY_SOURCE)
# Render every assembly view from its own saved file, preserving base scene.
for path,views in [(TEST_SOURCE,base_views),(CAPACITY_SOURCE,capacity_views)]:
    bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
    for view,entry in views.items():
        cam=camera(scene,'refinement_reference',entry['position_m'],entry['target_m'],entry['ortho_scale_m'])
        cam.rotation_euler=entry['rotation_euler_xyz_radians'];cam.data.clip_start=entry['clip_start_m'];cam.data.clip_end=entry['clip_end_m']
        scene.camera=cam;scene.render.filepath=str(REPO/entry['path']);bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(cam,do_unlink=True)
fs=dict(settings);fs.update(source_sha256=fixture_hash,camera_views={**base_views,**capacity_views},secondary_sources=[{'path':str(CAPACITY_SOURCE.relative_to(REPO)),'sha256':capacity_hash}],dependencies=[{'path':str(SOURCE.relative_to(REPO)),'sha256':source_hash},{'path':str((PLATE/(PID+'.blend')).relative_to(REPO)),'sha256':verify_plate()['source']['sha256']}])
write_json(FIXTURE/'previews/render-settings.json',fs)
fm=read_json(FIXTURE/'asset.json');fm.update(version=TARGET_VERSION,source_revision_or_digest='sha256:'+fixture_hash,secondary_sources=[{'path':str(CAPACITY_SOURCE.relative_to(REPO)),'sha256':capacity_hash,'configuration':'10_45lb_plates_per_sleeve','plate_instances':20}],capacity_calculation=str((ASSET/'capacity-calculation.json').relative_to(REPO)))
fm['dependencies'][0].update(version=TARGET_VERSION,sha256=source_hash);fm['reference_renders']=list(fs['camera_views'].values());write_json(FIXTURE/'asset.json',fm)
m=read_json(ASSET/'asset.json');m['capacity_calculation']=str((ASSET/'capacity-calculation.json').relative_to(REPO));m['reference_renders']=[]
for views,sha in [(settings['camera_views'],source_hash),(base_views,fixture_hash),(capacity_views,capacity_hash)]:
    for view,entry in views.items():m['reference_renders'].append({'view':view,'configuration':entry['configuration'],'path':entry['path'],'source_revision_or_digest':'sha256:'+sha,'preset_revision':digest(__file__),'sha256':digest(REPO/entry['path'])})
write_json(ASSET/'asset.json',m)
verify_plate();print('BARBELL_REFINEMENT_COMPLETE',source_hash,fixture_hash,capacity_hash,capacity_record)
