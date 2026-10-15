# Code and artwork licensing

## Code and supporting text

The MIT terms in [LICENSE](../LICENSE) apply to original repository code, automation, documentation, and metadata templates. The existing MIT grant and copyright notice are retained with an explicit scope statement.

## Future 3D artwork

3D models, rigs, materials, textures, artistic content in Blender scenes and scene templates, renders, animations, and other artistic deliverables are outside the code license. A script embedded in a Blender file remains code; the surrounding artistic content requires its own terms. Exporting or changing file format does not change licensing scope.

No artwork license is selected by this scaffold. Select and approve artwork terms under decision A07 before releasing artwork. Do not label future artwork MIT merely because it lives in this repository. Until explicit terms are approved, this repository provides no artwork reuse grant.

For each future asset, record creator, origin, license identifier or full terms reference, attribution requirements, and relevant usage restrictions in `asset.json`. Place asset-specific terms in its folder as `LICENSE.artwork` when needed; record a repository-relative path or authoritative URL in metadata. Keep code and artistic dependencies distinguishable when packaging scenes or exports. Unknown licensing blocks `ready` status.

## Third-party content

Third-party models, textures, fonts, scripts, and other dependencies retain their original licenses. Record their provenance and confirm the intended redistribution and export use is permitted before inclusion. Preserve required notices and attribution with the asset and its deliverables. The MIT code license does not replace third-party terms.
