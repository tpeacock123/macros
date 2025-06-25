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


def ratio_histo(file,pb):

    t = file.Get("neuttree")
    t.SetCacheSize(0)
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
        entry = t.GetEntry()
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