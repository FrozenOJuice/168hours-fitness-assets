"""Measured palm contact + three-axis thumb opposition; read-only native fitting."""
import bpy,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Quaternion,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
import mannequin_v03_poses as baseline
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;baseline.pose('bar_grip');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');before=digest(SOURCE);names=[b.name for b in arm.data.bones if b.use_deform];lookup={body.vertex_groups[n].index:i for i,n in enumerate(names)};allp=np.array([v.co[:] for v in body.data.vertices]);W=np.zeros((len(allp),len(names)))
for v in body.data.vertices:
 for g in v.groups:
  if g.group in lookup:W[v.index,lookup[g.group]]=g.weight
handcols=[i for i,n in enumerate(names) if n.endswith('_l') and n.startswith(('hand_','thumb_','index_','middle_','ring_','little_'))];ids=np.flatnonzero(W[:,handcols].sum(1)>.75);P=allp[ids];W=W[ids];dominant=W.argmax(1);bar=np.array([.318,1.08]);radius=.014

def qmul(a,b):
 aw,ax,ay,az=np.moveaxis(a,-1,0);bw,bx,by,bz=np.moveaxis(b,-1,0);return np.stack((aw*bw-ax*bx-ay*by-az*bz,aw*bx+ax*bw+ay*bz-az*by,aw*by-ax*bz+ay*bw+az*bx,aw*bz+ax*by-ay*bx+az*bw),axis=-1)
def deform():
 real=[];dual=[]
 for n in names:
  M=arm.pose.bones[n].matrix@arm.data.bones[n].matrix_local.inverted();r=np.array(M.to_quaternion());t=np.r_[0,np.array(M.translation)];real.append(r);dual.append(.5*qmul(t,r))
 real=np.array(real);dual=np.array(dual);weight=W*np.where(real[dominant]@real.T<0,-1.,1.);r=weight@real;d=weight@dual;norm=np.linalg.norm(r,axis=1);r/=norm[:,None];d/=norm[:,None];d-=r*np.sum(r*d,axis=1)[:,None];conj=r*np.array([1,-1,-1,-1]);return qmul(qmul(r,np.c_[np.zeros(len(P)),P]),conj)[:,1:]+2*qmul(d,conj)[:,1:]
err=float(np.linalg.norm(core.coords()[ids]-deform(),axis=1).max());print('SAMPLER_ERROR',err,flush=True);assert err<2e-5
# Fit contact from actual palm surface; consumer offset keeps published rest anchors unchanged.
palm=W[:,names.index('hand_l')]>.70;h=arm.data.bones['hand_l'];t=(P-np.array(h.head_local))@np.array((h.tail_local-h.head_local).normalized());patch=palm&(t>.025)&(t<.078)&(P[:,1]>.004);assert patch.sum()>30
q=deform();rad=np.linalg.norm(q[:,1:]-bar,axis=1);indices=np.flatnonzero(patch);j=indices[np.argmin(rad[patch])];direction=(q[j,1:]-bar)/rad[j];offset=np.r_[0,-(rad[j]-radius)*direction];target=mc.get(ID+'__control_ik_hand_l');target.matrix_world.translation+=Vector(offset);mc.update();q=deform();print('PALM_OFFSET',offset.tolist(),'GAP',float(np.min(np.linalg.norm(q[patch,1:]-bar,axis=1)))-radius,flush=True)
body.hide_viewport=True;mc.get(ID+'__helper_linear_skin').hide_viewport=True;results={};diag={}
old=json.loads((PREVIOUS/'grip-fit.json').read_text())
for digit in ['index','middle','ring','little','thumb']:
 cols=[names.index(f'{digit}_{i:02}_l') for i in range(1,4)];mask=W[:,cols].sum(1)>.55;tips=W[:,cols[-1]]>.45
 if digit=='thumb':
  idx=W[:,names.index('index_03_l')]>.45;center=deform()[idx].mean(0);u=center[1:]-bar;u/=np.linalg.norm(u);thumb_target=np.r_[center[0]+.012,bar-u*(radius+.004)];print('THUMB_TARGET_YZ',thumb_target.tolist(),flush=True)
 def apply(a):
  if digit=='thumb':
   z,x,y,m,d=a;solver.pose.bones['thumb_01_l'].rotation_quaternion=Quaternion((0,0,1),z)@Quaternion((1,0,0),x)@Quaternion((0,1,0),y);mc.rotate('thumb_02_l',(1,0,0),m);mc.rotate('thumb_03_l',(1,0,0),d)
  else:
   for i,angle in enumerate(a,1):mc.rotate(f'{digit}_{i:02}_l',(1,0,0),float(angle))
  solver.update_tag();mc.update()
 def cost(a):
  apply(a);q=deform();rad=np.linalg.norm(q[:,1:]-bar,axis=1);pen=max(0,radius-float(rad[mask].min()));near=abs(float(np.quantile(rad[tips],.1))-(radius+.0006));distance=float(np.linalg.norm(q[tips].mean(0)-thumb_target)) if digit=='thumb' else .0;regular=.002*np.linalg.norm(np.array(a)-np.array([.9,1.1,.7])) if digit!='thumb' else 0;return near+2*pen+12*max(0,pen-.005)+1.2*distance+regular
 best=([old['thumb'][0],old['thumb'][1],0,old['thumb'][2],old['thumb'][3]] if digit=='thumb' else old[digit]);score=cost(best)
 starts=([[zz,xx,yy,mm,.5] for zz in [-1.4,-.7,0,.7,1.4] for xx in [-1.2,-.6,0,.6,1.2] for yy in [-1.3,0,1.3] for mm in [.6,1.2]] if digit=='thumb' else [[a,b,.7] for a in [.65,1.,1.35] for b in [.6,1.1,1.5]])
 for a in starts:
  c=cost(a)
  if c<score:best,score=a.copy(),c
 for step in [.35,.15,.06,.025]:
  for repeat in range(2):
   for k in range(len(best)):
    for delta in [-step,step]:
     a=best.copy();lo=-1.5 if digit=='thumb' and k in [0,1,2] else -.4 if digit!='thumb' and k==0 else 0;hi=1.5 if digit=='thumb' and k in [0,2] else 1.8;a[k]=float(np.clip(a[k]+delta,lo,hi));c=cost(a)
     if c<score:best,score=a,c
 apply(best);results[digit]=best;q=deform();r=np.linalg.norm(q[:,1:]-bar,axis=1);diag[digit]={'closest_gap_m':float(r[mask].min()-radius),'tip_centroid_m':q[tips].mean(0).tolist(),'objective':float(score)};print('DIGIT',digit,best,diag[digit],flush=True)
write_json(A/'grip-contact-fit.json',{'shaft_radius_m':radius,'shaft_center_m':[0,.318,1.08],'wrist_contact_offset_m':offset.tolist(),'digits':results,'thumb_order':['base_z','base_x','base_y_opposition','middle_x','distal_x'],'method':'Measured actual palm contact, consumer-owned wrist offset, independent bounded digit fit; 3-axis thumb base and opposing index-distal target. Mirrored right, final actual Blender mesh checks required.','sampler_max_error_m':err,'diagnostics':diag,'source_sha256':before,'script_sha256':digest(Path(__file__))});assert digest(SOURCE)==before
