"""Read-only numeric stacking/clearance checks on every migrated plate/bar fixture.

Dimensions come from saved geometry and attachment frames; collar/scene allowances
come from the existing manifests. Does not create geometry or resave sources.
"""
from pathlib import Path
import bpy, json, math, sys, hashlib
from mathutils import Vector

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from barbell_20kg_common import asset_instance_frame

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    manifests = [json.loads(p.read_text()) for p in (REPO/'assets/equipment').rglob('asset.json') if 'history' not in p.parts]
    assets = {m['collection']:m for m in manifests}
    checks = []
    def check(name, expected, actual, passed):
        checks.append({'check':name, 'expected':expected, 'actual':actual, 'result':'PASS' if passed else 'FAIL'})
    fixtures = [json.loads(p.read_text()) for p in (REPO/'scenes/templates').glob('*/asset.json') if p.parent.name.startswith('168h_')]
    for fixture in fixtures:
        if not fixture.get('placement', {}).get('capacity_per_sleeve'):
            continue
        sources = [(fixture['source'], 1)]
        for entry in fixture.get('secondary_sources', []):
            expected = fixture['placement']['capacity_per_sleeve'] if entry['role']=='diagnostic_maximum' else fixture['placement']['example_per_sleeve']
            sources.append((entry['path'],expected))
        for source, expected_count in sources:
            path = REPO/source
            before = digest(path)
            bpy.ops.wm.open_mainfile(filepath=str(path))
            bpy.context.view_layer.update()
            instances = [o for o in bpy.context.scene.objects if o.instance_type=='COLLECTION']
            bars = [o for o in instances if assets.get(o.instance_collection.name, {}).get('origin_contract', {}).get('profile')=='olympic_barbell']
            plates = [o for o in instances if assets.get(o.instance_collection.name, {}).get('origin_contract', {}).get('profile')=='olympic_plate']
            check(source+':linked_instance_counts', {'bars':1,'plates':2*expected_count}, {'bars':len(bars),'plates':len(plates)},len(bars)==1 and len(plates)==2*expected_count)
            bar = bars[0]; bm=assets[bar.instance_collection.name]; pm=assets[plates[0].instance_collection.name]
            col=plates[0].instance_collection
            bore=col.all_objects[pm['anchors']['bore_center']['object']].matrix_world
            body=col.all_objects[pm['origin_contract']['geometry_objects'][0]]
            bp=[bore.inverted()@(body.matrix_world@v.co) for v in body.data.vertices]
            radius=min(math.hypot(v.x,v.z) for v in bp)
            ring=sorted({(round(v.x,12),round(v.z,12)) for v in bp if math.hypot(v.x,v.z)<=radius*1.001},key=lambda p:math.atan2(p[1],p[0]))
            minimum_bore=min(math.hypot(a[0]+b[0],a[1]+b[1]) for a,b in zip(ring,ring[1:]+ring[:1]))
            capacity=bm['compatibility']['capacity']; collar=capacity['collar_allowance_m']; tip=capacity['tip_margin_m']
            centers={}; side_records={}
            for side in ['l','r']:
                load=asset_instance_frame(bar)@bar.instance_collection.all_objects[bm['anchors']['load_'+side]['object']].matrix_world
                end=asset_instance_frame(bar)@bar.instance_collection.all_objects[bm['anchors']['sleeve_end_'+side]['object']].matrix_world
                outward=(load.to_3x3()@Vector((0,1,0))).normalized()
                length=(end.translation-load.translation).dot(outward)
                rows=[]
                for instance in plates:
                    transform=asset_instance_frame(instance)
                    center=(transform@bore).translation
                    axial=(center-load.translation).dot(outward)
                    if axial<0:continue
                    points=[transform@(o.matrix_world@v.co) for o in col.all_objects if o.type=='MESH' for v in o.data.vertices]
                    projected=[(p-load.translation).dot(outward) for p in points]
                    rows.append({'instance':instance.name,'center_m':list(center),'start_m':min(projected),'end_m':max(projected),'axis_error_m':(center-load.translation).cross(outward).length,'axis_direction_error':((transform@bore).to_3x3()@Vector((0,1,0))-outward).length,'floor_z_m':min(p.z for p in points)})
                rows.sort(key=lambda e:e['start_m'])
                check(source+':'+side+':plate_count',expected_count,len(rows),len(rows)==expected_count)
                sleeve=bar.instance_collection.all_objects[next(n for n in bm['components']['sleeves'] if n.endswith('_'+side))]
                sleeve_points=[asset_instance_frame(bar)@(sleeve.matrix_world@v.co) for v in sleeve.data.vertices]
                radial=max((p-load.translation-outward*((p-load.translation).dot(outward))).length for p in sleeve_points if 1e-5<(p-load.translation).dot(outward)<length-1e-5)
                clearance=minimum_bore/2-radial
                gaps=[b['start_m']-a['end_m'] for a,b in zip(rows,rows[1:])]
                flange_gap=rows[0]['start_m']; spare=length-rows[-1]['end_m']-collar-tip
                check(source+':'+side+':alignment', '<=1e-6m/rad-vector error', rows, all(e['axis_error_m']<1e-6 and e['axis_direction_error']<1e-6 and abs(e['floor_z_m'])<1e-6 for e in rows))
                check(source+':'+side+':bore_sleeve_clearance','>=0.00039m',{'minimum_bore_m':minimum_bore,'maximum_sleeve_radius_m':radial,'radial_clearance_m':clearance},clearance>.00039)
                check(source+':'+side+':stack_spacing',capacity['interplate_gap_m'],gaps,all(abs(g-capacity['interplate_gap_m'])<1e-6 for g in gaps))
                check(source+':'+side+':flange_collar_tip_clearance',{'flange_gap_m':capacity['flange_gap_m'],'collar_m':collar,'tip_m':tip,'spare_after_reserves_m':'>=0'}, {'flange_gap_m':flange_gap,'spare_after_reserves_m':spare},abs(flange_gap-capacity['flange_gap_m'])<1e-6 and spare>=0)
                centers[side]=[Vector(e['center_m']) for e in rows]
                side_records[side]={'sleeve_length_m':length,'plate_pitch_m':rows[0]['end_m']-rows[0]['start_m'],'minimum_gap_m':min(gaps) if gaps else None,'radial_clearance_m':clearance,'spare_after_reserves_m':spare}
            # Reflection about the midpoint frame; current fixture is axis-aligned.
            middle=(asset_instance_frame(bar)@bar.instance_collection.all_objects[bm['anchors']['axis_center']['object']].matrix_world).translation
            symmetry=max((a-Vector((2*middle.x-b.x,b.y,b.z))).length for a,b in zip(centers['l'],centers['r']))
            check(source+':symmetric_placement','<=1e-6m',symmetry,symmetry<1e-6)
            check(source+':intersection_exclusion','positive radial and flange/interplate envelope clearances',side_records,all(e['radial_clearance_m']>0 and (e['minimum_gap_m'] is None or e['minimum_gap_m']>0) and e['spare_after_reserves_m']>=0 for e in side_records.values()))
            check(source+':source_unchanged',before,digest(path),before==digest(path))
    report={'date':'2026-10-15','scope':'digital packing and alignment of unchanged, previously manifold/BVH-validated geometry; no physical strength claim','checks':checks,'pass':sum(e['result']=='PASS' for e in checks),'fail':sum(e['result']=='FAIL' for e in checks),'validator_sha256':digest(Path(__file__))}
    (REPO/'docs/audits/origin-compatibility-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('ORIGIN_COMPATIBILITY',report['pass'],report['fail'])
    if report['fail']:raise RuntimeError('Origin compatibility validation failed')

if __name__=='__main__':run()
