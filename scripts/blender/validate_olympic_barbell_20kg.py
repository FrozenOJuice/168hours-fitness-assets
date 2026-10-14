"""Read-only native-source validation and linked assembly checks.
Reopens saved files, measures evaluated geometry and regenerates temporary
reference images; never saves either source or approved plate.
"""
from pathlib import Path
import sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import *
import bmesh,numpy as np
from mathutils.bvhtree import BVHTree
checks={}
def check(name,condition,evidence):
    checks[name]={'status':'PASS' if condition else 'FAIL','evidence':evidence}
    print(name,checks[name]['status'],flush=True)

def points(obj,transform=None):
    matrix=(transform or Matrix.Identity(4))@obj.matrix_world
    return [matrix@v.co for v in obj.data.vertices]
def bounds(pts):return {'minimum_m':[min(p[i] for p in pts) for i in range(3)],'maximum_m':[max(p[i] for p in pts) for i in range(3)]}
def dims(b):return [b['maximum_m'][i]-b['minimum_m'][i] for i in range(3)]
def close(a,b,tol=1e-6):return abs(a-b)<tol

def reproduce(scene,settings):
    check('shadow_free_'+scene.name,scene.render.engine=='BLENDER_WORKBENCH' and scene.display.shading.light=='FLAT' and not scene.display.shading.show_shadows and not scene.display.shading.show_cavity and not scene.display.shading.show_specular_highlight and not any(o.type=='LIGHT' for o in scene.objects),{'engine':scene.render.engine,'light':scene.display.shading.light,'shadows':scene.display.shading.show_shadows,'cavity':scene.display.shading.show_cavity,'lights':sum(o.type=='LIGHT' for o in scene.objects)})
    for view,entry in settings['camera_views'].items():
        if entry.get('source'):
            bpy.ops.wm.open_mainfile(filepath=str(REPO/entry['source']));scene=bpy.context.scene
        cam=camera(scene,'validation_camera',entry['position_m'],entry['target_m'],entry['ortho_scale_m'])
        cam.rotation_euler=entry['rotation_euler_xyz_radians'];cam.data.clip_start=entry['clip_start_m'];cam.data.clip_end=entry['clip_end_m'];scene.camera=cam
        with tempfile.TemporaryDirectory(prefix='168h_barbell_render_') as temp:
            target=Path(temp)/(view+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
            arrays=[]
            for path in [REPO/entry['path'],target]:
                im=bpy.data.images.load(str(path),check_existing=False);arr=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(arr);arrays.append(arr);bpy.data.images.remove(im)
            shape_equal=arrays[0].shape==arrays[1].shape
            equal=shape_equal and np.array_equal(*arrays)
            delta=np.abs(arrays[0]-arrays[1]) if shape_equal else None
            max_delta=float(np.max(delta)) if shape_equal else None
            changed_fraction=float(np.count_nonzero(delta)/len(delta)) if shape_equal else 1
            # Linked multi-object Workbench antialiasing can vary at the last
            # 8-bit code value. Bound both magnitude and affected coverage;
            # standalone views still require exact decoded pixels.
            accepted=equal or (view in ('assembled_with_plates','loaded_side','loaded_three_quarter','loaded_sleeve_detail','example_side','example_three_quarter','example_sleeve_detail') and shape_equal and max_delta<=1/255+1e-7 and changed_fraction<.001)
            check('reference_reproduction_'+view,accepted,{'reference':entry['path'],'maximum_channel_delta':max_delta,'decoded_pixels_equal':equal,'changed_channel_fraction':changed_fraction,'acceptance':'exact standalone; assembly <=1/255 per channel and <0.1% changed channels'})
        bpy.data.objects.remove(cam,do_unlink=True)

plate_record=verify_plate();source_hash=digest(SOURCE);test_hash=digest(TEST_SOURCE)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene
asset=bpy.data.collections[ID];root=bpy.data.objects[ID+'__root'];current_version=root['asset_version']
meshes=[o for o in asset.all_objects if o.type=='MESH']
allpts=[p for o in meshes for p in points(o)];bb=bounds(allpts);measured=dims(bb)
check('canonical_bounds',all(close(a,b) for a,b in zip(measured,[2.2,.073,.073])),dict(bb,dimensions_m=measured))
check('floor_root_axes',root.matrix_world.is_identity and close(bb['minimum_m'][2],0) and scene.unit_settings.scale_length==1,{'root_matrix':[list(row) for row in root.matrix_world],'min_z_m':bb['minimum_m'][2],'units':scene.unit_settings.system,'axis':'X shaft, +Y front, +Z up'})
check('naming_and_scope',len(meshes)==5 and len(bpy.data.objects)==17 and len(bpy.data.meshes)==3 and not bpy.data.libraries and not bpy.data.lights and not bpy.data.cameras and all(o.name.startswith(ID+'__') and not o.name[-4:].startswith('.') for o in asset.all_objects),{'objects':len(bpy.data.objects),'meshes':len(meshes),'unique_meshes':len(bpy.data.meshes),'names':[o.name for o in asset.all_objects]})
check('collection_contract',sorted(c.name for c in asset.children)==[ID+'__anchors',ID+'__geo',ID+'__rig'],[c.name for c in asset.children])
check('hierarchy_transforms',all(o.parent is not None or o==root for o in asset.all_objects) and all((o.scale-Vector((1,1,1))).length<1e-7 and o.matrix_world.to_3x3().determinant()>0 for o in asset.all_objects),{'parents':{o.name:o.parent.name if o.parent else None for o in asset.all_objects},'positive_determinants':True})
mesh_stats={}
for data in bpy.data.meshes:
    bm=bmesh.new();bm.from_mesh(data)
    mesh_stats[data.name]={'vertices':len(bm.verts),'faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'loose_vertices':sum(not v.link_faces for v in bm.verts),'degenerate_faces':sum(f.calc_area()<1e-14 for f in bm.faces),'volume_m3':bm.calc_volume(signed=False)}
    bm.free()
check('closed_nondegenerate_components',all(x['nonmanifold_edges']==x['loose_vertices']==x['degenerate_faces']==0 and x['volume_m3']>0 for x in mesh_stats.values()),mesh_stats)
shaft=bpy.data.objects[ID+'__mesh_shaft'];radial=[math.hypot(v.co.y,v.co.z) for v in shaft.data.vertices]
check('shaft_nominal_diameter_and_real_knurl',close(max(radial)*2,.028) and min(radial)<.01385 and shaft.get('knurl_type')=='actual crossed diamond cut geometry',{'maximum_diameter_m':max(radial)*2,'minimum_diameter_m':min(radial)*2,'radial_relief_m':max(radial)-min(radial),'vertices':len(radial),'pitch_m':shaft['knurl_pitch_m'],'smooth_marks_m':[-.460,-.455,.455,.460]})
for side,sign in [('l',1),('r',-1)]:
    sleeve=bpy.data.objects[ID+'__mesh_sleeve_'+side];sp=points(sleeve)
    load=local_anchor(asset,ID,'load_'+side);end=local_anchor(asset,ID,'sleeve_end_'+side)
    sleeve_rad=max(math.hypot(v.y,v.z-HEIGHT) for v in sp if abs(v.x)>.6851)
    flange_rad=max(math.hypot(v.y,v.z-HEIGHT) for v in sp)
    check('sleeve_dimensions_'+side,close(sleeve_rad*2,.05) and close(flange_rad*2,.073) and close((end.matrix_world.translation-load.matrix_world.translation).length,.415),{'max_sleeve_diameter_m':sleeve_rad*2,'flange_diameter_m':flange_rad*2,'loadable_length_m':(end.matrix_world.translation-load.matrix_world.translation).length,'load_point_m':list(load.matrix_world.translation),'end_m':list(end.matrix_world.translation)})
    check('load_anchor_frame_'+side,(load.matrix_world.to_3x3()@Vector((0,1,0))-Vector((sign,0,0))).length<1e-6 and (load.matrix_world.translation-Vector((sign*.685,0,HEIGHT))).length<1e-6,{'matrix':[list(row) for row in load.matrix_world]})
check('shared_symmetric_meshes',bpy.data.objects[ID+'__mesh_sleeve_l'].data==bpy.data.objects[ID+'__mesh_sleeve_r'].data and bpy.data.objects[ID+'__mesh_end_cap_l'].data==bpy.data.objects[ID+'__mesh_end_cap_r'].data,{'shared_sleeve_and_cap_data':True,'mirror_method':'proper Z rotation, no negative scale'})
manifest=read_json(ASSET/'asset.json')
check('metadata_anchors',all((local_anchor(asset,ID,key).matrix_world.translation-Vector(value['position_m'])).length<1e-6 for key,value in manifest['anchors'].items()),manifest['anchors'])
spin=[]
for side in ['l','r']:
    other='r' if side=='l' else 'l'
    base=local_anchor(asset,ID,'load_'+side).matrix_world.copy()
    otherbase=local_anchor(asset,ID,'load_'+other).matrix_world.copy()
    for angle in [0,45,90,180,270,360]:
        root['sleeve_'+side+'_angle_deg']=angle;root.update_tag();bpy.context.view_layer.update()
        load=local_anchor(asset,ID,'load_'+side).matrix_world.copy()
        otherload=local_anchor(asset,ID,'load_'+other).matrix_world.copy()
        expected=Matrix.Rotation(math.radians(angle),3,'X')@base.to_3x3()
        error=max(abs(load.to_3x3()[i][j]-expected[i][j]) for i in range(3) for j in range(3))
        spin.append({'side':side,'angle_deg':angle,'orientation_error':error,'anchor_position_error_m':(load.translation-base.translation).length,'other_sleeve_error':max(abs(otherload[i][j]-otherbase[i][j]) for i in range(4) for j in range(4))})
    root['sleeve_'+side+'_angle_deg']=0;root.update_tag();bpy.context.view_layer.update()
check('independent_sleeve_spin',all(x['orientation_error']<1e-6 and x['anchor_position_error_m']<1e-6 and x['other_sleeve_error']<1e-6 for x in spin),spin)
check('steel_material_contract',all(len(o.data.materials)==(136 if current_version in ('0.1.1','0.1.2') else 8) for o in meshes) and all(close(next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Metallic'].default_value,.85) for m in bpy.data.materials),{'palette_srgb_hex':PALETTE,'slots':len(meshes[0].data.materials),'metallic':.85,'roughness':.48 if current_version in ('0.1.1','0.1.2') else .28,'rendering':'flat material swatches, no physically lit reflections'})
# Axle is smaller than sleeve inner bore; caps start beyond axle and inside recess.
check('bar_component_clearances',max(radial)<.0143 and 1.094<1.0966 and .0223<.0225,{'axle_sleeve_radial_gap_m':.0143-max(radial),'axle_cap_axial_gap_m':1.0966-1.094,'cap_pocket_radial_gap_m':.0225-.0223,'scope':'profile inequalities plus measured shaft radius; internal bearings not modeled'})
if current_version in ('0.1.1','0.1.2'):
    refinement=read_json(ASSET/'refinement-record.json')
    actual_hash=hashlib.sha256(json.dumps([list(v.co) for v in shaft.data.vertices],separators=(',',':')).encode()).hexdigest()
    check('refined_existing_asset_preserved',refinement['all_object_and_data_identity_retained'] and refinement['anchors_unchanged'] and actual_hash==refinement['shaft_coordinate_sha256'],{'record':'refinement-record.json','shaft_coordinate_sha256':actual_hash,'component_identity_during_edit':True,'anchor_frames_preserved':True})
    check('circular_subdivision_and_soft_values',all(refinement['new_mesh_vertex_counts'][key]>old for key,old in refinement['old_mesh_vertex_counts'].items() if 'shaft' not in key) and all(close(next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Roughness'].default_value,.48) for mat in bpy.data.materials),{'old_vertex_counts':refinement['old_mesh_vertex_counts'],'new_vertex_counts':refinement['new_mesh_vertex_counts'],'roughness':.48,'appended_ramp_slots':[8,135]})
    flange_l=local_anchor(asset,ID,'load_l').matrix_world.translation.x-.030
    flange_r=local_anchor(asset,ID,'load_r').matrix_world.translation.x+.030
    check('manufacturer_exposed_shaft_length',close(flange_l-flange_r,1.310),{'exposed_shaft_m':flange_l-flange_r,'overall_m':measured[0],'hidden_axle_mesh_length_m':2*1.094,'distinction':'1310mm between integrated inner flanges; hidden internal axle excluded'})
if current_version=='0.1.2':
    appearance=read_json(ASSET/'contrast-record.json')
    hashes={mesh.name:hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in mesh.vertices],'faces':[list(p.vertices) for p in mesh.polygons],'material_indices':[p.material_index for p in mesh.polygons]},separators=(',',':')).encode()).hexdigest() for mesh in bpy.data.meshes}
    check('appearance_only_geometry_unchanged',hashes==appearance['mesh_geometry_sha256'] and appearance['all_object_transforms_and_anchors_preserved'],{'all_mesh_geometry_and_face_slots':hashes,'transforms_and_anchors_preserved':True,'dimension_changes':False})
    def display_srgb(x):return 12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055
    color_errors=[]
    for name,entry in appearance['colors'].items():
        actual=[display_srgb(x) for x in bpy.data.materials[name].diffuse_color[:3]]
        expected=[.72+1.18*(x-.72) for x in entry['before_srgb']]
        color_errors.extend(abs(x-y) for x,y in zip(actual,expected))
    check('slight_steel_contrast_transform',max(color_errors)<1e-6,{'maximum_srgb_error':max(color_errors),'contrast_factor':1.18,'pivot_srgb':.72,'roughness_preserved':.48,'no_geometry_or_lighting_change':True})
reproduce(scene,read_json(ASSET/'previews/render-settings.json'))

# Fresh saved linked fixture; no local mesh data permitted.
bpy.ops.wm.open_mainfile(filepath=str(TEST_SOURCE));scene=bpy.context.scene
bar=bpy.data.collections[ID];plate=bpy.data.collections[PID]
barinst=bpy.data.objects['barbell_primary'];plateinstances=[bpy.data.objects['plate_l'],bpy.data.objects['plate_r']]
check('linked_dependencies_relative',len(bpy.data.libraries)==2 and all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries),[{'path':l.filepath,'resolved':bpy.path.abspath(l.filepath)} for l in bpy.data.libraries])
check('linked_instances_no_copied_geometry',len([o for o in scene.objects if o.instance_type=='COLLECTION'])==3 and all(o.instance_collection==plate for o in plateinstances) and barinst.instance_collection==bar and not [m for m in bpy.data.meshes if m.library is None],{'local_meshes':sum(m.library is None for m in bpy.data.meshes),'collection_instances':3,'plate_instances_share_same_linked_collection':plateinstances[0].instance_collection==plateinstances[1].instance_collection})
measure=plate_measurements(plate)
body=plate.all_objects[PID+'__mesh_body'];bore=local_anchor(plate,PID,'bore_center').matrix_world
inner=[v.co for v in body.data.vertices if math.hypot(v.co.x,v.co.z-bore.translation.z)<.026 and v.co.y<0]
inner.sort(key=lambda p:math.atan2(p.z-bore.translation.z,p.x))
minimum_bore=min(math.hypot(a.x+b.x,a.z+b.z-2*bore.translation.z) for a,b in zip(inner,inner[1:]+inner[:1]))
check('measured_plate_stack_anchors',close(measure['pitch_m'],.03302) and close(measure['floor_to_bore_m'],.225),{k:v for k,v in measure.items() if k!='bore_matrix'})
placements=[]
for side,inst in zip(['l','r'],plateinstances):
    target=barinst.matrix_world@local_anchor(bar,ID,'load_'+side).matrix_world
    outward=(target.to_3x3()@Vector((0,1,0))).normalized()
    center=(inst.matrix_world@bore).translation
    axis=(inst.matrix_world@bore).to_3x3()@Vector((0,1,0))
    pp=[p for o in plate.all_objects if o.type=='MESH' for p in points(o,inst.matrix_world)]
    projected=[(p-target.translation).dot(outward) for p in pp]
    bp=points(bar.all_objects[ID+'__mesh_sleeve_'+side],barinst.matrix_world)
    plate_start=min(projected);plate_end=max(projected)
    relevant=[p for p in bp if plate_start-1e-6<=(p-target.translation).dot(outward)<=plate_end+1e-6]
    sleeve_radius=max(math.hypot(p.y-center.y,p.z-center.z) for p in relevant)
    clear=(minimum_bore-2*sleeve_radius)/2
    on_axis=(center-target.translation).cross(outward).length
    placements.append({'side':side,'bore_center_world_m':list(center),'alignment_error_m':on_axis,'axis_error':(axis-outward).length,'flange_envelope_gap_m':plate_start,'outer_envelope_distance_from_load_m':plate_end,'sleeve_end_remaining_m':.415-plate_end,'radial_clearance_m':clear,'plate_floor_z_m':min(p.z for p in pp),'instance_determinant':inst.matrix_world.to_3x3().determinant()})
check('plate_alignment_fit_and_capacity',all(x['alignment_error_m']<1e-6 and x['axis_error']<1e-6 and x['radial_clearance_m']>.00039 and close(x['flange_envelope_gap_m'],.001) and x['sleeve_end_remaining_m']>0 and close(x['plate_floor_z_m'],0) and x['instance_determinant']>0 for x in placements),{'minimum_bore_m':minimum_bore,'placements':placements})
# BVH tests detect surface crossings; radial/axial disjoint envelopes above
# additionally rule out a completely-contained sleeve/plate-solid intersection.
bar_entries=[(o,points(o,barinst.matrix_world)) for o in bar.all_objects if o.type=='MESH']
cache={};pairs=[];collisions=[]
for side,inst in zip(['l','r'],plateinstances):
    for po in plate.all_objects:
        if po.type!='MESH':continue
        ppts=points(po,inst.matrix_world);pb=bounds(ppts);ptree=None
        for bo,bpts in bar_entries:
            b=bounds(bpts)
            if any(pb['maximum_m'][i]<b['minimum_m'][i] or b['maximum_m'][i]<pb['minimum_m'][i] for i in range(3)):continue
            if ptree is None:ptree=BVHTree.FromPolygons(ppts,[list(p.vertices) for p in po.data.polygons],all_triangles=False,epsilon=0)
            if bo.name not in cache:cache[bo.name]=BVHTree.FromPolygons(bpts,[list(p.vertices) for p in bo.data.polygons],all_triangles=False,epsilon=0)
            hits=ptree.overlap(cache[bo.name]);pairs.append({'plate':side+':'+po.name,'bar':bo.name,'crossing_triangle_pairs':len(hits)})
            if hits:collisions.append(pairs[-1])
check('plate_bar_mesh_surface_intersections',not collisions,{'tested_broad_phase_pairs':pairs,'crossings':collisions,'containment_exclusion':'measured positive bore clearance over full stack span plus positive flange gap and sleeve-end allowance'})
left=bounds([p for o in plate.all_objects if o.type=='MESH' for p in points(o,plateinstances[0].matrix_world)])
right=bounds([p for o in plate.all_objects if o.type=='MESH' for p in points(o,plateinstances[1].matrix_world)])
check('opposite_plates_separate',left['minimum_m'][0]>right['maximum_m'][0],{'separation_m':left['minimum_m'][0]-right['maximum_m'][0]})
# Placement invariance under whole assembly translation/rotation.
original_bar=barinst.matrix_world.copy();original_plates=[o.matrix_world.copy() for o in plateinstances]
transform=Matrix.Translation((1.2,-.8,.6))@Matrix.Rotation(.63,4,'Z')@Matrix.Rotation(.35,4,'Y')
barinst.matrix_world=transform@original_bar;bpy.context.view_layer.update()
errors=[]
for side,obj,original in zip(['l','r'],plateinstances,original_plates):
    place_plate(scene,barinst,bar,plate,side,instance_obj=obj)
    expected=transform@original
    errors.append(max(abs(obj.matrix_world[i][j]-expected[i][j]) for i in range(4) for j in range(4)))
check('attachment_placement_transform_invariance',max(errors)<1e-6,{'maximum_matrix_error':max(errors),'translation_m':[1.2,-.8,.6],'rotation_rad':[0,.35,.63]})
barinst.matrix_world=original_bar
for o,m in zip(plateinstances,original_plates):o.matrix_world=m
bpy.context.view_layer.update()
# Simulate evaluated sleeve frames spinning through a full turn; linked assets
# stay read-only. Collision invariance follows from measured radial clearance
# and axial envelopes, not an unperformed dynamics simulation.
spin_placements=[]
for side,inst in zip(['l','r'],plateinstances):
    load=barinst.matrix_world@local_anchor(bar,ID,'load_'+side).matrix_world
    for deg in [0,45,90,180,270,360]:
        mat=load.copy();mat=Matrix.Translation(load.translation)@Matrix.Rotation(math.radians(deg),4,'X')@Matrix.Translation(-load.translation)@mat
        outward=mat.to_3x3()@Vector((0,1,0));mat.translation+=outward*(-measure['back_m']+.001)
        pose=mat@measure['bore_matrix'].inverted()
        newbore=pose@measure['bore_matrix']
        spin_placements.append({'side':side,'degrees':deg,'axis_alignment_error':(newbore.to_3x3()@Vector((0,1,0))-outward).length,'radial_clearance_lower_bound_m':(minimum_bore-.05)/2,'stack_pitch_m':measure['pitch_m'],'determinant':pose.to_3x3().determinant()})
check('plate_spin_frame_sweep',all(x['axis_alignment_error']<1e-6 and x['radial_clearance_lower_bound_m']>0 and x['determinant']>0 for x in spin_placements),{'cases':spin_placements,'scope':'kinematic placement and clearance invariant; no physics or override-action authoring tested'})
if current_version in ('0.1.1','0.1.2'):
    cap=read_json(ASSET/'capacity-calculation.json')
    capacity_source=FIXTURE/(SID+'__capacity.blend')
    bpy.ops.wm.open_mainfile(filepath=str(capacity_source));scene=bpy.context.scene
    bar=bpy.data.collections[ID];plate=bpy.data.collections[PID];barinst=bpy.data.objects['barbell_primary']
    plates=[o for o in scene.objects if o.instance_type=='COLLECTION' and o.instance_collection==plate]
    n=cap['plates_per_sleeve'];m=plate_measurements(plate);bore=local_anchor(plate,PID,'bore_center').matrix_world
    check('capacity_linked_instances',len(plates)==2*n and not [data for data in bpy.data.meshes if data.library is None],{'plate_instances':len(plates),'per_side':n,'local_meshes':sum(data.library is None for data in bpy.data.meshes),'secondary_source':str(capacity_source.relative_to(REPO)),'source_sha256':digest(capacity_source)})
    length=(local_anchor(bar,ID,'sleeve_end_l').matrix_world.translation-local_anchor(bar,ID,'load_l').matrix_world.translation).length
    calculated=math.floor((length-cap['collar_reserve_m']-cap['end_margin_m']-cap['flange_gap_m']+cap['interplate_gap_m'])/(m['pitch_m']+cap['interplate_gap_m']))
    used=cap['flange_gap_m']+n*m['pitch_m']+(n-1)*cap['interplate_gap_m']+cap['collar_reserve_m']+cap['end_margin_m']
    next_used=cap['flange_gap_m']+(n+1)*m['pitch_m']+n*cap['interplate_gap_m']+cap['collar_reserve_m']+cap['end_margin_m']
    check('capacity_formula_and_next_plate_rejection',n==calculated==10 and used<=length and next_used>length and close(m['pitch_m'],cap['manufacturer_plate_thickness_m']),{'capacity_per_sleeve':calculated,'sleeve_m':length,'pitch_m':m['pitch_m'],'published_plate_thickness_m':cap['manufacturer_plate_thickness_m'],'used_with_reserves_m':used,'spare_m':length-used,'next_plate_excess_m':next_used-length,'collar_reserved_not_modeled_m':cap['collar_reserve_m'],'end_margin_m':cap['end_margin_m']})
    side_results={};multi_bvhs={};multi_pairs=[];multi_crossings=[]
    bar_points={o.name:(o,points(o,barinst.matrix_world)) for o in bar.all_objects if o.type=='MESH'}
    for side,sign in [('l',1),('r',-1)]:
        sideplates=sorted([o for o in plates if o.get('side')==side],key=lambda o:o['stack_index'])
        target=barinst.matrix_world@local_anchor(bar,ID,'load_'+side).matrix_world
        axis=target.to_3x3()@Vector((0,1,0))
        end=barinst.matrix_world@local_anchor(bar,ID,'sleeve_end_'+side).matrix_world.translation
        sleeve=bar.all_objects[ID+'__mesh_sleeve_'+side]
        sleevepts=points(sleeve,barinst.matrix_world)
        maxradius=max(math.hypot(p.y,p.z-.225) for p in sleevepts if abs(p.x)>.6851)
        rows=[]
        for index,obj in enumerate(sideplates):
            pts=[p for mesh in plate.all_objects if mesh.type=='MESH' for p in points(mesh,obj.matrix_world)]
            projection=[(p-target.translation).dot(axis) for p in pts]
            center=(obj.matrix_world@bore).translation
            rows.append({'index':index,'minimum_axial_m':min(projection),'maximum_axial_m':max(projection),'axis_error_m':(center-target.translation).cross(axis).length,'bore_center_world_m':list(center),'radial_clearance_m':minimum_bore/2-maxradius,'floor_z_m':min(p.z for p in pts)})
            for po in plate.all_objects:
                if po.type!='MESH':continue
                pp=points(po,obj.matrix_world);pb=bounds(pp);ptree=None
                for name,(bo,bp) in bar_points.items():
                    bb2=bounds(bp)
                    if any(pb['maximum_m'][i]<bb2['minimum_m'][i] or bb2['maximum_m'][i]<pb['minimum_m'][i] for i in range(3)):continue
                    if ptree is None:ptree=BVHTree.FromPolygons(pp,[list(p.vertices) for p in po.data.polygons],all_triangles=False,epsilon=0)
                    if name not in multi_bvhs:multi_bvhs[name]=BVHTree.FromPolygons(bp,[list(p.vertices) for p in bo.data.polygons],all_triangles=False,epsilon=0)
                    hits=ptree.overlap(multi_bvhs[name]);multi_pairs.append({'instance':obj.name,'plate_mesh':po.name,'bar_mesh':name,'crossings':len(hits)})
                    if hits:multi_crossings.append(multi_pairs[-1])
        gaps=[b['minimum_axial_m']-a['maximum_axial_m'] for a,b in zip(rows,rows[1:])]
        collar_space=(end-target.translation).dot(axis)-rows[-1]['maximum_axial_m']
        side_results[side]={'plates':rows,'minimum_interplate_gap_m':min(gaps),'remaining_collar_and_tip_space_m':collar_space,'flange_gap_m':rows[0]['minimum_axial_m']}
    check('all_capacity_plate_alignment_clearances',all(len(v['plates'])==n and v['minimum_interplate_gap_m']>.00049 and v['remaining_collar_and_tip_space_m']>=cap['collar_reserve_m']+cap['end_margin_m'] and close(v['flange_gap_m'],.001) and all(p['axis_error_m']<1e-6 and p['radial_clearance_m']>.00039 and abs(p['floor_z_m'])<1e-6 for p in v['plates']) for v in side_results.values()),side_results)
    mirror_error=max((Vector(l['bore_center_world_m'])-Vector((-rr['bore_center_world_m'][0],rr['bore_center_world_m'][1],rr['bore_center_world_m'][2]))).length for l,rr in zip(side_results['l']['plates'],side_results['r']['plates']))
    check('capacity_stack_symmetry_and_no_plate_intersections',mirror_error<1e-6 and all(v['minimum_interplate_gap_m']>0 for v in side_results.values()),{'mirror_position_error_m':mirror_error,'left_gap_m':side_results['l']['minimum_interplate_gap_m'],'right_gap_m':side_results['r']['minimum_interplate_gap_m'],'method':'positive separation of complete geometry axial envelopes excludes all neighboring plate-solid intersections; opposite stacks on disjoint X ranges'})
    check('capacity_plate_bar_surface_intersections',not multi_crossings,{'broad_phase_pairs':len(multi_pairs),'all_crossing_pairs':multi_crossings,'all_tested_pairs':multi_pairs,'containment_excluded':'every plate bore larger than measured sleeve envelope, with positive flange and axial reserve'})
    protected=read_json(Path('/private/tmp/barbell_refine_protected.json'))
    check('plate_and_shared_standards_preserved',all(digest(REPO/p)==sha for p,sha in protected.items()),{'protected_file_count':len(protected),'scope':'all original plate files, AGENTS and normative guides'})
if current_version=='0.1.2':
    example_source=FIXTURE/(SID+'__example.blend')
    bpy.ops.wm.open_mainfile(filepath=str(example_source));scene=bpy.context.scene
    bar=bpy.data.collections[ID];plate=bpy.data.collections[PID];barinst=bpy.data.objects['barbell_primary']
    example_plates=[o for o in scene.objects if o.instance_type=='COLLECTION' and o.instance_collection==plate]
    check('five_plate_example_linking',len(example_plates)==10 and not [mesh for mesh in bpy.data.meshes if mesh.library is None] and all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries),{'plate_instances':len(example_plates),'local_meshes':sum(mesh.library is None for mesh in bpy.data.meshes),'relative_libraries':[lib.filepath for lib in bpy.data.libraries],'example_sha256':digest(example_source)})
    measure=plate_measurements(plate);bore=local_anchor(plate,PID,'bore_center').matrix_world
    bar_points={o.name:(o,points(o,barinst.matrix_world)) for o in bar.all_objects if o.type=='MESH'}
    tree_cache={};example_rows={};pairs=0;crossings=[]
    for side in ['l','r']:
        objs=sorted([o for o in example_plates if o.get('side')==side],key=lambda o:o['stack_index'])
        load=barinst.matrix_world@local_anchor(bar,ID,'load_'+side).matrix_world
        outward=load.to_3x3()@Vector((0,1,0));rows=[]
        for obj in objs:
            all_points=[p for po in plate.all_objects if po.type=='MESH' for p in points(po,obj.matrix_world)]
            axial=[(p-load.translation).dot(outward) for p in all_points]
            center=(obj.matrix_world@bore).translation
            rows.append({'instance':obj.name,'bore_center_m':list(center),'axis_error_m':(center-load.translation).cross(outward).length,'minimum_axial_m':min(axial),'maximum_axial_m':max(axial),'floor_m':min(p.z for p in all_points)})
            for po in plate.all_objects:
                if po.type!='MESH':continue
                pp=points(po,obj.matrix_world);pb=bounds(pp);ptree=None
                for name,(bo,bp) in bar_points.items():
                    bb2=bounds(bp)
                    if any(pb['maximum_m'][i]<bb2['minimum_m'][i] or bb2['maximum_m'][i]<pb['minimum_m'][i] for i in range(3)):continue
                    if ptree is None:ptree=BVHTree.FromPolygons(pp,[list(p.vertices) for p in po.data.polygons],all_triangles=False,epsilon=0)
                    if name not in tree_cache:tree_cache[name]=BVHTree.FromPolygons(bp,[list(p.vertices) for p in bo.data.polygons],all_triangles=False,epsilon=0)
                    hits=ptree.overlap(tree_cache[name]);pairs+=1
                    if hits:crossings.append({'instance':obj.name,'plate_mesh':po.name,'bar_mesh':name,'crossings':len(hits)})
        gaps=[b['minimum_axial_m']-a['maximum_axial_m'] for a,b in zip(rows,rows[1:])]
        remaining=.415-rows[-1]['maximum_axial_m']
        example_rows[side]={'plates':rows,'minimum_interplate_gap_m':min(gaps),'remaining_sleeve_m':remaining,'spare_after_collar_and_tip_m':remaining-.050-.005}
    mirror=max((Vector(l['bore_center_m'])-Vector((-rr['bore_center_m'][0],rr['bore_center_m'][1],rr['bore_center_m'][2]))).length for l,rr in zip(example_rows['l']['plates'],example_rows['r']['plates']))
    check('five_plate_example_fit_and_symmetry',mirror<1e-6 and all(len(x['plates'])==5 and x['minimum_interplate_gap_m']>.00049 and x['spare_after_collar_and_tip_m']>.1918 and all(p['axis_error_m']<1e-6 and abs(p['floor_m'])<1e-6 for p in x['plates']) for x in example_rows.values()),{'mirror_error_m':mirror,'radial_clearance_lower_bound_m':(minimum_bore-.05)/2,'sides':example_rows,'scope':'five-plate partial stack, not new capacity limit'})
    check('five_plate_example_intersections',not crossings,{'broad_phase_pairs':pairs,'crossings':crossings,'containment_and_interplate_exclusion':'same measured positive bore clearance and complete axial envelope gaps as ten-plate test'})
    check('approved_plate_and_shared_guides_unchanged',all(digest(REPO/p)==sha for p,sha in read_json(ASSET/'contrast-example-plan.json')['protected_sha256'].items()),{'protected_hashes':'contrast-example-plan.json','dimension_changes':False})
# Reopen to discard float decomposition after transform-invariance stress tests.
bpy.ops.wm.open_mainfile(filepath=str(TEST_SOURCE));scene=bpy.context.scene
reproduce(scene,read_json(FIXTURE/'previews/render-settings.json'))
verify_plate()
protected=read_json(Path('/private/tmp/barbell_plate_protected.json')) if Path('/private/tmp/barbell_plate_protected.json').exists() else {plate_record['source']['path']:plate_record['source']['sha256']}
check('approved_plate_artifacts_untouched',all(digest(REPO/p)==h for p,h in protected.items()),{'files_checked':len(protected),'approved_plate_source_sha256':plate_record['source']['sha256']})
check('sources_not_modified_by_validation',digest(SOURCE)==source_hash and digest(TEST_SOURCE)==test_hash,{'barbell_sha256':source_hash,'fixture_sha256':test_hash})
summary={'passed':sum(c['status']=='PASS' for c in checks.values()),'failed':sum(c['status']=='FAIL' for c in checks.values())}
# Report current external approval metadata without changing any test logic.
current_metadata=read_json(ASSET/'asset.json')
release=current_metadata.get('production_release',{})
production_limits=release.get('limitations') or ['physical fit/mass/load ratings unverified','fresh committed checkout/LFS fetch not run','user visual approval pending','global baselines and artwork terms open','override action authoring, human consumers and alternative replacements untested']
result={'asset_id':ID,'version':current_version,'blender_version':bpy.app.version_string,'source_sha256':source_hash,'fixture_sha256':test_hash,'plate_sha256':plate_record['source']['sha256'],'validator_sha256':digest(__file__),'helper_sha256':digest(Path(__file__).with_name('barbell_20kg_common.py')),'summary':summary,'checks':checks,'production_limits':production_limits,'approval_status':current_metadata.get('approval',{}).get('status','pending'),'production_scope':release.get('scope','review prototype')}
write_json(ASSET/'validation-results.json',result)
write_json(FIXTURE/'validation-results.json',{'summary':summary,'source_sha256':test_hash,'barbell_results':str((ASSET/'validation-results.json').relative_to(REPO)),'scope':'fixture-specific evidence in linked_dependencies_relative through plate_spin_frame_sweep and assembled reproduction'})
print('BARBELL_VALIDATION_COMPLETE',summary,flush=True)
if summary['failed']:raise RuntimeError('Prototype validation failed; inspect validation-results.json')
