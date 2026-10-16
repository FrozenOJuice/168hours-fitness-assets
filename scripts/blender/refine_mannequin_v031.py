"""Refine the preserved CC0 skin: general joint ownership, traced regions, continuous translucency."""
import bpy,sys,json,math,numpy as np,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as cp
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;cp.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');before=digest(SOURCE);p=np.array([v.co[:] for v in body.data.vertices]);x,y,z=p.T;ax=abs(x);rawhash=hashlib.sha256(p.tobytes()).hexdigest()
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
# Blend joint skinning methods over continuous shoulder and inguinal regions.
a=body.data.attributes['anatomy_linear_shoulder_blend'];old=np.empty(len(p),dtype=np.float32);a.data.foreach_get('value',old);hip=.82*np.exp(-((z-.915)/.145)**4)*smooth((ax-.025)/.04)*(1-smooth((ax-.19)/.065));a.data.foreach_set('value',np.maximum(old,hip).astype(np.float32))
# Torso stays on thorax; lateral deltoid transitions to humerus. Buttock upper skin retains pelvis ownership.
names=[b.name for b in arm.data.bones if b.use_deform];lookup={body.vertex_groups[n].index:i for i,n in enumerate(names)};W=np.zeros((len(p),len(names)))
for v in body.data.vertices:
 for g in v.groups:
  if g.group in lookup:W[v.index,lookup[g.group]]=g.weight
for side,sign in [('l',1),('r',-1)]:
 sx=x*sign;region=smooth((sx-.08)/.05)*(1-smooth((sx-.215)/.025))*smooth((z-1.17)/.07)*(1-smooth((z-1.48)/.05));hum=smooth((sx-(.174+.17*np.maximum(1.4-z,0)))/.070)*smooth((z-1.21)/.13);clav=(1-hum)*.28*smooth((z-1.38)/.08)*smooth((sx-.06)/.12);sp=smooth((z-1.25)/.13);target=np.zeros_like(W)
 for n,w in [('upper_arm_'+side,hum),('clavicle_'+side,clav),('spine_03',(1-hum-clav)*sp),('spine_02',(1-hum-clav)*(1-sp))]:target[:,names.index(n)]=w
 W=W*(1-region[:,None])+target*region[:,None]
 # Anatomical groin crease slants down medially; posterior buttock uses a broader pelvis transition.
 front=smooth((y+.025)/.08);hipline=.915+.20*(sx-.105);lo=hipline-.095-.025*front;hi=hipline+.065-.015*front;femur=1-smooth((z-lo)/(hi-lo));femur*=.55+.45*front
 region=smooth((sx-.012)/.035)*(1-smooth((sx-.20)/.045))*smooth((z-.78)/.055)*(1-smooth((z-.985)/.04));target=np.zeros_like(W);target[:,names.index('thigh_'+side)]=femur;target[:,names.index('pelvis')]=1-femur;W=W*(1-region[:,None])+target*region[:,None]
# Mesh-neighbor diffusion removes hard ownership boundaries without bridging disconnected surfaces.
edges=np.array([e.vertices[:] for e in body.data.edges]);src=np.r_[edges[:,0],edges[:,1]];dst=np.r_[edges[:,1],edges[:,0]];counts=np.bincount(dst,minlength=len(p));region=np.maximum(np.exp(-((z-1.385)/.13)**4-((ax-.18)/.12)**4),.75*np.exp(-((z-.91)/.13)**4-((ax-.11)/.12)**4));cols=[names.index(n) for n in ['pelvis','thigh_l','thigh_r','spine_01','spine_02','spine_03','clavicle_l','clavicle_r','upper_arm_l','upper_arm_r']];sub=W[:,cols];total=sub.sum(1)
for _ in range(12):
 avg=np.stack([np.bincount(dst,weights=sub[src,i],minlength=len(p))/np.maximum(counts,1) for i in range(len(cols))],axis=1);sub+=(avg-sub)*(.5*region)[:,None];sub*= (total/np.maximum(sub.sum(1),1e-15))[:,None]
W[:,cols]=sub;W/=np.maximum(W.sum(1),1e-15)[:,None]
for i,n in enumerate(names):
 g=body.vertex_groups[n];g.remove(list(range(len(p))))
 for j in np.flatnonzero(W[:,i]>1e-8):g.add([int(j)],float(W[j,i]),'REPLACE')
# Continuous, general joint-angle-dependent relaxation; no named-pose switches or new bones.
for kind,center,width,iters,strength in [('hip',.915,.115,65,.65),('shoulder',1.405,.125,35,.32)]:
 for side,sign in [('l',1),('r',-1)]:
  cx=arm.data.bones[('thigh' if kind=='hip' else 'upper_arm')+'_'+side].head_local.x;mask=np.exp(-((z-center)/width)**4-((x-cx)/(.11 if kind=='hip' else .13))**4);g=body.vertex_groups.new(name='anatomy_'+kind+'_motion_'+side)
  for j in np.flatnonzero(mask>.001):g.add([int(j)],float(mask[j]),'REPLACE')
  mod=body.modifiers.new('anatomy_'+kind+'_motion_'+side,'SMOOTH');mod.vertex_group=g.name;mod.iterations=iters;mod.factor=0;d=mod.driver_add('factor').driver
  for axis in ['X','Z']:
   v=d.variables.new();v.name='r'+axis.lower();v.type='TRANSFORMS';t=v.targets[0];t.id=solver;t.bone_target=('thigh' if kind=='hip' else 'upper_arm')+'_'+side;t.transform_type='ROT_'+axis;t.transform_space='LOCAL_SPACE';t.rotation_mode='XYZ'
  d.expression=f'{strength}*max(0,min(1,(sqrt(rx*rx+rz*rz)-0.25)/1.25))';bpy.context.view_layer.objects.active=body
  while body.modifiers.find(mod.name)>body.modifiers.find('illustration_and_highlights'):bpy.ops.object.modifier_move_up(modifier=mod.name)
# Trace anatomically shaped rest-surface boundaries; feather along real mesh edges.
pec=[(.012,1.425),(.075,1.447),(.135,1.438),(.185,1.415),(.208,1.390),(.177,1.355),(.130,1.316),(.055,1.300),(.013,1.316)]
quad=[(.088,.883),(.127,.87),(.146,.80),(.139,.685),(.119,.552),(.105,.528),(.084,.575),(.069,.70),(.070,.819)]
def polygon_mask(u,v,poly,feather=.004):
 inside=np.zeros(len(u),dtype=bool);dist=np.ones(len(u))*1e9
 for i,(a,b) in enumerate(poly):
  c,d=poly[(i+1)%len(poly)];inside^=((b>v)!=(d>v))&(u<(c-a)*(v-b)/(d-b+1e-15)+a);du,dv=c-a,d-b;t=np.clip(((u-a)*du+(v-b)*dv)/(du*du+dv*dv),0,1);dist=np.minimum(dist,np.hypot(u-a-t*du,v-b-t*dv))
 return smooth(.5+np.where(inside,dist,-dist)/(2*feather))
fields={}
for side,sign in [('l',1),('r',-1)]:
 sx=x*sign;front=smooth((y+.005)/.045);fields['muscle_pectoralis_major_'+side]=polygon_mask(sx,z,pec)*front
 a=arm.data.bones['upper_arm_'+side].head_local;u=(arm.data.bones['upper_arm_'+side].tail_local-a).normalized();v=p-np.array(a);t=v@np.array(u);r=np.linalg.norm(v-t[:,None]*np.array(u),axis=1);cap=smooth((t+.065)/.045)*(1-smooth((t-.085)/.08))*smooth((sx-.14)/.05)*(1-smooth((r-.065)/.04))
 for part in ['anterior','middle','posterior']:
  direction=front if part=='anterior' else smooth((-y+.005)/.045) if part=='posterior' else 1-smooth((abs(y)-.008)/.035)
  fields['muscle_deltoid_'+part+'_'+side]=cap*direction
 longitudinal=smooth((t-.035)/.045)*(1-smooth((t-.235)/.075));width=.065*np.sqrt(np.maximum(0,1-((t-.17)/.19)**2));belly=longitudinal*(1-smooth((r-width+.015)/.035))
 fields['muscle_biceps_brachii_'+side]=belly*smooth((y+.005)/.04);fields['muscle_triceps_brachii_'+side]=belly*smooth((-y+.002)/.045)
 fields['muscle_rectus_femoris_'+side]=polygon_mask(sx,z,quad,.005)*smooth((y-.008)/.045)
for mid,field in fields.items():
 for _ in range(4):field=.65*field+.35*np.bincount(dst,weights=field[src],minlength=len(p))/np.maximum(counts,1)
 attr=body.data.attributes.get(mid)
 if attr:attr.data.foreach_set('value',field.astype(np.float32))
 g=body.vertex_groups[mid];g.remove(list(range(len(p))))
 for j in np.flatnonzero(field>.001):g.add([int(j)],float(field[j]),'REPLACE')
# No removed skin faces: local alpha becomes an evaluated attribute, independent per override.
ng=body.modifiers['illustration_and_highlights'].node_group;delete=next(n for n in ng.nodes if n.bl_idname=='GeometryNodeDeleteGeometry');out=next(n for n in ng.nodes if n.bl_idname=='NodeGroupOutput');store=next(n for n in ng.nodes if n.bl_idname=='GeometryNodeStoreNamedAttribute');window_node=next(n for n in ng.nodes if n.bl_idname=='GeometryNodeInputNamedAttribute' and n.inputs['Name'].default_value=='xray_window');enabled=ng.nodes.get('Value.028');mul=ng.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';ng.links.new(window_node.outputs['Attribute'],mul.inputs[0]);ng.links.new(enabled.outputs[0],mul.inputs[1]);alpha=ng.nodes.new('ShaderNodeMath');alpha.operation='MULTIPLY_ADD';alpha.inputs[1].default_value=-.84;alpha.inputs[2].default_value=1;ng.links.new(mul.outputs[0],alpha.inputs[0]);opacity=ng.nodes.new('GeometryNodeStoreNamedAttribute');opacity.data_type='FLOAT';opacity.domain='POINT';opacity.inputs['Name'].default_value='xray_alpha';ng.links.new(store.outputs['Geometry'],opacity.inputs['Geometry']);ng.links.new(alpha.outputs[0],opacity.inputs['Value']);ng.links.new(opacity.outputs['Geometry'],out.inputs['Geometry']);ng.nodes.remove(delete)
cx=arm.data.bones['thigh_l'].head_local.x;rho=np.sqrt(((x-cx)/.075)**2+((z-.735)/.175)**2);window=(1-smooth((rho-.55)/.45))*smooth((y+.005)/.035);body.data.attributes['xray_window'].data.foreach_set('value',window.astype(np.float32))
def emission_material(name,translucent=False):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;mat.diffuse_color=(.48,.51,.53,1);nodes=mat.node_tree.nodes;nodes.clear();links=mat.node_tree.links;out=nodes.new('ShaderNodeOutputMaterial');color=nodes.new('ShaderNodeAttribute');color.attribute_name='Color';em=nodes.new('ShaderNodeEmission');links.new(color.outputs['Color'],em.inputs['Color'])
 if translucent:
  attr=nodes.new('ShaderNodeAttribute');attr.attribute_name='xray_alpha';tr=nodes.new('ShaderNodeBsdfTransparent');mix=nodes.new('ShaderNodeMixShader');links.new(attr.outputs['Fac'],mix.inputs[0]);links.new(tr.outputs[0],mix.inputs[1]);links.new(em.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs['Surface']);mat.surface_render_method='DITHERED';mat.use_transparency_overlap=False;mat.use_transparent_shadow=False
 else:links.new(em.outputs[0],out.inputs['Surface'])
 return mat
body.data.materials[0]=emission_material(ID+'__material_skin_translucency_review',True);deep=mc.get(ID+'__mesh_vastus_intermedius_l');deep.data.materials.clear();deep.data.materials.append(emission_material(ID+'__material_deep_muscle_review'))
body.data.update();cp.pose('neutral_a_pose');assert hashlib.sha256(np.array([v.co[:] for v in body.data.vertices]).tobytes()).hexdigest()==rawhash
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',m);write_json(A/'refinement-record.json',{'input_sha256':before,'source_sha256':digest(SOURCE),'raw_vertex_sha256_unchanged':rawhash,'script_sha256':digest(Path(__file__)),'rest_profile_sha256':digest(A/'rest-profile.json'),'joint_method':'Spatial anatomical ownership +12neighbor diffusion steps; continuous LBS/DQ hip blend; per-joint swing-magnitude Smooth, zero in rest. Existing posterior knee field retained. No named pose switches or new deform bones.','mask_boundaries':{'pectoral_fan_xz_m':pec,'rectus_femoris_xz_m':quad,'other':'Bone-local belly/cap contours, anterior/middle/posterior partitions; mesh-neighbor feathering. Artist-authored, not clinical segmentation.'},'xray':'Continuous full topology. Smooth local skin alpha1..0.16 driven by actual root state via GN attribute; emission/transparent Eevee shader, skinned underlying schematic deep volume.','preserved':'53canonical bones, rest profile,11anchor frames, all78IDs and neutral raw geometry; approved equipment untouched','limitations':['Mask boundaries remain review annotations, not certified anatomy','Renderer experiment asset-local; Workbench does not display material alpha','Private corrections need export bake; not biomechanical simulation']})
