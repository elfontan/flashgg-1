from ROOT import *
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import CMSGraphics, CMS_lumi
from ROOT import TFile, TTree, TList
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--minV', dest='minV', default='-0.9', help='Minimum Value for maxPhoId')
argparser.add_argument('--maxV', dest='maxV', default='1.0', help='Maximum Value for maxPhoId')
argparser.add_argument('--log', dest='log', default=False, help='Log scale in the y axis')
argparser.add_argument('--norm', dest='norm', default=False, help='Norm factor')
argparser.add_argument('--sb', dest='sb', default=False, help='Norm factor')
argparser.add_argument('--hyp', dest='hyp', default='NEAREST', help='Strategy for building the mass hypothesis')

args = argparser.parse_args()
outputdir = args.outdir
minValue = args.minV
maxValue = args.maxV
logScale = args.log
normFactor = args.norm
sbScenario = args.sb
massHyp = args.hyp

# ----------------------
# Obtain histogram files
# ----------------------
# All 2018 data
f_data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+massHyp+"/out_all2018Data_bkg_newSamplesFlat.root","READ") 
#f_data = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/"+massHyp+"/out_all2018Data_bkg.root","READ") 
# Data from the sideband
#f_sideband = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/"+massHyp+"/out_sbData_bkg.root","READ") 


# Get trees and create histograms for data
# ----------------------------------------
t_dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
#t_sb0 = f_sideband.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
 
h_diphoMass_pre0 = TH1F("h_diphoMass_pre0", "h_diphoMass_pre0", 80, 0, 40)
h_diphoMass_pre1 = TH1F("h_diphoMass_pre1", "h_diphoMass_pre1", 80, 0, 40)
h_diphoMass_pre2 = TH1F("h_diphoMass_pre2", "h_diphoMass_pre2", 80, 0, 40)
h_diphoMass_pre3 = TH1F("h_diphoMass_pre3", "h_diphoMass_pre3", 80, 0, 40)
h_diphoMass_pre4 = TH1F("h_diphoMass_pre4", "h_diphoMass_pre4", 80, 0, 40)
h_diphoMass_pre5 = TH1F("h_diphoMass_pre5", "h_diphoMass_pre5", 80, 0, 40)
h_diphoMass_pre6 = TH1F("h_diphoMass_pre6", "h_diphoMass_pre6", 80, 0, 40)

#h_diphoMass_mgg0 = TH1F("h_diphoMass_mgg0", "h_diphoMass_mgg0", 60, 0, 30)
#h_diphoMass_sba0 = TH1F("h_diphoMass_sba0", "h_diphoMass_sba0", 60, 0, 30)

c_dat0 = 0
for ev_dat0 in t_dat0:
    c_dat0 += 1
    if (ev_dat0.NNScore > 0.2):
        h_diphoMass_pre0.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.3):
        h_diphoMass_pre1.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.4):
        h_diphoMass_pre2.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.5):
        h_diphoMass_pre3.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.6):
        h_diphoMass_pre4.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.8):
        h_diphoMass_pre5.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.9):
        h_diphoMass_pre6.Fill(ev_dat0.dipho_mass)    

    
# Plotting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

canvasname = "c_sculpting"
c1 = TCanvas(canvasname,canvasname,1200,900)
c1.cd()
#c1.SetLeftMargin(0.15)

c1.SetBottomMargin(0.1)
c1.SetLeftMargin(1.9)

h_diphoMass_pre0.GetXaxis().SetTitle("m_{#gamma#gamma}")
h_diphoMass_pre0.GetYaxis().SetTitle("Events")
h_diphoMass_pre0.GetYaxis().SetTitleOffset(1.9)
h_diphoMass_pre0.GetYaxis().SetTitleSize(25)
h_diphoMass_pre0.GetYaxis().SetTitleFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelFont(43)
h_diphoMass_pre0.GetYaxis().SetLabelOffset(0.01)
h_diphoMass_pre0.GetYaxis().SetLabelSize(25)
h_diphoMass_pre0.SetLineWidth(2)
h_diphoMass_pre0.SetLineColor(kCyan-3)

h_diphoMass_pre1.SetLineWidth(2)
h_diphoMass_pre1.SetLineColor(kAzure+1)
h_diphoMass_pre2.SetLineWidth(2)
h_diphoMass_pre2.SetLineColor(kGreen-8)
h_diphoMass_pre3.SetLineWidth(2)
h_diphoMass_pre3.SetLineColor(kBlue-7)
h_diphoMass_pre4.SetLineWidth(2)
h_diphoMass_pre4.SetLineColor(kViolet-4)
h_diphoMass_pre5.SetLineWidth(2)
h_diphoMass_pre5.SetLineColor(kMagenta-7)
h_diphoMass_pre6.SetLineWidth(2)
h_diphoMass_pre6.SetLineColor(kPink+4)

h_diphoMass_pre1.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre2.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre3.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre4.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre5.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre6.SetMaximum(2.5*h_diphoMass_pre6.GetMaximum())
h_diphoMass_pre0.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre0.Integral())
h_diphoMass_pre1.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre1.Integral())
h_diphoMass_pre2.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre2.Integral())
h_diphoMass_pre3.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre3.Integral())
h_diphoMass_pre4.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre4.Integral())
h_diphoMass_pre5.Scale(h_diphoMass_pre6.Integral()/h_diphoMass_pre5.Integral())
h_diphoMass_pre0.Draw("hist")
h_diphoMass_pre1.Draw("hist same")
h_diphoMass_pre2.Draw("hist same")
h_diphoMass_pre3.Draw("hist same")
h_diphoMass_pre4.Draw("hist same")
h_diphoMass_pre5.Draw("hist same")
h_diphoMass_pre6.Draw("hist same")

leg = TLegend(0.35,0.15,0.7,0.45)
#leg = TLegend(0.15,0.55,0.6,0.88)
leg.AddEntry(h_diphoMass_pre0,"NN score > 0.2")
leg.AddEntry(h_diphoMass_pre1,"NN score > 0.3")
leg.AddEntry(h_diphoMass_pre2,"NN score > 0.4")
leg.AddEntry(h_diphoMass_pre3,"NN score > 0.5")
leg.AddEntry(h_diphoMass_pre4,"NN score > 0.6")
leg.AddEntry(h_diphoMass_pre5,"NN score > 0.8")
leg.AddEntry(h_diphoMass_pre6,"NN score > 0.9")
leg.SetLineWidth(0)
leg.Draw("same")

line = TLine(70, 0, 70, h_diphoMass_pre0.GetMaximum())
line.SetLineStyle(2)
line.Draw("same")

#CMS Title and Lumi info
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_NNbins_norm.png")
c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_NNbins_norm.pdf")
