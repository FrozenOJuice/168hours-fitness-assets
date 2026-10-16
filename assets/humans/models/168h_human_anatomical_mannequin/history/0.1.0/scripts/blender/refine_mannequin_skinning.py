"""Review deformation fairing, no skeleton or equipment changes."""
from pathlib import Path
import bpy,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,SOURCE
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));assert not (A/'skinning-finish.json').exists()
body=bpy.data.objects[ID+'__mesh_body'];before=digest(SOURCE)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
# Smooth only canonical bone weights, never muscle masks or body geometry.
bpy.ops.object.mode_set(mode='WEIGHT_PAINT');bpy.ops.object.vertex_group_smooth(group_select_mode='BONE_DEFORM',factor=.85,repeat=25);bpy.ops.object.vertex_group_normalize_all(group_select_mode='BONE_DEFORM',lock_active=False);bpy.ops.object.mode_set(mode='OBJECT')
for m in body.modifiers:
 if m.type=='ARMATURE':m.use_deform_preserve_volume=False
# Fair the remaining construction ledge at the upper hip.
g=body.vertex_groups.new(name='hip_continuity')
for v in body.data.vertices:
 x,y,z=v.co
 if abs(x)<.25 and .88<z<1.065:g.add([v.index],1,'REPLACE')
sm=body.modifiers.new('hip_finish','SMOOTH');sm.vertex_group=g.name;sm.factor=.8;sm.iterations=60
while body.modifiers.find(sm.name)>0:bpy.ops.object.modifier_move_up(modifier=sm.name)
bpy.ops.object.modifier_apply(modifier=sm.name)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',m);write_json(A/'skinning-finish.json',{'before_sha256':before,'after_sha256':digest(SOURCE),'changes':'25 canonical-only weight smoothing iterations and normalization; linear blend to reduce IK twisting inflation; local hip silhouette fairing60 iterations; muscle masks/rig unchanged','script_sha256':digest(Path(__file__))})
