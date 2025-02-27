# Gen Plots

# import ROOT in batch mode
import numpy as np
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
from ROOT import *
gROOT.SetBatch(True)
sys.argv = oldargv
gStyle.SetOptStat(0)
gStyle.SetOptFit(1)

from array import array
import CMS_lumi

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, help='name of variable as directory folder')
parser.add_argument('--label', type=str, help='name of variable as x-axis label')
args = parser.parse_args()
var = args.name
lbl = args.label


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)

c1 = TCanvas("c1","c1",1000,800)
c1.cd()
c1.SetLeftMargin(0.15)
#c1.SetLogy()

gghfile = TFile(var+"/gen_ggh30.root", "READ")
genggh = gghfile.Get("gen"+var.lower()+"ggh")
genggh.SetXTitle(lbl)
genggh.SetYTitle("Gen Level Events")
genggh.SetMinimum(0.0)
if (var=="LeadEta" or var=="SubleadEta"): genggh.SetMaximum(5500.0)
genggh.SetLineColor(kRed+2)
genggh.Draw("histsame")

alpfile = TFile(var+"/gen_alp30.root", "READ")
genalp = alpfile.Get("gen"+var.lower()+"alp")
genalp.SetMinimum(0.0)
genalp.SetLineColor(kViolet-6)
genalp.Draw("histsame")

gghfileacc = TFile(var+"/gen_ggh30acc.root", "READ")
gengghacc = gghfileacc.Get("gen"+var.lower()+"gghacc")
gengghacc.SetMinimum(0.0)
gengghacc.SetLineColor(kRed-7)
gengghacc.SetLineStyle(2)
gengghacc.Draw("histsame")

alpfileacc = TFile(var+"/gen_alp30acc.root", "READ")
genalpacc = alpfileacc.Get("gen"+var.lower()+"alpacc")
genalpacc.SetMinimum(0.0)
genalpacc.SetLineColor(kViolet-4)
genalpacc.SetLineStyle(2)
genalpacc.Draw("histsame")

if (var=="DR"):
  cat03 = TLine(0.3,0.0,0.3,3000.0)
  cat03.SetLineColor(28)
  cat03.SetLineWidth(3)
  cat03.SetLineStyle(2)
  cat03.Draw("same")

if (var=="DR"): leg = TLegend(0.18,0.58,0.53,0.88)
else: leg = TLegend(0.50,0.65,0.85,0.85)
leg.SetBorderSize(0)
#leg.SetTextSize(0.2)
leg.SetHeader("30 GeV BSM Models","C")
if (var=="DR"):
  leg.AddEntry(genggh,"ggH: "+str(np.round(genggh.Integral(0,12)/genggh.Integral()*100,2))+"% events with dR < 0.3","l")
  leg.AddEntry(genalp,"ALP: "+str(np.round(genalp.Integral(0,12)/genalp.Integral()*100,2))+"% events with dR < 0.3","l")
  leg.AddEntry(gengghacc,"ggH: "+str(round(gengghacc.Integral()/genggh.Integral()*100,2))+"% in Acceptance Region and","l")
  leg.AddEntry(0,str(np.round(gengghacc.Integral(0,12)/gengghacc.Integral()*100,2))+"% in Acceptance Region with dR < 0.3","")
  leg.AddEntry(genalpacc,"ALP: "+str(round(genalpacc.Integral()/genalp.Integral()*100,2))+"% in Acceptance Region and","l")
  leg.AddEntry(0,str(np.round(genalpacc.Integral(0,12)/genalpacc.Integral()*100,2))+"% in Acceptance Region with dR < 0.3","")
else:
  leg.AddEntry(genggh,"ggH at Gen Level")
  leg.AddEntry(genalp,"ALP at Gen Level")
  leg.AddEntry(gengghacc,"ggH: "+str(round(gengghacc.Integral()/genggh.Integral()*100,2))+"% in Acceptance Region")
  leg.AddEntry(genalpacc,"ALP: "+str(round(genalpacc.Integral()/genalp.Integral()*100,2))+"% in Acceptance Region")
leg.Draw("same")

#CMS lumi stuff
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = " Simulation Preliminary"
CMS_lumi.lumi_sqrtS     = "2018 (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c1, 0, 0)

c1.Update()
c1.SaveAs("/eos/user/a/atsatsos/www/ALPMCDistributions_DEC2024/sig_gen_"+var.lower()+"_30gev.png")
c1.SaveAs("/eos/user/a/atsatsos/www/ALPMCDistributions_DEC2024/sig_gen_"+var.lower()+"_30gev.pdf")

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
c1.SaveAs("/eos/user/a/atsatsos/www/ALPMCDistributions_DEC2024/sig_gen_"+var.lower()+"_30gev_log.png")
c1.SaveAs("/eos/user/a/atsatsos/www/ALPMCDistributions_DEC2024/sig_gen_"+var.lower()+"_30gev_log.pdf")

