"""Pose-dependent posterior knee compression and measured static grip-center correction."""
from pathlib import Path
import bpy,sys,json,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import R,A,ID,RID,SOURCE
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));assert not (A/'foundation-joint-correction.json').exists();before=digest(SOURCE);body=bpy.data.objects[ID+'__mesh_body'];solver=bpy.data.objects[RID+'__armature_solver'];arm=bpy.data.objects[ID+'__armature_deform'];xyz=np.array([v.co[:] for v in body.data.vertices]);x,y,z=xyz.T
ng=bpy.data.node_groups.new(ID+'__knee_corrective_fields','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nodes=ng.nodes;links=ng.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');acc=None;mod=body.modifiers.new('foundation_posterior_knee_corrective','NODES');mod.node_group=ng
for side,sign in [('l',1),('r',-1)]:
 knee=arm.data.bones['shin_'+side].head_local;kneeweight=np.exp(-((z-knee.z)/.105)**4-((x-knee.x)/.09)**4)*np.clip((-y-.020)/.025,0,1)*.018;attr=body.data.attributes.new('foundation_knee_compression_'+side,'FLOAT','POINT');attr.data.foreach_set('value',kneeweight.astype(np.float32))
 mask=nodes.new('GeometryNodeInputNamedAttribute');mask.data_type='FLOAT';mask.inputs['Name'].default_value=attr.name;socket=ng.interface.new_socket(name='Knee flexion '+side,in_out='INPUT',socket_type='NodeSocketFloat');socket.default_value=0;socket.min_value=0;socket.max_value=1.25;mod[socket.identifier]=0.;driver=mod.driver_add('["'+socket.identifier+'"]').driver;var=driver.variables.new();var.name='bend';var.type='TRANSFORMS';t=var.targets[0];t.id=solver;t.bone_target='shin_'+side;t.transform_type='ROT_X';t.transform_space='LOCAL_SPACE';t.rotation_mode='XYZ';driver.expression='max(0,min(1.25,-bend/1.5707963267948966))';mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(mask.outputs['Attribute'],mul.inputs[0]);links.new(inp.outputs[socket.identifier],mul.inputs[1])
 if acc:
  add=nodes.new('ShaderNodeMath');add.operation='ADD';links.new(acc,add.inputs[0]);links.new(mul.outputs[0],add.inputs[1]);acc=add.outputs[0]
 else:acc=mul.outputs[0]
combine=nodes.new('ShaderNodeCombineXYZ');links.new(acc,combine.inputs['Y']);pos=nodes.new('GeometryNodeSetPosition');links.new(inp.outputs['Geometry'],pos.inputs['Geometry']);links.new(combine.outputs[0],pos.inputs['Offset']);links.new(pos.outputs['Geometry'],out.inputs['Geometry']);bpy.context.view_layer.objects.active=body
while body.modifiers.find(mod.name)>0:bpy.ops.object.modifier_move_up(modifier=mod.name)
hc=json.loads((A/'human-contract.json').read_text())
for side in ['l','r']:
 obj=bpy.data.objects[ID+'__anchor_hand_grip_'+side];mat=obj.matrix_world.copy();u=(arm.data.bones['hand_'+side].tail_local-arm.data.bones['hand_'+side].head_local).normalized();mat.translation+=u*.016;obj.matrix_world=mat;bpy.context.view_layer.update();hc['anchors']['hand_grip_'+side]['position_m']=list(obj.matrix_world.translation)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'human-contract.json',hc);m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['anchors']=hc['anchors'];write_json(A/'asset.json',m);write_json(A/'foundation-joint-correction.json',{'before_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'knees':'Preskin18mm maximum posterior soft-tissue compression, smooth105mm axial/90mm transverse field, driven by actual private shin localX flexion; zero atrest; no extra bones','grip':'Measured center shifted16mm distally:68mm alonghand,28mm palm-normal; frame semantics and all11anchor names unchanged'})
