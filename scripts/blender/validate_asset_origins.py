"""Metadata/category-driven, read-only equipment origin audit. No model IDs in rules."""
from pathlib import Path
import argparse,json,hashlib,sys,math
import bpy
from mathutils import Vector,Euler,Matrix
REPO=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vec(axis):
    v=Vector((0,0,0));v['XYZ'.index(axis[-1])]=-1 if axis.startswith('-') else 1;return v
def audit(m,registry):
    rows=[];tol=registry['tolerance_m'];cfg=m.get('origin_contract',{});profile=registry['profiles'].get(cfg.get('profile'))
    def check(key,expected,actual,ok=None):
        if ok is None:ok=len(expected)==len(actual) and all(math.isfinite(a) and math.isfinite(b) and abs(a-b)<=tol for a,b in zip(expected,actual))
        rows.append({'check':key,'expected':expected,'actual':actual,'result':'PASS' if ok else 'FAIL'})
    if not profile:
        check('registered_origin_profile','registered origin_contract.profile',cfg.get('profile'),False);return rows
    col=bpy.data.collections.get(m['collection']);root=bpy.data.objects.get(m['root'])
    if not col or not root:
        check('published_root_collection', [m['root'],m['collection']],None,False);return rows
    bpy.context.view_layer.update();objects=list(col.all_objects);meshes=[o for o in objects if o.type=='MESH']
    selected=[col.all_objects[n] for n in cfg.get('geometry_objects',[])] or meshes
    points=[o.matrix_world@v.co for o in selected for v in o.data.vertices]
    low=Vector([min(p[i] for p in points) for i in range(3)]);high=Vector([max(p[i] for p in points) for i in range(3)])
    center=(low+high)/2
    datum=Vector((center.x,center.y,low.z)) if profile['datum']=='floor_bounds_center' else center
    if profile['datum']=='floor_bounds_center':
        contact=[p for p in points if abs(p.z-low.z)<=tol]
        datum=Vector(((min(p.x for p in contact)+max(p.x for p in contact))/2,(min(p.y for p in contact)+max(p.y for p in contact))/2,low.z))
    if profile['datum']=='bore_center':
        import numpy as np
        axis='XYZ'.index(profile['primary_axis']);radial=[i for i in range(3) if i!=axis]
        radii=[math.hypot(p[radial[0]]-center[radial[0]],p[radial[1]]-center[radial[1]]) for p in points]
        inner=[p for p,r in zip(points,radii) if r<=min(radii)*1.001]
        a=np.array([[2*p[radial[0]],2*p[radial[1]],1] for p in inner]);b=np.array([p[radial[0]]**2+p[radial[1]]**2 for p in inner])
        fit=np.linalg.lstsq(a,b,rcond=None)[0]
        datum[radial[0]]=float(fit[0]);datum[radial[1]]=float(fit[1])
        residual=float(np.max(np.abs(a@fit-b)))
        check('circular_bore_fit','>=3 vertices, rank3, squared-radius residual<=1e-8',{'vertices':len(inner),'residual':residual},len(inner)>=3 and np.linalg.matrix_rank(a)==3 and residual<=1e-8)
    check('root_functional_datum',list(datum),list(root.matrix_world.translation))
    check('collection_pivot_matches_root',list(root.matrix_world.translation),list(col.instance_offset))
    check('declared_authoring_root',cfg.get('authoring_root_position_m',[]),list(root.matrix_world.translation),len(cfg.get('authoring_root_position_m',[]))==3 and (root.matrix_world.translation-Vector(cfg['authoring_root_position_m'])).length<=tol)
    check('root_rotation',[0,0,0],list(root.rotation_euler))
    check('source_authoring_floor',[cfg.get('source_authoring_floor_z_m')],[low.z])
    check('metric_units','METRIC / scale1',[bpy.context.scene.unit_settings.system,bpy.context.scene.unit_settings.scale_length],bpy.context.scene.unit_settings.system=='METRIC' and bpy.context.scene.unit_settings.scale_length==1)
    check('coordinate_axes',registry['axes'],m.get('axes'),m.get('axes')==registry['axes'])
    def desc(o):
        while o.parent:
            o=o.parent
            if o==root:return True
        return False
    check('root_hierarchy','all objects descend from unparented root',[o.name for o in objects if o!=root and not desc(o)],root.parent is None and all(o==root or desc(o) for o in objects))
    for o in objects:
        check('unit_positive_scale:'+o.name,[1,1,1],list(o.scale),all(math.isfinite(v) and abs(v-1)<tol for v in o.scale) and o.matrix_world.to_3x3().determinant()>0)
        if o.type=='MESH':
            declared=cfg.get('component_frames',{}).get(o.name)
            actual_position=list((root.matrix_world.inverted()@o.matrix_world).translation)
            check('component_origin:'+o.name,declared['root_local_position_m'] if declared else [],actual_position,declared is not None and bool(declared.get('purpose')) and len(declared['root_local_position_m'])==3 and all(abs(a-b)<=tol for a,b in zip(declared['root_local_position_m'],actual_position)))
            expected=cfg.get('allowed_component_rotations',{}).get(o.name,[0,0,0]);actual=o.rotation_euler.to_matrix();target=Euler(expected).to_matrix()
            check('rigid_rotation:'+o.name,expected,list(o.rotation_euler),max(abs(actual[i][j]-target[i][j]) for i in range(3) for j in range(3))<=tol)
    for key in profile['required_anchors']:
        check('required_anchor:'+key,'declared and present',m.get('anchors',{}).get(key),key in m.get('anchors',{}) and m['anchors'][key]['object'] in col.all_objects)
    inv=root.matrix_world.inverted()
    for key,e in m.get('anchors',{}).items():
        o=col.all_objects.get(e['object'])
        if o is None:check('anchor:'+key,e['object'],None,False);continue
        frame=inv@o.matrix_world
        check('anchor_name:'+key,m['id']+'__anchor_'+key,o.name,o.name==m['id']+'__anchor_'+key)
        check('anchor_position:'+key,e['position_m'],list(frame.translation))
        forward=vec(e['forward']);up=vec(e['up'])
        check('anchor_forward:'+key,list(forward),list(frame.to_3x3()@Vector((0,1,0))))
        check('anchor_up:'+key,list(up),list(frame.to_3x3()@Vector((0,0,1))))
        rule=profile.get('anchor_rules',{}).get(key)
        if rule:
            target=datum.copy()
            if rule=='floor':target.z=low.z
            elif rule=='max_axis':target['XYZ'.index(profile['primary_axis'])]=high['XYZ'.index(profile['primary_axis'])]
            elif rule=='min_axis':target['XYZ'.index(profile['primary_axis'])]=low['XYZ'.index(profile['primary_axis'])]
            elif rule=='top':target=o.matrix_world.translation.copy();target.z=high.z
            check('anchor_geometry_datum:'+key,list(target),list(o.matrix_world.translation))
    lengths=list(high-low);axis='XYZ'.index(profile['primary_axis'])
    rule=profile['primary_axis_rule']
    check('physical_primary_axis',profile['primary_axis'],lengths,rule=='none' or (lengths[axis]>=max(lengths)-tol if rule=='longest' else lengths[axis]<=min(lengths)+tol))
    for lib in bpy.data.libraries:
        check('relative_resolved_library:'+lib.name,'// relative and exists',lib.filepath,lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists())
    return rows

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--manifest');parser.add_argument('--output');parser.add_argument('--origins',action='store_true');opts=parser.parse_args(args)
    registry=json.loads((REPO/'docs/equipment-origin-rules.json').read_text());reports=[]
    manifests=[REPO/opts.manifest] if opts.manifest else sorted(p for p in (REPO/'assets/equipment').rglob('asset.json') if 'history' not in p.parts)
    for p in manifests:
        m=json.loads(p.read_text());src=REPO/m['source'];before=sha(src)
        bpy.ops.wm.open_mainfile(filepath=str(src));checks=audit(m,registry)
        assert sha(src)==before
        reports.append({'asset_id':m['id'],'version':m['version'],'source':m['source'],'source_sha256':before,'checks':checks,'pass':sum(c['result']=='PASS' for c in checks),'fail':sum(c['result']=='FAIL' for c in checks)})
    out={'standard':registry['id'],'date':'2026-10-15','blender_version':bpy.app.version_string,'validator_sha256':sha(Path(__file__)),'rules_sha256':sha(REPO/'docs/equipment-origin-rules.json'),'assets':reports,'pass':sum(x['pass'] for x in reports),'fail':sum(x['fail'] for x in reports)}
    path=REPO/opts.output if opts.output else ((REPO/opts.manifest).parent/'origin-validation.json' if opts.manifest else REPO/'docs/audits/origin-audit-results.json');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n');print('ORIGIN_AUDIT',out['pass'],out['fail'])
    if out['fail']:raise RuntimeError('Origin deviations: inspect expected/actual report')
if __name__=='__main__':main()
