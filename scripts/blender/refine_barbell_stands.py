"""In-place0.1.1 hook/lock refinement; retain source objects, frames and shared data."""
from pathlib import Path
import bpy,bmesh,sys,json,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_barbell_stands import R,ID,A,SOURCE
from build_stands_review_assembly import F,OUT
from barbell_20kg_common import digest,write_json

def replace(part,verts,faces):
    o=bpy.data.objects[ID+'__mesh_'+part+'_l'];inv=o.matrix_basis.inverted();mesh=o.data
    slots=list(mesh.materials);mesh.clear_geometry();mesh.from_pydata([inv@Vector(v) for v in verts],[],faces);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update()
    assert list(mesh.materials)==slots
    for p in mesh.polygons:p.material_index=1 if p.normal.z>.4 else 2 if abs(p.normal.x)>.5 else 0
    return o

def profile(part,points,width):
    n=len(points);verts=[(x,y,z) for x in [-width/2,width/2] for y,z in points];faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return replace(part,verts,faces)

def box(part,x0,x1,y0,y1,z0,z1):
    v=[(x,y,z) for z in [z0,z1] for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]];return replace(part,v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])

def rod(verts,faces,center,radius,length,axis='X',n=48):
    start=len(verts);c=Vector(center);d=Vector((1,0,0) if axis=='X' else (0,1,0));u=Vector((0,1,0) if axis=='X' else (1,0,0));v=d.cross(u)
    for h in [-length/2,length/2]:
        for i in range(n):verts.append(tuple(c+d*h+radius*(math.cos(i*2*math.pi/n)*u+math.sin(i*2*math.pi/n)*v)))
    faces.extend([tuple(start+i for i in reversed(range(n))),tuple(start+n+i for i in range(n))]);faces.extend((start+i,start+(i+1)%n,start+(i+1)%n+n,start+i+n) for i in range(n))

def wire(verts,faces,points,radius,closed=False,n=12):
    start=len(verts);ps=[Vector(p) for p in points];count=len(ps)
    for i,p in enumerate(ps):
        tangent=ps[(i+1)%count]-ps[(i-1)%count] if closed else ps[min(i+1,count-1)]-ps[max(0,i-1)]
        tangent.normalize();u=Vector((1,0,0));u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u)
        for k in range(n):verts.append(tuple(p+radius*(math.cos(k*2*math.pi/n)*u+math.sin(k*2*math.pi/n)*v)))
    for i in range(count if closed else count-1):
        for k in range(n):faces.append((start+i*n+k,start+i*n+(k+1)%n,start+((i+1)%count)*n+(k+1)%n,start+((i+1)%count)*n+k))
    if not closed:faces.extend([tuple(start+k for k in reversed(range(n))),tuple(start+(count-1)*n+k for k in range(n))])

def drill(o,radius,length,center,axis):
    # Work on temporary data and transfer back to retain original shared mesh identity.
    tmp=bpy.data.objects.new('temporary_machining',o.data.copy());bpy.context.scene.collection.objects.link(tmp);tmp.matrix_world=o.matrix_world.copy()
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=length,location=center);c=bpy.context.object
    c.rotation_euler=(math.pi/2,0,0) if axis=='Y' else (0,0,0)
    bpy.ops.object.select_all(action='DESELECT');tmp.select_set(True);bpy.context.view_layer.objects.active=tmp
    mod=tmp.modifiers.new('through_drill','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name)
    bm=bmesh.new();bm.from_mesh(tmp.data);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    data=tmp.data;bpy.data.objects.remove(tmp,do_unlink=True);bpy.data.meshes.remove(data);bpy.data.objects.remove(c,do_unlink=True)
    for p in o.data.polygons:p.material_index=1 if p.normal.z>.4 else 2 if abs(p.normal.x)>.5 else 0

if __name__=='__main__':
    plan=json.loads((A/'refinement-plan.json').read_text());assert digest(SOURCE)==plan['predecessor_sha256'],'Exact predecessor required; never rerun on successor'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));col=bpy.data.collections[ID];root=col.all_objects[ID+'__root'];bpy.context.view_layer.update()
    before={o.name:{'matrix':[list(row) for row in o.matrix_basis],'data':o.data.name if o.type=='MESH' else None,'vertices':[tuple(v.co) for v in o.data.vertices] if o.type=='MESH' else None,'slots':[m.name for m in o.data.materials] if o.type=='MESH' else None} for o in col.all_objects}
    # Concave protected saddle with a ramped lead-in; existing contact frame unchanged.
    arc=[(.14+.02*math.sin(t),.948-.02*math.cos(t)) for t in [(-1.1+i*2.2/32) for i in range(33)]]
    top=[(.050,.950),(.100,.950),*arc,(.180,.952),(.195,.963),(.202,.970)]
    angles=[-1.1+i*2.2/32 for i in range(33)]
    underside=lambda radius,offset:[(y,z-offset) for y,z in top[:2]]+[(.14+radius*math.sin(t),.948-radius*math.cos(t)) for t in angles]+[(y,z-offset) for y,z in top[-3:]]
    liner_bottom=underside(.026,.006);steel_bottom=underside(.036,.016)
    profile('hook_shelf',steel_bottom+list(reversed(liner_bottom)),.060)
    profile('hook_liner',liner_bottom+list(reversed(top)),.058)
    box('hook_back',-.030,.030,.030,.054,.898,1.048)
    box('hook_back_liner',-.029,.029,.054,.060,.950,1.034)
    profile('hook_lip',[(.195,.936),(.222,.951),(.222,.969),(.216,.975),(.208,.975),(.198,.967)],.060)
    profile('hook_lip_liner',[(.198,.965),(.208,.975),(.216,.975),(.216,.979),(.207,.979),(.194,.966)],.058)
    # Actual transverse fastener through inner tube, not a sideways decorative cylinder.
    verts=[];faces=[];rod(verts,faces,(0,.009,.994),.004,.096,'Y');rod(verts,faces,(0,.060,.994),.0085,.003,'Y');rod(verts,faces,(0,.065,.994),.0075,.007,'Y',6);rod(verts,faces,(0,-.041,.994),.0075,.008,'Y',6);replace('hook_fastener',verts,faces)
    inner=col.all_objects[ID+'__mesh_upright_inner_l'];drill(inner,.0045,.10,(.55,0,.994),'Y')
    # Keep published5/8in shaft and real17mm detent openings; chamfer its inserted end.
    verts=[];faces=[];n=64
    for x,radius in [(-.085,.0068),(-.083,.0079375),(.083,.0079375),(.085,.0072)]:
        for k in range(n):verts.append((x,radius*math.cos(k*2*math.pi/n),.90+radius*math.sin(k*2*math.pi/n)))
    faces=[tuple(reversed(range(n))),tuple(3*n+k for k in range(n))]+[(i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k) for i in range(3) for k in range(n)]
    pin=replace('adjustment_pin',verts,faces);drill(pin,.00175,.04,(.55-.060,0,.900),'Z')
    verts=[];faces=[];rod(verts,faces,(.077,0,.90),.015,.010);replace('pin_washer',verts,faces)
    verts=[];faces=[];pts=[(.103,.017*math.cos(t),.9+.022*math.sin(t)) for t in [-math.pi/2+i*math.pi/32 for i in range(33)]];wire(verts,faces,pts,.0028,True);rod(verts,faces,(.092,0,.9),.0045,.022);replace('pin_grip',verts,faces)
    verts=[];faces=[];pts=[(-.060,0,.878),(-.060,0,.918),(-.060,.002,.923),(-.060,.007,.926),(-.060,.014,.924),(-.060,.018,.918),(-.060,.017,.908),(-.060,.010,.894),(-.060,.011,.884)];wire(verts,faces,pts,.0012);replace('pin_retainer',verts,faces)
    # Stepped polymer guide covers the steel top and centers the inner tube.
    o=box('polymer_guide',-.043,.043,-.043,.043,.948,.978);drill_tmp=bpy.data.objects.new('guide_cutter',None)
    # Hollow square guide via temporary Boolean, preserving original group/slots.
    tmp=bpy.data.objects.new('temporary_guide',o.data.copy());bpy.context.scene.collection.objects.link(tmp);tmp.matrix_world=o.matrix_world.copy()
    bpy.ops.mesh.primitive_cube_add(size=1,location=(.55,0,.963));c=bpy.context.object;c.dimensions=(.061,.061,.06);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bpy.ops.object.select_all(action='DESELECT');tmp.select_set(True);bpy.context.view_layer.objects.active=tmp;mod=tmp.modifiers.new('guide_opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name)
    bm=bmesh.new();bm.from_mesh(tmp.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update();d=tmp.data;bpy.data.objects.remove(tmp,do_unlink=True);bpy.data.meshes.remove(d);bpy.data.objects.remove(c,do_unlink=True);bpy.data.objects.remove(drill_tmp)
    for p in o.data.polygons:p.material_index=1 if p.normal.z>.4 else 2 if abs(p.normal.x)>.5 else 0
    changed=[]
    for o in col.all_objects:
        b=before[o.name];assert [list(row) for row in o.matrix_basis]==b['matrix'],o.name
        if o.type=='MESH':
            assert o.data.name==b['data'] and [m.name for m in o.data.materials]==b['slots'],o.name
            if [tuple(v.co) for v in o.data.vertices]!=b['vertices']:changed.append(o.name)
    root['asset_version']='0.1.1';bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
    meta=json.loads((A/'asset.json').read_text());meta['source_revision_or_digest']='sha256:'+digest(SOURCE);meta['refinement']['status']='implemented; QA pending';write_json(A/'asset.json',meta)
    write_json(A/'refinement-record.json',{'version':'0.1.1','predecessor_sha256':plan['predecessor_sha256'],'source_sha256':digest(SOURCE),'refiner_sha256':digest(Path(__file__)),'changed_geometry_objects':changed,'preserved_objects':len(before),'preserved_shared_mesh_data':32,'origins_matrices_slots_preserved':True,'source_rebuilt':False})
    # Open existing fixture and preserve its placements; relative links remain intact.
    bpy.ops.wm.open_mainfile(filepath=str(OUT));bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True,relative_remap=False)
    for name in ['asset.json','build-record.json']:
        p=F/name;j=json.loads(p.read_text());j['version']='0.1.1';j['source_revision_or_digest']='sha256:'+digest(OUT);j['source_sha256']=digest(OUT)
        for dep in j['dependencies']:
            if dep['id']==ID:dep.update(version='0.1.1',sha256=digest(SOURCE))
        write_json(p,j)
    print('STANDS_REFINED',len(changed),'geometry objects; original objects/data/frames retained')
