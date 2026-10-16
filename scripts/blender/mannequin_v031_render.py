"""Scoped Xray emission/transparency preset; ordinary views retain Workbench."""
import bpy
from barbell_20kg_common import setup as standard_setup

def setup(scene):
 standard_setup(scene)
 if 'xray' not in scene.name:return
 scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=64;scene.eevee.use_shadows=False;scene.eevee.use_fast_gi=False;scene.eevee.use_raytracing=False
 scene.world=bpy.data.worlds.new(scene.name+'__white_world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1
 scene.render.use_freestyle=True;style=scene.view_layers[0].freestyle_settings;lines=style.linesets[0] if style.linesets else style.linesets.new('silhouette');lines.select_silhouette=True;lines.select_crease=False;lines.select_border=False;lines.select_external_contour=True;
 if lines.linestyle is None:lines.linestyle=bpy.data.linestyles.new(scene.name+'__outline')
 lines.linestyle.color=(.12,.14,.15);lines.linestyle.thickness=1.0
