import bpy,sys,json,numpy as np
from mathutils import Quaternion,Vector
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
from build_anatomical_mannequin import R,A,ID,RID
from barbell_20kg_common import write_json
F=R/'scenes/templates/168h_template_mannequin_core_poses';suite=json.loads((F/'suite.json').read_text());bpy.context.window.scene=bpy.data.scenes[suite['poses']['bar_grip']['scene']];c=bpy.data.collections[suite['poses']['bar_grip']['character_collection']];mc.MAPPING={o.override_library.reference.name:o for o in c.all_objects if o.override_library};o=mc.get(ID+'__mesh_body');a=mc.get(RID+'__armature_solver')
for m in o.modifiers:
 if m.type=='NODES':m.show_viewport=False
ids={o.vertex_groups[f'thumb_{i:02}_l'].index for i in range(1,4)};indices=np.array([v.index for v in o.data.vertices if sum(g.weight for g in v.groups if g.group in ids)>.7]);buffer=np.empty(len(o.data.vertices)*3,dtype=np.float32)
def apply(v):
 b=a.pose.bones['thumb_01_l'];b.rotation_quaternion=Quaternion((0,0,1),float(v[0]))@Quaternion((1,0,0),float(v[1]));mc.rotate('thumb_02_l',(1,0,0),float(v[2]));mc.rotate('thumb_03_l',(1,0,0),float(v[3]));a.update_tag();bpy.context.view_layer.update()
def score(v):
 apply(v);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();me.vertices.foreach_get('co',buffer);p=buffer.reshape(-1,3)[indices];r=float(np.linalg.norm(p[:,1:]-np.array([.318,1.082]),axis=1).min());e.to_mesh_clear();return abs(r-.0144)+5*max(0,.014-r),r
choices=[]
for z in [0,.4,.8,1.2]:
 for x in [-.8,-.4,0,.4,.8,1.2]:
  v=np.array([z,x,.4,.4]);s,r=score(v);choices.append((s,v,r))
best,vals,rad=min(choices,key=lambda t:t[0]);ranges=[(0,1.4),(-1,1.5),(0,1.3),(0,1.3)]
for step in [.25,.1,.04,.015]:
 for k in range(4):
  choices=[]
  for t in np.linspace(max(ranges[k][0],vals[k]-step*2),min(ranges[k][1],vals[k]+step*2),9):
   v=vals.copy();v[k]=t;s,r=score(v);choices.append((s,v,r))
  best,vals,rad=min(choices,key=lambda t:t[0])
p=A/'grip-fit.json';d=json.loads(p.read_text());d['digits']['thumb']={'angles_radians':vals.tolist(),'closest_radial_distance_m':rad,'axis_first':'Z_then_X_CMC_opposition'};write_json(p,d);print('THUMB_FIT',vals.tolist(),rad,flush=True)
