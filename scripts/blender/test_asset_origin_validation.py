"""Meaningful failure-injection checks for reusable origin audit; never saves a blend."""
from pathlib import Path
import bpy,json,sys,copy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_asset_origins import audit,REPO
if __name__=='__main__':
    manifests=[json.loads(p.read_text()) for p in (REPO/'assets/equipment').rglob('asset.json') if 'history' not in p.parts]
    m=next(x for x in manifests if x['origin_contract']['profile']=='flat_bench');rules=json.loads((REPO/'docs/equipment-origin-rules.json').read_text());results=[]
    def case(name,mutate,expected):
        bpy.ops.wm.open_mainfile(filepath=str(REPO/m['source']));meta=copy.deepcopy(m);mutate(meta);bpy.context.view_layer.update();checks=audit(meta,rules);failed=[c['check'] for c in checks if c['result']=='FAIL'];ok=any(x.startswith(expected) for x in failed);results.append({'case':name,'expected_failure':expected,'observed_failures':failed,'result':'PASS' if ok else 'FAIL'})
    case('unknown future category fails closed',lambda x:x['origin_contract'].update(profile='unregistered'), 'registered_origin_profile')
    case('offset differs from root',lambda x:setattr(bpy.data.collections[x['collection']],'instance_offset',(0,0,.1)),'collection_pivot_matches_root')
    case('anchor offset drifts',lambda x:setattr(bpy.data.objects[x['anchors']['pad_center']['object']],'location',(0,0,.5)),'anchor_position:pad_center')
    case('negative scale',lambda x:setattr(bpy.data.objects[x['root']],'scale',(-1,1,1)),'unit_positive_scale:')
    case('wrong root rotation',lambda x:setattr(bpy.data.objects[x['root']],'rotation_euler',(0,0,.5)),'root_rotation')
    case('wrong support frame',lambda x:setattr(bpy.data.objects[x['anchors']['back_support']['object']],'rotation_euler',(1,0,0)),'anchor_forward:back_support')
    out={'checks':results,'pass':sum(c['result']=='PASS' for c in results),'fail':sum(c['result']=='FAIL' for c in results)};(REPO/'docs/audits/origin-validator-tests.json').write_text(json.dumps(out,indent=2)+'\n');print('ORIGIN_TESTS',out['pass'],out['fail'])
    if out['fail']:raise RuntimeError('Validator missed a deviation')
