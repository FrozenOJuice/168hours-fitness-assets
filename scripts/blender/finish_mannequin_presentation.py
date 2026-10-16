"""Final presentation pass for first review, without altering canonical interfaces."""
from pathlib import Path
import bpy,sys,json,numpy as np,math
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import SOURCE,A,ID,RID
from barbell_20kg_common import digest,write_json
assert json.loads((A/'asset.json').read_text())['version']=='0.1.0', 'Legacy0.1 prototype script; use the current foundation/core tools';bpy.ops.wm.open_mainfile(filepath=str(SOURCE));assert not (A/'presentation-finish.json').exists()
body=bpy.data.objects[ID+'__mesh_body'];solver=bpy.data.objects[RID+'__armature_solver'];xyz=np.array([v.co[:] for v in body.data.vertices]);x,y,z=xyz.T
for side,sign in [('l',1),('r',-1)]:
 sx=x*sign;top=1.395-.13*sx;bottom=1.25+.30*sx
 def smooth(v):v=np.clip(v,0,1);return v*v*(3-2*v)
 values=smooth((sx-.012)/.018)*smooth((.185-sx)/.035)*smooth((top-z)/.018)*smooth((z-bottom)/.018)*smooth((y-.025)/.025);mid='muscle_pectoralis_major_'+side;body.data.attributes[mid].data.foreach_set('value',values.astype(np.float32));vg=body.vertex_groups[mid];vg.remove(list(range(len(xyz))))
 for i in np.flatnonzero(values>1e-4):vg.add([int(i)],float(values[i]),'REPLACE')
 next(c for c in solver.pose.bones['forearm_'+side].constraints if c.type=='IK').pole_angle=-math.pi/2
body.modifiers['xray_boundary_fairing'].iterations=50
deep=bpy.data.objects[ID+'__mesh_vastus_intermedius_l'];sub=deep.modifiers.new('deep_anatomical_continuity','SUBSURF');sub.levels=2;sub.render_levels=2
while deep.modifiers.find(sub.name)>1:
 bpy.context.view_layer.objects.active=deep;bpy.ops.object.modifier_move_up(modifier=sub.name)
bpy.context.scene.camera.data.ortho_scale=2.05
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['published_datablocks']=[ID];write_json(A/'asset.json',m);write_json(A/'presentation-finish.json',{'source_sha256':digest(SOURCE),'changes':'broader pectoral masks, smooth deep-muscle subdivision and aperture, symmetric flared arm IK pole angles, whole-character native camera','script_sha256':digest(Path(__file__))})
