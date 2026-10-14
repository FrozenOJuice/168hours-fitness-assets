# Barbell / plate compatibility fixture

Version **0.1.2**, approved internal illustration reference / validated test fixtures, Codex, 2026-10-14. [Barbell spec](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/SPEC.md) defines verified dimensions, unchanged interface, algorithm, material treatment, packing formula and explicit assumptions. [Metadata](asset.json), [validation](validation.md), [settings](previews/render-settings.json).

## Source configurations

- [168h_template_barbell_plate_compatibility.blend](168h_template_barbell_plate_compatibility.blend): existing one original plate on each sleeve, linked barbell 0.1.2 + approved plate 0.1.4; source SHA256 `808cb6a15c6041908b1fd4d95cb8091c0a691a7288324f7fcbf0005417b901ec`. Three collection-instance empties and one camera, zero local meshes.
- [168h_template_barbell_plate_compatibility__capacity.blend](168h_template_barbell_plate_compatibility__capacity.blend): 10 original plate instances per sleeve, three reference cameras, same linked barbell/plate collections; source SHA256 `e6ff6f88ca0f59539dbfb77dc914f4a1777e8daaef770d10d889f0c5960621f1`. Twenty plate instances plus one bar instance, zero local mesh data. Default saved camera is the broadside loaded elevation.

Both use relative libraries and the original approved plate SHA256 `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`. This is a technical fixture, not an exercise scene or approved global scene preset. No collars/benches/humans/physics added. Collar space is reserved numerically, not modeled.

## Automatic placement and capacity

Unchanged outward load frames (+Y maps to ±X) align plate bore, subtract its rotated root-to-bore offset and measure actual plate stack_back/front plus all geometry. Actual floor-to-bore determines loaded centerline height. Single-plate helper `place_plate` retained; full stack adds each index's 0.5 mm display gap to its measured pitch. All transforms use positive scale. Left/right labels refer to subject sides.

Actual 415 mm sleeve and 33.020001 mm plate pitch, 50 mm sourced-length collar allowance, 5 mm tip, 1 mm flange and 0.5 mm interplate gaps yield 10 plates per side. Stack 334.700009 mm; outside sleeve space ~79.3 mm; collar+tip reserve consumes 55 mm, spare24.3 mm. Eleventh exceeds by9.22 mm. See [capacity calculation](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/capacity-calculation.json) for provenance, sensitivity and limits. Casting dimensions and collar-axis interpretation remain provisional physical assumptions; count is a digital packing result, not a rating.

## Validation and reproduction

55 aggregate machine checks plus twelve-view image review in the barbell [results](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/validation-results.json). Zero full-stack plate/bar surface crossings in80 broad-phase pairs; positive radial/axial envelopes also exclude containment and neighboring-plate overlap. All20 bore centers aligned and symmetric, radial clearance~0.400 mm, adjacent envelope gap≥0.49988 mm. Kinematic frame spin/compound-transform tests retained; no full physics or override-action authoring tested.

Run barbell read-only validator with Blender5.1.1. Refinement script opens existing barbell, then regenerates both linked fixture sources; no plate build/refinement script should run. Libraries remain relative and originals unchanged. Current on-disk files must be reopened to see updates in an already-open Blender session. Fresh committed local clone/LFS fetch/checkout and fsck PASS. User acceptance is complete under A12. Hardware fit/mass/load ratings, actual collar fitting and other asset replacements remain outside supported scope. Artwork terms unselected A07; code/docs MIT separately.

## Reference index

- [assembled_with_plates](previews/168h_template_barbell_plate_compatibility__assembled_with_plates__two_45lb_plates.png), two_45lb_plates.
- [loaded_side](previews/168h_template_barbell_plate_compatibility__loaded_side__10_per_sleeve.png), 10_45lb_plates_per_sleeve.
- [loaded_three_quarter](previews/168h_template_barbell_plate_compatibility__loaded_three_quarter__10_per_sleeve.png), 10_45lb_plates_per_sleeve.
- [loaded_sleeve_detail](previews/168h_template_barbell_plate_compatibility__loaded_sleeve_detail__10_per_sleeve.png), 10_45lb_plates_per_sleeve.

Loaded_side is the broadside +Y thickness/count view; it supplements canonical +X end-on side. Settings include each secondary source, camera matrix, palette and output. Exact/last-bit-bounded comparisons recorded per view. Rendering these fixtures never replaces approved plate reference images.

## Requested five-plate partial example —0.1.2

Preferred visual example: [five-per-sleeve source](168h_template_barbell_plate_compatibility__example.blend), ten linked original plates, three cameras, zero local meshes. Partial stack5×33.02+4×0.5=167.10mm. From415mm sleeve,1mm flange gap,50mm collar and5mm tip allowances leave191.90mm spare; no collar geometry modeled. Capacity stays10; original ten-per-sleeve file is diagnostic maximum, not the presentation load.

The slight steel contrast edit changes no bar/plate geometry or attachment frames. [Compatibility findings](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/compatibility-review.md) precede the edit; all manufacturer comparisons/approval limits stay documented there. Five-example relative links, alignment, symmetry, clearances and40 broad-phase mesh collision pairs pass in the shared validator. Main and both secondary source hashes are in asset.json and render settings.55 aggregate checks pass; user appearance/production approval is complete for internal illustration use under A12; physical hardware verification and external licensing remain limitations.

New retained example views:
- [example_side](previews/168h_template_barbell_plate_compatibility__example_side__5_per_sleeve.png), five per sleeve.
- [example_three_quarter](previews/168h_template_barbell_plate_compatibility__example_three_quarter__5_per_sleeve.png), five per sleeve.
- [example_sleeve_detail](previews/168h_template_barbell_plate_compatibility__example_sleeve_detail__5_per_sleeve.png), five per sleeve.

## A12 approved five-plate reference

User approved the barbell for internal library production,2026-10-14. The existing __example.blend is the checksum-pinned five-plates-per-sleeve reference, not a new model. Native files and PNGs are unchanged. Asset metadata now ready/approved for the scoped internal Blender illustration use; single/ten files remain validated compatibility diagnostics. See the barbell approval-record.json and finalization-qa.json for approval evidence and source/image digests. No external artwork license, hardware load rating or shared-standard promotion is implied.
