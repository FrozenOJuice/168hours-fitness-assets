"""Initial-review surface fairing/sculpt, preserves topology, rig and muscle API."""
from pathlib import Path
import sys,bpy,math,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,SOURCE,R,RA
from barbell_20kg_common import digest,write_json
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));body=bpy.data.objects[ID+'__mesh_body'];before=digest(SOURCE)
assert not (A/'surface-polish.json').exists(),'One-shot; avoid cumulative sculpt'
g=body.vertex_groups.new(name='surface_fairing')
for v in body.data.vertices:
    x,y,z=v.co
    weight=1.0 if .12<z<1.5 else .12
    if abs(x)>.47:weight=.03
    g.add([v.index],weight,'REPLACE')
    if .94<z<1.04 and abs(x)<.25:
        f=(1.04-z)/.10;limit=.13+.062*(f*f*(3-2*f))
        if abs(x)>limit:v.co.x=math.copysign(limit+(abs(x)-limit)*.12,x)
bpy.context.view_layer.objects.active=body;body.select_set(True)
mod=body.modifiers.new('review_surface_fairing','SMOOTH');mod.factor=.85;mod.iterations=45;mod.vertex_group=g.name
while body.modifiers.find(mod.name)>0:bpy.ops.object.modifier_move_up(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)
for v in body.data.vertices:
    x,y,z=v.co
    if y>.025 and 1.06<z<1.42 and abs(x)<.18:
        pec=.006*math.exp(-((abs(x)-.08)/.066)**4-((z-1.32)/.067)**4)
        sternum=-.0025*math.exp(-(x/.014)**2-((z-1.27)/.14)**4)
        abs_def=.0018*math.exp(-((abs(x)-.043)/.033)**4)*sum(math.exp(-((z-q)/.025)**2) for q in [1.12,1.18,1.24])
        v.co.y+=pec+sternum+abs_def
    if y>.03 and 1.55<z<1.73:
        v.co.y+=.009*math.exp(-(x/.014)**2-((z-1.642)/.027)**2)-.003*(math.exp(-((x-.028)/.016)**2)+math.exp(-((x+.028)/.016)**2))*math.exp(-((z-1.665)/.009)**2)
low=min(v.co.z for v in body.data.vertices);high=max(v.co.z for v in body.data.vertices)
for v in body.data.vertices:v.co.z=(v.co.z-low)*1.75/(high-low)
from mathutils import Vector
from mathutils.bvhtree import BVHTree
tree=BVHTree.FromPolygons([v.co for v in body.data.vertices],[p.vertices[:] for p in body.data.polygons])
hc=json.loads((A/'human-contract.json').read_text())
for key in ['hand_grip_l','hand_grip_r','back_support']:
    obj=bpy.data.objects[hc['anchors'][key]['object']];frame=obj.matrix_world.copy()
    if key.startswith('hand'):frame.translation.y=.034
    else:
        hit=tree.ray_cast(Vector((0,-.5,frame.translation.z)),Vector((0,1,0)),1)[0]
        assert hit is not None;frame.translation.y=hit.y
    obj.matrix_world=frame;bpy.context.view_layer.update();hc['anchors'][key]['position_m']=list(obj.matrix_world.translation);hc['anchors'][key]['rotation_quaternion_wxyz']=list(obj.matrix_world.to_quaternion())
# Increase restrained form value separation without lights/shadows/AO.
for o in [body,bpy.data.objects[ID+'__mesh_vastus_intermedius_l']]:
    group=next(m.node_group for m in o.modifiers if m.type=='NODES')
    shade=next(n for n in group.nodes if n.type=='MATH' and n.operation=='MULTIPLY_ADD');shade.inputs[1].default_value=.42;shade.inputs[2].default_value=.50
    base=next(n for n in group.nodes if n.type=='MIX_RGB');base.inputs[1].default_value=(.12,.145,.16,1);base.inputs[2].default_value=(.63,.67,.69,1)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['dimensions_m']=[max(v.co[k] for v in body.data.vertices)-min(v.co[k] for v in body.data.vertices) for k in range(3)];write_json(A/'asset.json',m)
write_json(A/'human-contract.json',hc);m['anchors']=hc['anchors'];write_json(A/'asset.json',m)
write_json(A/'surface-polish.json',{'before_source_sha256':before,'after_source_sha256':digest(SOURCE),'geometry':'same vertex count/topology;45 localized fairing iterations, softened hip outline, subtle pectoral/sternum/abdominal/nose/orbital displacement','rig_skeleton_anchors':'unchanged','illustration_ramp':'normal dot(0.28,0.72,0.62)*0.42+0.50; gray endpoints(.12,.145,.16)/(.63,.67,.69)','script_sha256':digest(Path(__file__))})
