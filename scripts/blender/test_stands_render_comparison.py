"""Boundary/regression cases for explicitly approved local image acceptance."""
from pathlib import Path
import json,sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from compare_stands_render import compare
R=Path(__file__).resolve().parents[2];A=R/'assets/equipment/racks/168h_equipment_barbell_stands'
limits=json.loads((A/'render-comparison-policy.json').read_text())['limits']
base=np.full((1000,1600,4),128,dtype=np.uint8);rows=[]
def case(name,image,expected,scoped=True):
    result=compare(base,image,limits if scoped else None)
    rows.append({'case':name,'expected':expected,'observed':result,'result':'PASS' if result['result']==expected else 'FAIL'})
case('exact image accepted',base.copy(),'PASS')
x=base.copy();x[0,0,0]+=8;case('sparse 8-code edge difference accepted',x,'PASS')
x=base.copy();x[0,0,0]+=9;case('9-code error rejected',x,'FAIL')
x=base.copy();x[0,0,3]+=1;case('any alpha change rejected',x,'FAIL')
x=base.copy();x[:5,:,:3]+=1;case('broad drift rejected',x,'FAIL')
x=base.copy();x[0,:1000,:3]+=8;case('mean-error gate rejects sparse excessive aggregate energy',x,'FAIL')
x=base.copy();x[0,0,0]+=1;case('unscoped exact view rejects 1-code change',x,'FAIL',False)
case('resolution mismatch rejected',base[:999].copy(),'FAIL')
# Test independently the two strict coverage boundaries.
wide=dict(limits,max_rgb_8bit_delta=255,mean_absolute_rgba_8bit_delta_lte=255)
x=base.copy();x.reshape(-1,4)[:6400,0]+=1
r=compare(base,x,wide);rows.append({'case':'channel coverage boundary fails','result':'PASS' if r['result']=='FAIL' else 'FAIL'})
report={'checks':rows,'pass':sum(r['result']=='PASS' for r in rows),'fail':sum(r['result']=='FAIL' for r in rows)}
(A/'render-comparison-tests.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['fail']==0,report
print('STANDS_RENDER_COMPARISON_TESTS',report['pass'],report['fail'])
