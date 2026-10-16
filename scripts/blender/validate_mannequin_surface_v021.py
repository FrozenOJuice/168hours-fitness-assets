"""Read-only asset-local refinement regressions. Does not certify anatomy or release."""
from pathlib import Path
import bpy,json,sys,math,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import R,A,ID,RID,SOURCE
from barbell_20kg_common import digest,write_json
import mannequin_core_poses as cp
import mannequin_review_common as mc
checks=[]
def check(name,ok,actual,expected):checks.append(dict(check=name,result='PASS' if ok else 'FAIL',actual=actual,expected=expected))
def profile(p):
 result=[]
 for z in np.arange(1.025,1.401,.025):
  m=(abs(p[:,0])<.06)&(abs(p[:,2]-z)<.008)&(p[:,1]>0)
  result.append([float(z),float(np.median(p[m,1]))])
 return np.array(result)
before=digest(SOURCE);archive=A/'history/0.2.0'/SOURCE.name
# Load only predecessor body object for measured coordinates/topology/groups, no scene posing.
with bpy.data.libraries.load(str(archive),link=False) as (src,dst):dst.objects=[ID+'__mesh_body']
old=dst.objects[0];baseline=np.array([v.co[:] for v in old.data.vertices]);faces=[p.vertices[:] for p in old.data.polygons]
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mc.MAPPING=None;cp.pose('neutral_a_pose');body=mc.get(ID+'__mesh_body');arm=mc.get(ID+'__armature_deform');p=np.array([v.co[:] for v in body.data.vertices]);neutral=cp.coords()
check('preserved_topology',len(p)==len(baseline) and faces==[f.vertices[:] for f in body.data.polygons],{'vertices':len(p),'quads':len(faces)},'Same214050vertices/214048quads and exact face indices')
check('neutral_correctives_zero',float(np.linalg.norm(p-neutral,axis=1).max())<1e-6,float(np.linalg.norm(p-neutral,axis=1).max()),'Neutral raw/evaluated geometry residual<1um')
hand_ids={body.vertex_groups[n].index for n in body.vertex_groups.keys() if n.startswith(('hand_','thumb_','index_','middle_','ring_','little_'))}
hand=[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in hand_ids)>.7];err=float(np.linalg.norm(p[hand]-baseline[hand],axis=1).max());check('hand_geometry_preserved',err<1e-6,err,'No hand/finger sculpt displacement>1um; retained measured grip fit')
bp,ap=profile(baseline),profile(p);oldjump=float(abs(np.diff(bp[:,1])).max());newjump=float(abs(np.diff(ap[:,1])).max());check('anterior_torso_ledge_reduced',newjump<.009 and newjump<oldjump*.5,{'before_max_25mm_band_step_m':oldjump,'after_max_25mm_band_step_m':newjump,'before':bp.tolist(),'after':ap.tolist()},'Local diagnostic: maximum adjacent anterior median step<9mm and less than half predecessor; visual profile also required')
# Compare a preserved rest-index region. The archived V0.2 pose was measured before editing.
# Reproduce archived skin evaluation in isolated temporary input by loading its collection below.
cp.pose('arms_raised');raised=cp.coords();mask=(abs(baseline[:,0])>.10)&(abs(baseline[:,0])<.24)&(baseline[:,2]>1.28)&(baseline[:,2]<1.43)
current_width=float(abs(raised[mask,0]).max())
# Baseline maximum from identical rest-index region measured before editing.
diagnosis=json.loads((A/'surface-diagnosis.json').read_text());baseline_width=diagnosis['overhead_comparison_region']['baseline_max_abs_x_m'];check('overhead_lateral_expansion_reduced',current_width<baseline_width-.015,{'before_max_x_m':baseline_width,'after_max_x_m':current_width},'Measured local lateral extremum reduced by at least15mm; not universal anthropometric acceptance')
# Repeatability and independent pose drivers; shoulder fields must stay zero on inactive arm.
solver=mc.get(RID+'__armature_solver');mod=body.modifiers['foundation_shoulder_volume_corrective'];inputkeys=[i.identifier for i in mod.node_group.interface.items_tree if i.item_type=='SOCKET' and i.in_out=='INPUT' and i.socket_type=='NodeSocketFloat'];sweep=[]
for angle in [0,30,60,90,110]:
 cp.pose('neutral_a_pose');mc.rotate('clavicle_l',(0,0,1),-math.radians(angle*25/110));mc.rotate('upper_arm_l',(0,0,1),-math.radians(angle));mc.update();a=cp.coords();values=[float(mod[k]) for k in inputkeys];sweep.append({'upper_arm_degrees':angle,'modifier_inputs':values,'finite':bool(np.isfinite(a).all())})
check('shoulder_sweep_independent',all(s['finite'] and abs(s['modifier_inputs'][1])<1e-6 for s in sweep) and abs(sweep[-1]['modifier_inputs'][0]-1)<1e-5,sweep,'Five left-arm elevations finite; right correction0; left full at110deg')
cp.pose('neutral_a_pose');check('source_read_only',digest(SOURCE)==before,digest(SOURCE),before)
summary={k:sum(c['result']==k for c in checks) for k in ['PASS','FAIL']};write_json(A/'surface-refinement-validation.json',{'version':'0.2.1','source_sha256':before,'baseline_sha256':digest(archive),'validator_sha256':digest(Path(__file__)),'criteria':'Asset-local diagnostic regressions, not shared approval or complete self-intersection/motion certification','summary':summary,'checks':checks});print('SURFACE_REFINEMENT',summary)
if summary['FAIL']:print([c for c in checks if c['result']=='FAIL']);raise SystemExit(1)
