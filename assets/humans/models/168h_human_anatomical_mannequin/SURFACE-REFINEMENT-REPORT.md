# Mannequin0.2.1 surface / shoulder review —2026-10-16

**Status: REVIEW; owner anatomy/style approval pending.** This refines the existing continuous0.2.0 mesh. No topology replacement, Human V1 definition, canonical rest profile, equipment artifact, muscle-mask expansion, clothing, variant or exercise scene was created or changed.

## Chest investigation and correction

Raw neutral skin and fully evaluated neutral skin differ by at most0.000133mm. The protrusion therefore originates in the base geometry, rather than skinning or a live modifier. Inspection of the0.2.0 refinement script identifies a bounded chest flattening ending atZ1.18m. The retained mesh has an abrupt upper-abdominal ledge beneath that flattened chest: the largest anterior median-depth change between adjacent25mm height bands is22.242mm.

Direct editing of the same vertices refits a continuous anterior chest/ribcage/waist/abdominal envelope, with broad restrained pectoral forms, shallow sternum/inferior separation and subtle rectus relief. The largest adjacent-band change is now4.792mm. These bands are a repeatable local diagnostic, not an anatomical population standard. Front, side and three-quarter torso closeups visually confirm removal of the pointed ledge. Posterior torso and full neutral views were inspected for comparable discontinuities; no comparable isolated torso protrusion was found. Normal broad scapular, pelvic and gluteal forms are retained.

## Shoulder investigation and correction

The merged graphical shoulder/clavicle weights extended too far into the torso. DQ skinning additionally expands mixed shoulder rotations. The same overhead test remains25degrees clavicle elevation plus110degrees upper-arm change from45degree A-pose; the test was not made easier.

17,477upper-torso vertices receive localized ribcage/clavicle/humerus ownership, followed by32iterations of actual edge-neighbor weight fairing. An independent post-skin corrective per arm offsets overhead DQ expansion toward measured linear-skin positions, adds a smooth axillary lift and fairs the posed shoulder surface. Maximum stored combined vector is121.168mm in the extreme overhead target; this is a substantial deformation correction, not a small cosmetic shading adjustment. It is zero in neutral, ramps from30to110degrees upper-arm localZ elevation, and does not replace the existing knee corrective or alter hand skinning.160neighbor blur iterations soften the residual local creases.

The same preserved rest-index shoulder region's largest lateral X extremum drops from286.112mm to232.844mm (53.269mm inward per lateral extremum). This measures reduced bulging, not anthropometric correctness. Five unilateral elevations0/30/60/90/110degrees produce finite geometry and leave the other arm's correction at0. Modifier-input drivers remap per hierarchy override, so scenes do not share pose factors.

This is a frontal-plane elevation prototype. It does not implement a full scapulothoracic mechanism or arbitrary swing/twist-aware corrective system. It remains under review; numerical improvement does not approve anatomy.

## Anatomy, proportions and illustration

Same214,050vertices /214,048quads and exact face indices; one continuous closed body. Existing deltoid/arm forms, quadriceps and calves receive restrained geometric relief. The chest and abdomen are sculpted directly; these details read without muscle highlights. Hip/flank/glute emphasis is reduced modestly for a more neutral illustration. Hands/finger coordinates remain exactly unchanged. Height stays1.75m provisionally; measured rest skeleton and all11anchors are unchanged.

The local normal-value ramp has stronger gray contrast, with native dark silhouettes. Flat vertex color, no lights/cast shadows, no AO/cavity/specular, opaque white and the existing32AA/color-management setup remain. This is an asset-local review choice, not a shared human preset or palette approval. Back-facing areas are intentionally darker in the fixed root-space normal ramp; that bias remains a style review item.

## Visual review of all seven core states

Reviewer: Codex, direct PNG inspection,2026-10-16. This is an implementation review, not owner acceptance or medical/anatomical certification.

| State | Inspected evidence / finding |
| --- | --- |
| Neutral A-pose | Full front/back, torso front/side/three-quarter; pointed under-chest ledge removed, continuous torso, readable restrained relief. Muscle detail is still simplified. |
| Arms raised | Three-quarter and shoulder side/three-quarter closeups; large wing-like bulge substantially reduced and clavicular creases smoothed. Some upper-arm contour flattening and simplified axillary fold remain. |
| Elbow flexion | Three-quarter; elbows bend coherently and hands remain articulated. Inner elbow crease is still stylized. |
| Seated | Side; knees remain separated/aligned, calf/thigh folds visible. Posterior-knee and groin creases are still sharper than a finished anatomical model. |
| Lying supine | Three-quarter; coherent torso and limb orientation; root placement is a rigid support test, not compressible-body-on-bench validation. |
| Hip flexion / knee bend | Three-quarter; no visual inward knee collapse. High-flexion groin fold and upper-thigh transition remain stiff. |
| Bar grip | Three-quarter and hand detail; retained mirrored underhand fit, fingers articulate around the unchanged approved28mm shaft. Thumb opposition remains simplified; arbitrary grip shapes are not certified. |

Seven neutral/torso PNGs and18core-suite PNGs are current. Three shoulder detail views supplement the standard overhead side/three-quarter views. Separate delivery ZIPs contain these two groups and their render settings; authoritative evidence remains in the corresponding previews folders.

## Validation and remaining limits

The seven additional surface regressions pass: exact topology, zero neutral corrective, identical hands, smoother anterior torso profile, reduced overhead lateral expansion, independent unilateral shoulder sweep and read-only source preservation. Final foundation checks:60PASS/0FAIL, including knee sweep, source/suite links,53-bone lengths, IK/FK transitions and static grip. Final actual-source/offline Human V1:392PASS/65FAIL, solely missing masks. Results are recorded in validation.md and their JSON reports. Overhead whole-body volume changes from predecessor1.08314×neutral to current0.96946×neutral; this is diagnostic, not local-anatomy certification. Sampled digit/palm closest gaps remain0.356–0.505mm with zero sampled penetration.47Human V1 unit tests and142registry checks pass.65unimplemented muscle bindings continue to fail full contract coverage; no masks were added or falsely accepted.

Remaining weaknesses: pose-specific shoulder field rather than general shoulder mechanics; contour flattening at extreme elevation; sharp high-flexion groin/posterior-knee/inner-elbow folds; untested forearm pronation and extreme wrist/ankle/twist; sparse pose samples rather than full-motion self-collision certification. The160iteration posed fairing adds evaluation cost and needs future profiling before animation production. Static underhand28mm fit does not guarantee arbitrary grips. Partial anatomy masks, clothing, variants, retarget/export, H01–H05 and artwork terms remain unresolved.

Reproduction and geometry/weight/corrective parameters: SPEC.md, surface-refinement.json and scripts/blender/refine_mannequin_surface_v021.py. Preserved0.2.0 source, matching rig and renders are under history/0.2.0. Ordinary re-rendering uses render_mannequin_core.py and build_mannequin_core_suite.py. Keep review status; do not resume exercise posing on the strength of diagnostic passes alone.
