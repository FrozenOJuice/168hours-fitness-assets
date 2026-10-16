"""Read-only gate investigation; never replaces accepted files or comparison criteria."""
from pathlib import Path
import bpy, sys, json, math
import numpy as np
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_barbell_stands import A, R, ID, SOURCE
from build_stands_review_assembly import F, OUT, SID, BBID
from barbell_20kg_common import asset_instance_frame, setup, camera, digest, write_json
DEST=R/'exports/illustrations/stands_gate_investigation'

def triangles(obj, frame):
    mesh=obj.data; mesh.calc_loop_triangles()
    transform=np.array(frame@obj.matrix_world, dtype=np.float64)
    xyz=np.array([(*v.co,1) for v in mesh.vertices],dtype=np.float64)@transform.T
    return xyz[np.array([t.vertices[:] for t in mesh.loop_triangles])][...,:3]

def segments(p1,q1,p2,q2):
    # Ericson clamped segment/segment closest points (double precision).
    u=q1-p1; v=q2-p2; w=p1-p2
    a=u@u; b=u@v; c=v@v; d=u@w; e=v@w
    den=a*c-b*b
    s=np.clip((b*e-c*d)/den,0,1) if den>1e-30 else 0.
    t=(b*s+e)/c
    if t<0: t=0.;s=np.clip(-d/a,0,1)
    elif t>1:t=1.;s=np.clip((b-d)/a,0,1)
    return p1+s*u,p2+t*v

def triangle_pair(t,u):
    candidates=[]
    # mathutils float32 is avoided for point/face tests by projection and barycentrics.
    for pts,face,flip in [(t,u,False),(u,t,True)]:
        a,b,c=face; normal=np.cross(b-a,c-a);nn=normal@normal
        for p in pts:
            q=p-normal*((p-a)@normal/nn)
            v0=b-a;v1=c-a;v2=q-a
            aa=v0@v0;bb=v0@v1;cc=v1@v1;dd=v2@v0;ee=v2@v1
            det=aa*cc-bb*bb; x=(cc*dd-bb*ee)/det;y=(aa*ee-bb*dd)/det
            if x>=-1e-12 and y>=-1e-12 and x+y<=1+1e-12:
                candidates.append((q,p) if flip else (p,q))
    for i in range(3):
        for j in range(3):candidates.append(segments(t[i],t[(i+1)%3],u[j],u[(j+1)%3]))
    return min(candidates,key=lambda pair:np.linalg.norm(pair[0]-pair[1]))

def contact(after=False):
    t=np.array([[0.,0,0],[1,0,0],[0,1,0]])
    p,q=triangle_pair(t,t+np.array([0,0,5e-6]));assert abs(np.linalg.norm(p-q)-5e-6)<1e-12
    bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene
    stand=s.objects['stands_pair'];bar=s.objects['barbell_primary']
    sf=asset_instance_frame(stand);wf=asset_instance_frame(bar)
    ts=triangles(bar.instance_collection.all_objects[BBID+'__mesh_shaft'],wf)
    rows=[]
    for side in ['l','r']:
        liner=stand.instance_collection.all_objects[ID+'__mesh_hook_liner_'+side]
        us=triangles(liner,sf);best=.001; witness=None;tested=0
        # AABB distance is a rigorous lower bound: discard only pairs above best distance.
        ulo=us.min(axis=1);uhi=us.max(axis=1)
        global_lower=np.maximum(np.maximum(ulo.min(axis=0)-ts.max(axis=1),ts.min(axis=1)-uhi.max(axis=0)),0)
        for ti in np.flatnonzero(np.linalg.norm(global_lower,axis=1)<=best):
            t=ts[ti]
            lower=np.maximum(np.maximum(ulo-t.max(axis=0),t.min(axis=0)-uhi),0)
            possible=np.flatnonzero(np.linalg.norm(lower,axis=1)<=best)
            for ui in possible:
                p,q=triangle_pair(t,us[ui]);dist=float(np.linalg.norm(p-q));tested+=1
                if dist<best:best=dist;witness={'shaft_triangle':int(ti),'liner_triangle':int(ui),'shaft_point_m':p.tolist(),'liner_point_m':q.tolist()}
        rows.append({'side':side,'minimum_triangle_distance_m':best,'witness':witness,'triangle_pairs_tested':tested,'shaft_triangles':len(ts),'liner_triangles':len(us)})
    write_json(A/('contact-investigation-after.json' if after else 'contact-investigation.json'),{'method':'exhaustive triangle-pair minimum with conservative AABB pruning, float64 world transforms, vertex-face and clamped edge-edge distances; existing BVH test separately excludes crossing','source_sha256':digest(SOURCE),'assembly_sha256':digest(OUT),'script_sha256':digest(Path(__file__)),'checks':rows,'criteria_changed':False})
    print('CONTACT_INVESTIGATION',rows)

def render_probe():
    DEST.mkdir(parents=True,exist_ok=True)
    entries={'assembled':((3.4,-4.2,2.7),(0,.10,.60),2.8),'side':((4,.10,.60),(0,.10,.60),2.8)}
    records=[]
    # Full reopen vs same-scene repeats; optional diagnostics change transient settings only.
    for trial in range(3):
        bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene;setup(s)
        for o in list(bpy.data.objects):
            if o.type=='CAMERA' and not o.library:bpy.data.objects.remove(o,do_unlink=True)
        for view,(pos,target,scale) in entries.items():
            cam=camera(s,SID+'__camera_'+view,pos,target,scale);s.camera=cam
            for repeat in range(2):
                p=DEST/f'{view}_{trial}_{repeat}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
                records.append({'view':view,'trial':trial,'repeat':repeat,'path':str(p.relative_to(R)),'sha256':digest(p)})
    import gpu
    write_json(A/'render-investigation-inputs.json',{'records':records,'source_sha256':digest(SOURCE),'assembly_sha256':digest(OUT),'native_sources_resaved':False,'gpu':{'backend':gpu.platform.backend_type_get(),'vendor':gpu.platform.vendor_get(),'renderer':gpu.platform.renderer_get(),'version':gpu.platform.version_get()},'version':bpy.app.version_string,'script_sha256':digest(Path(__file__))})

def settings_probe():
    DEST.mkdir(parents=True,exist_ok=True);rows=[]
    for variant in ['threads1','no_outline','no_aa','bench_hidden','clip10']:
        for trial in range(3):
            bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene;setup(s)
            if variant=='threads1':s.render.threads_mode='FIXED';s.render.threads=1
            if variant=='no_outline':s.display.shading.show_object_outline=False
            if variant=='no_aa':s.display.render_aa='OFF'
            if variant=='bench_hidden':s.objects['bench_primary'].hide_render=True
            cam=camera(s,'probe',(4,.10,.60),(0,.10,.60),2.8);s.camera=cam
            if variant=='clip10':cam.data.clip_end=10
            p=DEST/f'{variant}_{trial}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
            rows.append({'variant':variant,'trial':trial,'path':str(p.relative_to(R))})
    arrays={}
    for row in rows:
        im=bpy.data.images.load(str(R/row['path']),check_existing=False);arrays[row['path']]=np.array(im.pixels[:]);bpy.data.images.remove(im)
    stats=[]
    for variant in ['threads1','no_outline','no_aa','bench_hidden','clip10']:
        rr=[r for r in rows if r['variant']==variant];diffs=[np.abs(arrays[a['path']]-arrays[b['path']]) for i,a in enumerate(rr) for b in rr[i+1:]]
        stats.append({'variant':variant,'max_8bit_delta':round(max(float(d.max()) for d in diffs)*255),'max_changed_channel_fraction':max(float(np.count_nonzero(d)/d.size) for d in diffs)})
    write_json(A/'render-settings-investigation.json',{'diagnostic_settings_only':True,'authoritative_settings_changed':False,'source_sha256':digest(SOURCE),'assembly_sha256':digest(OUT),'results':stats});print(stats)

if __name__=='__main__':
    before={p:digest(p) for p in [SOURCE,OUT]}
    contact('--contact-after' in sys.argv) if '--contact' in sys.argv or '--contact-after' in sys.argv else settings_probe() if '--settings' in sys.argv else render_probe()
    assert all(digest(p)==h for p,h in before.items())
