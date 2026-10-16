# Preliminary mannequin bench-press technical review fixture — 0.1.0

Review only. This static technical fixture links the approved flat bench and 20 kg Olympic barbell unchanged. A fully editable hierarchy override supplies character pose and root highlight values while the body mesh and shared canonical rest skeleton remain linked. Local copies of shading node groups remap highlight drivers to the overridden root; no equipment/body mesh is copied or edited.

Build with scripts/blender/build_mannequin_bench_review.py in an empty Blender 5.1.1 session. Character root is rotated to face upward, with its pelvis near the foot end of the pad. Neutral profile +Y maps to world +Z; neutral headward +Z maps to world +Y. Exact root matrix, dependencies, source hashes and camera settings are in build-record.json, asset.json and previews/render-settings.json.

Pad top is 0.4572 m. Bar midpoint is (0, -0.07, 0.95) m; target grip stations are (-0.34, -0.07, 0.95) / (0.34, -0.07, 0.95) m. Both wrists use seeded two-bone IK with separate elbow poles, articulated finger poses and matching hand orientation. Feet use separate IK/poles with provisional ankle targets (±0.20, -1.02, 0.095) m. Bilateral pectorals are primary, triceps secondary. No motion or technique approval is implied.

Three-quarter, side and grip-detail PNGs are retained. Geometry checks reload the saved fixture, verify linked body data, mirrored grip frames, approximate floor clearance and zero body/bench evaluated triangle surface crossings. Source-equipment SHA pins stay unchanged. This is not a collision-free finger grip certification; palm/web deformation, thumb opposition, exact soles and extreme-pose anatomy require review. The source mannequin stays neutral and is never resaved by this builder. No rack, human duplication, plates or new equipment are created.

Results: assets/humans/models/168h_human_anatomical_mannequin/review-validation.json and validation.md. All files retain review status and unselected artwork release terms.


## Superseded human dependency — 2026-10-16

The user requests foundational correction before further exercise work. The saved fixture source is retained without geometry/pose edits, but its references may resolve to the successor human. Its 0.1.0 compatibility/renders are historical and are not validation evidence for the current mannequin. Do not use or refine this fixture until the corrected core pose suite is reviewed.
