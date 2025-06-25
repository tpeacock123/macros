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
    for i in [0.0,1.0]:
        file = "input_nuclroot_files/nucleon_pb{pbval}_1milevts.root".format(pbval = i)
        file = ROOT.TFile(file)
        looper(file)
@profile
def looper(file):
    t = file.Get("neuttree")
    nv = ROOT.NeutVect()
    address = ROOT.addressof(nv,byref = True)
    t.SetBranchAddress("vectorbranch",cast['void*'](address))
    for i in range(t.GetEntries()):
        t.GetEntry(i)
        if i== 10000:
            break
        elif i % 1000 == 0:
            print(i)
            print(nv.Npart())


        
__main__()