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

void is_alive(NeutVect *nvect, bool &isAlive, double &initKe);

TH1D* ratio_histo(int iterations,const char* file, std::string pb);





