"""Measured palm-clearance adjustment for the0.2 static28mm grip test."""
from pathlib import Path
import bpy,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,SOURCE
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));m=json.loads((A/'asset.json').read_text());assert m['status']=='review';hc=json.loads((A/'human-contract.json').read_text());before=digest(SOURCE)
for side in ['l','r']:
 o=bpy.data.objects[ID+'__anchor_hand_grip_'+side];mat=o.matrix_world.copy();assert abs(mat.translation.y-.028)<1e-5;mat.translation.y=.032;o.matrix_world=mat;bpy.context.view_layer.update();hc['anchors']['hand_grip_'+side]['position_m']=list(o.matrix_world.translation)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);m['anchors']=hc['anchors'];m['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',m);write_json(A/'human-contract.json',hc);write_json(A/'grip-datum-refinement.json',{'before_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'datum':'68mm distal,32mm palm-normal; actual measured palm/shaft clearance drives this local parameter','reason':'Extended grip test caught2.625mm palm penetration;4mm normal correction and per-digit refit; diagnostic tolerance unchanged'})
