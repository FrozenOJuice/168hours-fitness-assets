"""Read-only foundation geometry/contact diagnostics, distinct from Human V1 release gates."""
from pathlib import Path
import bpy,bmesh,sys,json,math,numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import R,A,ID,RID,SOURCE
import mannequin_review_common as mc
import mannequin_core_poses as cp
from barbell_20kg_common import digest,write_json
F=R/'scenes/templates/168h_template_mannequin_core_poses';FS=F/(F.name+'.blend');checks=[];diagnostics={}
def check(key,ok,actual,expected):checks.append({'check':key,'result':'PASS' if ok else 'FAIL','actual':actual,'expected':expected})
def get_mesh(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=np.array([(e.matrix_world@p.co)[:] for p in m.vertices]);faces=[p.vertices[:] for p in m.polygons];e.to_mesh_clear();return v,faces

def volume(points,tri):return abs(float(np.sum(np.einsum('ij,ij->i',points[tri[:,0]],np.cross(points[tri[:,1]],points[tri[:,2]])))/6))
def bvh(points,faces,selection):
 chosen=[f for f in faces if all(selection[i] for i in f)]
 return BVHTree.FromPolygons([Vector(p) for p in points],chosen) if chosen else None

def run():
 plan=json.loads((A/'foundation-plan.json').read_text());bad=[p for p,h in plan['protected_sha256'].items() if digest(R/p)!=h];check('protected_equipment_and_V1',not bad,bad,'No changes to protected213files')
 before=digest(SOURCE);bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;cp.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');root=mc.get(ID+'__root');rest,faces=get_mesh(body)
 check('source_height_floor',abs(np.ptp(rest[:,2])-1.75)<1e-5 and abs(rest[:,2].min())<1e-5,{'height_m':float(np.ptp(rest[:,2])),'floor_m':float(rest[:,2].min())},'1.75m stature and floor0, each±10um')
 bm=bmesh.new();bm.from_mesh(body.data);seen=set();components=0
 for v in bm.verts:
  if v.index in seen:continue
  components+=1;stack=[v];seen.add(v.index)
  while stack:
   q=stack.pop()
   for edge in q.link_edges:
    other=edge.other_vert(q)
    if other.index not in seen:seen.add(other.index);stack.append(other)
 nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();check('neutral_connected_manifold',components==1 and nonmanifold==0,{'components':components,'nonmanifold_edges':nonmanifold},'One closed continuous skin; no disconnected construction parts')
 edges=np.array([e.vertices[:] for e in body.data.edges]);restlength=np.linalg.norm(rest[edges[:,0]]-rest[edges[:,1]],axis=1);tri=np.array([[f[0],f[i],f[i+1]] for f in faces for i in range(1,len(f)-1)]);restvol=volume(rest,tri)
 # Deterministic IK startup/switch and orientation checks on actual rig.
 ikresults={}
 for limb,tip,hinge,shift in [('arm','hand','forearm',(0,.06,.03)),('leg','foot','shin',(0,.08,.04))]:
  for side in ['l','r']:
   cp.pose('neutral_a_pose');beforemat=solver.matrix_world@solver.pose.bones[tip+'_'+side].matrix;cp.snap_ik(limb,side);start=solver.matrix_world@solver.pose.bones[tip+'_'+side].matrix;target=mc.get(ID+'__control_ik_'+tip+'_'+side);snap=(start.translation-beforemat.translation).length;target.matrix_world.translation+=Vector(shift);solver.update_tag();mc.update();actual=solver.matrix_world@solver.pose.bones[tip+'_'+side].matrix;err=(actual.translation-target.matrix_world.translation).length;axiserr=max((actual.to_3x3().col[i].normalized()-target.matrix_world.to_3x3().col[i].normalized()).length for i in range(3));cp.snap_fk(limb,side);back=solver.matrix_world@solver.pose.bones[tip+'_'+side].matrix;backerr=(back.translation-actual.translation).length;backaxes=max((back.to_3x3().col[i].normalized()-actual.to_3x3().col[i].normalized()).length for i in range(3));ikresults[limb+'_'+side]={'switch_back_position_error_m':backerr,'switch_back_axis_error':backaxes,'switch_position_error_m':snap,'target_error_m':err,'orientation_axis_error':axiserr}
 check('four_native_IK_targets',all(v['target_error_m']<.0001 and v['orientation_axis_error']<1e-4 for v in ikresults.values()),ikresults,'Reachable seeded targets within0.1mm; axes within1e-4; local diagnostic criteria only')
 check('FK_to_IK_contact_continuity',all(v['switch_position_error_m']<.0001 for v in ikresults.values()),ikresults,'Position residual<0.1mm using explicit snap helper; no direct-toggle guarantee')
 check('IK_to_FK_frame_continuity',all(v['switch_back_position_error_m']<.0001 and v['switch_back_axis_error']<1e-4 for v in ikresults.values()),ikresults,'Explicit snap helper returns solved frames within0.1mm and1e-4 axes')
 # Five-angle knee stress sweep; numerical samples, not a complete animation certification.
 for angle in [0,30,60,90,105]:
  cp.pose('hip_flexion_knee_bend');mc.rotate('shin_l',(1,0,0),-math.radians(angle));mc.update();points,_=get_mesh(body);knee=arm.data.bones['shin_l'].head_local.z;th=bvh(points,faces,(rest[:,0]>.015)&(rest[:,2]>knee+.04)&(rest[:,2]<.84));ca=bvh(points,faces,(rest[:,0]>.015)&(rest[:,2]<knee-.04)&(rest[:,2]>.14));cross=len(th.overlap(ca));check('knee_sweep:'+str(angle),cross==0,{'angle_degrees':angle,'thigh_calf_crossings':cross},'Zero disjoint thigh/calf surface crossings with hip80deg and knee0..105deg')
 cp.pose('neutral_a_pose');check('source_bytes_unchanged',before==digest(SOURCE),digest(SOURCE),before)
 bpy.ops.wm.open_mainfile(filepath=str(FS));suite=json.loads((F/'suite.json').read_text());check('all_seven_saved_scenes',set(suite['poses'])==set(cp.POSES),list(suite['poses']),cp.POSES)
 for name,record in suite['poses'].items():
  s=bpy.data.scenes[record['scene']];bpy.context.window.scene=s;collection=bpy.data.collections[record['character_collection']];mc.MAPPING={o.override_library.reference.name:o for o in collection.all_objects if o.override_library};mc.update();body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver')
  if '--linear-test' in sys.argv:
   next(m for m in body.modifiers if m.type=='ARMATURE').use_deform_preserve_volume=False
  points,pfaces=get_mesh(body)
  check(name+':linked_mesh',bool(body.data.library),body.data.library.filepath if body.data.library else None,'Shared source geometry, no per-pose mesh copy')
  check(name+':finite_closed_surface',np.isfinite(points).all() and pfaces==faces,{'vertices':len(points),'faces':len(pfaces),'nonfinite':int(np.sum(~np.isfinite(points)))},'Same closed topology and finite evaluated vertices')
  lengths={b.name:abs((arm.matrix_world@arm.pose.bones[b.name].tail-arm.matrix_world@arm.pose.bones[b.name].head).length-b.length) for b in arm.data.bones};check(name+':no_bone_stretch',max(lengths.values())<1e-5,{'max_error_m':max(lengths.values())},'Every canonical bone length retained within10um')
  ratios=np.linalg.norm(points[edges[:,0]]-points[edges[:,1]],axis=1)/np.maximum(restlength,1e-10);vr=volume(points,tri)/restvol;diagnostics[name]={'volume_ratio':vr,'edge_stretch_p99':float(np.quantile(ratios,.99)),'edge_stretch_max':float(ratios.max()),'bounds_min_m':points.min(axis=0).tolist(),'bounds_max_m':points.max(axis=0).tolist()}
  check(name+':global_volume',.85<vr<1.15,vr,'Diagnostic whole-body volume ratio0.85..1.15; not proof of local anatomy')
  if name in ['neutral_a_pose','seated','hip_flexion_knee_bend','bar_grip']:
   kneeinfo={};masks={}
   for side,sign in [('l',1),('r',-1)]:
    sourcebone=arm.data.bones['shin_'+side];sourceknee=sourcebone.head_local;kneepoint=arm.matrix_world@arm.pose.bones['shin_'+side].head;mask=(abs(rest[:,2]-sourceknee.z)<.025)&(rest[:,0]*sign>.025);masks[side]=mask;width=float(np.ptp(points[mask,0]));rw=float(np.ptp(rest[mask,0]));kneeinfo[side]={'skeletal_x_drift_m':abs(kneepoint.x-sourceknee.x),'skin_x_width_ratio':width/rw}
   check(name+':knee_alignment',all(v['skeletal_x_drift_m']<1e-5 and .8<v['skin_x_width_ratio']<1.2 for v in kneeinfo.values()),kneeinfo,'No inward skeletal drift>10um; knee skin transverse width retained80..120%')
   gap=float(points[masks['l'],0].min()-points[masks['r'],0].max());check(name+':knee_surface_gap',gap>0,gap,'Positive lateral separation; projection overlap is not geometry collision')
   left=bvh(points,faces,(rest[:,0]>.015)&(rest[:,2]<.84));right=bvh(points,faces,(rest[:,0]<-.015)&(rest[:,2]<.84));overlap=len(left.overlap(right));check(name+':left_right_leg_intersections',overlap==0,overlap,'Zero triangle surface crossings for separate leg regions below hip')
  if name in ['seated','hip_flexion_knee_bend']:
   for side,sign in [('l',1),('r',-1)]:
    knee=arm.data.bones['shin_'+side].head_local.z;thigh=bvh(points,faces,(rest[:,0]*sign>.015)&(rest[:,2]>knee+.04)&(rest[:,2]<.84));calf=bvh(points,faces,(rest[:,0]*sign>.015)&(rest[:,2]<knee-.04)&(rest[:,2]>.14));n=len(thigh.overlap(calf));check(name+':thigh_calf_intersection_'+side,n==0,n,'Zero disjoint thigh/calf surface crossings outside knee transition')
  if name=='bar_grip':
   errors={};grip={}
   for side,sign in [('l',1),('r',-1)]:
    p=mc.get(ID+'__anchor_hand_grip_'+side).matrix_world.translation;errors[side]=(p-Vector((sign*.29,.318,1.082))).length
    # Canonical digit group membership selects actual skin, independent of metadata anchors.
    fingers={}
    for digit in ['thumb','index','middle','ring','little']:
     group_ids={body.vertex_groups[f'{digit}_{i:02}_{side}'].index for i in range(1,4)};indices=[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in group_ids)>.7];pnts=points[indices];rad=np.linalg.norm(pnts[:,1:]-np.array([.318,1.082]),axis=1);fingers[digit]={'minimum_radial_distance_m':float(rad.min()),'penetration_m':max(0,.014-float(rad.min())),'closest_gap_m':max(0,float(rad.min())-.014)}
    palmgroup=body.vertex_groups['hand_'+side].index;palm_indices=[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group==palmgroup)>.7];palmrad=np.linalg.norm(points[palm_indices,1:]-np.array([.318,1.082]),axis=1);fingers['palm']={'minimum_radial_distance_m':float(palmrad.min()),'penetration_m':max(0,.014-float(palmrad.min())),'closest_gap_m':max(0,float(palmrad.min())-.014)}
    grip[side]=fingers
   check('bar_grip:anchor_contacts',max(errors.values())<.0001,errors,'Both shaft grip centers within0.1mm, mirrored580mm spacing')
   diagnostics[name]['finger_contacts']=grip;maxpenetration=max(v['penetration_m'] for d in grip.values() for v in d.values());maxgap=max(v['closest_gap_m'] for d in grip.values() for k,v in d.items() if k not in ['thumb','palm']);check('bar_grip:finger_contacts',maxpenetration<=.002 and maxgap<=.005,{'max_penetration_m':maxpenetration,'max_finger_gap_m':maxgap,'by_digit':grip},'Proposed diagnostic limits≤2mm penetration and≤5mm closest finger gap; thumb opposition separately reviewed')
 check('all_artifacts_unchanged_by_validation',digest(SOURCE)==before and digest(FS)==suite['source_sha256'],{'source_sha256':digest(SOURCE),'suite_sha256':digest(FS)},'No source file saved by validator')
 summary={k:sum(c['result']==k for c in checks) for k in ['PASS','FAIL']};write_json((R/'exports/illustrations/foundation_linear_validation.json') if '--linear-test' in sys.argv else A/'foundation-validation.json',{'date':'2026-10-16','version':json.loads((A/'asset.json').read_text())['version'],'source_sha256':before,'suite_sha256':digest(FS),'validator_sha256':digest(Path(__file__)),'criteria_scope':'Asset-local diagnostic thresholds, not shared human approval or clinical limits','summary':summary,'checks':checks,'pose_diagnostics':diagnostics,'limitations':['Finite snapshots, not a continuous motion sweep','Full self intersection/containment and clinical joint limits not certified','Anatomy/style approval remains manual','Muscle coverage remainsincomplete; garments/variants/exports outside this pass']});print('FOUNDATION_CHECKS',json.dumps(summary));print('FAILURES',json.dumps([c for c in checks if c['result']=='FAIL']))
 if summary['FAIL']:raise SystemExit(1)
if __name__=='__main__':run()
