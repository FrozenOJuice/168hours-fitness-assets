"""Seven reproducible human foundation tests, independent of exercise scenes."""
import bpy,math,numpy as np
from mathutils import Vector,Matrix,Quaternion
import mannequin_review_common as mc
ID=mc.ID;RID=mc.RID
POSES=['neutral_a_pose','arms_raised','elbow_flexion','seated','lying_supine','hip_flexion_knee_bend','bar_grip']
def coords():
 body=mc.get(ID+'__mesh_body');e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();p=np.array([(e.matrix_world@v.co)[:] for v in m.vertices]);e.to_mesh_clear();return p

def snap_ik(limb,side):
 """Deterministic nonstretch switch from canonical straight rest to current solved contact."""
 solver=mc.get(RID+'__armature_solver');tip='hand' if limb=='arm' else 'foot';hinge='forearm' if limb=='arm' else 'shin';upper='upper_arm' if limb=='arm' else 'thigh';mc.update()
 target=mc.get(ID+'__control_ik_'+tip+'_'+side);target.matrix_world=solver.matrix_world@solver.pose.bones[tip+'_'+side].matrix
 start=solver.matrix_world@solver.pose.bones[upper+'_'+side].head;end=solver.matrix_world@solver.pose.bones[hinge+'_'+side].tail;joint=solver.matrix_world@solver.pose.bones[hinge+'_'+side].head;axis=(end-start).normalized();bend=joint-(start+axis*(joint-start).dot(axis))
 if bend.length<1e-5:bend=Vector((0,-1 if limb=='arm' else 1,0))
 else:bend.normalize()
 pole=mc.get(ID+'__control_pole_'+('elbow' if limb=='arm' else 'knee')+'_'+side);pole.matrix_world.translation=joint+bend*.30
 mc.rotate(hinge+'_'+side,(1,0,0),.15 if limb=='arm' else -.15);mc.get(ID+'__root')['ik_fk_'+limb+'_'+side]=1.;mc.get(RID+'__armature_solver').update_tag();mc.update()

def pose(name):
 assert name in POSES;mc.neutral();root=mc.get(ID+'__root');root.matrix_world=Matrix.Identity(4)
 if name=='arms_raised':
  for side,sign in [('l',1),('r',-1)]:mc.rotate('clavicle_'+side,(0,0,1),-sign*math.radians(25));mc.rotate('upper_arm_'+side,(0,0,1),-sign*math.radians(110))
 if name in ['elbow_flexion','bar_grip']:
  for side in ['l','r']:mc.rotate('forearm_'+side,(1,0,0),math.radians(110 if name=='elbow_flexion' else 85))
 if name=='seated':
  for side in ['l','r']:mc.rotate('thigh_'+side,(1,0,0),math.pi/2);mc.rotate('shin_'+side,(1,0,0),-math.pi/2)
  mc.update();root.location.z-=float(coords()[:,2].min())
 if name=='lying_supine':
  root.matrix_world=Matrix.Rotation(math.pi/2,4,'X');mc.update();root.location.z-=float(coords()[:,2].min())
 if name=='hip_flexion_knee_bend':mc.rotate('thigh_l',(1,0,0),math.radians(80));mc.rotate('shin_l',(1,0,0),-math.radians(105))
 if name=='bar_grip':
  for side,sign in [('l',1),('r',-1)]:
   snap_ik('arm',side);target=mc.get(ID+'__control_ik_hand_'+side);target.matrix_world=Matrix.Translation((sign*.29,.25,1.05));mc.get(ID+'__control_pole_elbow_'+side).matrix_world.translation=(sign*.32,-.25,1.15)
   # The static reference uses retained measured per-digit fit parameters.
   import json
   from build_anatomical_mannequin import A
   fit=json.loads((A/'grip-fit.json').read_text())['digits']
   for digit in ['index','middle','ring','little']:
    for i,angle in enumerate(fit[digit]['angles_radians'],1):mc.rotate(f'{digit}_{i:02}_{side}',(1,0,0),angle)
   z,x,m,d=fit['thumb']['angles_radians'];solver=mc.get(RID+'__armature_solver');solver.pose.bones['thumb_01_'+side].rotation_quaternion=Quaternion((0,0,1),sign*z)@Quaternion((1,0,0),x)
   mc.rotate('thumb_02_'+side,(1,0,0),m);mc.rotate('thumb_03_'+side,(1,0,0),d)
 mc.update()

def snap_fk(limb,side):
 """Preserve solved limb frames while returning to the private canonical FK facade."""
 solver=mc.get(RID+'__armature_solver');chain=[n+'_'+side for n in (['upper_arm','forearm','hand'] if limb=='arm' else ['thigh','shin','foot'])];mc.update();solved={n:solver.pose.bones[n].matrix.copy() for n in chain};mc.get(ID+'__root')['ik_fk_'+limb+'_'+side]=0.;mc.update()
 for n in chain:solver.pose.bones[n].matrix=solved[n];bpy.context.view_layer.update()
 solver.update_tag();mc.update()
