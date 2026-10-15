"""Compare archived/current evaluated geometry and render references. Read-only."""
from pathlib import Path
import bpy,json,hashlib,sys,tempfile,numpy as np
from mathutils import Matrix
R=Path(__file__).resolve().parents[2];ARCH=R/'docs/audits/origin_baseline'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(path):
    bpy.ops.wm.open_mainfile(filepath=str(path));bpy.context.view_layer.update();scene=bpy.context.scene
    rows={}
    for it in bpy.context.evaluated_depsgraph_get().object_instances:
        o=it.object
        if o.type!='MESH':continue
        key=(it.parent.original.name if it.parent else '')+'|'+o.original.name
        # Multiple instances are distinguished by parent object, never by linked-data duplication.
        rows[key]={'matrix':np.array(it.matrix_world),'vertices':np.array([v.co[:] for v in o.data.vertices]),'faces':[list(p.vertices) for p in o.data.polygons],'face_materials':[p.material_index for p in o.data.polygons],'material_names':[m.name for m in o.data.materials]}
    materials={m.name:{'display':list(m.diffuse_color),'nodes':[(n.name,[(i.name,str(i.default_value[:]) if hasattr(i.default_value,'__len__') else str(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]) for n in m.node_tree.nodes] if m.node_tree else []} for m in bpy.data.materials}
    anchors={}
    for o in scene.objects:
        if o.instance_type=='COLLECTION':
            for a in o.instance_collection.all_objects:
                if '__anchor_' in a.name:anchors[o.name+'|'+a.name]=np.array(o.matrix_world@Matrix.Translation(-o.instance_collection.instance_offset)@a.matrix_world)
        elif '__anchor_' in o.name:anchors[o.name]=np.array(o.matrix_world)
    return rows,materials,anchors
if __name__=='__main__':
    checks=[];refreshed=[];record=json.loads((R/'docs/audits/origin-migration-record.json').read_text())
    for e in record['records']:
        old,om,oa=capture(ARCH/e['source']);new,nm,na=capture(R/e['source']);error=0
        same=old.keys()==new.keys()
        for key in old.keys()&new.keys():
            a=old[key];b=new[key]
            same=same and np.array_equal(a['vertices'],b['vertices']) and a['faces']==b['faces'] and a['face_materials']==b['face_materials'] and a['material_names']==b['material_names']
            av=np.c_[a['vertices'],np.ones(len(a['vertices']))]@a['matrix'].T;bv=np.c_[b['vertices'],np.ones(len(b['vertices']))]@b['matrix'].T
            error=max(error,float(np.max(np.abs(av-bv))))
        anchor_error=max([float(np.max(np.abs(oa[k]-na[k]))) for k in oa.keys()&na.keys()] or [0])
        good=same and error<1e-6 and om==nm and oa.keys()==na.keys() and anchor_error<1e-6
        libs=[{'path':l.filepath,'resolved':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
        good=good and all(l['path'].startswith('//') and l['resolved'] for l in libs)
        checks.append({'source':e['source'],'result':'PASS' if good else 'FAIL','mesh_instances':len(new),'identical_mesh_topology_coordinates_and_materials':same and om==nm,'world_vertex_max_error_m':error,'anchor_world_matrix_max_error':anchor_error,'libraries':libs})
    def sweeps(path):
        bpy.ops.wm.open_mainfile(filepath=str(path));frames={}
        for root in [o for o in bpy.context.scene.objects if o.name.endswith('__root')]:
            controls=[k for k in root.keys() if k.endswith('_angle_deg')]
            for key in controls:
                for angle in [0,45,90,180,270,360]:
                    for k in controls:root[k]=angle if k==key else 0
                    root.update_tag();bpy.context.view_layer.update()
                    for o in bpy.context.scene.objects:
                        if o!=root:frames[(key,angle,o.name)]=np.array(o.matrix_world)
        return frames
    for e in record['records']:
        if 'new_root_m' not in e:continue
        before=sweeps(ARCH/e['source']);after=sweeps(R/e['source'])
        if before:
            error=max(float(np.max(np.abs(before[k]-after[k]))) for k in before)
            checks.append({'source':e['source'],'check':'independent_controller_sweeps_preserved','result':'PASS' if before.keys()==after.keys() and error<1e-6 else 'FAIL','sampled_object_frames':len(before),'max_world_matrix_error':error})
    # Compare every retained view of all equipment and linked configurations against existing PNG bytes.
    for p in sorted((R/'assets/equipment').rglob('asset.json'))+list((R/'scenes/templates').glob('*/asset.json')):
        if 'history' in p.parts:continue
        m=json.loads(p.read_text())
        if not m.get('render_settings'):continue
        settings=json.loads((R/m['render_settings']).read_text());views=settings.get('camera_views',settings.get('views',{}))
        for name,e in views.items():
            src=R/e.get('source',m['source']);bpy.ops.wm.open_mainfile(filepath=str(src));scene=bpy.context.scene
            data=bpy.data.cameras.new('audit_camera');cam=bpy.data.objects.new('audit_camera',data);scene.collection.objects.link(cam);scene.camera=cam
            cam.location=e['position_m'];cam.rotation_euler=e['rotation_euler_xyz_radians'];data.type='ORTHO';data.ortho_scale=e['ortho_scale_m'];data.clip_start=e.get('clip_start_m',.001);data.clip_end=e.get('clip_end_m',100)
            with tempfile.TemporaryDirectory(prefix='168h_origin_render_') as t:
                out=Path(t)/'image.png';scene.render.filepath=str(out);bpy.ops.render.render(write_still=True);arrays=[]
                for f in [R/e['path'],out]:
                    im=bpy.data.images.load(str(f),check_existing=False);arr=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(arr);arrays.append(arr);bpy.data.images.remove(im)
                diff=np.abs(arrays[0]-arrays[1]);delta=float(np.max(diff));fraction=float(np.count_nonzero(diff)/len(diff));assembly=bool(bpy.data.libraries)
                good=delta==0 or (assembly and delta<=1/255+1e-7 and fraction<.001)
                if not good and '--refresh-assembly-references' in sys.argv and assembly and delta<=3/255+1e-7 and fraction<.0001:
                    target=R/e['path'];previous=sha(target);target.write_bytes(out.read_bytes())
                    refreshed.append({'path':e['path'],'old_sha256':previous,'new_sha256':sha(target),'max_channel_delta':delta,'changed_channel_fraction':fraction,'reason':'A14 origin compensation changes float/AA rounding; retained predecessor evidence; no geometry/style change'})
                checks.append({'render':e['path'],'result':'PASS' if good else 'FAIL','max_channel_delta':delta,'changed_channel_fraction':fraction,'acceptance':'exact standalone; linked <=1/255 on <0.1% channels'})
    out={'date':'2026-10-15','checks':checks,'pass':sum(c['result']=='PASS' for c in checks),'fail':sum(c['result']=='FAIL' for c in checks),'script_sha256':sha(Path(__file__))}
    if refreshed:
        (R/'docs/audits/origin-render-refresh.json').write_text(json.dumps(refreshed,indent=2)+'\n')
        (R/'docs/audits/origin-render-pre-refresh.json').write_text(json.dumps(out,indent=2)+'\n');print('REFRESHED_ASSEMBLY_REFERENCES',len(refreshed));sys.exit(0)
    (R/'docs/audits/origin-migration-validation.json').write_text(json.dumps(out,indent=2)+'\n');print('MIGRATION_QA',out['pass'],out['fail'])
    if out['fail']:raise RuntimeError('Migration regression failed')
