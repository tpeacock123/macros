from nucleon_helpful_functions import *
import numpy as np

ROOT.TH1.AddDirectory(False)

f = ROOT.TFile("incoming_proton_vs_outgoing_proton_ke.root")

t = f.Get("incomingpKEoutgoingKE")