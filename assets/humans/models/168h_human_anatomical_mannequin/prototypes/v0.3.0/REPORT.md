# Mannequin anatomy foundation review —0.3.0

**Recommendation:** retain this isolated CC0-derived prototype as the stronger anatomy foundation for the next review. Neutral anatomy is substantially more recognizable than the preserved smooth predecessor. **It is not yet a production-quality deformation or complete muscle-highlight asset.** Do not replace the master or resume finished exercise-scene production on the strength of structural tests alone.

## Selection and rights

Selected Dan Ulrich's Body Male - Realistic from official Blender Human Base Meshes1.4.1, plus a localized same-topology female-pelvis blend. Official native collection metadata identifies both as CC0. Source archive/native hashes, embedded license evidence and six candidate screening renders are retained under references/. RESEARCH.md compares the predecessor, realistic/stylized Blender bodies, MB-Lab, Z-Anatomy and an older BlendSwap basemesh. The selected body has actual coherent anatomical surface forms and an editable10582vertex quad cage; it is unrigged and still requires character-specific deformation work. No paid assets/subscriptions, executable download imports or installed add-ons.

CC0 allows commercial copying, adaptation and redistribution: https://creativecommons.org/publicdomain/zero/1.0/. Project original artwork/rig/corrective additions retain unselected release terms, separate from MIT scripts/docs. Source choice does not change any repository-wide artwork grant.

## Delivered implementation

- One continuous closed169,362vertex/169,360quad skin, provisional1.75m adult stature, floor root, canonical45°A-pose, correct meter axes and normalized transforms.
- All53V1output bones, articulated digits, private solver/FK/IK facade,11bone-owned/full-frame anchors and measured rest profile. New proportions require retargeting; old animations cannot simply be assumed compatible.
- Corrected finger landmarks, normalized manual weight refinements, shared-mesh hybrid shoulder skinning, neutral-bound joint fairing, pose-driven knee relaxation and posterior soft-tissue compression. No added output/deform bones.
- Muted gray normal-driven illustrated rendering, dark silhouettes, no cast shadows/AO/specular/photographic textures. Numeric human preset is asset-local/provisional.
- All78muscle IDs/156primary-secondary root controls retained.14nonempty superficial masks and one schematic deep region demonstrate independent colors and posed local revelation.63regions remain unimplemented and fail coverage validation.
-13linked pose/highlight states,32test/comparison renders;7neutral/body-torso references. Approved barbell is linked only for grip and remains byte-identical.

## Visual findings

| State | Observed result / remaining weakness |
| --- | --- |
| Neutral A-pose + standing | Coherent human silhouette; pectoral/deltoid/arm/abdominal/quadriceps/calf forms visible without highlights. Muscular shoulders/chest and face still lean masculine; universal gender-neutral proportions are not approved. Back tonal ramp is darker than front. |
| Arms raised | Original severe shoulder wings greatly reduced by removing torso leakage and locally blending DQ/LBS. Simplified axillary/latissimus contours and long underarm stretch remain; no dynamic scapular anatomy or full twist/sweep validation. |
| Elbow flexion | Articulated bend and recognizable arm volume; elbow crease/volume still simplified. No full-range forearm pronation/supination evidence. |
| Seated | Legs bend coherently and sampled knees do not cross. Groin/thigh transition and lower abdomen pinch; hands remain in diagnostic A-pose position, not a natural seated action. No bench/body support-contact certification. |
| Supine | Whole-body orientation is correct and recognizable, no exercise assembly. No soft support compression or detailed floor-contact claim. |
| Hip flexion/knee bend | Anatomical leg remains coherent and sampled thigh/calf crossing corrected. Strong visible fold/ridge around anterior hip/groin remains; this is a real visual limitation despite the numeric knee PASS. |
| Squat | Both legs bend symmetrically; no sampled thigh/calf or distinct-leg crossings. Deep knee folds and bulky groin/lower-abdominal compression remain too stylized for finished exercise illustration. Snapshot is a deformation stress test, not coached squat technique. |
| Bar grip | Four fingers curl around the actual28mm shaft. Measured anchors align; sampled fingers clear the shaft. Palm~8.4mm away and thumb opposition incomplete: usable rig/contact prototype, unfinished grip. |
| Primary/secondary highlights | Independent channels change actual posed skin colors; source muscle forms remain visible. Masks are soft analytic approximations (pectoral masks visibly too rectangular), not anatomical segmentation. |
| Deep Xray neutral/flexed | On-character aperture reveals a skinned red schematic vastus-intermedius volume in both states. Jagged cutout and partial occlusion remain visibly rough; no anatomically accurate attachments/contraction. |
| Old/new comparison | Equal1.75m scale and identical SINGLEgray/STUDIO diagnostic shading, no shadows/AO/specular. Old viewer-left/new viewer-right; new surface forms are stronger. Comparison is not a claim of shared rest-profile/animation equivalence. |

## Validation and limits

Existing unit suite47PASS; registry/schema142PASS; saved-native and offline contract394PASS/63FAIL (only missing bindings). Local actual-source/study diagnostics57PASS/0FAIL.385protected source/contract/equipment/prior fixture files unchanged. Detailed values/criteria in validation.md and machine-readable reports. Current source `86bad3bb57a1bd1789d2f759aa485fbd957e64d971998c463b757f9b5d7cb1a2`; study `15a21d8ee932b7cfe6a6770a5317a9b0c96236249beeb437db0acf9c72a8dc7f`; rest profile `9d06d26065ddc915329877aed6a49563f599614fe67972e6a1d303b40b2dce0a`.

These are sparse read-only diagnostics, not full collision/containment, realistic biomechanics, clinical anatomy, production retargeting, alternate body/garment support or export certification. Native private GN/correctives must be baked/adapted for external pipelines. H01–H05 release decisions remain open. The source and saved study are review-only; no asset approval or shared contract change.

## Opening and continuing

Character: `/Users/joeldehoog/Developer/168hours-fitness-assets/assets/humans/models/168h_human_anatomical_mannequin/prototypes/v0.3.0/168h_human_anatomical_mannequin.blend`

Linked pose/comparison study: `/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_mannequin_anatomy_study/168h_template_mannequin_anatomy_study.blend`

Rest-data library (controls live in character): `/Users/joeldehoog/Developer/168hours-fitness-assets/assets/humans/rigs/168h_rig_mannequin_v1/prototypes/v0.3.0/168h_rig_mannequin_v1.blend`

Open the character for neutral source work. Open the study and select a named scene in Blender's scene selector to inspect the13saved states; source geometry stays linked. All authoritative PNGs are in the respective previews folders. Render ZIPs are separated into unassembled and tests/comparison under exports/illustrations; delivery-audit.json records exact package/file hashes.

Next work should prioritize artist-led hip/groin and shoulder motion correctives, palm/thumb fit and source-aligned superficial masks, followed by a wider pose/motion and replacement test suite. The current source is a convincing improvement to neutral anatomy, not an excuse to declare those unfinished systems complete.
