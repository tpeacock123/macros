import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("../pbdialtest_1milevts_pbon.root")
t = f.Get("neuttree")
tot_energy = ROOT.TH1F("h", "Prob Dist", 100, 0, 10000)
no_int_energy = ROOT.TH1F("h", "Prob Dist", 100, 0, 10000)
pb_flag = ROOT.TH1F("h", "surivial probs", 50, -0.1, 1)
counter = 0

for event in t:

    interaction = True
    counter +=1
    if counter == 300000:
        break
    nvect = event.vectorbranch
    nopart = nvect.Npart()
    nosteps = nvect.NnucFsiStep()
    #print(nopart)

    init_energy = 0
    final_energy = 0
    print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")

    print("pbprob",nvect.NrintNucleonPBprob)
    print("cascade prob", nvect.NrintNucleonCascadeProb)


    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
    
        if(nvect.ParentIdx(i)== 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and nvect.Mode != abs(2) and pinfo.fIsAlive==1):
            #print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
            parent = i
            init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            tot_energy.Fill(init_energy)
            pb_flag.Fill(1 - nvect.NrintNucleonCascadeProb)
            interaction = False
        
    if interaction == False:
        for k in range(nopart):
            pinfo = nvect.PartInfo(k)
            print(k, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(k),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)

    #print(init_energy, final_energy)


pb_flag.Draw("hist")
pb_flag.SaveAs("PBprobpb1.root")

