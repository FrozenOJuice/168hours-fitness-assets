"""Run existing origin regression tests, redirecting only their report destinations."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scripts/blender'))
for filename,old,new in [
 ('test_asset_origin_validation.py',"REPO/'docs/audits/origin-validator-tests.json'","REPO/'assets/equipment/racks/168h_equipment_barbell_stands/final-origin-validator-tests.json'"),
 ('test_origin_placement.py',"r/'docs/audits/origin-placement-helper-tests.json'","r/'assets/equipment/racks/168h_equipment_barbell_stands/final-origin-placement-helper-tests.json'")]:
    p=R/'scripts/blender'/filename;source=p.read_text();assert source.count(old)==1
    exec(compile(source.replace(old,new),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
