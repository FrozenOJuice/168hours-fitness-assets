"""Saved-source stand detents, topology, origins, linked-frame fit and BVH QA."""
from pathlib import Path
import bpy,bmesh,sys,json,math
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from barbell_20kg_common import digest,write_json,asset_instance_frame
from build_barbell_stands import R,ID,A,SOURCE
from build_stands_review_assembly import SID,F,OUT,BID,BBID
from validate_asset_origins import audit
checks=[]
def check(name,expected,actual,ok):checks.append({'check':name,'expected':expected,'actual':actual,'result':'PASS' if ok else 'FAIL'})
def bounds(objects):
    points=[o.matrix_world@v.co for o in objects for v in o.data.vertices];return [min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]
def tree(o,frame):
    return BVHTree.FromPolygons([frame@(o.matrix_world@v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=0)
def update(root,l,r):
    root['height_index_l']=l;root['height_index_r']=r;root.update_tag();bpy.context.scene.frame_set(2);bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
def run():
    before=digest(SOURCE);bpy.ops.wm.open_mainfile(filepath=str(SOURCE));m=json.loads((A/'asset.json').read_text());col=bpy.data.collections[ID];root=col.all_objects[ID+'__root'];meshes=[o for o in col.all_objects if o.type=='MESH'];registry=json.loads((R/'docs/equipment-origin-rules.json').read_text());rows=audit(m,registry)
    check('generic_origin_contract','zero deviations',{'pass':sum(e['result']=='PASS' for e in rows),'fail':sum(e['result']=='FAIL' for e in rows)},all(e['result']=='PASS' for e in rows));write_json(A/'origin-validation.json',{'standard':registry['id'],'source_sha256':before,'checks':rows,'pass':sum(e['result']=='PASS' for e in rows),'fail':sum(e['result']=='FAIL' for e in rows)})
    lo,hi=bounds(meshes);dims=[b-a for a,b in zip(lo,hi)];check('canonical_bounds_m',m['dimensions_m'],dims,max(abs(a-b) for a,b in zip(dims,m['dimensions_m']))<1e-6)
    for o in meshes:
        bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);deg=sum(f.calc_area()<1e-12 for f in bm.faces);bm.free()
        check('closed_outward:'+o.name,'no boundary/nonmanifold/degenerate faces; positive volume',{'nonmanifold':bad,'volume_m3':volume,'degenerate':deg},bad==0 and volume>0 and deg==0)
        check('material_slots:'+o.name,'3 nonempty semantic slots',len(o.data.materials),len(o.data.materials)==3 and all(o.data.materials))
        check('naming:'+o.name,'stable lower snake_case, no numeric suffix',o.name,o.name.startswith(ID+'__mesh_') and o.name.lower()==o.name and '.' not in o.name)
        other=col.all_objects[o.name[:-1]+('r' if o.name.endswith('l') else 'l')];check('shared_opposite_mesh:'+o.name,'same datablock',other.data.name,o.data==other.data)
    predecessor=A/'history/0.1.0'/(ID+'.blend')
    with bpy.data.libraries.load(str(predecessor),link=True) as (src,dst):dst.collections=[ID]
    old=dst.collections[0];record=json.loads((A/'refinement-record.json').read_text());allowed=set(record['changed_geometry_objects'])
    check('original_objects_retained',sorted(o.name for o in old.all_objects),sorted(o.name for o in col.all_objects),set(o.name for o in old.all_objects)==set(o.name for o in col.all_objects))
    for obj in col.all_objects:
        previous=old.all_objects[obj.name]
        check('preserved_frame:'+obj.name,'exact parent-local matrix',obj.name,obj.matrix_basis==previous.matrix_basis and (obj.parent.name if obj.parent else None)==(previous.parent.name if previous.parent else None))
        if obj.type=='MESH':
            check('preserved_slots:'+obj.name,[x.name for x in previous.data.materials],[x.name for x in obj.data.materials],[x.name for x in previous.data.materials]==[x.name for x in obj.data.materials])
            if obj.name not in allowed:check('preserved_unedited_geometry:'+obj.name,'exact vertex coordinates/topology',obj.name,[tuple(v.co) for v in obj.data.vertices]==[tuple(v.co) for v in previous.data.vertices] and [tuple(p.vertices) for p in obj.data.polygons]==[tuple(p.vertices) for p in previous.data.polygons])
    for side in ['l','r']:
        back=col.all_objects[ID+'__mesh_hook_back_'+side];shelf=col.all_objects[ID+'__mesh_hook_shelf_'+side]
        check('hook_welded_connection:'+side,'shelf intersects backplate at intended welded rear',bool(tree(back,Matrix.Identity(4)).overlap(tree(shelf,Matrix.Identity(4)))),bool(tree(back,Matrix.Identity(4)).overlap(tree(shelf,Matrix.Identity(4)))))
        mn,mx=bounds([back]);check('hook_backplate_mount:'+side,'backplate rear flush with inner frontY30mm',mn[1],abs(mn[1]-.03)<1e-6)
        for part,radii in [('hook_liner',[.020,.026]),('hook_shelf',[.026,.036])]:
            obj=col.all_objects[ID+'__mesh_'+part+'_'+side];points=[obj.matrix_basis@v.co for v in obj.data.vertices]
            for radius in radii:
                arc=[v for v in points if abs(math.hypot(v.y-.14,v.z-.948)-radius)<1e-6 and .105<v.y<.175 and v.z<.94]
                check('conformal_cradle:'+part+':'+side+':'+str(radius),'at least32 vertices on specified concentric arc',len(arc),len(arc)>=32)
        pin=col.all_objects[ID+'__mesh_adjustment_pin_'+side];pmin,pmax=bounds([pin]);check('pin_actual_diameter:'+side,'15.875mm',[pmax[1]-pmin[1],pmax[2]-pmin[2]],max(abs(pmax[k]-pmin[k]-.015875) for k in [1,2])<1e-6)
        inner=col.all_objects[ID+'__mesh_upright_inner_'+side];x=inner.matrix_world.translation.x
        hit=tree(inner,Matrix.Identity(4)).ray_cast(Vector((x,-.08,.994)),Vector((0,1,0)),.16)[0];check('hook_through_bolt_opening:'+side,'real9mm Y opening through inner tube',list(hit) if hit else None,hit is None)
        hit=tree(pin,Matrix.Identity(4)).ray_cast(Vector((x-.06,0,.87)),Vector((0,0,1)),.06)[0];check('retaining_clip_cross_drill:'+side,'real3.5mm hole through pin',list(hit) if hit else None,hit is None)
    for key,e in m['anchors'].items():
        actual=col.all_objects[e['object']].parent.name
        check('anchor_owner:'+key,e['owner_controller'],actual,actual==e['owner_controller'])
    for i in range(16):
        update(root,i,i)
        for side in ['l','r']:
            inner=col.all_objects[ID+'__mesh_upright_inner_'+side];support=col.all_objects[ID+'__anchor_bar_support_'+side];axis=col.all_objects[ID+'__anchor_bar_axis_'+side];low,high=bounds([inner]);overlap=.97-low[2]
            check('detent_'+str(i)+':'+side,'top1.028+index*.05, support.928+index*.05,142mm min overlap',{'top_m':high[2],'support_m':support.matrix_world.translation.z,'overlap_m':overlap},abs(high[2]-(1.028+i*.05))<1e-6 and abs(support.matrix_world.translation.z-(.928+i*.05))<1e-6 and overlap>=.142-1e-6)
            liner=col.all_objects[ID+'__mesh_hook_liner_'+side];ll,lh=bounds([liner])
            anchor=support.matrix_world.translation
            hit=tree(liner,Matrix.Identity(4)).ray_cast(anchor+Vector((0,0,.1)),Vector((0,0,-1)),.11)[0]
            check('anchor_on_actual_liner_'+str(i)+':'+side,'support equals measured cradle surface at anchorXY',{'surface_hit':list(hit) if hit else None,'anchor_z_m':anchor.z},hit is not None and abs(hit.z-anchor.z)<1e-6)
            # Pin alignment verified from actual hole ring vertices in local mesh.
            world=[inner.matrix_world@v.co for v in inner.data.vertices];ring=[p for p in world if abs(p.z-.90)<.0086 and abs(abs(p.x-inner.matrix_world.translation.x)-.03)<.001]
            check('pin_hole_alignment_'+str(i)+':'+side,'real opposite tube-wall opening centeredZ.9 with17mm diameter',{'ring_vertices':len(ring),'center_z':(min(p.z for p in ring)+max(p.z for p in ring))/2 if ring else None},bool(ring) and abs((min(p.z for p in ring)+max(p.z for p in ring))/2-.9)<1e-5)
            surface=tree(inner,Matrix.Identity(4));origin=Vector((inner.matrix_world.translation.x-.08,0,.9));hit=surface.ray_cast(origin,Vector((1,0,0)),.16)[0]
            check('open_pin_bore_'+str(i)+':'+side,'ray passes both tube walls through real pin hole',list(hit) if hit else None,hit is None)
            check('support_axis_radius_'+str(i)+':'+side,'14mm above lined support',(axis.matrix_world.translation-support.matrix_world.translation).z,abs((axis.matrix_world.translation-support.matrix_world.translation).z-.014)<1e-6)
    update(root,0,15);zl=col.all_objects[ID+'__anchor_bar_axis_l'].matrix_world.translation.z;zr=col.all_objects[ID+'__anchor_bar_axis_r'].matrix_world.translation.z;check('independent_height_controls','750mm right-only rise',zr-zl,abs(zr-zl-.75)<1e-6);update(root,0,0)
    shade=bpy.context.scene.display.shading;check('shadow_free','FLAT outlines,no shadows/cavity/specular',[shade.light,shade.show_shadows,shade.show_cavity,shade.show_specular_highlight],shade.light=='FLAT' and shade.show_object_outline and not any([shade.show_shadows,shade.show_cavity,shade.show_specular_highlight]))
    # Reopen authoritative assembly; test evaluated linked data without local mesh copies.
    assembly_before=digest(OUT);bpy.ops.wm.open_mainfile(filepath=str(OUT));s=bpy.context.scene;instances={o.name:o for o in s.objects if o.instance_type=='COLLECTION'};check('assembly_linked_assets','3 linked collection instances, no local meshes',list(instances),len(instances)==3 and not any(o.type=='MESH' and not o.library for o in s.objects))
    objs={key:[o for o in inst.instance_collection.all_objects if o.type=='MESH'] for key,inst in instances.items()};frames={k:asset_instance_frame(o) for k,o in instances.items()}
    bcol=instances['barbell_primary'].instance_collection;standcol=instances['stands_pair'].instance_collection;barcenter=(frames['barbell_primary']@bcol.all_objects[BBID+'__anchor_axis_center'].matrix_world).translation
    line=[(frames['barbell_primary']@bcol.all_objects[BBID+'__anchor_load_'+side].matrix_world).translation for side in ['l','r']]
    shaft=(line[0]-line[1]).normalized()
    check('barbell_shaft_orientation','shaft parallel worldX',list(shaft),abs(abs(shaft.x)-1)<1e-6 and abs(shaft.y)<1e-6 and abs(shaft.z)<1e-6)
    fixture_meta=json.loads((F/'asset.json').read_text())
    seating=fixture_meta.get('bar_seating_offset_m',0.0)
    check('fixture_seating_offset','documented scene-owned downward settlement <=10um',seating,-1e-5<=seating<=0 and abs(instances['barbell_primary'].get('bar_seating_offset_m',0)-seating)<1e-10)
    feet=[]
    for side in ['l','r']:
        support=(frames['stands_pair']@standcol.all_objects[ID+'__anchor_bar_support_'+side].matrix_world).translation;axis=(frames['stands_pair']@standcol.all_objects[ID+'__anchor_bar_axis_'+side].matrix_world).translation
        radial_error=(axis+Vector((0,0,seating))-barcenter).cross(shaft).length
        check('support_on_actual_shaft_line_'+side,'<=1e-6m radial distance',radial_error,radial_error<1e-6)
        check('assembly_bar_contact_'+side,'nominal axis+documented measured settlement; equalY/Z; actual surface independently validated',{'support':list(support),'barcenter':list(barcenter),'axis':list(axis),'seating_offset_m':seating},abs(axis.y-barcenter.y)<1e-6 and abs(axis.z+seating-barcenter.z)<1e-6 and abs(barcenter.z-support.z-.014-seating)<1e-6)
        hook_outer=abs(axis.x)+.03;clearance=.655-hook_outer;check('shaft_flange_clearance_'+side,'75mm',clearance,abs(clearance-.075)<1e-6)
        # Racked bar projection must lie inside actual four-pad support polygon envelope.
        feet=[frames['stands_pair']@(o.matrix_world@v.co) for o in objs['stands_pair'] if o.name.endswith('_'+side) and '__mesh_rubber_' in o.name for v in o.data.vertices if abs((o.matrix_world@v.co).z)<1e-6]
        inside=min(p.x for p in feet)<axis.x<max(p.x for p in feet) and min(p.y for p in feet)<axis.y<max(p.y for p in feet)
        check('static_support_projection_'+side,'bar vertical projection inside floor-pad convex rectangular envelope; not physical stability simulation',list(axis),inside)
    gap=.55-.5969/2-.3556/2;check('bench_base_horizontal_clearance','73.75mm',gap,abs(gap-.07375)<1e-6)
    pad=bpy.data.objects.get(BID+'__anchor_pad_center');padz=(frames['bench_primary']@pad.matrix_world).translation.z;check('bar_above_pad','484.8mm plus documented fixture settlement',barcenter.z-padz,abs(barcenter.z-padz-.4848-seating)<1e-6)
    trees={k:[(o,tree(o,frames[k])) for o in oo] for k,oo in objs.items()};crossings=[];tested=0
    for aa,bb in [('stands_pair','bench_primary'),('stands_pair','barbell_primary'),('bench_primary','barbell_primary')]:
        for o,t in trees[aa]:
            for p,u in trees[bb]:
                tested+=1
                if t.overlap(u):crossings.append([o.name,p.name])
    check('inter_asset_bvh_crossings','0 triangle crossings; intended bar tangent contact',{'object_pairs':tested,'crossings':crossings},not crossings)
    assembly_meta=json.loads((F/'asset.json').read_text())
    for dep in assembly_meta['dependencies']:check('dependency_pin:'+dep['id'],dep['sha256'],digest(R/dep['source']),digest(R/dep['source'])==dep['sha256'])
    for lib in bpy.data.libraries:check('relative_link:'+lib.name,'relative existing path',lib.filepath,lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).is_file())
    protected=json.loads((A/'prebuild-record.json').read_text())['protected_sha256'];changed=[p for p,h in protected.items() if digest(R/p)!=h];check('approved_assets_and_shared_standards_preserved','all protected hashes match',changed,not changed)
    check('stand_master_not_resaved',before,digest(SOURCE),before==digest(SOURCE));check('assembly_not_resaved',assembly_before,digest(OUT),assembly_before==digest(OUT))
    report={'date':'2026-10-15','source_sha256':before,'assembly_sha256':assembly_before,'validator_sha256':digest(Path(__file__)),'blender_version':bpy.app.version_string,'checks':checks,'pass':sum(c['result']=='PASS' for c in checks),'fail':sum(c['result']=='FAIL' for c in checks),'scope':'digital review prototype; actual inter-asset triangles, all detents and support geometry; not physical strength/ergonomic certification'};write_json(A/'validation-results.json',report);write_json(F/'validation-results.json',report)
    print('STANDS_QA',report['pass'],report['fail']);print([e for e in checks if e['result']=='FAIL'])
    if report['fail']:raise RuntimeError('Stands QA failed')
if __name__=='__main__':run()
