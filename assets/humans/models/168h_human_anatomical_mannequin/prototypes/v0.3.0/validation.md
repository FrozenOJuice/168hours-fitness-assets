# Validation record — anatomical mannequin0.3.0

Reviewer: Codex,2026-10-16. Status: **review, not ready**. SourceSHA256 `86bad3bb57a1bd1789d2f759aa485fbd957e64d971998c463b757f9b5d7cb1a2`; studySHA256 `15a21d8ee932b7cfe6a6770a5317a9b0c96236249beeb437db0acf9c72a8dc7f`. Dependencies pinned in asset.json. Standards: unchanged Human Model ContractV1 registries/AGENTS; provisional asset-local Workbench preset in previews/render-settings.json. Blender5.1.1; no add-ons. No release/visual approval requested or inferred.

## Automated evidence

| Check | Result | Evidence and scope |
| --- | --- | --- |
| Existing V1 unit suite |47PASS|unit-validation.json; data/schema tests, not anatomy |
| V1 registry/schema pins |142PASS/0FAIL|registry-validation.json |
| Saved-native V1 inspection + offline snapshot |394PASS/63FAIL|observed.json, observed.validation.json, contract-validation.json; only63unimplemented muscle bindings fail |
| Local actual-source/study diagnostics |57PASS/0FAIL|study-validation.json; sparse states, knees/leg separation, IK/snap, anchors, finite geometry, helper isolation, dynamic color/Xray checks |
| Protected predecessor/equipment/contract bytes |385unchanged|plan.json + preserved_work check |

The63coverage failures remain real failures. Structural passes do not certify visual anatomy. No tolerances were weakened to eliminate knee intersections. The Xray vertex-count expectation was corrected solely for intentional DeleteGeometry removal of faces **and unused vertices**; all ordinary poses still require the full vertex count.

Zero measured disjoint thigh/calf crossings in seated, hip/knee bend and squat, and zero crossings between distinct leg regions below hips. Tests exclude±40mm knee-transition and use declared rest-region masks; not a universal self-intersection/containment test. Native joint compression is an artist-authored correction, not clinical mechanics.

Four reachable IK/snap cases remain within0.1mm (largest target residual0.001502mm). Mirrored grip-anchor error~0.031mm; sampled selected finger penetration0mm and maximum closest-finger gap2.154mm. Palm gaps~8.4mm and simplified thumb opposition prevent claiming a finished gripping system. Full triangle/cylinder collision, wrist-twist motion and load-bearing hand contact are not validated.

Localized Xray removes387skin faces and exposes an actual skinned deep volume before the posterior wall on the test ray. This proves on-character local revelation, not accurate vastus-intermedius anatomy or polished aperture edges. Independent selected pectoral primary affects actual surface colors without opposite-pectoral leakage; primary/secondary colors differ.15nonempty bindings/78 remain provisional;63empty. No clothing implementation or through-clothing proof.

## Mandatory review checklist

Rows follow docs/review-checklist.md; PASS has the bounded meaning stated here.

| ID | Result | Evidence / limitation |
| --- | --- | --- |
|D01|PASS|Prebuild SPEC retained; final implementation, rationale and reproduction appended.|
|D02|FAIL|H01–H05 release approvals unresolved; V1 unchanged.|
|D03|PASS|A18 records user-authorized isolated choices; no shared standard promoted.|
|D04|FAIL|Documented provisional physique/style, incomplete coverage and unselected project artwork release terms prevent release.|
|D05|PASS|Single continuous skin, shared-mesh helper; linked rig/equipment and pose overrides.|
|D06|PASS|Official native embedded CC0 author/license evidence, provenance hashes and comparison in RESEARCH.md; artwork/code terms separate.|
|T01|PASS|Stable family ID and published names isolated under prototypes/v0.3.0; names inspected.|
|T02|PASS|Floor4.32e-9m, height1.749999996m; provisional target1.75m. Metadata A-pose envelope.|
|T03|PASS|Human inspector canonical axes, floor root, collection offset, normalized transforms and frames pass.|
|T04|FAIL|One continuous closed all-quad skin and sampled knees pass; extreme hip folds and shoulder mechanics remain visually limited.|
|T05|PASS|53canonical bones/11anchors and4IK/snap cases pass; exact frames in observed.json.|
|T06|FAIL|V1 interface passes;63muscle regions empty; no retarget/export release certification.|
|T07|PASS|Fresh CLI opens saved character/study; relative linked libraries resolve, no add-ons. Fresh remote LFS checkout not tested.|
|T08|NOT RUN|One static28mm-shaft grip sampled; no body variant, arbitrary equipment replacement or full motion certification.|
|T09|PASS|385protected masters/contracts/equipment/prior fixtures retain exact bytes; no replacement applied.|
|T10|N/A|Equipment category-origin validator does not cover human profiles; V1 inspector checks human origins/frames.|
|V01|PASS|7unassembled and32study PNGs, including all13states, closeups and two comparisons.|
|V02|PASS|PNG hashes/source/preset pins in metadata/settings; packaging script verifies all paths/hashes.|
|V03|PASS|Asset-local settings record cameras, resolution, engine, AA, color management, palette/ramp, outlines, alpha/background and comparison override. Workbench has no stochastic render seed.|
|V04|FAIL|Visual inspection confirms improved neutral anatomy but hip/groin creases, thumb/palm and Xray edges still require correction/review. Muscular physique is not accepted as a universal gender-neutral body.|
|V05|PASS|No cast shadows/AO/cavity/specular; tonal surface illustration only.|
|V06|NOT RUN|Ordered scripts and pinned inputs supplied; no second-machine reproduction or pixel-exact claim.|
|V07|N/A|Native review and PNGs only; no animation/interchange export requested or certified.|
|R01|PASS|Current SPEC, manifests, provenance, validation records and review limitations supplied.|
|R02|PASS|Existing .blend LFS and ignored backups/cache/generated-export rules apply. Work remains uncommitted; no commit requested.|
|R03|FAIL|Review prototype; no owner acceptance, full anatomy/coverage/retarget/export evidence or resolved release decisions.|

## Visual inspection and outcome

Inspected final neutral body/torso views, all pose families in three-quarter or side, overhead shoulder closeup, grip detail, highlight states, Xray states and front comparison. REPORT.md records pose-specific findings. No qualified anatomy reviewer or owner has accepted these. Not all32views receive an independent human review. Keep reference images, source pins and failures when continuing refinement. Any source/rig/preset changes invalidate dependent evidence and require regeneration/revalidation.

Remaining priority: hip/groin and lower-abdominal flexion correctives; broader scapular/shoulder/twist motion; palm/thumb contact; source-aligned muscle boundaries and deep-window finish. Complete63missing bindings, garment behavior, retarget/replacement and export evidence before release. Preserve current master/equipment until explicit replacement review. No approval date/reference exists.
