
#include <vector>
#include <cmath>

void nuiscomp_comparison_nu(){
    gStyle->SetOptStat(0);

    auto c1 = new TCanvas("opx","loooo",900,900);c1->SetGrid();
    TFile *data = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_1.0_to_1.0_nu.root");
    TH1D *neut6_PB = (TH1D*) data->Get("MINERvA_CC0pinp_STV_XSec_1Dpmu_nu_MC");
    neut6_PB->SetLineColor(1);
    neut6_PB->SetLineWidth(3);

    TFile *data2 = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_0.0_to_1.0_nu.root");
    TH1D *neut6_PB0 = (TH1D*) data2->Get("MINERvA_CC0pinp_STV_XSec_1Dpmu_nu_MC");
    neut6_PB0->SetLineColor(4);
    neut6_PB0->SetLineWidth(3);

    TFile *data3 = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_0.0_to_0.0_nu.root");
    TH1D *neut6_P = (TH1D*) data3->Get("MINERvA_CC0pinp_STV_XSec_1Dpmu_nu_MC");
    neut6_P->SetLineColor(2);
    neut6_P->SetLineWidth(3);

    double chiSquared{0.0};
    //chiSquared = chisquared(neut6_PB, neut6_PB0);  
    //std::cout << chiSquared << std::endl;
   
    auto legend = new TLegend(0.5,0.7,0.9,0.9);
    legend->SetHeader("Data Source","c"); 
    legend->AddEntry(neut6_PB0,"FSI PB 0.0 -> 1.0: reweight","l"); 
    legend->AddEntry(neut6_P,"FSI PB 0.0 -> 0.0: reweight","l"); 
    legend->AddEntry(neut6_PB,"FSI PB 1.0 -> 1.0: reweight","l"); 

    neut6_P->Draw();
    neut6_P->GetXaxis()->SetRange(1,30);
    neut6_PB0->GetXaxis()->SetTitle("muon KE [MeV]");
    neut6_PB->Draw("same");
    neut6_PB0->Draw("same");
    legend->Draw();
    //h_diff->Draw();
}



