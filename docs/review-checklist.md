# Asset review checklist and validation record

Copy this reusable checklist into each future asset directory as `validation.md`. Apply to new assets and updates; extend with [category-specific cases](category-standards.md). Adjust policy links relative to the asset folder when copying this file. No assets have been built or validated yet. This is manual validation, not an automated Blender test suite.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Asset ID / version / category:
- Source revision or file digest / dependency revisions:
- `SPEC.md` and `asset.json` paths:
- Standards revision / style preset and revision:
- Blender / add-on versions:
- Reviewer / date:
- Status being requested (`review` or `ready`):
- Applicable open decisions, approved exceptions, and acceptance reference:

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | NOT RUN | |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | NOT RUN | |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | NOT RUN | |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | NOT RUN | |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](licensing.md) | NOT RUN | |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | NOT RUN | |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | NOT RUN | |
| T03 | Axes, intentional category origin, root/collection pivot agreement, component frames, hierarchy, normalized transforms and rest/configuration match A14 | NOT RUN | |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | NOT RUN | |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | NOT RUN | |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | NOT RUN | |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | NOT RUN | |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | NOT RUN | |
| T10 | Generic category origin validator reports expected/actual root, component and anchor frames; unknown profiles fail closed | NOT RUN | |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | NOT RUN | |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | NOT RUN | |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | NOT RUN | |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | NOT RUN | |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | NOT RUN | |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | NOT RUN | |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | NOT RUN | |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | NOT RUN | |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | NOT RUN | |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | NOT RUN | |

## Category-specific checks

Add rows for the actual measurement and compatibility cases required by the applicable category. State fixture/consumer, input configuration, expected result/tolerance, observed result, and evidence. Do not mark hypothetical fixtures as tested.

| Case | Configuration / expected result | Observed result | Status / evidence |
| --- | --- | --- | --- |
| TBD | TBD | TBD | NOT RUN |

## Outcome and changes since review

- Overall result and supported compatibility claims:
- Outstanding failures / unperformed checks / reasons:
- Approver, date, and explicit acceptance reference:
- Changed source, spec, preset, or dependency revisions since review:
- Invalidated results and required reruns:

After material changes, revert status to `draft` or `review` and mark affected results `NOT RUN`; retain prior evidence history. Mark `ready` only when the [workflow gates](asset-workflow.md) are satisfied.
