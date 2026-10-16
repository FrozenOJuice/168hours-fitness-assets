"""Human V1 structural/release QA. Stdlib only; never creates Blender content.

Schemas are Draft2020-12 documents. This checker implements only their declared
vocabulary; unsupported validation keywords fail closed, not silently ignored.
"""
from pathlib import Path
import argparse, hashlib, json, math, re
R = Path(__file__).resolve().parents[2]
D = R / 'docs/contracts/human-v1'

def read(path):
    def constant(value): raise ValueError('Nonfinite JSON constant: '+value)
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(Path(path).read_text(), parse_constant=constant, object_pairs_hook=pairs)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def norm(v): return math.sqrt(sum(x*x for x in v))
def sub(a,b): return [x-y for x,y in zip(a,b)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def unit(v):
    n=norm(v)
    return [x/n for x in v] if n>1e-12 else [0,0,0]
def close(a,b,t=1e-6): return norm(sub(a,b)) <= t
def quaternion_axis(q,index):
    w,x,y,z=q
    columns=[[1-2*(y*y+z*z),2*(x*y+w*z),2*(x*z-w*y)],
             [2*(x*y-w*z),1-2*(x*x+z*z),2*(y*z+w*x)],
             [2*(x*z+w*y),2*(y*z-w*x),1-2*(x*x+y*y)]]
    return columns[index]
def check(rows,name,expected,actual,ok):
    rows.append(dict(check=name,expected=expected,actual=actual,result='PASS' if ok else 'FAIL'))

def schema_vocabulary_errors(schema,path='$schema'):
    allowed={'$schema','$id','title','description','type','properties','required','additionalProperties',
             'items','minItems','maxItems','enum','const','pattern','minimum','maximum',
             'exclusiveMinimum','minLength'}
    errors=[path+': unsupported keyword '+k for k in set(schema)-allowed]
    for key,child in schema.get('properties',{}).items():errors+=schema_vocabulary_errors(child,path+'.'+key)
    for key in ['additionalProperties','items']:
        if isinstance(schema.get(key),dict):errors+=schema_vocabulary_errors(schema[key],path+'.'+key)
    return errors

def schema_errors(value,schema,path='$',_checked=False):
    if not _checked:
        vocabulary=schema_vocabulary_errors(schema)
        if vocabulary:return vocabulary
    allowed={'$schema','$id','title','description','type','properties','required','additionalProperties',
             'items','minItems','maxItems','enum','const','pattern','minimum','maximum',
             'exclusiveMinimum','minLength'}
    unknown=set(schema)-allowed
    if unknown:return [path+': unsupported schema keywords '+','.join(sorted(unknown))]
    errors=[]
    types={'null':lambda v:v is None,'object':lambda v:isinstance(v,dict),
           'array':lambda v:isinstance(v,list),'string':lambda v:isinstance(v,str),
           'boolean':lambda v:isinstance(v,bool),'number':lambda v:type(v) in (int,float) and math.isfinite(v),
           'integer':lambda v:type(v) is int}
    if 'type' in schema:
        choices=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
        if any(t not in types for t in choices):return [path+': unsupported schema type']
        if not any(types[t](value) for t in choices):return [path+': expected '+str(choices)]
    if 'const' in schema and value!=schema['const']:errors.append(path+': wrong constant')
    if 'enum' in schema and value not in schema['enum']:errors.append(path+': value outside enum')
    if isinstance(value,dict):
        props=schema.get('properties',{})
        errors += [path+': missing '+k for k in schema.get('required',[]) if k not in value]
        for key,item in value.items():
            if key in props:errors+=schema_errors(item,props[key],path+'.'+key,True)
            elif schema.get('additionalProperties') is False:errors.append(path+': unexpected '+key)
            elif isinstance(schema.get('additionalProperties'),dict):errors+=schema_errors(item,schema['additionalProperties'],path+'.'+key,True)
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0) or len(value)>schema.get('maxItems',float('inf')):errors.append(path+': invalid array length')
        for i,item in enumerate(value):errors+=schema_errors(item,schema.get('items',{}),path+f'[{i}]',True)
    if isinstance(value,str):
        if len(value)<schema.get('minLength',0):errors.append(path+': string too short')
        if 'pattern' in schema and re.search(schema['pattern'],value) is None:errors.append(path+': pattern mismatch')
    if type(value) in (int,float):
        if not math.isfinite(value):errors.append(path+': nonfinite number')
        if value<schema.get('minimum',-float('inf')) or value>schema.get('maximum',float('inf')):errors.append(path+': outside bounds')
        if 'exclusiveMinimum' in schema and value<=schema['exclusiveMinimum']:errors.append(path+': below exclusive minimum')
    return errors

def registry_checks():
    sk=read(D/'skeleton.json');cat=read(D/'muscles.json');rows=[]
    lock=read(D/'contract-lock.json')
    for entry in lock['inputs']:
        p=(R/entry['path']).resolve();actual=sha(p) if p.is_relative_to(R.resolve()) and p.is_file() else None
        check(rows,'contract_pin:'+entry['path'],entry['sha256'],actual,actual==entry['sha256'])
    errors=schema_errors(cat,read(R/'schemas/human-muscle-catalog-v1.schema.json'))
    check(rows,'catalog_schema','valid catalog fields',errors,not errors)
    if errors:return rows
    names=[b['name'] for b in sk['bones']];ids=[e['id'] for e in cat['entries']]
    check(rows,'registry_bone_names','unique snake_case',names,len(set(names))==len(names) and all(re.fullmatch('[a-z][a-z0-9_]*',n) for n in names))
    seen=set()
    for b in sk['bones']:
        check(rows,'registry_parent:'+b['name'],'parent precedes child; only root unparented',b['parent'],b['parent'] in seen if b['name']!='root' else b['parent'] is None)
        seen.add(b['name'])
    check(rows,'registry_muscle_ids','unique bilateral IDs',len(ids),len(set(ids))==len(ids))
    for e in cat['entries']:
        other=e['pair_id']+('_r' if e['side']=='l' else '_l')
        check(rows,'registry_muscle_pair:'+e['id'],'stable pair and anatomical classification',other,e['id']==e['pair_id']+'_'+e['side'] and other in ids and bool(e['anatomical_name']) and bool(e['group']) and e['representation'] in ['muscle','region','aggregate'])
    return rows

def activation_checks(doc):
    errors=schema_errors(doc,read(R/'schemas/exercise-muscles-v1.schema.json'));rows=[]
    check(rows,'activation_schema','valid JSON schema fields',errors,not errors)
    if errors:return rows
    ids={e['id'] for e in read(D/'muscles.json')['entries']}
    check(rows,'activation_ids','catalog IDs only',sorted(set(doc['primary'])|set(doc['secondary'])),(set(doc['primary'])|set(doc['secondary']))<=ids)
    overlap=set(doc['primary'])&set(doc['secondary'])
    check(rows,'activation_roles','no ID in both roles',sorted(overlap),not overlap)
    return rows

def rest_fingerprint(bones):
    fields=['name','parent','deform','connected','head_m','tail_m','z_axis']
    data=[{k:b[k] for k in fields} for b in sorted(bones,key=lambda b:b['name'])]
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def export_checks(doc):
    rows=[];errs=schema_errors(doc,read(R/'schemas/human-export-v1.schema.json'))
    check(rows,'export_schema','versioned export profile',errs,not errs)
    if errs:return rows
    expected={b['name'] for b in read(D/'skeleton.json')['bones']};names=doc['bone_names']
    check(rows,'export_bone_interface','exact canonical skeleton, no control bones',names,set(names)==expected and len(names)==len(expected) and not doc['control_bones_included'])
    check(rows,'export_timing','ordered frames; animation positive FPS and baked',doc['frame_rate_fps'],doc['start_frame']<=doc['end_frame'] and (doc['role']!='animation' or doc['baked_animation'] and doc['frame_rate_fps'] is not None))
    a=doc['axis_conversion'];columns=[[a[i][j] for i in range(3)] for j in range(3)]
    det=(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    check(rows,'export_axis_conversion','proper rigid basis change, no translation/mirroring/scale',a,all(abs(norm(c)-1)<1e-6 for c in columns) and all(abs(dot(columns[i],columns[j]))<1e-6 for i in range(3) for j in range(i)) and abs(det-1)<1e-6 and close([a[i][3] for i in range(3)],[0,0,0]) and close(a[3],[0,0,0,1]))
    check(rows,'export_muscle_state','animation retains semantic states',doc['muscle_state_delivery'],doc['role']!='animation' or doc['muscle_state_delivery'] in ['embedded','sidecar'])
    return rows

EVIDENCE=['manual_anatomy','clothing_highlight','ik_fk_contacts','retarget_contacts','illustration_export','animation_export','linked_replacement','reference_renders']
def character_checks(manifest,snapshot,release=False,base=None):
    rows=[];base=Path(base or R)
    for value,name in [(manifest,'human-character-v1'),(snapshot,'human-snapshot-v1')]:
        errs=schema_errors(value,read(R/'schemas'/(name+'.schema.json')))
        check(rows,name+'_schema','valid fields/types',errs,not errs)
    if any(r['result']=='FAIL' for r in rows):return rows
    sk=read(D/'skeleton.json');cat=read(D/'muscles.json');expected={b['name']:b for b in sk['bones']}
    names=[b['name'] for b in snapshot['bones']];actual={b['name']:b for b in snapshot['bones']}
    check(rows,'skeleton_structure','exact core bone set, no duplicates',names,set(actual)==set(expected) and len(names)==len(actual))
    ident=[[1 if i==j else 0 for j in range(4)] for i in range(4)]
    for key in ['root_matrix','armature_matrix']:
        error=max(abs(snapshot[key][i][j]-ident[i][j]) for i in range(4) for j in range(4))
        check(rows,key,'identity in source authoring frame',error,error<=1e-6)
    check(rows,'collection_pivot','floor root zero',snapshot['collection_offset_m'],close(snapshot['collection_offset_m'],[0,0,0]))
    check(rows,'units','meters, unit scale1',snapshot['scale_length'],snapshot['scale_length']==1)
    for flag in ['hierarchy_valid','transforms_normalized','skinning_valid','ik_valid','joint_constraints_valid']:
        check(rows,flag,True,snapshot[flag],snapshot[flag])
    check(rows,'body_floor','lowest body point Z0 ±10um',snapshot['body_min_z_m'],abs(snapshot['body_min_z_m'])<=1e-5)
    check(rows,'body_height','declared measured stature ±10um',{'declared':manifest['height_m'],'measured':snapshot['body_height_m']},manifest['height_m'] is not None and abs(manifest['height_m']-snapshot['body_height_m'])<=1e-5)
    for name,b in actual.items():
        if name not in expected:continue
        e=expected[name];y=unit(sub(b['tail_m'],b['head_m']));projected=sub([0,1,0],[dot([0,1,0],y)*v for v in y])
        if norm(projected)<1e-6:projected=sub([0,0,1],[dot([0,0,1],y)*v for v in y])
        z=unit(projected)
        check(rows,'bone_contract:'+name,{'parent':e['parent'],'deform':e['deform'],'connected':e['connected']},{k:b[k] for k in ['parent','deform','connected']},all(b[k]==e[k] for k in ['parent','deform','connected']))
        check(rows,'bone_frame:'+name,'nonzero length, canonical roll, identity pose',b['z_axis'],norm(sub(b['tail_m'],b['head_m']))>1e-6 and close(b['z_axis'],z,1e-5) and b['pose_identity'])
        if e['connected'] and e['parent'] in actual:check(rows,'connected_joint:'+name,'head=parent tail',b['head_m'],close(b['head_m'],actual[e['parent']]['tail_m']))
    if set(expected)<=set(actual):
        check(rows,'root_bone_datum','head0/tailZ0.1',actual['root']['head_m'],close(actual['root']['head_m'],[0,0,0]) and close(actual['root']['tail_m'],[0,0,.1]))
        check(rows,'pelvis_floor_projection','pelvis headXY0',actual['pelvis']['head_m'],norm(actual['pelvis']['head_m'][:2])<=1e-6)
        for name in ['pelvis','spine_01','spine_02','spine_03','neck','head']:
            y=unit(sub(actual[name]['tail_m'],actual[name]['head_m']))
            check(rows,'axial_upright:'+name,'+Z',y,close(y,[0,0,1],1e-5))
        for side,sign in [('l',1),('r',-1)]:
            direction=[sign/math.sqrt(2),0,-1/math.sqrt(2)]
            for name in ['upper_arm','forearm','hand']:
                b=actual[name+'_'+side];v=unit(sub(b['tail_m'],b['head_m']));angle=math.degrees(math.acos(max(-1,min(1,dot(v,direction)))))
                check(rows,'a_pose:'+name+'_'+side,'45deg arm down ±0.1deg',angle,angle<=.1)
            for digit in ['thumb','index','middle','ring','little']:
                target=[sign,0,0] if digit=='thumb' else direction
                for i in range(1,4):
                    b=actual[f'{digit}_{i:02}_{side}'];v=unit(sub(b['tail_m'],b['head_m']))
                    check(rows,'finger_pose:'+b['name'],'straight canonical digit direction',v,close(v,target,1e-5))
            for name in ['thigh','shin']:
                b=actual[name+'_'+side];v=unit(sub(b['tail_m'],b['head_m']))
                check(rows,'leg_rest:'+name+'_'+side,'straight -Z',v,close(v,[0,0,-1],1e-5))
            b=actual['toe_'+side];v=unit(sub(b['tail_m'],b['head_m']));check(rows,'toe_forward:'+side,'+Y',v,close(v,[0,1,0],1e-5))
            check(rows,'anatomical_side:'+side,'hip/shoulder on declared side',[actual['thigh_'+side]['head_m'][0],actual['upper_arm_'+side]['head_m'][0]],all(actual[n+'_'+side]['head_m'][0]*sign>0 for n in ['thigh','upper_arm']))
    required_controls=set(sk['required_controls'])|{'fk_'+n for n,b in expected.items() if b['deform']}
    check(rows,'animation_armature_name','stable canonical object suffix',manifest['armature'],manifest['armature']==manifest['asset_id']+'__armature_deform')
    check(rows,'body_inventory','nonempty unique body object set',manifest['body_objects'],bool(manifest['body_objects']) and len(set(manifest['body_objects']))==len(manifest['body_objects']))
    check(rows,'control_interface','all logical controls declared and resolve',sorted(required_controls-set(snapshot['resolved_controls'])),required_controls<=set(manifest['controls']) and required_controls<=set(snapshot['resolved_controls']))
    for key in ['ik_fk_arm_l','ik_fk_arm_r','ik_fk_leg_l','ik_fk_leg_r']:
        ref=manifest['controls'].get(key)
        check(rows,'ik_fk_switch:'+key,'canonical root property;0=FK,1=IK',ref,bool(ref and ref['object']==manifest['asset_id']+'__root' and ref['bone'] is None and ref.get('property')==key))
    for key in ['solver_bindings','joint_limit_bindings']:
        required={'ik_hand_l','ik_hand_r','ik_foot_l','ik_foot_r'} if key=='solver_bindings' else {'forearm_l','forearm_r','shin_l','shin_r'}
        check(rows,key,'required limb mappings',sorted(manifest[key]),required<=set(manifest[key]))
    observed={e['key']:e for e in snapshot['anchors']}
    check(rows,'anchor_uniqueness','no duplicates',len(snapshot['anchors']),len(snapshot['anchors'])==len(observed))
    for e in sk['anchors']:
        key=e['key'];decl=manifest['anchors'].get(key);obs=observed.get(key)
        ok=bool(decl and obs and obs['exists'])
        if ok:
            q=obs['rotation_quaternion_wxyz'];dq=decl['rotation_quaternion_wxyz']
            ok=(obs['object']==manifest['asset_id']+'__anchor_'+key==decl['object'] and obs['bone']==decl['bone']==e['bone'] and close(obs['position_m'],decl['position_m']) and abs(norm(q)-1)<1e-5 and abs(norm(dq)-1)<1e-5 and abs(abs(dot(q,dq))-1)<1e-5)
            if key=='floor_contact':ok=ok and close(obs['position_m'],[0,0,0])
            if 'contact_' in key:ok=ok and abs(obs['position_m'][2])<=1e-5
            if key=='pelvis' and 'pelvis' in actual:ok=ok and close(obs['position_m'],actual['pelvis']['head_m'])
            if key.startswith('hand_grip_') and e['bone'] in actual:
                bone=actual[e['bone']];v=sub(bone['tail_m'],bone['head_m']);length=norm(v);delta=sub(obs['position_m'],bone['head_m']);along=dot(delta,unit(v))
                radial=norm(sub(delta,[along*x for x in unit(v)]))
                ok=ok and -.1*length<=along<=1.5*length and radial<=length
            if 'contact_' in key and e['bone'] in actual:
                bone=actual[e['bone']];ok=ok and obs['position_m'][0]*(1 if key.endswith('_l') else -1)>0 and abs(obs['position_m'][0]-bone['head_m'][0])<=norm(sub(bone['tail_m'],bone['head_m']))
            y,z=[0,1,0],[0,0,1]
            if key.startswith('hand_grip_'):
                sign=1 if key.endswith('_l') else -1;y=[sign/math.sqrt(2),0,1/math.sqrt(2)];z=[0,1,0]
            if key=='back_support':y,z=[0,0,1],[0,-1,0]
            ok=ok and close(quaternion_axis(q,1),y,1e-5) and close(quaternion_axis(q,2),z,1e-5)
        check(rows,'attachment:'+key,'canonical name/owner/frame/datum',obs,ok)
    wanted={e['id'] for e in cat['entries'] if e['required']};bindings=manifest['muscle_bindings'];muscles={e['id']:e for e in snapshot['muscles']}
    check(rows,'muscle_coverage','all core IDs declared and observed; no duplicates',sorted(wanted-set(muscles)),wanted<=set(bindings) and wanted<=set(muscles) and len(muscles)==len(snapshot['muscles']))
    check(rows,'muscle_ids','only known IDs',sorted(set(bindings)-wanted),set(bindings)<=wanted and set(muscles)<=wanted)
    properties=[];mask_references=[]
    for mid,b in bindings.items():
        properties.extend([b['primary_property'],b['secondary_property']]);mask_references.append((b['object'],b['vertex_group']));m=muscles.get(mid)
        ok=bool(m and b['object'] in manifest['body_objects'] and b['primary_property']=='highlight_primary__'+mid and b['secondary_property']=='highlight_secondary__'+mid and m['object']==b['object'] and m['vertex_group']==b['vertex_group'] and m['positive_vertices']>0 and 0<=m['weight_min']<=m['weight_max']<=1 and m['primary_exists'] and m['secondary_exists'] and 0<=m['primary']<=1 and 0<=m['secondary']<=1)
        check(rows,'muscle_binding:'+mid,'nonempty independently controlled mask, weights/controls0..1',m,ok)
    check(rows,'independent_highlight_properties','distinct primary/secondary properties per ID',len(properties),len(properties)==len(set(properties)))
    check(rows,'independent_muscle_masks','distinct body/group binding per region',len(mask_references),len(mask_references)==len(set(mask_references)))
    check(rows,'clothing_inventory','metadata matches actual clothing presence',snapshot['clothing_present'],snapshot['clothing_present']==bool(manifest['clothing_objects']))
    check(rows,'clothing_highlight_route','visible through clothing; backend proof required for release',manifest['clothing_highlight'],not snapshot['clothing_present'] or manifest['clothing_highlight']['mode']!='none' and bool(manifest['clothing_highlight']['implementation_reference']))
    fingerprint=rest_fingerprint(snapshot['bones'])
    check(rows,'rest_profile_hash','observed fingerprint=declared fingerprint',fingerprint,fingerprint==snapshot['rest_profile_sha256']==manifest['rest_profile']['sha256'])
    if release:
        check(rows,'measured_observer','read-only Blender observation, not synthetic test data',snapshot['observer'],snapshot['observer'].startswith('blender_read_only/'))
        def pinned(path,digest):
            if not path or not digest:return False
            p=(base/path).resolve()
            return p.is_relative_to(base.resolve()) and p.is_file() and sha(p)==digest
        check(rows,'rest_profile_artifact','pinned bone rest-profile file',manifest['rest_profile']['path'],pinned(manifest['rest_profile']['path'],manifest['rest_profile']['sha256']))
        # Profile files use canonical compact JSON hashing, not incidental formatting.
        if manifest['rest_profile']['path']:
            p=(base/manifest['rest_profile']['path']).resolve()
            if p.is_relative_to(base.resolve()) and p.is_file():
                check(rows,'rest_profile_contents','same measured bones',str(p),rest_fingerprint(read(p))==fingerprint)
        for limb in ['forearm_l','forearm_r','shin_l','shin_r']:
            lim=manifest['joint_limits'].get(limb)
            check(rows,'approved_joint_limits:'+limb,'recorded finite limits and approval reference',lim,bool(lim and lim['approval_reference'] and all(a<=b for a,b in zip(lim['min_radians'],lim['max_radians']))))
        statuses={e['check']:e for e in manifest['evidence']}
        for name in EVIDENCE:
            e=statuses.get(name);check(rows,'release_evidence:'+name,'pass plus pinned existing evidence',e,bool(e and e['status']=='pass' and pinned(e['path'],e['sha256'])))
        for role in ['illustration','animation']:
            profiles=[p for p in manifest['export_profiles'] if p['role']==role]
            check(rows,'export_profile:'+role,'one approved pinned profile',profiles,len(profiles)==1 and profiles[0]['approved'] and pinned(profiles[0]['settings_path'],profiles[0]['settings_sha256']))
            if len(profiles)==1 and pinned(profiles[0]['settings_path'],profiles[0]['settings_sha256']):
                doc=read(base/profiles[0]['settings_path']);rows+=export_checks(doc)
                check(rows,'export_profile_role:'+role,'role/id match, approval reference present',doc.get('role'),doc.get('role')==role and doc.get('id')==profiles[0]['id'] and bool(doc.get('approval_reference')))
        unresolved=set(read(D/'contract.json')['open_decisions'])-set(manifest['resolved_decisions'])
        check(rows,'release_decisions','H01-H05 resolved with linked asset evidence',sorted(unresolved),not unresolved)
        asset_path=(base/manifest['asset_manifest']).resolve()
        valid=asset_path.is_relative_to(base.resolve()) and asset_path.is_file()
        if valid:
            asset=read(asset_path);source=(R/asset.get('source','')).resolve()
            valid=asset.get('id')==manifest['asset_id'] and source.is_relative_to(R.resolve()) and source.is_file() and sha(source)==snapshot['source_sha256']
        check(rows,'source_and_manifest_pin','observed source hash and asset identity match',str(asset_path),valid)
    return rows

def compare_characters(first,first_snapshot,second,second_snapshot):
    rows=character_checks(first,first_snapshot)+character_checks(second,second_snapshot)
    valid=all(r['result']=='PASS' for r in rows)
    same=first_snapshot.get('rest_profile_sha256')==second_snapshot.get('rest_profile_sha256')
    a={e['key']:e for e in first_snapshot.get('anchors',[])};b={e['key']:e for e in second_snapshot.get('anchors',[])}
    deltas=[]
    for key in sorted(set(a)&set(b)):
        position=norm(sub(a[key]['position_m'],b[key]['position_m']))
        rotation=abs(abs(dot(a[key]['rotation_quaternion_wxyz'],b[key]['rotation_quaternion_wxyz']))-1)
        deltas.append({'anchor':key,'position_delta_m':position,'quaternion_dot_deviation':rotation})
    return {'result':'PASS' if valid else 'FAIL','compatibility':'direct_pose_candidate' if valid and same else 'retarget_required' if valid else 'incompatible',
            'rest_profiles_equal':same,'contact_recalibration_required':not same or any(e['position_delta_m']>1e-6 or e['quaternion_dot_deviation']>1e-5 for e in deltas),
            'anchor_differences':deltas,'checks':rows,'limits':'Candidate interface classification only; no action, skin deformation, reach or collision test performed.'}

def report(rows):
    return {'contract':'168h_human_model@1.0.0','checks':rows,'pass':sum(r['result']=='PASS' for r in rows),'fail':sum(r['result']=='FAIL' for r in rows),'limits':'Structural data checks are not proof of anatomy, deformation, retargeting or rendering quality. Release evidence must be independently reviewed.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--snapshot');p.add_argument('--compare-manifest');p.add_argument('--compare-snapshot');p.add_argument('--activation');p.add_argument('--export-profile');p.add_argument('--release',action='store_true');p.add_argument('--output');args=p.parse_args()
    rows=registry_checks()
    if args.activation:rows+=activation_checks(read(args.activation))
    if args.export_profile:rows+=export_checks(read(args.export_profile))
    if args.manifest or args.snapshot:
        if not(args.manifest and args.snapshot):p.error('--manifest and --snapshot are required together')
        rows+=character_checks(read(args.manifest),read(args.snapshot),args.release,Path(args.manifest).resolve().parent)
    elif args.release:p.error('--release requires a manifest and measured snapshot')
    result=report(rows)
    if args.compare_manifest or args.compare_snapshot:
        if not(args.manifest and args.snapshot and args.compare_manifest and args.compare_snapshot):p.error('comparison requires both complete manifest/snapshot pairs')
        comparison=compare_characters(read(args.manifest),read(args.snapshot),read(args.compare_manifest),read(args.compare_snapshot))
        result=report(rows+comparison.pop('checks'));result['pair_compatibility']=comparison
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output:Path(args.output).write_text(text)
    print('HUMAN_V1',result['pass'],'PASS',result['fail'],'FAIL')
    if result['fail']:raise SystemExit(1)

if __name__=='__main__':main()
