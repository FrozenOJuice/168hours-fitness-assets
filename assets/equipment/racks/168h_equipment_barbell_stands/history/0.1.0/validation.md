# Asset review checklist and validation record

Copy this reusable checklist into each future asset directory as `validation.md`. Apply to new assets and updates; extend with [category-specific cases](../../../../docs/category-standards.md). Adjust policy links relative to the asset folder when copying this file. Current prototype has saved-source machine QA and manual render review; see validation-results.json.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Asset ID / version / category: 168h_equipment_barbell_stands /0.1.0 /equipment-racks
- Source revision or file digest / dependency revisions: 839aa792f464b2b043f4d95ca219159b067710c0ee314febc7f59f419983caad; standalone none; assembly pins in fixture asset.json
- `SPEC.md` and `asset.json` paths: SPEC.md /asset.json in this directory
- Standards revision / style preset and revision: prebuild-record.json /stands_review_flat@0.1.0 /0bf2ed0637846172998a2e8bba6d86f6d4b4f7ec230fc91ee14debac4202d2a9
- Blender / add-on versions: 5.1.1 /none
- Reviewer / date: Codex technical/manual QA /2026-10-15; user acceptance pending
- Status being requested (`review` or `ready`): review
- Applicable open decisions, approved exceptions, and acceptance reference: Local prototype design/interface/preset acceptance and V06 assembly reproduction pending; no shared exception or acceptance granted

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Prebuild spec/manifest/checklist digests retained; current facts reconciled in SPEC.md. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | Release approval pending; scoped prototype uses existing approved style cues, no shared promotion. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | 269 protected hashes unchanged; asset-local proposals only. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | NOT RUN | Digital facts agree, but release-critical design/licensing and exact assembly reproduction remain open. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | 64 mesh objects/32 data; all opposing components share meshes. No approved geometry duplicated. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](../../../../docs/licensing.md) | NOT RUN | Original procedural provenance documented; no third-party artwork. External artwork terms unselected, MIT code/docs separate. |

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
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | PASS | Scoped fixture only: approved bench/barbell linked, actual shaft line, liner contact,75mm flange/73.75mm base clearances, zero BVH crossings. No alternative/human/physical test. |
| T10 | Generic category origin validator reports expected/actual root, component and anchor frames; unknown profiles fail closed | PASS | Existing rack origin profile used,243 detailed expected/actual checks; no new hardcoded rule. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | N/A — new asset | No existing consumers of this new interface; all original approved assets unchanged. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | 5standalone views incl front/side/threequarter/max/detail;3assembly views. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | All preview paths/source/preset/image hashes in manifests and settings. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | Blender/version/engine/cameras/palette/native outlines/32AA/Standard/whitebackground recorded. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | PASS | Manual delivery-size review of all8images; full silhouettes, contact readable, no logos. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | FLAT/nativeoutlines; no lights/ground/shadows/AO/cavity/specular/baked maps. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | FAIL | 5standalone exact PASS;3assembly exact FAIL. Final final probe max6/255 on0.05169% channels; no tolerance waiver, unresolved review/release gate. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | N/A — native review only | No interchange/fabrication exports or A08 production formats claimed. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | SPEC, metadata, local decisions, evidence/index and source pins reconciled. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | LFS attrs and backup/export ignores verified; new files untracked, no commit requested. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | NOT RUN | Review prototype; user design approval and exact assembly reproduction unresolved, external art license unselected. |

## Category-specific checks

Add rows for the actual measurement and compatibility cases required by the applicable category. State fixture/consumer, input configuration, expected result/tolerance, observed result, and evidence. Do not mark hypothetical fixtures as tested.

| Case | Configuration / expected result | Observed result | Status / evidence |
| --- | --- | --- | --- |
| Saved-source detents/contact | 16height detents, mixed0/15,28mm bar shaft+X | 449PASS/0FAIL plus243 generic origin details | validation-results.json / origin-validation.json |

## Outcome and changes since review

- Overall result and supported compatibility claims:
- Outstanding failures / unperformed checks / reasons:
- Approver, date, and explicit acceptance reference:
- Changed source, spec, preset, or dependency revisions since review:
- Invalidated results and required reruns:

After material changes, revert status to `draft` or `review` and mark affected results `NOT RUN`; retain prior evidence history. Mark `ready` only when the [workflow gates](../../../../docs/asset-workflow.md) are satisfied.

## Recorded outcome

Review prototype completed.449geometry/compatibility checks PASS,243generic-origin details PASS; same449PASS after relocation.5standalone renders exact;3assembly exact comparisons FAIL and remain open. All269protected files unchanged. No release approval or shared-standard changes. Native/render/source changes invalidate these records.

Pair floor_contact ownership is explicitly checked against the pair root; floor_l/r belong to independent stand controllers, sliding anchors to corresponding upper controllers. All449checks pass on current and relocated sources.
