# Import ROOT in batch mode
import numpy as np
import sys
oldargv = sys.argv[:]
sys.argv = ['-b-']
from ROOT import gStyle, gROOT, TFile, TCanvas, TLegend, kRed, kViolet, kAzure, TLine
gROOT.SetBatch(True)
sys.argv = oldargv
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)

from array import array
import CMS_lumi

# Define the list of variables and their labels
variables = [
    {"name": "LeadPT", "label": "Leading Photon p_{T} [GeV]"},
    {"name": "SubleadPT", "label": "Subleading Photon p_{T} [GeV]"},
    {"name": "LeadEta", "label": "Leading Photon #eta"},
    {"name": "SubleadEta", "label": "Subleading Photon #eta"},
    {"name": "DiphotonPT", "label": "Diphoton p_{T} [GeV]"},
    {"name": "DR", "label": "#Delta R"}
]

# Loop through each variable
for var_dict in variables:
    var = var_dict["name"]
    lbl = var_dict["label"]

    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    c1 = TCanvas(f"c1_{var}", f"c1_{var}", 1000, 800)
    c1.cd()
    c1.SetLeftMargin(0.15)

    gghfile = TFile(f"Plots/{var}/gen_alpPlusjet30.root", "READ")
    genggh = gghfile.Get(f"gen{var.lower()}alp")
    genggh.SetXTitle(lbl)
    genggh.SetYTitle("Gen Level Events")
    genggh.SetMinimum(0.0)
    if var in ["LeadEta", "SubleadEta"]:
        genggh.SetMaximum(5500.0)
    genggh.SetLineColor(kAzure + 1)
    genggh.Draw("histsame")

    alpfile = TFile(f"Plots/{var}/gen_alp30.root", "READ")
    genalp = alpfile.Get(f"gen{var.lower()}alp")
    genalp.SetMinimum(0.0)
    genalp.SetLineColor(kViolet - 6)
    genalp.Draw("histsame")

    gghfileacc = TFile(f"Plots/{var}/gen_alpPlusjet30acc.root", "READ")
    gengghacc = gghfileacc.Get(f"gen{var.lower()}alpacc")
    gengghacc.SetMinimum(0.0)
    gengghacc.SetLineColor(kAzure - 4)
    gengghacc.SetLineStyle(2)
    gengghacc.Draw("histsame")

    alpfileacc = TFile(f"Plots/{var}/gen_alp30acc.root", "READ")
    genalpacc = alpfileacc.Get(f"gen{var.lower()}alpacc")
    genalpacc.SetMinimum(0.0)
    genalpacc.SetLineColor(kViolet - 4)
    genalpacc.SetLineStyle(2)
    genalpacc.Draw("histsame")

    if var == "DR":
        cat03 = TLine(0.3, 0.0, 0.3, 3000.0)
        cat03.SetLineColor(28)
        cat03.SetLineWidth(3)
        cat03.SetLineStyle(2)
        cat03.Draw("same")

    if var == "DR":
        leg = TLegend(0.18, 0.58, 0.53, 0.88)
    else:
        leg = TLegend(0.50, 0.65, 0.85, 0.85)
    leg.SetBorderSize(0)
    leg.SetHeader("30 GeV BSM Models", "C")
    if var == "DR":
        leg.AddEntry(genggh, f"ALP (+1j): {np.round(genggh.Integral(0, 12) / genggh.Integral() * 100, 2)}% events with dR < 0.3", "l")
        leg.AddEntry(genalp, f"ALP: {np.round(genalp.Integral(0, 12) / genalp.Integral() * 100, 2)}% events with dR < 0.3", "l")
        leg.AddEntry(gengghacc, f"ALP (+1j): {round(gengghacc.Integral() / genggh.Integral() * 100, 2)}% in Acceptance Region and", "l")
        leg.AddEntry(0, f"{np.round(gengghacc.Integral(0, 12) / gengghacc.Integral() * 100, 2)}% in Acceptance Region with dR < 0.3", "")
        leg.AddEntry(genalpacc, f"ALP (+1j): {round(genalpacc.Integral() / genalp.Integral() * 100, 2)}% in Acceptance Region and", "l")
        leg.AddEntry(0, f"{np.round(genalpacc.Integral(0, 12) / genalpacc.Integral() * 100, 2)}% in Acceptance Region with dR < 0.3", "")
    else:
        leg.AddEntry(genggh, "ALP (+1j) at Gen Level")
        leg.AddEntry(genalp, "ALP at Gen Level")
        leg.AddEntry(gengghacc, f"ALP (+1j): {round(gengghacc.Integral() / genggh.Integral() * 100, 2)}% in Acceptance Region")
        leg.AddEntry(genalpacc, f"ALP: {round(genalpacc.Integral() / genalp.Integral() * 100, 2)}% in Acceptance Region")
    leg.Draw("same")

    # CMS lumi stuff
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText = " Simulation Preliminary"
    CMS_lumi.lumi_sqrtS = "2018 (13 TeV)"
    CMS_lumi.cmsTextSize = 0.6
    CMS_lumi.lumiTextSize = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(c1, 0, 0)

    c1.Update()
    c1.SaveAs(f"/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Interpretation/ALPsimulation/alpPlusJet_vs_alp/sig_gen_{var.lower()}_alpPlusJet30GeV.png")
    c1.SaveAs(f"/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Interpretation/ALPsimulation/alpPlusJet_vs_alp/sig_gen_{var.lower()}_alpPlusJet30GeV.pdf")

    genggh.SetMinimum(0.1)
    gengghacc.SetMinimum(0.1)
    genalp.SetMinimum(0.1)
    genalpacc.SetMinimum(0.1)

    genggh.SetMaximum(10000000)
    gengghacc.SetMaximum(10000000)
    genalp.SetMaximum(10000000)
    genalpacc.SetMaximum(10000000)

    c1.Update()
    c1.SetLogy()
    c1.SaveAs(f"/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Interpretation/ALPsimulation/alpPlusJet_vs_alp/sig_gen_{var.lower()}_alpPlusJet30GeV_log.png")
    c1.SaveAs(f"/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/Interpretation/ALPsimulation/alpPlusJet_vs_alp/sig_gen_{var.lower()}_alpPlusJet30GeV_log.pdf")
