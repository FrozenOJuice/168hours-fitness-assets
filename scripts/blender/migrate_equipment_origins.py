"""A14 authorized root/pivot migration. Preserve native world geometry; no modeling."""
from pathlib import Path
import bpy,json,hashlib,sys
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[2];ARCH=R/'docs/audits/origin_baseline'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def datahash(o):
    return hashlib.sha256(json.dumps({'v':[list(v.co) for v in o.data.vertices],'p':[list(p.vertices) for p in o.data.polygons],'slots':[p.material_index for p in o.data.polygons],'materials':[m.name for m in o.data.materials]},separators=(',',':')).encode()).hexdigest()
def matrix_error(a,b):return max(abs(a[i][j]-b[i][j]) for i in range(4) for j in range(4))
if __name__=='__main__':
    records=[];offsets={}
    manifests=[p for p in (R/'assets/equipment').rglob('asset.json') if 'history' not in p.parts]
    for p in manifests:
        m=json.loads(p.read_text());profile=m['origin_contract']['profile']
        if profile=='flat_bench':continue
        src=R/m['source'];old=ARCH/m['source'];assert sha(src)==sha(old),'Migration only accepts archived predecessor'
        bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update();c=bpy.data.collections[m['collection']];root=bpy.data.objects[m['root']]
        key='bore_center' if profile=='olympic_plate' else 'axis_center'
        datum=bpy.data.objects[m['anchors'][key]['object']].matrix_world.translation.copy()
        oldoffset=c.instance_offset.copy();world={o.name:o.matrix_world.copy() for o in c.all_objects if o!=root};hashes={o.name:datahash(o) for o in c.all_objects if o.type=='MESH'}
        root.location=datum;bpy.context.view_layer.update()
        for o in list(root.children):
            o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_world=world[o.name]
        c.instance_offset=datum;bpy.context.view_layer.update()
        errors={o.name:matrix_error(o.matrix_world,world[o.name]) for o in c.all_objects if o!=root}
        assert max(errors.values())<1e-6,errors
        assert hashes=={o.name:datahash(o) for o in c.all_objects if o.type=='MESH'}
        root['geometry_version']=root.get('asset_version');root['asset_version']='1.0.0';root['origin_interface_version']='1.0.0'
        inv=root.matrix_world.inverted()
        for entry in m['anchors'].values():
            o=bpy.data.objects[entry['object']];frame=inv@o.matrix_world;entry['position_m']=list(frame.translation);entry['rotation_euler_xyz_radians']=list(frame.to_euler('XYZ'))
        m['origin_contract']['authoring_root_position_m']=list(datum);m['origin_contract']['collection_instance_offset_m']=list(datum)
        m['version']='1.0.0';m['geometry_version']=root['geometry_version']
        for interface in m.get('interfaces',[]):interface['version']='1.0.0'
        m['origin_migration']={'decision':'A14','status':'approved_applied','date':'2026-10-15','predecessor_source':str(old.relative_to(R)),'predecessor_sha256':sha(old),'world_geometry_changed':False,'breaking_origin_interface':True,'consumer_compensation':'M_new=M_old@Translation(new_collection_offset-old_collection_offset)'}
        bpy.ops.wm.save_as_mainfile(filepath=str(src),compress=True);m['source_revision_or_digest']='sha256:'+sha(src);dump(p,m)
        offsets[m['collection']]=list(datum-oldoffset)
        records.append({'source':m['source'],'predecessor_sha256':sha(old),'source_sha256':sha(src),'new_root_m':list(datum),'new_offset_m':list(c.instance_offset),'component_world_matrix_max_error':max(errors.values()),'mesh_data_material_slot_hashes':hashes,'world_geometry_preserved':True})
    # Compensation uses each old saved instance matrix; source libraries now have new offsets.
    for p in sorted((R/'scenes').rglob('*.blend')):
        old=ARCH/p.relative_to(R)
        if not old.exists():continue
        assert sha(p)==sha(old)
        bpy.ops.wm.open_mainfile(filepath=str(p));changes=[]
        for o in bpy.context.scene.objects:
            if o.instance_type=='COLLECTION' and o.instance_collection.name in offsets:
                before=o.matrix_world.copy();delta=Vector(offsets[o.instance_collection.name]);o.matrix_world=before@Matrix.Translation(delta)
                changes.append({'instance':o.name,'delta_source_m':list(delta),'old_matrix':[list(row) for row in before],'new_matrix':[list(row) for row in o.matrix_world]})
        bpy.context.view_layer.update()
        for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(p.parent))
        bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
        records.append({'source':str(p.relative_to(R)),'predecessor_sha256':sha(old),'source_sha256':sha(p),'instance_compensations':changes})
    dump(R/'docs/audits/origin-migration-record.json',{'decision':'A14','date':'2026-10-15','approved_by':'user explicit migration approval','records':records,'script_sha256':sha(Path(__file__))})
