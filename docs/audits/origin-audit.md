# Equipment origin audit —2026-10-15

**Final results: 297 origin checks,28 migration/geometry/render checks,42 all-fixture stacking/clearance checks,6 failure-injection cases and2 automatic-placement cases passed (375 total); zero current failures. Migration approved and complete; bench remains review.**

A14 explicitly approved by the user: “Approve the root/pivot migration and fixture updates.” The requested standards and safe correction are implemented. No geometry redesign or visual-standard change.

| Asset | Before | Required and implemented functional origin | Result |
| --- | --- | --- | --- |
| 45lb Olympic plate | Floor root; collection offset0 | Exact bore center; root/collection authoring position(0,0,225mm), root-local bore(0,0,0) | Corrected, asset/interface1.0.0; geometry0.1.4 |
| 20kg Olympic barbell | Floor root; collection offset0 | Shaft-axis midpoint; root/collection authoring position(0,0,36.5mm), root-local axis(0,0,0) | Corrected, asset/interface1.0.0; geometry0.1.2 |
| Flat bench | Centered floor root/offset0 | Floor-level support-footprint center(0,0,0) | Already correct; source0.1.1 unchanged |

Existing authoring floor Z0 is preserved. Source authoring translations are intentional, root rotation is zero and scale positive1; collection offsets make the linked insertion/rotation pivot equal the functional root. Component origins remain their explicit construction/pivot frames and are listed/validated in metadata. Plate body origin is a retained static construction frame, not the insertion pivot. Opposite bar sleeve/cap use documented proper Zπ rotations to share data. No negative scale or anonymous attachment frames.

All three barbell/plate fixtures have compensated instance matrices, relative resolved links, unchanged evaluated world geometry, full anchor frames and fit. Source mesh coordinates/topology/materials are unchanged. Independent sleeve control sweeps and offset-aware automatic placement pass. Current expected/actual evidence: [origin-audit-results.json](origin-audit-results.json), [origin-migration-validation.json](origin-migration-validation.json), [origin-placement-helper-tests.json](origin-placement-helper-tests.json), [origin-validator-tests.json](origin-validator-tests.json). Original35 plate/55 barbell-fixture/72 bench checks rerun on disposable baseline, summarized in [legacy-validation-summary.json](legacy-validation-summary.json). Historical full validator assumptions are not silently applied to the new interfaces.

Four assembly references exceeded historical strict reproduction tolerance after float/AA rounding; refreshed from migrated saved scenes. Old differences and exact predecessor images remain in [origin-render-pre-refresh.json](origin-render-pre-refresh.json), [origin-render-refresh.json](origin-render-refresh.json) and [origin_baseline](origin_baseline/ARCHIVE.md). Maximum delta3/255 on0.002328125% channels; standalone images reproduce exactly. Current references pass the original tolerances after refresh; no tolerance/global style relaxed. Original A10/A12 approval records now pin exact archived artifacts. The migration authorization/successor source pins live in [origin-migration-record.json](origin-migration-record.json).

## Reproduction

Blender5.1.1, no add-ons, from repository root:

- `Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_asset_origins.py`
- `Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_origin_migration.py`
- `Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/test_asset_origin_validation.py`

Existing plate/barbell/bench validator names invoke the same current pipeline by default; add `-- --origins` for only roots/anchors/transforms, with optional `--manifest assets/.../asset.json`. Future profiles are data-driven in docs/equipment-origin-rules.json; unknown profiles fail. Noncircular bores/new datum strategies need explicit implementation and tests; broad racks/machines need actual category geometry before numerical compatibility claims.

## Remaining limitations

External consumers outside this repository were not inspected or modified. They must select1.0.0 deliberately and compensate old instance matrices using the documented delta. No authored rig override actions, human fit, physical load/mass certification or new artwork licensing is claimed. Plate remains visually approved/review for engineering release; barbell retains approved internal illustration scope with A14 origin migration; bench remains review. A14 is approved and complete; this snapshot is committed in repository finalization.

## Current native files and delivery bundles

- [/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/benches/168h_equipment_flat_bench/168h_equipment_flat_bench.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/benches/168h_equipment_flat_bench/168h_equipment_flat_bench.blend)
- [/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/168h_equipment_olympic_barbell_20kg.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/168h_equipment_olympic_barbell_20kg.blend)
- [/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/168h_equipment_olympic_plate_45lb_cast_iron.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/168h_equipment_olympic_plate_45lb_cast_iron.blend)
- [/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility.blend)
- [/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility__capacity.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility__capacity.blend)
- [/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility__example.blend](/Users/joeldehoog/Developer/168hours-fitness-assets/scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility__example.blend)

- Standalone render bundle: `/Users/joeldehoog/Developer/168hours-fitness-assets/exports/illustrations/origin_audit_unassembled_renders.zip`
- Linked fixture render bundle: `/Users/joeldehoog/Developer/168hours-fitness-assets/exports/illustrations/origin_audit_assembled_renders.zip`


## Finalization validation

[Numeric compatibility report](origin-compatibility-validation.json): one/five/ten plates per sleeve remain aligned, symmetric and clear. Measured radial clearance~0.400mm, interplate gap~0.500mm, flange gap~1mm. With50mm collar and5mm tip reserves, ten-plate configuration retains~24.3mm; five-plate example~191.9mm. Original geometry/topology/materials/world anchors preserved within1e-6m; all21 retained reference views pass recorded comparisons. Failure-injection tests detect future incorrect pivots, frames, scales, rotations and unknown profiles. Default per-asset validation entry points enforce origin, preserved-baseline and numeric compatibility checks. No global tolerance/visual standards changed during finalization.
