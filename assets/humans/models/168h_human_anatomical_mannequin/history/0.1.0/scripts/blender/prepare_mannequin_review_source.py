"""Set usable native review camera and form modulation; no contract/equipment edits."""
from pathlib import Path
import sys,bpy,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import SOURCE,A,ID
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;s.render.resolution_x=1200;s.render.resolution_y=1600;s.camera.data.ortho_scale=1.8
for o in [bpy.data.objects[ID+'__mesh_body'],bpy.data.objects[ID+'__mesh_vastus_intermedius_l']]:
 ng=next(m.node_group for m in o.modifiers if m.type=='NODES');nodes=ng.nodes;links=ng.links
 shade=next(n for n in nodes if n.type=='MATH' and n.operation=='MULTIPLY_ADD');factor=nodes.new('ShaderNodeMath');factor.operation='MULTIPLY_ADD';factor.inputs[1].default_value=.35;factor.inputs[2].default_value=.65;links.new(shade.outputs[0],factor.inputs[0])
 for mix in list(nodes):
  if mix.type=='MIX_RGB' and not mix.inputs[2].is_linked and any(abs(mix.inputs[2].default_value[0]-v)<1e-5 for v in [.66,.85]):
   tone=nodes.new('ShaderNodeMixRGB');tone.blend_type='MULTIPLY';tone.inputs[0].default_value=1;tone.inputs[1].default_value=mix.inputs[2].default_value;links.new(factor.outputs[0],tone.inputs[2]);links.new(tone.outputs[0],mix.inputs[2])
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',m)
