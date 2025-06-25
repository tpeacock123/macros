import ROOT
import sys 
import numpy as np
import array
import pandas as pd 
from memory_profiler import profile
from nucleon_helpful_functions import *
import time

from cppyy.ll import cast

from pympler.tracker import SummaryTracker


ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

def __main__():
    plotlist = []
    histo = ROOT.TH1F()
    histo_dict = {
        0.0: [],
        0.25: [],
        0.5:[],
        0.75:[],
        1.0:[]
    }
    
    f=[]
    for pbv in histo_dict:
        file = "input_nuclroot_files/nucleon_pb{pbval}_1milevts.root".format(pbval = pbv)
        file = ROOT.TFile(file)
        f.append(file)
        histo_dict[pbv] =  ratio_histo(file,pbv)    

    clone_histo_0 = histo_dict[0.0][0].Clone()
    for pbv in histo_dict:
        clone_histo = histo_dict[pbv][0].Clone()
        clone_histo.Divide(clone_histo_0)
        plotlist.append(clone_histo)

    ratioplots = ROOT.TH2F("pbvsKE","pbvsKE",15,0.,800.,len(histo_dict),0,len(histo_dict))

    for i in range(len(plotlist)):
        for j in range(1,plotlist[i].GetNbinsX()):
            ratioplots.Fill(plotlist[i].GetBinCenter(j),i, (plotlist[i].GetBinContent(j)))

    file = ROOT.TFile("nucleonsurvivalhistos_og.root", "RECREATE")
    for hist in histo_dict.values():
        hist[0].Write()
        hist[1].Write()
    ratioplots.Write()
    file.Close()

@profile
def ratio_histo(file,pb):
    print(file)
    t = file.Get("neuttree")
    name = "surivial_histo_{pb_}".format(pb_ = pb)
    survival_histo = ROOT.TH1F(name, "histo",15,0,800)
    name = "initke_histo_{pb_}".format(pb_ = pb)
    initke_histo = ROOT.TH1F(name, "histo",15,0,800)

    counter = 0
    nv = ROOT.NeutVect()
    address = ROOT.addressof(nv,byref = True)
    t.SetBranchAddress("vectorbranch",cast['void*'](address))
    for i in range(t.GetEntries()):
        t.GetEntry(i)

        if i == 10000:
            break
        elif i % 1000 == 0:
            print(i)
        nvt = nucleon_nvect_reader(nv)
        x = nvt.nucleon_survival()    
        initke_histo.Fill(x[2])
        if x[0] ==1:
            survival_histo.Fill(x[2])

    name = "ratio_histo_{pb_}".format(pb_ = pb)
    ratio_histo = survival_histo.Clone(name)
    ratio_histo.Divide(initke_histo)
    return ratio_histo,initke_histo

start_time = time.time()
__main__()
print("--- %s seconds ---" % (time.time() - start_time))
