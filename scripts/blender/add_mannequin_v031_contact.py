"""General cylinder contact correction on hand skin, with editable private frames/radius."""
import bpy,sys,numpy as np,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import write_json,digest
import mannequin_review_common as mc
import mannequin_core_poses as core
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;core.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');root=mc.get(ID+'__root');root['grip_contact_enabled']=0.;root['grip_radius_m']=.014;before=digest(SOURCE);ng=bpy.data.node_groups.new(ID+'__cylinder_hand_contact','GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nodes=ng.nodes;links=ng.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');pos=nodes.new('GeometryNodeInputPosition');geo=inp.outputs['Geometry']
def mathnode(op,*args):
 n=nodes.new('ShaderNodeMath');n.operation=op
 for i,v in enumerate(args):
  if isinstance(v,(int,float)):n.inputs[i].default_value=v
  else:links.new(v,n.inputs[i])
 return n.outputs[0]
def vectornode(op,*args):
 n=nodes.new('ShaderNodeVectorMath');n.operation=op
 for i,v in enumerate(args):
  if isinstance(v,(tuple,list)):n.inputs[i].default_value=v
  else:links.new(v,n.inputs[i])
 return n.outputs['Value'] if op in ['DOT_PRODUCT','LENGTH'] else n.outputs['Vector']
def driver_value(prop):
 n=nodes.new('ShaderNodeValue');d=n.outputs[0].driver_add('default_value').driver;v=d.variables.new();v.name='a';v.targets[0].id=root;v.targets[0].data_path='["'+prop+'"]';d.expression='a';return n.outputs[0]
enabled=driver_value('grip_contact_enabled');radius=driver_value('grip_radius_m')
for side in ['l','r']:
 frame=bpy.data.objects.new(ID+'__control_grip_cylinder_'+side,None);body.users_collection[0].objects.link(frame);frame.parent=root;frame.location=(0,.318,1.08);frame.empty_display_type='ARROWS';frame.empty_display_size=.04;frame.hide_render=True;frame.hide_set(True)
 info=nodes.new('GeometryNodeObjectInfo');info.transform_space='RELATIVE';info.inputs['Object'].default_value=frame;rot=nodes.new('FunctionNodeRotateVector');rot.inputs['Vector'].default_value=(1,0,0);links.new(info.outputs['Rotation'],rot.inputs['Rotation']);axis=rot.outputs['Vector'];delta=vectornode('SUBTRACT',pos.outputs['Position'],info.outputs['Location']);dot=vectornode('DOT_PRODUCT',delta,axis);along=nodes.new('ShaderNodeVectorMath');along.operation='SCALE';links.new(axis,along.inputs[0]);links.new(dot,along.inputs['Scale']);radial=vectornode('SUBTRACT',delta,along.outputs['Vector']);length=vectornode('LENGTH',radial);normal=vectornode('NORMALIZE',radial);depth=mathnode('MAXIMUM',0,mathnode('SUBTRACT',mathnode('ADD',radius,.00035),length));groups={g.index for g in body.vertex_groups if g.name.endswith('_'+side) and g.name.startswith(('hand_','thumb_','index_','middle_','ring_','little_'))};w=np.array([sum(g.weight for g in v.groups if g.group in groups) for v in body.data.vertices]);w=np.clip((w-.75)/.2,0,1);name='anatomy_hand_contact_'+side;attr=body.data.attributes.new(name,'FLOAT','POINT');attr.data.foreach_set('value',w.astype(np.float32));named=nodes.new('GeometryNodeInputNamedAttribute');named.data_type='FLOAT';named.inputs['Name'].default_value=name;scale=mathnode('MULTIPLY',depth,mathnode('MULTIPLY',enabled,named.outputs['Attribute']));off=nodes.new('ShaderNodeVectorMath');off.operation='SCALE';links.new(normal,off.inputs[0]);links.new(scale,off.inputs['Scale']);setpos=nodes.new('GeometryNodeSetPosition');links.new(geo,setpos.inputs['Geometry']);links.new(off.outputs['Vector'],setpos.inputs['Offset']);geo=setpos.outputs['Geometry']
links.new(geo,out.inputs['Geometry']);mod=body.modifiers.new('anatomy_hand_cylinder_contact','NODES');mod.node_group=ng;bpy.context.view_layer.objects.active=body
while body.modifiers.find(mod.name)>body.modifiers.find('illustration_and_highlights'):bpy.ops.object.modifier_move_up(modifier=mod.name)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'contact-refinement.json',{'input_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'method':'Post-skin radial projection only for hand skin inside radius+0.35mm. Editable per-hand private cylinder frames orient shaft axis; radius control. No geometry deletion or equipment edits. No pose names in correction.','neutral':'Disabled; raw skin/rest profile/anchors unchanged','limits':'Soft-tissue contact adapter only; does not certify arbitrary equipment, gripping force or finger/finger collision. Record measured maximum correction, reject excessive displacement rather than hide bad anatomy.'})
