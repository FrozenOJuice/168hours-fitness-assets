"""Fit static core-test digit curls to measured28mm shaft; no source save or rig change."""
from pathlib import Path
import bpy,sys,json,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import R,A,ID,RID
import mannequin_review_common as mc
from barbell_20kg_common import write_json,digest
F=R/'scenes/templates/168h_template_mannequin_core_poses';suite=json.loads((F/'suite.json').read_text());scene=bpy.data.scenes[suite['poses']['bar_grip']['scene']];bpy.context.window.scene=scene;c=bpy.data.collections[suite['poses']['bar_grip']['character_collection']];mc.MAPPING={o.override_library.reference.name:o for o in c.all_objects if o.override_library};body=mc.get(ID+'__mesh_body');arm=mc.get(RID+'__armature_solver')
for mod in body.modifiers:
 if mod.type=='NODES':mod.show_viewport=False
bar=np.array([.318,1.082]);buffer=np.empty(len(body.data.vertices)*3,dtype=np.float32);results={}
if '--little-only' in sys.argv:results=json.loads((A/'grip-fit.json').read_text())['digits']
def closest(indices):
 bpy.context.view_layer.update();e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();me.vertices.foreach_get('co',buffer);points=buffer.reshape(-1,3)[indices];rad=np.linalg.norm(points[:,1:]-bar,axis=1);e.to_mesh_clear();return float(rad.min())
for digit in (['little'] if '--little-only' in sys.argv else ['index','middle','ring','little','thumb']):
 groups={body.vertex_groups[f'{digit}_{i:02}_l'].index for i in range(1,4)};indices=np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.7]);vals=np.array([1.8,1.1,.8] if digit!='thumb' else [.9,.7,.4]);initial=vals.copy();ranges=[(.8,2.0),(0,1.8),(0,1.3)] if digit!='thumb' else [(0,1.4),(0,1.3),(0,1.3)]
 def apply(v):
  for i,value in enumerate(v,1):mc.rotate(f'{digit}_{i:02}_l',(0,0,1) if digit=='thumb' and i==1 else (1,0,0),float(value))
  arm.update_tag()
 def score(v):
  apply(v);r=closest(indices);return abs(r-.0144)+max(0,.014-r)*5+.00001*float(np.sum((v-initial)**2)),r
 best,_=score(vals)
 if digit=='little':
  coarse=[]
  for aa in [.8,1.0,1.25,1.5,1.75,2.0]:
   for bb in [0,.4,.8,1.2,1.6]:
    for cc in [0,.4,.8,1.2]:
     vv=np.array([aa,bb,cc]);ss,rr=score(vv);coarse.append((ss,vv,rr))
  best,vals,_=min(coarse,key=lambda t:t[0])
 for step in [.25,.10,.04,.015]:
  for k in range(3):
   choices=[]
   for v in np.linspace(max(ranges[k][0],vals[k]-step*2),min(ranges[k][1],vals[k]+step*2),9):
    candidate=vals.copy();candidate[k]=v;s,r=score(candidate);choices.append((s,candidate.copy(),r))
   best,vals,rad=min(choices,key=lambda t:t[0])
 apply(vals);rad=closest(indices);results[digit]={'angles_radians':vals.tolist(),'closest_radial_distance_m':rad,'axis_first':'Z' if digit=='thumb' else 'X'};print('FIT_DIGIT',digit,json.dumps(results[digit]),flush=True)
write_json(A/'grip-fit.json',{'scope':'Core static underhand grip only, source mesh unchanged; local provisional fit','bar_center_yz_m':bar.tolist(),'shaft_radius_m':.014,'nominal_skin_gap_m':.0004,'digits':results,'fitter_sha256':digest(Path(__file__))})
