# Generated exports

Store model deliverables in `models/`, still images in `illustrations/`, and motion deliverables in `animations/`. Contents are ignored by Git except this file and folder placeholders; authoritative sources belong in `assets/` or `scenes/`.

Proposed layout: `<type>/<scene_or_asset_id>/<version>/<preset>/`. Use filenames `<asset_or_scene_id>__<view_or_action>__<preset>.<ext>` and retain an export manifest alongside each batch with source Git revision, asset versions, Blender version, output settings, units/axis conversion, and provenance. Do not put timestamps in stable asset IDs.

Formats and delivery specifications require approval (A08). No exporter or export files have been created. If a release needs tracked deliverables, agree a release-artifact storage policy rather than bypassing ignore rules ad hoc.
