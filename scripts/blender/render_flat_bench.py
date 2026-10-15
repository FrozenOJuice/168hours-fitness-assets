"""Render saved standalone bench; does not resave or change geometry. MIT code."""
from pathlib import Path
import bpy, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
from build_flat_bench import REPO,ID,ASSET,SOURCE

def render(directory=None):
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    scene=bpy.context.scene;setup(scene)
    for o in list(bpy.data.objects):
        if o.type=='CAMERA':bpy.data.objects.remove(o,do_unlink=True)
    entries={
        'side':((3,0,.24),(0,0,.24),1.50),
        'three_quarter':((1.8,2.8,1.6),(0,0,.25),1.55),
        'front':((0,3,.24),(0,0,.24),.90),
        'top':((0,0,3),(0,0,0),2.10)
    }
    views={}
    for view,(position,target,scale) in entries.items():
        cam=camera(scene,ID+'__camera_'+view,position,target,scale)
        path=(Path(directory) if directory else ASSET/'previews')/f'{ID}__{view}__flat.png'
        path.parent.mkdir(parents=True,exist_ok=True)
        scene.camera=cam;scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        views[view]=camera_config(cam,path,target,'flat');views[view]['sha256']=digest(path)
    return views

if __name__=='__main__':
    views=render()
    write_json(ASSET/'previews/render-settings.json',{
        'id':'flat_bench_review_flat@0.1.0','status':'asset-local review proposal; not shared preset',
        'source_sha256':digest(SOURCE),'renderer_script_sha256':digest(Path(__file__)),
        'setup_helper_sha256':digest(Path(__file__).with_name('barbell_20kg_common.py')),
        'blender_version':bpy.app.version_string,'add_ons':[], 'engine':'BLENDER_WORKBENCH',
        'lighting':'FLAT; no light objects, specular highlights, ground plane or baked maps',
        'shadows':False,'ambient_occlusion':False,'cavity':False,'color_type':'MATERIAL',
        'resolution':[1600,1000],'percentage':100,'format':'PNG','color_mode':'RGBA','bit_depth':8,
        'sampling':'32 AA','seed':None,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,
        'background':'opaque white WORLD','outline':{'method':'native Workbench object outline','color_linear':[.015,.018,.022],'width':'native fixed screen-space; no configurable numeric width; not library-wide standard'},
        'palette':{m.name:m.get('srgb_hex') for m in bpy.data.materials},'frame':1,'views':views})
    print('BENCH_RENDERS_COMPLETE')
