"""Isolated pose-dependent posterior soft-tissue compression; zero in neutral."""
import bpy,sys,numpy as np,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as cp
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;cp.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');before=digest(SOURCE);p=np.array([v.co[:] for v in body.data.vertices]);rawhash=hashlib.sha256(p.tobytes()).hexdigest();x,y,z=p.T
for side in ['l','r']:
 k=arm.data.bones['shin_'+side].head_local;w=.035*np.exp(-((z-k.z)/.23)**4-((x-k.x)/.09)**4)*np.clip((-y-.015)/.035,0,1);body.data.attributes['anatomy_posterior_compression_'+side].data.foreach_set('value',w.astype(np.float32))
body.data.update();mc.update();assert hashlib.sha256(np.array([v.co[:] for v in body.data.vertices]).tobytes()).hexdigest()==rawhash
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
write_json(A/'knee-contact-refinement.json',{'before_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'raw_vertex_sha256_before_and_after':rawhash,'neutral_offset_m':0,'compression':'Posterior-only +Y pre-skin offset; per-shin local flexion driver unchanged, 35mm@90deg capped1.5x; quartic knee-centered falloff230mmZ/90mmX, back-face factor clamp((-Y-15mm)/35mm)','investigation':'22mm/105mm field missed bulk hamstring/calf overlap outside the joint. Scaling amplitude alone did not cure squat. Trials25mm/180mm and35mm/180mm retained crossings;35mm/230mm removed both sides in130deg squat. No collision criterion relaxed. Final saved-state tests and renders determine acceptance.','limitations':'Artist-authored soft-tissue compression, not biomechanical simulation. Deep-flexion folds still require visual review.'})
