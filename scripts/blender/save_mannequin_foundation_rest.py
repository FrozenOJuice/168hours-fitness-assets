"""Evaluate and save neutral runtime driver state before measured-source inspection."""
from pathlib import Path
import bpy,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,SOURCE
import mannequin_review_common as mc
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;mc.neutral();bpy.context.view_layer.update()
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();e.to_mesh_clear()
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',m)
print('NEUTRAL_SAVED',bpy.data.is_dirty)
