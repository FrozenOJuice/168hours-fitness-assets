# Anatomical mannequin V0.3.1 — refinement specification

Review only. User selects the CC0 V0.3 foundation and authorizes autonomous refinement. Preserve V0.3.0, its continuous skin/rest profile/53-bone interface/78IDs/11anchor frames and all approved equipment. Governing AGENTS, V1 registries and existing category/style/workflow/licensing guides remain unchanged.

Before implementation: improve skin-weight ownership and general joint-angle-driven soft tissue across shoulder sweeps and hip/knee motion, not one named pose; measure palm/finger/thumb contact on actual28mm shaft, preserve existing anchor frames and document any scene-owned contact offset. Trace superficial mask boundaries on the actual selected anatomy with smooth mesh-connected regions rather than rectangular analytic fields. Keep missing coverage failing. Replace topology-deleting Xray with continuous skin, smooth local opacity and a skinned deep volume. Asset-local emission/transparency renderer experiment is authorized by this request; no global renderer/palette change. Normal references retain the existing flat illustrated preset, no cast shadows/AO.

Retest neutral/standing/overhead/elbow/sitting/supine/hip/knee/squat/grip, expand multi-direction shoulder and lower-limb samples, compare against preserved V0.3.0 under equal rendering. Do not certify retarget/export/clothing/medical anatomy or unseen motion. Record all scripts/measurements, observed weaknesses and source/render hashes; keep review.


## Finished implementation for review

Version0.3.1 retains the same169,362vertex/169,360quad continuous CC0-derived skin and exact raw neutral coordinates as0.3.0. Provisional1.75m stature, floor root, +Zup/+Yfront/+Xanatomical-left, normalized transforms,53canonical bones and all11anchor rest frames are unchanged. The measured rest profile remains `mannequin_1750_anatomy@0.3.0`; the isolated0.3.0rig-data library is reused without modification. Old0.2master/profiles remain separate and require retargeting. Shared V1 definitions/equipment and prior0.3.0sources/evidence are preserved by plan.json.

### General deformation

Selected shoulder solution preserves prior ownership and applies70connected-mesh diffusion steps to thorax/clavicle/humerus weights, preserving per-vertex canonical influence totals. No named pose triggers, added weighted bones or special overhead sculpt. Existing local hybrid DQ/LBS skinning and neutral-bound48iteration CorrectiveSmooth are retained. A broad spatial repaint was rejected after forward-arm tests revealed new flaps from torso influence leaking onto the upper arm; the selected source restores original ownership before diffusion. Typical shoulder edge strain improves, while the worst local edge still worsens slightly. This is not a fully corrected scapular/axillary system.

Hip ownership now distinguishes anterior inguinal transition and posterior buttock/pelvis ownership, with local connected-weight fairing. A continuous0.82maximum LBS blend reduces DQ hip bulging; per-hip swing-magnitude relaxation uses65iterations and factor0..0.65, zero at rest, based on local X/Z rotation magnitude. Existing posterior knee compression and knee relaxation remain. These are general joint-angle fields, not pose-name conditions or physical simulation. Hip crease shape and strain measurements remain mixed; higher local strain is documented rather than mislabeled as full improvement.

### Hand contact and reusable controls

A measured palm patch drives the consumer-owned wrist contact offset in grip-contact-fit.json. Published rest anchors remain unchanged; scene configuration owns this offset, as V1 permits. Digits are independently fit against the actual28mm shaft using verified DQ sampling; thumb CMC uses three local axes for opposition plus two phalange flexions. Root/control interfaces remain intact.

Private additions: root `grip_contact_enabled` (default0) and `grip_radius_m` (default0.014), plus per-hand `__control_grip_cylinder_l/r` frames. The frame's localX is the cylinder axis; edit frame and radius to retarget the contact proxy. Geometry Nodes move only hand skin that lies inside radius+0.35mm outward radially, after skinning and before illustration colors. Current maximum adjustment4.851mm. It is a soft-contact prototype, not a replacement for correct finger pose or a universal collision/force solver. Fingers need refitting when diameter or grasp orientation changes.20/32mm diameter probes verify the correction responds; they do not certify complete grips at those diameters.

Private enable/radius properties are explicitly library-overridable. Reopened fixture tests exposed and corrected an initial persistence issue where enable1 reverted to source default0. All dependent references/checks were regenerated. Final saved-state palm gap0.683mm maximum, thumb0.350mm, maximum closest-finger gap2.193mm, zero sampled penetration.37,666selected actual hand triangles clear the infinite28mm cylinder by at least0.197mm. Wrist transition/end caps, contact pressure and finger/finger collisions are outside this diagnostic.

### Anatomical highlighting

Same78IDs/156channels;14superficial masks plus one schematic deep binding remain nonempty,63bindings remain FAIL. Pectoralis major follows an authored fan boundary on the actual rest surface. Rectus femoris uses an elongated tapered contour; deltoid caps and biceps/triceps use bone-local belly/cap shapes with anterior/middle/posterior partitions. Four connected-edge feathering steps soften boundaries. These are stored semantic vertex-group regions that deform with skin, not screen-space rectangles or separate diagram overlays.

Exact boundary coordinates/formulas are in refine_mannequin_v031.py/refinement-record.json. They are artist annotations, not clinical segmentation. Boundaries/partitions still require anatomy review; no remaining masks, clothing behavior or body variants are falsely declared complete. Anatomical reference: OpenStax upper-limb chapter, https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs; no diagrams imported.

### Localized X-ray translucency

The body no longer deletes skin geometry. All169,360skin faces remain even with Xray enabled. A smooth rest-surface field around the selected left deep thigh region is deformed with the character; GN evaluates `xray_alpha` from1outside to0.16inside. The material mixes transparent and vertex-color emission shaders using sorted BLENDED alpha. The existing skinned schematic vastus-intermedius volume appears behind translucent skin. Local opacity follows posing; no separate diagram, hole or detached overlay. The deep volume is not a new atlas reconstruction or simulated contraction.

Ordinary references retain Workbench FLAT/VERTEX and the existing numeric ramp/palette. Only named Xray fixture scenes use asset-local Eevee emission/alpha, shadows/GI/AO/specular off,64samples, opaque white world and1px Freestyle silhouettes. This is a provisional implementation experiment, not a shared renderer/style change. Workbench cannot display local material transparency; use the fixture Xray scenes in rendered view/F12 for the effect. Arbitrary alpha sorting, garments and external shader export remain unvalidated.

### Review, reproduction and licensing

Seven neutral/torso references and57movement/comparison PNGs.21saved states: prior core13; lateral/forward/diagonal arms, unilateral shoulder axial directions, hip abduction, lunge and Xray-disabled control. Eight comparison views cover neutral, shoulders, seated, hip bend and highlighting against preserved0.3.0. Pose angles are local illustration stress tests, not medical ROM or coached exercise demonstrations. Test signs/overlaps were visually inspected; hip-abduction sign and bilateral shoulder-test hand overlap were corrected in the test definitions.

Start from a preserved copy of0.3.0native/sidecars into sibling0.3.1; do not apply non-idempotent scripts over an already refined source. With Blender5.1.1background/factory-startup, ordered scripts: refine_mannequin_v031.py → add_mannequin_v031_contact.py → finalize_mannequin_v031_skin.py → finalize_mannequin_v031_contact.py → repack_mannequin_v031.py → fit_mannequin_v031_grip.py → render_mannequin_v031_neutral.py → build_mannequin_v031_review.py. Existing source/rig/refinement scripts and source provenance are retained, no paid dependencies/add-ons. The first broad repaint is an intermediate superseded by finalize_skin, not the delivered binding.

Run inspect_human_contract.py with local human-contract.json/observed.json; pipeline/validate_human_contract.py; validate_mannequin_v031.py; validate_mannequin_v031_movement.py; validate_mannequin_v031_renders.py; existing unit tests. Package with pipeline/package_mannequin_v031_review.py. Exact source/render/script pins are in the JSON records/delivery-audit. Not a byte-identical cross-machine or animation/export guarantee.

Upstream Dan Ulrich realistic male/female anatomy remains CC0; provenance/source/license evidence lives in preserved0.3.0/references and RESEARCH.md. No paid content. Original project artwork/rig/corrective release terms remain unselected, separate from MIT code/docs. User selects this foundation, not production acceptance. Status remains review; H01–H05 wider release gates remain open. See REPORT.md/validation.md for remaining failures and visual weaknesses.
