# Asset category standards

Level 2: category-specific requirements, inheriting the [shared technical conventions](asset-conventions.md) and [global style guide](visual-style.md). Do not copy those shared values into a second competing standard. Status: the documentation requirements are mandatory; origin/axis/transform/link rules are approved under A14; other numerical/technical defaults remain proposed under A03 unless approved. Human V1 establishes its logical skeleton interface under A15; this does not select equipment dimensions, material implementations or a built rig.

Every asset uses the shared ID, meter/axis, transform, naming, and metadata contract unless an approved exception says otherwise. Each specification must select the applicable row below and explicitly declare its implemented interface and required anchors. Suggested anchor names in the common guide are not proof that an interface exists. Record local position and orientation, tolerances, and the rest configuration for every published anchor.

| Category / location | Required specification details | Origin, attachments, and compatibility |
| --- | --- | --- |
| Human models — `assets/humans/models/` | [Human V1](contracts/human-v1/README.md): measured rest profile, anatomy/muscle masks, binding, clothing highlighting and supported compatibility class | Floor root under pelvis; exact11 anchors and53-bone output interface; no proportion-independent contact guarantee |
| Rigs — `assets/humans/rigs/` | Human V1 skeleton/roll/A-pose, private controls mapped to FK/IK facade, limits/solver/skin/export evidence | A15 establishes the interface portion of A02; H01–H05 implementation/profile choices and actual production evidence remain open |
| Free weights — `assets/equipment/free_weights/` | Overall dimensions, grip diameter/length, plate/hole/sleeve sizes, weight labels and source, load configuration, reusable plate/handle components | Functional origin by subtype under A14; declare `grip_center` or `grip_l`/`grip_r` and `load_l`/`load_r` where applicable; verify hand fit and plate/sleeve clearance; mass labels never substitute for measured size |
| Benches — `assets/equipment/benches/` | Pad/support height, width/length, frame footprint, adjustment pivots and angle ranges, supported configurations | Floor footprint root; declare seat/back support and floor frames as applicable; verify support/contact and pose at supported adjustments |
| Racks — `assets/equipment/racks/` | Upright spacing, footprint/height, hole pitch, hook/safety heights, bar clearance, configurable components | Floor footprint root; document bar-support and attachment frames, naming any additions in the spec; verify compatible bars, load ranges, and safety clearances |
| Machines — `assets/equipment/machines/` | Frame, seat/pad and handles, travel/adjustment limits, pivots, load points, movement path; simplified mechanisms and rationale | Floor footprint root; declare handle, seat, load, and floor frames as applicable; validate moving contacts and clearances across supported range |
| Materials — `assets/materials/` | Semantic purpose, palette references, node/datablock names, inputs/ranges, dependencies, outline interactions, shadow-free behavior | No geometry root required; stable slots and input interfaces; use a documented common preview fixture when authorized; renderer compatibility declared |
| Styles — `assets/styles/` | Palette roles, outline settings, color management, emphasis controls, render compatibility, preset version | Published preset/datablock interface instead of geometric anchors; test against representative human/equipment fixtures; A04–A05 govern open choices |
| Exercise scenes — `scenes/exercises/` | Linked asset versions/configurations, required interfaces, poses/actions and timing, contact offsets, motion ranges, camera/style presets | Scene placement roots and constraints target published anchors; validate substitution and contact throughout motion; no duplicated source geometry |
| Scene templates — `scenes/templates/` | Camera transforms/framing, render settings, background/alpha, color management, style dependencies, supported composition bounds | Stable camera/preset names; no dependency on exercise scenes; demonstrate reuse with different compatible subjects |

## New categories and interfaces

Human-specific update2026-10-15: [A15](decisions.md#a15--human-model-contract-v1)
establishes [Human Model Contract V1](contracts/human-v1/README.md), superseding
only the prior human origin/skeleton/rest-pose proposals and corresponding
opening disclaimer. Equipment rules remain unchanged. No human/rig exists yet;
profile, anatomy, renderer and export implementations still require approval.

Use existing components and interfaces where possible. If a new category or incompatible interface is needed, propose it in [Decisions](decisions.md) with affected assets, rationale, migration, and validation evidence. Publish the approved contract here or in the common guide, then reference it from individual specs. Do not invent exact equipment dimensions, anatomy standards, topology budgets, or rig compatibility to fill a template.

## Category release evidence

The [shared review checklist](review-checklist.md) applies to every category. Add category-specific measurements and interface cases to the asset's own validation record. A non-geometric asset may mark geometric checks `N/A` with a reason, but still needs an interface test, reproducible visual evidence, and licensing review. A first asset without an existing compatible replacement uses a documented fixture and remains explicit about which interchangeability claims are untested.

## Olympic weight plates — technical interface and visual reference

A09 authorized development of the [45 lb cast-iron plate](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/SPEC.md); A10 now approves its 0.1.4 appearance as the first equipment visual reference and the current standard for future traditional cast-iron plate assets. Technical interface ratification remains separate. Proposed reusable interface `olympic_plate_bore@0.1.0` uses +Y for the bore/stack axis; historical0.x used a floor-level root. A14 now requires the bore-center root and `olympic_plate_bore@1.0.0`, preserving the accepted appearance, and `bore_center`, `stack_front`, `stack_back`, and `floor_contact` anchors. Record each plate's actual bore-center height and stacking envelope; scenes align via anchors rather than assume the root is the bore center. Front/back stack frames define the maximum axial envelope, including lettering. Future plates must explicitly declare diameter, bore minimum, bore clearance/chamfers, rim/hub/web profile, nominal weight label, and stack pitch. Do not assume all 45 lb cast-iron plates have a 450 mm diameter.

Review instances may share linked collection/mesh data; rotation of the whole instance changes facing without negative scale. A sleeve fit is a measured clearance claim, not proof of real-barbell compatibility. Real consumer substitution remains required before claiming production interoperability. Promote or change this contract only through A03/A09 approval and compatibility review.

### Approved cast-iron plate visual reference

Reference **`cast_iron_plate_visual@1`**: `168h_equipment_olympic_plate_45lb_cast_iron`, geometry version **0.1.4**, user-approved 2026-10-14 under **A10**. The [approval record](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/reference-approval.json) pins the exact source and five images; the [asset specification](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/SPEC.md) distinguishes visual acceptance from provisional engineering settings. This is the first visual-direction reference in the equipment library, with normative inheritance scoped to traditional cast-iron plates. Other equipment may use it as a style cue, not as a geometry mandate.

Future cast-iron plates must preserve this visual family unless an explicit approved variation applies:

- Traditional, brand-neutral casting silhouette with a raised outer lip, recessed face, structured center hub and defined side waist.
- Four diagonal raised ribs per face that narrow outward and emerge smoothly from the center-ring shoulder; no abrupt cap drawn across the hub face.
- Matte charcoal surfaces with restrained flat value separation, near-white readable **actual raised mesh lettering**, and darker extrusion sides. The approved reference swatches/implementation are captured in its metadata; do not silently introduce a different appearance.
- Balanced viewer-relative weight labels on both faces. This 45 lb reference uses 45 LB left and 20.4 KG right; other weights must use their own correct nominal labels.
- STANDARD follows a clean upper arc with adequate N–D separation. BARBELL is laid out as ordinary upright upper-arc text, then rotated **as a whole** 180° about the plate center; it must look normal when the whole plate is turned like a steering wheel. Retain the rotation-proof review case.
- Clean illustrated treatment, precise silhouettes and selective structural edge definition; no cast/contact shadows, AO/cavity, baked shadows, or photoreal wear/noise.

Compare future front, side, three-quarter and reverse images against the pinned reference at equal output scale. Inspect both unrotated and 180°-rotated typography. Reference geometry is a visual/proportion example; **do not copy its provisional 450 mm diameter, 33.02 mm envelope, profile dimensions or absolute text/rib sizes into other assets as approved physical standards**. Use measured/manufacturer dimensions and declared bore/stack interfaces per the shared conventions. A different renderer is acceptable only after documented image comparison and applicable technical approval; visual acceptance does not choose the library renderer.

The accepted source/renders are frozen for this reference. Do not regenerate or polish them merely to align metadata. An authorized future change requires retained predecessor evidence, a versioned successor and explicit approval before replacing the reference. Optional polish is recorded in the asset spec and is not current work.


## Approved equipment origin contract (A14)

User origin-audit request and explicit root/pivot migration approval,2026-10-15. This supersedes the old blanket floor-root proposal for free weights; no visual/material standard changes.

| Profile | Required functional origin | Canonical orientation | Required anchors |
| --- | --- | --- | --- |
| olympic_plate | Exact circular mounting-hole center, at mid-depth | Bore/stack+Y, radial planeXZ, +Z up | bore_center at root; stack_front/back at actual axial envelope; floor_contact |
| olympic_barbell | Shaft-axis midpoint between overall ends | Shaft+X, +Y front, +Z up; subject-left loading+X | axis_center and grip_center at root; load_l/r and sleeve_end_l/r on sleeve axes; floor_contact |
| flat_bench | Floor level, horizontal center beneath support footprint | Length/head+Y, width+X, +Z up | floor_contact at root; pad_center, seat_center, back_support on support surfaces |
| rack / machine | Floor level, horizontal supported-footprint center | +Z up, +Y user-facing; machine motion axes explicitly declared | floor_contact plus applicable support/load/handle frames |

Collection insertion pivot and root must coincide in authoring coordinates. Source floor height and intentional component origins must be documented; geometry centroids are not acceptable automatic substitutes. New profiles need a measurement strategy, dimensions, anchor frames and consumer tests. Rack/machine numerical geometry/axes beyond the above remain unspecified until actual category work; their supplied profiles are starting rules, not evidence of existing assets or interchangeability. Common transform/linking math and validation commands live in [shared conventions](asset-conventions.md#automated-origin-validation). Existing asset roots migrated with world geometry/appearance preserved; exact predecessor references archived under docs/audits/origin_baseline. Current root/interface versions are1.0.0 for plate/barbell; bench stays0.1.1.
