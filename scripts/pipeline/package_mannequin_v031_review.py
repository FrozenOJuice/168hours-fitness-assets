"""Reconcile final indexes and verify/publish separate V0.3.1 review render ZIPs locally."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,struct
R=Path(__file__).resolve().parents[2];ID='168h_human_anatomical_mannequin';A=R/'assets/humans/models'/ID/'prototypes/v0.3.1';OLD=A.parent/'v0.3.0';F=R/'scenes/templates/168h_template_mannequin_movement_review';SOURCE=A/(ID+'.blend');FS=F/(F.name+'.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
m=read(A/'asset.json');suite=read(F/'suite.json');settings=read(F/'previews/render-settings.json');state=read(A/'study-validation.json');motion=read(A/'movement-validation.json');render=read(A/'render-validation.json');observed=read(A/'observed.json');contract=read(A/'contract-validation.json')
assert m['status']=='review' and m['source_revision_or_digest']=='sha256:'+sha(SOURCE)
assert state['source_sha256']==motion['source_sha256']==render['source_sha256']==observed['source_sha256']==suite['character_sha256']==sha(SOURCE)
assert state['study_sha256']==render['fixture_sha256']==suite['source_sha256']==settings['source_sha256']==sha(FS)
assert state['summary']=={'PASS':82,'FAIL':0} and motion['summary']=={'PASS':90,'FAIL':0} and render['summary']=={'PASS':2,'FAIL':0}
assert contract['pass']==394 and contract['fail']==63 and all(c['check'].startswith('muscle_binding:') for c in contract['checks'] if c['result']=='FAIL')
assert sha(R/'scripts/blender/build_mannequin_v031_review.py')==suite['builder_sha256'];assert sha(R/'scripts/blender/mannequin_v031_poses.py')==suite['pose_helper_sha256']
assert sha(A/'rest-profile.json')==sha(OLD/'rest-profile.json')==observed['rest_profile_sha256']
for dep in m['dependencies']:assert sha(R/dep['source'])==dep['sha256']
for dep in read(OLD/'asset.json')['dependencies']:assert sha(R/dep['source'])==dep['sha256'],'Previous rig dependency changed'
protected=read(A/'plan.json')['protected_sha256'];assert all(sha(R/p)==h for p,h in protected.items())
fm=read(F/'asset.json');fm['source_revision_or_digest']='sha256:'+sha(FS);fm['reference_renders']=[{'view':n,**v,'source_revision_or_digest':'sha256:'+sha(FS)} for n,v in settings['views'].items()]
for dep in fm['dependencies']:assert sha(R/dep['source'])==dep['sha256']
write(F/'asset.json',fm)
groups={};images={}
for folder,count in [(A,7),(F,57)]:
 s=read(folder/'previews/render-settings.json');listed={R/d['path']:d['sha256'] for d in s['views'].values()};assert set(listed)==set((folder/'previews').glob('*.png')) and len(listed)==count;assert s['source_sha256']==sha(SOURCE if folder==A else FS)
 for p,h in listed.items():
  assert sha(p)==h;raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';w,hgt=struct.unpack('>II',raw[16:24]);images[str(p.relative_to(R))]={'sha256':h,'pixels':[w,hgt]}
 groups[folder]=listed
out=R/'exports/illustrations';out.mkdir(parents=True,exist_ok=True);packages=[]
for folder,name in [(A,'mannequin_v031_unassembled_renders.zip'),(F,'mannequin_v031_tests_comparison_renders.zip')]:
 files=[*sorted(groups[folder]),folder/'previews/render-settings.json',A/'REPORT.md'];files+=[F/'suite.json'] if folder==F else [];target=out/name
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for p in files:z.write(p,p.name)
  z.writestr('REVIEW_NOTES.txt','V0.3.1review, not production approved. CC0-derived anatomy; original project artwork release terms unselected, separate from MIT code/docs. Full source/validation/provenance and limitations in REPORT.md. Normal Workbench views and experimental Eevee translucent Xray are explicitly separate local presets.63missing muscle bindings remain failures.\n')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
 packages.append({'path':str(target.relative_to(R)),'sha256':sha(target),'png_count':len(groups[folder]),'CRC_and_member_hashes':'PASS'})
ignored=subprocess.run(['git','check-ignore',str(out/packages[0]['path'].split('/')[-1]),str(SOURCE)+'1'],cwd=R,capture_output=True,text=True,check=True);assert len(ignored.stdout.splitlines())==2
lfs=subprocess.run(['git','check-attr','filter','--',str(SOURCE.relative_to(R)),str(FS.relative_to(R))],cwd=R,capture_output=True,text=True,check=True);assert all(l.endswith(': lfs') for l in lfs.stdout.splitlines())
write(A/'delivery-audit.json',{'date':'2026-10-16','status':'review','source_sha256':sha(SOURCE),'fixture_sha256':sha(FS),'protected_files_unchanged':len(protected),'previous_rig_pins':'PASS','source_and_reference_pins':'PASS','authoritative_png_count':len(images),'images':images,'packages':packages,'LFS_rules':lfs.stdout.splitlines(),'ignored_exports_backups':ignored.stdout.splitlines(),'package_script_sha256':sha(Path(__file__)),'remaining_contract_failures':63,'production_approval':None});print('DELIVERY_AUDIT PASS',len(images),'PNGs, protected',len(protected));print(json.dumps(packages,indent=2))
