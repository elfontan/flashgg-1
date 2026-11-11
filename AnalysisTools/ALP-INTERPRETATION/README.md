# ALP diphoton interpretation

Source inputs and workflows for direct ALP production, gridpack generation and conversion of diphoton signal limits into bounds on the decay constant.

| Area | Contents |
| --- | --- |
| [Gridpack production](gridpack/README.md) | Seven mass-point card sets and a helper for a pinned genproductions checkout |
| [UFO models](models/README.md) | Production `axion_UFO` and original `ALP_linear_UFO` source snapshots |
| [Baseline notebook](interpretation/notebooks/ALP_fa_limits.ipynb) | Matched theory prediction, limit conversion, expected bands and internal checks |
| [Input data](interpretation/data/README.md) | Cross-section limits, supplied theory rates and metadata |
| [MiniAOD production](miniaod/README.md) | Sample-factory recipe and ALP shower fragments |
| [PDF study](validation/pdf_study/README.md) | Small text records from the existing generator studies |

## Run the interpretation

From the repository root, with Python 3:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r interpretation/requirements.txt
jupyter lab interpretation/notebooks/ALP_fa_limits.ipynb
```

Run all cells in order. The notebook also supports a working directory beneath the repository root. To execute without opening the UI:

```bash
mkdir -p interpretation/results
jupyter nbconvert --to notebook --execute interpretation/notebooks/ALP_fa_limits.ipynb --output ALP_fa_limits_executed.ipynb --output-dir interpretation/results
```

The prediction is supplied at fa = 1 TeV, with c1 = c2 = c3 = 10, up to one additional parton and jet matching. Linear interpolation and K = 2 are used to convert signal limits. The branching fraction is already included in the theory input. Plots and CSV results are written to `interpretation/results/`.

The notebook includes input validation, scaling, interpolation, band-ordering and inverse-conversion checks. Stored outputs are cleared for version control.

## Repository scope

The top-level ignore rules include only the curated directories above and documentation. MadGraph/CMSSW installations, external repositories, generated events, archives and local outputs are excluded from version control. Production instructions are provided in the relevant directories.

[The source manifest](docs/source_manifest.json) records relative source locations and SHA-256 hashes for verbatim snapshots. The external software is fetched separately. The theory metadata records the provenance available in this workspace; a full generator-run provenance for every supplied theory point is still needed for future production reproducibility.

This is a local preparation for review. No commit, GitHub repository or remote publication has been created.
