import ROOT
import sys 
import time
import numpy as np
import pandas as pd 
from memory_profiler import profile, memory_usage
from nucleon_helpful_functions import *
from cppyy.ll import cast

ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

ROOT.TH1.AddDirectory(False)

def __main__():
    plotlist = []
    histo_dict = {
        0.0: [],
        0.25: [],
        0.5:[],
        0.75:[],
        1.0:[]
    }
    
    for pbv in histo_dict:
        print(1)
       # fil = "input_nuclroot_files/nucleon_pb{pbval}_1milevts.root".format(pbval = pbv)
        fil = "/mnt/macros/input_nuclroot_files/nucleon_pb1.0_1milevts.root"
        file = ROOT.TFile(fil)
        histo_dict[pbv] = ratio_histo(file,pbv) 

    clone_histo_0 = histo_dict[0.0][0].Clone()
    for pbv in histo_dict:
        clone_histo = histo_dict[pbv][0].Clone()
        clone_histo.Divide(clone_histo_0)
        plotlist.append(clone_histo)

    ratioplots = ROOT.TH2F("pbvsKE","pbvsKE",15,0.,800.,len(histo_dict),0,len(histo_dict))

    for i in range(len(plotlist)):
        for j in range(1,plotlist[i].GetNbinsX()):
            ratioplots.Fill(plotlist[i].GetBinCenter(j),i, (plotlist[i].GetBinContent(j)))

    file = ROOT.TFile("nucleonsurvivalhistos_2_every10.root", "RECREATE")
    for hist in histo_dict.values():
        hist[0].Write()
        hist[1].Write()
    ratioplots.Write()


@profile
def ratio_histo(file,pb):

    t = file.Get("neuttree")
    print(t)
    t.SetBranchStatus("*", 0)
    t.SetBranchStatus("vectorbranch", 1)

    name = "surivial_histo_{pb_}".format(pb_ = pb)
    survival_histo = ROOT.TH1F(name, "histo",15,0,800)
    name = "initke_histo_{pb_}".format(pb_ = pb)
    initke_histo = ROOT.TH1F(name, "histo",15,0,800)

    event_generator = events_generator2(t)
    
    for survival_status, kinetic_energy in event_generator:
        initke_histo.Fill(kinetic_energy)
        if survival_status == 1:
            survival_histo.Fill(kinetic_energy)
    t.Delete() 
    file.Close()
    name = "ratio_histo_{pb_}".format(pb_ = pb)
    ratio_histo = survival_histo.Clone(name)
    ratio_histo.Divide(initke_histo)
    return ratio_histo,initke_histo

def events_generator(t):
    counter = 0
    for event in t:
    
        counter += 1
        if counter == 100000:
            break
        elif counter % 1000 == 0:
            print(counter)
            
        nvect = event.vectorbranch
        nvt = nucleon_nvect_reader(nvect)

        x = nvt.nucleon_survival()    
        yield x[0],x[2] # Yield the result (survival status, kinetic energy)

def events_generator2(t):
    nv = ROOT.NeutVect()
    address = ROOT.addressof(nv,byref = True)
    t.SetBranchAddress("vectorbranch",cast['void*'](address))
    for i in range(t.GetEntries()):
        entry = t.GetEntry(i)
        if i== 200000:
            break
        elif i % 10000 == 0:
            print(i)
        nvt = nucleon_nvect_reader(nv)
        x = nvt.nucleon_survival()    
        yield x[0],x[2] # Yield the result (survival status, kinetic energy)

start_time = time.time()
__main__()
print("--- %s seconds ---" % (time.time() - start_time))



