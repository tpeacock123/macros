
extern "C" {
  double GetScaleFactor(double fermiMomentum = 0.0, double kineticEnergy = 0.0);
}

double GetScaleFactor(double fermiMomentum = 0.0, double kineticEnergy = 0.0){
    TH1::AddDirectory(false);
    TFile *inputFile = TFile::Open("incomingKE_vs_outgoingKE_slices.root");
    TCanvas* weightCanv = (TCanvas*) inputFile->Get("pb_scale_values3");
    TH2D* weightHist = (TH2D*) weightCanv->GetListOfPrimitives()->FindObject("Weight_on_x-sec");

    return weightHist->Interpolate(125.0,181);
}

