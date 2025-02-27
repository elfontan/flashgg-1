# ------------------------------------------------------ #
# Use this script within an environment allowing python: #
# ------------------------------------------------------ #
#python3 prepareHisto_nnScore.py --pnn nearest_flat
from ROOT import TFile, TTree, TBranch, TList, gROOT, gSystem, TChain, TH1F, TCanvas, TLegend
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
argparser.add_argument('--pnn', dest='pnn', default='nearest_flat_plusFlatBkg_norm40', help='PNN case considerd')

args = argparser.parse_args()
scenario  = args.pnn

print("Data File Processing...")
f_data = ROOT.TFile.Open("/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/"+scenario+"/out_all2018Data_bkg_newSamplesFlat.root")
treeData = f_data.Get("tagsDumper/trees/Data_13TeV_UntaggedTag_0")
h_nnScore_data = TH1F("h_nnScore_data", "h_nnScore_data", 50, 0, 1)
h_nnScore_data.Sumw2()

treeData.Draw("NNScore>>h_nnScore_data", "(CMS_hgg_mass>0)", "goff")
#treeData.Draw("NNScore>>h_nnScore_data", "(CMS_hgg_mass>0 && event%10==0)", "goff")
print("Data File Processing Done.")

masses = [10,15,20,25,30,35,40,45,50,55,60,65,70]
#colors = [kMagenta-7, kOrange - 3,  kBlue, kAzure+7, kCyan-3, kTeal - 7, kSpring - 7]       
col_list = [kRed - 7, kPink - 6, kMagenta - 7, kViolet + 6, kBlue, kAzure + 7, kCyan - 3, kTeal - 7, kGreen, kSpring - 7, kYellow, kOrange - 3, kRed - 3]

output_file = ROOT.TFile.Open("histoFile_nnScores_allMC_data_arcReview.root", "RECREATE")
#output_file = ROOT.TFile.Open("histoFile_nnScores_allMC_data_paperDraft.root", "RECREATE")
output_file.cd()
h_nnScore_data.Write()

for mass in masses:
    #filename = dir+f"gghSig_Systematics/m{mass}/out_ggh_{mass}_13TeV_UntaggedTag_0.root"
    filename = f"/eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/{scenario}/out_ggH_M{mass}_newSamplesFlat.root"

    # Open the ROOT file
    # ------------------
    file = ROOT.TFile.Open(filename, "READ")
    
    # Get the tree
    # ------------
    tree = file.Get("tagsDumper/trees/ggh_"+str(mass)+"_13TeV_UntaggedTag_0")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("INPUTFile: ", file)
    print("TREE: ", tree)
    #tree.Print()
    histoname = "h_nnScore_M"+str(mass)
    histonameW = "h_nnScoreW_M"+str(mass)
    h =  TH1F(histoname, histoname, 50, 0, 1)
    h_w =  TH1F(histonameW, histonameW, 50, 0, 1)
    h.Sumw2()
    h_w.Sumw2()
    tree.Draw("NNScore>>h_nnScore_M"+str(mass), "(CMS_hgg_mass>0)", "goff")
    tree.Draw("NNScore>>h_nnScoreW_M"+str(mass), "weight*(CMS_hgg_mass>0)", "goff")
    output_file.cd()
    h.Write()
    h_w.Write()
    file.Close()
    
output_file.Close()
