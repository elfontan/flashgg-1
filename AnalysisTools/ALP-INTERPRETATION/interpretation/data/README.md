# Interpretation inputs

* `cross_section_limits_v1.yaml`: expected and observed diphoton cross-section limits in pb, with asymmetric expected bands, from [HEPData table 1, version 1](https://doi.org/10.17182/hepdata.166445.v1/t1). Masses are in GeV.
* `theory_baseline_1j_matched.csv`: supplied LO cross section times diphoton branching fraction in pb, at 13 masses from 10 to 70 GeV, at a reference decay constant of 1 TeV. The matching and PDF assumptions are in the accompanying JSON.
* `theory_baseline_1j_matched.json`: original supplied metadata, preserved verbatim. Its reference to a conversation records the source available in this workspace; a generator run identifier for every supplied theory point is not available.

The notebook applies K = 2 once, during the conversion to decay-constant limits. The CSV already includes the branching fraction. Linear interpolation is restricted to the tabulated mass range. No published decay-constant limits or historical theory tables are required by the baseline.

The gridpack cards are production examples. Their existence alone does not establish that they reproduce every entry of the supplied theory table. Record the resolved PDF, matching settings, run logs and post-matching normalization with any replacement table.
