# Mannequin 0.1.0 — review validation, 2026-10-16

**Overall: REVIEW / not production ready.** No owner visual approval or full anatomy certification is recorded. Passing structural checks do not waive empty masks, observed deformation defects or unperformed release gates. This report extends the existing asset checklist and Human V1 checklist.

Evidence: `observed.json` and `observed.validation.json` (actual saved Blender source); `contract-validation.json` (392 PASS / 65 FAIL, exclusively missing muscle masks); `registry-validation.json` (142 PASS / 0 FAIL); `unit-test-results.json` (47 tests PASS); `review-validation.json` (17 diagnostic checks PASS / 0 FAIL). Counts overlap across reports and must not be added as independent coverage. All65missing mask failures remain active. No validation criteria changed.

Source, fixture, script, dependency and image digests are pinned in the reports/metadata. Standards snapshot is prebuild-record.json. Reviewer: Codex technical/render inspection, not clinical anatomy approval. Blender5.1.1, no add-ons, local review renderer. Root origins and V1 definitions unchanged. Artwork release terms unselected.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Prebuild SPEC/prebuild-record defined before modeling; final SPEC, manifests and stage records reconciled. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | Reviewed/pinned standards; H01–H05 and visual/physique/ROM/export/artwork approvals remain open for production. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | Protected source/standard digest audit passes; A16 documents user-authorized local prototype choices only. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | FAIL | Review documentation agrees; release-critical anatomy coverage, numeric limits and artwork terms remain unresolved. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | New original human; canonical rest data linked from separate rig source. Fixture body/equipment data stay linked. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](licensing.md) | NOT RUN | Original procedural artwork; no imported meshes/textures. MIT scripts/docs separate; artwork license unselected. |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | ID/source/collection/root/published datablocks agree; V1 names and control facade inspected. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | Actual neutral skin height1.750000002m; floor−2.34e−9m, threshold0.00001m; other dimensions provisional and documented. |
| T03 | Axes, intentional category origin, root/collection pivot agreement, component frames, hierarchy, normalized transforms and rest/configuration match A14 | PASS | Human V1 inspector checks meter axes, root/armature identity, floor/collection pivot0 and A-pose/local bone frames. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | FAIL | One closed connected skin,318766verts/318764faces,0nonmanifold edges; bends work but visual pinching/faceting at large shoulder/hip/wrist rotations remains. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | All11anchor frames/owners and required FK/IK facade bindings inspect correctly; seeded actual hand/foot targets pass sampled tests. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | 53canonical bones/52deform, individual digits, measured rest fingerprint, linked rig-data and body material slots intact. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | NOT RUN | Blender5.1.1 successfully reloads source and fixture with relative libraries/no add-ons; separate fresh-checkout/LFS test not performed. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | NOT RUN | One linked bench/barbell pose tested; no second character or retarget/replacement motion test. |
| T10 | Generic category origin validator reports expected/actual root, component and anchor frames; unknown profiles fail closed | N/A | A14 generic validator covers equipment categories. Human origin/frames enforced by the actual saved-character V1 inspector; no equipment edited. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | PASS | Existing equipment, normative definitions and pre-existing fixtures protected byte-for-byte; no consumers of this new human preceded it. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | 10retained standalone/demo views and3fixture views; source/settings/camera/PNG pins in indices. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | All current indexed PNG paths and SHA256 values checked by delivery audit; previews retained outside ignored exports. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | WorkbenchFLAT/VERTEX,32AA,Standard,white RGBA,exact cameras/frame/resolution/ramp/outline/native width documented; no stochastic path tracer. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | FAIL | Rendered review confirms recognizable continuous mannequin and working highlights; shoulders/hip ledge, palm web/finger grip, X-ray depth and large-rotation skinning need polish/review. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | No ground/lights, cast shadows, AO/cavity/specular or baked image textures; actual PNGs visually inspected. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | NOT RUN | Saved-source render and fixture builders repeatedly exercised; commands/digests recorded. Independent checkout/session and strict pixel comparison not certified. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | NOT RUN | Review PNG bundles only; animation/vector/consumer export profiles and roundtrips not selected or validated. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | SPEC/USAGE/metadata/A16/reference indices and actual validation reports describe current review source. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | Git LFS filter applies to blend sources; blend backups/exports ignored. New files are uncommitted; user did not request a commit. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | FAIL | Review only:65empty masks explicitly fail coverage; anatomy/deformation/production approval and other release gates remain incomplete. |

## Human V1 extension and measured cases

| Check | Result | Actual / limitation / evidence |
| --- | --- | --- |
| Contract/schema/catalog and source/dependency pins | PASS | Actual inspector; immutable V1 lock and prebuild guard |
| 53bones / parents / connected / deform flags / digits | PASS | All exact V1 canonical names; 52deform plus root |
| Meter axes / intentional floor origin / collection pivot | PASS | Identity root/armatures, floor≈0, offset0 |
| Measured 45° A-pose / local roll / rest profile | PASS | Measured rest-profile.json matches stored fingerprint |
| Skin-weight normalization | PASS | Actual body/deep weights inspected; no unweighted vertices |
| Deformation quality over a production motion range | FAIL | Sample bends deform but shoulder/hip/wrist pinching and twist need corrective work; no production range certified |
| FK facade / hand-foot IK / poles / no stretch | PASS | Required bindings plus four reachable targets tested with nonzero bend seeds; position residuals below0.1mm local diagnostic threshold |
| IK/FK snap / twist / singularity recovery | NOT RUN | Manual seeded straight-chain startup works; no automatic snap/recovery certification |
| Joint constraints | NOT RUN | Four active engineering hinge guardrails structurally checked; complete sourced clinical limits unapproved |
| 11 anchor frames and bone ownership | PASS | Full source frames inspected; posed grips follow output |
| 78 independent masks and anatomy boundaries | FAIL | 13real masks (12surface+1deep),65empty; all78IDs/156APIproperties preserved; boundaries need review |
| Primary / secondary actual shading | PASS | Evaluated pec colors change by0.461, role difference0.268; rendered combined regional highlights and posed biceps/pec/triceps evidence |
| On-character deep X-ray | PASS | Actual skin window removes6415faces; real deep geometry skinned tothigh_l and moves with bent thigh; style/anatomy unapproved |
| Highlight through garments | NOT RUN | No garments supported/created; cannot claim coverage through clothing |
| Retarget / proportion swap / animation interchange | NOT RUN | Only one measured profile; no second character or animation/export claim |
| Linked bench pose grip frames | PASS | 680mm mirrored stations; maximum residual≈0.002mm; exact values review-validation.json |
| Body versus bench intersections | PASS | Zero evaluated triangle surface crossings after pose placement correction; not a containment/self-collision proof |
| Floor planting | NOT RUN | No floor penetration in sampled pose; actual minimum Z positive, sole support approximate |
| Bar / palm / individual finger contact | NOT RUN | Gripping fingers articulated and anchor centers match shaft; thumb opposition/webbing and full collision-free moving contact not certified |
| Human visual reference approval | NOT RUN | Local gray/red/amber ramp, outlines and X-ray need owner review |
| Export bake / sidecar / target roundtrip | NOT RUN | No selected export profiles or animation bake |
| H01–H05 / artwork approval | NOT RUN | Local prototype only; global decisions remain open |

## Commands and expected outcomes

From repository root (macOS native Blender5.1.1):

```sh
python3 -m unittest discover -s tests -p test_human_contract.py
python3 scripts/pipeline/validate_human_contract.py --output assets/humans/models/168h_human_anatomical_mannequin/registry-validation.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup assets/humans/models/168h_human_anatomical_mannequin/168h_human_anatomical_mannequin.blend --python-exit-code 1 --python scripts/blender/inspect_human_contract.py -- --manifest assets/humans/models/168h_human_anatomical_mannequin/human-contract.json --output assets/humans/models/168h_human_anatomical_mannequin/observed.json
python3 scripts/pipeline/validate_human_contract.py --manifest assets/humans/models/168h_human_anatomical_mannequin/human-contract.json --snapshot assets/humans/models/168h_human_anatomical_mannequin/observed.json --output assets/humans/models/168h_human_anatomical_mannequin/contract-validation.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_mannequin_review.py
```

The inspector and character validator intentionally exit1 for65empty bindings. Do not hide their exit code or relax full-coverage gates. The asset-local diagnostic validator reports numerical/configuration cases, not full anatomy acceptance. Re-render with render_anatomical_mannequin.py; rebuild only the review fixture with build_mannequin_bench_review.py. Neither operation saves the neutral character source or any equipment source.

## Corrections during this first build

Surface fairing unified the initial construction; root/published interfaces remained fixed. Initial hip polish accidentally affected hand vertices sharing a height band and was discarded from the pre-polish checkpoint; delivered evidence uses the corrected region restriction. A measured rather than unnormalized rest-axis fingerprint fixed an early metadata mismatch. IK from a perfectly straight chain initially left hands high; nonzero bend seeds and symmetric arm pole settings fixed support coordinates. Local skin-weight smoothing/linear blending reduced joint inflation. Moving the human toward the bench foot end removed detected thigh/pad/frame intersections; no equipment geometry/dimensions changed. All final evidence was regenerated/invalidated as appropriate.

Remaining work: full muscle coverage, reviewed anatomy/highlight boundaries, shoulder/hip/palm/finger deformation and contact refinement, automatic rig snapping/twist behavior, clothing if supported, second-character retarget/replacement proof, approved export/animation pipeline and separate artwork licensing. No current claim of production readiness, clinical accuracy or safe bench-press technique.
