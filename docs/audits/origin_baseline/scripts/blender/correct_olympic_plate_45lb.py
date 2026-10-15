"""Correct existing 0.1.3 typography tangents and blend spoke roots to 0.1.4.
Existing objects/data are retained; BARBELL glyph geometry is regenerated.
Body and non-BARBELL topology are preserved. Includes a full-plate 180-degree proof.
"""
from pathlib import Path
import bpy,hashlib,json,math
from mathutils import Matrix
REPO=Path(__file__).resolve().parents[2]
ID='168h_equipment_olympic_plate_45lb_cast_iron'
ASSET=REPO/'assets/equipment/free_weights'/ID
SOURCE=ASSET/f'{ID}.blend'
PREDECESSOR='61557cd8d31ded1c5d6700792ad8b2e7e7b6924099315056047a3d2f55d8ca13'
VERSION='0.1.4'
settings=json.loads((ASSET/'previews/render-settings.json').read_text())
input_digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene;root=bpy.data.objects[ID+'__root']
body=bpy.data.objects[ID+'__mesh_body'];ribs=bpy.data.objects[ID+'__mesh_ribs']


def topology(m):
 return hashlib.sha256(json.dumps({'edges':[list(e.vertices) for e in m.edges],'faces':[list(p.vertices) for p in m.polygons]},separators=(',',':')).encode()).hexdigest()


def coords(m):
 return hashlib.sha256(json.dumps([list(v.co) for v in m.vertices],separators=(',',':')).encode()).hexdigest()


pointers={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
topologies={m.name:topology(m) for m in bpy.data.meshes}
body_coords=coords(body.data)
anchors={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}
if root.get('asset_version')=='0.1.3':
 assert input_digest==PREDECESSOR
 for facing,sign in [('front',1),('back',-1)]:
  standard=bpy.data.objects[ID+'__mesh_label_standard_'+facing]
  centers=[]
  for index in range(8):
   offset=math.radians(-24+48*index/7);angle=math.pi/2-offset
   centers.append((.165*math.cos(angle),.165*math.sin(angle),index))
  for vertex in standard.data.vertices:
   u=-sign*vertex.co.x;v=vertex.co.z-.225
   cu,cv,index=min(centers,key=lambda p:(p[0]-u)**2+(p[1]-v)**2)
   # Rotate the entire glyph along the circle, preserving its tangent angle.
   delta=(.001/.165) if index<=3 else -(.001/.165)
   c,s=math.cos(delta),math.sin(delta)
   u,v=c*u-s*v,s*u+c*v
   vertex.co.x=-sign*u;vertex.co.z=.225+v
  standard.data.update();standard['nd_additional_arc_gap_m']=.002
 # Bury the root cap under the inner hub, retaining the original mesh rings.
 for component in range(8):
  sign=1 if component<4 else -1
  angle=math.radians([45,135,225,315][component%4]);c,s=math.cos(angle),math.sin(angle)
  width=.017;radius=.043;bottom=.0118;top=.0140
  cross=[(-width,bottom),(width,bottom),(width,top-.0012),(width-.0013,top),(-width+.0013,top),(-width,top-.0012)]
  for index,(tangent,axial) in enumerate(cross):
   ribs.data.vertices[component*24+index].co=(radius*c-tangent*s,sign*axial,.225+radius*s+tangent*c)
 ribs.data.update();ribs['radial_rows_m']=[.043,.075,.150,.205]
 ribs['hub_root_transition']='root cap below hub face; emerges gradually through shoulder'
 root['asset_version']=VERSION
 root['corrected_from_sha256']=PREDECESSOR
elif root.get('asset_version')!=VERSION:raise RuntimeError('Unsupported source revision')
# Generate clean BARBELL glyph geometry on a normal upper arc, then rotate
# the ENTIRE word 180 degrees in the plate plane. This avoids inheriting any
# malformed per-vertex glyph grouping from the earlier inversion operation.
barbell_groups={}
for facing,sign in [('front',1),('back',-1)]:
 target=bpy.data.objects[ID+'__mesh_label_barbell_'+facing]
 vertices=[];faces=[];groups=[]
 for index,char in enumerate('BARBELL'):
  offset=math.radians((index-3)*(48/7))
  angle=math.pi/2-offset
  cu,cv=.165*math.cos(angle),.165*math.sin(angle)
  turn=angle-math.pi/2;c,t=math.cos(turn),math.sin(turn)
  curve=bpy.data.curves.new(ID+'__corrected_glyph_temporary','FONT')
  curve.body=char;curve.align_x='CENTER';curve.align_y='CENTER'
  curve.size=.027;curve.extrude=.00175;curve.bevel_depth=.000162
  curve.bevel_resolution=2;curve.resolution_u=8
  obj=bpy.data.objects.new(ID+'__corrected_glyph_temporary',curve)
  bpy.data.collections[ID+'__geo'].objects.link(obj)
  bpy.context.view_layer.objects.active=obj;obj.select_set(True)
  bpy.ops.object.convert(target='MESH')
  data=bpy.context.object.data
  low=min(v.co.z for v in data.vertices);high=max(v.co.z for v in data.vertices)
  base=len(vertices)
  for vertex in data.vertices:
   x,y,z=vertex.co
   upper_u=cu+c*x-t*y;upper_v=cv+t*x+c*y
   # Literal whole-word 180 degree steering-wheel rotation about plate center.
   u,v=-upper_u,-upper_v
   axial=.0062+(z-low)/(high-low)*.0038
   vertices.append((-sign*u,sign*axial,.225+v))
  faces.extend(tuple(base+i for i in polygon.vertices) for polygon in data.polygons)
  groups.append({'character':char,'first_vertex':base,'vertex_count':len(data.vertices),
                 'upright_upper_arc_center_m':[cu,cv],'upright_glyph_angle_radians':turn})
  bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(data)
 target.data.clear_geometry();target.data.from_pydata(vertices,[],faces);target.data.update()
 for polygon in target.data.polygons:polygon.material_index=0 if sign*polygon.normal.y>.8 else 1
 target['orientation']='literal_whole_word_180_from_upright_upper_arc'
 target['arc_glyph_spacing_degrees']=48/7
 barbell_groups[facing]=groups
for curve in list(bpy.data.curves):
 if curve.users==0:bpy.data.curves.remove(curve)
for font in list(bpy.data.fonts):
 if font.users==0:bpy.data.fonts.remove(font)
assert pointers=={o.name:(o.as_pointer(),o.data.as_pointer() if o.data else None) for o in bpy.data.objects}
assert all(topologies[m.name]==topology(m) for m in bpy.data.meshes if 'barbell' not in m.name)
assert body_coords==coords(body.data)
assert anchors=={o.name:[list(row) for row in o.matrix_local] for o in bpy.data.objects if 'anchor_' in o.name}
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE),check_existing=False)
digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest();script_digest=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
record={'version':VERSION,'predecessor_version':'0.1.3','predecessor_sha256':PREDECESSOR,'source_sha256':digest,
 'script_sha256':script_digest,'all_object_and_mesh_data_identity_preserved':True,
 'all_non_barbell_mesh_topology_preserved':True,'mesh_topology_sha256':{m.name:topology(m) for m in bpy.data.meshes},'barbell_glyph_geometry_regenerated_in_existing_datablocks':True,'barbell_glyph_groups':barbell_groups,
 'body_coordinates_unchanged':True,'body_coordinate_sha256':body_coords,'anchors_unchanged':True,
 'standard_nd_additional_arc_gap_m':.002,
 'barbell_orientation':'normal upper-arc BARBELL rotated as a whole 180 degrees about plate center',
 'barbell_tangent_correction':'clean upright upper-arc glyph geometry rotated as an entire word 180 degrees; shared 48/7 degree tracking with STANDARD',
 'rib_root_radius_m':.043,'rib_root_top_axial_m':.014,'hub_face_axial_m':.0145,
 'rib_root_base_axial_m':.0118,'root_cap_buried':True}
(ASSET/'correction-record.json').write_text(json.dumps(record,indent=2)+'\n')
settings.update(source_sha256=digest,asset_version=VERSION,preset='plate_review_flat@0.1.4',
 correction_script='scripts/blender/correct_olympic_plate_45lb.py',correction_script_sha256=script_digest,predecessor_sha256=PREDECESSOR)
camdata=bpy.data.cameras.new(ID+'__camera_reference');cam=bpy.data.objects.new(ID+'__camera_reference',camdata)
scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO'
# Retain the standard four views; add a physical camera-roll check equivalent
# to turning the plate 180 degrees like a steering wheel.
config=dict(settings['camera_views']['front'])
roll=(Matrix.Rotation(math.pi,3,'Z'))
front_rotation=Matrix.Identity(3)
from mathutils import Euler
front_rotation=Euler(config['rotation_euler_xyz_radians'],'XYZ').to_matrix()
config['rotation_euler_xyz_radians']=list((front_rotation@roll).to_euler('XYZ'))
config['path']=str((ASSET/'previews'/f'{ID}__rotated_180_check__standing.png').relative_to(REPO))
config['purpose']='Full plate rotated 180 degrees in image plane: BARBELL must read like ordinary upright upper-arc text.'
settings['camera_views']['rotated_180_check']=config
for view,config in settings['camera_views'].items():
 cam.location=config['position_m'];cam.rotation_euler=config['rotation_euler_xyz_radians'];cam.data.ortho_scale=config['ortho_scale_m']
 scene.render.filepath=str(REPO/config['path']);bpy.ops.render.render(write_still=True)
(ASSET/'previews/render-settings.json').write_text(json.dumps(settings,indent=2)+'\n')
print('PLATE_TYPOGRAPHY_ROOT_CORRECTION_COMPLETE',digest)
