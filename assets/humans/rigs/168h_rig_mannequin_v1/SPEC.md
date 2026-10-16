# Mannequin V1 rig-data library —0.2.0 REVIEW

Current source:168h_rig_mannequin_v1__foundation_v02.blend. The original168h_rig_mannequin_v1.blend is retained for the archived0.1.0 character. The new metric native file publishes168h_rig_mannequin_v1__skeleton_data_foundation_v02, with53 canonical V1 bones, exact parentage/connectivity/local roll, floor root and measured45°A-pose. No skin, extra output bone or animation is added here.

Graphical joint measurements derive from pinned CC0 MakeHuman data and are adapted to V1 by mannequin_foundation_data.py. The profile fingerprint and source/dependency hashes are recorded in asset.json and the character's rest-profile.json. This changes provisional proportions/rest profile, not shared V1 semantics. It is not direct-pose compatible with0.1.0.

The character links this rest data into separate local private solver and solved-output objects. Skin weights, IK/FK mechanisms, explicit snap helpers, knee corrective and pose state live with that character/fixture; this file alone is a measured rest library, not a standalone certified animator control rig. See [character SPEC](../../models/168h_human_anatomical_mannequin/SPEC.md), validation.md and FOUNDATION-REPORT.md.

Review only. No clinical limits, automatic retarget guarantee, extra twist-bone contract, animation/export roundtrip or artwork release approval. Upstream graphical data CC0; original code/docs MIT separately; project artwork terms unselected. Equipment and shared standards unchanged.
