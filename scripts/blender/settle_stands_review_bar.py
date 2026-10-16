"""One-shot fixture-only settlement of measured tessellation gap; source assets untouched."""
from pathlib import Path
import sys,json,shutil
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_barbell_stands import R,A,SOURCE
from build_stands_review_assembly import F,OUT,BBID
from barbell_20kg_common import digest,write_json
def run():
    meta=json.loads((F/'asset.json').read_text());assert 'bar_seating_offset_m' not in meta
    evidence=json.loads((A/'contact-investigation.json').read_text())
    assert evidence['assembly_sha256']==digest(OUT)
    assert all(4e-6<r['minimum_triangle_distance_m']<6e-6 for r in evidence['checks'])
    archive=F/'history/0.1.1-before-contact'
    if archive.exists():assert digest(archive/OUT.name)==digest(OUT)
    else:
        archive.mkdir(parents=True)
        for p in F.iterdir():
            if p.is_file() and p.suffix!='.blend1':shutil.copy2(p,archive/p.name)
        shutil.copytree(F/'previews',archive/'previews')
    sources={R/d['source']:digest(R/d['source']) for d in meta['dependencies']}
    before=digest(OUT);bpy.ops.wm.open_mainfile(filepath=str(OUT))
    objs={o.name:o.matrix_world.copy() for o in bpy.context.scene.objects};bar=bpy.context.scene.objects['barbell_primary']
    # Leave <0.1um positive separation: a nearest float32 placement at -4.8um
    # overshoots the exact facet contact by ~0.03um and creates BVH crossings.
    requested=-4.7e-6;bar.location.z+=requested;bpy.context.view_layer.update()
    actual=float(bar.matrix_world.translation.z-objs[bar.name].translation.z)
    assert abs(actual-requested)<1e-7
    assert all(o.matrix_world==objs[o.name] for o in bpy.context.scene.objects if o!=bar)
    bar['bar_seating_offset_m']=actual
    bar['seating_basis']='Measured tessellated shaft/liner contact; source anchors and geometry preserved'
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True,relative_remap=False)
    assert all(digest(p)==h for p,h in sources.items())
    meta['bar_seating_offset_m']=actual
    meta['bar_center_m'][2]+=actual
    meta['instance_frames']['barbell_primary']=[list(row) for row in bar.matrix_world]
    meta['source_revision_or_digest']='sha256:'+digest(OUT)
    meta['reference_renders_state']='captured pre-contact fixture; retained views must pass comparison against settled source before approval'
    write_json(F/'asset.json',meta)
    record={'before_sha256':before,'after_sha256':digest(OUT),'requested_vertical_offset_m':requested,'actual_vertical_offset_m':actual,'scope':'only barbell_primary instance world Z and local descriptive properties; bench/stands instances, source geometry/materials/anchors and shared standards unchanged','evidence':'contact-investigation.json','source_sha256':{str(p.relative_to(R)):h for p,h in sources.items()},'script_sha256':digest(Path(__file__)),'archive':str(archive.relative_to(R))}
    write_json(A/'contact-correction.json',record)
    print('BAR_SETTLEMENT',record)
if __name__=='__main__':run()
