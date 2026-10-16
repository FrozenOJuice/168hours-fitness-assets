"""Anatomical weight ownership refinement of isolated study; preserves masters."""
import bpy,json,sys,math,numpy as np
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;core.pose('neutral_a_pose');o=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');before=digest(SOURCE);p=np.array([v.co[:] for v in o.data.vertices]);x,y,z=p.T;ax=abs(x)
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
core_names=[b.name for b in arm.data.bones if b.use_deform];indices={o.vertex_groups[n].index:n for n in core_names};edited=0
for v in o.data.vertices:
 xx,yy,zz=p[v.index];a=abs(xx);side='l' if xx>0 else 'r';old={indices[g.group]:g.weight for g in v.groups if g.group in indices};target={};alpha=0
 if 1.10<zz<1.54 and a<.35:
  alpha=float(smooth((zz-1.10)/.08)*(1-smooth((zz-1.49)/.05))*(1-smooth((a-.30)/.05)))
  h=float(smooth((a-(.155+.10*max(1.4-zz,0)))/.070)*smooth((zz-1.15)/.15));c=(1-h)*float(smooth((zz-1.38)/.09)*smooth((a-.055)/.10))*.35;sp=float(smooth((zz-1.25)/.15));target={'upper_arm_'+side:h,'clavicle_'+side:c,'spine_03':(1-h-c)*sp,'spine_02':(1-h-c)*(1-sp)}
 elif .20<zz<1.01 and a<.24:
  alpha=float(smooth((zz-.20)/.055)*(1-smooth((zz-.97)/.04)))
  knee=arm.data.bones['shin_'+side].head_local.z;shin=float(smooth((knee+.07-zz)/.14));hip=float(smooth((.995-zz)/.145));target={'pelvis':1-hip,'thigh_'+side:hip*(1-shin),'shin_'+side:hip*shin}
 if alpha>0:
  edited+=1
  for n in core_names:o.vertex_groups[n].add([v.index],old.get(n,0)*(1-alpha)+target.get(n,0)*alpha,'REPLACE')
# Smooth only the edited upper-torso weights along actual cage edges.
names=['spine_01','spine_02','spine_03','clavicle_l','upper_arm_l','clavicle_r','upper_arm_r'];lookup={o.vertex_groups[n].index:i for i,n in enumerate(names)};w=np.zeros((len(p),len(names)))
for v in o.data.vertices:
 for g in v.groups:
  if g.group in lookup:w[v.index,lookup[g.group]]=g.weight
edges=np.array([e.vertices[:] for e in o.data.edges]);src=np.r_[edges[:,0],edges[:,1]];dst=np.r_[edges[:,1],edges[:,0]];counts=np.bincount(dst,minlength=len(p));tot=w.sum(1);region=smooth((z-1.15)/.1)*(1-smooth((z-1.49)/.05))*(1-smooth((ax-.30)/.05))
for _ in range(20):
 avg=np.stack([np.bincount(dst,weights=w[src,i],minlength=len(p))/np.maximum(counts,1) for i in range(len(names))],axis=1);w+=(avg-w)*(.65*region)[:,None];w*= (tot/np.maximum(w.sum(1),1e-20))[:,None]
for v in o.data.vertices:
 if region[v.index]<=0:continue
 for i,n in enumerate(names):o.vertex_groups[n].add([v.index],float(w[v.index,i]),'REPLACE')
# Bake only surface finish at neutral for consistent topology and floor evidence.
bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier='anatomy_surface_finish');p=np.array([v.co[:] for v in o.data.vertices]);floor=float(p[:,2].min());scale=1.75/np.ptp(p[:,2]);p[:,2]-=floor;p*=scale;o.data.vertices.foreach_set('co',p.astype(np.float32).ravel());o.data.update()
# Keep actual target export53bones unchanged; sub-millimeter surface normalization is recorded.
# Local tonal contrast improves anatomy readability under no-shadow rendering.
ng=o.modifiers['illustration_and_highlights'].node_group
for n in ng.nodes:
 if n.bl_idname=='ShaderNodeMath' and n.operation=='MULTIPLY_ADD':n.inputs[1].default_value=.78;n.inputs[2].default_value=.35
 if n.bl_idname=='ShaderNodeMixRGB' and not n.inputs[1].is_linked:n.inputs[1].default_value=(.10,.13,.15,1);n.inputs[2].default_value=(.58,.62,.64,1)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'bind-refinement.json',{'input_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'edited_cage_vertices':edited,'surface_finish_baked':True,'floor_translation_m':floor,'surface_scale':float(scale),'weights':'Localized torso/clavicle/upper-arm ownership,20edge-neighbor fairing steps; explicit smooth thigh/shin and pelvis transition','canonical_rest_profile':'unchanged by surface finish normalization'})
