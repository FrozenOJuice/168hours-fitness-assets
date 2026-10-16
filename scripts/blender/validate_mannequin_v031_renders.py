"""Read final PNGs: visible localized deep color, continuous-skin transparency on/off proof."""
import bpy,sys,numpy as np,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mannequin_v031_common import *
from barbell_20kg_common import write_json,digest

def pixels(path):
 im=bpy.data.images.load(str(path),check_existing=False);a=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(a);shape=(im.size[1],im.size[0],4);bpy.data.images.remove(im);return a.reshape(shape)
s=json.loads((F/'previews/render-settings.json').read_text());on=s['views']['xray_neutral_three_quarter'];off=s['views']['xray_disabled_three_quarter'];a=pixels(R/on['path']);b=pixels(R/off['path']);assert a.shape==b.shape;delta=np.max(abs(a[:,:,:3]-b[:,:,:3]),axis=2);red=(a[:,:,0]-a[:,:,1]>.04)&(a[:,:,0]-a[:,:,2]>.04);redoff=(b[:,:,0]-b[:,:,1]>.04)&(b[:,:,0]-b[:,:,2]>.04);changed=float(np.mean(delta>.01));checks=[{'check':'visible_deep_color','result':'PASS' if red.sum()>1000 and redoff.sum()<100 else 'FAIL','actual':{'on_red_pixels':int(red.sum()),'off_red_pixels':int(redoff.sum())},'expected':'Actual Xray render visibly reveals selected deep color; disabled counterpart does not'},{'check':'local_effect_and_opaque_background','result':'PASS' if changed<.03 and np.max(abs(a[:,:,3]-1))<1e-5 else 'FAIL','actual':{'changed_pixel_fraction_above_0_01':changed,'max_alpha_background_error':float(np.max(abs(a[:,:,3]-1)))},'expected':'Fewer than3% full-frame pixels change; opaque background preserved. Local experiment diagnostic, not a production pixel-match tolerance.'}];summary={k:sum(c['result']==k for c in checks) for k in ['PASS','FAIL']};write_json(A/'render-validation.json',{'source_sha256':digest(SOURCE),'fixture_sha256':digest(FS),'validator_sha256':digest(Path(__file__)),'inputs':{'on':on,'off':off},'checks':checks,'summary':summary,'limitations':'Color/pixel evidence proves visible/localized effect, not clinical accuracy, transparency sorting over arbitrary camera motion or accepted anatomy.'});print('RENDER_VALIDATION',summary)
if summary['FAIL']:raise SystemExit(1)
