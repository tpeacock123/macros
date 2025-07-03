#include <iostream>
#include <vector>
#include <map>
#include <string>

#include <TFile.h>
#include <TH1D.h>
#include <TTree.h>
#include <TH2D.h>
#include <TFile.h>
#include <TStyle.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <chrono>

#include "CommonBlockIFace.h"
#include "2d_histogram_gen.h"


int main(){
    TH1::AddDirectory(false);

    TFile *inputFile = TFile::Open("../../neut_build_dir/NHSG_3milevts_kerethrow.root");
    // bin split into 50 bins under 50, 50 bins from 50 to 200, and then 50 bins from 200 to 2000
    // 0 - 49: 50 bins, 50 - 199 : 50 bins, 
    int binno = 201;
    // bin split into 50 bins under 50, 50 bins from 50 to 200, and then 50 bins from 200 to 2000
    // 0 - 49: 50 bins, 50 - 199 : 50 bins, 
    double x_bin_array[binno];
    for(int i{0}; i < binno; ++i){
        if(i < 50){
            x_bin_array[i] = 1.0*i;
        }
        else if(50 <= i && i < 100){
            x_bin_array[i] = 3.*i - 100.;
        }
        else{
            x_bin_array[i] = 18.*i - 1600.;
        }
    }
    int y_binno = 76;
    double y_bin_array[y_binno];
    for(int i{0}; i < y_binno; ++i){
        y_bin_array[i] = 10*i;
    }


    TH2D inE_vs_outE_histo_pp("incomingKE_vs_outgoingKE_pp","incomingKE_vs_outgoingKE_pp",binno-1,x_bin_array, y_binno-1,y_bin_array);
    TH2D inE_vs_outE_histo_pn("incomingKE_vs_outgoingKE_pn","incomingKE_vs_outgoingKE_pn",binno-1,x_bin_array, y_binno-1,y_bin_array);
    TTree* t = (TTree*) inputFile->Get("neuttree");
    t->SetBranchStatus("*", 0);
    t->SetBranchStatus("vectorbranch", 1);
    NeutVect *nvect = NULL;
    TBranch *branch = t->GetBranch("vectorbranch");
    branch->SetAddress(&nvect);
    branch->SetAutoDelete(true);

    int start{0};
    for(int i = start; i < 3000000; i++){
        if(i % 100000 == 0){
            std::cout << i << std::endl;
        }

        double initKE(0.0);
        double daughterKE{0.0};

        t->GetEntry(i);
        init_energies(nvect, initKE);
        //std::cout << initKE << std::endl;
        bool ppflag = false;

        daughter_nuclei_energies(nvect,daughterKE, ppflag);
 
        if(daughterKE != 0)  inE_vs_outE_histo_pp.Fill(initKE,daughterKE);
       // if(daughterKE != 0 && ppflag == true) inE_vs_outE_histo_pp.Fill(initKE,daughterKE);
        //else if(daughterKE != 0 && ppflag == false) inE_vs_outE_histo_pn.Fill(initKE,daughterKE);
        
    }
    inputFile->Close();
    delete inputFile;

    TFile* outputFile = TFile::Open("incomingKE_vs_outgoingKE_rebin_Kecut2.root", "recreate");
    inE_vs_outE_histo_pp.Write();
    inE_vs_outE_histo_pn.Write();
    outputFile->Close();
    delete outputFile;
}

void init_energies(NeutVect *nvect,double &initKe){
    int nPart = nvect->Npart();
    for (int particle=0;particle<nPart; particle++){
        auto pInfo = nvect->PartInfo(particle);
        if(particle == 0 && nvect->ParentIdx(particle) ==0 && (pInfo->fPID == abs(2212)))
        {
            //std::cout << particle << " " << pInfo->fIsAlive << " " << pInfo->fPID<< "  ("  << pInfo->fP.X() << "," << pInfo->fP.Y() << "," << pInfo->fP.Z() << ") " << << std::endl;
            double x{pInfo->fP.X()};
            double y{pInfo->fP.Y()};
            double z{pInfo->fP.Z()};
            double mass{pInfo->fMass};

            initKe = (std::sqrt(x*x+ y*y + z*z + mass*mass) - mass);
        }
    }
}

void daughter_nuclei_energies(NeutVect *nvect,double &daughterKE, bool &ppflag){
    int nPart = nvect->Npart();
    std::vector<double> daughter_energies;
    std::vector<int> flavour;

    for (int particle=0;particle<nPart; particle++){
        double ke{0.0};
        auto pInfo = nvect->PartInfo(particle);
        if(particle > 3 && nvect->ParentIdx(particle) ==4 && (pInfo->fPID == abs(2212) || pInfo->fPID == abs(2112)) && pInfo->fIsAlive == 1 )
        {
            //std::cout << particle << " " << pInfo->fIsAlive << " " << pInfo->fPID<< "  ("  << pInfo->fP.X() << "," << pInfo->fP.Y() << "," << pInfo->fP.Z() << ") " << std::endl;
            double x{pInfo->fP.X()};
            double y{pInfo->fP.Y()};
            double z{pInfo->fP.Z()};
            double mass{pInfo->fMass};

            ke = (std::sqrt(x*x+ y*y + z*z));
            daughter_energies.push_back(ke);
            flavour.push_back(pInfo->fPID);
        }
    }  
    if(daughter_energies.size() == 2)
    {
        if (flavour[0] == flavour[1]) {
            ppflag = true;
        }
        auto index = std::distance(std::begin(daughter_energies), std::min_element(std::begin(daughter_energies), std::end(daughter_energies)));
        //std::cout << "index of smallest element: " <<  index << " " << daughter_energies[index] << std::endl;
        daughterKE = daughter_energies[index];
    }
}



