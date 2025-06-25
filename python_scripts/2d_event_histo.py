import ROOT
import sys 
import numpy as np
from helpful_functions import *

ROOT.gStyle.SetOptStat(0)

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

interaction_energy_p_casc = ROOT.TH2F("interaction_energy_p_casc", "Interaction Type Against nucleon Energy",75,0,5000, 5,1, 5)
below_PF_histo = ROOT.TH1F("below_PF_histo", "below PF_histo",75,0,5000)
below_PF_histo_surv = below_PF_histo.Clone("below_PF_histo_surv")
below_PF_histo_cascs = below_PF_histo.Clone("below_PF_histo_cascs")
below_PF_histo_cascs_2 = below_PF_histo.Clone("below_PF_histo_cascs_0.66")
below_PF_histo_cascs_3 = below_PF_histo.Clone("below_PF_histo_cascs_0.33")
below_PF_histo.GetXaxis().SetTitle("Pre FSI/Post PI Neutron Energy (MeV)")
below_PF_histo_surv.SetLineColor(2)
below_PF_histo_cascs.SetLineColor(3)
below_PF_histo_cascs_2.SetLineColor(4)
below_PF_histo_cascs_3.SetLineColor(5)

PB_histo = ROOT.TH1F("PB_histo", "below PF_histo",75,0,5000)
PB_histo_surv = PB_histo.Clone("PB_histo_surv")
PB_histo_cascs = PB_histo.Clone("PB_histo_cascs")
PB_histo_cascs_2 = PB_histo.Clone("PB_histo_cascs_0.66")
PB_histo_cascs_3 = PB_histo.Clone("PB_histo_cascs_0.33")
PB_histo.GetXaxis().SetTitle("Pre FSI/Post PI Neutron Energy (MeV)")
PB_histo_surv.SetLineColor(2)
PB_histo_cascs.SetLineColor(3)
PB_histo_cascs_2.SetLineColor(4)
PB_histo_cascs_3.SetLineColor(5)

survival_histo = ROOT.TH1F("Survival_histo", "surivival histo",300,0,5000)
survival_histo.GetXaxis().SetTitle("Pre FSI/Post PI Neutron Energy (MeV)")

yAxis = interaction_energy_p_casc.GetYaxis()
yAxis.SetBinLabel(1, "Survival")
yAxis.SetBinLabel(2, "Pbed")
yAxis.SetBinLabel(3, "Below PFermi")
yAxis.SetBinLabel(4, "Above PFermi")
interaction_energy_p_surv = interaction_energy_p_casc.Clone("interaction_energy_p_surv")
interaction_energy_n_casc = interaction_energy_p_casc.Clone("interaction_energy_n_casc")
interaction_energy_n_surv = interaction_energy_p_casc.Clone("interaction_energy_n_surv")
interaction_energy_n_casc_2 = interaction_energy_p_casc.Clone("interaction_energy_n_casc_0.5")
interaction_energy_n_casc_3 = interaction_energy_p_casc.Clone("interaction_energy_n_casc_0.0")

f = ROOT.TFile("pb1.0_1milevts.root")
t = f.Get("neuttree")

counter = 0
pb_frac = 0
pb_frac2 = 0
for event in t:
    counter +=1
    if counter == 300000:
        break
    nvect = event.vectorbranch
    nvt = nvect_reader(nvect)

    init_energy = 0
    final_energy = 0
    print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")

   # print("pbprob",nvect.NrintNucleonPBprob)
    #print("cascade prob", nvect.NrintNucleonCascadeProb)
    prob_1 =  nvect.NrintNucleonCascadeProb*nvect.NrintNucleonPBprob
    #print(prob_1)
    noflags = 0
    interaction = 0
    interaction_fraction = 1

    flags = nvt.interaction_counter()
    pb = nvt.is_pauliblocked()
    if(flags[0] == 0 and flags[1] == 0): #survival, no cascade interactions occuring
        interaction = 1 
    elif(flags[0] == flags[1] and pb == 1): #All interactions Pauli blocked, so survival
        interaction = 1 #pauli blocked
        pb_frac += 1
    elif(flags[0] != 0 and flags[1] != 0 and pb == 1): #Pauli blocking has occured at least once, but cascade has happened
        interaction = 2 #pauli blocked
        pb_frac2 += 1
        interaction_fraction = flags[0]/flags[1]
    elif(flags[0] != 0 and flags[1] != 0): # at least one interaction below the fermi momentum
        interaction = 3 #Below p_fermi
        interaction_fraction = flags[0]/flags[1]

    elif(flags[0] == 0 and flags[1] != 0): # no 
        interaction = 4 #above p_fermi
    else:
        interaction = 1 #-999 code, interaction never reaches nucleon cascade, so survival
        
    p_casc_energy = nvt.casc_proton_energy()

    if(p_casc_energy[2] == 2212):
        interaction_energy_p_casc.Fill(p_casc_energy[0],interaction)
#    if(p_casc_energy[1] == 1 and p_casc_energy[2] == 2212):
#        interaction_energy_p_surv.Fill(p_casc_energy[0],interaction)
    if(p_casc_energy[2] == 2112):
        interaction_energy_n_casc.Fill(p_casc_energy[0],interaction)
#    if(p_casc_energy[1] == 1 and p_casc_energy[2] == 2112):
        interaction_energy_n_surv.Fill(p_casc_energy[0],interaction)
    
    if (interaction == 1) and (p_casc_energy[2] == 2212):
        survival_histo.Fill(p_casc_energy[0])

    if (interaction == 2) and (p_casc_energy[2] == 2212):
        PB_histo.Fill(p_casc_energy[0])
        print(interaction_fraction)
        if interaction_fraction == 1.0:
            PB_histo_surv.Fill(p_casc_energy[0])
        if 2/3 <= interaction_fraction <1.0:
            PB_histo_cascs.Fill(p_casc_energy[0])
        if 1/3 <= interaction_fraction < 1.0:
            PB_histo_cascs_2.Fill(p_casc_energy[0])
        if 0 <= interaction_fraction < 1/3:
            PB_histo_cascs_3.Fill(p_casc_energy[0])

    if (interaction == 3) and (p_casc_energy[2] == 2212):
        below_PF_histo.Fill(p_casc_energy[0])
        print(interaction_fraction)
        if interaction_fraction == 1.0:
            below_PF_histo_surv.Fill(p_casc_energy[0])
        if 2/3 <= interaction_fraction <1.0:
            below_PF_histo_cascs.Fill(p_casc_energy[0])
        if 1/3 <= interaction_fraction < 1.0:
            below_PF_histo_cascs_2.Fill(p_casc_energy[0])
        if 0 <= interaction_fraction < 1/3:
            below_PF_histo_cascs_3.Fill(p_casc_energy[0])
    



print("survived","cascaded")
print(pb_frac,pb_frac2)
file = ROOT.TFile("pb1.0_IntEvChannel_plusbreakdown_sameseed.root", "RECREATE") # or "UPDATE" if you already have the file

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
interaction_energy_p_casc.GetZaxis().SetRange(0,12000)
interaction_energy_p_casc.GetXaxis().SetTitle("Pre FSI/Post PI Proton Energy (MeV)")
interaction_energy_p_casc.Draw("colz")
canvas.Write("interaction_energy_p_casc")
#interaction_energy_p_surv.Write()
canvas2 = ROOT.TCanvas("canvas2", "hist from Text File", 800, 600)
interaction_energy_n_casc.GetZaxis().SetRange(0,12000)
interaction_energy_n_casc.GetXaxis().SetTitle("Pre FSI/Post PI Neutron Energy (MeV)")
interaction_energy_n_casc.Draw("colz")
canvas2.Write("interaction_energy_n_casc")

canvas3 = ROOT.TCanvas("canvas3", "blargh", 800, 600)

legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(below_PF_histo_surv,"All fsi steps can be PBed, potential survival","l"); 
legend.AddEntry(below_PF_histo_cascs,"fraction of pbed events 0.66 - 1","l"); 
legend.AddEntry(below_PF_histo_cascs_2,"fraction of pbed events 0.33 - 0.66","l"); 
legend.AddEntry(below_PF_histo_cascs_3,"fraction of pbed events 0.00 - 0.33","l"); 

below_PF_histo.Draw("l")
below_PF_histo_surv.Draw("lsame")
below_PF_histo_cascs.Draw("lsame")
below_PF_histo_cascs_2.Draw("lsame")
below_PF_histo_cascs_3.Draw("lsame")
legend.Draw()
canvas3.Write("Below_PF_histo")

canvas4 = ROOT.TCanvas("canvas4", "blargh", 800, 600)

legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(PB_histo_surv,"All fsi steps PBed, potential survival","l"); 
legend.AddEntry(PB_histo_cascs,"fraction of pbed events 0.66 - 1","l"); 
legend.AddEntry(PB_histo_cascs_2,"fraction of pbed events 0.33 - 0.66","l"); 
legend.AddEntry(PB_histo_cascs_3,"fraction of pbed events 0.00 - 0.33","l"); 

PB_histo.Draw("l")
PB_histo_surv.Draw("lsame")
PB_histo_cascs.Draw("lsame")
PB_histo_cascs_2.Draw("lsame")
PB_histo_cascs_3.Draw("lsame")
legend.Draw()
canvas4.Write("PB_histo")
#interaction_energy_n_surv.Write()

canvas5 = ROOT.TCanvas("canvas5", "blargh2", 800, 600)
survival_histo.Draw()
canvas5.Write("Survival_histo")

file.Close()
    


    


