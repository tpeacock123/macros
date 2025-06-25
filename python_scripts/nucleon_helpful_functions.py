import ROOT
import sys 
import numpy as np
ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

from helpful_functions import *

class nucleon_nvect_reader(nvect_reader):

    def __init__(self, nvect_,flavor): 
	    super().__init__(nvect_,flavour=flavor)  
       
    def nucleon_survival(self):   
        fin_mom =0
        init_mom =0
        alive = 0
        
        for i in range(self.nopart):   
            pinfo = self.nvect.PartInfo(i)
            if i == 0 and self.nvect.ParentIdx(i) ==0 and (pinfo.fPID == abs(self.beam_flavour)):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_mom =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass

            if self.nvect.ParentIdx(i) ==2 and (pinfo.fPID == abs(self.beam_flavour) and i == 3):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                fin_mom =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                alive = pinfo.fIsAlive
    
        return alive, fin_mom,init_mom
    
    def init_nucleon_energy(self):
        for i in range(self.nopart):   
            pinfo = self.nvect.PartInfo(i)
            if i == 0 and self.nvect.ParentIdx(i) ==0 and (pinfo.fPID == abs(self.beam_flavour)):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_ke =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
    
        return init_ke
    
    def daughter_nuclei_energies(self):
        init_ke =[]
        flavour = []
        for i in range(self.nopart): 
            pinfo = self.nvect.PartInfo(i)
            #if i > 3 and self.nvect.ParentIdx(i) ==4 and pinfo.fIsAlive == 1:
            if (i >= 2 and (pinfo.fPID == 2212 or pinfo.fPID == 2112) and pinfo.fIsAlive == 1):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_ke.append(np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass)
                flavour.append(pinfo.fPID)
        return init_ke, flavour
    
    def survival_energy(self):
        flag = False
        for i in range(self.nopart):   
            pinfo = self.nvect.PartInfo(i)
            if i == 0 and self.nvect.ParentIdx(i) ==0 and (pinfo.fPID == abs(self.beam_flavour)):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_ke =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                init_x = pinfo.fP.X()
                init_y = pinfo.fP.Y()
                init_z = pinfo.fP.Z()
                init_mom = np.asarray([init_x,init_y,init_z])

            if (pinfo.fPID == abs(self.beam_flavour) and pinfo.fIsAlive == 1):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                surv_ke =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                surv_x = pinfo.fP.X()
                surv_y = pinfo.fP.Y()
                surv_z = pinfo.fP.Z()
                surv_mom = np.asarray([surv_x,surv_y,surv_z])
                #print(surv_mom,init_mom)
                cos_theta =  np.dot(surv_mom,init_mom)/(np.linalg.norm(surv_mom)*np.linalg.norm(init_mom))
                theta = np.arccos(cos_theta)
                if (surv_ke - init_ke < 10 and abs(theta) < 0.05):
                    flag == True
                    #print(surv_mom,init_mom)
                    return init_ke, surv_ke
        return init_ke, -999.99
                
    def multiplicity(self):
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

