# Gender-neutral anatomical mannequin — 0.1.0 review prototype

Specified before modeling on 2026-10-16. The current user request authorizes this first human, provisional implementation choices, poses and a separate technical bench-press fixture. It does not approve a human visual reference or change Human Model Contract V1. Status remains **review**; this asset is not production ready.

## Governing references and immutable scope

Follow AGENTS.md, docs/asset-workflow.md, docs/visual-style.md, docs/asset-conventions.md, docs/category-standards.md, and docs/contracts/human-v1/README.md. `prebuild-record.json` pins the reviewed standards, all existing equipment and existing fixtures. `review-validation.json` checks those bytes remain unchanged. A16 in docs/decisions.md records local choices; H01–H05 remain open.

## Dimensions, axes and origins

| Quantity | Value | State |
| --- | --- | --- |
| Neutral skin stature / minimum Z | 1.750000 m / 0 m | Measured; 1.75 m design choice provisional |
| A-pose X span / Y depth | 1.443881 m / 0.331347 m | Measured envelope, including hands / feet |
| Root / collection instance offset | (0, 0, 0) m | V1 floor projection under pelvis |
| Canonical pelvis head | (0, 0, 0.94) m | Measured provisional rest profile |
| Upper arm / forearm bone lengths | 0.295 / 0.255 m | Provisional anatomy profile |
| Thigh / shin bone lengths | 0.430 / 0.415 m | Provisional anatomy profile |
| Hand / finger articulation | 0.095 m hand bone; three bones per digit | Exact V1 names; lengths provisional |
| Neutral foot length | approximately 0.277 m | Original sculpt, not footwear measurement |

Meters, +Z up, +Y anterior/front, +X anatomical left. Neutral arm/forearm/hand chains descend 45° from horizontal. Bone local Y points head-to-tail; local Z is the V1 projected anterior vector. Root, solver, output and body object transforms are identity/unit positive scale. Bone rest coordinates intentionally contain joint positions. Floor root is an intentional contact datum, not the geometric center. `rest-profile.json` is the measured 53-bone profile and SHA256 fingerprint; `human-contract.json` contains the exact 11 anchor frames.

## Geometry and anatomy decisions

Original loft-based torso, neck/head, limbs, palms, articulated digits and feet are united by a 2.8 mm voxel remesh. The final neutral skin is **one closed connected mesh: 318,766 vertices, 318,764 quad faces, zero nonmanifold edges**. Construction solids are not delivered as disconnected visible limbs. Local surface fairing and subtle pectoral/sternum/abdominal/nasal/orbital displacement provide a smooth mannequin surface; no genital geometry, hair, clothes, branding, texture or external model is used.

A separate original left vastus intermedius volume sits beneath the anterior thigh and follows `thigh_l`. Its 240-vertex source is subdivided twice for the review. It is a simplified demonstration volume, not a medical dissection. General anatomical placement was reviewed against OpenStax Anatomy and Physiology 2e, sections [11.5 upper limb](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs) and [11.6 lower limb](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs). These references do not verify this sculpt or its measurements. No third-party artwork was imported.

Neutral anatomy still needs artistic review, especially shoulder contour, the hip transition, hands, and facial simplification. The high-density voxel mesh is a review sculpt; animation-oriented retopology, twist handling and corrective shapes have not been certified.

## Rig and interfaces

The separate rig file publishes canonical armature data for all **53 V1 bones, 52 deforming**. The character links that data into separate local objects: `168h_rig_mannequin_v1__armature_solver` and `168h_human_anatomical_mannequin__armature_deform`. Output pose bones copy the private solved transforms; only the output skins the body. Private controls are not export skeleton bones.

The manifest maps root-motion/pelvis, all 52 FK controls, four hand/foot IK targets, four elbow/knee poles and four root IK/FK switches. Fingers are individually posed with three segments per digit. The four two-bone IK chains disable stretching. Arm pole angles are -π/2 on both sides; leg angles are 0 left / π right. These are local solver choices, not shared standards. Start a tiny elbow/knee bend before enabling IK from the perfectly straight A-pose (`enable_ik` helper); automatic FK/IK snapping, singularity recovery, twist controls and animation blending have not been validated.

Four local hinge constraints provide provisional engineering guardrails, recorded in the manifest. They are not approved clinical ROM limits or a complete anatomical joint-limit system. Shoulders, wrists, hips and fingers still need reviewed constraints before production animation.

All 11 anchors are bone attached except floor contact: floor_contact, pelvis, back_support, bilateral hand_grip, foot_contact, heel_contact and toe_contact. Neutral hand-grip centers use a 34 mm anterior offset from the wrist plane and a 55 mm distal offset, provisionally tuned to the existing 28 mm shaft. Back support is ray-measured on the actual posterior skin. Posed frames follow the solved output. Different bodies need new measured profiles/contact adapters; V1 naming does not guarantee direct action reuse or automatic retargeting.

## Muscle implementation and X-ray

All **78 canonical IDs**, 78 group bindings, and 156 independent root properties (`highlight_primary__<id>`, `highlight_secondary__<id>`, values 0–1) are preserved. **Only 13 masks are implemented:** bilateral pectoralis major, anterior/middle/posterior deltoid, biceps brachii, triceps brachii, and left vastus intermedius. The remaining **65 empty masks fail full-coverage validation**. They are not substituted with unrelated skin regions.

Actual surface-region FLOAT attributes and selectable vertex groups drive Geometry Nodes Color fields after skinning. Primary is muted red; secondary is warm amber; primary takes precedence in a region. These local review colors need approval. Masks deform with the skin. The local `xray_enabled` property removes a defined front-left thigh patch to expose real underlying skinned deep geometry on the character; a driven fairing modifier softens the aperture. This is an experimental cutaway/X-ray presentation, not optical transparency or a separate diagram. Both neutral and bent-thigh examples are rendered. Aperture edge, depth readability and exact anatomical boundaries remain review items.

No garments exist. Through-clothing highlighting, complete anatomy coverage, activation-role accuracy and anatomical expansion are **not validated**. All existing core IDs remain unchanged.

## Materials and rendering

Muted gray matte body with a restrained computed-normal value ramp, not photoreal skin. No image textures. Asset-local Workbench FLAT/VERTEX, Standard/None/exposure 0/gamma 1, native dark object outlines, 32 AA, opaque white, no cast shadows, no AO/cavity/specular. Geometry-node grayscale endpoints and highlight colors are recorded in `previews/render-settings.json`; no shared preset is approved by this asset. Neutral/demo renders are 1200 × 1600; the linked fixture is 1600 × 1000. Native outline width is renderer controlled. Equipment source materials are unchanged; assembly uses Workbench's material fallback on equipment without Color attributes.

`previews/` retains front/back/side/three-quarter, muscle front/back, bent limbs, hand grip, neutral deep X-ray and bent deep X-ray. The separate fixture retains assembled three-quarter, side and grip-detail renders. Indices pin native sources, settings, camera matrices, frame and PNG digests. No export/animation format or pixel tolerance is approved here.

## Compatibility fixture and observed limits

`scenes/templates/168h_template_mannequin_bench_press/` links the approved flat bench and Olympic barbell unchanged and uses a local hierarchy override of the character. Its body mesh and canonical rest data remain linked; only local pose/highlight state and shading node groups vary. No equipment or body mesh is duplicated into the fixture.

The preliminary pose uses 680 mm grip spacing and bar center (0, -0.07, 0.95) m. Measured hand anchors are within 0.002 mm of mirrored shaft stations. Body/bench evaluated surface-crossing check passes after moving the pelvis toward the pad's foot end; no dimensions or approved equipment were changed. This demonstrates assembly interfaces, not safe exercise technique or a collision-free moving grip. Hands still need contact polish; shoulder/hip/palm deformation shows limitations at large rotations. Sole contact is approximate and requires manual review. Self intersections and bar/finger clearance throughout motion are unverified.

## Reproduction and use

See `USAGE.md`. Fresh construction requires an empty target character source; never overwrite this source by rerunning the builder. Original build sequence is build_anatomical_mannequin.py → polish_mannequin_surface.py → finalize_mannequin_review.py → prepare_mannequin_review_source.py → refine_mannequin_skinning.py → finish_mannequin_presentation.py. One-shot guards prevent cumulative sculpting. Scripts and stage records retain digests; same-version regeneration is recorded, not claimed pixel exact.

Render existing source with render_anatomical_mannequin.py. Build the technical fixture with build_mannequin_bench_review.py. Run inspect_human_contract.py, validate_human_contract.py, validate_mannequin_review.py and the 47 Human V1 unit tests. Exact commands and expected partial failures are in validation.md. Blender 5.1.1/no add-ons is provisional for this review.

## Approval / release boundaries

Review the physique and sculpt, mask boundaries, red/amber palette, deep cutaway, rig ergonomics, constraints and grip/deformation quality. H01–H05 remain unresolved globally. No approved equipment, shared contract definition, shared visual standard or existing fixture changed. The user has not approved this mannequin. Original artwork licensing remains unselected and separate from MIT code/documentation. Full coverage, garments if supported, retarget/replacement tests, anatomy acceptance, animation and export roundtrips block production readiness.
