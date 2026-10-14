# Asset review checklist

Use for future assets; no assets exist to review yet. Manual checks are intentional at this stage. Add automation when the approved Blender baseline and interfaces are implemented.

## Sources and identity

- Stable ID, category, filename, collection, root, and metadata agree.
- Version and review status are explicit; breaking interface changes have a major version.
- Provenance, usage rights, attribution, and measurement sources are recorded. Artwork terms are explicit and separate from the MIT code license; see [Licensing policy](licensing.md).
- Source opens in the pinned Blender version without missing data or unapproved add-ons.

## Geometry and interface

- Dimensions match recorded measurements and tolerance, in meters.
- Axes, root, rest configuration, and transforms follow conventions.
- Published anchors have the declared names and frames, and move with relevant bones/mechanisms.
- Rig/control and material-slot contracts match the declared interface version.
- Dependencies resolve with relative paths from a fresh clone with LFS content retrieved.
- A compatible replacement is exercised in a representative scene; placement, posing, support, grip, and collision/clearance are reviewed.

## Style and delivery

- Anatomy and equipment read clearly at output size in representative views.
- Outline width is consistent, including internal overlaps and animation frames when applicable.
- No cast shadows, contact shadows, ambient occlusion, or baked shadows appear.
- Camera, palette, color management, resolution, background, and alpha match the approved preset.
- Export format, axes, units, and motion settings match downstream requirements.
- Export metadata records the source revision, asset versions, preset, and Blender version.
- Generated files, caches, backup saves, and temporary downloads are excluded from Git.
