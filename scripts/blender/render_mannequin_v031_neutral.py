"""Authoritative unassembled neutral references only, no source save."""
import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
import mannequin_review_common as mc
import mannequin_core_poses as core
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;core.pose('neutral_a_pose');s=bpy.context.scene;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1200;s.render.resolution_y=1600;before=digest(SOURCE);views={}
for view,pos in {'front':(0,5,.88),'back':(0,-5,.88),'side':(5,0,.88),'three_quarter':(2.6,5,1.65),'torso_front':(0,5,1.27),'torso_side':(5,0,1.27),'torso_three_quarter':(2.6,5,1.55)}.items():
 target=(0,0,1.27) if view.startswith('torso') else (0,0,.88);scale=.85 if view.startswith('torso') else 2.35;s.camera=camera(s,ID+'__camera_neutral_'+view,pos,target,scale);p=A/'previews'/f'{ID}__{view}__neutral.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);views[view]={**camera_config(s.camera,p,target,'neutral_a_pose'),'sha256':digest(p)}
settings={'id':'mannequin_anatomy_flat@0.3.1','status':'asset-local provisional','source_sha256':before,'blender_version':bpy.app.version_string,'engine':'BLENDER_WORKBENCH','light':'FLAT','color_type':'VERTEX','normal_ramp':'dot(.28,.72,.62)*.78+.35; endpoints(.10,.13,.15)/(.58,.62,.64)','shadows':False,'AO_cavity':False,'specular':False,'outline':'native dark object silhouette','AA':32,'resolution':[1200,1600],'background':'opaque white','color_management':'Standard/None/exposure0/gamma1','renderer_sha256':digest(Path(__file__)),'views':views};write_json(A/'previews/render-settings.json',settings);m=json.loads((A/'asset.json').read_text());m['reference_renders']=[{'view':key,**v,'source_revision_or_digest':'sha256:'+before,'preset_revision':digest(A/'previews/render-settings.json')} for key,v in views.items()];write_json(A/'asset.json',m);assert digest(SOURCE)==before
