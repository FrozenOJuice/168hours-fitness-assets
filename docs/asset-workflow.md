# Mandatory asset creation and update workflow

Applies to models, rigs, equipment, materials, styles, exercises, and scene templates. This is a documentation and review system; asset-specific plate validation/render scripts exist, while a general automated library pipeline is not established. Read [AGENTS.md](../AGENTS.md) for session instructions.

## Documentation hierarchy

| Level | Authoritative location | Responsibility |
| --- | --- | --- |
| 1 — Global style | [Visual style](visual-style.md) | Shared appearance and reference-render protocol; distinguish approved direction from open choices |
| 2 — Category standards | [Shared conventions](asset-conventions.md) plus [category requirements](category-standards.md) | Common technical contracts and category-specific dimensions, geometry, origins, attachments, and compatibility |
| 3 — Individual specification | `<asset_directory>/SPEC.md` and `asset.json` | The actual asset's design, measured facts, implementation, dependencies, exceptions, and evidence |

Global and category requirements take precedence over an individual specification unless an explicit approved exception applies. `SPEC.md` contains rationale and reproduction instructions; `asset.json` contains structured facts and evidence paths. Both must agree. If a contradiction exists, flag and resolve it before implementation. Reference the standards at a Git revision rather than copying their prose into each spec.

## 1. Review standards and reuse opportunities

Read all three levels where they exist, the [decision register](decisions.md), and the [licensing policy](licensing.md). Inspect comparable assets and downstream scenes. List reusable components, required interfaces, applicable decision IDs, and unresolved choices in the specification. No standard may be silently altered to fit an asset.

Gate: applicable production choices are approved, or the user has explicitly authorized a bounded prototype with recorded provisional assumptions. A prototype cannot be marked `ready` while required standards remain unresolved.

## 2. Specify before building

Create `SPEC.md` from [the reusable template](../templates/asset-specification.md), `asset.json` from [the manifest example](../templates/asset-manifest.example.json), and `validation.md` from [the checklist](review-checklist.md) inside the asset directory. When copying Markdown templates/checklists, resolve their policy links relative to the new file location; keep evidence paths local to the asset. These files are required for every future asset, including non-geometric assets. Fill the relevant category fields and explain `N/A` values. References need source/provenance, intended use, and measurement method.

Record target dimensions/tolerances, geometry/component plan, materials/style references, anchor frames, supported configurations, dependencies, consumer compatibility, planned reference views, reproduction steps, and proposed exceptions. Keep unknowns explicit. Route changes to shared standards through [the change process](decisions.md); do not treat an asset spec as approval.

Gate: implementation targets are sufficiently defined to build and validate, with approval evidence for deviations or blockers. Drafts may contain unknowns; implementation must not invent answers to approval-dependent choices.

## 3. Build with the specified conventions

Use reusable linked components/materials and published interfaces. Keep instance placement and exercise pose out of reusable geometry sources. Record exact Blender/add-on versions, source revisions, control settings, procedural inputs, and non-obvious manual steps. If implementation requires a design change, update the spec and resolve approval implications before continuing the affected work.

Gate: source, metadata, and specification describe the same design; dependencies are relative, versioned, and permitted for the intended use.

## 4. Generate standardized reference renders

Follow [the global reference-render protocol](visual-style.md). Retain the selected review set under `<asset_directory>/previews/` with a render-settings record and links from the spec/manifest. Place trial renders and delivery batches in ignored `exports/`. Do not claim reference renders exist before generating and inspecting them.

Gate: review views and relevant configurations are complete and reproducible from recorded source and preset revisions. Unresolved appearance choices block visual acceptance. The user may approve a pinned rendered appearance while its underlying production settings remain provisional; record these separate scopes as described below.

## 5. Validate the implementation

Complete `validation.md` with `PASS`, `FAIL`, `NOT RUN`, or justified `N/A` for each check, observed values, evidence, date, and reviewer. Run the generic category-driven origin audit under A14, recording expected/actual root/collection pivots and component/anchor frames. Check dimensions and naming, local frames and transforms, dependency resolution from a fresh checkout, supported controls/configurations, replacement behavior in named consumers, and visual output. Recheck moving contacts over the motion range, not just one frame.

Gate: no applicable `FAIL` or `NOT RUN`, no unresolved release decisions, and no undocumented exception. First assets must identify missing downstream tests; use an explicit fixture, and limit compatibility claims to demonstrated cases. Never fabricate a passing result to complete the checklist.

## 6. Reconcile documentation and release status

Replace target facts with verified implemented values while retaining design rationale and change history. Update metadata, dependencies, exceptions, reference index, and validation results. Record the reviewed source Git revision (or source-file digest for uncommitted review), render preset revision, approver, and decision references. Update shared docs only for explicitly approved shared changes.

Status transitions: `draft` → `review` when specification, implementation, and evidence are complete enough to inspect; `review` → `ready` only when all gates pass and asset acceptance by the recorded reviewer is recorded. Revise to `draft` or `review` after a change that invalidates evidence; record which tests must be repeated. A pure draft specification is not a finished asset.

## Replacement and standards changes

Preserve existing contracts. Proposed breaks require a major interface/asset version, list of affected consumers, explicit approval, migration steps, and regression evidence. Keep old usable versions available through Git/release revisions and document how consumers select the intended version. An asset exception has bounded scope and does not change the global/category defaults. Use [the standards-change template](../templates/standards-change.md) for either a shared change or an exception requiring approval.

## Visual-reference approval is separate from production readiness

When the user designates an asset as a reference, record `visual_reference.status=approved`, scope, version, approver/date, explicit approval evidence, source digest, and reference-image digests. Keep the existing `asset.json.status` (`draft`/`review`/`ready`) for production-release progression; add a labeled `production_release` state so the two axes are unambiguous. A visually approved reference can remain at `review` for production because engineering verification, artwork terms, or delivery standards are open. That does not make the visual approval pending.

A10's plate 0.1.4 is the first example. Its appearance is the current cast-iron plate reference; its exact source and images are pinned in its approval record. Documentation-only acceptance does not require resaving/rebuilding the model or rerendering existing evidence. Verify unchanged artifact checksums and documentation/metadata consistency instead. Record approval scope and provisional facts in the spec, and link the accepted category standard from the global guide and AGENTS.md.

For future authorized reference changes, preserve the accepted source/render snapshot in version control or release storage before replacing its master, invalidate affected evidence, and obtain explicit successor-reference approval. Retain historical approval records. Optional polish notes do not authorize a model edit.
