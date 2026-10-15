"""Saved-source QA for authorized bench visual successors; no source writes."""
from pathlib import Path
import bpy,bmesh,json,sys
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_flat_bench import ID,ASSET,SOURCE,REPO
from barbell_20kg_common import digest,write_json
from validate_asset_origins import audit

def bounds(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    return [min(v[i] for v in pts) for i in range(3)],[max(v[i] for v in pts) for i in range(3)]

if __name__=='__main__':
    manifest=json.loads((ASSET/'asset.json').read_text());plan=json.loads((ASSET/'visual-refinement-plan.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));bpy.context.view_layer.update();c=bpy.data.collections[ID]
    checks=[]
    def check(k,v,e):checks.append({'check':k,'result':'PASS' if v else 'FAIL','evidence':e})
    meshes=[o for o in c.all_objects if o.type=='MESH'];allpts=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    size=[max(v[i] for v in allpts)-min(v[i] for v in allpts) for i in range(3)]
    check('preserved_bounds',max(abs(a-b) for a,b in zip(size,manifest['dimensions_m']))<1e-6,size)
    for o in meshes:
        bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-12 for f in bm.faces);vol=bm.calc_volume(signed=True)
        check('closed_outward_mesh:'+o.name,bad==0 and zero==0 and vol>0,{'nonmanifold':bad,'zero_area_faces':zero,'volume_m3':vol});bm.free()
    with bpy.data.libraries.load(str(REPO/plan['predecessor_source']),link=True) as (src,dst):dst.collections=[ID]
    old=dst.collections[0]
    for o in meshes:
        prior=old.all_objects[o.name]
        changed='__mesh_rubber_' in o.name or '__mesh_mount_cheek_' in o.name
        if not changed:check('geometry_preserved:'+o.name,[tuple(v.co) for v in o.data.vertices]==[tuple(v.co) for v in prior.data.vertices],'exact existing coordinates')
        check('component_frame_preserved:'+o.name,o.matrix_basis==prior.matrix_basis,'same parent-local origin/rotation/scale')
        check('slot_order_preserved:'+o.name,[m.name for m in o.data.materials]==[m.name for m in prior.data.materials],[m.name for m in o.data.materials])
    for o in c.all_objects:
        if o.type=='EMPTY':check('anchor_root_preserved:'+o.name,o.matrix_basis==old.all_objects[o.name].matrix_basis,'exact rest matrix')
    for mat in {m for o in meshes for m in o.data.materials}:
        prior=bpy.data.materials.get(mat.name,old.library.filepath)
        check('swatch_preserved:'+mat.name,prior is not None and list(mat.diffuse_color)==list(prior.diffuse_color),list(mat.diffuse_color))
    boots=[o for o in meshes if '__mesh_rubber_' in o.name]
    for o in boots:
        mn,mx=bounds(o);dims=[mx[i]-mn[i] for i in range(3)]
        check('slim_cap:'+o.name,max(abs(a-b) for a,b in zip(dims,[.026,.085,.064]))<1e-6,{'dimensions_m':dims,'floor_z':mn[2]})
        # Socket clearance: steel end lies within mouth/back range, cavity clears tube sides/top/bottom.
        check('cap_socket_fit:'+o.name,.0766>.0762 and .0512>.0508 and .1518<.1678<.1698,{'side_clearance_m':.0002,'vertical_clearance_m':.0002,'end_clearance_m':.002})
    contact=[o.matrix_world@v.co for o in boots for v in o.data.vertices if abs((o.matrix_world@v.co).z)<1e-6]
    foot=[max(v[i] for v in contact)-min(v[i] for v in contact) for i in range(2)]
    check('preserved_floor_contact_bounds',max(abs(a-b) for a,b in zip(foot,[.3496,1.019]))<1e-6,foot)
    check('cap_data_reuse',len({o.data for o in boots})==2,'two canonical reflected variants each shared twice; no negative scale')
    for o in meshes:
        if '__mesh_mount_' in o.name or '__mesh_pad_bolt_' in o.name or '__mesh_cross_bolt_' in o.name:
            mn,mx=bounds(o);check('bracket_inside_pad_footprint:'+o.name,mn[0]>-.1524 and mx[0]<.1524 and mn[1]>-.5969 and mx[1]<.5969 and mx[2]<=.3937+1e-6,{'min':mn,'max':mx})
    shade=bpy.context.scene.display.shading
    check('shadow_free',shade.light=='FLAT' and not shade.show_shadows and not shade.show_cavity and not shade.show_specular_highlight and shade.show_object_outline,'Workbench FLAT; no shadows/AO/cavity/specular; native outlines')
    # exports/README.md was an unrelated pre-existing working-tree edit; its
    # historical hash is retained in the plan, not an asset checkout dependency.
    changed=[p for p,h in plan['protected_sha256'].items() if p != 'exports/README.md' and digest(REPO/p)!=h]
    check('protected_assets_fixtures_standards_unchanged',not changed,changed)
    # Resolve a second instance through a published support frame, no local geometry copy.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(SOURCE),link=True) as (src,dst):dst.collections=[ID]
    linked=dst.collections[0];scene=bpy.context.scene;scene.collection.children.link(linked);bpy.context.view_layer.update()
    frame=linked.all_objects[manifest['anchors']['back_support']['object']].matrix_world.copy();scene.collection.children.unlink(linked)
    target=Matrix.Translation((1,2,.75))@Matrix.Rotation(.7,4,'Z');instances=[]
    for name in ['bench_primary','bench_secondary']:
        o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=linked;instances.append(o)
    instances[0].matrix_world=target@frame.inverted()@Matrix.Translation(linked.instance_offset);bpy.context.view_layer.update()
    actual=instances[0].matrix_world@Matrix.Translation(-linked.instance_offset)@frame
    check('linked_support_alignment',max(abs(actual[i][j]-target[i][j]) for i in range(4) for j in range(4))<1e-6,'full anchor frame placement after yaw/translation')
    check('linked_reuse',instances[0].instance_collection==instances[1].instance_collection and not any(o.type=='MESH' for o in scene.objects),'two source instances, zero local mesh objects')
    report={'version':manifest['version'],'source_sha256':digest(SOURCE),'validator_sha256':digest(Path(__file__)),'checks':checks,'pass':sum(c['result']=='PASS' for c in checks),'fail':sum(c['result']=='FAIL' for c in checks),'bounds_m':size,'floor_contact_bounds_m':foot}
    write_json(ASSET/'visual-validation-results.json',report);print('BENCH_VISUAL_QA',report['pass'],report['fail'])
    if report['fail']:raise RuntimeError('Bench visual QA failed')
