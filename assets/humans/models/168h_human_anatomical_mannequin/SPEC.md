# Anatomical mannequin — 0.2.1 surface / shoulder refinement / REVIEW

This preserves and refines the continuous0.2.0 human foundation, which replaced the rejected0.1.0 prototype. Neutral anatomy, joint binding and core pose behavior are the targets. Do not resume exercise-scene work until this foundation is reviewed. No approved equipment, shared V1 definition, visual standard, clothing or alternate character is changed/created.

## Governing standards and scope

AGENTS.md; docs/asset-workflow.md; docs/asset-conventions.md; docs/category-standards.md; docs/visual-style.md; docs/licensing.md; docs/contracts/human-v1/README.md and its pinned JSON registries. A17 and its0.2.1 refinement entry in docs/decisions.md, foundation-plan.json and surface-refinement-plan.json document the authorized provisional implementation. The protected213-file digest set remains unchanged. Version0.1.0 source/profile/spec/renders are retained in history/0.1.0; its openable source is under that folder's library/assets/humans/models/168h_human_anatomical_mannequin/. Its original rig-data source also remains intact.

## Anatomy and geometry correction

Replaced the loft/voxel-union surface and distance-to-bone weights with adapted **CC0 MakeHuman hm08 body-only quad topology and graphical joint/weight data**. Source and licensing are pinned in references/makehuman/provenance.json. No upstream application code, add-on, texture, human rig hierarchy or animation is imported. Source graphical skeleton measurements/weights are adapted to our existing53-bone contract, not adopted as a new contract.

The new surface gives coherent clavicle/deltoid transitions, a distinct ribcage and waist, continuous pelvis/gluteal mass, shaped thigh/calf/knee contours, recognizable palms/digits and natural feet/toes. The0.2.0 chest simplification left an abrupt anterior upper-abdominal ledge;0.2.1 corrects the underlying surface with a continuous chest/ribcage/abdominal profile. Subtle pectoral, rectus, deltoid, arm, quadriceps and calf relief is actual mesh geometry. Modest hip/flank/glute reduction softens sex-specific emphasis; owner proportion review remains pending. Facial features remain simple and texture free. Body-only source is13,380 vertices/13,378 faces; subdivision yields **214,050 vertices /214,048quad faces**, one connected closed skin with zero nonmanifold edges. Helper clothing, genitals, hair, eyes, teeth, joint-marker and other separate source groups are excluded. Existing left deep-muscle demonstration geometry remains a separate skinned component, not part of this correction's anatomy acceptance.

Source-frame/palm and leg-splay adapters repose the graphical data into V1. Feet are translated/rebound as a coherent foot including toes; merely flattening an inclined toe source frame had lifted the forefoot and was corrected. Torso and limbs remain one continuous surface rather than separate visible solids.

## Dimensions and origins

| Quantity | Measured current value | Approval state |
| --- | --- | --- |
| Skin stature / floor | 1.750000 m /0 m | Measured fit; stature provisional |
| A-pose span X / envelope depth Y | 1.312810 m /0.310128 m | Measured; body profile provisional |
| Shoulder joint spacing | 0.351352 m | Measured; not percentile data |
| Hip joint spacing | 0.195439 m | Measured provisional profile |
| Pelvis / knee / ankle head Z | 0.940711 /0.474217 /0.074359 m | Measured |
| Upper arm / forearm / hand bone | 0.238422 /0.237061 /0.101002 m | Measured graphical-profile lengths |
| Thigh / shin bone | 0.441282 /0.399858 m | Measured |
| Grip offset / tested shaft | 68 mm distal,32 mm palm normal /28 mm diameter | Local measured static fit |

These are original adapted illustration proportions, not clinical, universal or population-percentile standards. Body mesh envelope includes fingers/feet. Actual bone coordinates and roll are in rest-profile.json with fingerprint mannequin_1750_foundation@0.2.0. The previous profile is not direct-pose compatible.

Meters; +Z up, +Y anterior, +X anatomical left. Identity source root/armatures/body transforms, positive unit scale and collection offset0. Intentional floor root below pelvis, not geometry centroid. Axial bones point +Z; arm/forearm/hand descend45°; canonical digits, straight -Z legs and +Y toe rules remain exact. All53names/parents/deform/connectivity semantics and11anchor names/owners/full frames are preserved. Foot/heel/toe anchors remain on the neutral sole plane; back support is measured on the new posterior skin; hands use the measured grip envelope. Origins/axis semantics are not redesigned.

## Rig and deformation implementation

A separate0.2metric native library publishes the measured53-bone rest data. Original0.1rig file is preserved. The character links the0.2data into separate private solver and canonical solved-output objects. Required root/pelvis/FK controls, hand/foot IK targets, poles and four IK/FK switches retain their mapped names. Only solved output skins the body; no extra export/deform bones are introduced.

Source graphical weights are merged by the explicit source-to-core adapter in foundation-build.json and normalized. Root weights map to deforming pelvis; facial weights map to head, source split limb weights to their canonical limb, metacarpals to hands and separate source toes to the single canonical toe. All fingers remain individually articulated. Dual-quaternion skinning preserves joint volume.0.2.1 localizes clavicle/humerus ownership in the upper torso and smooths the changed weights over32edge-neighbor iterations. Skinning alone still overexpands high-elevation shoulders, so an asset-local corrective follows it; no certified twist-distribution adapter exists.

Knees and elbows use anatomical localX flexion; native IK transverse axes are locked, stretching is disabled and provisional limit fields are explicit. Engineering ranges are illustration guardrails, not approved clinical ROM. **Posterior knee soft tissue has a continuous pre-skin corrective field**: up to18 mm anterior compression at90° flexion, smoothly limited to1.25×, with105 mm axial/90 mm transverse falloff and posterior-only masking. It is zero at rest and driven by actual solved shin localX. Per-object modifier-input drivers keep all seven linked instances independent. This removes measured thigh/calf surface crossings at90°/105° while preserving the canonical skeleton and neutral silhouette.

mannequin_core_poses.py supplies explicit snap_ik/snap_fk helpers. They retain current solved frames and use nonzero bend seeds/poles for the exactly straight V1 rest pose. Four sampled reachable targets and both switching directions are measured. Directly toggling float modes is not an automatic snap UI; large twist, singular poles/unreachable targets and a full animated sweep are not certified.

## Seven core pose tests

The separate linked suite contains named scenes for neutral_a_pose, arms_raised, elbow_flexion, seated, lying_supine, hip_flexion_knee_bend and bar_grip. Body geometry/rest data are linked; only pose controls, driver copies and cameras vary. Each scene has three-quarter and side views; bar_grip also has a hand detail. There is no bench-press scene, chair or clothing in this suite.

Raised arms combine25°clavicular elevation and110°upper-arm change from the45°A-pose; this is a provisional simplified shoulder/scapular adapter. Elbows flex110°. Seated hips/knees are±90°. The unilateral test uses hip80°/knee105°; a separate five-sample knee test covers0,30,60,90,105°. Supine is a rigid whole-root orientation/floor-placement test. Static underhand grip uses mirrored580 mm stations on the approved barbell at(0,0.318,1.082)m. The bar source is unchanged. Per-digit curl and multi-axis thumb-opposition fits are retained in grip-fit.json. Palm testing caught2.625 mm penetration missed by finger-only tests; a4 mm normal datum correction and refit resolved it without weakening criteria.

## Visual setup and muscle scope

Muted gray, smooth texture-free anatomical mannequin, simplified face, clean illustrated appearance and native dark silhouettes. WorkbenchFLAT/VERTEX, Standard/None/exposure0/gamma1,32AA, white opaque background; no cast shadows, AO/cavity, specular or baked shadows. Local normal-value ramp is documented in previews/render-settings.json. Numeric human style remains review-only; no shared preset changes.

All 78 canonical muscle IDs and156primary/secondary properties remain. Only13existing demonstrations are provisionally remapped;65 empty masks continue to fail full coverage. Boundary/anatomy acceptance, deep-X-ray polish, through-clothing, alternate bodies and exports are not priorities or validated claims in this pass. Seven current neutral references (four full-body and three torso closeups) and18core-pose references (including three overhead shoulder closeups) replace the current render package;0.1.0 renders remain archived.

## Validation and limits

See validation.md and FOUNDATION-REPORT.md. Current actual-source inspection checks53 bones,45°rest, origins/normalized transforms, anchors and weights. Full contract reports392 PASS/65 FAIL, all65failures being unimplemented muscle masks. The unchanged contract software has47passing unit tests and142passing registry checks. Foundation diagnostics have60 PASS/0 FAIL, including closed skin, pose topology/lengths/volume, knee alignment/gaps/intersections/sweep, IK frames/switching and static digit/palm fit. Diagnostic tolerances are local review measurements, not shared approved contact standards or anatomy certification.

Remaining weaknesses: improved but still simplified overhead shoulder/scapular mechanics, pose-specific corrective and residual axillary/upper-arm contour flattening; residual sharp soft-tissue creases at high flexion; untested forearm pronation/twist and extreme wrist/ankle motion; sparse pose/contact sampling; one static underhand28 mm grip rather than arbitrary equipment grasping; unreviewed proportions/anatomical mask boundaries. No production/clinical/retarget/export or collision-free motion claim. The old bench fixture is explicitly invalidated, not revalidated or refined.

## Native source and reproduction

Open the main .blend for neutral review, or the core-suite .blend and choose its named scene. USAGE.md lists controls and exact commands. Re-render existing source with render_mannequin_core.py; rebuild the seven-state diagnostic fixture with build_mannequin_core_suite.py. The original correction, joint-field, native repack, grip fitting and datum scripts plus stage digests record the0.2.0 construction. refine_mannequin_surface_v021.py modifies that preserved mesh directly; it does not rerun the upstream mesh adapter or change topology. Use retained fit parameters for current reproduction; refit only after geometry, proportions or grip diameter changes. One-shot/version guards protect masters and rejected predecessors; do not blindly rerun sculpt/bind scripts over a reviewed source.

Native scene/UI state inherited from the rejected prototype caused the dirty-load guard to fail even after stripping test copies. A factory-clean scene container and append of the same collection resolved it; native-repack.json proves identical skin geometry before/after. Inspector guards and V1 definitions were not relaxed.

## Licensing and approval

Upstream graphical data retain CC0-1.0 with full notices and exact repository commit. Original adapter/scripts/docs are MIT; project artistic output remains outside MIT with release terms unselected. The source model, rig and all tests remain **review**. A17 authorizes the correction, not visual or production approval. H01–H05 remain open. Review the neutral human, core tests and remaining shoulder/twist/contact weaknesses before returning to exercise work.

## 0.2.1 anatomy / deformation refinement

See surface-diagnosis.json, surface-refinement-plan.json, surface-refinement.json, surface-refinement-validation.json and SURFACE-REFINEMENT-REPORT.md. The chest issue existed in raw neutral vertices: maximum raw/evaluated deviation0.000133mm. The previous bounded chest cap caused a22.242mm median anterior-depth step between adjacent25mm height bands. Direct continuous mesh editing reduces that step to4.792mm, without hiding it with materials, overlays or modifiers. The posterior torso was visually checked; no comparable isolated ledge was found. Hands/finger coordinates are identical to0.2.0; no additional masks were implemented.

The shoulder corrective is an original per-asset prototype, not a new V1 semantic. A post-skin vector field offsets the measured overhead DQ expansion toward the linear-skin result, with a smooth axillary lift of up to70mm and inward25mm nominal fields. The measured combined displacement, rather than those component amplitudes, is recorded in surface-refinement.json. A160iteration neighbor blur fairs only the shoulder-weighted posed region. Independent modifier inputs use each private upper-arm localZ elevation:0 through30degrees, linear ramp to1 at110degrees, clamped thereafter. The canonical output rig, rest profile, all11anchor frames and existing knee correction remain unchanged. Driver targets are remapped separately for every saved hierarchy override. This directional corrective is tested in the documented frontal-plane raise; arbitrary swing/twist and motion paths need further work.

The local gray normal ramp increases amplitude from0.28to0.70 and bias from0.57to0.43; low gray endpoint becomes(0.12,0.145,0.16), high endpoint(0.62,0.65,0.67). Native dark outlines, flat vertex colors, opaque white background and no shadows/AO/cavity/specular remain. This is a provisional human-only review preset, not a shared palette change. Normals produce directional tonal contrast without physical lights or occlusion.

Neutral front/back/side/three-quarter and torso front/side/three-quarter images are indexed in asset.json and previews/render-settings.json. All seven core states are regenerated in the separate linked suite, with overhead front/side/three-quarter shoulder details. No bench-press work, equipment edits, variants or garments.

For reproducible refinement replay, use an isolated checkout: restore history/0.2.0/168h_human_anatomical_mannequin.blend to the master source location, retain its matching0.2rig dependency, remove only the replay checkout's surface-refinement.json one-shot marker, and run refine_mannequin_surface_v021.py. Never run the adapter/replacement builder on the current source. Replay geometry/weights are reproducible; Blender save-container bytes may differ. Ordinary review only needs render_mannequin_core.py and build_mannequin_core_suite.py, which do not edit the character source. Run validate_mannequin_surface_v021.py in addition to the existing foundation and Human V1 checks.
