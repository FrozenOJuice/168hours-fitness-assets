# 168Hours Fitness Human Model Contract V1

**Official interface: `168h_human_model@1.0.0`, established 2026-10-15 under
[A15](../../decisions.md#a15--human-model-contract-v1).** The user authorized this
shared human foundation. This establishes names, semantics, rest conventions and
compatibility gates; it does not approve a built character, rig implementation,
anatomical illustration or delivery preset. No model, animation or scene is
created by this contract. Existing equipment standards and accepted artifacts
remain unchanged.

This is the human/rig category extension of [shared conventions](../../asset-conventions.md),
not a competing style guide. Follow the [global style](../../visual-style.md),
[workflow](../../asset-workflow.md) and [licensing](../../licensing.md) requirements.
The machine-readable authorities are [contract.json](contract.json),
[skeleton.json](skeleton.json) and [muscles.json](muscles.json). JSON carries exact
lists; prose defines meaning. A disagreement is a failure requiring correction,
never permission to silently change the interface.
[contract-lock.json](contract-lock.json) pins the normative registries/schemas;
registry validation fails on drift. Update a lock only with a documented,
authorized contract revision, not to hide a broken test. Editorial prose does
not change an interface; breaking semantic changes require major-version migration.

## Skeleton, source frames and standard A-pose

The canonical animation skeleton has **53 bones**: one nondeforming `root`, six
axial deform bones, and23 per side. `_l` is the subject's anatomical left (+X),
`_r` right (−X). Bone names are the table below **without an asset prefix** so
animation paths are character-independent. Object/collection names retain the
existing `<asset_id>__<role>_<part>` convention. No `.L`, numeric suffixes or
automatic renaming. Parents and connected flags are exact in skeleton.json.

An assembled character publishes `<asset_id>` collection, `<asset_id>__root`
Empty, `__geo`, `__rig`, `__anchors`, and `<asset_id>__armature_deform` object.
The installation root and armature have identity transforms in source authoring
space; collection instance offset is zero. One unit is one meter. +Z up, +Y
anterior/forward, +X anatomical left. Place the root intentionally on floorZ0
under the pelvis bone head's XY projection, not at the mesh centroid. Pelvis
motion and root motion are distinct. Source mesh objects have positive unit
scale and zero rotation; construction translations must be documented. Scene
placement occurs on linked collection instances, using existing offset-aware
placement math; source posing uses validated overrides/adapters.

Rest requirements:

- Upright pelvis/spine/neck/head; axial bones point +Z. Both hips and shoulders
  are on their declared anatomical sides; feet point +Y with sole supportZ0.
- Upper arms, forearms and hands extend straight in the XZ plane, **45° below
  horizontal** on each side. Shoulders/clavicles are character measurements.
  Palms face +Y. Elbows and knees are straight in the bind rest pose; do not
  silently add bend to avoid an IK singularity.
- Index/middle/ring/little digits are straight and parallel to the hand's long
  axis. Thumb chain points45° from that axis toward projected +Z in the palm
  plane (in this A-pose, toward outward ±X). Finger-root separation, lengths,
  palm size and thumb placement are measured in each rest profile.
- All ten digits have three articulated bones. **Thumb01 is the metacarpal,
  thumb02 proximal phalanx, thumb03 distal phalanx**; the other digits use proximal,
  middle and distal phalanges. This does not invent a third thumb phalanx.
  One composite toe bone per foot is V1; facial/individual-toe bones are not core.
- Bone local +Y points from head to tail. Local +Z is root-space +Y projected
  perpendicular to bone+Y and normalized; if the projection has length<1e-6,
  project root-space +Z instead. Local +X=Y×Z. This fully defines roll and avoids
  mirrored negative scales. `root` head(0,0,0), tail(0,0,0.1)m is a transform bone,
  not an anatomical segment. All other bone lengths are character-specific.

There is **no mandated1800mm person or masculine/feminine proportion ratio**.
Measured stature, joint positions, bone lengths and anatomical sources belong in
the character SPEC and canonical `rest-profile.json`. A synthetic1800mm JSON test
fixture is a software test only, not an approved anthropometric reference.

### Exact bone hierarchy

| Bone | Parent | Connected | Deforms |
| --- | --- | --- | --- |
| `root` | None | false | false |
| `pelvis` | `root` | false | true |
| `spine_01` | `pelvis` | true | true |
| `spine_02` | `spine_01` | true | true |
| `spine_03` | `spine_02` | true | true |
| `neck` | `spine_03` | true | true |
| `head` | `neck` | true | true |
| `clavicle_l` | `spine_03` | false | true |
| `upper_arm_l` | `clavicle_l` | true | true |
| `forearm_l` | `upper_arm_l` | true | true |
| `hand_l` | `forearm_l` | true | true |
| `thumb_01_l` | `hand_l` | false | true |
| `thumb_02_l` | `thumb_01_l` | true | true |
| `thumb_03_l` | `thumb_02_l` | true | true |
| `index_01_l` | `hand_l` | false | true |
| `index_02_l` | `index_01_l` | true | true |
| `index_03_l` | `index_02_l` | true | true |
| `middle_01_l` | `hand_l` | false | true |
| `middle_02_l` | `middle_01_l` | true | true |
| `middle_03_l` | `middle_02_l` | true | true |
| `ring_01_l` | `hand_l` | false | true |
| `ring_02_l` | `ring_01_l` | true | true |
| `ring_03_l` | `ring_02_l` | true | true |
| `little_01_l` | `hand_l` | false | true |
| `little_02_l` | `little_01_l` | true | true |
| `little_03_l` | `little_02_l` | true | true |
| `thigh_l` | `pelvis` | false | true |
| `shin_l` | `thigh_l` | true | true |
| `foot_l` | `shin_l` | true | true |
| `toe_l` | `foot_l` | true | true |
| `clavicle_r` | `spine_03` | false | true |
| `upper_arm_r` | `clavicle_r` | true | true |
| `forearm_r` | `upper_arm_r` | true | true |
| `hand_r` | `forearm_r` | true | true |
| `thumb_01_r` | `hand_r` | false | true |
| `thumb_02_r` | `thumb_01_r` | true | true |
| `thumb_03_r` | `thumb_02_r` | true | true |
| `index_01_r` | `hand_r` | false | true |
| `index_02_r` | `index_01_r` | true | true |
| `index_03_r` | `index_02_r` | true | true |
| `middle_01_r` | `hand_r` | false | true |
| `middle_02_r` | `middle_01_r` | true | true |
| `middle_03_r` | `middle_02_r` | true | true |
| `ring_01_r` | `hand_r` | false | true |
| `ring_02_r` | `ring_01_r` | true | true |
| `ring_03_r` | `ring_02_r` | true | true |
| `little_01_r` | `hand_r` | false | true |
| `little_02_r` | `little_01_r` | true | true |
| `little_03_r` | `little_02_r` | true | true |
| `thigh_r` | `pelvis` | false | true |
| `shin_r` | `thigh_r` | true | true |
| `foot_r` | `shin_r` | true | true |
| `toe_r` | `foot_r` | true | true |

All core bones except `root` deform. Connected chains share parent tail/child
head; clavicles, thighs, pelvis and first digit bones are unconnected branches.
No extra bone is allowed in the V1 animation/export skeleton. Private controls,
helpers or corrective systems cannot replace/rename core bones. A private
deformation rig must publish a documented bake/deformation adapter; additional
weighted bones require an explicitly versioned extension and consumer review.
V1's implemented skinning validator checks canonical-core skinning only.

### Animation skeleton versus animator rig

The skeleton is the stable solved-output interface. Character-specific control
shapes, control names, mechanisms, twist helpers and IK solvers are private to a
rig source under `assets/humans/rigs/`. Geometry sources remain under
`assets/humans/models/`. Do not duplicate skin meshes to distribute a rig.
Character composition publishes the canonical armature wrapper and binds linked
geometry/rig dependencies by recorded versions and rest-profile fingerprints.
An override hierarchy or scripted assembly must be proven before it becomes a
supported implementation (H01); this document does not claim a working adapter.

Required logical facade controls, mapped to actual object/bone references in
`human-contract.json`:

- `root_motion`, `pelvis`;
- `ik_hand_l/r`, `pole_elbow_l/r`, `ik_foot_l/r`, `pole_knee_l/r`;
- `ik_fk_arm_l/r`, `ik_fk_leg_l/r`: root float properties0..1,0=FK/1=IK,
  explicitly mapped with `{object: <asset_id>__root, bone: null, property: <key>}`;
- `fk_<bone_name>` for every52 deform bones, including all finger phalanges.

Actions/poses intended for exchange target canonical solved bones, not private
control names. Quaternion rotation channels are the exchange convention; root
translation/rotation carry locomotion, pelvis stays anatomical. Nonroot animated
translation/scale and squash/stretch need a separate declared extension; they
are not portable V1 behavior. FK controls and IK targets accept full frames,
including wrist/foot orientation. IK/FK mode switching must preserve the solved
pose (no pop); private blend/snap APIs must be documented and tested.
Configured IK may have zero influence in the saved FK rest mode; the inspector
checks the configured graph while actual switching/snap behavior needs motion
evidence. The saved solved skeleton must equal its rest matrices, not merely
have zero animator channels while constraints secretly pose it.

### IK, constraints and contact requirements

Hand IK solves upper_arm→forearm, tip at wrist, chain length2; foot IK solves
thigh→shin, tip at ankle, chain length2. Independently control hand/foot orientation
and finger curl. Do not include fingers or toes in a two-bone limb solver.
Root/torso are not accidentally pulled by limb IK. Stretch is off. Every limb
has an explicit pole target; reference elbow plane is toward−Y and knee plane
toward+Y, with nonzero pole distances recorded relative to limb lengths. Solvers
must handle the straight A-pose deterministically without flipping or changing
the bind skeleton. Pole angles and rotation-offset adapters are implementation
details requiring reproducible metadata and motion tests.

Elbow flexion is primarily localX; forearm localY may carry pronation/supination
through a declared adapter, with lateral elbow deviation constrained. Knees use
localX flexion with other axes locked. Shoulders/hips have multi-axis orientation;
wrists/ankles and fingers have individually documented ranges. Do not apply a
single hinge to an anatomical ball joint. **V1 does not prescribe medical or
universal numerical ROM limits.** H02 requires a sourced, approved rig limit
profile, min/max radians and sign conventions per joint, active local constraints,
no unwanted scaling, IK/FK contact and singularity tests. Limits are illustration
guardrails, not diagnosis or physical safety certification.

The static inspector verifies declared two-bone IK/pole targets, stretch-off and
local limit constraints at their recorded owners. It cannot establish solver
quality, orientation-follow behavior or correct anatomical motion from one frame;
those are explicit manual/animated release gates.

## Equipment/support attachment interface

Publish11 Empty anchors named `<asset_id>__anchor_<key>`. Each frame is measured
root-local in the A-pose and declares its owner bone, position and WXYZ unit
quaternion. Bone parenting/constraints must follow the actual solved skeleton.
Do not attach scenes to skin vertices, private control shapes or bone indices.

| Keys | Owner | Position / canonical rest frame |
| --- | --- | --- |
| `floor_contact` | installation root | Origin; +Y front,+Z up |
| `pelvis` | pelvis | Pelvis bone head; +Y front,+Z up |
| `hand_grip_l/r` | hand_l/r | Virtual grip-cylinder center within the palm/finger grasp envelope; +Y along palm transverse/radial axis,+Z outward palm normal |
| `foot_contact_l/r` | foot_l/r | Sole support center; +Y forward,+Z up |
| `heel_contact_l/r` | foot_l/r | Heel sole patch; +Y forward,+Z up |
| `toe_contact_l/r` | toe_l/r | Forefoot/toe support patch; +Y forward,+Z up |
| `back_support` | spine_02 | Posterior torso support patch; +Y toward head,+Z outward posterior |

Hand rest frame+Y=(±√½,0,√½),+Z=(0,1,0), with+X=Y×Z. All four foot/heel/toe
contact categories lie on floorZ0 in the A-pose. Back frame+Y=(0,0,1),
+Z=(0,−1,0). Anchors must be measured against actual skin/contact geometry;
matching copied metadata is insufficient. Hand centers/skin offsets depend on
hand size and the tested grip. The face of a material is not a contact datum.

Scenes align these full frames to existing equipment grip/support frames and own
their pose/configuration offsets. Preserve the approved bar's +X shaft and
bench's existing support axes; do not rotate or rename equipment anchors to fit
a human. Record grip diameter, span, palm/finger contact and clearance for each
consumer. A different wrist width, limb length or torso depth requires re-solving
contacts and collision checks. No existing equipment-to-human consumer is tested
because no human has been authorized/built yet.

## Standard muscle catalog and highlight API

[muscles.json](muscles.json), with a [readable catalog](muscle-catalog.md), defines **78 stable regions:39 bilateral pairs**.
Every entry has immutable ID, pair ID, subject-relative side, anatomical name,
functional display group and representation kind. `muscle_deltoid_anterior_l`
is a region of Deltoid, not an invented separate muscle. Erector spinae and
iliopsoas are explicitly aggregates. Anatomical names are distinguished from
original display-group classifications. This is a fitness illustration catalog,
not an exhaustive atlas or exercise-activation database.

All mannequin/masculine/feminine/custom characters expose every core ID even
when using simplified surface topology. One weighted semantic vertex-group mask
per ID maps onto a body mesh; a mask is not required to be separate muscle
geometry. Keep masks independent and nonempty; values0..1, with overlaps only
when anatomically intentional and documented. Another body can remap masks to
different topology while keeping identical IDs. Aggregates must not be confused
with a future detailed subdivision or activated twice accidentally.

Publish root custom float properties for each region:

- `highlight_primary__<muscle_id>` in0..1;
- `highlight_secondary__<muscle_id>` in0..1.

Each channel is individually addressable; zero means off. Primary takes precedence
over secondary for the same region in display composition, rather than mixing
two colors unpredictably. Exercise metadata uses the versioned activation schema,
separate `primary` and `secondary` ID→weight maps; an ID cannot appear in both.
Omitted IDs are off; laterality is never inferred from the camera. Activation
weights are illustration controls, **not measured EMG, injury advice or a
physiological percentage**. Which muscles are primary/secondary depends on the
exercise variant and must be curated/reviewed; no exercises are assigned here.

Highlighting must remain visible **through every supported clothing variant**.
Skin shaders alone do not satisfy this. Declare an overlay or projected-mask
adapter, driven from the same IDs/properties and deforming with the body. Do not
erase garment structure or expose skin simply to bypass occlusion. Preserve
silhouette/outline readability, no shadows/AO, independently addressable regions,
and primary/secondary distinction. Exact palette, opacity, projection, deep-layer
presentation and renderer are H03/H04 approval decisions. Render proof includes
unclothed/clothed front/back/side, overlapping regions and both roles; automated
mask existence cannot prove that a clothing shader displays the correct anatomy.

Additive future anatomy needs new stable IDs, named parent/region relationships,
catalog version and an explicit capability negotiation. Never recycle an ID or
silently change an aggregate's coverage. Keep the V1 core available in adapters;
splitting/renaming/removing core IDs or changing meanings requires a new major
contract and migration. Extensions are namespaced under metadata `extensions`,
not inserted as unknown core bones/IDs. Current tooling intentionally fails
closed on unknown catalog/contract versions until their rules are implemented.

### Anatomy references and review limits

Names and regional context were checked against OpenStax Anatomy & Physiology2e:
[upper limb](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs),
[trunk](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax),
[lower limb](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
Only names/reference links are retained; no diagrams, models or textures imported.
Catalog partition/display grouping is original project design, not a medical
standard. A qualified anatomy/art review of actual region boundaries is H03.

## Interchangeability and honest guarantees

| Compatibility level | Guarantee after validation | What is not guaranteed |
| --- | --- | --- |
| Interface compatible | Same53 bone semantics/parents,78 muscle IDs, facade and11 anchors, meter/axis/origin rules | Correct anatomy, deformation or visual quality solely from names |
| Direct-pose compatible | Same rest-profile fingerprint, skeleton version and action-channel policy allow canonical bone transforms to be reused | Intersections caused by different skin/clothing thickness |
| Retarget compatible | A declared tested adapter solves different bone lengths/rest locations using shared semantics and equipment contacts | Applying the same action unchanged preserves hand/foot placement |
| Export compatible | Approved pinned output profile, baked canonical skeleton, retained muscle-state mapping and consumer roundtrip proof | Shader/IK/driver portability, identical raster output across renderers |

Morphology labels never select a different skeleton or muscle namespace. Surface
variants may share a rest profile. Different proportions have distinct measured
profiles; do not falsely mark them direct-pose compatible or scale the source
armature to fake compatibility. A profile fingerprint hashes exact names,
parents, rest heads/tails, connected/deform flags and roll axes in meters.
Store `rest-profile.json` as UTF-8 canonical compact sorted-key JSON with no
trailing newline, bone entries sorted by name and only those fields; its byte
SHA256 equals the computed fingerprint. Cosmetic JSON formatting is not a profile
revision. Remeasure/rebind deliberate rest changes; do not overwrite a bound pose.

Retargeting must solve root/pelvis placement, reach, shoulder spacing, hand size,
finger grip, foot planting and torso support. Short limbs may not reach a target;
large bodies may intersect otherwise valid equipment. IK can slide feet, flip
poles, lose wrist orientation, distort joints or cause finger penetration.
Twist distribution and skin deformation do not follow automatically from a
matching hierarchy. A pose retarget adapter must declare source/target profiles,
scale strategy, root motion, contact priorities, solver/version, unreachable
target behavior and measured errors. No automatic retargeting is certified by
this foundation; final contact/motion review is mandatory after replacement.

## Illustration and animation output contract

Use the existing style/metadata/reference-render system. Human material roles
retain `skin_base`, `muscle_primary`, `muscle_secondary`, `bone`, `outline`;
implementation/palette approval remains H04. Clothing uses named semantic slots
and the same region-ID adapter. Assets must declare a supported illustration
and animation profile via [export schema](../../../schemas/human-export-v1.schema.json).
Profiles record actual Blender/exporter versions, format, source axes/units,
proper rigid target-axis conversion, frame range/rate, root-motion mode,
canonical bone names, control exclusion and muscle-state delivery.

Animation exports bake solved transforms into the canonical skeleton, exclude
private controls and constraints, and retain muscle states embedded or in a
versioned sidecar. Record sampling and rotation continuity; bake at the approved
frame rate and recheck the target application. If in-place motion is selected,
retain root trajectory in a sidecar. Original rig remains editable; bake into a
disposable export copy, not the source. No automatic pipeline or default format,
FPS, resolution, Blender baseline or glTF shader support is selected here (H05).

The [Blender bone-roll manual](https://docs.blender.org/manual/en/5.1/animation/armatures/bones/editing/bone_roll.html)
supports treating roll as an explicit local-axis contract. Blender-specific rig
constraints are runtime mechanisms, not promises of animation interchange.

## Automated validation and required manual evidence

Tools and schemas are reusable with Python3.9+ and require no new Python package:

```sh
python3 scripts/pipeline/validate_human_contract.py
python3 -m unittest discover -s tests -p 'test_human_contract.py' -v
```

The first command validates authoritative registry structure/laterality, not an
unbuilt character. The schema engine implements the explicitly used subset of
Draft2020-12 keywords; it is **not a general JSON Schema implementation**. Unsupported
validation keywords fail closed. Schemas are also usable by standard2020-12
validators in a caller's environment. No dependency is installed silently.

Use `--activation exercise-muscles.json` to validate an exercise's future muscle
assignment, or `--export-profile profile.json` to check a proposed output profile
without treating it as approved. No exercise/animation is created by validation.

Future authorized character validation:

```sh
Blender --background path/to/character.blend --python scripts/blender/inspect_human_contract.py -- --manifest path/to/human-contract.json --output path/to/observed.json
python3 scripts/pipeline/validate_human_contract.py --manifest path/to/human-contract.json --snapshot path/to/observed.json --output path/to/validation.json
```

Use `--rest-profile-output` on the inspector to record measured canonical JSON;
populate the metadata digest and rerun before claiming compatibility. Use
`--release` for production gates. The read-only inspector checks source identity,
bone structure/frames/rest pose, root and collection pivot, body floor/height,
normalized transforms/hierarchy, canonical skin weights, resolved facade controls,
IK/limit constraints, actual anchor frames and muscle masks/properties. It never
builds/resaves a character or creates actions. An offline supplied snapshot is
not independently measured truth; production must retain its inspector/source
revision and verify the source digest.

For two actual observed characters, add `--compare-manifest other/human-contract.json
--compare-snapshot other/observed.json` to the offline command. It reports
`direct_pose_candidate`, `retarget_required` or `incompatible`, plus anchor frame
differences/contact-recalibration requirements. Candidate classification is not
proof of animation/deformation correctness. Both characters must independently
pass structure checks; different rest fingerprints always require retargeting.

Release also requires resolved H01–H05 decisions and **pinned PASS evidence** for
anatomy review, through-clothing highlighting, IK/FK contacts, retarget contacts,
linked replacement, reference views and illustration/animation export. Evidence
presence and SHA256 can be checked; the semantic quality of a render or physical
contact must be independently reviewed. Synthetic snapshots cannot satisfy
measured-source release evidence. Partial/placeholder templates fail compatibility
and release gates rather than advertising a completed human.

Current software tests inject missing fingers, wrong parents/roll/A-pose,
origins/scales, missing controls/IK, anchor owner/frame drift, missing/empty
muscle masks, coupled controls, clothing occlusion routes, malformed inputs,
rest-profile mismatch, and unsupported/unbaked export declarations. They are
pure JSON/math tests, **not a built or visually validated human rig**. The static
Blender inspector has no real-character integration test yet; that remains a
first-character release requirement.

## Open approval decisions and version control

| ID | Still requires approval | Consequence |
| --- | --- | --- |
| H01 | First measured body/rest-profile(s), adult/age scope, supported Blender baseline, actual source/rig linking and override/adapter implementation | No selected physique, production rig or direct-pose compatibility class yet |
| H02 | Sourced numeric joint-limit profiles, IK/FK implementation, singularity/twist behavior and contact tolerances over motion | No medically universal ROM, solver or animation-quality guarantee |
| H03 | Actual anatomy boundaries/simplification, aggregate/deep-region treatment, through-clothing anatomical presentation and exercise-role review | Catalog semantics established; illustrated/anatomical correctness unproven |
| H04 | Skin/clothing/primary/secondary palette, opacity, outline/shader/highlight backend and reviewed human preset | Existing no-shadow/AO direction preserved; numeric human visual preset unselected |
| H05 | Required animation/illustration formats, target software, FPS/resolution/alpha, baking and roundtrip profiles; artwork release terms where applicable | Export API defined; no format implementation, remote release or external artwork grant approved |

These are extensions of existing A01/A02/A04/A05/A07/A08, not silent approvals or
equipment changes. Record exact user approval and evidence in the existing
decision register and each relevant asset SPEC before implementation/release.
Individual assets use the [human templates](../../../templates/human/README.md)
alongside the existing manifest/spec/checklist. Stable interfaces are V1; breaking
bone, rest-axis, core ID, anchor or channel changes require a new major version,
retained predecessors, affected-consumer audit and approved migration. Additive
capabilities require explicit declared versions and consumer negotiation.
