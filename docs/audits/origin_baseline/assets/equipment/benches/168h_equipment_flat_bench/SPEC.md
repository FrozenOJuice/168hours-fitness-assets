# Asset specification: 168h_equipment_flat_bench

## Identity and status

Version **0.1.1**, equipment/benches. **Review prototype; design not approved.** Initial specification/metadata/checklist existed before build; their pre-build digests are preserved in build-record.json. Codex for 168Hours Fitness, 2026-10-14. Standalone fixed flat utility bench; no uprights, rack, human, barbell assembly, wheels or exercise scene.

Source: [168h_equipment_flat_bench.blend](168h_equipment_flat_bench.blend). Metadata: [asset.json](asset.json). Technical/manual evidence: [validation.md](validation.md). Standards read before build: [AGENTS](../../../../AGENTS.md), [style](../../../../docs/visual-style.md), [conventions](../../../../docs/asset-conventions.md), [bench category row](../../../../docs/category-standards.md), [workflow](../../../../docs/asset-workflow.md), [licensing](../../../../docs/licensing.md), [decisions](../../../../docs/decisions.md). Exact pre-build hashes/base Git revision in [standards-snapshot.json](standards-snapshot.json). Approved plate 0.1.4/A10 and barbell 0.1.2/A12 specs, manifests, QA and frozen approval evidence reviewed; their checksum records verified before work. They are visual cues, not bench geometry standards. A13 records this asset-local proposal. A01–A08 global decisions remain unchanged.

## Dimensions and geometry

All meter values, numerical validation tolerance 0.000001 m; not fabrication tolerances. Manufacturer context: [Rogue Flat Utility Bench 2.0](https://www.roguefitness.com/rogue-flat-utility-bench-2-0), consulted 2026-10-14, lists overall length 47 in, width 14 in, height 18 in, pad width 12 in, pad thickness 2.5 in, 2×3 in steel context. This brand-neutral asset uses those dimensional facts only; no reference images/CAD/artwork downloaded. Model does not claim to reproduce that product, strength rating or 11-gauge wall thickness.

| Measurement | Target | Basis / approval state |
| --- | --- | --- |
| Overall X/Y/Z | 0.3556 / 1.1938 / 0.4572 | Matches manufacturer overall 14/47/18 in envelope; pending bench design approval |
| Pad width / top height / thickness | 0.3048 / 0.4572 / 0.0635 | Manufacturer published 12/18/2.5 in; numerically validated in saved source |
| Pad length | 1.1938 | Inferred from overall length and pad-dominant layout; **provisional**, not explicitly published pad length |
| Rubber-foot outer envelope X/Y | 0.3556 / 1.025 | Width manufacturer context; longitudinal foot positions/spacing **provisional**. Rubber envelope is shorter than overall pad envelope; actual Z0 patch bounds349.6×1019mm due lower-edge rounding |
| Substrate thickness | 0.0127 | Provisional mounting board, excluded from foam thickness |
| Steel leg horizontal section / foot section | 0.0508 × 0.0762 | Manufacturer 2×3 in context; sloped legs use this horizontal cut section (not a verified perpendicular extrusion profile), closed illustration solids, no wall gauge claim |
| Central spine | 0.0508 × 0.0508, length 1.0 | Provisional generic support arrangement |
| Pad plan corner / edge radii | 0.030 / 0.014 top / 0.006 lower | Provisional gentle rounding; preserve central flat contact area |
| Rounded rubber shoes / foot centers | 0.0756 × 0.085 × 0.064; X±0.14, Y±0.47 | Provisional original four-foot layout |

Canonical +Z up, length/head +Y, width/subject-left +X; root is centered on ground footprint at (0,0,0), identity transform. All rigid mesh scale/rotation normalized; local component translations permit shared geometry; all source objects descend from root. No adjustments, rig, deformation or physics. Fixed flat angle 0°. Pad is separate from substrate, spine, two sloping legs, two transverse feet, two mounting rails and four rounded rubber shoes. Refinement adds actual near-flush upholstery piping, four upper gussets, four saddle mounting cheeks, four pad bolts with washers and four cross-bolt heads. All13 original mesh objects/data identities remain; pad topology is preserved and vertex positions adjusted, shared rubber topology refined in place. Original main frame/substrate geometry remains unchanged. Feet, mounting rails and four boots reuse mesh data. Two opposing leg slopes use distinct baked data from one recipe rather than negative instance scale. Subtle geometric edge rounding, no decorative noise or logos. Closed illustration components with intended overlapping steel joints/boots; not a Boolean-unioned fabrication model. No intentional penetration into foam.

## Published interfaces and replacement

Top collection `168h_equipment_flat_bench`, subcollections `__geo` / `__anchors`, root `__root`; object pattern `__mesh_<part>` / `__anchor_<name>`. Proposed asset-local `bench_support@0.1.0`, not a ratified category contract. Anchors all identity XYZ Euler (radians), +Y head/forward and +Z surface normal:

| Key | Local position (m) | Purpose |
| --- | --- | --- |
| floor_contact | (0,0,0) | Place bench on floor |
| pad_center | (0,0,0.4572) | Central flat support surface |
| seat_center | (0,-0.30,0.4572) | Suggested pelvis/seat support location, not anatomical fit claim |
| back_support | (0,0.15,0.4572) | Suggested upper-back contact |
| head_support | (0,0.40,0.4572) | Suggested head contact |
| head_end | (0,0.5969,0.4572) | Pad-envelope endpoint; rounded edge is not a flat contact here |
| foot_end | (0,-0.5969,0.4572) | Opposite pad-envelope endpoint |

Scene placement must use instance root and anchor frames, not vertices. Bench length +Y permits a future rack/bar axis +X, consistent with approved barbell orientation. No rack clearances/human poses certified: consumers must verify shoulder/pelvis/feet support and rack interference for actual body dimensions. Endpoint frames bound the envelope; center/seat/back/head frames lie on the unrounded flat pad top. Height or envelope replacements need pose/contact review and a versioned interface migration for breaks. First bench has no alternate replacement asset; validate linked two-instance reuse and frame alignment in a disposable technical test, not an exercise scene.

## Materials and visual design

Use existing clean equipment visual direction: matte charcoal, controlled face values, white background, clear native outlines, no cast/contact shadows, AO/cavity, textures or baked lighting. Asset-local `flat_bench_review_flat@0.1.0` uses approved barbell capture settings (Workbench FLAT, 1600×1000 RGBA8, 32AA, Standard/None, exposure0/gamma1, no specular) as a review proposal only. Global numeric palette/engine/output decisions remain open. Fixed vertex/face role values convey construction without lights.

Semantic slot groups: padding 25282D top / 1C1F24 side / 30343A edge; frame 363A40 body / 454A51 top / 2A2D32 side; grip/rubber 17191D with 24272C edge; substrate 202328. Frame swatches reuse approved plate color values as cues; padding/rubber variants are local proposals. Principled roughness1/metallic0. No shared material library exists to link; no geometry from approved equipment is appropriate for a bench. Create unique bench shapes, reuse symmetric part data and captured render helper code; no new shared palette/library. Stable per-mesh semantic slot order documented in metadata after build.

## Dependencies and licensing

No external asset, texture, font, add-on or linked material dependency. Code renderer helper imports `scripts/blender/barbell_20kg_common.py` for existing setup/camera functions only; does not rebuild or modify approved sources. Original procedural artwork by Codex for 168Hours Fitness. Artwork license **null / not licensed for external redistribution**, separate from MIT code/docs; authorized internal prototype review only. No mass/load rating, competition certification or hardware safety claim.

## Reproduction instructions

From repository root, Blender 5.1.1, no add-ons:

1. Fetch LFS sources; retain existing approved artifacts. Read spec/manifest before build.
2. The authoritative source is already refined; open it directly. `build_flat_bench.py` is the historical0.1.0 builder and **must not be rerun over the refined source**. To reproduce the in-place edit in a disposable checkout only, restore `history/0.1.0/168h_equipment_flat_bench.blend` to the canonical source and run `/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/blender/refine_flat_bench.py`. The script requires the exact predecessor hash, retains original identities and modifies only this bench.
3. Run that Blender command with `scripts/blender/render_flat_bench.py` to reopen saved source and regenerate retained front (+Y), side (+X), three-quarter (+X/+Y) and top references.
4. Run with `scripts/blender/validate_flat_bench.py` for saved-file topology, measurements, anchors, relative links, duplicate-data reuse and linked placement tests. Camera/engine/palette details in `previews/render-settings.json`, results in `validation-results.json`.
5. Run with `scripts/blender/reproduce_flat_bench_renders.py` to regenerate disposable references and compare decoded pixels; source is never resaved.
6. Manual actual-size render review and checklist reconciliation required; design acceptance remains user decision. ZIP contains standalone references only, under ignored exports/illustrations; no interchange export settings claimed (A08 open).

## Reference render index

Front, side, three_quarter and top, canonical `flat` configuration, frame1. All four references rendered and inspected at 1600×1000. Source SHA256 `6a1c111e801358dc62e44040ed6fce2ed2c40c6b3444928c9db603b17e5b63fb`; preset revision SHA256 `250a4ad5c2af067ad9974f6282cb0081cec9e76ac85973df685f32df1b2280f3`.

| View | Retained reference |
| --- | --- |
| side | [168h_equipment_flat_bench__side__flat.png](previews/168h_equipment_flat_bench__side__flat.png) |
| three_quarter | [168h_equipment_flat_bench__three_quarter__flat.png](previews/168h_equipment_flat_bench__three_quarter__flat.png) |
| front | [168h_equipment_flat_bench__front__flat.png](previews/168h_equipment_flat_bench__front__flat.png) |
| top | [168h_equipment_flat_bench__top__flat.png](previews/168h_equipment_flat_bench__top__flat.png) |


## Exceptions and unresolved issues

No conflicting shared-standard exception. User-authorized prototype scopes A01/A03/A04/A05/A06/A08 choices locally under A13; nothing promoted to global standard. Pending: bench appearance/proportions, inferred pad length, foot/spine/rounding details, palette and anchor proposal; tested human/rack consumers and alternative replacement; physical pad compression/mass/load strength; separate artwork license (A07). These prevent production-ready status. No changes to approved plate/barbell or shared visual/category standards.

## Validation and acceptance

Saved-source validation: **72 PASS / zero FAIL**, [machine results](validation-results.json); 30 mesh objects / 15 unique mesh datablocks, all closed manifold and nondegenerate. Measured overall bounds X/Y/Z 0.355599999 / 1.193799973 / 0.457199991 m; floor Z0. Pad width/length/thickness 304.8/1193.8/63.5 mm within 0.001 mm numerical tolerance, top Z457.2 mm. Four boots contact Z0; rubber outer envelope355.6×1025 mm, actual Z0 contact-patch bounds349.6×1019 mm; no frame penetration into foam, substrate touches foam bottom intentionally. Welded frame/boot joins intentionally overlap and are not fabricated joint certificates.

Linked two-instance fixture verifies shared library data and back-support mapping to (1,2,0.75) with yaw90°, full frame error below1e-6; no local geometry copy. This is an unsaved technical test, not an exercise scene or actual alternative-bench/human/rack test. All four decoded references reproduced exactly (max channel delta0) in a fresh process: [render-reproduction.json](render-reproduction.json). A relocated standalone source is also tested; fresh committed Git/LFS checkout remains NOT RUN.

Manual image review: pad rounding and support/foot silhouettes readable, charcoal roles distinct, no shadows/AO or branding. User approval pending; lifecycle remains review/not_ready. [Validation checklist](validation.md) distinguishes prototype passes from release gates. All protected approved-equipment/fixture files, shared standards and prior exports/README change preserved byte-for-byte. No redesign of existing assets.

## Change history

| Date / version | Change | Approval |
| --- | --- | --- |
| 2026-10-14 / 0.1.0 | Initial specification before geometry; standalone flat utility bench prototype | User authorized creation; design acceptance pending |
| 2026-10-14 / 0.1.1 | In-place upholstery/rubber/structural connection refinement; original main frame and support interface retained; all references/QA refreshed | User authorized refinement; design acceptance pending |


## Delivery

Standalone source and four retained previews are authoritative. Bundle: `exports/illustrations/flat_bench_unassembled_renders.zip` (all four PNGs plus render-settings.json). This is the unassembled asset group only; the bench is shown in its normal built state, without other equipment. No assembled/test-scene blend was requested or retained. Source, docs and evidence are uncommitted pending repository review; LFS attributes and temporary/export ignores verified.


## 0.1.1 refinement plan — specified before editing

User authorized in-place commercial-detail refinement, review only. Preserve13 original objects and mesh datablocks, published root/anchors/interface/material slots, main steel members, nominal bounds and cameras. Reshape existing cushion vertices with30mm plan corners,14mm top roll and6mm lower roll; retain flat contact top Z457.2mm. Add restrained embedded piping and a side upholstery groove. Reshape the existing shared rubber-foot data to rounded, tapered slip-on shoes with a low perimeter sole lip, same footprint and floor contacts. Add paired upper gussets, four saddle cheeks and reusable bolt/washer details beneath the pad. Original spine/legs/feet/rails remain; no factory reset or bench builder.

Manufacturer dimensions rechecked2026-10-14 at the existing linked Rogue page: overall47×14×18in, pad12in wide/2.5in thick,2×3in frame context. No global or nominal-dimension correction needed. Pad length remains inferred; ground footprint/support layout, new upholstery profile/rubber shape and all connections are provisional original illustrative details, not verified manufacturing drawings. Prior evidence was invalidated before editing; current saved-source checks and all four renders have now been rerun. Release remains review/not_ready. Exact predecessor, scope and pre-edit evidence in [refinement-plan.json](refinement-plan.json); retained0.1.0 snapshot in [history/0.1.0](history/0.1.0/README.md); an additional local backup is under ignored exports/models/flat_bench_review_history/0.1.0.


### 0.1.1 implemented construction and review

[refinement-record.json](refinement-record.json) records the preserved identities and source/script hashes. Main spine/legs/feet/rails/substrate vertices are byte-equivalent numerically to the saved predecessor; original pad connectivity is unchanged. The18 existing pad perimeter rows now form a softer14mm top roll and30mm plan corners, with flat center support retained. A0.6mm-radius actual piping tube sits near the upper shoulder, inside the nominal pad envelope; a0.6mm-deep narrow side groove suggests upholstery joining without fabric noise or simulated wear. These are review details, not shared upholstery standards.

The four shoes retain one original mesh datablock and positions but use a rounded, tapered six-level profile,12mm nominal plan corners at the sole and a low protective lip. Shoe height64mm; outer width/depth75.6/85mm, top65.6/79mm. The floor patch is smaller than the widest sole envelope; both are recorded explicitly. Four upper6mm-thick gussets reinforce the leg/spine visual connection. Four6×64×64mm mounting cheeks flank the support; four vertical pad fasteners include18mm washers and approximately11.6mm hex-head vertex diameters. Four transverse heads indicate the bracket connection. No thread, rated bolted/welded connection, tube wall gauge or structural analysis is claimed. Original visible steel dimensions and palette are preserved.

All new details inherit existing three-slot charcoal material families; no new swatches, textures, engine, camera, outline or shared preset changes. Intended gusset/frame, washer/bracket and upholstery/pad contacts overlap locally. Steel does not enter the cushion. Rounded shoes cover support ends; no extra equipment introduced. Current four-image actual-size review confirms softer cushioning, readable seam treatment and structured under-pad construction without shadows/AO. Optional future manufacturing details require a separate authorized revision; approval remains pending.
