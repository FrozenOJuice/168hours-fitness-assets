# 168Hours Fitness — Blender Asset Library

A modular library for reusable human models, rigs, fitness equipment, materials, exercise scenes, and scene templates.

**Status:** repository scaffold and proposed conventions only. No 3D models, rigs, materials, or Blender scenes have been created. Architecture choices awaiting approval are recorded in [Decisions](docs/decisions.md).

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

## Working approach

1. Review the [proposed conventions](docs/asset-conventions.md) and [approval decisions](docs/decisions.md) before authoring production assets.
2. Create one directory per asset in the appropriate category, named with its stable asset ID. Keep its source `.blend`, metadata, and any dependencies together.
3. Copy [asset metadata](templates/asset-manifest.example.json) into that directory as `asset.json` and replace every example value. The template is illustrative, not an actual library asset.
4. Build scenes from linked asset collections. Keep exercise poses and placement in exercise scenes; keep reusable geometry in asset sources.
5. Check each asset against the [review checklist](docs/review-checklist.md) before marking it ready.
6. Write generated deliverables under `exports/`. Retain reproducible source files and record export settings.

## Git and dependencies

Git was already initialized before this scaffold. Existing history and remote configuration are preserved; no new remote is configured.

`.gitattributes` routes Blender sources and common 3D interchange files (`.blend`, `.fbx`, `.glb`, `.obj`, `.stl`, `.ply`, `.abc`, `.usdc`, `.usdz`, and binary `.bin` buffers) through Git LFS. Textual `.gltf` and `.usda` descriptions remain diffable in Git. For other formats, select an explicit storage rule before adding large sources. Install Git LFS on contributor machines and run `git lfs install` after cloning, followed by `git lfs pull` to retrieve existing binary assets. Repository LFS availability and quotas must be confirmed before adding large files. Use `git lfs ls-files` to inspect tracked binaries.

Blender version and optional dependencies are pending approval. This repository currently requires no add-ons and contains no executable pipeline. See [Decisions](docs/decisions.md) before selecting software or adding dependencies.

Use small, focused commits for sources, metadata, and documentation. Binary `.blend` files are not text-mergeable: coordinate ownership before editing the same file. Do not commit caches, backup saves, downloaded third-party libraries, or generated exports. Folder placeholders make the structure visible in a fresh clone.

## Visual direction

Clean anatomical illustrations, precise outlines, no cast or contact shadows, and recognizable equipment. Use readable silhouettes, restrained surfaces, and consistent anatomical emphasis. See the [visual specification](docs/visual-style.md).

## Licensing

Code, automation, documentation, and metadata templates use the MIT terms in [LICENSE](LICENSE). Future 3D artwork and artistic deliverables are excluded from that grant and require separate approved terms. No artwork license has been selected. See [Licensing policy](docs/licensing.md) for scope, provenance, and third-party requirements.
