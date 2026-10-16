"""Render corrected native source neutral views; no source save."""
from pathlib import Path
import bpy,json,sys
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
from build_anatomical_mannequin import R,A,ID,SOURCE
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
from mannequin_core_poses import pose,coords
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;s=bpy.context.scene;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=1200;s.render.resolution_y=1600;pose('neutral_a_pose');before=digest(SOURCE);views={}
for key,pos in {'front':(0,5,.88),'back':(0,-5,.88),'side':(5,0,.88),'three_quarter':(2.6,5,1.8), 'torso_front':(0,5,1.25), 'torso_side':(5,0,1.25), 'torso_three_quarter':(2.6,5,1.55)}.items():
 target=(0,0,1.25) if key.startswith('torso_') else (0,0,.88); scale=.73 if key.startswith('torso_') else 2.05; s.camera=camera(s,ID+'__foundation_camera_'+key,pos,target,scale);p=A/'previews'/f'{ID}__{key}__foundation_v02.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);views[key]={**camera_config(s.camera,p,target,'neutral_a_pose'),'sha256':digest(p)}
settings={'id':'mannequin_foundation_flat@0.2.1','status':'asset-local review','source_sha256':before,'blender_version':bpy.app.version_string,'engine':'BLENDER_WORKBENCH','light':'FLAT','color_type':'VERTEX','normal_ramp':'dot(.28,.72,.62)*.70+.43; gray endpoints(.12,.145,.16)/(.62,.65,.67)','outline':'native dark object outline','shadows':False,'AO_cavity':False,'specular':False,'resolution':[1200,1600],'AA':32,'color_management':'Standard/None/exposure0/gamma1','background':'opaque white','renderer_sha256':digest(Path(__file__)),'views':views};write_json(A/'previews/render-settings.json',settings)
m=json.loads((A/'asset.json').read_text());m['reference_renders']=[{'view':k,**v,'source_revision_or_digest':'sha256:'+before,'preset_revision':digest(A/'previews/render-settings.json')} for k,v in views.items()];m['standards']['style_preset']=settings['id'];m['standards']['style_preset_revision']=digest(A/'previews/render-settings.json');write_json(A/'asset.json',m);assert digest(SOURCE)==before
