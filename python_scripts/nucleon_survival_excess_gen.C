#include <iostream>
#include <vector>
#include <map>
#include <string>

#include <chrono>

#include "NeutVect.h"
#include "NucleonNvectReader.h" // Assuming this is your custom class

TH1F* ratio_histo(TFile* file, double pb);
std::vector<std::pair<int, double>> events_generator2(TTree* t);

int nucleon_survival_excess() 
{
    auto start = std::chrono::high_resolution_clock::now();

    gStyle->SetOptStat(0);

    std::map<double, std::vector<TH1F*>> histo_dict;
    std::vector<double> pb_values = {0.0, 0.25, 0.5, 0.75, 1.0};

    for (double pb : pb_values) {
        std::string fil = "input_nuclroot_files/nucleon_pb" + std::to_string(pb) + "_1milevts.root";
        TFile* file = TFile::Open(fil.c_str());
        histo_dict[pb] = {ratio_histo(file, pb), nullptr}; // Initialize with ratio_histo and null init_histo
    }

    TH1F* clone_histo_0 = (TH1F*)histo_dict[0.0][0]->Clone();
    std::vector<TH1F*> plotlist;

    for (double pb : pb_values) {
        TH1F* clone_histo = (TH1F*)histo_dict[pb][0]->Clone();
        clone_histo->Divide(clone_histo_0);
        plotlist.push_back(clone_histo);
    }

    TH2F* ratioplots = new TH2F("pbvsKE", "pbvsKE", 15, 0., 800., pb_values.size(), 0, pb_values.size());

    for (size_t i = 0; i < plotlist.size(); ++i) {
        for (int j = 1; j <= plotlist[i]->GetNbinsX(); ++j) {
            ratioplots->Fill(plotlist[i]->GetBinCenter(j), i, plotlist[i]->GetBinContent(j));
        }
    }

    TFile* outfile = new TFile("nucleonsurvivalhistos_2_every10.root", "RECREATE");
    for (auto& pair : histo_dict) {
        pair.second[0]->Write(); // ratio_histo
        pair.second[1] = (TH1F*)pair.second[0]->Clone(std::string("initke_" + std::to_string(pair.first)).c_str());
        pair.second[1]->Reset();
    }
    for (double pb : pb_values){
        std::string fil = "input_nuclroot_files/nucleon_pb" + std::to_string(pb) + "_1milevts.root";
        TFile* file = TFile::Open(fil.c_str());
        TTree* t = (TTree*)file->Get("neuttree");
        std::vector<std::pair<int, double>> events = events_generator2(t);
        for(const auto& event : events){
            histo_dict[pb][1]->Fill(event.second);
        }
        histo_dict[pb][1]->Write();
        delete t;
        delete file;
    }

    ratioplots->Write();

    outfile->Close();

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
    std::cout << "--- " << duration.count() << " seconds ---" << std::endl;

    return 0;
}

TH1F* ratio_histo(TFile* file, double pb) {
    TTree* t = (TTree*)file->Get("neuttree");
    t->SetCacheSize(0);
    t->SetBranchStatus("*", 0);
    t->SetBranchStatus("vectorbranch", 1);

    std::string name = "surivial_histo_" + std::to_string(pb);
    TH1F* survival_histo = new TH1F(name.c_str(), "histo", 15, 0, 800);

    name = "initke_histo_" + std::to_string(pb);
    TH1F* initke_histo = new TH1F(name.c_str(), "histo", 15, 0, 800);

    std::vector<std::pair<int, double>> events = events_generator2(t);

    for (const auto& event : events) {
        initke_histo->Fill(event.second);
        if (event.first == 1) {
            survival_histo->Fill(event.second);
        }
    }

    name = "ratio_histo_" + std::to_string(pb);
    TH1F* ratio_histo_result = (TH1F*)survival_histo->Clone(name.c_str());
    ratio_histo_result->Divide(initke_histo);

    delete t;
    delete file;
    delete initke_histo;
    delete survival_histo;

    return ratio_histo_result;
}

std::vector<std::pair<int, double>> events_generator2(TTree* t) {
    NeutVect* nv = new NeutVect();
    t->SetBranchAddress("vectorbranch", nv);
    std::vector<std::pair<int, double>> results;

    for (Long64_t i = 0; i < t->GetEntries(); ++i) {
        t->GetEntry(i);
        if (i == 200000) {
            break;
        } else if (i % 10000 == 0) {
            std::cout << i << std::endl;
        }
        NucleonNvectReader nvt(*nv);
        std::pair<int, double> x = nvt.nucleon_survival();
        results.push_back(x);
    }
    delete nv;
    return results;
}