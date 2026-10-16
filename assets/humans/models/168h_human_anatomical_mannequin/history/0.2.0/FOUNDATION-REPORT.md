# Human foundation correction report —0.2.0 / REVIEW

The neutral surface and bind were replaced under the same reusable asset/root/object interfaces. This is a foundation correction, not a bench-press refinement. Four neutral renders and a separate seven-state test library with15 renders are current. No approved equipment or shared Human V1 definition changed. The rejected0.1.0 source, rig, specs/profile and renders remain retained.

## What changed

| Area | Correction |
| --- | --- |
| Human silhouette | Adapted CC0 continuous quad topology replaces the voxel-union body; coherent ribcage, waist, pelvis, limbs, palms and feet |
| Proportions / bind | Measured provisional1.75 m profile;53 canonical bones remeasured/rebound; exactV1rest axes/A-pose preserved |
| Face / chest | Simplified gray anatomical mannequin face; smooth chest reduces secondary-sex emphasis |
| Skinning | Anatomical source weights explicitly merged/normalized into52 deform groups, individually articulated digits, volume-preserving skinning |
| Knees | LocalX hinge/locked transverse IK axes; continuous posterior soft-tissue compression removes measured thigh/calf intersections |
| Hands / feet | Palm-roll/source-leg-splay adapters; feet/toes rebound coherently; static per-digit/thumb fit to existing28mmshaft |
| Rig controls | Separate solver/output maintained; explicit two-way IK/FK snap helpers tested; no extra export bones |
| Native file | Clean scene/UI repack resolves inherited dirty-load flag; geometry hash identical before/after; inspector guard unchanged |
| Consumers | Old bench fixture explicitly invalidated; no exercise work performed; new linked core tests replace its evidence |

Source provenance is references/makehuman/provenance.json: official CC0 graphical files at commit `a8bc2d54ff0ac92e78ff71431b1023eda42bf482`. No upstream program logic/add-on is installed/imported. Original scripts/docs remain MIT separately; project artwork terms still unselected.

## Validation evidence

| Evidence | Result | Scope |
| --- | --- | --- |
| Human V1 unit suite |47 PASS | Schema/semantic/fault-injection tooling |
| Pinned registry |142 PASS /0 FAIL | Canonical definition/schema integrity |
| Actual saved-character inspection |392 PASS /65 FAIL | All failures are empty muscle masks; no waiver |
| Foundation diagnostics |60 PASS /0 FAIL | Actual saved native model and seven linked states |
| Protected inputs |213unchanged files | Equipment, normativeV1/schemas, origin/style/workflow rules and original rig |

These counts overlap and must not be added as independent coverage. Full contract/release status is not PASS. Anatomical/manual owner approval is not inferred from numerical structure tests.

## Core test results

| Pose / case | Measured result | Review limit |
| --- | --- | --- |
| Neutral A-pose |1.75 m skin height, floor0, one connected closed214,050 vertex skin;53 bones/11 frames and normalized transforms pass | Physique/silhouette needs owner acceptance |
| Arms raised | Correct canonical lengths and finite continuous surface; whole-body volume ratio1.08314 | Shoulder/scapular area broadens too much; needs further polish before production |
| Elbow flexion110° | No stretch; stable continuous skin, volume ratio0.99806 | Extreme flexion/twist not exhaustively tested |
| Seated90°hip/knee | No inward knee X drift; knee skin width retained≈100%; zero separate-leg/thigh-calf crossings | Posterior crease remains visually sharp; no seat/pad fit claimed |
| Supine | Rigid root orientation maintains geometry/volume and front/up directions | Not a bench contact/technique test |
| Hip80° /knee105° | No inward drift or tested leg intersections; knee lateral skin gap≈83.55 mm | No full-ROM certification |
| Knee sweep0,30,60,90,105° | Zero disjoint thigh/calf surface crossings at all five samples | Sparse diagnostic sweep, not all motion |
| Four hand/foot IK cases | Max target position error≈0.0103 mm; orientation axes match | Only sampled reachable targets/poles |
| FK→IK /IK→FK | Max position residual≈0.0025 mm /0.00014 mm using explicit helpers | Raw float toggles do not provide a snap UI |
| Static underhand bar grip | Mirrored580 mm stations; every sampled digit/palm outside14mmshaft radius; closest gaps≈0.356–0.505 mm | Only28mmshaft/static pose; surface-vertex sampling is not full collision simulation |

Grip testing was extended from fingers to palms: an actual2.625 mm palm penetration was detected and fixed by moving the virtual grip center4 mm in the palm-normal direction and refitting digit curls. Little-finger fitting needed a coarse search to escape a bad local minimum. Criteria were not weakened. Final datum is68 mm distal/32 mm normal; all anchor names/frame semantics remain unchanged. The approved barbell is linked byte-for-byte intact.

## Remaining weaknesses and review decisions

- Full overhead shoulder/scapular silhouette still looks broad; the current53-bone facade has no certified scapular/twist adapter. Numeric volume preservation does not mean the shape is artistically accepted.
- High-flexion hip/posterior-knee/elbow creases need artistic review. Current sample intersections are resolved; arbitrary combinations and full self-containment are not proven.
- Forearm pronation/supination, extreme wrist/ankle rotations, unreachable IK and a general animator UI are not fully tested. Explicit snap helpers are required for tested mode transitions.
- Only the measured static underhand28mmgrip is demonstrated. Other bar diameters, overhand/neutral grips, finger self-collision, force/pressure and moving contacts remain unvalidated.
-13muscle demonstrations are provisional remaps;65 masks remain empty. No muscle anatomy/coverage, deep effect, clothing, alternate physique, retarget or export acceptance is claimed by this pass.
- Body profile, human illustration preset, numeric anatomical limits and artwork release terms remain provisional/H01–H05 open.

Keep status REVIEW. Review this neutral mannequin and core suite before returning to exercise scenes. Do not promote these local diagnostic limits or proportions to shared standards.
