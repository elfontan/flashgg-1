import os
import numpy as np
import sys
from ROOT import gROOT, gStyle, gSystem, TH1F, TLorentzVector
from DataFormats.FWLite import Handle, Events
from FWCore.PythonUtilities.LumiList import LumiList

# Set ROOT to batch mode
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)

# Path to ROOT files
root_dir = "/eos/user/e/elfontan/SampleFactory/alpGG_M30_ggj_TuneCP5_13p6TeV_madgraph-pythia8/chain_RunIISummer20UL18wmLHEGEN-RunIISummer20UL18NanoAODv9/20250107_000119/"

# Generate list of ROOT files
root_files = [
    "file:" + os.path.join(root_dir, f)
    for f in os.listdir(root_dir)
    if f.endswith(".root")
]

# CMSSW-style file list variable
alpfiles30 = "gen_files_30 = " + str(root_files)
print(alpfiles30)

# Load required libraries
gSystem.Load("libFWCoreFWLite.so")
gSystem.Load("libDataFormatsFWLite.so")
from PhysicsTools.PythonAnalysis import FWLiteEnabler
FWLiteEnabler.enable()

# FWLite handles and labels
gen, genLabel = Handle("GenEventInfoProduct"), ("generator")
handlePruned, prunedLabel = Handle("std::vector<reco::GenParticle>"), ("prunedGenParticles")

# Define histograms
histograms = {
    "genalp": TH1F("genalp", "genalp", 200, 0, 5),
    "genalpacc": TH1F("genalpacc", "genalpacc", 200, 0, 5),
    "genleadetaalp": TH1F("genleadetaalp", "genleadetaalp", 180, -6, 6),
    "genleadetaalpacc": TH1F("genleadetaalpacc", "genleadetaalpacc", 180, -6, 6),
    "gensubleadetaalp": TH1F("gensubleadetaalp", "gensubleadetaalp", 180, -6, 6),
    "gensubleadetaalpacc": TH1F("gensubleadetaalpacc", "gensubleadetaalpacc", 180, -6, 6),
    "genleadptalp": TH1F("genleadptalp", "genleadptalp", 200, 0, 200),
    "genleadptalpacc": TH1F("genleadptalpacc", "genleadptalpacc", 200, 0, 200),
    "gensubleadptalp": TH1F("gensubleadptalp", "gensubleadptalp", 200, 0, 200),
    "gensubleadptalpacc": TH1F("gensubleadptalpacc", "gensubleadptalpacc", 200, 0, 200),
    "gendiphotonptalp": TH1F("gendiphotonptalp", "gendiphotonptalp", 200, 0, 400),
    "gendiphotonptalpacc": TH1F("gendiphotonptalpacc", "gendiphotonptalpacc", 200, 0, 400),
    "gendralp": TH1F("gendralp", "gendralp", 200, 0, 5),
    "gendralpacc": TH1F("gendralpacc", "gendralpacc", 200, 0, 5),
}

# Enable Sumw2 for all histograms
for hist in histograms.values():
    hist.Sumw2()

# Process events
events = Events(root_files)
for i, event in enumerate(events):
    if i % 1000 == 0:
        print("Processed {} events".format(i))
    if i == 300000:
        break

    event.getByLabel(prunedLabel, handlePruned)
    event.getByLabel(genLabel, gen)

    weight = 1.0 if gen.product().weight() != 0.0 else 0.0
    pruned = handlePruned.product()

    # Photon selection and processing
    npho = 0
    pho = {}
    for p in pruned:
        if abs(p.pdgId()) == 22 and p.status() == 1:
            pho[npho] = TLorentzVector(p.px(), p.py(), p.pz(), p.energy())
            npho += 1

    if npho >= 2:
        phom = pho[0] + pho[1]
        phodr = np.sqrt((pho[0].Eta() - pho[1].Eta())**2 + (pho[0].Phi() - pho[1].Phi())**2)
        histograms["gendralp"].Fill(phodr, weight)
        histograms["gendiphotonptalp"].Fill(phom.Pt(), weight)

        # Leading and subleading photons
        lead_pt, sublead_pt = max(pho[0].Pt(), pho[1].Pt()), min(pho[0].Pt(), pho[1].Pt())
        lead_eta, sublead_eta = (pho[0].Eta(), pho[1].Eta()) if pho[0].Pt() > pho[1].Pt() else (pho[1].Eta(), pho[0].Eta())

        histograms["genleadptalp"].Fill(lead_pt, weight)
        histograms["gensubleadptalp"].Fill(sublead_pt, weight)
        histograms["genleadetaalp"].Fill(lead_eta)
        histograms["gensubleadetaalp"].Fill(sublead_eta)

        # Acceptance cuts
        if (lead_pt > 30.0 and sublead_pt > 18.0) or (lead_pt > 18.0 and sublead_pt > 30.0):
            if abs(lead_eta) < 2.5 and abs(sublead_eta) < 2.5:
                histograms["gendralpacc"].Fill(phodr, weight)
                histograms["gendiphotonptalpacc"].Fill(phom.Pt(), weight)
                histograms["genleadptalpacc"].Fill(lead_pt, weight)
                histograms["gensubleadptalpacc"].Fill(sublead_pt, weight)
                histograms["genleadetaalpacc"].Fill(lead_eta)
                histograms["gensubleadetaalpacc"].Fill(sublead_eta)

# Save histograms
output_dir = "output_histograms"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for name, hist in histograms.items():
    hist.SaveAs(os.path.join(output_dir, "{}.root".format(name)))
