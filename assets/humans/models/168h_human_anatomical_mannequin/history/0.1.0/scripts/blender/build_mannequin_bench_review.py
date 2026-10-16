"""Linked technical pose fixture. Never writes approved equipment or character source."""
from pathlib import Path
import bpy,sys,math,json
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import mannequin_review_common as mc
from build_anatomical_mannequin import R,A,ID,RID,SOURCE
from barbell_20kg_common import setup,camera,digest,write_json,link_collection,instance,camera_config
FID='168h_template_mannequin_bench_press';F=R/'scenes/templates'/FID;FS=F/(FID+'.blend')
BID='168h_equipment_flat_bench';BAR='168h_equipment_olympic_barbell_20kg'
def build():
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name=FID;setup(s);s.display.shading.color_type='VERTEX'
 c=link_collection(SOURCE,ID);inst=instance(s,c,'mannequin_link_reference');bpy.context.view_layer.update()
 override=c.override_hierarchy_create(s,bpy.context.view_layer,reference=inst,do_fully_editable=True)
 if inst.name in bpy.data.objects:bpy.data.objects.remove(inst,do_unlink=True)
 if override.name not in s.collection.children:s.collection.children.link(override)
 mapping={o.override_library.reference.name:o for o in override.all_objects if o.override_library}
 mc.MAPPING=mapping;root=mapping[ID+'__root'];solver=mapping[RID+'__armature_solver'];body=mapping[ID+'__mesh_body']
 # Local shading drivers must address the local overridden root, not the linked source.
 for o in [body,mapping[ID+'__mesh_vastus_intermedius_l']]:
  for mod in o.modifiers:
   if mod.type=='NODES':
    mod.node_group=mod.node_group.copy()
    if mod.node_group.animation_data:
     for driver in mod.node_group.animation_data.drivers:
      for var in driver.driver.variables:
       for t in var.targets:
        if t.id and t.id.name==ID+'__root':t.id=root
 mc.neutral()
 root.matrix_world=Matrix.Translation((0,-1.56,.568))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Rotation(math.pi/2,4,'X');mc.update()
 # Place back just above the actual pad surface, measured from the source body.
 local_points=[v.co for v in body.data.vertices if .70<v.co.z<1.70 and abs(v.co.x)<.13]
 lower=min(v.y for v in local_points);root.location.z=.4572-lower+.0003;mc.update()
 bench_col=link_collection(R/'assets/equipment/benches'/BID/(BID+'.blend'),BID);bench=instance(s,bench_col,'bench_reference',Matrix.Translation(bench_col.instance_offset))
 bar_col=link_collection(R/'assets/equipment/free_weights'/BAR/(BAR+'.blend'),BAR);bar=instance(s,bar_col,'barbell_reference',Matrix.Translation((0,-.07,.95))@Matrix.Translation(bar_col.instance_offset))
 desired={};hand_orientation=Matrix.Rotation(math.pi,4,'Z')
 for side,sign in [('l',-1),('r',1)]:
  grip=Vector((sign*.34,-.07,.95));wrist=grip+Vector((0,.055,-.034));target=mapping[ID+'__control_ik_hand_'+side];target.matrix_world=Matrix.Translation(wrist)@hand_orientation
  pole=mapping[ID+'__control_pole_elbow_'+side];pole.matrix_world.translation=(sign*.52,-.14,.55)
  mc.rotate('forearm_'+side,(1,0,0),.5);root['ik_fk_arm_'+side]=1.;desired['hand_'+side]=list(wrist)
  target=mapping[ID+'__control_ik_foot_'+side];mat=solver.data.bones['foot_'+side].matrix_local.copy();mat.translation=(sign*.20,-1.02,.095);target.matrix_world=mat;pole=mapping[ID+'__control_pole_knee_'+side];pole.matrix_world.translation=(sign*.20,-1.4,.50);mc.rotate('shin_'+side,(1,0,0),-.5);root['ik_fk_leg_'+side]=1.;desired['foot_'+side]=[sign*.20,-1.02,.095]
  mc.grip(side,1.4)
 mc.highlight('muscle_pectoralis_major_l');mc.highlight('muscle_pectoralis_major_r');mc.highlight('muscle_triceps_brachii_l','secondary');mc.highlight('muscle_triceps_brachii_r','secondary');mc.update()
 contacts={}
 for side in ['l','r']:
  arm=mapping[ID+'__armature_deform'];contacts[side]={'wrist_actual_m':list((arm.matrix_world@arm.pose.bones['hand_'+side].matrix).translation),'wrist_target_m':desired['hand_'+side],'grip_anchor_actual_m':list(mapping[ID+'__anchor_hand_grip_'+side].matrix_world.translation),'expected_bar_station_m':[(-1 if side=='l' else 1)*.34,-.07,.95]}
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(F))
 for obj in override.all_objects:
  if obj.type=='ARMATURE':obj.hide_set(True)
 records={}
 views={'assembled_three_quarter':((2.8,3.2,2.3),(0,-.32,.55),2.8),'assembled_side':((3,0,1.1),(0,-.38,.55),2.65),'grip_detail':((-.75,1.2,1.6),(-.34,-.07,.95),.43)}
 for key,(pos,target,scale) in views.items():
  s.camera=camera(s,FID+'__camera_'+key,pos,target,scale);p=F/'previews'/f'{FID}__{key}__bench_press_review.png';p.parent.mkdir(exist_ok=True);s.render.filepath=str(p);bpy.ops.render.render(write_still=True);records[key]={**camera_config(s.camera,p,target,'preliminary bench press'),'sha256':digest(p)}
 s.camera=bpy.data.objects[FID+'__camera_assembled_three_quarter'];s.render.filepath=records['assembled_three_quarter']['path']
 bpy.ops.wm.save_as_mainfile(filepath=str(FS),compress=True,relative_remap=False)
 write_json(F/'build-record.json',{'source_sha256':digest(FS),'character_sha256':digest(SOURCE),'contacts':contacts,'bench_pad_top_m':.4572,'character_root_matrix':[[float(v) for v in row] for row in root.matrix_world],'body_mesh_linked':bool(body.data.library),'body_mesh_library':body.data.library.filepath if body.data.library else None,'views':records,'status':'review; contact/deformation requires validation'})
 print('FIXTURE_CONTACTS',json.dumps(contacts))
if __name__=='__main__':build()
