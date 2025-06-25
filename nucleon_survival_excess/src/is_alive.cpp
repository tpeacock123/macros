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

void is_alive(NeutVect *nvect, bool &isAlive, double &initKe){
    int nPart = nvect->Npart();
        //std::cout << nvect->EventNo << std::endl;
        for (int particle=0;particle<nPart; particle++){
            auto pInfo = nvect->PartInfo(particle);
            if(particle == 0 && nvect->ParentIdx(particle) ==0 && (pInfo->fPID == abs(2212)))
            {
                //std::cout << particle << " " << pInfo->fIsAlive << " " << pInfo->fPID<< "  ("  << pInfo->fP.X() << "," << pInfo->fP.Y() << "," << pInfo->fP.Z() << ") "<< std::endl;
                double x{pInfo->fP.X()};
                double y{pInfo->fP.Y()};
                double z{pInfo->fP.Z()};
                double mass{pInfo->fMass};

                initKe = (std::sqrt(x*x+ y*y + z*z + mass*mass) - mass);
                //std::cout << initKe << std::endl;
            }
            if(nvect->ParentIdx(particle) ==2 && (pInfo->fPID == abs(2212)) && particle == 3)
            {
                //std::cout << particle << " " << pInfo->fIsAlive << " " << pInfo->fPID<< "  ("  << pInfo->fP.X() << "," << pInfo->fP.Y() << "," << pInfo->fP.Z() << ") "<< std::endl;
                if(pInfo->fIsAlive == 1)
                {
                    isAlive = true;
                }
            }
        }
}