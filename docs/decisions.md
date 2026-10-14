# Architecture decisions requiring approval

Status: all decisions below are open. The scaffold does not install dependencies, author models or choose a renderer. Code/documentation licensing is separated from future artwork in [Licensing policy](licensing.md); an artwork license has not been selected. Proposed defaults in the other documents are planning assumptions until approved.

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
