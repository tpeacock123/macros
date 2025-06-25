import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("pb1.0_1milevts.root")
t = f.Get("neuttree")
multiplicity = ROOT.TH1F("h", "Prob Dist", 100, 0, 5000)
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
    bestmom = 0
    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
        if (i >= 2 and (pinfo.fPID == 2212) and pinfo.fIsAlive == 1):
            init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            if( init_energy > bestmom):
                bestmom = init_energy
                init_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass


    
    multiplicity.Fill(bestmom)
            

multiplicity.Draw("hist")
multiplicity.SaveAs("leadingnucleondist_pb0.root")