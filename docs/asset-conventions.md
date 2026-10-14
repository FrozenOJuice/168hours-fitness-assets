# Shared asset conventions

Level 2 common technical contracts, extended by [category standards](category-standards.md). Technical defaults below remain proposals under A03; documentation and workflow requirements are mandatory under [the workflow](asset-workflow.md). These interfaces describe the intended library contract; approval decisions are tracked separately in [Decisions](decisions.md). No implementation or compatibility guarantee exists yet.

## Identity and layout

Use lowercase ASCII `snake_case` for directories, filenames, asset IDs, collection names, and object names. Avoid spaces and Blender-generated numeric suffixes in published names.

Stable ID pattern: `168h_<category>_<descriptive_name>`. Examples: `168h_equipment_flat_bench`, `168h_human_anatomical_adult`, `168h_rig_humanoid`, `168h_material_outline`. Categories are `human`, `rig`, `equipment`, `material`, `style`, `exercise`, and `template`. Add variants only when meaningful, such as `_adjustable` or `_neutral`; do not encode version numbers in stable IDs.

Each future asset folder contains its source `<asset_id>.blend` (or documented non-geometric source), `SPEC.md`, `asset.json`, and `validation.md`. Define the specification before building; keep it synchronized with the finished asset. Use `textures/` only when external textures are necessary; retain selected reference renders and their settings under `previews/` as required by the global guide. For example:

```text
assets/equipment/benches/168h_equipment_flat_bench/
  168h_equipment_flat_bench.blend
  asset.json
  SPEC.md
  validation.md
  textures/               # Optional
  previews/               # Required reference evidence for finished assets
```

Use semantic asset versions (`1.0.0`) in metadata. Breaking changes to anchors, axes, dimensions, bone naming, material slots, or control behavior require a major version and dependent-scene review. A stable ID identifies a family; each scene must record the asset version or Git revision it was verified against. Blender links follow paths, so versions are not automatically pinned: reproduce a release from its Git revision, and test upgrades deliberately.

## Units, coordinates, and transforms

Use Metric units, unit scale `1.0`, and meters internally: one Blender unit equals one meter. Store metadata dimensions as `[x, y, z]` in meters in the canonical rest configuration. Record measurement sources and tolerances; do not infer real-world dimensions solely from photographs. Equipment must use measured or manufacturer-specified dimensions before release.

Use a right-handed coordinate system: +Z up, +Y forward, +X toward the subject's anatomical left when the subject faces +Y. Left/right names always refer to the subject, never the camera. Default cameras look toward the subject's front; export axis conversion belongs in an export preset, not in asset geometry.

Place the equipment root at the center of its ground footprint, at floor Z=0. Human roots sit at the floor projection of the pelvis in the rest pose; a separate pelvis anchor marks actual pelvis height. Document any exception. Canonical assets have root translation/rotation zero and scale one. Normalize mesh transforms before rigging; do not blindly apply transforms to finished rigs. Placement happens through the scene's asset instance root.

## Replaceable collection interface

Publish one top-level collection named `<asset_id>`. Inside it use `<asset_id>__geo`, `__rig`, and `__anchors` subcollections as applicable. Expose a root Empty `<asset_id>__root`; all asset objects must descend from it, directly or through the rig. Material-only and style libraries publish named datablocks and declare those in metadata instead of claiming a geometry root.

Use `<asset_id>__<role>_<part>` for objects, such as `168h_equipment_flat_bench__mesh_pad`. Put instance-specific names in scenes, for example `bench_primary`; do not rename linked source datablocks to distinguish instances.

Anchors are Empty objects with stable logical names recorded in metadata, for example `168h_equipment_flat_bench__anchor_seat_center`. Each anchor defines a full local frame (+Y forward, +Z up), not just a point. Typical interfaces:

| Asset type | Suggested anchors |
| --- | --- |
| Human | `pelvis`, `hand_grip_l`, `hand_grip_r`, `foot_contact_l`, `foot_contact_r` |
| Barbell / dumbbell | `grip_l`, `grip_r` or `grip_center`, `load_l`, `load_r` where applicable |
| Bench | `seat_center`, `back_support`, `floor_contact` |
| Rack / machine | `floor_contact`, `handle_l`, `handle_r`, `seat_center`, `load_point` where applicable |

Only advertise anchors that exist. Human grip/contact anchors follow their relevant bones. Metadata declares an interface ID and version, such as `bench_support@1`, and the required logical anchors. A replacement must match the scene's required interface and supported ranges; shape similarity alone is insufficient. Equipment anchor frames describe the contact surface; the exercise stores any hand/body orientation offset needed for a particular pose.

Scenes constrain handles or placement controllers to anchors, not mesh vertices, polygon indices, or arbitrary internal objects. Record expected support height, grip width, load clearance, and adjustable ranges when an exercise needs them. A bench height change can still require a pose adjustment: the interface reduces rebuild work, but does not guarantee collision-free swaps. Review contacts and motion after every replacement.

## Human and rig separation

Keep human geometry and rig source assets separate. Publish compatible skinning, bone, rest-pose, and control-interface versions in metadata. Until a skeleton is approved, do not claim that arbitrary human meshes and rigs are interchangeable. Distinguish body proportion changes from surface/anatomy variants.

Exercise scenes own pose/action data and rig overrides. Equipment owns its adjustment mechanisms and limits; scenes own the selected configuration. Use named controls and declared rig interfaces, never raw mesh edits, to describe exercise motion. Rig implementation, neutral pose, and bone naming remain pending approval.

## Linking, dependencies, and materials

Proposed default: link asset collections from their sources; use library overrides only when local posing or adjustment is needed. Avoid appending duplicate production geometry into every exercise. Prove the override and action workflow in a small integration scene once modeling is authorized.

Use relative Blender paths (`//...`), no machine-specific absolute paths. Record direct dependencies by asset ID, version, and repository-relative source path. Shared dependencies must form an acyclic graph: materials/styles → assets → exercise scenes; templates may reference materials/styles but must not depend on exercise scenes. Avoid hidden dependencies and external add-ons unless approved and documented.

Keep material slot order stable within an interface version and use semantic slots: `skin_base`, `muscle_primary`, `muscle_secondary`, `bone`, `equipment_frame`, `equipment_padding`, `equipment_grip`, `outline`. Use only applicable slots and document mappings. The renderer-specific implementation of these slots remains open.

## Metadata and release

Use [the manifest example](../templates/asset-manifest.example.json) as a starting point; it is not a schema or automatic validator. Required release information: `SPEC.md` and validation paths, standards revision, reference-render index and render-settings path, decision/exception references, tested compatibility cases, stable ID, asset/version/interface versions, source path, Blender version, units/axes, bounds, root and published datablocks, anchors or controls, material mappings, dependencies, provenance/license, and review status. Scene metadata also records asset versions/configurations and camera/style presets. Use `null` for unknown facts during drafting; unknown dimensions, licenses, or compatibility cannot be marked ready. Artwork needs separate explicit terms under the [licensing policy](licensing.md); it does not inherit the MIT code license.

Review status progresses from `draft` to `review` to `ready`. Verify dimensions, relative links, contacts, outlines, and export settings using the [checklist](review-checklist.md). Never use the illustrative manifest's dimensions as a specification for a real asset.

## Shared change control

Never silently change these contracts to accommodate an asset. Submit shared changes and conflicting asset exceptions through [Decisions](decisions.md); record explicit approval and compatibility/migration evidence. Prefer reusable components over duplicated geometry. Keep stable names and paths for existing consumers, and record major versions for approved breaks. The asset specification must explain design rationale, dependency versions, and reproduction steps sufficiently for a new developer/session to continue the work.

## Evidence metadata format

In `asset.json`, use repository-relative paths for source, specification, validation record, standards, render settings, and reference evidence. Each `reference_renders` entry records `view`, `configuration`, `frame` (or null for a still), `path`, `source_revision_or_digest`, and `preset_revision`. Each `exceptions` or `design_decisions` entry identifies the decision ID and approval reference; an empty list means none, not implicit approval. Compatibility test entries identify consumer/fixture IDs and versions, configuration ranges, result, and the corresponding validation evidence. Pin direct dependencies by ID, version, and relative source path. Fields may be null or empty in drafts; completed assets must contain the applicable evidence, and `N/A` needs a reason in the specification/validation record.

For designated visual references, also record the independent approval/release states and checksum-pinned source/images described in [the workflow](asset-workflow.md#visual-reference-approval-is-separate-from-production-readiness). A rendered appearance can be approved while physical/global technical defaults remain provisional. This does not change the `draft`/`review`/`ready` production lifecycle.
