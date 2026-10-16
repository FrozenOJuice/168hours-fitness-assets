"""Render saved review sources, or reproduce pixels without resaving either blend."""
from pathlib import Path
import bpy,sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import setup,camera,camera_config,digest,write_json
from build_barbell_stands import R,ID,A,SOURCE
from build_stands_review_assembly import SID,F,OUT

def render(reproduce=False,assembly_only=False):
    result=[]; comparisons=[]
    policy=None;policy_path=A/'render-comparison-policy.json'
    if reproduce and policy_path.exists():
        policy=json.loads(policy_path.read_text())
        assert policy['status']=='approved'
        for entry in policy['pinned_inputs']:assert digest(R/entry['path'])==entry['sha256'],entry['path']
    for src,folder,tag,entries in [
      (SOURCE,A,ID,{'front':((0,4,.55),(0,0,.55),2.2,'bench'),'side':((4,0,.55),(0,0,.55),2.0,'bench'),'three_quarter':((3.3,4.4,2.8),(0,0,.55),2.85,'bench'),'maximum_height':((3.3,4.4,2.8),(0,0,.92),3.7,'maximum_height'),'hook_detail':((1.0,.6,1.22),(.55,.10,.97),.38,'bench'),'adjustment_detail':((.15,-.35,1.14),(.50,0,.93),.33,'bench')}),
      (OUT,F,SID,{'assembled':((3.4,-4.2,2.7),(0,.10,.60),2.8,'bench_barbell'),'side':((4,.10,.60),(0,.10,.60),2.8,'bench_barbell'),'front':((0,-4,.60),(0,.10,.60),2.8,'bench_barbell')})]:
        if assembly_only and src==SOURCE:continue
        before=digest(src);bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;setup(s)
        for o in list(bpy.data.objects):
            if o.type=='CAMERA' and not o.library:bpy.data.objects.remove(o,do_unlink=True)
        views={}
        for view,(pos,target,scale,config) in entries.items():
            if src==SOURCE:
                root=bpy.data.objects[ID+'__root']
                for side in ['l','r']:root['height_index_'+side]=15 if config=='maximum_height' else 0
                root.update_tag();s.frame_set(1);bpy.context.view_layer.update()
            cam=camera(s,tag+'__camera_'+view,pos,target,scale);s.camera=cam
            expected=folder/'previews'/f'{tag}__{view}__{config}.png'
            p=(R/'exports/illustrations/stands_reproduction'/tag/expected.name) if reproduce else expected;p.parent.mkdir(parents=True,exist_ok=True)
            s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
            if reproduce:
                comparisons.append((tag+':'+view,expected,p))
            else:
                views[view]=camera_config(cam,p,target,config);views[view]['sha256']=digest(p)
        assert before==digest(src)
        if not reproduce:
            settings={'id':'stands_review_flat@0.1.0','status':'asset-local review proposal; no shared change','source_sha256':before,'renderer_sha256':digest(Path(__file__)),'helper_sha256':digest(Path(__file__).with_name('barbell_20kg_common.py')),'blender_version':bpy.app.version_string,'add_ons':[],'engine':'BLENDER_WORKBENCH','lighting':'FLAT; no lights/ground/baked lighting','shadows':False,'ambient_occlusion':False,'cavity':False,'specular':False,'resolution':[1600,1000],'percentage':100,'format':'PNG','color_mode':'RGBA','bit_depth':8,'sampling':'32AA','seed':None,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background':'opaque white WORLD','outline':{'method':'native Workbench object outline','color_linear':[.015,.018,.022],'width':'native fixed screen space; not global numeric standard'},'palette':{m.name:m.get('srgb_hex') for m in bpy.data.materials},'views':views}
            write_json(folder/'previews/render-settings.json',settings);meta=json.loads((folder/'asset.json').read_text());meta['reference_renders']=[{'view':k,'path':v['path'],'configuration':v['configuration'],'frame':1,'sha256':v['sha256'],'source_revision_or_digest':'sha256:'+before,'preset_revision':digest(folder/'previews/render-settings.json')} for k,v in views.items()];write_json(folder/'asset.json',meta)
    if reproduce:
        # Keep pixel comparison image datablocks out of the render sequence.
        # Only explicitly approved assembly views use the pinned local exception.
        import numpy as np
        from compare_stands_render import compare
        for view,expected,p in comparisons:
            images=[bpy.data.images.load(str(x),check_existing=False) for x in [expected,p]]
            arrays=[np.rint(np.asarray(im.pixels[:]).reshape(im.size[1],im.size[0],4)*255).astype(np.uint8) for im in images]
            limits=policy['limits'] if policy and view in policy['views'] else None
            result.append({'view':view,**compare(arrays[0],arrays[1],limits)})
            for im in images:bpy.data.images.remove(im)
        write_json(A/'render-reproduction.json',{'source_sha256':digest(SOURCE),'assembly_sha256':digest(OUT),'renderer_sha256':digest(Path(__file__)),'policy_sha256':digest(policy_path) if policy else None,'checks':result,'pass':all(e['result']=='PASS' for e in result),'master_sources_resaved':False});assert all(e['result']=='PASS' for e in result),result
    print('STANDS_RENDER',result if reproduce else 'COMPLETE')
if __name__=='__main__':render('--reproduce' in sys.argv,'--assembly-only' in sys.argv)
