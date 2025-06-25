

class nvect_reader {
public:

    nvect_reader(NeutVect* nvect){
        nopart = nvect->Npart();
        novert = nvect->NnucFsiVert();
        nosteps = nvect->NnucFsiStep();
    }

    def nucleon_survival(){
        fin_mom =0
        init_mom =0
        alive = 0
        
        for i in range(self.nopart):   
            pinfo = self.nvect.PartInfo(i)
            if i == 0 and self.nvect.ParentIdx(i) ==0 and (pinfo.fPID == abs(2212)):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                init_mom =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass

            if self.nvect.ParentIdx(i) ==2 and (pinfo.fPID == abs(2212) and i == 3):
                #print(i, " ", pinfo.fIsAlive,"       ",self.nvect.ParentIdx(i),"              ", pinfo.fPID, "    ",pinfo.fP.X(), pinfo.fP.Y(), pinfo.fP.Z(), pinfo.fMass)
                fin_mom =np.sqrt((pinfo.fP.X()**2 + pinfo.fP.Y()**2 +pinfo.fP.Z()**2)+pinfo.fMass**2)-pinfo.fMass
                alive = pinfo.fIsAlive
    
        return alive, fin_mom,init_mom
    }
    
private:
    NeutVect* nvect;
    int nopart;
    int novert;
    int nosteps;
};