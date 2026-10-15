# Asset specification: <asset_id>

Copy to the future asset folder as `SPEC.md`. Replace all placeholders; use `TBD` for draft unknowns and `N/A — reason` for inapplicable fields. This file is a template, not an existing asset or approval. Keep structured facts consistent with `asset.json`.

## Identity and status

- Asset ID / category / repository path:
- Asset version / status (`draft`, `review`, `ready`):
- Author / reviewer / dates:
- Intended use and supported consumers:
- Source `.blend` path or other authoritative preset/source:
- Reviewed source Git revision or file digest:
- Applicable global/common/category standards and their Git revisions:
- Applicable decision IDs, approval references, and unresolved blockers:

## Dimensions and geometry

| Measurement | Target (meters unless stated) | Implemented value | Tolerance | Source / method |
| --- | --- | --- | --- | --- |
| Bounds X / Y / Z in canonical configuration | TBD | TBD | TBD | TBD |
| Category-specific critical measurements | TBD | TBD | TBD | TBD |

- Canonical configuration, units, axes, origin, root, transforms:
- Geometry breakdown, anatomical or equipment simplifications and rationale:
- Topology/deformation requirements, modifiers, procedural parameters, detail limits:
- Reused component IDs/versions and why any unique geometry is needed:
- Supported variants and adjustment ranges; excluded configurations:
- Measurement/reference provenance and permission to retain reference files:

## Published interfaces and replacement

- Collection/root/datablock names:
- Interface IDs and versions; compatible rig/skeleton/rest pose if applicable:

| Logical anchor / control | Published object / bone | Local position (m) and orientation (explicit convention) | Limits / tolerance | Purpose |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

- Material slots / node inputs / order and supported values:
- Tested consumers/replacements and configuration ranges:
- Contact offsets, support/grip requirements, clearance expectations:
- Compatibility limitations, breaking changes, version/migration plan:

## Materials and visual design

- Global style/palette/preset IDs and revisions:
- Semantic material roles, shared datablocks, parameters, and texture sources:
- Outline treatment, anatomical emphasis, surface simplifications:
- Lighting/shadow-free setup and rationale for any asset-specific treatment:
- Camera/framing and background requirements:
- Design decisions: alternatives considered, chosen approach, reason, approval reference:

## Dependencies and licensing

| Dependency ID / version | Relative source path | Purpose / interface | Provenance / terms |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

- Creator/origin and separate artwork license terms/reference:
- Third-party notices and attribution required in outputs:
- External tools/add-ons and versions; no undocumented machine-local dependencies:

## Reproduction instructions

1. Check out the specified source/dependency revisions and fetch LFS files.
2. Record exact Blender version, add-ons, operating assumptions, and open source path.
3. List procedural inputs, commands/scripts or ordered manual build/update steps, including measurements, constraints, skinning, and configuration controls where relevant.
4. Identify render scene/preset revision and all overrides; record camera transforms/projection/framing, lighting, renderer, color management, resolution, alpha, outline width, samples, frame/configuration, and seed when relevant.
5. List validation steps/fixtures and export settings; explain how to reproduce each reference image from source.

## Reference render index

Store selected review evidence in `previews/`, with `previews/render-settings.json` recording the actual settings. Match the global protocol; retain extra configuration/interface views as needed. Do not substitute unrendered filenames for evidence.

| View / configuration / frame | Relative image path | Source revision or digest / preset revision | Review notes |
| --- | --- | --- | --- |
| Front | TBD | TBD | TBD |
| Side | TBD | TBD | TBD |
| Three-quarter | TBD | TBD | TBD |

Non-geometric assets: name the documented preview fixture and why each view is appropriate; approved alternate coverage must be recorded.

## Exceptions and unresolved issues

| Standard / decision | Exception or issue | Scope / reason / affected consumers | Approval evidence / mitigation |
| --- | --- | --- | --- |
| None, or TBD | TBD | TBD | TBD |

## Validation and acceptance

- Link `validation.md`, summarize actual results and outstanding checks:
- Approver / date / acceptance reference:
- Evidence invalidated by later changes; required reruns:

## Change history

| Date / version | What changed and why | Compatibility / evidence impact | Decision / approval |
| --- | --- | --- | --- |
| TBD | Initial specification | TBD | TBD |
