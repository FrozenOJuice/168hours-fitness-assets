"""CC0 Blender anatomy foundation -> isolated Human V1 prototype. No master edits."""
from pathlib import Path
import bpy,bmesh,json,sys,math,numpy as np
from mathutils import Vector,Matrix,Quaternion
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v03_common import *
import build_anatomical_mannequin as original
from barbell_20kg_common import setup,camera,digest,write_json
from mannequin_foundation_data import frame
SK=original.SK;CAT=original.CAT

def make_data(name,g,normals=None):
 data=bpy.data.armatures.new(name);obj=bpy.data.objects.new(name+'__object',data);bpy.context.scene.collection.objects.link(obj);bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
 for b in SK['bones']:
  eb=data.edit_bones.new(b['name']);eb.head,eb.tail=g[b['name']];eb.use_deform=b['deform'];eb.align_roll(Vector((normals or {}).get(b['name'],(0,1,0))))
 for b in SK['bones']:
  eb=data.edit_bones[b['name']]
  if b['parent']:eb.parent=data.edit_bones[b['parent']];eb.use_connect=b['connected']
 bpy.ops.object.mode_set(mode='OBJECT');obj.select_set(False);return obj

def build():
 assert not SOURCE.exists() or ('--rebuild-isolated' in sys.argv and (A/'history/initial_hand_fit').is_dir()),'Preserve isolated candidates before explicit rebuild'
 bpy.ops.wm.open_mainfile(filepath=str(A/'references/human_base_meshes_bundle.blend'));source=bpy.data.objects['GEO-body_male_realistic'];female=bpy.data.objects['GEO-body_female_realistic'];source.modifiers[0].levels=1;female.modifiers[0].levels=1;bpy.context.view_layer.update()
 meshes=[]
 for obj in [source,female]:meshes.append(bpy.data.meshes.new_from_object(obj.evaluated_get(bpy.context.evaluated_depsgraph_get())))
 arrays=[]
 for me in meshes:
  pts=np.array([v.co[:] for v in me.vertices]);pts[:,:2]*=-1;pts[:,2]-=pts[:,2].min();pts*=1.75/np.ptp(pts[:,2]);arrays.append(pts)
 p=arrays[0];faces=[f.vertices[:] for f in meshes[0].polygons];same=faces==[f.vertices[:] for f in meshes[1].polygons]
 # Neutral genital contour from same-topology CC0 female pelvis, localized only.
 if same:
  x,y,z=p.T;blend=.9*np.exp(-(x/.045)**4-((z-.88)/.09)**4)*np.clip((y-.015)/.065,0,1);p+=(arrays[1]-p)*blend[:,None]
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;setup(s);me=bpy.data.meshes.new(ID+'__anatomy_cage');me.from_pydata(p.tolist(),[],faces);me.update();body=bpy.data.objects.new(ID+'__mesh_body',me);s.collection.objects.link(body)
 # Original measured source-pose landmarks, meters; front+Y, arm palms face medially.
 src={'root':((0,0,0),(0,0,.1))};ax=[('pelvis',.96,1.07),('spine_01',1.07,1.19),('spine_02',1.19,1.34),('spine_03',1.34,1.49),('neck',1.49,1.59),('head',1.59,1.735)]
 for n,a,b in ax:src[n]=((0,0,a),(0,0,b))
 normals={};target={n:(Vector(a),Vector(b)) for n,(a,b) in src.items()}
 for side,sign in [('l',1),('r',-1)]:
  v=lambda x,y,z:Vector((sign*x,y,z))
  shoulder=v(.19,0,1.425);elbow=v(.318,.005,1.105);wrist=v(.397,.085,.887);palm=v(.432,.105,.803)
  src['clavicle_'+side]=(Vector((0,0,1.49)),shoulder);src['upper_arm_'+side]=(shoulder,elbow);src['forearm_'+side]=(elbow,wrist);src['hand_'+side]=(wrist,palm)
  long=(palm-wrist).normalized();radial=Vector((0,1,0));normal=-sign*long.cross(radial).normalized()
  for n in ['upper_arm','forearm','hand']:normals[n+'_'+side]=tuple(normal)
  # Explicit digit landmarks across source palm; three bones per digit.
  fingers={'index':[(.425,.169,.846),(.432,.174,.818),(.434,.176,.794),(.434,.176,.777)],'middle':[(.425,.145,.840),(.434,.146,.803),(.435,.147,.773),(.435,.147,.751)],'ring':[(.425,.115,.835),(.431,.116,.801),(.431,.117,.768),(.431,.117,.745)],'little':[(.421,.071,.837),(.429,.068,.808),(.430,.066,.778),(.429,.066,.755)],'thumb':[(.398,.130,.874),(.384,.157,.858),(.378,.177,.848),(.378,.183,.838)]}
  target['clavicle_'+side]=(Vector((0,0,1.49)),v(.19,0,1.425));start=target['clavicle_'+side][1];u=Vector((sign,0,-1)).normalized()
  for n in ['upper_arm','forearm','hand']:
   a,b=src[n+'_'+side];end=start+u*(b-a).length;target[n+'_'+side]=(start.copy(),end.copy());start=end
  transform=frame(*target['hand_'+side])@frame(wrist,palm,normal).inverted()
  for digit,points in fingers.items():
   points=[v(*a) for a in points];start=transform@points[0];direction=Vector((sign,0,0)) if digit=='thumb' else u
   for i in range(1,4):
    n=f'{digit}_{i:02}_{side}';src[n]=(points[i-1],points[i]);normals[n]=tuple(normal);end=start+direction*(points[i]-points[i-1]).length;target[n]=(start.copy(),end.copy());start=end
  src['thigh_'+side]=(v(.105,0,.955),v(.125,.012,.49));src['shin_'+side]=(src['thigh_'+side][1],v(.145,.005,.09));src['foot_'+side]=(src['shin_'+side][1],v(.155,.14,.025));src['toe_'+side]=(src['foot_'+side][1],v(.16,.205,.025))
  start=v(.105,0,.955)
  for n in ['thigh','shin']:
   a,b=src[n+'_'+side];end=start+Vector((0,0,-(b-a).length));target[n+'_'+side]=(start.copy(),end.copy());start=end
  shift=start-src['foot_'+side][0];target['foot_'+side]=(start.copy(),src['foot_'+side][1]+shift);target['toe_'+side]=(target['foot_'+side][1].copy(),target['foot_'+side][1]+Vector((0,(src['toe_'+side][1]-src['toe_'+side][0]).length,0)))
 bind=make_data(ID+'__temporary_source_bind',src,normals)
 bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bind.select_set(True);bpy.context.view_layer.objects.active=bind;bpy.ops.object.parent_set(type='ARMATURE_AUTO')
 missing=[v.index for v in me.vertices if not any(g.weight>0 for g in v.groups)];print('HEAT_UNWEIGHTED',len(missing));assert not missing,'Bone heat failed; investigate before publishing'
 # Repose weighted source into canonical frames, then freeze as new bind geometry.
 for b in bind.pose.bones:b.rotation_mode='QUATERNION'
 for entry in SK['bones']:
  n=entry['name'];bind.pose.bones[n].matrix=frame(*target[n]);bpy.context.view_layer.update()
 bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=next(m.name for m in body.modifiers if m.type=='ARMATURE'));body.parent=None;body.matrix_world=Matrix.Identity(4);bpy.data.objects.remove(bind,do_unlink=True)
 # Normalize all to exact floor1.75, including canonical joint coordinates.
 pts=np.array([v.co[:] for v in me.vertices]);floor=float(pts[:,2].min());scale=1.75/np.ptp(pts[:,2]);pts[:,2]-=floor;pts*=scale;me.vertices.foreach_set('co',pts.astype(np.float32).ravel())
 for n in target:
  if n=='root':continue
  target[n]=tuple(Vector((v.x*scale,v.y*scale,(v.z-floor)*scale)) for v in target[n])
 target['root']=(Vector((0,0,0)),Vector((0,0,.1)))
 # Save native separate canonical rig data; source wrapper is composed below.
 rig=make_data(RID+'__skeleton_data_anatomy_v03',target);data=rig.data;RA.mkdir(parents=True,exist_ok=True);rig.name=RID+'__armature';rc=bpy.data.collections.new(RID);s.collection.children.link(rc);s.collection.objects.unlink(rig);rc.objects.link(rig);rr=bpy.data.objects.new(RID+'__root',None);rc.objects.link(rr);rig.parent=rr;bpy.data.libraries.write(str(RSOURCE),{rc},path_remap='RELATIVE_ALL',compress=True)
 # Store native body as temporary data, then append into existing tested rig/control wrapper.
 temp=A/'references/adapted_unbound.blend';bpy.data.libraries.write(str(temp),{body},compress=True);write_json(A/'measured-source-joints.json',{'source':{n:[list(a),list(b)] for n,(a,b) in src.items()},'canonical':{n:[list(a),list(b)] for n,(a,b) in target.items()},'method':'Original visual-landmark fit in selected CC0 scan; provisional anatomical joint measurements','heat_unweighted_vertices':len(missing),'female_pelvis_same_topology':same})
 bpy.ops.wm.open_mainfile(filepath=str(MASTER/(ID+'.blend')));old=bpy.data.objects[ID+'__mesh_body'];parent=old.parent;collections=list(old.users_collection)
 with bpy.data.libraries.load(str(temp),link=False) as (f,t):t.objects=[ID+'__mesh_body']
 new=t.objects[0];new.name=ID+'__mesh_body_new';bpy.data.objects.remove(old,do_unlink=True);new.name=ID+'__mesh_body';new.parent=parent;new.matrix_world=Matrix.Identity(4)
 for c in collections:c.objects.link(new)
 with bpy.data.libraries.load(str(RSOURCE),link=True) as (f,t):t.armatures=[RID+'__skeleton_data_anatomy_v03']
 arm=bpy.data.objects[ID+'__armature_deform'];solver=bpy.data.objects[RID+'__armature_solver'];arm.data=t.armatures[0];solver.data=t.armatures[0]
 for o in [arm,solver]:
  for b in o.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=(1,0,0,0);b.location=(0,0,0);b.scale=(1,1,1)
 for side in ['l','r']:
  for stem in ['forearm','shin']:solver.pose.bones[stem+'_'+side].ik_stretch=0
 root=bpy.data.objects[ID+'__root'];root.matrix_world=Matrix.Identity(4)
 for key in root.keys():
  if key.startswith(('highlight_','ik_fk_')) or key=='xray_enabled':root[key]=0.
 # Normalize heat weights, preserving only canonical deform influences.
 core={b['name'] for b in SK['bones'] if b['deform']}
 for v in new.data.vertices:
  weights=[(new.vertex_groups[g.group].name,g.weight) for g in v.groups if new.vertex_groups[g.group].name in core];total=sum(w for n,w in weights)
  for n,w in weights:new.vertex_groups[n].add([v.index],w/total,'REPLACE')
 for f in new.data.polygons:f.use_smooth=True
 skin=new.modifiers.new('canonical_skinning','ARMATURE');skin.object=arm;skin.use_deform_preserve_volume=True
 sub=new.modifiers.new('anatomy_surface_finish','SUBSURF');sub.levels=1;sub.render_levels=1
 mat=bpy.data.materials.new(ID+'__material_anatomy_gray');mat.diffuse_color=(.46,.49,.51,1);new.data.materials.clear();new.data.materials.append(mat)
 # Semantic IDs remain stable; a deliberately partial set of surface demonstrations.
 pts=np.array([v.co[:] for v in new.data.vertices]);x,y,z=pts.T;implemented=[]
 for e in CAT['entries']:
  mid=e['id'];new.vertex_groups.new(name=mid);field=np.zeros(len(pts));sign=1 if e['side']=='l' else -1;ax=sign*x
  if 'pectoralis_major' in mid:field=np.exp(-((ax-.085)/.065)**4-((z-1.35)/.065)**4)*np.clip((y-.025)/.055,0,1)
  if 'deltoid_' in mid:
   c=np.array(target['upper_arm_'+e['side']][0]);field=np.exp(-((x-c[0])/.065)**4-((z-c[2])/.075)**4)*np.clip((ax-.12)/.04,0,1)
   if 'anterior' in mid:field*=np.clip((y+.01)/.055,0,1)
   elif 'posterior' in mid:field*=np.clip((-y+.015)/.055,0,1)
   else:field*=np.clip((ax-.17)/.055,0,1)
  if 'biceps_brachii' in mid or 'triceps_brachii' in mid:
   a,b=target['upper_arm_'+e['side']];u=(b-a).normalized();v=pts-np.array(a);t=v@np.array(u);r=np.linalg.norm(v-t[:,None]*np.array(u),axis=1);field=np.exp(-((t-.15)/.075)**4-(r/.075)**4)*(ax>.15)*np.clip(((y if 'biceps' in mid else -y)+.005)/.04,0,1)
  if 'rectus_femoris' in mid:field=np.exp(-((ax-.105)/.05)**4-((z-.73)/.15)**4)*np.clip((y-.015)/.055,0,1)
  if float(field.max())>.2:
   implemented.append(mid)
   for i in np.flatnonzero(field>.001):new.vertex_groups[mid].add([int(i)],float(field[i]),'REPLACE')
  attr=new.data.attributes.new(mid,'FLOAT','POINT');attr.data.foreach_set('value',field.astype(np.float32))
 # Existing deep volume remains a clear experimental placeholder, rebound/repositioned later.
 original.color_nodes(new,root,implemented,True)
 ng=new.modifiers['illustration_and_highlights'].node_group
 for node in ng.nodes:
  if node.bl_idname=='ShaderNodeMath' and node.operation=='MULTIPLY_ADD':node.inputs[1].default_value=.55;node.inputs[2].default_value=.48
 window=np.exp(-((x-.105)/.045)**4-((z-.73)/.08)**4)*np.clip((y-.01)/.05,0,1);attr=new.data.attributes.new('xray_window','FLOAT','POINT');attr.data.foreach_set('value',window.astype(np.float32))
 # Full-frame anchors follow canonical bones; read actual skin for back support.
 hc=json.loads((MASTER/'human-contract.json').read_text());tree=BVHTree.FromPolygons([Vector(v) for v in pts],[p.vertices[:] for p in new.data.polygons])
 for key,d in hc['anchors'].items():
  bone=d['bone'];pos=target[bone][0].copy() if bone else Vector((0,0,0));q=Quaternion((1,0,0,0))
  if 'contact_' in key:pos.z=0;pos.y={'foot':.07,'heel':-.035,'toe':.17}[key.split('_')[0]]
  if key.startswith('hand_grip'):
   sign=1 if key.endswith('_l') else -1;u=(target[bone][1]-target[bone][0]).normalized();pos+=u*.058+Vector((0,.030,0));yv=Vector((sign,0,1)).normalized();zv=Vector((0,1,0));q=Matrix((yv.cross(zv),yv,zv)).transposed().to_quaternion()
  if key=='back_support':
   hit=tree.ray_cast(Vector((0,-.5,pos.z)),Vector((0,1,0)),1)[0];assert hit;pos.y=hit.y;q=Quaternion((1,0,0),math.pi/2)
  obj=bpy.data.objects[d['object']];obj.matrix_world=Matrix.Translation(pos)@q.to_matrix().to_4x4();bpy.context.view_layer.update();d['position_m']=list(obj.matrix_world.translation);d['rotation_quaternion_wxyz']=list(obj.matrix_world.to_quaternion())
 # Existing IK targets are reset to the new measured rest wrists/ankles and poles.
 for side,sign in [('l',1),('r',-1)]:
  for tip,hinge,poleaxis in [('hand','forearm',-1),('foot','shin',1)]:
   obj=bpy.data.objects[ID+'__control_ik_'+tip+'_'+side];obj.matrix_world=arm.matrix_world@arm.data.bones[tip+'_'+side].matrix_local
   pole=bpy.data.objects[ID+'__control_pole_'+('elbow' if tip=='hand' else 'knee')+'_'+side];pole.matrix_world.translation=target[hinge+'_'+side][0]+Vector((0,poleaxis*.3,0))
 # Reposition the experimental deep vastus volume relative to measured thigh.
 deep=bpy.data.objects[ID+'__mesh_vastus_intermedius_l'];center=np.mean([v.co[:] for v in deep.data.vertices],axis=0);desired=np.array([target['thigh_l'][0].x,.015,.73]);offset=desired-center
 for v in deep.data.vertices:v.co+=Vector(offset)
 for mod in deep.modifiers:
  if mod.type=='ARMATURE':mod.object=arm
 # Save neutral illustration source without modifying the masters.
 setup(bpy.context.scene);bpy.context.scene.display.shading.color_type='VERTEX';bpy.context.scene.camera=camera(bpy.context.scene,ID+'__anatomy_camera',(2.6,5,1.65),(0,0,.88),2.05)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(A))
 bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
 hc['asset_manifest']='asset.json';hc['rest_profile']={'id':'mannequin_1750_anatomy@0.3.0','path':'rest-profile.json','sha256':None};hc['height_m']=1.75;write_json(A/'human-contract.json',hc)
 m=json.loads((A/'asset.json').read_text());m.update(status='review',blender_version=bpy.app.version_string,units='meters',axes={'up':'+Z','forward':'+Y','subject_left':'+X'},root=ID+'__root',collection=ID,source_revision_or_digest='sha256:'+digest(SOURCE),dimensions_m=np.ptp(pts,axis=0).tolist(),anchors=hc['anchors'],dependencies=[{'id':RID,'version':'0.3.0','source':str(RSOURCE.relative_to(R)),'sha256':digest(RSOURCE)}],muscle_coverage={'implemented_surface_ids':implemented,'unimplemented_count':78-len(implemented),'status':'partial prototype; anatomical boundaries unapproved'},render_settings=str((A/'previews/render-settings.json').relative_to(R)));write_json(A/'asset.json',m)
 write_json(A/'build-record.json',{'source_sha256':digest(SOURCE),'script_sha256':digest(Path(__file__)),'vertices':len(new.data.vertices),'polygons':len(new.data.polygons),'source_bind_landmarks':'measured-source-joints.json','source_skinning':'Blender bone-heat starting bind, normalized canonical influences, no unweighted vertices','canonical_profile':'new measured V1 profile; retarget required for prior poses','superficial_masks':implemented,'limitations':['Bone-heat bind requires visual deformation refinement','Deep volume remains experimental simplified anatomy, not certified muscle reconstruction','Sparse surface masks; full coverage intentionally incomplete']})
 print('ANATOMY_PROTOTYPE_BUILT',len(new.data.vertices),len(implemented))
if __name__=='__main__':build()
