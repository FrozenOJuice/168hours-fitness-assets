# Global style guide

Level 1 of the [documentation system](asset-workflow.md). This extends the original visual direction; it does not select open technical settings. Individual assets reference this guide and approved presets instead of redefining them.

## Standards and approval status

| Area | Approved direction / mandatory requirement | Undecided implementation |
| --- | --- | --- |
| Illustration | User-specified clean anatomical illustrations and recognizable equipment | Exact anatomical detail and emphasis rules (A02, A05) |
| Outlines | Precise, readable, consistent outlines | Method and thickness at output size (A04, A05) |
| Lighting | User-specified no shadows; omit cast/contact shadows, ambient occlusion, and baked shadows | Renderer and flat/unlit material setup (A04) |
| Colors | Shared semantic palette; no asset-specific palette drift | Actual color values and muscle-highlight roles (A05) |
| Materials | Reuse shared semantic materials and preserve slot interfaces | Node implementation, surface parameters, and approved swatches (A03–A05) |
| Cameras | Consistent reference framing and readable contacts | Orthographic default is proposed; exact projection, transforms, margins, and scale (A05) |
| Rendering | Reproducible presets and reference evidence are mandatory | Blender version, engine, sampling, color management, resolution, alpha/background, and output formats (A01, A04, A05, A08) |

The visual direction comes from the user's project brief. The workflow/documentation requirements come from the user's standards request. The first [cast-iron plate visual reference](category-standards.md#approved-cast-iron-plate-visual-reference) is approved under A10, including its rendered charcoal/near-white appearance and structural/typographic treatment. Its captured settings reproduce that reference; numerical camera/render/software values are not thereby ratified as library-wide defaults. Record proposals and approval evidence in [Decisions](decisions.md) before establishing or changing shared values.

## Intent

Create clean anatomical illustrations with precise outlines, no shadows, and recognizable equipment. Clarity of movement, anatomy, and contact points takes priority over surface realism.

## Appearance

- Human anatomy: readable proportions and simplified muscle groups; use restrained color to distinguish primary and secondary muscles. Anatomy detail should support the exercise explanation.
- Equipment: preserve identifying silhouettes, handles, pads, plates, adjustment points, and functional proportions. Avoid decorative details that obscure mechanics.
- Outlines: crisp, consistent visible silhouettes with selective interior lines where anatomy or overlapping parts need clarification. Avoid noisy triangulation or outlines around every polygon.
- Surfaces: flat, controlled color with no cast shadows, contact shadows, ambient occlusion, or baked shadow textures. Prefer flat anatomical color regions to lighting gradients.
- Background: clean solid background or transparency according to the approved output preset. No ground-plane shadow.
- Framing: consistent subject scale and margins, with camera views that reveal movement and equipment contact. Orthographic projection is the proposed default; perspective may need a separate equipment preset.

## Reusable style controls

Separate palette, outline width, anatomy emphasis, camera projection, resolution, background, and color-management settings from asset geometry. Store approved style presets under `assets/styles/` and reusable camera/render setups under `scenes/templates/`.

Define outline thickness in final-image pixels and test it at the intended delivery resolution; do not bake resolution-dependent strokes into geometry. Global numeric palette, line width, color management, render engine, and outline implementation remain pending approval. A10 approves the rendered cast-iron reference appearance and palette as a comparison baseline, with its technical production settings still provisional.

## Visual acceptance

Review front, side, and three-quarter views at actual delivery size. Confirm anatomy and equipment remain recognizable, silhouettes do not merge, grip/support points read clearly, and there are no cast/contact shadows or ambient occlusion. Compare the same style on a human and on equipment before approving a preset. The [approved 0.1.4 plate reference](category-standards.md#approved-cast-iron-plate-visual-reference) establishes the current traditional cast-iron plate visual family. It does not establish a human/machine geometry standard or a library-wide technical render preset.

## Mandatory reference-render protocol

Every completed asset must have a retained review set and sufficient settings to reproduce it. Once an approved preset exists, use the same preset revision, resolution, pixel outline width, palette, color management, and framing rule across comparable assets. Record any approved category variation; never silently tune the global style for one asset.

Required baseline views: front (camera on +Y looking toward the subject), side (camera on +X looking toward the subject), and three-quarter (camera on +X/+Y). Exact elevation, distance/orthographic scale, camera roll, subject bounds, and margins must come from the approved preset and be recorded. Add views of hidden attachment points, extremes of supported adjustment, and contact-critical motion frames. Rigs, materials, and styles use a named reproducible preview fixture; an approved alternate set may replace irrelevant views with a documented reason.

Retain selected review images under `<asset_directory>/previews/`, named `<asset_id>__<view>__<configuration>.<approved_ext>`. These are required documentation evidence, distinct from disposable exports. Link each image from `SPEC.md` and `asset.json`; record view, configuration/frame, source Git revision or file digest, and preset revision. Keep `previews/render-settings.json` alongside them with actual Blender/add-on versions, render engine, camera transforms/projection/framing, resolution, color management, palette/material versions, outline settings, lighting, background/alpha, sampling, and seed where applicable. Include reproduction commands or manual steps in `SPEC.md`.

Review at actual delivery size for anatomical/equipment recognition, silhouette separation, internal line quality, contact readability, and absence of all shadows. Before visual approval, undecided render choices must be labeled provisional. A user may approve a pinned rendered result as a visual reference while its underlying renderer/delivery settings remain provisional for broader production use; record those separate states as in A10. Do not infer technical or licensing approval from appearance approval.
