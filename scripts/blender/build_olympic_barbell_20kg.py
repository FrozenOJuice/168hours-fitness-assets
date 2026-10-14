"""Build the explicitly requested barbell review prototype and linked fixture.
Refuses overwrite unless -- --replace-review is passed. Never writes the plate.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import *
import bmesh
verify_plate()
if (SOURCE.exists() or TEST_SOURCE.exists()) and '--replace-review' not in sys.argv:
    raise RuntimeError('Prototype exists. Review authorization before using --replace-review.')
assert (ASSET/'SPEC.md').exists() and (ASSET/'asset.json').exists()
prebuild=digest(ASSET/'SPEC.md')
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.name=ID+'__source';setup(scene)
asset=bpy.data.collections.new(ID);scene.collection.children.link(asset)
parts={}
for name in ['geo','rig','anchors']:
    parts[name]=bpy.data.collections.new(ID+'__'+name);asset.children.link(parts[name])
root=bpy.data.objects.new(ID+'__root',None);asset.objects.link(root)
root.empty_display_type='PLAIN_AXES';root.empty_display_size=.08
root['asset_id']=ID;root['asset_version']=VERSION;root['interface']='olympic_barbell_load@0.1.0';root['nominal_mass_kg']=20.0
asset.asset_mark();asset.asset_data.description='20 kg Olympic barbell; silver illustrated review prototype, 2200 mm / 28 mm / 50 mm sleeves. See SPEC.md.'
for tag in ['168Hours Fitness','equipment','barbell','20_kg','review_prototype']:asset.asset_data.tags.new(tag)

def linear(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mats=[]
for i,color in enumerate(PALETTE):
    mat=bpy.data.materials.new(ID+'__material_'+('steel_value_'+str(i) if i<7 else 'grip_mark'))
    rgb=tuple(linear(int(color[j:j+2],16)/255) for j in [0,2,4])
    mat.diffuse_color=(*rgb,1);mat.use_nodes=True
    node=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value=(*rgb,1);node.inputs['Metallic'].default_value=.85;node.inputs['Roughness'].default_value=.28
    mats.append(mat)

def mesh_obj(name,verts,faces,parent,origin):
    mesh=bpy.data.meshes.new(ID+'__data_'+name)
    mesh.from_pydata(verts,[],faces);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    o=bpy.data.objects.new(ID+'__mesh_'+name,mesh);parts['geo'].objects.link(o);o.parent=parent;o.location=origin
    for mat in mats:mesh.materials.append(mat)
    for poly in mesh.polygons:
        c=poly.center;n=poly.normal;theta=math.atan2(c.z,c.y)
        light=.35+.30*(math.sin(theta)+1)/2+.24*math.exp(-(((theta-.35+math.pi)%(2*math.pi)-math.pi)/.20)**2)
        light-=min(.12,abs(n.x)*.10)
        poly.material_index=max(0,min(6,round((light-.35)/.55*6)))
        poly.use_smooth=True
    return o

# Continuous surface, crossed diagonal cut grooves inside the 28 mm envelope.
N=192;waves=48;pitch=2*math.pi*.014/waves;step=pitch/4
rings={-1.094,1.094,-.655,.655,-.210,.210,-.060,.060,-.460,-.455,.455,.460}
for lo,hi in [(-.655,-.460),(-.455,-.210),(-.060,.060),(.210,.455),(.460,.655)]:
    count=math.ceil((hi-lo)/step)
    rings.update(lo+(hi-lo)*i/count for i in range(count+1))
rings=sorted(rings)
verts=[]
def tri(t):return 1-abs((t/math.pi)%2-1)
for x in rings:
    knurled=(abs(x)<.060 or .210<abs(x)<.655) and not (.455<=abs(x)<=.460)
    fade=min(1,max(0,(.655-abs(x))/.001),max(0,(abs(x)-.210)/.001)) if abs(x)>.060 else min(1,max(0,(.060-abs(x))/.001))
    for j in range(N):
        theta=2*math.pi*j/N
        radius=.014
        if knurled:radius-=.000160*fade*(1-min(tri(waves*theta+2*math.pi*x/pitch),tri(waves*theta-2*math.pi*x/pitch)))
        if .455<abs(x)<.460:radius-=.00004
        verts.append((x,radius*math.cos(theta),radius*math.sin(theta)))
faces=[]
for i in range(len(rings)-1):
    for j in range(N):
        k=(j+1)%N;faces.append((i*N+j,(i+1)*N+j,(i+1)*N+k,i*N+k))
faces+=[tuple(reversed(range(N))),tuple((len(rings)-1)*N+j for j in range(N))]
shaft=mesh_obj('shaft',verts,faces,root,(0,0,HEIGHT))
shaft['knurl_type']='actual crossed diamond cut geometry';shaft['knurl_pitch_m']=pitch;shaft['knurl_radial_depth_m']=.000160
for p in shaft.data.polygons:
    x=abs(p.center.x)
    if .455<=x<=.460:p.material_index=7
    elif x<.060 or .210<x<.655:
        # Controlled facet values reveal the real diamond cuts under flat rendering.
        if p.normal.x>.035:p.material_index=max(0,p.material_index-1)
        elif p.normal.x<-.035:p.material_index=min(6,p.material_index+1)
    p.use_smooth=abs(p.normal.x)<.999

# One shared positive-X sleeve mesh, mirrored via a proper 180 degree Z rotation.
# Flange is part of sleeve, NOT a removable plate-retaining collar.
pivot=.670
profile=[(.655,.0143),(.655,.0355),(.656,.0365),(.6835,.0365),(.685,.035),(.685,.026),(.686,.025),(.690,.025)]
for i in range(80):
    x=.695+i*.005
    if x+.0008<1.096:profile.extend([(x-.0004,.025),(x,.02492),(x+.0004,.025)])
profile.extend([(1.0985,.025),(1.100,.0235),(1.100,.0225),(1.095,.0225),(1.095,.0143)])
verts=[(x-pivot,r*math.cos(2*math.pi*j/N),r*math.sin(2*math.pi*j/N)) for x,r in profile for j in range(N)]
faces=[(i*N+j,((i+1)%len(profile))*N+j,((i+1)%len(profile))*N+(j+1)%N,i*N+(j+1)%N) for i in range(len(profile)) for j in range(N)]
controls={};sleeves={}
for side,sign in [('l',1),('r',-1)]:
    control=bpy.data.objects.new(ID+'__control_sleeve_'+side,None);parts['rig'].objects.link(control);control.parent=root;control.location=(sign*pivot,0,HEIGHT)
    control.empty_display_type='CIRCLE';control.empty_display_size=.05
    prop='sleeve_'+side+'_angle_deg';root[prop]=0.0
    root.id_properties_ui(prop).update(description='Independent sleeve rotation about global +X in degrees; periodic',default=0.0)
    root.property_overridable_library_set('["'+prop+'"]',True)
    driver=control.driver_add('rotation_euler',0).driver
    var=driver.variables.new();var.name='angle';var.type='SINGLE_PROP';var.targets[0].id=root;var.targets[0].data_path='["'+prop+'"]'
    driver.expression='angle*pi/180'
    controls[side]=control
    if side=='l':o=mesh_obj('sleeve_l',verts,faces,control,(0,0,0))
    else:
        o=bpy.data.objects.new(ID+'__mesh_sleeve_r',sleeves['l'].data);parts['geo'].objects.link(o);o.parent=control;o.rotation_euler.z=math.pi
    sleeves[side]=o
# Unbranded recessed caps: no textual logo and no detached collars.
cap_profile=[(1.0966,0),(1.0966,.0221),(1.097,.0223),(1.099,.0223),(1.0994,.0218),(1.0994,0)]
# Use triangle fans at axis poles to avoid duplicate/degenerate pole vertices.
def solid_lathe(profile):
    v=[];loops=[];f=[]
    for x,r in profile:
        if r==0:loops.append([len(v)]);v.append((x-pivot,0,0))
        else:
            loops.append(list(range(len(v),len(v)+N)));v.extend((x-pivot,r*math.cos(2*math.pi*j/N),r*math.sin(2*math.pi*j/N)) for j in range(N))
    for a,b in zip(loops,loops[1:]):
        for j in range(N):
            k=(j+1)%N
            if len(a)==1:f.append((a[0],b[j],b[k]))
            elif len(b)==1:f.append((a[j],b[0],a[k]))
            else:f.append((a[j],b[j],b[k],a[k]))
    return v,f
v,f=solid_lathe(cap_profile)
cap=mesh_obj('end_cap_l',v,f,controls['l'],(0,0,0))
cap2=bpy.data.objects.new(ID+'__mesh_end_cap_r',cap.data);parts['geo'].objects.link(cap2);cap2.parent=controls['r'];cap2.rotation_euler.z=math.pi
for obj in [sleeves['l'],cap]:
    for poly in obj.data.polygons:
        if abs(poly.normal.x)>.8:poly.material_index=3;poly.use_smooth=False

anchors={}
positions={'grip_center':(0,0,HEIGHT),'grip_l':(.350,0,HEIGHT),'grip_r':(-.350,0,HEIGHT),'axis_center':(0,0,HEIGHT),'floor_contact':(0,0,0)}
for side,sign in [('l',1),('r',-1)]:
    positions['load_'+side]=(sign*.685,0,HEIGHT);positions['sleeve_end_'+side]=(sign*1.1,0,HEIGHT)
for key,pos in positions.items():
    o=bpy.data.objects.new(ID+'__anchor_'+key,None);parts['anchors'].objects.link(o)
    moving=key.startswith('load_') or key.startswith('sleeve_end_')
    side=key[-1] if moving else None;o.parent=controls[side] if moving else root
    o.location=Vector(pos)-(o.parent.location if moving else Vector((0,0,0)))
    if moving:o.rotation_euler.z=-math.pi/2 if side=='l' else math.pi/2
    elif key=='axis_center':o.rotation_euler.z=-math.pi/2
    o.empty_display_type='ARROWS';o.empty_display_size=.035;o['logical_anchor']=key
bpy.context.view_layer.update()
for key in positions:
    o=bpy.data.objects[ID+'__anchor_'+key]
    anchors[key]={'object':o.name,'position_m':list(o.matrix_world.translation),'rotation_euler_xyz_radians':list(o.matrix_world.to_euler()),'forward':('+X' if key.endswith('_l') else '-X') if key.startswith(('load_','sleeve_end_')) else ('+X' if key=='axis_center' else '+Y'),'up':'+Z','moves_with':o.parent.name}
viewport();bpy.context.view_layer.objects.active=root;root.select_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,check_existing=False)
source_hash=digest(SOURCE)
views=add_views(scene)
settings={'status':'asset-local provisional review preset; user design acceptance pending','preset':PRESET,'blender_version':bpy.app.version_string,'blender_build_hash':bpy.app.build_hash.decode(),'addons_required':[],'engine':'BLENDER_WORKBENCH','source_sha256':source_hash,'resolution':[1600,1000],'format':'PNG','color_mode':'RGBA','bit_depth':8,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'palette_srgb_hex':PALETTE,'metallic':.85,'roughness':.28,'material_interpretation':'Workbench flat material swatches; radial geometric face bands simulate restrained steel shading; Principled parameters stored but not rendered','lighting':'FLAT; no lights','shadows':False,'ambient_occlusion':False,'cavity':False,'baked_textures':[],'specular_highlight':False,'outlines':{'method':'native Workbench object silhouette','enabled':True,'width':'native at 1600x1000; no exposed pixel-width control','color_linear_rgb':[.015,.018,.022]},'background':{'linear_rgb':[1,1,1],'transparent':False},'antialiasing_samples':'32','random_seed':'N/A deterministic Workbench','camera_views':views,'builder':'scripts/blender/build_olympic_barbell_20kg.py','builder_sha256':digest(__file__),'helpers_sha256':digest(Path(__file__).with_name('barbell_20kg_common.py'))}
write_json(ASSET/'previews/render-settings.json',settings)
m=read_json(ASSET/'asset.json')
m.update(status='review',blender_version=bpy.app.version_string,anchors=anchors,source_revision_or_digest='sha256:'+source_hash,
 physical_properties={'nominal_mass_kg':20,'mass_simulation_validated':False,'overall_length_m':2.2,'shaft_diameter_m':.028,'exposed_shaft_length_m':1.31,'sleeve_diameter_max_m':.05,'loadable_sleeve_length_m':.415,'flange_width_m':.030,'flange_diameter_m':.073,'knurl_pitch_m':pitch,'knurl_radial_recess_m':.000160},
 components={'shaft':shaft.name,'sleeves':[ID+'__mesh_sleeve_'+s for s in ['l','r']],'end_caps':[ID+'__mesh_end_cap_'+s for s in ['l','r']],'controls':[ID+'__control_sleeve_'+s for s in ['l','r']],'bilateral_shared_mesh_data':True},
 material_slots={str(i):{'material':mat.name,'semantic_role':'equipment_frame' if i<7 else 'equipment_grip','srgb_hex':PALETTE[i]} for i,mat in enumerate(mats)},
 reference_renders=[{'view':view,'configuration':entry['configuration'],'path':entry['path'],'source_revision_or_digest':'sha256:'+source_hash,'preset_revision':settings['builder_sha256']} for view,entry in views.items()])
m['standards']['style_preset_revision']=settings['builder_sha256'];write_json(ASSET/'asset.json',m)
write_json(ASSET/'build-record.json',{'version':VERSION,'source_sha256':source_hash,'prebuild_specification_sha256':prebuild,'builder_sha256':settings['builder_sha256'],'helpers_sha256':settings['helpers_sha256'],'plate_source_sha256':verify_plate()['source']['sha256'],'prebuild_specification_defined':True,'original_geometry':True})
scene,bar,plate=make_fixture()
assembly_views=add_views(scene,assembled=True)
viewport((0,0,.225),2.8)
scene.camera=bpy.data.objects[SID+'__camera_assembled_with_plates']
bpy.ops.wm.save_as_mainfile(filepath=str(TEST_SOURCE),compress=True,check_existing=False)
fixture_hash=digest(TEST_SOURCE)
# Acceptance images must come from the serialized, reopened fixture.
# Library-instance transforms can round at save/load; do not compare a
# pre-save render to a post-save validation render.
bpy.ops.wm.open_mainfile(filepath=str(TEST_SOURCE))
scene=bpy.context.scene
for view,entry in assembly_views.items():
    cam=camera(scene,'post_save_reference',entry['position_m'],entry['target_m'],entry['ortho_scale_m'])
    cam.rotation_euler=entry['rotation_euler_xyz_radians'];cam.data.clip_start=entry['clip_start_m'];cam.data.clip_end=entry['clip_end_m']
    scene.camera=cam;scene.render.filepath=str(REPO/entry['path']);bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam,do_unlink=True)
fixture_settings=dict(settings);fixture_settings.update(source_sha256=fixture_hash,camera_views=assembly_views,dependencies=[{'path':str(SOURCE.relative_to(REPO)),'sha256':source_hash},{'path':str((PLATE/(PID+'.blend')).relative_to(REPO)),'sha256':verify_plate()['source']['sha256']}])
write_json(FIXTURE/'previews/render-settings.json',fixture_settings)
fm=read_json(FIXTURE/'asset.json');fm.update(status='review',blender_version=bpy.app.version_string,source_revision_or_digest='sha256:'+fixture_hash,reference_renders=list(assembly_views.values()),render_settings=str((FIXTURE/'previews/render-settings.json').relative_to(REPO)),local_mesh_objects=0,instance_names=['barbell_primary','plate_l','plate_r'],units='meters',axes={'up':'+Z','forward':'+Y','subject_left':'+X'})
fm['dependencies'][0]['sha256']=source_hash;write_json(FIXTURE/'asset.json',fm)
m=read_json(ASSET/'asset.json');m['reference_renders'] += [{'view':'assembled_with_plates','configuration':'two_45lb_plates','path':assembly_views['assembled_with_plates']['path'],'source_revision_or_digest':'sha256:'+fixture_hash,'preset_revision':settings['builder_sha256']}];write_json(ASSET/'asset.json',m)
verify_plate()
print('BARBELL_BUILD_COMPLETE',source_hash,fixture_hash)
