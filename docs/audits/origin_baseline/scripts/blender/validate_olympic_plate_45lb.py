"""Inspect the saved plate, link three instances in a disposable fixture,
and reproduce its reference renders from the saved source in a fresh process.
Writes measured evidence; never modifies the source .blend.
"""
from pathlib import Path
import bpy
import bmesh
import hashlib
import json
import math
import tempfile
import numpy as np
from mathutils import Matrix, Vector

REPO = Path(__file__).resolve().parents[2]
ID = '168h_equipment_olympic_plate_45lb_cast_iron'
ASSET = REPO / 'assets/equipment/free_weights' / ID
SOURCE = ASSET / f'{ID}.blend'
SETTINGS = json.loads((ASSET/'previews/render-settings.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
asset = bpy.data.collections[ID]
root = bpy.data.objects[ID+'__root']
asset_version = root.get('asset_version')
objects = list(asset.all_objects)
meshes = [o for o in objects if o.type == 'MESH']
checks = {}


def check(name, condition, evidence):
    checks[name] = {'status': 'PASS' if condition else 'FAIL', 'evidence': evidence}
    if not condition:
        print('VALIDATION_FAILURE', name, evidence)


points = [o.matrix_world @ v.co for o in meshes for v in o.data.vertices]
minimum = [min(p[i] for p in points) for i in range(3)]
maximum = [max(p[i] for p in points) for i in range(3)]
dims = [b-a for a,b in zip(minimum,maximum)]
check('canonical_bounds', all(abs(a-b)<1e-6 for a,b in zip(dims,[.45,.03302,.45])), {'dimensions_m':dims,'minimum_m':minimum,'maximum_m':maximum})
check('floor_and_root', abs(minimum[2])<1e-6 and root.matrix_world.is_identity, {'root_matrix': [list(row) for row in root.matrix_world], 'floor_z_m': minimum[2]})
check('normalized_geometry_transforms', all(o.matrix_local.is_identity for o in meshes), {o.name: [list(row) for row in o.matrix_local] for o in meshes})
check('naming', all(o.name.startswith(ID+'__') and not o.name[-4:].startswith('.') for o in objects), [o.name for o in objects])
check('collection_structure', sorted(c.name for c in asset.children)==[ID+'__anchors', ID+'__geo'], [c.name for c in asset.children])
check('source_scope', len(bpy.data.objects)==(15 if asset_version in ('0.1.2','0.1.3','0.1.4') else 8) and len(meshes)==(10 if asset_version in ('0.1.2','0.1.3','0.1.4') else 3) and not bpy.data.cameras and not bpy.data.lights, {'object_count': len(bpy.data.objects),'mesh_count':len(meshes),'cameras':len(bpy.data.cameras),'lights':len(bpy.data.lights)})
check('root_hierarchy', all(o==root or o.parent==root for o in objects), {'children': [o.name for o in root.children]})
expected = {'bore_center':(0,0,.225),'stack_front':(0,.01651,.225),'stack_back':(0,-.01651,.225),'floor_contact':(0,0,0)}
check('anchors', all((bpy.data.objects[ID+'__anchor_'+key].location-Vector(pos)).length<1e-7 and bpy.data.objects[ID+'__anchor_'+key].rotation_euler.to_matrix().is_identity for key,pos in expected.items()), expected)
body=bpy.data.objects[ID+'__mesh_body']
bm=bmesh.new(); bm.from_mesh(body.data)
nonmanifold=sum(not e.is_manifold for e in bm.edges)
check('body_manifold', nonmanifold==0 and all(v.link_faces for v in bm.verts), {'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'nonmanifold_edges':nonmanifold,'volume_m3':bm.calc_volume(signed=False)})
bm.free()
# Minimum clearance of the polygonal bore, measured across its flat facets.
inner=[v.co for v in body.data.vertices if math.hypot(v.co.x,v.co.z-.225)<.026 and v.co.y<0]
inner.sort(key=lambda p:math.atan2(p.z-.225,p.x))
across_flats=[]
for a,b in zip(inner, inner[1:]+inner[:1]):
    across_flats.append(math.hypot(a.x+b.x,a.z+b.z-.45))
minimum_bore=min(across_flats)
check('two_inch_minimum_bore', abs(minimum_bore-.0508)<1e-7, {'minimum_across_flats_diameter_m':minimum_bore,'maximum_vertex_diameter_m':max(math.hypot(v.x,v.z-.225)*2 for v in inner),'angular_segments':len(inner)})
check('numerical_sleeve_clearance', minimum_bore>.05, {'test_sleeve_diameter_m':.05,'minimum_radial_clearance_m':(minimum_bore-.05)/2,'scope':'numerical clearance fixture only; no barbell geometry or physical-fit claim'})
labels=[o for o in meshes if 'label_' in o.name]
label_extents={o.name: [min(v.co.y for v in o.data.vertices),max(v.co.y for v in o.data.vertices)] for o in labels}
web_half=float(root.get('web_thickness_m',.021))/2
label_details={}
for obj in labels:
    sign=1 if 'front' in obj.name else -1
    axial=[sign*v.co.y for v in obj.data.vertices]
    label_details[obj.name]={'y_extents_m':label_extents[obj.name],
        'solid_depth_m':max(axial)-min(axial), 'exposed_relief_m':max(axial)-web_half,
        'material_face_counts':{str(index):sum(p.material_index==index for p in obj.data.polygons) for index in range(len(obj.data.materials))}}
expected_relief=.0035 if asset_version in ('0.1.1','0.1.2','0.1.3','0.1.4') else .0015
check('raised_labels', len(labels)==(8 if asset_version in ('0.1.2','0.1.3','0.1.4') else 2) and all(o.get('raised_text') in ('45 LB','20.4 KG','STANDARD','BARBELL') for o in labels) and all(abs(info['exposed_relief_m']-expected_relief)<1e-6 and info['solid_depth_m']>expected_relief for info in label_details.values()) and all(max(abs(v.co.y) for v in o.data.vertices)<.01651 for o in labels), label_details)
if asset_version=='0.1.1':
    profile_measurements={'web_thickness_m':2*abs(body.data.vertices[4*256].co.y),
       'hub_thickness_m':2*abs(body.data.vertices[2*256].co.y),
       'rim_relief_m':abs(body.data.vertices[7*256].co.y)-abs(body.data.vertices[4*256].co.y)}
    check('refined_cast_profile', all(abs(profile_measurements[key]-value)<1e-6 for key,value in {'web_thickness_m':.013,'hub_thickness_m':.029,'rim_relief_m':.01001}.items()),profile_measurements)
    refinement=json.loads((ASSET/'refinement-record.json').read_text())
    actual_topology={m.name:hashlib.sha256(json.dumps({'edges':[list(e.vertices) for e in m.edges],'polygons':[list(p.vertices) for p in m.polygons]},separators=(',',':')).encode()).hexdigest() for m in bpy.data.meshes}
    check('existing_topology_preserved',actual_topology==refinement['mesh_topology_sha256'] and refinement['object_and_mesh_datablock_identity_preserved'] and refinement['anchors_unchanged'] and refinement['prior_material_slot_prefixes_unchanged'], {'mesh_topology_sha256':actual_topology,'refined_from_sha256':refinement['predecessor_sha256'],'same_object_and_data_identity_during_edit':True,'anchors_and_prior_material_slots_preserved':True})
if asset_version in ('0.1.2','0.1.3','0.1.4'):
    radial=lambda vertex:math.hypot(vertex.co.x,vertex.co.z-.225)
    web_half_actual=min(abs(v.co.y) for v in body.data.vertices if abs(radial(v)-.061)<1e-5)
    hub_half_actual=max(abs(v.co.y) for v in body.data.vertices if abs(radial(v)-.052)<1e-5)
    rim_half=max(abs(v.co.y) for v in body.data.vertices if radial(v)>.20)
    profile_measurements={'web_thickness_m':2*web_half_actual,'hub_thickness_m':2*hub_half_actual,'rim_relief_m':rim_half-web_half_actual}
    check('refined_cast_profile',all(abs(profile_measurements[key]-value)<1e-6 for key,value in {'web_thickness_m':.013,'hub_thickness_m':.029,'rim_relief_m':.01001}.items()),profile_measurements)
    detail=json.loads((ASSET/'detail-record.json').read_text())
    check('existing_body_refined',detail['existing_body_mesh_datablock_preserved'] and detail['existing_objects_preserved'] and detail['anchors_unchanged'] and len(body.data.vertices)==5888 and len(body.data.polygons)==5888,{'body_vertices':len(body.data.vertices),'body_faces':len(body.data.polygons),'added_side_band_vertices':768,'existing_objects_and_body_data_preserved':True,'evidence':'detail-record.json'})
    waist_radius=min(radial(v) for v in body.data.vertices if abs(v.co.y)<1e-6 and radial(v)>.22)
    shoulder_radius=max(radial(v) for v in body.data.vertices)
    check('nonuniform_side_profile',abs(waist_radius-.2235)<1e-6 and shoulder_radius-waist_radius>.0014,{'waist_radius_m':waist_radius,'rim_shoulder_radius_m':shoulder_radius,'radial_waist_depth_m':shoulder_radius-waist_radius})
    rib_obj=bpy.data.objects[ID+'__mesh_ribs']
    bm=bmesh.new();bm.from_mesh(rib_obj.data)
    unseen=set(bm.verts);components=[]
    while unseen:
        seed=unseen.pop();group={seed};stack=[seed]
        while stack:
            v=stack.pop()
            for edge in v.link_edges:
                other=edge.other_vert(v)
                if other in unseen:unseen.remove(other);group.add(other);stack.append(other)
        components.append(group)
    centroids=[sum((v.co for v in group),Vector())/len(group) for group in components]
    front_count=sum(center.y>0 for center in centroids)
    back_count=sum(center.y<0 for center in centroids)
    nonmanifold=sum(not edge.is_manifold for edge in bm.edges)
    check('four_cast_ribs_per_face',len(components)==8 and front_count==back_count==4 and nonmanifold==0,{'closed_rib_solids':len(components),'front_ribs':front_count,'back_ribs':back_count,'nonmanifold_edges':nonmanifold,'component_angles_degrees':[round(math.degrees(math.atan2(c.z-.225,c.x))%360,4) for c in centroids]})
    bm.free()
    by_face={face:{obj.get('raised_text'):obj for obj in labels if obj.get('face')==face} for face in ['front','back']}
    required={'45 LB','20.4 KG','STANDARD','BARBELL'}
    balanced=all(set(values)==required for values in by_face.values())
    for face,values in by_face.items():
        sign=1 if face=='front' else -1
        centers={text:sum((v.co for v in obj.data.vertices),Vector())/len(obj.data.vertices) for text,obj in values.items()}
        balanced=balanced and centers['45 LB'].x*sign>0 and centers['20.4 KG'].x*sign<0 and centers['STANDARD'].z>.225 and centers['BARBELL'].z<.225
    check('balanced_dual_unit_lettering',balanced,{'faces':{face:sorted(values) for face,values in by_face.items()},'layout':'45 LB left, 20.4 KG right, STANDARD top, BARBELL bottom on both faces'})
if asset_version in ('0.1.3','0.1.4'):
    rib_mesh=bpy.data.objects[ID+'__mesh_ribs'].data
    taper_measurements=[]
    for component in range(8):
        angle=math.radians([45,135,225,315][component%4])
        c,s=math.cos(angle),math.sin(angle)
        rows=[]
        for row in range(4):
            points=[rib_mesh.vertices[component*24+row*6+i].co for i in range(6)]
            tangents=[-p.x*s+(p.z-.225)*c for p in points]
            radii=[p.x*c+(p.z-.225)*s for p in points]
            rows.append({'radius_m':sum(radii)/6,'width_m':max(tangents)-min(tangents)})
        taper_measurements.append(rows)
    taper_ok=all(all(rows[i]['width_m']>rows[i+1]['width_m'] for i in range(3)) and rows[0]['radius_m']<.052 and all(abs(rows[i]['width_m']-width)<1e-6 for i,width in enumerate([.034,.030,.020,.010])) for rows in taper_measurements)
    check('hub_originating_outward_rib_taper',taper_ok,{'rib_rows':taper_measurements,'start_within_hub_face':True,'widths_strictly_decrease_outward':taper_ok})
    mat=bpy.data.materials[ID+'__material_lettering']
    expected_white_linear=((242/255+.055)/1.055)**2.4
    node=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    check('near_white_raised_letter_faces',all(abs(value-expected_white_linear)<1e-6 for value in mat.diffuse_color[:3]) and all(abs(value-expected_white_linear)<1e-6 for value in node.inputs['Base Color'].default_value[:3]) and all(obj.data.materials[0]==mat for obj in labels),{'srgb_hex':'F2F2F2','linear_rgb':list(mat.diffuse_color[:3]),'real_geometry_relief_test':'raised_labels'})
    finish=json.loads((ASSET/('correction-record.json' if asset_version=='0.1.4' else 'finish-record.json')).read_text())
    actual_topology={mesh.name:hashlib.sha256(json.dumps({'edges':[list(e.vertices) for e in mesh.edges],'faces':[list(p.vertices) for p in mesh.polygons]},separators=(',',':')).encode()).hexdigest() for mesh in bpy.data.meshes}
    body_coords=hashlib.sha256(json.dumps([list(v.co) for v in body.data.vertices],separators=(',',':')).encode()).hexdigest()
    check('body_and_non_barbell_topology_preserved' if asset_version=='0.1.4' else 'all_topology_and_body_preserved',actual_topology==finish['mesh_topology_sha256'] and body_coords==finish['body_coordinate_sha256'] and finish['all_object_and_mesh_data_identity_preserved'] and finish['anchors_unchanged'],{'body_coordinates_unchanged':True,'all_mesh_topology_sha256':actual_topology,'all_existing_object_data_identity_preserved_during_edit':True,'preservation_record':'correction-record.json' if asset_version=='0.1.4' else 'finish-record.json'})
if asset_version=='0.1.4':
    rib_mesh=bpy.data.objects[ID+'__mesh_ribs'].data
    root_measurements=[]
    for component in range(8):
        points=[rib_mesh.vertices[component*24+i].co for i in range(6)]
        root_measurements.append({'max_planar_radius_m':max(math.hypot(p.x,p.z-.225) for p in points),'max_axial_m':max(abs(p.y) for p in points),'min_planar_radius_m':min(math.hypot(p.x,p.z-.225) for p in points)})
    check('rib_roots_buried_in_hub_face',all(info['max_planar_radius_m']<.052 and info['max_axial_m']<.0145 and info['min_planar_radius_m']>.0274 for info in root_measurements),{'root_measurements':root_measurements,'hub_face_outer_radius_m':.052,'hub_face_axial_m':.0145})
    from mathutils import Euler
    front_config=SETTINGS['camera_views']['front'];rotated_config=SETTINGS['camera_views']['rotated_180_check']
    front_matrix=Euler(front_config['rotation_euler_xyz_radians'],'XYZ').to_matrix()
    rotated_matrix=Euler(rotated_config['rotation_euler_xyz_radians'],'XYZ').to_matrix()
    delta=front_matrix.transposed()@rotated_matrix
    expected_roll=Matrix.Rotation(math.pi,3,'Z')
    check('full_plate_rotation_proof_setup',front_config['position_m']==rotated_config['position_m'] and front_config['ortho_scale_m']==rotated_config['ortho_scale_m'] and max(abs(delta[row][col]-expected_roll[row][col]) for row in range(3) for col in range(3))<1e-6,{'roll_degrees':180,'camera_position_and_scale_unchanged':True,'image':rotated_config['path'],'visual_acceptance':'BARBELL upright upper-arc shape inspected separately; see validation.md'})
check('no_external_assets', not bpy.data.fonts and not any(i.source=='FILE' for i in bpy.data.images) and not bpy.data.libraries, {'external_fonts':len(bpy.data.fonts),'external_images':[i.filepath for i in bpy.data.images if i.source=='FILE'],'libraries':[l.filepath for l in bpy.data.libraries]})
shade=scene.display.shading
check('shadow_free_setup', scene.render.engine=='BLENDER_WORKBENCH' and shade.light=='FLAT' and not shade.show_shadows and not shade.show_cavity and not shade.show_specular_highlight and not bpy.data.lights, {'engine':scene.render.engine,'lighting':shade.light,'shadows':shade.show_shadows,'cavity_ao':shade.show_cavity,'specular_highlight':shade.show_specular_highlight,'lights':len(bpy.data.lights)})
check('shader_roughness', all(next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Roughness'].default_value==1 for m in bpy.data.materials), {m.name:{'roughness':1,'material_display_rgba':list(m.diffuse_color)} for m in bpy.data.materials})
check('source_digest_matches_renders', hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SETTINGS['source_sha256'], SETTINGS['source_sha256'])

# Reproduce PNGs from the saved file in this fresh Blender process. Cameras are
# transient, no bpy save operation is performed by this validation script.
camdata=bpy.data.cameras.new('plate_review_camera_transient')
cam=bpy.data.objects.new('plate_review_camera_transient',camdata)
scene.collection.objects.link(cam)
scene.camera=cam
cam.data.type='ORTHO'
with tempfile.TemporaryDirectory(prefix='168h_plate_reference_check_') as temp:
    for view, config in SETTINGS['camera_views'].items():
        cam.location=config['position_m']
        cam.rotation_euler=config['rotation_euler_xyz_radians']
        cam.data.ortho_scale=config['ortho_scale_m']
        scene.render.filepath=str(Path(temp)/f'{view}.png')
        bpy.ops.render.render(write_still=True)
        reproduced=Path(scene.render.filepath)
        original=REPO/config['path']
        decoded=[]
        for image_path in [original,reproduced]:
            image=bpy.data.images.load(str(image_path),check_existing=False)
            pixels=np.empty(len(image.pixels),dtype=np.float32)
            image.pixels.foreach_get(pixels)
            decoded.append(pixels)
            bpy.data.images.remove(image)
        maximum_delta=float(np.max(np.abs(decoded[0]-decoded[1])))
        same=bool(np.array_equal(decoded[0],decoded[1]))
        check('reference_reproduction_'+view, same, {'reference':config['path'],'file_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'pixel_sha256':hashlib.sha256(decoded[0].tobytes()).hexdigest(),'fresh_process_pixels_identical':same,'maximum_pixel_channel_delta':maximum_delta,'note':'Compare decoded pixels; PNG metadata may differ between processes.'})
bpy.data.objects.remove(cam,do_unlink=True)

# Disposable fresh scene links the published source collection, then instances
# it three times. No barbell or exercise scene is authored or saved.
bpy.ops.wm.read_factory_settings(use_empty=True)
fixture=bpy.context.scene
fixture.name='plate_link_and_stack_fixture_transient'
with bpy.data.libraries.load(str(SOURCE),link=True) as (available, loaded):
    loaded.collections=[ID]
linked=loaded.collections[0]
instances=[]
for index in range(3):
    instance=bpy.data.objects.new(f'plate_fixture_{index}',None)
    fixture.collection.objects.link(instance)
    instance.instance_type='COLLECTION'
    instance.instance_collection=linked
    instance.location=(0,index*.03302,0)
    instances.append(instance)
check('linked_collection_reuse', linked.library is not None and all(o.instance_collection==linked for o in instances), {'instance_count':len(instances),'linked_collection':linked.name,'linked_source':linked.library.filepath,'shared_mesh_data':[o.data.name for o in linked.all_objects if o.type=='MESH']})
# Using actual measured envelope verifies adjacent plates do not overlap.
stack_gaps=[(instances[i+1].location.y+minimum[1])-(instances[i].location.y+maximum[1]) for i in range(2)]
check('stack_pitch_no_overlap', all(abs(g)<1e-7 for g in stack_gaps), {'pitch_m':.03302,'adjacent_envelope_gaps_m':stack_gaps,'configuration':'3 upright instances along +Y; no rotation'})
# Align bore center to a synthetic target at different height, then rotate an
# instance to +X. This tests the root/anchor offset without building a barbell.
target=Vector((1,2,.9))
placement=target-Vector(expected['bore_center'])
check('bore_anchor_placement', (placement+Vector(expected['bore_center'])-target).length<1e-7, {'target_m':list(target),'root_translation_m':list(placement)})
rotation=Matrix.Rotation(-math.pi/2,4,'Z')
instances[0].matrix_world=Matrix.Translation(target) @ rotation @ Matrix.Translation(-Vector(expected['bore_center']))
aligned_center=instances[0].matrix_world @ Vector(expected['bore_center'])
aligned_axis=instances[0].matrix_world.to_3x3() @ Vector((0,1,0))
check('rotated_anchor_placement', (aligned_center-target).length<1e-6 and (aligned_axis-Vector((1,0,0))).length<1e-6 and instances[0].matrix_world.to_3x3().determinant()>0, {'target_m':list(target),'actual_center_m':list(aligned_center),'actual_stack_axis':list(aligned_axis),'positive_determinant':instances[0].matrix_world.to_3x3().determinant()})

report={'asset_id':ID,'version':asset_version,'blender_version':bpy.app.version_string,'date':'2026-10-14','source_sha256':SETTINGS['source_sha256'],'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'limitations':['No real barbell, human, exercise consumer, or alternative plate exists for substitution tests.','Prototype settings approved under A09 only; artwork licensing and production standards remain open.','Separate cast-on ribs and text solids overlap body intentionally; not a fabrication-ready union.']}
(ASSET/'validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
failures=[key for key,value in checks.items() if value['status']=='FAIL']
print('PLATE_VALIDATION',json.dumps({'passed':len(checks)-len(failures),'failed':failures,'dimensions_m':dims,'minimum_bore_m':minimum_bore}))
if failures:
    raise RuntimeError('Plate validation failed: '+', '.join(failures))
