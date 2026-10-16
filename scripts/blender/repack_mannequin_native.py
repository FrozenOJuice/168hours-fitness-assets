"""Repack reviewed data into clean native scene/UI containers; verify geometry is unchanged."""
from pathlib import Path
import bpy,sys,shutil,json,hashlib,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,RID,SOURCE,RA
from barbell_20kg_common import setup,camera,digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));before=digest(SOURCE)
def geometry():
 o=bpy.data.objects[ID+'__mesh_body'];v=np.array([v.co[:] for v in o.data.vertices],dtype=np.float32);f=np.array([list(p.vertices) for p in o.data.polygons],dtype=np.int32);return hashlib.sha256(v.tobytes()+f.tobytes()).hexdigest()
gbefore=geometry();tmp=A/'__native_repack_input.blend';shutil.copy2(SOURCE,tmp);bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(tmp),link=False) as(src,dst):dst.collections=[ID]
c=dst.collections[0];s=bpy.context.scene;s.collection.children.link(c);s.name=ID+'__foundation_review';setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1200;s.render.resolution_y=1600
# Retain the separate linked canonical rest library if append localized dependency data.
for name in [ID+'__armature_deform',RID+'__armature_solver']:
 obj=bpy.data.objects[name]
 if not obj.data.library:
  path=RA/(RID+'__foundation_v02.blend')
  with bpy.data.libraries.load(str(path),link=True) as(src,dst):dst.armatures=[RID+'__skeleton_data_foundation_v02']
  obj.data=dst.armatures[0]
s.camera=camera(s,ID+'__camera_three_quarter',(2.6,5,1.8),(0,0,.88),2.05)
for obj in c.all_objects:
 if obj.type=='ARMATURE':obj.hide_set(True)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   sp=area.spaces.active;sp.shading.type='SOLID';sp.shading.light='FLAT';sp.shading.color_type='VERTEX';sp.shading.show_shadows=False;sp.shading.show_cavity=False;sp.shading.show_specular_highlight=False;sp.shading.show_object_outline=True;sp.region_3d.view_location=(0,0,.88);sp.region_3d.view_distance=2.5;sp.region_3d.view_rotation=s.camera.rotation_euler.to_quaternion()
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(A))
bpy.context.view_layer.update();assert geometry()==gbefore
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);tmp.unlink();m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['dependencies'][0]['sha256']=digest(RA/(RID+'__foundation_v02.blend'));write_json(A/'asset.json',m);write_json(A/'native-repack.json',{'before_sha256':before,'source_sha256':digest(SOURCE),'geometry_sha256_before':gbefore,'geometry_sha256_after':geometry(),'script_sha256':digest(Path(__file__)),'purpose':'Clean inherited native scene/UI state; no geometry or rig-interface edits'})
print('REPACK_DIRTY',bpy.data.is_dirty)
