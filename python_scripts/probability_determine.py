import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("pb1.0_1mil_forsurvival.root")
t = f.Get("neuttree")
surival_prob_histogram = ROOT.TH1F("h", "Prob Dist", 100, 0, 10000)

counter = 0
for event in t:
    counter +=1
    if counter == 400000:
        break
    nvect = event.vectorbranch
    nopart = nvect.Npart()
    nosteps = nvect.NnucFsiStep()
    #print(nopart)

    init_energy = 0
    final_energy = 0
    interaction = True

    print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")

    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
    
        if(nvect.ParentIdx(i)== 0 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and nvect.Mode != abs(2)):
            #print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
            init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
        
        if (i >= 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1):
            nucleon_no +=1
        
        if (i >= 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1):
            if( init_energy > bestmom):
                bestmom = init_energy
                init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass



        if nucleon_no == 1:
            print("pbprob",nvect.NrintNucleonPBprob)
            print("cascade prob", nvect.NrintNucleonCascadeProb)