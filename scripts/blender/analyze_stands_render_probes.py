"""Compare disposable probes and localize changes; approved strict gate is untouched."""
from pathlib import Path
import bpy,sys,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_barbell_stands import A,R
from build_stands_review_assembly import F,OUT,SID
from investigate_stands_gates import DEST
from barbell_20kg_common import write_json,setup,camera
def load(p):
    im=bpy.data.images.load(str(p),check_existing=False)
    x=np.rint(np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4)*255).astype(np.int16)
    bpy.data.images.remove(im);return x
def stats(a,b):
    d=np.abs(a-b);changed=np.any(d!=0,axis=2);yx=np.argwhere(changed)
    return {'max_8bit_delta':int(d.max()),'changed_channel_fraction':float(np.count_nonzero(d)/d.size),'changed_pixel_fraction':float(changed.mean()),'mean_absolute_8bit_delta':float(d.mean()),'changed_pixel_bbox_xy_bottom_origin':[[int(yx[:,1].min()),int(yx[:,0].min())],[int(yx[:,1].max()),int(yx[:,0].max())]] if len(yx) else None}
rows=[]
bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene;setup(s)
for view,pos in [('assembled',(3.4,-4.2,2.7)),('side',(4,.10,.60))]:
    arrays=[load(DEST/f'{view}_{i}_{j}.png') for i in range(3) for j in range(2)]
    ref=load(F/'previews'/f'{SID}__{view}__bench_barbell.png')
    pairs=[{'probe':i,'against_reference':stats(ref,a)} for i,a in enumerate(arrays)]
    repeats=[{'a':i,'b':j,**stats(arrays[i],arrays[j])} for i in range(len(arrays)) for j in range(i+1,len(arrays))]
    cam=camera(s,'diagnostic_'+view,pos,(0,.1,.6),2.8);s.camera=cam;bpy.context.view_layer.update()
    changed=np.any(ref!=arrays[0],axis=2);coords=np.argwhere(changed);hits={}
    from mathutils import Vector
    rot=cam.matrix_world.to_3x3();width=cam.data.ortho_scale;height=width*1000/1600
    for y,x in coords:
        origin=cam.matrix_world@Vector(((x+.5)/1600*width-width/2,(y+.5)/1000*height-height/2,0))
        result=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,rot@Vector((0,0,-1)))
        name=result[4].name if result[0] else 'background/antialias-edge'
        hits[name]=hits.get(name,0)+1
    # Retained diagnostic downsample? full heatmap highlights all changed pixels red.
    pic=ref.astype(np.float32)/255;pic[changed,:3]=[1,0,0]
    im=bpy.data.images.new(view+'_changed_pixels',width=1600,height=1000,alpha=True)
    im.pixels[:]=pic.ravel();im.filepath_raw=str(DEST/(view+'_changes.png'));im.file_format='PNG';im.save();bpy.data.images.remove(im)
    rows.append({'view':view,'reference_comparisons':pairs,'pairwise_repeat_comparisons':repeats,'changed_pixel_ray_hits_first_probe':hits})
write_json(A/'render-investigation.json',{'comparisons':rows,'comparison_domain':'decoded RGBA8, no image registration/filtering; exact criterion unchanged','approval':'none; diagnostic only'})
print(json.dumps(rows,indent=2))
