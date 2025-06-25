#include <iostream>
#include <vector>
#include <map>
#include <string>

double GetScaleFactor(double fermiMomentum, double kineticEnergy){
    TH1::AddDirectory(false);
    TFile *inputFile = TFile::Open("incomingKEvsoutgoingKE_slices.root");
    TH2D* weightHisto = (TH2D*) inputFile->Get("pb_scale_values3")->GetListOfPrimitives()->FindObject("Weight_on_x-sec");

    return scaleFactor;
}