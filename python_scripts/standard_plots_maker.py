import ROOT
import sys 
import numpy as np
from nucleon_helpful_functions import *

def prob_pbon(name):
    f = ROOT.TFile(name)
    t = f.Get("neuttree")
    counter = 0
    list =[]

    for event in t:
        counter +=1
        if counter == 30000:
            break
        nvect = event.vectorbranch
        nvt =  nucleon_nvect_reader(nvect)

        #print(nvect.NrintNucleonCascadeProb)
        list.append(nvect.NrintNucleonCascadeProb)
    return list

#ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")


survival_histo = ROOT.TH1F("proton_survival_histo", "histo",200,0,600)
init_histo = survival_histo.Clone("init_histo")
muon_histo = ROOT.TH1F("muon_histo", "histo",200,0,1500)
proton_he_histo = ROOT.TH1F("proton_he_histo", "histo",200,0,600)
neutron_he_histo = ROOT.TH1F("neutron_he_histo", "histo",200,0,600)


char = "aaa"
i = 1
while (char != "_pb"):
    i += 1
    char = sys.argv[1][i-2] + sys.argv[1][i-1] + sys.argv[1][i]
    pb_stat = sys.argv[1][i+1]+sys.argv[1][i+2]
print(pb_stat)


f = ROOT.TFile(sys.argv[1])
t = f.Get("neuttree")
counter = 0

if (len(sys.argv) > 2 and sys.argv[2] == "rw"):
    listprob = prob_pbon(sys.argv[3])


for event in t:
    counter +=1
    if counter == 30000:
        break
    nvect = event.vectorbranch
    nvt =  nucleon_nvect_reader(nvect)

    if (len(sys.argv) > 2 and sys.argv[2] == "rw"):
        weight = nvect.NrintNucleonCascadeProb/listprob[counter-1]
        print(weight)
    else:
        weight = 1
    #nvt.particle_printer()

    muon_e = nvt.muon_energy()
    if (muon_e !=0):
        muon_histo.Fill(weight*muon_e)
        #print("muon energy", muon_e)

    casc_data = nvt.casc_proton_energy()
    if(casc_data[2] == 2212):
        init_histo.Fill(weight*casc_data[0])
    if(casc_data[1]==1 and casc_data[2] == 2212):
        #print("surv energy", casc_data[0])
        survival_histo.Fill(casc_data[0])
    survival_prob = survival_histo.Clone()
    survival_prob.Divide(init_histo)

    proton_highest_energy = nvt.nucleon_high_energy(2212)
    if (proton_highest_energy != 0):
        proton_he_histo.Fill(proton_highest_energy)
        #print(proton_highest_energy)

    neutron_highest_energy = nvt.nucleon_high_energy(2112)
    if (neutron_highest_energy != 0):
        neutron_he_histo.Fill(neutron_highest_energy)
        #print(neutron_highest_energy)

if(len(sys.argv) > 2 and sys.argv[2] == "rw"):
    file = ROOT.TFile("standard_plots_1mil_pb{}_rw.root".format(pb_stat), "RECREATE")
else:
    print("here!")
    file = ROOT.TFile("standard_plots_1mil_pb{}_test4_t2kflux.root".format(pb_stat), "RECREATE")   
survival_histo.Write()
muon_histo.Write()
proton_he_histo.Write()
neutron_he_histo.Write()
survival_prob.Write("survival probability")
file.Close()
    

