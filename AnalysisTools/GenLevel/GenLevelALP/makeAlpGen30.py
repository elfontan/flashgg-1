# Gen Plots - done for ggh but need to edit for ALP!!

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

#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument('--name', type=str, help='name of variable as directory folder',choices=['LeadEta', 'SubleadEta', 'LeadPT', 'SubleadPT', 'DiphotonPT', 'DR'])
#args = parser.parse_args()
#var = args.name

# load FWLite C++ libraries
gSystem.Load("libFWCoreFWLite.so");
gSystem.Load("libDataFormatsFWLite.so");
#AutoLibraryLoader.enable()
FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

gen, genLabel = Handle("GenEventInfoProduct"), ("generator")
#handlePruned, prunedLabel  = Handle("std::vector<reco::GenParticle>"), ("genParticles")
handlePruned, prunedLabel  = Handle("std::vector<reco::GenParticle>"), ("prunedGenParticles")

# -----------------------
# Making Histograms: ALP
# -----------------------
eventsalp = Events(alpfiles30)

genalp = TH1F("genalp","genalp", 200,0,5); genalp.Sumw2()
genalpacc = TH1F("genalpacc","genalpacc", 200,0,5); genalpacc.Sumw2()

genleadetaalp = TH1F("genleadetaalp","genleadetaalp", 180,-6,6); genleadetaalp.Sumw2()
genleadetaalpacc = TH1F("genleadetaalpacc","genleadetaalpacc", 180,-6,6); genleadetaalpacc.Sumw2()
gensubleadetaalp = TH1F("gensubleadetaalp","gensubleadetaalp", 180,-6,6); gensubleadetaalp.Sumw2()
gensubleadetaalpacc = TH1F("gensubleadetaalpacc","gensubleadetaalpacc", 180,-6,6); gensubleadetaalpacc.Sumw2()

genleadptalp = TH1F("genleadptalp","genleadptalp", 200,0,200); genleadptalp.Sumw2()
genleadptalpacc = TH1F("genleadptalpacc","genleadptalpacc", 200,0,200); genleadptalpacc.Sumw2()
gensubleadptalp = TH1F("gensubleadptalp","gensubleadptalp", 200,0,200); gensubleadptalp.Sumw2()
gensubleadptalpacc = TH1F("gensubleadptalpacc","gensubleadptalpacc", 200,0,200); gensubleadptalpacc.Sumw2()

gendiphotonptalp = TH1F("gendiphotonptalp","gendiphotonptalp", 200,0,400); gendiphotonptalp.Sumw2()
gendiphotonptalpacc = TH1F("gendiphotonptalpacc","gendiphotonptalpacc", 200,0,400); gendiphotonptalpacc.Sumw2()
gendralp = TH1F("gendralp","gendralp", 200,0,5); gendralp.Sumw2()
gendralpacc = TH1F("gendralpacc","gendralpacc", 200,0,5); gendralpacc.Sumw2()



for i,event in enumerate(eventsalp):
  if (i==100): break
  #if (i%1000==0): print(i)
  #if (i==300000): break
  event.getByLabel(prunedLabel, handlePruned)
  event.getByLabel(genLabel, gen)

  if (gen.product().weight() != 0.0): w = 1.0
  pruned = handlePruned.product()

  npho=0;
  pho={}
  phom=TLorentzVector(0,0,0,0)

  for p in pruned:
    if (abs(p.pdgId())==22 and p.status()==1):
      pho[npho]=TLorentzVector(p.px(),p.py(),p.pz(),p.energy())
      npho+=1
      
  print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
  print("Number of photons: ", npho)

  if npho>=2:
    phom = pho[0]+pho[1]
    phodr = np.sqrt((pho[0].Eta()-pho[1].Eta())*(pho[0].Eta()-pho[1].Eta())+(pho[0].Phi()-pho[1].Phi())*(pho[0].Phi()-pho[1].Phi()))
    if(abs(pho[0].Phi()-pho[1].Phi()) > np.pi): phodr = np.sqrt( (pho[0].Eta()-pho[1].Eta())*(pho[0].Eta()-pho[1].Eta()) + (2*np.pi-(pho[0].Phi()-pho[1].Phi()))*(2*np.pi-(pho[0].Phi()-pho[1].Phi())) )
    gendralp.Fill(phodr,w)
    gendiphotonptalp.Fill(phom.Pt(),w)
    genleadptalp.Fill(max(pho[0].Pt(),pho[1].Pt()),w)
    gensubleadptalp.Fill(min(pho[0].Pt(),pho[1].Pt()),w)
    print("Diphoton pt = ", phom.Pt())

    if (pho[0].Pt() > pho[1].Pt()):
      genleadetaalp.Fill(pho[0].Eta())
      gensubleadetaalp.Fill(pho[1].Eta())
    else:
      genleadetaalp.Fill(pho[1].Eta())
      gensubleadetaalp.Fill(pho[0].Eta())
    if ((pho[0].Pt()>30.0 and pho[1].Pt()>18.0) or (pho[0].Pt()>18.0 and pho[1].Pt()>30.0)):
      if (abs(pho[0].Eta())<2.5 and abs(pho[1].Eta())<2.5):
        gendralpacc.Fill(phodr,w)
        gendiphotonptalpacc.Fill(phom.Pt(),w)
        genleadptalpacc.Fill(max(pho[0].Pt(),pho[1].Pt()),w)
        gensubleadptalpacc.Fill(min(pho[0].Pt(),pho[1].Pt()),w)
        if (pho[0].Pt() > pho[1].Pt()):
          genleadetaalpacc.Fill(pho[0].Eta())
          gensubleadetaalpacc.Fill(pho[1].Eta())
        else:
          genleadetaalpacc.Fill(pho[1].Eta())
          gensubleadetaalpacc.Fill(pho[0].Eta())

# ---------------
# Save histograms
# ---------------
#genleadetaalp.SaveAs("Plots/LeadEta/gen_alp30.root")
#gensubleadetaalp.SaveAs("Plots/SubleadEta/gen_alp30.root")
#genleadptalp.SaveAs("Plots/LeadPT/gen_alp30.root")
#gensubleadptalp.SaveAs("Plots/SubleadPT/gen_alp30.root")
#gendiphotonptalp.SaveAs("Plots/DiphotonPT/gen_alp30.root")
#gendralp.SaveAs("Plots/DR/gen_alp30.root")

#genleadetaalpacc.SaveAs("Plots/LeadEta/gen_alp30acc.root")
#gensubleadetaalpacc.SaveAs("Plots/SubleadEta/gen_alp30acc.root")
#genleadptalpacc.SaveAs("Plots/LeadPT/gen_alp30acc.root")
#gensubleadptalpacc.SaveAs("Plots/SubleadPT/gen_alp30acc.root")
#gendiphotonptalpacc.SaveAs("Plots/DiphotonPT/gen_alp30acc.root")
#gendralpacc.SaveAs("Plots/DR/gen_alp30acc.root")
