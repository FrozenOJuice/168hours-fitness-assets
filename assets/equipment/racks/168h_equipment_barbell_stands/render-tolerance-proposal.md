# Proposed assembly comparison exception — approval required

Status: **approved and applied, 2026-10-15**. The user explicitly answered
“Approve this scoped comparison exception” to the complete numeric proposal.
[Applied policy](render-comparison-policy.json); all nine views now pass, with
seven pixel-exact and two within the approved limits. The proposal and original
strict-failure evidence below explain the acceptance decision. This is an asset-local exception for
the assembled and side views of `168h_template_stands_bench_barbell`, not a shared
style or validation-standard change.

## Evidence and cause

Blender 5.1.1, Apple M1 Metal backend, recorded Workbench FLAT / 32 AA preset.
Six repeated renders per view, including repeated renders without reopening and
three file reopens, vary despite identical native inputs and camera settings.
Across reference and pairwise comparisons, the final-fixture measured maxima are:

| View | Channel difference, 8-bit units | Changed RGBA channels | Changed pixels | Mean absolute difference, 8-bit units |
| --- | --- | --- | --- | --- |
| Assembled | 6 | 0.052500% | 0.084188% | 0.00073141 |
| Side | 8 | 0.035516% | 0.049188% | 0.00092157 |

Evidence: `render-investigation.json`, `render-investigation-inputs.json`,
`render-settings-investigation.json`, retained diagnostic PNGs under `qa/`.
Changing the scene render-thread count to one and reducing camera far clipping
to 10 m do not remove variation. Disabling AA increases peak differences to 11.
Disabling object outlines gives exact repeated output in three diagnostic side
renders. Hiding the bench reduces but does not eliminate variation. Changes
localize primarily to bench structural/detail edges, with smaller stand-hook
changes. This isolates the unstable rendering path to the native object-outline
effect on this assembly. The precise GPU/object-ID scheduling mechanism remains
unproven; depth/ID ordering at coincident component surfaces is a plausible cause,
not an established Blender defect diagnosis.

Blender's [outline implementation](https://github.com/blender/blender/blob/main/source/blender/draw/engines/workbench/workbench_effect_outline.cc)
describes an object-ID-buffer effect. That source is contextual evidence, not
proof of the internal cause on the installed binary. No renderer/palette/software
baseline was changed. Disabling outlines would change the required appearance,
so that diagnostic was not adopted. Other views still use exact comparison.

## Proposed acceptance limits

All conditions must hold simultaneously for these **two assembly views only**:

- Same 1600 × 1000 RGBA8 image dimensions; no registration, blur, edge masks,
  resampling, color correction or perceptual preprocessing.
- Maximum absolute RGB-channel difference **≤8/255**.
- Alpha must match **exactly**.
- Changed-channel fraction **<0.1%**, denominator all RGBA channels.
- Changed-pixel fraction **<0.15%**, a pixel changes if any channel changes.
- Mean absolute difference over all RGBA channels **≤0.002 in 8-bit units**.
- All six standalone renders and assembly front must remain **pixel-exact**.
- Geometry/contact/origin/dimension/dependency checks must independently pass;
  tolerances cannot excuse geometry changes, shifted cameras or missing assets.
- Current native sources, preset and reference images stay hash-pinned. An
  authorized input revision requires new explicit evidence; no automatic baseline
  replacement. Manual review must confirm unchanged silhouette, outlines, palette
  and shadow-free appearance.

The 8/255 maximum covers the measured sparse edge variation without allowing a
larger single-channel error. Coverage and mean-error bounds prevent broad image
drift and allow modest repeat variation beyond the observed coverage. These are
observed limits for this hardware/scene, not a universal guarantee. Runs outside
any limit fail and require investigation. This exception is broader in peak
channel difference than the older barbell assembly's 1/255 exception; it is not
implicitly approved by that precedent.

## Contact correction is separate and complete

The original facet-to-facet distances were 4.799192 and 4.798168 µm. A fixture-only
barbell Z settlement of **−4.708766937 µm** leaves 0.093209 and 0.092185 µm positive
facet separation, within the unchanged 1 µm contact criterion. Zero inter-asset
BVH crossings; equal hook support height, mirrored X positions, clearances and
all detents/anchors pass. The first attempted float32 step overshot contact by
about 0.03 µm and failed the intersection test; it was replaced by the nearest
nonintersecting step, with the failed-trial evidence retained. No source asset
geometry, materials, origins or anchors were modified.

All three assembly references were refreshed for this authorized contact-corrected
fixture; their original sources/images/settings remain under the fixture's
`history/0.1.1-before-contact/`. The exception is to compare repeated renders of
the same corrected source, not to excuse changes between source versions.

## Reproduction

Use the pinned Blender executable with `--background --factory-startup
--python-exit-code 1 --python` and each script below from the repository root:

1. `scripts/blender/validate_barbell_stands.py` — 647 PASS, zero FAIL.
2. `scripts/blender/validate_stands_final.py` — 45 PASS, zero FAIL.
3. `scripts/blender/validate_stands_regressions.py` — 6 fault-injection and 2
   automatic placement cases PASS; frozen shared reports preserved.
4. `scripts/blender/investigate_stands_gates.py -- --contact-after` — exhaustive
   noncrossing triangle-distance measurement with conservative AABB pruning.
5. `scripts/blender/render_barbell_stands.py -- --reproduce` — strict gate remains
   7 PASS / 2 FAIL. Do not run the capture mode to hide this failure.
6. `scripts/blender/investigate_stands_gates.py` then
   `scripts/blender/analyze_stands_render_probes.py` — unchanged-input repeat
   comparisons. `-- --settings` runs transient diagnostic variants only.

Approval requested: accept the limits above for these two views, preserve the
illustration design, then implement the explicitly approved local policy, rerun
all gates, and approve/commit only if every applicable check passes.
