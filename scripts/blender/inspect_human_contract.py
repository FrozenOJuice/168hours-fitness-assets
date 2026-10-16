"""Observe an existing saved character read-only; output JSON, never build or save.

Blender --background <character.blend> --python this.py -- --manifest ... --output ...
The current foundation has no character; only --help is exercised until creation
is explicitly authorized. The export/visual/retarget gates require separate proof.
"""
from pathlib import Path
import argparse, sys, json, math
import bpy
from mathutils import Vector
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scripts/pipeline'))
from validate_human_contract import read, sha, rest_fingerprint, character_checks, report, registry_checks

def run():
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);p.add_argument('--rest-profile-output');p.add_argument('--release',action='store_true')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    registry=registry_checks()
    if any(row['result']=='FAIL' for row in registry):raise ValueError('Human V1 registry/schema pin validation failed; resolve drift before inspection')
    mp=Path(args.manifest).resolve();m=read(mp);asset=read(mp.parent/m['asset_manifest'])
    source=Path(bpy.data.filepath)
    if not source.is_file() or source.resolve()!=(R/asset['source']).resolve():raise ValueError('Open the declared saved source; source mismatch')
    if bpy.data.is_dirty:raise ValueError('Save/reopen the intended source before read-only inspection; unsaved changes are not source-hash evidence')
    reserved={source.resolve(),mp,(mp.parent/m['asset_manifest']).resolve()}
    outputs=[Path(args.output).resolve(),Path(args.output).with_suffix('.validation.json').resolve()]
    if args.rest_profile_output:outputs.append(Path(args.rest_profile_output).resolve())
    if len(set(outputs))!=len(outputs) or any(o.suffix!='.json' or o in reserved for o in outputs):raise ValueError('Outputs must be distinct JSON sidecars, never source/metadata files')
    before=sha(source);root=bpy.data.objects[asset['root']];col=bpy.data.collections[asset['collection']];arm=bpy.data.objects[m['armature']]
    if arm.type!='ARMATURE':raise ValueError('Declared skeleton is not an armature')
    inverse=root.matrix_world.inverted();frame=inverse@arm.matrix_world
    def matrix(o):return [list(row) for row in o.matrix_world]
    def desc(o):
        seen=set()
        while o and o not in seen:
            if o==root:return True
            seen.add(o);o=o.parent
        return False
    def resolve(ref):
        obj=bpy.data.objects.get(ref['object'])
        if obj is None:return None
        if ref.get('property'):
            value=obj.get(ref['property'])
            if type(value) not in [int,float] or not math.isfinite(value):return None
            if ref['property'].startswith('ik_fk_') and not 0<=value<=1:return None
            return obj
        return obj.pose.bones.get(ref['bone']) if ref['bone'] and obj.type=='ARMATURE' else obj if ref['bone'] is None else None
    def constraint_target(c,ref,pole=False):
        return getattr(c,'pole_target' if pole else 'target',None)==bpy.data.objects.get(ref['object']) and getattr(c,'pole_subtarget' if pole else 'subtarget','')==(ref['bone'] or '')
    bpy.context.view_layer.update();evaluated_arm=arm.evaluated_get(bpy.context.evaluated_depsgraph_get());bones=[]
    for b in arm.data.bones:
        pose=arm.pose.bones[b.name];solved=evaluated_arm.pose.bones[b.name]
        identity=all(abs(pose.matrix_basis[i][j]-(1 if i==j else 0))<1e-6 and abs(solved.matrix[i][j]-b.matrix_local[i][j])<1e-6 for i in range(4) for j in range(4))
        bones.append({'name':b.name,'parent':b.parent.name if b.parent else None,'deform':b.use_deform,'connected':b.use_connect,'head_m':list(frame@b.head_local),'tail_m':list(frame@b.tail_local),'z_axis':list((frame.to_3x3()@b.matrix_local.to_3x3().col[2]).normalized()),'pose_identity':identity})
    points=[];skinning=True;deps=bpy.context.evaluated_depsgraph_get();core={b.name for b in arm.data.bones if b.use_deform}
    for name in m['body_objects']:
        obj=bpy.data.objects.get(name)
        if obj is None or obj.type!='MESH':raise ValueError('Missing body mesh:'+name)
        modifiers=[x for x in obj.modifiers if x.type=='ARMATURE' and x.show_viewport and x.show_render]
        skinning=skinning and len(modifiers)==1 and modifiers[0].object==arm
        group_names={g.index:g.name for g in obj.vertex_groups}
        for v in obj.data.vertices:
            weights=[g.weight for g in v.groups if group_names[g.group] in core]
            root_weights=[g.weight for g in v.groups if group_names[g.group]=='root']
            skinning=skinning and abs(sum(weights)-1)<=1e-4 and all(0<=w<=1 for w in weights) and not any(root_weights)
        evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh()
        points.extend(inverse@(evaluated.matrix_world@v.co) for v in mesh.vertices);evaluated.to_mesh_clear()
    if not points:raise ValueError('No measured body vertices')
    anchors=[]
    for key,e in m['anchors'].items():
        obj=bpy.data.objects.get(e['object']);local=inverse@obj.matrix_world if obj else None
        owner=obj.parent_bone if obj and obj.parent_type=='BONE' and obj.parent==arm else None
        anchors.append({'key':key,'object':e['object'],'bone':owner,'position_m':list(local.translation) if local else [0,0,0],'rotation_quaternion_wxyz':list(local.to_quaternion()) if local else [1,0,0,0],'exists':bool(obj and desc(obj))})
    muscles=[]
    for mid,e in m['muscle_bindings'].items():
        obj=bpy.data.objects.get(e['object']);group=obj.vertex_groups.get(e['vertex_group']) if obj and obj.type=='MESH' else None
        weights=[]
        if group:
            for v in obj.data.vertices:
                weights.extend(g.weight for g in v.groups if g.group==group.index)
        muscles.append({'id':mid,'object':e['object'],'vertex_group':e['vertex_group'],'positive_vertices':sum(w>0 for w in weights),'weight_min':min(weights,default=0),'weight_max':max(weights,default=0),'primary_exists':e['primary_property'] in root,'secondary_exists':e['secondary_property'] in root,'primary':float(root.get(e['primary_property'],0)),'secondary':float(root.get(e['secondary_property'],0))})
    ik_valid=True
    for key,ref in m['solver_bindings'].items():
        owner=resolve(ref);controls=m['controls'];pole='pole_elbow_' if key.startswith('ik_hand_') else 'pole_knee_';pole+=key[-1]
        candidates=[c for c in owner.constraints if c.type=='IK'] if owner else []
        ik_valid=ik_valid and key in controls and pole in controls and any(c.chain_count==2 and 0<=c.influence<=1 and not c.mute and not c.use_stretch and constraint_target(c,controls[key]) and constraint_target(c,controls[pole],True) for c in candidates)
    limits_valid=True
    for name,ref in m['joint_limit_bindings'].items():
        owner=resolve(ref);expected=m['joint_limits'].get(name);constraints=[c for c in owner.constraints if c.type=='LIMIT_ROTATION' and c.owner_space=='LOCAL' and not c.mute and c.influence==1] if owner else []
        limits_valid=limits_valid and bool(expected) and any(all(getattr(c,'use_limit_'+ax) and abs(getattr(c,'min_'+ax)-expected['min_radians'][i])<1e-6 and abs(getattr(c,'max_'+ax)-expected['max_radians'][i])<1e-6 for i,ax in enumerate('xyz')) for c in constraints)
    rigid=[o for o in col.all_objects if o.type in ['MESH','ARMATURE']]
    normalized=all(all(abs(v-1)<1e-6 for v in o.matrix_basis.to_scale()) and o.matrix_basis.to_quaternion().angle<1e-6 and o.matrix_basis.to_3x3().determinant()>0 for o in rigid)
    snapshot={'contract':'168h_human_snapshot@1.0.0','source_sha256':before,'units':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length,'root_matrix':matrix(root),'armature_matrix':matrix(arm),'collection_offset_m':list(col.instance_offset),'body_min_z_m':min(p.z for p in points),'body_height_m':max(p.z for p in points)-min(p.z for p in points),'hierarchy_valid':all(desc(o) for o in col.all_objects),'transforms_normalized':normalized,'skinning_valid':bool(skinning),'bones':bones,'anchors':anchors,'resolved_controls':[k for k,ref in m['controls'].items() if resolve(ref) is not None],'muscles':muscles,'clothing_present':any(bpy.data.objects.get(n) is not None for n in m['clothing_objects']),'rest_profile_sha256':rest_fingerprint(bones),'observer':'blender_read_only/'+bpy.app.version_string,'ik_valid':bool(ik_valid),'joint_constraints_valid':bool(limits_valid)}
    if args.rest_profile_output:
        fields=['name','parent','deform','connected','head_m','tail_m','z_axis'];profile=[{k:b[k] for k in fields} for b in sorted(bones,key=lambda b:b['name'])]
        Path(args.rest_profile_output).write_text(json.dumps(profile,sort_keys=True,separators=(',',':'),allow_nan=False))
    Path(args.output).write_text(json.dumps(snapshot,indent=2,allow_nan=False)+'\n')
    result=report(registry+character_checks(m,snapshot,args.release,mp.parent));Path(args.output).with_suffix('.validation.json').write_text(json.dumps(result,indent=2)+'\n')
    assert sha(source)==before,'Source bytes unexpectedly changed'
    print('HUMAN_INSPECTION',result['pass'],result['fail'])
    if result['fail']:raise SystemExit(1)

if __name__=='__main__':run()
