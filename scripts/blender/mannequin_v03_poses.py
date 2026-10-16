"""Anatomy-study poses; no exercise scenes. Private controls, canonical output."""
import math,json
import bpy
from mathutils import Matrix,Quaternion,Vector
import mannequin_review_common as mc
import mannequin_core_poses as core
from mannequin_v03_common import A,ID,RID
coords=core.coords
POSES=['neutral_a_pose','neutral_standing','arms_raised','elbow_flexion','seated','lying_supine','hip_flexion_knee_bend','squat','bar_grip','muscles_neutral','muscles_flexed','xray_neutral','xray_flexed']
def pose(name):
 if name in core.POSES and name!='bar_grip':core.pose(name);return
 core.pose('neutral_a_pose');root=mc.get(ID+'__root')
 if name=='neutral_standing':
  for side,sign in [('l',1),('r',-1)]:mc.rotate('upper_arm_'+side,(0,0,1),sign*math.pi/4)
 if name=='squat':
  for side in ['l','r']:mc.rotate('thigh_'+side,(1,0,0),math.radians(100));mc.rotate('shin_'+side,(1,0,0),math.radians(-130));mc.rotate('foot_'+side,(1,0,0),math.radians(30))
  mc.rotate('spine_01',(1,0,0),math.radians(12));mc.update();root.location.z-=float(core.coords()[:,2].min())
 if name=='bar_grip':
  for side,sign in [('l',1),('r',-1)]:
   mc.rotate('forearm_'+side,(1,0,0),1.2);mc.update();core.snap_ik('arm',side);mc.get(ID+'__control_ik_hand_'+side).matrix_world=Matrix.Translation((sign*.30,.26,1.05));mc.get(ID+'__control_pole_elbow_'+side).matrix_world.translation=(sign*.35,-.25,1.15)
   angles=json.loads((A/'grip-fit.json').read_text()) if (A/'grip-fit.json').exists() else {}
   for digit in ['index','middle','ring','little']:
    for i,angle in enumerate(angles.get(digit,[.9,1.,.7]),1):mc.rotate(f'{digit}_{i:02}_{side}',(1,0,0),angle)
   z,x,m,d=angles.get('thumb',[.2,.5,.55,.6]);mc.get(RID+'__armature_solver').pose.bones['thumb_01_'+side].rotation_quaternion=Quaternion((0,0,1),sign*z)@Quaternion((1,0,0),x);mc.rotate('thumb_02_'+side,(1,0,0),m);mc.rotate('thumb_03_'+side,(1,0,0),d)
 if name.startswith('muscles'):
  if name.endswith('flexed'):core.pose('elbow_flexion')
  for side in ['l','r']:
   for n in ['pectoralis_major','biceps_brachii']:mc.highlight('muscle_'+n+'_'+side)
   mc.highlight('muscle_deltoid_anterior_'+side,'secondary');mc.highlight('muscle_rectus_femoris_'+side,'secondary')
 if name.startswith('xray'):
  if name.endswith('flexed'):core.pose('hip_flexion_knee_bend')
  root['xray_enabled']=1.;mc.highlight('muscle_vastus_intermedius_l')
 mc.update()
