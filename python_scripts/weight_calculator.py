import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("../input_root_files/pb1.0_1milevts.root")
t = f.Get("neuttree")

weightfile = ROOT.TFile("/mnt/macros/nucleon_survival_excess/build/survhisto_700k.root")
weight_histo = weightfile.Get("pbvsKE")

from helpful_functions import *


weighth = ROOT.TH1F("weight", "Prob Dist", 40, 0.5, 1.5)
Muon_energy = ROOT.TH1F("muon", "Prob Dist", 15, 0, 800)
initenergy = ROOT.TH1F("muon", "Prob Dist", 15, 0, 800)
Proton_energy = ROOT.TH1F("proton", "Prob Dist", 15, 0, 800)
Muon_energy_w = ROOT.TH1F("muon_weight", "Prob Dist", 15, 0, 800)
Proton_energy_w = ROOT.TH1F("proton_weight", "Prob Dist", 15, 0, 800)

counter = 0
prob_1 = 1
for event in t:
    interaction = True
    interaction_weird = False
    counter +=1
    if counter == 100000:
        break
    nvect = event.vectorbranch
    nopart = nvect.Npart()
    nosteps = nvect.NnucFsiStep()
    #print(nopart)

    init_energy = 0
    final_energy = 0
    #print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")

    #print("pbprob",nvect.NrintNucleonPBprob)
    #print("cascade prob", nvect.NrintNucleonCascadeProb)
    prob_1 =  nvect.NrintNucleonCascadeProb*nvect.NrintNucleonPBprob
    #print(prob_1)
   
    noflags = 0
    interaction = 0
    for i in range(nosteps):
        nucfsisinfo = nvect.NucFsiStepInfo(i)
        noflags += nucfsisinfo.fPBFlag 
        interaction_flag = nucfsisinfo.fVertFlagStep

        if(-4 < interaction_flag < 4 ):
            print("yep")
            interaction += 1 
        if(interaction_flag == -999):
            interaction_weird = True
    #print("pb prob cross check = ", noflags, interaction)
    #print(noflags,interaction)
    
    
    bestmom = 0
    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
#        if interaction_weird == True:
#            print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)        
        if(nvect.ParentIdx(i)== 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and nvect.Mode != abs(2)):
            #print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
            init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
        
        if (i >= 1 and (pinfo.fPID == abs(13)) and pinfo.fIsAlive == 1):
            mu_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass

        if (i >= 2 and (pinfo.fPID == 2212) and pinfo.fIsAlive == 1):
            x_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            if( init_energy > bestmom):
                bestmom = x_energy

        if (i == 3 and ((pinfo.fPID == abs(2112)) or pinfo.fPID == abs(2212))):
            p_casc_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            #print(p_casc_energy)
        

    if(init_energy <= 800):
        initenergy.Fill(init_energy)
        for i in range(1, 21):
            if p_casc_energy > (20-i)*(800/20):
                p_casc_energy2 = (20-(i))*(800/20)
                bin = (20 - (i))+1
                break


        #print(weight_histo.GetXaxis().GetBinCenter(bin))

        if(interaction == 0 and noflags == 0):
            proton = init_energy
            print(init_energy)
            Proton_energy.Fill(proton)
            weight = weight_histo.GetBinContent(bin,5)
            proton_w = init_energy*weight
            Proton_energy_w.Fill(proton_w)
        elif(interaction != 0 and noflags != 0):
            weight = 1/weight_histo.GetBinContent(bin,5)
        else:
            weight = 1
        
        
        w_bestmom = bestmom*weight
        w_mu_energy = mu_energy*weight

        weighth.Fill(weight)
        Muon_energy.Fill(mu_energy)
        Muon_energy_w.Fill(w_mu_energy)
        #print(weight)

ratio = Proton_energy.Clone("ratio")

Proton_energy.Divide(initenergy)

ratio_w = initenergy.Clone("ratio_2")

Proton_energy_w.Divide(initenergy)
        
file = ROOT.TFile("weight_histograms_pb1_again2.root", "RECREATE") # or "UPDATE" if you already have the file

# Write each histogram to the file

Muon_energy.Write()
Proton_energy.Write()
Muon_energy_w.Write()
Proton_energy_w.Write()
ratio.Write()
ratio_w.Write()

# Close the file
file.Close()
