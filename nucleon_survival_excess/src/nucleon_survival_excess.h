#include <iostream>
#include <vector>
#include <map>
#include <string>

#include <chrono>

TH1F* ratio_histo(TFile* file, double pb);
std::vector<std::pair<int, double>> events_generator2(TTree* t);

int nucleon_survival_excess(); 