"""Link approved sources into a technical review assembly; never append geometry."""
from pathlib import Path
import bpy,sys,json,math
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import setup,camera,link_collection,instance,asset_instance_frame,digest,write_json
from build_barbell_stands import R,ID,A,SOURCE
SID='168h_template_stands_bench_barbell';F=R/'scenes/templates'/SID;OUT=F/(SID+'.blend')
BID='168h_equipment_flat_bench';BBID='168h_equipment_olympic_barbell_20kg'

def build():
    assert not OUT.exists(),'Initial builder cannot overwrite review assembly'
    paths=[A,R/'assets/equipment/benches'/BID,R/'assets/equipment/free_weights'/BBID]
    manifests=[json.loads((p/'asset.json').read_text()) for p in paths]
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name=SID+'__review';setup(s)
    cols=[link_collection(R/m['source'],m['collection']) for m in manifests]
    stands=instance(s,cols[0],'stands_pair',Matrix.Translation((0,.58,0))@Matrix.Rotation(math.pi,4,'Z'))
    bench=instance(s,cols[1],'bench_primary',Matrix.Identity(4))
    bpy.context.view_layer.update()
    frames=[asset_instance_frame(stands)@cols[0].all_objects[ID+'__anchor_bar_axis_'+side].matrix_world for side in ['l','r']]
    center=(frames[0].translation+frames[1].translation)/2
    bar=instance(s,cols[2],'barbell_primary',Matrix.Identity(4))
    bpy.context.view_layer.update()
    barframe=cols[2].all_objects[BBID+'__anchor_axis_center'].matrix_world.copy()
    target=barframe.copy();target.translation=center  # preserve canonical anchor orientation: its +Y follows shaft+X
    bar.matrix_world=target@barframe.inverted()@Matrix.Translation(cols[2].instance_offset)
    bpy.context.view_layer.update()
    cam=camera(s,SID+'__camera_assembled',(3.4,-4.2,2.7),(0,.1,.6),2.8);s.camera=cam
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                sp=area.spaces.active;sp.shading.light='FLAT';sp.shading.color_type='MATERIAL';sp.shading.show_shadows=False;sp.shading.show_cavity=False;sp.shading.show_specular_highlight=False;sp.shading.show_object_outline=True;sp.region_3d.view_distance=3;sp.region_3d.view_location=(0,.1,.6);sp.region_3d.view_rotation=cam.rotation_euler.to_quaternion();sp.region_3d.view_perspective='ORTHO'
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(F))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True,relative_remap=False)
    meta=json.loads((F/'asset.json').read_text());meta['source_revision_or_digest']='sha256:'+digest(OUT)
    meta['dependencies']=[{'id':m['id'],'version':m['version'],'source':m['source'],'sha256':digest(R/m['source'])} for m in manifests]
    meta['instance_frames']={o.name:[list(row) for row in o.matrix_world] for o in [stands,bench,bar]};meta['bar_center_m']=list(center)
    write_json(F/'asset.json',meta);write_json(F/'build-record.json',{'source_sha256':digest(OUT),'builder_sha256':digest(Path(__file__)),'dependencies':meta['dependencies'],'bar_center_m':list(center),'placement':'existing bar axis_center frame aligned automatically to midpoint of two stands bar_axis anchors'})
    print('ASSEMBLY_BUILD',list(center))
if __name__=='__main__':build()
