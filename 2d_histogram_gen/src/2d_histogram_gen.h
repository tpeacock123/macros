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

void daughter_nuclei_energies(NeutVect *nvect, double &daughterKE, bool &ppflag);

void init_energies(NeutVect *nvect, double &initKe);