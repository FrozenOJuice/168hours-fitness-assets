"""Expanded linked movement review and V0.3.0 comparisons; approved equipment read-only."""
import bpy,sys,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from mannequin_v031_render import setup
from barbell_20kg_common import camera,camera_config,digest,write_json,link_collection,instance
import mannequin_review_common as mc
import mannequin_v031_poses as poses
import mannequin_v03_poses as oldposes
import build_mannequin_anatomy_study as shared
FID=F.name;shared.FID=FID

def character(scene,col):
 ref=instance(scene,col,'character_link_reference');bpy.context.view_layer.update();c=col.override_hierarchy_create(scene,bpy.context.view_layer,reference=ref,do_fully_editable=True)
 if ref.name in bpy.data.objects:bpy.data.objects.remove(ref,do_unlink=True)
 if c.name not in scene.collection.children:scene.collection.children.link(c)
 mapping=shared.mapping(c)
 for o in c.all_objects:
  for mod in o.modifiers:
   if mod.type=='NODES':
    mod.node_group=mod.node_group.copy()
    for n in mod.node_group.nodes:
     for sock in n.inputs:
      if hasattr(sock,'default_value') and isinstance(sock.default_value,bpy.types.Object) and sock.default_value.name in mapping:sock.default_value=mapping[sock.default_value.name]
    if mod.node_group.animation_data:
     for d in mod.node_group.animation_data.drivers:
      for v in d.driver.variables:
       for t in v.targets:
        if t.id and t.id.name in mapping:t.id=mapping[t.id.name]
  if o.animation_data:
   for d in o.animation_data.drivers:
    for v in d.driver.variables:
     for t in v.targets:
      if t.id and t.id.name in mapping:t.id=mapping[t.id.name]
  if o.type=='ARMATURE' or '__helper_' in o.name or '__control_grip_cylinder_' in o.name:o.hide_set(True)
 return c,mapping

def build():
 bpy.ops.wm.read_factory_settings(use_empty=True);first=bpy.context.scene;col=link_collection(SOURCE,ID);records={};views={}
 for i,name in enumerate(poses.POSES):
  s=first if i==0 else bpy.data.scenes.new(FID+'__'+name);s.name=FID+'__'+name;bpy.context.window.scene=s;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1600;s.render.resolution_y=1200;c,mc.MAPPING=character(s,col);poses.pose(name);points=poses.coords();rec={'scene':s.name,'character_collection':c.name,'root_object':mc.get(ID+'__root').name,'body_mesh_linked':bool(mc.get(ID+'__mesh_body').data.library),'pose':name,'engine':s.render.engine,'views':{}}
  if name=='bar_grip':
   bid='168h_equipment_olympic_barbell_20kg';bc=link_collection(R/'assets/equipment/free_weights'/bid/(bid+'.blend'),bid);o=instance(s,bc,'bar_grip_reference',Matrix.Translation((0,.318,1.08))@Matrix.Translation(bc.instance_offset));rec.update(bar_object=o.name,shaft_radius_m=.014,bar_center_m=[0,.318,1.08]);points=np.concatenate([points,np.array([[-1.1,.318,1.08],[1.1,.318,1.08]])])
  for view,direction in [('three_quarter',(2.6,5,1.4)),('side',(5,0,.15))]:
   p=F/'previews'/f'{FID}__{name}__{view}.png';rec['views'][view]=shared.shot(s,view,points,direction,p,name);views[name+'_'+view]=rec['views'][view]
  details={}
  if name=='arms_raised':details={k:((0,0,1.52),d,.95) for k,d in [('shoulder_front',(0,5,.1)),('shoulder_side',(5,0,.1)),('shoulder_three_quarter',(2.6,5,.5))]}
  if name=='bar_grip':details={'hand_detail':(mc.get(ID+'__anchor_hand_grip_l').matrix_world.translation,(.4,.8,.6),.30)}
  if name.startswith('xray'):details={'thigh_detail':((.105,0,.735),(1.5,5,.4),.52)}
  for view,(target,direction,scale) in details.items():
   cam=camera(s,FID+'__camera_'+name+'_'+view,Vector(target)+Vector(direction),target,scale);s.camera=cam;p=F/'previews'/f'{FID}__{name}__{view}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);rec['views'][view]={**camera_config(cam,p,target,name),'sha256':digest(p)};views[name+'_'+view]=rec['views'][view]
  s.camera=bpy.data.objects[FID+'__camera_'+name+'_three_quarter'];records[name]=rec
 oldcol=link_collection(PREVIOUS/(ID+'.blend'),ID);comparisons={}
 for name in ['neutral_a_pose','arms_forward','arms_lateral','arms_raised','seated','hip_flexion_knee_bend','muscles_neutral']:
  s=bpy.data.scenes.new(FID+'__comparison_'+name);bpy.context.window.scene=s;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=2000;s.render.resolution_y=1400;points=[];cols=[]
  for csrc,shift,isold in [(oldcol,.85,True),(col,-.85,False)]:
   c,mc.MAPPING=character(s,csrc)
   if isold and name in oldposes.POSES:oldposes.pose(name)
   else:poses.pose(name)
   mc.get(ID+'__root').location.x+=shift;mc.update();points.extend(poses.coords().tolist());cols.append(c.name)
  for view,direction in ([('front',(0,5,.05)),('three_quarter',(2.6,7,1.2))] if name=='neutral_a_pose' else [('three_quarter',(2.6,7,1.2))]):
   p=F/'previews'/f'{FID}__comparison_{name}__{view}.png';v=shared.shot(s,view,np.array(points),direction,p,'v030_left_v031_right');views['comparison_'+name+'_'+view]=v
  comparisons[name]={'scene':s.name,'collections':cols,'viewer_order':'V0.3.0 left /V0.3.1 right in front view; world+X/-X respectively','style':'Same flat VERTEX illustrated preset; same numeric ramp, masks intentionally differ in highlight case'}
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(F))
 bpy.context.window.scene=bpy.data.scenes[records['neutral_a_pose']['scene']];bpy.ops.wm.save_as_mainfile(filepath=str(FS),compress=True,relative_remap=False)
 write_json(F/'suite.json',{'id':FID,'version':'0.3.1','status':'review','source_sha256':digest(FS),'character_sha256':digest(SOURCE),'previous_sha256':digest(PREVIOUS/(ID+'.blend')),'builder_sha256':digest(Path(__file__)),'pose_helper_sha256':digest(Path(__file__).with_name('mannequin_v031_poses.py')),'poses':records,'comparisons':comparisons})
 write_json(F/'previews/render-settings.json',{'engine':'BLENDER_WORKBENCH normally; BLENDER_EEVEE only xray scenes','light':'FLAT vertex illustration /emission transparent Xray','shadows':False,'AO_cavity_GI':False,'specular':False,'AA':32,'xray_samples':64,'xray_alpha':'Smooth skin field1..0.16, BLENDED, no face deletion','xray_outline':'Freestyle silhouette1px','normal_outline':'Workbench native silhouette','resolution':[1600,1200],'comparison_resolution':[2000,1400],'color_management':'Standard/None/exposure0/gamma1','background':'opaque white','source_sha256':digest(FS),'views':views})
 print('MOVEMENT_REVIEW',len(records),len(views))
if __name__=='__main__':build()
