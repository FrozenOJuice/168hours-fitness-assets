# Shared asset conventions

Level 2 common technical contracts, extended by [category standards](category-standards.md). Origin/axis/transform/link rules under A14 are now approved by the2026-10-15 audit request and explicit migration approval; other technical defaults remain proposals under A03; documentation and workflow requirements are mandatory under [the workflow](asset-workflow.md). These interfaces describe the intended library contract; approval decisions are tracked separately in [Decisions](decisions.md). No implementation or compatibility guarantee exists yet.

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

Equipment roots use intentional functional datums under **A14 / equipment_origins@1**: Olympic plates at the exact mounting-bore center; barbells at the shaft-axis midpoint between overall ends; floor equipment (benches/racks/machines) at the horizontal center of the supported footprint at floor level. Do not use Origin to Geometry or a vertex-average centroid as a default. Asymmetric lettering, handles or detail must not move a functional origin. Datum methods and category axes are in [category standards](category-standards.md#approved-equipment-origin-contract-a14).

An asset root Empty defines the published installation frame. Mesh-object origins are component construction/pivot frames, not the asset insertion origin: retain intentional axle, sleeve, joint and shared-data frames; static parts may retain documented authoring origins. Never blindly center every component. All published geometry must descend from the root. The top collection's `instance_offset` must equal the root's position in the source authoring frame; otherwise linking a collection rotates about a different point from manipulating the root.

Prefer authoring the root at (0,0,0) for new assets. A declared authoring translation is allowed when preserving an existing floor-Z0 source: current plate root is(0,0,.225)m, barbell root(0,0,.0365)m; their collection offsets match. Their **functional root-local origin is(0,0,0)**, floor anchors lie below it. This explicit translation is an intentional datum, not an unapplied placement transform. Roots have zero rotation and unit positive scale. Rigid meshes require unit positive scale and zero rotation unless a declared proper rotation is necessary for shared symmetric geometry (current barbell opposite sleeve/cap use Zπ). Never use negative scale. Anchor/controller orientation is intentional and must match its declared full frame; do not apply transforms to finished rigs. Human root/skeleton rules are now defined by A15/Human V1; unselected implementation choices remain H01–H05.

Attachment metadata `position_m` is root-local. Name each Empty `<asset_id>__anchor_<logical_key>`; record units, position, full rotation, +Y/+Z directions in root space, owner/controller and interface version. Validate geometry-critical contacts independently against the bore, endpoints, floor or support surface, not only against copied metadata. No unnamed or hypothetical anchors are published.

Scene placement belongs on collection instances. Source-space point/anchor placement uses `M_instance @ Translation(-collection.instance_offset) @ M_anchor`; align a desired anchor frame T using `M_instance = T @ inverse(M_anchor) @ Translation(collection.instance_offset)`. The helper `asset_instance_frame` implements source-space compensation. Keep relative resolved links, original shared data and version pins. An origin/offset change is a breaking interface change even when world geometry is preserved: obtain approval, retain predecessor evidence, major-version the interface, compensate every consumer and validate world geometry/anchors and renders.

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

Keep human geometry and rig source assets separate. [Human Model Contract V1](contracts/human-v1/README.md), established under A15, now defines53 solved bones,45-degree A-pose, local roll, floor origin,78 muscle regions,11 anchors and a mapped FK/IK facade. Publish compatible skinning, bone, measured rest-profile and control-interface versions. This resolves human interface naming/rest conventions; it does not make arbitrary meshes/rigs interchangeable. Different body proportions need tested retarget/contact adapters; surface-only variants with identical rest profiles can share canonical transforms.

Exercise scenes own pose/action data and rig overrides. Equipment owns its adjustment mechanisms and limits; scenes own the selected configuration. Use named controls and declared rig interfaces, never raw mesh edits, to describe exercise motion. Human V1 defines bone names and neutral pose; actual rig/override implementation, body profiles, numeric limits, anatomy appearance and export presets remain H01–H05 approval items. Equipment standards are unchanged.

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


## Automated origin validation

Run Blender5.1.1 with `--background --factory-startup --python-exit-code 1 --python scripts/blender/validate_asset_origins.py`. Discover current equipment manifests, excluding archived `history/` folders. Reports contain expected/actual values and explicit failures. Each manifest declares `origin_contract.profile`, geometry selectors, authoring root/offset and allowed component rotations; rules live in [equipment-origin-rules.json](equipment-origin-rules.json). Add future profiles/rule strategies rather than asset-name conditionals; unknown profiles fail closed. Circle fitting currently supports circular Olympic bores; noncircular/asymmetric datums need a declared validated method. Root-local anchor matching, geometric datum checks, hierarchy, axes, scale/rotation and collection offsets are mandatory. Existing asset validators expose this audit via `-- --origins` (optional `--manifest <repository-relative asset.json>`). The0.x full suites retain archived historical checks; A14's current-source geometry/material/world-placement and render regression suite is `validate_origin_migration.py`. Never silently weaken a legacy assertion or overwrite frozen reports to accommodate a migration.

Existing plate/barbell/bench validator entry points now default to the current generic origin audit plus migration regression; `-- --origins` selects the origin audit alone. Original0.x detailed validators/code are retained in the archived baseline for historical geometry checks.
