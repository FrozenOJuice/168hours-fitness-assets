"""Publish the graphical rest data as a complete metric native rig-library file."""
from pathlib import Path
import bpy,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import RA,RID
from barbell_20kg_common import setup
p=RA/(RID+'__foundation_v02.blend');bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;setup(s)
for c in list(bpy.data.collections):
 if c.name not in s.collection.children:s.collection.children.link(c)
bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True,relative_remap=False)
