"""Apply approved asset-local 0.1.3 typography and monotonic rib refinement.
Edits existing vertices/materials only; all source objects/data/topology retained.
Run in an isolated Blender 5.1.1 process; 0.1.3 reruns only save/rerender.
"""
from pathlib import Path
import bpy
import hashlib,json,math

REPO=Path(__file__).resolve().parents[2]
ID='168h_equipment_olympic_plate_45lb_cast_iron'
ASSET=REPO/'assets/equipment/free_weights'/ID
SOURCE=ASSET/f'{ID}.blend'
PREDECESSOR='6459107e4e960f5157c3a8b735e3753eea71b376945547a4cb04f01c39c41393'
VERSION='0.1.3'
settings=json.loads((ASSET/'previews/render-settings.json').read_text())
input_digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene;root=bpy.data.objects[ID+'__root']
body=bpy.data.objects[ID+'__mesh_body'];ribs=bpy.data.objects[ID+'__mesh_ribs']
labels=[o for o in bpy.data.objects if o.type=='MESH' and 'label_' in o.name]
assert len(labels)==8 and len(ribs.data.vertices)==192
pointers={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
anchor_matrices={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}


def topology(data):
    return hashlib.sha256(json.dumps({'edges':[list(e.vertices) for e in data.edges],'faces':[list(p.vertices) for p in data.polygons]},separators=(',',':')).encode()).hexdigest()


def coordinates(data):
    return hashlib.sha256(json.dumps([list(v.co) for v in data.vertices],separators=(',',':')).encode()).hexdigest()


topologies={m.name:topology(m) for m in bpy.data.meshes}
body_coordinates=coordinates(body.data)
old_stations=[(.052,.009,.0135,.0149),(.070,.013,.0062,.012),(.185,.013,.0062,.012),(.205,.010,.0135,.016)]
new_stations=[(.049,.017,.0135,.0149),(.075,.015,.0062,.012),(.150,.010,.0062,.012),(.205,.005,.0135,.016)]


def rib_points(stations):
    points=[]
    for sign in [1,-1]:
        for degrees in [45,135,225,315]:
            angle=math.radians(degrees);c,s=math.cos(angle),math.sin(angle)
            for radius,width,bottom,top in stations:
                for tangent,axial in [(-width,bottom),(width,bottom),(width,top-.0012),(width-.0013,top),(-width+.0013,top),(-width,top-.0012)]:
                    points.append((radius*c-tangent*s,sign*axial,.225+radius*s+tangent*c))
    return points


if root.get('asset_version')=='0.1.2':
    assert input_digest==PREDECESSOR,'Unexpected predecessor; inspect before editing.'
    for vertex,expected in zip(ribs.data.vertices,rib_points(old_stations)):
        assert max(abs(vertex.co[i]-expected[i]) for i in range(3))<1e-6,'Unexpected rib vertex order'
    for vertex,point in zip(ribs.data.vertices,rib_points(new_stations)):vertex.co=point
    ribs.data.update()
    ribs['radial_rows_m']=[row[0] for row in new_stations]
    ribs['half_widths_m']=[row[1] for row in new_stations]
    ribs['taper']='monotonic hub-to-rim width reduction'
    for obj in labels:
        sign=1 if obj['face']=='front' else -1
        text=obj['raised_text']
        glyph_centers=[]
        if text in ['STANDARD','BARBELL']:
            for index in range(len(text)):
                offset=math.radians(-24+48*index/(len(text)-1))
                angle=math.pi/2-offset if text=='STANDARD' else -math.pi/2+offset
                glyph_centers.append((.165*math.cos(angle),.165*math.sin(angle)))
        for vertex in obj.data.vertices:
            u=-sign*vertex.co.x;v=vertex.co.z-.225
            if text in ['45 LB','20.4 KG']:
                center_u=-.127 if text=='45 LB' else .127
                u=center_u+(u-center_u)*1.08;v*=1.08
            else:
                center_u,center_v=min(glyph_centers,key=lambda center:(center[0]-u)**2+(center[1]-v)**2)
                du,dv=(u-center_u)*1.08,(v-center_v)*1.08
                if text=='BARBELL':
                    # Reverse glyph positions on the same lower arc and rotate
                    # each glyph 180 degrees: inverted reading, not mirrored type.
                    u=-center_u-du;v=center_v-dv
                else:
                    u=center_u+du;v=center_v+dv
            vertex.co.x=-sign*u;vertex.co.z=.225+v
            # Axial coordinate remains unchanged: real 3.5 mm raised relief.
        obj.data.update()
        obj['planar_scale_relative_to_012']=1.08
        obj['orientation']='inverted_180_on_lower_arc' if text=='BARBELL' else 'upright'
    mat=bpy.data.materials[ID+'__material_lettering']
    srgb=242/255
    value=((srgb+.055)/1.055)**2.4
    mat.diffuse_color=(value,value,value,1)
    node=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value=(value,value,value,1)
    root['asset_version']=VERSION
    root['visual_direction']='approved for this plate by user, 2026-10-14; 0.1.3 execution pending review'
    root['finished_from_sha256']=PREDECESSOR
elif root.get('asset_version')!=VERSION:
    raise RuntimeError('Unsupported source revision')

assert pointers=={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
assert topologies=={m.name:topology(m) for m in bpy.data.meshes}
assert body_coordinates==coordinates(body.data)
assert anchor_matrices=={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}
assert scene.render.engine=='BLENDER_WORKBENCH' and scene.display.shading.light=='FLAT'
assert not scene.display.shading.show_shadows and not scene.display.shading.show_cavity and not bpy.data.lights
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),check_existing=False)
digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
script_digest=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
record={'version':VERSION,'predecessor_version':'0.1.2','predecessor_sha256':PREDECESSOR,
        'input_sha256':input_digest,'source_sha256':digest,'script_sha256':script_digest,
        'all_object_and_mesh_data_identity_preserved':True,'all_mesh_topology_preserved':True,
        'mesh_topology_sha256':topologies,'body_coordinates_unchanged':True,
        'body_coordinate_sha256':body_coordinates,'anchors_unchanged':True,
        'letter_face_srgb_hex':'F2F2F2','planar_letter_scale':1.08,
        'letter_exposed_relief_m':.0035,'barbell_orientation':'180-degree glyph rotation with reversed lower-arc placement on both faces',
        'rib_stations_m':new_stations,'rib_half_widths_m':[row[1] for row in new_stations],
        'visual_direction_approval':'User: Refine the approved 45 lb Olympic plate visual direction. Keep the current overall design and style. 2026-10-14.',
        'approval_scope':'this plate visual direction; not global standards or production/licensing acceptance'}
(ASSET/'finish-record.json').write_text(json.dumps(record,indent=2)+'\n')
settings.update(source_sha256=digest,asset_version=VERSION,preset='plate_review_flat@0.1.3',
                finish_script='scripts/blender/finish_olympic_plate_45lb.py',finish_script_sha256=script_digest,predecessor_sha256=PREDECESSOR)
settings['palette_srgb_hex']['lettering']='F2F2F2'
settings['material_versions']={key:VERSION for key in settings['material_versions']}
camdata=bpy.data.cameras.new(ID+'__camera_reference');cam=bpy.data.objects.new(ID+'__camera_reference',camdata)
scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO'
for view,config in settings['camera_views'].items():
    cam.location=config['position_m'];cam.rotation_euler=config['rotation_euler_xyz_radians'];cam.data.ortho_scale=config['ortho_scale_m']
    scene.render.filepath=str(REPO/config['path']);bpy.ops.render.render(write_still=True)
(ASSET/'previews/render-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
print('PLATE_APPROVED_DIRECTION_REFINEMENT_COMPLETE',digest)
