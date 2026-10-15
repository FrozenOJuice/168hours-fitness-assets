# Origin migration proposal — A14, 2026-10-15

**Status: approved and implemented; final validation complete.** The plan below is preserved as historical pre-migration evidence. Current applied record: [origin-migration-record.json](origin-migration-record.json).

Requested category rules are authorized by the current origin-audit request. Applying breaking changes to existing approved linked assets is a separate approval gate explicitly requested by the user. No Blender source is changed by this proposal.

Measured current roots and collection instance offsets are (0,0,0) for all three assets. Plate bore center is (0,0,0.225)m; barbell center is (0,0,0.0365)m; bench floor-footprint center is (0,0,0)m. The first two roots and linked-collection pivots therefore differ from the requested functional origins. Correct datum anchors already exist. All source geometry currently rests at floor Z0.

## Concrete proposed correction

1. Preserve the pinned approved plate/barbell source/render snapshots and introduce major interface versions before replacing published sources. Keep existing approval evidence historical; visual appearance is not redesigned or automatically reapproved as a new checksum baseline.
2. Move plate root to its bore-center datum, delta (0,0,+0.225)m; move barbell root to its axis-center datum, delta (0,0,+0.0365)m in the existing authoring frame. Keep all mesh vertices, materials, component world matrices and anchor world matrices unchanged. Recompute parent-relative matrices and remove/recalculate parent-inverse compensation deliberately; retain normalized rigid scale and documented controller rotations.
3. Set each collection's instance_offset to its new root position, so the linked-collection pivot equals the asset root. Moving only the Empty would leave collection instances rotating about the old floor pivot.
4. For every existing collection instance with matrix M, compensate by M_new = M @ Translation(delta). The effective geometry stays M_new @ Translation(-new_offset) @ vertex = M @ vertex. Update each instance in all three barbell/plate fixtures, metadata local anchor frames and placement helpers; preserve sleeve controls, drivers, constraints and every evaluated world-space mesh/anchor frame. Bench remains unchanged.
5. Validate before/after world vertices, material/topology hashes, three fixture configurations, bore/sleeve fit, root rotation/positive scale, controller spin sweeps and exact or previously documented last-bit-bounded render comparison. Audit external consumers not in this repository separately; path links elsewhere cannot be repaired by this repository audit.
6. Update source/fixture/render digests and migration records without overwriting original A10/A12 approval evidence. Record successor acceptance scope explicitly. Existing sources stay untouched until approval to perform this interface migration.

## Why approval is needed

Root and collection-pivot changes alter published transform semantics and source checksums. Uncompensated consumers translate or rotate incorrectly. User step4 explicitly requires approval before corrections that could break compatibility; AGENTS.md also requires major-version/migration review for published breaks. Bench is already compliant. No unambiguous origin deviation can be corrected here without touching these published interfaces.
