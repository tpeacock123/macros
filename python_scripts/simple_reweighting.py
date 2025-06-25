import ROOT
import sys 
import numpy as np
import cppyy

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
ROOT.gSystem.Load("libNEUTUtils.so")

f = ROOT.TFile("pb1.0_1mil_forsurvival.root")



rw = NReWeight()
rw.AdoptWeightEngine("NuXSecRES", NuXSecRESEngine())
