"""Pure-data fixtures only: no bpy, meshes, armatures, actions or scenes created."""
from pathlib import Path
import copy,json,sys,unittest,subprocess
import tempfile
from unittest.mock import patch
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts/pipeline'))
from validate_human_contract import *

def synthetic():
    sk=read(D/'skeleton.json');m=read(R/'templates/human/human-contract.example.json')
    m['height_m']=1.8;m['body_objects']=['test_body'];bones=[];geo={}
    geo.update(root=([0,0,0],[0,0,.1]))
    levels=[1,1.1,1.25,1.4,1.55,1.65,1.8]
    for i,n in enumerate(['pelvis','spine_01','spine_02','spine_03','neck','head']):geo[n]=([0,0,levels[i]],[0,0,levels[i+1]])
    for side,sign in [('l',1),('r',-1)]:
        geo['clavicle_'+side]=([0,0,1.55],[.18*sign,0,1.55]);v=[sign/math.sqrt(2),0,-1/math.sqrt(2)]
        start=geo['clavicle_'+side][1]
        for n,length in [('upper_arm',.30),('forearm',.26),('hand',.10)]:
            end=[a+length*b for a,b in zip(start,v)];geo[n+'_'+side]=(start,end);start=end
        for digit in ['thumb','index','middle','ring','little']:
            start=geo['hand_'+side][1];direction=[sign,0,0] if digit=='thumb' else v
            for i in range(1,4):
                end=[a+.025*b for a,b in zip(start,direction)];geo[f'{digit}_{i:02}_{side}']=(start,end);start=end
        geo['thigh_'+side]=([.1*sign,0,1],[.1*sign,0,.55]);geo['shin_'+side]=([.1*sign,0,.55],[.1*sign,0,.08])
        geo['foot_'+side]=([.1*sign,0,.08],[.1*sign,.16,.03]);geo['toe_'+side]=([.1*sign,.16,.03],[.1*sign,.22,.03])
    for spec in sk['bones']:
        head,tail=geo[spec['name']];y=unit(sub(tail,head));z=sub([0,1,0],[dot([0,1,0],y)*v for v in y])
        if norm(z)<1e-6:z=sub([0,0,1],[dot([0,0,1],y)*v for v in y])
        bones.append({**spec,'head_m':head,'tail_m':tail,'z_axis':unit(z),'pose_identity':True})
    controls=set(sk['required_controls'])|{'fk_'+b['name'] for b in bones if b['deform']}
    m['controls']={k:{'object':'test_controls','bone':None} for k in controls}
    for key in ['ik_fk_arm_l','ik_fk_arm_r','ik_fk_leg_l','ik_fk_leg_r']:m['controls'][key]={'object':m['asset_id']+'__root','bone':None,'property':key}
    for key in ['ik_hand_l','ik_hand_r','ik_foot_l','ik_foot_r']:m['solver_bindings'][key]={'object':'test_rig','bone':'test_solver'}
    for name in ['forearm_l','forearm_r','shin_l','shin_r']:
        m['joint_limit_bindings'][name]={'object':'test_rig','bone':name};m['joint_limits'][name]={'min_radians':[0,0,0],'max_radians':[1,0,0],'approval_reference':None}
    anchors=[]
    for e in sk['anchors']:
        pos=[0,0,0] if not e['bone'] else geo[e['bone']][0].copy()
        if 'contact' in e['key']:pos[2]=0
        quat=[1,0,0,0]
        if e['key']=='back_support':quat=[math.sqrt(.5),math.sqrt(.5),0,0]
        if e['key']=='hand_grip_l':quat=[-.2705980500730985,.2705980500730985,.6532814824381883,.6532814824381883]
        if e['key']=='hand_grip_r':quat=[.2705980500730985,-.2705980500730985,.6532814824381883,.6532814824381883]
        decl={'object':m['asset_id']+'__anchor_'+e['key'],'bone':e['bone'],'position_m':pos,'rotation_quaternion_wxyz':quat}
        m['anchors'][e['key']]=decl;anchors.append({'key':e['key'],**decl,'exists':True})
    muscles=[]
    for e in read(D/'muscles.json')['entries']:
        mid=e['id'];binding={'object':'test_body','vertex_group':mid,'primary_property':'highlight_primary__'+mid,'secondary_property':'highlight_secondary__'+mid};m['muscle_bindings'][mid]=binding
        muscles.append({'id':mid,'object':'test_body','vertex_group':mid,'positive_vertices':3,'weight_min':0,'weight_max':1,'primary_exists':True,'secondary_exists':True,'primary':0,'secondary':0})
    fingerprint=rest_fingerprint(bones);m['rest_profile']['sha256']=fingerprint
    identity=[[1 if i==j else 0 for j in range(4)] for i in range(4)]
    s={'contract':'168h_human_snapshot@1.0.0','source_sha256':'0'*64,'units':'METRIC','scale_length':1,'root_matrix':identity,'armature_matrix':copy.deepcopy(identity),'collection_offset_m':[0,0,0],'body_min_z_m':0,'body_height_m':1.8,'hierarchy_valid':True,'transforms_normalized':True,'skinning_valid':True,'ik_valid':True,'joint_constraints_valid':True,'bones':bones,'anchors':anchors,'resolved_controls':sorted(controls),'muscles':muscles,'clothing_present':False,'rest_profile_sha256':fingerprint,'observer':'synthetic_test_only'}
    return m,s

class ContractTests(unittest.TestCase):
    def setUp(self):self.m,self.s=synthetic()
    def failed(self,name):
        rows=character_checks(self.m,self.s)
        self.assertTrue(any(r['result']=='FAIL' and r['check'].startswith(name) for r in rows),name)
    def test_registry(self):self.assertFalse(any(r['result']=='FAIL' for r in registry_checks()))
    def test_registry_drift_fails(self):
        with patch('validate_human_contract.sha',return_value='0'*64):
            self.assertTrue(any(r['check'].startswith('contract_pin:') and r['result']=='FAIL' for r in registry_checks()))
    def test_valid_data(self):self.assertFalse(any(r['result']=='FAIL' for r in character_checks(self.m,self.s)))
    def test_pair_direct_pose(self):self.assertEqual(compare_characters(self.m,self.s,copy.deepcopy(self.m),copy.deepcopy(self.s))['compatibility'],'direct_pose_candidate')
    def test_pair_retarget_required(self):
        m,s=copy.deepcopy(self.m),copy.deepcopy(self.s);next(b for b in s['bones'] if b['name']=='head')['tail_m'][2]=1.85;s['body_height_m']=m['height_m']=1.85
        s['rest_profile_sha256']=m['rest_profile']['sha256']=rest_fingerprint(s['bones'])
        result=compare_characters(self.m,self.s,m,s);self.assertEqual(result['compatibility'],'retarget_required');self.assertTrue(result['contact_recalibration_required'])
    def test_pair_incompatible(self):
        m,s=copy.deepcopy(self.m),copy.deepcopy(self.s);s['bones'].pop();self.assertEqual(compare_characters(self.m,self.s,m,s)['compatibility'],'incompatible')
    def test_no_finger(self):self.s['bones']=[b for b in self.s['bones'] if b['name']!='index_03_l'];self.failed('skeleton_structure')
    def test_wrong_parent(self):self.s['bones'][10]['parent']='root';self.failed('bone_contract')
    def test_duplicate_bone(self):self.s['bones'].append(self.s['bones'][-1]);self.failed('skeleton_structure')
    def test_extra_deform_bone(self):self.s['bones'].append({**self.s['bones'][-1],'name':'custom_twist'});self.failed('skeleton_structure')
    def test_wrong_roll(self):self.s['bones'][10]['z_axis']=[1,0,0];self.failed('bone_frame')
    def test_t_pose_rejected(self):b=next(b for b in self.s['bones'] if b['name']=='upper_arm_l');b['tail_m']=[b['head_m'][0]+.3,0,b['head_m'][2]];self.failed('a_pose')
    def test_shifted_root(self):self.s['root_matrix'][2][3]=.1;self.failed('root_matrix')
    def test_scale(self):self.s['scale_length']=.01;self.failed('units')
    def test_floor(self):self.s['body_min_z_m']=.01;self.failed('body_floor')
    def test_pelvis_projection(self):next(b for b in self.s['bones'] if b['name']=='pelvis')['head_m'][0]=.1;self.failed('pelvis_floor_projection')
    def test_pose_not_rest(self):self.s['bones'][10]['pose_identity']=False;self.failed('bone_frame')
    def test_missing_pole(self):self.s['resolved_controls'].remove('pole_elbow_l');self.failed('control_interface')
    def test_ik_fk_switch(self):self.m['controls']['ik_fk_arm_l']['property']='other';self.failed('ik_fk_switch')
    def test_ik(self):self.s['ik_valid']=False;self.failed('ik_valid')
    def test_constraint(self):self.s['joint_constraints_valid']=False;self.failed('joint_constraints_valid')
    def test_bad_anchor_owner(self):self.s['anchors'][3]['bone']='root';self.failed('attachment')
    def test_shifted_anchor(self):self.s['anchors'][0]['position_m'][2]=.1;self.failed('attachment')
    def test_nonunit_anchor(self):self.s['anchors'][0]['rotation_quaternion_wxyz']=[2,0,0,0];self.failed('attachment')
    def test_anchor_orientation_not_copied_metadata(self):self.s['anchors'][0]['rotation_quaternion_wxyz']=[0,0,0,1];self.m['anchors']['floor_contact']['rotation_quaternion_wxyz']=[0,0,0,1];self.failed('attachment')
    def test_missing_muscle(self):self.s['muscles'].pop();self.failed('muscle_coverage')
    def test_empty_mask(self):self.s['muscles'][0]['positive_vertices']=0;self.failed('muscle_binding')
    def test_wrong_mask_object(self):self.s['muscles'][0]['object']='other';self.failed('muscle_binding')
    def test_shared_control(self):items=list(self.m['muscle_bindings'].values());items[1]['primary_property']=items[0]['primary_property'];self.failed('independent_highlight_properties')
    def test_shared_mask(self):items=list(self.m['muscle_bindings'].values());items[1]['vertex_group']=items[0]['vertex_group'];self.failed('independent_muscle_masks')
    def test_bad_highlight_range(self):self.s['muscles'][0]['primary']=2;self.failed('muscle_binding')
    def test_clothes_hide_highlight(self):self.s['clothing_present']=True;self.m['clothing_objects']=['shirt'];self.failed('clothing_highlight_route')
    def test_rest_fingerprint(self):self.s['rest_profile_sha256']='1'*64;self.failed('rest_profile_hash')
    def test_no_export_release(self):rows=character_checks(self.m,self.s,True);self.assertTrue(any(r['check']=='export_profile:animation' and r['result']=='FAIL' for r in rows))
    def test_synthetic_not_release_evidence(self):rows=character_checks(self.m,self.s,True);self.assertTrue(any(r['check']=='measured_observer' and r['result']=='FAIL' for r in rows))
    def test_schema_unknown_field(self):self.m['invented_standard']=1;self.failed('human-character-v1_schema')
    def test_schema_bool_is_not_number(self):self.s['scale_length']=True;self.failed('human-snapshot-v1_schema')
    def test_schema_nonfinite(self):self.s['scale_length']=float('nan');self.failed('human-snapshot-v1_schema')
    def test_unsupported_schema_fails_closed(self):self.assertTrue(schema_errors(1,{'oneOf':[]}))
    def test_unused_unsupported_schema_fails_closed(self):self.assertTrue(schema_errors({}, {'type':'object','properties':{'unused':{'oneOf':[]}}}))
    def test_cli_fail_exit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'activation.json';out=Path(d)/'result.json';doc=read(R/'templates/human/exercise-muscles.example.json');doc['primary']={'unknown':1};p.write_text(json.dumps(doc))
            result=subprocess.run([sys.executable,str(R/'scripts/pipeline/validate_human_contract.py'),'--activation',str(p),'--output',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,1);self.assertGreater(read(out)['fail'],0)
    def test_documented_lists_match_registries(self):
        prose=(D/'README.md').read_text()
        found=re.findall(r'^\| `([a-z0-9_]+)` \| (`[a-z0-9_]+`|None) \| (true|false) \| (true|false) \|$',prose,re.M)
        expected=[(b['name'],'`'+b['parent']+'`' if b['parent'] else 'None',str(b['connected']).lower(),str(b['deform']).lower()) for b in read(D/'skeleton.json')['bones']]
        self.assertEqual(found,expected)
        table=(D/'muscle-catalog.md').read_text()
        for e in read(D/'muscles.json')['entries']:
            if e['side']=='l':self.assertIn('| `'+e['id']+'` | `'+e['pair_id']+'_r` | '+e['anatomical_name']+' | '+e['group']+' | '+e['representation']+' / '+e['region']+' |',table)
    def test_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text('{"id":1,"id":2}')
            with self.assertRaises(ValueError):read(p)
    def test_activation(self):
        d=read(R/'templates/human/exercise-muscles.example.json');mid=read(D/'muscles.json')['entries'][0]['id'];d['primary']={mid:1};self.assertFalse(any(r['result']=='FAIL' for r in activation_checks(d)));d['secondary']={mid:.5};self.assertTrue(any(r['result']=='FAIL' for r in activation_checks(d)))
    def test_activation_unknown_muscle(self):d=read(R/'templates/human/exercise-muscles.example.json');d['primary']={'invented':1};self.assertTrue(any(r['result']=='FAIL' for r in activation_checks(d)))
    def test_draft_templates_schema_valid(self):self.assertFalse(schema_errors(read(R/'templates/human/human-contract.example.json'),read(R/'schemas/human-character-v1.schema.json')))
    def test_export_requirements(self):
        doc={'id':'test','contract':'168h_human_model@1.0.0','role':'animation','format':'unselected_test_only','blender_version':'test','exporter_version':'test','source_units':'meters','source_axes':{'up':'+Z','forward':'+Y','subject_left':'+X'},'axis_conversion':[[1 if i==j else 0 for j in range(4)] for i in range(4)],'frame_rate_fps':30,'start_frame':1,'end_frame':2,'baked_animation':True,'control_bones_included':False,'bone_names':[b['name'] for b in read(D/'skeleton.json')['bones']],'muscle_state_delivery':'sidecar','root_motion':'preserved','approval_reference':None}
        self.assertFalse(any(r['result']=='FAIL' for r in export_checks(doc)))
        for field,value in [('baked_animation',False),('control_bones_included',True),('frame_rate_fps',None),('muscle_state_delivery','pixels')]:
            altered=copy.deepcopy(doc);altered[field]=value;self.assertTrue(any(r['result']=='FAIL' for r in export_checks(altered)),field)
        doc['axis_conversion'][0][0]=-1;self.assertTrue(any(r['check']=='export_axis_conversion' and r['result']=='FAIL' for r in export_checks(doc)))

if __name__=='__main__':unittest.main()
