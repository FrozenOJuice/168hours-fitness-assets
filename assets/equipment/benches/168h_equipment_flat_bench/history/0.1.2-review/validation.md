# Asset review checklist: 168h_equipment_flat_bench

**Current A14 result: asset0.1.1, 144 origin/transform/component/anchor checks PASS; current migration regression28 PASS.** Native/source/preset pins in current asset.json and docs/audits/origin-migration-record.json. Historical0.x rows below retain frozen geometry/visual approval evidence and are superseded for changed origin semantics by the A14 section.

Version0.1.1, reviewer Codex, 2026-10-14; user design approval pending. [SPEC.md](SPEC.md), [asset.json](asset.json), [results](validation-results.json), [pre-build snapshot](standards-snapshot.json), [render reproduction](render-reproduction.json). Lifecycle review, production not_ready. Source SHA256 `6a1c111e801358dc62e44040ed6fce2ed2c40c6b3444928c9db603b17e5b63fb`.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Equipment/benches; 0.1.1 fixed flat review prototype, no asset approval inferred.
- Blender5.1.1, no add-ons; manufacturer context documented in SPEC.
- A13 scopes local prototype choices; A10/A12 frozen equipment references verified unchanged. Global A01–A08 unresolved as recorded.
- Base revision and exact standards/protected file hashes in standards-snapshot.json; pre-build spec/metadata/checklist digests in build-record.json.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Original pre-build hashes in build-record.json; refinement specified in SPEC/asset.json/refinement-plan.json before saved-source edit. Current facts reconciled after QA. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | Prototype authorized under A13; production/global defaults and design approval pending. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | No shared guide/category/AGENTS change; protected hashes pass; A13 is local proposal only. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | NOT RUN | Spec/JSON agree for prototype; physical assumptions, artwork terms and release approvals remain open explicitly. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | Unique bench geometry required; 30 objects use15 data blocks; feet/rails/boots reuse data. No existing asset geometry copied. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](../../../../docs/licensing.md) | NOT RUN | Original creator/context documented, no third-party artwork. MIT applies to code/docs only; separate artwork grant remains null. |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | collection_contract/naming_and_scope: correct ID/path/root and two component subcollections. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | overall_bounds/pad_dimensions/ground_footprint in validation-results.json; numerical tolerance1e-6m. |
| T03 | Axes, origin, root hierarchy, transforms, and rest/configuration state match the specified contract | PASS | floor_center/meter_units/root_hierarchy/rigid_normalized_transforms: canonical floor root, normalized rigid scale/rotation. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | PASS | All30 closed outward-oriented nondegenerate meshes; rounded pad, flat-cut sloped legs, fixed angle0°, intended support joins documented. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | Seven anchor frames verified; four support ray casts hit flat top with +Z normal. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | Rigid no-rig asset; semantic slot order stable and recorded per component in manifest. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | NOT RUN | Saved source opens; relocated source and linking test pass separately. Fresh committed Git/LFS checkout not run: new asset uncommitted. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | NOT RUN | Linked two-instance frame mapping passes. Alternate bench/human pose/rack consumers do not exist/tested; replacement suitability not certified. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | N/A | First bench; no existing bench consumers to regress. Protected existing plate/barbell/fixture artifacts unchanged. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | Retained front/side/three_quarter/top views, fixed flat configuration/frame1. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | All four retained image paths/digests and source/preset digest match manifest. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | render-settings.json captures engine/version/cameras/framing/AA/palette/outline/white background/Standard color. No stochastic seed or numerical line-width control in Workbench. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | PASS | Codex actual-size inspection: recognizable fixed utility bench, readable pad edge and frame/foot separation, no logos. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | Workbench FLAT, no lights/ground/cavity/specular/shadows; no AO or baked maps; manual four-angle inspection. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | PASS | Fresh-process render-reproduction.json: all four decoded images exactly match, source bytes unchanged. Build recipe/helper hashes pinned. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | N/A | Requested native source and review PNG bundle only; no production/interchange export contract selected. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | Spec, manifest, A13 decision, README index, source/render hashes and this record reconciled. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | LFS and ignores verified; required new sources/evidence are untracked/uncommitted, not claimed as committed. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | NOT RUN | User design approval, applicable release choices/artwork terms and downstream tests pending; remains review. |

## Category-specific checks

Add rows for the actual measurement and compatibility cases required by the applicable category. State fixture/consumer, input configuration, expected result/tolerance, observed result, and evidence. Do not mark hypothetical fixtures as tested.

| Case | Configuration / expected result | Observed result | Status / evidence |
| --- | --- | --- | --- |
| Flat pad contacts | center/seat/back/head anchors on Z457.2mm | Four +Z raycast normals, height error below1e-6m | PASS |
| Instance alignment | back_support to (1,2,.75), yaw90° | Full-frame error below1e-6, two instances share collection and linked data | PASS |
| Floor support | Four boots Z0; outer envelope355.6×1025mm; actual contact349.6×1019mm | Measured within1e-6m | PASS |
| Relocated source | Separate temp folder, no external dependencies | See relocation-check.json | PASS |
| Real consumers/replacement | Human/rack/alternate bench | No authored compatible consumers yet | NOT RUN |

## Outcome and changes since review

- Overall result: 72 automated prototype PASS checks, zero FAIL, four reference image pixel comparisons PASS. Shared standards and accepted assets preserved.
- Unperformed: release gate rows above; no actual human/rack/substitute bench test; fresh committed checkout not run.
- User design acceptance: pending. Codex technical/manual review only, 2026-10-14.
- In-place0.1.1 refinement; original main frame/substrate/source object names, original data identities and anchor frames verified against retained predecessor. No external asset dependency or approved-equipment change.
- Future geometry/palette/anchor changes invalidate affected checks and render digests; rerun saved-file QA/references before acceptance.

After material changes, revert status to `draft` or `review` and mark affected results `NOT RUN`; retain prior evidence history. Mark `ready` only when the [workflow gates](../../../../docs/asset-workflow.md) are satisfied.


0.1.1 refinement QA complete: 72 technical PASS / zero FAIL; all four references exactly reproduce. Source-preservation and declared material-slot checks added; new details remain review choices. User design approval remains pending. See refinement-plan.json/refinement-record.json and retained history/0.1.0.


Refinement-specific evidence: exact predecessor/current comparison verifies8 unchanged main-frame/substrate meshes,8 root/anchor frames, original pad polygon connectivity and21 original object/data names. In-process pointer identity was asserted during editing; matching current source hash is recorded. Actual piping remains within the nominal cushion envelope. All component slot orders agree with manifest. Extra meshes reuse shared data. `actual_rubber_floor_contact_bounds` distinguishes the flat-floor patch from the rounded rubber envelope. Hardware/shoe/cushion geometry is illustrative; strength, real hardware fit and human/rack compatibility remain untested.


## A14 current-origin validation —2026-10-15

Origin profile flat_bench approved; root/collection pivot [0, 0, 0]m in authoring frame, root-local datum zero. Current expected/actual results in [origin audit](../../../../docs/audits/origin-audit-results.json). This section supersedes historical floor-root expectations for plate/barbell. Current geometry/materials and evaluated world frames checked against archived baseline; three linked fixture sources compensated. New functional-origin interface is1.0.0 for free weights; bench remains0.1.1. Frozen historical reports/approvals remain under docs/audits/origin_baseline. Four assembly PNGs refreshed only for micro anti-alias differences; see origin-render-refresh.json and current render regression. External consumers/rig overrides beyond recorded tests remain unverified. No redesign or new artwork grant.


A14 finalization2026-10-15: origin migration **approved and complete**. Current library audit297 PASS; world/geometry/material/render regression28 PASS; all three fixture stacking/clearance checks42 PASS;6 failure-injection and2 automatic placement cases PASS. No native geometry/source edit during finalization. Bench remains review/not_ready; no design approval granted. Final evidence: docs/audits/origin-migration-record.json and origin-compatibility-validation.json; repository commit identifies this finalized snapshot.


0.1.2 refinement validation completed; see current evidence below. User acceptance pending; review status retained.


## Current0.1.2 final visual polish —2026-10-15

Review prototype, approval pending.161 saved-source geometry/material/frame/reuse/cap/bracket checks PASS;144 origin checks PASS; four reference image pixel comparisons PASS, max delta0. Source SHA/digests in asset.json. All8 changed object geometries are the four cap variants and four mounting cheeks; remaining coordinates unchanged, original object frames/anchors/pad and major dimensions preserved. Two cap data variants shared twice, normalized positive scale. Actual cap cavity clearances measured from the specified tube-end cross section; no fabrication/load rating claimed. Independent full-frame linked support-placement and two-instance reuse pass.

Current technical evidence is visual-validation-results.json, origin-validation.json and render-reproduction.json; historical0.1.1/A14 results above are preserved as history, not treated as current source geometry checks. Reviewed four images at1600×1000: slender foot-end coverage, clear steel/bracket/pad separation, no bracket protrusion beyond pad footprint, unchanged no-shadow/AO style. All protected other-equipment/fixtures, shared guides/AGENTS and original exports/README edit unchanged. Future cap/bracket/material/source changes invalidate these results. Bench remains review/not_ready and uncommitted until separately requested.
