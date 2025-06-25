import ROOT
import sys 
import numpy as np
ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

class nvect_reader:
    def __init__(self, nvect_,flavour = 2212):
        self.nvect = nvect_
        self.nopart = self.nvect.Npart()
        self.novert = self.nvect.NnucFsiVert()
        self.nosteps = self.nvect.NnucFsiStep()
        self.beam_flavour = flavour

    def muon_energy(self):
        muon_energy = 0
        for i in range(self.nopart):
            pinfo = self.nvect.PartInfo(i)
            if ( i==2 and pinfo.fPID == 13):
                muon_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
            elif(i ==2 and pinfo.fPID != 13):
                muon_energy = -999.9

        return muon_energy
    
    def casc_proton_energy(self):
        p_casc_energy = 0
        alive = 2
        pid = 0
        for i in range(self.nopart):
            pinfo = self.nvect.PartInfo(i)

            if (i == 3 and ((pinfo.fPID == abs(2112)) or pinfo.fPID == abs(2212))):
                if (pinfo.fIsAlive == 0):
                    p_casc_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                    pid =pinfo.fPID
                    alive=pinfo.fIsAlive
                elif (pinfo.fIsAlive == 1):
                    p_casc_energy =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                    pid =pinfo.fPID
                    alive=pinfo.fIsAlive

        return p_casc_energy,alive, pid


    def interaction_counter(self):
        noflags = 0 
        interaction = 0
        for i in range(self.nosteps):
            nucfsisinfo = self.nvect.NucFsiStepInfo(i)
            noflags += nucfsisinfo.fPBFlag 
            interaction_flag = nucfsisinfo.fVertFlagStep

            if(-4 < interaction_flag < 4 ):
                interaction += 1 

        return noflags, interaction, 0
    
    def is_pauliblocked(self):
        PB = 0
        for i in range(self.novert):
            nucfsivinfo = self.nvect.NucFsiVertInfo(i)
            flag = nucfsivinfo.fVertFlag
            if flag  < 0:
                flaglist = [-1]
            else:
                flaglist = [int(i) for i in str(flag)]
            if len(flaglist) == 4:
                PB = 1
        return PB

    def neutrino_multiplicity(self):
        nucleon_no = 0
        for i in range(self.nopart):
            pinfo = self.nvect.PartInfo(i)
            if (i >= 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1):
                nucleon_no +=1

        if nucleon_no == 0:
            for j in range(self.nopart):
                pinfo = self.nvect.PartInfo(j)
                #print(j, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(j),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
        
        return nucleon_no

    def neutrino_daughter_nuclei_energies(self):
        init_ke =[]
        flavour = []
        for i in range(self.nopart): 
            pinfo = self.nvect.PartInfo(i)
            if i >= 1 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1:
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_ke.append(np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass)
                flavour.append(pinfo.fPID)
        return init_ke, flavour

    def Print(self):
        print("~~~~~~~~~Particles~~~~~~~") 
        print("ID Vertex ID Parent Particle  particle  mom")
        for i in range(self.nopart):
            pinfo = self.nvect.PartInfo(i)
            print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
            pinfo.fP.X()**2 + pinfo.fP.X()**2 +pinfo.fP.Y()**2
            
            P = (pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)
            print("energy", np.sqrt(P+pinfo.fMass**2)-pinfo.fMass)
    
    def kinetic_energy(self,pinfo):
        return np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
    
