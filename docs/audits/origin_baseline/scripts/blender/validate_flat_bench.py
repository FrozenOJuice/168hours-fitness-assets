"""Bench-specific saved-source QA. MIT code; does not approve artwork or hardware."""
from pathlib import Path
import bpy, bmesh, sys, json, math
from mathutils import Matrix, Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_flat_bench import REPO,ID,ASSET,SOURCE
from barbell_20kg_common import digest,write_json

results=[]
def check(key,condition,evidence):
    results.append({'check':key,'result':'PASS' if condition else 'FAIL','evidence':evidence})

def bounds(objects):
    points=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
    return [min(v[i] for v in points) for i in range(3)],[max(v[i] for v in points) for i in range(3)]

def close(a,b,t=1e-6):return max(abs(x-y) for x,y in zip(a,b))<t

def run(source=SOURCE,output=None):
    bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    manifest=json.loads((ASSET/'asset.json').read_text())
    scene=bpy.context.scene;col=bpy.data.collections.get(ID);root=bpy.data.objects.get(ID+'__root')
    meshes=[o for o in col.all_objects if o.type=='MESH'];lo,hi=bounds(meshes)
    measurements={'bounds_min_m':lo,'bounds_max_m':hi,'bounds_size_m':[hi[i]-lo[i] for i in range(3)],'components':{}}
    check('overall_bounds',close(measurements['bounds_size_m'],manifest['dimensions_m']),measurements['bounds_size_m'])
    check('floor_center',close(lo[:2],[-hi[0],-hi[1]]) and abs(lo[2])<1e-6 and close(root.location,(0,0,0)),{'min':lo,'max':hi,'root':list(root.location)})
    check('meter_units',scene.unit_settings.system=='METRIC' and scene.unit_settings.scale_length==1,scene.unit_settings.system)
    check('collection_contract',len(col.children)==2 and {c.name for c in col.children}=={ID+'__geo',ID+'__anchors'},[c.name for c in col.children])
    check('naming_and_scope',len(meshes)==manifest['components']['mesh_objects'] and all(o.name.startswith(ID+'__') and not o.name[-4:].startswith('.') for o in col.all_objects),[o.name for o in col.all_objects])
    def descendant(o):
        while o.parent:
            o=o.parent
            if o==root:return True
        return False
    check('root_hierarchy',all(o==root or descendant(o) for o in col.all_objects),'every asset object descends from identity root')
    check('rigid_normalized_transforms',all(close(o.scale,(1,1,1)) and close(o.rotation_euler,(0,0,0)) for o in col.all_objects),'unit positive scale, zero rotations; local translations allowed')
    check('no_rigs_or_unapplied_modifiers',all(not o.modifiers for o in meshes) and not any(o.type=='ARMATURE' for o in col.all_objects),'fixed flat rigid components')
    for o in meshes:
        mn,mx=bounds([o]);measurements['components'][o.name]={'min_m':mn,'max_m':mx,'dimensions_m':[mx[i]-mn[i] for i in range(3)],'vertices':len(o.data.vertices),'faces':len(o.data.polygons)}
        bm=bmesh.new();bm.from_mesh(o.data)
        invalid=sum(not e.is_manifold for e in bm.edges);degenerate=sum(f.calc_area()<1e-12 for f in bm.faces)
        negative=any(not math.isfinite(x) for v in bm.verts for x in v.co)
        check('closed_nondegenerate_'+o.name.split('__mesh_')[-1],invalid==0 and degenerate==0 and not negative and bm.calc_volume(signed=True)>0,{'nonmanifold_edges':invalid,'zero_area_faces':degenerate,'volume_m3':bm.calc_volume(signed=True)})
        bm.free()
    pad=bpy.data.objects[ID+'__mesh_pad'];padlo,padhi=bounds([pad])
    check('pad_dimensions',close([padhi[i]-padlo[i] for i in range(3)],[.3048,1.1938,.0635]) and abs(padhi[2]-.4572)<1e-6,{'min':padlo,'max':padhi})
    foam_gaps={o.name:padlo[2]-bounds([o])[1][2] for o in meshes if o!=pad and not o.name.endswith('__mesh_upholstery_seam')}
    check('no_frame_foam_penetration',min(foam_gaps.values())>=-1e-6,{'clearance_to_foam_bottom_m':foam_gaps,'intentional_support_substrate_contact':True})
    boots=[o for o in meshes if '__mesh_rubber_' in o.name];blo,bhi=bounds(boots)
    check('four_floor_contacts',len(boots)==4 and all(abs(bounds([o])[0][2])<1e-6 for o in boots),{o.name:bounds([o])[0][2] for o in boots})
    check('ground_footprint',close([bhi[0]-blo[0],bhi[1]-blo[1]],[.3556,1.025]),{'min':blo,'max':bhi})
    contact=[o.matrix_world@v.co for o in boots for v in o.data.vertices if abs((o.matrix_world@v.co).z)<1e-6]
    contact_bounds=[max(v[i] for v in contact)-min(v[i] for v in contact) for i in range(2)]
    measurements['rubber_outer_envelope_xy_m']=[bhi[0]-blo[0],bhi[1]-blo[1]]
    measurements['floor_contact_bounds_xy_m']=contact_bounds
    check('actual_rubber_floor_contact_bounds',close(contact_bounds,manifest['physical_properties'].get('floor_contact_bounds_m',contact_bounds)),{'xy_m':contact_bounds,'note':'contact patch distinct from wider rounded rubber envelope'})
    check('shared_boot_mesh',len({o.data for o in boots})==1,'four boots share one data block')
    for kind in ['foot','mount_rail']:
        pair=[o for o in meshes if o.name.startswith(ID+'__mesh_'+kind+'_')]
        check('shared_'+kind,len(pair)==2 and pair[0].data==pair[1].data,[o.name for o in pair])
    check('material_roles',all(len(o.data.materials)==3 and all(m.name.startswith(ID+'__material_') for m in o.data.materials) for o in meshes),'ordered body/top/side variants; pad top/side/edge; asset-local semantic roles in manifest')
    check('no_external_art_dependencies',len(bpy.data.libraries)==0 and not any(i.source=='FILE' for i in bpy.data.images) and len(bpy.data.fonts)<=1,'no linked assets, file textures or custom fonts')
    check('shadow_free_preset',scene.render.engine=='BLENDER_WORKBENCH' and scene.display.shading.light=='FLAT' and not scene.display.shading.show_shadows and not scene.display.shading.show_cavity and not scene.display.shading.show_specular_highlight and scene.display.shading.show_object_outline,'Workbench FLAT, outlines; shadows/cavity/specular off; no AO lighting')
    check('no_lights_or_ground',not any(o.type=='LIGHT' for o in scene.objects) and all(o.name in col.all_objects for o in scene.objects if o.type=='MESH'),'no light objects or ground plane')
    for key,entry in manifest['anchors'].items():
        o=col.all_objects.get(entry['object'])
        check('anchor_'+key,o is not None and close(o.matrix_world.translation,entry['position_m']) and close(o.rotation_euler,entry['rotation_euler_xyz_radians']),entry)
    for key in ['pad_center','seat_center','back_support','head_support']:
        o=col.all_objects[ID+'__anchor_'+key];pos=o.matrix_world.translation.copy()
        hit,loc,norm,index=pad.ray_cast(pos+Vector((0,0,.1)),Vector((0,0,-1)))
        check('flat_support_'+key,hit and abs(loc.z-pos.z)<1e-6 and close(norm,(0,0,1)),{'anchor':list(pos),'hit':list(loc),'normal':list(norm)})
    protected=json.loads((ASSET/'standards-snapshot.json').read_text())['protected_files']
    altered=[p for p,h in protected.items() if not (REPO/p).is_file() or digest(REPO/p)!=h]
    check('approved_assets_and_shared_standards_unchanged',not altered,{'changed_paths':altered,'checked_files':len(protected)})
    if (ASSET/'refinement-record.json').is_file():
        record=json.loads((ASSET/'refinement-record.json').read_text())
        plan=json.loads((ASSET/'refinement-plan.json').read_text())
        predecessor=REPO/plan['prior_snapshot']/(ID+'.blend')
        check('refinement_source_record',digest(source)==record['source_sha256'] and digest(predecessor)==plan['predecessor_sha256'],{'current':digest(source),'predecessor':digest(predecessor)})
        with bpy.data.libraries.load(str(predecessor),link=True) as (src,dst):dst.collections=[ID]
        prior=dst.collections[0]
        unchanged=[];interface=[];identity=[]
        for old in prior.all_objects:
            new=col.all_objects.get(old.name)
            identity.append(new is not None and (new.type!='MESH' or new.data.name==old.data.name))
            if old.type=='EMPTY':interface.append(new is not None and new.matrix_basis==old.matrix_basis)
            if old.type=='MESH' and not (old.name.endswith('__mesh_pad') or '__mesh_rubber_' in old.name):
                unchanged.append(new is not None and len(old.data.vertices)==len(new.data.vertices) and all(a.co==b.co for a,b in zip(old.data.vertices,new.data.vertices)) and list(new.data.polygons[0].vertices)==list(old.data.polygons[0].vertices))
        check('original_object_and_data_names_retained',all(identity) and record['original_objects_and_data_identity_preserved'],{'original_objects':len(identity),'in_process_identity_assertion':True})
        check('original_main_frame_and_substrate_unchanged',all(unchanged),{'compared_meshes':len(unchanged),'method':'exact saved predecessor/current vertex comparison'})
        check('original_root_and_anchor_frames_unchanged',all(interface),{'compared_frames':len(interface)})
        oldpad=prior.all_objects[ID+'__mesh_pad']
        check('original_pad_topology_retained',len(pad.data.vertices)==len(oldpad.data.vertices) and [list(p.vertices) for p in pad.data.polygons]==[list(p.vertices) for p in oldpad.data.polygons],'vertex coordinates refined, original topology retained')
        seam=col.all_objects[ID+'__mesh_upholstery_seam'];slo,shi=bounds([seam])
        check('upholstery_within_nominal_pad_envelope',all(slo[i]>=padlo[i]-1e-6 and shi[i]<=padhi[i]+1e-6 for i in range(3)),{'seam_min_m':slo,'seam_max_m':shi})
        check('declared_material_slot_order',all([m.name.split('__material_')[1] for m in o.data.materials]==manifest['component_material_slot_order'][o.name] for o in meshes),'all component slots match manifest including added details; original role order retained')
    # Separate unsaved linking fixture: two instances, anchor-mapped rotated placement, no local mesh copies.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(source),link=True) as (src,dst):dst.collections=[ID]
    linked=dst.collections[0];a=linked.all_objects[ID+'__anchor_back_support']
    fixture=bpy.context.scene
    # Evaluate freshly linked hierarchy before reading matrix_world; unloaded data is initially identity.
    fixture.collection.children.link(linked);bpy.context.view_layer.update()
    frame=a.matrix_world.copy();fixture.collection.children.unlink(linked)
    target=Matrix.Translation((1,2,.75))@Matrix.Rotation(math.pi/2,4,'Z')
    inst=bpy.data.objects.new('bench_primary',None);fixture.collection.objects.link(inst);inst.instance_type='COLLECTION';inst.instance_collection=linked;inst.matrix_world=target@frame.inverted()
    other=bpy.data.objects.new('bench_secondary',None);fixture.collection.objects.link(other);other.instance_type='COLLECTION';other.instance_collection=linked;other.location=(-2,0,0)
    bpy.context.view_layer.update()
    actual=inst.matrix_world@frame
    check('linked_anchor_alignment',max(abs(actual[i][j]-target[i][j]) for i in range(4) for j in range(4))<1e-6,{'target_translation_m':list(target.translation),'actual_translation_m':list(actual.translation),'yaw_degrees':90})
    check('two_instances_no_geometry_duplication',inst.instance_collection==other.instance_collection and all(o.library is not None for o in linked.all_objects) and not any(o.type=='MESH' for o in fixture.objects),'two collection instances; original data remains linked; no local meshes')
    # Resolve source after moving to a self-contained temporary checkout-style tree.
    check('relocatable_no_hidden_dependencies',source.is_file() and len(bpy.data.libraries)==1,'source loads from supplied path; no external geometry/material/texture dependencies; fresh Git/LFS clone not claimed')
    report={'asset_id':ID,'version':manifest['version'],'source_sha256':digest(source),'validator_sha256':digest(Path(__file__)),'blender_version':bpy.app.version_string,'measurements':measurements,'checks':results,'summary':{'pass':sum(c['result']=='PASS' for c in results),'fail':sum(c['result']=='FAIL' for c in results)},'untested':['human pose/support','rack clearance','alternate bench replacement','physical mass/load strength','fresh committed Git/LFS checkout']}
    write_json(output or ASSET/'validation-results.json',report)
    print('BENCH_QA',json.dumps(report['summary']))
    if report['summary']['fail']:raise RuntimeError('Bench QA failed')

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    run(Path(args[0]) if args else SOURCE,Path(args[1]) if len(args)>1 else None)
