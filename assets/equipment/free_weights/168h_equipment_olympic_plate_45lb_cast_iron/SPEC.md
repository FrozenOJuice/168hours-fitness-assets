# Asset specification: 168h_equipment_olympic_plate_45lb_cast_iron

## Identity and status

- Category: equipment / free weights / Olympic weight plate. Asset version `0.1.4`; **approved visual-direction reference** `cast_iron_plate_visual@1` under A10; production lifecycle `review`, not `ready`. Geometry version is unchanged.
- Author/reviewer: Codex for 168Hours Fitness, 2026-10-14. The user approved the overall plate visual direction; the current 0.1.4 model and all five existing renders are now accepted as the first equipment visual reference, 2026-10-14.
- Source: [168h_equipment_olympic_plate_45lb_cast_iron.blend](168h_equipment_olympic_plate_45lb_cast_iron.blend). Current SHA256 `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`.
- Standalone reusable collection for future bench press, squat and deadlift scenes; no barbell, human or exercise scene authored.
- Standards: [global style](../../../../docs/visual-style.md), [shared conventions](../../../../docs/asset-conventions.md), [category standards](../../../../docs/category-standards.md), [workflow](../../../../docs/asset-workflow.md), [licensing](../../../../docs/licensing.md), and [AGENTS.md](../../../../AGENTS.md). Base revision `c91545cbe2e5a0909078b879508ef63501959827`; exact working-tree standard hashes in [standards-snapshot.json](standards-snapshot.json). A10 now establishes the cast-iron plate visual-reference standard; global engineering/software/delivery choices remain separate.
- Authorization: A09 approved local review prototype; user requested the rib, face lettering, hub/rim and side-profile refinement on 2026-10-14. User clarified **“45 LB left and 20.4 KG right on both faces.”** The user now explicitly approves this plate’s overall visual direction and requests whiter/larger raised letters, inverted BARBELL, and hub-originating outward-tapering ribs. Scope remains this plate; it does not approve global standards or production/licensing readiness.

## Dimensions and geometry

| Measurement | Target | Implemented / numerical tolerance |
| --- | --- | --- |
| Outer diameter | 0.450 m | 0.449999988 m, ±0.000001 m |
| Axial envelope / stack pitch | 0.03302 m | 0.033020001 m, ±0.000001 m |
| Minimum bore | 0.0508 m (2 in) | 0.050799978 m, ±0.000001 m |
| Maximum bore vertex diameter | ~0.0508038 m | Polygon circumscribes the required clearance circle |
| Web thickness | 0.013 m | 0.013000000 m |
| Center hub thickness | 0.029 m | 0.028999999 m |
| Outer rim relief above face | 0.01001 m | 0.010010000 m |
| Outer side waist radius | 0.2235 m | 0.223499987 m |
| Radial side-waist recess | 0.0015 m | 0.001500027 m below outer shoulder |
| Raised text relief above web | 0.0035 m | ~0.0035 m; 0.0038 m total solid depth |
| Canonical bounds X/Y/Z | 0.450 / 0.03302 / 0.450 m | 0.449999988 / 0.033020001 / 0.449999988 m |

These are numerical model tolerances, not manufacturing tolerances. The minimum floor Z is 0. Nominal labels `45 LB` and `20.4 KG` identify equipment weight; no density-based mass, physics, or fabrication accuracy is claimed.

The 450 mm diameter remains the A09-approved prototype assumption, not a universal cast-iron dimension. Its current proportion/appearance is accepted visually; this does not verify 450 mm as a production engineering dimension. Dimensional context: [Rogue traditional Olympic plates](https://www.roguefitness.com/rogue-olympic-plates), consulted 2026-10-14, lists its 45 lb plate at 17.5 in diameter and 1.3 in thickness. Thickness informs the envelope; this asset is not an exact manufacturer replica. No manufacturer artistic content is imported.

### Existing body refinement

The existing body object and mesh datablock are retained. Revision 0.1.1's 256-segment annulus had 5,120 vertices/quads; only its outer side band was locally subdivided with three cuts along each of 256 axial edges. The resulting closed manifold body has **5,888 vertices and 5,888 quads**, zero nonmanifold edges. Its bore, web, hub, face rim, root and attachment dimensions remain intact. Body topology therefore changes locally; full topology preservation from 0.1.1 is not claimed.

The straight bore polygon uses vertex radius `0.0254 / cos(pi/256)` to preserve the exact 50.8 mm minimum clearance. Bore wall ends at Y=±12 mm; the bore entrance chamfer reaches r=27.4 mm/Y=±14.5 mm. Hub face extends to r=52 mm, shoulder transitions through r=56 mm/Y=±12 mm and reaches the web at r=61 mm/Y=±6.5 mm. Recessed web extends to r=197 mm. Inner rim transitions through r=202 mm/Y=±13.8 mm and r=204 mm/Y=±16.51 mm, then a flat rim extends to r=223 mm before its outer chamfer reaches r=225 mm/Y=±14.51 mm.

The original straight outer cylinder now tapers to a shallow waist: radius 223.5 mm at Y≈−7.255, 0, +7.255 mm between full-size outer shoulders. This creates an actual nonuniform side silhouette and distinct rim bands while retaining 450 mm overall diameter and 33.02 mm maximum pitch. Flat material separation makes the channel readable without shadows/AO.

### Four cast ribs per face

Four diagonal raised sections at 45°, 135°, 225°, 315° connect the hub shoulder toward the rim on each face. Eight closed solids share one published `__mesh_ribs` datablock/object; they are generated from one symmetric construction recipe instead of eight separately authored components. Each rib begins below the center hub face at r=43 mm and narrows continuously toward the rim, with sloped ends and physical chamfered top edges. Revision 0.1.4 sinks the existing rib root caps beneath the hub face so they emerge gradually through its shoulder; rib object/data/topology are retained.

| Radius (m) | Half-width (m) | Axial base magnitude (m) | Axial top magnitude (m) |
| --- | --- | --- | --- |
| 0.043 | 0.017 | 0.0118 | 0.0140 |
| 0.075 | 0.015 | 0.0062 | 0.0120 |
| 0.150 | 0.010 | 0.0062 | 0.0120 |
| 0.205 | 0.005 | 0.0135 | 0.0160 |

Full rib widths decrease monotonically from 34 → 30 → 20 → 10 mm at increasing radii. The six-vertex chamfered cross-section retains a 1.3 mm lateral bevel and 1.2 mm top bevel depth. The inner cap is fully buried under the hub face: its maximum planar radius is ~46.24 mm (inside the 52 mm hub face) and its top Y magnitude is 14.0 mm (below the 14.5 mm hub face). The rib rises out through the shoulder toward the unchanged 75 mm row, avoiding the previous cap across the ring. Outer tips still integrate into the rim. Mid-face ribs rise 5.5 mm above the recessed web. All remain inside the stack envelope and outside the bore. Four diagonal ribs leave four clear lettering quadrants.

### Raised face lettering

Both faces display **45 LB on the viewer's left**, **20.4 KG on the right**, **STANDARD above**, and **BARBELL below**. All are actual extruded, bevelled mesh lettering, with near-white #F2F2F2 faces and darker charcoal sides. Real 3D relief is retained at 3.5 mm; the color change does not replace geometry. No logos or additional markings. STANDARD/BARBELL are the requested generic descriptors.

- Weight labels are centered at local face-horizontal ±127 mm, at hub-center height. Original font sizes were 0.032 m (`45 LB`) and 0.025 m (`20.4 KG`); existing planar mesh geometry is now 8% larger about each label anchor, equivalent to 0.03456 m and 0.027 m sizes. Axial extrusion depth is unchanged.
- Both words use a 165 mm arc and equivalent 0.027 m font size. STANDARD keeps its existing glyph meshes; its S/T/A/N half shifts 1 mm left along the arc and its D/A/R/D half shifts 1 mm right, adding 2 mm at the central N–D gap while retaining the other spacing/tangent angles. BARBELL uses clean raised glyph geometry in the existing two word objects/datablocks: first lay it out as normal upright upper-arc text, using STANDARD’s original 48/7° tracking step (±20.571° for seven glyphs), then rotate the entire word 180° around the plate center. This preserves natural spacing, curve and letter orientation when the plate is turned like a steering wheel. Letterforms are not mirrored. See the rotated-plate proof render.
- Text solid depth is 3.8 mm: base magnitude Y=6.2 mm, top magnitude Y=10.0 mm, including 0.3 mm overlap with the web and 3.5 mm exposed relief. Built-in Bfont is converted to mesh; no runtime font dependency.
- Preexisting `__mesh_label_front` and `__mesh_label_back` objects/data are reused for the relocated `45 LB` labels. New `__mesh_label_kg_<face>`, `__mesh_label_standard_<face>`, and `__mesh_label_barbell_<face>` objects complete the layout. BARBELL glyph geometry/connectivity is regenerated to remove malformed inherited lettering, inside its existing object/data. Other label topology and all published object names remain stable.

Body, ribs and text are separate overlapping cast-on solids for clean visual reuse, not a boolean-unioned fabrication model. Full source scope: **10 mesh objects and 5 empties** (root plus four anchors), no camera/light/rig in the saved source. All added geometry is parented to the same root and has normalized identity object transforms. Repeated plates link/instance this collection and share all its geometry/material data.

## Published interfaces and replacement

Stable Asset Browser collection `168h_equipment_olympic_plate_45lb_cast_iron` with `__geo` and `__anchors`, root `168h_equipment_olympic_plate_45lb_cast_iron__root` at floor footprint center (0,0,0), identity transforms. Plate stands in XZ; +Y front/axial, +Z up, +X subject-left. Center at (0,0,0.225). No axis or root exception.

Interface **`olympic_plate_bore@0.1.0` remains unchanged**. Detail revision 0.1.4 does not alter its dimensions, anchor frames, published source path or existing material indices.

| Anchor | Full-ID object suffix | Local position (m) | Frame |
| --- | --- | --- | --- |
| bore_center | `__anchor_bore_center` | (0,0,0.225) | +Y axial, +Z up |
| stack_front | `__anchor_stack_front` | (0,+0.01651,0.225) | +Y axial, +Z up |
| stack_back | `__anchor_stack_back` | (0,−0.01651,0.225) | +Y axial, +Z up |
| floor_contact | `__anchor_floor_contact` | (0,0,0) | +Y axial, +Z up |

Place instances by aligning `bore_center` with a sleeve target, compensating the rotated (0,0,0.225) root-to-bore offset. Rotate +Y onto the sleeve direction, repeat at 33.02 mm pitch plus any deliberate scene gap, and reverse facing with a 180° rotation rather than negative scale. Stack frames define the maximum envelope, not an outward -Y back normal.

Validated reuse: three external linked collection instances, nonoverlapping stack envelopes, numerical 50.0 mm sleeve clearance (~0.4 mm radial), root-offset placement and rotation onto +X at a synthetic target. No real barbell, human, exercise consumer or alternative plate has been authored/tested. Those production compatibility claims remain open. Geometry topology is internal, not a substitute for named anchor interfaces.

## Materials and visual design

Asset-local preset `plate_review_flat@0.1.4` retains Blender 5.1.1 Workbench, flat lighting, native silhouette outlines, white background, 1024×1024 references, Standard/None color management and 32-sample antialiasing. **No shadows, ambient occlusion/cavity, lights, specular highlights, ground plane, or baked textures.** The matte body palette is unchanged; only the existing letter-face color changes from #9CA1A8 to requested near-white #F2F2F2:

| Existing material variant | sRGB | Usage |
| --- | --- | --- |
| cast_iron | #363A40 | Sides, waist, text bevel/sides |
| web | #454A51 | Recessed face and rib top planes |
| rim | #2A2D32 | Structural edge/rib-side contrast |
| hub | #50555C | Center hub and outer chamfer |
| lettering | #F2F2F2 | Raised near-white letter faces |

Principled nodes retain roughness 1 and metallic 0; Workbench uses matching linear-converted material display colors. Body slot order remains cast_iron/web/rim/hub; all lettering uses lettering at 0, cast_iron at 1. Ribs reuse web/cast_iron/rim at slots 0/1/2. No new material or texture dependencies. Improved depth comes from modeled surfaces and flat color regions, not simulated shadow maps. Native outline width is renderer-controlled at 1024 px; no geometry is added to imitate a fixed screen-width stroke. Other engines require an approved shadow-free consumer setup.

Design rationale: four diagonal ribs provide casting structure and balanced text space; left/right units and upper/lower arched descriptors resemble traditional generic gym equipment without logos. Hub/rim retain physically defined steps, and a shallow side waist breaks up the previous uniform slab. New details remain compact and subordinate to the recognizable circular silhouette. This plate’s visual direction is explicitly approved by the user. Exact 0.1.3 implementation values remain reviewable; no global design standard is approved.

## Dependencies and licensing

No external geometry, texture, font-file, add-on, rig or library dependencies. Blender Bfont is converted and unused authoring font data removed. Validator uses NumPy bundled with Blender. Original artwork authored for 168Hours Fitness; artwork terms remain unset under A07, separate from MIT code/documentation. No redistribution grant is inferred. Nominal unit labels are visual equipment markings; mass simulation remains unvalidated.

## Reproduction instructions

Run in a separate Blender 5.1.1 process from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/blender/correct_olympic_plate_45lb.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python scripts/blender/validate_olympic_plate_45lb.py
```

Substitute the executable path on other systems. The [current correction script](../../../../scripts/blender/correct_olympic_plate_45lb.py) opens the existing source. For the recorded 0.1.3 predecessor it edits STANDARD positions and rib root vertices once; it generates clean BARBELL geometry as an upright upper-arc word and rotates that entire word 180°. For an already-corrected 0.1.4 source it does not repeat the spacing/root edits and safely regenerates the same BARBELL mesh in the existing datablocks. It then saves the plate before transient review cameras are created.

[correction-record.json](correction-record.json) records source/edit-script hashes, preserved objects/data, unchanged body coordinates and non-BARBELL topology, glyph ranges/upper-arc definitions, and buried root dimensions. No plate/body rebuild occurs. BARBELL mesh connectivity can change; do not claim whole-asset topology preservation for this correction. Exact white colors, relief, body dimensions, anchors and interfaces are unchanged. Historical builder/refinement/detail/finish scripts are provenance only; do not run them to overwrite the current master.

Local predecessors are archived under ignored `exports/models/plate_review_history/0.1.0/` through `0.1.3/` for rollback, not as runtime dependencies or tracked releases. Current-source rerender/validation requires no archive. Reconcile source/evidence digests after any later edit or resave.

Source is saved before transient cameras are created; the asset opens in a framed flat front viewport. [Render settings](previews/render-settings.json) records source and edit-script hashes, Blender/build, palette, lighting flags, camera positions/Euler rotations, 0.56 m orthographic scale, frame 1, RGBA PNG 8-bit output, resolution, color management and antialiasing. Random seed is inapplicable to deterministic Workbench. The validator reopens the saved source in a fresh process, reproduces references in a disposable folder and compares decoded pixels, then tests linking/stacking/placement in an unsaved disposable fixture.

This update ran in an isolated Blender process and did not revert any existing live Blender session. The current deliverable is the updated master file on disk; reopen it to see this revision in Blender.

## Reference render index

All views use the same standing configuration, frame 1, target (0,0,0.225), 0.56 m orthographic scale and 1024×1024 resolution. Camera/palette/lighting standards are unchanged. The four standard views and an additional whole-plate 180° proof were inspected at output size and independently reproduced pixel-for-pixel.

| View | Retained image | Camera position (m) |
| --- | --- | --- |
| Front | [Front](previews/168h_equipment_olympic_plate_45lb_cast_iron__front__standing.png) | (0,1.2,0.225) |
| Side | [Side](previews/168h_equipment_olympic_plate_45lb_cast_iron__side__standing.png) | (1.2,0,0.225) |
| Three-quarter | [Three-quarter](previews/168h_equipment_olympic_plate_45lb_cast_iron__three_quarter__standing.png) | (0.82,1.05,0.675) |
| Reverse side | [Reverse side](previews/168h_equipment_olympic_plate_45lb_cast_iron__back__standing.png) | (0,−1.2,0.225) |

The additional [180° whole-plate proof](previews/168h_equipment_olympic_plate_45lb_cast_iron__rotated_180_check__standing.png) uses the same front-camera position/scale with a 180° optical-axis roll. It turns BARBELL upright at the top of the entire plate, directly verifying the steering-wheel viewing requirement. The word reads as normal curved text, with clean spacing and correct letter order. This is a transient camera view, not an exercise scene or a changed asset pose.

Front/back show four ribs and the same viewer-relative balanced labels; side shows recessed waist/flanged shoulders; three-quarter reveals rib and letter relief, hub, bore and rim. Required review images/settings are retained with the asset, while trial outputs and share bundles remain under ignored exports.

## Exceptions and unresolved issues

No conflicting root/axis/material interface exception is introduced. A10 approves the current 0.1.4 appearance as the cast-iron plate category visual reference. A01/A03/A04/A05/A07/A08 production decisions remain open; A06 remote LFS capacity and a full committed-checkout/LFS-fetch test remain unverified. Manufacturer-exact diameter/profile, actual mass, fabrication union, physical barbell fit and production/fabrication readiness are not claimed.

## Validation and acceptance

[Validation checklist](validation.md) and [measured results](validation-results.json) record **35 PASS, zero FAIL** for implemented technical checks, including manifold body/rib solids, four ribs per face, all four raised labels per face, actual side recess, preserved bore/dimensions/anchors, linked stack/rotated placement, no-shadow setup and five independent reference reproductions. Production gates remain NOT RUN/open as documented. Visual-reference acceptance is complete under A10. Production lifecycle remains review because nonvisual release gates remain open. Future edits invalidate affected evidence.

## Change history

| Date / version | Change | Compatibility / evidence |
| --- | --- | --- |
| 2026-10-14 / 0.1.0 | First approved review prototype, simple dish face and raised 45 LB | Initial standalone asset; source archived locally |
| 2026-10-14 / 0.1.1 | Existing profile deepened; more defined hub/rim, 3.5 mm lettering relief | Same topology/interfaces; 26 checks passed at that revision |
| 2026-10-14 / 0.1.2 plan | Recorded latest rib/lettering/side request before editing; user confirmed both units left/right on both faces | Prior detail/render evidence invalidated before edits |
| 2026-10-14 / 0.1.2 review | Added four cast ribs per face, curved generic words, dual units, recessed side waist | Existing body/object identity retained; side topology locally extended; unchanged bore/anchors/envelope; 29 checks pass |

Historical source chain: 0.1.1 SHA256 `4cab3d6b487e1f9e45dd7548cce0a4d6c42efa56812e173948939b5ad8c7fe20`; 0.1.3 SHA256 `61557cd8d31ded1c5d6700792ad8b2e7e7b6924099315056047a3d2f55d8ca13`. Historical [0.1.1 refinement record](refinement-record.json) is retained for provenance; current geometry evidence uses correction-record.json and validation-results.json.

## Approved plate direction and current feedback correction

The overall plate direction remains user-approved and asset-specific: traditional brand-neutral cast iron, matte charcoal, near-white real raised lettering, clean illustrated appearance/outlines, no shadows/AO, both weight units on both faces, four outward-tapering spokes and the structured hub/rim/waist. Current corrections implement the user's feedback; they do not change shared standards or resolve global production/licensing choices.

The previous 0.1.3 BARBELL inversion and inspection claim were rejected by user feedback. They are superseded here: a literal whole-word rotation from a clean upright upper arc, paired with a full-plate 180° proof, is now the required acceptance method. Do not restore the old per-letter inversion/tangent logic. BARBELL glyph geometry was corrected inside the existing word datablocks with STANDARD-like tracking. STANDARD's central N–D pair gains 2 mm; other spacing remains stable. Ribs retain their 34/30/20/10 mm outward width taper, with root caps at r=43 mm/Y=±14.0 mm buried beneath the hub before emerging through the shoulder.

Current source SHA256: `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`. 0.1.3 predecessor SHA256: `61557cd8d31ded1c5d6700792ad8b2e7e7b6924099315056047a3d2f55d8ca13`. [Current correction record](correction-record.json) is authoritative for this edit; finish-record.json, detail-record.json and refinement-record.json are historical only. All 15 existing objects and ten mesh datablocks remain, body coordinates/anchors and non-BARBELL topology are unchanged; BARBELL geometry is explicitly regenerated to remove the defect. Exact raised relief and all overall/interface dimensions remain.

35 implemented checks pass, including manifold body/ribs, buried root caps, monotonic taper, near-white raised letters, unchanged bore/stack/anchors, a correct 180° proof-camera transform, and independent reproduction of all five reference images. Manual visual review of the proof confirms normal upright BARBELL lettering; source tests alone are not treated as proof of typographic quality. This execution is now accepted as the visual reference under A10; no visual acceptance is pending for the pinned baseline.

| Date / version | Correction | Review / compatibility |
| --- | --- | --- |
| 2026-10-14 / 0.1.4 pre-edit | Recorded spacing, steering-wheel orientation and root-integration feedback before editing | Prior affected visual checks invalidated |
| 2026-10-14 / 0.1.4 review | Clean whole-word BARBELL rotation/spacing, +2 mm central STANDARD gap, buried/fading hub roots; added 180° proof | 35 checks pass; body/interface preserved; new typography subsequently accepted under A10 |

## Current approval and provisional-setting matrix — A10, 2026-10-14

The user explicitly approved the **current plate** as the first visual-direction reference for the equipment library and the reference standard for future cast-iron plate assets. Reference ID `cast_iron_plate_visual@1`; geometry version 0.1.4 and all render bytes remain unchanged. [reference-approval.json](reference-approval.json) pins the accepted source, five images and current settings record. Visual acceptance is complete; `status=review` is the separate production-release lifecycle, not a request for another visual approval. Internal historical review labels in the unchanged `.blend` are superseded by this external approval record; the file was not resaved just to change tags.

| Item | Current value / behavior | Approval state and scope |
| --- | --- | --- |
| Current geometry/rendered result | Exact 0.1.4 source plus front/side/three-quarter/reverse/180° proof images | **Approved visual reference**, frozen by source/image hashes |
| Appearance | Traditional cast-iron raised rim/recess/hub/waist; four tapered ribs blending into hub; matte charcoal, clean illustration and clear edges | **Approved** category visual characteristics; inherit for future traditional cast-iron plates |
| Lettering/content | Actual raised near-white mesh; 45 LB left / 20.4 KG right on both faces, STANDARD and whole-word-rotated BARBELL; corrected spacing | **Approved visual/content treatment** for this asset; other plate weights require their own nominal labels |
| Hole requirement | 50.8 mm / exactly 2 in minimum opening | **Approved explicit design requirement** for this asset; physical sleeve/manufacturing tolerance and real fit still unverified |
| Nominal weight marks | 45 lb / rounded 20.4 kg label | **Approved label identity**; density-derived mass/simulation is **unverified** |
| Outer diameter | 450 mm | **Provisional physical dimension**; approved prototype construction choice and visually accepted proportion, not measured/manufacturer-exact production size |
| Maximum thickness / pitch | 33.02 mm | **Provisional physical dimension**; manufacturer dimensional context only, not verified for this original casting or all 45 lb plates |
| Profile/rib/text numeric dimensions | Web 13 mm, hub 29 mm, rim relief 10.01 mm, waist depth 1.5 mm; widths 34/30/20/10 mm; buried root r=43 mm; 3.5 mm letter relief | **Captured approved visual implementation**, but engineering tolerances and universal dimensions remain **provisional**; preserve the accepted asset and scale/design other sizes deliberately |
| Palette | Charcoal variants #363A40/#454A51/#2A2D32/#50555C; lettering #F2F2F2 | Rendered contrast/swatches are the **approved visual comparison baseline** for cast-iron plates; shader/color-management implementation is not a universal numeric standard |
| Coordinates/interface | Meters, +Z up/+Y axial, floor root, four anchors, `olympic_plate_bore@0.1.0` | **Implemented and tested locally**; wider library ratification A03 and actual consumer compatibility remain **provisional/open** |
| Blender / renderer / shader setup | Blender 5.1.1, Workbench FLAT, roughness 1/metallic 0 display-matched materials | **Reproducibility facts**, **provisional production software/render implementation** under A01/A04; no shadow/AO appearance is approved and mandatory |
| Camera/output/outline settings | 1024 px PNG, 0.56 m orthographic scale, native Workbench lines, Standard/None, 32 AA samples, white background | Existing images are **approved evidence**; exact settings and wider export/projection/alpha/delivery standards remain **provisional** under A04/A05/A08 |
| Artwork rights / production release | Original artwork; no artwork license selected, physical consumer/checkout/LFS service checks incomplete | **Open**, not approved by visual acceptance; code/documentation MIT remains separate |

## Reference use and optional future polish

Future cast-iron plate assets inherit the [category reference characteristics](../../../../docs/category-standards.md#approved-cast-iron-plate-visual-reference), reuse shared components/material roles where appropriate, and compare rendered views against this pinned baseline. Copy visual language, not 45 lb physical dimensions or labels to every weight. Maintain named interfaces and review contacts/clearances separately. The 180° plate rotation is a required typography review case.

No polish was applied or is required for current visual-reference acceptance. Optional future work, only with authorization: inspect small-output lettering/outline legibility, consider subtle additional cast-transition fillets at extreme close-up, and verify manufacturer measurements/sleeve fit before a production release. These notes do not reopen the approved appearance or authorize a model/render change.

Preserve the current approved source/images. Future authorized edits require a retained predecessor, new version/evidence and explicit successor-reference approval. A hash mismatch must not silently become the reference. No artwork license or engineering certification follows from this approval.

2026-10-14 / documentation approval A10: current 0.1.4 accepted as `cast_iron_plate_visual@1`; approval states and provisional facts finalized; model, renders, executable scripts and measured test results unchanged.
