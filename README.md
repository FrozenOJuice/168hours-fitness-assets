# 168Hours Fitness — Blender Asset Library

A modular library for reusable human models, rigs, fitness equipment, materials, exercise scenes, and scene templates.

**Status:** the [45 lb cast-iron plate, geometry 0.1.4](assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/SPEC.md), is the **first approved equipment visual-direction reference** and current [traditional cast-iron plate visual standard](docs/category-standards.md#approved-cast-iron-plate-visual-reference), approved 2026-10-14 under A10. Its model and five renders are pinned in [reference-approval.json](assets/equipment/free_weights/168h_equipment_olympic_plate_45lb_cast_iron/reference-approval.json). Visual approval is complete; production dimensions/fit, global software/render/export choices and artwork terms remain explicitly provisional/open. No redesign was performed during approval.

## Current library assets

- [20 kg Olympic barbell](assets/equipment/free_weights/168h_equipment_olympic_barbell_20kg/SPEC.md), 0.1.2, **approved and production-ready for internal Blender illustration use** under A12: preserved steel finish/knurling, independent sleeves and validated plate anchors. Exact source/images and five-plate example pinned in its approval-record.json; external artwork licensing and physical load certification are not claimed.
- [Linked barbell / plate compatibility fixtures](scenes/templates/168h_template_barbell_plate_compatibility/SPEC.md): digital alignment/clearance/intersection tests, original approved plate linked in one-per-sleeve, five-per-sleeve presentation example and calculated ten-per-sleeve diagnostic configurations; collar allowance reserved. This is a technical fixture, not an exercise scene or approved shared template.

## Library structure

```text
assets/
  humans/
    models/              # Body geometry and anatomical variants
    rigs/                # Reusable deformation and control rigs
  equipment/
    free_weights/        # Dumbbells, barbells, plates, kettlebells
    benches/
    racks/
    machines/
  materials/             # Shared material and node-group libraries
  styles/                # Reusable illustration treatments and palettes
scenes/
  exercises/             # Linked assets, exercise poses, and choreography
  templates/             # Cameras, framing, backgrounds, and render setup
scripts/
  blender/               # Future Blender operators and validation
  pipeline/              # Future packaging and export automation
exports/
  models/                # Generated model deliverables
  illustrations/         # Generated still images
  animations/            # Generated animated deliverables
  README.md              # Export policy
docs/                   # Conventions, decisions, review, references
templates/              # Metadata templates for new assets
```

## Documentation and mandatory workflow

[AGENTS.md](AGENTS.md) instructs future Codex sessions to follow this system. Extend these authoritative guides rather than duplicating standards:

1. **Global Style Guide:** [visual style](docs/visual-style.md) records shared appearance, approval status, and reference-render requirements.
2. **Asset Category Standards:** [shared conventions](docs/asset-conventions.md) define common contracts; [category standards](docs/category-standards.md) add category-specific requirements.
3. **Individual Asset Specifications:** every future asset requires `SPEC.md`, `asset.json`, `validation.md`, and retained reference evidence beside its source. Start from the [specification template](templates/asset-specification.md), [metadata example](templates/asset-manifest.example.json), and [review checklist](docs/review-checklist.md).

The [mandatory workflow](docs/asset-workflow.md) is: review standards → specify → build → render references → validate → reconcile documentation. Do not mark an asset ready with missing evidence, unknown release facts, unapproved exceptions, or untested compatibility claims.

Never silently change a shared standard. Record proposed changes or exceptions in [Decisions](docs/decisions.md) using the [change template](templates/standards-change.md), and obtain approval before applying them. Reuse components and maintain existing interfaces; document approved breaking changes and migration. Global Blender, rig, palette, and render choices remain open; the approved cast-iron plate reference appearance is scoped to that category.

## Git and dependencies

Git was already initialized before this scaffold. Existing history and remote configuration are preserved; no new remote is configured.

`.gitattributes` routes Blender sources and common 3D interchange files (`.blend`, `.fbx`, `.glb`, `.obj`, `.stl`, `.ply`, `.abc`, `.usdc`, `.usdz`, and binary `.bin` buffers) through Git LFS. Textual `.gltf` and `.usda` descriptions remain diffable in Git. For other formats, select an explicit storage rule before adding large sources. Install Git LFS on contributor machines and run `git lfs install` after cloning, followed by `git lfs pull` to retrieve existing binary assets. Repository LFS availability and quotas must be confirmed before adding large files. Use `git lfs ls-files` to inspect tracked binaries.

Blender version and optional dependencies are pending approval. This repository requires no add-ons. Asset-specific plate build/validation scripts are provided under `scripts/blender/`; there is no general library pipeline yet. See [Decisions](docs/decisions.md) before selecting software or adding dependencies.

Use small, focused commits for sources, metadata, and documentation. Binary `.blend` files are not text-mergeable: coordinate ownership before editing the same file. Do not commit caches, backup saves, downloaded third-party libraries, or generated exports. Folder placeholders make the structure visible in a fresh clone.

## Visual direction

Clean anatomical illustrations, precise outlines, no cast or contact shadows, and recognizable equipment. Use readable silhouettes, restrained surfaces, and consistent anatomical emphasis. See the [visual specification](docs/visual-style.md).

## Licensing

Code, automation, documentation, and metadata templates use the MIT terms in [LICENSE](LICENSE). Future 3D artwork and artistic deliverables are excluded from that grant and require separate approved terms. No artwork license has been selected. See [Licensing policy](docs/licensing.md) for scope, provenance, and third-party requirements.
