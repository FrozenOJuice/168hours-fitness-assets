"""Thirteen linked pose/highlight states and comparisons; no exercise assembly."""
from pathlib import Path
import bpy,json,sys,numpy as np
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
import mannequin_v03_poses as cp
from mannequin_v03_common import R,A,ID,RID,SOURCE,F,FS,MASTER
from barbell_20kg_common import setup,camera,camera_config,digest,write_json,link_collection,instance
FID=F.name;BAR='168h_equipment_olympic_barbell_20kg'
def mapping(collection):return {o.override_library.reference.name:o for o in collection.all_objects if o.override_library}
def shot(scene,key,points,direction,path,pose):
 lo,hi=points.min(axis=0),points.max(axis=0);target=Vector((lo+hi)*.5);cam=camera(scene,FID+'__camera_'+pose+'_'+key,target+Vector(direction)*5,target,3.0);inv=cam.matrix_world.inverted();bpy.context.view_layer.update();inv=cam.matrix_world.inverted();project=np.array([(inv@Vector(p))[:] for p in points]);aspect=scene.render.resolution_x/scene.render.resolution_y;cam.data.ortho_scale=max(float(np.ptp(project[:,0])),float(np.ptp(project[:,1]))*aspect)*1.12;scene.camera=cam;scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);return {**camera_config(cam,path,target,pose),'sha256':digest(path)}
def build():
 bpy.ops.wm.read_factory_settings(use_empty=True);first=bpy.context.scene;c=link_collection(SOURCE,ID);records={};allviews={}
 for index,name in enumerate(cp.POSES):
  s=first if index==0 else bpy.data.scenes.new(FID+'__'+name);s.name=FID+'__'+name;bpy.context.window.scene=s;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1600;s.render.resolution_y=1200
  inst=instance(s,c,'character_link_reference');bpy.context.view_layer.update();override=c.override_hierarchy_create(s,bpy.context.view_layer,reference=inst,do_fully_editable=True)
  if inst.name in bpy.data.objects:bpy.data.objects.remove(inst,do_unlink=True)
  if override.name not in s.collection.children:s.collection.children.link(override)
  mc.MAPPING=mapping(override);root=mc.get(ID+'__root');body=mc.get(ID+'__mesh_body')
  for obj in [body,mc.get(ID+'__mesh_vastus_intermedius_l')]:
   for mod in obj.modifiers:
    if mod.type=='NODES':
     mod.node_group=mod.node_group.copy()
     for node in mod.node_group.nodes:
      for socket in node.inputs:
       if hasattr(socket,'default_value') and isinstance(socket.default_value,bpy.types.Object) and socket.default_value.name in mc.MAPPING:socket.default_value=mc.MAPPING[socket.default_value.name]
     if mod.node_group.animation_data:
      for driver in mod.node_group.animation_data.drivers:
       for var in driver.driver.variables:
        for t in var.targets:
         if t.id and t.id.name in mc.MAPPING:t.id=mc.MAPPING[t.id.name]
  for obj in override.all_objects:
   if obj.animation_data:
    for driver in obj.animation_data.drivers:
     for var in driver.driver.variables:
      for t in var.targets:
       if t.id and t.id.name in mc.MAPPING:t.id=mc.MAPPING[t.id.name]
  cp.pose(name);points=cp.coords();record={'scene':s.name,'character_collection':override.name,'root_object':root.name,'body_mesh_linked':bool(body.data.library),'body_mesh_data':body.data.name,'pose':name,'views':{}}
  if name=='bar_grip':
   barcol=link_collection(R/'assets/equipment/free_weights'/BAR/(BAR+'.blend'),BAR);bar=instance(s,barcol,'bar_grip_reference',Matrix.Translation((0,.318,1.080))@Matrix.Translation(barcol.instance_offset));record['bar_object']=bar.name;record['shaft_radius_m']=.014;record['bar_center_m']=[0,.318,1.080]
   points=np.concatenate([points,np.array([[-1.10,.318,1.080],[1.10,.318,1.080]])])
  for view,direction in [('three_quarter',(2.6,5,1.4)),('side',(5,0,.15))]:
   p=F/'previews'/f'{FID}__{name}__{view}.png';record['views'][view]=shot(s,view,points,direction,p,name);allviews[name+'_'+view]=record['views'][view]
  if name=='arms_raised':
   for view,direction in [('shoulder_front',(0,5,.1)),('shoulder_side',(5,0,.1)),('shoulder_three_quarter',(2.6,5,.5))]:
    target=Vector((0,0,1.52));cam=camera(s,FID+'__camera_'+name+'_'+view,target+Vector(direction),target,.95);s.camera=cam;p=F/'previews'/f'{FID}__{name}__{view}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);record['views'][view]={**camera_config(cam,p,target,name),'sha256':digest(p)};allviews[name+'_'+view]=record['views'][view]
  if name=='bar_grip':
   p=F/'previews'/f'{FID}__bar_grip__hand_detail.png';anchor=mc.get(ID+'__anchor_hand_grip_l').matrix_world.translation;cam=camera(s,FID+'__camera_grip_detail',anchor+Vector((.4,.8,.6)),anchor,.30);s.camera=cam;s.render.filepath=str(p);bpy.ops.render.render(write_still=True);record['views']['hand_detail']={**camera_config(cam,p,anchor,name),'sha256':digest(p)};allviews[name+'_hand_detail']=record['views']['hand_detail']
  s.camera=bpy.data.objects[FID+'__camera_'+name+'_three_quarter']
  for obj in override.all_objects:
   if obj.type=='ARMATURE':obj.hide_set(True)
  records[name]=record
 # Front camera faces -Y: old at+X is viewer-left, new at-X is viewer-right.
 comparison=bpy.data.scenes.new(FID+'__comparison');bpy.context.window.scene=comparison;setup(comparison);comparison.display.shading.color_type='SINGLE';comparison.display.shading.single_color=(.47,.50,.52);comparison.display.shading.light='STUDIO';comparison.display.shading.show_shadows=False;comparison.display.shading.show_cavity=False;comparison.display.shading.show_specular_highlight=False;comparison.render.resolution_x=2000;comparison.render.resolution_y=1400
 oldcol=link_collection(MASTER/(ID+'.blend'),ID);instance(comparison,oldcol,'preserved_master_left',Matrix.Translation((.85,0,0)));instance(comparison,c,'anatomy_prototype_right',Matrix.Translation((-.85,0,0)))
 for view,pos in [('front',(0,6,.88)),('three_quarter',(2.6,7,1.65))]:
  cam=camera(comparison,FID+'__camera_comparison_'+view,pos,(0,0,.88),3.45);comparison.camera=cam;p=F/'previews'/f'{FID}__comparison__{view}.png';comparison.render.filepath=str(p);bpy.ops.render.render(write_still=True);allviews['comparison_'+view]={**camera_config(cam,p,(0,0,.88),'master_left_prototype_right'),'sha256':digest(p)}
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(F))
 bpy.context.window.scene=bpy.data.scenes[records['neutral_a_pose']['scene']];bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(FS),compress=True,relative_remap=False)
 write_json(F/'suite.json',{'id':FID,'version':'0.3.0','status':'review','source_sha256':digest(FS),'character_sha256':digest(SOURCE),'pose_helper_sha256':digest(Path(__file__).with_name('mannequin_v03_poses.py')),'core_helper_sha256':digest(Path(__file__).with_name('mannequin_core_poses.py')),'builder_sha256':digest(Path(__file__)),'poses':records,'scope':'core human foundation only; no exercise scene approval'})
 write_json(F/'previews/render-settings.json',{'engine':'BLENDER_WORKBENCH','light':'FLAT','color_type':'VERTEX/equipment material fallback','shadows':False,'AO_cavity':False,'specular':False,'AA':32,'resolution':[1600,1200],'comparison_override':{'light':'STUDIO','color_type':'SINGLE','single_color':[.47,.50,.52],'resolution':[2000,1400],'purpose':'Equal gray diagnostic evaluation, avoiding unequal per-character color ramps; no shadows/AO/specular'},'color_management':'Standard/None/exposure0/gamma1','outline':'native dark object outline','background':'opaque white','source_sha256':digest(FS),'views':allviews})
 print('CORE_SUITE',len(records),len(allviews))
if __name__=='__main__':build()
