import ROOT
import sys 
import numpy as np

ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
f = ROOT.TFile("pb0.0_1milevts.root")
t = f.Get("neuttree")
h = ROOT.TH1F("h", "Prob Dist", 50, -1.1, 1.1)

for event in t:
    nvect = event.vectorbranch
    goodevent = False

    print("~~~~~~~~~~~~~~~~~~~~~~~~")   
    print("~~~~~~~EVENT", nvect.EventNo, "~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~")

    print("pb rand", nvect.NrintNucleonPBRand)
    print("pbprob",nvect.NrintNucleonPBprob)
    print("cascade prob", nvect.NrintNucleonCascadeProb)
    nosteps = nvect.NnucFsiStep()
    print("steps",nosteps)
    nopart = nvect.Npart()
    novert = nvect.NnucFsiVert()
    nopipart = nvect.NfsiPart()
    print(nopart)

    print("~~~~~~~~~Particles~~~~~~~") 
    print("ID Vertex ID Parent Particle  particle  mom")
    for i in range(nopart):
        pinfo = nvect.PartInfo(i)
        print(i, " ", pinfo.fIsAlive,"       ",nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
        pinfo.fP.X()**2 + pinfo.fP.X()**2 +pinfo.fP.Y()**2
        
        P = (pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)
        print("energy", np.sqrt(P+pinfo.fMass**2)-pinfo.fMass)


    print("~~~~~~~~~NUC FSI VERTICES~~~~~~~") 
    print("number of vertices", novert)
    interaction = 0
    for i in range(novert):
        print("~~~~~~~~~~~~~~~~~~~~~~~~")  
        nucfsivinfo = nvect.NucFsiVertInfo(i)
        flag = nucfsivinfo.fVertFlag
        if flag  < 0:
            flaglist = [-1]
        else:
            flaglist = [int(i) for i in str(flag)]
        if len(flaglist) == 4:
            print("PB!")
        else:
            while len(flaglist) != 4:
                flaglist.insert(0, 0)

        print(flaglist[3])
        if (0< flaglist[3] < 4):
            interaction +=1
        indices = ["x","y","z","energy"]
        for i in range(len(indices)):
            print(indices[i], nucfsivinfo.fMom[i])
  
    print("steps")
    noflags = 0
    interaction = 0
    for i in range(nosteps):
        nucfsisinfo = nvect.NucFsiStepInfo(i)
        noflags += nucfsisinfo.fPBFlag 
        interaction_flag = nucfsisinfo.fVertFlagStep
        print(noflags,nucfsisinfo.fPBFlag, interaction_flag)
        if interaction_flag < 4:
            interaction += 1 
    print("pb prob cross check = ", noflags, interaction)
    if noflags > interaction:
        sys.exit(1)

    h.Fill(nvect.NrintNucleonPBprob)

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
h.Draw("hist")
canvas.SaveAs("pbprob_dist_PB0.0_craxy.png")

