from ROOT import *
import CMS_lumi
import ROOT, array, random, copy
from ROOT import TCanvas, TFile, TH1, TH1F, TF1, gSystem, TChain
import ROOT, array, CMS_lumi, random, copy
from ROOT import TFile, TTree, TList
from collections import OrderedDict
import argparse
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

argparser = argparse.ArgumentParser(description='Parser used for non default arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=True)
argparser.add_argument('--outdir', dest='outdir', default='./', help='Output dir')
argparser.add_argument('--log', dest='log', default=False, help='Log scale')

args = argparser.parse_args()
outputdir = args.outdir
logScale = args.log

# ----------------------
# Obtain histogram files
# ----------------------
f_dataDef = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Apr2024_flashggNtuples/data/EGamma_All_Summer20UL.root","READ")
f_dataNew = TFile("/eos/user/e/elfontan/DiPhotonAnalysis/Feb2025_ARCReviewTests/data2018D_noPtOverM.root","READ")

# Get trees and create histograms for data
# ----------------------------------------
datDef = f_dataDef.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
datNew = f_dataNew.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
#mgg0 = para.Get("tagsDumper/trees/mgg_bkg_13TeV_UntaggedTag_0")
#sig0_10 = para.Get("tagsDumper/trees/ggh_10_13TeV_UntaggedTag_0")

var_list = ["dipho_mass"]
label_list = ["m_{#gamma#gamma}"]

histo_datDef_list = OrderedDict()
histo_datNew_list = OrderedDict()

# Create a dictionary to store the binning information for each variable
# ----------------------------------------------------------------------
binning_info = { 
    var_list[0]: (160, 0., 80.),   #dipho_mass 
}

for variable in var_list:
    nbins, xlow, xhigh = binning_info[variable]
    print("var_list[i]", variable)
    print("nbins = ", nbins)
    print("xlow = ", xlow)
    print("xhigh = ", xhigh)
    histo_datDef_list[variable + "_datDef"] = TH1F("h_" + variable + "_datDef", "h_" + variable + "_datDef", nbins, xlow, xhigh)
    histo_datNew_list[variable + "_datNew"] = TH1F("h_" + variable + "_datNew", "h_" + variable + "_datNew", nbins, xlow, xhigh)


    # Fill the histograms
    datDef.Draw(variable + ">>h_" + variable + "_datDef", "CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7", "goff")     
    datNew.Draw(variable + ">>h_" + variable + "_datNew", "CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7", "goff")     
    #datDef.Draw(variable + ">>h_" + variable + "_dat0", "weight*weight_allDD*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")     
    #mgg0.Draw(variable + ">>h_" + variable + "_mgg0", "weight*weight_allDD*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")
    #sig0_10.Draw(variable + ">>+h_" + variable + "_sig0", "weight*(CMS_hgg_mass>0 && min(dipho_leadIDMVA,dipho_subleadIDMVA)>-0.7)", "goff")

idx = 0
for variable in var_list:
    print(variable)

    # MC Scaling
    datDef = histo_datDef_list[variable + "_datDef"]
    datNew = histo_datNew_list[variable + "_datNew"]
    #mgg0 = histo_mgg0_list[variable + "_mgg0"]
    #sig0 = histo_sig0_list[variable + "_sig0"]
    
    # Plotting
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    canvasname = "c_"+variable
    c1 = TCanvas(canvasname,canvasname,1200,1200)
    c1.cd()
    c1.SetLeftMargin(0.018)
    
    # Upper plot pad - Data histos
    pad1 = TPad("pad1","pad1", 0, 0.36, 1, 1.0)
    pad1.Draw()
    pad1.cd()
    #pad1.SetLogy()
    pad1.SetBottomMargin(0.01)
    pad1.SetLeftMargin(1.9)
    
    datDef.SetLineColor(kAzure-3)
    datDef.SetLineWidth(3)
    datNew.SetLineColor(kMagenta-7)
    datNew.SetLineWidth(3)
    
    datDef.GetXaxis().SetLabelSize(0)
      
    datDef.GetYaxis().SetTitle("A.U.")
    #datDef.GetYaxis().SetTitle("Events")
    #datDef.GetYaxis().SetTitleSize(25)
    datDef.GetYaxis().SetTitleFont(43)
    datDef.GetYaxis().SetTitleOffset(1.9)
    datDef.GetYaxis().SetLabelFont(43)
    datDef.GetYaxis().SetLabelOffset(0.01)
    datDef.GetYaxis().SetLabelSize(25)
    
    #datDef.Scale(datNew.Integral()/datDef.Integral())
    datNew.Scale(54.4/(31.95*171/300))
    datDef.SetMaximum(1.5*datDef.GetMaximum())
    datDef.Draw("histo")
    datNew.Draw("histo same")
        
    leg = TLegend(0.15,0.65,0.7,0.85)
    #leg = TLegend(0.45,0.35,0.85,0.55) #log
    leg.AddEntry(datDef,"Default preselection (2018)")
    leg.AddEntry(datNew,"Removing pt/m cut (2018D)")
    leg.SetLineWidth(0)
    leg.Draw("same")
    
    c1.Update()
    c1.cd()
    
    # Lower plot pad - Ratio plot
    pad2 = TPad("pad2","pad2", 0, 0.01, 1, 0.35)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    pad2.SetTopMargin(0.)
    pad2.SetBottomMargin(0.17)
    pad2.SetLeftMargin(0.11)
    
    # Define ratio plot
    rp = datNew.Clone("rp")
    rp.SetLineColor(kBlack)
    rp.SetMinimum(0.5)
    rp.SetMaximum(1.5)
    rp.SetStats(0)
    rp.Divide(datDef) 
    rp.SetMarkerStyle(22)
    rp.SetTitle("") 
    
    rp.SetYTitle("TestPresel/DefPresel")
    #rp.SetYTitle("DefPresel/TestPresel")
    rp.GetYaxis().SetNdivisions(505)
    rp.GetYaxis().SetTitleSize(25)
    rp.GetYaxis().SetTitleFont(43)
    rp.GetYaxis().SetTitleOffset(1.9)
    rp.GetYaxis().SetLabelFont(43)
    rp.GetYaxis().SetLabelSize(25)
    
    rp.SetXTitle(label_list[idx])
    rp.GetXaxis().SetTitleSize(25)
    rp.GetXaxis().SetTitleFont(43)
    rp.GetXaxis().SetTitleOffset(3.9)
    rp.GetXaxis().SetLabelFont(43)
    rp.GetXaxis().SetLabelSize(25)
    rp.GetXaxis().SetLabelOffset(0.02)
    
    rp.Draw("ep")
    #rp.SaveAs("ratios_"+variable+"_noWSig.root")
    
    c1.Update()
    c1.cd()
    
    #CMS Title and Lumi info
    CMS_lumi.writeExtraText = True
    CMS_lumi.extraText      = "Preliminary"
    CMS_lumi.lumi_sqrtS     = "2018D (13 TeV)"
    #CMS_lumi.lumi_sqrtS     = "54.4 fb^{-1} (13 TeV)"
    CMS_lumi.cmsTextSize    = 0.6
    CMS_lumi.lumiTextSize   = 0.46
    CMS_lumi.extraOverCmsTextSize = 0.75
    CMS_lumi.relPosX = 0.12
    CMS_lumi.CMS_lumi(pad1, 0, 0)
    
    c1.Update()
    c1.SaveAs(outputdir+"/"+variable+"_checkingPresel_2018D.png")
    c1.SaveAs(outputdir+"/"+variable+"_checkingPresel_2018D.pdf")
    
    idx += 1
    print("Data default preselection: ", datDef.Integral())
    print("Data updated preselection: ", datNew.Integral())
