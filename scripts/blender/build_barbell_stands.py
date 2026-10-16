"""Original independent stands review prototype. MIT code; artwork separate."""
from pathlib import Path
import bpy,bmesh,sys,json,math
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import setup,camera,digest,write_json
R=Path(__file__).resolve().parents[2];ID='168h_equipment_barbell_stands';A=R/'assets/equipment/racks'/ID;SOURCE=A/(ID+'.blend')

def linear(h):
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in [int(h[i:i+2],16)/255 for i in (0,2,4)])+(1,)
def material(role,h):
    m=bpy.data.materials.new(ID+'__material_'+role);m.diffuse_color=linear(h);m.use_nodes=True
    n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');n.inputs['Base Color'].default_value=m.diffuse_color;n.inputs['Roughness'].default_value=1;n.inputs['Metallic'].default_value=0;m['srgb_hex']=h;m['semantic_role']='equipment_grip' if role.startswith('grip') else 'equipment_frame';return m

def active(o):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o

def finish(o,part,parent,group='steel',bevel=.001):
    o.name=ID+'__mesh_'+part+'_l';o.data.name=ID+'__geometry_'+part
    for c in list(o.users_collection):c.objects.unlink(o)
    geo.objects.link(o);o.parent=parent
    if bevel:
        active(o);m=o.modifiers.new('physical_edge_rounding','BEVEL');m.width=bevel;m.segments=4
        bpy.ops.object.modifier_apply(modifier=m.name)
    o.data.materials.clear()
    for m in mats[group]:o.data.materials.append(m)
    for p in o.data.polygons:p.material_index=1 if p.normal.z>.4 else 2 if abs(p.normal.x)>.5 else 0
    return o

def cube(dims,loc):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o

def box(part,dims,loc,parent,group='steel',bevel=.001):return finish(cube(dims,loc),part,parent,group,bevel)

def cut(o,cutter):
    active(o);m=o.modifiers.new('machined_opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)

def cylinder(radius,length,loc,axis='X',verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=length,location=loc);o=bpy.context.object
    o.rotation_euler=(0,math.pi/2,0) if axis=='X' else (math.pi/2,0,0) if axis=='Y' else (0,0,0)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return o

def tube(part,width,depth,z0,z1,wall,parent,holes):
    o=cube((width,depth,z1-z0),(0,0,(z0+z1)/2));cut(o,cube((width-2*wall,depth-2*wall,z1-z0+.02),(0,0,(z0+z1)/2)))
    for z in holes:cut(o,cylinder(.0085,width+.02,(0,0,z)))
    # Exact Boolean may leave isolated tiny boundary gaps at coplanar hole seams.
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
    return finish(o,part,parent,bevel=0 if len(holes)>1 else .0007)

def gusset(part,x,parent):
    verts=[(x+s*.003,y,z) for s in [-1,1] for y,z in [(-.19,.07),(.19,.07),(0,.29)]]
    mesh=bpy.data.meshes.new(part);mesh.from_pydata(verts,[],[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]);mesh.update()
    o=bpy.data.objects.new(part,mesh);bpy.context.scene.collection.objects.link(o);return finish(o,part,parent,bevel=.0015)

def empty(name,parent,col,location=(0,0,0)):
    o=bpy.data.objects.new(ID+'__'+name,None);col.objects.link(o);o.parent=parent;o.location=location;o.empty_display_size=.04;o.empty_display_type='ARROWS';return o

def driver(obj,property,side):
    d=obj.driver_add('location',2).driver;d.expression='index * 0.05';v=d.variables.new();v.name='index';v.targets[0].id=root;v.targets[0].data_path='["height_index_'+side+'"]'

if __name__=='__main__':
    assert not SOURCE.exists(),'Never overwrite an existing approved/review source through initial builder'
    meta=json.loads((A/'asset.json').read_text());pre={n:digest(A/n) for n in ['SPEC.md','asset.json','validation.md']}
    bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.name=ID+'__review';setup(scene)
    col=bpy.data.collections.new(ID);scene.collection.children.link(col);geo=bpy.data.collections.new(ID+'__geo');anc=bpy.data.collections.new(ID+'__anchors');col.children.link(geo);col.children.link(anc)
    root=empty('root',None,anc);root['asset_id']=ID;root['asset_version']='0.1.0';root['review_status']='review_prototype'
    for s in ['l','r']:
        root['height_index_'+s]=0;root.id_properties_ui('height_index_'+s).update(min=0,max=15,description='Discrete50mm telescoping extension; match both sides when supporting a bar')
    mats={'steel':[material('frame_'+n,h) for n,h in [('body','363A40'),('top','454A51'),('side','2A2D32')]],'grip':[material('grip_'+n,h) for n,h in [('body','17191D'),('top','24272C'),('side','17191D')]],'hardware':[material('hardware_'+n,h) for n,h in [('body','6D747E'),('top','8C949F'),('side','454A51')]]}
    fixed=empty('control_stand_l',root,anc,(.55,0,0));upper=empty('control_upper_l',fixed,anc);driver(upper,'height_index_l','l')
    rails=[]
    for s,x in [('outer',.25345),('inner',-.25345)]:
        rails.append(box('base_rail_'+s,(.06,.6023,.06),(x,0,.04),fixed,bevel=.002))
        for e,y in [('front',.26115),('rear',-.26115)]:box('rubber_'+s+'_'+e,(.09,.10,.01),(x,y,.005),fixed,'grip',.002)
        box('rail_cap_'+s+'_front',(.062,.012,.062),(x,.30115,.04),fixed,'grip',.002)
        box('rail_cap_'+s+'_rear',(.062,.012,.062),(x,-.30115,.04),fixed,'grip',.002)
    box('base_tie',(.5669,.08,.06),(0,0,.04),fixed,bevel=.002)
    tube('upright_outer',.08,.08,.07,.97,.004,fixed,[.90])
    tube('upright_inner',.06,.06,.078,1.028,.003,upper,[.15+.05*i for i in range(16)])
    # Short guide ring bridges the nominal telescope gap, without intersecting inner tube.
    o=cube((.086,.086,.022),(0,0,.959));cut(o,cube((.061,.061,.05),(0,0,.959)));finish(o,'polymer_guide',fixed,'grip',.0007)
    box('inner_top_cap',(.061,.061,.006),(0,0,1.025),upper,'grip',.0015)
    for side,x in [('a',-.045),('b',.045)]:
        gusset('base_gusset_'+side,x,fixed)
        for z in [.12,.215]:finish(cylinder(.012,.009,(x+(-.008 if x<0 else .008),0,z),verts=6),'gusset_bolt_'+side+'_'+str(int(z*1000)),fixed,'hardware',.0006)
    finish(cylinder(.0079375,.14,(0,0,.90)),'adjustment_pin',fixed,'hardware',.0005)
    finish(cylinder(.016,.014,(.077,0,.90)),'pin_washer',fixed,'hardware',.0007)
    box('pin_grip',(.027,.03,.04),(.097,0,.90),fixed,'grip',.004)
    bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=12,location=(-.072,0,.90),major_radius=.014,minor_radius=.0015,rotation=(0,math.pi/2,0));o=bpy.context.object;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);finish(o,'pin_retainer',fixed,'hardware',0)
    box('hook_back',(.06,.012,.15),(0,.048,.973),upper,bevel=.002)
    box('hook_shelf',(.06,.16,.01),(0,.134,.917),upper,bevel=.0015)
    box('hook_lip',(.06,.012,.054),(0,.208,.944),upper,bevel=.002)
    box('hook_liner',(.058,.132,.006),(0,.139,.925),upper,'grip',.0004)
    box('hook_back_liner',(.058,.006,.099),(0,.057,.9775),upper,'grip',.001)
    box('hook_lip_liner',(.058,.006,.039),(0,.199,.9475),upper,'grip',.001)
    finish(cylinder(.006,.074,(0,.048,.994),verts=48),'hook_fastener',upper,'hardware',.0005)
    # Opposite stand: independent control hierarchy, original mesh datablocks shared.
    fixed_r=empty('control_stand_r',root,anc,(-.55,0,0));upper_r=empty('control_upper_r',fixed_r,anc);driver(upper_r,'height_index_r','r')
    originals=[o for o in col.all_objects if o.type=='MESH']
    for o in originals:
        n=bpy.data.objects.new(o.name[:-1]+'r',o.data);geo.objects.link(n);n.parent=upper_r if o.parent==upper else fixed_r;n.matrix_basis=o.matrix_basis.copy()
    for key,e in meta['anchors'].items():
        side=key[-1];parent=root if key=='floor_contact' else (upper if side=='l' else upper_r) if key.startswith('bar_') else (fixed if side=='l' else fixed_r)
        p=e['position_m'].copy()
        if parent!=root:p[0]-=.55 if side=='l' else -.55
        empty('anchor_'+key,parent,anc,p)
    bpy.context.view_layer.update()
    meta['origin_contract']['component_frames']={o.name:{'root_local_position_m':list(o.matrix_world.translation),'purpose':'Intentional component construction frame at canonical index0; upper parts follow declared height controller'} for o in col.all_objects if o.type=='MESH'}
    meta['components']={'mesh_objects':len(originals)*2,'unique_mesh_data':len({o.data for o in col.all_objects if o.type=='MESH'}),'controllers':{s:ID+'__control_stand_'+s for s in ['l','r']},'upper_controllers':{s:ID+'__control_upper_'+s for s in ['l','r']},'reuse':'Every opposite-stand mesh shares corresponding left mesh data; no negative scale'}
    col.asset_mark();col.asset_data.author='168Hours Fitness';col.asset_data.description='Independent telescoping barbell stands pair — review prototype';col.asset_data.tags.new('review_prototype');col.asset_data.tags.new('stands')
    cam=camera(scene,ID+'__camera_three_quarter',(3.3,4.4,2.8),(0,0,.55),2.85);scene.camera=cam
    for o in col.all_objects:
        if o.type=='EMPTY':o.hide_set(True)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                sp=area.spaces.active;sp.shading.light='FLAT';sp.shading.color_type='MATERIAL';sp.shading.show_shadows=False;sp.shading.show_cavity=False;sp.shading.show_specular_highlight=False;sp.shading.show_object_outline=True;sp.region_3d.view_distance=3.2;sp.region_3d.view_location=(0,0,.55);sp.region_3d.view_rotation=cam.rotation_euler.to_quaternion();sp.region_3d.view_perspective='ORTHO'
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True)
    meta['material_slots']={'equipment_frame':[m.name for family in ['steel','hardware'] for m in mats[family]],'equipment_grip':[m.name for m in mats['grip']]}
    meta['source_revision_or_digest']='sha256:'+digest(SOURCE);write_json(A/'asset.json',meta)
    write_json(A/'build-record.json',{'prebuild_document_sha256':pre,'source_sha256':digest(SOURCE),'builder_sha256':digest(Path(__file__)),'blender_version':bpy.app.version_string,'components':meta['components']})
    print('STANDS_BUILD',meta['components'])
