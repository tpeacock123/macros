import ROOT
import sys 
import numpy as np
import array
import uproot
from memory_profiler import profile
from nucleon_helpful_functions import *


ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")


def ratio_histo(file,pb):

    

ratio_histo("a",1.0)


