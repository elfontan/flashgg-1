# UFO snapshots

These are source snapshots, with original author information retained. File origins and SHA-256 hashes are in [the manifest](../docs/source_manifest.json).

| Directory | Origin | Use |
| --- | --- | --- |
| `axion_UFO` | `MG5NLO/standalone-tut/MG5_aMC_v2_9_18/models/axion_UFO` | Model imported by the production cards; includes `WALP` and an ALP decay width |
| `ALP_linear_UFO` | Original top-level `ALP_linear_UFO` | Reference export; the ALP particle has zero width |

The snapshots differ beyond the directory name: export versions, some coupling expressions, and the ALP width definition differ. Do not interchange them silently. The legacy import style is retained for MadGraph's model conversion; these are not ordinary installable Python packages.

Both contain the `a a ax` and `g g ax` vertices used for the ALP diphoton process. `a` is the photon, `g` the gluon and `ax` the ALP (PDG 9000005).
