"""Fit a static28mm grip, using exact DQ hand sampling verified against Blender first.
No source/rig save. Values remain review-only; final Blender geometry is rechecked.
"""
import bpy,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Quaternion
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
import mannequin_v03_poses as poses
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;poses.pose('bar_grip');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');before=digest(SOURCE);names=[b.name for b in arm.data.bones if b.use_deform];lookup={body.vertex_groups[n].index:i for i,n in enumerate(names)};allp=np.array([v.co[:] for v in body.data.vertices]);W=np.zeros((len(allp),len(names)))
for v in body.data.vertices:
 for g in v.groups:
  if g.group in lookup:W[v.index,lookup[g.group]]=g.weight
handcols=[i for i,n in enumerate(names) if n.endswith('_l') and n.startswith(('hand_','thumb_','index_','middle_','ring_','little_'))];selected=W[:,handcols].sum(1)>.75;ids=np.flatnonzero(selected);P=allp[ids];W=W[ids];dominant=W.argmax(1);bar=np.array([.318,1.080])
def qmul(a,b):
 aw,ax,ay,az=np.moveaxis(a,-1,0);bw,bx,by,bz=np.moveaxis(b,-1,0)
 return np.stack((aw*bw-ax*bx-ay*by-az*bz,aw*bx+ax*bw+ay*bz-az*by,aw*by-ax*bz+ay*bw+az*bx,aw*bz+ax*by-ay*bx+az*bw),axis=-1)
def deform():
 real=[];dual=[]
 for n in names:
  M=arm.pose.bones[n].matrix@arm.data.bones[n].matrix_local.inverted();r=np.array(M.to_quaternion());t=np.r_[0,np.array(M.translation)];real.append(r);dual.append(.5*qmul(t,r))
 real=np.array(real);dual=np.array(dual);sign=np.where(real[dominant]@real.T<0,-1.,1.);weight=W*sign;r=weight@real;d=weight@dual;norm=np.linalg.norm(r,axis=1);r/=norm[:,None];d/=norm[:,None];d-=r*np.sum(r*d,axis=1)[:,None];conj=r*np.array([1,-1,-1,-1]);point=np.c_[np.zeros(len(P)),P];return qmul(qmul(r,point),conj)[:,1:]+2*qmul(d,conj)[:,1:]
actual=core.coords()[ids];approx=deform();err=float(np.linalg.norm(actual-approx,axis=1).max());print('DQ_SAMPLER_ERROR',err);assert err<2e-5,'Do not optimize an unverified geometry approximation'
body.hide_viewport=True;mc.get(ID+'__helper_linear_skin').hide_viewport=True
results={}
for digit in ['index','middle','ring','little','thumb']:
 cols=[names.index(f'{digit}_{i:02}_l') for i in range(1,4)];mask=W[:,cols].sum(1)>.55;tips=W[:,cols[-1]]>.45
 if not tips.any():tips=mask
 def apply(a):
  if digit=='thumb':
   z,x,m,d=a;solver.pose.bones['thumb_01_l'].rotation_quaternion=Quaternion((0,0,1),z)@Quaternion((1,0,0),x);mc.rotate('thumb_02_l',(1,0,0),m);mc.rotate('thumb_03_l',(1,0,0),d)
  else:
   for i,angle in enumerate(a,1):mc.rotate(f'{digit}_{i:02}_l',(1,0,0),float(angle))
  solver.update_tag();mc.update()
 def cost(a):
  apply(a);q=deform();r=np.linalg.norm(q[:,1:]-bar,axis=1);gap=float(np.mean(abs(r[tips]-.0146)));penetration=max(0,.014-float(r[mask].min()));return gap+12*penetration
 best=[.2,.5,.55,.6] if digit=='thumb' else [.9,1.,.7];score=cost(best)
 # Broad proximal/middle initialization prevents a collapsed curl local optimum.
 for aa in ([0,.4,.8,1.2] if digit=='thumb' else [.35,.8,1.25,1.65]):
  for bb in [.2,.7,1.2,1.65]:
   trial=best.copy();trial[0 if digit!='thumb' else 1]=aa;trial[1 if digit!='thumb' else 2]=bb;c=cost(trial)
   if c<score:best,score=trial,c
 for step in [.25,.10,.04]:
  for k in range(len(best)):
   for delta in [-step,step]:
    trial=best.copy();trial[k]=float(np.clip(trial[k]+delta,-.5 if digit=='thumb' and k==0 else 0,1.8));c=cost(trial)
    if c<score:best,score=trial,c
 apply(best);results[digit]=best;print('DIGIT',digit,best,score,flush=True)
write_json(A/'grip-fit.json',results);write_json(A/'grip-fit-method.json',{'source_sha256':before,'script_sha256':digest(Path(__file__)),'sampler_max_error_m':err,'method':'Measured canonical DQ hand sampling verified against Blender; bounded per-digit proximal/middle/distal coordinate descent, then final actual geometry validation required','shaft_center_m':[0,.318,1.08],'shaft_radius_m':.014,'scope':'One static underhand grip; no force, general hand pose, full-face collision or contact certification'});assert digest(SOURCE)==before
