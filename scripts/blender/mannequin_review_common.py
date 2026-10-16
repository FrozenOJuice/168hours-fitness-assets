"""Asset-local pose/highlight tools, not a shared human standard."""
from pathlib import Path
import bpy,sys,math
from mathutils import Quaternion,Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import R,A,ID,RID,SOURCE,SK,CAT,G
MAPPING=None
def get(name):return MAPPING[name] if MAPPING is not None else bpy.data.objects[name]
def update():
    root=get(ID+'__root');root.update_tag();bpy.context.scene.frame_set(2);bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
def neutral():
    root=get(ID+'__root');solver=get(RID+'__armature_solver')
    for b in solver.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=(1,0,0,0);b.location=(0,0,0);b.scale=(1,1,1)
    for key in ['ik_fk_arm_l','ik_fk_arm_r','ik_fk_leg_l','ik_fk_leg_r','xray_enabled']:root[key]=0.
    for e in CAT['entries']:
        for role in ['primary','secondary']:root['highlight_'+role+'__'+e['id']]=0.
    update()
def rotate(name,axis,angle):get(RID+'__armature_solver').pose.bones[name].rotation_quaternion=Quaternion(Vector(axis),angle)
def highlight(mid,role='primary',value=1):get(ID+'__root')['highlight_'+role+'__'+mid]=float(value)
def grip(side,amount=1):
    for digit in ['index','middle','ring','little']:
        for index,angle in [(1,.65),(2,1.15),(3,.75)]:rotate(f'{digit}_{index:02}_{side}',(1,0,0),angle*amount)
    for index,angle in [(1,.40),(2,.65),(3,.6)]:rotate(f'thumb_{index:02}_{side}',(1,0,0),angle*amount)
def pose(name):
    neutral();root=get(ID+'__root')
    if name=='bend':
        rotate('upper_arm_l',(1,0,0),.3);rotate('forearm_l',(1,0,0),1.25);rotate('forearm_r',(1,0,0),.7);rotate('thigh_l',(1,0,0),.3);rotate('shin_l',(1,0,0),-1.1);rotate('foot_l',(1,0,0),.8)
        highlight('muscle_biceps_brachii_l');highlight('muscle_deltoid_anterior_l','secondary');grip('l',.45)
    if name=='muscles':
        for side in ['l','r']:
            for n in ['pectoralis_major','biceps_brachii']:highlight('muscle_'+n+'_'+side)
            for n in ['deltoid_anterior','deltoid_middle','deltoid_posterior','triceps_brachii']:highlight('muscle_'+n+'_'+side,'secondary')
    if name=='grip':rotate('forearm_l',(1,0,0),.8);grip('l');grip('r');highlight('muscle_biceps_brachii_l','secondary')
    if name in ['xray','xray_bend']:
        root['xray_enabled']=1.;highlight('muscle_vastus_intermedius_l')
        if name=='xray_bend':rotate('thigh_l',(1,0,0),.25);rotate('shin_l',(1,0,0),-.7)
    update()

def enable_ik(limb,side):
    """Seed the perfectly straight V1 rest chain before enabling solver; not a snap tool."""
    rotate(('forearm' if limb=='arm' else 'shin')+'_'+side,(1,0,0),.5 if limb=='arm' else -.5)
    get(ID+'__root')['ik_fk_'+limb+'_'+side]=1.;update()
