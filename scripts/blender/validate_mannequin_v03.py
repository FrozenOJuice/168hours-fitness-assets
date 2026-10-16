"""Read-only anatomy-study diagnostics; explicit failures, not anatomical certification."""
import bpy,bmesh,json,sys,math,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
import mannequin_v03_poses as poses
checks=[];diagnostics={}
def check(name,ok,actual,expected):checks.append({'check':name,'result':'PASS' if ok else 'FAIL','actual':actual,'expected':expected})
def geometry(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();p=np.array([(e.matrix_world@v.co)[:] for v in me.vertices]);faces=[f.vertices[:] for f in me.polygons];e.to_mesh_clear();return p,faces

def bvh(p,faces,mask):return BVHTree.FromPolygons([Vector(v) for v in p],[f for f in faces if all(mask[i] for i in f)])
def colors(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();attr=me.color_attributes['Color'];c=np.empty(len(attr.data)*4,dtype=np.float32);attr.data.foreach_get('color',c);e.to_mesh_clear();return c.reshape(-1,4)
def run():
 before=digest(SOURCE);fsbefore=digest(FS);plan=json.loads((A/'plan.json').read_text());bad=[p for p,h in plan['protected_sha256'].items() if digest(R/p)!=h];check('preserved_work',not bad,{'protected_files':len(plan['protected_sha256']),'changed':bad},'All protected masters, equipment, V1 and prior fixtures unchanged')
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;core.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');root=mc.get(ID+'__root');rest,faces=geometry(body)
 check('floor_and_stature',abs(float(rest[:,2].min()))<1e-5 and abs(float(np.ptp(rest[:,2]))-1.75)<1e-5,{'floor_m':float(rest[:,2].min()),'height_m':float(np.ptp(rest[:,2]))},'Floor0 and provisional1.75m,10um diagnostic tolerance')
 bm=bmesh.new();bm.from_mesh(body.data);nonmanifold=sum(not e.is_manifold for e in bm.edges);seen=set();components=0
 for v in bm.verts:
  if v.index in seen:continue
  stack=[v];seen.add(v.index);components+=1
  while stack:
   a=stack.pop()
   for edge in a.link_edges:
    b=edge.other_vert(a)
    if b.index not in seen:seen.add(b.index);stack.append(b)
 bm.free();check('continuous_closed_skin',nonmanifold==0 and components==1,{'nonmanifold_edges':nonmanifold,'components':components,'vertices':len(rest),'faces':len(faces)},'One continuous closed neutral body')
 helper=mc.get(ID+'__helper_linear_skin');check('hybrid_shared_geometry',helper.data==body.data and helper.hide_render,{'shared_mesh':helper.data==body.data,'helper_hidden_render':helper.hide_render},'Second skinning evaluation shares exact mesh datablock; not duplicate visible geometry')
 # Dynamic independent colors, actual evaluated geometry color data.
 base=colors(body);root['highlight_primary__muscle_pectoralis_major_l']=1.;mc.update();primary=colors(body);right=(rest[:,0]<-.055)&(rest[:,2]>1.29)&(rest[:,2]<1.41);changed=int(np.sum(np.max(abs(primary-base),axis=1)>.01));rightdelta=float(np.max(abs(primary[right]-base[right])));check('primary_highlight_local',changed>50 and rightdelta<.001,{'changed_vertices':changed,'opposite_pectoral_max_delta':rightdelta},'Selected primary changes actual surface colors while opposite pectoral remains unchanged within0.001')
 core.pose('neutral_a_pose');root['highlight_secondary__muscle_pectoralis_major_l']=1.;mc.update();secondary=colors(body);check('primary_secondary_distinct',float(np.max(abs(primary-secondary)))>.1,float(np.max(abs(primary-secondary))),'Independent primary/secondary channels produce distinct actual colors')
 core.pose('neutral_a_pose');root['xray_enabled']=1.;root['highlight_primary__muscle_vastus_intermedius_l']=1.;mc.update();cut,cutfaces=geometry(body);deep,dfaces=geometry(mc.get(ID+'__mesh_vastus_intermedius_l'));cx=arm.data.bones['thigh_l'].head_local.x;origin=Vector((cx,1,.735));direction=Vector((0,-1,0));skin=BVHTree.FromPolygons([Vector(v) for v in cut],cutfaces);muscle=BVHTree.FromPolygons([Vector(v) for v in deep],dfaces);hs=skin.ray_cast(origin,direction,2);hd=muscle.ray_cast(origin,direction,2);visible=hd[0] is not None and (hs[0] is None or hd[3]<hs[3]);check('localized_on_character_xray',len(cutfaces)<len(faces) and visible,{'removed_skin_faces':len(faces)-len(cutfaces),'deep_first_on_window_ray':visible,'deep_ray_distance_m':hd[3]},'Local aperture exposes a skinned deep volume on the character, before posterior body wall')
 # Existing FK/IK snap helpers on four limb cases, same tolerances as prior local suite.
 ik={}
 for limb,tip,delta in [('arm','hand',(0,.035,.02)),('leg','foot',(0,.06,.03))]:
  for side in ['l','r']:
   core.pose('neutral_a_pose');pre=solver.pose.bones[tip+'_'+side].matrix.copy();core.snap_ik(limb,side);target=mc.get(ID+'__control_ik_'+tip+'_'+side);target.matrix_world.translation+=Vector(delta);mc.update();actual=solver.pose.bones[tip+'_'+side].matrix.copy();err=(actual.translation-target.matrix_world.translation).length;core.snap_fk(limb,side);back=solver.pose.bones[tip+'_'+side].matrix;ik[limb+'_'+side]={'target_error_m':err,'IK_FK_return_error_m':(back.translation-actual.translation).length}
 check('four_IK_and_snap_cases',all(v['target_error_m']<.0001 and v['IK_FK_return_error_m']<.0001 for v in ik.values()),ik,'Four measured reachable targets and snap returns<0.1mm; sparse motion diagnostic only')
 bpy.ops.wm.open_mainfile(filepath=str(FS));suite=json.loads((F/'suite.json').read_text());check('all_saved_states',set(suite['poses'])==set(poses.POSES),list(suite['poses']),'All13documented pose/highlight/Xray states saved')
 for name,record in suite['poses'].items():
  s=bpy.data.scenes[record['scene']];bpy.context.window.scene=s;c=bpy.data.collections[record['character_collection']];mc.MAPPING={o.override_library.reference.name:o for o in c.all_objects if o.override_library};mc.update();body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');p,pf=geometry(body)
  count_ok=len(p)<=len(rest) if name.startswith('xray') else len(p)==len(rest)
  check(name+':linked_and_finite',bool(body.data.library) and count_ok and np.isfinite(p).all(),{'linked':bool(body.data.library),'vertices':len(p),'faces':len(pf)},'Shared linked skin and finite positions; only Xray intentionally removes faces and their unused vertices')
  lengths={b.name:abs((arm.pose.bones[b.name].tail-arm.pose.bones[b.name].head).length-b.length) for b in arm.data.bones};check(name+':bone_lengths',max(lengths.values())<1e-5,max(lengths.values()),'No canonical bone stretch>10um')
  info=body.modifiers['anatomy_hybrid_shoulder_skin'].node_group.nodes.get('Object Info');actualhelper=info.inputs['Object'].default_value;check(name+':private_helper_remap',actualhelper==mc.get(ID+'__helper_linear_skin'),actualhelper.name,'ObjectInfo points at this override helper, not another pose/library source')
  if name in ['seated','squat','hip_flexion_knee_bend']:
   results={}
   for side,sign in [('l',1),('r',-1)]:
    knee=arm.data.bones['shin_'+side].head_local.z;th=bvh(p,pf,(rest[:,0]*sign>.015)&(rest[:,2]>knee+.04)&(rest[:,2]<.84));calf=bvh(p,pf,(rest[:,0]*sign>.015)&(rest[:,2]<knee-.04)&(rest[:,2]>.14));n=len(th.overlap(calf));results[side]=n
   check(name+':disjoint_thigh_calf_crossings',all(n==0 for n in results.values()),results,'Zero disjoint thigh/calf triangle crossings outside±40mm knee transition; same local criterion as earlier prototype')
   left=bvh(p,pf,(rest[:,0]>.015)&(rest[:,2]<.84));right=bvh(p,pf,(rest[:,0]<-.015)&(rest[:,2]<.84));cross=len(left.overlap(right));check(name+':separate_leg_crossings',cross==0,cross,'Zero crossings between distinct left/right leg regions below hips')
  if name=='bar_grip':
   contacts={};anchors={}
   for side,sign in [('l',1),('r',-1)]:
    anchors[side]=(mc.get(ID+'__anchor_hand_grip_'+side).matrix_world.translation-Vector((sign*.30,.318,1.08))).length;by={}
    for digit in ['thumb','index','middle','ring','little','palm']:
     groups={body.vertex_groups['hand_'+side].index} if digit=='palm' else {body.vertex_groups[f'{digit}_{i:02}_{side}'].index for i in range(1,4)};indices=[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.7]
     rad=np.linalg.norm(p[indices,1:]-np.array([.318,1.08]),axis=1);m=float(rad.min());by[digit]={'closest_gap_m':max(0,m-.014),'max_sampled_penetration_m':max(0,.014-m),'samples':len(indices)}
    contacts[side]=by
   check('grip_anchor_alignment',max(anchors.values())<.0001,anchors,'Mirrored600mm grip stations on actual28mm shaft, anchor residual<0.1mm')
   pen=max(v['max_sampled_penetration_m'] for by in contacts.values() for v in by.values());gap=max(v['closest_gap_m'] for by in contacts.values() for k,v in by.items() if k not in ['thumb','palm']);check('grip_surface_samples',pen<=.002 and gap<=.005,{'max_sampled_penetration_m':pen,'max_finger_closest_gap_m':gap,'contacts':contacts},'Retained asset-local diagnostic≤2mm sampled penetration/≤5mm closest finger gap; not full-face collision or arbitrary gripping certification');diagnostics[name]=contacts
 check('sources_unchanged_by_validation',digest(SOURCE)==before and digest(FS)==fsbefore,{'character':digest(SOURCE),'study':digest(FS)},'Read-only native validation')
 summary={k:sum(c['result']==k for c in checks) for k in ['PASS','FAIL']};write_json(A/'study-validation.json',{'version':'0.3.0','date':'2026-10-16','source_sha256':before,'study_sha256':fsbefore,'validator_sha256':digest(Path(__file__)),'summary':summary,'checks':checks,'diagnostics':diagnostics,'scope':'Asset-local diagnostics; anatomy/style/manual/full coverage/release approval separate','limitations':['Sparse snapshots, not full motion or medical/clinical validation','Full self-containment and hand-face/cylinder collisions not certified','Missing muscle coverage remains FAIL','Artist review required; no production readiness claim']});print('STUDY_VALIDATION',summary);print('FAILURES',json.dumps([c for c in checks if c['result']=='FAIL']))
 if summary['FAIL']:raise SystemExit(1)
if __name__=='__main__':run()
