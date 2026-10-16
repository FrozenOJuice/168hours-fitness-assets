"""Read-only official CC0 foundation screening; not final illustration preset."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector,Matrix
R=Path.cwd();sys.path.insert(0,str(R/'scripts/blender'))
from barbell_20kg_common import setup,camera
from mannequin_v03_common import A
path=A/'references/human_base_meshes_bundle.blend';bpy.ops.wm.open_mainfile(filepath=str(path));info=[]
for name in ['GEO-body_male_realistic','GEO-body_female_realistic']:
 o=bpy.data.objects[name];info.append({'name':name,'modifiers':[(m.name,m.type,getattr(m,'levels',None),getattr(m,'total_levels',None)) for m in o.modifiers],'groups':[g.name for g in o.vertex_groups],'collections':[(c.name,c.asset_data.author,c.asset_data.license) for c in o.users_collection if c.asset_data]})
print('DETAILS',json.dumps(info));p=A/'references/source-screening';p.mkdir(exist_ok=True)
for name in ['GEO-body_male_realistic','GEO-body_female_realistic']:
 o=bpy.data.objects[name]
 for m in o.modifiers:
  if m.type=='MULTIRES':m.levels=2;m.render_levels=2
  elif m.type=='MASK':m.show_viewport=False;m.show_render=False
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=bpy.data.meshes.new_from_object(e);c=bpy.data.objects.new('candidate_'+name,me);s=bpy.data.scenes.new(name);bpy.context.window.scene=s;s.collection.objects.link(c);c.rotation_euler.z=3.141592653589793
 bpy.context.view_layer.update();vs=[c.matrix_world@v.co for v in me.vertices];floor=min(v.z for v in vs);height=max(v.z for v in vs)-floor;scale=1.75/height
 for v in me.vertices:v.co.z-=floor;v.co*=scale
 mat=bpy.data.materials.new('gray');mat.diffuse_color=(.48,.51,.53,1);me.materials.clear();me.materials.append(mat)
 for f in me.polygons:f.use_smooth=True
 setup(s);s.display.shading.light='STUDIO';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.show_specular_highlight=False;s.render.resolution_x=1000;s.render.resolution_y=1400
 for key,pos in [('front',(0,5,.88)),('side',(5,0,.88)),('quarter',(2.6,5,1.65))]:
  s.camera=camera(s,'cam_'+name+key,pos,(0,0,.88),2.05);s.render.filepath=str(p/(name+'_'+key+'.png'));bpy.ops.render.render(write_still=True)
