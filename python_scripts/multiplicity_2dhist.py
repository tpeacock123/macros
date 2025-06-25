import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("pb0.0_1mil_forsurvival.root")
t = f.Get("neuttree")
multiplicity = ROOT.TH2F("h", "Prob Dist", 12,0, 12, 75,0,5000)
counter = 0
for event in t:
    counter +=1
    if counter == 200000:
        break
    nvect = event.vectorbranch
    nopart = nvect.Npart()
    nosteps = nvect.NnucFsiStep()
    #print(nopart)

    init_energy = 0
    nucleon_no = 0
    flag = False

    print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")

    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
    
        if(nvect.ParentIdx(i)== 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112)):
            #print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
            init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)

            print(init_energy)
        
        if (i >= 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1):
            nucleon_no +=1

    if nucleon_no == 0:
        for j in range(nopart):
            pinfo = nvect.PartInfo(j)
            print(j, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(j),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)

    multiplicity.Fill(nucleon_no, init_energy)
            




multiplicity.Draw("LEGO1")
multiplicity.SaveAs("pb0_multiplicity_energy_2d.root")