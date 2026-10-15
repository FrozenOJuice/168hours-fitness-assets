# Asset review checklist and validation record

**Current A14 result: asset1.0.0, 84 origin/transform/component/anchor checks PASS; current migration regression28 PASS.** Native/source/preset pins in current asset.json and docs/audits/origin-migration-record.json. Historical0.x rows below retain frozen geometry/visual approval evidence and are superseded for changed origin semantics by the A14 section.

Copy this reusable checklist into each future asset directory as `validation.md`. Apply to new assets and updates; extend with [category-specific cases](../../../../docs/category-standards.md). Adjust policy links relative to the asset folder when copying this file. Barbell 0.1.2 review record: 55 automated checks passed plus visual review. This combines the reusable checklist, asset-specific automated checks and manual image review.

Use `PASS`, `FAIL`, `NOT RUN`, or `N/A — reason`. Record measured/observed values, repository-relative evidence paths, and commands or manual steps; a checkbox or assertion without evidence is insufficient. Every applicable `FAIL`/`NOT RUN` blocks `ready`; checks outside the explicitly approved A12 internal illustration scope are recorded as exclusions, not passing hardware tests. An inapplicable check requires a reason; missing equipment/consumers does not justify an unqualified compatibility claim.

## Review identity

- Asset `168h_equipment_olympic_barbell_20kg` / 0.1.2, equipment/free_weights, 2026-10-14.
- Reviewer: Codex technical and image inspection; user design acceptance recorded under A12. Status **ready**, approved for internal Blender illustration use under A12.
- Source SHA256 `9c6c8c83666553c0f2d49e8a4547aba6b8eaa191d493940e8d16f8b319f9cfcb`; fixture and plate hashes in [results](validation-results.json).
- [SPEC.md](SPEC.md), [asset.json](asset.json), [standards snapshot](standards-snapshot.json), [render settings](previews/render-settings.json).
- Blender 5.1.1, no add-ons, bundled NumPy for pixel comparison; `barbell_review_flat@0.1.2` local provisional preset.
- Current user explicitly authorizes existing-asset refinement and capacity tests. A11 records local choices/proposed contract; global A01/A03/A04/A05/A06/A07/A08 open.

## Specification and approval gates

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| D01 | Specification was defined before building and now describes finished geometry, dimensions, materials, interfaces, rationale, dependencies, and reproduction steps | PASS | Original pre-build hash in build-record.json; Original geometry plan in refinement-plan.json, current findings/plan in compatibility-review.md and contrast-example-plan.json, preserved predecessor files, finished facts reconciled. |
| D02 | Applicable global/category standards are referenced at a revision; approval-dependent choices are resolved for release | PASS | A12 explicitly approves captured asset-local software/material/interface/delivery choices for internal illustration use; global standards unchanged. |
| D03 | Shared changes and conflicting exceptions have explicit approval, scope, consumer impact, and mitigation; no silent standards change | PASS | A11 is a local proposal; category/global standards and every plate artifact remain unchanged. |
| D04 | Specification and JSON agree; no placeholders or unknown release-critical dimensions, settings, licenses, or compatibility facts | PASS | Current metadata/spec facts agree and limitations are explicit. Nominal mass/hardware/third-party redistribution are outside approved internal illustration scope; no unknowns silently asserted. |
| D05 | Reuse opportunities were assessed; new or duplicated geometry has a documented reason | PASS | No prior silver/barbell component existed; sleeves/caps share 2 mesh datablocks, and single-plate fixture links the original plate twice and capacity fixture links it20 times, with zero local geometry. |
| D06 | Creator, origin, separate artwork license, attribution, and measurement references are documented; third-party use is permitted under the [licensing policy](../../../../docs/licensing.md) | PASS | Original creator/provenance documented, no third-party artwork imported. User A12 authorizes internal production. Artwork distribution rights remain reserved/unselected separately from MIT; no external grant claimed. |

## Geometry and technical contracts

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| T01 | Asset ID, path, filename, collection/root, and published datablock names agree and follow conventions | PASS | naming_and_scope and collection_contract; 17 objects, 5 meshes, 3 unique mesh datablocks. Sleeve/cap circular subdivisions increased; original object/data identity, all mesh coordinates/topology/face slots and nine anchors unchanged by0.1.2. |
| T02 | Canonical bounds and all category-critical measurements match specified meter values within stated tolerances; record actual readings | PASS | canonical_bounds, shaft_nominal_diameter_and_real_knurl, sleeve_dimensions_l/r. Numerical length 2.200000048 m; shaft 28 mm, sleeves 50 mm; hardware accuracy not claimed. |
| T03 | Axes, origin, root hierarchy, transforms, and rest/configuration state match the specified contract | PASS | floor_root_axes, hierarchy_transforms: meter units, +X shaft, +Y front, +Z up, floor root identity, positive determinant/unit scale. |
| T04 | Geometry, topology/deformation, reusable components, and adjustable limits match the spec | PASS | closed_nondegenerate_components and bar_component_clearances; actual knurl relief, separate hollow sleeves and caps, no physical bearings/flex. |
| T05 | Anchor/control names, local positions/orientations, motion behavior, and interface versions match declarations | PASS | metadata_anchors, load_anchor_frame_l/r, independent_sleeve_spin and placement/spin sweeps match proposed local interface. |
| T06 | Rig/skeleton/rest-pose compatibility and material slot/input order remain valid | PASS | steel_material_contract verifies eight stable prefix slots plus 128 appended soft-steel slots; rigid pivots need no human skeleton. No skin/rig compatibility claim. |
| T07 | Pinned Blender opens the source; dependencies resolve via relative paths from a fresh checkout with LFS content fetched, without hidden add-ons | PASS | PASS — fresh committed local clone,LFS fetch/checkout of5 native sources and fsck; all relative libraries resolve and55+35 checks rerun from checkout. No remote service test. |
| T08 | Compatible replacement works in named consumer/fixture cases; grips, support, pose, and clearance are checked across required configurations/motion | PASS | Scoped original plate 0.1.4 single/five/ten-per-sleeve fixtures: measured stack anchors, alignment/fit/capacity, zero BVH crossings, transform invariance and frame spin sweep. Alternative replacements/humans/override actions untested. |
| T09 | Existing consumers remain compatible, or an approved major-version/migration plan and regression evidence cover every affected consumer | PASS | No plate geometry, metadata or approved images changed; approved_plate_artifacts_untouched. The existing single/ten consumers were refreshed and pass, and the five-plate example was added with unchanged anchor/controller names; the capacity consumer adds instances only. |

## Reference renders and reproducibility

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| V01 | Front, side, three-quarter and relevant configurations/contact views exist, or alternate fixture coverage has explicit approval and rationale | PASS | Full_length +Y front, side +X end-on, three_quarter +X/+Y; shaft/end details, one-plate assembly, five-plate example and ten-plate diagnostic broadside/quarter/detail. |
| V02 | Render index paths resolve to retained review images under `previews/`; source and preset revisions/digests are recorded | PASS | Twelve retained PNGs, indexed in SPEC/metadata with source/settings hashes; assembly image lives with its fixture. |
| V03 | Recorded render settings include Blender/add-ons, renderer, camera transforms/projection/framing, resolution, palette/material versions, outline width, lighting, color management, background/alpha, samples, configuration/frame, and seed where relevant | PASS | Both updated render-settings.json records include actual camera/projection/roll, color values, flags, output, samples, versions and script hashes. Seed N/A deterministic Workbench. |
| V04 | Actual-size review confirms recognizable anatomy/equipment, consistent precise outlines, separated silhouettes, and readable contact points | PASS | All twelve images inspected at 1600×1000: recognizable silver bar, sleeve transitions/end recesses, readable actual knurl geometry in close-up and clean plate contacts. User appearance approval complete under A12. |
| V05 | No cast/contact shadows, ambient occlusion, or baked shadow textures appear | PASS | shadow_free checks plus inspected images: flat material values, no lamps/ground, shadows/cavity/AO/specular off; no baked textures. |
| V06 | Another checkout/session can reproduce the selected references using the documented versions, inputs, dependencies, preset, and ordered steps | PASS | Five standalone images reproduce exactly; assembly differs by at most 1/255 on fewer than 0.1% of channels. Exact observed coverage and comparison limit are recorded in validation-results.json. |
| V07 | Required delivery settings match A08 if exports are part of this asset's scope; no unrequested deliverables are claimed | N/A — review evidence only | No production export/delivery format asserted; A08 remains open. |

## Documentation and repository completion

| ID | Check | Result | Evidence / observed values / reason |
| --- | --- | --- | --- |
| R01 | Specification, metadata, dependencies, exceptions, decisions, reference index, and change history reflect the implementation | PASS | Specification, metadata, build/validation records, fixture references and proposal A11 reconciled. |
| R02 | Source and retained evidence are tracked with appropriate LFS rules; caches, backups, trials, and generated exports are ignored | PASS | PASS — sources tracked through LFS; retained PNGs/docs tracked; backups/caches/exports ignored; local fsck and fresh checkout pass. |
| R03 | All applicable results pass, limits are explicit, no release decisions remain open, and reviewer asset acceptance is recorded | PASS | User A12 production acceptance recorded for explicit internal illustration scope;55 existing machine checks PASS,35 plate checks PASS in disposable copy. Accepted limitations do not imply missing hardware/external-license tests. |

## Category-specific checks

| Case | Observed result | Status / evidence |
| --- | --- | --- |
| Existing geometry/interfaces | Shaft coordinates, nine anchor frames, all object/data identities preserved; sleeve/cap subdivisions only | PASS — refined_existing_asset_preserved |
| Smooth steel ends | 576 angular samples; uniform axial disk values; softer ramp and 0.48 stored roughness | PASS — circular_subdivision_and_soft_values + image inspection |
| Manufacturer dimensions | 2200 total / 1310 exposed / 415 sleeve / 50 sleeve diameter / 28 shaft mm | PASS — canonical_bounds, manufacturer_exposed_shaft_length, sleeve_dimensions_l/r |
| Original plate thickness | 33.020001 mm measured envelope matches 1.3 in manufacturer context | PASS — capacity_formula_and_next_plate_rejection |
| Capacity | 10 per sleeve with 50 mm collar, 5 mm tip, 1 mm flange and 0.5 mm interplate gaps; 11 exceeds by 9.22 mm | PASS — capacity_formula_and_next_plate_rejection |
| Full linked stack | 20 plate instances, zero local geometry; original source unchanged | PASS — capacity_linked_instances |
| All plate alignment/clearance | ~0.400 mm radial, ≥0.49988 mm interplate gap, ~79.3 mm outer space | PASS — all_capacity_plate_alignment_clearances |
| Symmetry and collisions | Mirror error <1µm; zero crossings in 80 broad-phase pairs; full-envelope separation | PASS — capacity_stack_symmetry_and_no_plate_intersections / capacity_plate_bar_surface_intersections |
| Independent spin and transformed placement | Source drivers and frame placement retain supported sampled behavior | PASS — independent_sleeve_spin, attachment_placement_transform_invariance, plate_spin_frame_sweep |
| Original plate / normative guides | All pre-edit hashes match | PASS — plate_and_shared_standards_preserved |
| Five-per-sleeve example |10 linked original instances, zero local mesh copies; aligned symmetric bore centers,0.5mm gap and191.90mm spare after collar/tip |PASS — five_plate_example_linking / five_plate_example_fit_and_symmetry |
| Five-example mesh crossings |40 broad-phase plate/bar pairs, zero crossings; positive envelopes rule out containment/interplate overlap |PASS — five_plate_example_intersections |
| Slight contrast only |factor1.18 about0.72; all mesh/face-slot hashes and object/anchor frames unchanged |PASS — appearance_only_geometry_unchanged / slight_steel_contrast_transform |
| Hardware mass/loads/fit, exact collar install, alternative assets and authored override actions | Unverified; expressly outside A12 supported illustration scope | N/A — excluded from this scoped release, not claimed tested |

## Outcome and changes since review

**55 automated PASS, zero FAIL**, plus twelve-view inspection. Five unloaded references and the loaded broadside reproduce exact decoded pixels. Other linked assembly views use the documented ≤1/255 channel and <0.1% changed-channel comparison bound; exact observed values in validation-results.json. No bound relaxed in 0.1.2.

Source and primary fixture hashes pinned; capacity fixture hash in metadata and capacity_linked_instances evidence. Plate and normative shared guides are unchanged. User acceptance is complete under A12. Applicable internal illustration gates pass, including fresh committed local Git/LFS checkout. External artwork licensing, hardware/dynamic tests and a general override-action pipeline are excluded limitations, not silently claimed complete. Future source/interface/material/camera/dependency changes invalidate affected evidence.

0.1.2 findings recommend no dimension correction. Compatibility-review.md was recorded first and remains checksum-pinned. All12 images inspected; approved plate and normative guides remain unchanged. Full committed checkout/LFS, real mass/fit/load ratings and user visual acceptance still unverified.

## A12 finalization outcome

User explicitly approves current0.1.2 for production-ready internal library illustration use. All55 barbell checks and35 existing plate checks were rerun successfully. Master/fixture/PNG hashes unchanged; approved plate and shared guides untouched. Ready is scoped to the documented Blender illustration workflow; mass/strength/manufacturing, actual collars/other assets/override actions and external artwork distribution are not claimed. Local committed-checkout QA PASS is recorded in finalization-qa.json, including5 native LFS objects,fsck and55+35 repeated checks.


## A14 current-origin validation —2026-10-15

Origin profile olympic_barbell approved; root/collection pivot [0.0, 0.0, 0.0364999994635582]m in authoring frame, root-local datum zero. Current expected/actual results in [origin audit](../../../../docs/audits/origin-audit-results.json). This section supersedes historical floor-root expectations for plate/barbell. Current geometry/materials and evaluated world frames checked against archived baseline; three linked fixture sources compensated. New functional-origin interface is1.0.0 for free weights; bench remains0.1.1. Frozen historical reports/approvals remain under docs/audits/origin_baseline. Four assembly PNGs refreshed only for micro anti-alias differences; see origin-render-refresh.json and current render regression. External consumers/rig overrides beyond recorded tests remain unverified. No redesign or new artwork grant.


A14 finalization2026-10-15: origin migration **approved and complete**. Current library audit297 PASS; world/geometry/material/render regression28 PASS; all three fixture stacking/clearance checks42 PASS;6 failure-injection and2 automatic placement cases PASS. No native geometry/source edit during finalization. Existing visual/release scope unchanged. Final evidence: docs/audits/origin-migration-record.json and origin-compatibility-validation.json; repository commit identifies this finalized snapshot.
