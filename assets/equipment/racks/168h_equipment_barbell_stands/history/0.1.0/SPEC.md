# Asset specification: 168h_equipment_barbell_stands

Source: [168h_equipment_barbell_stands.blend](168h_equipment_barbell_stands.blend). Metadata: [asset.json](asset.json). Checklist: [validation.md](validation.md).

## Identity and approval

Version0.1.0, **review prototype**, equipment/racks. Original pair of separate height-adjustable standalone barbell stands; no connecting crossbar, storage pegs, collars, safety arms, humans or exercise animation. Creation and a technical linked review assembly explicitly authorized2026-10-15. Appearance, local interface and detail choices await user approval. Shared standards unchanged. Read AGENTS, README, global style, common/category contracts, workflow, decision register/licensing and approved plate/barbell/bench specifications before modeling. Exact approved artifact and normative guide hashes retained in prebuild-record.json; protect all approved geometry/materials/renders.

## Sources and dimensions

Manufacturer context: [Vulcan Olympic Adjustable Squat Stands](https://www.vulcanstrength.com/Adjustable-Squat-Stands-Olympic-p/v-oly1.htm), consulted2026-10-15. Published per-stand footprint24.5×23.5in (622.3×596.9mm), adjustable upright up to70in (1778mm),5/8in pin and protected hooks. Original illustration inspired by this construction type, not a replica or load-rated product. [Rogue independent S-4](https://www.roguefitness.com/rogue-s-4-squat-stand-2) corroborates H-bases, reinforced bolted connections and lined J-cups; its fixed-height upright is not the selected mechanism.

| Dimension | Meters | Evidence/state |
| --- | --- | --- |
| Per-stand base X/Y | .5969/.6223 | Published Vulcan pair of footprint dimensions; assigning depth24.5in is an original orientation choice |
| Maximum telescoping tube top | 1.778 | Manufacturer-supported70in context, excludes hook backplate extension |
| Default tube top / overall height | 1.028 /1.048 | Provisional bench setup, measured digital geometry |
| Pair overall X/Y/Z | 1.6969/.6223/1.048 | Derived from1100mm center spacing and footprint; provisional spacing |
| Outer upright | 80×80mm, Z70–970mm, wall4mm | Original provisional section/length |
| Inner upright | 60×60mm, length950mm, wall3mm, bottom78mm at rest | Original provisional;10mm nominal lateral gap bridged by polymer guide,142mm overlap at maximum extension |
| Adjustment | index0–15,50mm pitch | Local review proposal, rest/min support928mm, max1678mm; integer controls independently per side |
| Pin | 15.875mm | Published5/8in context; holes17mm local clearance |
| Hook | width60mm, lined shelf Y90–190mm, support plane Z928mm at rest | Original provisional open+Y J-profile; backplate and retaining lip;28mm shaft center Z942mm |

No inference of real mass, gauge, steel strength, load rating or manufacturing compliance. Source units meters, tolerance1e-6m for digital checks only. Base contact patches and pair root intentionally centered at floorZ0. +Zup/+Yfront(open hook)/+Xsubject-left. Pair root and collection pivot(0,0,0); each independent stand controller floor at(+/-.55,0,0). Mesh origins are documented construction frames, never arbitrary geometry-centering. All mesh scale1/rotation0; mirrored components share data without negative transforms. Source pair remains modular with separate left/right fixed base and sliding upper controller.

## Geometry, reuse and controls

H-base: two longitudinal steel rails, transverse lower tie, four rubber floor pads per stand, reinforced triangular gussets and bolt heads. Hollow outer/inner tubes, real through holes and removable support-pin geometry with grip/retainer details, dark polymer telescope guide at collar. Hook has structural shelf/back/lip and dark polymer bar-contact liner. Intended welded joints, pin-through-holes and guide/telescope engagement are documented internal contacts; no unrelated asset penetrations permitted. Symmetric parts reuse mesh data, whole opposite stand shares all matching data. Geometry must have closed outward components, no loose edges or degenerate faces.

Root custom integer properties height_index_l/r0–15 drive upper controller Z=index*.05. Sliding geometry and support/axis anchors follow; fixed outer pin atZ900mm engages one of16 real holes in the inner tube at every detent. UI ranges document limits; validation tests all detents, minimum/maximum extension and mixed left/right state. A racked bar requires equal heights. No physical motion/safety simulation. Component source origins recorded in manifest; native driver graph is local and requires no addon. Library overrides/actions are not yet authored/tested.

## Interfaces and replacement

Asset-local proposal independent_barbell_support@0.1.0. Stable top collection/root and __geo/__anchors children. Anchors: floor_contact at pair root; floor_l/r at each stand's floor controller; bar_support_l/r at(X+/-550,Y140,Z928)mm; bar_axis_l/r at sameXY/Z942mm for the existing28mm bar. All rest frames+Yforward/+Zup. Support and axis anchors move with upper controller. Axis anchors are radius-specific convenience; future bars align using support surface plus their measured radius. No other bar/rack/human substitutions certified.

Review fixture links this pair plus approved bench0.1.2 and barbell1.0.0. Stands rotated180° so hooks face toward bench foot end(-Y), pair floor centerY580mm; bar centerY440mm and Z942mm. Bench remains at floor origin, head+Y; bar Xshaft. Pair support centers1100mm apart, each hook outer edge580mm from bar center vs exposed shaft end655mm,75mm axial flange clearance. Inner base edge251.55mm vs bench overall halfwidth177.8mm leaves73.75mm horizontal clearance. Bar axis484.8mm above pad; racked setup only, no anatomical ergonomic claim. Verify actual saved evaluated triangles with BVH plus numeric clearances. Source-approved assets linked with relative paths and original data, never appended/modified. No plates loaded in this scope.

## Materials and rendering

Reuse approved equipment numerical cues locally: charcoal steel363A40 body/454A51 top/2A2D32 side; grip/liner17191D/24272C; restrained brighter hardware from existing steel family. No branding. Existing Blender5.1.1/WorkbenchFLAT helper,1600×1000RGBA8,32AA,Standard/None, whitebackground/native dark outlines, no lights/ground/specular/shadows/AO/cavity. This is asset-local preset stands_review_flat@0.1.0, not shared default. Camera records will accompany references. Standalone front+Y,side+X,three-quarter+X/+Y, plus maximum-height detail as useful; separate linked assembly views for fit and contact.

## Licensing, dependencies and reproduction

Original procedural artwork, no imported meshes/images/textures/fonts/addons. No external artwork grant selected; code/docs MIT separately. Source asset has no external geometry dependency; assembly dependencies pinned by sourceSHA and version. Do not rerun builders over approved equipment. From repo root using Blender5.1.1 --background --factory-startup --python-exit-code 1: initial build scripts are scripts/blender/build_barbell_stands.py and build_stands_review_assembly.py and refuse to overwrite existing files. Use them only in a disposable build with new outputs absent. For saved-source review, run scripts/blender/render_barbell_stands.py and validate_barbell_stands.py. Native roots/anchors/height controls saved; all outputs validated from reopened source. Reference reproduction uses renderer -- --reproduce into ignored exports, never resaves master. Approved equipment, fixtures, AGENTS and normative guides remain hash protected. Git commit/fresh remote checkout not requested; LFS/ignore attributes checked.

## References and acceptance

Initial pre-build state recorded in prebuild-record.json; completed evidence follows. Review approval remains pending even if technical tests pass. Future visual/interface changes require authorized revision and revalidation. No new shared category, origin rule or software standard established.


## Completed prototype and review evidence —2026-10-15

Source0.1.0:64 closed mesh objects/32 unique mesh datablocks. Each opposite stand shares its matching geometry; independent floor/slider controllers and seven published anchors.449 geometry/material/naming/detent/pin-opening/dependency/linked-contact checks PASS, zero FAIL;243 detailed generic origin checks PASS. Tests cover all16 equal detents and a mixed0/15 case, actual liner-top support, real hole rays,142mm minimum telescope overlap, normalized transforms and correct +X bar shaft. Separate saved fixture links all three original sources with no local meshes. Actual inter-asset BVH pairs have zero crossings; no physical stability or strength certification. Racked shaft projection is inside each four-pad footprint. Approved sources and269 protected files are unchanged.

Original plate visual approval pins, its migrated current source/renders, approved bench and barbell source/render pins were verified. Published pair is one library collection with two independently movable floor controllers; separate per-stand collections and authored library-override/animation use remain future proposals, not claims. Pair root remains centered only in the declared canonical spacing/configuration; changing spacing requires contact/origin revalidation.

Initial QA corrected invalid Boolean hole edges/material-null slots, a36.5mm linked-root height offset, and a wrong bar shaft orientation caused by discarding the source anchor frame rotation. Small accidental Boolean boundary gaps were closed while preserving real through holes; no post-hole bevel on the perforated inner tube. Current tests explicitly cover those defects. Camera framing now includes all rubber pads; side view intentionally superimposes the two stands. No approved source was edited.

Fresh process and relocated library validation both PASS449 checks and all relative links resolve. This is a filesystem relocation test, not a committed Git/LFS checkout or remote hosting test. Five standalone reference views reproduce exactly. **All three assembly strict exact-pixel comparisons FAIL** in the final probe: final probe max6/255 on0.05169% channels. Differences are small raster edge/depth variations; exact cause is not established. No tolerance was relaxed, no production/reproducibility approval claimed. This is an open V06 review/release gate; inspect render-reproduction.json and keep current captured assembly images pinned. Do not edit approved bar/bench geometry to mask it. Native sources are never resaved by validators/render reproduction.

### Current reference views

- [front — bench](previews/168h_equipment_barbell_stands__front__bench.png)
- [side — bench](previews/168h_equipment_barbell_stands__side__bench.png)
- [three_quarter — bench](previews/168h_equipment_barbell_stands__three_quarter__bench.png)
- [maximum_height — maximum_height](previews/168h_equipment_barbell_stands__maximum_height__maximum_height.png)
- [hook_detail — bench](previews/168h_equipment_barbell_stands__hook_detail__bench.png)

Assembly references and captured camera settings live beside the linked fixture. SHA256/source/preset pins are in both manifests and previews/render-settings.json. Both groups use1600×1000RGBA8, no shadows/AO/cavity/specular; all current views manually inspected at delivery size for recognizable geometry/outline and clear contact. Review status retained; exact assembly reproduction, design acceptance, detailed dimensions/interface and external artwork terms remain open.

### Editing and reuse

Open the standalone master. In the Outliner select168h_equipment_barbell_stands__root (unhide the Empty if needed); Object Properties → Custom Properties → height_index_l / height_index_r. Set integer0–15. Both must match when racking a level bar. Normal driver evaluation moves only the corresponding slider/hook/anchors by50mm per index. Source control_stand_l/r floor frames are the individual installation controls; changing either placement requires revalidating pair origin and bar fit. Linked scenes use the published collection and asset_instance_frame helper, not mesh vertex constraints. Library overrides/actions are not yet tested; do not imply a linked source property is directly editable in a consumer.

For reproduction run Blender5.1.1 --background --factory-startup --python-exit-code 1 --python scripts/blender/render_barbell_stands.py -- --reproduce. It returns nonzero while the strict assembly comparison fails; this is deliberate, not suppressed. Geometry QA command uses scripts/blender/validate_barbell_stands.py. Keep current authoritative source and review evidence; initial builders refuse overwrite. Global numeric defaults remain unchanged.

### Decisions requiring review

Accept/revise appearance, base construction, hook proportions, telescoping mechanism and50mm detents; accept/revise1100mm support spacing and928mm bench support height; review the pair-publication and independent control/anchor interface. Manufacturer dimensional context is documented separately from these original choices. Approve a release only after resolving the exact assembly-render gate and explicitly defining intended artwork/release scope. No optional shared-standard change is required to review this prototype.

### Delivery

Standalone: exports/illustrations/stands_unassembled_renders.zip (5PNGs+settings). Linked assembly: exports/illustrations/stands_assembled_renders.zip (3PNGs+settings). Native source and assembly remain at manifest paths. No commit requested for this creation step; source files are untracked but have LFS attributes, and backups/ZIP exports are ignored.

Final source review: pair floor_contact parent is the aggregate root (unchanged canonical position); anchor ownership is verified explicitly. Current449checks and243detailed origin checks PASS; final native source digest is in asset.json.
