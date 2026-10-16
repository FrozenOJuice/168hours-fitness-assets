"""Local knee skin relaxation and measured V1 profile sidecars; no master writes."""
import bpy,sys,json,math,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as cp
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;cp.pose('neutral_a_pose');o=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');p=np.array([v.co[:] for v in o.data.vertices]);before=digest(SOURCE)
for side in ['l','r']:
 group=o.vertex_groups.new(name='anatomy_knee_relaxation_'+side);k=arm.data.bones['shin_'+side].head_local;w=np.exp(-((p[:,2]-k.z)/.105)**4-((p[:,0]-k.x)/.09)**4)
 for i in np.flatnonzero(w>.001):group.add([int(i)],float(w[i]),'REPLACE')
 mod=o.modifiers.new('anatomy_knee_relaxation_'+side,'SMOOTH');mod.vertex_group=group.name;mod.iterations=55;mod.factor=0;d=mod.driver_add('factor').driver;v=d.variables.new();v.name='bend';v.type='TRANSFORMS';t=v.targets[0];t.id=solver;t.bone_target='shin_'+side;t.transform_type='ROT_X';t.transform_space='LOCAL_SPACE';t.rotation_mode='XYZ';d.expression='0.8*max(0,min(1.4,-bend/1.5707963267948966))';bpy.context.view_layer.objects.active=o
 while o.modifiers.find(mod.name)>o.modifiers.find('illustration_and_highlights'):bpy.ops.object.modifier_move_up(modifier=mod.name)
# Re-measure back support against the final neutral skin.
from mathutils.bvhtree import BVHTree
tree=BVHTree.FromPolygons([v.co for v in o.data.vertices],[f.vertices[:] for f in o.data.polygons]);anchor=bpy.data.objects[ID+'__anchor_back_support'];matrix=anchor.matrix_world.copy();hit=tree.ray_cast(Vector((0,-.5,matrix.translation.z)),Vector((0,1,0)),1)[0];matrix.translation.y=hit.y;anchor.matrix_world=matrix;bpy.context.view_layer.update()
profile=[]
for b in sorted(arm.data.bones,key=lambda b:b.name):profile.append({'name':b.name,'parent':b.parent.name if b.parent else None,'deform':b.use_deform,'connected':b.use_connect,'head_m':list(b.head_local),'tail_m':list(b.tail_local),'z_axis':list(b.matrix_local.to_3x3().col[2].normalized())})
(A/'rest-profile.json').write_text(json.dumps(profile,sort_keys=True,separators=(',',':'),allow_nan=False));hc=json.loads((A/'human-contract.json').read_text());hc['rest_profile']['sha256']=digest(A/'rest-profile.json')
for key,d in hc['anchors'].items():
 obj=bpy.data.objects[d['object']];d['position_m']=list(obj.matrix_world.translation);d['rotation_quaternion_wxyz']=list(obj.matrix_world.to_quaternion())
write_json(A/'human-contract.json',hc);bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m.update(source_revision_or_digest='sha256:'+digest(SOURCE),dimensions_m=np.ptp(p,axis=0).tolist(),anchors=hc['anchors']);write_json(A/'asset.json',m);write_json(A/'source-finish.json',{'before_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'knee_relaxation':'55iterations Smooth, posterior knee correction already in stack; factor0neutral,0.8at90deg, capped1.12; actual geometry, not shading','rest_profile_sha256':hc['rest_profile']['sha256']})
