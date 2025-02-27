import ROOT
import os
import CMS_lumi
from ROOT import TFile, TCanvas, TLegend, TPad

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

logScale = True

# Define directories and their corresponding histogram names and labels
plot_config = {
    "Plots/LeadPT": ("genleadptggh", "Lead Photon p_{T} [GeV]", "LeadPhotonPt_Comparison"),
    "Plots/SubleadPT": ("gensubleadptggh", "Sublead Photon p_{T} [GeV]", "SubleadPhotonPt_Comparison"),
    "Plots/LeadEta": ("genleadetaggh", "Lead Photon eta", "LeadPhotonEta_Comparison"),
    "Plots/SubleadEta": ("gensubleadetaggh", "Sublead Photon eta", "SubleadPhotonEta_Comparison"),
    "Plots/DiphotonPT": ("gendiphotonptggh", "Dihoton p_{T} [GeV]", "DiphotonPt_Comparison"),
    "Plots/DR": ("gendrggh", "DR", "DR_Comparison"),
}

# Output directory for plots
output_dir = "/eos/user/e/elfontan/www/Hgg_veryLowMass_AN/ARCReviewChecks/alpInterpretation/ggH_weightsImpact/"
os.makedirs(output_dir, exist_ok=True)

# Loop over all configurations
for directory, (hist_name, x_axis_label, plot_caption) in plot_config.items():
    
    # Open ROOT files
    file1 = TFile.Open(f"{directory}/gen_ggh30.root")
    file2 = TFile.Open(f"{directory}/gen_ggh30_noWeights.root")

    # Retrieve histograms
    hist1 = file1.Get(hist_name)
    hist2 = file2.Get(hist_name)

    if not hist1 or not hist2:
        print(f"Histogram '{hist_name}' not found in files under {directory}")
        continue

    # Set histogram styles
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetLineWidth(2)
    hist1.SetMarkerColor(ROOT.kBlue)
    hist1.SetMarkerStyle(20)

    hist2.SetLineColor(ROOT.kRed)
    hist2.SetLineWidth(2)
    hist2.SetMarkerColor(ROOT.kRed)
    hist2.SetMarkerStyle(24)

    # Compute integrals
    integral1 = hist1.Integral()
    integral2 = hist2.Integral()

    # Create main canvas with pads
    canvas = TCanvas("canvas", plot_caption, 800, 800)
    canvas.Divide(1, 2, 0.01, 0.01)
    
    pad1 = canvas.cd(1)
    if (logScale):
        pad1.SetLogy()
    pad1.SetPad(0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.15)
    #pad1.SetGridx()
    #pad1.SetGridy()
    
    # Draw histograms on the main pad
    hist1.SetTitle("")
    if (logScale):
        hist1.SetMaximum(30 * max(hist1.GetMaximum(), hist2.GetMaximum()))
    else:
        hist1.SetMaximum(1.5 * max(hist1.GetMaximum(), hist2.GetMaximum()))
    hist1.GetXaxis().SetLabelSize(0)
    hist1.GetYaxis().SetTitle("Events")
    hist1.GetYaxis().SetTitleSize(0.05)
    hist1.GetYaxis().SetLabelSize(0.04)
    hist1.Draw("HIST E")
    hist2.Draw("HIST E SAME")

    # Add legend
    legend = TLegend(0.45, 0.7, 0.88, 0.85)
    legend.SetHeader("ggH NLO 01j MC")
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.SetFillStyle(0)
    legend.AddEntry(hist1, f"With Weights (Integral: {integral1:.1f})", "l")
    legend.AddEntry(hist2, f"No Weights (Integral: {integral2:.1f})", "l")
    legend.Draw()

    # CMS Title and Lumi info
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.lumi_sqrtS = "13 TeV"
    CMS_lumi.cmsTextSize = 0.6
    CMS_lumi.lumiTextSize = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(pad1, 0, 0)

    # Create the ratio plot pad
    pad2 = canvas.cd(2)
    pad2.SetPad(0, 0.0, 1, 0.3)
    pad2.SetTopMargin(0.02)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.15)
    pad2.SetGridx()
    pad2.SetGridy()

    # Create the ratio histogram
    ratio_hist = hist1.Clone("ratio_hist")
    ratio_hist.Divide(hist2)
    ratio_hist.SetLineColor(ROOT.kBlack)
    ratio_hist.SetMarkerColor(ROOT.kBlack)
    ratio_hist.SetMarkerStyle(20)
    ratio_hist.SetTitle("")
    ratio_hist.GetYaxis().SetTitle("Unweighted/W")
    ratio_hist.GetYaxis().SetNdivisions(505)
    ratio_hist.GetYaxis().SetTitleSize(0.1)
    ratio_hist.GetYaxis().SetLabelSize(0.08)
    ratio_hist.GetYaxis().SetTitleOffset(0.5)
    ratio_hist.GetXaxis().SetTitle(x_axis_label)
    ratio_hist.GetXaxis().SetTitleSize(0.12)
    ratio_hist.GetXaxis().SetLabelSize(0.1)
    ratio_hist.GetXaxis().SetTitleOffset(1.0)
    ratio_hist.GetYaxis().SetRangeUser(0,2)

    # Draw ratio plot
    ratio_hist.Draw("EP")

    # Save plots
    output_name = f"{output_dir}/{hist_name}_ggh_genWeightsImpact"
    if (logScale):
        canvas.SaveAs(f"{output_name}_log.pdf")
        canvas.SaveAs(f"{output_name}_log.png")
    else:
        canvas.SaveAs(f"{output_name}.pdf")
        canvas.SaveAs(f"{output_name}.png")

    print(f"Saved plots as {output_name}.pdf and .png")

