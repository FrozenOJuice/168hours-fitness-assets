# Asset specification: 168h_equipment_barbell_stands

Source: [168h_equipment_barbell_stands.blend](168h_equipment_barbell_stands.blend). Metadata: [asset.json](asset.json). Checklist: [validation.md](validation.md).

## Identity and approval

Version0.1.1, **approved internal illustration asset**, equipment/racks. Original pair of separate height-adjustable standalone barbell stands; no connecting crossbar, storage pegs, collars, safety arms, humans or exercise animation. Creation and a technical linked review assembly explicitly authorized2026-10-15. Appearance, local interface and original detail choices are accepted for the internal illustration scope recorded in approval-record.json. Shared standards unchanged. Read AGENTS, README, global style, common/category contracts, workflow, decision register/licensing and approved plate/barbell/bench specifications before modeling. Exact approved artifact and normative guide hashes retained in prebuild-record.json; protect all approved geometry/materials/renders.

## Sources and dimensions

Manufacturer context: [Vulcan Olympic Adjustable Squat Stands](https://www.vulcanstrength.com/Adjustable-Squat-Stands-Olympic-p/v-oly1.htm), consulted2026-10-15. Published per-stand footprint24.5×23.5in (622.3×596.9mm), adjustable upright up to70in (1778mm),5/8in pin and protected hooks. Original illustration inspired by this construction type, not a replica or load-rated product. [Rogue independent S-4](https://www.roguefitness.com/rogue-s-4-squat-stand-2) corroborates H-bases, reinforced bolted connections and lined J-cups; its fixed-height upright is not the selected mechanism.

| Dimension | Meters | Evidence/state |
| --- | --- | --- |
| Per-stand base X/Y | .5969/.6223 | Published Vulcan pair of footprint dimensions; assigning depth24.5in is an original orientation choice |
| Maximum telescoping tube top | 1.778 | Manufacturer-supported70in context, excludes hook backplate extension |
| Default tube top / overall height | 1.028 /1.048 | Provisional bench setup, measured digital geometry |
| Pair overall X/Y/Z | 1.6969/.6223/1.048 | Derived from1100mm center spacing and footprint; provisional spacing |
| Outer upright | 80×80mm, Z70–970mm, wall4mm | Original provisional section/length |
| Inner upright | 60×60mm, length950mm, wall3mm, bottom78mm at rest | Original provisional;6mm per-side internal tube clearance centered by a61mm guide opening,142mm overlap at maximum extension |
| Adjustment | index0–15,50mm pitch | Local review proposal, rest/min support928mm, max1678mm; integer controls independently per side |
| Pin | 15.875mm | Published5/8in context; holes17mm local clearance |
| Hook | width60mm, lined saddle Y50–202mm; retaining lip toY222mm, support plane Z928mm at rest | Original provisional20mm-radius protected cradle, open+Y lead-in/lip;28mm shaft centerZ942mm |

No inference of real mass, gauge, steel strength, load rating or manufacturing compliance. Source units meters, tolerance1e-6m for digital checks only. Base contact patches and pair root intentionally centered at floorZ0. +Zup/+Yfront(open hook)/+Xsubject-left. Pair root and collection pivot(0,0,0); each independent stand controller floor at(+/-.55,0,0). Mesh origins are documented construction frames, never arbitrary geometry-centering. All mesh scale1/rotation0; mirrored components share data without negative transforms. Source pair remains modular with separate left/right fixed base and sliding upper controller.

## Geometry, reuse and controls

H-base: two longitudinal steel rails, transverse lower tie, four rubber floor pads per stand, reinforced triangular gussets and bolt heads. Hollow outer/inner tubes, real through holes and removable support-pin geometry with grip/retainer details, dark polymer telescope guide at collar. Hook has a concentric curved cradle, ramped lead-in, protected upturned lip/back and a connected mounting backplate; exact details below. Intended welded joints, pin-through-holes and guide/telescope engagement are documented internal contacts; no unrelated asset penetrations permitted. Symmetric parts reuse mesh data, whole opposite stand shares all matching data. Geometry must have closed outward components, no loose edges or degenerate faces.

Root custom integer properties height_index_l/r0–15 drive upper controller Z=index*.05. Sliding geometry and support/axis anchors follow; fixed outer pin atZ900mm engages one of16 real holes in the inner tube at every detent. UI ranges document limits; validation tests all detents, minimum/maximum extension and mixed left/right state. A racked bar requires equal heights. No physical motion/safety simulation. Component source origins recorded in manifest; native driver graph is local and requires no addon. Library overrides/actions are not yet authored/tested.

## Interfaces and replacement

Asset-local proposal independent_barbell_support@0.1.0. Stable top collection/root and __geo/__anchors children. Anchors: floor_contact at pair root; floor_l/r at each stand's floor controller; bar_support_l/r at(X+/-550,Y140,Z928)mm; bar_axis_l/r at sameXY/Z942mm for the existing28mm bar. All rest frames+Yforward/+Zup. Support and axis anchors move with upper controller. Axis anchors are radius-specific convenience; future bars align using support surface plus their measured radius. No other bar/rack/human substitutions certified.

Review fixture links this pair plus approved bench0.1.2 and barbell1.0.0. Stands rotated180° so hooks face toward bench foot end(-Y), pair floor centerY580mm; bar centerY440mm and Z942mm. Bench remains at floor origin, head+Y; bar Xshaft. Pair support centers1100mm apart, each hook outer edge580mm from bar center vs exposed shaft end655mm,75mm axial flange clearance. Inner base edge251.55mm vs bench overall halfwidth177.8mm leaves73.75mm horizontal clearance. Bar axis484.8mm above pad; racked setup only, no anatomical ergonomic claim. Verify actual saved evaluated triangles with BVH plus numeric clearances. Source-approved assets linked with relative paths and original data, never appended/modified. No plates loaded in this scope.

## Materials and rendering

Reuse approved equipment numerical cues locally: charcoal steel363A40 body/454A51 top/2A2D32 side; grip/liner17191D/24272C; restrained brighter hardware from existing steel family. No branding. Existing Blender5.1.1/WorkbenchFLAT helper,1600×1000RGBA8,32AA,Standard/None, whitebackground/native dark outlines, no lights/ground/specular/shadows/AO/cavity. This is asset-local preset stands_review_flat@0.1.0, not shared default. Camera records accompany the retained references. Standalone front+Y,side+X,three-quarter+X/+Y, plus maximum-height detail as useful; separate linked assembly views for fit and contact.

## Licensing, dependencies and reproduction

Original procedural artwork, no imported meshes/images/textures/fonts/addons. No external artwork grant selected; code/docs MIT separately. Source asset has no external geometry dependency; assembly dependencies pinned by sourceSHA and version. Do not rerun builders over approved equipment. From repo root using Blender5.1.1 --background --factory-startup --python-exit-code 1: initial build scripts are scripts/blender/build_barbell_stands.py and build_stands_review_assembly.py and refuse to overwrite existing files. Use them only in a disposable build with new outputs absent. For saved-source review, run scripts/blender/render_barbell_stands.py and validate_barbell_stands.py. Native roots/anchors/height controls saved; all outputs validated from reopened source. Reference reproduction uses renderer -- --reproduce into ignored exports, never resaves master. Approved equipment, fixtures, AGENTS and normative guides remain hash protected. A focused local commit is authorized by finalization; LFS/ignore attributes checked. No remote push requested.

## References and acceptance

Initial pre-build state recorded in prebuild-record.json; completed evidence follows. Initial review approval was pending; the authoritative final approval section below now records acceptance. Future visual/interface changes require authorized revision and revalidation. No new shared category, origin rule or software standard established.


## Completed in-place refinement0.1.1 —2026-10-15

Historical refinement-stage status was **review, not approved**; superseded by final approval below. [Pre-edit plan](refinement-plan.json), [implementation/preservation record](refinement-record.json), and [manufacturer evidence](manufacturer-reference.md) distinguish facts from unpublished original design choices. Exact0.1.0 source, metadata, QA and references retained under history/0.1.0; earlier results there are historical. The initial builder is not rerun.

All76 existing objects,64 mesh objects/32 shared mesh data, original component origins/matrices,7 anchor frames and owners, root/collection pivot, independent16detent controllers and material slot order are retained.26 objects use13 refined shared meshes; the remaining38 meshes have exact prior coordinates/topology. Existing materials/palette/shader setup unchanged. Counterpart geometry remains shared with positive normalized transforms.

### Hook and adjustment construction

The actual raised steel/liner cradle uses concentric20/26/36mm radii:6mm protective polymer and10mm steel radial thickness through the arc, with a ramped entry and upturned protected lip. Support bottom remainsY140/Z928mm, bar axisY140/Z942mm. Steel width60mm, liner58mm. Welded rear shelf overlaps the backplate4mm; backplate now seats flush against the60mm inner tube, rather than floating in front. An8mmY-axis through-bolt fits real9mm tube openings; front and rear liner details protect contact regions. These are original commercial-style illustration choices, not exact proprietary J-hook drawings.

Existing15.875mm locking pin now has a chamfered end,170mm length, D-loop grip, washer and real3.5mm retainer cross-drill with2.4mm-wire spring R-clip. All16 existing17mm bores/50mm positions engage the fixed pin atZ900mm; minimum overlap142mm and independent0/15 case validated. Stepped polymer guide opening61mm gives0.5mm side clearance around60mm slider. Actual outer tube internal72mm gives6mm side gap, correcting the earlier10mm figure that compared outer section sizes rather than internal clearance. No overall dimensions, anchor/axis/range/interface change; independent_barbell_support@0.1.0 remains the same asset-local proposal.

### Validation and compatibility

**646 existing checks PASS;243 origin details PASS. Final additional measured seating and strict assembly reproduction fail; see final-audit.json.** Reports: validation-results.json /origin-validation.json. Tests independently compare predecessor matrices, hierarchy, material slots and unedited geometry, measure concentric arcs and actual cradle surface, ray-test both pin walls/hook-bolt bores/cross-drill, and verify every detent. Source root floor(0,0,0), individual floor framesX±550mm, unit positive transforms and existing seven support/contact anchors are intact.

Existing review assembly links the refined pair, approved bench0.1.2 and barbell1.0.0 with original instance matrices. Bar axis(0,.44,.942)m and shaft+X; 1100mm support centers,75mm flange clearance,73.75mm bench-to-base envelope clearance,484.8mm bar axis above pad. Actual inter-asset triangles have zero crossings. Intended welded hook/structural contacts are documented internal joins. Historical0.1.1-before-resave646checks passed after filesystem relocation; relative links resolve. No physical safety, human fit, alternate model, load rating or animated override claim. All269 protected original equipment/fixtures/shared-guide files remain identical.

### Reference evidence and remaining issue

Six standalone views (front,side,three-quarter,maximum height,hook detail,adjustment detail) and3assembly views (assembled,side,front) regenerated and manually inspected at1600×1000. All6standalone references and assemblyfront reproduce exactly. Strict equality still **FAILS for assembled and assemblyside**: previous refinement probe maximum8/255 on0.02139% channels. No tolerance change/waiver; exact cause remains unresolved. See render-reproduction.json. Keep status review/not_ready; V06 remains open despite passing geometry/compatibility. Global standards and approved asset appearances unchanged.

- [front /bench](previews/168h_equipment_barbell_stands__front__bench.png)
- [side /bench](previews/168h_equipment_barbell_stands__side__bench.png)
- [three_quarter /bench](previews/168h_equipment_barbell_stands__three_quarter__bench.png)
- [maximum_height /maximum_height](previews/168h_equipment_barbell_stands__maximum_height__maximum_height.png)
- [hook_detail /bench](previews/168h_equipment_barbell_stands__hook_detail__bench.png)
- [adjustment_detail /bench](previews/168h_equipment_barbell_stands__adjustment_detail__bench.png)

Source/image/presetSHA256 pins are in asset.json and previews/render-settings.json. Assembly references/settings/metadata are retained beside its source. Artwork license remains separate/unselected; manufacturer photo is not bundled.

### Reproduction and controls

Open the existing master; never run the initial builder over it. Root height_index_l/r custom integer properties0–15 move corresponding upper geometry/anchors50mm per index. Use equal values for a level racked bar. Independent stand controller floors and pair root remain intentionally positioned; placements/spacing changes require contact/origin revalidation. Linked consumers use published frames/asset_instance_frame; authored library overrides/actions are still untested.

To reproduce the authorized in-place edit only in a disposable copy, restore the retained0.1.0 stand source to its canonical path, retain refinement-plan.json, then run Blender5.1.1 --background --factory-startup --python-exit-code 1 --python scripts/blender/refine_barbell_stands.py. Exact predecessorSHA guard prevents rerunning over the successor. Run render_barbell_stands.py and validate_barbell_stands.py with the same CLI prefix. Renderer -- --reproduce writes ignored outputs and returns nonzero while strict assembly pixel equality fails; it never resaves native sources. The archived fixture must be restored to its canonical path to resolve its original relative links; archive bytes are intentionally not rewritten.

### Decisions and delivery

Approve/revise the current commercial-style hook/cradle, pin/clip/guide details, original dimensional interpretations,1100mm spacing/928mm bench support, and local control/preset interface after review. No shared-standard promotion is proposed. Exact assembly rendering, artwork release scope, physical engineering and untested consumers remain explicit limitations. No production approval requested or inferred.

Standalone ZIP: exports/illustrations/stands_unassembled_renders.zip (6PNGs+settings). Assembly ZIP: exports/illustrations/stands_assembled_renders.zip (3PNGs+settings). Same native source paths; no commit requested. New required evidence is retained under the asset/fixture, not only ignored exports.

## Final validation —approval withheld,2026-10-15

User requests approval/commit only if all checks pass, preserving the current approved visual design. **Condition not met: no approval and no commit.** [Final audit](final-audit.json) is authoritative for this attempt. Current native source and all reference PNGs are untouched during validation; approved bench/barbell/plate and shared standards are unchanged.

Existing646checks and243origin details PASS. Additional independent measurements43PASS/2FAIL,6failure-injection and2offset-aware placement regressions PASS. Direct geometry confirms73.74996mm horizontal bench separation,74.99999/75.00005mm flange margins,1100mm mirrored support spacing, no interasset BVH crossings and all16locking detents/anchors. Pin nominal radial clearance0.5625mm; actual tessellated bore-face measurements0.54412–0.54424mm are positive at all positions. These sampled/face distances are distinguished from nominal circular dimensions; no physical fit certification.

F01: Nominal28mm-envelope axis is correctly aligned atZ942mm, but sampled knurled-shaft vertices remain4.827976µm above the liner on both hooks (59axial rays show minimum6.79493µm). Additional actual-contact check uses1µm and FAILS; earlier nominal-anchor tests did not detect this. Exact closest-triangle contact should be verified before applying any scene-owned settlement offset; this audit is not an exhaustive triangle-distance proof. Preserve source anchors and approved barbell/bench geometry.

F02: Current strict reproduction7PASS/2FAIL:6standalone and assemblyfront exact; assembled/side differ by up to8/255 on0.02309375%channels. No shared preset/tolerance waiver. Correct reproducibility before production approval.

An unrecorded native resave changed sourceSHA5ef637f5…→5b209122… before this turn. Exact compared objects/topology/coordinates/frames/materials/drivers/cameras/render semantics are identical; saved-revision-comparison.json records it. Retained old validated source at history/0.1.1-before-resave, corrected current manifest/dependency SHA only. Original refinement-record/render-settings/image capture source pins still identify retained5ef…bytes; current source is5b… and standalone images reproduce exactly. No source resave or geometry change in this final validation. The earlier relocation result remains historical and is not falsely relabeled as a checkout of the new serialization.

Manufacturer page rechecked2026-10-15:24.5×23.5in footprint,70in maximum upright,5/8in pin and UHMW protectors corroborated. Tube-top vs overall height datum remains unverified; current tube top1778mm/backplate1798mm. Detailed stock, pitch, hook and clip values remain original assumptions. This is an internal illustration asset candidate, not a manufacturer replica or load-rated product.

Commands: existing validate_barbell_stands.py; new validate_stands_final.py for direct measurements (returns nonzero for F01), compare_stands_saved_revision.py for durable digest reconciliation; render_barbell_stands.py -- --reproduce returns nonzero for F02. All use the existing Blender5.1.1 --background --factory-startup --python-exit-code 1 --python prefix. Final reports under this asset retain the expected/actual values and script digests.

## Final resolved validation and approval — 2026-10-15

**Approved / ready for internal 168Hours Blender illustration-library use.** This
section supersedes earlier review/failure statements; historical evidence remains
retained. Approval follows the user's conditional finalization request and explicit
“Approve this scoped comparison exception” answer. Source stand geometry0.1.1,
materials, origins, anchors, controls and all approved equipment bytes are unchanged.
[Approval record](approval-record.json) pins the native sources, current references
and accepted local policy. No shared standard is changed.

The original shaft/liner facet gap is real: 4.799192 /4.798168 µm measured by
exhaustive triangle distances with conservative AABB pruning, beyond ray/vertex
sampling. It arises from discrete surface geometry at the nominal28mm anchor
placement. Only the scene-owned barbell instance is lowered4.708766937µm. Final
positive distances0.093209 /0.092185µm meet the unchanged1µm criterion, with zero
BVH crossings. No source geometry was corrected or duplicated. A first float32
placement overshot by~0.03µm, failed collision QA and was replaced; evidence is
retained in contact-first-trial*.json. Published axis anchors remain nominal,
radius-specific frames; consumers measure the actual surface and own settlement.

Current fixture0.1.2 bar center(0,0.439999997616,0.941995263100)m;1100mm
support centers,73.74996mm bench clearance,74.99999/75.00005mm flange margins.
All16detents, engagement/clearance of both pins, root/pivots, normalized transforms
and seven anchors pass. Only original unpublished details remain provisional
physical assumptions; manufacturer footprint622.3×596.9mm,5/8in pin15.875mm
and70in upper-height context remain documented.70in-to-tube-top datum is still
an interpretation;1798mm backplate top is not claimed as a manufacturer dimension.

Workbench's native outline path varies on identical linked inputs; disabling
outlines is diagnostic only. Single render thread, reduced far clipping and
AA changes did not solve it while preserving appearance. The internal GPU cause
is not proven. Explicitly approved [comparison policy](render-comparison-policy.json)
applies only to assembly assembled/side: RGBmax8/255, exact alpha,<0.1% changed
RGBA channels,<0.15% changed pixels, mean absolute RGBA error≤0.002 in8bit units.
All six standalone views and assembly front remain exact. No blur/mask/alignment
or automatic rebaseline is allowed. All three assembly views were refreshed for
the corrected fixture; originals retained in its history/0.1.1-before-contact.

**647geometry/compatibility +243origin details +45independent measurements PASS;
6origin failure-injection +2placement +9comparison boundary tests PASS. All9
reference views pass in three ordered runs(27comparisons); relocated copy passes
647+45+9checks.** See final-audit.json, final-measurements.json,
render-repeat-validation.json, render-comparison-tests.json and
relocation-validation.json. Current corrected assembly views manually inspected:
unchanged silhouettes, palette/outlines, symmetric support, no shadows/AO.

Reproduction: run validate_barbell_stands.py, validate_stands_final.py,
validate_stands_regressions.py, test_stands_render_comparison.py and
validate_stands_render_sequence.py using Blender5.1.1 with
--background --factory-startup --python-exit-code 1 --python. The independent
facet proof uses investigate_stands_gates.py -- --contact-after. Do not rerun
settle_stands_review_bar.py on the corrected fixture; it is one-shot provenance.

Accepted assumptions apply to internal illustration use only: original unpublished
sections/hook/pitch/spacing details; no physical strength/load/ergonomics or
authored override-animation certification. External artwork terms remain separate
from MIT code/docs and unselected. These limitations do not claim new shared
standards or broaden manufacturer verification.

Fresh local Git/LFS checkout validation also passes647geometry+243origin details+45measurements+9reference views; Git and LFS integrity checks PASS. See committed-checkout-validation.json. The final documentation amendment preserves the tested source/model/policy/script/reference bytes.
