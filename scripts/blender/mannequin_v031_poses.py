"""Core poses plus multi-direction shoulder/hip tests; scene-owned grip contact adapter."""
import bpy,math,json
from mathutils import Matrix,Quaternion,Vector
import mannequin_review_common as mc
import mannequin_core_poses as core
import mannequin_v03_poses as baseline
from mannequin_v031_common import A,ID,RID
coords=core.coords
POSES=baseline.POSES+['arms_lateral','arms_forward','arms_diagonal','shoulder_internal_rotation','shoulder_external_rotation','hip_abduction','lunge','xray_disabled']
def pose(name):
 mc.get(ID+'__root')['grip_contact_enabled']=0.
 if name in baseline.POSES:
  baseline.pose(name)
  if name=='bar_grip' and (A/'grip-contact-fit.json').exists():
   fit=json.loads((A/'grip-contact-fit.json').read_text())
   for side,sign in [('l',1),('r',-1)]:
    target=mc.get(ID+'__control_ik_hand_'+side);target.matrix_world.translation+=Vector(fit['wrist_contact_offset_m'])
    for digit,angles in fit['digits'].items():
     if digit=='thumb':
      z,x,y,m,d=angles;mc.get(RID+'__armature_solver').pose.bones['thumb_01_'+side].rotation_quaternion=Quaternion((0,0,1),sign*z)@Quaternion((1,0,0),x)@Quaternion((0,1,0),sign*y);mc.rotate('thumb_02_'+side,(1,0,0),m);mc.rotate('thumb_03_'+side,(1,0,0),d)
     else:
      for i,angle in enumerate(angles,1):mc.rotate(f'{digit}_{i:02}_{side}',(1,0,0),angle)
   mc.get(ID+'__root')['grip_contact_enabled']=1.;mc.update()
  return
 core.pose('neutral_a_pose')
 for side,sign in [('l',1),('r',-1)]:
  if name=='arms_lateral':mc.rotate('upper_arm_'+side,(0,0,1),-sign*math.pi/4)
  if name in ['arms_forward','shoulder_internal_rotation','shoulder_external_rotation']:
   q=Quaternion((1,0,0),math.pi/2)
   if name.startswith('shoulder_'):q=q@Quaternion((0,1,0),sign*math.radians(45 if 'internal' in name else -45));mc.rotate('forearm_'+side,(1,0,0),math.radians(75))
   if name.startswith('shoulder_') and side=='r':continue
   mc.get(RID+'__armature_solver').pose.bones['upper_arm_'+side].rotation_quaternion=q
  if name=='arms_diagonal':mc.get(RID+'__armature_solver').pose.bones['upper_arm_'+side].rotation_quaternion=Quaternion((1,0,0),math.radians(65))@Quaternion((0,0,1),-sign*math.radians(65))
  if name=='hip_abduction':mc.rotate('thigh_'+side,(0,0,1),-sign*math.radians(25));mc.rotate('shin_'+side,(1,0,0),-math.radians(35))
  if name=='lunge':mc.rotate('thigh_'+side,(1,0,0),math.radians(70 if side=='l' else -20));mc.rotate('shin_'+side,(1,0,0),-math.radians(90 if side=='l' else 35))
 mc.update()
 if name=='lunge':mc.get(ID+'__root').location.z-=float(coords()[:,2].min());mc.update()
