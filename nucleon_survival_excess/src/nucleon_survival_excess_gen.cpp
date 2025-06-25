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
#include "neutvect.h"
#include "is_alive.h"


int main(){
    TH1::AddDirectory(false);

    std::string base_file_path = "../../input_nuclroot_files/nucleon_pb";
    std::string suffix = "_3milevts.root";
    TH1D *x = NULL;

    std::map<std::string, TH1D*> pbv {
        {"0.0", x},
        {"0.25",x}, 
        {"0.5",x}, 
        {"0.75",x}, 
        {"1.0",x}};

    std::map<std::string, TH1D*> ratio {
        {"0.0", x},        
        {"0.25", x},
        {"0.5",x}, 
        {"0.75",x}, 
        {"1.0",x}};
    //potentially just do this as a reference to pbv?

    for (auto& p : pbv)
    {

        std::stringstream ss;
        ss << base_file_path << p.first << suffix;
        std::string file_path = ss.str();

        const char* file = file_path.c_str();
        std::cout << file << std::endl;

        //file = "../../input_nuclroot_files/nucleon_pb1.0_1milevts.root";
        p.second = ratio_histo(2800000,file,p.first);
    }

    TH1D* clonePB0 = (TH1D*)pbv["0.0"]->Clone();
    for (auto& p : ratio)
    {
        TH1D* cloneHisto = (TH1D*)pbv[p.first]->Clone();
        cloneHisto->Divide(clonePB0);
        p.second = cloneHisto;
        std::cout << p.second->IsA() << std::endl;
    }

    TH2D ratioplots("pbvsKE","pbvsKE",20,0.,800.,pbv.size(),0,pbv.size());
    int bin = 0;
    for(auto& m : ratio)
    {
        for(auto l{1}; l <m.second->GetNbinsX()+1; l++){
            ratioplots.Fill(m.second->GetBinCenter(l),bin,(m.second->GetBinContent(l)));
        }
        bin +=1;
    }

    TFile* outputFile = TFile::Open("survhisto_700k.root", "recreate");
    //outputFile->cd();
    ratioplots.Write();
    for (auto& p : pbv)
    {
        p.second->Write();
        //ratio[p.first]->Write();
    }
    outputFile->Close();
    delete outputFile;

}

