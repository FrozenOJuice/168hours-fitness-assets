"""One-shot refinement of existing 0.2.0 topology, not a body rebuild.
Input preserved in history/0.2.0; canonical rest/anchors and protected assets unchanged.
"""
from pathlib import Path
import bpy,sys,json,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,RID,SOURCE
from barbell_20kg_common import digest,write_json
import mannequin_core_poses as cp
import mannequin_review_common as mc
assert not (A/'surface-refinement.json').exists(),'Already applied; use archived predecessor for intentional revision'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));cp.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');before=digest(SOURCE)
p=np.array([v.co[:] for v in body.data.vertices]);q=p.copy();x,y,z=p.T;a=abs(x)
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
def gauss(x,c,w):return np.exp(-((x-c)/w)**2)
# Refit anterior torso continuously, including lower ribcage and waist; no hard Z cap.
front=smooth((y-.005)/.05);lateral=np.exp(-(a/.17)**6);axial=smooth((z-.91)/.09)*(1-smooth((z-1.405)/.065));influence=front*lateral*axial
# Smooth sagittal body envelope: lower abdomen -> waist -> ribs -> pectorals.
profile=.105+.010*gauss(z,1.02,.09)-.013*gauss(z,1.15,.10)+.008*gauss(z,1.33,.075)
profile-=.018*(a/.17)**2
# Broad pectoral bellies plus shallow sternum and inferior separation, not breast forms.
profile+=.010*gauss(a,.078,.050)*gauss(z,1.345,.049)
profile-=.0028*gauss(x,0,.013)*gauss(z,1.29,.14)
profile-=.0020*gauss(z,1.285,.012)*gauss(a,.075,.065)
# Quiet rectus columns / tendinous intersections; actual relief, no texture masks.
profile+=.0035*gauss(a,.036,.025)*gauss(z,1.14,.12)
for zz in [1.075,1.13,1.185,1.24]:profile-=.0015*gauss(z,zz,.008)*gauss(a,.036,.032)
q[:,1]+=(profile-y)*influence
# Reduce hip/flank and glute emphasis gently without moving skeleton or floor.
q[:,0]*=1-.045*gauss(z,.92,.10)*smooth((a-.075)/.06)*(1-smooth((a-.20)/.035))
q[:,1]*=1-.075*gauss(z,.91,.11)*smooth((-y-.035)/.06)
# Muscle relief along existing limb axes, away from joints/hands/feet.
for side,sign in [('l',1),('r',-1)]:
 shoulder=np.array(arm.data.bones['upper_arm_'+side].head_local);elbow=np.array(arm.data.bones['forearm_'+side].head_local)
 axis=(elbow-shoulder);length=np.linalg.norm(axis);u=axis/length;v=p-shoulder;t=v@u;rad=v-t[:,None]*u
 bell=gauss(t,length*.47,length*.24)*(x*sign>0)*(1-smooth((np.linalg.norm(rad,axis=1)-.075)/.030))
 # Existing continuous deltoid and biceps/triceps volumes receive restrained relief.
 q[:,1]+=.006*bell*smooth((y-.012)/.045)-.004*bell*smooth((-y-.01)/.045)
 delt=gauss(t,.015,.055)*gauss(np.linalg.norm(rad,axis=1),.058,.030)*(x*sign>.10)
 q+=rad/np.maximum(np.linalg.norm(rad,axis=1),1e-8)[:,None]*(.0035*delt)[:,None]
 hip=arm.data.bones['thigh_'+side].head_local;knee=arm.data.bones['shin_'+side].head_local;ankle=arm.data.bones['foot_'+side].head_local
 leg=gauss(x,hip.x,.055)*(z>knee.z+.055)*(z<hip.z-.055)
 q[:,1]+=.006*leg*gauss(z,.70,.115)*smooth((y-.025)/.055)
 # Shallow groove separating rectus/vastus, fading out well before the knee.
 q[:,1]-=.0018*gauss(x,hip.x+sign*.027,.010)*gauss(z,.69,.10)*smooth((y-.02)/.055)
 calf=gauss(x,ankle.x,.050)*gauss(z,.29,.09)*smooth((-y-.02)/.045)
 q[:,1]-=.0045*calf
body.data.vertices.foreach_set('co',q.astype(np.float32).ravel());body.data.update()
# Replace overextended clavicle/shoulder source weights ONLY in upper torso.
# Keep hands/fingers, lower torso and all knees untouched. Smooth anatomical ownership.
changed=0
for vert,point in zip(body.data.vertices,p):
 xx,yy,zz=point;aa=abs(xx)
 if not (1.245<zz<1.49 and aa<.275):continue
 side='l' if xx>=0 else 'r';sign=1 if xx>=0 else -1
 names=['spine_01','spine_02','spine_03','clavicle_'+side,'upper_arm_'+side]
 old={g.group:g.weight for g in vert.groups};indices=[body.vertex_groups[n].index for n in names];total=sum(old.get(i,0) for i in indices)
 if total<1e-6:continue
 blend=float(smooth((zz-1.245)/.045)*(1-smooth((zz-1.455)/.035))*(1-smooth((aa-.245)/.030)))
 # Torso skin below axilla follows ribs, lateral shoulder cap follows humerus.
 boundary=.158+.035*float(smooth((1.405-zz)/.105))
 hum=float(smooth((aa-boundary)/.055));clav=(1-hum)*float(smooth((zz-1.365)/.065))*float(smooth((aa-.06)/.10))*.45
 target=[0,0,1-hum-clav,clav,hum]
 for name,i,tgt in zip(names,indices,target):body.vertex_groups[name].add([vert.index],old.get(i,0)*(1-blend)+total*tgt*blend,'REPLACE')
 changed+=1
# Smooth changed weights over actual shared edges: prevents source-group eligibility seams.
names=['spine_01','spine_02','spine_03','clavicle_l','upper_arm_l','clavicle_r','upper_arm_r']
indices=[body.vertex_groups[n].index for n in names];lookup={i:k for k,i in enumerate(indices)}
w=np.zeros((len(p),len(names)))
for v in body.data.vertices:
 for g in v.groups:
  if g.group in lookup:w[v.index,lookup[g.group]]=g.weight
edges=np.array([e.vertices[:] for e in body.data.edges]);src=np.r_[edges[:,0],edges[:,1]];dst=np.r_[edges[:,1],edges[:,0]];count=np.bincount(dst,minlength=len(p));tot=w.sum(axis=1)
region=smooth((z-1.245)/.045)*(1-smooth((z-1.455)/.035))*(1-smooth((a-.245)/.030))
for iteration in range(32):
 avg=np.stack([np.bincount(dst,weights=w[src,k],minlength=len(p))/count for k in range(len(names))],axis=1)
 w+=(avg-w)*(.7*region)[:,None]
 w*= (tot/np.maximum(w.sum(axis=1),1e-20))[:,None]
for v in body.data.vertices:
 if region[v.index]<=0:continue
 for k,n in enumerate(names):body.vertex_groups[n].add([v.index],float(w[v.index,k]),'REPLACE')
# Local illustrated gray contrast; no lighting, cavity, shadow or AO.
ng=body.modifiers['illustration_and_highlights'].node_group
for n in ng.nodes:
 if n.bl_idname=='ShaderNodeMath' and n.operation=='MULTIPLY_ADD':n.inputs[1].default_value=.70;n.inputs[2].default_value=.43
 if n.bl_idname=='ShaderNodeMixRGB' and not n.inputs[1].is_linked:
  n.inputs[1].default_value=(.12,.145,.16,1);n.inputs[2].default_value=(.62,.65,.67,1)
cp.pose('neutral_a_pose');neutral=cp.coords();cp.pose('arms_raised');dq=cp.coords()
skin=body.modifiers['canonical_skinning'];skin.use_deform_preserve_volume=False;mc.update();linear=cp.coords();skin.use_deform_preserve_volume=True;mc.update()
# Add localized post-skin DQ volume correction based on measured DQ-vs-LBS difference.
# Zero at rest; shoulder only, retains DQ elbows/knees/hands; no new deform bones.
mask=gauss(z,1.365,.105)*smooth((a-.08)/.08)*(1-smooth((a-.29)/.06))
delta=(linear-dq)*mask[:,None]
# Axillary skin needs to rise with the humerus, not remain a hanging lateral flap.
# Smooth symmetric soft-tissue lift; recorded local prototype, zero in neutral.
axilla=gauss(z,1.345,.080)*gauss(a,.185,.075)*smooth((a-.085)/.055)
delta[:,0]-=np.sign(x)*.025*axilla
delta[:,2]+=.070*axilla
ng=bpy.data.node_groups.new(ID+'__shoulder_volume_corrective','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nodes=ng.nodes;links=ng.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');mod=body.modifiers.new('foundation_shoulder_volume_corrective','NODES');mod.node_group=ng;total=None;fair=None
for side,sign in [('l',1),('r',-1)]:
 attr=body.data.attributes.new('foundation_shoulder_delta_'+side,'FLOAT_VECTOR','POINT');d=delta*(x*sign>0)[:,None];attr.data.foreach_set('vector',d.astype(np.float32).ravel());named=nodes.new('GeometryNodeInputNamedAttribute');named.data_type='FLOAT_VECTOR';named.inputs['Name'].default_value=attr.name
 socket=ng.interface.new_socket(name='Arm elevation '+side,in_out='INPUT',socket_type='NodeSocketFloat');mod[socket.identifier]=0.;driver=mod.driver_add('["'+socket.identifier+'"]').driver;var=driver.variables.new();var.name='raise_arm';var.type='TRANSFORMS';t=var.targets[0];t.id=solver;t.bone_target='upper_arm_'+side;t.transform_type='ROT_Z';t.transform_space='LOCAL_SPACE';t.rotation_mode='XYZ';driver.expression=f'max(0,min(1,({-sign}*raise_arm-0.5235987756)/1.3962634016))'
 scale=nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';links.new(named.outputs['Attribute'],scale.inputs[0]);links.new(inp.outputs[socket.identifier],scale.inputs['Scale'])
 fairattr=body.data.attributes.new('foundation_shoulder_fair_'+side,'FLOAT','POINT');fairattr.data.foreach_set('value',(gauss(z,1.37,.10)*gauss(a,.19,.10)*(x*sign>0)).astype(np.float32));fm=nodes.new('GeometryNodeInputNamedAttribute');fm.data_type='FLOAT';fm.inputs['Name'].default_value=fairattr.name;mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(fm.outputs['Attribute'],mul.inputs[0]);links.new(inp.outputs[socket.identifier],mul.inputs[1])
 if fair:
  addf=nodes.new('ShaderNodeMath');addf.operation='ADD';links.new(fair,addf.inputs[0]);links.new(mul.outputs[0],addf.inputs[1]);fair=addf.outputs[0]
 else:fair=mul.outputs[0]
 if total:
  add=nodes.new('ShaderNodeVectorMath');add.operation='ADD';links.new(total,add.inputs[0]);links.new(scale.outputs['Vector'],add.inputs[1]);total=add.outputs['Vector']
 else:total=scale.outputs['Vector']
setpos=nodes.new('GeometryNodeSetPosition');links.new(inp.outputs['Geometry'],setpos.inputs['Geometry']);links.new(total,setpos.inputs['Offset']);position=nodes.new('GeometryNodeInputPosition');blur=nodes.new('GeometryNodeBlurAttribute');blur.data_type='FLOAT_VECTOR';blur.inputs['Iterations'].default_value=160;links.new(position.outputs['Position'],blur.inputs['Value']);diff=nodes.new('ShaderNodeVectorMath');diff.operation='SUBTRACT';links.new(blur.outputs['Value'],diff.inputs[0]);links.new(position.outputs['Position'],diff.inputs[1]);fscale=nodes.new('ShaderNodeVectorMath');fscale.operation='SCALE';links.new(diff.outputs[0],fscale.inputs[0]);links.new(fair,fscale.inputs['Scale']);finish=nodes.new('GeometryNodeSetPosition');links.new(setpos.outputs['Geometry'],finish.inputs['Geometry']);links.new(fscale.outputs[0],finish.inputs['Offset']);links.new(finish.outputs['Geometry'],out.inputs['Geometry']);bpy.context.view_layer.objects.active=body
while body.modifiers.find(mod.name)>body.modifiers.find('canonical_skinning')+1:bpy.ops.object.modifier_move_up(modifier=mod.name)
cp.pose('neutral_a_pose');bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
write_json(A/'surface-refinement.json',{'version':'0.2.1','status':'review','before_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'vertices':len(p),'faces':len(body.data.polygons),'max_vertex_edit_m':float(np.linalg.norm(q-p,axis=1).max()),'shoulder_vertices_reweighted':changed,'shoulder_delta_max_m':float(np.linalg.norm(delta,axis=1).max()),'chest_cause':'Raw-neutral vs evaluated maximum delta 0.000133mm: original hard-bound chest fairing leaves upper-abdominal ledge; underlying geometry refit continuously','corrective':'Asset-local postskin shoulder DQ-to-linear offset at overhead, driven independently per arm after30deg local elevation, fully at110deg; not a universal swing/twist corrective','rest_profile':'unchanged','canonical_interfaces':'unchanged'})
m=json.loads((A/'asset.json').read_text());m['version']='0.2.1';m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['dimensions_m']=[float(v) for v in np.ptp(neutral,axis=0)];write_json(A/'asset.json',m)
