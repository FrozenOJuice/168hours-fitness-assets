"""Sampled multi-axis motion, old/new strain measurements and actual hand contact triangles."""
import bpy,sys,numpy as np,json,math
from pathlib import Path
from mathutils import Quaternion,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
import mannequin_v031_poses as poses
from validate_mannequin_v031 import geometry,bvh
checks=[];records={}
def check(n,ok,value,expected):checks.append({'check':n,'result':'PASS' if ok else 'FAIL','actual':value,'expected':expected})
for path,label in [(PREVIOUS/(ID+'.blend'),'v030'),(SOURCE,'v031')]:
 before=digest(path);bpy.ops.wm.open_mainfile(filepath=str(path));mc.MAPPING=None;body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');rest=np.array([v.co[:] for v in body.data.vertices]);edges=np.array([e.vertices[:] for e in body.data.edges]);base=np.linalg.norm(rest[edges[:,0]]-rest[edges[:,1]],axis=1);upper=(abs(rest[edges[:,0],0])>.1)&(abs(rest[edges[:,0],0])<.34)&(rest[edges[:,0],2]>1.15)&(rest[edges[:,0],2]<1.5);lower=(rest[edges[:,0],2]>.35)&(rest[edges[:,0],2]<1.0);records[label]=[]
 cases=[('shoulder_'+direction+'_'+str(deg),direction,deg,0) for direction in ['lateral','forward','diagonal'] for deg in [0,20,40,60,80,100]]+ [('shoulder_twist_'+str(deg),'twist',deg,0) for deg in [-60,-30,30,60]]+[('hip_'+str(h)+'_knee_'+str(k),'lower',h,k) for h in [0,45,90,110] for k in [0,45,90,130]]
 for name,kind,angle,knee in cases:
  core.pose('neutral_a_pose');root=mc.get(ID+'__root')
  if 'grip_contact_enabled' in root:root['grip_contact_enabled']=0.
  for side,sign in [('l',1),('r',-1)]:
   a=math.radians(angle)
   if kind=='lateral':q=Quaternion((0,0,1),-sign*a)
   elif kind=='forward':q=Quaternion((1,0,0),a)
   elif kind=='diagonal':q=Quaternion((1,0,0),.7*a)@Quaternion((0,0,1),-sign*.7*a)
   elif kind=='twist':q=Quaternion((1,0,0),math.pi/2)@Quaternion((0,1,0),sign*a)
   else:mc.rotate('thigh_'+side,(1,0,0),a);mc.rotate('shin_'+side,(1,0,0),-math.radians(knee));continue
   mc.get(RID+'__armature_solver').pose.bones['upper_arm_'+side].rotation_quaternion=q
  mc.update();p,faces=geometry(body);lengths=[abs((b.tail-b.head).length-arm.data.bones[b.name].length) for b in arm.pose.bones];valid=bool(np.isfinite(p).all()) and max(lengths)<1e-5 and len(p)==len(rest);check(label+':'+name+':finite_rigid_bones',valid,{'max_bone_length_error_m':max(lengths),'finite':bool(np.isfinite(p).all())},'Finite full skin and canonical lengths preserved within10um')
  ratio=np.linalg.norm(p[edges[:,0]]-p[edges[:,1]],axis=1)/np.maximum(base,1e-10);mask=lower if kind=='lower' else upper;rec={'case':name,'canonical_local_angle_deg':angle,'knee_flexion_deg':knee,'edge_stretch_ratio_p50_p95_p99_max':np.quantile(ratio[mask],[.5,.95,.99,1]).tolist()}
  if kind=='lower' and label=='v031' and knee>=90:
   collisions={}
   for side,sign in [('l',1),('r',-1)]:
    z=arm.data.bones['shin_'+side].head_local.z;th=bvh(p,faces,(rest[:,0]*sign>.015)&(rest[:,2]>z+.04)&(rest[:,2]<.84));calf=bvh(p,faces,(rest[:,0]*sign>.015)&(rest[:,2]<z-.04)&(rest[:,2]>.14));collisions[side]=len(th.overlap(calf))
   rec['disjoint_thigh_calf_crossings']=collisions;check(name+':knee_crossings',not any(collisions.values()),collisions,'Zero disjoint thigh/calf triangle crossings outside40mm joint transition; retained earlier local criterion')
  records[label].append(rec)
  print('SWEEP',label,name,flush=True)
 check(label+':native_unchanged',digest(path)==before,digest(path),'Read-only validation')
# Actual current skin contact, not only an optimizer estimate.
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;poses.pose('bar_grip');body=mc.get(ID+'__mesh_body');p,faces=geometry(body);enabled=mc.get(ID+'__root')['grip_contact_enabled'];mc.get(ID+'__root')['grip_contact_enabled']=0.;mc.update();unprojected,_=geometry(body);correction=np.linalg.norm(p-unprojected,axis=1);check('contact_correction_bound',float(correction.max())<=.006,float(correction.max()),'Private contact correction<=6mm; asset-local soft-tissue diagnostic, no contact force claim')
handgroup={g.index for g in body.vertex_groups if g.name.startswith(('hand_','thumb_','index_','middle_','ring_','little_'))};mask=np.array([sum(g.weight for g in v.groups if g.group in handgroup)>.75 for v in body.data.vertices]);tri=[]
for f in faces:
 if all(mask[i] for i in f):
  for j in range(1,len(f)-1):tri.append([f[0],f[j],f[j+1]])
t=p[np.array(tri),1:]-np.array([.318,1.08]);a=t[:,0];b=t[:,1];c=t[:,2];best=np.ones(len(t))*1e9
cross=lambda u,v:u[:,0]*v[:,1]-u[:,1]*v[:,0]
orient=cross(b-a,c-a);s1=cross(b-a,-a);s2=cross(c-b,-b);s3=cross(a-c,-c);inside=((s1>=0)&(s2>=0)&(s3>=0)|(s1<=0)&(s2<=0)&(s3<=0))&(abs(orient)>1e-14)
for u,v in [(a,b),(b,c),(c,a)]:
 d=v-u;f=np.clip(-np.sum(u*d,axis=1)/np.maximum(np.sum(d*d,axis=1),1e-20),0,1);best=np.minimum(best,np.linalg.norm(u+f[:,None]*d,axis=1))
best[inside]=0;penetration=max(0,.014-float(best.min()));check('hand_triangle_cylinder_clearance',penetration<=.0001,{'triangles':len(tri),'min_radial_clearance_m':float(best.min()-.014),'max_penetration_m':penetration},'Selected actual hand triangles clear infinite shaft cylinder within0.1mm; wrist transition, finger/finger collision and end caps excluded')
# Diameter changes must recompute contacts; verify adapter itself responds in editable source.
mc.get(ID+'__root')['grip_contact_enabled']=1.
for radius in [.010,.016]:
 mc.get(ID+'__root')['grip_radius_m']=radius;mc.update();q,_=geometry(body);r=np.linalg.norm(q[mask,1:]-np.array([.318,1.08]),axis=1);check('cylinder_radius_'+str(radius),float(r.min())>=radius-.0001,float(r.min()-radius),'Same general contact projection responds to radius without source geometry edits; finger-pose refit still needed')
summary={s:sum(c['result']==s for c in checks) for s in ['PASS','FAIL']};write_json(A/'movement-validation.json',{'version':'0.3.1','source_sha256':digest(SOURCE),'previous_sha256':digest(PREVIOUS/(ID+'.blend')),'validator_sha256':digest(Path(__file__)),'summary':summary,'checks':checks,'sampled_motion':records,'scope':'38local-transform snapshots per body, not full anatomical motion or clinical ROM. Strain ratios are observations, not accepted quality thresholds. Explicit collision diagnostics remain failures if present.'});print('MOVEMENT_VALIDATION',summary);print('FAILURES',json.dumps([c for c in checks if c['result']=='FAIL']))
if summary['FAIL']:raise SystemExit(1)
