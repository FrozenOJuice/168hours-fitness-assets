"""Retain proven shoulder ownership; diffuse connected weights instead of repainting arm skin."""
import bpy,sys,numpy as np,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
bpy.ops.wm.open_mainfile(filepath=str(PREVIOUS/(ID+'.blend')));mc.MAPPING=None;o=mc.get(ID+'__mesh_body');names=[b.name for b in mc.get(ID+'__armature_deform').data.bones if b.use_deform];lookup={o.vertex_groups[n].index:i for i,n in enumerate(names)};p=np.array([v.co[:] for v in o.data.vertices]);W=np.zeros((len(p),len(names)))
for v in o.data.vertices:
 for g in v.groups:
  if g.group in lookup:W[v.index,lookup[g.group]]=g.weight
edges=np.array([e.vertices[:] for e in o.data.edges]);src=np.r_[edges[:,0],edges[:,1]];dst=np.r_[edges[:,1],edges[:,0]];counts=np.bincount(dst,minlength=len(p));region=np.exp(-((p[:,2]-1.38)/.15)**4-((abs(p[:,0])-.20)/.15)**4);cols=[names.index(n) for n in ['spine_01','spine_02','spine_03','clavicle_l','upper_arm_l','clavicle_r','upper_arm_r']];sub=W[:,cols];total=sub.sum(1)
for _ in range(70):
 avg=np.stack([np.bincount(dst,weights=sub[src,i],minlength=len(p))/np.maximum(counts,1) for i in range(len(cols))],axis=1);sub+=(avg-sub)*(.65*region)[:,None];sub*= (total/np.maximum(sub.sum(1),1e-15))[:,None]
W[:,cols]=sub;bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;core.pose('neutral_a_pose');o=mc.get(ID+'__mesh_body');before=digest(SOURCE);inds=np.flatnonzero(p[:,2]>1.1)
for i,n in enumerate(names):
 g=o.vertex_groups[n];g.remove(inds.tolist())
 for j in inds[W[inds,i]>1e-8]:g.add([int(j)],float(W[j,i]),'REPLACE')
for side in ['l','r']:o.modifiers.remove(o.modifiers['anatomy_shoulder_motion_'+side])
o.data.materials[0].surface_render_method='BLENDED'
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'skin-finalization.json',{'input_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'shoulder':'Restore original ownership above1.1m, then70mesh-neighbor diffusion steps of thorax/clavicle/humerus influences. Preserve per-vertex influence total; no new shoulder relaxation modifier. Retain original hybrid DQ/LBS and bound joint fairing.','rejected_trial':'Broad spatial repaint mistakenly put torso weights on upper-arm skin, producing forward-pose flaps. Narrowing repaint still worsened max stretch; rejected. New shoulders use original proven ownership, not rejected trial.','forward_trial_edge_ratios':{'previous_p95':1.68787,'selected_p95':1.58715,'previous_max':3.34871,'selected_max':3.55641},'xray':'Sorted alpha blending replaces dithering grain; continuous skin, same opacity field/material semantics','limitations':'p95improves but worst local edge stretch slightly increases; broad motion/visual tests still required, no full deformation success claim'})
