"""0.2 foundation correction: pinned CC0 topology/weight data adapted to unchanged V1."""
from pathlib import Path
import bpy,bmesh,sys,json,math,numpy as np
from mathutils import Vector,Matrix,Quaternion
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_anatomical_mannequin as original
from mannequin_foundation_data import canonical_data,frame,REF
from build_anatomical_mannequin import R,A,ID,RID,SOURCE,RA,SK,CAT
from barbell_20kg_common import digest,write_json
NEW_RIG=RA/(RID+'__foundation_v02.blend')
def run():
 assert (A/'foundation-plan.json').exists()
 assert not (A/'foundation-build.json').exists() or ('--rebuild-review' in sys.argv and json.loads((A/'asset.json').read_text())['status']=='review'),'Explicit review rebuild only; never overwrite an approved asset'
 bpy.ops.wm.open_mainfile(filepath=str(A/'history/0.1.0/library/assets/humans/models'/ID/(ID+'.blend')));root=bpy.data.objects[ID+'__root'];body=bpy.data.objects[ID+'__mesh_body'];arm=bpy.data.objects[ID+'__armature_deform'];solver=bpy.data.objects[RID+'__armature_solver'];before=digest(SOURCE)
 old_thigh=arm.data.bones['thigh_l'].matrix_local.copy();points,faces,g,names,weights,adapt,ids=canonical_data()
 for c in list(body.modifiers):body.modifiers.remove(c)
 body.vertex_groups.clear();me=bpy.data.meshes.new(ID+'__foundation_surface');me.from_pydata(points.tolist(),[],faces);me.update();body.data=me
 # Neutral chest simplification: remove secondary-sex emphasis without changing the ribcage silhouette.
 chest=body.vertex_groups.new(name='foundation_chest_fairing')
 for v in me.vertices:
  x,y,z=v.co
  if 1.18<z<1.44 and abs(x)<.20:
   cap=.081+.013*math.exp(-((z-1.34)/.12)**2)-.018*(x/.18)**2
   if y>cap:v.co.y=cap+(y-cap)*.10
   if y>0:chest.add([v.index],1,'REPLACE')
 bm=bmesh.new();bm.from_mesh(me);boundary=[e for e in bm.edges if e.is_boundary];bmesh.ops.holes_fill(bm,edges=boundary,sides=64);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 # Face creation fills small eye/mouth borders only; no new vertices, weights remain indexed.
 assert len(me.vertices)==len(points)
 for name in names:body.vertex_groups.new(name=name)
 for k,name in enumerate(names):
  vg=body.vertex_groups[name]
  for i in np.flatnonzero(weights[:,k]>1e-7):vg.add([int(i)],float(weights[i,k]),'REPLACE')
 bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
 sm=body.modifiers.new('neutral_chest_simplification','SMOOTH');sm.vertex_group=chest.name;sm.factor=.7;sm.iterations=12;bpy.ops.object.modifier_apply(modifier=sm.name)
 sub=body.modifiers.new('continuous_anatomical_loops','SUBSURF');sub.levels=2;bpy.ops.object.modifier_apply(modifier=sub.name)
 low=min(v.co.z for v in me.vertices);high=max(v.co.z for v in me.vertices)
 # modifier_apply replaces mesh datablock; fit the actual subdivided body and the rest profile together.
 me=body.data;low=min(v.co.z for v in me.vertices);high=max(v.co.z for v in me.vertices);scale=1.75/(high-low)
 for v in me.vertices:v.co.z=(v.co.z-low)*scale;v.co.x*=scale;v.co.y*=scale
 for name,(a,b) in list(g.items()):
  if name!='root':g[name]=((a-Vector((0,0,low)))*scale,(b-Vector((0,0,low)))*scale)
 for p in me.polygons:p.use_smooth=True
 me.materials.append(bpy.data.materials[ID+'__material_skin_base'])
 # Publish new measured rest data; retain old rig file unchanged for the archived predecessor.
 rc=bpy.data.collections.new(RID+'__foundation_library');bpy.context.scene.collection.children.link(rc);rr=bpy.data.objects.new(RID+'__root',None);rc.objects.link(rr)
 data=bpy.data.armatures.new(RID+'__skeleton_data_foundation_v02');ro=bpy.data.objects.new(RID+'__armature',data);rc.objects.link(ro);ro.parent=rr;original.G=g;original.make_bones(data,ro)
 bpy.data.libraries.write(str(NEW_RIG),{rc},path_remap='RELATIVE',fake_user=True,compress=True)
 for obj in list(rc.objects):bpy.data.objects.remove(obj,do_unlink=True)
 bpy.data.collections.remove(rc);bpy.data.armatures.remove(data)
 with bpy.data.libraries.load(str(NEW_RIG),link=True) as(src,dst):dst.armatures=[RID+'__skeleton_data_foundation_v02']
 for obj in [solver,arm]:obj.data=dst.armatures[0]
 bpy.context.view_layer.update()
 hc=json.loads((A/'human-contract.json').read_text())
 for side in ['l','r']:
  for limb,tip,hinge,poleaxis,lo,hi in [('arm','hand','forearm',-1,0,2.62),('leg','foot','shin',1,-2.62,0)]:
   b=solver.pose.bones[hinge+'_'+side];b.lock_ik_y=True;b.lock_ik_z=True;b.use_ik_limit_x=True;b.ik_min_x=lo;b.ik_max_x=hi;b.ik_stretch=0
   ik=next(c for c in b.constraints if c.type=='IK');ik.use_stretch=False;ik.iterations=500;ik.pole_angle=-math.pi/2;ik.chain_count=2
   lim=next(c for c in b.constraints if c.type=='LIMIT_ROTATION');lim.min_x=lo;lim.max_x=hi;lim.min_y=-1.2 if limb=='arm' else 0;lim.max_y=1.2 if limb=='arm' else 0;lim.min_z=lim.max_z=0
   hc['joint_limits'][b.name]={'min_radians':[lim.min_x,lim.min_y,0],'max_radians':[lim.max_x,lim.max_y,0],'approval_reference':None}
   solver.pose.bones[('upper_arm' if limb=='arm' else 'thigh')+'_'+side].ik_stretch=0
   target=bpy.data.objects[ID+'__control_ik_'+tip+'_'+side];target.matrix_world=arm.data.bones[tip+'_'+side].matrix_local.copy()
   pole=bpy.data.objects[ID+'__control_pole_'+('elbow' if limb=='arm' else 'knee')+'_'+side];pole.location=Vector(g[hinge+'_'+side][0])+Vector((0,poleaxis*.30,0))
 for obj in [solver,arm]:
  for b in obj.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=(1,0,0,0);b.location=(0,0,0);b.scale=(1,1,1)
 for key in root.keys():
  if isinstance(root[key],float):root[key]=0.
 skin=body.modifiers.new('canonical_skinning','ARMATURE');skin.object=arm;skin.use_deform_preserve_volume=True
 # Keep canonical region IDs and the existing demonstration subset; boundaries are provisional remaps, not anatomy passes.
 xyz=np.array([v.co[:] for v in me.vertices]);x,y,z=xyz.T;implemented=[]
 for e in CAT['entries']:body.vertex_groups.new(name=e['id'])
 for side,sign in [('l',1),('r',-1)]:
  a,b=np.array(g['upper_arm_'+side][0]),np.array(g['upper_arm_'+side][1]);u=b-a;t=(xyz-a)@u/(u@u);rad=np.linalg.norm(xyz-(a+np.clip(t,0,1)[:,None]*u),axis=1);upper=(rad<.085)*(x*sign>.13);cap=np.exp(-((t-.10)/.34)**4)*upper
  patterns={'pectoralis_major':np.exp(-((x-sign*.075)/.07)**4-((z-1.30)/.065)**4)*(y>.035)*(x*sign>.01),'biceps_brachii':np.exp(-((t-.57)/.30)**4)*upper*(y>.012),'triceps_brachii':np.exp(-((t-.57)/.34)**4)*upper*(y<-.015),'deltoid_anterior':cap*(y>.02),'deltoid_middle':cap*(abs(y)<.025),'deltoid_posterior':cap*(y<-.02)}
  for name,values in patterns.items():original.attr(body,'muscle_'+name+'_'+side,np.clip(values,0,1));implemented.append('muscle_'+name+'_'+side)
 original.attr(body,'xray_window',np.exp(-((x-.098)/.046)**4-((z-.69)/.16)**4)*(y>.035),False)
 original.color_nodes(body,root,implemented,True)
 ng=next(m.node_group for m in body.modifiers if m.type=='NODES');shade=next(n for n in ng.nodes if n.type=='MATH' and n.operation=='MULTIPLY_ADD');shade.inputs[1].default_value=.28;shade.inputs[2].default_value=.57;base=next(n for n in ng.nodes if n.type=='MIX_RGB');base.inputs[1].default_value=(.25,.28,.30,1);base.inputs[2].default_value=(.62,.65,.67,1)
 deep=bpy.data.objects[ID+'__mesh_vastus_intermedius_l'];newthigh=arm.data.bones['thigh_l'].matrix_local.copy();transform=newthigh@old_thigh.inverted()
 for v in deep.data.vertices:v.co=transform@v.co
 bpy.context.view_layer.update();tree=BVHTree.FromPolygons([v.co for v in me.vertices],[p.vertices[:] for p in me.polygons])
 for key,decl in hc['anchors'].items():
  bone=decl['bone'];pos=Vector(g[bone][0]) if bone else Vector((0,0,0));q=Quaternion((1,0,0,0))
  if 'contact_' in key:pos.z=0;pos.y={'foot':.07,'heel':-.035,'toe':.17}[key.split('_')[0]]
  if key.startswith('hand_grip'):
   sign=1 if key.endswith('_l') else -1;u=(g[bone][1]-g[bone][0]).normalized();pos+=u*.052+Vector((0,.028,0));yv=Vector((sign,0,1)).normalized();zv=Vector((0,1,0));q=Matrix((yv.cross(zv),yv,zv)).transposed().to_quaternion()
  if key=='back_support':
   hit=tree.ray_cast(Vector((0,-.5,pos.z)),Vector((0,1,0)),1)[0];assert hit;pos.y=hit.y;q=Quaternion((1,0,0),math.pi/2)
  obj=bpy.data.objects[decl['object']];obj.matrix_world=Matrix.Translation(pos)@q.to_matrix().to_4x4();bpy.context.view_layer.update();decl['position_m']=list(obj.matrix_world.translation);decl['rotation_quaternion_wxyz']=list(obj.matrix_world.to_quaternion())
 bpy.context.scene.camera.data.ortho_scale=2.05
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(A))
 bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
 write_json(A/'human-contract.json',hc)
 m=json.loads((A/'asset.json').read_text());m.update(version='0.2.0',source_revision_or_digest='sha256:'+digest(SOURCE),anchors=hc['anchors'],dimensions_m=[float(np.ptp(np.array([v.co[:] for v in me.vertices])[:,i])) for i in range(3)],dependencies=[{'id':RID,'version':'0.2.0','source':str(NEW_RIG.relative_to(R)),'sha256':digest(NEW_RIG)}],provenance={'creator':'MakeHuman contributors; adapted by Codex for168Hours Fitness','origin':'CC0 hm08 body topology and graphical joint/weight data, pinned references/makehuman/provenance.json; original V1 adapter, neutral simplification and illustration setup','upstream_license':'CC0-1.0','license':None,'license_reference':'references/makehuman/LICENSE.ASSETS.md','attribution':'Upstream notices retained; project artwork release terms remain unselected; original scripts/docs MIT'},review={'status':'review_prototype','date':'2026-10-16','approval_reference':None,'foundation_correction':'built; seven-pose validation pending'});m['muscle_coverage']['status']='13 provisional remaps;65unimplemented; no anatomy coverage approval';m['reference_renders']=[];write_json(A/'asset.json',m)
 write_json(RA/'asset.json',{'id':RID,'category':'rig','version':'0.2.0','status':'review','source':str(NEW_RIG.relative_to(R)),'source_revision_or_digest':'sha256:'+digest(NEW_RIG),'skeleton':'168h_human_skeleton@1.0.0','rest_profile_sha256':None,'implementation':'V1 canonical rest profile adapted from CC0 graphical joint data; separate source file preserves0.1.0','license':None,'upstream_license':'CC0-1.0'})
 write_json(A/'foundation-build.json',{'version':'0.2.0','prior_source_sha256':before,'source_sha256':digest(SOURCE),'rig_sha256':digest(NEW_RIG),'script_sha256':digest(Path(__file__)),'adapter_sha256':digest(Path(__file__).with_name('mannequin_foundation_data.py')),'source_vertices':len(ids),'source_faces':len(faces),'final_vertices':len(me.vertices),'final_faces':len(me.polygons),'bone_count':len(arm.data.bones),'source_to_core_weight_adapter':adapt,'removed_helper_groups':'All OBJ groups exceptbody; no source skeleton imported as output','skin':'Mapped anatomical weights, normalized; dual quaternion preserves joint volume','controls':'V1 FK/IK facade retained; IK axes locked at knee, native nonstretch limits; manual transition helper tested separately'})
 print('FOUNDATION_BUILD',len(me.vertices),len(me.polygons))
if __name__=='__main__':run()
