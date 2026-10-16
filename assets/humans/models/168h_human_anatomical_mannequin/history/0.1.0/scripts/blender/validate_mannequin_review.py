"""Read-only actual-source/posed-fixture review checks. Does not waive V1 coverage gates."""
from pathlib import Path
import bpy,sys,json,math,numpy as np,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
from build_anatomical_mannequin import R,A,ID,RID,SOURCE,RSOURCE
from barbell_20kg_common import digest,write_json
F=R/'scenes/templates/168h_template_mannequin_bench_press';FS=F/(F.name+'.blend');checks=[]
def record(key,ok,actual,expected):checks.append({'id':key,'result':'PASS' if ok else 'FAIL','actual':actual,'expected':expected})
def evaluated(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=e.to_mesh();xyz=np.array([(e.matrix_world@v.co)[:] for v in mesh.vertices]);colors=np.array([v.color[:] for v in mesh.color_attributes['Color'].data]) if mesh.color_attributes.get('Color') else None;faces=len(mesh.polygons);e.to_mesh_clear();return xyz,colors,faces
def run():
 protected=json.loads((A/'prebuild-record.json').read_text())['protected_sha256'];bad=[p for p,h in protected.items() if digest(R/p)!=h];record('protected_equipment_contract_and_existing_fixtures',not bad,bad,'No bytes changed')
 before=digest(SOURCE);bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;mc.neutral();body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');solver=mc.get(RID+'__armature_solver');root=mc.get(ID+'__root');xyz,c,n=evaluated(body)
 record('source_stature_m',abs(float(np.ptp(xyz[:,2]))-1.75)<1e-5,float(np.ptp(xyz[:,2])),1.75)
 record('floor_m',abs(float(xyz[:,2].min()))<1e-5,float(xyz[:,2].min()),0)
 record('separate_solver_and_output',arm!=solver and arm.data==solver.data and bool(arm.data.library),{'output':arm.name,'solver':solver.name,'linked_canonical_data':bool(arm.data.library)},'Two pose objects, one linked53-bone rest data')
 bm=bmesh.new();bm.from_mesh(body.data);seen=set();sizes=[]
 for v in bm.verts:
  if v.index in seen:continue
  stack=[v];seen.add(v.index);count=0
  while stack:
   q=stack.pop();count+=1
   for e in q.link_edges:
    other=e.other_vert(q)
    if other.index not in seen:seen.add(other.index);stack.append(other)
  sizes.append(count)
 nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();record('continuous_watertight_neutral_body',len(sizes)==1 and nonmanifold==0,{'components':len(sizes),'component_vertices':sorted(sizes,reverse=True),'nonmanifold_edges':nonmanifold},'One closed connected skin mesh')
 changed={}
 for pose in ['bend','grip']:
  mc.pose(pose);points,colors,faces=evaluated(body);delta=np.linalg.norm(points-xyz,axis=1);changed[pose]={'moved_vertices':int(np.sum(delta>1e-5)),'max_displacement_m':float(delta.max()),'finite':bool(np.isfinite(points).all())};record('pose_deforms_'+pose,changed[pose]['finite'] and changed[pose]['moved_vertices']>100,changed[pose],'>100 finite moved vertices; does not certify visual anatomy')
 mc.neutral();mc.highlight('muscle_pectoralis_major_l');mc.update();_,primary,_=evaluated(body);mc.neutral();mc.highlight('muscle_pectoralis_major_l','secondary');mc.update();_,secondary,_=evaluated(body)
 record('primary_secondary_actual_color',np.max(abs(primary-c))>.05 and np.max(abs(primary-secondary))>.05,{'primary_delta':float(np.max(abs(primary-c))),'role_delta':float(np.max(abs(primary-secondary)))},'Actual evaluated colors change independently, distinct roles')
 mc.pose('xray');_,_,xn=evaluated(body);deep=mc.get(ID+'__mesh_vastus_intermedius_l');dx,dc,dn=evaluated(deep);record('on_character_deep_cutaway',xn<n and len(dx)>0,{'neutral_skin_faces':n,'window_skin_faces':xn,'deep_vertices':len(dx),'deep_bone_groups':[g.name for g in deep.vertex_groups]},'Actual surface aperture exposes actual skinned deep muscle; anatomy review pending')
 mc.pose('xray_bend');posed_deep,_,_=evaluated(deep);mc.pose('xray');rest_deep,_,_=evaluated(deep);delta=np.linalg.norm(posed_deep-rest_deep,axis=1);record('deep_muscle_follows_pose',delta.max()>.02,{'max_displacement_m':float(delta.max())},'>20mm actual evaluated deep-muscle movement with thigh pose')
 # Test four IK chains with reachable targets and nonzero bend seeds.
 mc.neutral();errors={}
 for side,sign in [('l',1),('r',-1)]:
  for limb,tip,hinge,shift,angle in [('arm','hand','forearm',(0,.10,.10),.5),('leg','foot','shin',(0,.10,.08),-.5)]:
   target=mc.get(ID+'__control_ik_'+tip+'_'+side);target.matrix_world.translation+=Vector(shift);mc.rotate(hinge+'_'+side,(1,0,0),angle);root['ik_fk_'+limb+'_'+side]=1.;mc.update();actual=arm.matrix_world@arm.pose.bones[tip+'_'+side].matrix;err=(actual.translation-target.matrix_world.translation).length;errors[limb+'_'+side]=err
 record('reachable_ik_targets',max(errors.values())<.0001,errors,'Each position residual<0.1mm asset-local test threshold, not an approved shared contact tolerance')
 record('source_unchanged_by_validation',digest(SOURCE)==before,digest(SOURCE),before)
 bpy.ops.wm.open_mainfile(filepath=str(FS));mc.MAPPING={o.override_library.reference.name:o for o in bpy.context.scene.objects if o.override_library};root=mc.get(ID+'__root');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');grips={s:mc.get(ID+'__anchor_hand_grip_'+s).matrix_world.translation.copy() for s in ['l','r']};err={s:(grips[s]-Vector(((-1 if s=='l' else 1)*.34,-.07,.95))).length for s in grips}
 record('bench_fixture_grip_stations',max(err.values())<.0001,err,'Within0.1mm at symmetric680mm grip span')
 record('bench_fixture_symmetry',abs(grips['l'].x+grips['r'].x)<1e-5 and abs(grips['l'].y-grips['r'].y)<1e-5 and abs(grips['l'].z-grips['r'].z)<1e-5,{s:list(p) for s,p in grips.items()},'Mirrored X/equal YZ within0.01mm')
 record('fixture_body_geometry_linked',bool(body.data.library),{'library':body.data.library.filepath if body.data.library else None},'Source mesh linked, no duplicate/edit of canonical body geometry')
 points,_,_=evaluated(body);record('fixture_floor_clearance',points[:,2].min()>=-.002,{'minimum_body_z_m':float(points[:,2].min())},'No floor penetration beyond2mm diagnostic threshold; final sole support remains manual review')
 # Exact evaluated surface crossing count with linked bench components. Contact/interior containment still needs manual review.
 bodyeval=body.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=bodyeval.to_mesh();tree=BVHTree.FromPolygons([bodyeval.matrix_world@v.co for v in mesh.vertices],[p.vertices[:] for p in mesh.polygons]);bodyeval.to_mesh_clear();bench=bpy.data.objects['bench_reference'];crossings={};bodylo=points.min(axis=0);bodyhi=points.max(axis=0)
 for obj in bench.instance_collection.all_objects:
  if obj.type!='MESH':continue
  e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();mat=bench.matrix_world@obj.matrix_world;verts=[mat@v.co for v in me.vertices];ps=np.array([p[:] for p in verts])
  if np.all(ps.max(axis=0)>=bodylo) and np.all(ps.min(axis=0)<=bodyhi):
   bt=BVHTree.FromPolygons(verts,[p.vertices[:] for p in me.polygons]);overlap=tree.overlap(bt)
   if overlap:
    centers=np.array([np.mean([points[i] for i in body.data.polygons[a].vertices],axis=0) for a,b in overlap]);crossings[obj.name]={'pairs':len(overlap),'body_centroid_min_m':centers.min(axis=0).tolist(),'body_centroid_max_m':centers.max(axis=0).tolist()}
  e.to_mesh_clear()
 record('bench_fixture_surface_intersections',not crossings,crossings,'Zero evaluated body/bench triangle surface crossings; hands/bar contact separately reviewed')
 summary={s:sum(c['result']==s for c in checks) for s in ['PASS','FAIL']};write_json(A/'review-validation.json',{'date':'2026-10-16','status':'review; incomplete muscle/anatomy/deformation/export gates remain','source_sha256':before,'fixture_sha256':digest(FS),'validator_sha256':digest(Path(__file__)),'summary':summary,'checks':checks,'not_certified':['all78musclecoverage','clinicalanatomy','fullROManimationdeformation','garments','retargetingsecondcharacter','export_roundtrip','collision_free_fingergrip','productionrelease']});print('MANNEQUIN_REVIEW_CHECKS',json.dumps(summary));print('FAILURES',json.dumps([c for c in checks if c['result']=='FAIL']))
if __name__=='__main__':run()
