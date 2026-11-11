# Gridpack production

The card snapshots cover ALP masses 10, 20, 30, 40, 50, 60 and 70 GeV at 13 TeV. Each directory contains the process, run and customization cards. Editor backups have been omitted; all `.dat` files are unchanged from the supplied `loMLM_AlpToGGj_fixedCtilV2_M*` directories.

The process contains direct ALP production with zero and one extra matrix-element parton, followed by a diphoton decay. In MadGraph, `a` denotes the photon and `ax` denotes the ALP.

## Prepare a separate checkout

Run these commands from the repository root. `external/` is ignored by Git.

```bash
mkdir -p external
git clone https://github.com/cms-sw/genproductions.git external/genproductions
git -C external/genproductions checkout 082de8dc377f80fb3d867e0192feafe3a563e848
python3 gridpack/scripts/prepare_genproductions.py external/genproductions
```

The revision is the HEAD recorded in the original local checkout. It selects MadGraph 2.9.18. The helper copies the cards and the `axion_UFO` Python sources, then inserts a local model-copy command immediately after MadGraph configuration. It is safe to rerun with the same inputs and refuses conflicting edits. It does not modify the original working installation.

This replaces the original recipe's machine-specific model-copy step. The old local generation script currently copies an unrelated `DMsimp_s_spin1` model; do not use that edited script for this ALP recipe. The top-level reference `ALP_linear_UFO` also cannot simply replace `axion_UFO`: the production customization uses its `WALP` parameter.

## Generate and validate

Enter the site's supported EL7 environment for the historical Run-2 setup (the original recipe used a personal `start_el7.sh` helper). The historical output used `slc7_amd64_gcc10` and `CMSSW_12_4_8`. That helper is not part of this repository. CMS/CVMFS access, the compatible compiler environment, and generator downloads are external prerequisites.

```bash
cd external/genproductions/bin/MadGraph5_aMCatNLO
./gridpack_generation.sh loMLM_m30_ggj_fixedCtilV2 cards/production/13TeV/loMLM_AlpToGGj_fixedCtilV2_M30/
```

Use the corresponding name and directory for another mass. To exercise a generated archive, unpack it into a separate work directory and run:

```bash
mkdir -p /tmp/alp-gridpack-validation
cd /tmp/alp-gridpack-validation
tar -xf /path/to/loMLM_m30_ggj_fixedCtilV2_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
./runcmsgrid.sh 10000 4 4
```

The arguments are event count, random seed and core count. Record the resolved run and parameter cards, cross section, width, PDF, and software versions. Gridpack generation and event production have not been rerun as part of the repository cleanup.

## Settings that affect the normalization

The customization sets `fa = 1000` GeV, `cBtil = 0.01349156`, `cWtil = 0.02694808`, `cGtil = 0.093949`, `CaPhi = 0` and an automatic ALP width. The UFO's tilde coefficients are not the notebook's numerical `c_i = 10` labels; preserve the existing convention.

The run cards use 6500 GeV beams. Their initial `ickkw = 0` and `xqcut = 0` are overridden by customization to `ickkw = 1` and `xqcut = 10` GeV. The run-card PDF is the `$DEFAULT_PDF_SETS` placeholder resolved by genproductions. Inspect the final run card; use an explicit central PDF ID of 325500 when targeting the notebook's supplied benchmark, and record that production variant separately from these verbatim examples.

LHE production alone is not the post-matching prediction. Pythia matching, including `qCut`, affects the accepted rate. [MiniAOD fragments](../miniaod/README.md) preserve the available matching variations; they do not establish which variation produced every point in the supplied theory table. Validate matching and the resulting normalization before replacing the table.
