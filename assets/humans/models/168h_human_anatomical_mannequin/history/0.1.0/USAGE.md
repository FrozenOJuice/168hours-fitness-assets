# Open and use the review mannequin

Open `168h_human_anatomical_mannequin.blend` in Blender 5.1.1. Keep the repository folder structure so its relative rig-library link resolves. The saved character opens in neutral A-pose; F12 renders the native three-quarter camera. Saved viewport is solid FLAT with vertex colors, outlines and no shadows/AO. In a different workspace select Solid → Color Type: Attribute/Vertex (Color) to see the evaluated Geometry Nodes colors; Material Preview/Cycles does not implement this local Workbench display pipeline.

The already posed linked example is `scenes/templates/168h_template_mannequin_bench_press/168h_template_mannequin_bench_press.blend`. Open it separately to see the bench/barbell example. This delivery does not replace a file already open in another Blender session; reopen the intended path.

Select `168h_human_anatomical_mannequin__root` in the Outliner, Object Properties → Custom Properties. Each implemented region has `highlight_primary__muscle_...` and `highlight_secondary__muscle_...` (0–1). For example set `highlight_primary__muscle_pectoralis_major_l` to 1. Set `xray_enabled` to 1 plus `highlight_primary__muscle_vastus_intermedius_l` to 1 for the on-character deep window. Empty masks intentionally do nothing and fail coverage.

Unhide `168h_rig_mannequin_v1__armature_solver` in the Outliner to pose its FK bones. Do not edit the output skeleton, linked rest data, or attachment transforms. Hand/foot target and elbow/knee pole empties are under the character rig collection. Root properties `ik_fk_arm_l/r` and `ik_fk_leg_l/r` select FK=0 / IK=1. Seed a small bend before enabling a straight rest chain; moving targets beyond chain reach will not stretch the bones. There is no certified FK/IK snap tool yet.

For reproducible transient demonstrations, use Blender's Python Console (absolute path shown; no file is saved):

```python
import sys
sys.path.insert(0, '/Users/joeldehoog/Developer/168hours-fitness-assets/scripts/blender')
import mannequin_review_common as review
review.MAPPING = None
review.pose('muscles')  # or neutral, bend, grip, xray, xray_bend
review.neutral()
```

Run this in the standalone mannequin file. The linked fixture uses its own override mapping; do not run the standalone helper blindly there. Use its saved pose or the fixture builder. Rendering scripts reopen saved sources and do not save demonstration changes to the master. Source root, rest pose and collection pivot stay neutral for reuse.

Render bundles contain pictures only. Keep the complete repository/LFS sources to open linked Blender assets. No add-on or downloaded model is required.
