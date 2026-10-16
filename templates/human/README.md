# Future human asset templates

Foundation only; no asset is created by copying these files. Read the
[official V1 contract](../../docs/contracts/human-v1/README.md) and AGENTS.md first.

1. Start `SPEC.md`, `asset.json`, `validation.md` from the existing repository
   templates/checklist; preserve their licensing, provenance, style and release
   sections. Add [human-specification.md](human-specification.md) and
   [human-validation.md](human-validation.md) sections to those files.
2. Copy [human-contract.example.json](human-contract.example.json) beside the
   future asset as `human-contract.json`. Add a repository-relative
   `human_contract` reference to `asset.json`. Paths inside human-contract.json
   are relative to its directory unless explicitly declared repository-relative
   (the source in asset.json follows the existing repository convention).
3. Replace every draft value with observed character data. Use the53 canonical
   bones,11 anchor keys, logical IK/FK facade and78 muscle IDs from the contract's
   JSON registries. Do not type a competing list. Record real measured stature,
   dependencies, canonical rest profile, maps and supported clothing variants.
4. Declare controls as `{object, bone}` references; `bone:null` means an object
   target. The four `ik_fk_arm_l/r` and `ik_fk_leg_l/r` switches map to canonical
   root properties using the optional `property` field (0FK/1IK). `solver_bindings` maps each ik_hand/ik_foot key to its actual two-bone
   IK constraint owner. `joint_limit_bindings` maps forearm/shin logical names to
   actual local-limit constraint owners. Declare actual local min/max radians
   and approval references. More joint profiles may be added explicitly.
5. Muscle masks are vertex groups on declared body meshes, separate from bone
   weights. Properties live on the published installation root. Use the canonical
   primary/secondary property names, never a shared property for multiple IDs.
6. Record the future saved character using the read-only inspector; optionally
   write its canonical rest-profile JSON. Populate its SHA256 then rerun checks.
   Keep reference renders/settings and validation evidence under the asset;
   disposable bake/illustration outputs go under ignored exports.
7. Build export-profile JSON from human-export-v1.schema.json only after actual
   renderer/format/consumer approval. Record pinned files/evidence and run
   `--release`; empty arrays/nulls are draft placeholders, not a successful rig.

The example JSON is schema-valid draft data and deliberately fails actual
character compatibility/release. It is not a1800mm default person, selected rig,
animation or production export profile. `exercise-muscles.example.json` is a
future metadata form, not a created exercise or a medical activation assignment.

Asset-specific creative/deformation decisions need sufficiently detailed source,
joint measurements, binding steps, control maps, shader parameters and review
references for another developer to reproduce them. Code/docs are MIT; artwork
terms are separate. No model or skeleton builder is supplied in this task.
