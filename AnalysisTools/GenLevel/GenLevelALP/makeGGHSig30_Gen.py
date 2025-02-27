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
# --------------------------
#ggh
eventsggh = Events(gghfiles30)

genleadetaggh = TH1F("genleadetaggh","genleadetaggh", 180,-6,6); genleadetaggh.Sumw2()
genleadetagghacc = TH1F("genleadetagghacc","genleadetagghacc", 180,-6,6); genleadetagghacc.Sumw2()
gensubleadetaggh = TH1F("gensubleadetaggh","gensubleadetaggh", 180,-6,6); gensubleadetaggh.Sumw2()
gensubleadetagghacc = TH1F("gensubleadetagghacc","gensubleadetagghacc", 180,-6,6); gensubleadetagghacc.Sumw2()

genleadptggh = TH1F("genleadptggh","genleadptggh", 200,0,200); genleadptggh.Sumw2()
genleadptgghacc = TH1F("genleadptgghacc","genleadptgghacc", 200,0,200); genleadptgghacc.Sumw2()
gensubleadptggh = TH1F("gensubleadptggh","gensubleadptggh", 200,0,200); gensubleadptggh.Sumw2()
gensubleadptgghacc = TH1F("gensubleadptgghacc","gensubleadptgghacc", 200,0,200); gensubleadptgghacc.Sumw2()

gendiphotonptggh = TH1F("gendiphotonptggh","gendiphotonptggh", 200,0,400); gendiphotonptggh.Sumw2()
gendiphotonptgghacc = TH1F("gendiphotonptgghacc","gendiphotonptgghacc", 200,0,400); gendiphotonptgghacc.Sumw2()
gendrggh = TH1F("gendrggh","gendrggh", 200,0,5); gendrggh.Sumw2()
gendrgghacc = TH1F("gendrgghacc","gendrgghacc", 200,0,5); gendrgghacc.Sumw2()

for i,event in enumerate(eventsggh):
  if (i%1000==0): print(i)
  if (i==150000): break
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (gen.product().weight() > 0.0): w = 1.0
  #elif (gen.product().weight() < 0.0): w = 1.0
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
      #print("pho["+str(index)+"].Pt() = "+str(pt))
      #print("---------------------------")
        
    # Combine the two leading photons
    phom = photons[0][1] + photons[1][1]

    phodr = np.sqrt((photons[0][1].Eta()-photons[1][1].Eta())*(photons[0][1].Eta()-photons[1][1].Eta())+(photons[0][1].Phi()-photons[1][1].Phi())*(photons[0][1].Phi()-photons[1][1].Phi()))
    if(abs(photons[0][1].Phi()-photons[1][1].Phi()) > np.pi): phodr = np.sqrt( (photons[0][1].Eta()-photons[1][1].Eta())*(photons[0][1].Eta()-photons[1][1].Eta()) + (2*np.pi-(photons[0][1].Phi()-photons[1][1].Phi()))*(2*np.pi-(photons[0][1].Phi()-photons[1][1].Phi())) )
    gendrggh.Fill(phodr,w)
    gendiphotonptggh.Fill(phom.Pt(),w)
    genleadptggh.Fill(max(photons[0][1].Pt(),photons[1][1].Pt()),w)
    gensubleadptggh.Fill(min(photons[0][1].Pt(),photons[1][1].Pt()),w)
    genleadetaggh.Fill(photons[0][1].Eta(),w)
    gensubleadetaggh.Fill(photons[1][1].Eta(),w)
    if ((photons[0][1].Pt()>30.0 and photons[1][1].Pt()>18.0) or (photons[0][1].Pt()>18.0 and photons[1][1].Pt()>30.0)):
      if (abs(photons[0][1].Eta())<2.5 and abs(photons[1][1].Eta())<2.5):
        gendrgghacc.Fill(phodr,w)
        gendiphotonptgghacc.Fill(phom.Pt(),w)
        genleadptgghacc.Fill(max(photons[0][1].Pt(),photons[1][1].Pt()),w)
        gensubleadptgghacc.Fill(min(photons[0][1].Pt(),photons[1][1].Pt()),w)
        genleadetagghacc.Fill(photons[0][1].Eta(),w)
        gensubleadetagghacc.Fill(photons[1][1].Eta(),w)

genleadetaggh.SaveAs("Plots/LeadEta/gen_ggh30.root")
gensubleadetaggh.SaveAs("Plots/SubleadEta/gen_ggh30.root")
genleadptggh.SaveAs("Plots/LeadPT/gen_ggh30.root")
gensubleadptggh.SaveAs("Plots/SubleadPT/gen_ggh30.root")
gendiphotonptggh.SaveAs("Plots/DiphotonPT/gen_ggh30.root")
gendrggh.SaveAs("Plots/DR/gen_ggh30.root")

genleadetagghacc.SaveAs("Plots/LeadEta/gen_ggh30acc.root")
gensubleadetagghacc.SaveAs("Plots/SubleadEta/gen_ggh30acc.root")
genleadptgghacc.SaveAs("Plots/LeadPT/gen_ggh30acc.root")
gensubleadptgghacc.SaveAs("Plots/SubleadPT/gen_ggh30acc.root")
gendiphotonptgghacc.SaveAs("Plots/DiphotonPT/gen_ggh30acc.root")
gendrgghacc.SaveAs("Plots/DR/gen_ggh30acc.root")
