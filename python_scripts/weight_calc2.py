import ROOT
import sys 
import numpy as np
from helpful_functions import *

ROOT.gStyle.SetOptStat(0)
ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")



pb1 = ROOT.TFile("pb1.0_IntEvChannel_plusbreakdown_sameseed.root")
pb0  = ROOT.TFile("pb0.0_IntEvChannel_plusbreakdown_sameseed.root")
pb05  = ROOT.TFile("pb0.5_IntEvChannel_plusbreakdown_sameseed.root")


pb1_survival_histo = pb1.Get("Survival_histo").GetListOfPrimitives().FindObject("Survival_histo")
pb0_survival_histo = pb0.Get("Survival_histo").GetListOfPrimitives().FindObject("Survival_histo")
pb05_survival_histo = pb05.Get("Survival_histo").GetListOfPrimitives().FindObject("Survival_histo")

pb_param_vs_KE = ROOT.TH2F("pb_param_vs_KE", "Interaction Type Against nucleon Energy",180,0, 3000,4,1,4)

for i in range(1, 181):
    x = pb1_survival_histo.GetBinCenter(i)
    #x = pb1_survival_histo.GetBinContent(i)
#    x = pb1_survival_histo.GetBinContent(i)
    print(x)
    pb_param_vs_KE.Fill(pb0_survival_histo.GetBinCenter(i),1,pb0_survival_histo.GetBinContent(i)/pb0_survival_histo.GetBinContent(i))
    pb_param_vs_KE.Fill(pb05_survival_histo.GetBinCenter(i),2,pb05_survival_histo.GetBinContent(i)/pb0_survival_histo.GetBinContent(i))
    pb_param_vs_KE.Fill(pb1_survival_histo.GetBinCenter(i),3,pb1_survival_histo.GetBinContent(i)/pb0_survival_histo.GetBinContent(i))

file = ROOT.TFile("pb_param_vs_KE.root", "RECREATE") # or "UPDATE" if you already have the file

canvas = ROOT.TCanvas("canvas5", "blargh2", 800, 600)
pb_param_vs_KE.Draw()
canvas.Write("pbvke")

file.Close()
    


