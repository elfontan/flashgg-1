# ------------------------------------------------------ #
# Use this script within an environment allowing python: #
# ------------------------------------------------------ #
# python3 plot_NNScore.py --o /eos/user/e/elfontan/www/Hgg_veryLowMass_Paper/
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain, TH1F, TCanvas, TLegend, TProfile
from ROOT import kBlack, kRed, kPink, kMagenta, kViolet, kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange
import random, copy
import ROOT, array, CMSGraphics, CMS_lumi
import argparse
import sys
import os

gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--o', dest='o', default='/eos/user/e/elfontan/www/Hgg_veryLowMass_Paper', help='Output dir')

args = argparser.parse_args()
outdir  = args.o

print("Data File Processing...")
f_histos = ROOT.TFile.Open("histoFile_nnScores_allMC_data_arcReview.root")
h_nnScore_data = f_histos.Get("h_nnScore_data")

#masses = [15,25,30,35,45,50,55,60,70]
#col_list = [kBlue, kAzure + 7, kCyan + 3, kCyan - 3, kTeal - 7, kGreen - 6, kOrange - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3]
masses = [15,25,35,45,50,55,70]
col_list = [kBlue, kAzure + 7, kCyan - 3, kTeal - 7, kOrange - 3, kPink - 6, kMagenta - 7, kPink - 6, kViolet + 6,kRed - 3]
#masses = [10,15,20,25,30,35,40,45,50,55,60,65,70]
#col_list = [kSpring - 7,kBlue, kOrange + 7, kAzure + 7, kCyan + 3, kCyan - 3, kTeal - 7, kGreen - 6, kOrange - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3, kPink - 6, kMagenta - 7, kViolet + 6,kRed - 3]


canvas = TCanvas("canvas", "canvas", 1400, 1000)
canvas.SetLogy()
canvas.SetBottomMargin(0.12)
canvas.SetLeftMargin(0.12)
canvas.SetRightMargin(0.08)

h_nnScore_data.GetXaxis().SetTitleOffset(1.2)
h_nnScore_data.GetXaxis().SetTitleSize(0.05)
h_nnScore_data.GetYaxis().SetTitleSize(0.05)
h_nnScore_data.GetXaxis().SetLabelSize(0.05)
h_nnScore_data.GetYaxis().SetLabelSize(0.05)
h_nnScore_data.GetXaxis().SetTitle("NN score")
h_nnScore_data.GetYaxis().SetTitle("Events")
#h_nnScore_data.GetYaxis().SetTitle("Events (#sigma_{ggH} = 1 pb)")
h_nnScore_data.SetTitle("")
h_nnScore_data.SetLineColor(kBlack)
h_nnScore_data.SetMarkerColor(kBlack)
h_nnScore_data.SetMarkerStyle(20)
h_nnScore_data.SetMarkerSize(1.1)
h_nnScore_data.SetMinimum(10)
h_nnScore_data.SetMaximum(200.0*h_nnScore_data.GetMaximum())
h_nnScore_data.Draw("EPX")

legend = TLegend(0.55, 0.65, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetNColumns(2)
legend.AddEntry(h_nnScore_data, "Data", "EPX")
#legend.AddEntry(h_nnScore_data, "SR Data (10%)", "EPX")


idx = 0
mass_medians = []

for mass in masses:
    histoname = "h_nnScoreW_M"+str(mass)
    h = f_histos.Get(histoname)
    print("Integral for mass ", str(mass), " = ", h.Integral())

    h.SetLineWidth(2)            
    h.SetLineColor(col_list[idx])
    h.Scale(10000)
    h.Draw("hist same")
    canvas.Update()
    legend.AddEntry(h, "gg#phi ("+str(mass)+")", "l")
    #legend.AddEntry(h, "m = "+str(mass)+" GeV", "l")
    #legend.AddEntry(h, "#it{m}_{#gamma#gamma} = "+str(mass)+" GeV", "l")

    # Calculate the median PNN score for this mass
    median = 0
    cumulative = 0
    total = h.Integral()
    for bin in range(1, h.GetNbinsX() + 1):
        cumulative += h.GetBinContent(bin)
        if cumulative >= total / 2.0:
            median = h.GetBinCenter(bin)
            break
    # Calculate median PNN score for this mass and store it
    #profile = h.ProfileX()
    #median = profile.GetBinContent(profile.GetMaximumBin())

    mass_medians.append((mass, median))
    idx += 1

legend.Draw()

#cmsTag=ROOT.TLatex()                                                                                                                                                                                              
#cmsTag.SetNDC()                                  
#cmsTag.SetTextAlign(11)                                                                                                                       
#cmsTag.SetTextSize(0.06)                                                                                                                    
#cmsTag.DrawLatexNDC(0.16,0.82,"#scale[1.0]{CMS}")                                                                                                                            
cmsTag2 = ROOT.TLatex()               
cmsTag2.SetNDC()                                                                                             
cmsTag2.SetTextAlign(11)                                                                                               
cmsTag2.SetTextFont(52)                                                                                                    
cmsTag2.SetTextSize(0.06)                                                                    
#cmsTag2.DrawLatexNDC(0.27, 0.83, "Work in progress")
cmsTag2.DrawLatexNDC(0.255, 0.82, "Preliminary")
#cmsTag2.DrawLatexNDC(0.269, 0.82945, "Preliminary")

# Draw SR line:
line1 = ROOT.TLine(0.8, 10, 0.8, 250000)
line1.SetLineColor(ROOT.kGray+2)                                                                                                                                         
line1.SetLineStyle(7)                                                                                                                                                       
line1.SetLineWidth(3)                                                                                                        
line1.Draw("same")

latex = ROOT.TLatex()                                                                                                                                                                                         
latex.SetTextFont(42)                                                                                                                                                                                              
latex.SetTextSize(0.05)                                                                                                                                                      
latex.SetTextAlign(22)                                                                                                                                       
latex.SetTextColor(ROOT.kGray+2)
latex.DrawLatex(0.85, 90000, "SR")


# CMS Title and Lumi info
# -----------------------
CMS_lumi.writeExtraText = False
CMS_lumi.extraText      = ""
#CMS_lumi.lumi_sqrtS     = "2018 (13 TeV)"
CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.65
CMS_lumi.lumiTextSize   = 0.5
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.045
CMS_lumi.CMS_lumi(canvas, 0, 11)
canvas.Update()

canvas.Draw()
canvas.SaveAs(outdir+"/nnScore_allSig_data_paperDraft_ARC.png")
canvas.SaveAs(outdir+"/nnScore_allSig_data_paperDraft_ARC.pdf")


############################
# PNN Profile plot VS mass #
############################
canvas2 = TCanvas("canvas2", "canvas2", 1000, 800)
#canvas2 = TCanvas("canvas2", "canvas2", 1200, 600)
canvas2.SetBottomMargin(0.12)
canvas2.SetLeftMargin(0.12)

g_medians = ROOT.TGraph(len(mass_medians))
g_medians.SetMarkerStyle(22)
g_medians.SetMarkerColor(kAzure+7)
g_medians.SetMarkerSize(1.9)
g_medians.SetLineStyle(2)
g_medians.SetLineColor(kBlack)

for i, (mass, median) in enumerate(mass_medians):
    g_medians.SetPoint(i, mass, median)

g_medians.GetXaxis().SetTitleOffset(1.25)
g_medians.GetXaxis().SetTitleSize(0.045)
g_medians.GetYaxis().SetTitleSize(0.045)
g_medians.GetYaxis().SetRangeUser(0.6,0.9)
g_medians.GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
g_medians.GetYaxis().SetTitle("Median PNN Score")
g_medians.SetTitle("")
g_medians.Draw("APL")

# CMS Title and Lumi info
CMS_lumi.CMS_lumi(canvas2, 0, 11)
canvas2.Update()

canvas2.Draw()
#canvas2.SaveAs(outdir+"/profilePNN_vs_mass_final.png")
#canvas2.SaveAs(outdir+"/profilePNN_vs_mass_final.pdf")
