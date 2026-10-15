# Flat bench0.1.2 final approval validation —2026-10-15

**PASS / approved / ready for internal Blender illustration/library use.** User requested final approval conditional on validation. [Approval record](approval-record.json) pins source/settings/four PNGs. Pre-approval documentation retained in history/0.1.2-review; earlier migration and refinement evidence remains historical.

| Gate | Result and evidence |
| --- | --- |
| Specification before build and refinements | PASS: build-record.json, refinement-plan.json, visual-refinement-plan.json |
| Identity/naming/components/material roles | PASS:30 meshes,16 unique data; original object frames and semantic slot order retained; visual-validation-results.json |
| Dimensions | PASS:355.6×1193.8×457.2mm overall within1e-6m; pad304.8mm wide,63.5mm thick, top457.2mm; manufacturer context/inferred details distinguished in SPEC |
| Functional origin/collection pivot | PASS:(0,0,0) centered floor support, equipment_origins@1 |
| Axes/transforms/anchors | PASS:+Zup/+Yhead/+Xwidth; normalized rigid transforms and7 full root-local anchor frames;144 origin checks |
| Geometry/topology/contact | PASS:161 geometry/material/reuse checks; manifold outward meshes, no foam/frame penetration; intended structural joints documented |
| Relative dependencies and reuse | PASS:no external artwork dependencies; two linked instances share source geometry, full-frame back_support placement; no copied meshes |
| Replacement/animation/human/rack | Not claimed: no alternate bench, human or rack consumer exists; fixed-flat0° only; consumers must validate contacts |
| Visual/style | PASS:four1600×1000 views inspected; charcoal/clear outlines, FLAT, no cast/contact shadows, AO/cavity/specular or branding |
| Reference reproduction | PASS:four exact decoded comparisons, zero changed channels; saved master never resaved |
| Approval and licensing | PASS:user approves current asset for internal library use; original geometry provenance; no external artwork grant; MIT code/docs separate |
| Export/physical certification | N/A: no interchange format, fabrication, load rating or physical simulation advertised |
| Shared standards/other approved assets | PASS:protected files unchanged; asset-local approval only |

Current commands from repository root: Blender5.1.1 --background --factory-startup --python-exit-code 1 --python scripts/blender/validate_flat_bench.py; repeat with reproduce_flat_bench_renders.py. Historical builders/refiners must never be rerun over this approved source. Approval is invalidated by future native/render changes. Final additional regression and packaging checks are recorded in documentation-check.json.

Fresh committed local Git/LFS checkout PASS:15 LFS sources/fsck,161 geometry+144 origin checks,4 exact render comparisons. Tested commit and report digests in documentation-check.json.
