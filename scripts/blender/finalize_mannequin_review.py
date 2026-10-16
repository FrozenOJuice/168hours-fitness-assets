"""Finish the first review source; still not a production approval."""
from pathlib import Path
import bpy,sys,json,math,numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_anatomical_mannequin import A,ID,RID,SOURCE,G,CAT
from barbell_20kg_common import digest,write_json
assert json.loads((A/'asset.json').read_text())['version']=='0.1.0', 'Legacy0.1 prototype script; use the current foundation/core tools';bpy.ops.wm.open_mainfile(filepath=str(SOURCE));assert not (A/'review-finish.json').exists()
before=digest(SOURCE);root=bpy.data.objects[ID+'__root'];body=bpy.data.objects[ID+'__mesh_body'];indices=[]
for v in body.data.vertices:
    x,y,z=v.co;ax=abs(x)
    if .10<ax<.36 and 1.35<z<1.53:
        cap=1.448-.55*max(ax-.19,0)
        if z>cap:v.co.z=cap+(z-cap)*.08
        indices.append(v.index)
    if z<.12:v.co.y*=.88
g=body.vertex_groups.new(name='shoulder_finish');g.add(indices,1,'REPLACE');bpy.context.view_layer.objects.active=body;body.select_set(True)
sm=body.modifiers.new('shoulder_continuity','SMOOTH');sm.factor=.9;sm.iterations=45;sm.vertex_group=g.name
while body.modifiers.find(sm.name)>0:bpy.ops.object.modifier_move_up(modifier=sm.name)
bpy.ops.object.modifier_apply(modifier=sm.name)
xyz=np.array([v.co[:] for v in body.data.vertices]);x,y,z=xyz.T
def smooth(v):v=np.clip(v,0,1);return v*v*(3-2*v)
for side,sign in [('l',1),('r',-1)]:
    sx=x*sign;top=1.39-.2*sx;bottom=1.22+.78*sx
    values=smooth((sx-.012)/.020)*smooth((.18-sx)/.025)*smooth((top-z)/.018)*smooth((z-bottom)/.018)*smooth((y-.025)/.025)
    mid='muscle_pectoralis_major_'+side;body.data.attributes[mid].data.foreach_set('value',values.astype(np.float32));vg=body.vertex_groups[mid];vg.remove(list(range(len(xyz))))
    for i in np.flatnonzero(values>1e-4):vg.add([int(i)],float(values[i]),'REPLACE')
    a,b=Vector(G['hand_'+side][0]),Vector(G['hand_'+side][1]);u=(b-a).normalized();delta=xyz-np.array(a);along=delta@np.array(u);radial=np.linalg.norm(delta-along[:,None]*np.array(u),axis=1)
    palm=np.flatnonzero((along>-.004)&(along<.082)&(radial<.047)).tolist()
    for bone in bpy.data.objects[ID+'__armature_deform'].data.bones:
        if bone.use_deform:body.vertex_groups[bone.name].remove(palm)
    body.vertex_groups['hand_'+side].add(palm,1,'REPLACE')
window=np.exp(-((x-.103)/.058)**4-((z-.745)/.184)**4)*(y>.044)
body.data.attributes['xray_window'].data.foreach_set('value',window.astype(np.float32));vg=body.vertex_groups.new(name='xray_window')
for i in np.flatnonzero(window>1e-4):vg.add([int(i)],float(window[i]),'REPLACE')
smoothmod=body.modifiers.new('xray_boundary_fairing','SMOOTH');smoothmod.factor=0;smoothmod.iterations=5;smoothmod.vertex_group='xray_window'
d=smoothmod.driver_add('factor').driver;var=d.variables.new();var.name='enabled';var.targets[0].id=root;var.targets[0].data_path='["xray_enabled"]';d.expression='enabled*.5'
for key in root.keys():
    if key!='_RNA_UI':root.property_overridable_library_set('["'+key+'"]',True)
for o in [body,bpy.data.objects[ID+'__mesh_vastus_intermedius_l']]:
    ng=next(m.node_group for m in o.modifiers if m.type=='NODES');nodes=ng.nodes;links=ng.links
    shade=next(n for n in nodes if n.type=='MATH' and n.operation=='MULTIPLY_ADD');factor=nodes.new('ShaderNodeMath');factor.operation='MULTIPLY_ADD';factor.inputs[1].default_value=.35;factor.inputs[2].default_value=.65;links.new(shade.outputs[0],factor.inputs[0])
    for mix in list(nodes):
        if mix.type=='MIX_RGB' and mix.inputs[2].default_value[0] in [.66,.85]:
            tone=nodes.new('ShaderNodeMixRGB');tone.blend_type='MULTIPLY';tone.inputs[0].default_value=1;tone.inputs[1].default_value=mix.inputs[2].default_value;links.new(factor.outputs[0],tone.inputs[2]);links.new(tone.outputs[0],mix.inputs[2])
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),compress=True,relative_remap=False)
m=json.loads((A/'asset.json').read_text());m['source_revision_or_digest']='sha256:'+digest(SOURCE);m['dimensions_m']=[max(v.co[k] for v in body.data.vertices)-min(v.co[k] for v in body.data.vertices) for k in range(3)];write_json(A/'asset.json',m)
write_json(A/'review-finish.json',{'before_sha256':before,'after_sha256':digest(SOURCE),'changes':'softened shoulder silhouette, anatomical fan-shaped pec masks, neutral foot length277mm, more stable palm weights, larger smooth experimental aperture, root properties explicitly library-overridable','script_sha256':digest(Path(__file__))})
