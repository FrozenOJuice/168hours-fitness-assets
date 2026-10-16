"""Render isolated anatomical study, with source pins and no source save."""
import bpy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
import mannequin_review_common as mc
import mannequin_v03_poses as poses
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;s=bpy.context.scene;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1200;s.render.resolution_y=1600;before=digest(SOURCE);views={}
for state in ['neutral_a_pose','arms_raised','elbow_flexion','seated','squat']:
 poses.pose(state)
 for view,pos in [('front',(0,5,.88)),('three_quarter',(2.6,5,1.65))]:
  s.camera=camera(s,ID+'__study_camera_'+state+'_'+view,pos,(0,0,.88),2.2 if state=='arms_raised' else 2.05);p=A/'previews'/f'{ID}__{view}__{state}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);views[state+'_'+view]={**camera_config(s.camera,p,(0,0,.88),state),'sha256':digest(p)}
write_json(A/'previews/render-settings.json',{'id':'mannequin_anatomy_flat@0.3.0','status':'local review only','source_sha256':before,'engine':'BLENDER_WORKBENCH','light':'FLAT','color_type':'VERTEX','shadows':False,'AO_cavity':False,'specular':False,'AA':32,'resolution':[1200,1600],'color_management':'Standard/None/exposure0/gamma1','background':'opaque white','outline':'native dark object outline','views':views});assert before==digest(SOURCE)
