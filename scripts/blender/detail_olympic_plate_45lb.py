"""Add requested 0.1.2 cast ribs, dual-unit lettering and stepped side profile.
Refines the existing 0.1.1 body/data in place; it never calls the original builder.
Run in an isolated Blender 5.1.1 process. Rerunning 0.1.2 only rerenders.
"""
from pathlib import Path
import bpy, bmesh
import hashlib, json, math
from mathutils import Matrix, Vector

REPO=Path(__file__).resolve().parents[2]
ID='168h_equipment_olympic_plate_45lb_cast_iron'
ASSET=REPO/'assets/equipment/free_weights'/ID
SOURCE=ASSET/f'{ID}.blend'
VERSION='0.1.2'
PREDECESSOR='4cab3d6b487e1f9e45dd7548cce0a4d6c42efa56812e173948939b5ad8c7fe20'
settings=json.loads((ASSET/'previews/render-settings.json').read_text())
input_digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
root=bpy.data.objects[ID+'__root']
body=bpy.data.objects[ID+'__mesh_body']
geo=bpy.data.collections[ID+'__geo']
mesh=body.data
before_objects={o.name:o.as_pointer() for o in bpy.data.objects}
before_body_pointer=body.data.as_pointer()
anchors_before={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}
materials={key:bpy.data.materials[ID+'__material_'+key] for key in ['cast_iron','web','rim','hub','lettering']}
R=.225


def recalc(data):
    bm=bmesh.new();bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(data);bm.free();data.update()


def create_or_update_mesh(name,vertices,faces,matlist,raised_text=None):
    obj=bpy.data.objects.get(ID+'__mesh_'+name)
    if obj is None:
        data=bpy.data.meshes.new(ID+'__mesh_'+name+'_data')
        obj=bpy.data.objects.new(ID+'__mesh_'+name,data)
        geo.objects.link(obj)
    else:
        data=obj.data
        data.clear_geometry()
    data.from_pydata(vertices,[],faces)
    data.materials.clear()
    for mat in matlist:data.materials.append(mat)
    recalc(data)
    obj.parent=root
    obj.matrix_local=Matrix.Identity(4)
    if raised_text is not None:
        obj['raised_text']=raised_text
        obj['exposed_relief_m']=.0035
    return obj


def glyph_mesh(text,size,u,v,rotation,sign):
    curve=bpy.data.curves.new(ID+'__font_temporary','FONT')
    curve.body=text;curve.align_x='CENTER';curve.align_y='CENTER'
    curve.size=size;curve.extrude=.00175;curve.bevel_depth=.00015
    curve.bevel_resolution=2;curve.resolution_u=8
    obj=bpy.data.objects.new(ID+'__text_temporary',curve)
    geo.objects.link(obj)
    bpy.context.view_layer.objects.active=obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    data=bpy.context.object.data
    vertices=[]
    c,s=math.cos(rotation),math.sin(rotation)
    for vertex in data.vertices:
        x,y,z=vertex.co
        uu=u+c*x-s*y;vv=v+s*x+c*y
        vertices.append((-sign*uu,sign*(.0081+z),R+vv))
    faces=[tuple(p.vertices) for p in data.polygons]
    bpy.data.objects.remove(obj,do_unlink=True)
    bpy.data.meshes.remove(data)
    return vertices,faces


def lettering(name,text,size,u,v,sign,arc=None):
    verts=[];faces=[]
    parts=[]
    if arc:
        direction=1 if arc=='bottom' else -1
        center=-math.pi/2 if arc=='bottom' else math.pi/2
        spread=math.radians(24)
        for index,char in enumerate(text):
            offset=-spread+2*spread*index/(len(text)-1)
            angle=center+direction*offset
            # Upper word traverses left-to-right around the top semicircle;
            # lower word traverses left-to-right around the bottom.
            if arc=='top':angle=math.pi/2-offset
            parts.append(glyph_mesh(char,size,.165*math.cos(angle),.165*math.sin(angle),angle-center,sign))
    else:
        parts=[glyph_mesh(text,size,u,v,0,sign)]
    for pv,pf in parts:
        offset=len(verts);verts.extend(pv)
        faces.extend([tuple(i+offset for i in face) for face in pf])
    obj=create_or_update_mesh(name,verts,faces,[materials['lettering'],materials['cast_iron']],text)
    for p in obj.data.polygons:p.material_index=0 if sign*p.normal.y>.8 else 1
    obj['face']='front' if sign==1 else 'back'
    obj['layout']='arc_'+arc if arc else 'left_weight' if u<0 else 'right_weight'
    return obj


if root.get('asset_version')=='0.1.1':
    assert input_digest==PREDECESSOR,'Unexpected predecessor; inspect before editing.'
    assert len(mesh.vertices)==5120 and len(mesh.polygons)==5120
    # Locally subdivide only the old outer cylindrical side band. Existing
    # central bore, web, hub and rim topology/objects stay in place.
    bm=bmesh.new();bm.from_mesh(mesh)
    edges=[]
    for edge in bm.edges:
        a,b=edge.verts
        radii=[math.hypot(v.co.x,v.co.z-R) for v in edge.verts]
        if min(radii)>.2249 and a.co.y*b.co.y<0:
            edges.append(edge)
    assert len(edges)==256,len(edges)
    bmesh.ops.subdivide_edges(bm,edges=edges,cuts=3,use_grid_fill=True)
    for vertex in bm.verts:
        radius=math.hypot(vertex.co.x,vertex.co.z-R)
        if radius>.2249 and abs(vertex.co.y)<.0144:
            scale=.2235/radius
            vertex.co.x*=scale;vertex.co.z=R+(vertex.co.z-R)*scale
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(mesh);bm.free();mesh.update()
    for polygon in mesh.polygons:
        coords=[mesh.vertices[i].co for i in polygon.vertices]
        radius=sum(math.hypot(v.x,v.z-R) for v in coords)/len(coords)
        axial=sum(abs(v.y) for v in coords)/len(coords)
        if radius>.222 and axial<.0144:
            polygon.material_index=0 if axial<.0073 else 2
            polygon.use_smooth=True
    # Four diagonal ribs on each face, generated from one symmetric cast-rib
    # construction recipe. One published mesh holds the eight closed solids.
    verts=[];faces=[]
    rib_stations=[(.052,.009,.0135,.0149),(.070,.013,.0062,.012),
                  (.185,.013,.0062,.012),(.205,.010,.0135,.0160)]
    for sign in [1,-1]:
        for angle_deg in [45,135,225,315]:
            angle=math.radians(angle_deg);ca,sa=math.cos(angle),math.sin(angle)
            start=len(verts)
            for radius,width,bottom,top in rib_stations:
                cross=[(-width,bottom),(width,bottom),(width,top-.0012),
                       (width-.0013,top),(-width+.0013,top),(-width,top-.0012)]
                for tangent,axial in cross:
                    verts.append((radius*ca-tangent*sa,sign*axial,R+radius*sa+tangent*ca))
            faces.append(tuple(start+i for i in reversed(range(6))))
            for row in range(3):
                for j in range(6):
                    faces.append((start+row*6+j,start+row*6+(j+1)%6,start+(row+1)*6+(j+1)%6,start+(row+1)*6+j))
            faces.append(tuple(start+18+i for i in range(6)))
    ribs=create_or_update_mesh('ribs',verts,faces,[materials['web'],materials['cast_iron'],materials['rim']])
    for p in ribs.data.polygons:
        p.material_index=0 if abs(p.normal.y)>.8 else 1 if abs(p.normal.y)>.25 else 2
    ribs['rib_count_per_face']=4;ribs['angles_degrees']=[45,135,225,315]
    for sign,facing in [(1,'front'),(-1,'back')]:
        # Preserve both preexisting weight-label object and mesh datablocks.
        lettering('label_'+facing,'45 LB',.032,-.127,0,sign)
        lettering('label_kg_'+facing,'20.4 KG',.025,.127,0,sign)
        lettering('label_standard_'+facing,'STANDARD',.025,0,0,sign,arc='top')
        lettering('label_barbell_'+facing,'BARBELL',.025,0,0,sign,arc='bottom')
    for curve in list(bpy.data.curves):
        if curve.users==0:bpy.data.curves.remove(curve)
    for font in list(bpy.data.fonts):
        if font.users==0:bpy.data.fonts.remove(font)
    root['asset_version']=VERSION
    root['rib_count_per_face']=4
    root['lettering_layout']='45 LB left; 20.4 KG right; STANDARD top; BARBELL bottom; both faces'
    root['side_waist_radius_m']=.2235
    root['detailed_from_sha256']=PREDECESSOR
elif root.get('asset_version')!=VERSION:
    raise RuntimeError('Unsupported source revision')

assert body.data.as_pointer()==before_body_pointer
assert all(bpy.data.objects[name].as_pointer()==pointer for name,pointer in before_objects.items())
assert anchors_before=={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}
assert not bpy.data.lights and scene.render.engine=='BLENDER_WORKBENCH'
assert not scene.display.shading.show_shadows and not scene.display.shading.show_cavity
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),check_existing=False)
source_digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
record={'version':VERSION,'predecessor_version':'0.1.1','predecessor_sha256':PREDECESSOR,
        'source_sha256':source_digest,'input_sha256':input_digest,
        'existing_body_mesh_datablock_preserved':True,'existing_objects_preserved':True,
        'anchors_unchanged':True,'interface_unchanged':True,'body_topology_locally_extended':True,
        'body_vertices':len(mesh.vertices),'body_faces':len(mesh.polygons),
        'side_waist_radius_m':.2235,'rib_stations_m':rib_stations if 'rib_stations' in globals() else 'unchanged from source',
        'ribs_per_face':4,'rib_angles_degrees':[45,135,225,315],
        'lettering_layout':root['lettering_layout'],
        'script':'scripts/blender/detail_olympic_plate_45lb.py',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'shared_standards_changed':False}
(ASSET/'detail-record.json').write_text(json.dumps(record,indent=2)+'\n')
settings.update(source_sha256=source_digest,asset_version=VERSION,preset='plate_review_flat@0.1.2',
                detail_script=record['script'],detail_script_sha256=record['script_sha256'],
                predecessor_sha256=PREDECESSOR)
settings['material_versions']={key:VERSION for key in settings['material_versions']}
settings['outlines']['edge_definition']='Native silhouettes and flat charcoal separation on raised ribs, hub/rim bevels, waist and real extruded letter sides; no shadows/AO.'
camdata=bpy.data.cameras.new(ID+'__camera_reference')
cam=bpy.data.objects.new(ID+'__camera_reference',camdata)
scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO'
for view,config in settings['camera_views'].items():
    cam.location=config['position_m'];cam.rotation_euler=config['rotation_euler_xyz_radians']
    cam.data.ortho_scale=config['ortho_scale_m']
    scene.render.filepath=str(REPO/config['path'])
    bpy.ops.render.render(write_still=True)
(ASSET/'previews/render-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
print('PLATE_CAST_DETAIL_COMPLETE',source_digest,record['body_vertices'],record['body_faces'])
