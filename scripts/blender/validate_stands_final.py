"""Read-only final measurements for stands, approved bench and barbell contacts."""
from pathlib import Path
import bpy,sys,json,math
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_barbell_stands import R,ID,A,SOURCE
from build_stands_review_assembly import F,OUT,BID,BBID
from barbell_20kg_common import asset_instance_frame,digest,write_json
from validate_barbell_stands import tree,update,bounds
rows=[]
def check(name,expected,actual,ok):rows.append({'check':name,'expected':expected,'actual':actual,'result':'PASS' if ok else 'FAIL'})
def run():
    pins_before={p:digest(p) for p in [SOURCE,OUT]}
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));col=bpy.data.collections[ID];root=col.all_objects[ID+'__root']
    # Read geometry independently of manifest target sizes.
    for side in ['l','r']:
        pads=[o for o in col.all_objects if '__mesh_rubber_' in o.name and o.name.endswith('_'+side)];lo,hi=bounds(pads);size=[hi[k]-lo[k] for k in [0,1]]
        check('manufacturer_base:'+side,'596.9x622.3mm contextual orientation',size,abs(size[0]-.5969)<1e-6 and abs(size[1]-.6223)<1e-6)
    update(root,15,15)
    for side in ['l','r']:
        lo,hi=bounds([col.all_objects[ID+'__mesh_upright_inner_'+side]]);check('manufacturer_max_tube_top:'+side,'1778mm; manufacturer height datum interpretation remains provisional',hi[2],abs(hi[2]-1.778)<1e-6)
    for i in range(16):
        update(root,i,i)
        for side in ['l','r']:
            inner=col.all_objects[ID+'__mesh_upright_inner_'+side];cx=inner.matrix_world.translation.x
            pts=[inner.matrix_world@v.co for v in inner.data.vertices]
            ring=[p for p in pts if abs(abs(p.x-cx)-.03)<1e-6 and abs(p.y)<.0086 and abs(p.z-.9)<.0086]
            radii=[math.hypot(p.y,p.z-.9) for p in ring]
            pin=col.all_objects[ID+'__mesh_adjustment_pin_'+side];lo,hi=bounds([pin]);pin_radius=(hi[1]-lo[1])/2
            surface=tree(inner,Matrix.Identity(4));nearest=[surface.find_nearest(Vector((cx+xx,0,.9)))[3] for xx in [.0275,.0285,.0295]]
            clearance=min(nearest)-pin_radius if radii else None
            check('measured_pin_clearance:'+side+':'+str(i),'positive measured clearance; nominal0.5625mm, tessellated opening recorded',{'sampled_rim_vertices':len(ring),'min_vertex_hole_radius_m':min(radii) if radii else None,'nearest_hole_face_distance_m':min(nearest),'pin_radius_m':pin_radius,'radial_clearance_m':clearance},bool(radii) and clearance>0)
    bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene;stands=s.objects['stands_pair'];bench=s.objects['bench_primary'];bar=s.objects['barbell_primary'];sc=stands.instance_collection;bc=bench.instance_collection;wc=bar.instance_collection;sf=asset_instance_frame(stands);bf=asset_instance_frame(bench);wf=asset_instance_frame(bar)
    bench_pts=[bf@(o.matrix_world@v.co) for o in bc.all_objects if o.type=='MESH' for v in o.data.vertices];bench_half=max(abs(p.x) for p in bench_pts)
    center=(wf@wc.all_objects[BBID+'__anchor_axis_center'].matrix_world).translation;shaft_obj=wc.all_objects[BBID+'__mesh_shaft'];shaft_tree=tree(shaft_obj,wf);shaft_pts=[wf@(shaft_obj.matrix_world@v.co) for v in shaft_obj.data.vertices];ends=[min(p.x for p in shaft_pts),max(p.x for p in shaft_pts)]
    contacts=[]
    for side in ['l','r']:
        points=[sf@(o.matrix_world@v.co) for o in sc.all_objects if o.type=='MESH' and o.name.endswith('_'+side) for v in o.data.vertices];edge=min(abs(p.x) for p in points);gap=edge-bench_half
        check('measured_bench_to_stand:'+side,'>=73.75mm horizontal separating envelope',{'stand_inner_x_m':edge,'bench_half_width_m':bench_half,'horizontal_gap_m':gap},abs(gap-.07375)<1e-6)
        support=(sf@sc.all_objects[ID+'__anchor_bar_support_'+side].matrix_world).translation;contacts.append(support)
        hookpts=[sf@(o.matrix_world@v.co) for o in sc.all_objects if '__mesh_hook_' in o.name and o.name.endswith('_'+side) for v in o.data.vertices];extent=max(abs(p.x-center.x) for p in hookpts);flange_points=[wf@(obj.matrix_world@v.co) for obj in wc.all_objects if '__mesh_sleeve_' in obj.name for v in obj.data.vertices]
        halfshaft=min(abs(p.x-center.x) for p in flange_points);margin=halfshaft-extent
        check('measured_hook_flange_margin:'+side,'75mm based on actual shaft and hook envelopes',{'half_shaft_m':halfshaft,'hook_outer_station_m':extent,'margin_m':margin},abs(margin-.075)<1e-6)
        # Sample actual stock shaft underside over the full58mm liner width.
        gaps=[]
        for n in range(59):
            p=support+Vector((-.029+n*.001,0,-.02));hit=shaft_tree.ray_cast(p,Vector((0,0,1)),.08)[0]
            if hit is not None:gaps.append(hit.z-support.z)
        liner_tree=tree(sc.all_objects[ID+'__mesh_hook_liner_'+side],sf);surface_gaps=[]
        for point in shaft_pts:
            if abs(point.x-support.x)<=.029+1e-6:
                hit=liner_tree.ray_cast(Vector((point.x,point.y,support.z+.2)),Vector((0,0,-1)),.3)[0]
                if hit is not None:surface_gaps.append(point.z-hit.z)
        check('actual_bar_bottom_contact:'+side,'no penetration; actual bottom contact within1e-6m',{'rays':len(gaps),'min_vertical_gap_m':min(gaps) if gaps else None,'max_vertical_gap_m':max(gaps) if gaps else None,'actual_vertex_to_liner_min_gap_m':min(surface_gaps) if surface_gaps else None,'surface_vertices':len(surface_gaps)},len(gaps)==59 and bool(surface_gaps) and min(surface_gaps)>=-1e-6 and abs(min(surface_gaps))<1e-6)
    a,b=contacts;check('symmetric_j_hook_contacts','X mirrored around bar midpoint, equalY/Z;1100mm separation',{'left':list(a),'right':list(b),'center':list(center),'separation_m':(a-b).length},abs(a.x+b.x-2*center.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6 and abs((a-b).length-1.1)<1e-6)
    for p,h in pins_before.items():check('source_bytes_preserved:'+p.name,h,digest(p),digest(p)==h)
    report={'date':'2026-10-15','source_sha256':digest(SOURCE),'assembly_sha256':digest(OUT),'validator_sha256':digest(Path(__file__)),'checks':rows,'pass':sum(c['result']=='PASS' for c in rows),'fail':sum(c['result']=='FAIL' for c in rows),'scope':'independent measured digital geometry and static contact; no manufacturing or strength certification'};write_json(A/'final-measurements.json',report)
    print('STANDS_FINAL_MEASUREMENTS',report['pass'],report['fail']);print([c for c in rows if c['result']=='FAIL'])
    if report['fail']:raise RuntimeError('Final measurement deviations')
if __name__=='__main__':run()
