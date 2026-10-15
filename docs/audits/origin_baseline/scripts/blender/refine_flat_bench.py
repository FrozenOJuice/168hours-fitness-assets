"""Refine saved prototype in place; retains original objects/data. MIT code, artwork separate."""
from pathlib import Path
import bpy, math, json, sys
from mathutils import Vector, Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_flat_bench import ID,ASSET,SOURCE,REPO
from barbell_20kg_common import digest,write_json

def rounded_loop(w,l,r,segments=16):
    points=[]
    for cx,cy,start in [(w-r,l-r,0),(-w+r,l-r,90),(-w+r,-l+r,180),(w-r,-l+r,270)]:
        for k in range(segments):
            t=math.radians(start+k*90/(segments-1));points.append((cx+r*math.cos(t),cy+r*math.sin(t)))
    return points

def roles(group):
    names={'frame':['frame_body','frame_top','frame_side'],'padding':['padding_top','padding_side','padding_edge'],'grip':['grip_body','grip_top','grip_side']}
    return [bpy.data.materials[ID+'__material_'+k] for k in names[group]]

def assign(mesh,group):
    if not mesh.materials:
        for m in roles(group):mesh.materials.append(m)
    mesh.update()
    for p in mesh.polygons:
        p.material_index=(0 if p.normal.z>.98 else 2 if abs(p.normal.z)>.12 else 1) if group=='padding' else (1 if p.normal.z>.5 else 2 if abs(p.normal.x)>.5 else 0)

def obj(part,mesh,loc=(0,0,0)):
    o=bpy.data.objects.new(ID+'__mesh_'+part,mesh);geo.objects.link(o);o.parent=root;o.location=loc;return o

def solid(part,verts,faces,group='frame',bevel=0):
    mesh=bpy.data.meshes.new(ID+'__geometry_'+part);mesh.from_pydata(verts,[],faces);mesh.update();o=obj(part,mesh)
    if bevel:
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
        m=o.modifiers.new('physical_edge_rounding','BEVEL');m.width=bevel;m.segments=6;bpy.ops.object.modifier_apply(modifier=m.name)
    import bmesh
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    assign(o.data,group);return o

def block(part,dims,loc,bevel=.001):
    x,y,z=[v/2 for v in dims]
    verts=[(a,b,c) for c in [-z,z] for a,b in [(-x,-y),(x,-y),(x,y),(-x,y)]]
    o=solid(part,verts,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],bevel=bevel);o.location=loc;return o

def ring_solid(mesh,profile):
    n=64;verts=[]
    for z,w,l,r in profile:verts.extend((x,y,z) for x,y in rounded_loop(w,l,r))
    faces=[tuple(reversed(range(n)))]
    for row in range(len(profile)-1):
        for k in range(n):
            j=(k+1)%n;faces.append((row*n+k,row*n+j,(row+1)*n+j,(row+1)*n+k))
    faces.append(tuple((len(profile)-1)*n+k for k in range(n)))
    mesh.clear_geometry();mesh.from_pydata(verts,[],faces);mesh.update()

def fastener(part,axis):
    # Solid stepped washer + hex head; shared data, no imported bolts or textures.
    n=48;profiles=[(-.0035,.0058,'hex'),(0,.0058,'hex'),(0,.009,'round'),(.0018,.009,'round')]
    verts=[]
    for z,r,shape in profiles:
        for k in range(n):
            theta=2*math.pi*k/n
            if shape=='hex':r0=r*math.cos(math.pi/6)/math.cos((theta%(math.pi/3))-math.pi/6)
            else:r0=r
            p=Vector((r0*math.cos(theta),r0*math.sin(theta),z))
            if axis=='X':p=Matrix.Rotation(math.pi/2,3,'Y')@p
            verts.append(p)
    faces=[tuple(reversed(range(n)))]
    for row in range(3):
        for k in range(n):faces.append((row*n+k,row*n+(k+1)%n,(row+1)*n+(k+1)%n,(row+1)*n+k))
    faces.append(tuple(3*n+k for k in range(n)))
    return solid(part,verts,faces,bevel=.00025)

if __name__=='__main__':
    plan=json.loads((ASSET/'refinement-plan.json').read_text());assert digest(SOURCE)==plan['predecessor_sha256'],'Refine only the recorded predecessor; do not rerun blindly.'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));col=bpy.data.collections[ID];geo=bpy.data.collections[ID+'__geo'];root=bpy.data.objects[ID+'__root']
    old={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in col.all_objects}
    frames={o.name:[list(row) for row in o.matrix_basis] for o in col.all_objects if o.type=='EMPTY'}
    untouched={o.name: [tuple(v.co) for v in o.data.vertices] for o in col.all_objects if o.type=='MESH' and not (o.name.endswith('__mesh_pad') or '__mesh_rubber_' in o.name)}
    pad=bpy.data.objects[ID+'__mesh_pad'];assert len(pad.data.vertices)==18*64
    rings=[(.3937,.006),(.3945,.003),(.396,.001),(.3997,0),(.411,0),(.412,.0006),(.4128,.0006),(.4138,0),(.435,0),(.4432,0)]
    rings.extend((.4432+.014*math.sin(k*math.pi/16),.014*(1-math.cos(k*math.pi/16))) for k in range(1,9))
    for row,(z,inset) in enumerate(rings):
        for k,(x,y) in enumerate(rounded_loop(.1524-inset,.5969-inset,.030-inset)):
            pad.data.vertices[row*64+k].co=(x,y,z)
    assign(pad.data,'padding')
    # Actual near-flush piping follows the rolled shoulder, wholly inside nominal envelope.
    points=rounded_loop(.1524-.0019,.5969-.0019,.030-.0019,32);n=len(points);verts=[];tube=.0006
    for i,(x,y) in enumerate(points):
        prev=Vector(points[(i-1)%n]);nxt=Vector(points[(i+1)%n]);t=(nxt-prev).normalized();normal=Vector((t.y,-t.x))
        for k in range(8):
            theta=2*math.pi*k/8;verts.append((x+tube*normal.x*math.cos(theta),y+tube*normal.y*math.cos(theta),.4492+tube*math.sin(theta)))
    faces=[]
    for i in range(n):
        for k in range(8):faces.append((i*8+k,((i+1)%n)*8+k,((i+1)%n)*8+(k+1)%8,i*8+(k+1)%8))
    seam=solid('upholstery_seam',verts,faces,'padding')
    for p in seam.data.polygons:p.material_index=2
    boots=[o for o in col.all_objects if '__mesh_rubber_' in o.name];mesh=boots[0].data
    profile=[(-.0325,.0348,.0395,.010),(-.0305,.0378,.0425,.012),(-.0245,.0378,.0425,.012),(-.0225,.0368,.0415,.012),(.0255,.0338,.0405,.010),(.0315,.0328,.0395,.010)]
    ring_solid(mesh,profile);assign(mesh,'grip')
    # Triangular gussets seat against both main spine and sloped leg sides.
    for end,sign in [('head',1),('foot',-1)]:
        yz=[(sign*.27,.331),(sign*.389,.331),(sign*.410,.255)]
        if sign<0:yz.reverse()
        verts=[(x,y,z) for x in [-.003,.003] for y,z in yz]
        gusset=solid('gusset_'+end+'_l',verts,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],bevel=.0015)
        gusset.location.x=.0274
        obj('gusset_'+end+'_r',gusset.data,(-.0274,0,0))
    plate=block('mount_cheek_head_l',(.006,.064,.064),(.0294,.34,.349),.0015)
    for end,y in [('head',.34),('foot',-.34)]:
        for side,x in [('l',.0294),('r',-.0294)]:
            if end=='head' and side=='l':continue
            obj('mount_cheek_'+end+'_'+side,plate.data,(x,y,.349))
    bolt=fastener('pad_bolt_head_l','Z');bolt.location=(.092,.34,.3538)
    for end,y in [('head',.34),('foot',-.34)]:
        for side,x in [('l',.092),('r',-.092)]:
            if end=='head' and side=='l':continue
            obj('pad_bolt_'+end+'_'+side,bolt.data,(x,y,.3538))
    # Cross bolt heads mirrored by vertex-space transformation into a second shared mesh.
    cross=fastener('cross_bolt_head_r','X');cross.location=(-.0342,.34,.349)
    mirror=cross.data.copy();mirror.name=ID+'__geometry_cross_bolt_l'
    for v in mirror.vertices:v.co.x=-v.co.x
    # Reflection reverses winding; restore outward normals.
    import bmesh
    bm=bmesh.new();bm.from_mesh(mirror);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(mirror);bm.free()
    obj('cross_bolt_foot_r',cross.data,(-.0342,-.34,.349))
    obj('cross_bolt_head_l',mirror,(.0342,.34,.349));obj('cross_bolt_foot_l',mirror,(.0342,-.34,.349))
    bpy.context.view_layer.update()
    preserved=all((bpy.data.objects[n].as_pointer(),bpy.data.objects[n].data.as_pointer() if bpy.data.objects[n].data else None)==v for n,v in old.items())
    assert preserved
    assert all([list(row) for row in bpy.data.objects[n].matrix_basis]==m for n,m in frames.items())
    assert all([tuple(v.co) for v in bpy.data.objects[n].data.vertices]==vs for n,vs in untouched.items())
    root['asset_version']='0.1.1'
    for o in col.all_objects:
        if o.type=='EMPTY':o.hide_set(True)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
    meshes=[o for o in col.all_objects if o.type=='MESH']
    write_json(ASSET/'refinement-record.json',{'version':'0.1.1','predecessor_sha256':plan['predecessor_sha256'],'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'original_objects_and_data_identity_preserved':preserved,'anchors_transforms_preserved':True,'main_frame_substrate_vertices_preserved':True,'original_pad_topology_preserved':True,'rubber_shared_data_retained_topology_changed':True,'added_objects':[o.name for o in col.all_objects if o.name not in old],'mesh_objects':len(meshes),'unique_mesh_data':len({o.data for o in meshes}),'materials':{o.name:[m.name for m in o.data.materials] for o in meshes},'blender_version':bpy.app.version_string})
    print('BENCH_REFINEMENT_COMPLETE',len(meshes),digest(SOURCE))
