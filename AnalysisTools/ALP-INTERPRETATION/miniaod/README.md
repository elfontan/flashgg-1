# MiniAOD production

The `fragments/` directory preserves all 20 local ALP generator fragments, including matching-scale variations. Their filenames say `13p6TeV`, but their configured `comEnergy` is **13000 GeV**, consistent with the gridpack cards. Check the configuration itself when choosing an energy. The matched fragments specify `nQmatch = 5`; review the flavour and matching choices together with the PDF before treating a variant as a benchmark.

The original workflow uses the external sample factory:

```bash
git clone ssh://git@gitlab.cern.ch:7999/shjeon/sample_factory.git
cd sample_factory
source setup.sh
```

Create your user configuration under `configs/` with your XRootD host and output LFN. For example, use `root://eosuser.cern.ch/` with your own EOS user directory. Copy the chosen fragment from this repository into `data/fragments/` and set its `externalLHEProducer.args` to the intended gridpack archive.

Use the UL18 chain `data/chains/chain_RunIISummer20UL18wmLHEGEN-RunIISummer20UL18NanoAODv9.json` and configure the output tiers to retain `RunIISummer20UL18MiniAODv2` as required. The original setup notes state that pileup preparation is handled automatically by the factory. The external factory revision was not recorded in those notes; record it for future campaigns.

Example smoke run, followed by the original campaign size:

```bash
./runFactory.py -c data/chains/chain_RunIISummer20UL18wmLHEGEN-RunIISummer20UL18NanoAODv9.json -f data/fragments/xqcut10_qcut20_jetMerging_alpGG_M30_ggj_TuneCP5_13p6TeV_madgraph-pythia8.py -n 10 -j 10
./runFactory.py -c data/chains/chain_RunIISummer20UL18wmLHEGEN-RunIISummer20UL18NanoAODv9.json -f data/fragments/xqcut10_qcut20_jetMerging_alpGG_M30_ggj_TuneCP5_13p6TeV_madgraph-pythia8.py -n 100 -j 4000
```

Select the 60 GeV fragment for the corresponding second campaign. The chosen 20 GeV shower matching scale is an example among the preserved variants. Outputs go to the EOS destination configured for your account. No MiniAOD production was launched during this cleanup.
