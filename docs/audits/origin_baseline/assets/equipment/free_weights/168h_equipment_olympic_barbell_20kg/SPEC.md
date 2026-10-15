# Asset specification: 168h_equipment_olympic_barbell_20kg

## Identity and status

Version **0.1.2**, equipment/free_weights, **approved / production-ready for internal168Hours Fitness Blender illustration use**, Codex for 168Hours Fitness, 2026-10-14. User requested renewed manufacturer/plate compatibility review, a slight steel contrast increase and a 4–5-plate example; selected five per sleeve. Findings and recommendations were documented before the appearance-only edit. No dimension change was needed or applied. User production approval is recorded under A12; this does not change shared standards. Geometry version0.1.2 remains unchanged. [Source](168h_equipment_olympic_barbell_20kg.blend), [metadata](asset.json), [validation](validation.md), [measured results](validation-results.json).

Reviewed [AGENTS](../../../../AGENTS.md), [global style](../../../../docs/visual-style.md), [common conventions](../../../../docs/asset-conventions.md), [category standards](../../../../docs/category-standards.md), [workflow](../../../../docs/asset-workflow.md), [decisions](../../../../docs/decisions.md), [licensing](../../../../docs/licensing.md), and approved plate 0.1.4 spec/metadata/validation/approval. A10 supplies the clean illustrated equipment cue; its geometry/palette remain specific to cast iron. A11 remains the local barbell/interface proposal. Global A01/A03/A04/A05/A06/A07/A08 are open. Pre-build [standards snapshot](standards-snapshot.json); current pre-edit plan and protected hashes in [refinement-plan.json](refinement-plan.json). Specification plan existed before the refinement; source/fixture/script predecessor copies retained locally under ignored exports/models/barbell_review_history/0.1.0.

## Verified dimensions and proportions

Values below are manufacturer-supported **design dimensions verified numerically in the model**, not physical measurements, manufacturing tolerances or competition certification. Numerical comparison tolerance 0.000001 m. Model dimensions were already proportionate: no sleeve shortening, bar rescaling or forced capacity change was appropriate.

| Measurement | Published design value | Implemented / method |
| --- | --- | --- |
| Overall length | 2200 mm | 2200.000048 mm mesh bounds |
| Exposed shaft between inner flange faces | 1310 mm | 1310.000005 mm; derived from total − 2×(415+30), matches standard Olympic shaft context |
| Shaft maximum diameter | 28 mm | 28 mm maximum vertex radius; knurl cut below envelope |
| Loadable sleeve each | 415 mm | 415.000016 mm between load/end anchors, profile endpoints verified |
| Sleeve maximum diameter | 50 mm | 50 mm geometric envelope, independent of shallow grooves |
| Integrated flange width | 30 mm | inner face X±655 mm → load face X±685 mm |
| Flange diameter | 73 mm | numerical 72.999999 mm; retained historical-IWF minimum reference choice, not all manufacturers' exact flange size |
| Canonical bounds X/Y/Z | 2200 / 73 / 73 mm | measured 2200.000048 / 72.999999 / 72.999999 mm |
| Existing plate axial envelope | 33.02 mm / 1.3 in context | measured 33.020001 mm from all linked geometry and stack anchors |

Sources rechecked 2026-10-14: [Eleiko Performance Weightlifting Bar sheet](https://media.eleiko.com/admin/download-product-sheet.aspx?articlecode=3070100&language=en-us) lists 20 kg, 2200 mm overall, 415 mm sleeves, 50 mm diameter and 30 mm flange width. [Eleiko Olympic shaft context](https://eleiko.com/en/stories/multi-purpose-bars) identifies 1310 mm as standard Olympic exposed shaft length; 1310 is also derived directly from the cited 20 kg bar's dimensions. [Rogue Olympic Weightlifting Bar](https://www.roguefitness.com/rogue-olympic-weightlifting-bar-stainless-steel) corroborates a 28 mm 20 kg shaft, approximately 2200 mm overall and approximately 414 mm sleeves. [Rogue cast-iron plates](https://www.roguefitness.com/rogue-olympic-plates) lists 45 lb thickness 1.3 in = 33.02 mm. These are dimensional references, not imported CAD/artwork or a manufacturer replica. The approved plate's 450 mm diameter is still its provisional original design, not Rogue's 17.5 in diameter.

Distinguish **1310 mm exposed shaft** from the hidden internal axle: existing shaft mesh extends 2188 mm between end-cap pockets, mostly inside hollow sleeves. The hidden axle length is not the grip section length. Nominal 20 kg identity remains unverified by density/mass simulation; no strength or load rating is claimed.

## Calculated plate capacity including collar space

[Calculation inputs/results](capacity-calculation.json) derive count from actual linked plate envelope and actual sleeve anchor distance. **10 existing 45 lb plates per sleeve** fit the documented setup; the sleeve dimensions are retained because they match real full-size bars. Thin cast-iron plates naturally allow more plates than thick bumpers.

| Input / result per sleeve | Value | Evidence / state |
| --- | --- | --- |
| Loadable length L | 415 mm | sourced bar dimension; measured digital anchors |
| Plate envelope t | 33.020001 mm | existing linked geometry; published 33.02 mm context, physical casting still provisional |
| Collar axial allowance C | 50 mm | [Eleiko Lock-Jaw Pro 2 sheet](https://media.eleiko.com/admin/download-product-sheet.aspx?articlecode=3060925&language=en-us) lists 50 mm length; interpreting length as sleeve occupancy is an explicit assumption |
| Tip margin E | 5 mm | local clearance assumption, includes staying away from end chamfer; not manufacturer tolerance |
| Initial flange gap F | 1 mm | local visual/contact clearance assumption |
| Interplate envelope gap g | 0.5 mm | local display clearance, not claimed compressed hardware spacing |
| Maximum n | 10 | floor((L−C−E−F+g)/(t+g)) |
| Ten-plate stack | 334.700009 mm | 10t + 9g |
| Used with flange/collar/tip allowance | 390.700009 mm | F + stack + C + E |
| Spare after all allowances | 24.300007 mm | L − used |
| Eleventh plate | exceeds available length by 9.219994 mm | same inputs, n=11 |

The model leaves approximately **79.3 mm** of sleeve outside the ten-plate stack; 50 mm is reserved for a collar, 5 mm for the end margin, with approximately 24.3 mm remaining. No collar geometry is created or shown. Close-packed plates (g=0) with the same collar/margins still yield 10. Hypothetical 38 mm collar occupancy permits 11; hypothetical 70 mm occupancy permits 10. Those sensitivity values are not verified collar products. Without the 5 mm tip margin and without gaps, 11 plates plus a 50 mm collar leave only ~0.78 mm to the nominal tip, within the modeled 1.5 mm end chamfer, so that is not the reviewed usable setup. Capacity depends on actual casting, collar and clearance; **10 is this documented packing result, not a universal plate count or safe load rating**.

## Geometry refinement and modular interface

Canonical +X shaft, +Y front, +Z up; root at floor-footprint (0,0,0), identity, centerline Z0.0365 m. Subject-left +X (`l`), right −X (`r`), camera-independent. Collection `168h_equipment_olympic_barbell_20kg` retains `__geo`, `__rig`, `__anchors`, root `__root`, all 17 existing objects and three shared mesh datablocks. Five mesh objects: continuous shaft, two independent hollow sleeves with integrated shoulders, two recessed unbranded caps. No removable collars or bearings/flex/physics added. Both sleeves share one mesh, caps share another; right components use proper 180° Z rotation with positive scale.

The existing sleeve/cap circumferential edges were locally subdivided 3× (192→576 angular segments) and projected back to their original radial profiles. No profile endpoints, radii, shaft geometry or attachment frames were rescaled. Shaft remains 420,672 vertices / 420,482 faces, shared sleeve now 145,728 vertices/faces, shared cap 2,306 vertices / 2,112 faces. All three closed components have no nonmanifold edges, loose vertices or degenerate faces. Existing object/mesh-data identity during the edit, unchanged shaft coordinates and all nine anchor frames are recorded in [refinement record](refinement-record.json). High-detail master; no LOD created.

Actual diamond knurl geometry, pitch 1.832596 mm and 0.160 mm maximum radial recess, is preserved. Center knurl ±60 mm; side knurl ±210→±655 mm, smooth 5 mm markings ±455→±460 mm. Sleeve grooves remain 0.080 mm deep at 5 mm pitch. These detailing values and simplified 0.300 mm internal axle clearance are provisional original design, not manufacturer-exact machining specifications.

Interface **`olympic_barbell_load@0.1.0` unchanged**, locally tested/proposed, not globally ratified. Published anchor object suffix `__anchor_<name>`:

| Anchor | Root-local position (m) | Frame at zero spin |
| --- | --- | --- |
| grip_center | (0,0,0.0365) | +Y forward, +Z up |
| grip_l / grip_r | (±0.350,0,0.0365) | +Y forward, +Z up; human fit untested |
| axis_center | (0,0,0.0365) | local +Y points +X, +Z up |
| load_l / load_r | (±0.685,0,0.0365) | local +Y points outward ±X, +Z up |
| sleeve_end_l / sleeve_end_r | (±1.100,0,0.0365) | local +Y points outward ±X, +Z up |
| floor_contact | (0,0,0) | +Y forward, +Z up |

Independent `__control_sleeve_l/r` pivots at (±0.670,0,0.0365) retain X rotation drivers from root `sleeve_l_angle_deg/r`, default 0, library-overridable. Global +X angle convention on both sides; periodic. Linked collection instances are static; future authored animation needs hierarchy overrides and consumer plate updates from evaluated load frames. Tested independent controls and kinematic plate frames through 0/45/90/180/270/360°, not a complete override-action workflow.

Automatic plate placement maps linked plate +Y onto outward load-frame +Y, compensates its floor-root/bore offset, uses measured back/front envelopes and each index's measured pitch plus selected interplate gap. Actual plate floor-to-bore sets bar height. No plate copying or edits. One-plate and full-capacity [fixture sources](../../../../scenes/templates/168h_template_barbell_plate_compatibility/SPEC.md) retain relative links; full stack has 20 collection instances sharing original plate data and no local meshes. Instance placement remains symmetric under compound whole-assembly transforms. Version/revalidate future anchor/dimension/slot/path breaks; no consumer break introduced here.

## Materials and illustration

Local provisional `barbell_review_flat@0.1.2`, Blender 5.1.1 Workbench FLAT, native silhouette outlines, white background, Standard/None, 1600×1000 RGBA PNG, 32 AA. No lights, ground, cast/contact shadows, cavity/AO, baked textures or photoreal reflections. Softer steel appearance comes from a broad low-contrast radial value curve with 128 finely stepped swatches. Axial end faces now use uniform values so polar material segmentation does not appear as cuts or facets. Knurl facet contrast is restrained but actual relief remains readable in close-up.

Original slots **0..7 remain in order**: seven silver equipment_frame variants and equipment_grip mark. Slots **8..135** append 128 soft-steel equipment_frame variants (current sRGB ramp from roughly [0.5194,0.54064,0.5607] to [0.8734,0.89464,0.9147], applying 1.18 contrast about0.72 to the previous ramp); current faces use this ramp and grip mark slot 7. Material datablock names/prefixes are preserved; no shared material extracted/changed. Principled nodes store metallic 0.85, roughness **0.48**, but Workbench renders display swatches, not the shader nodes. The broad illustrated highlight is a material-value treatment, not a shadow or physical reflection. Exact settings in [render-settings.json](previews/render-settings.json). No global palette/renderer/interface standard promotion.

## Dependencies and licensing

Master has no external runtime dependencies/add-ons/textures/fonts. Test files link barbell 0.1.2 and approved plate 0.1.4 by relative paths with hashes. Plate source SHA256 `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2` and all approved plate artifacts remain unchanged. Barbell source SHA256 `9c6c8c83666553c0f2d49e8a4547aba6b8eaa191d493940e8d16f8b319f9cfcb`; one-plate fixture `808cb6a15c6041908b1fd4d95cb8091c0a691a7288324f7fcbf0005417b901ec`; capacity fixture `e6ff6f88ca0f59539dbfb77dc914f4a1777e8daaef770d10d889f0c5960621f1`.

Original artwork authored for 168Hours Fitness. Artwork license null/unselected A07; code/documentation MIT separately. No manufacturer artwork/branding/CAD imported. Hardware fit, mass, loading/dynamic/strength tests, human/exercise consumers and alternative asset replacement remain unverified. Fresh local committed Git/LFS checkout is verified; global production defaults and remote LFS upload/capacity remain outside the scoped approval; visually accepted proportions are not production certification.

## Reproduction and review workflow

Use isolated Blender5.1.1, no add-ons, and run from repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/blender/validate_olympic_barbell_20kg.py
```

The validator opens current saved barbell, single-plate, five-plate and capacity native sources read-only, checks geometry/interfaces/fit/collisions and reproduces all references into temporary folders. It never saves sources or edits the approved plate. Five unloaded views require exact decoded pixels; assembly views use the existing ≤1/255 and<0.1% changed-channel comparison limit. Per-view observations are in validation-results.json.

The current appearance update was implemented with scripts/blender/contrast_olympic_barbell_20kg.py against the preserved0.1.1 source. It changes existing material swatches only and creates a five-plate scene from the first five linked instances on each side. contrast-record.json hashes all mesh coordinates/topology/face slots and object frames before/after. Treat creation/refinement/contrast scripts as versioned mutation provenance, not commands to rerun casually over the master. For deterministic reconstruction, start from the recorded0.1.1 predecessor archive; do not cumulatively apply contrast. Current render settings and exact colors are recorded. Any authorized resave/regeneration requires refreshed hashes and validation. Source is on disk; the user's already-open Blender session was not reloaded.

## Reference render index

Twelve current review renders, all manually inspected. The main new example has five plates per sleeve; the ten-plate set remains diagnostic maximum evidence. Front is full_length (+Y); canonical side is +X end-on. Additional **loaded_side** is a +Y broadside elevation so all plate thicknesses can be counted; it does not silently redefine canonical side axes. Cameras/settings/source hashes recorded per view, including secondary capacity file. Seed N/A to deterministic Workbench.

| View | Image | Source / configuration |
| --- | --- | --- |
| full_length | [full_length](previews/168h_equipment_olympic_barbell_20kg__full_length__unloaded.png) | unloaded |
| side | [side](previews/168h_equipment_olympic_barbell_20kg__side__unloaded.png) | unloaded |
| three_quarter | [three_quarter](previews/168h_equipment_olympic_barbell_20kg__three_quarter__unloaded.png) | unloaded |
| detail | [detail](previews/168h_equipment_olympic_barbell_20kg__detail__unloaded.png) | unloaded |
| end_detail | [end_detail](previews/168h_equipment_olympic_barbell_20kg__end_detail__unloaded.png) | unloaded |
| assembled_with_plates | [assembled_with_plates](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__assembled_with_plates__two_45lb_plates.png) | two_45lb_plates |
| loaded_side | [loaded_side](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__loaded_side__10_per_sleeve.png) | 10_45lb_plates_per_sleeve |
| loaded_three_quarter | [loaded_three_quarter](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__loaded_three_quarter__10_per_sleeve.png) | 10_45lb_plates_per_sleeve |
| loaded_sleeve_detail | [loaded_sleeve_detail](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__loaded_sleeve_detail__10_per_sleeve.png) | 10_45lb_plates_per_sleeve |
| example_side | [example_side](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__example_side__5_per_sleeve.png) | 5_45lb_plates_per_sleeve |
| example_three_quarter | [example_three_quarter](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__example_three_quarter__5_per_sleeve.png) | 5_45lb_plates_per_sleeve |
| example_sleeve_detail | [example_sleeve_detail](../../../../scenes/templates/168h_template_barbell_plate_compatibility/previews/168h_template_barbell_plate_compatibility__example_sleeve_detail__5_per_sleeve.png) | 5_45lb_plates_per_sleeve |

Unloaded full-length/three-quarter scale 2.50 m, side 0.12 m, shaft detail 0.38 m, end detail 0.30 m. Assembly and full-capacity elevation/three-quarter 2.50 m; loaded sleeve detail 0.68 m. Full camera matrices, roll, clipping and settings in the two render-settings.json files. Five standalone images and loaded_side reproduce exact decoded pixels; other assembly images pass the previously documented 1/255 per-channel, <0.1% changed-channel comparison limit. Actual deltas/coverage recorded in validation-results.json; bit-exact output is not claimed for all linked assembly views.

## Validation, assumptions and approval

**55 automated PASS, zero FAIL**, plus all twelve actual-size image inspections. Numerical single/five/ten-per-sleeve fit verified: ~0.400 mm minimum radial sleeve clearance, symmetric placement, ~1 mm flange gap, ≥0.49988 mm measured adjacent-plate envelope separation, ≥79.300 mm outside stack for collar/tip space. Zero mesh surface crossings in 80 full-stack broad-phase pairs; positive radial/axial envelopes exclude containment and interplate overlap. No shared-standard or approved plate changes.

A12 approves the refined steel/knurl contrast, original28mm/center-knurl variant and current local material/attachment/controller implementation for this asset. Collar type/axial occupancy, 5 mm tip and 0.5 mm display-gap assumptions are explicit and must be rechecked against the actual future collar/casting. Global production decisions, artwork terms and physical verification remain open. Current production approval A12 accepts the recorded asset-local settings/assumptions for internal illustration use; limitations below remain explicit. Future source/dependency/geometry/material/camera changes invalidate affected results.

## Change history

| Date / version | Change | Compatibility / evidence |
| --- | --- | --- |
| 2026-10-14 / 0.1.0 | First barbell review prototype and single-plate fixture | 34 prior checks; archived locally, superseded by 0.1.1 |
| 2026-10-14 / 0.1.1 plan | Recorded user refinement request, manufacturer comparisons, collar/packing inputs before editing | refinement-plan.json and local predecessor archive |
| 2026-10-14 / 0.1.1 | Refined existing circular edges and steel values; unchanged verified dimensions/shaft/anchors; added capacity fixtures and renders | 46 checks PASS, nine views; user visual approval pending |

## 0.1.2 compatibility review and requested example

[Manufacturer findings and recommendations](compatibility-review.md) were written before changing the source; their digest is pinned in contrast-example-plan.json. The report recommends no dimension changes:415mm sleeves match real manufacturer specs and33.02mm plate thickness matches traditional cast iron. Approved450mm plate remains5.5mm larger than the cited444.5mm product, but this original asset is not a manufacturer replica. Do not rescale that approved asset without explicit variation approval and anchor migration. This difference does not cause the capacity result.

Bar geometry, topology, material slot order/face assignments, transforms, anchors and controllers are unchanged from0.1.1. Only128 existing steel swatches have slightly greater contrast around sRGB0.72: factor1.18. Broad smooth shading, metallic0.85/roughness0.48, knurl geometry, no-shadow/AO treatment and outline method are preserved. [Contrast record](contrast-record.json) is authoritative for current appearance; the0.1.1 refinement record remains geometry provenance.

The new [168h_template_barbell_plate_compatibility__example.blend](../../../../scenes/templates/168h_template_barbell_plate_compatibility/168h_template_barbell_plate_compatibility__example.blend) links five original45lb plates per sleeve, zero local meshes. Stack is167.10mm including four0.5mm gaps; with1mm flange,50mm collar and5mm tip reserve, used223.10mm, spare191.90mm. Sleeve outside stack is246.90mm. No collar geometry is added. This is an illustrative partial load, not a claimed typical load, new maximum or strength rating. Capacity remains10 under the existing explicit allowances; ten images are labeled diagnostic maximum.

All55 machine checks pass, including example symmetry, ten-instance data reuse, 40 example plate/bar broad-phase mesh pairs with zero crossings, all geometry hashes and protected plate/shared guides. Twelve views inspected; raw reproduction comparisons retained. Current example SHA256 `a10ad55bf52c1873fe5ccd8a2b73ef100382276cf7aa9ebd7c580019cbb9b0f7`. Native bar `9c6c8c83666553c0f2d49e8a4547aba6b8eaa191d493940e8d16f8b319f9cfcb`; single fixture `808cb6a15c6041908b1fd4d95cb8091c0a691a7288324f7fcbf0005417b901ec`; capacity `e6ff6f88ca0f59539dbfb77dc914f4a1777e8daaef770d10d889f0c5960621f1`. Current source and five-plate reference are approved and ready under A12 for the documented internal illustration scope; external artwork terms/global defaults/hardware verification remain separate limitations.

| Date / version | Change | Evidence |
| --- | --- | --- |
| 2026-10-14 /0.1.2 | Manufacturer/plate findings first; no dimensional correction; slight steel swatch contrast, five-plate example |55 PASS, no FAIL;12 references; approved plate unchanged |

## A12 production approval —2026-10-14

The user explicitly instructed: “Finalize and approve the20kg Olympic barbell as a production-ready asset for the168Hours Fitness library.” Current metadata status is **ready**, approval **approved**, geometry version **0.1.2 unchanged**. [approval-record.json](approval-record.json) pins the exact native bar, all three fixtures, twelve reference images and captured preset files. Existing internal review labels in unchanged .blend sources are historical; the external approval record is authoritative. No geometry, materials, transforms, native sources, PNG pixels or shared standards were changed for finalization.

Production scope is reusable **Blender illustration content in the internal168Hours Fitness library**, using captured Blender5.1.1/Workbench settings, current geometry/materials and `olympic_barbell_load@0.1.0` attachment/controller contract. A12 approves these choices for this asset and the saved five-plates-per-sleeve presentation reference. Global baselines are not promoted. The existing user instruction takes precedence over earlier prototype-only status. This approval is not a manufacturing, physical mass/strength/load-rating certification or an external artwork redistribution license. Artwork remains separate from MIT code/docs; no external artwork reuse grant is inferred. Existing global A07 remains unchanged.

Manufacturer dimensions and URLs remain in the verified dimension table and compatibility-review.md. The accepted packing result is10 plates/sleeve with50mm collar allowance,5mm tip margin,1mm flange gap and0.5mm interplate gaps:24.3mm spare after all allowances. Approved five-plate example uses167.1mm stack and leaves191.9mm spare after all reserves. Minimum bore/sleeve radial clearance~0.400mm, symmetric alignment and zero intersections verified in named single/five/ten fixtures. Actual collar orientation/occupancy and casting tolerances must be checked for a different consumer; the current assumptions are accepted for these illustration configurations.

[Finalization QA](finalization-qa.json): all55 existing barbell checks rerun PASS; all35 existing plate checks rerun PASS in a disposable copy so its frozen report remains unchanged. Names, normalized/positive transforms, roots, nine frames, independent rotation controls, relative links, plate reuse, digital dimensions, clearance, symmetry, topology and reference reproduction are confirmed. No claim of humans/alternative replacements, physics or authored override-action testing is added. Fresh committed local clone/LFS fetch/checkout and fsck pass, with55+35 checks repeated from the checkout; no remote push/upload requested.

All accepted artifacts are frozen for this reference. Future edits need explicit authorization, retained predecessor and new validation/approval evidence. Historical findings remain history; unresolved external licensing/global/hardware topics do not reopen the user's current scoped internal-production approval.
