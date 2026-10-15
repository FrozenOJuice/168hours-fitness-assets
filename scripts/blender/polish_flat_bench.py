"""User-authorized 0.1.2 in-place cap/bracket/contrast refinement. MIT code."""
from pathlib import Path
import sys,json,bpy,bmesh
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_flat_bench import ID,ASSET,SOURCE,REPO
from refine_flat_bench import rounded_loop
from barbell_20kg_common import digest,write_json

def cap(mesh,sign):
    n=64;verts=[]
    # External rounded YZ profile with short axial coverage and beveled ends.
    for x,inset in [(.0118,.002),(.0148,0),(.0348,0),(.0378,.003)]:
        verts.extend((sign*x,y,z-.0005) for y,z in rounded_loop(.0425-inset,.032-inset,.003))
    # Socket opening and closed inner stop, clearance around the existing steel tube.
    for x in [.0118,.0298]:
        verts.extend((sign*x,y,z+.0029) for y,z in rounded_loop(.0383,.0256,.0015))
    faces=[]
    for row in range(3):
        for k in range(n):faces.append((row*n+k,row*n+(k+1)%n,(row+1)*n+(k+1)%n,(row+1)*n+k))
    faces.append(tuple(3*n+k for k in range(n)))
    for k in range(n):
        j=(k+1)%n
        faces.append((k,4*n+k,4*n+j,j))
        faces.append((4*n+k,5*n+k,5*n+j,4*n+j))
    faces.append(tuple(reversed([5*n+k for k in range(n)])))
    mesh.clear_geometry();mesh.from_pydata(verts,[],faces);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    for p in mesh.polygons:p.material_index=1 if p.normal.z>.5 else 2 if p.normal.z<-.5 else 0

if __name__=='__main__':
    plan=json.loads((ASSET/'visual-refinement-plan.json').read_text());assert digest(SOURCE)==plan['predecessor_sha256'],'Refine recorded predecessor only; do not rerun blindly.'
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));bpy.context.view_layer.update();col=bpy.data.collections[ID]
    objects=list(col.all_objects);pointers={o.name:o.as_pointer() for o in objects};matrices={o.name:o.matrix_world.copy() for o in objects}
    before_coords={o.name:[tuple(v.co) for v in o.data.vertices] for o in objects if o.type=='MESH'}
    original_colors={m.name:list(m.diffuse_color) for m in bpy.data.materials}
    boots=[o for o in objects if '__mesh_rubber_' in o.name]
    left=boots[0].data;right=left.copy();right.name=ID+'__geometry_rubber_end_cap_r'
    cap(left,1);cap(right,-1)
    for o in boots:o.data=left if o.name.endswith('_l') else right
    cheeks=[o for o in objects if '__mesh_mount_cheek_' in o.name]
    for v in cheeks[0].data.vertices:v.co.y*=54/64;v.co.z=v.co.z*(56/64)+.004
    cheeks[0].data.update()
    main=[o for o in objects if o.type=='MESH' and any(o.name.endswith('__mesh_'+k) for k in ['spine','leg_head','leg_foot','foot_head','foot_foot','mount_rail_head','mount_rail_foot'])]
    for mesh in {o.data for o in main}:
        for p in mesh.polygons:p.material_index=1 if p.normal.z>.5 else 2 if p.normal.z<-.5 else 0
    for p in cheeks[0].data.polygons:p.material_index=1 if abs(p.normal.x)>.5 else 0 if p.normal.z>.5 else 2
    bpy.context.view_layer.update()
    assert original_colors=={m.name:list(m.diffuse_color) for m in bpy.data.materials}
    assert all(o.as_pointer()==pointers[o.name] and o.matrix_world==matrices[o.name] for o in objects)
    changed_geometry=[o.name for o in objects if o.type=='MESH' and before_coords[o.name]!=[tuple(v.co) for v in o.data.vertices]]
    assert set(changed_geometry)=={o.name for o in boots+cheeks}
    bpy.data.objects[ID+'__root']['asset_version']='0.1.2'
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
    write_json(ASSET/'visual-refinement-record.json',{'version':'0.1.2','source_sha256':digest(SOURCE),'predecessor_sha256':plan['predecessor_sha256'],'script_sha256':digest(Path(__file__)),'all_object_identities_and_frames_preserved':True,'all_material_datablocks_colors_and_nodes_preserved':True,'changed_geometry_objects':changed_geometry,'mesh_objects':len([o for o in objects if o.type=='MESH']),'unique_mesh_data':len({o.data for o in objects if o.type=='MESH'}),'rubber_cap_variants':{'left':left.name,'right':right.name,'each_shared_by':2},'cap_outer_dimensions_m':[.026,.085,.064],'cap_socket_dimensions_m':[.018,.0766,.0512],'cheek_dimensions_m':[.006,.054,.056]})
    print('BENCH_POLISH_COMPLETE',digest(SOURCE))
