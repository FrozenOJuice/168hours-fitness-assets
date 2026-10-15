# Linked barbell / plate fixture validation

0.1.2, approved internal illustration reference, Codex 2026-10-14. [Specification](SPEC.md), [metadata](asset.json), [result pointer](validation-results.json). Shares the barbell's [full checklist](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/validation.md) and [measured results](../../../assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/validation-results.json); no competing validation system.

| Check | Result | Evidence |
| --- | --- | --- |
| Relative dependencies | PASS | Existing one-plate and capacity native files reopen with original source links |
| No geometry copies | PASS | Primary2, capacity20 and example10 plate collection instances; no local meshes |
| Plate pitch/capacity | PASS | 33.020001 mm, 10/side, collar50 + tip5 mm reserved; eleventh exceeds9.22 mm |
| All aligned and symmetric | PASS | all_capacity_plate_alignment_clearances / capacity_stack_symmetry_and_no_plate_intersections |
| Clearance and intersections | PASS | ~0.400 mm radial, ≥0.49988 mm stack gap; 80 broad-phase pairs, zero crossings; separating envelopes exclude containment |
| Attachment/spin invariance | PASS | Original load frames and controllers retained; sampled source spin and transformed placement pass |
| Render evidence | PASS | Seven assembled references, recorded native source per view; exact or previously documented1/255/<0.1% comparison |
| Plate/standards preservation | PASS | Protected hashes unchanged |
| Fresh committed local checkout/LFS | PASS |5 native objects fetched/checked out,fsck and55+35 checks pass |
| Hardware/collar fit, physical loads, other replacements/override actions | N/A — excluded scope | Unverified; no such claims |
| User design approval | PASS | A12 internal illustration scope; external artwork terms and global defaults remain outside scope |

No source geometry/anchors are edited in either fixture; only collection instances and cameras are local. Approved plate remains immutable. Open the primary .blend for two plates or __capacity.blend for20 plates. Any later source/interface/material/camera edits invalidate affected evidence.

Five-example checks PASS:10 linked plates, zero local geometry, positive0.5mm complete-envelope gaps,191.90mm spare after collar/tip reserve, symmetric aligned placement and zero40-pair plate/bar crossings.55 aggregate machine checks pass; no geometry or shared-guide changes. Sources and per-view comparison results are pinned in the barbell validation-results.json.

A12: user production approval complete for existing native barbell/five-plate example; no artifact resave or redesign.55 barbell and35 isolated plate checks pass. External redistribution/hardware certification/global standard approval remain excluded; current internal illustration readiness is approved.
