"""Build only the user-authorized standalone bench prototype. Code: MIT; artwork separate."""
from pathlib import Path
import bpy, json, math, sys
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from barbell_20kg_common import setup, camera, digest, write_json

REPO = Path(__file__).resolve().parents[2]
ID = '168h_equipment_flat_bench'
ASSET = REPO/'assets/equipment/benches'/ID
SOURCE = ASSET/(ID+'.blend')

def linear(hexcolor):
    values=[int(hexcolor[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values)+(1,)

def material(role, color):
    m=bpy.data.materials.new(ID+'__material_'+role)
    m.diffuse_color=linear(color); m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=m.diffuse_color
    bsdf.inputs['Roughness'].default_value=1;bsdf.inputs['Metallic'].default_value=0
    m['semantic_role']={'padding':'equipment_padding','frame':'equipment_frame','grip':'equipment_grip','substrate':'equipment_frame'}[role.split('_')[0]]; m['srgb_hex']=color
    return m

def rounded_pad():
    # True rounded footprint plus quarter-circle vertical edge roll, not a bevel shading trick.
    rings=[]
    for step in range(9):
        t=step*math.pi/16
        rings.append((.3937+.006*(1-math.cos(t)), .006*(1-math.sin(t))))
    rings.append((.4512,0))
    for step in range(1,9):
        t=step*math.pi/16
        rings.append((.4512+.006*math.sin(t),.006*(1-math.cos(t))))
    verts=[];n=64
    for z,inset in rings:
        w=.3048/2-inset;l=1.1938/2-inset;r=.022-inset
        for cx,cy,start in [(w-r,l-r,0),(-w+r,l-r,90),(-w+r,-l+r,180),(w-r,-l+r,270)]:
            for k in range(16):
                theta=math.radians(start+k*90/15)
                verts.append((cx+r*math.cos(theta),cy+r*math.sin(theta),z))
    faces=[tuple(reversed(range(n)))]
    for row in range(len(rings)-1):
        for k in range(n):
            j=(k+1)%n;faces.append((row*n+k,row*n+j,(row+1)*n+j,(row+1)*n+k))
    faces.append(tuple((len(rings)-1)*n+k for k in range(n)))
    mesh=bpy.data.meshes.new(ID+'__geometry_pad');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(ID+'__mesh_pad',mesh);geo.objects.link(obj);obj.parent=root
    for mat in mats['padding']:mesh.materials.append(mat)
    for p in mesh.polygons:
        p.material_index=0 if p.normal.z>.98 else 2 if abs(p.normal.z)>.12 else 1
    return obj

def box(part, dims, location, group='frame', bevel=.002, reuse=None):
    if reuse:
        obj=bpy.data.objects.new(ID+'__mesh_'+part,reuse.data);geo.objects.link(obj)
    else:
        bpy.ops.mesh.primitive_cube_add(size=1)
        obj=bpy.context.object;obj.name=ID+'__mesh_'+part
        for col in list(obj.users_collection):col.objects.unlink(obj)
        geo.objects.link(obj);obj.dimensions=dims
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        mod=obj.modifiers.new('physical_edge_rounding','BEVEL');mod.width=bevel;mod.segments=6
        bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.data.name=ID+'__geometry_'+part
        for mat in mats[group]:obj.data.materials.append(mat)
        for p in obj.data.polygons:
            p.material_index=1 if p.normal.z>.5 else 2 if abs(p.normal.x)>.5 else 0
    obj.location=location;obj.parent=root;return obj

def leg(part, sign):
    # Sloped support with horizontal cut ends, seated into the foot/spine joints.
    verts=[]
    for z,offset in [(-.159,sign*.05),(.159,-sign*.05)]:
        for x,y in [(-.0254,-.0381),(.0254,-.0381),(.0254,.0381),(-.0254,.0381)]:
            verts.append((x,y+offset,z))
    mesh=bpy.data.meshes.new(ID+'__geometry_'+part)
    mesh.from_pydata(verts,[],[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.update()
    o=bpy.data.objects.new(ID+'__mesh_'+part,mesh);geo.objects.link(o);o.parent=root;o.location=(0,sign*.42,.209)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    mod=o.modifiers.new('physical_edge_rounding','BEVEL');mod.width=.002;mod.segments=6
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for mat in mats['frame']:mesh.materials.append(mat)
    for p in mesh.polygons:p.material_index=1 if p.normal.z>.5 else 2 if abs(p.normal.x)>.5 else 0
    return o

if __name__=='__main__':
    assert (ASSET/'SPEC.md').is_file() and (ASSET/'asset.json').is_file()
    prebuild={p:digest(ASSET/p) for p in ['SPEC.md','asset.json','validation.md']}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene;scene.name=ID+'__review';setup(scene)
    col=bpy.data.collections.new(ID);scene.collection.children.link(col)
    geo=bpy.data.collections.new(ID+'__geo');col.children.link(geo)
    anc=bpy.data.collections.new(ID+'__anchors');col.children.link(anc)
    root=bpy.data.objects.new(ID+'__root',None);anc.objects.link(root)
    root['asset_id']=ID;root['asset_version']='0.1.0';root['review_status']='review_prototype'
    root['interface']='bench_support@0.1.0';root.empty_display_size=.05
    mats={k:[material(role,c) for role,c in colors] for k,colors in {
      'padding':[('padding_top','25282D'),('padding_side','1C1F24'),('padding_edge','30343A')],
      'frame':[('frame_body','363A40'),('frame_top','454A51'),('frame_side','2A2D32')],
      'grip':[('grip_body','17191D'),('grip_top','24272C'),('grip_side','17191D')],
      'substrate':[('substrate_body','202328'),('substrate_top','202328'),('substrate_side','202328')]
    }.items()}
    rounded_pad()
    box('pad_substrate',(.2808,1.1698,.0127),(0,0,.38735),'substrate',.003)
    box('spine',(.0508,1.0,.0508),(0,0,.3556))
    rail=box('mount_rail_head',(.24,.0508,.0254),(0,.34,.3683))
    box('mount_rail_foot',None,(0,-.34,.3683),reuse=rail)
    leg('leg_head',1);leg('leg_foot',-1)
    foot=box('foot_head',(.3356,.0762,.0508),(0,.47,.0354))
    box('foot_foot',None,(0,-.47,.0354),reuse=foot)
    boot=None
    for end,y in [('head',.47),('foot',-.47)]:
        for side,x in [('l',.14),('r',-.14)]:
            o=box('rubber_'+end+'_'+side,(.0756,.085,.065),(x,y,.0325),'grip',.003,reuse=boot)
            if boot is None:boot=o
    manifest=json.loads((ASSET/'asset.json').read_text())
    for key,entry in manifest['anchors'].items():
        o=bpy.data.objects.new(entry['object'],None);anc.objects.link(o);o.parent=root
        o.location=entry['position_m'];o.empty_display_type='ARROWS';o.empty_display_size=.035;o.show_in_front=True
    col.asset_mark();col.asset_data.description='Standalone flat utility bench — 168Hours review prototype, not approved production.'
    col.asset_data.author='168Hours Fitness';col.asset_data.tags.new('bench');col.asset_data.tags.new('review_prototype')
    cam=camera(scene,ID+'__camera_three_quarter',(1.8,2.8,1.6),(0,0,.25),1.55);scene.camera=cam
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:
        if o.type=='EMPTY':o.hide_set(True)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                s=area.spaces.active;s.shading.light='FLAT';s.shading.color_type='MATERIAL';s.shading.show_shadows=False;s.shading.show_cavity=False
                s.shading.show_specular_highlight=False;s.shading.show_object_outline=True;s.shading.background_type='WORLD'
                s.region_3d.view_distance=2;s.region_3d.view_location=(0,0,.25)
                s.region_3d.view_rotation=cam.rotation_euler.to_quaternion();s.region_3d.view_perspective='ORTHO'
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
    write_json(ASSET/'build-record.json',{'prebuild_document_sha256':prebuild,'blender_version':bpy.app.version_string,'source_sha256':digest(SOURCE),'builder_sha256':digest(Path(__file__)),'helper_sha256':digest(Path(__file__).with_name('barbell_20kg_common.py')),'component_counts':{'meshes':len([o for o in col.all_objects if o.type=='MESH']),'unique_mesh_data':len({o.data for o in col.all_objects if o.type=='MESH'})}})
    print('BENCH_BUILD_COMPLETE',digest(SOURCE))
