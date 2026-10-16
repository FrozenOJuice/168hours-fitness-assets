# Human V1 schemas

These Draft2020-12 schemas extend the existing asset metadata system. They do not
replace asset.json or the asset workflow. The official contract is
[Human V1](../docs/contracts/human-v1/README.md); normative inputs are checksum
pinned in its contract-lock.json.

| Schema | Use |
| --- | --- |
| human-character-v1.schema.json | Companion human-contract.json: body/rig interfaces, controls, measured profile, masks, anchors, constraints and export/evidence declarations |
| human-snapshot-v1.schema.json | Read-only Blender observations, distinct from self-declared metadata |
| human-muscle-catalog-v1.schema.json | Stable bilateral muscle/region/aggregate registry |
| exercise-muscles-v1.schema.json | Future exercise primary/secondary assignments; does not create an exercise |
| human-export-v1.schema.json | Proposed/approved output-profile settings; does not implement an exporter |

Use the Python validator for semantic checks across the schemas and canonical
registries. It implements only the vocabulary these files use, rejects unknown
keywords and nonfinite/duplicate-key JSON, and needs no installed schema package.
A schema-valid draft with empty maps is not a compatible character. `--release`
requires observed source/profile identity, approved/pinned profiles and retained
manual/integration evidence; structural declarations alone never certify export,
clothing visibility, anatomical boundaries or animation quality.
