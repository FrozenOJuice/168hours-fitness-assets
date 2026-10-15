# Architecture decisions requiring approval

Status: A14 resolves the origin/axis/transform/link portion of A03; other A01–A08 global choices remain open. A10 approves the first equipment visual reference and the traditional cast-iron plate appearance standard only. The mandatory documentation/workflow requirements and the original user-specified visual direction are recorded separately below; they do not approve these technical choices. A09 authorizes the first asset-local plate review prototype; it does not select global renderer/software standards or install dependencies. Code/documentation licensing is separated from future artwork in [Licensing policy](licensing.md); an artwork license has not been selected. Proposed defaults in the other documents are planning assumptions until approved.

| ID | Decision | Proposed direction | Approval needed because |
| --- | --- | --- | --- |
| A01 | Blender baseline | Pin one supported Blender LTS version after checking the team's machines and required features; upgrade deliberately | File, rig, override, and rendering compatibility depend on it |
| A02 | Human / rig standard | One canonical skeleton and named control interface; separate mesh variants; agree rest pose, bone naming, anatomy detail, proportions, and deformation approach before modeling | Changing the skeleton can invalidate skinning, exercise actions, and constraints |
| A03 | Asset and scene interfaces | Approve meter units, axes, root placement, versioned collection/anchor interfaces, and linked collections with library overrides as documented | These contracts determine whether assets and scenes can be reused and exchanged |
| A04 | Illustration renderer | Evaluate a flat/unlit surface treatment and one outline method in the approved Blender version; require zero shadows and no ambient occlusion | Render engine, outline behavior, transparency, and animation stability affect every asset |
| A05 | Visual presets | Approve palette, muscle emphasis, outline width at output size, orthographic default, background, and color management | Consistency across stills and animations requires a shared art direction |
| A06 | Binary storage / collaboration | Use LFS for Blender and common 3D interchange sources; confirm host quota and contributor setup; consider binary locking if the host and workflow support it | Binary size and concurrent edits affect storage cost and recoverability; no locking configuration has been enabled |
| A07 | License and sourcing | Select separate terms for original models, rigs, materials, artwork, and artistic exports; define third-party intake and attribution rules | MIT covers code/documentation/templates only; future artwork terms remain open |
| A08 | Delivery formats | Agree required PNG/SVG/video/model outputs, dimensions, frame rates, alpha, export axes, and downstream platform constraints | For example, vector output requires a compatible outline/export workflow and is not guaranteed by a raster render |

## Approval process

Record the approved choice, approver, date, rationale, and any validation evidence below each decision ID when a decision is made. Update dependent conventions in the same change. Approval of this scaffold alone does not resolve these choices.

No user approval is needed to inspect the scaffold or edit the documentation. Resolve A01–A03 and sourcing terms before production modeling; resolve A04–A05 before publishing a reusable style/template; resolve A06 before committing substantial binaries; resolve A08 before building export automation. Prototype work can be authorized separately without declaring a production standard.

## Established requirements (not open technical choices)

- User project brief: clean anatomical illustrations, precise outlines, no shadows, recognizable equipment. Implementation choices remain A04–A05.
- User standards request: three documentation levels, specification before building, standardized reference evidence, validation, documentation reconciliation, reuse, compatibility, and explicit approval for shared changes. Implemented in [the workflow](asset-workflow.md) and [AGENTS.md](../AGENTS.md).
- User licensing instruction: MIT code/documentation terms remain separate from future artwork. Selecting artwork terms remains A07.

## Mandatory change and exception process

Use [the standards-change template](../templates/standards-change.md). Assign the next unused decision ID, retain `proposed` status, identify exact current/proposed values, rationale, affected consumers, compatibility impact, migration, and evidence. Asset exceptions must specify their bounded scope and mitigation and be linked from the individual spec/manifest. A proposal is not an approved baseline.

Do not implement a shared design change or conflicting exception until the user/project owner explicitly approves it. Record approver, date, choice, and approval reference. Existing session authorization counts when it explicitly covers that choice; do not ask again for the same approval. Continue documentation and independent authorized work while an affected choice is pending. After approval, update the authoritative guide and affected specs/metadata together; retain decision history and record supersession.

## A09 — First 45 lb cast-iron plate review prototype (prototype approved)

- Type: asset-local review choices; no global baseline change. Proposer: Codex, 2026-10-14.
- Scope: `168h_equipment_olympic_plate_45lb_cast_iron` only. User explicitly requested this asset; prototype settings approved by the user in this session.
- Proposed: 450 mm diameter, 33.02 mm stacking envelope, exact user-specified 50.8 mm bore; original stepped cast-iron profile and raised `45 LB` text. Blender 5.1.1 with a local flat Workbench charcoal/outline preset; no lights, shadows, cavity/AO, or ground plane. Exact colors/cameras/settings will be recorded with the prototype, not added as approved global defaults.
- Alternatives: manufacturer-specific 444.5 mm traditional plate diameter, photoreal rendering, or deferring until production standards exist. Proposed direction supports readable neutral equipment review without selecting global standards.
- Impact: no existing consumer assets or scenes; floor origin and +Y forward remain as proposed conventions. Proposed bore/stack anchors support future placement and instances; actual consumers must still be tested.
- Validation plan: measure bounds/bore/transforms, verify manifold annular body and label envelopes, render front/side/three-quarter/back, test linked collection instances and numerical sleeve/stack fixtures without authoring a barbell.
- Approval: user, 2026-10-14, response “Approve the documented review prototype” to the scoped prototype-settings question. This authorizes asset-local review construction and renders, not promotion to production standards. A01/A03/A04/A05/A07/A08 remain open for production; no artwork terms chosen.
- Migration: if production choices change, update the specification and regenerate with the recorded builder, bump interface/asset major versions for incompatible contracts, and revalidate future consumers.

A09 implementation evidence: [plate specification](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/SPEC.md), measured validation results, and front/side/three-quarter/back reference renders. Native source contains only the plate collection and floor-root/anchor interface; review cameras and link/stack fixtures are transient. Status remains review.

### A09 — Asset-specific visual direction approval, 2026-10-14

The user explicitly called the 45 lb plate visual direction approved and requested refinements while retaining the overall design/style. Approved scope: this plate's traditional brand-neutral cast-iron direction, matte charcoal body, clean illustrated treatment, precise outlines/no shadows/AO, raised dual-unit and descriptor lettering on both faces, inverted BARBELL, and four ribs tapering outward from the hub. The request authorizes local whiter/larger lettering and taper adjustments.

Implementation 0.1.3 records #F2F2F2 lettering, +8% planar size, retained 3.5 mm relief, inverted lower-arc BARBELL and 34/30/20/10 mm rib widths in the [asset specification](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/SPEC.md). These exact values are presented for review; overall direction approval does not imply global preset approval, production readiness, licensing selection or physical interoperability. A01–A08 retain their existing global status. The newly refined execution remains available for final user review.

## A10 — First equipment visual reference / cast-iron plate standard (approved)

- Approver/date: user, 2026-10-14. Explicit instruction: “Approve the current 45 lb Olympic plate as the first visual-direction reference asset for the 168Hours Fitness equipment library.”
- Accepted artifact: `168h_equipment_olympic_plate_45lb_cast_iron` **0.1.4**, source SHA256 `b56d464dfcb9881b944acb7d13501c3e3ebc1e22bfa34690295a47be9fd941f2`, five existing reference/proof images pinned in [reference-approval.json](../assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/reference-approval.json).
- Result: current visual reference **`cast_iron_plate_visual@1`**, first in the equipment library; authoritative inheritance rules in [category standards](category-standards.md#approved-cast-iron-plate-visual-reference). Current geometry and rendered appearance are visually accepted, including corrected BARBELL rotation/spacing, STANDARD spacing and integrated tapered rib roots. This supersedes the pending visual acceptance of 0.1.4, not the historical rejection of the earlier lettering.
- Approval scope: cast-iron plate appearance, proportion language, material/letter contrast, raised geometry and shadow-free illustration. The exact existing rendered result is the visual comparison baseline.
- Not approved by inference: manufacturer-exact diameter/thickness/profile dimensions, physical mass/fit, global skeleton/interface/Blender/renderer settings, universal pixel line width, delivery formats, LFS service capacity or artwork licensing. Explicit prior 50.8 mm bore/nominal-label requirements remain approved for this asset.
- Lifecycle: `visual_reference.status=approved`; `asset.json.status=review` continues to describe production-release progress, with `production_release.status=not_ready`. Visual reference designation is complete and usable now; production gates remain explicit.
- Change control: documentation only in this approval step; source and all PNG bytes unchanged. Keep the pinned baseline intact. A future authorized variation must retain predecessor evidence and record a versioned replacement/approval before superseding the reference. No polishing is requested now.

## A11 — 20 kg barbell review prototype / proposed load interface

- Scope: [barbell 0.1.0](../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/SPEC.md) and its [linked compatibility fixture](../scenes/templates/168h_template_barbell_plate_compatibility/SPEC.md) only. User, 2026-10-14, explicitly requested construction and testing and instructed “Keep this a review prototype until we approve its design. Do not change shared standards without approval.” This authorizes scoped prototype work; appearance/global contracts are **not approved**.
- Implemented local proposal: `olympic_barbell_load@0.1.0`, +X shaft, floor root, outward load frames (+Y onto ±X), separate independent sleeve pivots driven by overridable degree properties. Common naming/units/relative linking proposals are followed, no incompatible exception or plate modification.
- Dimensional context: 2200 mm length, 28 mm shaft, 1310 mm exposed spacing, 50×415 mm sleeves, 30 mm integrated shoulders, 73 mm flange diameter. Sources and distinction between published dimensions, measured digital geometry and provisional details are in SPEC. No hardware/competition certification. The integrated shoulder is part of each sleeve, not a removable collar.
- Pending design approval: 28 mm weightlifting shaft and center knurl vs hybrid/powerlifting variants; knurl contrast/depth; silver bands/material parameters; sleeve/end-cap detailing; local anchor/controller contract. Silver preset is local, not shared; other variants/new shared palette or renderer require separate proposals.
- Evidence: 34 automated checks PASS, no FAIL; six retained views; linked 45 lb plate on each side, ~0.39998 mm radial clearance, ~1 mm flange gap, no mesh crossings, exact standalone references and bounded last-bit assembly differences. No alternative barbell or plate replacement, humans or authored override actions tested. Original plate source and all artifacts unchanged.
- Migration: keep interface proposed until explicit approval. Consumers declare interface/version and actual sleeve/stack envelopes; dimension/anchor/slot breaks require version/migration review. Scope of any approved shared promotion must be recorded before changing category/common guides.
- Approval state: prototype creation authorized; **user visual/design acceptance pending**. A01/A03/A04/A05/A06/A07/A08 remain open; no artwork license selected. No global or cast-iron visual standard changed.

### A11 — 0.1.1 existing-asset refinement (review, no shared promotion)

User authorized smoothing sleeve ends/steel values, manufacturer dimension review, realistic plate packing with collar space and multi-plate evidence while retaining the attachment system. Current 0.1.1 edits existing sleeve/cap geometry locally, keeps all object/data identities, shaft geometry, load frames, dimensions and independent sleeve controls. Current appearance remains pending user review; no global/cast-iron standards changed.

Manufacturer recheck supports the existing 2200/1310/415/50/28 mm overall/exposed shaft/sleeve/sleeve diameter/shaft dimensions. No sleeve shortening was justified. Existing33.02 mm cast-iron plate envelope matches published1.3 inch thickness context. Documented50 mm collar length allowance,5 mm tip margin,1 mm flange gap and0.5 mm neighboring gaps yield10 plates/sleeve; an11th exceeds by9.22 mm. Collar interpretation/margins are local assumptions, not production tolerance approval; no collars created. Source URLs, sensitivity, calculated/read values and limits in the asset SPEC/capacity-calculation.json.

46 checks pass including all20 linked-plate positions, symmetry, positive clearance, zero80-pair mesh crossings and nine reference comparisons. Original plate and normative guides unchanged. Updated silver values/knurl contrast, local contract, software/renderer/delivery/artwork terms and hardware fit/load ratings remain review/open. This extends A11's authorized prototype scope and does not approve shared numeric standards.

### A11 —0.1.2 review and presentation example (no dimensional changes)

User requested manufacturer compatibility findings before dimension edits, a slight steel contrast increase and a4–5 plate example. Findings in the barbell compatibility-review.md were recorded first: retain415mm sleeves and33.02mm plate pitch; ten remains a packing maximum with documented50mm collar/5mm tip/scene gaps. Approved450mm plate differs from the cited444.5mm manufacturer's product; it is an original reference, not a replica, so no correction is authorized or recommended for this scope.

Authorized implementation changes existing prototype steel swatches only (1.18 contrast about0.72) and creates a five-per-sleeve linked partial-stack example. All mesh coordinates/topology/face slots, transforms, named interface and approved plate are preserved.55 checks pass across single/five/ten cases and12 references. No shared numerical standards ratified. User appearance approval, actual collar/manufacturing fit, artwork/global production decisions remain open. Ten images remain diagnostic; five is the requested presentation example.

## A12 — Approved20kg barbell / internal library production readiness

Approver:user,2026-10-14. Explicit instruction: “Finalize and approve the20kg Olympic barbell as a production-ready asset for the168Hours Fitness library.” Accepted existing geometry0.1.2 and captured materials/style/settings, `olympic_barbell_load@0.1.0`, verified manufacturer dimensions and saved five-plates-per-sleeve reference. Exact hashes and original approval wording in the barbell approval-record.json.

Status ready/approved for **internal reusable Blender illustration production**; all55 existing barbell checks PASS and35 plate checks PASS on an isolated copy. Native geometry/material/render bytes preserved. Ten-per-sleeve packing result and50mm collar/5mm tip/scene gaps are accepted documented illustration assumptions, not hardware/strength certification. Five is the presentation reference; ten remains diagnostic maximum.

A12 supersedes A11's pending asset-local acceptance and prototype-only status for this existing barbell. It does not change global technical standards or the approved plate; existing globals A01–A08 retain their separate status. Original artwork can be used internally as explicitly requested; no external artwork licensing/redistribution grant is selected or inferred. MIT code/docs remain separate. Local commit/LFS reproducibility QA will be recorded; remote upload/quotas are outside the requested commit. No new models or unrelated asset edits.


## A13 — Standalone flat utility bench prototype (design approval pending)

- User,2026-10-14, authorized a standard commercial standalone flat bench, explicitly review prototype; no rack/human/exercise scene or shared-standard change. [Specification](../assets/equipment/benches/168h_equipment_flat_bench/SPEC.md) records scoped choices before build, manufacturer facts and provisional geometry/interfaces/settings.
- Proposed asset `168h_equipment_flat_bench`0.1.0; `bench_support@0.1.0`, floor root, length/head+Y, width+X. Fixed pad angle0°. Geometry13 meshes/8 unique data blocks; feet/rails/boots shared. No approved plate/barbell changes.
- Dimensional context from [Rogue Flat Utility Bench2.0](https://www.roguefitness.com/rogue-flat-utility-bench-2-0), consulted2026-10-14: 47/14/18in overall,12in pad width,2.5in pad thickness. Local pad-length inference1193.8mm, support layout/1025mm ground footprint, rounded edges/substrate/foot details remain provisional. No physical load certification or exact manufacturer replica claimed.
- Review choices: matte charcoal pad/frame face values, existing shadow-free Workbench capture settings scoped locally; proposed support anchors and generic sloped-leg/two-foot construction. User must review bench appearance/proportions and anchor proposal before readiness. A01–A08 and shared style/category standards remain unchanged.
- Evidence:47 prototype checks PASS, four retained views manually inspected and exactly reproduced; two original-source collection instances and rotated back-support frame alignment checked. No human/rack/alternate bench compatibility certified. No conflicting exception or migration required for existing consumers; future dimensional/interface breaks must be versioned/retested.
- Separate artwork terms and release gates remain open. This entry records authorized prototype work, **not design acceptance or a new category/global standard**.


### A13 refinement0.1.1 — authorized, design approval still pending

User requested in-place commercial-quality refinement. All original bench objects/data identities, main frame/substrate geometry, pad topology, root/anchors, nominal dimensions and material roles preserved. Cushion roll/corners and subtle geometry upholstery seam refined; rounded tapered rubber shoes replace blocky profiles in the original shared data; upper gussets, saddle plates and reusable fasteners added. Manufacturer dimensional reference rechecked; no overall scaling correction. 72 saved-source checks PASS plus exact four-view reproduction. Original0.1.0 is retained in the asset history folder for reproducible preservation QA. New details remain provisional, no fabrication/load rating inferred. Review lifecycle and open global standards unchanged.


## A14 — Functional equipment origins and approved linked migration (2026-10-15)

User requested intentional category roots, axes, root/object distinction, anchors, normalized transforms, generic automation and safe corrections. Explicit follow-up approval: **“Approve the root/pivot migration and fixture updates.”** [Concrete proposal](audits/origin-migration-proposal.md), [applied record](audits/origin-migration-record.json), [current audit](audits/origin-audit-results.json), [regression](audits/origin-migration-validation.json).

Approved scope: plate root at bore center, barbell root at midpoint, bench at centered floor support; collection pivots coincide with roots. Common+Z up/+Y front/+X subject-left; plate bore+Y, bar shaft+X, bench length+Y. Declared authoring translations and proper shared-component rotations allowed; unit positive scale, full root-local anchor frames and offset-aware linked placement required. Root changes are interface-major migrations, not visual redesigns. Plate/barbell become1.0.0 with geometry0.1.4/0.1.2 unchanged; bench0.1.1 source unchanged. Three fixture sources compensated and versioned1.0.0. Original native files, references and approval records retained under audits/origin_baseline; existing visual/artwork approval scopes unchanged. A03 origin/axis/transform/link portion is resolved by A14; other open design/software/licensing decisions are not ratified by inference.

Four assembled reference images require refresh due float/anti-alias rounding at<=3/255 on<0.0024% channels; original evidence retained and differences in origin-render-refresh.json. Standalone appearances unchanged exactly; refreshed current references must pass original reproduction tolerances. No standard/tolerance is silently relaxed. External linked consumers outside this repository must migrate deliberately using the documented compensation; none were inspected or modified.


### A14 finalization — approved and complete,2026-10-15

User requested final validation and commit if all checks pass. All375 current checks PASS (297 origins,28 preserved-geometry/world/render,42 all-fixture stacking/clearance,6 failure injection,2 placement). Native source bytes unchanged during finalization; original approval evidence retained. Existing root/axis/transform/link standards enforced by metadata/rules and default validator entry points. Bench remains review/not_ready; no model redesign, new visual standard or artwork license. This finalized snapshot is recorded by its repository commit.
