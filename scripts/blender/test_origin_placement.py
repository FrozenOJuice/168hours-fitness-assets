"""Read-only A14 linked automatic-placement regression; no fixture saved."""
from pathlib import Path
import sys,bpy,json
from mathutils import Vector
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'scripts/blender'))
from barbell_20kg_common import make_fixture,local_anchor,asset_instance_frame,PID,ID
scene,bar,plate=make_fixture();bi=bpy.data.objects['barbell_primary'];checks=[]
for side in ['l','r']:
 p=bpy.data.objects['plate_'+side];target=asset_instance_frame(bi)@local_anchor(bar,ID,'load_'+side).matrix_world;actual=asset_instance_frame(p)@local_anchor(plate,PID,'bore_center').matrix_world;out=target.to_3x3()@Vector((0,1,0));delta=actual.translation-target.translation
 axial=delta.dot(out);radial=delta.cross(out).length
 checks.append({'side':side,'axis_error_m':radial,'center_offset_from_flange_m':axial,'expected_m':.01651+.001,'result':'PASS' if radial<1e-6 and abs(axial-.01751)<1e-6 else 'FAIL'})
(r/'docs/audits/origin-placement-helper-tests.json').write_text(json.dumps({'checks':checks,'pass':all(c['result']=='PASS' for c in checks)},indent=2)+'\n');print(checks)
if not all(c['result']=='PASS' for c in checks):raise RuntimeError('Placement helper failed')
