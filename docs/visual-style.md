# Visual style proposal

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

Define outline thickness in final-image pixels and test it at the intended delivery resolution; do not bake resolution-dependent strokes into geometry. Exact palette, line width, color management, render engine, and outline implementation are pending approval.

## Visual acceptance

Review front, side, and three-quarter views at actual delivery size. Confirm anatomy and equipment remain recognizable, silhouettes do not merge, grip/support points read clearly, and there are no cast/contact shadows or ambient occlusion. Compare the same style on a human and on equipment before approving a preset. No sample model or render is included in this scaffold.
