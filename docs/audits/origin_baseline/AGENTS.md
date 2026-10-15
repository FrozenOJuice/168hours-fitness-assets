# Instructions for 168Hours Fitness asset work

These requirements apply throughout this repository. Extend the existing system rather than creating competing guides. This repository contains standards, templates, and an approved first plate visual reference with separate production-release status; do not create or modify models unless the user's active task authorizes that work.

## Read before working

Read [README](README.md), the [global style guide](docs/visual-style.md), [shared conventions](docs/asset-conventions.md), the applicable [category standards](docs/category-standards.md), [decisions](docs/decisions.md), [workflow](docs/asset-workflow.md), and [licensing policy](docs/licensing.md). For an existing asset, also read its `SPEC.md`, `asset.json`, and `validation.md`, plus its dependency and consumer specifications.

## Mandatory asset workflow

1. Review existing standards, assets, components, and dependencies before proposing new geometry. Identify relevant approved standards and unresolved decisions.
2. Write or update the asset's `SPEC.md` from [the specification template](templates/asset-specification.md) and its `asset.json` from [the manifest example](templates/asset-manifest.example.json) before building. Record dimensions, geometry, materials, anchors, compatibility, design rationale, dependencies, exceptions, and reproducible settings. Resolve applicable approval blockers first; document any explicitly authorized prototype assumptions.
3. Build only within the user's authorized scope using established conventions. Reuse linked assets, shared materials, and components before duplicating geometry. Document why a unique component is needed.
4. Generate the reference views required by the global guide using an approved, recorded preset. Retain selected review evidence under the asset's `previews/`; put disposable outputs under ignored `exports/`.
5. Copy the [review checklist](docs/review-checklist.md) to the asset's `validation.md`; record actual results and evidence for dimensions, naming, dependency resolution, interfaces, replacement, rendering, and licensing. Do not claim checks were performed when they were not.
6. Update the specification, metadata, dependencies, decisions, exceptions, reference index, and validation record to describe the finished asset. Only mark `ready` after all applicable gates pass and approval evidence exists. Invalidate stale checks after changes.

Apply the same workflow to changes to existing assets. Detailed gates and status transitions are in [the workflow](docs/asset-workflow.md). Manual visual/documentation review is required. Asset-specific plate validators exist; do not assume there is a general library validator.

## Shared standards and compatibility

- Never silently change shared design standards or promote proposals to approved standards. Submit proposed changes in [the existing decision register](docs/decisions.md) using [the change template](templates/standards-change.md). Record approval from the user/project owner before applying a shared standard change; continue independent authorized work while approval is pending.
- Follow explicit user authorization already given in the session. Documentation edits that record existing requirements do not need a new approval. Unknown technical/art choices are not approved by inference.
- Do not use an individual exception to redefine a shared standard. Record scope, reason, affected consumers, approval, and mitigation; conflicting exceptions require approval before implementation.
- Preserve stable asset IDs, published collections, anchors, material slots, rig/control interfaces, and relative source paths. Document a major version and migration plan for approved breaking changes; never silently break consumers.
- Design replacements around declared interfaces, contact frames, configuration ranges, and tested consumers. Recheck grips, support, pose, and clearance after swaps.
- Record enough versions, measurements, references, commands/manual steps, settings, and decisions for another developer or Codex session to reproduce the asset. Keep specification and JSON facts consistent; stop and reconcile contradictions before building.
- Keep MIT code/documentation licensing separate from artwork terms. Unknown artwork provenance or license blocks release.
- Use existing Git LFS rules for 3D sources, ignore temporary files and generated exports, and do not place required review evidence only in ignored directories. No new renderer, skeleton, add-on, or software baseline may be selected silently.

## Approved visual references

Before creating a traditional cast-iron plate, read the [approved category reference](docs/category-standards.md#approved-cast-iron-plate-visual-reference) and the reference asset's `SPEC.md`, `asset.json`, and `reference-approval.json`. Current reference is `cast_iron_plate_visual@1`, plate geometry 0.1.4. Compare declared source/render SHA256 values before using the reference; a mismatch must be investigated, not silently adopted as a new baseline.

Inherit the approved appearance and typography/rotation review cases. Do not treat its provisional physical dimensions, software or export settings as approved universal standards; use the spec's approval matrix. Keep other weights' nominal labels accurate. Visual approval and production readiness are separate fields: this reference is visually approved even though its release lifecycle remains `review`.

Do not rerun a builder/refinement script, resave the `.blend`, regenerate acceptance renders or apply optional polish to the approved reference without a user-authorized asset change. Metadata/approval documentation may be updated within the requested scope while preserving artifact bytes. Future successor changes must preserve the accepted baseline/evidence and record explicit supersession approval.

## Delivery preference

For every asset creation or refinement delivery, provide the full absolute file paths to the asset `.blend`, any relevant assembly/test `.blend`, and the render ZIP. Create or refresh separate ZIPs for unassembled asset renders and assembled/test-scene renders under `exports/illustrations/`, and include clickable links plus full absolute paths to each. Include all current views in the appropriate bundle; do not mix assembled and unassembled views in one ZIP unless the user requests it. If only one group exists, provide that group only. Keep authoritative renders in their existing `previews/` locations. Do not make the user ask separately for paths or the render bundle.
