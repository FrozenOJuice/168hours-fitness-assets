"""Make private contact controls persist in linked overrides; no contract/frame changes."""
import bpy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));root=bpy.data.objects[ID+'__root'];before=digest(SOURCE)
for name in ['grip_contact_enabled','grip_radius_m']:root.property_overridable_library_set('["'+name+'"]',True)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'override-contact-fix.json',{'input_sha256':before,'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'correction':'Explicitly mark private contact enable/radius properties library-overridable. Saved-state validation revealed enabled contact reverted to source default0 after reload; direct-source tests alone missed it. No shared interface, bone, anchor or equipment changes.'})
