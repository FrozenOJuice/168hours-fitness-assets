"""Asset-local prototype helpers; not an approved shared library standard."""
from pathlib import Path
import bpy, hashlib, json, math
from mathutils import Matrix, Vector
REPO = Path(__file__).resolve().parents[2]
ID = '168h_equipment_olympic_barbell_20kg'
ASSET = REPO/'assets/equipment/free_weights'/ID
SOURCE = ASSET/(ID+'.blend')
PID = '168h_equipment_olympic_plate_45lb_cast_iron'
PLATE = REPO/'assets/equipment/free_weights'/PID
SID = '168h_template_barbell_plate_compatibility'
FIXTURE = REPO/'scenes/templates'/SID
TEST_SOURCE = FIXTURE/(SID+'.blend')
VERSION = '0.1.0'
HEIGHT = .0365
PRESET = 'barbell_review_flat@0.1.0'
PALETTE = ['6D747E','8C949F','ADB5BE','C5CBD2','DDE2E7','EDF0F3','FAFBFC','89929E']

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path, data): Path(path).write_text(json.dumps(data,indent=2)+'\n')
def read_json(path): return json.loads(Path(path).read_text())
def verify_plate():
    record=read_json(PLATE/'reference-approval.json')
    for entry in [record['source'],record['render_settings'],record['validation_results'],*record['images']]:
        assert digest(REPO/entry['path'])==entry['sha256'],entry['path']
    manifest=read_json(PLATE/'asset.json')
    if manifest.get('origin_migration'):
        source=REPO/manifest['source']
        migration=read_json(REPO/'docs/audits/origin-migration-record.json')
        current=next(e for e in migration['records'] if e['source']==manifest['source'])
        assert digest(source)==current['source_sha256']==manifest['source_revision_or_digest'].removeprefix('sha256:'),'Current A14 plate differs from approved migrated source'
    return record

def setup(scene):
    scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
    scene.unit_settings.length_unit='METERS'
    scene.render.engine='BLENDER_WORKBENCH'
    scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
    scene.render.film_transparent=False;scene.display.render_aa='32'
    shade=scene.display.shading
    shade.light='FLAT';shade.color_type='MATERIAL';shade.show_shadows=False;shade.show_cavity=False
    shade.show_specular_highlight=False;shade.show_object_outline=True;shade.object_outline_color=(.015,.018,.022)
    shade.background_type='WORLD'
    scene.world=bpy.data.worlds.new(scene.name+'__world');scene.world.color=(1,1,1)
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    scene.frame_set(1)

def camera(scene,name,position,target,scale):
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);scene.collection.objects.link(o)
    data.type='ORTHO';data.ortho_scale=scale;data.clip_start=.001;data.clip_end=100
    o.location=position;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o

def camera_config(cam,path,target,configuration):
    return {'path':str(Path(path).relative_to(REPO)),'position_m':list(cam.location),'rotation_euler_xyz_radians':list(cam.rotation_euler),
            'projection':'ORTHO','ortho_scale_m':cam.data.ortho_scale,'target_m':list(target),'clip_start_m':cam.data.clip_start,'clip_end_m':cam.data.clip_end,'configuration':configuration,'frame':1}

def add_views(scene,assembled=False):
    z=.225 if assembled else HEIGHT
    if assembled:
        entries={'assembled_with_plates':((2.7,3.6,1.8),(0,0,z),2.50)}
        directory=FIXTURE/'previews';tag=SID;config='two_45lb_plates'
    else:
        entries={
          'full_length':((0,3,z),(0,0,z),2.50),
          'side':((3,0,z),(0,0,z),.12),
          'three_quarter':((2.0,3.8,1.65),(0,0,z),2.50),
          'detail':((.62,.40,.21),(.53,0,z),.38),
          'end_detail':((1.45,.48,.24),(1.01,0,z),.30)}
        directory=ASSET/'previews';tag=ID;config='unloaded'
    views={}
    for view,(position,target,scale) in entries.items():
        cam=camera(scene,tag+'__camera_'+view,position,target,scale)
        path=directory/f'{tag}__{view}__{config}.png'
        views[view]=camera_config(cam,path,target,config)
        scene.camera=cam;scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    return views

def link_collection(path,name):
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):
        assert name in src.collections
        dst.collections=[name]
    return dst.collections[0]

def instance(scene,col,name,matrix=None):
    o=bpy.data.objects.new(name,None);scene.collection.objects.link(o)
    o.instance_type='COLLECTION';o.instance_collection=col
    if matrix is not None:o.matrix_world=matrix
    return o

def local_anchor(col,asset_id,key):
    return col.all_objects[asset_id+'__anchor_'+key]

def asset_instance_frame(obj):
    """A14: collection instance matrix includes pivot; source coordinates require offset removal."""
    return obj.matrix_world@Matrix.Translation(-obj.instance_collection.instance_offset)

def plate_measurements(col):
    bore=local_anchor(col,PID,'bore_center').matrix_world.copy()
    frame=bore.inverted()
    points=[frame@(o.matrix_world@v.co) for o in col.all_objects if o.type=='MESH' for v in o.data.vertices]
    back=min(v.y for v in points);front=max(v.y for v in points)
    stackback=(frame@local_anchor(col,PID,'stack_back').matrix_world.translation).y
    stackfront=(frame@local_anchor(col,PID,'stack_front').matrix_world.translation).y
    assert abs(back-stackback)<1e-6 and abs(front-stackfront)<1e-6
    floor=local_anchor(col,PID,'floor_contact').matrix_world.translation
    return {'bore_matrix':bore,'back_m':back,'front_m':front,'pitch_m':front-back,'floor_to_bore_m':bore.translation.z-floor.z}

def place_plate(scene,bar_instance,bar_col,plate_col,side,index=0,gap=.001,instance_obj=None):
    m=plate_measurements(plate_col)
    target=asset_instance_frame(bar_instance)@local_anchor(bar_col,ID,'load_'+side).matrix_world
    outward=(target.to_3x3()@Vector((0,1,0))).normalized()
    target.translation+=outward*(-m['back_m']+gap+index*m['pitch_m'])
    matrix=target@m['bore_matrix'].inverted()
    obj=instance_obj or instance(scene,plate_col,'plate_'+side)
    obj.matrix_world=matrix@Matrix.Translation(plate_col.instance_offset)
    obj['placement']='load frame + measured linked back envelope + 1mm gap; compensate bore-root offset'
    return obj,m

def make_fixture():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene;scene.name=SID;setup(scene)
    bar=link_collection(SOURCE,ID);plate=link_collection(PLATE/(PID+'.blend'),PID)
    bar_instance=instance(scene,bar,'barbell_primary')
    plate_instances={side:instance(scene,plate,'plate_'+side) for side in ['l','r']}
    bpy.context.view_layer.update()
    m=plate_measurements(plate)
    axis=local_anchor(bar,ID,'axis_center').matrix_world.translation
    bar_instance.location.z=m['floor_to_bore_m']-axis.z+bar.instance_offset.z
    bpy.context.view_layer.update()
    for side in ['l','r']:place_plate(scene,bar_instance,bar,plate,side,instance_obj=plate_instances[side])
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath,start=str(FIXTURE))
    scene['purpose']='linked barbell/plate compatibility fixture, not exercise scene'
    bpy.context.view_layer.update()
    return scene,bar,plate

def viewport(target=(0,0,HEIGHT),distance=2.7):
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                sp=area.spaces.active;sp.region_3d.view_perspective='ORTHO'
                sp.region_3d.view_location=target;sp.region_3d.view_distance=distance
                sp.region_3d.view_rotation=Vector((0,-1,0)).to_track_quat('-Z','Y')
                sp.shading.type='SOLID';sp.shading.light='FLAT';sp.shading.color_type='MATERIAL'
                sp.shading.show_shadows=False;sp.shading.show_cavity=False;sp.shading.show_specular_highlight=False
                sp.shading.show_object_outline=True;sp.shading.object_outline_color=(.015,.018,.022)
                sp.shading.background_type='VIEWPORT';sp.shading.background_color=(1,1,1)
                sp.overlay.show_overlays=False
