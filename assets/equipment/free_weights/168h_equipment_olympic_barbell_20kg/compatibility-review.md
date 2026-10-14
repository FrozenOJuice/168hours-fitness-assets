# Barbell / approved plate compatibility review

2026-10-14, before the 0.1.2 appearance/example update. This review extends the existing asset SPEC and capacity-calculation.json; it is not a new shared standard. User requested dimension verification and recommendations before dimensional edits, a slight steel-contrast increase and a 4–5-plate example. **Recommendation: no dimension changes.** The approved plate and all global/category standards stay unchanged. Proceed only with the explicitly authorized prototype material-value refinement and five linked plates per sleeve. Source assets and evidence were archived locally before this step under exports/models/barbell_review_history/0.1.1.

## Manufacturer comparison

Sources checked 2026-10-14; original geometry, no manufacturer artwork imported. All dimensions below are millimeters unless stated. Digital values are measured model values, not physical manufacturing measurements/tolerances.

| Item | Current design / digital measurement | Published reference | Finding / recommendation |
| --- | --- | --- | --- |
| Bar overall | 2200 / 2200.000048 | Eleiko 2200 | Retain |
| Exposed shaft | 1310 / 1310.000005 between flange faces | Derived from Eleiko 2200−2×(415+30)=1310; standard Olympic context | Retain; hidden internal axle mesh length 2188 is not grip length |
| Shaft diameter | 28 | Rogue Olympic Weightlifting Bar 28 | Retain; center knurl is variant-specific, not a requirement of every manufacturer bar |
| Sleeve loadable length | 415 / 415.000016 | Eleiko415; Rogue16.30in=414.02 | Retain; 415 is a real manufacturer dimension, not excessive geometry |
| Sleeve diameter | 50 | Eleiko50 | Retain |
| Integrated flange width / diameter | 30 / 73 | Eleiko width30; historical IWF rim minimum73 | Retain; exact flange shape/diameter is prototype detail, not an exact Eleiko replica |
| Plate stack envelope | 33.02 / 33.020001 | Rogue45lb traditional cast iron1.3in=33.02 | Retain; thin cast iron is not a bumper plate |
| Plate outer diameter | 450 / 449.999988 | Rogue45lb17.5in=444.5 | Original approved visual plate is not a Rogue replica. Difference5.5mm (1.2373%) does not affect axial capacity. Keep approved asset unchanged |
| Plate minimum bore | 50.8 / ~50.799982 | User explicitly approved exactly2in | Retain; against modeled50mm sleeve yields~0.39998mm radial clearance; real fit unverified |
| Collar allowance | 50 | Eleiko Lock-Jaw Pro2 length50 | Sourced product length interpreted as axial occupancy; verify actual collar selection/orientation before production |

References: [Eleiko 20kg bar](https://media.eleiko.com/admin/download-product-sheet.aspx?articlecode=3070100&language=en-us), [Rogue 20kg bar](https://www.roguefitness.com/rogue-olympic-weightlifting-bar-stainless-steel), [Rogue traditional plates](https://www.roguefitness.com/rogue-olympic-plates), [Eleiko collar](https://media.eleiko.com/admin/download-product-sheet.aspx?articlecode=3060925&language=en-us). Published dimensions support the chosen prototype; they do not certify this original mesh or establish universal hardware dimensions.

## Capacity with collars

Keep the existing explicit assumptions: L415 sleeve, t33.02 actual plate envelope, C50 collar occupancy, E5 tip margin, F1 initial flange gap, g0.5 between complete plate envelopes. Tip reserve keeps the collar away from the modeled1.5mm end chamfer. F/E/g are local scene allowances, not manufacturer tolerances.

`n_max = floor((L-C-E-F+g)/(t+g)) = floor(359.5/33.52) = 10` per sleeve.

| Plates per sleeve | Plate stack incl. interplate gaps | Sleeve used incl. flange/collar/tip allowances | Spare after all allowances |
| --- | --- | --- | --- |
| 4 | 133.58 | 189.58 | 225.42 |
| 5 — requested example | 167.10 | 223.10 | 191.90 |
| 10 — diagnostic maximum | 334.70 | 390.70 | 24.30 |
| 11 | 368.22 | 424.22 | −9.22 (does not fit) |

With g=0 and the same50mm collar,5mm tip and1mm flange reserve, capacity is still10. With a hypothetical38mm collar it can be11; with70mm it remains10. These alternate collar values are sensitivity scenarios, not verified products. Ignoring the tip reserve/gaps allows11+50mm collar with only0.78mm to nominal tip, inside the modeled end-chamfer region; that is not the usable reviewed setup.

Ten is a plausible **geometric packing maximum for these thin plates and this collar allowance**, not a universal plate count, typical exercise load, load rating or strength/dynamics result. Four/five plates are illustrative partial stacks. Increasing plate thickness or shortening sleeves solely to force4–5 as maximum would contradict the cited dimensions. Actual casting/lettering/collar tolerances may change the result.

## Recommended action and approval boundaries

1. Retain bar dimensions, plate dimensions, bore/stack anchors, origins and controls.
2. Keep ten-per-sleeve as a labeled diagnostic capacity fixture; present a separate five-per-sleeve linked example as the main new visual example. No plate geometry duplication and no collar asset authored.
3. Increase only barbell-local soft-steel swatch contrast about sRGB0.72 by a factor1.18. Preserve broad smooth gradients, current material names/slots, mesh face assignments, actual knurl geometry, metallic0.85/roughness0.48, outlines, no shadows/AO. This is explicitly requested prototype appearance work, not a shared palette change.
4. Do not modify the approved plate to444.5mm. If a manufacturer-exact replica is desired later, propose a separately versioned variation, migrate floor/bore anchors and revalidate with explicit approval first.
5. Keep artwork terms/global render choices/physical hardware fit and engineering verification open. Revalidate current digital dimensions and single/five/ten linked configurations after the appearance-only edit; record evidence separately from production readiness.

No dimensional edit is authorized or necessary in this step. Findings and this recommendation are recorded before the source is modified.
