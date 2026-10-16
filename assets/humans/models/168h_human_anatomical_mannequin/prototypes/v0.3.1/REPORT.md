# V0.3.1 mannequin refinement — review report

The selected CC0 anatomical foundation is preserved. This iteration improves typical shoulder weight transitions, adds general hip/contact mechanisms, replaces rectangular muscle patches with anatomy-shaped contours, and replaces the X-ray cutout with actual localized skin translucency. **It remains a review prototype: shoulder/axillary compression and deep hip/groin folds are not fully corrected.** Some strain measurements worsen, so this is not an unqualified deformation-quality pass.

## What changed

- Shoulder skin retains the prior anatomical ownership, with 70 connected-mesh diffusion steps over thorax/clavicle/humerus influences. Existing hybrid DQ/LBS and bound corrective smoothing remain. Rejected repaint trials are documented; the source does not retain their severe forward-arm flaps.
- Hip weights distinguish anterior groin and posterior buttock/pelvis transitions. Local LBS/DQ blending and swing-driven relaxation apply continuously across movements. Existing knee corrections remain. No named-pose switches or new weighted bones.
- Palm position is measured against the actual skin. A consumer-owned wrist offset and three-axis thumb opposition improve the grasp. A private, editable cylinder-contact adapter prevents small skin penetrations without editing the barbell. Saved overrides now retain enable/radius settings after reload.
- Pectorals use a fan-shaped rest-surface boundary; deltoids/arms follow bone-local caps/bellies; rectus femoris uses tapered longitudinal contours. Connected-edge feathering replaces rectangular fields. Boundaries remain artist annotations requiring anatomy review.
- X-ray retains every skin face, smoothly lowers local opacity to 0.16 and shows the skinned schematic deep muscle through it. Sorted alpha blending removes the cutout/jagged aperture. Only these experimental views use emission-based Eevee with no shadows/AO/GI/specular; ordinary views retain the existing Workbench illustrated preset.

The neutral raw surface, stature, 53 canonical bones, rest profile, 78 muscle IDs, 156 highlight channels and 11 anchor frames remain unchanged. The 0.3.0 rig-data library is reused. All 486 protected inputs, including prior work, equipment and V1 definitions, retain their recorded bytes. No paid assets, subscriptions or add-ons.

## Validation

| Evidence | Result | Scope |
| --- | --- | --- |
| Saved source + reloaded linked fixture | 82 PASS / 0 FAIL | Core/expanded states, finite geometry, transforms/anchors, bone lengths, helper remapping, colors, continuous X-ray skin and sampled hand contact |
| Motion and contact suite | 90 PASS / 0 FAIL | 38 local-transform snapshots per version; retained knee-crossing checks, actual hand triangles, bounded contact correction and diameter response |
| Render on/off evidence | 2 PASS / 0 FAIL | Deep color visibly appears only in localized region; opaque background retained |
| Existing V1 unit tests | 47 PASS | Data/schema tests |
| Registry checks | 142 PASS / 0 FAIL | Canonical registry/schema pins |
| Native + offline V1 contract | 394 PASS / 63 FAIL | All failures are unimplemented muscle bindings, not silently waived |

These diagnostics establish bounded implementation behavior, not accepted anatomy or natural deformation. The manual quality/release gate remains FAIL. Full motion, finger-to-finger collision, clothes, alternate bodies, animation retarget/replacement and external export are unvalidated.

The saved grip has maximum sampled palm gap **0.683 mm**, thumb gap **0.350 mm**, closest-finger gap **2.193 mm**, and no sampled shaft penetration. **37,666 selected actual hand triangles** clear the infinite 28 mm shaft cylinder by at least **0.197 mm**. This conservatively contains the approved shaft's documented maximum radius; its knurl is recessed below that envelope. Wrist transition/end caps and forces are excluded. Contact correction moves skin by up to **4.851 mm**, below the declared local 6 mm diagnostic bound. The general adapter responds to 20/32 mm diameter probes, but those are not certified fitted grips.

X-ray on/off renders reveal 4,179 red pixels versus zero in the disabled control; only 0.605% of the full frame changes above the diagnostic threshold. All 169,360 skin faces remain. The deep volume is still schematic, not reconstructed anatomical attachments or contraction.

## Visual review and remaining issues

| Area | Observed outcome / limitation |
| --- | --- |
| Neutral anatomy | Existing continuous shape and muscle forms preserved. No new physique or anatomical acceptance inferred. |
| Forward/lateral/diagonal arms and twist | Typical strain decreases across tested directions; forward-80° p95 edge ratio falls from 1.604 to 1.508. Axilla/chest still compress and shoulders can look capped. Worst local ratios increase in some cases (forward-100° maximum 3.792→4.099); no claim that all shoulder deformation is fixed. |
| Overhead | Broad silhouette remains coherent; underarm/latissimus transition and shoulder elevation still simplified. No dynamic scapular mechanics or full animation-range approval. |
| Sitting / hip bend / squat | Hip volume changes and general relaxation are implemented; sampled thigh/calf crossings remain zero. Groin/abdomen folds and sharp creases remain. Hip-90°/knee-90° p95 strain rises from 1.034 to 1.112, with mixed local results: this cannot be called globally improved deformation. |
| Abduction / lunge | Expanded stress cases inspected. Abduction test sign was corrected to spread legs; lunge is a diagnostic, not coached exercise technique. No support/contact or universal self-collision certification. |
| Grip | Palm and thumb now reach the shaft with no measured selected-triangle penetration. Fingertip spacing and compressed contact patches still look stylized; natural thumb/palm shape and grasp transitions need further art review. |
| Muscle masks | Pectoral fans and tapered thigh shapes read more anatomically than rectangles. Deltoid partitions, arm boundaries and transitions still require review. Only 15/78 nonempty bindings; 63 remain failures. |
| Deep translucency | Skin stays continuous and fades smoothly around the deep region, including posed tests. Schematic deep form and alpha sorting over arbitrary camera/body motion remain limitations. Workbench cannot display this local material opacity. |

Selected neutral, shoulder, lower-limb, grip, highlight, X-ray and comparison images were visually inspected. Not every one of the 64 PNGs has independent human acceptance. The expanded tests intentionally expose remaining weaknesses; passing finite/bone/contact checks does not excuse them.

## Open the deliverables

Character: `/Users/joeldehoog/Developer/168hours-fitness-assets/assets/humans/models/168h_human_anatomical_mannequin/prototypes/v0.3.1/168h_human_anatomical_mannequin.blend`

Linked movement/comparison fixture: `/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_mannequin_movement_review/168h_template_mannequin_movement_review.blend`

The fixture opens in neutral A-pose. Choose a named scene in Blender's scene selector; use `bar_grip` for contact and `xray_neutral` / `xray_flexed` for rendered translucency. Normal source work stays in the character file. Seven neutral/torso PNGs plus 57 test/comparison PNGs remain in the respective previews directories. Eight comparisons show preserved 0.3.0 versus 0.3.1 under the same illustrated shading. Full paths, hashes and separate ZIPs are recorded in delivery-audit.json.

Provenance/licensing and ordered reproduction steps are in SPEC.md; original CC0 evidence remains under preserved 0.3.0/references and RESEARCH.md. Original project artwork release terms remain separate from MIT code/docs. Preferred-foundation selection is recorded, while production acceptance and broader H01–H05 release gates remain open.

Source SHA256: `a51881017d440550f11b87e436964c607bc7a31840f7c22756e1b5d7e52158ae`. Fixture SHA256: `9949045adbef708ca547860a0dbf8271afc90226c627ce09325593584d2c57dd`.
