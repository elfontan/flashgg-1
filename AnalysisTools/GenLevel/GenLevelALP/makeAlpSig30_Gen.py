# -------------------------------------------------------------------------
# Very low mass diphoton analysis: Gen Plots
# ALP versus ggH comparisons
# -------------------------------------------------------------------------

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
from genfiles import *
import CMS_lumi


# load FWLite C++ libraries
# -------------------------
gSystem.Load("libFWCoreFWLite.so");
gSystem.Load("libDataFormatsFWLite.so");
FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

gen, genLabel = Handle("GenEventInfoProduct"), ("generator")
handlePruned, prunedLabel  = Handle("std::vector<reco::GenParticle>"), ("prunedGenParticles")

# Making Histograms
# -------------------------
# alpj
eventsalpj = Events(alpjfiles30)

genalpj = TH1F("genalpj","genalpj", 200,0,5); genalpj.Sumw2()
genalpjacc = TH1F("genalpjacc","genalpjacc", 200,0,5); genalpjacc.Sumw2()

genleadetaalpj = TH1F("genleadetaalpj","genleadetaalpj", 180,-6,6); genleadetaalpj.Sumw2()
genleadetaalpjacc = TH1F("genleadetaalpjacc","genleadetaalpjacc", 180,-6,6); genleadetaalpjacc.Sumw2()
gensubleadetaalpj = TH1F("gensubleadetaalpj","gensubleadetaalpj", 180,-6,6); gensubleadetaalpj.Sumw2()
gensubleadetaalpjacc = TH1F("gensubleadetaalpjacc","gensubleadetaalpjacc", 180,-6,6); gensubleadetaalpjacc.Sumw2()

genleadptalpj = TH1F("genleadptalpj","genleadptalpj", 200,0,200); genleadptalpj.Sumw2()
genleadptalpjacc = TH1F("genleadptalpjacc","genleadptalpjacc", 200,0,200); genleadptalpjacc.Sumw2()
gensubleadptalpj = TH1F("gensubleadptalpj","gensubleadptalpj", 200,0,200); gensubleadptalpj.Sumw2()
gensubleadptalpjacc = TH1F("gensubleadptalpjacc","gensubleadptalpjacc", 200,0,200); gensubleadptalpjacc.Sumw2()

gendiphotonptalpj = TH1F("gendiphotonptalpj","gendiphotonptalpj", 200,0,400); gendiphotonptalpj.Sumw2()
gendiphotonptalpjacc = TH1F("gendiphotonptalpjacc","gendiphotonptalpjacc", 200,0,400); gendiphotonptalpjacc.Sumw2()
gendralpj = TH1F("gendralpj","gendralpj", 200,0,5); gendralpj.Sumw2()
gendralpjacc = TH1F("gendralpjacc","gendralpjacc", 200,0,5); gendralpjacc.Sumw2()

genmassalpj = TH1F("genmassalpj","genmassalpj", 200,29.75,30.25); genmassalpj.Sumw2()
genmassalpjacc = TH1F("genmassalpjacc","genmassalpjacc", 200,29.75,30.25); genmassalpjacc.Sumw2()

for i,event in enumerate(eventsalpj):
  w = 0
  #print("------------------- Event",i)
  if (i%1000==0): print(i)
  if (i==150000): break
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)
  #if (i%1000==0): print(gen.product().weight())

  if (gen.product().weight() > 0.0): w = 1.0
  elif (gen.product().weight() < 0.0): w = -1.0
  pruned = handlePruned.product()

  npho=0;
  photons = []
  phom=TLorentzVector(0,0,0,0)

  for p in pruned:
    if (abs(p.pdgId())==22 and p.status()==1):
      pho=TLorentzVector(p.px(),p.py(),p.pz(),p.energy())
      photons.append((pho.Pt(), pho))

  npho = len(photons)
  #print("Number of photons = ", npho)

  if npho>=2:
    photons.sort(key=lambda x: x[0], reverse=True)
        
    #for index, (pt, pho) in enumerate(photons):
    #  print("pho["+str(index)+"].Pt() = "+str(pt))
    #  print("---------------------------")
        
    # Combine the two leading photons
    phom = photons[0][1] + photons[1][1]

    phodr = np.sqrt((photons[0][1].Eta()-photons[1][1].Eta())*(photons[0][1].Eta()-photons[1][1].Eta())+(photons[0][1].Phi()-photons[1][1].Phi())*(photons[0][1].Phi()-photons[1][1].Phi()))
    if(abs(photons[0][1].Phi()-photons[1][1].Phi()) > np.pi): phodr = np.sqrt( (photons[0][1].Eta()-photons[1][1].Eta())*(photons[0][1].Eta()-photons[1][1].Eta()) + (2*np.pi-(photons[0][1].Phi()-photons[1][1].Phi()))*(2*np.pi-(photons[0][1].Phi()-photons[1][1].Phi())) )
    gendralpj.Fill(phodr,w)
    genmassalpj.Fill(phom.M(),w)
    gendiphotonptalpj.Fill(phom.Pt(),w)
    genleadptalpj.Fill(max(photons[0][1].Pt(),photons[1][1].Pt()),w)
    gensubleadptalpj.Fill(min(photons[0][1].Pt(),photons[1][1].Pt()),w)
    if (photons[0][1].Pt() > photons[1][1].Pt()):
      genleadetaalpj.Fill(photons[0][1].Eta(),w)
      gensubleadetaalpj.Fill(photons[1][1].Eta(),w)
    else:
      genleadetaalpj.Fill(photons[1][1].Eta(),w)
      gensubleadetaalpj.Fill(photons[0][1].Eta(),w)
    if ((photons[0][1].Pt()>30.0 and photons[1][1].Pt()>18.0) or (photons[0][1].Pt()>18.0 and photons[1][1].Pt()>30.0)):
      if (abs(photons[0][1].Eta())<2.5 and abs(photons[1][1].Eta())<2.5):
        gendralpjacc.Fill(phodr,w)
        genmassalpjacc.Fill(phom.M(),w)
        gendiphotonptalpjacc.Fill(phom.Pt(),w)
        genleadptalpjacc.Fill(max(photons[0][1].Pt(),photons[1][1].Pt()),w)
        gensubleadptalpjacc.Fill(min(photons[0][1].Pt(),photons[1][1].Pt()),w)
        if (photons[0][1].Pt() > photons[1][1].Pt()):
          genleadetaalpjacc.Fill(photons[0][1].Eta(),w)
          gensubleadetaalpjacc.Fill(photons[1][1].Eta(),w)
        else:
          genleadetaalpjacc.Fill(photons[1][1].Eta(),w)
          gensubleadetaalpjacc.Fill(photons[0][1].Eta(),w)

genleadetaalpj.SaveAs("Plots/LeadEta/gen_alpj30.root")
gensubleadetaalpj.SaveAs("Plots/SubleadEta/gen_alpj30.root")
genleadptalpj.SaveAs("Plots/LeadPT/gen_alpj30.root")
gensubleadptalpj.SaveAs("Plots/SubleadPT/gen_alpj30.root")
gendiphotonptalpj.SaveAs("Plots/DiphotonPT/gen_alpj30.root")
gendralpj.SaveAs("Plots/DR/gen_alpj30.root")
genmassalpj.SaveAs("Plots/Mass/gen_alpj30.root")

genleadetaalpjacc.SaveAs("Plots/LeadEta/gen_alpj30acc.root")
gensubleadetaalpjacc.SaveAs("Plots/SubleadEta/gen_alpj30acc.root")
genleadptalpjacc.SaveAs("Plots/LeadPT/gen_alpj30acc.root")
gensubleadptalpjacc.SaveAs("Plots/SubleadPT/gen_alpj30acc.root")
gendiphotonptalpjacc.SaveAs("Plots/DiphotonPT/gen_alpj30acc.root")
gendralpjacc.SaveAs("Plots/DR/gen_alpj30acc.root")
genmassalpjacc.SaveAs("Plots/Mass/gen_alpj30acc.root")
