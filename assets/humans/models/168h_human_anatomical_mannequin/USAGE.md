# Review the corrected mannequin0.2.0

Open `168h_human_anatomical_mannequin.blend` from this folder in Blender 5.1.1. Reopen the file if another Blender window still shows0.1.0. The saved source is neutral A-pose and the native camera renders the whole model. Keep repository folders intact for the relative rig-library dependency.

Open scenes/templates/168h_template_mannequin_core_poses/168h_template_mannequin_core_poses.blend and use Blender's Scene selector to switch among the seven named tests. Each scene's active camera is its three-quarter view; additional side/detail cameras are named in its Outliner and suite.json. No skin is duplicated per test. Do not use the old bench-press fixture as current validation evidence.

Use Solid viewport shading → FLAT → Vertex/Attribute color (Color), outlines on, shadows/cavity/specular off. This asset-local display uses Geometry Nodes colors; Material Preview/Cycles is not the recorded illustration pipeline. Final review PNGs are under previews/ and the core suite's previews/.

Unhide `168h_rig_mannequin_v1__armature_solver` to pose FK bones. The animation/output armature remains separate. Targets/poles and root IK/FK float properties retain V1 names. Use explicit snap helpers for mode changes, not a raw mode toggle. The automatic posterior-knee modifier is driven by shin flexion and is zero in rest; do not manually force its inputs or edit anchors to fake contacts.

For standalone transient tests in Blender's Python Console:

```python
import sys
sys.path.insert(0, '/Users/joeldehoog/Developer/168hours-fitness-assets/scripts/blender')
import mannequin_review_common as review
import mannequin_core_poses as core
review.MAPPING = None
core.pose('seated') # any name from core.POSES
core.pose('neutral_a_pose')
core.snap_ik('arm', 'l')
core.snap_fk('arm', 'l')
```

Use this only in the standalone source. Saved suite scenes have separate override mappings; the builder handles them. No demonstration helper saves the source automatically. Root custom muscle properties still exist but coverage is incomplete; use the foundation suite for this review.

From repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/render_mannequin_core.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/build_mannequin_core_suite.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_mannequin_foundation.py
python3 -m unittest discover -s tests -p test_human_contract.py
python3 scripts/pipeline/validate_human_contract.py
```

The source inspector and character validator commands are in validation.md. They deliberately fail the65 missing muscle bindings. Legacy0.1.0 routines are version guarded. A fresh structural correction requires retained predecessor inputs and an explicit review revision; current pose/render reproduction uses the saved source and grip-fit.json, not a blind full rebuild. Fitting scripts are measurement tools for this static28 mm grip and must not silently redefine other grips or shared standards.

ZIPs contain review renders/settings/docs, not self-contained native model bundles. Use the complete repository/LFS files to open linked models.

## Current0.2.1 review

Reopen the master .blend from disk to see the refined mesh; an already-open Blender session does not reload it automatically. The linked0.2.0 measured skeleton library is intentionally unchanged. Current render packages contain7neutral/torso views and18core-test views. Shoulder correction is a pose-driven, frontal-elevation prototype; do not claim arbitrary twist compatibility. See SURFACE-REFINEMENT-REPORT.md.
