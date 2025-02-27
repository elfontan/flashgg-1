from ROOT import *
from ROOT import gSystem, gROOT
import ROOT, array, random, copy
from ROOT import TCanvas,  TFile, TTree, TList, TH1, TH1F, TF1, TChain
import CMSGraphics, CMS_lumi, random
import sys
import os
import argparse 

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


# Get trees and create histograms for data
# ----------------------------------------
t_dat0 = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")

h_diphoMass_nn1_dr0 = TH1F("h_diphoMass_nn1_dr0", "h_diphoMass_nn1_dr0", 70, 0, 70)
h_diphoMass_nn1_dr1 = TH1F("h_diphoMass_nn1_dr1", "h_diphoMass_nn1_dr1", 70, 0, 70)
h_diphoMass_nn1_dr2 = TH1F("h_diphoMass_nn1_dr2", "h_diphoMass_nn1_dr2", 70, 0, 70)

#h_diphoMass_mgg0 = TH1F("h_diphoMass_mgg0", "h_diphoMass_mgg0", 60, 0, 30)
#h_diphoMass_sba0 = TH1F("h_diphoMass_sba0", "h_diphoMass_sba0", 60, 0, 30)

import math
c_dat0 = 0
for ev_dat0 in t_dat0:
    
    if (abs(ev_dat0.leadPhi - ev_dat0.subleadPhi) <= 3.14159265358979312):
        dr = math.sqrt((ev_dat0.leadEta - ev_dat0.subleadEta) ** 2 + (ev_dat0.leadPhi - ev_dat0.subleadPhi) ** 2)
    elif (abs(ev_dat0.leadPhi - ev_dat0.subleadPhi) > 3.14159265358979312):
        dr = math.sqrt((ev_dat0.leadEta - ev_dat0.subleadEta) ** 2 + (2*3.14159265358979312 - abs(ev_dat0.leadPhi - ev_dat0.subleadPhi)) ** 2)

    c_dat0 += 1
    if (ev_dat0.NNScore > 0.5 and (dr >= 0.3 and dr < 0.5)):
        h_diphoMass_nn1_dr0.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.5 and (dr >= 0.5 and dr < 0.8)):
        h_diphoMass_nn1_dr1.Fill(ev_dat0.dipho_mass)    
    if (ev_dat0.NNScore > 0.5 and (dr >= 0.8 and dr < 1.2)):
        h_diphoMass_nn1_dr2.Fill(ev_dat0.dipho_mass)    

    
# Plotting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

canvasname = "c_sculpting"
c1 = TCanvas(canvasname,canvasname,1200,600)
c1.cd()
#c1.SetLeftMargin(0.15)

c1.SetBottomMargin(0.1)
c1.SetLeftMargin(1.9)

h_diphoMass_nn1_dr0.GetXaxis().SetTitle("m_{#gamma#gamma}")
h_diphoMass_nn1_dr0.GetYaxis().SetTitle("Events")
h_diphoMass_nn1_dr0.GetYaxis().SetTitleOffset(1.9)
h_diphoMass_nn1_dr0.GetYaxis().SetTitleSize(25)
h_diphoMass_nn1_dr0.GetYaxis().SetTitleFont(43)
h_diphoMass_nn1_dr0.GetYaxis().SetLabelFont(43)
h_diphoMass_nn1_dr0.GetYaxis().SetLabelOffset(0.01)
h_diphoMass_nn1_dr0.GetYaxis().SetLabelSize(25)
h_diphoMass_nn1_dr0.SetLineWidth(2)
h_diphoMass_nn1_dr0.SetLineColor(kCyan-3)

h_diphoMass_nn1_dr1.SetLineColor(kBlue-7)
h_diphoMass_nn1_dr1.SetLineWidth(2)
h_diphoMass_nn1_dr2.SetLineColor(kMagenta-7)
h_diphoMass_nn1_dr2.SetLineWidth(2)

h_diphoMass_nn1_dr0.SetMaximum(1.5*h_diphoMass_nn1_dr0.GetMaximum())
h_diphoMass_nn1_dr1.SetMaximum(1.5*h_diphoMass_nn1_dr0.GetMaximum())
h_diphoMass_nn1_dr2.SetMaximum(1.5*h_diphoMass_nn1_dr0.GetMaximum())

h_diphoMass_nn1_dr0.Draw("hist")
h_diphoMass_nn1_dr1.Draw("hist same")
h_diphoMass_nn1_dr2.Draw("hist same")

leg = TLegend(0.55,0.6,0.88,0.88)
leg.AddEntry(h_diphoMass_nn1_dr0,"dR = [0.3, 0.5], NN score > 0.5")
leg.AddEntry(h_diphoMass_nn1_dr1,"dR = [0.5, 0.8], NN score > 0.5")
leg.AddEntry(h_diphoMass_nn1_dr2,"dR = [0.8, 1.2], NN score > 0.5")
leg.SetLineWidth(0)
leg.Draw("same")


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
c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_NN0p5_dr.png")
c1.SaveAs(outputdir+"/diphoMass_allDataPreselOnly_NN0p5_dr.pdf")
