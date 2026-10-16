"""Three ordered full-reference reproductions with the approved local policy."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_barbell_stands import render,A
from barbell_20kg_common import write_json
runs=[]
for index in range(3):
    render(reproduce=True)
    runs.append({'run':index+1,**json.loads((A/'render-reproduction.json').read_text())})
write_json(A/'render-repeat-validation.json',{'runs':runs,'pass':sum(e['result']=='PASS' for r in runs for e in r['checks']),'fail':sum(e['result']=='FAIL' for r in runs for e in r['checks'])})
