"""Anatomically located schematic deep-muscle volume and smoother local aperture."""
import bpy,sys,numpy as np,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import digest,write_json
import mannequin_core_poses as cp
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));cp.pose('neutral_a_pose');body=bpy.data.objects[ID+'__mesh_body'];deep=bpy.data.objects[ID+'__mesh_vastus_intermedius_l'];arm=bpy.data.objects[ID+'__armature_deform'];cx=arm.data.bones['thigh_l'].head_local.x;verts=[];faces=[]
for j in range(17):
 t=j/16;z=.59+.29*t;r=(math.sin(math.pi*t)**.72)*.032+.003
 for k in range(32):a=2*math.pi*k/32;verts.append((cx+r*math.cos(a),.028+r*.78*math.sin(a),z))
for j in range(16):
 for k in range(32):a=j*32+k;b=j*32+(k+1)%32;faces.append((a,b,b+32,a+32))
faces+=[tuple(reversed(range(32))),tuple(range(16*32,17*32))];me=bpy.data.meshes.new(ID+'__deep_vastus_intermedius_study');me.from_pydata(verts,[],faces);me.update();deep.data=me;deep.vertex_groups.clear();group=deep.vertex_groups.new(name='thigh_l');group.add(list(range(len(verts))),1,'REPLACE');mid='muscle_vastus_intermedius_l';group=deep.vertex_groups.new(name=mid);group.add(list(range(len(verts))),1,'REPLACE');attr=me.attributes.new(mid,'FLOAT','POINT');attr.data.foreach_set('value',np.ones(len(verts),dtype=np.float32));me.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
for f in me.polygons:f.use_smooth=True
# One named experimental muscle, seated deep to the anterior quadriceps; no claim of an atlas.
p=np.array([v.co[:] for v in body.data.vertices]);window=np.exp(-((p[:,0]-cx)/.063)**4-((p[:,2]-.735)/.115)**4)*np.clip((p[:,1]-.005)/.035,0,1);body.data.attributes['xray_window'].data.foreach_set('value',window.astype(np.float32))
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False);write_json(A/'xray-refinement.json',{'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'region':'Left vastus intermedius, schematic fusiform deep volume anterior to femur, Z0.59..0.88m, selected through local body aperture','limitations':'Position/form provisional; not complete reconstruction of anatomical attachments or contraction; on-character localized cutaway, no separate diagram'})
