# Asset review checklist and validation record

Copy this reusable checklist into each future asset directory as `validation.md`. Apply to new assets and updates; extend with [category-specific cases](../../../../docs/category-standards.md). Adjust policy links relative to the asset folder when copying this file. Current prototype has saved-source machine QA and manual render review; see validation-results.json.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Asset ID / version / category: 168h_equipment_barbell_stands /0.1.1 /equipment-racks
- Source revision or file digest / dependency revisions: 5b20912217f58c5659a0aed4ed79349c8d8186323daec3be762b30a91c75bcae; source no external geometry; assembly dependency pins in fixture asset.json
- `SPEC.md` and `asset.json` paths: SPEC.md /asset.json in this directory
- Standards revision / style preset and revision: prebuild-record.json /stands_review_flat@0.1.0 /e5a83f4c2260704d4ba49c792d63aaece44805288fd4fa9b0cd3ff4475e9c6bf
- Blender / add-on versions: 5.1.1 /none
- Reviewer / date: Codex technical/manual QA /2026-10-15; user conditional acceptance completed under explicitly approved local comparison
- Final status: ready / approved internal illustration use; approval-record.json
- Applicable open decisions, approved exceptions, and acceptance reference: Local asset/interface/preset accepted for internal illustration use; scoped comparison approved in render-comparison-policy.json, no shared promotion.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Prebuild spec/manifest/checklist digests retained; current facts reconciled in SPEC.md. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | PASS | Asset-local choices accepted under conditional approval; shared numerical defaults remain unchanged. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | 269 protected hashes unchanged; asset-local proposals only. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | PASS | Current native, corrected fixture, metadata and reference pins reconciled; internal scope/physical assumptions/external license limits explicit. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | 64 mesh objects/32 data; all opposing components share meshes. No approved geometry duplicated. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](../../../../docs/licensing.md) | PASS | Original procedural provenance, no imported artwork; scoped internal approval recorded, external artwork reuse grant remains unselected and separate from MIT. |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | Stable ID/native/collection/root and lowercase names; saved-source checks. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | 1696.9x622.3x1048mm pair; perstand596.9x622.3mm. Manufacturer context/provisional details distinguished. |
| T03 | Axes, intentional category origin, root/collection pivot agreement, component frames, hierarchy, normalized transforms and rest/configuration match A14 | PASS | 243 generic origin details; centered floor root/pivot, intentional component frames, +Zup/+Yfront, positive unit transforms. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | PASS | All closed/outward/nondegenerate meshes; all16 detents and0/15 mixed controls; genuine open pin bores. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | Seven anchors and measured liner support, sliding frames follow controls; local interface0.1.0. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | Three nonempty semantic slots per mesh, no skeleton; independent rigid sliders. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | PASS | Saved Blender5.1.1 reopen and relocated filesystem copy pass; relative links resolve, no hidden addons. Fresh committed Git/LFS checkout NOT RUN. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | PASS | 647 compatibility checks,45independent measurements,0crossings; actual contact0.093209/0.092185µm<1µm after scene-owned settlement; anchors/sources unchanged. |
| T10 | Generic category origin validator reports expected/actual root, component and anchor frames; unknown profiles fail closed | PASS | Existing rack origin profile used,243 detailed expected/actual checks; no new hardcoded rule. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | N/A — new asset | No existing consumers of this new interface; all original approved assets unchanged. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | 6standalone views incl front/side/threequarter/max/detail;3assembly views. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | All preview paths/source/preset/image hashes in manifests and settings. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | Blender/version/engine/cameras/palette/native outlines/32AA/Standard/whitebackground recorded. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | PASS | Manual delivery-size review of all9images; full silhouettes, contact readable, no logos. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | FLAT/nativeoutlines; no lights/ground/shadows/AO/cavity/specular/baked maps. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | PASS | 9views PASS,3runs/27comparisons;7views exact,2within explicitly approved render-comparison-policy.json; relocated9views PASS. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | N/A — native review only | No interchange/fabrication exports or A08 production formats claimed. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | SPEC, metadata, local decisions, evidence/index and source pins reconciled. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | PASS | LFS/ignore attributes verified; focused tracking/commit and fresh-checkout evidence recorded during repository finalization. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | PASS | All scoped tests pass; user conditional approval and explicit numeric-policy approval recorded; internal-use restrictions explicit. |

## Category-specific checks

Add rows for the actual measurement and compatibility cases required by the applicable category. State fixture/consumer, input configuration, expected result/tolerance, observed result, and evidence. Do not mark hypothetical fixtures as tested.

| Case | Configuration / expected result | Observed result | Status / evidence |
| --- | --- | --- | --- |
| Saved-source detents/contact | 16height detents, concentric cradle, clip/hook holes, preservation and28mm bar shaft+X | 646PASS/0FAIL plus243 generic origin details | validation-results.json / origin-validation.json |

## Outcome and changes since review

- Overall result and supported compatibility claims:
- Outstanding failures / unperformed checks / reasons:
- Approver, date, and explicit acceptance reference:
- Changed source, spec, preset, or dependency revisions since review:
- Invalidated results and required reruns:

After material changes, revert status to `draft` or `review` and mark affected results `NOT RUN`; retain prior evidence history. Mark `ready` only when the [workflow gates](../../../../docs/asset-workflow.md) are satisfied.

## Recorded outcome0.1.1

646geometry/preservation/compatibility checks PASS;243origin details PASS; same646PASS after relocation. All76objects/original frames/32shared data and slot order preserved,38unedited meshes exact. Current source/preset/image pins in asset.json. Sixstandalone images and assemblyfront exact; twoassembly images strict FAIL (max8/255,on0.02139% channels). Review acceptance, precise unpublished dimensions, external artwork release and V06 remain open. Original269protected files unchanged; no shared-standard change. Full implementation evidence in refinement-record.json and manufacturer-reference.md.

## Historical failed approval gate — superseded below

**FAIL / approval withheld; no commit.**646existing checks and243origin details PASS; direct measurements43PASS/2FAIL; origin fault/placement6+2PASS; pixel reproduction7PASS/2FAIL. Current authoring serialization reconciled by exact semantic comparison, original artifact retained. All native source and reference PNG bytes preserved during this audit. Read final-audit.json/SPEC final section for F01 seating, F02 reproduction, actual pin clearance and recommended corrections. Earlier PASS contact statements refer only to nominal anchor placement and are superseded by this measured contact gate.

## Current final outcome — supersedes earlier failed audit

Approved internal illustration asset.647geometry+243origin+45measurement checks PASS,6+2origin/placement tests PASS,9image-comparison tests PASS,27reference comparisons PASS. Contact corrected only in fixture; existing1µm and zero-crossing gates unchanged. Two assembly comparisons use the explicit approved exception; all others exact. See approval-record.json/final-audit.json and SPEC final section. Earlier failed records are historical; no open approval blocker remains.

Repository finalization PASS: focused commit includes native/history/evidence under existing LFS rules; fresh local Git/LFS checkout passes647+45+9checks, with243origin details. Git/LFS fsck PASS. Existing unrelated exports/README.md edit left untouched. Evidence: committed-checkout-validation.json.
