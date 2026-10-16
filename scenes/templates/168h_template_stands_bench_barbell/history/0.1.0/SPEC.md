# Linked stands/bench/barbell review fixture

Review0.1.0; technical assembly only, no humans or exercise animation. Links independent stand pair, approved bench0.1.2 and barbell1.0.0; dependency digests and actual instance frames recorded after construction. Setup, assumptions and geometry contacts inherit the stands SPEC.md. Bench+Yhead atfloor0; stands rotatedZpi atY.58, bar placed automatically using support/axis frames. Unloaded bar, no plates/collars. Contact planes tangent, all other asset surfaces disjoint. Original sources protected by prebuild-record.json. References and numerical/BVH/reproduction results to be recorded after QA.

## Completed review evidence

Saved source relative-links all3assets; no local copied meshes. Bar axis_center placed at(0,.44,.942)m with canonical shaft+X, level/tangent to both actual lined supports. Bench root(0,0,0); pair floor at(0,.58,0) rotatedZpi.75mm axial hook-to-flange margin,73.75mm inner base-to-bench envelope clearance; shaft484.8mm above pad.449geometry/compatibility checks PASS, zero triangle crossings;243source origin details PASS. Controls tested across16detents and independently, but this saved fixture uses equal index0 only; no human, lifting animation or load certification. Sources unchanged.

Three reference views under previews (assembled,side,front), indexed with source/preset/image hashes in asset.json. Current exact-pixel reproduction FAIL on tiny edge/depth differences; not waived and no production approval. See source asset render-reproduction.json and validation.md for metrics/limitations. Review status remains. Source/root/anchor bug corrections are documented in build-record.json and stand SPEC.
