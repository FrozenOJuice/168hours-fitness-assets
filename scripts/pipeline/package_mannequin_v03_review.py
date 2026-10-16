"""Verify pinned review evidence and package separate native-review render bundles."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,struct
R=Path(__file__).resolve().parents[2];ID='168h_human_anatomical_mannequin';RID='168h_rig_mannequin_v1';A=R/'assets/humans/models'/ID/'prototypes/v0.3.0';F=R/'scenes/templates/168h_template_mannequin_anatomy_study';RA=R/'assets/humans/rigs'/RID/'prototypes/v0.3.0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
source=A/(ID+'.blend');fixture=F/(F.name+'.blend');rig=RA/(RID+'.blend');m=read(A/'asset.json');fm=read(F/'asset.json');suite=read(F/'suite.json');v=read(A/'study-validation.json');obs=read(A/'observed.json')
assert m['source_revision_or_digest']=='sha256:'+sha(source)
assert fm['source_revision_or_digest']=='sha256:'+sha(fixture)
assert v['source_sha256']==obs['source_sha256']==suite['character_sha256']==sha(source)
assert v['study_sha256']==suite['source_sha256']==sha(fixture)
assert v['summary']=={'PASS':57,'FAIL':0}
assert read(A/'contract-validation.json')['fail']==63
for manifest in [m,fm]:
 for d in manifest['dependencies']:assert sha(R/d['source'])==d['sha256'],d
assert sha(rig)==read(RA/'asset.json')['source_revision_or_digest'].removeprefix('sha256:')
assert sha(A/'rest-profile.json')==obs['rest_profile_sha256']
assert sha(R/'scripts/blender/build_mannequin_anatomy_study.py')==suite['builder_sha256']
assert sha(R/'scripts/blender/mannequin_v03_poses.py')==suite['pose_helper_sha256']
protected=read(A/'plan.json')['protected_sha256'];assert all(sha(R/p)==h for p,h in protected.items())
images={};groups={}
for root,expected in [(A,7),(F,32)]:
 settings=read(root/'previews/render-settings.json');listed={R/d['path']:d['sha256'] for d in settings['views'].values()};assert set(listed)==set((root/'previews').glob('*.png')) and len(listed)==expected
 assert settings['source_sha256']==sha(source if root==A else fixture)
 for p,h in listed.items():
  assert sha(p)==h,p
  raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';w,hgt=struct.unpack('>II',raw[16:24]);assert w>0 and hgt>0
  images[str(p.relative_to(R))]={'sha256':h,'pixels':[w,hgt]}
 groups[root]=listed
# Reconcile coverage metadata with known observed implementation, never invent missing coverage.
m['muscle_coverage']['implemented_deep_ids']=['muscle_vastus_intermedius_l'];m['muscle_coverage']['unimplemented_count']=63;write(A/'asset.json',m)
notes='Review prototype0.3.0, not production approved. CC0 upstream Dan Ulrich Blender Human Base Meshes1.4.1; original project artwork release terms unselected, MIT code/docs separate. See asset REPORT.md/validation.md.63muscle regions unimplemented; strong hip folds, shoulder mechanics, palm/thumb fit and jagged schematic Xray remain limited. Final references use flat illustrated shading; comparisons/source screening use identical diagnostic studio shading without shadows/AO/specular.\n'
output=R/'exports/illustrations';output.mkdir(parents=True,exist_ok=True);packages=[]
for root,name in [(A,'mannequin_v03_unassembled_renders.zip'),(F,'mannequin_v03_tests_comparison_renders.zip')]:
 target=output/name;files=[*sorted(groups[root]),root/'previews/render-settings.json'];files += [F/'suite.json'] if root==F else []
 if root==A:files+=sorted((A/'references/source-screening').glob('*.png'))
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for p in files:z.write(p,('research_source_screening/' if p.parent.name=='source-screening' else '')+p.name)
  z.writestr('REVIEW_NOTES.txt',notes+('Includes7final neutral/torso views and6unadapted source-screening views.\n' if root==A else 'Includes32test/compare views over13states plus overhead/grip closeups and2comparisons.\n'))
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for p in files:
   key=('research_source_screening/' if p.parent.name=='source-screening' else '')+p.name;assert hashlib.sha256(z.read(key)).hexdigest()==sha(p)
 packages.append({'path':str(target.relative_to(R)),'sha256':sha(target),'png_count':sum(p.suffix=='.png' for p in files),'CRC_and_member_hashes':'PASS'})
ignore=subprocess.run(['git','check-ignore',str(output/packages[0]['path'].split('/')[-1]),str(source)+ '1'],cwd=R,capture_output=True,text=True);assert ignore.returncode==0 and len(ignore.stdout.splitlines())==2
lfs=subprocess.run(['git','check-attr','filter','--',str(source.relative_to(R)),str(fixture.relative_to(R)),str(rig.relative_to(R))],cwd=R,capture_output=True,text=True,check=True);assert all(l.endswith(': lfs') for l in lfs.stdout.splitlines())
write(A/'delivery-audit.json',{'date':'2026-10-16','status':'review','source_sha256':sha(source),'fixture_sha256':sha(fixture),'rig_sha256':sha(rig),'protected_files_unchanged':len(protected),'source_and_render_pins':'PASS','authoritative_reference_png_count':39,'additional_research_screening_png_count':6,'images':images,'packages':packages,'LFS_rules':lfs.stdout.splitlines(),'ignored_exports_backups':ignore.stdout.splitlines(),'package_script_sha256':sha(Path(__file__)),'release_approval':None})
print('DELIVERY_AUDIT PASS',len(images),'reference PNGs +6research; protected',len(protected));print(json.dumps(packages,indent=2))
