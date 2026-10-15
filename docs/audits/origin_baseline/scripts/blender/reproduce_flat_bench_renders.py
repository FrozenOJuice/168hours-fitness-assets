"""Reopen native prototype, render disposable comparisons and compare decoded pixels."""
from pathlib import Path
import bpy, sys, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_flat_bench import render
from build_flat_bench import REPO,ID,ASSET,SOURCE
from barbell_20kg_common import digest,write_json

if __name__=='__main__':
    directory=REPO/'exports/illustrations/flat_bench_reproduction'
    before=digest(SOURCE);views=render(directory);checks=[]
    for view in views:
        name=f'{ID}__{view}__flat.png'
        arrays=[]
        for path in [ASSET/'previews'/name,directory/name]:
            im=bpy.data.images.load(str(path),check_existing=False)
            pixels=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(pixels)
            arrays.append(pixels);bpy.data.images.remove(im)
        diff=np.abs(arrays[0]-arrays[1]);checks.append({'view':view,'result':'PASS' if np.max(diff)==0 else 'FAIL','decoded_max_channel_delta':float(np.max(diff)),'changed_channels':int(np.count_nonzero(diff))})
    checks.append({'check':'source_not_resaved','result':'PASS' if before==digest(SOURCE) else 'FAIL'})
    write_json(ASSET/'render-reproduction.json',{'source_sha256':before,'blender_version':bpy.app.version_string,'checks':checks,'pass':all(c['result']=='PASS' for c in checks),'script_sha256':digest(Path(__file__))})
    print('BENCH_RENDER_REPRODUCTION',checks)
    if not all(c['result']=='PASS' for c in checks):raise RuntimeError('Image reproduction mismatch')
