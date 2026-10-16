"""Original review mannequin builder. Never touches equipment or Human V1 definitions."""
from pathlib import Path
import bpy,sys,json,math
import numpy as np
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/blender'));sys.path.insert(0,str(R/'scripts/pipeline'))
from barbell_20kg_common import digest,write_json,setup,camera
from validate_human_contract import rest_fingerprint,read
ID='168h_human_anatomical_mannequin';A=R/'assets/humans/models'/ID;SOURCE=A/(ID+'.blend')
RID='168h_rig_mannequin_v1';RA=R/'assets/humans/rigs'/RID;RSOURCE=RA/(RID+'.blend')
SK=read(R/'docs/contracts/human-v1/skeleton.json');CAT=read(R/'docs/contracts/human-v1/muscles.json')

def col(name,parent=None):
    c=bpy.data.collections.new(name);(parent.children if parent else bpy.context.scene.collection.children).link(c);return c
def empty(name,collection,parent=None,position=(0,0,0)):
    o=bpy.data.objects.new(name,None);collection.objects.link(o);o.parent=parent;o.location=position;o.empty_display_size=.04;return o
def move(o,c):
    for old in list(o.users_collection):old.objects.unlink(o)
    c.objects.link(o)
def mesh(name,verts,faces,c):
    data=bpy.data.meshes.new(name+'__data');data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(name,data);c.objects.link(o);return o
def loft(name,sections,c,axis='z',sides=40):
    # Section: centerXYZ, elliptical radii in transverse plane.
    verts=[]
    for center,rx,ry in sections:
        for j in range(sides):
            t=2*math.pi*j/sides
            off=(rx*math.cos(t),ry*math.sin(t),0) if axis=='z' else (rx*math.cos(t),0,ry*math.sin(t))
            verts.append(tuple(Vector(center)+Vector(off)))
    faces=[]
    for i in range(len(sections)-1):
        for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces += [tuple(reversed(range(sides))),tuple((len(sections)-1)*sides+j for j in range(sides))]
    return mesh(name,verts,faces,c)
def tube(name,start,end,profiles,c,sides=32):
    a=Vector(start);b=Vector(end);u=(b-a).normalized();front=Vector((0,1,0));front=(front-u*front.dot(u)).normalized();radial=u.cross(front).normalized()
    verts=[]
    for t,rx,ry in profiles:
        center=a+(b-a)*t
        for j in range(sides):ang=j*2*math.pi/sides;verts.append(tuple(center+radial*(rx*math.cos(ang))+front*(ry*math.sin(ang))))
    faces=[]
    for i in range(len(profiles)-1):
        for j in range(sides):k=i*sides+j;l=i*sides+(j+1)%sides;faces.append((k,l,l+sides,k+sides))
    faces+=[tuple(reversed(range(sides))),tuple((len(profiles)-1)*sides+j for j in range(sides))]
    return mesh(name,verts,faces,c)
def coords():
    g={'root':((0,0,0),(0,0,.1))};z=[.94,1.035,1.17,1.31,1.43,1.535,1.70]
    for i,n in enumerate(['pelvis','spine_01','spine_02','spine_03','neck','head']):g[n]=((0,0,z[i]),(0,0,z[i+1]))
    for s,sign in [('l',1),('r',-1)]:
        g['clavicle_'+s]=((0,0,1.43),(.185*sign,0,1.43));u=Vector((sign,0,-1)).normalized();rad=Vector((sign,0,1)).normalized();start=Vector(g['clavicle_'+s][1])
        for n,length in [('upper_arm',.295),('forearm',.255),('hand',.095)]:end=start+u*length;g[n+'_'+s]=(tuple(start),tuple(end));start=end
        wrist=Vector(g['hand_'+s][0]);palmend=Vector(g['hand_'+s][1])
        for digit,offset,length in [('index',.030,.082),('middle',.007,.091),('ring',-.017,.083),('little',-.039,.064)]:
            start=palmend+rad*offset
            for i,fraction in enumerate([.45,.32,.23],1):end=start+u*length*fraction;g[f'{digit}_{i:02}_{s}']=(tuple(start),tuple(end));start=end
        start=wrist+u*.035+rad*.038;direction=Vector((sign,0,0))
        for i,length in enumerate([.033,.028,.025],1):end=start+direction*length;g[f'thumb_{i:02}_{s}']=(tuple(start),tuple(end));start=end
        g['thigh_'+s]=((sign*.10,0,.94),(sign*.10,0,.51));g['shin_'+s]=((sign*.10,0,.51),(sign*.10,0,.095));g['foot_'+s]=((sign*.10,0,.095),(sign*.10,.155,.035));g['toe_'+s]=((sign*.10,.155,.035),(sign*.10,.225,.035))
    return g
G=coords()
def make_bones(data,obj):
    bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for spec in SK['bones']:
        b=data.edit_bones.new(spec['name']);b.head,b.tail=G[b.name];b.use_deform=spec['deform']
        if spec['parent']:b.parent=data.edit_bones[spec['parent']];b.use_connect=spec['connected']
        u=(b.tail-b.head).normalized();z=Vector((0,1,0))-u*u.y
        if z.length<1e-6:z=Vector((0,0,1))-u*u.z
        b.align_roll(z.normalized())
    bpy.ops.object.mode_set(mode='OBJECT');obj.select_set(False)
def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.8
    return m
def weight(o):
    xyz=np.array([v.co[:] for v in o.data.vertices]);names=[b['name'] for b in SK['bones'] if b['deform']];ds=[]
    for name in names:
        a,b=np.array(G[name][0]),np.array(G[name][1]);v=b-a;t=np.clip(((xyz-a)@v)/(v@v),0,1);ds.append(np.sum((xyz-(a+t[:,None]*v))**2,axis=1))
    dist=np.array(ds).T;winner=np.argmin(dist,axis=1)
    # Narrow finger falloff prevents neighbor fingers pulling each other.
    sigma=np.where(np.char.startswith(np.array(names)[winner],'thumb')|np.char.startswith(np.array(names)[winner],'index')|np.char.startswith(np.array(names)[winner],'middle')|np.char.startswith(np.array(names)[winner],'ring')|np.char.startswith(np.array(names)[winner],'little'),.008,.045)
    near=np.argsort(dist,axis=1)[:,:4];d=np.take_along_axis(dist,near,axis=1);w=np.exp(-(d-d[:,0,None])/(sigma[:,None]**2));w/=w.sum(axis=1)[:,None]
    groups=[o.vertex_groups.new(name=n) for n in names]
    for i in range(len(xyz)):
        for k in range(4):
            if w[i,k]>.00001:groups[int(near[i,k])].add([i],float(w[i,k]),'REPLACE')
    # Normalize after dropping insignificant influences.
    for v in o.data.vertices:
        total=sum(x.weight for x in v.groups)
        for x in v.groups:o.vertex_groups[x.group].add([v.index],x.weight/total,'REPLACE')
def attr(o,name,values,group=True):
    a=o.data.attributes.new(name,'FLOAT','POINT');a.data.foreach_set('value',np.asarray(values,dtype=np.float32))
    if group:
        g=o.vertex_groups.get(name) or o.vertex_groups.new(name=name)
        for i in np.flatnonzero(values>1e-4):g.add([int(i)],float(values[i]),'REPLACE')
def drive(socket,owner,key):
    d=socket.driver_add('default_value').driver;d.type='SCRIPTED';v=d.variables.new();v.name='value';v.targets[0].id=owner;v.targets[0].data_path='["'+key+'"]';d.expression='value'
def color_nodes(o,root,muscle_ids,cut=False):
    color=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT');o.data.color_attributes.active_color=color
    group=bpy.data.node_groups.new(o.name+'__illustration','GeometryNodeTree');group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    nodes=group.nodes;links=group.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');geo=inp.outputs['Geometry']
    normal=nodes.new('GeometryNodeInputNormal');dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(.28,.72,.62);links.new(normal.outputs['Normal'],dot.inputs[0]);shade=nodes.new('ShaderNodeMath');shade.operation='MULTIPLY_ADD';shade.inputs[1].default_value=.18;shade.inputs[2].default_value=.62;links.new(dot.outputs['Value'],shade.inputs[0])
    base=nodes.new('ShaderNodeMixRGB');base.blend_type='MIX';base.inputs[1].default_value=(.22,.255,.28,1);base.inputs[2].default_value=(.62,.66,.68,1);links.new(shade.outputs[0],base.inputs[0]);current=base.outputs[0]
    for mid in muscle_ids:
        mask=nodes.new('GeometryNodeInputNamedAttribute');mask.data_type='FLOAT';mask.inputs['Name'].default_value=mid
        for role,target in [('secondary',(.85,.48,.19,1)),('primary',(.66,.20,.17,1))]:
            val=nodes.new('ShaderNodeValue');drive(val.outputs[0],root,'highlight_'+role+'__'+mid)
            mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(mask.outputs['Attribute'],mul.inputs[0]);links.new(val.outputs[0],mul.inputs[1])
            mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=target;links.new(mul.outputs[0],mix.inputs[0]);links.new(current,mix.inputs[1]);current=mix.outputs[0]
    store=nodes.new('GeometryNodeStoreNamedAttribute');store.data_type='FLOAT_COLOR';store.domain='POINT';store.inputs['Name'].default_value='Color';links.new(geo,store.inputs['Geometry']);links.new(current,store.inputs['Value']);geo=store.outputs['Geometry']
    if cut:
        field=nodes.new('GeometryNodeInputNamedAttribute');field.data_type='FLOAT';field.inputs['Name'].default_value='xray_window'
        threshold=nodes.new('ShaderNodeMath');threshold.operation='GREATER_THAN';threshold.inputs[1].default_value=.5;links.new(field.outputs['Attribute'],threshold.inputs[0])
        value=nodes.new('ShaderNodeValue');drive(value.outputs[0],root,'xray_enabled')
        mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';links.new(threshold.outputs[0],mul.inputs[0]);links.new(value.outputs[0],mul.inputs[1]);delete=nodes.new('GeometryNodeDeleteGeometry');delete.domain='FACE';links.new(geo,delete.inputs['Geometry']);links.new(mul.outputs[0],delete.inputs['Selection']);geo=delete.outputs['Geometry']
    links.new(geo,out.inputs['Geometry']);mod=o.modifiers.new('illustration_and_highlights','NODES');mod.node_group=group

def build():
    assert not SOURCE.exists(),'Do not overwrite existing character sources; revise explicitly'
    if not RSOURCE.exists():
        bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;setup(s);rc=col(RID);rr=empty(RID+'__root',rc);data=bpy.data.armatures.new(RID+'__skeleton_data');ro=bpy.data.objects.new(RID+'__armature',data);rc.objects.link(ro);ro.parent=rr;make_bones(data,ro)
        bpy.ops.wm.save_as_mainfile(filepath=str(RSOURCE),compress=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name=ID+'__review';setup(s);s.display.shading.color_type='VERTEX'
    c=col(ID);geo=col(ID+'__geo',c);rig=col(ID+'__rig',c);anc=col(ID+'__anchors',c);root=empty(ID+'__root',c)
    for e in CAT['entries']:
        for role in ['primary','secondary']:root['highlight_'+role+'__'+e['id']]=0.;root.id_properties_ui('highlight_'+role+'__'+e['id']).update(min=0,max=1)
    root['xray_enabled']=0.;root.id_properties_ui('xray_enabled').update(min=0,max=1)
    with bpy.data.libraries.load(str(RSOURCE),link=True) as(src,dst):dst.armatures=[RID+'__skeleton_data']
    data=dst.armatures[0];solver=bpy.data.objects.new(RID+'__armature_solver',data);rig.objects.link(solver);solver.parent=root
    arm=bpy.data.objects.new(ID+'__armature_deform',data);rig.objects.link(arm);arm.parent=root
    bpy.context.view_layer.update()
    controls={};solvers={};limits={};limitbindings={}
    for key in ['root_motion','pelvis']:controls[key]={'object':solver.name,'bone':'root' if key=='root_motion' else 'pelvis'}
    for spec in SK['bones']:
        name=spec['name'];pb=solver.pose.bones[name];pb.rotation_mode='QUATERNION';arm.pose.bones[name].rotation_mode='QUATERNION'
        cc=arm.pose.bones[name].constraints.new('COPY_TRANSFORMS');cc.target=solver;cc.subtarget=name;cc.owner_space='POSE';cc.target_space='POSE'
        if spec['deform']:controls['fk_'+name]={'object':solver.name,'bone':name}
    for side in ['l','r']:
        for limb,tip,owner,polekind,poledir in [('arm','hand','forearm','elbow',-1),('leg','foot','shin','knee',1)]:
            mode='ik_fk_'+limb+'_'+side;root[mode]=0.;root.id_properties_ui(mode).update(min=0,max=1);controls[mode]={'object':root.name,'bone':None,'property':mode}
            target=empty(ID+'__control_ik_'+tip+'_'+side,rig,root);target.matrix_world=arm.data.bones[tip+'_'+side].matrix_local.copy();target.empty_display_type='CUBE';target.empty_display_size=.035
            pole=empty(ID+'__control_pole_'+polekind+'_'+side,rig,root,Vector(G[owner+'_'+side][0])+Vector((0,poledir*.35,0)))
            controls['ik_'+tip+'_'+side]={'object':target.name,'bone':None};controls['pole_'+polekind+'_'+side]={'object':pole.name,'bone':None}
            ik=solver.pose.bones[owner+'_'+side].constraints.new('IK');ik.target=target;ik.pole_target=pole;ik.chain_count=2;ik.use_stretch=False;ik.influence=0
            ik.pole_angle=0 if side=='l' else math.pi
            driver=ik.driver_add('influence').driver;var=driver.variables.new();var.name='blend';var.targets[0].id=root;var.targets[0].data_path='["'+mode+'"]';driver.expression='blend'
            solver.pose.bones[owner+'_'+side].ik_stretch=0
            solvers['ik_'+tip+'_'+side]={'object':solver.name,'bone':owner+'_'+side}
            rot=solver.pose.bones[tip+'_'+side].constraints.new('COPY_ROTATION');rot.target=target;rot.owner_space='WORLD';rot.target_space='WORLD';rot.influence=0
            driver=rot.driver_add('influence').driver;var=driver.variables.new();var.name='blend';var.targets[0].id=root;var.targets[0].data_path='["'+mode+'"]';driver.expression='blend'
            name=owner+'_'+side;lo=[-2.7,-1.6,0] if limb=='arm' else [-2.7,0,0];hi=[2.7,1.6,0] if limb=='arm' else [0,0,0]
            lim=solver.pose.bones[name].constraints.new('LIMIT_ROTATION');lim.owner_space='LOCAL'
            for i,ax in enumerate('xyz'):setattr(lim,'use_limit_'+ax,True);setattr(lim,'min_'+ax,lo[i]);setattr(lim,'max_'+ax,hi[i])
            limits[name]={'min_radians':lo,'max_radians':hi,'approval_reference':None};limitbindings[name]={'object':solver.name,'bone':name}
    parts=[]
    torso=[(.84,.075,.075),(.89,.125,.10),(.96,.145,.108),(1.02,.13,.095),(1.09,.115,.082),(1.17,.128,.092),(1.25,.15,.103),(1.32,.171,.108),(1.38,.174,.095),(1.42,.16,.075),(1.45,.11,.060),(1.47,.055,.048)]
    parts.append(loft('construction_torso',[((0,-.005,z),rx,ry) for z,rx,ry in torso],geo))
    parts.append(loft('construction_neck',[((0,0,z),rx,ry) for z,rx,ry in [(1.40,.06,.05),(1.46,.052,.048),(1.51,.043,.041),(1.56,.048,.043),(1.59,.055,.048)]],geo))
    headsections=[(1.535,.031,.036,.005),(1.56,.046,.048,.014),(1.59,.062,.059,.010),(1.63,.075,.068,.001),(1.67,.078,.071,0),(1.70,.073,.067,-.002),(1.73,.055,.052,-.005),(1.745,.028,.030,-.006),(1.75,.002,.002,-.006)]
    head=loft('construction_head',[((0,y,z),rx,ry) for z,rx,ry,y in headsections],geo,sides=64)
    for v in head.data.vertices:
        x,y,z=v.co
        if y>0:
            nose=.014*math.exp(-(x/.017)**2-((z-1.642)/.029)**2);eyes=.005*(math.exp(-((x-.031)/.020)**2)+math.exp(-((x+.031)/.020)**2))*math.exp(-((z-1.665)/.009)**2);v.co.y+=nose-eyes
    parts.append(head)
    for side,sign in [('l',1),('r',-1)]:
        parts.append(tube('construction_shoulder_'+side,(sign*.125,0,1.41),G['upper_arm_'+side][1],[(-.1,.056,.057),(0,.065,.061),(.20,.067,.064),(.45,.053,.052),(.8,.037,.035),(1,.033,.034)],geo))
        parts.append(tube('construction_upper_'+side,*G['upper_arm_'+side],[(-.12,.054,.052),(0,.059,.060),(.25,.061,.057),(.5,.056,.060),(.75,.046,.046),(1,.032,.035),(1.08,.028,.028)],geo))
        parts.append(tube('construction_forearm_'+side,*G['forearm_'+side],[(-.08,.033,.033),(0,.035,.036),(.22,.046,.039),(.45,.039,.034),(.75,.026,.026),(1,.021,.022),(1.10,.020,.020)],geo))
        parts.append(tube('construction_palm_'+side,*G['hand_'+side],[(-.1,.021,.021),(0,.025,.022),(.4,.042,.021),(.75,.045,.018),(1,.040,.015),(1.05,.035,.013)],geo))
        for digit in ['thumb','index','middle','ring','little']:
            start=G[digit+'_01_'+side][0];end=G[digit+'_03_'+side][1];radius=.010 if digit!='little' else .0085
            parts.append(tube('construction_'+digit+'_'+side,start,end,[(-.18,radius,radius*.88),(0,radius,radius*.9),(.35,radius*.95,radius*.85),(.7,radius*.8,radius*.75),(.93,radius*.65,radius*.65),(1.03,.002,.002)],geo,sides=20))
        parts.append(tube('construction_thigh_'+side,*G['thigh_'+side],[(-.12,.082,.09),(0,.092,.104),(.22,.092,.103),(.48,.08,.09),(.72,.061,.065),(1,.043,.047),(1.08,.042,.041)],geo))
        parts.append(tube('construction_calf_'+side,*G['shin_'+side],[(-.1,.042,.044),(0,.046,.048),(.24,.061,.064),(.42,.058,.064),(.65,.037,.041),(.85,.027,.027),(1,.026,.027),(1.09,.028,.028)],geo))
        foot=loft('construction_foot_'+side,[((sign*.1,y,z),rx,rz) for y,z,rx,rz in [(-.065,.047,.032,.042),(-.04,.045,.039,.044),(0,.05,.041,.046),(.06,.041,.045,.035),(.14,.034,.050,.026),(.20,.029,.048,.023),(.235,.026,.032,.017),(.25,.025,.004,.005)]],geo,axis='y');parts.append(foot)
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:p.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=parts[0];body.name=ID+'__mesh_body'
    # Consistent outward geometry before volume union.
    import bmesh
    bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()
    rem=body.modifiers.new('seamless_anatomical_union','REMESH');rem.mode='VOXEL';rem.voxel_size=.0028;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
    smooth=body.modifiers.new('surface_fairing','SMOOTH');smooth.factor=.65;smooth.iterations=5;bpy.ops.object.modifier_apply(modifier=smooth.name)
    low=min(v.co.z for v in body.data.vertices);high=max(v.co.z for v in body.data.vertices)
    for v in body.data.vertices:v.co.z=(v.co.z-low)*1.75/(high-low)
    for p in body.data.polygons:p.use_smooth=True
    body.parent=root;body.data.materials.append(material(ID+'__material_skin_base',(.45,.49,.51)));weight(body)
    skin=body.modifiers.new('canonical_skinning','ARMATURE');skin.object=arm;skin.use_deform_preserve_volume=True
    xyz=np.array([v.co[:] for v in body.data.vertices]);implemented=[];bindings={}
    for e in CAT['entries']:body.vertex_groups.new(name=e['id'])
    for side,sign in [('l',1),('r',-1)]:
        x,y,z=xyz.T
        pec=np.exp(-((x-sign*.087)/.075)**4-((z-1.315)/.075)**4)*(y>.045)*(x*sign>.012)
        patterns={'pectoralis_major':pec}
        a,b=np.array(G['upper_arm_'+side][0]),np.array(G['upper_arm_'+side][1]);v=b-a;t=(xyz-a)@v/(v@v);distance=np.linalg.norm(xyz-(a+np.clip(t,0,1)[:,None]*v),axis=1)
        upper=(distance<.09)*(x*sign>.14)
        patterns['biceps_brachii']=np.exp(-((t-.56)/.34)**4)*upper*(y>.018)
        patterns['triceps_brachii']=np.exp(-((t-.56)/.36)**4)*upper*(y<-.02)
        cap=np.exp(-((t-.13)/.28)**4)*upper
        patterns['deltoid_anterior']=cap*(y>.027);patterns['deltoid_posterior']=cap*(y<-.027);patterns['deltoid_middle']=cap*(abs(y)<.03)
        for name,values in patterns.items():
            mid='muscle_'+name+'_'+side;values=np.clip(values,0,1);attr(body,mid,values);implemented.append(mid)
    x,y,z=xyz.T;window=np.exp(-((x-.103)/.047)**4-((z-.741)/.119)**4)*(y>.044);attr(body,'xray_window',window,False)
    deep=loft(ID+'__mesh_vastus_intermedius_l',[((.10,.027,z),rx,ry) for z,rx,ry in [(.59,.004,.004),(.62,.020,.018),(.70,.038,.030),(.79,.039,.029),(.86,.026,.025),(.90,.004,.004)]],geo)
    deep.parent=root;deep.data.materials.append(material(ID+'__material_deep_muscle',(.65,.24,.18)))
    for p in deep.data.polygons:p.use_smooth=True
    g=deep.vertex_groups.new(name='thigh_l');g.add(list(range(len(deep.data.vertices))),1,'REPLACE');mod=deep.modifiers.new('canonical_skinning','ARMATURE');mod.object=arm
    mid='muscle_vastus_intermedius_l';attr(deep,mid,np.ones(len(deep.data.vertices)));implemented.append(mid);color_nodes(deep,root,[mid]);color_nodes(body,root,[x for x in implemented if x!=mid],True)
    for e in CAT['entries']:
        target=deep if e['id']==mid else body;bindings[e['id']]={'object':target.name,'vertex_group':e['id'],'primary_property':'highlight_primary__'+e['id'],'secondary_property':'highlight_secondary__'+e['id']}
    anchors={}
    for e in SK['anchors']:
        key=e['key'];bone=e['bone'];pos=Vector((0,0,0));q=Quaternion((1,0,0,0))
        if bone:pos=Vector(G[bone][0])
        if 'contact_' in key:
            pos.z=0;pos.y={'foot':.075,'heel':-.035,'toe':.20}[key.split('_')[0]]
        if key.startswith('hand_grip'):
            side=key[-1];u=(Vector(G['hand_'+side][1])-Vector(G['hand_'+side][0])).normalized();pos+=u*.055+Vector((0,.018,0));yv=Vector(((1 if side=='l' else -1)/math.sqrt(2),0,1/math.sqrt(2)));zv=Vector((0,1,0));q=Matrix((yv.cross(zv),yv,zv)).transposed().to_quaternion()
        if key=='back_support':pos.y=-.105;q=Quaternion((1,0,0),math.pi/2)
        obj=empty(ID+'__anchor_'+key,anc);obj.rotation_mode='QUATERNION';target=Matrix.Translation(pos)@q.to_matrix().to_4x4()
        if bone:
            obj.parent=arm;obj.parent_type='BONE';obj.parent_bone=bone;bpy.context.view_layer.update();obj.matrix_world=target
        else:obj.parent=root;obj.matrix_world=target
        bpy.context.view_layer.update();anchors[key]={'object':obj.name,'bone':bone,'position_m':list(obj.matrix_world.translation),'rotation_quaternion_wxyz':list(obj.matrix_world.to_quaternion())}
    for obj in [arm,solver]:obj.display_type='WIRE';obj.hide_set(True)
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(A))
    cam=camera(s,ID+'__camera_three_quarter',(3.3,5,2.2),(0,0,.88),2.05);s.camera=cam
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                sp=area.spaces.active;sp.shading.type='SOLID';sp.shading.light='FLAT';sp.shading.color_type='VERTEX';sp.shading.show_shadows=False;sp.shading.show_cavity=False;sp.shading.show_specular_highlight=False;sp.shading.show_object_outline=True;sp.region_3d.view_location=(0,0,.88);sp.region_3d.view_distance=2.5;sp.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
    bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
    bones=[]
    for b in data.bones:bones.append({'name':b.name,'parent':b.parent.name if b.parent else None,'deform':b.use_deform,'connected':b.use_connect,'head_m':list(b.head_local),'tail_m':list(b.tail_local),'z_axis':list(b.matrix_local.to_3x3().col[2])})
    profile=[{k:b[k] for k in ['name','parent','deform','connected','head_m','tail_m','z_axis']} for b in sorted(bones,key=lambda b:b['name'])];(A/'rest-profile.json').write_text(json.dumps(profile,sort_keys=True,separators=(',',':'),allow_nan=False))
    hc=read(R/'templates/human/human-contract.example.json');hc.update(asset_id=ID,armature=arm.name,body_objects=[body.name,deep.name],morphology='mannequin',height_m=1.75,rest_profile={'id':'mannequin_1750_review@0.1.0','path':'rest-profile.json','sha256':digest(A/'rest-profile.json')},controls=controls,anchors=anchors,muscle_bindings=bindings,joint_limits=limits,solver_bindings=solvers,joint_limit_bindings=limitbindings);write_json(A/'human-contract.json',hc)
    meta=read(A/'asset.json');meta.update(status='review',source_revision_or_digest='sha256:'+digest(SOURCE),dimensions_m=[max(v.co[k] for v in body.data.vertices)-min(v.co[k] for v in body.data.vertices) for k in range(3)],anchors=anchors,material_slots={'skin_base':body.data.materials[0].name},dependencies=[{'id':RID,'version':'0.1.0','source':str(RSOURCE.relative_to(R)),'sha256':digest(RSOURCE)}],muscle_coverage={'canonical_ids':78,'implemented_ids':implemented,'unimplemented_ids':[e['id'] for e in CAT['entries'] if e['id'] not in implemented],'status':'incomplete; fail full coverage'},provenance={'creator':'Codex for168Hours Fitness','origin':'Original procedural anatomy','license':None,'attribution':'Code/docs MIT; artwork excluded'},review={'status':'review_prototype','date':'2026-10-16','approval_reference':None});write_json(A/'asset.json',meta)
    write_json(RA/'asset.json',{'id':RID,'category':'rig','version':'0.1.0','status':'review','source':str(RSOURCE.relative_to(R)),'source_revision_or_digest':'sha256:'+digest(RSOURCE),'skeleton':'168h_human_skeleton@1.0.0','rest_profile_sha256':digest(A/'rest-profile.json'),'implementation':'canonical linked armature data; character source owns solver/control assembly','license':None})
    write_json(A/'build-record.json',{'builder_sha256':digest(Path(__file__)),'source_sha256':digest(SOURCE),'rig_sha256':digest(RSOURCE),'mesh_vertices':len(body.data.vertices),'mesh_faces':len(body.data.polygons),'bone_count':len(data.bones),'anchors':len(anchors),'implemented_muscles':implemented,'voxel_size_m':.0028,'surface_fairing_iterations':5})
    print('MANNEQUIN_BUILD',len(body.data.vertices),len(data.bones),len(implemented))
if __name__=='__main__':build()
