# Asset review checklist and validation record

**Current A14 result: asset1.0.0, 69 origin/transform/component/anchor checks PASS; current migration regression28 PASS.** Native/source/preset pins in current asset.json and docs/audits/origin-migration-record.json. Historical0.x rows below retain frozen geometry/visual approval evidence and are superseded for changed origin semantics by the A14 section.

Validation for `168h_equipment_olympic_plate_45lb_cast_iron` version `0.1.4`, 2026-10-14, reviewer Codex. Status **approved visual reference** under A10; separate production lifecycle review/not ready. Source SHA256 `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`. Exact versions, metadata, standards hashes, render inputs, and evidence are in SPEC.md, asset.json, standards-snapshot.json, previews/render-settings.json, and validation-results.json. A09 prototype authorization: user response “Approve the documented review prototype.” Overall plate visual direction is approved by the user; current 0.1.4 execution is visually accepted under A10; production readiness is not claimed. This record combines per-asset automated checks and manual visual/documentation review.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Asset ID/version/category: `168h_equipment_olympic_plate_45lb_cast_iron` / `0.1.4` / equipment/free_weights.
- Source digest: `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`; no external asset dependencies.
- Specification/metadata: [SPEC.md](SPEC.md), [asset.json](asset.json).
- Standards: [snapshot](standards-snapshot.json), base `c91545c`; preset `plate_review_flat@0.1.4` with refinement-script hash in render-settings.json.
- Tool: Blender 5.1.1, no add-ons; bundled NumPy for pixel comparison.
- Reviewer/date/status: Codex, 2026-10-14, review prototype. Overall direction approved; current execution approved as visual reference; artwork license/production release remain open.
- A09 prototype choices approved; A01/A03/A04/A05/A07/A08 production choices and A06 remote LFS capacity remain open.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Pre-build SPEC.md existed before builder execution; reconciled after geometry and evidence generation. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | A09 authorized the prototype; A10 approves the current visual reference, not production release. Applicable production standards A01/A03/A04/A05/A07/A08 remain open; exact current docs hashed in standards-snapshot.json. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | A10 explicitly authorizes this category visual reference and inheritance rules; global technical standards remain separate. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | NOT RUN | Implemented facts agree with asset.json; artwork license and production choices remain explicitly unknown, blocking ready. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | Repository had no prior geometry/materials to reuse. Three linked instances share one collection/ten meshes; the rib recipe reuses symmetry and all existing materials; linked_collection_reuse evidence. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](../../../../docs/licensing.md) | NOT RUN | Original geometry and manufacturer dimensional source documented; no third-party artistic content imported. Artwork terms not selected (A07). |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | validation-results.json: naming, collection_structure, source_scope. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | validation-results.json: canonical_bounds, two_inch_minimum_bore; diameter 449.999988 mm, envelope 33.020001 mm, bore 50.799978 mm within 0.001 mm numerical tolerance. |
| T03 | Axes, origin, root hierarchy, transforms, and rest/configuration state match the specified contract | PASS | floor_and_root, normalized_geometry_transforms; source floor Z=0, root/mesh transforms identity, +Y bore axis. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | PASS | body_manifold: 5888 vertices/5888 quads/zero nonmanifold edges; raised_labels verifies actual 3.8 mm solids/3.5 mm exposed relief. refined_cast_profile verifies 13 mm web/29 mm hub/10.01 mm rim relief; existing_body_refined verifies original body data and object identity preserved with 768 locally added side-band vertices; four_cast_ribs_per_face/nonuniform_side_profile/balanced_dual_unit_lettering and the new hub_originating_outward_rib_taper/near_white_raised_letter_faces/body_and_non_barbell_topology_preserved checks pass. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | anchors, bore_anchor_placement, rotated_anchor_placement; exact names/frames/coordinates match spec. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | Rigid plate; rig checks N/A. shader_roughness and documented material assignments retain all body slots and label slot 0; a reused dark side material is appended at label slot 1. No existing slot or interface was removed/reordered. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | NOT RUN | Fresh Blender process reopens source with no external dependencies/add-ons (no_external_assets). Full fresh committed Git checkout/LFS fetch not run; files are uncommitted. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | PASS | Scoped fixture cases only: linked_collection_reuse, stack_pitch_no_overlap, numerical_sleeve_clearance, bore_anchor_placement, rotated_anchor_placement. No real consumer/alternative-plate claim. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | N/A — no existing consumers | First asset. Future compatibility is not claimed; migration/version policy is documented in SPEC.md. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | Front, side, three-quarter, back and full-plate 180° proof PNGs present; body has no moving/adjustable configurations. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | SPEC.md/asset.json index five tracked-intended preview paths; render-settings.json records exact source and builder digest. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | previews/render-settings.json records actual versions, camera transforms/projection/scale, colors, shadows/AO flags, native outlines, resolution, Standard/None color management, 32-sample AA, frame 1. Seed N/A for deterministic Workbench. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | PASS | Codex inspected the four standard views and the 180° rotation proof at 1024 px: four readable raised ribs, left 45 LB/right 20.4 KG and curved STANDARD/BARBELL on both faces, visible cast details at oblique angles, stepped side waist, clear bore/rim/hub and silhouettes. Native outlines plus flat color regions; overall direction is user-approved; current 0.1.4 execution is now accepted as visual reference under A10. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | shadow_free_setup and visual inspection: no lights/ground, flat Workbench, shadows/cavity/AO/specular off, no baked textures. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | PASS | All five reference_reproduction checks pass in a fresh Blender process: decoded pixels exactly equal, max channel delta 0. PNG metadata may differ; builder/validator and settings are retained. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | N/A — no delivery export | Only requested review PNGs and native blend source produced; production delivery presets remain A08. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | SPEC.md, metadata, A09/category appendix, render index, and validation evidence reconciled after generation. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | Git LFS attributes and ignores verified; sources, scripts, and selected evidence are currently uncommitted/untracked. No claim of committed tracking. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | NOT RUN | Prototype technical review passes; release approvals, art license, real consumers remain open. Visual acceptance is complete; production status remains review. |

## Category-specific checks

| Case | Configuration / expected result | Observed result | Status / evidence |
| --- | --- | --- | --- |
| Bore vs numerical sleeve | 50.8 mm minimum opening vs 50.0 mm cylindrical envelope | ~0.4 mm radial clearance | PASS — numerical_sleeve_clearance; no barbell authored |
| Stack | Three +Y-aligned linked instances at 33.02 mm pitch | Adjacent measured envelope gaps 0 m within floating-point precision | PASS — stack_pitch_no_overlap |
| Target placement/rotation | Bore anchor maps to (1,2,0.9); +Y maps to +X | Alignment within 0.000001 m; positive determinant | PASS — rotated_anchor_placement |
| Reversed-face readability | Front and back references | Both show upright 45 LB / 20.4 KG / STANDARD and whole-word inverted BARBELL, plus four ribs; BARBELL is upright in the 180° proof | PASS — visual reference inspection |
| Real barbell/alternative plate substitution | Existing consumer and compatible replacement | None exist in scope | NOT RUN — no physical-fit or production substitution claim |

## Outcome and changes since review

Review prototype is complete; all 35 implemented machine-readable checks pass. Production release remains blocked by explicit open choices and missing downstream tests above. Overall direction approval is recorded; current execution is visually accepted under A10; no production license/readiness is claimed.

Source digest and builder/validator digests are recorded with evidence. Geometry, text, anchor, palette, camera, or source/dependency changes invalidate affected checks; rerun the builder/validator as applicable, update digests and reference records, and reconcile SPEC.md/asset.json. A10 records visual acceptance separately from these technical checks. Future production approval or successor-reference approval must identify its own scope and evidence.


## 0.1.4 review-feedback correction validation

The earlier BARBELL orientation/appearance check was insufficient and was rejected by user feedback. It is superseded by this correction and the literal full-plate 180° viewing proof. The updated user feedback was recorded before editing; affected checks were rerun. **35 PASS, zero FAIL** for implemented technical checks.

- Typography: clean BARBELL glyph geometry is generated on a normal upright upper arc with the original STANDARD tracking step (48/7 degrees), then the entire word is rotated 180° around the plate center. Both source word objects/datablocks are retained. Manual inspection of the whole rotated plate confirms normal curved BARBELL text, correct order and clean spacing. Fonts remain actual mesh geometry with 3.5 mm raised relief, near-white faces and dark sides.
- STANDARD: central N–D arc spacing increases by 2 mm; each half moves 1 mm around the same arc with tangent orientations preserved. Front/reverse views inspected for improved separation.
- Roots: all eight physical rib caps have maximum planar radius ~46.24 mm, below the 52 mm hub-face radius, and axial top magnitude 14.0 mm below the 14.5 mm hub face. The transition emerges through the shoulder toward the unchanged 75 mm row. Body/rib manifold and monotonic outward taper checks pass.
- Preservation: existing object/data identity retained; body vertex coordinates and non-BARBELL mesh topology are unchanged. BARBELL mesh geometry/connectivity may change and is not falsely claimed preserved. Four anchors, bore, dimensions, stack envelope, palette, renderer and normalized transforms pass.
- Rotation proof: camera position/orthographic scale match the front view with exactly 180° optical-axis roll; the whole plate is turned in the image, not only the label. The fifth image independently reproduces identical decoded pixels, as do all four standard views.

Manual image evidence is required for typography; technical check counts alone do not establish visual acceptance. Overall approved direction remains; the current corrections are accepted as the visual reference under A10. Global standards/artwork terms/actual barbell compatibility and committed-checkout tests remain open. During the 0.1.4 geometry correction, shared standards were unchanged by hash comparison; the subsequent A10 documentation approval establishes the category visual reference without changing geometry. Correction provenance, source/script hashes and reference paths are reconciled in correction-record.json, SPEC.md and asset.json.

## A10 visual-reference acceptance — documentation-only finalization

User, 2026-10-14: “Approve the current 45 lb Olympic plate as the first visual-direction reference asset for the 168Hours Fitness equipment library.” This accepts current source version 0.1.4 and its five existing images as `cast_iron_plate_visual@1`. Visual acceptance is **PASS/complete**; no model or render change was made. Source/image hashes are pinned in reference-approval.json.

The existing 35 technical PASS results remain valid and were not rerun or rewritten for a documentation-only approval. Approval-step checks verify artifact/script/test-report byte preservation, metadata/approval consistency, JSON and document links. Production gates D02/D04/D06/T07/R02/R03 remain open as labeled; R03's remaining uncertainty is release readiness, not current visual acceptance. The approved-versus-provisional matrix in SPEC.md is authoritative. Optional polish has no current action attached.


## A14 current-origin validation —2026-10-15

Origin profile olympic_plate approved; root/collection pivot [0.0, 0.0, 0.22499999403953552]m in authoring frame, root-local datum zero. Current expected/actual results in [origin audit](../../../../docs/audits/origin-audit-results.json). This section supersedes historical floor-root expectations for plate/barbell. Current geometry/materials and evaluated world frames checked against archived baseline; three linked fixture sources compensated. New functional-origin interface is1.0.0 for free weights; bench remains0.1.1. Frozen historical reports/approvals remain under docs/audits/origin_baseline. Four assembly PNGs refreshed only for micro anti-alias differences; see origin-render-refresh.json and current render regression. External consumers/rig overrides beyond recorded tests remain unverified. No redesign or new artwork grant.


A14 finalization2026-10-15: origin migration **approved and complete**. Current library audit297 PASS; world/geometry/material/render regression28 PASS; all three fixture stacking/clearance checks42 PASS;6 failure-injection and2 automatic placement cases PASS. No native geometry/source edit during finalization. Existing visual/release scope unchanged. Final evidence: docs/audits/origin-migration-record.json and origin-compatibility-validation.json; repository commit identifies this finalized snapshot.
