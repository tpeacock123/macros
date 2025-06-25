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

TH1D* ratio_histo(int iterations,const char* file,std::string pb)
{
    clock_t clkStart;
    clock_t clkFinish;

    clkStart = clock();
    TFile *outputFile = TFile::Open(file);

    TH1D inEhisto("inEhisto","init KE hist", 20, 0, 800);
    TH1D survEhisto("survEhisto","survival KE hist", 20, 0, 800);

    TTree* t = (TTree*) outputFile->Get("neuttree");
    t->SetBranchStatus("*", 0);
    t->SetBranchStatus("vectorbranch", 1);
    NeutVect *nvect = NULL;
    TBranch *branch = t->GetBranch("vectorbranch");
    branch->SetAddress(&nvect);
    branch->SetAutoDelete(true);

    int start{00};
    for(int i = start; i < start+iterations; i++){
        if(i % 10000 == 0){
            std::cout << i << std::endl;
        }

        bool isAlive = false;
        double initKe{0.0};
        t->GetEntry(i);
 
        is_alive(nvect,isAlive,initKe);
        inEhisto.Fill(initKe);
        if (isAlive ==true){
            survEhisto.Fill(initKe);
        }

    }
    
    outputFile->Close();
    delete outputFile;
    inEhisto.Delete();
    survEhisto.Delete();

    std::stringstream ss;
    ss << "ratioHisto" << pb;
    std::string histName = ss.str();
    TH1D* ratioHisto = (TH1D*)survEhisto.Clone(histName.c_str());

    ratioHisto->Divide(&inEhisto);
    clkFinish= clock();
    std::cout << clkFinish - clkStart << std::endl;
    return ratioHisto;
}
