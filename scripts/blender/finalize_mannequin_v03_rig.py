"""Make the isolated rest-data library openable; preserve exact canonical bone data."""
import bpy,sys,json,hashlib,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import setup,write_json,digest
bpy.ops.wm.read_factory_settings(use_empty=True)
tmp=RA/'__rig_repack_input.blend';shutil.copy2(RSOURCE,tmp)
with bpy.data.libraries.load(str(tmp),link=False) as (f,t):t.collections=[RID]
c=t.collections[0];s=bpy.context.scene;s.collection.children.link(c);setup(s);arm=next(o for o in c.all_objects if o.type=='ARMATURE')
def fingerprint():
 return digest(A/'rest-profile.json'),[(b.name,list(b.head_local),list(b.tail_local),[list(row) for row in b.matrix_local]) for b in arm.data.bones]
before=fingerprint();s.name=RID+'__anatomy_rest_library';bpy.context.view_layer.objects.active=arm;arm.select_set(True);arm.show_in_front=True;bpy.ops.wm.save_as_mainfile(filepath=str(RSOURCE),compress=True,relative_remap=False);assert fingerprint()==before;tmp.unlink()
write_json(RA/'asset.json',{'id':RID,'version':'0.3.0','status':'review','source':str(RSOURCE.relative_to(R)),'source_revision_or_digest':'sha256:'+digest(RSOURCE),'rest_profile_sha256':digest(A/'rest-profile.json'),'contract':'168h_human_model@1.0.0','implementation':'Canonical53bone rest-data library; character owns private solver/FK/IK/helper/corrective composition','artwork_license':None});(RA/'SPEC.md').write_text('# Isolated mannequin anatomy rig-data library0.3.0\n\n53canonical bones, V1names/parents/roll/A-pose preserved. New measured profile for the CC0 anatomical study; not direct-pose compatible with0.2.0. The character source owns animator controls and corrective deformation. No supplier rig or extra output/weighted bones. Metric native scene/root collection are openable. Review only; original rig libraries unchanged.\n')
m=json.loads((A/'asset.json').read_text());m['dependencies'][0]['sha256']=digest(RSOURCE);write_json(A/'asset.json',m)
