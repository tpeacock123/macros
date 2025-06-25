#incoming proton momentum against lowest outgoing proton 

#get incoming proton Ke

#search stack for two particles which have come from this initial proton
#get the lowest proton energy

from nucleon_helpful_functions import *
import numpy as np

ROOT.TH1.AddDirectory(False)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

inkevsoutke_hist = ROOT.TH2D("incomingKE_vs_outgoingKE","incomingKE_vs_outgoingKE",40,0.0,1000.0,40,0.0,1000.0)


f = ROOT.TFile("neut_build_dir/NHSG_10milevts_forhisto.root")
t = f.Get("neuttree")
counter = 0

for event in t:
    counter +=1
    if counter % 100000 == 0:
        print(counter)
    if counter == 5000000:
        break
    nvect = event.vectorbranch
    nvt =  nucleon_nvect_reader(nvect)
    daughter_ke = nvt.daughter_nuclei_energies()
    incoming_ke = nvt.init_nucleon_energy()
    if len(daughter_ke) == 2:
        output_ke = np.asarray(daughter_ke).min()

        inkevsoutke_hist.Fill(incoming_ke,output_ke)

inkevsoutke_hist.GetXaxis().SetTitle("Incoming proton KE [MeV]")
inkevsoutke_hist.GetYaxis().SetTitle("KE of outgoing proton with lowest KE [MeV]")

file = ROOT.TFile("incoming_proton_vs_outgoing_proton_ke_final.root", "RECREATE")   
inkevsoutke_hist.Write()
file.Close()