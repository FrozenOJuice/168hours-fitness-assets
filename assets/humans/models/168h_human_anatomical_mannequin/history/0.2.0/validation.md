# Mannequin foundation0.2.0 validation —2026-10-16

**REVIEW, not production ready.** Actual-source inspector/contract validator:392 PASS/65 FAIL (only unimplemented muscle masks). Foundation tests:60 PASS/0 FAIL. Unit tests:47 PASS. Registry:142 PASS. Numerical passes do not approve anatomy or waive missing masks/production gates. Diagnostic thresholds are scoped to this asset and are not shared approved contact/clinical standards.

Evidence: observed.json, observed.validation.json, contract-validation.json, foundation-validation.json, registry-validation.json, unit-test-results.json; native source/dependency/scene/PNG pins in manifests and presets. Protected inputs are pinned in foundation-plan.json. Manual/render reviewer is Codex; owner anatomy/visual acceptance is pending. See FOUNDATION-REPORT.md for remaining weaknesses. The older0.1.0 checklist/reports are retained in history/0.1.0.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Foundation plan/SPEC recorded before geometry changes; final SPEC/report/metadata match current0.2.0. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | NOT RUN | Standards reviewed/pinned; H01–H05 and production/artwork approvals remain open. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | 213 protected files unchanged; A17 records user-authorized local correction, no shared definition change. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | FAIL | Current facts agree; full anatomy/coverage/export/licensing release facts remain unresolved. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | Reuse of licensed body topology; separate rig data; linked core tests share skin data. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](licensing.md) | NOT RUN | Upstream graphical CC0 notices/source hashes retained; original code/docs MIT separately; project artwork release terms unselected. |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | Stable model/collection/root/output and53 canonical names/11 anchors preserved; current manifests reconcile paths/versions. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | Measured skin1.75 m/floor0 within10um; current profile and other provisional dimensions recorded in SPEC/rest-profile.json. |
| T03 | Axes, intentional category origin, root/collection pivot agreement, component frames, hierarchy, normalized transforms and rest/configuration match A14 | PASS | Actual V1 inspector checks source axes, intentional floor origin, positive unit transforms, offset0 and canonical rest frames. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | FAIL | Continuous closed skin and core deformation diagnostics pass; full-overhead shoulder/scapular shape and extreme/twist behavior still need correction/review. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | 11 source frames/owners and facade inspect correctly; four IK targets/orientations, explicit two-way snapping and static grip measured. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | 53 bones/52 deform, finger chains, measured new profile, normalized weights and skin material role retained. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | NOT RUN | Fresh Blender processes reload current source/suite with relative libraries/no add-ons; independent fresh checkout/LFS clone not tested. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | NOT RUN | One morphology and7 pose states only; no second-character replacement/retarget claim. |
| T10 | Generic category origin validator reports expected/actual root, component and anchor frames; unknown profiles fail closed | N/A | A14generic tool targets equipment. Human origin/frames are enforced by V1 actual-source inspection; equipment is unchanged. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | PASS | Approved sources unchanged; rejected0.1.0 profile/native/evidence retained and old review bench fixture explicitly invalidated. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | 4neutral references plus15 core-suite renders cover all 7requested poses and hand detail. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | Current indexed image/source/settings paths and SHA256 values checked; old current-folder previews archived. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | Exact WorkbenchFLAT/VERTEX cameras/resolutions/AA/gray ramp/native outline/color management recorded in presets; local review settings only. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | FAIL | Neutral body reads substantially more human; core bends inspected. Shoulder broadening and high-flexion crease/grip presentation still require owner/art review. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | No ground shadows, AO/cavity/specular or baked image textures; source and review renders checked. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | NOT RUN | Saved-source render/suite regeneration exercised with retained parameters; independent checkout/pixel-exact reproduction not certified. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | NOT RUN | PNG review bundles only; animation/consumer export profiles and roundtrips outside this pass. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | SPEC/report/USAGE/metadata/decision/reference index/actual validation evidence describe current foundation. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | NOT RUN | Existing LFS applies to.blend/.obj; temporary backups/exports ignored. Changes remain uncommitted because this task did not request a commit. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | FAIL | Review only:65 empty masks and unperformed anatomy/production/retarget/export/artwork gates remain; no owner approval. |

## Human V1 and foundation cases

| Check | Result | Actual / limitation |
| --- | --- | --- |
|53bone structure, digits and roll/A-pose | PASS | Exact V1 names/parents/deform/connectivity; measured0.2.0 profile, identity saved output pose |
| Origin / units / transforms / collection pivot | PASS | Meters, root0 floor projection, positive unit scale/identity source transforms, offset0 |
|11 anchors / dynamic ownership | PASS | Source frames inspected; solved hand/foot orientation and static shaft stations measured |
| Skin weights / surface | PASS | Core normalized weights, one closed connected mesh,214050 verts/214048 faces, zero nonmanifold edges |
| FK facade / four IK targets and poles / stretch | PASS | Current graph inspected; native nonstretch solutions and orientation tests pass |
| IK/FK continuity | PASS | Explicit snap helpers tested both ways; raw mode property toggles are not a general snapping UI |
| Seven saved pose states | PASS | Linked data and finite identical topology; all bone lengths retained |
| Knee collapse / intersections | PASS | Zero tested inward X drift, width≈100%, positive knee separation; zero tested separate-leg and disjoint thigh/calf crossings |
| Five-angle knee sweep | PASS |0/30/60/90/105°with hip80°; zero sampled thigh/calf crossings |
| Static grip | PASS |580mmspan,28mmshaft; all selected digit and palm vertices outside cylinder; closest gaps≈0.356–0.505 mm |
| Complete deformation/art acceptance | FAIL | Overhead shoulder/scapular broadening, residual high-flexion creases and twist/extreme motion remain weaknesses |
|78muscle masks / anatomical boundaries | FAIL |78 IDs/156 properties retained;13 provisional remaps/65 empty; no false full-coverage claim |
| Clothing highlighting | NOT RUN | No garments in this correction scope |
| Second-character retarget/replacement | NOT RUN | New profile not direct-pose compatible with rejected0.1.0; no alternate morphology built |
| Full continuous motion/self-collision/clinical ROM | NOT RUN | Sparse diagnostic poses/sweep only; no safety or physiological claim |
| Approved human preset / anatomy reference | NOT RUN | Local illustrated gray style preserved; owner approval pending |
| Export / animation / bake / roundtrip | NOT RUN | Outside correction focus; no target profile chosen |
| H01–H05 / artwork release terms | NOT RUN | Local review implementation only |

## Re-run commands

From repository root:

```sh
python3 -m unittest discover -s tests -p test_human_contract.py
python3 scripts/pipeline/validate_human_contract.py --output assets/humans/models/168h_human_anatomical_mannequin/registry-validation.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup assets/humans/models/168h_human_anatomical_mannequin/168h_human_anatomical_mannequin.blend --python-exit-code 1 --python scripts/blender/inspect_human_contract.py -- --manifest assets/humans/models/168h_human_anatomical_mannequin/human-contract.json --output assets/humans/models/168h_human_anatomical_mannequin/observed.json
python3 scripts/pipeline/validate_human_contract.py --manifest assets/humans/models/168h_human_anatomical_mannequin/human-contract.json --snapshot assets/humans/models/168h_human_anatomical_mannequin/observed.json --output assets/humans/models/168h_human_anatomical_mannequin/contract-validation.json
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_mannequin_foundation.py
```

The character inspector/offline validator deliberately exit1 for65 missing bindings. Do not waive those failures or label full Human V1 coverage/release PASS. The foundation tool reports60actual diagnostic cases and preserves source bytes; its criteria do not replace the manual/release checklist. Source and test renders are regenerated with render_mannequin_core.py and build_mannequin_core_suite.py respectively. Both operate on the saved source and retained grip-fit.json; they do not save/edit the character or approved barbell.

## Correction history / limits

SPEC and foundation-plan.json were written before the bind/topology replacement. Source-frame adaptation initially lifted toes; binding the coherent foot/toes through the foot frame corrected it. Real posterior knee surface crossings at90°/105°were removed by a zero-at-rest continuous soft-tissue field, not by changing test tolerances. Finger-only contact tests missed palm penetration; extending the test found it, and the measured grip datum/refit resolved it. Little-finger optimizer local-minimum failure was fixed with a coarse search. Inherited native scene/UI load-state dirtiness was removed by a geometry-preserving clean repack; inspector guard unchanged. All affected final source/suite/renders/reports were refreshed.

The old bench fixture is invalidated; do not infer new exercise compatibility. Keep REVIEW until owner anatomy/style acceptance and outstanding deformation/release gates are resolved. Do not promote provisional proportions, motion/contact criteria or numeric render values into shared standards.
