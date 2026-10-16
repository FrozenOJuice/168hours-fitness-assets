# Human foundation core pose suite —0.2.1 REVIEW

Seven named static scenes: neutral_a_pose, arms_raised, elbow_flexion, seated, lying_supine, hip_flexion_knee_bend, bar_grip. This replaces exercise-first testing. Each scene is a hierarchy override with linked source skin and canonical rig data; local pose/control state, input drivers, shading node groups and cameras are separate. No duplicate source mesh, bench, rack, chair, clothing or new equipment model is created.

The bar-grip scene alone links the approved20kg Olympic barbell unchanged. Underhand stations are(±0.29,0.318,1.082)m with28 mm shaft diameter. The pose helper uses explicit IK/FK adapters, fitted articulated digit curls and multi-axis thumb opposition from retained grip-fit.json. Hands and palms are measured numerically; no force/safety claim.

Build with scripts/blender/build_mannequin_core_suite.py. Pose angles and control logic are in mannequin_core_poses.py; suite.json pins the source, helper and builder and names all scenes/collections. Each test has three-quarter/side PNGs; grip has one hand detail and overhead has three shoulder closeups,18views total. Exact cameras and WorkbenchFLAT/no-shadow/no-AO settings are in previews/render-settings.json.

Validate by reloading the saved suite with validate_mannequin_foundation.py. Results are retained with the human asset in foundation-validation.json: all 60 diagnostics pass. This includes topology/length/volume checks, knee X alignment and skin gaps, separate-leg and disjoint thigh/calf intersections, five knee angles, four IK position/orientation cases, explicit mode-transition continuity, linked mesh reuse and static grip clearance. Criteria are local diagnostics; anatomy and human visual approval remain manual.

Overhead lateral expansion is reduced with the0.2.1 localized shoulder corrective. Residual axillary/upper-arm simplification, arbitrary swing/twist/ROM and arbitrary gripping remain weaknesses. The canonical rig-data/rest profile stays0.2.0 while this fixture consumes character0.2.1. There is no full continuous-motion/self-collision certification. All scenes and the human remain review. The0.1.0 bench fixture is explicitly obsolete for this profile; it is not modified/revalidated as an exercise.

Final0.2.1 run:60foundation diagnostics and7surface regressions PASS. Actual-source Human V1 retains65missing-mask failures. Direct visual inspection and remaining high-flexion/shoulder limitations are recorded in the character SURFACE-REFINEMENT-REPORT.md. No owner approval is implied.
