"""Render from saved character; poses/highlights are transient and reproducible."""
import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
from mannequin_review_common import *
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
def render(draft=False):
    mc.MAPPING=None;bpy.ops.wm.open_mainfile(filepath=str(SOURCE));before=digest(SOURCE);s=bpy.context.scene;setup(s);s.display.shading.color_type='VERTEX';s.render.resolution_x=600 if draft else 1200;s.render.resolution_y=800 if draft else 1600
    views={'front':('neutral',(0,5,.88),(0,0,.88),2.05),'back':('neutral',(0,-5,.88),(0,0,.88),2.05),'side':('neutral',(5,0,.88),(0,0,.88),2.05),'three_quarter':('neutral',(3.3,5,2.2),(0,0,.88),2.05),'muscles_front':('muscles',(0,4,1.30),(0,0,1.30),1.25),'muscles_back':('muscles',(0,-4,1.30),(0,0,1.30),1.25),'bent_limbs':('bend',(3,5,2.2),(0,0,.88),2.05),'hand_grip':('grip',(1.4,3,1.1),(.55,.03,1.05),.43),'deep_xray':('xray',(.9,4,1.0),(.10,.02,.75),.47)}
    views['deep_xray_bent']=('xray_bend',(.9,4,1.0),(.10,.02,.75),.65)
    selected={'three_quarter':views['three_quarter']} if draft else views;records={}
    for key,(config,pos,target,scale) in selected.items():
        pose(config)
        if key=='hand_grip':
            target=tuple(get(ID+'__anchor_hand_grip_l').matrix_world.translation);pos=tuple(Vector(target)+Vector((1.4,3,.5)))
        if key=='deep_xray_bent':
            b=get(ID+'__armature_deform').pose.bones['thigh_l'];target=tuple((b.head+b.tail)*.5);pos=tuple(Vector(target)+Vector((.9,4,.4)))
        cam=camera(s,ID+'__camera_'+key,pos,target,scale);s.camera=cam
        p=(R/'exports/illustrations/mannequin_draft.png') if draft else A/'previews'/f'{ID}__{key}__{config}.png';p.parent.mkdir(parents=True,exist_ok=True);s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
        records[key]={**camera_config(cam,p,target,config),'sha256':digest(p)}
    assert digest(SOURCE)==before
    if not draft:
        settings={'id':'mannequin_review_vertex_flat@0.1.0','status':'asset-local provisional','source_sha256':before,'blender_version':bpy.app.version_string,'engine':'BLENDER_WORKBENCH','light':'FLAT','color_type':'VERTEX; evaluated geometry-node Color field','body_ramp':'normal dot(0.28,0.72,0.62)*0.42+0.50, gray endpoints (0.12,0.145,0.16)/(0.63,0.67,0.69); highlight form factor shade*0.35+0.65','primary_linear':[.66,.20,.17],'secondary_linear':[.85,.48,.19],'no_shadows':True,'no_AO_cavity':True,'no_specular':True,'outline':'native Workbench dark object outline','resolution':[1200,1600],'AA':32,'color_management':'Standard/None/exposure0/gamma1','background':'opaque white','renderer_sha256':digest(Path(__file__)),'pose_helper_sha256':digest(Path(__file__).with_name('mannequin_review_common.py')),'views':records};write_json(A/'previews/render-settings.json',settings)
        m=json.loads((A/'asset.json').read_text());m['reference_renders']=[{'view':k,**v,'source_revision_or_digest':'sha256:'+before,'preset_revision':digest(A/'previews/render-settings.json')} for k,v in records.items()];m['render_settings']=str((A/'previews/render-settings.json').relative_to(R));write_json(A/'asset.json',m)
    print('MANNEQUIN_RENDER',len(records))
if __name__=='__main__':render('--draft' in sys.argv)
